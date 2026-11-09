# Machine learning for bioinformatics

Simple hands-on exercises, with code that is easy to read and teach.
Exercises 1 through 8 are available as simple, self-contained notebooks.

## Open the exercises in Google Colab

| Exercise | Topic | Run notebook |
| --- | --- | --- |
| [Exercise 1](exercise_1.ipynb) | Create an artificial TFBS dataset | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_1.ipynb) |
| [Exercise 2](exercise_2.ipynb) | Logistic regression with a bag of k-mers | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_2.ipynb) |
| [Exercise 3](exercise_3.ipynb) | Logistic regression on real human non-TATA promoter sequences | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_3.ipynb) |
| [Exercise 4](exercise_4.ipynb) | Decision tree and random forest on artificial TFBS data | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_4.ipynb) |
| [Exercise 5](exercise_5.ipynb) | Gradient boosting on artificial TFBS data | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_5.ipynb) |
| [Exercise 6](exercise_6.ipynb) | Compare logistic regression, random forest, and gradient boosting on real non-TATA promoters | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_6.ipynb) |
| [Exercise 7](exercise_7.ipynb) | Motif XOR: perceptron and random forest, then a ReLU MLP | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_7.ipynb) |
| [Exercise 8](exercise_8.ipynb) | Probabilistic positional motifs with one-hot DNA and a 1D CNN | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/exercise_8.ipynb) |

Start with Exercise 1 and download its CSV. Then open Exercise 2, upload the CSV
using the Colab Files sidebar, and set `ifile` to the uploaded filename.
Exercises 3 and 6 download their own public benchmark data; no CSV upload is needed.
Exercises 4 and 5 use the same Exercise 1 CSV as Exercise 2; upload it and set `ifile` in the same way.
Exercises 7 and 8 create and save their own datasets; no upload is needed.

The buttons open the versions on GitHub's `main` branch, not local changes.
If the repository is private, you need repository access and must authorize Colab
to access private repositories through its GitHub notebook browser.

## Local setup (optional)

Exercise 8 adds PyTorch, which is normally available in Colab. For a CPU-only local
installation, first install PyTorch from its official CPU wheel index:

```powershell
python -m pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cpu
```

Then install the course dependencies:

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
- Select test and validation sequences randomly per label, then use the remaining
  sequences for training. Both counts are calculated from the original class size.
- Fit vocabulary and logistic regression on training sequences only.
- Compare validation accuracy, balanced accuracy, precision, recall, F1,
  ROC-AUC, average precision, and log loss, plus ROC/precision-recall curves
  and confusion matrices for every k.
- Select k by validation ROC-AUC, then evaluate only that model on the test set.
- The final cell reveals test results: stop before it during validation discussion.
  **Run all includes the test evaluation.**

## Exercise 3: real human non-TATA promoters

Open `exercise_3.ipynb` with its **Open In Colab** button and run the cells in order.
The first code cell installs `pyarrow`, the Parquet reader used by pandas.

- Download `human_nontata_promoters` from the Genomic Benchmarks maintainers'
  Hugging Face repository, using a fixed dataset revision.
- Use real 251-nt sequences: label 1 is a non-TATA promoter, label 0 a non-promoter.
- Keep the official 9,034-sequence test set unchanged.
- Reserve 20% per label from the official 27,097-sequence training set for validation:
  21,678 training sequences and 5,419 validation sequences.
- Keep the original class proportions and retain sequences containing unknown bases (`N`).
- Walk through k=4, then compare k=1 through 10 with the same metrics and plots as Exercise 2.
- Select k by validation ROC-AUC; fit vocabulary and model on training sequences only.
- Stop before the final cell until selection is complete. **Run all includes test evaluation.**

This is benchmark evaluation, not a claim of chromosome-held-out evaluation or
proof that the model has learned a biological promoter mechanism.

## Exercise 4: decision tree and random forest

Open `exercise_4.ipynb` with its **Open In Colab** button and set `ifile` to the
Exercise 1 CSV path. In Colab, upload the CSV and set `ifile` to its filename.

- Train a decision tree and a random forest with 100 trees on the artificial data.
- Use the same 70% training / 20% validation / 10% test split as Exercise 2.
- Walk through both models at k=4, then compare k=1 through 7 separately; no mixed k-mers.
- Show the same metrics, ROC/precision-recall curves, and confusion matrices as Exercise 2.
- Select k separately for each model using validation ROC-AUC.
- Evaluate the two selected models on test data only in the final cell.
  **Run all includes test evaluation.**

The random forest uses sparse counts and available CPU cores, but larger k can
be slower to train. Full Exercise 4 training has not yet been timed or validated.

## Exercise 5: gradient boosting

Open `exercise_5.ipynb` and set `ifile` to the Exercise 1 CSV path.
In Colab, upload the CSV and set `ifile` to its filename.

- Keep k=4 fixed and use the same 70% training / 20% validation / 10% test split.
- Add shallow trees sequentially with `GradientBoostingClassifier` and binary log loss.
- Plot training and validation log loss for 1 through 200 trees.
- Select the tree count by lowest validation log loss, with learning rate 0.1 and depth 2 fixed.
- Compare with a decision tree and a 100-tree random forest at the same k and split.
- Show all eight metrics, ROC/precision-recall curves, and confusion matrices.
- Evaluate only the selected gradient boosting model on test data in the final cell.
  **Run all includes test evaluation.**

## Exercise 6: compare three models on real non-TATA promoters

Open `exercise_6.ipynb` with its **Open In Colab** button and run the cells in order.
No CSV upload or earlier notebook is required.

