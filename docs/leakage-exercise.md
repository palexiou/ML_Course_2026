# Separate split-leakage investigation

`paste_ready/02_split_leakage.py` generates related sequences by mutating family backgrounds. Balanced random family labels are independent of those backgrounds. A 1-nearest-neighbor model uses cosine distance on training-fitted k-mer counts. This demonstrates family memorization, not a biological motif rule.

The flawed row split permits relatives in training and validation; the corrected split separates groups. Both runs save `group_id`, train/validation manifests, `sample_id,probability` predictions, nearest-training sample/group evidence, metrics, and plots in `course_output/leakage/`. The comparison table's `split` names the strategy; the manifest's `split` gives membership. Balanced accuracy is this isolated exercise's declared primary metric, not the main comparison metric.

| Seed | Flawed overlapping groups | Flawed balanced accuracy | Corrected overlapping groups | Corrected balanced accuracy |
|---|---:|---:|---:|---:|
| 2026 | 197 | 1.000000 | 0 | 0.516369 |
| 101 | 199 | 1.000000 | 0 | 0.464366 |
| 102 | 193 | 1.000000 | 0 | 0.426956 |
| 103 | 194 | 0.991667 | 0 | 0.457579 |

These are actual local runs. Finite-sample corrected scores can fall on either side of chance. Group overlap and its removal establish the lesson; no guaranteed score drop is required. The course's protected test data is not used.

Planned final Day 1 route: inspect flawed metrics/manifest (5 minutes), identify the independence unit (5), predict and run group correction (5), compare nearest-family evidence (5), discuss supported conclusions (5), retain recap/buffer (5). This is a plan, not observed classroom timing. A shorter instructor-led route projects saved tables and asks the same questions before showing the correction. Worked explanations are in `instructor/answers.md`.

Actual Colab behavior and a timed classroom rehearsal remain instructor checks. Saved local outputs must be labeled as previous runs, not live execution.
