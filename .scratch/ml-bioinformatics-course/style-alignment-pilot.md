# Presentation style alignment pilot

2026-11-03 · Design findings and local validation; not classroom acceptance.

## Existing documentation and scope

No shared wiki, `docs/index.md`, or wiki directory was found in the project file inventory. Existing navigation starts at [README.md](../../README.md) and links to the slides, practicals, instructor guidance, and verification records. [docs/course-design.md](../../docs/course-design.md) records confirmed choices; [GLOSSARY.md](../../GLOSSARY.md) and [docs/adr/](../../docs/adr/) carry domain terminology/decisions. Agent conventions live in `docs/agents/`; local specs/issues live under `.scratch/<feature>/`, with separate numbered issues and Status lines. No wiki was created. A wiki location remains a user decision.

Delivered only [slides/pilots/day1-logistic-story.html](../../slides/pilots/day1-logistic-story.html) and this scratch report. Seven self-contained slides, plain white/blue teaching style, embedded Source Sans 3 font and license, inline SVG/CSS/JS. No course rewrite, main-deck integration, framework, deployment, PR, or commit. Existing user changes were preserved.

## Findings and source pointers

- The authoritative [annotated outline, original slide 09](../../slides/teaching-outline.md) asks for a more visual logistic-regression explanation; the instructor also questions ten minutes per slide. The [Day 1 guide](../../slides/day1-teaching-guide.md) already allocates several short slides per topic. Its 70–80-minute block maps to current Day 1 slides 28–31.
- [Current deck](../../slides/index.html#day-1-slide-28) teaches contributions, an interactive sigmoid, a decision, and fitting. Its arithmetic is explicit, but the illustrative counts do not originate from a visible sequence in that block. The pilot supplies that missing visual continuity; it does not claim the existing explanation lacks these concepts.
- Reviewed reference contact sheets: `/tmp/ml-transformers-style-review/render-contact-{1,2}.jpg` and `/tmp/ml-genomics-style-review/render-contact-1.jpg`, from PDFs in `/home/palexiou/ml-presentation-style-review/`. Transformers 2–4 builds relationship → ReLU → hidden units; 11–13 preserves one DNA sequence while changing its representation. Genomics 36–40 develops gene/RNA/protein → differential needs → regulation. The transferable teaching pattern is a stable drawing with one meaningful change per slide, followed by real figures once concepts are established.
- [ADR 0001](../../docs/adr/0001-controlled-sequence-classification.md) and [ADR 0002](../../docs/adr/0002-validation-for-development-protected-test-comparison.md) remain the boundaries: simulated classification, training-only fitting, validation development, frozen workflows before the planned Day 3 protected-test comparison, no test-guided tuning. [Practical B](../../instructor/day1-practical.md) fits the actual model later in Colab. Viewing this pilot executes no course workflow.
- [Slides README](../../slides/README.md), [QA record](../../slides/qa.md), and local issues 01, 05, and 10 distinguish local checks from pending Colab/classroom verification. Their statuses were not changed.

## Pilot mapping

| Pilot slide / stable HTML ID | Teaching change | Current Day 1 source | Suggested time |
| --- | --- | --- | --- |
| 1 · `dna-counts` | Trace DNA to three selected overlapping counts | 17–18 context; 28 | 1:00 |
| 2 · `learned-weights` | Add weights to the same count columns | 28 | 1:30 |
| 3 · `weighted-score` | Add products, bias, and total score | 28 | 1:30 |
| 4 · `sigmoid` | Trace score → curve → probability | 29 | 2:00 |
| 5 · `threshold` | Separate probability from decision rule | 30 | 1:00 |
| 6 · `decision` | Apply the rule; ask for the unknown true label | 30 | 1:00 |
| 7 · `fitting` | Explain training and the evaluation boundary | 31 | 2:00 |

The same invented 21-base sequence, `TATACCGCGCGCGTATAAATG`, appears on every slide. Its selected counts are TATA=2, AATG=1, CGCG=3. Illustrative weights +0.6, +0.8, −0.2 and bias −0.4 give z=1 and p≈0.731. Other observed words remain present; their weights are explicitly set to zero for this reduced illustration. Every slide labels the example as illustrative, not course results. The 0.5 course threshold is preserved. No observed label or biological conclusion is invented.

Notes provide what to say, what to point at, deliberate pauses/questions, expected answers, and the next transition. The final cue returns to main Day 1 slide 32. The ten-minute allocation is a proposal, not a timed rehearsal.

## Smallest reproducible editing workflow

Keep the annotated outline as the authority for instructor intent. For each approved section, record a short beat list: stable slide ID, concept, visible takeaway, diagram change, spoken explanation, pointing cue, and transition. Preserve those IDs when slide numbers move. Carry the source-outline section into the existing deck data's `source` field; the current deck already supports this mapping.

Use the existing slide data as the shared implementation record for HTML and the teaching guide. If repeated regeneration warrants automation, one small standard-library script can emit the guide from those same records; do not introduce a new presentation framework or Markdown compiler. Update an approved beat and its deck record together, then check the mapping and rendered slide before moving on. Browser-local edits/exported copies are review drafts: reconcile accepted wording back to the source before rebuilding. No synchronization tooling was built in this pilot.

## Validation and limits

Local Google Chrome 143 through `/tmp/ml-course-slide-qa-venv` Playwright, opening `file:` directly with network disabled:

- All seven slides checked at 1280×720 and 390×844: fixed 1920×1080 canvas, uniform 16:9 scaling, viewport/content bounds, diagram/takeaway/footer separation, one active visible slide, and no toolbar overlap. Screenshots/contact sheets inspected at both sizes.
- Keyboard arrows, Space, Page Up/Down, Home/End; wheel; synthetic swipe; stable hash links; all speaker-note fields and Escape; editing/autosave; exported HTML reopened after clearing storage; embedded font loading; reduced-motion behavior passed. No page errors or external requests were observed.
- Independent sequence-window counting and arithmetic confirmed the selected counts, z=1, p=0.731058579, and class 1 at threshold 0.5. The hypothetical 0.8 threshold would yield class 0 without changing p.
- Print output has seven pages and excludes controls/notes. The mandatory skill base CSS is included in full. Resize inspection found and corrected an inherited reduced-motion stage transition; print inspection found and corrected an extra blank page from the screen-reader announcement.
- SHA-256 comparisons confirmed that the main deck, annotated outline, teaching guide, README, prior QA, and practical guide remained byte-for-byte unchanged during this work.

Temporary evidence: `/tmp/ml-logistic-pilot/qa.py`, `qa-results.json`, `contact-1280.jpg`, `contact-390.jpg`, individual PNGs, and `pilot.pdf`. These are local inspection artifacts, not deck dependencies. Checks do not establish projector readability, physical-device touch behavior, other-browser compatibility, actual Colab execution, or classroom pacing. Phone rendering intentionally letterboxes a full slide; it is not a phone reading layout. Text edits can exceed the designed bounds and require another visual check.

Open the HTML directly; arrows/Space navigate, N opens notes, E edits title/takeaway wording, and Save HTML or Ctrl/Cmd+S exports a portable copy. The coordinating parent can present this HTML through `html_preview`/`html_render`; no preview tools, desktop apps, or server were used here.

## 2026-11-03 · Instructor feedback: more breathing space

Authoritative feedback on the first seven-slide pilot: “The slides are a bit too busy for my liking. Too many super-titles, sub-titles etc. I like the concept, but we need more breathing space on the slide”. This supersedes the original density/hierarchy choices. It retains the explanatory concept and model, and does not authorize a new palette chooser or course-content rewrite. Applied as frontend-slides Mode C, with the root glossary, accepted ADRs, and linked agent instructions preserved.

The original findings above remain historical evidence. Specifically superseded: the DNA appearing on every slide, the persistent full-pipeline story rail, repeated course/author headers and footers, takeaway blocks, dense table-style calculations, and editing “title/takeaway” wording. The current pilot has one short main title and one large focal figure per slide; E edits titles. The seven stable IDs and original teaching/source mapping remain unchanged. The earlier inventory statement about wiki absence describes the original inspection, not the current repository; this revision creates or edits no wiki.

Removed the repeated course labels, story breadcrumb rail, sequence-length subtitle, repeated author/course footer, and all separate takeaway blocks. Only a small “Illustrative example · not course results” disclosure and tiny page count remain on the stage. The figure area was redesigned at 1728×720 inside the same fixed 1920×1080 canvas, without preserving slots for deleted chrome or adding decorative panels. Essential scientific labels remain within the figures; transitions, qualifications, evaluation details, and pointing cues live in the instructor notes. This follows the historical MALTAomics DL pp. 29–31 precedent identified in [the source review](maltaomics-source-review.md): preserve the object being transformed and enlarge the operation under discussion.

| Slide / stable ID | Revised focal object; explanation preserved |
| --- | --- |
| 1 · `dna-counts` | One visible 21-base DNA string, marked overlapping windows, and three large selected counts. |
| 2 · `learned-weights` | The same three feature columns and counts, now paired with signed weights; omitted weights explicitly zero. |
| 3 · `weighted-score` | The same columns become products, then one sum with the bias identified and z=1.0. |
| 4 · `sigmoid` | One enlarged sigmoid, mapping the carried score z=1 to p≈0.731; axes, guides, and formula retained. |
| 5 · `threshold` | One probability number line and the two regions defined by the course threshold 0.5. |
| 6 · `decision` | Exactly the same probability dot and threshold positions, now applying the inequality and asking for the true label. |
| 7 · `fitting` | One training-data → fitting → weights/bias figure, with a small loss-reduction loop and evaluation-boundary reminder. |

The invented sequence remains `TATACCGCGCGTATAAATG`, with TATA=2, AATG=1, CGCG=3. Weights remain +0.6, +0.8, −0.2; products +1.2, +0.8, −0.6; bias −0.4; z=1; p=0.7310585786300049; class 1 at threshold 0.5. No true label or biological discovery is invented. Notes retain the 160-base course-sequence distinction, training-only vocabulary/parameter fitting, validation development, and workflow freezing before the protected Day 3 test comparison. Speaking allocations and return to main Day 1 slide 32 remain proposals, not rehearsal results.

### Packaging and verification for this revision

- Repackaged both complete embedded Source Sans 3 fonts from TTF to WOFF2 with existing fontTools/Brotli tooling. Both retain all 1,801 glyphs and identical character maps, glyph order, and advance metrics; the original copyright/OFL remains embedded. No course dependency was added. Final HTML: **244,468 bytes / 244,373 characters**, down from 677,089 bytes (63.9% smaller), below the CHAT tool's 512,000-character cap. Offline typography remains self-contained.
- Reused `/tmp/ml-course-slide-qa-venv` and revised `/tmp/ml-logistic-pilot/qa.py` to inspect the actual one-title/one-figure layout. Local Chrome 143 opened the file directly with network disabled. All seven screenshots were inspected at 1280×720 and 390×844; fixed 1920×1080 uniform scaling, 16:9 aspect, stage bounds, title/figure/footer separation, toolbar separation, and one visible active slide passed. Additional SVG text-bounds and pairwise text-overlap checks passed for every slide. Those checks exposed font-box spacing at the count/class labels and sigmoid formula; spacing was corrected before the final capture.
- Keyboard arrows/Space/Page Up/Page Down/Home/End, wheel, synthetic swipe, stable hash links, all note fields, Escape, phone note scrolling/close focus, E/hover editing, local autosave, saved HTML reopened after clearing storage, and Ctrl+S export passed. Normal-motion final layouts and reduced-motion behavior passed. No page errors or external requests occurred.
- Independent sliding-window counting and numerical arithmetic confirmed all selected counts, contributions, z, p, class 1 at 0.5, and the oral hypothetical class 0 at 0.8. The full mandatory viewport base CSS remains included. Print hides notes/controls and produces exactly seven 16:9 pages, confirmed with `pdfinfo`.
- SHA-256 checks against this revision's starting files confirm the main deck, annotated outline, teaching guide, slides README, earlier QA, practical guide, and glossary are unchanged by this work. Only the pilot HTML and this appended scratch record were edited; no wiki, commits, PRs, deployment, server, preview tools, or host-setup changes were made.

Temporary evidence remains under `/tmp/ml-logistic-pilot/`: `qa.py`, `extra-checks.py`, `qa-results.json`, `extra-results.json`, all fourteen viewport screenshots, `contact-1280.jpg`, `contact-390.jpg`, and `pilot.pdf`. These are inspection artifacts, not deck dependencies. The coordinating parent handles inline presentation; no `html_preview` or `html_render` attempt was made by this design task. Local checks do not establish projector readability, physical-device touch behavior, other-browser support, Colab execution, classroom pacing, or instructor acceptance. Phone output intentionally letterboxes the same slide. Subsequent title edits still require a bounds check.