- Download the same pinned non-TATA promoter benchmark as Exercise 3.
- Preserve its official test set and reserve 20% per label from official training for validation.
- Give all three models the same training-fitted, sparse bag-of-6-mers representation.
- Compare logistic regression (not the classic perceptron), a 100-tree random forest,
  and gradient boosting with 200 depth-2 trees and learning rate 0.1.
- Keep k=6 and model settings fixed; there is no hyperparameter search.
- Compare all eight metrics, overlaid ROC/precision-recall curves, and confusion matrices.
- Evaluate all three fitted models on the official test set only in the final cell.
  **Run all includes test evaluation.**

This is a fixed-setting benchmark comparison, not an equally tuned competition or
chromosome-held-out evaluation. Gradient boosting may take longer to train.

## Exercise 7: motif XOR, perceptron, random forest, and MLP

Open `exercise_7.ipynb` and run cells in order. No earlier notebook is required.
Stop after the dataset-saving cell if you only want the new CSV.

- Create 20,000 sequences of 100 nt using two fixed 10-nt motifs with equal base composition.
- Positive means motif A or motif B, **but not both**. Neither and both are negative.
  Each of the four cases has 5,000 sequences.
- Make all four variants of each random background, rejecting unintended motif occurrences.
  Insertions replace bases, use the supplied orientation, and have at least five background
  bases between them so no 6-mer touches both sites.
- Save `exercise_7_output/dataset.csv`, including the sequence, label, motif-presence flags,
  and background ID. Change `ofile` in the first code cell to choose the path.
- Keep each background's four variants together in a 70% training / 20% validation / 10% test
  split. This avoids sharing nearly identical backgrounds across splits.
- Demonstrate the perceptron's XOR limitation using motif-presence indicators.
- Compare a classic perceptron with a 100-tree random forest first, inspecting validation
  accuracy overall and for each XOR case before introducing the MLP.
- Then demonstrate a hand-written two-ReLU network and train the ReLU MLP.
- Give all three models identical training-fitted, sparse bag-of-6-mers counts.
  Presence flags and background IDs are never inputs to the k-mer models.
- Train an MLP with 16 ReLU hidden units for up to 60 epochs using Adam. Select the saved
  epoch with the lowest validation log loss, without refitting on validation data.
- Compare classification and ranking metrics, confusion matrices, and accuracy for each
  XOR case. Perceptron scores are not probabilities, so no perceptron log loss is reported.
- Evaluate all three fitted models on the reserved test backgrounds only in the final code cell.
  **Run all includes test evaluation.**

For every matched quartet, the k-mer vectors satisfy
`x_neither + x_both = x_A_only + x_B_only`. A linear classifier therefore cannot classify
all four correctly: its accuracy ceiling on this balanced dataset is 75%, not 50%.
The task is a controlled demonstration of nonlinear feature combinations, not a model of
a particular natural promoter. A possible follow-up is motif spacing, where short-k-mer
counts discard the relationship between separated elements.

## Exercise 8: probabilistic positional motifs with a CNN

Open `exercise_8.ipynb` and run cells in order. Dataset generation and model training
are in the same notebook. No earlier exercise or CSV upload is needed.

- Create 20,000 independent 1,000-nt sequences with equal class sizes and uniformly sampled
  background bases. Plant one sampled instance of each of two 10-nt motifs per sequence.
- Specify count matrices, normalize columns to sampling probabilities, and calculate
  log-odds PWMs. Motif A has an ATG core with 99.9% conservation per base; motif B has
  a TATAAA core with 97% conservation per base. Flanks are more variable.
- Class 0: motif B is uniform across full-length placements that do not overlap A.
- Class 1: the nominal TATA core start relative to the A of ATG follows a discrete,
  truncated two-sided Gaussian shape on -100 through -30 nt, peaked at -50 nt. Its widths
  are 20 nt on the upstream side and 8 nt on the downstream side. The asymmetric curve's
  mean is upstream of its peak; samples are not clipped at the endpoints.
- Use the same ATG anchor range (101–996 inclusive) and motif probabilities in both classes.
  Keep chance background matches and class-0 placements in the concentrated region.
  Labels record the generating class, rather than a hard offset threshold.
- Save `exercise_8_output/dataset.csv`, including labels, nominal core anchors, full motif
  starts, offsets and the sampled motif strings. Change `ofile` to choose the path.
- Split 70% / 20% / 10% per label for training, validation and test.
- Encode bases as one-hot vectors. Only sequences reach the model; metadata is used for
  dataset checks and interpretation of errors.
- Use the supplied PWMs as fixed convolutional motif scanners, followed by local pooling,
  a trainable convolution/ReLU layer, global max pooling and a binary output. The learned
  part combines known motif responses over a 133-base receptive field; it does not discover
  the motifs from scratch. All model inputs are one-hot sequence encodings.
- Show the forward pass, `loss.backward()`, and the Adam optimizer update explicitly.
  Run 25 epochs and restore the weights with the lowest validation cross-entropy.
- Report all eight metrics and errors by class and offset region. Evaluate the selected
  weights on test sequences only in the final code cell. **Run all includes test evaluation.**

This is an artificial spacing task. TATA boxes concern transcription initiation; ATG is
a translation start codon, not a transcription start site. The labels are not a biological
rule for recognizing functional promoters or translated genes. Chance positional overlap
and motif variability make some examples intrinsically ambiguous.

## Tests

```powershell
python -m unittest discover -s tests
```

Future notebooks will be short, manually written, and focused on the specified
exercise. No notebook generators, shared course framework, or presentation tools.
