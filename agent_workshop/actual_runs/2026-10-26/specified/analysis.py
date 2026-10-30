"""Actual development-only simple-signal baseline: python analysis.py."""

import hashlib
import importlib.metadata
import json
import platform
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, average_precision_score, balanced_accuracy_score
from sklearn.metrics import confusion_matrix, precision_score, recall_score, roc_auc_score
from threadpoolctl import threadpool_limits


ROOT = Path(__file__).resolve().parent
SEED = 2026
THRESHOLD = 0.5
PRIMARY_METRIC = "roc_auc"
MANUAL = {"roc_auc": 0.8019444444, "average_precision": 0.8024506157}
INPUTS = ["AGENTS.md", "specification.md", "skills/scientific-audit/SKILL.md",
          "dataset_description.txt", "train.csv", "validation.csv",
          "split_manifest.csv", "simulation_truth.csv"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_table(name, columns):
    table = pd.read_csv(ROOT / name, dtype=str, keep_default_na=False)
    require(list(table.columns) == columns, f"{name}: unexpected columns")
    require(len(table) > 0, f"{name}: empty table")
    require(not table.eq("").any().any(), f"{name}: empty fields")
    require(table.sample_id.is_unique, f"{name}: duplicate sample IDs")
    return table


def align_predictions(labels, predictions):
    require(labels.sample_id.is_unique, "duplicate label IDs")
    require(list(predictions.columns) == ["sample_id", "probability"], "prediction schema")
    require(predictions.sample_id.is_unique, "duplicate prediction IDs")
    require(set(labels.sample_id) == set(predictions.sample_id), "prediction ID coverage")
    aligned = labels[["sample_id", "label"]].merge(predictions, on="sample_id", validate="one_to_one", how="left", sort=False)
    probabilities = pd.to_numeric(aligned.probability, errors="raise").to_numpy(float)
    require(np.isfinite(probabilities).all(), "nonfinite probabilities")
    require(((probabilities >= 0) & (probabilities <= 1)).all(), "probabilities outside [0,1]")
    return aligned.label.astype(int).to_numpy(), probabilities


def evaluate(labels, probabilities):
    decisions = (probabilities >= THRESHOLD).astype(int)
    both_classes = len(np.unique(labels)) == 2
    return {
        "roc_auc": float(roc_auc_score(labels, probabilities)) if both_classes else None,
        "average_precision": float(average_precision_score(labels, probabilities)) if both_classes else None,
        "accuracy": float(accuracy_score(labels, decisions)),
        "balanced_accuracy": float(balanced_accuracy_score(labels, decisions)) if both_classes else None,
        "precision": float(precision_score(labels, decisions, zero_division=0)),
        "recall": float(recall_score(labels, decisions, zero_division=0)),
        "confusion_matrix": confusion_matrix(labels, decisions, labels=[0, 1]).tolist(),
        "metric_limitations": [] if both_classes else ["One class: ROC-AUC, AP, balanced accuracy withheld."],
        "zero_division_policy": "precision/recall use 0 if denominator is zero",
    }


def inspect_inputs():
    columns = ["sample_id", "group_id", "sequence", "label", "split"]
    train = read_table("train.csv", columns)
    validation = read_table("validation.csv", columns)
    manifest = read_table("split_manifest.csv", ["sample_id", "group_id", "split"])
    truth = read_table("simulation_truth.csv", ["sample_id", "motif_planted", "motif_start"])
    for name, table in [("train", train), ("validation", validation)]:
        require(table.sequence.str.fullmatch("[ACGT]+").all(), f"{name}: invalid DNA")
        require(table.sequence.str.len().eq(160).all(), f"{name}: expected 160-base DNA")
        require(table.label.isin(["0", "1"]).all(), f"{name}: nonbinary labels")
        require(table.split.eq(name).all(), f"{name}: unexpected split")
        require(table.sample_id.str.startswith("simple-2026-").all(), f"{name}: unexpected variant")
    combined = pd.concat([train, validation], ignore_index=True)
    require(combined.sample_id.is_unique, "cross-split sample overlap")
    require(set(manifest.split) == {"train", "validation"}, "manifest: unexpected split")
    require(set(manifest.sample_id) == set(combined.sample_id), "manifest ID coverage mismatch")
    matched = combined.merge(manifest, on="sample_id", suffixes=("", "_manifest"), validate="one_to_one")
    require(matched.group_id.eq(matched.group_id_manifest).all(), "manifest group mismatch")
    require(matched.split.eq(matched.split_manifest).all(), "manifest split mismatch")
    overlap = set(train.group_id) & set(validation.group_id)
    require(not overlap, "cross-split group overlap")
    require(set(truth.sample_id) == set(combined.sample_id), "truth ID coverage mismatch")
    require(truth.motif_planted.isin(["True", "False"]).all(), "invalid motif flag")
    starts = pd.to_numeric(truth.motif_start, errors="raise")
    require((starts % 1 == 0).all(), "noninteger motif positions")
    planted = truth.motif_planted.eq("True")
    require((starts[~planted] == -1).all(), "unexpected unplanted motif position")
    require(starts[planted].between(0, 152).all(), "invalid planted motif position")
    truth = combined[["sample_id", "sequence", "label", "split"]].merge(truth, on="sample_id", validate="one_to_one")
    require(all(row.sequence[int(row.motif_start):int(row.motif_start) + 8] == "TATAAATG"
                for row in truth.itertuples() if row.motif_planted == "True"), "planted motif mismatch")
    evidence = {"cross_split_sample_overlap": 0, "cross_split_group_overlap": len(overlap),
                "manifest_exact_coverage_and_metadata_match": True,
                "truth_exact_coverage_and_planted_motif_match": True,
                "all_groups_singleton": bool(combined.group_id.is_unique), "splits": {}}
    for name, table in [("train", train), ("validation", validation)]:
        evidence["splits"][name] = {
            "samples": len(table), "groups": int(table.group_id.nunique()),
            "class_counts": {str(label): int(table.label.eq(str(label)).sum()) for label in [0, 1]},
            "positive_fraction": float(table.label.eq("1").mean()),
            "sorted_id_sha256": hashlib.sha256("\n".join(sorted(table.sample_id)).encode()).hexdigest(),
        }
    rates = truth.assign(planted=truth.motif_planted.eq("True")).groupby(["split", "label"]).planted.mean()
    evidence["observed_planted_fractions"] = {f"{split}/label_{label}": value for (split, label), value in rates.items()}
    return train, validation, evidence


def main():
    started = time.perf_counter()
    started_at = datetime.now(timezone.utc).isoformat()
    hashes = {name: digest(ROOT / name) for name in INPUTS + ["analysis.py"]}
    train, validation, input_evidence = inspect_inputs()
    inspected_at = time.perf_counter()
    require(train.label.nunique() == 2, "training requires both classes; stop before fitting")
    vectorizer = CountVectorizer(analyzer="char", ngram_range=(4, 4), lowercase=False)
    classifier = LogisticRegression(max_iter=2000, random_state=SEED)
    configuration = {
        "variant": "simple-signal", "primary_metric": PRIMARY_METRIC, "threshold": THRESHOLD,
        "seed": SEED, "feature_input": "sequence only", "CPU_thread_limit": 1,
        "vectorizer": vectorizer.get_params(), "classifier": classifier.get_params(),
        "manual_configuration_comparison_before_evaluation": "Specified 4-mer counts, lowercase=False, max_iter=2000 and seed=2026 match. Unspecified settings use installed sklearn defaults. Manual versions, solver, C, tolerance, source and predictions were not supplied and cannot be verified. No tuning or alternative fits.",
    }
    configuration["vectorizer"]["dtype"] = str(configuration["vectorizer"]["dtype"])
    print("DECLARED BEFORE FIT/EVALUATION:", json.dumps(configuration, sort_keys=True), flush=True)
    with threadpool_limits(limits=1), warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        train_features = vectorizer.fit_transform(train.sequence)
        validation_features = vectorizer.transform(validation.sequence)
        classifier.fit(train_features, train.label.astype(int))
        fitted_at = time.perf_counter()
        positive_column = int(np.flatnonzero(classifier.classes_ == 1)[0])
        probabilities = classifier.predict_proba(validation_features)[:, positive_column]
    require(not any(issubclass(item.category, ConvergenceWarning) for item in recorded), "classifier failed to converge")
    prediction_path = ROOT / "validation_predictions_simple_signal_4mer_logreg.csv"
    pd.DataFrame({"sample_id": validation.sample_id, "probability": probabilities}).to_csv(prediction_path, index=False)
    predictions = pd.read_csv(prediction_path, dtype={"sample_id": str}, float_precision="round_trip")
    labels, aligned_probabilities = align_predictions(validation, predictions)
    metrics = evaluate(labels, aligned_probabilities)
    shuffled_labels, shuffled_probabilities = align_predictions(validation, predictions.sample(frac=1, random_state=SEED))
    require(np.array_equal(labels, shuffled_labels) and np.array_equal(aligned_probabilities, shuffled_probabilities), "alignment depends on prediction order")
    results = {
        "execution_type": "actual local CPU run, not illustrative", "started_at_UTC": started_at,
        "command": "python analysis.py", "configuration": configuration,
        "versions": {"python": sys.version, "platform": platform.platform(), **{name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scipy", "scikit-learn", "threadpoolctl"]}},
        "sha256": hashes, "input_checks": input_evidence, "validation_metrics": metrics,
        "manual_metrics_user_supplied": MANUAL,
        "agent_minus_manual": {name: metrics[name] - value if metrics[name] is not None else None for name, value in MANUAL.items()},
        "fit_evidence": {"training_feature_shape": list(train_features.shape), "validation_feature_shape": list(validation_features.shape), "vocabulary_fit_samples": len(train), "classifier_fit_samples": len(train), "iterations": classifier.n_iter_.tolist(), "warnings": [str(item.message) for item in recorded]},
        "prediction_evidence": {"file": prediction_path.name, "sha256": digest(prediction_path), "rows": len(predictions), "unique_exact_validation_ID_coverage": True, "finite_unit_interval": True, "label_1_probabilities": True, "shuffled_prediction_alignment_unchanged": True},
        "timings_seconds": {"input_inspection": inspected_at - started, "feature_extraction_and_fit": fitted_at - inspected_at, "through_prediction_reload_and_evaluation": time.perf_counter() - started},
    }
    (ROOT / "evaluation_report.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sections = ["# Actual development-only run report",
        f"Started (UTC): {started_at}. Actual local CPU execution, not illustrative. Only simple-signal supplied.",
        "## Prespecified workflow and decisions",
        "ROC-AUC primary; AP secondary; threshold probability >= 0.5. Exactly one fit, no tuning. Sequence only; vocabulary and classifier fit training only; validation transform/predict only. Simulation truth audited, never input to model or selection. Fixed manifest checked, not replaced.",
        configuration["manual_configuration_comparison_before_evaluation"],
        "## Actual validation and provenance", "```json\n" + json.dumps(results, indent=2, sort_keys=True) + "\n```",
        "Confusion matrix rows=true [0,1], columns=predicted [0,1]. Manual aggregate scores are user-supplied for these fixed IDs; without manual predictions or ID digest that identity claim cannot independently be verified. Timing excludes final report serialization. Re-running overwrites generated reports/predictions.",
        "## Evaluation boundary and limitations",
        "No network calls, commits, paid services, protected test reads or other run outputs used in this session. This session access record is not proof of the historical manual test boundary. No test performance reported; revealed test evidence is not fresh evaluation for this run.",
        "Supplied description: simulated 160-base DNA, TATAAATG planting probabilities 0.9 for label 1 and 0.1 for label 0, uniform background, generator seed 2026, singleton independent groups. Observed planting fractions reported, not forced to nominal values. Group checks do not prove real-world biological independence. No claims of real promoter recognition, discovery, general grammar, test generalization or universal model superiority. Future model selection needs an agreed independent test for final assessment.",
        "No interaction variant, leakage exercise, CNN or embeddings executed. The specified interaction control uses fixed-position motif order, matching flanks and identical 4-mer bags: bag counts cannot distinguish identical feature vectors with opposite labels. No measured interaction result or CNN/pretrained-model advantage claimed.",
        "Scientific audit: scientific_audit.md. Full evidence: evaluation_report.json. Command history and verification are in the appended execution record."]
    (ROOT / "run_report.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    print(json.dumps({key: results[key] for key in ["validation_metrics", "agent_minus_manual", "timings_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
