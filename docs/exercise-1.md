# Exercise 1: artificial TFBS dataset

Run from the repository root:

```powershell
python course_code/exercise_1.py
```

The script writes `exercise_1_output/dataset.csv` with two columns:
`sequence` and `label`. It contains 10,000 positives (`label = 1`), followed
by 10,000 negatives (`label = 0`). Every sequence is 100 nt long.

Background bases are sampled independently with probabilities
A = C = G = T = 0.25. These are sampling probabilities, not a requirement
for exactly 25 occurrences of each base in every sequence.

Each positive has one sampled 10-nt motif planted into its background.
Only the first 10 columns of the supplied PFM are used. Each column is
divided by its own total to obtain A/C/G/T probabilities, then each motif
position is sampled independently. No pseudocounts are added.

The motif replaces 10 background bases, keeping the sequence length at
100 nt. Its zero-based start is sampled uniformly from 0 through 90,
inclusive. Motifs are planted in the supplied orientation only.

Negatives are unmodified background sequences; chance motif matches are
not filtered out. Positives can also contain chance matches outside the
planted motif. The 25% probabilities describe the background, not the
final base composition after motif planting.

The random seed is 42. No data splits, models, or other exercises are added.
