"""Check the specified Exercise 1 dataset and motif sampling."""

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "course_code"))
import exercise_1


class Exercise1Tests(unittest.TestCase):
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
