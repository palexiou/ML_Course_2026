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


## Comments

### November 3, 2026 · Day 3 section-by-section breakdown

At the instructor's request ("put this in the spec of Day 3 and do the same for all the sections"), rewrote the [Day 3 story](../../../Slides/Day_3/story.md) in the Day 2 format. It now has 65 content beats (11/12/9/7/12/14) plus two breaks. Each beat has content, notes, pointing/reveal guidance and a transition. Ideas from the instructor's earlier foundation-model deck are integrated. Facts were checked against `course_code/` and `instructor/verification/embeddings.md`, which corrected the earlier draft:
- Live extraction uses the first two training rows.
- Timings are the measured October 26 values.
- The model card excludes plants and viruses.
- Old fixed-motif primary scores are barred from the revised chart.
- The freeze completes before 150, and the reveal prints only test values, never prefilled.
- Caches are absent from Git, so a fresh Colab runtime extracts every row.

One deviation from the guide is flagged: extraction takes 60–80 instead of 60–75. This is a specification only; no HTML, notebook, run or reveal was performed, and the status remains ready-for-human. This supersedes the "70 beats" description in the entry below.

### November 3, 2026 · Day 3 story specification drafted

Drafted the complete [Day 3 story specification](../../../Slides/Day_3/story.md) across six sections and 70 content beats within the 180-minute structure (160 teaching minutes + two 10-minute breaks at 50–60 and 100–110). Connects Day 2 convolutional feature detectors to self-supervised pretraining (MLM) and attention mechanisms; pins Nucleotide Transformer v2 50M (`InstaDeepAI/nucleotide-transformer-v2-50m-multi-species`, revision `81b29e5786726d891dbf929404ef20adca5b36f1`) and CC-BY-NC-SA-4.0 license; details small live extraction vs full cached embeddings; enforces defensive sample ID cache alignment and sequence SHA-256 matching; compares k-mer, CNN, and embedding representations on validation data across compute, metrics, and domain shift; and details the formal 140–150 verbal freeze gate and explicit 150–165 test reveal protocol (`REVEAL THE FROZEN TEST RESULTS`). All slide IDs, visible content, speaking notes, and practical checkpoints are specced out. Status remains ready-for-human pending slide build and instructor review.

### November 2, 2026 · story-driven presentation revision

Rewrote the four-day HTML deck around questions, predictions, experiments, and evidence. Visible teaching text is approximately 52% shorter; detailed teaching content remains in expandable Notes references. Timings and scientific boundaries are preserved. All 60 scenes passed local Chrome layout checks at three viewport sizes, navigation, notes, local links, editing/export, and 60-page printing. See [presentation QA](../../../Slides/qa.md) for evidence and limits. The original bundled slide acceptance criterion is not claimed fully complete: the named frontend-slides skill was unavailable, classroom-output alignment remains an instructor check, and the actual Agentomics materials remain pending. Overall ticket status stays ready-for-human.

### November 3, 2026 · Day 3 implemented for instructor review

Implemented the reviewed [story](../../../Slides/Day_3/story.md) as [65 content slides plus two breaks](../../../Slides/Day_3/presentation.html), with native illustrations, attention/masking/alignment interactions and detailed cues. Open discussion replaces the earlier scored-choice beat; contextual pooling does not imply order invariance. The existing combined GitHub notebook now embeds live extraction, cache/prediction readbacks, the completed synthetic alignment exercise, identity failures and four-workflow validation comparison. This supersedes the earlier separate scaffold/completed-notebook delivery criterion: completed GitHub ipynb → Colab is the instructor-approved route, with separate scaffold material retained.

[Current local evidence](../../../instructor/verification/embeddings.md#current-ppm-lesson-verification--2026-11-03) records actual stage 04 execution and all four matched validation workflows, without tuning. A copied workspace passed a 32-artifact freeze and refused a second freeze. No reveal was run, no protected course test score exists, and the actual development workspace remains unfrozen. Test slides default empty and may import the saved result only after the instructor's classroom action. [QA](../../../Slides/qa.md#day-3-implementation--2026-11-03) records offline figures/controls/navigation/notes/export/printing. Status stays **ready-for-human** for visual approval, hosted Colab, classroom/network/timing rehearsal and the planned single reveal; local computational checks do not satisfy those remaining gates. No commit or push in this task.
