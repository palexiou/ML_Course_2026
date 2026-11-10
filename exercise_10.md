# Exercise 10: build and evaluate a miRNA–target binding predictor

Work in **groups of three**. Build a predictor using the **Hejret 2023 dataset linked by miRBench**, and build an independent evaluation program that can score prediction files from different models on the same held-out test set. Your predictor receives a miRNA sequence and a target-site sequence and predicts support for a binding interaction.

Your group owns the data preparation, modeling, evaluation, documentation, and GitHub workflow. Choose an approach you can explain and run with your available computing resources. A clear, reproducible experiment matters more than a complicated model.

## 1. Create your shared GitHub repository

One member creates a repository and adds the other two as collaborators. All three members clone it and contribute using their own accounts.

- Write a README with the research question, team members, setup instructions, and exact commands needed to reproduce your work.
- Use GitHub Issues to divide the work into small tasks with an owner and a clear completion condition.
- Make small commits whenever you finish a meaningful piece of work. Use messages that explain the change; do not save all contributions for one final upload.
- Use branches and pull requests. Have a teammate review each substantial change before merging it.
- Keep dated project notes recording decisions, problems, experiments, and next steps. Record unsuccessful experiments as well as successful ones.
- Do not commit large datasets, temporary files, credentials, or generated model files. Document how to download or obtain required artifacts.

Start with one person leading data preparation, one leading modeling, and one leading evaluation and reproducibility. These are coordination roles: review one another's work and rotate responsibilities. Every member should understand the full pipeline and make substantive contributions.

## 2. Understand the data before modeling

Use miRBench's processed **`AGO2_CLASH_Hejret2023`, version 7**, from [Zenodo record 20540907](https://zenodo.org/records/20540907), as linked by the [miRBench dataset loader](https://github.com/katarinagresova/miRBench/blob/6a9c9cca8891fc0dea8deab22030fcb6256c2412/src/miRBench/dataset.py). Read the documentation and inspect the files before choosing features or a model.

