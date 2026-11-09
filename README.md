# Machine learning for bioinformatics

Simple hands-on exercises, with code that is easy to read and teach.
Only Exercise 1 is implemented for now.

## Setup

```powershell
python -m pip install -r course_code/requirements.txt
```

## Exercise 1: artificial TFBS dataset

Open `exercise_1.ipynb` for the step-by-step, self-contained notebook.
In Google Colab, choose **File > Upload notebook**, select this file, then
run the cells from top to bottom. Change `ofile` in the first code cell to
choose the output CSV path. The final Markdown cell explains how to download
the CSV from Colab.

The command-line script remains available:

```powershell
python course_code/exercise_1.py --ofile "exercise_1_output/dataset.csv"
```

Without `--ofile`, the output is also `exercise_1_output/dataset.csv`.
Parent directories are created automatically.

- 10,000 positives and 10,000 negatives, each 100 nt long.
- Background bases are sampled independently: A = C = G = T = 25%.
- Each positive has one sampled 10-nt motif planted at a random valid position.
- Only the first 10 columns of the supplied PFM are used, with each column
  normalized separately to nucleotide probabilities. No pseudocounts are added.
- Motifs replace background bases and use the supplied orientation.
- Negatives have no planted motif; chance motif matches are not filtered out.
- CSV columns: `sequence`, `label` (1 = positive, 0 = negative).
- Random seed: 42. No data splits or models.

## Tests

```powershell
python -m unittest discover -s tests
```

Future notebooks will be short, manually written, and focused on the specified
exercise. No notebook generators, shared course framework, or presentation tools.
