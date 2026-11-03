# Presentation verification

## Full Day 1 implementation — 2026-11-03

The instructor authorized specifying Section 6 and then building the remaining Day 1 slides. The [actual deck](Day_1/presentation.html) has **112 slides**: 24 introduction, 18 regulatory patterns, 16 logistic regression, 16 metrics, 20 trees/forests, 16 explainability and two ten-minute breaks. The [active story](Day_1/story.md) contains visible-content and speaking notes for each section. All 42 opening records are preserved exactly; the former 40 later records are replaced, with legacy links mapped to the matching new concepts. Days 2–4 and the annotated outline are unchanged by this build. This supersedes the pending/stale-later-Day-1 status in the Section 2 report below.

Sections 3–6 use the approved short-title/one-visual layout and separated blue/orange figures. The persistent selected k-mers retain orange/blue/purple identity. Instructor notes retain toy versus empirical provenance without repetitive visible “Illustrative example” banners. Interactive figures cover sigmoid, actual one-weight logistic-loss descent, fixed-score threshold changes, ROC/PR selected points and the constructed tree's three paths. The loss illustration is distinguished from the actual L-BFGS fit in notes. Tree training explicitly depicts class separation. Forest trees operate in parallel and average probabilities. The primary interpretation uses the 15-position PPM and expected internal-window enrichment; old fixed-word benchmark/interpretation claims are removed from the current Day 1 deck.

**Scientific/notebook evidence:** the generated [Day 1 notebook](../notebooks/01_simple_signal.ipynb) was executed locally from a clean workspace through Sections 3–6. Focused Section 4 cells reuse predictions without fitting; Section 5 executes the canonical paired workflow; Section 6 verifies the full contribution sum and reads the paired feature tables. The [current validation record](../instructor/verification/day1-current.json) binds generator settings/files, exact source hashes, package versions and artifact hashes. Logistic validation ROC-AUC/AP = **0.608333/0.607054**; forest = **0.611875/0.597040**, on the same 240 rows. The deck reports both perspectives without assuming a universal winner. No tuning followed and no protected-test score was computed.

Verification:

- Offline Google Chrome at **1280×720 and 390×844**: all **224 slide/viewport combinations** pass fixed 16:9 stage, active/inert isolation, slide/control bounds, title clearance, SVG text-overlap and overflow checks. Desktop contact sheets and selected phone/full-size captures were visually inspected. Label overlaps found during the first pass were corrected. Phone output letterboxes the same stage; it does not claim full classroom readability on a phone.
- Sigmoid endpoints and reference values; eight monotone toy gradient steps/reset; confusion arithmetic at 0.5, cutoff extremes, undefined precision, ROC/PR point updates and constant ranking summaries; all three tree paths/reset; all 112 current anchors and legacy later anchors pass. Wheel/touch events on interactive figures do not navigate; calculated readouts are excluded from text editing.
- Notes/Escape and keyboard isolation, title selector, browser editing/autosave/reload, portable export/reopen and four day links pass. No script errors or network requests occur. Printing with notes open hides notes/controls and produces **112 PDF pages**.
- **13 tests** pass, including clean-workspace execution, no refitting in Section 4, alternate threshold and explanation-row checks, paired identity/label alignment, full probability reconstruction and an explicit block on reading protected test/truth tables as notebook inputs. Notebook hashes/exact teaching cells/syntax/empty outputs and deterministic regeneration pass. Mypy passes all 16 checked source files. Teaching arithmetic/timings and source fingerprint checks pass.
- Annotated outline SHA-256 remains `651f5eed4cfdaff0607cfc60764bbc6e1cd4693124106e2eca0b31614c824f12`. The first 42 records are byte-equivalent as JSON values to the approved pre-build records. Days 2–4 files retain their pre-build bytes.

Rebuild from [build_day1_slides.py](../tools/build_day1_slides.py); embedded interactions come from [day1_interactions.js](../tools/day1_interactions.js). Notebook checkpoints are generated from [build_course.py](../tools/build_course.py) and [day1_teaching.py](../tools/day1_teaching.py). Temporary screenshots, execution log, artifact files, contact sheets, printed PDF and browser verification scripts are under `/tmp/ml-day1-final/`; they are review evidence, not delivery dependencies.

**Limits:** instructor visual/content review, timed classroom rehearsal, projector readability and actual hosted Colab execution remain unverified. The new notebook/deck content is local and awaits the next push; the `main` Colab link does not yet serve these revisions. No commit or push was performed. Days 2–4 still need their own section review/design work.

## Section 2 implementation — 2026-11-03

