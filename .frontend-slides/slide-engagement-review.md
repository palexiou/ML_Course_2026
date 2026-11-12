# BioIT AI Engineering: slide engagement review

Reviewed the original **44-slide white/reference-style deck** on 12 November
2026. Read the actual HTML and Markdown teaching script, inspected all four
rendered contact sheets, and inspected selected full-size screenshots (including
the real skill file, Main Flow, grouped splitting, and its assertion).

These are **subjective pedagogical design judgements**, not empirical attention
measurements. A high score means the current presentation of the material feels
monotonous; it does not imply that the scientific content is wrong or unimportant.

## Rubric

| Score | Meaning |
| --- | --- |
| 1–2 | Purposeful change of pace; immediate, clear purpose. Preserve. |
| 3–4 | Concrete visual or interaction already anchors the explanation. Refine. |
| 5–6 | Useful example or artifact, but the default layout obscures its value. Annotate or enlarge. |
| 7–8 | Mostly verbal; another instance of the same headline/definition/two-column page. Redesign around the actual concept. |
| 9–10 | High monotony and a major missed opportunity to make a relationship or mechanism visible. Prioritise. |

Judgement combines visual sameness, need to translate prose into a mental model,
concreteness of the teaching example, and position in the surrounding sequence.
The original scores average **7.2/10**; **25 of 44** are 8 or above. This aggregate
is an editorial baseline, not a claim about measured student engagement.

## Principal finding

The deck has a useful conceptual order and careful definitions. Its problem is
that almost every concept is presented in the same visual form: large serif
heading, grey definition, then two ruled columns of prose or a small beige code
box beside prose. The diagram is often already latent in the explanation, but
students have to construct it themselves. By the final scientific section even
important advice looks like another page of notes.

Keep the explanations. Place them beside the mechanism, artifact, or example
they explain. Do not replace them with slogans, generic robots, stock DNA
imagery, or invented model-performance charts.

## Every original slide

Original numbering is retained here so that later inserted dividers do not
invalidate the review. Scores refer to the version before redesign.

