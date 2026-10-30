---
name: scientific-audit
description: Audit simulated DNA classification analyses for group leakage, sample alignment, evaluation integrity, and supported scientific claims. Use for the course analysis review, not general code style checks.
---

# Scientific audit

Read the analysis specification, development inputs, code, provenance, and reported claims. Keep protected test files and test caches closed. The course uses simulation, not a real promoter-discovery benchmark.

Trace the independence unit from `group_id` through split construction and evaluation. Unique `sample_id` values do not prove group separation. For the isolated leakage exercise, propose a group-respecting split and refit; do not alter the main course's fixed split identities.

Trace every fitted transformation to training rows. For embeddings, require immutable model/extraction provenance and exact sample-to-cache alignment. Reject duplicate/missing IDs before joining predictions or embeddings; never infer identity from row position. Prediction probabilities refer to label 1 and must be finite within [0,1].

Check that metrics and thresholds were declared before evaluation, comparisons use the same variant and IDs, and test access follows an explicit freeze/reveal record. Day 3 results cannot be fresh evidence for agent models developed after reveal. An unsupported claim of “test untouched” is not an access record.

Compare interpretation with the simulation construction. The interaction dataset variant is a fixed-position motif-order control with identical 4-mer bags and matching flanks. A position-preserving CNN can access information discarded by bag counts; this does not establish general grammar or real promoter recognition.

Return findings as: claim, observed evidence, consequence, repair, and remaining uncertainty. Separate engineering execution from scientific validity. Label a manually authored fixture as such and leave missing actual-run evidence missing. Do not manufacture metrics or authorize new experiments merely to complete the audit.
