"""Execute the delivered Section 3 cells, stopping before metrics and forests."""

from collections import Counter
from contextlib import chdir, redirect_stdout
from io import StringIO
import hashlib
import json
import math
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parents[1]


class Section3NotebookTests(unittest.TestCase):
    def test_generated_classroom_path_from_empty_workspace(self):
        notebook = json.loads((ROOT / "notebooks/01_simple_signal.ipynb").read_text())
        cells = {cell["id"]: "".join(cell["source"]) for cell in notebook["cells"]}
        read_csv = pd.read_csv
        reads = []

        def development_read(path, *args, **kwargs):
            reads.append(Path(path).name)
            self.assertIn(Path(path).name, {"train.csv", "validation.csv"})
            return read_csv(path, *args, **kwargs)

        namespace = {"__name__": "__section3_notebook__", "ALLOWED_TEST_REVEAL": False}

        def run(name):
            exec(compile(cells[name], f"01_simple_signal.ipynb:{name}", "exec"), namespace)

        with TemporaryDirectory(prefix="ml-course-section3-") as temp, chdir(temp), \
                redirect_stdout(StringIO()) as output, \
                patch.dict(os.environ, {"ALLOWED_TEST_REVEAL": "0"}), \
                patch("subprocess.check_call", side_effect=AssertionError("No installation during local check")), \
                patch("pandas.read_csv", side_effect=development_read), \
                patch.object(RandomForestClassifier, "fit", side_effect=AssertionError("No forest in Section 3")):
            self.assertEqual(list(Path(temp).iterdir()), [])
            for name in ("setup", "shared-definitions-0", "definitions-01"):
                run(name)
            # Fail if a teaching cell accidentally crosses into the full workflow/evaluation.
            with patch.dict(namespace, {
                "run_experiment": unittest.mock.Mock(side_effect=AssertionError("No full workflow")),
                "validation_metrics": unittest.mock.Mock(side_effect=AssertionError("No metric summary")),
                "roc_auc_score": unittest.mock.Mock(side_effect=AssertionError("No ROC-AUC in Section 3")),
                "average_precision_score": unittest.mock.Mock(side_effect=AssertionError("No AP in Section 3")),
            }):
                for name in ("s3-data", "s3-counts", "s3-fit", "s3-prediction", "s3-loss", "s3-gradient"):
                    run(name)

                train, validation = namespace["s3_train"], namespace["s3_validation"]
                self.assertEqual((len(train), len(validation)), (720, 240))
                self.assertTrue(set(train.sample_id).isdisjoint(validation.sample_id))
                self.assertTrue(set(train.group_id).isdisjoint(validation.group_id))
                self.assertEqual(namespace["s3_x_train"].shape, (720, 256))
                self.assertEqual(namespace["s3_x_validation"].shape, (240, 256))
                vocabulary = {sequence[i:i + 4] for sequence in train.sequence
                              for i in range(len(sequence) - 3)}
                self.assertEqual(set(namespace["s3_words"]), vocabulary)
                record = namespace["s3_record"]
                expected_counts = Counter(record.sequence[i:i + 4] for i in range(len(record.sequence) - 3))
                actual_counts = namespace["s3_count_row"]
                self.assertEqual(actual_counts[actual_counts > 0].to_dict(), dict(expected_counts))
                self.assertEqual(actual_counts.sum(), 157)

                classifier = namespace["s3_classifier"]
                self.assertEqual(classifier.classes_.tolist(), [0, 1])
                self.assertEqual(classifier.solver, "lbfgs")
                z = math.fsum(float(count) * float(weight) for count, weight in
                              zip(actual_counts, classifier.coef_[0])) + float(classifier.intercept_[0])
                self.assertAlmostEqual(z, namespace["s3_score"], places=11)
                p = 1 / (1 + math.exp(-z))
                np.testing.assert_allclose(namespace["s3_probabilities"], [1 - p, p], atol=1e-12)
                label = int(record.label)
                independent_loss = -(label * math.log(p) + (1 - label) * math.log1p(-p))
                self.assertAlmostEqual(independent_loss, namespace["s3_row_loss"], places=11)
                train_probabilities = classifier.predict_proba(namespace["s3_x_train"])[:, 1]
                independent_mean = math.fsum(-math.log(p_i if y else 1 - p_i)
                                             for y, p_i in zip(train.label, train_probabilities)) / len(train)
                self.assertAlmostEqual(independent_mean, namespace["s3_mean_training_loss"], places=11)
                self.assertLess(-math.log(0.95), 0.1)
                self.assertGreater(-math.log(0.05), 2.9)

                loss, gradient = namespace["s3_toy_loss"], namespace["s3_toy_gradient"]
                for weight in (-2.0, 0.0, 1.5):
                    epsilon = 1e-5
                    numerical = (loss(weight + epsilon) - loss(weight - epsilon)) / (2 * epsilon)
                    self.assertAlmostEqual(gradient(weight), numerical, places=8)
                steps = namespace["s3_step_table"]
                self.assertEqual(len(steps), 9)
                self.assertTrue(np.all(np.diff(steps.loss) < 0))
                self.assertGreater(steps.loss.iloc[-1], 0)
                self.assertLess(steps.loss.iloc[-1], steps.loss.iloc[0])
                np.testing.assert_allclose(steps.weight.to_numpy()[1:],
                                           steps.weight.to_numpy()[:-1] - 0.8 * steps.gradient.to_numpy()[:-1])

                # A second preparation run must verify and reuse the same canonical artifacts.
                destination = Path("simple_signal_output")
                before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in destination.iterdir()}
                with patch.dict(namespace, {
                    "generate_course_dataset": unittest.mock.Mock(side_effect=AssertionError("Must reuse data"))
                }):
                    run("s3-data")
                self.assertEqual(before, {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                          for path in destination.iterdir()})
                self.assertEqual(set(before), {"train.csv", "validation.csv", "protected_test.csv",
                                              "split_manifest.csv", "simulation_truth.csv", "generation.json"})
                self.assertEqual(set(path.name for path in Path(temp).iterdir()), {"simple_signal_output"})
                self.assertEqual(reads, ["train.csv", "validation.csv"] * 2)
                self.assertNotIn("roc_auc", output.getvalue())
                self.assertNotIn("average_precision", output.getvalue())
                self.assertFalse(Path("course_output/test_results.json").exists())

                # Exercise the two small edits offered to students, without touching the notebook file.
                first_id = record.sample_id
                cells["s3-counts"] = cells["s3-counts"].replace("s3_row_index = 0", "s3_row_index = 1")
                for name in ("s3-counts", "s3-fit", "s3-prediction", "s3-loss"):
                    run(name)
                self.assertNotEqual(namespace["s3_record"].sample_id, first_id)
                cells["s3-gradient"] = cells["s3-gradient"].replace("s3_learning_rate = 0.8", "s3_learning_rate = 0.2")
                run("s3-gradient")
                slower_steps = namespace["s3_step_table"]
                self.assertTrue(np.all(np.diff(slower_steps.loss) < 0))
                self.assertGreater(slower_steps.loss.iloc[-1], steps.loss.iloc[-1])


if __name__ == "__main__":
    unittest.main()
