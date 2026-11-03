# Slide revision workflow history

Recorded on 2026-11-03. [Index and source snapshots](index.md#source-snapshots).

## Evidence and decisions available on 2026-11-03

- On 2026-11-03, the instructor retained the annotated [outline](../../Slides/teaching-outline.md) as authority for intent, with annotations preserved; the [latest visual correction](teaching-preferences.md#latest-visual-correction--2026-11-03) took precedence over earlier layering assumptions.
- On 2026-11-03, an **uncommitted working-tree observation** of the [Day 1 guide](../../Slides/Day_1/previous-teaching-guide.md) found several slides per explanation and separate explanation, question, expected-answer, and transition cues. This describes the hashed document snapshot, not committed deck behavior or classroom acceptance.
- On 2026-11-03, the **uncommitted pilot report** described a seven-slide logistic-regression proposal and local validation. Its reported checks did not establish projector readability, classroom pacing, or actual Colab execution; this wiki did not reverify the HTML.
- On 2026-11-03, the instructor reported a separate pilot revision in progress. Its changing file was outside this wiki task's inspection/editing scope; no completion or acceptance was inferred.

## Proposed editing sequence — 2026-11-03

On 2026-11-03, the agent proposed the following sequence, informed by the [pilot report's editing proposal](../../.scratch/ml-bioinformatics-course/style-alignment-pilot.md) and [reference findings](reference-materials.md). This was proposed practice, not a newly verified implementation.

1. **Intent:** Read the relevant annotated outline section and latest instructor correction. Record the concepts the instructor needs to explain; completion means each proposed slide serves an explicit concept or transition.
2. **Beats:** Sketch several focused slides for the explanation, keeping the example and visual positions stable. Record concept, meaningful visual change, spoken explanation, pointing cue, question/answer where useful, and transition; completion means the explanation can be followed step by step.
3. **Visual review:** Apply the [instructor's breathing-space preference](teaching-preferences.md), with supplementary detail in notes. Completion means the central visual explains the ML operation and visible hierarchy does not crowd it; retain enough labels/equations to teach the mechanism.
4. **Practical transition:** State when to switch to Colab, what to run or inspect, what students should notice, and when to return. Completion means an instructor can distinguish slide explanation from executable notebook work.
5. **Reconcile accepted edits:** Keep accepted wording and speaking cues aligned with their outline section and guide. Preserve stable identifiers where available; the pilot report proposed shared source records and reconciliation of browser-local drafts, but did not establish synchronization tooling.
6. **Validate the approved revision:** Inspect rendering, navigation, notes, and practical correspondence, then record what was actually checked. Treat measured pacing and actual Colab execution as separate evidence requirements.

## Scientific boundaries — decisions acknowledged 2026-11-03

On 2026-11-03, [ADR 0001](../adr/0001-controlled-sequence-classification.md) and [ADR 0002](../adr/0002-validation-for-development-protected-test-comparison.md), at the [repository commit recorded in the index](index.md#reading-and-authority), documented accepted simulated sequence classification, validation-based development, and a protected Day 3 test comparison after freezing workflows. The flawed split-leakage exercise remained a separate teaching activity under those decisions.

On 2026-11-03, the instructor clarified that these constraints should support clear ML teaching rather than dominate its framing. The proposed review checked alignment with those decisions without substituting repeated warnings for conceptual explanation.

## Handoff evidence — observed 2026-11-03

- On 2026-11-03, the uncommitted snapshots of [issue 05](../../.scratch/ml-bioinformatics-course/issues/05-make-day-1-classroom-ready.md) and [issue 10](../../.scratch/ml-bioinformatics-course/issues/10-rehearse-and-hand-over-course.md) recorded `ready-for-human`, with actual Colab checks and timed rehearsal still outstanding. Those observations did not establish classroom readiness; follow the issues for later evidence.
- On 2026-11-03, the instructor limited this task to the four wiki pages, with no source-report, outline, deck, ADR, or agent-rule changes, no commit/deployment, and no new tool framework or schedule.
- On 2026-11-03, the proposed next-session entry was [the index](index.md), then the relevant preference and source pages; any later accepted correction should receive a dated entry and explicit supersession where needed.

## Superseding checkpoint direction — 2026-11-03

On 2026-11-03, the instructor approved the clean pilot style and authorized documentation consolidation, commit and push. This supersedes the earlier wiki-only/no-commit scope and the entries recording the pilot revision as outside inspection or awaiting approval. The exact approval and production-label treatment are recorded in [teaching preferences](teaching-preferences.md#style-approved--2026-11-03).

On 2026-11-03, the instructor requested story discussion before further slide implementation. The active sequence became: edit [day1-story.md](../../Slides/Day_1/story.md), discuss section 1, implement that section with detailed notes, verify it, then continue section by section. The six-section timetable remained proposed; this checkpoint did not rebuild the main deck. The earlier six-step workflow above remains historical guidance, superseded where it assumes mandatory student execution or starts slide implementation before story discussion.

On 2026-11-03, the inventory found overlapping narrative entry points in the slides README, annotated outline, expanded guide and this proposed workflow. The checkpoint consolidated active narrative planning into the story and style authority into teaching preferences, shortened the README, and marked the expanded guide as historical **in place**, preserving its links and cues. It retained the annotated outline, practical cells, accepted timetable history, ADRs/glossary, local tracker, source reviews and agent-workshop material. No physical moves or new archive index were needed.

On 2026-11-03, the recommended demonstration/optional-follow-along route remained a proposal, and [README findings](../../README.md#github-notebooks-and-colab) distinguished GitHub-to-Colab support from absent course notebook packaging and untested execution. No notebook, execution protocol or source report was rewritten. The earlier material was checkpointed at `palexiou/ML_Course_2026@2b242e2`; use [QA history](../../Slides/qa.md) for this checkpoint's limited checks, separate from the earlier rendering reports.

## Later instructor clarification and packaging — 2026-11-03

On 2026-11-03, the instructor expanded cleanup and confirmed the topic sequence and GitHub/Colab delivery; see the [single decision record](teaching-preferences.md#later-instructor-clarification-and-packaging--2026-11-03). This supersedes the earlier in-place-only scope. The [root map](../../README.md#cleanup-map--2026-11-03) records implemented moves, per-day decks and consolidated practicals/notebooks. Continue detailed story discussion and section-by-section style application; packaging does not establish a completed redesign or Colab rehearsal.

## Actual opening implementation authorized — 2026-11-03

On 2026-11-03, the instructor supplied the concrete Section 1 sequence and authorized immediate slide implementation; this supersedes the earlier requirement to stop at another general planning report. Follow the [latest direction](teaching-preferences.md#actual-section-1-direction--2026-11-03). The [actual Day 1 deck](../../Slides/Day_1/presentation.html#day-1-intro-welcome) now has a 24-slide opening for review, followed by the 50 preserved later records. The existing story carries the slide list, rationale and sources; do not create a parallel planning/report hierarchy.

Validate offline `file:` rendering at 1280×720 and 390×844, fixed-stage scaling, whitespace and overlaps, active-slide isolation, notes, editing/export/reopen, real QR decoding, relative day links, print page count with notes hidden, reduced motion and the later sigmoid/threshold/tree controls. Use stable new intro IDs so old diagnostic autosaves cannot override new slides; preserve later source-ID anchors and edit keys. Keep per-slide timing proposals in notes. Record evidence and limits in [QA](../../Slides/qa.md), retain the outline bytes and other-day decks, and leave Sections 2–6's style conversion for separate instructor review. No notebook execution or protected-test reveal is needed for slide QA.

## Section 2 discussion scope — 2026-11-03

On 2026-11-03, the instructor provisionally accepted the opening and requested the next section's specification; see the [dated direction](teaching-preferences.md#proceed-to-section-2-specification--2026-11-03). The agent drafted [Section 2 in the existing story](../../Slides/Day_1/story.md#section-2), with 14 proposed slide IDs, separate visible content and speaking paragraphs, and a 25-minute allocation. These are discussion beats, not implemented slides or instructor approval of the proposal; this supersedes the earlier story instruction to wait for Section 1 review before proceeding.

On 2026-11-03, this task's validation scope was Markdown links/anchors, timing arithmetic, independently counted overlapping windows, and comparison with canonical simulation/feature logic. Reading the existing early DNA HTML records supplies continuity only; no browser work, HTML edits, notebook changes, model fitting, test-score reveal, new planning hierarchy, commit or push belongs to this specification task. Deliver file links in chat. The previous rendering checklist applies when slide implementation is separately authorized, not as a reason to open this draft in a browser.

## Section 2 implementation and palette authorized — 2026-11-03

On 2026-11-03, the instructor authorized proceeding from the discussion draft to actual Section 2 slides; see the [superseding teaching and dataset decisions](teaching-preferences.md#revised-section-2-variable-sites-and-test-purpose--2026-11-03) and [palette correction](teaching-preferences.md#figure-palette-correction--2026-11-03). This supersedes the preceding spec-only/no-HTML boundary. Keep the annotated outline intact, apply targeted Section 2 story patches to preserve concurrent Section 3 specification work, and preserve later HTML teaching content except authorized figure colors. The scientific agent owns generator/notebooks/tests/ADRs/glossary; read-only input checks do not transfer that ownership or establish new scientific results.

On 2026-11-03, implementation uses the frontend-slides [skill](/home/palexiou/.codex-router/skills/frontend-slides/SKILL.md), its fixed-stage CSS/architecture, and the approved logistic reference. The user's existing style and explicit file-link-only instruction supersede the skill's new-style discovery, automatic opening and preview suggestions. Check actual offline Chrome screenshots at 1280×720 and 390×844, text and diagram bounds, notes/navigation/edit/export/reopen/print/reduced motion, day links, and unchanged later interactions. Record evidence, stale later scientific claims and coverage in [QA](../../Slides/qa.md#section-2-implementation--2026-11-03). No scientific results, protected-test reveal, commit or push is part of this slide task.
