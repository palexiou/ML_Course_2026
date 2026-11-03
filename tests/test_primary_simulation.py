"""Scientific generator and provenance contracts; never score protected labels."""

from dataclasses import replace
from collections import Counter
from itertools import product
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "course_code"))
from course_core import (
    BASE_ORDER, DEFAULT_MOTIF_PPM, SimulationConfig, assign_splits, build_interaction_dataset,
    expected_motif_kmers, generate_course_dataset, read_dataset, save_dataset,
    settings_fingerprint, simulation_settings, validate_generation,
)


class PrimarySimulationTests(unittest.TestCase):
    def test_default_matrix_and_immutable_array_input(self) -> None:
        matrix = np.array(DEFAULT_MOTIF_PPM)
        config = SimulationConfig(motif_ppm=matrix)
        matrix[0] = 0
        self.assertEqual(config.motif_ppm, DEFAULT_MOTIF_PPM)
        self.assertEqual(hash(config), hash(SimulationConfig()))
        matrix = np.array(config.motif_ppm)
        self.assertEqual(matrix.shape, (15, 4))
        self.assertTrue(np.all(matrix > 0))
        self.assertTrue(np.all(matrix.max(axis=1) >= 0.5))
        np.testing.assert_allclose(matrix.sum(axis=1), 1)
        self.assertIn((0.5, 0.4, 0.05, 0.05), config.motif_ppm)
        self.assertGreater(len(set(config.motif_ppm)), 10)

    def test_invalid_configurations(self) -> None:
        matrices = [np.ones((14, 4)), np.ones((15, 3)), np.ones((4, 15))]
        for value in (0, -0.1, np.nan, np.inf):
            matrix = np.array(DEFAULT_MOTIF_PPM)
            matrix[0, 0] = value
            matrices.append(matrix)
        for row in ((0.25, 0.25, 0.25, 0.25), (0.6, 0.1, 0.1, 0.1)):
            matrix = np.array(DEFAULT_MOTIF_PPM)
            matrix[0] = row
            matrices.append(matrix)
        matrix = np.array(DEFAULT_MOTIF_PPM)
        matrix[0] = (1, 1e-20, 1e-20, 1e-20)
        matrices.append(matrix)
        for matrix in matrices:
            with self.subTest(matrix=matrix.shape), self.assertRaises(ValueError):
                SimulationConfig(motif_ppm=matrix)
        with self.assertRaises(ValueError):
            SimulationConfig(sequence_length=14)
        for name in ("positive_plant_probability", "negative_plant_probability"):
            for value in (-0.01, 1.01, np.nan, np.inf):
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    replace(SimulationConfig(), **{name: value})
        with self.assertRaises(TypeError):
            SimulationConfig(motif="TATAAATG")  # type: ignore[call-arg]

    def test_reproducibility_identities_splits_and_truth(self) -> None:
        config = SimulationConfig()
        samples, truth = generate_course_dataset(config)
        repeated, repeated_truth = generate_course_dataset(config)
        pd.testing.assert_frame_equal(samples, repeated)
        pd.testing.assert_frame_equal(truth, repeated_truth)
        self.assertEqual(set(samples), {"sample_id", "group_id", "sequence", "label"})
        self.assertTrue(samples.sample_id.is_unique)
        self.assertEqual(samples.label.value_counts().to_dict(), {0: 600, 1: 600})
        self.assertTrue(samples.sequence.str.len().eq(160).all())
        self.assertTrue(samples.sequence.map(lambda s: set(s) <= set(BASE_ORDER)).all())
        # Reconstruct the previous generator's label/ID construction independently.
        labels = np.repeat([0, 1], 600)
        np.random.default_rng(config.seed).shuffle(labels)
        np.testing.assert_array_equal(samples.label, labels)
        self.assertEqual(samples.sample_id.tolist(), [f"simple-2026-{i:05d}" for i in range(1200)])
        split = assign_splits(samples, config.seed)
        self.assertEqual(split.split.value_counts().to_dict(), {"train": 720, "validation": 240, "test": 240})
        self.assertEqual(split.groupby("group_id").split.nunique().max(), 1)
        self.assertTrue(split.groupby("split").label.mean().eq(0.5).all())
        # A probability change affects DNA/truth, but not labels or partitions.
        changed, _ = generate_course_dataset(replace(config, positive_plant_probability=0.8))
        pd.testing.assert_series_equal(assign_splits(changed, config.seed).split, split.split)
        for sample, record in zip(samples.itertuples(), truth.itertuples()):
            if record.motif_planted:
                self.assertTrue(0 <= record.motif_start <= 145)
                self.assertEqual(sample.sequence[record.motif_start:record.motif_start + 15], record.sampled_site)
            else:
                self.assertTrue(pd.isna(record.motif_start))
                self.assertIsNone(record.sampled_site)
        sites = truth.loc[truth.motif_planted, "sampled_site"]
        consensus = "".join(BASE_ORDER[i] for i in np.argmax(config.motif_ppm, axis=1))
        self.assertGreater(sites.nunique(), 100)
        self.assertGreater((sites != consensus).mean(), 0.9)

    def test_uniform_start_bounds_and_exact_fit(self) -> None:
        class BoundaryGenerator:
            def __init__(self) -> None:
                self.generator = np.random.Generator(np.random.PCG64(91))
                self.calls = 0

            def __getattr__(self, name):
                return getattr(self.generator, name)

            def integers(self, low, high):
                self.calls += 1
                self.assert_bounds = (low, high)
                return low if self.calls % 2 else high - 1

        for length in (15, 160):
            random = BoundaryGenerator()
            with patch("course_core.np.random.default_rng", return_value=random):
                samples, truth = generate_course_dataset(SimulationConfig(
                    sample_count=20, sequence_length=length,
                    positive_plant_probability=1, negative_plant_probability=1))
            self.assertEqual(random.assert_bounds, (0, length - 15 + 1))
            self.assertEqual(set(truth.motif_start), {0, length - 15})
            for seq, start, site in zip(samples.sequence, truth.motif_start, truth.sampled_site):
                self.assertEqual(seq[start:start + 15], site)

    def test_plant_rates_and_sampling_marginals(self) -> None:
        config = SimulationConfig(sample_count=16000, seed=872)
        samples, truth = generate_course_dataset(config)
        for label, expected in ((0, 0.05), (1, 0.95)):
            observed = truth.loc[samples.label == label, "motif_planted"].mean()
            self.assertLess(abs(observed - expected), 0.015)
        sites = np.array([list(site) for site in truth.loc[truth.motif_planted, "sampled_site"]])
        for position, row in enumerate(config.motif_ppm):
            for base, expected in zip(BASE_ORDER, row):
                self.assertLess(abs(np.mean(sites[:, position] == base) - expected), 0.025)
        starts = truth.loc[truth.motif_planted, "motif_start"].to_numpy(dtype=int)
        self.assertEqual(set(starts), set(range(146)))
        self.assertLess(abs(starts.mean() - 72.5), 2)

    def test_zero_planting_does_not_fabricate_truth(self) -> None:
        _, truth = generate_course_dataset(SimulationConfig(
            sample_count=20, positive_plant_probability=0, negative_plant_probability=0))
        self.assertFalse(truth.motif_planted.any())
        self.assertTrue(truth[["motif_start", "sampled_site"]].isna().all().all())

    def test_expected_fourmer_distribution_independent_calculation(self) -> None:
        config = SimulationConfig()
        words = ["".join(bases) for bases in product(BASE_ORDER, repeat=4)]
        expected = expected_motif_kmers(config, words).set_index("kmer")
        independent = {}
        # Successive expansion of each 4-position distribution, rather than indexing products.
        for start in range(12):
            partial = {"": 1.0}
            for row in config.motif_ppm[start:start + 4]:
                partial = {prefix + base: p * q for prefix, p in partial.items()
                           for base, q in zip(BASE_ORDER, row)}
            for word, probability in partial.items():
                independent[word] = independent.get(word, 0.0) + probability / 12
        np.testing.assert_allclose(expected.motif_window_probability, [independent[w] for w in words], atol=1e-15)
        self.assertAlmostEqual(expected.motif_window_probability.sum(), 1)
        np.testing.assert_allclose(expected.motif_vs_background_enrichment, expected.motif_window_probability * 256)
        self.assertTrue(expected.motif_window_probability.gt(0).all())
        self.assertTrue(expected_motif_kmers(replace(config, kmer_length=16), ["A" * 16]).empty)

    def test_generation_fingerprints_and_legacy_rejection(self) -> None:
        config = SimulationConfig(sample_count=40)
        matrix = np.array(config.motif_ppm)
        matrix[0, 0] += 0.01
        matrix[0, 1] -= 0.01
        configs = [config, replace(config, seed=2027), replace(config, positive_plant_probability=0.9),
                   replace(config, negative_plant_probability=0.1), replace(config, motif_ppm=tuple(map(tuple, matrix)))]
        self.assertEqual(len({settings_fingerprint(simulation_settings(c)) for c in configs}), len(configs))
        for key in ("base_order", "algorithm_version"):
            settings = simulation_settings(config)
            settings[key] = "different"
            self.assertNotEqual(settings_fingerprint(settings), settings_fingerprint(simulation_settings(config)))
        with TemporaryDirectory() as temp:
            root = Path(temp)
            samples, truth = generate_course_dataset(config)
            save_dataset(root, assign_splits(samples, config.seed), truth, simulation_settings(config))
            development = read_dataset(root)
            self.assertTrue(development.loc[development.split == "test", "label"].isna().all())
            self.assertIn("dataset_generation_sha256", development.attrs)
            metadata_path = root / "generation.json"
            original = metadata_path.read_text()
            metadata = json.loads(original)
            metadata["settings"]["positive_plant_probability"] = 0.7
            metadata_path.write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, "fingerprint"):
                read_dataset(root)
            metadata_path.write_text(original)
            metadata["schema_version"] = 1
            metadata_path.write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, "Incompatible"):
                read_dataset(root)
            metadata_path.write_text(original)
            metadata = json.loads(original)
            metadata["settings"]["algorithm_version"] = "old"
            metadata["settings_sha256"] = settings_fingerprint(metadata["settings"])
            metadata_path.write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, "algorithm"):
                read_dataset(root)
            metadata_path.write_text(original)
            with (root / "train.csv").open("a") as stream:
                stream.write("\n")
            with self.assertRaisesRegex(ValueError, "file identity"):
                validate_generation(root)
            with self.assertRaisesRegex(ValueError, "Legacy"):
                save_dataset(root, samples, truth, {"motif": "TATAAATG"})

    def test_interaction_control_survives_metadata_migration(self) -> None:
        samples, truth = build_interaction_dataset(pair_count=20)
        self.assertEqual(set(truth.first_motif), {"TATAAATG", "CGGACGTC"})
        for _, pair in samples.groupby("group_id"):
            sequences = pair.sequence.tolist()
            bags = [Counter(seq[start:start + 4] for start in range(len(seq) - 3)) for seq in sequences]
            self.assertEqual(bags[0], bags[1])
            self.assertEqual(set(pair.label), {0, 1})
            self.assertEqual(pair.split.nunique(), 1)
        with TemporaryDirectory() as temp:
            save_dataset(temp, samples, truth, {"seed": 2026, "pair_count": 20,
                                               "lesson": "separate fixed-position control"})
            restored = read_dataset(temp)
            self.assertEqual(restored.sequence.tolist(),
                             [seq for split in ("train", "validation", "test")
                              for seq in samples.loc[samples.split == split, "sequence"]])


if __name__ == "__main__":
    unittest.main()
