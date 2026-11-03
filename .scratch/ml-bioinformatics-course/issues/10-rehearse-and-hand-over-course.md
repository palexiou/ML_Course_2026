# 10: Rehearse and hand over the complete course

**What to build:** A coherent student and instructor course package with clear entry points, reusable resources, and a documented end-to-end rehearsal establishing what is actually ready for the classroom across all four sessions.

**Blocked by:** 05: Make Day 1 classroom-ready; 06: Make Day 2 classroom-ready; 09: Make Day 4 classroom-ready, including Agentomics.

**Status:** ready-for-human

- [ ] Provide clear student and instructor entry points for scaffolded notebooks, separate completed notebooks, course dataset variants and generation code, HTML slides, the one-page scientific-audit checklist, and instructor guidance.
- [x] Ensure every day is English-language and aligned with canonical terminology, the accepted simulation limitations, and the four-day timetable. Do not introduce homework, grading, compulsory submissions, or pre-course setup requirements.
- [ ] Rehearse the completed notebooks in sequence from fresh supported environments without hidden variables, unrecorded files, or prior-session state; distinguish intended student exercise placeholders from completed-notebook failures.
- [ ] Verify actual Colab behavior for required practicals and record any separately verified simple-laptop path, dependency setup, accelerator use, memory/runtime conditions, and execution costs. Do not infer Colab readiness from local-only runs.
- [x] Check correspondence among dataset generation settings, sample identities, split identities, model configurations, cached embedding provenance, notebook outputs, and known simulation truth across all sessions.
- [x] Verify validation-only model development, the isolated leakage exercise, frozen Day 3 workflows, and the absence of post-reveal test-guided tuning portrayed as independent evaluation.
- [x] Rehearse representative missing-code exercises, answers, optional extensions, and the Day 4 observation route so students without agent access can complete the intended scientific discussion.
- [ ] Exercise saved-output and recorded-agent contingencies separately from live execution; verify artifact availability and clear labels without treating contingency success as missing live or Colab verification.
- [ ] Visually inspect all rendered slides and the one-page checklist for readability, labels, equations, overflow, navigation, and agreement with actual notebook and demonstration content.
- [ ] Record measured setup and computation time within each 180-minute teaching envelope, including breaks, explanation, exercises, discussion, and buffer; preserve the final Agentomics and synthesis allocation.
- [x] Document the agreed cut-first priorities, one-instructor teaching guidance, access arrangements, and any genuine capability blocker requiring instructor help.
- [x] Deliver a concise rehearsal record distinguishing passed, failed, not-run, and blocked checks. Do not mark the package classroom-ready while required checks remain failed, blocked, or unverified.
- [x] Keep the parent spec unchanged and avoid unrelated infrastructure, hosted services, mandatory export formats, or new course scope during the handover.


## Implementation handoff

The instructor explicitly requested all remaining development now and will paste/arrange standalone code and check Colab manually. This authorizes downstream implementation without pretending earlier manual gates passed. Use `paste_ready/README.md`, `instructor/guide.md`, `instructor/verification.md`, and the linked per-experiment records. Distinct student snippets and completed answers replace agent-produced notebook presentation for this handoff; original notebook-presentation checkboxes remain unchecked rather than falsely claiming `.ipynb` delivery.

The executable paths, scientific safeguards, and available teaching materials are locally developed. Actual Colab runs, a timed classroom rehearsal, the planned course test reveal, genuine agent screen recording, and actual Agentomics access/demonstration remain separate instructor work where applicable. Ready-for-human is not resolved or classroom-ready. The course test results remain uncalculated. No commits or pushes were made.


## Comments

### November 2, 2026 · story-driven presentation revision

Rewrote the four-day HTML deck around questions, predictions, experiments, and evidence. Visible teaching text is approximately 52% shorter; detailed teaching content remains in expandable Notes references. Timings and scientific boundaries are preserved. All 60 scenes passed local Chrome layout checks at three viewport sizes, navigation, notes, local links, editing/export, and 60-page printing. See [presentation QA](../../../../slides/qa.md) for evidence and limits. The original bundled slide acceptance criterion is not claimed fully complete: the named frontend-slides skill was unavailable, classroom-output alignment remains an instructor check, and the actual Agentomics materials remain pending. Overall ticket status stays ready-for-human.
