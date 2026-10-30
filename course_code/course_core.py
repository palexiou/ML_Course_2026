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
