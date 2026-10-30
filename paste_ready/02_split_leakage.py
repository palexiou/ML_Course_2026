"""Standalone related-sequence leakage investigation; paste into one Colab cell."""

from dataclasses import asdict, dataclass
from importlib.metadata import version
from pathlib import Path
from time import perf_counter
import json
import platform

IMPORT_STARTED = perf_counter()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import (
    ConfusionMatrixDisplay, accuracy_score, average_precision_score,
    balanced_accuracy_score, confusion_matrix, precision_score,
    recall_score, roc_auc_score,
)
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

IMPORT_SECONDS = perf_counter() - IMPORT_STARTED


@dataclass(frozen=True)
class LeakageConfig:
    seed: int = 2026
    family_count: int = 240
    sequences_per_family: int = 6
    sequence_length: int = 160
    mutations_per_sequence: int = 1
    kmer_length: int = 6
    validation_fraction: float = 0.25

    def __post_init__(self) -> None:
        if not 0 <= self.seed < 2**32:
            raise ValueError("seed must be between 0 and 2**32 - 1")
        if self.family_count < 20 or self.family_count % 2:
            raise ValueError("family_count must be even and at least 20")
        if self.sequences_per_family < 2:
            raise ValueError("sequences_per_family must be at least 2")
        if not 1 <= self.kmer_length <= self.sequence_length:
            raise ValueError("kmer_length must be between 1 and sequence_length")
        if not 0 <= self.mutations_per_sequence <= self.sequence_length:
            raise ValueError("mutations_per_sequence must be between 0 and sequence_length")
        if not 0 < self.validation_fraction < 1:
            raise ValueError("validation_fraction must be between 0 and 1")


