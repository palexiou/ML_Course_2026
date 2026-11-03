"""Cheap synthetic cache/freeze checks; no CNN fitting, encoder or test reveal."""

import ast
import hashlib
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "course_code"))
from course_core import (
    SimulationConfig, assign_splits, generate_course_dataset, generation_contract,
    read_dataset, save_dataset, settings_fingerprint, simulation_settings, write_json, file_hash,
)


def isolated_contracts(filename, names, extra=None):
    """Compile exact pure contract functions without importing optional neural packages.

    Neural inference identity is a disclosed stub in the metadata-only freeze fixture.
    This does not exercise CNN inference, extraction, or the full freeze source capture.
    """
    path = Path(__file__).resolve().parents[1] / "course_code" / filename
    tree = ast.parse(path.read_text())
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in nodes} == set(names)
    namespace = dict(globals())
    namespace.update(extra or {})
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    return SimpleNamespace(**namespace)


# Read the actual declared representation constants, without importing torch.
source_path = Path(__file__).resolve().parents[1] / "course_code" / "course_inference.py"
constants = {}
for node in ast.parse(source_path.read_text()).body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
        if node.targets[0].id in {"MODEL_ID", "REVISION", "POOLING"}:
            constants[node.targets[0].id] = ast.literal_eval(node.value)
MODEL_ID, REVISION, POOLING = (constants[key] for key in ("MODEL_ID", "REVISION", "POOLING"))
contracts = isolated_contracts("course_inference.py", ["load_embedding_cache", "sequence_hashes"])
load_embedding_cache, sequence_hashes = contracts.load_embedding_cache, contracts.sequence_hashes


class GenerationArtifactTests(unittest.TestCase):
    def make_dataset(self, root):
        config = SimulationConfig(sample_count=40)
        samples, truth = generate_course_dataset(config)
        save_dataset(root, assign_splits(samples, config.seed), truth, simulation_settings(config))
        return read_dataset(root)

    def cache_values(self, samples):
        return {"sample_ids": samples.sample_id.to_numpy(dtype=str),
                "sequence_sha256": sequence_hashes(samples),
                "embeddings": np.arange(len(samples) * 512).reshape(len(samples), 512),
                "model_id": np.array(MODEL_ID), "revision": np.array(REVISION),
                "pooling": np.array(POOLING),
                "dataset_generation_sha256": np.array(samples.attrs["dataset_generation_sha256"])}

    def test_cache_requires_generation_and_retains_sequence_checks(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            samples = self.make_dataset(root / "data")
            path = root / "cache.npz"
            values = self.cache_values(samples)
            np.savez(path, **values)
            np.testing.assert_array_equal(load_embedding_cache(path, samples), values["embeddings"])
            shuffled = samples.sample(frac=1, random_state=51)
            np.testing.assert_array_equal(load_embedding_cache(path, shuffled), values["embeddings"][shuffled.index])
            for identity in (None, np.array("older-generation")):
                stale = values.copy()
                if identity is None:
                    stale.pop("dataset_generation_sha256")
                else:
                    stale["dataset_generation_sha256"] = identity
                np.savez(path, **stale)
                with self.assertRaisesRegex(ValueError, "generation identity"):
                    load_embedding_cache(path, samples)
            np.savez(path, **values)
            changed = samples.copy()
            changed.loc[0, "sequence"] = "A" * 160
            with self.assertRaisesRegex(ValueError, "sequence hashes"):
                load_embedding_cache(path, changed)

    def test_freeze_binds_generation_without_revealing(self):
        freeze = isolated_contracts("05_frozen_comparison.py",
                                    ["freeze_workflows", "artifact_paths", "write_exclusive"],
                                    {"inference_identity": lambda: {"fixture": "no neural inference"}})
        with TemporaryDirectory() as temp:
            root = Path(temp)
            records = {}
            for variant in ("simple", "interaction"):
                # Both fixture partitions use cheap primary generation, not course outcomes.
                samples = self.make_dataset(root / "datasets" / variant)
                cache_path = root / "embeddings" / f"{variant}.npz"
                cache_path.parent.mkdir(exist_ok=True)
                np.savez(cache_path, **self.cache_values(samples))
                records[variant] = {
                    "dataset_generation_sha256": samples.attrs["dataset_generation_sha256"],
                    "test_evaluated": False,
                    "training_ids": samples.loc[samples.split == "train", "sample_id"].tolist(),
                    "validation_ids": samples.loc[samples.split == "validation", "sample_id"].tolist(),
                }
            for path in freeze.artifact_paths(root):
                if not path.exists():
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("synthetic freeze-inventory placeholder; never run inference\n")
            write_json(root / "representation_run.json", {"runs": records})
            write_json(root / "embedding_run.json", {"runs": records})
            legacy = json.loads((root / "representation_run.json").read_text())
            legacy["runs"]["simple"].pop("dataset_generation_sha256")
            write_json(root / "representation_run.json", legacy)
            with self.assertRaisesRegex(ValueError, "Model generation identity"):
                freeze.freeze_workflows(root)
            self.assertFalse((root / "frozen_manifest.json").exists())
            write_json(root / "representation_run.json", {"runs": records})
            manifest = freeze.freeze_workflows(root)
            saved = json.loads((root / "frozen_manifest.json").read_text())
            self.assertEqual(settings_fingerprint(saved["generation_contract"]), settings_fingerprint(generation_contract()))
            self.assertEqual(manifest["inference_identity"], {"fixture": "no neural inference"})
            self.assertFalse((root / "test_results.json").exists())
            self.assertFalse((root / "test_predictions.csv").exists())


if __name__ == "__main__":
    unittest.main()
