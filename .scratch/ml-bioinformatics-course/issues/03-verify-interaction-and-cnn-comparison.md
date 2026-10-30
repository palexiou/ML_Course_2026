# 03: Verify the interaction-signal and CNN comparison

**What to build:** A runnable representation experiment comparing k-mer baselines with a small one-hot CNN on controlled simple-signal and interaction-signal dataset variants. Demonstrate what the representations expose or discard using measured outputs and controlled sequence changes, not an assumed model ranking.

**Blocked by:** 01: Verify the simple-signal classification workflow.

**Status:** ready-for-human

- [x] Select the interaction construction and small CNN together through development experiments, disclosing why the example probes the intended representation difference.
- [x] Preserve the same sequence-classification framing and known ground truth across the simple-signal and interaction-signal dataset variants.
- [x] Generate reproducible sample identities and correct splits for the interaction variant and reuse each variant's split identities across every compared representation.
- [x] Run logistic regression and random forest on k-mer features and the small CNN on one-hot sequences for the intended comparisons, with a consistent metric policy and validation-only development.
- [x] Train the CNN on the simple-signal variant as well as conduct the intended interaction comparison, so the Day 2 practical has a complete runnable path.
- [x] Verify that the chosen architecture can express the intended interaction rather than assuming convolution automatically provides the required behavior.
- [x] Inspect responses to controlled sequence changes and compare predictions with known simulation truth. Explain limitations instead of declaring that a filter necessarily represents a biological motif.
- [x] Repeat documented development runs or seeds sufficiently to distinguish the intended lesson from an accidental outcome; justify any numerical tolerance rather than require a CNN victory.
- [x] Keep final course test results protected during architecture and dataset calibration and provide frozen reproducible configurations for subsequent work.
- [ ] Verify actual Colab execution and record setup, training, memory/runtime conditions, and timings suitable for the approved teaching blocks without requiring a student-owned GPU.
- [x] Deliver runnable experiments, clearly identified saved outputs, and a verification record. Report any necessary scope change rather than silently increasing compute requirements.


## Implementation handoff

The instructor explicitly requested all remaining development now and will paste/arrange standalone code and check Colab manually. This authorizes downstream implementation without pretending earlier manual gates passed. Use `paste_ready/README.md`, `instructor/guide.md`, `instructor/verification.md`, and the linked per-experiment records. Distinct student snippets and completed answers replace agent-produced notebook presentation for this handoff; original notebook-presentation checkboxes remain unchecked rather than falsely claiming `.ipynb` delivery.

The executable paths, scientific safeguards, and available teaching materials are locally developed. Actual Colab runs, a timed classroom rehearsal, the planned course test reveal, genuine agent screen recording, and actual Agentomics access/demonstration remain separate instructor work where applicable. Ready-for-human is not resolved or classroom-ready. The course test results remain uncalculated. No commits or pushes were made.
