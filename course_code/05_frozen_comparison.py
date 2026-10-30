"""Freeze development artifacts, then explicitly reveal protected test results once."""

from pathlib import Path
from typing import Any, Callable
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import inspect
import json
from importlib.metadata import version
from textwrap import dedent

import joblib
import numpy as np
import pandas as pd
import torch

from course_core import classification_metrics, file_hash, read_dataset
from course_inference import SequenceCNN, one_hot, predict_cnn, load_embedding_cache, sequence_hashes

REVEAL_CONFIRMATION = "REVEAL THE FROZEN TEST RESULTS"


def artifact_paths(root: Path) -> list[Path]:
    paths = [root / name for name in ("representation_run.json", "representation_validation.csv", "representation_validation_predictions.csv", "embedding_run.json", "embedding_validation.csv")]
    for variant in ("simple", "interaction"):
        paths.extend(root / "datasets" / variant / name for name in ("train.csv", "validation.csv", "protected_test.csv", "split_manifest.csv", "simulation_truth.csv", "generation.json"))
        paths.extend(root / "models" / variant / name for name in ("logistic_regression.joblib", "random_forest.joblib", "cnn.pt", "cnn_history.csv", "foundation.joblib"))
        paths.append(root / "embeddings" / f"{variant}.npz")
        paths.append(root / "models" / variant / "foundation_validation_predictions.csv")
    paths.append(root / "models" / "interaction" / "controlled_order_changes.csv")
    return paths


def inference_identity() -> dict[str, Any]:
    functions: dict[str, Callable[..., Any]] = {"cnn_init": SequenceCNN.__init__, "cnn_forward": SequenceCNN.forward, "one_hot": one_hot, "predict_cnn": predict_cnn, "sequence_hashes": sequence_hashes, "load_embedding_cache": load_embedding_cache, "read_dataset": read_dataset, "classification_metrics": classification_metrics, "reveal_test": reveal_test}
    fingerprints = {}
    for name, function in functions.items():
        try:
            syntax = ast.dump(ast.parse(dedent(inspect.getsource(function))), include_attributes=False)
        except (OSError, TypeError) as error:
            raise RuntimeError("Cannot capture inference source. Run a script or a notebook cell that preserves source history before freezing.") from error
        fingerprints[name] = hashlib.sha256(syntax.encode("utf-8")).hexdigest()
    return {"source_sha256": fingerprints, "packages": {name: version(name) for name in ("numpy", "pandas", "scikit-learn", "torch")}}


