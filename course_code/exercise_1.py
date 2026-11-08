"""Generate Exercise 1: uniform DNA backgrounds with a planted 10-nt TFBS motif."""

from pathlib import Path

import numpy as np
import pandas as pd


BASES = np.array(list("ACGT"))
PFM = np.array([
    [87, 167, 281, 56, 8, 744, 40, 107, 851, 5],
    [291, 145, 49, 800, 903, 13, 528, 433, 11, 0],
    [76, 414, 449, 21, 0, 65, 334, 48, 32, 903],
    [459, 187, 134, 36, 2, 91, 11, 324, 18, 3],
])
MOTIF_PROBABILITIES = PFM / PFM.sum(axis=0, keepdims=True)
SEQUENCE_LENGTH = 100
SEQUENCES_PER_CLASS = 10_000
SEED = 42
OUTPUT_PATH = Path("exercise_1_output/dataset.csv")


def sample_motifs(rng: np.random.Generator, count: int) -> np.ndarray:
    motifs = np.empty((count, PFM.shape[1]), dtype="U1")
    for position in range(PFM.shape[1]):
        motifs[:, position] = rng.choice(
            BASES, size=count, p=MOTIF_PROBABILITIES[:, position]
        )
    return motifs


def generate_dataset(seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    sequences = rng.choice(
        BASES, size=(2 * SEQUENCES_PER_CLASS, SEQUENCE_LENGTH)
    )
    motifs = sample_motifs(rng, SEQUENCES_PER_CLASS)
    starts = rng.integers(
        0, SEQUENCE_LENGTH - PFM.shape[1] + 1, size=SEQUENCES_PER_CLASS
    )
    for row, (start, motif) in enumerate(zip(starts, motifs)):
        sequences[row, start:start + PFM.shape[1]] = motif
    return pd.DataFrame({
        "sequence": ["".join(sequence) for sequence in sequences],
        "label": np.repeat([1, 0], SEQUENCES_PER_CLASS),
    })


def main() -> None:
    dataset = generate_dataset()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(dataset):,} sequences to {OUTPUT_PATH}")
    print("10,000 positives (label 1), 10,000 negatives (label 0); 100 nt each.")


if __name__ == "__main__":
    main()
