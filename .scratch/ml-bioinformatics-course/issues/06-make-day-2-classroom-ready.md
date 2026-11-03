# 06: Make Day 2 classroom-ready

**What to build:** A complete session connecting classical prediction to neural networks, one-hot DNA, a small CNN, and the verified interaction comparison, with scaffolded code, interpretation tasks, aligned slides, and instructor guidance.

**Blocked by:** 03: Verify the interaction-signal and CNN comparison.

**Status:** ready-for-human

- [ ] Provide scaffolded and separate completed notebooks covering the verified simple-signal CNN practical and interaction comparison, with matching answers and optional extensions.
- [x] Use minutes 0-10 for a recap of what k-mer features expose or discard; use 10-50 for neurons, activations, loss, optimization, a simple prediction calculation, and one-hot DNA.
- [x] Connect the limited mathematical notation to code and explain backpropagation conceptually; do not require gradient derivations or full CNN implementation from scratch.
- [x] Keep breaks at minutes 50-60 and 100-110; use 60-100 for convolution, pooling, selected missing code, and small CNN training.
- [x] Use minutes 110-150 for the verified interaction experiment and controlled sequence changes, comparing methods on the same dataset variants and split identities.
- [x] Preserve minutes 150-180 for representation, cost, interpretation limits, questions, and buffer. Do not turn the session into a predetermined CNN victory.
- [x] Keep development comparisons on validation data, with protected test results unavailable as tuning feedback.
- [x] Deliver English-language HTML slides aligned with notebook outputs and terminology. Follow the installed frontend-slides workflow and visually check rendered content, equations, labels, readability, and navigation.
- [x] Supply ungraded prediction/interpretation questions, completed answers, instructor transitions, and clearly identified saved outputs for slow or failed live training.
- [ ] Rehearse the practical and document measured computation time within the teaching blocks, limitations of interpretation, and which optional details to cut before scientific discussion.


## Implementation handoff

The instructor explicitly requested all remaining development now and will paste/arrange standalone code and check Colab manually. This authorizes downstream implementation without pretending earlier manual gates passed. Use `paste_ready/README.md`, `instructor/guide.md`, `instructor/verification.md`, and the linked per-experiment records. Distinct student snippets and completed answers replace agent-produced notebook presentation for this handoff; original notebook-presentation checkboxes remain unchecked rather than falsely claiming `.ipynb` delivery.

The executable paths, scientific safeguards, and available teaching materials are locally developed. Actual Colab runs, a timed classroom rehearsal, the planned course test reveal, genuine agent screen recording, and actual Agentomics access/demonstration remain separate instructor work where applicable. Ready-for-human is not resolved or classroom-ready. The course test results remain uncalculated. No commits or pushes were made.


## Comments

### November 3, 2026 · Sections 5 and 6 implemented

