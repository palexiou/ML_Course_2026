# Precise analysis specification

## Objective and scope

Reproduce the development-only sequence-classification baseline on the supplied simulated course dataset and scientifically audit it against the manual workflow. Promoter prediction motivates the simulation; do not claim real promoter recognition or biological discovery. Do not maximize an unspecified “best” score or change the data generation to favor a method.

## Inputs

Use the instructor-supplied development-only `train.csv` and `validation.csv` for one named dataset variant, plus its split manifest and development-only simulation truth. Required columns are `sample_id,group_id,sequence,label,split`. Preserve the provided sample IDs and split identities. Validate unique IDs, uppercase A/C/G/T DNA, binary labels, expected split membership, and no cross-split group overlap. Inspect any mismatch and stop before fitting rather than silently removing samples. Keep labels, IDs, groups, split, and simulation truth out of model inputs.

## Evaluation boundary

Fit k-mer vocabulary and classifier on training only. Do not open protected test sequences, labels, predictions, caches, or results. Day 3's revealed results are historical evidence for auditing the frozen manual workflow; they cannot guide new agent model selection. New post-reveal models have validation evidence only. A new independent test would require a separately agreed experiment, not relabeling these data.

## Model and metrics

Use the manual baseline: character 4-mer counts, case preserved, and logistic regression with maximum 2,000 iterations and seed 2026. Compare on exactly the same validation IDs and variant as the manual run. Declare ROC-AUC primary before evaluating; also report average precision, class balance, accuracy, balanced accuracy, precision, recall, and confusion matrix at the fixed threshold 0.5. If either class is missing, report the metric limitation instead of inventing a score. Do not change hyperparameters, threshold, splits, or metrics based on test outcomes. Record differences from the manual configuration before comparing.

## Outputs and responsibilities

Return runnable standalone Python, a separate `sample_id,probability` validation prediction table for each variant/method, an evaluation report, and a scientific audit. Join by unique sample ID with exact ID coverage and finite probabilities in [0,1]. Record input hashes, source/configuration, seeds, versions, model settings, timings, selected workflow, and limitations. Supply evidence for group separation, training-only fitting, sample alignment, and the baseline comparison. Identify executed code versus proposed code and actual outputs versus illustrative examples.

Use local CPU execution where practical. Report missing dependencies/access promptly. Do not introduce paid student requirements, commit, publish, send messages, or mutate the protected data. If an input is missing, report that blocked step and finish independent inspection; do not substitute synthetic embeddings as if they were pretrained model output.

For the interaction dataset variant, explicitly describe the fixed-position motif-order control with matching flanks and identical 4-mer bags. A bag-of-4-mers baseline cannot distinguish identical feature vectors with opposite labels. Interpret measured evidence without promising a CNN or pretrained-model advantage.
