"""Shared simulation, evaluation, and artifact contracts for the course."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import hashlib
import json

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, average_precision_score, balanced_accuracy_score, confusion_matrix, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

@dataclass(frozen=True)
class SimulationConfig:
    seed: int = 2026
    sample_count: int = 1200
    sequence_length: int = 160
    motif: str = "TATAAATG"
    positive_plant_probability: float = 0.9
    negative_plant_probability: float = 0.1
    kmer_length: int = 4

    def __post_init__(self) -> None:
        if not 0 <= self.seed < 2**32:
            raise ValueError("seed must be between 0 and 2**32 - 1")
        if self.sample_count < 20 or self.sample_count % 2:
            raise ValueError("sample_count must be an even integer of at least 20")
        if not self.motif or not set(self.motif) <= set("ACGT"):
            raise ValueError("motif must be a nonempty uppercase DNA sequence")
        if self.sequence_length < len(self.motif):
            raise ValueError("sequence_length must be at least the motif length")
        if not 1 <= self.kmer_length <= self.sequence_length:
            raise ValueError("kmer_length must be between 1 and sequence_length")
        for probability in (
            self.positive_plant_probability,
            self.negative_plant_probability,
        ):
            if not 0 <= probability <= 1:
                raise ValueError("motif planting probabilities must be between 0 and 1")


def generate_course_dataset(
    config: SimulationConfig,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    random = np.random.default_rng(config.seed)
    labels = np.repeat([0, 1], config.sample_count // 2)
    random.shuffle(labels)
    sequences = random.choice(list("ACGT"), size=(config.sample_count, config.sequence_length))
    planting_probabilities = np.where(
        labels == 1,
        config.positive_plant_probability,
        config.negative_plant_probability,
    )
    planted = random.random(config.sample_count) < planting_probabilities
    starts = np.full(config.sample_count, -1, dtype=int)
    for index in np.flatnonzero(planted):
        start = int(random.integers(0, config.sequence_length - len(config.motif) + 1))
        sequences[index, start : start + len(config.motif)] = list(config.motif)
        starts[index] = start
    sample_ids = [f"simple-{config.seed}-{index:05d}" for index in range(config.sample_count)]
    samples = pd.DataFrame(
        {
            "sample_id": sample_ids,
            "group_id": sample_ids,
            "sequence": ["".join(sequence) for sequence in sequences],
            "label": labels,
        }
    )
    if samples["sequence"].duplicated().any():
        raise ValueError("The independent-sample variant contains duplicate sequences")
    truth = pd.DataFrame(
        {"sample_id": sample_ids, "motif_planted": planted, "motif_start": starts}
    )
    return samples, truth


def assign_splits(samples: pd.DataFrame, seed: int) -> pd.DataFrame:
    train_indices, heldout_indices = train_test_split(
        samples.index,
        test_size=0.4,
        stratify=samples["label"],
        random_state=seed,
    )
    validation_indices, test_indices = train_test_split(
        heldout_indices,
        test_size=0.5,
        stratify=samples.loc[heldout_indices, "label"],
        random_state=seed,
    )
    result = samples.copy()
    result["split"] = "train"
    result.loc[validation_indices, "split"] = "validation"
    result.loc[test_indices, "split"] = "test"
    if result.groupby("group_id")["split"].nunique().max() != 1:
        raise ValueError("Related sequences cross split boundaries")
    if len(train_indices) + len(validation_indices) + len(test_indices) != len(result):
        raise ValueError("Splits do not cover the course dataset")
    return result



def classification_metrics(labels: Any, probabilities: Any, evaluation_split: str) -> dict[str, Any]:
    if evaluation_split not in {"validation", "test"}:
        raise ValueError("Evaluation split must be validation or test")
    if not np.isfinite(probabilities).all() or np.any(np.asarray(probabilities) < 0) or np.any(np.asarray(probabilities) > 1):
        raise ValueError("Probabilities must be finite and between zero and one")
    predictions = (np.asarray(probabilities) >= 0.5).astype(int)
    return {
        "evaluation_split": evaluation_split, "primary_metric": "roc_auc", "decision_threshold": 0.5,
        "sample_count": len(labels), "roc_auc": float(roc_auc_score(labels, probabilities)),
        "average_precision": float(average_precision_score(labels, probabilities)),
        "accuracy": float(accuracy_score(labels, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(labels, predictions)),
        "precision": float(precision_score(labels, predictions, zero_division=0)),
        "recall": float(recall_score(labels, predictions, zero_division=0)),
        "confusion_matrix": confusion_matrix(labels, predictions, labels=[0, 1]).tolist(),
    }


def validation_metrics(labels: Any, probabilities: Any) -> dict[str, Any]:
    return classification_metrics(labels, probabilities, "validation")


def write_json(path: str | Path, value: Any) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def file_hash(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sample_hash(samples: pd.DataFrame) -> str:
    return hashlib.sha256(samples.to_csv(index=False, lineterminator="\n").encode()).hexdigest()


def save_dataset(root: str | Path, samples: pd.DataFrame, truth: pd.DataFrame, settings: dict[str, Any]) -> None:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    for split, filename in (("train", "train.csv"), ("validation", "validation.csv"), ("test", "protected_test.csv")):
        samples.loc[samples["split"] == split].to_csv(root / filename, index=False)
    samples[["sample_id", "group_id", "split"]].to_csv(root / "split_manifest.csv", index=False)
    truth.to_csv(root / "simulation_truth.csv", index=False)
    write_json(root / "generation.json", {"settings": settings, "dataset_sha256": sample_hash(samples)})


def read_dataset(root: str | Path, include_test_labels: bool = False) -> pd.DataFrame:
    root = Path(root)
    partitions = []
    for split, filename in (("train", "train.csv"), ("validation", "validation.csv"), ("test", "protected_test.csv")):
        if split == "test" and not include_test_labels:
            partition = pd.read_csv(root / filename, usecols=lambda column: column != "label")
            partition["label"] = np.nan
        else:
            partition = pd.read_csv(root / filename)
        required = {"sample_id", "group_id", "sequence", "label", "split"}
        non_null = required - ({"label"} if split == "test" and not include_test_labels else set())
        if not required <= set(partition) or partition[list(non_null)].isna().any().any():
            raise ValueError("Dataset columns are missing or contain null values")
        labels_expected = split != "test" or include_test_labels
        if partition.empty or not partition["split"].eq(split).all() or (labels_expected and set(partition["label"]) != {0, 1}):
            raise ValueError("A partition has an incorrect split or lacks both binary classes")
        partitions.append(partition)
    samples = pd.concat(partitions, ignore_index=True)
    if not samples["sample_id"].is_unique or not samples["sequence"].map(lambda sequence: bool(sequence) and set(sequence) <= set("ACGT")).all():
        raise ValueError("Dataset IDs or DNA sequences are invalid")
    if samples.groupby("group_id")["split"].nunique().max() != 1:
        raise ValueError("Related sequences cross split boundaries")
    if samples.groupby("sequence")["split"].nunique().max() != 1:
        raise ValueError("Duplicate DNA sequences cross split boundaries")
    manifest = pd.read_csv(root / "split_manifest.csv")
    expected = samples[["sample_id", "group_id", "split"]].sort_values("sample_id").reset_index(drop=True)
    actual = manifest.sort_values("sample_id").reset_index(drop=True)
    if not expected.equals(actual):
        raise ValueError("Split manifest does not match sample identities")
    return samples


def build_interaction_dataset(seed: int = 2026, pair_count: int = 240) -> tuple[pd.DataFrame, pd.DataFrame]:
    if pair_count < 20:
        raise ValueError("At least 20 independent pairs are required")
    random = np.random.default_rng(seed)
    motif_first, motif_second = "TATAAATG", "CGGACGTC"
    flank_left, flank_right = "GGGGGG", "CCCCCC"
    positions = (32, 80)
    records, truth = [], []
    for pair_index in range(pair_count):
        background = random.choice(list("ACGT"), size=160)
        group = f"order-{seed}-{pair_index:05d}"
        for label, motifs in ((1, (motif_first, motif_second)), (0, (motif_second, motif_first))):
            sequence = background.copy()
            for position, motif in zip(positions, motifs):
                block = flank_left + motif + flank_right
                sequence[position:position + len(block)] = list(block)
            sample_id = f"{group}-{label}"
            records.append({"sample_id": sample_id, "group_id": group, "sequence": "".join(sequence), "label": label})
            truth.append({"sample_id": sample_id, "first_block_start": positions[0], "second_block_start": positions[1], "first_motif": motifs[0], "second_motif": motifs[1]})
    samples = pd.DataFrame(records)
    groups = samples["group_id"].unique()
    train_groups, heldout_groups = train_test_split(groups, test_size=0.4, random_state=seed)
    validation_groups, test_groups = train_test_split(heldout_groups, test_size=0.5, random_state=seed)
    samples["split"] = "train"
    samples.loc[samples["group_id"].isin(validation_groups), "split"] = "validation"
    samples.loc[samples["group_id"].isin(test_groups), "split"] = "test"
    return samples, pd.DataFrame(truth)


"""Inference contracts shared by development and the frozen comparison."""

from pathlib import Path
from typing import Any
import hashlib

import numpy as np
import pandas as pd
import torch
from torch import nn

def one_hot(sequences: Any) -> torch.Tensor:
    encoded = np.stack([np.array(list(sequence))[:, None] == np.array(list("ACGT"))[None, :] for sequence in sequences]).astype(np.float32)
    return torch.from_numpy(encoded.transpose(0, 2, 1))


class SequenceCNN(nn.Module):
    def __init__(self, sequence_length: int = 160) -> None:
        super().__init__()
        self.filters = nn.Sequential(nn.Conv1d(4, 16, kernel_size=7, padding=3), nn.ReLU(), nn.Conv1d(16, 16, kernel_size=5, padding=2), nn.ReLU())
        self.classifier = nn.Sequential(nn.Linear(16 * sequence_length + 16, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, sequences: torch.Tensor) -> torch.Tensor:
        features = self.filters(sequences)
        representation = torch.cat([features.flatten(1), features.amax(dim=2)], dim=1)
        return self.classifier(representation).squeeze(1)


def predict_cnn(model: SequenceCNN, sequences: Any) -> np.ndarray:
    model.eval()
    with torch.inference_mode():
        return torch.sigmoid(model(one_hot(sequences))).numpy()


MODEL_ID = "InstaDeepAI/nucleotide-transformer-v2-50m-multi-species"
REVISION = "81b29e5786726d891dbf929404ef20adca5b36f1"
POOLING = "last_hidden_state_mean_excluding_special_tokens_and_padding"


def sequence_hashes(samples: pd.DataFrame) -> np.ndarray:
    return np.array([hashlib.sha256(sequence.encode("ascii")).hexdigest() for sequence in samples["sequence"]])


def load_embedding_cache(path: str | Path, samples: pd.DataFrame) -> np.ndarray:
    with np.load(path, allow_pickle=False) as cache:
        ids = cache["sample_ids"].astype(str)
        if len(set(ids)) != len(ids) or set(ids) != set(samples["sample_id"]):
            raise ValueError("Embedding cache sample identities do not match the dataset")
        if str(cache["revision"]) != REVISION or str(cache["model_id"]) != MODEL_ID or str(cache["pooling"]) != POOLING:
            raise ValueError("Embedding cache provenance does not match the declared representation")
        positions = pd.Index(ids).get_indexer(samples["sample_id"])
        if not np.array_equal(cache["sequence_sha256"][positions], sequence_hashes(samples)):
            raise ValueError("Embedding cache sequence hashes do not match the dataset")
        embeddings = cache["embeddings"][positions]
    if embeddings.shape != (len(samples), 512) or not np.isfinite(embeddings).all():
        raise ValueError("Embedding cache shape or values are invalid")
    return embeddings


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
    freeze_workflows()
