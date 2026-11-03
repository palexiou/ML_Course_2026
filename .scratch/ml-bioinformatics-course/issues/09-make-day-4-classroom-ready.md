# 09: Make Day 4 classroom-ready, including Agentomics

**What to build:** A complete final session that introduces agent components, demonstrates specification-driven work, leads a scientific audit, and connects those lessons to an instructor-led Agentomics example. Deliver slides, observation/participation materials, and instructor guidance as one usable session.

**Blocked by:** 08: Deliver the agent specification-and-audit experiment.

**Status:** ready-for-human

- [x] Use minutes 0-10 to recap scientific specification and the evaluation boundary, and 10-50 to introduce LLM context, tools, agent loops, project instructions, and skills before inspecting the vague-request demonstration.
- [x] Keep breaks at minutes 50-60 and 100-110; use 60-100 for the explicit specification, project instructions, relevant skill, and clean-run comparison.
- [x] Use minutes 110-150 for the verified scientific-audit activity with known simulation truth, manual-workflow comparisons, and ungraded discussion.
- [x] Make optional agent participation and observation equally usable for the intended learning outcomes; require no student-run Agentomics workflow or additional paid service.
- [ ] Prepare and rehearse an instructor-led Agentomics demonstration for minutes 150-170, connecting automation to split integrity, experimentation, reproducibility, and scientific audit rather than teaching another required platform.
- [x] Reserve minutes 170-180 for final questions and course synthesis, preserving the approved 20-minute demonstration and 10-minute discussion allocation.
- [ ] Obtain the actual instructor demonstration access and materials needed for Agentomics; report missing capability promptly rather than inventing product behavior or treating an unverified substitute as a completed rehearsal.
- [ ] Deliver English-language HTML slides, instructor transitions, discussion prompts, and the audit handout aligned with actual demonstration outputs. Follow the installed frontend-slides workflow and visually inspect rendering and navigation.
- [ ] Integrate the clearly identified saved-output and recorded-agent contingencies; identify any additional demonstration limitations and rehearse the available route honestly.
- [ ] Record measured timing and remaining limitations, prioritizing specification and scientific discussion over exhaustive agent operation detail.


## Implementation handoff

The instructor explicitly requested all remaining development now and will paste/arrange standalone code and check Colab manually. This authorizes downstream implementation without pretending earlier manual gates passed. Use `paste_ready/README.md`, `instructor/guide.md`, `instructor/verification.md`, and the linked per-experiment records. Distinct student snippets and completed answers replace agent-produced notebook presentation for this handoff; original notebook-presentation checkboxes remain unchecked rather than falsely claiming `.ipynb` delivery.

The executable paths, scientific safeguards, and available teaching materials are locally developed. Actual Colab runs, a timed classroom rehearsal, the planned course test reveal, genuine agent screen recording, and actual Agentomics access/demonstration remain separate instructor work where applicable. Ready-for-human is not resolved or classroom-ready. The course test results remain uncalculated. No commits or pushes were made.


## Comments

### November 3, 2026 · Day 4 section-by-section breakdown

At the instructor's request, updated the [Day 4 story](../../../Slides/Day_4/story.md) to follow the approved Day 2 and Day 3 section-by-section breakdown format. It specifies all 53 content beats (10/9/8/8/11/7) plus two 10-minute breaks across the 180-minute structure (160 teaching minutes + breaks at 50–60 and 100–110). Every slide includes slide ID, timing, slide content, speaking notes, Point / reveal guidance, and a transition. Fully grounded in course artifacts:
- Division of scientific responsibility: "agent executes; researcher defends".
- Enforces evaluation boundary (Day 3 test data is historical, never feedback for Day 4 agent development).
- Deconstructs `vague-prompt.md` and its dozen silent assumptions.
- Analyzes the authored teaching fixture (`fixture.md` / `flawed_analysis.py`) with all four flaws: group leakage, preprocessing leakage, inverted positional array join, and biological overclaims.
- Details the five pillars of `precise-spec.md`.
- Establishes the three-tier instruction model (`specification.md`, `AGENTS.md`, and skills).
- Inspects the October 26 actual runs (explaining the 0.904 vague run vs 0.802 specified run as different search spaces/objectives rather than prompt superiority).
- Guides the hands-on audit with `06_scientific_audit.py` and `audit-checklist.html`.
- Protects the reserved 20-minute Agentomics demonstration (150–170) with clear contingency labeling.
- Concludes with the 10-minute whole-course synthesis (170–180) across Count → Learn → Reuse → Delegate.

Status remains ready-for-human pending slide build authorization and instructor review. This supersedes the preliminary 68-beat entry below.

### November 3, 2026 · Day 4 story specification drafted

Drafted the complete [Day 4 story specification](../../../Slides/Day_4/story.md) across six sections and 68 content beats within the 180-minute structure (160 teaching minutes + two 10-minute breaks at 50–60 and 100–110). Covers the core division of scientific responsibility ("agent executes; researcher defends"); enforces the evaluation boundary (Day 3 test data is historical, never feedback for Day 4 agent development); deconstructs the vague prompt and its dozen silent assumptions; analyzes the authored teaching fixture (`fixture.md`) with its group leakage, preprocessing leakage, inverted predictions, and biological overclaims; details the five pillars of `precise-spec.md`; establishes the three-tier instruction model (`specification.md`, `AGENTS.md`, and skills); inspects the actual October 26 clean agent runs (explaining the 0.904 vague run vs 0.802 baseline as different search spaces/objectives rather than prompt superiority); guides the hands-on audit with `06_scientific_audit.py` and `audit-checklist.html`; protects the reserved 20-minute Agentomics demonstration (150–170) with clear contingency labeling; and concludes with the 10-minute whole-course synthesis (170–180). All slide IDs, visible content, speaking notes, and workshop checkpoints are specced out. Status remains ready-for-human pending slide build and instructor review.

### November 2, 2026 · story-driven presentation revision

Rewrote the four-day HTML deck around questions, predictions, experiments, and evidence. Visible teaching text is approximately 52% shorter; detailed teaching content remains in expandable Notes references. Timings and scientific boundaries are preserved. All 60 scenes passed local Chrome layout checks at three viewport sizes, navigation, notes, local links, editing/export, and 60-page printing. See [presentation QA](../../../Slides/qa.md) for evidence and limits. The original bundled slide acceptance criterion is not claimed fully complete: the named frontend-slides skill was unavailable, classroom-output alignment remains an instructor check, and the actual Agentomics materials remain pending. Overall ticket status stays ready-for-human.