| Original | Title | Boredom / 10 | Specific reason | Concrete visual or teaching redesign |
| ---: | --- | ---: | --- | --- |
| 01 | From copy-paste to coding agents | 8 | Opens like an interior reading page; the change in workflow is only described. | Draw the familiar student → chat → notebook → error → student loop next to an agent/tool loop. Keep an introductory paragraph explaining what moves between the parts. |
| 02 | What is a language model? | 8 | Two paragraphs explain an important distinction without making training versus use visible. | Draw two labelled phases: training data → parameter adjustment; then current context + trained model → response. Explain that reading a project file adds context rather than normally changing parameters. |
| 03 | System prompts and user prompts | 5 | Two real-looking prompt blocks give useful concreteness, but they sit as equivalent beige rectangles. | Present a labelled conversation stack with standing application guidance above the current user request. Keep the actual sequence assertion and mark both prompts as teaching examples. |
| 04 | What is a token? | 4 | Token chips introduce the first real visual encoding and relate to a definition. | Enlarge the chips and connect the text to token pieces. Add a small DNA/code text example without claiming measured boundaries; retain the tokenizer qualification. |
| 05 | How next-token generation works | 4 | The button supports explanation, but the tiny line is visually dominated by surrounding prose. | Make the expanding token strip the centre of the slide with a return arrow: context → next token → extended context. Preserve the explicit fixed-illustration label and avoid invented probabilities. |
| 06 | What belongs in the context? | 8 | “Information supplied to the model” remains an abstract list after several text slides. | Use a context tray containing labelled instruction, code, error, and small schema snippets. Put a repository outline outside the tray to show that files on disk are not automatically included. |
| 07 | The context window and longer tasks | 9 | A finite capacity and recoverable project record are explained only in prose; the first section ends on another list. | Show a schematic bounded context strip, older material becoming a summary, and a decision file read into a later request. Label the diagram as conceptual with no fake model capacity or percentage. |
| 08 | What is an agent? | 9 | A loop is literally listed as bullets; the major transition from text generation to action has no visual beat. | Use a large circular request/action/result loop with model, harness, and Python/files distinctly labelled. Keep the full definition above it and a short failing-check example beneath. |
| 09 | What happens during a tool call? | 6 | The grounded AGENTS.md example is good, but the return path must be inferred from a separate bullet list. | Draw a three-part trace: model requests `cat AGENTS.md` → harness executes → returned text enters the next request. Attach the actual rule to the result, not to generated narration. |
| 10 | Give an agent a bounded task | 6 | A practical prompt is present, but goal/scope/completion are not mapped to its lines. | Enlarge the brief and add callouts for goal, read-only scope, and observable evidence. Include a compact completion checklist aligned to these clauses. |
| 11 | What is a subagent? | 8 | Another paragraph beside a prompt does not make a second agent or context apparent. | Draw a main conversation handing a focused brief to a separate child context and receiving sources/findings. Keep both contexts labelled, with shared files drawn separately below. |
| 12 | A subagent can have its own configuration | 6 | Realistic YAML is useful but the explanatory list requires repeated eye-tracking between fields and prose. | Annotate the YAML directly: name/description, allowed tools, model, body. Add a read/search tool icon key and retain that this is an illustrative Claude Code configuration. |
| 13 | Why delegate into a separate context? | 9 | The benefit of a compressed handoff is described but not shown; this also repeats slide 11’s shape. | Show many search/cell snippets inside the child context becoming a short sourced handoff inside the parent context. Include one visible trade-off sentence: summaries can omit details and shared files remain shared. |
| 14 | What is a skill? | 8 | The package metaphor is an unillustrated list just before several similar file slides. | Make an opened instruction package with SKILL.md as the core and optional references/scripts/assets around it. Define the skill and distinguish guidance from tool execution explicitly. |
| 15 | Anatomy of a real SKILL.md file | 6 | The actual source is the right evidence, but annotations are distant bullets and the metadata/body division is not visible. | Enlarge the full verbatim grill-me file; bracket metadata and instruction body with short leader-line annotations. Highlight the explicit-invocation flag and show its supported-harness qualification. Preserve all source text. |
| 16 | The shared instructions explain the behaviour | 7 | Short source excerpts are valuable, but this looks like yet another code-plus-bullets slide. | Show grill-me → load grilling instructions → one illustrative question/answer round. Label quotations as source excerpts and the conversation as an authored example; explain that loading instructions is not spawning a subagent. |
| 17 | How a skill gets loaded | 9 | A three-stage loading mechanism is flattened into a list. | Draw discover → load SKILL.md → consult a referenced resource, with progressively opened documents. Preserve the explanation that detailed materials are read when relevant rather than all loaded initially. |
| 18 | How you ask to use a skill | 6 | Useful syntax looks like one generic code dump instead of the two interfaces students must recognise. | Put Claude Code `/grill-me` and Codex `$grill-me` in clearly named terminal/request strips. Beneath them explain availability, selection confirmation, and the idea to supply. Do not imply installation has happened. |
| 19 | What else can be in a skill folder? | 6 | The directory tree helps, but its relationship to executable actions remains in detached bullets. | Use an annotated file tree with short purpose labels at the leaves: guidance, executable helper, template. Distinguish reading a script from executing it with a tool. |
| 20 | What is an agent harness? | 9 | The essential “software around the model” relationship is expressed as another responsibilities list. | Draw a labelled harness enclosure around context assembly, model requests, permission checks, and tool execution. Keep files/tools outside the model itself and a short read-file walkthrough. |
| 21 | Models, harnesses, and T3 Code | 8 | The table is correct but asks students to mentally reconstruct the architecture. | Draw three connected bands for control surface, harness, and model; attach T3 Code, Claude Code/Codex, and configured model examples to their proper responsibilities. State boundaries can overlap. |
| 22 | T3 Code: start a working session | 9 | A slide about a graphical workspace contains no view of a workspace; its generic setup bullets could describe many tools. | Use a clearly labelled conceptual workspace illustration (or a verified current screenshot if available), marking project, selected agent, and task conversation. Keep a short explanation of the starting sequence; do not fabricate exact UI controls. |
| 23 | T3 Code: project, thread, and worktree | 8 | A table hides the most consequential distinction: another conversation does not create separate files. | Draw two task threads above a repository/folder map, then show a separately labelled worktree folder. Explain conversation separation versus working-directory separation; avoid implying every thread has a worktree. |
| 24 | T3 Code: inspect the work produced | 8 | A review checklist beside a long quote lacks the evidence it asks students to inspect. | Show an illustrative changed-code excerpt, a check result, and the completion report in separate labelled areas. Explain what each establishes; clearly mark any constructed run output as illustrative, preferably use the verified independent teaching assertions. |
| 25 | Matt’s grill-me: clarify an idea | 8 | Reintroduces the skill through prose and repeats earlier interview lists without showing an interview. | Show a short authored dialogue: broad intention → recommended clarifying question → explicit user decision. Keep the definition and explain who decides. Avoid using Exercise 10 as a prepared specification. |
| 26 | Choose the skill by where the answers are | 6 | The instructor’s routing table is concise and useful, but follows two earlier tables and has little visual orientation. | Preserve the exact four-row mapping with restrained source cues: your thinking, repository, another person, prototype. Use four labelled destinations or a decision map; do not turn alternatives into a mandatory pipeline. |
| 27 | Matt’s Main Flow: idea to checked work | 8 | Six rows are legible, but a requested flow looks like a reference table rather than an unfolding process. | Use a six-step connected artifact journey, with each skill name, one explanatory sentence, and output: decisions → spec → tickets → code/checks → review → improvements. Keep all six on one slide. |
| 28 | grill-with-docs: understand the project | 7 | A very short real wrapper occupies one beige panel beside another list; purpose is sound but visual rhythm stalls. | Show a repository excerpt feeding clarification and a glossary/decision note. Include the actual two-skill wrapper as a small source strip and distinguish inspected facts from agreed decisions. |
| 29 | to-spec: write down the agreement | 6 | The specification is concrete but resembles the preceding skill wrapper and subsequent ticket. | Present an annotated specification sheet: behaviour, edge cases, exclusions, acceptance. Tie each annotation to the actual small DNA policy and explain that to-spec records an existing agreement. |
| 30 | to-tickets: make a checkable increment | 7 | Another left code box repeats the spec, making the new abstraction hard to see. | Turn the current example into one task card with input, output, completion checks, and its policy dependency visible. Explain why this is a complete observable increment. Do not invent a large project plan. |
| 31 | implement: build and verify the behaviour | 5 | Python and assertions are concrete and audience-relevant, but execution is conveyed only by prose. | Show code and a small input/expected-result table (`ACGT`, empty, `ACNX`) aligned to the assertions. Use verified outputs only; preserve the stated string-input scope and simple explicit implementation. |
| 32 | code-review: check two different questions | 8 | The useful two-axis distinction is another evenly balanced prose layout. | Draw the same code/spec artifact examined by two labelled review lenses: standards and agreed behaviour, then aggregate findings. Give one concrete question per lens and retain that opinions need evidence. |
| 33 | retro: improve the next session | 9 | A hypothetical observation and proposal read as two final paragraphs at the end of a long uniform section. | Use an evidence → cause → proposed guidance timeline: empty-input ambiguity → repeated rework → record policy earlier. Mark the entire case as hypothetical and keep human review before adding guidance. |
| 34 | Define the scientific question first | 8 | Begins the most personally relevant section with another text page and a second example without a visual introduction. | Introduce the hypothetical gene-expression cohort with patient groups and sample tiles. Visually identify the unit of generalisation, then show the explanatory request for unseen-patient evaluation. |
| 35 | Give the assistant relevant evidence | 6 | Sample metadata is useful, but too small and disconnected from the expression data and split code it describes. | Turn the three invented metadata rows into a readable table linked by sample_id to a schematic expression matrix and split-code document. Explain joins and row/column meaning; no numerical results need be fabricated. |
| 36 | Resolve analysis choices before coding | 8 | Important design decisions appear as another dense list and quote after several similar slides. | Make a visible analysis decision sheet for grouping, missingness, metric, and validation. Show “unresolved → agreed” for one example and keep held-out test data outside model selection. |
| 37 | Make one change you can inspect | 8 | The definition is strong, but a long prompt and generic checklist do not make the scope boundary tangible. | Draw a small change boundary around split logic + overlap check, with model/metric outside the current change. Explain the bounded prompt alongside an illustrative cell/diff fragment. |
| 38 | Check what your evaluation measures | 10 | The scientific centrepiece is two paragraphs; patient leakage is much easier to understand when literally seen. | Make a large paired sample-allocation diagram: P01 samples crossing train/test versus all patient groups kept intact. Give each a full explanatory caption. No invented accuracy bars; state that grouped separation addresses one source of leakage. |
| 39 | Use examples with known answers | 5 | The deliberately failing assertion is excellent; students still have to compute the overlap from text. | Pair the code with two patient-ID sets and highlight P02 in the intersection. Show expected `AssertionError` as an illustrative expected outcome or verified teaching result, then explain the limited claim of a passing check. |
| 40 | Ask for evidence of completed work | 8 | Another long prompt beside a checklist repeats slides 24 and 37 without a new concrete artifact. | Show an evidence bundle: changed cell, actual check/returned result, remaining uncertainty. Connect each to a claim in a short completion report. Explain how a reviewer follows the claim back to evidence. |
| 41 | Record how the result was produced | 9 | Reproducibility is a process across time but is presented as static bullets and a paragraph. | Draw an analysis run path: identified inputs + environment/config + saved code → clean-kernel run → outputs. Add a compact manifest explaining seeds, versions, and saved split membership; no claim of universal bitwise identity. |
| 42 | Keep decisions with the analysis | 7 | The methods note is valuable, but after eight similar practice pages it feels like one more beige text box. | Present the note as a readable project artifact beside the relevant analysis/code outline, with links from question/grouping/metric to their rationale. Keep balanced accuracy explicitly illustrative. |
| 43 | Explain why you trust the analysis | 8 | A closing opportunity is used for another summary paragraph and list. | Turn it into an evidence-backed discussion page: show the cohort/split diagram with three question prompts about purpose, checks, and limitations. Preserve the explanation; invite a student to justify one decision before the demo. |
| 44 | Live Demo on Exercise 10 | 2 | Intentional minimal slide supplies a clear transition and is specifically constrained by the instructor. | Preserve only the exact visible words “Live Demo on Exercise 10”. No extra labels, illustration captions, feature list, or prebuilt demo. |