The [actual Day 1 deck](Day_1/presentation.html#day-1-dna-section) now has **18 Section 2 slides**, displayed as **25–42**, and **82 slides total**: 24 opening + 18 revised + 40 retained later records. Section 2 starts at `day-1-dna-section` and ends at `day-1-dna-ready-for-model`; all 18 anchors, visible content and speaking notes are in the [existing story](Day_1/story.md#section-2). Its allocations sum to **1,500 seconds / 25 minutes**, including the splash, three biology slides, open representation discussion and brief CV explanation; the 50–60 break remains separate. This implements the instructor's later authorization, superseding the earlier fourteen-beat/spec-only status. No commit or push was made.

The revised flow is **TF protein → related binding sites/motif → position probabilities versus PWM scores → simulated labeled classification → fresh 15-base sampled sites → open representation discussion → overlapping k-mers → bag with multiplicity → counts/pros/cons → concrete feature/label table → train/validation/test purposes → emphatic test boundary → conceptual CV → classifier and inference handoff**. CV is brief optional depth, bootstrap mechanics belong in Section 5 forests (training rows sampled **with replacement**), and logistic regression is the next transparent baseline; these are agent recommendations for review, not a new execution protocol or a claim of model superiority.

Scientific input checks:

- The current [canonical configuration](../course_code/course_core.py) was inspected read-only after the generator agent's changes became available. The plotted primary matrix has 15 positions in A/C/G/T order, each distribution strictly positive, summing to one, with maximum at least 0.5. The slide transposes code's position rows into visual position columns. The zoom is actual position 5: **0.50/0.40/0.05/0.05**. The site is freshly sampled independently across positions for each planting and inserted at a uniformly random valid start; **0.95/0.05** are class-conditional planting probabilities, not deterministic class definitions. Matrix/source provenance and full table rows are in the story. This is a read-only teaching-input check; the [scientific verification record](../instructor/verification/README.md) owns generator/test/notebook evidence.
- The biological toy alignment `ACGT / ACAT / ATGT / ACGA` and its 4×4 position probabilities were independently checked. Its observed zeros are finite-sample frequencies, distinct from the strictly positive generative matrix. Position frequencies/probabilities are not mislabeled as log-odds PWM weights; background, smoothing and the scoring formula are in notes. TF binding and regulatory activity remain context dependent, with no empirical biological claim from simulated labels.
- Independently counted the constructed **21-base** string `TATACCGCGCGCGTATAAATG`: **18** overlapping windows, **14** distinct words, selected counts **TATA=2 / AATG=1 / CGCG=3**. This string has no assigned class and is neither a sample nor consensus of the new 15-position model. The separate table uses two newly regenerated 160-base **training** rows, with counts **2/1/1, label 0** and **1/0/2, label 1**; full count rows sum to **157**. No classifier was fitted and no test score was calculated or shown.
- Training learns parameters and fitted preprocessing; validation guides development; test evaluates the full frozen workflow at the planned Day 3 gate. The visible statement **NO DECISION EVER MADE ON TEST** is reinforced in notes for representation, preprocessing, model/hyperparameter/threshold choices and disappointing outcomes. Official final scoring is distinguished from prohibited test guidance. CV refits preprocessing inside training folds while the test remains outside all development folds. The course's threshold remains fixed at 0.5.

Local presentation verification used offline Google Chrome 143 via Playwright, with `file:` URLs and no server or shared browser/preview opening:

- Captured all **82 slides at 1280×720 and 390×844**, plus all seven recolored reference slides at both sizes. All **164 Day 1 slide/viewport combinations** passed fixed 16:9 stage, content/control bounds and active/inert-slide checks. New Section 2 SVG text was also checked for overlaps and bounds, then reviewed in desktop/phone contact sheets and focused full-size captures. Tight label spacing was corrected. Phone output deliberately letterboxes the same full stage; it is not a claim of comfortable phone reading.
- Every new slide has SAY, pointing and transition notes, timing and source context. Notes/Escape, navigation isolation while notes are open, arrows/Space/Home/End/Page Up/Down, title selection, all new anchors and old Section 2 aliases passed. The representation discussion has no answer key. Old Section 2 autosaves cannot override the new IDs; retained later edit keys still work.
- E editing/autosave/reload, HTML export and reopening after clearing storage passed; exported HTML retains 82 records, a single selector list and later sigmoid bindings. All four journey links opened the correct day deck, and all rendered local targets exist.
- The preserved sigmoid gives 0.500 at zero and approximately 0.731 at one; confusion-matrix arithmetic, threshold extremes/undefined precision, three tree paths and reset passed. Their behavior/logic is unchanged apart from requested figure color literals. Printing with notes open hides notes/controls and produces **82 PDF pages**. Embedded fonts, reduced motion and inline script syntax passed. No page script errors or external network requests occurred.
- All **64 retained slide records** (24 Section 1 + 40 later) preserve teaching content, order, anchors, notes, calculations and geometry; differences are the newly authorized figure colors. Section 3's concurrent story specification was preserved by targeted patches; its HTML was not redesigned. The annotated outline remains byte-identical with SHA-256 `651f5eed4cfdaff0607cfc60764bbc6e1cd4693124106e2eca0b31614c824f12`. Days 2–4 decks are unchanged by this task.

Palette coverage: Day 1 figures and the approved logistic reference now use separated **blue `#0072B2` / orange `#D55E00`**, pale fills with dark text, gray context and purple `#7B4FA3` only for a third track. Resting/class 0 is blue and activated/class 1 orange in the relevant examples; training is blue and validation orange across split/CV diagrams. The persistent count/contribution mapping is **TATA orange / AATG blue / CGCG purple**, with bias neutral. Labels, counts, position markers, outlines and arrows retain the meaning beyond color. Probability intensity uses one coherent blue heatmap. Section 1 class figures, later Day 1 figures and the reference were visually reviewed after recoloring. Legacy Days 2–4 have not received a broad palette rewrite. The approved layout, typography and paper/navy text remain intact.

**Remaining stale scientific claims and teaching transitions, deliberately outside this section's content rewrite:**

| Location in current Day 1 HTML | Required follow-up before teaching it as the new primary task |
| --- | --- |
| [`day-1-slide-48`, displayed 68](Day_1/presentation.html#day-1-slide-48) | Old primary validation ROC-AUC bars **0.802 / 0.907** are historical; neither describes the revised probability-motif generator. Regenerate/replace in that section's review. |
| [`day-1-slide-49`, displayed 69](Day_1/presentation.html#day-1-slide-49) | “Words inside the planted motif” assumes one fixed word. Interpret coefficients/importance against distribution-derived expected internal-window k-mer probabilities and background enrichment. |
| [`day-1-slide-50`, displayed 70](Day_1/presentation.html#day-1-slide-50) | “Our planted motif is TATAAATG” and the five fixed fragments are obsolete for the primary task. The retained Section 6 story beat 2 has the same dependency. |
| [`day-1-slide-51`, displayed 71](Day_1/presentation.html#day-1-slide-51) | The instructor cue that the forest had higher validation ROC-AUC depends on the old run; do not carry it forward as a new observed result. |
| [`day-1-slide-24`–`day-1-slide-27`, displayed 44–47](Day_1/presentation.html#day-1-slide-24) | The retained Section 3 opening repeats evaluation roles now taught in Section 2. Its new story spec can resolve this when its implementation is authorized. |
| [`day-1-slide-42`, displayed 62](Day_1/presentation.html#day-1-slide-42) and other later timing notes | Historical break/section timings still reflect the previous deck rather than the full current six-section story. Only Section 2's 25-minute allocation is implemented here. |
| [Historical speaking guide](Day_1/previous-teaching-guide.md), [annotated outline](teaching-outline.md#day-1), retained old-day slides | Earlier fixed-motif descriptions/results are historical source evidence. The outline annotations remain untouched. Review remaining sections against the latest scientific implementation before reuse. |

The family-memorization result at [`day-1-slide-59`, displayed 79](Day_1/presentation.html#day-1-slide-59), miniature examples and fixed-order interaction variant are **separate controlled variants**, not evidence that the new primary task is perfectly separable; they were not rerun or relabeled here. Section 3 illustrative weights and tree leaf probabilities remain explicitly teaching values.

Temporary scripts, screenshots, contact sheets, export QA data, printed PDF and verification JSON remain under `/tmp/ml-section2-dnrinkpo/`; they are not new review decks or course dependencies. The actual HTML is approximately **576,000 characters**; the user explicitly waived the earlier inline-preview size target and requested file links only. No useful content was stripped to meet that old target. Material limits: instructor approval, timed 25-minute rehearsal, projector conditions and actual Colab execution remain unverified; no protected-test reveal, new benchmark, model comparison or full scientific migration validation was performed by this slide task.

## Section 1 implemented for review — 2026-11-03

The [actual Day 1 deck](Day_1/presentation.html#day-1-intro-welcome) now begins with 24 new Section 1 slides, replacing the old opening records 1–12. It contains 74 slides total. The [story](Day_1/story.md#1-course-and-ml-introduction--025) lists titles, stable anchors, proposed allocations totaling 25 minutes, rationale and conceptual sources. The opening follows the approved logistic reference's Source Sans 3 typography and blue/white palette. Sections 2–6 retain their earlier content/design pending review; the older verification entries below describe their historical editions and counts.

Local Chrome 143 via Playwright opened `file:` URLs with the network offline; no server, desktop app, notebook execution or protected-test scoring was used.

- All 24 new slides were captured at **1280×720 and 390×844** and inspected in four contact sheets, with focused full-size inspection of the self-supervised/next-token slides. No detected title/content/SVG-text overflow or text overlaps. Phone rendering intentionally letterboxes the same fixed 1920×1080 stage; this does not establish comfortable phone reading or projector readability.
- All **148 slide/viewport combinations** (74 × two sizes) passed stage, content and toolbar bounds and active/inert-slide checks. Only one slide is active. A reduced-motion override now disables slide transitions fully, preventing the inherited tiny visibility-transition delay from leaving an inactive slide briefly visible. The required full base CSS is embedded; the new teaching style is scoped to Section 1.
- Arrows/Home/End, title selector, new descriptive hashes, old opening aliases and later source anchors passed. The first DNA example remains `#day-1-slide-13`, now displayed as slide 25. New intro IDs prevent old diagnostic autosaves from contaminating the new slides; seeded stale opening edits were ignored, while a seeded later edit retained its original source identity.
- Notes for every new slide, Escape, navigation isolation while notes are open, E editing/autosave/reload and exported HTML reopened after clearing browser storage passed. The final discussion has no expected-answer heading or answer key. Export retains all 74 records and interaction bindings; relative day/resource links work when the export stays beside the canonical deck.
- The **actual rendered QR at 1280×720** decoded with ZXing-C++ to `https://github.com/palexiou/ML_Course_2026`, matching the clickable link. All four journey links opened their actual day decks. The private-repository access requirement is in notes; anonymous access is not claimed. All rendered local file targets exist.
- Existing sigmoid values at 0 and 1, the shared confusion-matrix arithmetic, threshold extremes/undefined precision, all three tree paths and reset passed after insertion; sigmoid binding also passed in exported/reopened HTML. The entire later interaction script is byte-identical to its starting version.
- Printing while notes are open hides notes and controls and generates **74 PDF pages**. Embedded font loading, reduced motion, inline JavaScript syntax and Markdown local links/heading anchors passed. No page errors or external requests occurred.
- All **50 later serialized slide objects** match the starting HTML byte-for-byte, including their IDs and source content. Story Sections 2–6, Days 2–4 and the annotated outline remain unchanged. The outline SHA-256 is still `651f5eed4cfdaff0607cfc60764bbc6e1cd4693124106e2eca0b31614c824f12`.

The self-contained full deck is **499,787 characters / 500,238 UTF-8 bytes**, below the requested 512,000-character preview target; no duplicate Section 1 file or framework was introduced. Temporary screenshots, contact sheets, printed PDF, QR, validation scripts and results are under `/tmp/ml-course-section1/`. The parent can pass the actual file's HTML to `html_preview`, then `html_render`, to show the opening in chat; no `preview_*` browser tool was used. No commit or push was made. Instructor visual approval, measured 25-minute pace, projector conditions and actual Colab execution remain unverified.

## Later 2026-11-03 restructure verification

The instructor expanded cleanup after `ea59dd8`. [Slides/index.html](index.html) links four genuinely separate offline decks, retaining only each day's data and necessary scripts. The font is embedded; the [approved pilot](Day_1/logistic-style-reference.html) remains a distinct reference. This packages the existing design; section-by-section redesign is still ahead. The [root cleanup map](../README.md#cleanup-map--2026-11-03) records canonical paths.

Local Chrome 143 through Playwright opened `file:` URLs with network offline:

| Day | Slides / printed PDF pages | Layouts checked |
| --- | --- | --- |
| 1 | 62 / 62 | 1280×720 and 390×844 |
| 2 | 15 / 15 | 1280×720 and 390×844 |
| 3 | 15 / 15 | 1280×720 and 390×844 |
| 4 | 14 / 14 | 1280×720 and 390×844 |

- All 212 slide/viewport combinations passed content/footer, stage and control bounds checks. Screenshots were reviewed in eight contact sheets after waiting for stable rendered frames. Phone views intentionally letterbox the full slide, not a phone reading layout.
- Day-local arrows/Home/End/select/hash navigation, cross-day selector/numeric keys, earlier index hashes, notes/Escape, editing/autosave and exported HTML reopened with cleared storage passed. Exports retain only their own day. Day 1 sigmoid, threshold extremes and all three tree paths/reset passed.
- All rendered local links exist. Embedded font loading passed; no page errors or external requests occurred. Printing hides notes and controls and produces exactly the page counts above. Packaging checks caught and corrected a trailing blank-page rule and an inherited reduced-motion stage transition; capture assertions wait for rendered state.
- Exact original slide-record comparison passed after the reviewed relative-link and notebook-delivery wording transformations. The annotated outline retained SHA-256 `651f5eed4cfdaff0607cfc60764bbc6e1cd4693124106e2eca0b31614c824f12`. Source reviews changed only link targets; original chat history, scientific Python modules, requirements, miniature solutions and unrelated agent-workshop bytes were preserved.

Notebook/code checks are recorded in [course verification](../instructor/verification/README.md#packaging-checks--2026-11-03). Markdown local-link/heading checks, staged whitespace and artifact/secret-pattern review complement the rendering checks. Temporary screenshots, PDFs, export copies and machine-readable results stayed under `/tmp/ml-course-restructure/` (transient export files beside decks were removed). Actual Colab execution, projector readability and measured teaching pace remain unverified; protected test outcomes were not calculated.

## 2026-11-03 documentation and repository checkpoint

Checkpointed previously authorized course work at `2b242e2`, then consolidated navigation and drafted [day1-story.md](Day_1/story.md). The story is proposed pending discussion; this checkpoint does not claim a main-deck style conversion or classroom readiness.

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

## Day 2 Section 1 — 2026-11-03

Implemented the authorized twelve-slide opening, using native SVG DNA, count tallies, weighted connections, circular neurons and function curves. The HTML now has 25 scenes: the twelve new slides replace the original first two; the thirteen later scene records are preserved exactly. Sections 2–6 retain their earlier content, timing and historical results; this is a partial review build. The [story](Day_2/story.md#section-1) describes the new opening and retains the proposed full-day structure separately.

Local Chrome checks used offline `file:` loading at 1280×720 and 390×844, with reduced motion; keyboard checks also used normal motion. The twelve opening slides passed bounds, title/content separation, SVG text overlap, toolbar separation and active-slide isolation checks at both sizes. A rendered twelve-slide contact sheet and notes screenshots were visually inspected. Curve/caption spacing and visibility inheritance in the new notes were corrected before the final checks.

- No page script errors or HTTP(S) requests during the offline run.
- ReLU presets and keyboard slider input produce the expected positive and zero activations; hidden-unit selection updates its path, weights, bias and activation; the three-step forward pass and reset work.
- New and legacy deep links, Arrow/Home/End navigation, N/Escape notes, all twelve SAY/POINT/TRANSITION note records, preserved later edit keys and isolation from old opening autosaves were checked.
- A title edit survived Save HTML and reopening the export; the exported ReLU control also worked.
- Print produced 25 pages at 1440×810 PDF points, with notes excluded and the forward-pass figure at full contrast.
- The builder is deterministic and idempotent. Later scene records, other-day HTML and the annotated outline match their prior versions. The 21-base example’s eighteen overlapping four-base windows independently give TATA=2, AATG=1 and CGCG=3. Hidden/output arithmetic is a disclosed teaching construction, with no fitted-model claims.

Rebuild with `python tools/build_day2_section1.py`; interaction source is `tools/day2_section1_interactions.js`. Temporary screenshots, contact sheet, PDF, export and check output are under `/tmp/ml-day2-section1/` and are not presentation dependencies. No models or notebooks were executed for this slide build. Classroom pacing, projector readability and the remaining Day 2 redesign are still pending; no commit or push was requested.

## Day 2 Section 2 — 2026-11-03

Implemented the authorized fourteen-slide learning section plus the 50–60 break. The deck has 37 scenes: twelve preserved opening records, fourteen new learning slides, the new break and ten preserved later records. The previous loss/optimization scenes and first break are replaced; the retained one-hot scene follows the new break. Its original timing and the later legacy timings/results remain pending Sections 3–6 redesign. The [story](Day_2/story.md#section-2) owns editable speaking, pointing/reveal and transition notes.

Local Chrome verification used offline `file:` loading at 1280×720 and 390×844. All 27 implemented slides/break passed bounds, SVG text overlap, title/content separation (allowing the centered section splash), toolbar separation and active-slide isolation checks at both sizes. Rendered contact sheets and selected interaction states were visually inspected. The training return-arrow/caption separation was corrected during review. No page script errors or HTTP(S) requests occurred in the final runs.

- Loss presets reproduce 0.223/1.609/0.554; the selected-weight plot gives 0.598/0.554/0.513 at weights 1.1/1.2/1.3. Keyboard slider input stays on the slide and its tangent stays within the plotted domain at both endpoints.
- Parameter/bias selection, label reveal, three-stage backward tracing/reset, one-weight descent/reset, six-step small/large-rate paths and code highlighting were checked. The descent produces v₁≈1.243, p≈0.585 and loss≈0.536, matching independent arithmetic.
- The epoch diagram reaches 704 examples after eleven updates and 720 after twelve, then starts a new pass with a changed illustrative row permutation. These are schematic row positions, not real sample identities. Validation selection marks epoch 8 and distinguishes it from the last epoch 24.
- All new note records, N/Escape, Home/End/arrows, new and old deep links, old retained edit keys, isolation from obsolete loss autosaves and opening ReLU/hidden-unit controls passed checks. Selected controls were also clicked at phone size.
- A Section 2 title edit survived Save HTML, clearing browser storage and reopening the export; the exported weight-step control worked. Print produced 37 pages at 1440×810 PDF points, with notes excluded and completed descent/checkpoint/backward figures. Interactive state restored after printing.
- The Section 2 builder is idempotent. Rebuilding Sections 1 and 2 in sequence preserves their records. Section 1’s twelve records and the ten retained legacy records match the pre-build snapshot exactly. Other-day decks, the annotated outline, canonical training code and combined notebook remain unchanged. Documentation file links, source syntax and continuous 25-minute Section 2 timing were checked.

Rebuild with `python tools/build_day2_section2.py`; inline interaction source is `tools/day2_section2_interactions.js`. Temporary screenshots, contact sheets, PDF, exported HTML and check output are under `/tmp/ml-day2-section2/` and are not delivery dependencies. All new plotted numbers are constructed teaching examples with source/provenance in Notes. No model fitting, notebook execution, current CNN benchmark, protected test scoring, commit or push is claimed. Actual Colab execution, full-session timing and projector readability remain separate checks.

## Day 2 Sections 3–4 — 2026-11-03

Implemented the instructor’s request to build Section 3 and then Section 4: **sixteen detector slides**, **fourteen sequence-readout slides** and the separate 115–125 break. The [Section 3 opening](Day_2/presentation.html#day-2-s3-section) starts at scene 28; [Section 4](Day_2/presentation.html#day-2-s4-section) starts at scene 44. The deck has 64 scenes: 56 implemented teaching slides, two aligned breaks and six retained legacy scenes awaiting Sections 5–6. The first 27 records and those six later records match the pre-build version exactly. The [story](Day_2/story.md) supplies the editable speaking, pointing and transition notes. Its Section 3/4 timings reconcile to 30/25 minutes; they are allocations, not measured classroom pacing.

The interrupted build’s checks were repeated locally before delivery. Offline Google Chrome loaded the actual file at **1280×720 and 390×844**. All **128 scene/viewport combinations** passed stage/content bounds, 16:9 scaling, toolbar clearance and active-slide isolation after transitions settled. SVG text-overlap checks passed for the 58 implemented scenes. All 31 new scenes/break were captured at both sizes; their desktop contact sheets were visually inspected. No script errors or HTTP(S) requests occurred.

- One-hot base selection and column progression; match score and ReLU reveals; all six sliding-window responses; padding on/off; and the base mutation/reset passed. Independent calculations confirm `ACCGTCCG → (0,1,0,0,0,1)` and `ACTGTCCG → (0,0,0,0,0,1)` for the constructed CCG detector.
- Global max, one maximum per channel, moving/removing tied peaks, channel-major flattening, position-sensitive hidden features, branch concatenation, output class reveal, architecture tracing and learned-stage controls passed. Moving the selected peak changes the constructed score from 1.0 to −0.6 while the maximum stays 1. The actual head dimensions remain 2560 + 16 = 2576 → 32 → one logit.
- All 64 current anchors and the fifteen historical Day 2 links were exercised. Notes isolate navigation and close with Escape. Interactive wheel events stay within the figure; calculated readouts are excluded from text editing. Base mutation and positional controls also passed at phone size.
- A title edit survived autosave/reload, portable HTML export, cleared browser storage and reopening; the exported mutation control remained functional. Printing hid notes and produced **64 pages**. Staged figures completed for print and restored their live reveal state afterward.
- Sequential Section 3/4 rebuilds are byte-identical. Builder syntax, source arithmetic and protected-file hashes passed: other-day HTML, annotated outline, canonical runtime code and all notebook bytes remained unchanged by this completion pass.

Rebuild with `python tools/build_day2_sequence_slides.py 3`, then `python tools/build_day2_sequence_slides.py 4`. The builder reads the reviewed story and embeds [day2_sequence_interactions.js](../tools/day2_sequence_interactions.js); no server or external asset is needed. Temporary scripts, screenshots, contact sheets, layout/control results and PDF are under `/tmp/ml-day2-sections34/`, not delivery dependencies.

All new filter/map/readout values are teaching constructions with provenance in Notes. Additional guided notebook cells, current-generator CNN benchmarking, actual Colab execution, projector readability and full-session rehearsal remain pending. The six legacy scenes retain their earlier timing/results and are not evidence of completed Sections 5–6. No model fitting, notebook execution, protected test scoring, commit or push was performed for this slide build.

## Day 2 Sections 5–6 — 2026-11-03

Implemented the reviewed fourteen-slide [training/comparison](Day_2/presentation.html#day-2-s5-section) and fourteen-slide [representation control](Day_2/presentation.html#day-2-s6-section). The deck now has **86 scenes: 84 content slides + two ten-minute breaks**, with 160 teaching + 20 break minutes. All first 58 records (Sections 1–4 and both breaks) are preserved exactly. All six legacy ending scenes and their old primary benchmarks are replaced. Native illustrations, actual histories, selectable response maps and paired probabilities follow the approved sparse blue/orange style; third methods use purple plus distinct marker shapes. Provenance and interpretation limits live in instructor notes.

**Current evidence:** [day2-current.json](../instructor/verification/day2-current.json) binds notebook/scientific/teaching/rehearsal source hashes, generation identities, validation predictions, histories, selected epochs, package versions and artifact hashes. Seed 2026, CPU/two threads, 24 epochs, unchanged canonical architecture/defaults; no parameter search. Primary logistic/forest/CNN validation ROC-AUC is **0.608333/0.611875/0.546528** and AP **0.607054/0.597040/0.555691** (240 rows). The separate control gives ROC-AUC/AP **0.5/0.5/1.0** (96 rows). Selected CNN epochs are 2/1, earliest highest validation ROC-AUC. Aggregate primary/control workflow times are 6.35/1.89 seconds on the recorded local CPU environment, covering all three methods per variant; these are not CNN-only, setup or Colab times. Subsequent reader corrections/rehearsals reused the same fitted artifacts; the record explicitly distinguishes the final readback wall time from the original fitting times.

**Notebook:** the existing combined notebook now captures the full stage 03 output, reveals primary results first, verifies identities/row alignment and metrics, reloads the selected checkpoint, plots both histories, inspects a validation row/channel, checks all 48 validation pairs' complete 4-mer equality and bag probabilities, and stops before stage 04/05. Repeating the run cell reuses a compatible completed run without refitting. Canonical model/runtime source is unchanged. A generated Day 1 metadata fingerprint changed because the shared builder changed; exact equality of all Day 1 cells/scientific sources was checked and recorded in day1-current.json, without refitting Day 1 or changing its results.

**Checks:**

- Local headless Chrome, offline, reduced motion, **1280×720 and 390×844**, all 86 slides at both sizes (172 combinations). Fixed 16:9 scaling, bounds, SVG text overlaps, one visible/active slide and toolbar separation passed; no page errors or external requests. Screenshots/contact sheets were inspected for all 28 new slides, including final control states.
- Training checkpoint selection, probability/label reveal, three saved validation rows × sixteen response channels, ROC-AUC/AP switch, DNA-block swap, paired chance argument, positional/max readout toggle, primary/control switch and all three saved pair inspections passed. New controls also work at the phone viewport. Calculated readouts are excluded from text editing; figure gestures do not navigate.
- Exact new anchors and all fifteen historical source hashes resolve. Notes, keyboard navigation, local autosave, edited portable HTML export/reopen and both earlier/new controls after export passed. Printing produces **86 pages**, hides notes/controls, completes staged figures and restores the prior live state afterward.
- Generated notebook cells executed locally through the Day 2 boundary; package installation was skipped because dependencies were satisfied in a temporary environment. Checkpoint inference/CSV agreement uses absolute tolerance 1e-6 for float32 CNN values, and within-pair bag equality uses 1e-12. Independent reader checks verified no refitting/protected-table reads and rejected missing/wrong source identity, misaligned labels and a deliberately broken equal-count pair.
- All 13 existing tests passed. Notebook syntax, exact embedded sources/teaching cells, hashes, empty outputs and no executable reveal calls passed. Mypy with the documented flags passed all 22 source files; 243 local document links/anchors resolved, including historical redirects. Small builder parser assertions/type clarifications preserve rendered values. The complete Day 2 rebuild chain succeeds; repeating the final builder is byte-identical and retains the first 58 records. `git diff --check` passed.

Reproduce notebook evidence with `MPLBACKEND=Agg python tools/rehearse_day2.py` in an environment with the course ML dependencies; a fresh temporary workspace is the default. `--workspace PATH` reuses a complete compatible run. Rebuild the final sections with `python tools/build_day2_evaluation_slides.py`; changed scientific/notebook/teaching identities require refreshed evidence. Temporary screenshots, browser scripts, logs, PDF and full run artifacts are under `/tmp/ml-day2-sections56/`; the portable evidence record and self-contained deck are in the repository.

**Limits:** actual Colab setup/execution, projector readability, physical-device interaction and measured classroom pacing remain unverified. The five-minute activity allocations are teaching proposals, not measured completion promises. No protected test result was calculated or used for a decision. No commit or push was performed; the GitHub/Colab main link includes the new notebook after publication.

## Day 3 implementation — 2026-11-03

Implemented the [reviewed story](Day_3/story.md) as [67 scenes](Day_3/presentation.html): 11/12/9/7/12/14 content slides plus the two ten-minute breaks. The timing intervals are continuous from 0 to 180 minutes, with 160 teaching minutes. The fifteen legacy scenes and their primary fixed-motif benchmarks are replaced; their old Day 3 hashes route to corresponding new topics. Every content scene has SAY, POINT, TRANSITION, timing and numerical/source provenance in Notes.

The [current local evidence](../instructor/verification/day3-current.json) binds figures to the current generator, model/checkpoint/pooling contract, generated notebook and scientific/teaching sources. Frozen-embedding validation ROC-AUC/AP is 0.496597/0.545287 on the primary PPM task and 0.800347/0.757830 on the paired order control. All four workflows use matched validation IDs; no retuning followed. The pinned encoder config is 12 layers, 16 heads and width 512; weight SHA-256 matches the earlier verified checkpoint. See [computational verification](../instructor/verification/embeddings.md#current-ppm-lesson-verification--2026-11-03) for extraction/fit timings and limits.

**Local Chrome checks passed** (`file://`, offline, reduced motion):

- All 67 scenes at **1280×720 and 390×844**: 134 slide/viewport combinations. One visible fixed 16:9 stage, no stage/toolbar collision, no measured content overflow or SVG text overlap. Screenshots and six contact sheets inspected; a heatmap-caption collision was corrected before the final run. No JavaScript errors or external page requests.
- Mask/target reveal; attention weights at 0/0.25/0.5/0.75/1, with outputs 6/5/4/3/2; positional failure and ID-aligned repair; ROC-AUC/AP toggles for both variants; checklist interaction and phone controls. Conceptual masking/attention values are identified in notes; no figure claims start-codon detection, guaranteed embedding similarity or order-invariant contextual pooling.
- Test table starts with 16 empty metric slots and the comparison chart has no test bars. Only a **synthetic UI fixture** checked result-import plumbing; invalid input is refused, reload/export begins empty again, and importing executes no model or reveal. Manifest verification remains the notebook's responsibility. No real course test values were calculated or imported.
- All 67 canonical anchors and 15 historical routes; keyboard navigation, Notes/Escape behavior, interaction gesture exclusions, local title editing/autosave, exported HTML reopening and working controls. **67-page printing** hides notes/controls and exposes the masked target for the static handout.

**Notebook/code checks passed:** all 13 existing tests; mypy across 25 source files; four-notebook syntax, source/teaching hashes, exact embedded definitions/cells, empty outputs and absence of executable reveal calls; generated Day 3 cells executed locally through extraction, cache/prediction readback, synthetic alignment/rejection and validation comparison. A copied workspace passed the 32-artifact freeze and refused another freeze; the actual development workspace stays unfrozen and unscored. Repeated completed stage 04 reads without extraction/refitting. The shared notebook change required refreshing Day 2 evidence with its existing fitted artifacts, and updating the Day 1 builder fingerprint only after verifying all Day 1 cell bytes/scientific sources unchanged. The Day 1, Day 2 and Day 4 decks, Day 4 story, annotated outline, glossary, ADRs and scientific modules remain byte-identical. Checked 186 local document-link destinations and `git diff --check`.

Final reviewed artifact SHA-256: Day 3 HTML `7f168cac8218fd00cafb2cb1cf8447b3daeb8ad70ab20b1916c8c5289937932f`; combined notebook `e1b5642b8606c0a6824581b11a1d6731bfcc4fc29f8a47b65ec467afcac08eaf`. Maintainer screenshot/contact sheets, browser results, execution logs and the print PDF are under `/tmp/ml-day3/`; model/cache/development outputs remain outside Git. Rebuild with `python tools/build_day3_slides.py`; it refuses stale empirical source fingerprints.

**Not established:** instructor visual approval, projector readability, physical phone behavior, hosted Colab execution/setup/restarts, classroom network/download timing, measured teaching pace, and the actual authorised single test reveal. No commit or push in this task; the main-branch Colab badge receives these local cells after publication. The model card and [official AlphaGenome source overview](https://github.com/google-deepmind/alphagenome) were consulted; AlphaGenome's native schematic cites Avsec et al., Nature 649 (2026), doi:10.1038/s41586-025-10014-0 and is not a reproduced course result.


## Day 4 implementation — 2026-11-03

Implemented the [Day 4 story](Day_4/story.md) as [55 scenes](Day_4/presentation.html): 53 content slides (10/9/8/8/11/7) and two breaks. All intervals and stated durations are continuous through 180 minutes: 160 teaching minutes plus breaks at 50–60 and 100–110. Every content slide has SAY, POINT, TRANSITION, timing and provenance notes. The instructor selected the Agentomics audit-discussion fallback for 150–170; the last ten minutes remain course synthesis. No product behavior is claimed.

Native figures illustrate delegation, context/tools/loops, group overlap, positional versus ID-aligned evaluation, instruction documents, historical metric comparison, audit findings and the four-day progression. The [completed Day 4 notebook](../notebooks/06_scientific_audit.ipynb) follows GitHub → Colab → setup/definitions → authored fixture → STOP → fixture audit/negative probes → genuine historical readback. [Source-bound local evidence](../instructor/verification/day4-current.json) separates the deliberately authored 100% → 0% fixture from historical fixed-motif agent results. Historical vague ROC-AUC/AP is 0.9041667/0.8589; specified is 0.8019444/0.8024506. Both use exactly 240 validation predictions and pass group/duplicate-sequence checks. Different features and searches prevent a causal prompt-quality conclusion.

**Local Chrome checks** (`file://`, offline, reduced motion):

- All 55 scenes at **1280×720 and 390×844**, 110 scene/viewport combinations: fixed 16:9 scaling, one visible/active slide, content bounds, SVG text overlaps and toolbar separation pass. All scenes were captured; five desktop contact sheets and representative phone/control screenshots were inspected. Small document-icon line positions were corrected to keep strokes inside the page. No JavaScript errors or HTTP(S) requests.
- Tool-loop progression, clean-exit defect reveal, all twelve missing decisions, positional/ID-aligned join, historical ROC-AUC/AP switch and six FAIL/UNVERIFIED findings pass at both sizes. Chart metrics are visibly labeled. The optional five-minute discussion timer passes start/pause/resume/reset, pause on leaving and expiry using an artificial browser clock; it never advances slides.
- All 55 canonical anchors and 14 historical aliases; notes and keyboard isolation; interactive wheel exclusion; title editing/autosave; portable HTML export/reopen with working controls. **55-page printing** hides notes/controls and exposes clean-exit defects. Interactive charts print their current state; printing does not expand every alternative state into additional pages.

**Notebook/source verification:** all non-installation code cells executed in an empty temporary workspace with existing dependencies. No classifier training, new agent service, archive-code execution or course test access/reveal. The fixture deliberately fits its vocabulary on all four rows; source inspection supplies that finding. Shuffling predictions leaves ID-aligned metrics unchanged; duplicate/missing/unexpected IDs and invalid probabilities are rejected. The automated report cannot infer preprocessing or actual test-access history from probability tables. Historical checkout hashes use LF; explicit CRLF reconstruction matches the original Windows input hashes. Full archive sources remain unchanged.

All 13 existing tests pass; mypy passes 28 source files; four-notebook syntax, exact source/teaching cells, hashes, empty outputs and no executable reveal calls pass. Rebuilding notebooks and Day 4 HTML is deterministic. Complete earlier notebook cell records and scientific bindings were compared with pre-Day-4 snapshots before refreshing metadata-only builder/notebook fingerprints in Days 1–3 evidence records. No earlier model results or fitting were changed. All 61 pre-Day-4 protected file hashes match: Days 1–3 decks/stories, annotated outline, glossary, ADRs, scientific modules and workshop/archive files.

All 133 distinct checked local document/slide link destinations resolve; `git diff --check` passes.

Final artifact SHA-256: Day 4 HTML `9d5074634f65ba9c7ed901edc3627563a5c995373fa6a60cd2df3ff92c2631b4`; audit notebook `1e3dd6f2514522f423a7e2a090b6a3ffbfa409e3f9d701c9a8abcdde53678bf0`. Rebuild with `python tools/build_day4_slides.py`; refresh computational evidence with `python tools/rehearse_day4.py` after changing the bound sources. Temporary screenshots, contact sheets, browser checks, print PDF and execution log are under `/tmp/ml-day4/`, outside Git.

**Limits:** hosted Colab setup/execution, classroom pace, projector readability and physical-device behavior remain unverified. Existing local dependencies were used, not a clean package installation. Actual Agentomics access/demo and genuine agent video remain pending; the selected discussion fallback is implemented. Changes are uncommitted/unpushed, so the main-branch Colab badge receives the new cells only after publication.
