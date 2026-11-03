# Presentation verification

## 2026-11-03 documentation and repository checkpoint

Checkpointed previously authorized course work at `2b242e2`, then consolidated navigation and drafted [day1-story.md](day1-story.md). The story is proposed pending discussion; this checkpoint does not claim a main-deck style conversion or classroom readiness.

- All repository Markdown local file links and Markdown heading anchors passed the checkpoint check, including retained source reports and corrected issue links. The unchanged main deck's 22 distinct local resource/asset targets exist.
- The annotated outline retained SHA-256 `651f5eed4cfdaff0607cfc60764bbc6e1cd4693124106e2eca0b31614c824f12`. The main deck and both scratch source reviews retained their starting bytes. The earlier teaching-guide body was retained except for one trailing space, with a historical-status notice prepended.
- The pilot's only file change removed one trailing space from its embedded font-license text; figures, notes, styling and scripts were unchanged. Inline JavaScript syntax checks passed for the main deck and pilot. Earlier rendering/interaction checks below and in the pilot report were not rerun or recast as new evidence.
- Checked six teaching allocations total 160 minutes, plus 20 minutes of breaks; independently checked the short sequence's selected counts, score/sigmoid calculation and shared confusion-matrix arithmetic. These checks establish consistency, not teaching pace.
- Read Google's official GitHub integration notebook and FAQ, inspected the existing scripts/practical cells, and confirmed private repository metadata. The [README](../README.md#github-notebooks-and-colab) records direct-opening support, absent course `.ipynb` files and concrete setup gaps. No model training, expensive downloads, Colab execution or protected-test scoring was performed.

Staged review includes whitespace and secret/artifact-pattern checks. No new datasets, notebook outputs, external reference attachments, screenshots, model files or temporary QA artifacts belong to this checkpoint. Projector readability, execution/setup timing and the final live-participation choice remain open.

## Current edition: expanded Day 1

November 2, 2026. Rebuilt Day 1 from the instructor's annotated outline into 62 shorter slides; the complete deck now has 106 slides. The supplied instructor identification is Panagiotis Alexiou, ERA Chair, University of Malta. The original annotated `teaching-outline.md` is byte-for-byte preserved. The new `day1-teaching-guide.md` maps every new slide to its original outline section and provides matching speaker cues.

Local verification used Google Chrome 143.0.7499.192 through Playwright:

- Rendered and visually reviewed all 62 Day 1 slides in seven contact sheets.
- Checked geometry for all 106 slides at 1920×1200, 1366×768, and 390×844: no detected content overflow, footer overlap, or stage/control overflow in 318 combinations.
- Checked the sigmoid at scores zero and one; probabilities are 0.500 and approximately 0.731.
- Verified the shared metric example: TP 30, FP 10, FN 20, TN 40; accuracy 0.70, precision 0.75, recall 0.60, F1 2/3. Checked both threshold extremes, including undefined precision when there are no positive predictions.
- Followed all three interactive decision-tree paths and checked reset behavior.
- Checked day navigation, the title-based slide selector, day-local hashes, input-field arrow handling, and speaker notes including Escape.
- Checked text editing, local autosave, HTML export, reopening with cleared local storage, retained interactive bindings, and the absence of duplicate selector entries after export.
- All linked local targets exist. No page script errors were reported.
- Print rendering exposes all 106 slides; the generated PDF has 106 pages and excludes notes.
- Compared the data objects for the 44 Day 2–4 slides with the preceding edition: their teaching content is unchanged.
- Confirmed that Day 1 timing intervals continuously cover 0–180, with breaks at 50–60 and 100–110. These are allocations, not measured classroom duration.

The notebook guide's Python blocks compile. Its data-inspection and completed fitting cells were exercised on the existing 720 training and 240 validation examples from the saved specified run. These checks use development data only. Practical C/D artifact names were checked against their producing scripts. Actual Colab execution and projector readability remain instructor checks.

Temporary screenshots, the PDF, and machine-readable verification output are in `/tmp/ml-course-day1-review/`. No server is required to open the deck. The browser automation preview rejected the `file:` protocol, so verification used local Chrome directly.

## Earlier edition: 60-slide story rewrite

November 2, 2026. Scope: the story rewrite of `index.html`, verified locally with Google Chrome 143.0.7499.192 through Playwright. This is presentation verification, not a Colab check or a timed classroom rehearsal.

## Editorial changes

- Retained all 60 scenes and their original day/timing assignments.
- Rebuilt the visible content around questions, predictions, experiments, and interpretation; retained the existing blue/white design and local font.
- Reduced visible teaching text from approximately 5,000 to 2,416 whitespace-delimited words, excluding navigation, timing labels, and notes: a 51.7% reduction. The median scene has 41 words by this measure. Counts use the rendered content strings, including chart text, as an approximate editorial measure.
- Replaced the four numerical result tables with charts of the same recorded validation results. Axes run from zero to one; the chance-ranking reference is 0.5. Scores are rounded to three decimal places on screen; full recorded values remain in the reference.
- Kept the original teaching content in expandable technical references within Notes, including detailed settings, worked examples, caveats, expected answers, and contingency guidance.
- Changed the vague-request scene to open the actual vague run before the specified-run comparison. The authored flawed fixture remains clearly separate from actual agent behavior.

## Local checks

All 60 scenes were rendered and inspected in four contact sheets. Layout bounds were checked for every scene at 1920×1200, 1366×768, and 390×844 CSS-pixel viewports. The phone check verifies scaled layout and controls, not comfortable reading of a projected slide on a small screen.

| Check | Result |
| --- | --- |
| Script execution | No page script errors |
| Content bounds | No detected content/footer overlap or content overflow in 180 scene/viewport combinations |
| Stage and controls | Inside the viewport with no toolbar overlap at the checked sizes |
| Keyboard | Arrows, Home/End, and numeric day jumps work |
| Day selector and deep links | All four day starts, `#day-3`, and `#slide-27` checked |
| Inactive scenes | Inert; only the current scene participates in interaction |
| Notes | Open, expand reference, scroll without changing slides, close with Escape |
| Text editing | Edit, autosave, reload, and export checked |
| Portable HTML | Exported edit survives clearing browser-local storage and reopening the export beside the assets |
| Local links | All local file targets in scenes and technical references exist |
| Print | 60 pages at 1440×810 PDF points; all scenes visible, notes excluded |
| Scientific boundaries | Charts use existing validation values; no course test scores calculated or inserted |

The checks found and corrected note-keyboard navigation and transitions affecting print visibility. Print styles now disable transitions and animations. Screenshots, the test PDF, and execution records were produced in `/tmp/ml-course-slide-work/`; these temporary QA outputs are not classroom dependencies.

## Remaining limits

The frontend-slides skill named in the original tickets was not available in this session; this revision uses the established deck and the user's requested editorial direction. No skill-based visual approval is claimed.

Projector readability, actual printer settings, full-session pacing, and actual Colab outputs still need instructor verification. The Day 3 reveal remains gated and has no prefilled results. The Agentomics scene remains a reserved slot with preparation explicitly pending, because access, actual example, materials, and rehearsal have not been supplied. A genuine agent screen recording remains pending. These limits do not prevent reviewing the rewritten presentation.
