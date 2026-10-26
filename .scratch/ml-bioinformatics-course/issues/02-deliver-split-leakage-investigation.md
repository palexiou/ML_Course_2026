# 02: Deliver the split-leakage investigation

**What to build:** A separate, runnable investigation in which students inspect a misleading evaluation caused by related sequences crossing a split, correct the split, and explain what the corrected evidence supports. Deliver questions, a worked answer, and saved outputs so the scientific audit can proceed even if live execution fails.

**Blocked by:** 01: Verify the simple-signal classification workflow.

**Status:** ready-for-agent

- [ ] Construct a reproducible leakage-exercise dataset variant with known related-sequence groups and an intentionally flawed split that visibly overlaps those groups.
- [ ] Keep this exercise separate from the correct course comparison so its invalid split, outputs, or preprocessing cannot silently become the baseline protocol.
- [ ] Provide a working analysis with predictions and validation-style metrics under the flawed split, without exposing or tuning against the protected course test set.
- [ ] Ask students to identify the flaw, propose a correction, and explain why the original result was not trustworthy before presenting the worked answer.
- [ ] Provide the corrected group-respecting analysis, verify the absence of cross-split group overlap, and compare the measured results with the flawed analysis.
- [ ] Support the intended lesson with actual observable overlap and its correction. Do not guarantee or manufacture a particular score drop.
- [ ] Supply selected missing code where useful, separate completed answers, instructor prompts, and clearly identified saved outputs corresponding to the recorded experiment.
- [ ] Rehearse the investigation within Day 1's final 30-minute envelope while preserving discussion, recap, and buffer; record a shorter instructor-led route if needed.
- [ ] Verify the exercise in the supported classroom environment and record any failed, blocked, or unverified checks honestly.
