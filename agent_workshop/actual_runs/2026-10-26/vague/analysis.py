"""Training-only model selection for the supplied simulated DNA task."""
import os

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"

import hashlib
import importlib.metadata
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, average_precision_score, balanced_accuracy_score,
    brier_score_loss, confusion_matrix, log_loss, roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

ROOT = Path(__file__).resolve().parent
SEED = 2026
MOTIF = "TATAAATG"


def motif_features(sequences):
    return np.asarray([[int(MOTIF in sequence)] for sequence in sequences])


def composition_features(sequences):
    return np.asarray([
        [sequence.count(base) / len(sequence) for base in "ACG"]
        for sequence in sequences
    ])


def make_model(name):
    if name == "prior":
        return make_pipeline(
            FunctionTransformer(motif_features), DummyClassifier(strategy="prior")
        )
    if name == "composition":
        return make_pipeline(
            FunctionTransformer(composition_features), StandardScaler(),
            LogisticRegression(C=1.0, max_iter=2000, random_state=SEED),
        )
    if name == "disclosed_motif":
        return make_pipeline(
            FunctionTransformer(motif_features),
            LogisticRegression(C=1e6, max_iter=2000, random_state=SEED),
        )
    return make_pipeline(
        CountVectorizer(analyzer="char", ngram_range=(4, 8), binary=True,
                        lowercase=False, dtype=np.float64),
        LogisticRegression(C=float(name.split("_")[-1]), solver="liblinear",
                           max_iter=2000, random_state=SEED),
    )


def metrics(labels, probabilities):
    predicted = (probabilities >= 0.5).astype(int)
    return {
        "log_loss": float(log_loss(labels, probabilities, labels=[0, 1])),
        "roc_auc": float(roc_auc_score(labels, probabilities)),
        "average_precision": float(average_precision_score(labels, probabilities)),
        "accuracy": float(accuracy_score(labels, predicted)),
        "balanced_accuracy": float(balanced_accuracy_score(labels, predicted)),
        "brier_score": float(brier_score_loss(labels, probabilities)),
        "confusion_matrix_true_rows_0_1_predicted_columns_0_1":
            confusion_matrix(labels, predicted, labels=[0, 1]).tolist(),
    }


def read_frame(filename, split):
    frame = pd.read_csv(ROOT / filename)
    required = {"sample_id", "group_id", "sequence", "label", "split"}
    if not required.issubset(frame.columns):
        raise ValueError(f"Missing columns in {filename}")
    if frame[list(required)].isna().any().any():
        raise ValueError(f"Missing values in {filename}")
    if not frame["split"].eq(split).all():
        raise ValueError(f"Incorrect split in {filename}")
    if not frame["sequence"].str.fullmatch("[ACGT]{160}").all():
        raise ValueError(f"Invalid DNA or length in {filename}")
    if set(frame["label"].unique()) != {0, 1}:
        raise ValueError(f"Invalid labels in {filename}")
    if frame["sample_id"].duplicated().any():
        raise ValueError(f"Duplicate sample IDs in {filename}")
    return frame


