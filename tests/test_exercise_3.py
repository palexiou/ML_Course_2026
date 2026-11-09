"""Check Exercise 3 without downloading data during the test suite."""

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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "course_code"))
from exercise_1 import generate_dataset


class Exercise3Tests(unittest.TestCase):
    def test_official_test_is_preserved_and_only_training_is_fitted(self):
        path = Path(__file__).resolve().parents[1] / "exercise_3.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        dataset = generate_dataset().rename(columns={"sequence": "seq"})
        dataset["seq"] = dataset["seq"] + dataset["seq"] + dataset["seq"].str[:51]
        official_train = pd.concat([dataset.iloc[:450], dataset.iloc[-300:]]).reset_index(drop=True)
        official_test = pd.concat([dataset.iloc[450:500], dataset.iloc[10000:10050]]).reset_index(drop=True)
        official_test.loc[0, "seq"] = "N" + official_test.loc[0, "seq"][1:]
        namespace = {"__name__": "__main__"}
        vocabulary_fits = []
        model_fits = []
        original_vectorizer_fit = CountVectorizer.fit_transform
        original_model_fit = LogisticRegression.fit

        def record_vocabulary_fit(vectorizer, sequences, *args, **kwargs):
            vocabulary_fits.append(tuple(sequences))
            return original_vectorizer_fit(vectorizer, sequences, *args, **kwargs)

        def record_model_fit(model, counts, labels, *args, **kwargs):
            model_fits.append(tuple(labels.index))
            return original_model_fit(model, counts, labels, *args, **kwargs)

        with redirect_stdout(StringIO()), \
                patch.object(pd, "read_parquet", side_effect=[official_train.copy(), official_test.copy()]) as download, \
                patch.object(CountVectorizer, "fit_transform", record_vocabulary_fit), \
                patch.object(LogisticRegression, "fit", record_model_fit), \
                patch.object(plt, "show", side_effect=lambda: plt.close("all")):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code" and cell["id"] != "install":
                    if cell["id"] == "test-evaluation":
                        self.assertNotIn("test_probabilities", namespace)
                        self.assertNotIn("test_results", namespace)
                    exec(compile("".join(cell["source"]), str(path), "exec"), namespace)

        self.assertEqual(download.call_count, 2)
        self.assertIn("train-00000", download.call_args_list[0].args[0])
        self.assertIn("test-00000", download.call_args_list[1].args[0])
        train = namespace["train_data"]
        validation = namespace["validation_data"]
        self.assertEqual(train.label.value_counts().to_dict(), {1: 360, 0: 240})
        self.assertEqual(validation.label.value_counts().to_dict(), {1: 90, 0: 60})
        self.assertTrue(set(train.index).isdisjoint(validation.index))
        self.assertEqual(set(train.index) | set(validation.index), set(official_train.index))
        pd.testing.assert_frame_equal(namespace["test_data"], official_test.rename(columns={"seq": "sequence"}))
        self.assertEqual(vocabulary_fits, [tuple(train.sequence)] * 11)
        self.assertEqual(model_fits, [tuple(train.index)] * 11)
        np.testing.assert_allclose(namespace["example_probabilities"], namespace["validation_probabilities"][4])
        results = namespace["validation_results"]
        self.assertEqual(list(results.index), list(range(1, 11)))
        self.assertTrue(np.isfinite(results.to_numpy()).all())
        pd.testing.assert_series_equal(namespace["example_results"].loc[4], results.loc[4])
        self.assertEqual(namespace["best_k"], results.roc_auc.idxmax())
        self.assertEqual(list(namespace["test_results"].index), [namespace["best_k"]])


if __name__ == "__main__":
    unittest.main()