The instructor authorized “OK, implement them.” Built the [28 final slides](../../../Slides/Day_2/presentation.html#day-2-s5-section), preserving all first 58 records and replacing all six legacy endings: 86 total scenes. The existing combined notebook now captures/reuses stage 03, verifies identities/alignment, reads curves/checkpoints/maps, inspects paired counts/probabilities and stops before Day 3. A current default local PPM run supplies empirical figures; no tuning or test scoring followed. [QA](../../../Slides/qa.md#day-2-sections-56--2026-11-03) records notebook execution, thirteen tests, type/source checks, offline 172 slide/viewport combinations, controls/export and 86-page printing. Guided Day 2 delivery is implemented; actual Colab execution, pacing and projector review remain open, so overall status stays ready-for-human. No commit or push.

### November 3, 2026 · Sections 5 and 6 specified first

At the instructor's request, expanded [Section 5](../../../Slides/Day_2/story.md#section-5) and [Section 6](../../../Slides/Day_2/story.md#section-6) to fourteen proposed slides each, retaining minutes 125–155 and 155–180. Every beat includes visible content, speaking notes, pointing/reveal guidance and a transition. Section 5 follows setup, one supplied run, actual histories, selected weights, inference/map inspection and matched validation metrics; Section 6 follows a swapped-block pair through complete count equality, equal predictions, the ROC-AUC 0.5 limit, positional readout and a five-minute paired notebook inspection, then closes toward Day 3. The full-day story is now 84 content beats plus two breaks. Timing, architecture dimensions, links and an independent synthetic check of the boundary-preserving construction were verified. Guided notebook readbacks/stops, compatible current CNN outputs and rehearsal remain future implementation work. This task changed planning only; no HTML/notebook/runtime changes, fitting, test scoring, commit or push. Overall status remains ready-for-human.

### November 3, 2026 · Sections 3 and 4 implemented in sequence

The instructor explicitly requested “Section 3 and then Section 4”. Implemented the [sixteen DNA/detector slides](../../../Slides/Day_2/presentation.html#day-2-s3-section), then the [fourteen pooling/readout slides](../../../Slides/Day_2/presentation.html#day-2-s4-section) and 115–125 break. Interactive one-hot selection, scanning, score/ReLU, padding, base mutation, pooling/flattening, positional weights, branch joining and architecture traces follow the reviewed stories. The Section 3 activity is complete in the HTML; extra notebook teaching cells remain planned. The deck has 64 scenes, preserving the first 27 records and six later legacy scenes exactly. See [QA](../../../Slides/qa.md#day-2-sections-34--2026-11-03). All new numerical diagrams are constructions; no model fitting, notebook execution, protected test scoring, commit or push is claimed. Sections 5–6 and full-session rehearsal remain pending; status stays ready-for-human.

### November 3, 2026 · Section 4 specification expanded

At the instructor’s request, expanded the [existing Section 4 story](../../../Slides/Day_2/story.md#section-4) to fourteen proposed slides across minutes 90–115, plus the separate ten-minute break. Each slide has visible content, speaking notes, pointing/reveal guidance and a transition. The existing CCG/GTC/TCC maps support per-channel global max, information loss, channel-major flattening, a constructed position-sensitive hidden neuron, the actual concatenate/dense head, output probability, complete architecture and learned/fixed distinctions. The closing four-minute discussion precedes actual training in Section 5. Arithmetic, dimensions, timing and canonical-source alignment were checked; the full story now has 77 content beats plus two breaks. Sections 1–3 and 5–6 content, HTML, notebooks, scientific code and original annotations are preserved. No implementation, architecture change, new benchmark or test scoring is claimed; overall status remains ready-for-human.

### November 3, 2026 · Section 3 specification expanded

Continuing the established spec/review/build sequence, expanded the [existing Section 3 story](../../../Slides/Day_2/story.md#section-3) to sixteen proposed slides across minutes 60–90, including a five-minute guided inspection. Each has visible content, speaking notes, pointing/reveal guidance and a transition. One-hot DNA leads to a local neuron, a constructed CCG filter, match/nonmatch calculations, scanning, feature maps, shared weights, multiple filters, learning, nearby-feature composition and padding. The controlled one-base change preserves the second response while removing the first. Toy arithmetic, shapes and source alignment were checked; the full story now has 74 content beats plus two breaks. This is specification work: Sections 1–2 HTML, later sections, notebook/runtime code and original annotations are preserved. The short notebook checkpoint is proposed, not delivered; overall status remains ready-for-human.

### November 3, 2026 · Section 2 implemented for review

The instructor’s “OK go for it” authorizes building the reviewed learning spec. Implemented [fourteen Section 2 slides](../../../Slides/Day_2/presentation.html#day-2-s2-section) and the 50–60 break with interactive loss/gradient curves, backward traces, a single-weight step, step-size paths, twelve-update epoch progression, source-aligned code highlighting and checkpoint selection. Speaker notes carry the story’s SAY/POINT/TRANSITION and constructed-number provenance. Section 1’s twelve records and ten later legacy records are preserved exactly; the old loss/optimization and first break are replaced. The retained one-hot scene follows the new break, with later timings/results still pending redesign. The deck has 37 scenes. See [QA](../../../Slides/qa.md#day-2-section-2--2026-11-03). No notebook/model execution, test scoring, commit or push is part of this build; full-session acceptance and ready-for-human status remain unchanged.

### November 3, 2026 · Section 2 specification expanded

The instructor requested the Day 2 Section 2 spec after the illustrated opening build. Expanded the [existing story’s learning section](../../../Slides/Day_2/story.md#section-2) to fourteen proposed slides across minutes 25–50, each with visible content, speaking notes, pointing/reveal guidance and a transition. The sequence keeps Section 1’s numerical network, adds a one-weight gradient/update illustration, separates minibatches from epochs, walks through five training statements and distinguishes validation checkpoint selection from early stopping and inference. Native explanatory illustrations remain the visual direction. Hand calculations, timing continuity and source alignment were checked; no HTML, notebook or runtime implementation is claimed. Section 1 and the later story sections are retained; the full-day content count becomes 71 plus two breaks. Overall status remains ready-for-human.

### November 3, 2026 · illustrated Section 1 authorized

The instructor approved the twelve-beat opening and requested more illustrations with fewer box diagrams. Implemented [Section 1](../../../Slides/Day_2/presentation.html#day-2-s1-welcome) with native SVG DNA, count tallies, weighted connections, activation curves, circular neurons and offline ReLU/hidden-unit/forward-pass controls. The [story](../../../Slides/Day_2/story.md#section-1) remains editable and supplies SAY text; POINT, TRANSITION, timing and numerical provenance are in Notes. The opening replaces the original first two scenes; the thirteen later records, anchors and edit keys are retained. Sections 2–6 are still proposals; later historical results/timings are not claimed aligned. See [QA](../../../Slides/qa.md#day-2-section-1--2026-11-03). Full-day acceptance and ready-for-human status remain unchanged.

### November 2, 2026 · story-driven presentation revision

Rewrote the four-day HTML deck around questions, predictions, experiments, and evidence. Visible teaching text is approximately 52% shorter; detailed teaching content remains in expandable Notes references. Timings and scientific boundaries are preserved. All 60 scenes passed local Chrome layout checks at three viewport sizes, navigation, notes, local links, editing/export, and 60-page printing. See [presentation QA](../../../Slides/qa.md) for evidence and limits. The original bundled slide acceptance criterion is not claimed fully complete: the named frontend-slides skill was unavailable, classroom-output alignment remains an instructor check, and the actual Agentomics materials remain pending. Overall ticket status stays ready-for-human.

### November 3, 2026 · Day 2 story specification requested

After the full Day 1 review build, the instructor requested the Day 2 specification. The active editable draft is [Slides/Day_2/story.md](../../../Slides/Day_2/story.md): six 25–30-minute sections, 69 proposed content beats plus two breaks, and visible-content/speaking summaries throughout. This proposes a second break at 115–125 and explicit guided notebook checkpoints; it does not record approval of those changes or a new HTML build. The approved low-density Day 1 style and GitHub ipynb → Colab delivery carry forward. The obsolete paste-ready/snippet handoff above is historical; the existing combined notebook is the delivery target.

The primary generator is now the variable 15-position PPM. Historical fixed-motif primary CNN scores and runtime are not current evidence. A source-bound stage 03 rehearsal, guided notebook readback/stops, slide implementation, hosted Colab checks and classroom pacing remain open. The protected test boundary is unchanged. No runtime source, notebook, HTML, annotated outline or project decision was changed by this planning revision. Status remains ready-for-human; this specification alone does not satisfy classroom-readiness criteria.
