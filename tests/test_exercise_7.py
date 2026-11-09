"""Check motif XOR, grouped splits, and the learned nonlinear classifier."""

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
from scipy.sparse import issparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import Perceptron
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.neural_network import MLPClassifier
from threadpoolctl import threadpool_limits


class Exercise7Tests(unittest.TestCase):
    def test_dataset_has_exact_motifs_and_no_linear_shortcut(self):
        path = Path(__file__).resolve().parents[1] / "exercise_7.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        cells = {cell["id"]: "".join(cell["source"]) for cell in notebook["cells"]}
        namespace = {"__name__": "__main__"}

        with TemporaryDirectory() as directory, chdir(directory), redirect_stdout(StringIO()):
            exec(compile(cells["settings"], str(path), "exec"), namespace)
            namespace["n_backgrounds"] = 100
            namespace["ofile"] = "custom directory/nested/xor.csv"
            exec(compile(cells["generate-data"], str(path), "exec"), namespace)
            exec(compile(cells["check-save"], str(path), "exec"), namespace)
            dataset = namespace["dataset"].copy()
            pd.testing.assert_frame_equal(pd.read_csv(namespace["ofile"]), dataset)
            exec(compile(cells["generate-data"], str(path), "exec"), namespace)
            pd.testing.assert_frame_equal(namespace["dataset"], dataset)
            namespace["seed"] = 43
            exec(compile(cells["generate-data"], str(path), "exec"), namespace)
            self.assertFalse(namespace["dataset"].equals(dataset))

        self.assertEqual(len(dataset), 400)
        self.assertEqual(dataset.label.value_counts().to_dict(), {0: 200, 1: 200})
        self.assertEqual(dataset.groupby(["has_a", "has_b"]).size().tolist(), [100] * 4)
        self.assertTrue(dataset.sequence.str.fullmatch("[ACGT]{100}").all())
        self.assertTrue(dataset.sequence.is_unique)
        np.testing.assert_array_equal(dataset.label, dataset.has_a ^ dataset.has_b)

        motif_a, motif_b = namespace["motif_a"], namespace["motif_b"]
        # Lookahead counts overlapping matches independently of the generation code.
        np.testing.assert_array_equal(dataset.sequence.str.count(f"(?={motif_a})"), dataset.has_a)
        np.testing.assert_array_equal(dataset.sequence.str.count(f"(?={motif_b})"), dataset.has_b)

        for _, quartet in dataset.groupby("background_id"):
            by_case = quartet.set_index(["has_a", "has_b"])
            self.assertEqual(set(by_case.index), {(0, 0), (1, 0), (0, 1), (1, 1)})
            start_a = by_case.loc[(1, 0), "sequence"].find(motif_a)
            start_b = by_case.loc[(0, 1), "sequence"].find(motif_b)
            self.assertGreaterEqual(abs(start_a - start_b), len(motif_a) + 5)
            expected = list(by_case.loc[(0, 0), "sequence"])
            expected[start_a:start_a + len(motif_a)] = motif_a
            expected[start_b:start_b + len(motif_b)] = motif_b
            self.assertEqual("".join(expected), by_case.loc[(1, 1), "sequence"])

        ordered = dataset.sort_values(["background_id", "has_a", "has_b"])
        for k in (1, 4, 6):
            counts = CountVectorizer(analyzer="char", ngram_range=(k, k)).fit_transform(ordered.sequence)
            # Opposite corners have identical sums in the full feature space.
            difference = counts[0::4] + counts[3::4] - counts[1::4] - counts[2::4]
            self.assertEqual(difference.count_nonzero(), 0)

    def test_training_preserves_background_holdouts_and_learns_xor(self):
        path = Path(__file__).resolve().parents[1] / "exercise_7.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__"}
        vocabulary_fits = []
        transformed_sequences = []
        perceptron_fits = []
        forest_fits = []
        mlp_fits = []
        original_vocabulary_fit = CountVectorizer.fit_transform
        original_transform = CountVectorizer.transform
        original_perceptron_fit = Perceptron.fit
        original_forest_fit = RandomForestClassifier.fit
        original_mlp_fit = MLPClassifier.partial_fit

        def record_vocabulary_fit(vectorizer, sequences, *args, **kwargs):
            vocabulary_fits.append(tuple(sequences))
            return original_vocabulary_fit(vectorizer, sequences, *args, **kwargs)

        def record_transform(vectorizer, sequences, *args, **kwargs):
            transformed_sequences.append(tuple(sequences))
            return original_transform(vectorizer, sequences, *args, **kwargs)

        def record_perceptron_fit(model, counts, labels, *args, **kwargs):
            if issparse(counts):
                perceptron_fits.append((id(counts), tuple(labels.index)))
            return original_perceptron_fit(model, counts, labels, *args, **kwargs)

        def record_mlp_fit(model, counts, labels, *args, **kwargs):
            mlp_fits.append((id(counts), tuple(labels.index)))
            return original_mlp_fit(model, counts, labels, *args, **kwargs)

        def record_forest_fit(model, counts, labels, *args, **kwargs):
            forest_fits.append((id(counts), tuple(labels.index)))
            return original_forest_fit(model, counts, labels, *args, **kwargs)

        with TemporaryDirectory() as directory, chdir(directory), redirect_stdout(StringIO()), \
                threadpool_limits(limits=1), \
                patch.object(CountVectorizer, "fit_transform", record_vocabulary_fit), \
                patch.object(CountVectorizer, "transform", record_transform), \
                patch.object(Perceptron, "fit", record_perceptron_fit), \
                patch.object(RandomForestClassifier, "fit", record_forest_fit), \
                patch.object(MLPClassifier, "partial_fit", record_mlp_fit), \
                patch.object(plt, "show", side_effect=lambda: plt.close("all")):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    if cell["id"] == "test-evaluation":
                        self.assertNotIn("x_test", namespace)
                        self.assertNotIn("y_test", namespace)
                        self.assertNotIn("test_scores", namespace)
                        self.assertNotIn("test_results", namespace)
                    exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
                    if cell["id"] == "fit-forest":
                        self.assertNotIn("mlp", namespace)
                        self.assertNotIn("two_relu_units", namespace["truth_table"])
                        self.assertEqual(list(namespace["baseline_validation_results"].index),
                                         ["Perceptron", "Random forest"])

        train = namespace["train_data"]
        validation = namespace["validation_data"]
        test = namespace["test_data"]
        self.assertEqual([len(split) for split in (train, validation, test)], [14_000, 4_000, 2_000])
        self.assertEqual(len(set(train.background_id) & set(validation.background_id)), 0)
        self.assertEqual(len(set(train.background_id) & set(test.background_id)), 0)
        self.assertEqual(len(set(validation.background_id) & set(test.background_id)), 0)
        self.assertEqual(set(train.index) | set(validation.index) | set(test.index), set(namespace["dataset"].index))
        for split in (train, validation, test):
            self.assertEqual(split.groupby(["has_a", "has_b"]).size().tolist(), [len(split) // 4] * 4)
        self.assertEqual(vocabulary_fits, [tuple(train.sequence)])
        self.assertEqual(transformed_sequences, [tuple(validation.sequence), tuple(test.sequence)])
        expected_fit = (id(namespace["x_train"]), tuple(train.index))
        self.assertEqual(perceptron_fits, [expected_fit])
        self.assertEqual(forest_fits, [expected_fit])
        self.assertEqual(mlp_fits, [expected_fit] * namespace["max_epochs"])
        self.assertEqual(namespace["x_train"].shape, (14_000, 4_096))
        np.testing.assert_array_equal(np.asarray(namespace["x_train"].sum(axis=1)).ravel(), 95)
        np.testing.assert_array_equal(namespace["truth_table"].two_relu_units, namespace["truth_table"].label)

        self.assertEqual(namespace["best_epoch"], int(np.argmin(namespace["validation_losses"])) + 1)
        self.assertEqual(namespace["mlp_model"].t_, len(train) * namespace["best_epoch"])
        self.assertAlmostEqual(
            log_loss(namespace["y_validation"], namespace["validation_scores"]["MLP"]),
            min(namespace["validation_losses"]),
        )
        for split in ("validation", "test"):
            results = namespace[f"{split}_results"]
            self.assertEqual(list(results.index), ["Perceptron", "Random forest", "MLP"])
            self.assertTrue(np.isfinite(results.to_numpy()).all())
            self.assertNotIn("log_loss", results.columns)
            self.assertLessEqual(results.loc["Perceptron", "accuracy"], 0.75)
            self.assertGreater(results.loc["MLP", "accuracy"], 0.97)
            self.assertGreater(results.loc["Random forest", "accuracy"], 0.97)
            by_case = namespace[f"{split}_case_results"].groupby(["has_a", "has_b"]).mean()
            self.assertTrue(by_case["MLP"].gt(0.95).all())
            self.assertTrue(by_case["Random forest"].gt(0.95).all())
            for name in ("Perceptron", "Random forest", "MLP"):
                self.assertAlmostEqual(
                    results.loc[name, "roc_auc"],
                    roc_auc_score(namespace[f"y_{split}"], namespace[f"{split}_scores"][name]),
                )
