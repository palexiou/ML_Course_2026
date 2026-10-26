# 03: Verify the interaction-signal and CNN comparison

**What to build:** A runnable representation experiment comparing k-mer baselines with a small one-hot CNN on controlled simple-signal and interaction-signal dataset variants. Demonstrate what the representations expose or discard using measured outputs and controlled sequence changes, not an assumed model ranking.

**Blocked by:** 01: Verify the simple-signal classification workflow.

**Status:** ready-for-agent

- [ ] Select the interaction construction and small CNN together through development experiments, disclosing why the example probes the intended representation difference.
- [ ] Preserve the same sequence-classification framing and known ground truth across the simple-signal and interaction-signal dataset variants.
- [ ] Generate reproducible sample identities and correct splits for the interaction variant and reuse each variant's split identities across every compared representation.
- [ ] Run logistic regression and random forest on k-mer features and the small CNN on one-hot sequences for the intended comparisons, with a consistent metric policy and validation-only development.
- [ ] Train the CNN on the simple-signal variant as well as conduct the intended interaction comparison, so the Day 2 practical has a complete runnable path.
- [ ] Verify that the chosen architecture can express the intended interaction rather than assuming convolution automatically provides the required behavior.
- [ ] Inspect responses to controlled sequence changes and compare predictions with known simulation truth. Explain limitations instead of declaring that a filter necessarily represents a biological motif.
- [ ] Repeat documented development runs or seeds sufficiently to distinguish the intended lesson from an accidental outcome; justify any numerical tolerance rather than require a CNN victory.
- [ ] Keep final course test results protected during architecture and dataset calibration and provide frozen reproducible configurations for subsequent work.
- [ ] Verify actual Colab execution and record setup, training, memory/runtime conditions, and timings suitable for the approved teaching blocks without requiring a student-owned GPU.
- [ ] Deliver runnable experiments, clearly identified saved outputs, and a verification record. Report any necessary scope change rather than silently increasing compute requirements.
