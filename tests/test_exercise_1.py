"""Check the specified Exercise 1 dataset and motif sampling."""

from contextlib import chdir, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import exercise_1


class Exercise1Tests(unittest.TestCase):
    def test_notebook_runs_independently_and_matches_script(self):
        path = Path(__file__).resolve().parents[1] / "exercise_1.ipynb"
        notebook = json.loads(path.read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__"}
        with TemporaryDirectory() as directory, chdir(directory), redirect_stdout(StringIO()):
            for cell in notebook["cells"]:
                if cell["cell_type"] == "code":
                    exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
            saved = pd.read_csv(namespace["ofile"])
        pd.testing.assert_frame_equal(saved, exercise_1.generate_dataset())

    def test_cli_default_and_custom_output_paths(self):
        script = Path(exercise_1.__file__).resolve()
        for output in (exercise_1.OUTPUT_PATH, Path("custom directory/nested/data.csv")):
            with self.subTest(output=output), TemporaryDirectory() as directory:
                arguments = [] if output == exercise_1.OUTPUT_PATH else ["--ofile", str(output)]
                result = subprocess.run(
                    [sys.executable, str(script), *arguments], cwd=directory,
                    capture_output=True, text=True, check=True,
                )
                saved = pd.read_csv(Path(directory) / output)
                pd.testing.assert_frame_equal(saved, exercise_1.generate_dataset())
                self.assertIn(str(output), result.stdout)
                if arguments:
                    self.assertFalse((Path(directory) / exercise_1.OUTPUT_PATH).exists())

    def test_first_ten_columns_and_position_probabilities(self):
        expected = np.array([
            [87, 167, 281, 56, 8, 744, 40, 107, 851, 5],
            [291, 145, 49, 800, 903, 13, 528, 433, 11, 0],
            [76, 414, 449, 21, 0, 65, 334, 48, 32, 903],
            [459, 187, 134, 36, 2, 91, 11, 324, 18, 3],
        ])
        np.testing.assert_array_equal(exercise_1.PFM, expected)
        motifs = exercise_1.sample_motifs(np.random.default_rng(17), 100_000)
        self.assertEqual(motifs.shape, (100_000, 10))
        for row, base in enumerate("ACGT"):
            observed = (motifs == base).mean(axis=0)
            np.testing.assert_allclose(
                observed, expected[row] / expected.sum(axis=0), atol=0.006, rtol=0
            )
            self.assertTrue(np.all(observed[expected[row] == 0] == 0))

    def test_dataset_counts_lengths_background_and_reproducibility(self):
        dataset = exercise_1.generate_dataset()
        self.assertEqual(list(dataset.columns), ["sequence", "label"])
        self.assertEqual(dataset.label.value_counts().to_dict(), {1: 10_000, 0: 10_000})
        self.assertTrue(dataset.sequence.str.len().eq(100).all())
        self.assertTrue(dataset.sequence.str.fullmatch("[ACGT]{100}").all())
        negatives = "".join(dataset.loc[dataset.label == 0, "sequence"])
        for base in "ACGT":
            self.assertAlmostEqual(negatives.count(base) / len(negatives), 0.25, delta=0.002)
        pd.testing.assert_frame_equal(dataset, exercise_1.generate_dataset())
        self.assertFalse(dataset.equals(exercise_1.generate_dataset(seed=43)))

    def test_one_insert_per_positive_and_full_position_range(self):
        marker_motifs = np.full((10_000, 10), "X")
        with patch.object(exercise_1, "sample_motifs", return_value=marker_motifs):
            dataset = exercise_1.generate_dataset()
        positives = dataset.loc[dataset.label == 1, "sequence"]
        negatives = dataset.loc[dataset.label == 0, "sequence"]
        self.assertTrue(positives.str.count("X").eq(10).all())
        self.assertTrue(positives.str.contains("X" * 10, regex=False).all())
        self.assertFalse(negatives.str.contains("X", regex=False).any())
        self.assertEqual(set(positives.str.find("X")), set(range(91)))
        backgrounds = "".join(dataset.sequence).replace("X", "")
        for base in "ACGT":
            self.assertAlmostEqual(backgrounds.count(base) / len(backgrounds), 0.25, delta=0.002)


if __name__ == "__main__":
    unittest.main()
