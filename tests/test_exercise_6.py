"""Check the three-model comparison without downloading the benchmark."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exercise_1 import generate_dataset


class Exercise6Tests(unittest.TestCase):
    def test_models_share_training_counts_and_preserve_official_test(self):
        path = Path(__file__).resolve().parents[1] / "exercise_6.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        dataset = generate_dataset().rename(columns={"sequence": "seq"})
        dataset["seq"] = dataset["seq"] + dataset["seq"] + dataset["seq"].str[:51]
        official_train = pd.concat([dataset.iloc[:150], dataset.iloc[-100:]]).reset_index(drop=True)
        official_test = pd.concat([dataset.iloc[150:170], dataset.iloc[10000:10020]]).reset_index(drop=True)
        official_test.loc[0, "seq"] = "N" + official_test.loc[0, "seq"][1:]
        namespace = {"__name__": "__main__"}
        vocabulary_fits = []
        model_fits = []
        visible_axes = []
        original_vectorizer_fit = CountVectorizer.fit_transform

        def record_vocabulary_fit(vectorizer, sequences, *args, **kwargs):
            vocabulary_fits.append((vectorizer.ngram_range, tuple(sequences)))
            return original_vectorizer_fit(vectorizer, sequences, *args, **kwargs)

        def record_fit(original_fit):
            def fit(model, counts, labels, *args, **kwargs):
                model_fits.append((id(counts), tuple(labels.index)))
                return original_fit(model, counts, labels, *args, **kwargs)
            return fit

        def close_plot():
            visible_axes.append(sum(ax.get_visible() for ax in plt.gcf().axes))
            plt.close("all")

        with redirect_stdout(StringIO()), \
                patch.object(pd, "read_parquet", side_effect=[official_train.copy(), official_test.copy()]) as download, \
                patch.object(CountVectorizer, "fit_transform", record_vocabulary_fit), \
                patch.object(LogisticRegression, "fit", record_fit(LogisticRegression.fit)), \
                patch.object(RandomForestClassifier, "fit", record_fit(RandomForestClassifier.fit)), \
                patch.object(GradientBoostingClassifier, "fit", record_fit(GradientBoostingClassifier.fit)), \
                patch.object(plt, "show", close_plot):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code" and cell["id"] != "install":
                    if cell["id"] == "test-evaluation":
                        self.assertNotIn("x_test", namespace)
                        self.assertNotIn("test_probabilities", namespace)
                        self.assertNotIn("test_results", namespace)
                    exec(compile("".join(cell["source"]), str(path), "exec"), namespace)

        self.assertEqual(download.call_count, 2)
        self.assertIn("train-00000", download.call_args_list[0].args[0])
        self.assertIn("test-00000", download.call_args_list[1].args[0])
        train = namespace["train_data"]
        validation = namespace["validation_data"]
        self.assertEqual(train.label.value_counts().to_dict(), {1: 120, 0: 80})
        self.assertEqual(validation.label.value_counts().to_dict(), {1: 30, 0: 20})
        self.assertTrue(set(train.index).isdisjoint(validation.index))
        self.assertEqual(set(train.index) | set(validation.index), set(official_train.index))
        pd.testing.assert_frame_equal(namespace["test_data"], official_test.rename(columns={"seq": "sequence"}))
        self.assertEqual(vocabulary_fits, [((6, 6), tuple(train.sequence))])
        self.assertEqual(model_fits, [(id(namespace["x_train"]), tuple(train.index))] * 3)
        np.testing.assert_array_equal(np.asarray(namespace["x_train"].sum(axis=1)).ravel(), 246)
        self.assertLessEqual(namespace["x_train"].shape[1], 4096)
        self.assertEqual(visible_axes, [2, 3, 2, 3])
        names = ["Logistic regression", "Random forest", "Gradient boosting"]
        self.assertEqual(list(namespace["models"]), names)
        for split in ("validation", "test"):
            results = namespace[f"{split}_results"]
            self.assertEqual(list(results.index), names)
            self.assertEqual(results.shape, (3, 8))
            self.assertTrue(np.isfinite(results.to_numpy()).all())
            for name in names:
                probabilities = namespace[f"{split}_probabilities"][name]
                labels = namespace[f"y_{split}"]
                self.assertEqual(len(probabilities), len(labels))
                self.assertAlmostEqual(results.loc[name, "roc_auc"], roc_auc_score(labels, probabilities))
                self.assertAlmostEqual(results.loc[name, "log_loss"], log_loss(labels, probabilities))
