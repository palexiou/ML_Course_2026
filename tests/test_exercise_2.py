"""Run the teaching notebook on a smaller dataset and check its split boundaries."""

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
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exercise_1 import generate_dataset


class Exercise2Tests(unittest.TestCase):
    def test_walkthrough_comparison_and_held_out_test(self):
        path = Path(__file__).resolve().parents[1] / "exercise_2.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        dataset = generate_dataset()
        small_dataset = pd.concat([dataset.head(300), dataset.tail(300)])
        namespace = {"__name__": "__main__"}
        vocabulary_fits = []
        model_fits = []
        original_vectorizer_fit = CountVectorizer.fit_transform
        original_model_fit = LogisticRegression.fit

        def record_vocabulary_fit(vectorizer, sequences, *args, **kwargs):
            vocabulary_fits.append(set(sequences.index))
            return original_vectorizer_fit(vectorizer, sequences, *args, **kwargs)

        def record_model_fit(model, counts, labels, *args, **kwargs):
            model_fits.append(set(labels.index))
            return original_model_fit(model, counts, labels, *args, **kwargs)

        with TemporaryDirectory() as directory, chdir(directory), redirect_stdout(StringIO()):
            Path("exercise_1_output").mkdir()
            small_dataset.to_csv("exercise_1_output/dataset.csv", index=False)
            with patch.object(CountVectorizer, "fit_transform", record_vocabulary_fit), \
                    patch.object(LogisticRegression, "fit", record_model_fit), \
                    patch.object(plt, "show", side_effect=lambda: plt.close("all")):
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        if cell["id"] == "test-evaluation":
                            self.assertNotIn("test_probabilities", namespace)
                            self.assertNotIn("test_results", namespace)
                        exec(compile("".join(cell["source"]), str(path), "exec"), namespace)

        train = namespace["train_data"]
        validation = namespace["validation_data"]
        test = namespace["test_data"]
        self.assertEqual((len(train), len(validation), len(test)), (420, 120, 60))
        self.assertTrue(set(train.index).isdisjoint(validation.index))
        self.assertTrue(set(train.index).isdisjoint(test.index))
        self.assertTrue(set(validation.index).isdisjoint(test.index))
        self.assertEqual(set(train.index) | set(validation.index) | set(test.index), set(range(600)))
        for split in (train, validation, test):
            self.assertEqual(split.label.mean(), 0.5)
        self.assertEqual(vocabulary_fits, [set(train.index)] * 11)
        self.assertEqual(model_fits, [set(train.index)] * 11)
        self.assertEqual(namespace["windows"], ["AC", "CA", "AC", "CA", "AC"])
        results = namespace["validation_results"]
        self.assertEqual(list(results.index), list(range(1, 11)))
        self.assertTrue(np.isfinite(results.to_numpy()).all())
        np.testing.assert_allclose(namespace["example_probabilities"], namespace["validation_probabilities"][4])
        pd.testing.assert_series_equal(namespace["example_results"].loc[4], results.loc[4])
        self.assertEqual(namespace["best_k"], results.roc_auc.idxmax())
        self.assertEqual(list(namespace["test_results"].index), [namespace["best_k"]])


if __name__ == "__main__":
    unittest.main()
