"""Check the k=7 cap and run the tree comparison on a smaller dataset."""

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
from sklearn.feature_extraction.text import CountVectorizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exercise_1 import generate_dataset


class Exercise4Tests(unittest.TestCase):
    def test_only_k_one_to_seven_are_compared(self):
        path = Path(__file__).resolve().parents[1] / "exercise_4.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        dataset = generate_dataset()
        small_dataset = pd.concat([dataset.head(300), dataset.tail(300)])
        namespace = {"__name__": "__main__"}
        fitted_ranges = []
        visible_axes = []
        original_fit = CountVectorizer.fit_transform

        def record_fit(vectorizer, sequences, *args, **kwargs):
            fitted_ranges.append(vectorizer.ngram_range)
            return original_fit(vectorizer, sequences, *args, **kwargs)

        def close_plot():
            visible_axes.append(sum(ax.get_visible() for ax in plt.gcf().axes))
            plt.close("all")

        with TemporaryDirectory() as directory, chdir(directory), redirect_stdout(StringIO()):
            Path("exercise_1_output").mkdir()
            small_dataset.to_csv("exercise_1_output/dataset.csv", index=False)
            with patch.object(CountVectorizer, "fit_transform", record_fit), patch.object(plt, "show", close_plot):
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        if cell["id"] == "test-evaluation":
                            self.assertNotIn("test_probabilities", namespace)
                            self.assertNotIn("test_results", namespace)
                        exec(compile("".join(cell["source"]), str(path), "exec"), namespace)

        self.assertEqual(fitted_ranges, [(4, 4)] + [(k, k) for k in range(1, 8)])
        self.assertEqual(visible_axes, [6, 1, 4, 7, 7, 6])
        results = namespace["validation_results"]
        self.assertEqual(len(results), 14)
        self.assertTrue(np.isfinite(results.to_numpy()).all())
        for name in ("Decision tree", "Random forest"):
            self.assertEqual(list(results.loc[name].index), list(range(1, 8)))
            np.testing.assert_allclose(namespace["example_probabilities"][name], namespace["validation_probabilities"][name][4])
            pd.testing.assert_series_equal(namespace["example_results"].loc[(name, 4)], results.loc[(name, 4)])
            self.assertEqual(namespace["best_k"][name], results.loc[name].roc_auc.idxmax())
            self.assertEqual(len(namespace["test_probabilities"][name]), 60)
        self.assertEqual(len(namespace["test_results"]), 2)
