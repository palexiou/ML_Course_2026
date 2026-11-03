# Representation experiment: local verification

## Construction and invariant

The interaction-signal dataset has 240 independent groups, two 160-base sequences per group. A shared background receives motif blocks at zero-based positions 32 and 80. Each block is six G bases, an eight-base motif, and six C bases. Positive sequences have `TATAAATG` then `CGGACGTC`; negatives reverse them. Motif starts are 38 and 86. Both members stay together: 144/48/48 groups in train/validation/test, or 288/96/96 sequences.

Matching flanks make every pair's character 4-mer bags exactly equal. The entrypoint checks paired training feature equality; the validation controlled-change table exposes predictions for opposite-label pairs. Any deterministic classifier of identical vectors assigns the same probability to both members. This is a representation invariant, not a desired score gap.

The CNN uses one-hot `(batch, ACGT, positions)` input, two padded 16-channel convolutions (kernels 7 and 5, ReLU), flattened position-bearing features plus global maximum features, and a 32-unit head. Adam: learning rate 0.002, batch 64, 24 CPU epochs. The highest validation ROC-AUC checkpoint is retained, earliest tie. This is validation-based development, not independent evaluation. Global pooling alone can discard the intended cue. Fixed positions and matching flanks are disclosed constructions, not general biological grammar or position-invariant learning.

## Actual validation-only runs

All methods use the same existing sample/group/split identities. Primary ROC-AUC and threshold 0.5 are fixed in advance. No protected course test scores were calculated.

| Dataset / method | Seed 2026 ROC-AUC | Development seeds 101 / 102 / 103 |
|---|---:|---|
| Simple-signal / logistic regression | 0.801944 | 0.805833 / 0.756528 / 0.796319 |
| Simple-signal / random forest | 0.906806 | 0.880451 / 0.877396 / 0.897361 |
| Simple-signal / CNN | 0.564306 | 0.527361 / 0.591528 / 0.542569 |
| Interaction-signal / logistic regression | 0.500000 | 0.500000 / 0.500000 / 0.500000 |
| Interaction-signal / random forest | 0.500000 | 0.500000 / 0.500000 / 0.500000 |
| Interaction-signal / CNN | 1.000000 | 1.000000 / 1.000000 / 1.000000 |

Separate development seeds show the lesson is not accidental. The simple-signal CNN performs poorly in this small-data, position-aware configuration; retain and explain that observation rather than hiding it. The order control is deliberately easy for a position-aware model and impossible for identical bags. No model-victory tolerance is an acceptance rule.

Original classical fitting plus CNN training took 25.89 seconds for simple-signal and 3.43 seconds for interaction-signal, excluding imports/setup. Latest measured records are in `course_output/representation_run.json` and `fresh_rehearsal.json`. Development outputs are under OS temp, separate from classroom artifacts.

Development readers omit protected test labels; frozen per-sequence extraction may see unlabeled test inputs without fitting. Script 05 hashes data, models, caches, configurations, and validation predictions; it fingerprints inference/metric source and package versions. Source capture needs a script or notebook cell retaining source history. These are accident guards, not adversarial security.

Actual Colab execution, memory measurement, projector checks, and a timed 180-minute classroom rehearsal remain separate instructor checks.
