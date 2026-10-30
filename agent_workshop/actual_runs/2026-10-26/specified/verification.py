"""Independent output checks and in-memory malformed-input probes; no model fitting."""

import json
import time

import numpy as np
import pandas as pd

import analysis


def main():
    started = time.perf_counter()
    report = json.loads((analysis.ROOT / "evaluation_report.json").read_text(encoding="utf-8"))
    for name, expected in report["sha256"].items():
        analysis.require(analysis.digest(analysis.ROOT / name) == expected, f"changed input/source: {name}")
    train, validation, checks = analysis.inspect_inputs()
    predictions = pd.read_csv(analysis.ROOT / report["prediction_evidence"]["file"], float_precision="round_trip")
    labels, probabilities = analysis.align_predictions(validation, predictions)
    positives = probabilities[labels == 1]
    negatives = probabilities[labels == 0]
    pairwise_auc = float(((positives[:, None] > negatives).sum() + 0.5 * (positives[:, None] == negatives).sum()) / (len(positives) * len(negatives)))
    order = np.argsort(-probabilities, kind="stable")
    sorted_labels = labels[order]
    sorted_scores = probabilities[order]
    boundaries = np.r_[np.flatnonzero(np.diff(sorted_scores)), len(labels) - 1]
    true_positives = np.cumsum(sorted_labels)[boundaries]
    precision = true_positives / (boundaries + 1)
    recall_increments = np.diff(np.r_[0, true_positives]) / labels.sum()
    independent_ap = float(np.sum(precision * recall_increments))
    analysis.require(np.isclose(pairwise_auc, report["validation_metrics"]["roc_auc"], atol=1e-14, rtol=0), "independent AUC mismatch")
    analysis.require(np.isclose(independent_ap, report["validation_metrics"]["average_precision"], atol=1e-14, rtol=0), "independent AP mismatch")
    passed = []
    invalid_predictions = {
        "duplicate_prediction_ID": pd.concat([predictions, predictions.iloc[:1]], ignore_index=True),
        "missing_prediction_ID": predictions.iloc[1:].copy(),
        "extra_prediction_ID": pd.concat([predictions, pd.DataFrame({"sample_id": ["not-a-supplied-ID"], "probability": [0.5]})], ignore_index=True),
        "nonfinite_probability": predictions.assign(probability=np.nan),
        "out_of_range_probability": predictions.assign(probability=1.01),
    }
    for name, malformed in invalid_predictions.items():
        try:
            analysis.align_predictions(validation, malformed)
        except ValueError as error:
            passed.append({"probe": name, "rejected": str(error)})
        else:
            raise AssertionError(f"accepted {name}")
    original_reader = analysis.read_table
    mutations = {
        "lowercase_DNA": ("train.csv", "sequence", "a" * 160),
        "nonbinary_label": ("train.csv", "label", "2"),
        "wrong_split": ("validation.csv", "split", "train"),
        "manifest_group_mismatch": ("split_manifest.csv", "group_id", "altered-group"),
        "truth_motif_position_mismatch": ("simulation_truth.csv", "motif_start", "999"),
    }
    for name, (target, column, value) in mutations.items():
        def malformed_reader(filename, columns):
            table = original_reader(filename, columns)
            if filename == target:
                table.loc[table.index[0], column] = value
            return table
        analysis.read_table = malformed_reader
        try:
            analysis.inspect_inputs()
        except ValueError as error:
            passed.append({"probe": name, "rejected": str(error)})
        else:
            raise AssertionError(f"accepted {name}")
        finally:
            analysis.read_table = original_reader
    one_class = analysis.evaluate(np.zeros(4, dtype=int), np.array([0.1, 0.2, 0.3, 0.4]))
    analysis.require(all(one_class[name] is None for name in ["roc_auc", "average_precision", "balanced_accuracy"]), "single-class metric policy")
    decisions = probabilities >= 0.5
    matrix = [[int(((labels == actual) & (decisions == predicted)).sum()) for predicted in [0, 1]] for actual in [0, 1]]
    analysis.require(matrix == report["validation_metrics"]["confusion_matrix"], "confusion matrix mismatch")
    output = {
        "command": "python -B verification.py", "verification_source_sha256": analysis.digest(analysis.ROOT / "verification.py"),
        "input_and_analysis_hashes_unchanged": True, "independent_pairwise_ROC_AUC": pairwise_auc,
        "independent_threshold_grouped_AP": independent_ap, "independent_confusion_matrix": matrix,
        "negative_probes": passed, "single_class_limitations_checked": True,
        "probe_scope": "Malformed copies in memory only; development CSVs unchanged; no fitting, tuning or new model.",
        "input_evidence": checks, "elapsed_seconds": time.perf_counter() - started,
    }
    (analysis.ROOT / "verification_results.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