## Redesign priorities

1. **Mechanisms students need to understand:** original 08–09, 11/13, 15, 17,
   20–21. These are genuine diagram opportunities, not requests for decoration.
2. **Scientific interpretation:** original 34–35 and especially 38–39. Reuse
   patient identities and sample shapes consistently. Make leakage inspectable.
3. **Pacing at scale:** original 01, 07, 22–24, 27, 33, 41, 43. Each should use
   a different artifact or relationship instead of another pair of paragraphs.
4. **Retain the effective anchors:** token chips and next-token interaction,
   actual skill source, simple runnable Python, and deliberately failing overlap
   check. Improve their visual prominence rather than removing them.

## Flow and section beats

Keep the established conceptual order:

LLM → agent → subagent → skill → harness → Matt's workflow → scientific practice.

Three short explanatory dividers would give useful breathing room without
inserting a splash before every three-slide subsection:

- **Before original 08:** move from generating a response to acting on a project.
  Use one sentence explaining that tools return evidence for the next step.
- **Before original 20:** move from reusable instructions to the software that
  runs the session. A small composite map can recap model/agent/skill/harness.
- **Before original 34:** move from engineering mechanisms to scientific
  judgement. Introduce the hypothetical repeated-sample cohort and question.

The Main Flow overview (original 27) can itself act as a visual section anchor;
it does not need another empty title slide. The original 44 already supplies the
demo transition. Section slides should include a useful orientation sentence,
not a motivational slogan.

