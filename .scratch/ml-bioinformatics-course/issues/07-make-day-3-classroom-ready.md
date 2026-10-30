# 07: Make Day 3 classroom-ready and deliver the protected test comparison

**What to build:** A complete session in which students understand pretraining, see a small live embedding extraction, classify cached embeddings, compare representations on validation data, and then inspect the planned test comparison after workflows have been frozen.

**Blocked by:** 04: Verify the frozen-embedding workflow.

**Status:** ready-for-human

- [ ] Provide scaffolded and separate completed notebooks with the verified small extraction and cached full-data classifier, matching answers, sample-alignment checks, and recorded embedding provenance.
- [x] Use minutes 0-10 for recap and 10-50 for attention, pretraining, embeddings, frozen representations, and the conceptual contrast with fine-tuning.
- [x] Keep breaks at minutes 50-60 and 100-110; use 60-100 for small live extraction followed by cached full-data classification.
- [x] Use minutes 110-150 for validation comparisons across k-mer, CNN, and embedding workflows, including performance, computation, interpretability, transfer, domain shift, and leakage risks.
- [x] Freeze the workflows, model-selection decisions, preprocessing, and any decision thresholds before revealing the final test comparison; preserve a reproducible record of those choices.
- [ ] Use minutes 150-180 for the planned test comparison, evidence-based conclusions, recap, and buffer. Do not tune models or dataset settings against the revealed results.
- [x] Explain that revealed test results cannot become fresh independent evidence for post-reveal model tuning, including during the later agent demonstration.
- [ ] Deliver English-language HTML slides aligned with actual outputs, the comparison sequence, and terminology. Follow the installed frontend-slides workflow and visually inspect rendering and navigation.
- [x] Supply instructor guidance, ungraded interpretation questions, optional extensions, and clearly identified saved extraction/results contingencies. Mark live extraction unverified if it cannot actually be executed.
- [ ] Rehearse the full session's computational path and protected-test sequence in the supported environment and record timings, evidence, and any blockers honestly.


## Implementation handoff

The instructor explicitly requested all remaining development now and will paste/arrange standalone code and check Colab manually. This authorizes downstream implementation without pretending earlier manual gates passed. Use `paste_ready/README.md`, `instructor/guide.md`, `instructor/verification.md`, and the linked per-experiment records. Distinct student snippets and completed answers replace agent-produced notebook presentation for this handoff; original notebook-presentation checkboxes remain unchecked rather than falsely claiming `.ipynb` delivery.

The executable paths, scientific safeguards, and available teaching materials are locally developed. Actual Colab runs, a timed classroom rehearsal, the planned course test reveal, genuine agent screen recording, and actual Agentomics access/demonstration remain separate instructor work where applicable. Ready-for-human is not resolved or classroom-ready. The course test results remain uncalculated. No commits or pushes were made.
