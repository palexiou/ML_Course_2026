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


