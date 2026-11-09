# Machine learning for bioinformatics

Simple hands-on exercises, with code that is easy to read and teach.
Exercises 1 and 2 are implemented as simple, self-contained notebooks.

## Open the exercises in Google Colab

| Exercise | Topic | Run notebook |
| --- | --- | --- |
| [Exercise 1](exercise_1.ipynb) | Create an artificial TFBS dataset | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_1.ipynb) |
| [Exercise 2](exercise_2.ipynb) | Logistic regression with a bag of k-mers | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_2.ipynb) |

Start with Exercise 1 and download its CSV. Then open Exercise 2, upload the CSV
using the Colab Files sidebar, and set `ifile` to the uploaded filename.

The buttons open the versions on GitHub's `main` branch, not local changes.
If the repository is private, you need repository access and must authorize Colab
to access private repositories through its GitHub notebook browser.

## Local setup (optional)

```powershell
python -m pip install -r course_code/requirements.txt
```

## Exercise 1: artificial TFBS dataset

Open `exercise_1.ipynb` for the step-by-step, self-contained notebook.
Use its **Open In Colab** button above, then run the cells from top to bottom.
Change `ofile` in the first code cell to
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

## Exercise 2: logistic regression with a bag of k-mers

Open `exercise_2.ipynb` and set `ifile` to the Exercise 1 CSV path.
In Colab, upload the CSV with the Files sidebar and set `ifile` to its filename.

- Count overlapping k-mers with a moving window, for k = 1 through 10.
- Walk through one k=4 model and all its validation results before the comparison loop.
- Use the same stratified 70% training / 20% validation / 10% test split for every k.
- Fit vocabulary and logistic regression on training sequences only.
- Compare validation accuracy, balanced accuracy, precision, recall, F1,
  ROC-AUC, average precision, and log loss, plus ROC/precision-recall curves
  and confusion matrices for every k.
- Select k by validation ROC-AUC, then evaluate only that model on the test set.
- The final cell reveals test results: stop before it during validation discussion.
  **Run all includes the test evaluation.**

## Tests

```powershell
python -m unittest discover -s tests
```

Future notebooks will be short, manually written, and focused on the specified
exercise. No notebook generators, shared course framework, or presentation tools.
