"""Check the pair-grid representation and 2D CNN's held-out evaluation."""

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


class Exercise10Tests(unittest.TestCase):
    def test_pair_channels_learning_and_final_test_download(self):
        path = Path(__file__).resolve().parents[1] / "exercise_10.ipynb"
        notebook = json.loads(path.read_text())
        rng = np.random.default_rng(8)
        fixture = pd.DataFrame({
            "noncodingRNA": ["".join(rng.choice(list("ACGT"), size=int(rng.integers(17, 27))))
                             for _ in range(240)],
            "gene": ["".join(row) for row in rng.choice(list("ACGT"), size=(240, 50))],
            "label": [0, 1] * 120,
            "Nunique": [0, 1000] * 120,
        })
        official_train = fixture.iloc[:200].reset_index(drop=True)
        official_test = fixture.iloc[200:].reset_index(drop=True)
        namespace = {"__name__": "__main__"}
        self.addCleanup(torch.set_num_threads, torch.get_num_threads())
        original_step = torch.optim.Adam.step
        optimizer_steps = []
        downloads = []

        def load_data(url, **kwargs):
            downloads.append(url)
            self.assertEqual(kwargs["sep"], "\t")
            self.assertEqual(kwargs["compression"], "gzip")
            self.assertEqual(set(kwargs["usecols"]), {"noncodingRNA", "gene", "label"})
            if "_train.tsv" in url:
                data = official_train
            else:
                self.assertEqual(cell["id"], "test-evaluation")
                self.assertIn("best_state", namespace)
                self.assertIn("validation_results", namespace)
                data = official_test
            return data[kwargs["usecols"]].copy()

        def record_step(optimizer, *args, **kwargs):
            for group in optimizer.param_groups:
                for parameter in group["params"]:
                    self.assertTrue(parameter.requires_grad)
                    self.assertIsNotNone(parameter.grad)
                    self.assertTrue(torch.isfinite(parameter.grad).all())
            for layer in (namespace["cnn"][0], namespace["cnn"][3]):
                self.assertGreater(layer.weight.grad.norm().item(), 0)
            optimizer_steps.append(1)
            return original_step(optimizer, *args, **kwargs)

        def check_model_inputs(model, inputs):
            encoded = inputs[0]
            self.assertEqual(tuple(encoded.shape[1:]), (17, 28, 50))
            torch.testing.assert_close(encoded.sum(dim=1), torch.ones_like(encoded[:, 0]))
            if model.training:
                for row in encoded.argmax(dim=1).byte().cpu().numpy():
                    self.assertIn(row.tobytes(), training_rows)
            else:
                self.assertFalse(torch.is_grad_enabled())

        with TemporaryDirectory() as directory:
            with chdir(directory), redirect_stdout(StringIO()), \
                    patch.object(pd, "read_csv", side_effect=load_data), \
                    patch.object(torch.optim.Adam, "step", record_step), \
                    patch.object(plt, "show", side_effect=lambda: plt.close("all")):
                for cell in notebook["cells"]:
                    if cell["cell_type"] != "code":
                        continue
                    if cell["id"] == "test-evaluation":
                        for name in ("test_data", "test_codes", "y_test", "test_probabilities", "test_results"):
                            self.assertNotIn(name, namespace)
                    exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
                    if cell["id"] == "settings":
                        namespace["max_epochs"] = 3
                        namespace["batch_size"] = 32
                        namespace["device"] = torch.device("cpu")
                    if cell["id"] == "encode-pairs":
                        training_rows = {row.numpy().tobytes() for row in namespace["train_codes"]}
                    if cell["id"] == "build-cnn":
                        model = namespace["cnn"]
                        self.assertEqual(sum(isinstance(layer, torch.nn.Conv2d) for layer in model), 2)
                        initial_state = {name: value.clone() for name, value in model.state_dict().items()}
                        model.register_forward_pre_hook(check_model_inputs)

            self.assertEqual(len(downloads), 2)
            self.assertIn("20540907", downloads[0])
            self.assertIn("_test.tsv", downloads[1])
            expected_validation = official_train.groupby("label").sample(frac=0.20, random_state=42)
            pd.testing.assert_frame_equal(namespace["validation_data"], expected_validation[namespace["input_columns"]])
            pd.testing.assert_frame_equal(
                namespace["train_data"], official_train.drop(expected_validation.index)[namespace["input_columns"]]
            )
            pd.testing.assert_frame_equal(namespace["test_data"], official_test[namespace["input_columns"]])
            self.assertEqual(len(optimizer_steps), len(namespace["train_loader"]) * 3)
            self.assertEqual(namespace["best_epoch"], int(np.argmin(namespace["validation_losses"])) + 1)
            for name, value in namespace["cnn"].state_dict().items():
                torch.testing.assert_close(value, namespace["best_state"][name], rtol=0, atol=0)
            for name in ("0.weight", "3.weight", "7.weight"):
                self.assertFalse(torch.equal(initial_state[name], namespace["cnn"].state_dict()[name]))
            self.assertAlmostEqual(namespace["validation_results"]["log_loss"], min(namespace["validation_losses"]), places=5)
            for split in ("validation", "test"):
                labels = namespace[f"y_{split}"]
                probabilities = namespace[f"{split}_probabilities"]
                results = namespace[f"{split}_results"]
                self.assertEqual(len(results), 8)
                self.assertTrue(np.isfinite(results).all())
                self.assertAlmostEqual(results["roc_auc"], roc_auc_score(labels, probabilities))
                self.assertAlmostEqual(results["log_loss"], log_loss(labels, probabilities))
                output = Path(directory) / namespace["output_dir"]
                predictions = pd.read_csv(output / f"{split}_predictions.csv")
                answers = pd.read_csv(output / f"{split}_answers.csv")
                self.assertEqual(list(predictions.columns), ["sample_id", "probability"])
                self.assertEqual(list(answers.columns), ["sample_id", "label"])
                self.assertTrue(predictions.sample_id.is_unique)
                self.assertEqual(predictions.sample_id.tolist(), answers.sample_id.tolist())
                np.testing.assert_allclose(predictions.probability, probabilities)
                np.testing.assert_array_equal(answers.label, labels)

        # Every ordered nucleotide pair has its own channel; padding has a separate channel.
        example = pd.DataFrame({"noncodingRNA": ["ACGT"], "gene": ["ACGT" * 12 + "AC"]})
        codes = namespace["encode_pairs"](example)
        self.assertEqual(codes.dtype, torch.uint8)
        np.testing.assert_array_equal(codes[0, :4, :4].numpy(), np.arange(16).reshape(4, 4))
        self.assertTrue(torch.all(codes[0, 4:] == 16))
        encoded = namespace["one_hot_pairs"](codes)
        self.assertEqual(tuple(encoded.shape), (1, 17, 28, 50))
        torch.testing.assert_close(encoded.sum(dim=1), torch.ones((1, 28, 50)))
        self.assertTrue(torch.all(encoded[0, :16, 4:] == 0))
        self.assertTrue(torch.all(encoded[0, 16, 4:] == 1))
        for mirna, target in (("A" * 29, "A" * 50), ("AC", "A" * 49), ("", "A" * 50)):
            with self.assertRaises(ValueError):
                namespace["encode_pairs"](pd.DataFrame({"noncodingRNA": [mirna], "gene": [target]}))
