# 01: Verify the simple-signal classification workflow

**What to build:** A reproducible, runnable path from the simple-signal course dataset through k-mer features to logistic regression and validation results, usable from a fresh Colab runtime or simple laptop. Establish the stable sample identities and evaluation boundary reused by later tickets without yet expanding the teaching package.

**Blocked by:** None (can start immediately).

**Status:** ready-for-human

- [x] Generate simulated DNA sequences with a clear planted motif, controlled noise, labels, sample identities, and known ground truth; record the generation settings and seeds needed to reproduce them.
- [x] Explicitly describe the task as simplified sequence classification motivated by promoter prediction, not real promoter recognition or chromosome scanning.
- [x] Define stable training, validation, and protected test identities and preserve any related-sequence grouping needed for correct evaluation.
- [x] Run the complete sequence-to-k-mer-to-logistic-regression workflow. Fit learned preprocessing on training data only and use validation results for model development.
- [x] Choose and justify a primary comparison metric before evaluating models; include understandable prediction-level and confusion-matrix outputs and appropriate ROC/precision-recall views without using the test set to choose the policy.
- [x] Keep final test results out of development outputs and document how later workflows reuse the same sample and split identities.
- [x] Verify the intended simple signal through reproducible development experiments with justified expectations, without adapting the example to the final course test results.
- [ ] Execute from a fresh environment and verify actual Colab execution; record dependency setup, runtime conditions, setup time, and execution time. Do not equate local success with Colab verification.
- [x] Keep the required path appropriate for a simple laptop or Colab without a student-owned GPU, and disclose any unverified compatibility claims or access blockers.
- [x] Deliver the runnable experiment, reproducible outputs, and a concise verification record. No full slide expansion is required by this ticket.

## Implementation handoff update

The instructor requested standalone code to paste into Colab manually, rather than agent-operated Colab execution or notebook presentation work. The coding agent will verify the standalone code locally and provide a manual Colab checklist. Actual Colab execution remains a separate instructor check and must not be reported as completed by local verification.

## Comments

The standalone experiment is implemented and locally verified, including a fresh virtual environment and separate development seeds. The remaining unchecked acceptance criterion is the instructor's actual Colab run; fresh local execution is complete but does not satisfy that criterion. The ticket is ready-for-human, not resolved. See the standalone-code handoff and local verification record for the manual check and measured results.
