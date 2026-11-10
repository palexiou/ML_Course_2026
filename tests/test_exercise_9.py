"""Check learned convolutions and benchmark split boundaries without a download."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.metrics import log_loss, roc_auc_score


class Exercise9Tests(unittest.TestCase):
    def test_convolutions_learn_without_training_on_validation_or_test(self):
        path = Path(__file__).resolve().parents[1] / "exercise_9.ipynb"
        notebook = json.loads(path.read_text())
        rng = np.random.default_rng(7)
        sequences = ["".join(row) for row in rng.choice(list("ACGT"), size=(290, 251))]
        official_train = pd.DataFrame({"seq": sequences[:250], "label": [1] * 150 + [0] * 100})
        official_test = pd.DataFrame({"seq": sequences[250:], "label": [1] * 20 + [0] * 20})
        official_test.loc[0, "seq"] = "N" + official_test.loc[0, "seq"][1:]
        namespace = {"__name__": "__main__"}
        self.addCleanup(torch.set_num_threads, torch.get_num_threads())
        original_step = torch.optim.Adam.step
        optimizer_steps = []

        def record_step(optimizer, *args, **kwargs):
            parameters = [p for group in optimizer.param_groups for p in group["params"]]
            self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all() for p in parameters))
            for layer in (namespace["cnn"][0], namespace["cnn"][3]):
                self.assertGreater(layer.weight.grad.norm().item(), 0)
            optimizer_steps.append(1)
            return original_step(optimizer, *args, **kwargs)

        def check_model_inputs(model, inputs):
            if model.training:
                for row in inputs[0].detach().cpu().numpy():
                    self.assertIn(row.tobytes(), training_rows)
            else:
                self.assertFalse(torch.is_grad_enabled())

        with redirect_stdout(StringIO()), \
                patch.object(pd, "read_parquet", side_effect=[official_train.copy(), official_test.copy()]) as download, \
                patch.object(torch.optim.Adam, "step", record_step), \
                patch.object(plt, "show", side_effect=lambda: plt.close("all")):
            for cell in notebook["cells"]:
                if cell["cell_type"] != "code" or cell["id"] == "install":
                    continue
                if cell["id"] == "test-evaluation":
                    for name in ("x_test", "y_test", "test_loader", "test_probabilities", "test_results"):
                        self.assertNotIn(name, namespace)
                exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
                if cell["id"] == "settings":
                    namespace["max_epochs"] = 3
                    namespace["batch_size"] = 32
                    namespace["device"] = torch.device("cpu")
                if cell["id"] == "encode-sequences":
                    training_rows = {row.numpy().tobytes() for row in namespace["x_train"]}
                if cell["id"] == "build-cnn":
                    model = namespace["cnn"]
                    self.assertTrue(all(p.requires_grad for p in model.parameters()))
                    initial_state = {name: value.clone() for name, value in model.state_dict().items()}
                    self.assertEqual(
                        {id(p) for p in model.parameters()},
                        {id(p) for group in namespace["optimizer"].param_groups for p in group["params"]},
                    )
                    model.register_forward_pre_hook(check_model_inputs)

        self.assertEqual(download.call_count, 2)
        self.assertIn("e0003669df0a180c8570ebe091ed91f20fa080ec", namespace["data_url"])
        self.assertIn("train-00000", download.call_args_list[0].args[0])
        self.assertIn("test-00000", download.call_args_list[1].args[0])
        expected_validation = official_train.groupby("label").sample(frac=0.20, random_state=42)
        pd.testing.assert_frame_equal(
            namespace["validation_data"], expected_validation.rename(columns={"seq": "sequence"})
        )
        pd.testing.assert_frame_equal(
            namespace["train_data"], official_train.drop(expected_validation.index).rename(columns={"seq": "sequence"})
        )
        pd.testing.assert_frame_equal(namespace["test_data"], official_test.rename(columns={"seq": "sequence"}))
        for split in ("train", "validation", "test"):
            data = namespace[f"{split}_data"]
            encoded = namespace[f"x_{split}"].cpu()
            self.assertEqual(tuple(encoded.shape), (len(data), 4, 251))
            self.assertEqual(encoded.dtype, torch.float32)
            self.assertTrue(torch.isfinite(encoded).all())
            decoded = np.array(list("ACGT"))[encoded.argmax(dim=1).numpy()]
            decoded[encoded.sum(dim=1).numpy() == 0] = "N"
            self.assertEqual(["".join(row) for row in decoded], data.sequence.tolist())
        torch.testing.assert_close(namespace["x_test"][0, :, 0], torch.zeros(4))
        self.assertEqual(len(optimizer_steps), len(namespace["train_loader"]) * 3)
        self.assertEqual(namespace["best_epoch"], int(np.argmin(namespace["validation_losses"])) + 1)
        for name, value in namespace["cnn"].state_dict().items():
            torch.testing.assert_close(value, namespace["best_state"][name], rtol=0, atol=0)
        for name in ("0.weight", "3.weight"):
            self.assertFalse(torch.equal(initial_state[name], namespace["cnn"].state_dict()[name]))
        self.assertTrue(torch.all(namespace["filter_changes"] > 0))
        self.assertAlmostEqual(namespace["validation_results"]["log_loss"], min(namespace["validation_losses"]), places=5)
        for split in ("validation", "test"):
            results = namespace[f"{split}_results"]
            labels = namespace[f"y_{split}"]
            probabilities = namespace[f"{split}_probabilities"]
            self.assertEqual(len(results), 8)
            self.assertTrue(np.isfinite(results).all())
            self.assertAlmostEqual(results["roc_auc"], roc_auc_score(labels, probabilities))
            self.assertAlmostEqual(results["log_loss"], log_loss(labels, probabilities))
        self.assertFalse(namespace["cnn"].training)
