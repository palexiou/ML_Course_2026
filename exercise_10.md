# Exercise 10: miRNA–target prediction group project

Work in **groups of two or three** to build a predictor for the Hejret 2023 dataset.

## Data

Download miRBench's processed `AGO2_CLASH_Hejret2023` training data directly from [Zenodo](https://zenodo.org/records/20540907):

[Download training data](https://zenodo.org/records/20540907/files/AGO2_CLASH_Hejret2023_train.tsv.gz?download=1)

Use these columns:

- `noncodingRNA`: miRNA sequence.
- `gene`: target-site sequence.
- `label`: prediction target; 1 = observed binding pair, 0 = synthetic negative pair.

Use only the two sequence columns as model inputs. **Do not use the other columns, including `Nunique`, which reveals the label.**

**Do not use the official test set.** Create your own training, validation, and held-out evaluation splits from the training file.

## Project

- Build a predictor. Choose and justify your own representation and model.
- Build a separate evaluation system that accepts predictions from any model and evaluates them against reference labels on held-out data. Choose appropriate metrics and explain them.
- Work in a shared GitHub repository. All members should contribute, commit meaningful work regularly, and keep notes of decisions, experiments, and results.
- Document how someone else can reproduce your work and run prediction and evaluation.

Organize the work yourselves and make your own implementation decisions.

## Submission

Submit your GitHub repository and a short report describing your approach, evaluation, results, limitations, and each member's contribution.
