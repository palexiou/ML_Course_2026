# Completed answers

Run each linked Python script as a whole in one cell, or run the file locally. No repository imports or prior cell state are required. Install NumPy, pandas, and scikit-learn if missing. These are short teaching examples, not fabricated full-course model results.

## Day 1

[Completed code](completed/day1_validation.py).

The missing arguments are `training["sequence"]`, `training["label"]`, `validation["sequence"]`, and `validation["sample_id"]`. The pipeline learns the vocabulary and classifier from training only. Validation estimates performance for development. The example is intentionally tiny; its output is not a stable performance estimate. ROC-AUC evaluates ranking across thresholds, while the confusion matrix uses the fixed threshold 0.5. A high score on simulated sequences supports only the simulated task, not real promoter recognition. A higher threshold can reduce positive calls and change precision/recall; it does not necessarily improve both.

For the separate leakage investigation, unique sample IDs are insufficient: related groups can occur in both partitions. Correct the group split and refit every learned step. The existing investigation assigns random group labels independently of background, so memorizing relatives need not generalize to new groups. Inspect measured overlap and results rather than promising a score drop. Keep these outputs separate from the main model comparison.

## Day 2

[Completed code](completed/day2_representation.py).

Sigmoid(1) is about 0.731. One-hot input has shape `(2, 4, 160)` after transposition, matching batch, channels, and sequence positions. Both bags are identical; the one-hot arrays differ. Any deterministic classifier given the same bag must produce the same prediction for both members, although their labels are opposite. The construction swaps motif blocks at fixed positions with matching flanks. It demonstrates discarded positional information. The actual CNN uses flattened convolution features as well as global maximum features; flattening retains absolute position. This is not evidence of general grammar or an inevitable advantage for CNNs on other data.

## Day 3

[Completed code](completed/day3_alignment.py).

Set the cache index to `sample_id`, verify unique IDs and exact set equality, and select `.loc[metadata["sample_id"]]`. Use the existing split masks after this alignment. Row position is not sample identity. Missing or duplicate IDs must fail before fitting. This example uses synthetic features and cannot establish pretrained-model performance.

A real cache needs sample-to-sequence correspondence and hashes, dataset variant, model identifier and immutable revision, tokenizer/revision, truncation and padding rules, layer, pooling, extraction mode, dtype, package versions, and runtime provenance. Fit learned scaling/classification on training only. At freeze, record model/preprocessing hashes, configurations, validation selection, metric/threshold policy, split manifest, validation predictions, and inference procedure. Explicit instructor authorization precedes protected test-label reads and scoring; frozen label-independent per-sequence extraction may use test inputs beforehand. Test predictions are created only after reveal. Post-reveal changes cannot reuse the same test as independent evidence.

## Day 4

[Completed code](completed/day4_audit.py) and [full worked scientific audit](../agent_workshop/worked-audit.md).

The overlapping group is `group-a`; sample IDs remain disjoint. A positional comparison yields an apparent accuracy of 1.0, while joining the authored probabilities to their IDs yields 0.0. These deliberately chosen values demonstrate alignment failure, not measured agent behavior. Neither number repairs group leakage or establishes biology. Rebuild the separate exercise using group-respecting development splits and training-only preprocessing, then regenerate predictions. Preserve the original main-course split identities. Do not tune against the revealed Day 3 test.

## Actual Day 4 run comparison

The [actual runs and parent audit](../agent_workshop/actual_runs/2026-10-26/README.md) are separate from the authored faulty fixture. Both runs were scientifically cautious. The vague run selected a disclosed-motif model by training-only group cross-validation/log loss; the specified run reproduced the fixed 4-mer baseline, including sample-aligned probabilities within 1e-12. Different objectives, features, and search mean their validation scores do not rank prompt quality. Ask students which scientific choices each request fixed, how to verify those choices, and why plausible code or a higher score is not biological discovery. Neither run establishes real promoter prediction.
