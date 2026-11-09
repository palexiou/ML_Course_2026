"""Run the boosting notebook on a small balanced dataset."""

from contextlib import chdir, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import log_loss

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exercise_1 import generate_dataset


class Exercise5Tests(unittest.TestCase):
    def test_validation_selects_boosting_round_before_test_evaluation(self):
        path = Path(__file__).resolve().parents[1] / "exercise_5.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        dataset = generate_dataset()
        small_dataset = pd.concat([dataset.head(100), dataset.tail(100)])
        namespace = {"__name__": "__main__"}
        visible_axes = []

        def close_plot():
            visible_axes.append(sum(ax.get_visible() for ax in plt.gcf().axes))
            plt.close("all")

        with TemporaryDirectory() as directory, chdir(directory), redirect_stdout(StringIO()):
            Path("exercise_1_output").mkdir()
            small_dataset.to_csv("exercise_1_output/dataset.csv", index=False)
            with patch.object(plt, "show", close_plot):
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        if cell["id"] == "test-evaluation":
                            self.assertNotIn("x_test", namespace)
                            self.assertNotIn("test_probabilities", namespace)
                            self.assertNotIn("test_results", namespace)
                        exec(compile("".join(cell["source"]), str(path), "exec"), namespace)

        self.assertEqual(visible_axes, [1, 9, 3])
        self.assertEqual([len(namespace[name]) for name in ("train_data", "validation_data", "test_data")], [140, 40, 20])
        self.assertEqual(namespace["x_train"].shape[1], 256)
        np.testing.assert_array_equal(np.asarray(namespace["x_train"].sum(axis=1)).ravel(), 97)
        self.assertEqual(len(namespace["validation_losses"]), namespace["max_trees"])
        self.assertTrue(np.isfinite(namespace["training_losses"]).all())
        self.assertTrue(np.isfinite(namespace["validation_losses"]).all())
        selected = namespace["best_n_trees"]
        self.assertEqual(selected, int(np.argmin(namespace["validation_losses"])) + 1)
        selected_model = namespace["models"]["Gradient boosting"]
        self.assertEqual(selected_model.n_estimators_, selected)
        for round_number, probabilities in enumerate(namespace["boosting_model"].staged_predict_proba(namespace["x_validation"]), start=1):
            if round_number == selected:
                np.testing.assert_allclose(probabilities[:, 1], namespace["validation_probabilities"]["Gradient boosting"])
                break
        self.assertAlmostEqual(log_loss(namespace["y_validation"], namespace["validation_probabilities"]["Gradient boosting"]), min(namespace["validation_losses"]))
        self.assertEqual(namespace["validation_results"].shape, (3, 8))
        self.assertTrue(np.isfinite(namespace["validation_results"].to_numpy()).all())
        self.assertEqual(list(namespace["test_results"].index), ["Gradient boosting"])
        self.assertEqual(len(namespace["test_probabilities"]), 20)
        self.assertTrue(np.isfinite(namespace["test_results"].to_numpy()).all())
