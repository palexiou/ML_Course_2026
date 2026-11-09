"""Check probabilistic motifs, position distributions, and CNN training boundaries."""

from contextlib import chdir, redirect_stdout
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import log_loss, roc_auc_score


class Exercise8Tests(unittest.TestCase):
    def test_sampled_motifs_and_class_specific_positions(self):
        path = Path(__file__).resolve().parents[1] / "exercise_8.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__"}
        self.addCleanup(torch.set_num_threads, torch.get_num_threads())

        with TemporaryDirectory() as directory, chdir(directory), redirect_stdout(StringIO()), \
                patch.object(plt, "show", side_effect=lambda: plt.close("all")):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
                    if cell["id"] == "settings":
                        namespace["n_positive"] = 4_000
                        namespace["n_negative"] = 4_000
                        namespace["ofile"] = "custom directory/nested/positions.csv"
                    if cell["id"] == "check-save":
                        break
            dataset = namespace["dataset"].copy()
            pd.testing.assert_frame_equal(pd.read_csv(namespace["ofile"]), dataset)
            generation = next(cell for cell in notebook["cells"] if cell["id"] == "generate-data")
            exec(compile("".join(generation["source"]), str(path), "exec"), namespace)
            pd.testing.assert_frame_equal(namespace["dataset"], dataset)
            namespace["seed"] = 43
            exec(compile("".join(generation["source"]), str(path), "exec"), namespace)
            self.assertFalse(namespace["dataset"].equals(dataset))

        self.assertEqual(dataset.label.value_counts().to_dict(), {0: 4_000, 1: 4_000})
        self.assertTrue(dataset.sequence.str.fullmatch("[ACGT]{1000}").all())
        self.assertTrue(dataset.sequence.is_unique)
        np.testing.assert_array_equal(dataset.offset, dataset.tata_start - dataset.atg_start)
        np.testing.assert_array_equal(dataset.atg_start, dataset.motif_a_start + 6)
        np.testing.assert_array_equal(dataset.tata_start, dataset.motif_b_start + 1)

        background_counts = dict.fromkeys("ACGT", 0)
        for i, row in enumerate(dataset.itertuples(index=False)):
            self.assertTrue(0 <= row.motif_a_start <= 990)
            self.assertTrue(0 <= row.motif_b_start <= 990)
            self.assertTrue(row.motif_b_start + 10 <= row.motif_a_start
                            or row.motif_b_start >= row.motif_a_start + 10)
            self.assertEqual(row.sequence[row.motif_a_start:row.motif_a_start + 10], row.motif_a_instance)
            self.assertEqual(row.sequence[row.motif_b_start:row.motif_b_start + 10], row.motif_b_instance)
            if i < 200:
                left, right = sorted([row.motif_a_start, row.motif_b_start])
                background = row.sequence[:left] + row.sequence[left + 10:right] + row.sequence[right + 10:]
                for base in "ACGT":
                    background_counts[base] += background.count(base)
        for count in background_counts.values():
            self.assertAlmostEqual(count / (200 * 980), 0.25, delta=0.01)

        for motif, consensus in (("a", "GCCACCATGG"), ("b", "CTATAAAGGC")):
            probabilities = namespace[f"motif_{motif}_probabilities"]
            np.testing.assert_allclose(probabilities.sum(axis=0), 1)
            np.testing.assert_allclose(namespace[f"motif_{motif}_pwm"], np.log2(probabilities / 0.25))
            self.assertEqual("".join(namespace["bases"][probabilities.argmax(axis=0)]), consensus)
            self.assertGreater(dataset[f"motif_{motif}_instance"].nunique(), 100)
            samples = np.array([list(instance) for instance in dataset[f"motif_{motif}_instance"]])
            observed = np.array([(samples == base).mean(axis=0) for base in "ACGT"])
            np.testing.assert_allclose(observed, probabilities, atol=0.015, rtol=0)
        np.testing.assert_allclose(namespace["motif_a_probabilities"][[0, 3, 2], [6, 7, 8]], 0.999)
        np.testing.assert_allclose(namespace["motif_b_probabilities"][[3, 0, 3, 0, 0, 0], range(1, 7)], 0.97)

        values = namespace["offset_values"]
        probabilities = namespace["offset_probabilities"]
        self.assertEqual(values[probabilities.argmax()], -50)
        self.assertAlmostEqual(probabilities.sum(), 1)
        peak = probabilities[values == -50][0]
        for offset in (-70, -42):
            self.assertAlmostEqual(probabilities[values == offset][0] / peak, np.exp(-0.5))
        positive = dataset[dataset.label == 1]
        self.assertTrue(positive.offset.between(-100, -30).all())
        observed_cdf = np.searchsorted(np.sort(positive.offset), values, side="right") / len(positive)
        self.assertLess(np.max(np.abs(observed_cdf - probabilities.cumsum())), 0.04)
        self.assertAlmostEqual(positive.offset.mean(), np.sum(values * probabilities), delta=1.0)

        negative = dataset[dataset.label == 0]
        self.assertTrue(negative.offset.gt(0).any())
        self.assertGreater(negative.offset.between(-100, -30).mean(), 0.04)
        self.assertLess(negative.offset.between(-100, -30).mean(), 0.11)
        # Rank B within its valid starts to test conditional uniformity, including edge cases.
        forbidden_low = np.maximum(0, negative.motif_a_start.to_numpy() - 9)
        forbidden_high = np.minimum(990, negative.motif_a_start.to_numpy() + 9)
        forbidden_count = forbidden_high - forbidden_low + 1
        b_starts = negative.motif_b_start.to_numpy()
        ranks = b_starts - np.where(b_starts > forbidden_high, forbidden_count, 0)
        uniform_quantiles = np.sort((ranks + 0.5) / (991 - forbidden_count))
        expected_quantiles = (np.arange(len(negative)) + 0.5) / len(negative)
        self.assertLess(np.max(np.abs(uniform_quantiles - expected_quantiles)), 0.04)
        for _, group in dataset.groupby("label"):
            self.assertTrue(group.atg_start.between(101, 996).all())
            quantiles = np.sort((group.atg_start.to_numpy() - 101 + 0.5) / 896)
            self.assertLess(np.max(np.abs(quantiles - expected_quantiles)), 0.04)

    def test_cnn_uses_sequences_and_selects_weights_without_test_data(self):
        path = Path(__file__).resolve().parents[1] / "exercise_8.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__"}
        self.addCleanup(torch.set_num_threads, torch.get_num_threads())
        optimizer_steps = []
        original_step = torch.optim.Adam.step

        def record_step(optimizer, *args, **kwargs):
            gradients = [p.grad for group in optimizer.param_groups for p in group["params"] if p.requires_grad]
            self.assertTrue(all(gradient is not None and torch.isfinite(gradient).all() for gradient in gradients))
            optimizer_steps.append(1)
            return original_step(optimizer, *args, **kwargs)

        def check_evaluation_gradients(model, inputs):
            if not model.training:
                self.assertFalse(torch.is_grad_enabled())

        with TemporaryDirectory() as directory, chdir(directory), redirect_stdout(StringIO()), \
                patch.object(plt, "show", side_effect=lambda: plt.close("all")), \
                patch.object(torch.optim.Adam, "step", record_step):
            for cell in notebook["cells"]:
                if cell["cell_type"] != "code":
                    continue
                if cell["id"] == "test-evaluation":
                    for name in ("x_test", "y_test", "test_probabilities", "test_results"):
                        self.assertNotIn(name, namespace)
                exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
                if cell["id"] == "settings":
                    namespace["n_positive"] = 400
                    namespace["n_negative"] = 400
                    namespace["max_epochs"] = 3
                    namespace["device"] = torch.device("cpu")
                if cell["id"] == "build-cnn":
                    initial_state = {name: value.clone() for name, value in namespace["cnn"].state_dict().items()}
                    namespace["cnn"].register_forward_pre_hook(check_evaluation_gradients)
                    self.assertFalse(any(p.requires_grad for p in namespace["motif_scanner"].parameters()))
                    examples = ["GCCACCATGG", "CTATAAAGGC"]
                    with torch.no_grad():
                        scores = namespace["motif_scanner"](namespace["encode_sequences"](examples))
                    for i, sequence in enumerate(examples):
                        ids = ["ACGT".index(base) for base in sequence]
                        for j, motif in enumerate(("a", "b")):
                            expected = namespace[f"motif_{motif}_pwm"][ids, range(10)].sum() / 10 - 0.6
                            self.assertAlmostEqual(scores[i, j, 0].item(), expected, places=5)

        train, validation, test = [namespace[name] for name in ("train_data", "validation_data", "test_data")]
        self.assertEqual([len(split) for split in (train, validation, test)], [560, 160, 80])
        self.assertTrue(set(train.index).isdisjoint(validation.index))
        self.assertTrue(set(train.index).isdisjoint(test.index))
        self.assertTrue(set(validation.index).isdisjoint(test.index))
        self.assertEqual(set(train.index) | set(validation.index) | set(test.index), set(namespace["dataset"].index))
        for split, tensor_name in ((train, "x_train"), (validation, "x_validation"), (test, "x_test")):
            self.assertEqual(split.label.value_counts().to_dict(), {0: len(split) // 2, 1: len(split) // 2})
            tensor = namespace[tensor_name].cpu()
            self.assertEqual(tuple(tensor.shape), (len(split), 4, 1000))
            torch.testing.assert_close(tensor.sum(dim=1), torch.ones((len(split), 1000)))
            decoded = np.array(list("ACGT"))[tensor.argmax(dim=1).numpy()]
            self.assertEqual(["".join(row) for row in decoded], split.sequence.tolist())
        self.assertEqual(len(optimizer_steps), len(namespace["train_loader"]) * namespace["max_epochs"])
        self.assertTrue(any(not torch.equal(initial_state[name], value) for name, value in namespace["cnn"].state_dict().items()))
        for name in ("0.weight", "0.bias"):
            torch.testing.assert_close(namespace["cnn"].state_dict()[name], initial_state[name], rtol=0, atol=0)
        self.assertEqual(namespace["best_epoch"], int(np.argmin(namespace["validation_losses"])) + 1)
        for name, value in namespace["cnn"].state_dict().items():
            torch.testing.assert_close(value, namespace["best_state"][name], rtol=0, atol=0)
        self.assertAlmostEqual(namespace["validation_results"]["log_loss"], min(namespace["validation_losses"]), places=5)
        for split in ("validation", "test"):
            results = namespace[f"{split}_results"]
            scores = namespace[f"{split}_probabilities"]
            labels = namespace[f"y_{split}"]
            self.assertEqual(len(results), 8)
            self.assertTrue(np.isfinite(results).all())
            self.assertTrue(((scores >= 0) & (scores <= 1)).all())
            self.assertAlmostEqual(results["roc_auc"], roc_auc_score(labels, scores))
            self.assertAlmostEqual(results["log_loss"], log_loss(labels, scores))
