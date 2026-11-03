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
