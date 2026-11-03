"""A standalone simulated DNA classification experiment for a script or Colab cell."""

from importlib.metadata import version
from pathlib import Path
from time import perf_counter
from typing import Any
import hashlib
import json
import platform

IMPORTS_STARTED = perf_counter()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

IMPORT_SECONDS = perf_counter() - IMPORTS_STARTED
PRIMARY_METRIC = "roc_auc"
DECISION_THRESHOLD = 0.5


from course_core import SimulationConfig, generate_course_dataset, assign_splits, validation_metrics, write_json, save_dataset, simulation_settings, settings_fingerprint, expected_motif_kmers


def run_experiment(
    output_dir: str | Path = "simple_signal_output",
    config: SimulationConfig | None = None,
    show_plot: bool = True,
) -> dict[str, Any]:
    started = perf_counter()
    config = config if config is not None else SimulationConfig()
    destination = Path(output_dir)
    if any((destination / marker).exists() for marker in ("frozen_manifest.json", "test_results.json")):
        raise RuntimeError("This experiment is frozen or revealed. Use a new development directory.")
    destination.mkdir(parents=True, exist_ok=True)
    samples, truth = generate_course_dataset(config)
    samples = assign_splits(samples, config.seed)
    train = samples.loc[samples["split"] == "train"]
    validation = samples.loc[samples["split"] == "validation"]
    generation_seconds = perf_counter() - started

    pipeline = Pipeline(
        [
            (
                "kmers",
                CountVectorizer(
                    analyzer="char",
                    ngram_range=(config.kmer_length, config.kmer_length),
                    lowercase=False,
                ),
            ),
            ("classifier", LogisticRegression(max_iter=2000)),
        ]
    )
    fit_started = perf_counter()
    pipeline.fit(train["sequence"], train["label"])
    fit_seconds = perf_counter() - fit_started
    evaluation_started = perf_counter()
    probabilities = pipeline.predict_proba(validation["sequence"])[:, 1]
    predictions = (probabilities >= DECISION_THRESHOLD).astype(int)
    metrics = {
        "primary_metric": PRIMARY_METRIC,
        "primary_metric_reason": "Ranking discrimination on balanced simulated labels; fixed before fitting.",
        "evaluation_split": "validation",
        "decision_threshold": DECISION_THRESHOLD,
        "sample_count": len(validation),
        "positive_prevalence": float(validation["label"].mean()),
        "roc_auc": float(roc_auc_score(validation["label"], probabilities)),
        "average_precision": float(average_precision_score(validation["label"], probabilities)),
        "accuracy": float(accuracy_score(validation["label"], predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(validation["label"], predictions)),
        "precision": float(precision_score(validation["label"], predictions, zero_division=0)),
        "recall": float(recall_score(validation["label"], predictions, zero_division=0)),
        "confusion_matrix": confusion_matrix(validation["label"], predictions, labels=[0, 1]).tolist(),
    }
    evaluation_seconds = perf_counter() - evaluation_started

    save_dataset(destination, samples, truth, simulation_settings(config))
    validation_predictions = validation[["sample_id", "label"]].copy()
    validation_predictions["probability"] = probabilities
    validation_predictions["prediction"] = predictions
    validation_predictions.to_csv(destination / "validation_predictions.csv", index=False)
    (destination / "validation_metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
    vectorizer = pipeline.named_steps["kmers"]
    classifier = pipeline.named_steps["classifier"]
    annotations = expected_motif_kmers(config, vectorizer.get_feature_names_out())
    pd.DataFrame(
        {"kmer": vectorizer.get_feature_names_out(), "coefficient": classifier.coef_[0]}
    ).merge(annotations, on="kmer", how="left").sort_values("coefficient", ascending=False).to_csv(
        destination / "kmer_coefficients.csv", index=False
    )

    forest = RandomForestClassifier(n_estimators=100, random_state=config.seed, n_jobs=2)
    forest_started = perf_counter()
    forest.fit(vectorizer.transform(train["sequence"]), train["label"])
    forest_fit_seconds = perf_counter() - forest_started
    forest_probabilities = forest.predict_proba(vectorizer.transform(validation["sequence"]))[:, 1]
    forest_metrics = validation_metrics(validation["label"], forest_probabilities)
    write_json(destination / "random_forest_validation_metrics.json", forest_metrics)
    forest_predictions = validation[["sample_id", "group_id", "label"]].copy()
    forest_predictions["probability"] = forest_probabilities
    forest_predictions.to_csv(destination / "random_forest_validation_predictions.csv", index=False)
    importance = pd.DataFrame({"kmer": vectorizer.get_feature_names_out(), "importance": forest.feature_importances_})
    importance = importance.merge(annotations, on="kmer", how="left")
    importance.sort_values("importance", ascending=False).to_csv(destination / "random_forest_importance.csv", index=False)
    comparison = pd.DataFrame([{"method": "logistic_regression", **metrics}, {"method": "random_forest", **forest_metrics}])
    comparison.to_csv(destination / "classical_validation.csv", index=False)

    figure, axes = plt.subplots(1, 3, figsize=(15, 4))
    ConfusionMatrixDisplay.from_predictions(
        validation["label"], predictions, labels=[0, 1], ax=axes[0], colorbar=False
    )
    axes[0].set_title("Validation confusion matrix (threshold 0.5)")
    RocCurveDisplay.from_predictions(
        validation["label"], probabilities, ax=axes[1], plot_chance_level=True
    )
    axes[1].set_title("Validation ROC curve")
    PrecisionRecallDisplay.from_predictions(
        validation["label"], probabilities, ax=axes[2], plot_chance_level=True
    )
    axes[2].set_title("Validation precision-recall curve (AP)")
    figure.tight_layout()
    figure.savefig(destination / "validation_curves.png", dpi=150)

    metadata = {
        "dataset_variant": "simple_signal",
        "simulation": simulation_settings(config),
        "settings_sha256": settings_fingerprint(simulation_settings(config)),
        "simulation_limitations": "Independent uniform-background sequences, not real promoters. Labels define a planted-motif mixture; motif presence is not a deterministic label rule.",
        "group_policy": "Each independently generated sequence is a singleton group; this does not infer biological homology.",
        "truth_policy": "motif_planted records deliberate insertion, not a scan or consensus match. Unplanted start/site are null. Truth fields are never model inputs.",
        "kmer_annotation": "motif_window_probability is the mean product of PPM probabilities across the 15-k+1 wholly internal windows. Enrichment divides by uniform-background probability 4^-k. Boundary windows and label mixtures are excluded; undefined for k>15. All words have positive probability, so there is no binary motif membership.",
        "split_counts": {name: int(count) for name, count in samples["split"].value_counts().items()},
        "split_policy": "Stratified 60/20/20 with recorded sample identities; reuse the manifest across representations.",
        "feature_fit_split": "train",
        "feature_count": len(vectorizer.get_feature_names_out()),
        "classifier_parameters": classifier.get_params(),
        "random_forest_parameters": forest.get_params(),
        "importance_caution": "Impurity-based importance is not causal evidence or proof of a biological motif; correlated overlapping k-mers share signal.",
        "protected_test_evaluated": False,
        "test_policy": "Exported for the planned Day 3 comparison only. File separation is a teaching convention, not an access-control boundary.",
        "dataset_sha256": hashlib.sha256(
            samples.to_csv(index=False, lineterminator="\n").encode("utf-8")
        ).hexdigest(),
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "packages": {
                name: version(name)
                for name in ("numpy", "pandas", "scikit-learn", "scipy", "matplotlib", "joblib", "threadpoolctl")
            },
        },
        "timing_seconds": {
            "imports": IMPORT_SECONDS,
            "generation_and_split": generation_seconds,
            "fit": fit_seconds,
            "random_forest_fit": forest_fit_seconds,
            "validation_evaluation": evaluation_seconds,
            "total": perf_counter() - started + IMPORT_SECONDS,
        },
    }
    (destination / "experiment_metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print("SIMULATION: simplified DNA classification, not real promoter recognition.")
    print("Primary metric chosen before fitting: validation ROC-AUC.")
    print(json.dumps(metrics, indent=2))
    print(comparison[["method", "roc_auc", "average_precision"]].to_string(index=False))
    print("Protected test sequences exported but NOT evaluated. Do not tune against them.")
    print(f"Artifacts: {destination.resolve()}")
    if show_plot:
        plt.show()
    plt.close(figure)
    return metrics


if __name__ == "__main__":
    run_experiment()