def main():
    started = time.perf_counter()
    timestamp = datetime.now(timezone.utc).isoformat()
    train = read_frame("train.csv", "train")
    validation = read_frame("validation.csv", "validation")
    for column in ("sample_id", "group_id", "sequence"):
        if set(train[column]) & set(validation[column]):
            raise ValueError(f"Train/validation overlap in {column}")
    if train["sequence"].duplicated().any() or validation["sequence"].duplicated().any():
        raise ValueError("Duplicate sequences within a split")
    manifest = pd.read_csv(ROOT / "split_manifest.csv")
    for frame in (train, validation):
        expected = frame[["sample_id", "group_id", "split"]].sort_values("sample_id").reset_index(drop=True)
        observed = manifest[manifest["sample_id"].isin(frame["sample_id"])][expected.columns]
        if not expected.equals(observed.sort_values("sample_id").reset_index(drop=True)):
            raise ValueError("Supplied split does not match manifest")

    sequences = train["sequence"].to_numpy()
    labels = train["label"].to_numpy()
    folds = list(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
                 .split(sequences, labels, train["group_id"]))
    candidates = ["prior", "composition", "disclosed_motif",
                  "kmer_0.1", "kmer_1.0", "kmer_10.0"]
    results = {}
    oof_predictions = train[["sample_id", "group_id", "label"]].copy()
    for name in candidates:
        model_started = time.perf_counter()
        probabilities = np.empty(len(train))
        fold_losses = []
        for fitting, held_out in folds:
            model = make_model(name)
            model.fit(sequences[fitting], labels[fitting])
            probabilities[held_out] = model.predict_proba(sequences[held_out])[:, 1]
            fold_losses.append(float(log_loss(labels[held_out], probabilities[held_out])))
        results[name] = metrics(labels, probabilities)
        results[name]["fold_log_losses"] = fold_losses
        results[name]["cv_seconds"] = time.perf_counter() - model_started
        oof_predictions[name] = probabilities
        print(json.dumps({"candidate": name, **results[name]}), flush=True)
    selected = min(candidates, key=lambda name: (results[name]["log_loss"], name))
    print("SELECTED", selected, flush=True)
    model = make_model(selected)
    model.fit(sequences, labels)
    probabilities = model.predict_proba(validation["sequence"].to_numpy())[:, 1]
    validation_metrics = metrics(validation["label"].to_numpy(), probabilities)
    predicted = (probabilities >= 0.5).astype(int)
    sample_count = len(validation)
    proportion = float(accuracy_score(validation["label"], predicted))
    z_score = 1.959963984540054
    denominator = 1 + z_score ** 2 / sample_count
    center = (proportion + z_score ** 2 / (2 * sample_count)) / denominator
    radius = z_score * np.sqrt(proportion * (1 - proportion) / sample_count
                              + z_score ** 2 / (4 * sample_count ** 2)) / denominator
    validation_metrics["accuracy_wilson_95_interval"] = [center - radius, center + radius]
    predictions = validation[["sample_id", "group_id", "label"]].copy()
    predictions["probability_label_1"] = probabilities
    predictions["predicted_label"] = predicted
    predictions["disclosed_motif_present"] = motif_features(validation["sequence"].to_numpy()).ravel()
    predictions.to_csv(ROOT / "validation_predictions.csv", index=False)
    oof_predictions.to_csv(ROOT / "train_oof_predictions.csv", index=False)
    motif_table = {}
    for split, frame in (("train", train), ("validation", validation)):
        presence = frame["sequence"].str.contains(MOTIF, regex=False)
        motif_table[split] = pd.crosstab(frame["label"], presence).reindex(
            index=[0, 1], columns=[False, True], fill_value=0).to_numpy().tolist()
    hashes = {
        filename: hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
        for filename in ("dataset_description.txt", "train.csv", "validation.csv",
                         "split_manifest.csv", "analysis.py")
    }
    fitted_details = {}
    if selected == "disclosed_motif":
        fitted_details = {
            "motif": MOTIF,
            "probability_without_motif": float(model.predict_proba(["C" * 160])[0, 1]),
            "probability_with_motif": float(model.predict_proba([MOTIF + "C" * 152])[0, 1]),
            "coefficient": model[-1].coef_.tolist(),
            "intercept": model[-1].intercept_.tolist(),
        }
    evidence = {
        "started_utc": timestamp, "seed": SEED,
        "python": sys.version, "platform": platform.platform(),
        "versions": {package: importlib.metadata.version(package)
                     for package in ("numpy", "pandas", "scipy", "scikit-learn")},
        "input_and_source_sha256": hashes,
        "train_rows": len(train), "validation_rows": len(validation),
        "selection": "minimum pooled training-only five-fold out-of-fold log loss",
        "threshold": 0.5, "cv": results, "selected_model": selected,
        "validation": validation_metrics,
        "motif_counts_true_label_rows_0_1_absent_present_columns": motif_table,
        "fitted_details": fitted_details,
        "elapsed_seconds_excluding_imports": time.perf_counter() - started,
    }
    (ROOT / "results.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    with (ROOT / "run_report.md").open("a", encoding="utf-8") as stream:
        stream.write("\n## Executed analysis evidence\n\n")
        stream.write("Command: `$env:PYTHONDONTWRITEBYTECODE='1'; python -B analysis.py 2>&1 | Tee-Object -FilePath execution.log`\n\n")
        stream.write("Full actual stdout: `execution.log`. Structured evidence: `results.json`.\n\n")
        stream.write("```json\n" + json.dumps(evidence, indent=2) + "\n```\n")
    print("VALIDATION", json.dumps(validation_metrics), flush=True)
    print("ELAPSED_SECONDS", evidence["elapsed_seconds_excluding_imports"], flush=True)


if __name__ == "__main__":
    main()