def write_exclusive(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as output:
        output.write(json.dumps(value, indent=2, allow_nan=False) + "\n")


def freeze_workflows(output_dir: str | Path = "course_output") -> dict[str, Any]:
    root = Path(output_dir)
    if (root / "test_results.json").exists():
        raise RuntimeError("Test results already exist; this is not a new independent evaluation")
    if (root / "frozen_manifest.json").exists():
        raise FileExistsError("A freeze already exists. Keep it unchanged or start in a new development directory.")
    representation = json.loads((root / "representation_run.json").read_text(encoding="utf-8"))
    embedding = json.loads((root / "embedding_run.json").read_text(encoding="utf-8"))
    for variant in ("simple", "interaction"):
        samples = read_dataset(root / "datasets" / variant)
        load_embedding_cache(root / "embeddings" / f"{variant}.npz", samples)
        for record in (representation["runs"][variant], embedding["runs"][variant]):
            if record["test_evaluated"]:
                raise ValueError("Development metadata reports previous test evaluation")
            for split, key in (("train", "training_ids"), ("validation", "validation_ids")):
                if sorted(record[key]) != sorted(samples.loc[samples["split"] == split, "sample_id"]):
                    raise ValueError("Model development identities differ from the dataset")
    fingerprints = {path.relative_to(root).as_posix(): file_hash(path) for path in artifact_paths(root)}
    manifest = {"created_utc": datetime.now(timezone.utc).isoformat(), "primary_metric": "roc_auc", "decision_threshold": 0.5, "methods": ["logistic_regression", "random_forest", "cnn", "foundation"], "artifacts": fingerprints, "inference_identity": inference_identity(), "policy": "Freeze all four workflows before test reveal. No post-reveal tuning is independent test evidence. Hashes enforce an accident guard, not adversarial access security."}
    write_exclusive(root / "frozen_manifest.json", manifest)
    print("Frozen. Test results have NOT been calculated. Discuss expected outcomes before revealing.")
    return manifest


def reveal_test(output_dir: str | Path = "course_output", confirmation: str = "") -> pd.DataFrame:
    if confirmation != REVEAL_CONFIRMATION:
        raise ValueError("Explicit confirmation is required to reveal protected test results")
    root = Path(output_dir)
    if (root / "test_results.json").exists():
        raise FileExistsError("Results have already been revealed. Read the saved results; do not retune and repeat.")
    manifest = json.loads((root / "frozen_manifest.json").read_text(encoding="utf-8"))
    if manifest["inference_identity"] != inference_identity():
        raise ValueError("Frozen inference implementation or package versions changed")
    expected_paths = {path.relative_to(root).as_posix() for path in artifact_paths(root)}
    if set(manifest["artifacts"]) != expected_paths:
        raise ValueError("Frozen artifact inventory is incomplete or unexpected")
    for relative, expected_hash in manifest["artifacts"].items():
        if file_hash(root / relative) != expected_hash:
            raise ValueError(f"Frozen artifact changed: {relative}")
    results, predictions = [], []
    for variant in ("simple", "interaction"):
        samples = read_dataset(root / "datasets" / variant, include_test_labels=True)
        test = samples.loc[samples["split"] == "test"]
        destination = root / "models" / variant
        probabilities_by_method = {}
        for method in ("logistic_regression", "random_forest"):
            classifier = joblib.load(destination / f"{method}.joblib")
            probabilities_by_method[method] = classifier.predict_proba(test["sequence"])[:, 1]
        checkpoint = torch.load(destination / "cnn.pt", map_location="cpu", weights_only=True)
        cnn = SequenceCNN(checkpoint["sequence_length"])
        cnn.load_state_dict(checkpoint["state_dict"])
        probabilities_by_method["cnn"] = predict_cnn(cnn, test["sequence"])
        features = load_embedding_cache(root / "embeddings" / f"{variant}.npz", samples)
        foundation = joblib.load(destination / "foundation.joblib")
        probabilities_by_method["foundation"] = foundation.predict_proba(features[samples["split"] == "test"])[:, 1]
        for method, probabilities in probabilities_by_method.items():
            metrics = classification_metrics(test["label"], probabilities, "test")
            results.append({"variant": variant, "method": method, **metrics})
            frame = test[["sample_id", "group_id", "label"]].copy()
            frame["probability"] = probabilities
            frame["variant"], frame["method"] = variant, method
            predictions.append(frame)
    write_exclusive(root / "test_results.json", {"revealed_utc": datetime.now(timezone.utc).isoformat(), "frozen_manifest_sha256": file_hash(root / "frozen_manifest.json"), "results": results, "interpretation": "One planned test comparison of validation-developed workflows, not a biological benchmark. Do not select changes using these test scores."})
    pd.concat(predictions, ignore_index=True).to_csv(root / "test_predictions.csv", index=False)
    table = pd.DataFrame(results)
    table.to_csv(root / "test_comparison.csv", index=False)
    print(table[["variant", "method", "roc_auc", "average_precision"]].to_string(index=False))
    return table


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["freeze", "reveal"])
    parser.add_argument("--output-dir", default="course_output")
    parser.add_argument("--confirm", default="")
    arguments = parser.parse_args()
    if arguments.action == "freeze":
        freeze_workflows(arguments.output_dir)
    else:
        reveal_test(arguments.output_dir, arguments.confirm)