The six per-skill slides need family resemblance without duplicate layouts:
repository evidence for grill-with-docs, annotated agreement for to-spec, bounded
task card for to-tickets, code/checked inputs for implement, two review lenses
for code-review, and evidence-to-improvement timeline for retro. A small common
six-step progress rail can connect them.

## Visual direction and factual safeguards

- Retain the white background, Newsreader text, JetBrains Mono labels/code,
  beige material surfaces, fine rules, and restrained gold accents. Variation
  should come from composition and explanatory diagrams, not a different theme.
- Use native SVG/HTML for loops, context boundaries, annotated files, folder
  maps, and patient/sample grouping. These are crisp, editable, and meaningful.
- Differentiate patient/sample identities with labels and shapes as well as
  colour. Gold is an accent, not the only carrier of correctness or error.
- A conceptual workspace is acceptable if clearly labelled; it must not imply
  that invented controls or screenshots exist in the current T3 Code version.
- Keep the whole Main Flow overview, all six individual skill slides,
  grill-me/routing, and the three dedicated T3 slides. Do not collapse the deck
  back into slogans to create room for illustrations.
- Preserve separate model/harness/control-surface roles, separate context versus
  shared filesystem, skill loading versus spawning a child, and training versus
  supplying request context. Progressive loading details vary by harness.
- Use no invented clinical data, measured token splits, accuracy improvements,
  live tool outputs, or claims that a second LLM proves correctness. Label
  teaching scenarios and expected outputs appropriately.
- Preserve the final Exercise 10 constraint exactly. No notebooks, prepared app,
  reference HTML, or Downloads original need changing for this redesign.
- After redesign, verify all fixed-stage slides for text fit, overlaps, and
  legible annotations at desktop and phone scales. Added illustrations should
  earn their space by explaining a relationship.
