# 05: Make Day 1 classroom-ready

**What to build:** A complete first session that one instructor can teach to 10-15 Python-capable master's students: in-class startup, a concise ML introduction, k-mer classification, valid evaluation, a random forest comparison, and the separate leakage investigation. Deliver the practical, answers, slides, and instructor guidance together.

**Blocked by:** 01: Verify the simple-signal classification workflow; 02: Deliver the split-leakage investigation.

**Status:** ready-for-human

- [ ] Provide distinct scaffolded and completed notebooks based on the verified workflow, with clearly marked missing-code tasks and interpretation questions rather than substantial coding from scratch.
- [x] Reserve minutes 0-10 for access checks and notebook startup during class; require no pre-course preparation or homework.
- [x] Use minutes 10-50 for a brief ungraded diagnostic, simulated promoter motivation, the concise ML map, sequence inspection, and k-mer features. Include classification versus regression and supervised, unsupervised, and self-supervised learning at the agreed introductory depth.
- [x] Keep the first break at minutes 50-60, the split protocol and logistic regression at 60-100, and the second break at 100-110.
- [x] Use minutes 110-150 for concise trees/random forests, working random forest code, validation comparison, and feature-importance interpretation against known simulation truth.
- [x] Fit the separate leakage investigation, discussion, recap, and buffer inside minutes 150-180 using the verified activity and its shorter route if necessary.
- [x] Protect final test results; student-facing Day 1 outputs support validation-based development and do not provide test-guided feedback.
- [ ] Deliver English-language HTML slides aligned with notebook steps, biological limitations, and canonical terminology. Follow the installed frontend-slides workflow, including visual-direction approval, and visually check rendered content and navigation.
- [x] Supply instructor transitions, expected answers, optional extensions, clearly identified saved outputs, and scope-reduction guidance that protects evaluation and interpretation before extra model detail.
- [ ] Rehearse the completed notebook and selected student exercises, record measured timings, and identify any mismatch with the 180-minute session rather than declaring readiness from timetable arithmetic alone.


## Implementation handoff

The instructor explicitly requested all remaining development now and will paste/arrange standalone code and check Colab manually. This authorizes downstream implementation without pretending earlier manual gates passed. Use `paste_ready/README.md`, `instructor/guide.md`, `instructor/verification.md`, and the linked per-experiment records. Distinct student snippets and completed answers replace agent-produced notebook presentation for this handoff; original notebook-presentation checkboxes remain unchecked rather than falsely claiming `.ipynb` delivery.

The executable paths, scientific safeguards, and available teaching materials are locally developed. Actual Colab runs, a timed classroom rehearsal, the planned course test reveal, genuine agent screen recording, and actual Agentomics access/demonstration remain separate instructor work where applicable. Ready-for-human is not resolved or classroom-ready. The course test results remain uncalculated. No commits or pushes were made.


## Comments

### November 2, 2026 · story-driven presentation revision

Rewrote the four-day HTML deck around questions, predictions, experiments, and evidence. Visible teaching text is approximately 52% shorter; detailed teaching content remains in expandable Notes references. Timings and scientific boundaries are preserved. All 60 scenes passed local Chrome layout checks at three viewport sizes, navigation, notes, local links, editing/export, and 60-page printing. See [presentation QA](../../../slides/qa.md) for evidence and limits. The original bundled slide acceptance criterion is not claimed fully complete: the named frontend-slides skill was unavailable, classroom-output alignment remains an instructor check, and the actual Agentomics materials remain pending. Overall ticket status stays ready-for-human.

### November 2, 2026 · instructor-led Day 1 revision

Implemented the instructor's annotations in `slides/teaching-outline.md`: a general course opening, supplied instructor identity, learning-map branches taught separately, individual metric definitions, a visual logistic-regression walkthrough, an interactive decision-tree path, explicit notebook activities, and a gradual bridge into related-sequence leakage. Day 1 now has 62 short slides, with speaking cues and transitions in Notes and a matching [teaching guide](../../../slides/day1-teaching-guide.md). The [notebook guide](../../../instructor/day1-practical.md) supplies the actual cells and distinguishes slide explanation from Colab execution. The annotated source was preserved. Local rendering, interaction, navigation, export, and printing checks passed; see [current QA](../../../slides/qa.md). Classroom timing and actual Colab verification remain open, so the overall issue remains ready-for-human.

### November 3, 2026 · style lock and story checkpoint

The instructor approved the clean logistic pilot style, with repetitive visible “Illustrative example” labels omitted when adapting production slides and provenance retained in notes/source. See [dated approval](../../../docs/course-wiki/teaching-preferences.md#style-approved--2026-11-03). The [active Day 1 story](../../../slides/day1-story.md) proposes six sections, 160 teaching minutes and two 10-minute breaks before section-by-section slide revision. Its later second break and changed startup arrangement remain proposals; earlier checked timing boxes describe the earlier implementation. The expanded teaching guide is historical in place; annotations and practicals are retained. Live student execution remains under discussion, not cancelled. [Colab findings](../../../README.md#github-notebooks-and-colab) establish direct opening support but no course `.ipynb` delivery or actual Colab run. Status remains ready-for-human; no classroom-readiness claim or new ticket layer.