def generate_leakage_dataset(config: LeakageConfig) -> pd.DataFrame:
    background_seed, label_seed, mutation_seed = np.random.SeedSequence(config.seed).spawn(3)
    background_random = np.random.default_rng(background_seed)
    label_random = np.random.default_rng(label_seed)
    mutation_random = np.random.default_rng(mutation_seed)
    alphabet = np.array(list("ACGT"))
    backgrounds = background_random.integers(0, 4, size=(config.family_count, config.sequence_length))
    family_labels = np.repeat([0, 1], config.family_count // 2)
    label_random.shuffle(family_labels)
    records = []
    for family_index, background in enumerate(backgrounds):
        for member_index in range(config.sequences_per_family):
            sequence = background.copy()
            positions = mutation_random.choice(
                config.sequence_length, config.mutations_per_sequence, replace=False
            )
            sequence[positions] = (
                sequence[positions]
                + mutation_random.integers(1, 4, size=config.mutations_per_sequence)
            ) % 4
            records.append({
                "sample_id": f"leakage-{config.seed}-{family_index:04d}-{member_index:02d}",
                "group_id": f"family-{family_index:04d}",
                "sequence": "".join(alphabet[sequence]),
                "label": int(family_labels[family_index]),
            })
    return pd.DataFrame(records)


def assign_split_indices(samples: pd.DataFrame, config: LeakageConfig) -> dict:
    row_indices = train_test_split(
        np.arange(len(samples)), test_size=config.validation_fraction,
        stratify=samples["label"], random_state=config.seed,
    )
    group_splitter = GroupShuffleSplit(
        n_splits=1, test_size=config.validation_fraction, random_state=config.seed
    )
    group_indices = next(group_splitter.split(samples, groups=samples["group_id"]))
    return {"flawed_row_split": row_indices, "corrected_group_split": group_indices}


def evaluate_split(samples, train_indices, validation_indices, split_name, config, output_dir):
    started = perf_counter()
    training = samples.iloc[train_indices]
    validation = samples.iloc[validation_indices]
    assert set(train_indices).isdisjoint(validation_indices)
    assert len(train_indices) + len(validation_indices) == len(samples)
    training_families = set(training["group_id"])
    validation_families = set(validation["group_id"])
    overlapping_families = training_families & validation_families
    if split_name == "flawed_row_split":
        assert len(overlapping_families) > 0, "The flawed split must expose family overlap"
    else:
        assert len(overlapping_families) == 0, "The corrected split must separate families"
    if training["label"].nunique() != 2 or validation["label"].nunique() != 2:
        raise ValueError("Both labels are needed in each partition; inspect the configuration")
    model = Pipeline([
        ("kmers", CountVectorizer(
            analyzer="char", ngram_range=(config.kmer_length, config.kmer_length), lowercase=False,
        )),
        ("classifier", KNeighborsClassifier(n_neighbors=1, metric="cosine", algorithm="brute")),
    ])
    model.fit(training["sequence"], training["label"])
    positive_class_index = int(np.flatnonzero(model.classes_ == 1)[0])
    probabilities = model.predict_proba(validation["sequence"])[:, positive_class_index]
    predicted_labels = (probabilities >= 0.5).astype(int)
    validation_features = model.named_steps["kmers"].transform(validation["sequence"])
    distances, neighbor_indices = model.named_steps["classifier"].kneighbors(validation_features)
    nearest_training = training.iloc[neighbor_indices[:, 0]]
    predictions = validation[["sample_id", "group_id", "label"]].copy()
    predictions["predicted_label"] = predicted_labels
    predictions["probability"] = probabilities
    predictions["family_seen_in_training"] = validation["group_id"].isin(training_families)
    predictions["nearest_training_sample_id"] = nearest_training["sample_id"].to_numpy()
    predictions["nearest_training_group_id"] = nearest_training["group_id"].to_numpy()
    predictions["nearest_training_cosine_distance"] = distances[:, 0]
    predictions["nearest_training_same_family"] = (
        predictions["group_id"] == predictions["nearest_training_group_id"]
    )
    metrics = {
        "split": split_name,
        "training_rows": len(training), "validation_rows": len(validation),
        "training_families": len(training_families), "validation_families": len(validation_families),
        "group_overlap_count": len(overlapping_families),
        "sample_overlap_count": len(set(training["sample_id"]) & set(validation["sample_id"])),
        "validation_rows_with_seen_family": int(predictions["family_seen_in_training"].sum()),
        "nearest_training_same_family_fraction": float(predictions["nearest_training_same_family"].mean()),
        "training_positive_fraction": float(training["label"].mean()),
        "validation_positive_fraction": float(validation["label"].mean()),
        "accuracy": float(accuracy_score(validation["label"], predicted_labels)),
        "balanced_accuracy": float(balanced_accuracy_score(validation["label"], predicted_labels)),
        "roc_auc": float(roc_auc_score(validation["label"], probabilities)),
        "average_precision": float(average_precision_score(validation["label"], probabilities)),
        "precision": float(precision_score(validation["label"], predicted_labels, zero_division=0)),
        "recall": float(recall_score(validation["label"], predicted_labels, zero_division=0)),
        "confusion_matrix": confusion_matrix(validation["label"], predicted_labels, labels=[0, 1]).tolist(),
        "vocabulary_size": len(model.named_steps["kmers"].vocabulary_),
        "fit_and_evaluate_seconds": perf_counter() - started,
    }
    case_dir = output_dir / split_name
    case_dir.mkdir(parents=True, exist_ok=True)
    manifest = samples[["sample_id", "group_id", "label"]].copy()
    manifest["split"] = "train"
    manifest.loc[validation.index, "split"] = "validation"
    manifest.to_csv(case_dir / "split_manifest.csv", index=False)
    predictions.to_csv(case_dir / "validation_predictions.csv", index=False)
    (case_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics, predictions


def save_plots(results, predictions, output_dir, show_plot):
    figure, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    for axis, metric in zip(axes, ["balanced_accuracy", "roc_auc"]):
        axis.bar(["Flawed row split", "Corrected group split"], [result[metric] for result in results])
        axis.axhline(0.5, color="black", linestyle="--", label="Chance reference")
        axis.set(title=metric.replace("_", " ").title(), ylim=(0, 1.05), ylabel="Validation score")
        axis.legend()
    figure.savefig(output_dir / "validation_comparison.png", dpi=150)
    figure, axes = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)
    for axis, result in zip(axes, results):
        ConfusionMatrixDisplay(np.asarray(result["confusion_matrix"]), display_labels=[0, 1]).plot(
            ax=axis, colorbar=False
        )
        axis.set_title(result["split"].replace("_", " "))
    figure.savefig(output_dir / "confusion_matrices.png", dpi=150)
    figure, axis = plt.subplots(figsize=(7, 4), constrained_layout=True)
    for result, prediction_table in zip(results, predictions):
        axis.hist(
            prediction_table["nearest_training_cosine_distance"], bins=np.linspace(0, 1, 31).tolist(),
            alpha=0.65, label=result["split"],
        )
    axis.set(xlabel="Cosine distance to nearest training sequence", ylabel="Validation rows")
    axis.legend()
    figure.savefig(output_dir / "nearest_training_distances.png", dpi=150)
    if show_plot:
        plt.show()
    plt.close("all")


def run(output_dir="course_output/leakage", show_plot=False, config=None):
    started = perf_counter()
    config = config or LeakageConfig()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    samples = generate_leakage_dataset(config)
    samples.to_csv(output_dir / "dataset.csv", index=False)
    results = []
    predictions = []
    for split_name, (train_indices, validation_indices) in assign_split_indices(samples, config).items():
        metrics, prediction_table = evaluate_split(
            samples, train_indices, validation_indices, split_name, config, output_dir
        )
        results.append(metrics)
        predictions.append(prediction_table)
    save_plots(results, predictions, output_dir, show_plot)
    comparison = pd.DataFrame(results).drop(columns="confusion_matrix")
    comparison.to_csv(output_dir / "metrics_comparison.csv", index=False)
    metadata = {
        "config": asdict(config), "python": platform.python_version(),
        "packages": {package: version(package) for package in ["numpy", "pandas", "scikit-learn", "matplotlib"]},
        "primary_metric": "balanced_accuracy",
        "model": "1-nearest-neighbor, cosine distance, raw character k-mer counts",
        "decision_threshold": 0.5,
        "label_generation": "Balanced random family labels independent of family background sequences",
        "protected_course_test_data_used": False,
        "import_seconds": IMPORT_SECONDS,
        "run_seconds_excluding_imports": perf_counter() - started,
        "interpretation": "Family memorization demonstration, not a true motif signal or biological discovery",
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(comparison[["split", "group_overlap_count", "balanced_accuracy", "roc_auc"]].to_string(index=False))
    print("Random family labels: inspect overlap and nearest-family evidence, not a guaranteed score gap.")
    print(f"Saved standalone leakage outputs to {output_dir.resolve()}")
    return comparison


if __name__ == "__main__":
    run()
