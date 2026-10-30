"""Compare bag-of-k-mers and a small position-aware CNN without scoring test data."""

from dataclasses import asdict
from pathlib import Path
from time import perf_counter
from typing import Any
import json

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from torch import nn

from course_core import SimulationConfig, assign_splits, build_interaction_dataset, generate_course_dataset, read_dataset, save_dataset, validation_metrics, write_json, sample_hash


from course_inference import SequenceCNN, one_hot, predict_cnn


def fit_cnn(train: pd.DataFrame, validation: pd.DataFrame, seed: int, epochs: int = 24) -> tuple[SequenceCNN, list[dict[str, Any]]]:
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    model = SequenceCNN(len(train.iloc[0]["sequence"]))
    inputs = one_hot(train["sequence"])
    labels = torch.tensor(train["label"].to_numpy(), dtype=torch.float32)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)
    random = torch.Generator().manual_seed(seed)
    history = []
    best_score = -1.0
    best_state = None
    for epoch in range(epochs):
        model.train()
        permutation = torch.randperm(len(train), generator=random)
        total_loss = 0.0
        for indices in permutation.split(64):
            optimizer.zero_grad()
            loss = nn.functional.binary_cross_entropy_with_logits(model(inputs[indices]), labels[indices])
            loss.backward()
            optimizer.step()
            total_loss += float(loss.detach()) * len(indices)
        score = validation_metrics(validation["label"], predict_cnn(model, validation["sequence"]))["roc_auc"]
        history.append({"epoch": epoch + 1, "training_loss": total_loss / len(train), "validation_roc_auc": score})
        if score > best_score:
            best_score = score
            best_state = {name: value.detach().clone() for name, value in model.state_dict().items()}
    if best_state is None:
        raise RuntimeError("CNN training did not produce a selected validation checkpoint")
    model.load_state_dict(best_state)
    return model, history


def run_representations(output_dir: str | Path = "course_output", seed: int = 2026, epochs: int = 24, show_plot: bool = True) -> pd.DataFrame:
    root = Path(output_dir)
    if any((root / marker).exists() for marker in ("frozen_manifest.json", "test_results.json")):
        raise RuntimeError("Test results have been revealed. Do not tune this course experiment afterward; use a new development directory.")
    config = SimulationConfig(seed=seed)
    samples, truth = generate_course_dataset(config)
    save_dataset(root / "datasets" / "simple", assign_splits(samples, seed), truth, asdict(config))
    interaction, interaction_truth = build_interaction_dataset(seed)
    save_dataset(root / "datasets" / "interaction", interaction, interaction_truth, {"seed": seed, "pair_count": 240, "positions": [32, 80], "matching_flanks": 6, "lesson": "fixed-position motif order, not universal CNN superiority"})
    results, all_predictions, run_records = [], [], {}
    for variant in ("simple", "interaction"):
        started = perf_counter()
        dataset = read_dataset(root / "datasets" / variant)
        train = dataset.loc[dataset["split"] == "train"]
        validation = dataset.loc[dataset["split"] == "validation"]
        destination = root / "models" / variant
        destination.mkdir(parents=True, exist_ok=True)
        if variant == "interaction":
            vectorizer = CountVectorizer(analyzer="char", ngram_range=(4, 4), lowercase=False)
            features = vectorizer.fit_transform(train["sequence"])
            first_rows = train["label"].to_numpy() == 1
            if (features[first_rows] != features[~first_rows]).nnz:
                raise RuntimeError("Paired k-mer bags differ; the intended representation control is invalid")
        models = {
            "logistic_regression": LogisticRegression(max_iter=2000),
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=2),
        }
        probabilities_by_method = {}
        for name, classifier in models.items():
            pipeline = Pipeline([("kmers", CountVectorizer(analyzer="char", ngram_range=(4, 4), lowercase=False)), ("classifier", classifier)])
            pipeline.fit(train["sequence"], train["label"])
            probabilities = pipeline.predict_proba(validation["sequence"])[:, 1]
            joblib.dump(pipeline, destination / f"{name}.joblib")
            probabilities_by_method[name] = probabilities
        cnn, history = fit_cnn(train, validation, seed, epochs)
        probabilities_by_method["cnn"] = predict_cnn(cnn, validation["sequence"])
        torch.save({"state_dict": cnn.state_dict(), "sequence_length": 160}, destination / "cnn.pt")
        pd.DataFrame(history).to_csv(destination / "cnn_history.csv", index=False)
        for name, probabilities in probabilities_by_method.items():
            metrics = validation_metrics(validation["label"], probabilities)
            results.append({"variant": variant, "method": name, **metrics})
            prediction_frame = validation[["sample_id", "group_id", "label"]].copy()
            prediction_frame["probability"] = probabilities
            prediction_frame["variant"] = variant
            prediction_frame["method"] = name
            all_predictions.append(prediction_frame)
        if variant == "interaction":
            controlled = validation[["sample_id", "group_id", "label"]].copy()
            for name, probabilities in probabilities_by_method.items():
                controlled[f"{name}_probability"] = probabilities
            controlled.to_csv(destination / "controlled_order_changes.csv", index=False)
        run_records[variant] = {"dataset_sha256": sample_hash(dataset), "training_ids": train["sample_id"].tolist(), "validation_ids": validation["sample_id"].tolist(), "seconds": perf_counter() - started, "cnn_epochs": epochs, "cnn_selection": "highest validation ROC-AUC, earliest tie", "test_evaluated": False}
    result = pd.DataFrame(results)
    result.to_csv(root / "representation_validation.csv", index=False)
    pd.concat(all_predictions, ignore_index=True).to_csv(root / "representation_validation_predictions.csv", index=False)
    write_json(root / "representation_run.json", {"seed": seed, "torch_version": torch.__version__, "device": "cpu", "runs": run_records, "interpretation": "The engineered interaction pairs have identical 4-mer counts. This CNN preserves position through flattening; global pooling alone would discard that cue. Fixed positions and matching flanks are a disclosed teaching construction, not evidence of real promoter prediction."})
    figure, axis = plt.subplots(figsize=(8, 4))
    result.pivot(index="variant", columns="method", values="roc_auc").plot.bar(ax=axis, ylim=(0, 1.05), ylabel="Validation ROC-AUC", rot=0)
    axis.axhline(0.5, linestyle="--", color="gray")
    figure.tight_layout()
    figure.savefig(root / "representation_validation.png", dpi=150)
    if show_plot:
        plt.show()
    plt.close(figure)
    print(result[["variant", "method", "roc_auc", "average_precision"]].to_string(index=False))
    print("Validation only. Test data remains unscored. Paired order control is intentionally engineered.")
    return result


if __name__ == "__main__":
    run_representations()
