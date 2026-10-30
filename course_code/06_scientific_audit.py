"""Recompute prediction evidence without mistaking it for a complete scientific audit."""

from pathlib import Path
from typing import Any
import argparse
import json

import numpy as np
import pandas as pd

from course_core import classification_metrics, write_json


def audit_predictions(samples: pd.DataFrame, predictions: pd.DataFrame, evaluation_split: str = "validation", claimed_metrics: dict[str, Any] | None = None) -> dict[str, Any]:
    required = {"sample_id", "group_id", "sequence", "label", "split"}
    if not required <= set(samples) or not {"sample_id", "probability"} <= set(predictions):
        raise ValueError("Missing dataset or prediction columns")
    if samples[list(required - {"label"})].isna().any().any() or not samples["sample_id"].is_unique:
        raise ValueError("Dataset identities must be unique and non-null")
    if not set(samples["split"]) <= {"train", "validation", "test"} or not set(samples["label"].dropna()) <= {0, 1}:
        raise ValueError("Unexpected split names or binary labels")
    if evaluation_split not in {"validation", "test"}:
        raise ValueError("Audit only validation or explicitly supplied test predictions")
    selected = samples.loc[samples["split"] == evaluation_split]
    if selected["label"].isna().any() or set(selected["label"]) != {0, 1}:
        raise ValueError("The requested evaluation split must contain both binary labels")
    if selected.empty or not predictions["sample_id"].is_unique or set(predictions["sample_id"]) != set(selected["sample_id"]):
        raise ValueError("Prediction IDs must cover the requested evaluation split exactly once")
    joined = selected.merge(predictions[["sample_id", "probability"]], on="sample_id", validate="one_to_one")
    probabilities = joined["probability"].to_numpy(dtype=float)
    if not np.isfinite(probabilities).all() or np.any((probabilities < 0) | (probabilities > 1)):
        raise ValueError("Predictions must be finite probabilities between zero and one")
    metrics = classification_metrics(joined["label"], probabilities, evaluation_split)
    overlapping_groups = samples.groupby("group_id")["split"].nunique()
    duplicate_sequences = samples.groupby("sequence")["split"].nunique()
    disagreements = []
    for metric, claimed in (claimed_metrics or {}).items():
        if metric not in metrics:
            disagreements.append(f"Unsupported metric claim: {metric}")
        elif isinstance(metrics[metric], (int, float)) and isinstance(claimed, (int, float)):
            if not np.isclose(metrics[metric], claimed, atol=1e-6, rtol=1e-6):
                disagreements.append(f"Claimed {metric}={claimed}; recomputed {metrics[metric]}")
        elif metrics[metric] != claimed:
            disagreements.append(f"Claimed {metric} differs from recomputed evidence")
    return {"metrics": metrics, "cross_split_group_count": int((overlapping_groups > 1).sum()), "cross_split_duplicate_sequence_count": int((duplicate_sequences > 1).sum()), "claim_disagreements": disagreements, "requires_manual_review": ["Is the independent group definition scientifically justified?", "Were all fitted preprocessing and model choices restricted to training and validation?", "Was the test workflow frozen before the planned reveal?", "Does model and embedding provenance match the claimed inputs?", "Do biological conclusions exceed the simulated task?"], "scope": "Recomputed evidence and identity checks only; not proof of correct training or biological validity"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("samples", type=Path)
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--split", choices=["validation", "test"], default="validation")
    parser.add_argument("--claims", type=Path)
    parser.add_argument("--output", type=Path, default=Path("course_output/audit_report.json"))
    arguments = parser.parse_args()
    claims = json.loads(arguments.claims.read_text(encoding="utf-8")) if arguments.claims else None
    report = audit_predictions(pd.read_csv(arguments.samples), pd.read_csv(arguments.predictions), arguments.split, claims)
    write_json(arguments.output, report)
    print(json.dumps(report, indent=2))
