"""Standalone fixed-position motif-order control, with no test data."""

from collections import Counter

import numpy as np


logit = 1.0
probability = 1.0 / (1.0 + np.exp(-logit))
random = np.random.default_rng(2026)
background = random.choice(list("ACGT"), size=160)
sequences = []
for motifs in (("TATAAATG", "CGGACGTC"), ("CGGACGTC", "TATAAATG")):
    sequence = background.copy()
    for position, motif in zip((32, 80), motifs):
        block = "GGGGGG" + motif + "CCCCCC"
        sequence[position:position + len(block)] = list(block)
    sequences.append("".join(sequence))
characters = np.array([list(sequence) for sequence in sequences])
alphabet = np.array(list("ACGT"))
encoded = (characters[:, :, None] == alphabet[None, None, :]).astype(np.float32)
channel_first = encoded.transpose(0, 2, 1)
bags = [Counter(sequence[start:start + 4] for start in range(len(sequence) - 3)) for sequence in sequences]
bags_equal = bags[0] == bags[1]
assert bags_equal
assert channel_first.shape == (2, 4, 160)
assert np.all(channel_first.sum(axis=1) == 1)
assert not np.array_equal(channel_first[0], channel_first[1])
print("Sigmoid(1):", probability)
print("One-hot shape (batch, ACGT channels, positions):", channel_first.shape)
print("Identical 4-mer bags:", bags_equal)
print("Opposite labels: 1, 0. Fixed-position motif-order control, not general grammar.")
