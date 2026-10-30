# 02: Deliver the split-leakage investigation

**What to build:** A separate, runnable investigation in which students inspect a misleading evaluation caused by related sequences crossing a split, correct the split, and explain what the corrected evidence supports. Deliver questions, a worked answer, and saved outputs so the scientific audit can proceed even if live execution fails.

**Blocked by:** 01: Verify the simple-signal classification workflow.

**Status:** ready-for-human

- [x] Construct a reproducible leakage-exercise dataset variant with known related-sequence groups and an intentionally flawed split that visibly overlaps those groups.
- [x] Keep this exercise separate from the correct course comparison so its invalid split, outputs, or preprocessing cannot silently become the baseline protocol.
- [x] Provide a working analysis with predictions and validation-style metrics under the flawed split, without exposing or tuning against the protected course test set.
- [x] Ask students to identify the flaw, propose a correction, and explain why the original result was not trustworthy before presenting the worked answer.
- [x] Provide the corrected group-respecting analysis, verify the absence of cross-split group overlap, and compare the measured results with the flawed analysis.
- [x] Support the intended lesson with actual observable overlap and its correction. Do not guarantee or manufacture a particular score drop.
- [x] Supply selected missing code where useful, separate completed answers, instructor prompts, and clearly identified saved outputs corresponding to the recorded experiment.
- [ ] Rehearse the investigation within Day 1's final 30-minute envelope while preserving discussion, recap, and buffer; record a shorter instructor-led route if needed.
- [ ] Verify the exercise in the supported classroom environment and record any failed, blocked, or unverified checks honestly.


## Implementation handoff

The instructor explicitly requested all remaining development now and will paste/arrange standalone code and check Colab manually. This authorizes downstream implementation without pretending earlier manual gates passed. Use `paste_ready/README.md`, `instructor/guide.md`, `instructor/verification.md`, and the linked per-experiment records. Distinct student snippets and completed answers replace agent-produced notebook presentation for this handoff; original notebook-presentation checkboxes remain unchecked rather than falsely claiming `.ipynb` delivery.

The executable paths, scientific safeguards, and available teaching materials are locally developed. Actual Colab runs, a timed classroom rehearsal, the planned course test reveal, genuine agent screen recording, and actual Agentomics access/demonstration remain separate instructor work where applicable. Ready-for-human is not resolved or classroom-ready. The course test results remain uncalculated. No commits or pushes were made.