- [Training data](https://zenodo.org/records/20540907/files/AGO2_CLASH_Hejret2023_train.tsv.gz?download=1): 8,140 examples.
- [Held-out test data](https://zenodo.org/records/20540907/files/AGO2_CLASH_Hejret2023_test.tsv.gz?download=1): 1,018 examples.

The downloads are gzip-compressed TSV files with headers; pandas can read them using `read_csv` with `sep='\t'`. Use these processed files rather than the original sequencing data or older model datasets.

Each row contains a pair of sequences: `noncodingRNA` is the mature miRNA, and `gene` is a **50-nt target-site sequence**, despite the column name. The sequences use A/C/G/T, with T instead of U. miRNAs vary in length, so decide and document how your representation handles this. Both sequences are supplied in 5′→3′ orientation; complementing or reversing them is a modeling choice you must explain.

`label=1` identifies a retained AGO2-CLASH binding pair. `label=0` identifies an in-silico constructed negative pair, not an experimentally verified absence of binding. **The target is not repression strength or gene-expression change.** For this project, only `gene` and `noncodingRNA` may be used as predictor inputs. Keep annotation columns for audits or error analysis. In particular, **exclude `Nunique`: positive rows have supporting reads and synthetic negatives have zero, so it reveals the answer.**

Your notes must answer:

- What biological question does one example represent?
- What information is available to a predictor at inference time?
- What is the target, and what does each target value mean?
- How many examples and distinct inputs are present? What is the target distribution?
- Are sequences missing, ambiguous, duplicated, or associated with conflicting targets?
- Which columns are valid inputs, and which would reveal the answer or otherwise leak information?

Record the exact source URL, downloaded filename, source revision or download date, and a file checksum. The source files do not provide a sample ID. Create one from the source split and original zero-based row number, for example `hejret2023_train_000000` or `hejret2023_test_000000`, before shuffling or splitting. Keep it unchanged throughout the pipeline. IDs are for bookkeeping and matching predictions, never model features. Document any filtering decisions and how they change the dataset size.

For source details and dataset caveats, see the [verified dataset notes](exercise_10_dataset_notes.md) and the [Hejret study](https://pmc.ncbi.nlm.nih.gov/articles/PMC10739727/).

## 3. Freeze training, validation, and test sets

Use the **official test file as the final held-out test set**. Do not recombine the two source files or resplit the test data. The benchmark's existing test targets are on chromosome 1; this is not a separate study or a holdout of unseen miRNA families. There is no additional official Hejret `leftout` file to obtain.

From the official training file, reserve **20% per label for validation, with seed 42**, and use the remaining examples for training. Record the sampling method and use the same membership for every experiment. Check for duplicate inputs before finalizing the split.

- Verify that no identical `(noncodingRNA, gene)` pair occurs in more than one split. Investigate conflicting labels or duplicates if found, and document any exclusion rather than silently altering the official test set.
- Save a split manifest containing `sample_id` and split membership, together with the random seed and split method.
- Fit vocabularies, scalers, feature selection, embeddings trained on this dataset, and all other learned preprocessing on training examples only.
- Use validation results to choose features, model settings, the training epoch, and any decision threshold.
- Do not use test targets for model or threshold selection. Finish and record your choices before the final test evaluation.

The official train/test files have distinct target chromosomes, but miRNAs and families overlap, and related target sequences can remain in both sets. Discuss what this benchmark does and does not establish about generalization to new miRNAs, targets, or experiments. Synthetic negatives also limit conclusions about natural binding prevalence.

## 4. Build a baseline and an improved predictor

First implement a simple baseline that produces valid predictions. Then investigate at least one improvement. Your choice of model is open: examples include logistic regression, tree-based models, an MLP, or a CNN that learns convolutional filters.

Keep the evaluation protocol fixed so you can interpret changes. Record each experiment's code version, inputs, preprocessing, hyperparameters, random seed, runtime, and validation results. Explain why you tried the change and what you learned. You are not required to outperform another group.

Your prediction entry point must load a saved model and accept new, unlabeled examples. It must not retrain the model or read the answer file. A notebook may support exploration, but another person must be able to generate predictions without manually editing cells or file paths.

For a first baseline, consider a simple representation of both sequences and a model from an earlier exercise. If you choose a CNN, consider how to represent the two inputs, pad variable-length miRNAs, and ensure the model can use both sequences. You choose the implementation; no starter model is supplied.

## 5. Build a model-independent evaluation program

Your evaluator accepts **an answer file and a prediction file**. It does not import the predictor, load its model, or train anything. Different predictors must be interchangeable through this CSV contract:

| File | Required columns | Meaning |
| --- | --- | --- |
| Unlabeled inputs | `sample_id,noncodingRNA,gene` | IDs and the two sequences; no labels or audit metadata |
| Answers | `sample_id,label` | The binary reference label |
| Predictions | `sample_id,probability` | A finite value in [0,1]; larger means stronger support for `label=1` |

Export one probability per example, not just a predicted class. If a method produces an unbounded score or a score with the opposite direction, document its conversion to a positive-class probability. Fit any calibration within the training data, using validation to assess choices. This file format lets the same evaluator score any predictor that follows the contract.

Use stable IDs to match predictions to answers. Never assume that file row order matches. Validate the files before calculating metrics:

- Require the documented columns and unique, nonempty IDs.
- Require exactly one prediction for every evaluated example. Reject missing IDs, duplicate IDs, and unexpected IDs; do not silently score an intersection.
- Reject missing or nonfinite predictions and values outside the documented range.
- Reject invalid targets and incompatible inputs with a clear explanation.

Report **average precision (AP)** as the primary ranking metric, plus ROC-AUC, accuracy, balanced accuracy, precision, recall, F1, and log loss. AP means the average-precision calculation, not trapezoidal area under the precision-recall curve. Draw ROC and precision-recall curves and a confusion matrix. Default to threshold 0.5 for class predictions; any alternative threshold must be chosen on validation data and fixed before test evaluation. Record the threshold in the output.

Handle undefined metrics explicitly, such as ROC-AUC with only one reference class, instead of silently returning a misleading number. Use a documented zero-division convention for precision and F1 when no positives are predicted.

Write a few small, hand-checkable evaluation tests: perfect predictions, shuffled prediction rows, missing and duplicate IDs, an unexpected ID, and invalid scores. Check that shuffled rows produce identical results and that malformed files fail clearly.

Save machine-readable metrics and plots to an output directory. Record the prediction file, answer file, evaluation settings, and code version with the results. Run the same evaluator on your baseline and improved model, without changing its code between them.

Before using the real test targets, demonstrate the evaluator on a tiny artificial example. Make sure another team member can run it independently.

Provide these command-line entry points. The filenames below are part of your deliverable, not files supplied by this exercise. You decide how to implement and serialize the model.

```bash
python train.py --train data/train.csv --validation data/validation.csv --output artifacts/model
python predict.py --model artifacts/model --input data/validation_inputs.csv --output results/validation_predictions.csv
python evaluate.py --answers data/validation_answers.csv --predictions results/validation_predictions.csv --output results/validation --threshold 0.5
```

Here `train.csv` and `validation.csv` contain `sample_id,noncodingRNA,gene,label`; the prediction inputs and answer files follow the separated contract above. Your preparation step creates these files from the official downloads. Document its exact command too. For the final evaluation, use `test_inputs.csv` and `test_answers.csv` with the same prediction and evaluation commands. The evaluator must work with a teammate's conforming prediction file without any code changes.

## 6. Work toward a reproducible handoff

Use these milestones to organize your own work:

1. **Plan:** shared repository, team roles, initial Issues, dataset description, and a recorded split plan.
2. **First complete pipeline:** a baseline creates predictions and the evaluator successfully scores them on validation data.
3. **Investigate:** compare a small number of justified changes using validation results and keep an experiment log.
4. **Freeze:** record the selected model, preprocessing, threshold if relevant, and the Git commit used for final evaluation.
5. **Final evaluation:** generate test predictions and score them once after selection. Report the result without changing the model in response.
6. **Handoff:** a teammate follows the README from a fresh clone, reproduces validation predictions and evaluation, and records any problems you fix.

If you discover a genuine implementation bug during final evaluation, document it, fix it, and explicitly report that the test set has already been inspected. Do not present the rerun as a previously untouched test.

## 7. Submit

Submit the shared GitHub repository URL, the final commit identifier, and a short report. Ensure the instructor can access the repository and any required model artifacts.

The repository must include:

- A README with setup, data acquisition, training, prediction, and evaluation instructions.
- Code for data preparation, the baseline, the improved predictor, and the independent evaluator.
- The stable-ID convention, frozen split manifest, dependency versions, and reproducibility settings.
- Dated project notes, an experiment table, and a short contribution statement from each member.
- Evaluation tests, final prediction files or clear artifact links, machine-readable metrics, and evaluation plots.

In the report, describe the biological task, dataset limitations, split, baseline, improvements, and final evaluation. Explain errors and limitations, distinguish validation from test results, and identify one sensible next experiment.

Be ready to demonstrate prediction and evaluation, explain a learned feature or model decision where possible, and show how your Git history and notes document collaboration. Assessment will consider task understanding, leakage prevention, evaluator correctness, reproducibility, justified experiments, and contributions from all three members.

Choose sensible defaults, document your assumptions, and investigate problems independently using the documentation and your teammates. Ask for help when you have a concrete question: describe what you expected, what happened, and what you tried.
