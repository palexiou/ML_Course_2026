# Day 4 story

**Section-by-section breakdown for instructor review — 2026-11-03.** All six sections are specified slide by slide. Each slide has an ID, a timing, the slide content, speaking notes, pointing/reveal guidance and a transition, following the format established in Day 2 and Day 3. These are discussion beats, not implemented slides. The [current Day 4 deck](presentation.html) still holds its 14 earlier scenes. Titles, emphasis and pacing remain editable.

**Working title:** Specifying, delegating, and scientifically auditing machine learning workflows.

**The story:** Over the first three days, we hand-built models, explored deep architectures, evaluated pretrained embeddings, and protected our evaluation boundary. Today we confront a new collaborator: AI coding agents. Who owns the scientific claim when an agent writes the code? The agent executes; the researcher defends. We inspect what happens when an agent receives a vague request ("Build the best promoter model"), contrast an authored flawed teaching fixture with genuine recorded agent runs, and learn how to constrain agents using precise specifications, persistent project instructions (`AGENTS.md`), and reusable audit skills. Students perform a hands-on scientific audit using our audit checklist and code, evaluate an automated workflow in Agentomics, and synthesize the four-day journey across count, learn, reuse, and delegate.

**End-of-day understanding:** Large language models predict tokens from context; agents use tool loops to read, edit, and execute code; vague requests force agents to make silent assumptions about targets, splits, and metrics; fluent code and 100% accuracy claims do not imply scientific validity; sample ID alignment and group split integrity must be verified independently; instructions and skills clarify expectations but do not guarantee truth; and all scientific claims remain the sole responsibility of the human scientist.

**Delivery and style:** Use the approved speaker-led style: one short title, one main visual, generous whitespace, blue `#0072B2` / orange `#D55E00` contrast, letters and shapes as well as colour, and detailed notes. Prefer explanatory illustrations (split matrices, loop diagrams, instruction pyramids, audit tables) to plain boxes. The required observation route works completely from local text files under `agent_workshop/` and Python scripts under `course_code/`, requiring no agent account, internet service, or payment. All discussion is ungraded. Practicals fit strictly within contact hours.

---

## Three-hour shape

| Minutes | Section | Main question | Teaching minutes |
| --- | --- | --- | --- |
| 0–25 | 1. Who owns the claim when an agent writes the code? | What changes when an agent writes the code? | 25 |
| 25–50 | 2. When instructions are vague: silent decisions and flaws | What happens when we leave scientific choices unsaid? | 25 |
| 50–60 | Break | | — |
| 60–80 | 3. Specifying the experiment: contracts and boundaries | How do we turn scientific intent into an unambiguous contract? | 20 |
| 80–100 | 4. Giving instructions a job: AGENTS.md, skills, and actual runs | Can instructions guarantee a correct scientific result? | 20 |
| 100–110 | Break | | — |
| 110–150 | 5. The scientific audit: evidence, consequence, and repair | How do we audit an analysis independently of its execution? | 40 |
| 150–180 | 6. Automated workflows and scientific responsibility | What must remain human scientific responsibility? | 30 |

**160 teaching minutes + 20 break minutes = 180 minutes.** There are 62 content beats (10/10/8/8/13/13) and two break slides. All timings are suggested allocations, not measured pacing. The breaks stay at minutes 50–60 and 100–110. Section 6 explicitly protects the reserved 20-minute Agentomics demonstration (150–170) and the final 10-minute whole-course synthesis (170–180), as recorded in [instructor/guide.md](../../instructor/guide.md#day-4--specify-delegate-and-audit).

**Sections:** [1 · Who owns the claim?](#section-1) · [2 · Vague prompts and fixtures](#section-2) · [3 · Precise specification](#section-3) · [4 · Instructions and actual runs](#section-4) · [5 · Scientific audit](#section-5) · [6 · Agentomics and responsibility](#section-6) · [Workshop plan](#workshop-plan) · [Evidence and scope](#evidence-and-scope)

---

<a id="section-1"></a>

## 1. Who owns the claim when an agent writes the code? · 0–25

**Story question:** When an AI coding agent generates and executes your analysis, who is responsible for the scientific claim?

**Exit understanding:** Define the division of responsibility between agent execution and human defense; recall the Day 3 evaluation boundary (Day 3 test data is historical, never feedback for Day 4 agent development); distinguish an LLM from an agent; explain context windows, tools, and the agent loop; and understand why exit code 0 is an engineering observation, not scientific evidence.

**Teaching thread:** Start by asking who defends a scientific claim when software writes the code. Move through: the division of responsibility → the Day 3 test boundary → what an LLM does (predicting tokens in context) → what tools add → the agent loop → the danger of trusting a clean exit code → observation route access.

**Scope and delivery:** This section is conceptual and conversational: no code execution or accounts needed. Connect directly to the evaluation lessons of Days 1–3.

### S1-01 · The new collaborator

**Proposed slide ID:** `day-4-s1-welcome` · **Time:** 0:00–1:30 (1:30)

**What is on slide:** Day 4 title banner. An illustrated split graphic: on the left, a researcher writing a hypothesis; on the right, an AI agent terminal generating Python scripts; connecting them is an arrow labelled "Delegation". The four-day journey indicator highlights Day 4.

**What I want to say:** Welcome to Day 4. Over the past three days, you have manually engineered features, trained neural networks, extracted transformer embeddings, and sealed an evaluation test set. Today we step into the modern reality of computational biology: delegating implementation to AI coding agents.

**Point / reveal:** Reveal the researcher on the left, then the agent terminal on the right, then the delegation arrow.

**Transition:** But before we look at code, who stands behind the results?

### S1-02 · The division of responsibility

**Proposed slide ID:** `day-4-s1-core-principle` · **Time:** 1:30–4:00 (2:30)

**What is on slide:** Two contrasting stone tablets:
- Left tablet (**The Agent: Execution**): Generates syntax, calls tools, handles runtime errors, formats tables, writes draft reports.
- Right tablet (**The Scientist: Responsibility**): Formulates question, designs splits, verifies leakage, defends claims in peer review.
Banner below: *"The agent executes; the researcher defends."*

**What I want to say:** Here is the foundational rule of Day 4: The agent executes; the researcher defends. If an agent writes code that leaks validation data, misaligns sample IDs, or invents biological claims, you cannot tell a peer reviewer or an examination committee, "The AI wrote it." You own the claim.

**Point / reveal:** Show the agent tablet first, then the scientist tablet, then underline the banner below.

**Transition:** That responsibility begins with enforcing our evaluation boundary.

### S1-03 · The Day 3 evaluation boundary reminder

**Proposed slide ID:** `day-4-s1-boundary-reminder` · **Time:** 4:00–7:00 (3:00)

**What is on slide:** Padlocked vault graphic from Day 3. Banner: *"Day 3 test scores are historical evidence, NOT agent targets."* A red barrier prevents any Day 4 agent from touching `protected_test.csv`.

**What I want to say:** Before we touch any agent tool, let us enforce our scientific boundary. Yesterday we revealed our protected test set. Those test sequences and scores are now historical facts. They are strictly sealed from Day 4. An agent tasked with developing a model today must work exclusively with development data (train and validation). Revealing test results to an agent would contaminate the entire experiment.

**Point / reveal:** Show the sealed vault, then draw the red barrier between Day 4 and the test data.

**Transition:** To understand what an agent can do, we must understand how it works.

### S1-04 · What is an LLM? Context and token prediction

**Proposed slide ID:** `day-4-s1-llm-basics` · **Time:** 7:00–10:00 (3:00)

**What is on slide:** Diagram of a context window: input prompt tokens $\rightarrow$ transformer attention layers $\rightarrow$ probability distribution over vocabulary $\rightarrow$ sampled next token. A callout highlights that the model has no persistent memory outside its active context window.

**What I want to say:** At its core, a Large Language Model is a statistical token predictor. Given a sequence of text tokens in its context window, it calculates the probability distribution of the next token. It does not "think" or "know biology" in a human sense; it predicts text that plausibly follows from the context it was given.

**Point / reveal:** Animate tokens entering the context box, the attention matrix lighting up, and the next token appearing.

**Transition:** What transforms a text predictor into an active agent?

### S1-05 · From LLM to Agent: Giving the model tools

**Proposed slide ID:** `day-4-s1-what-is-agent` · **Time:** 10:00–13:00 (3:00)

**What is on slide:** Transformation graphic: LLM alone (text in $\rightarrow$ text out) + Tools (read file, write file, execute bash terminal, python) = AI Coding Agent. An illustrated terminal shows the agent typing `python train.py` and reading the console output.

**What I want to say:** What turns a language model into an agent? Tools. When we equip an LLM with structured function calls—reading local files, writing code to disk, running shell commands, and inspecting errors—it ceases to be a passive chatbot and becomes an autonomous software agent.

**Point / reveal:** Reveal the LLM box, attach the tool icons around it, and show the terminal execution.

**Transition:** How does the agent decide what to do next?

### S1-06 · The Agent Loop: Inspect, Act, Observe, Revise

**Proposed slide ID:** `day-4-s1-agent-loop` · **Time:** 13:00–16:30 (3:30)

**What is on slide:** Circular loop flowchart:
1. **Inspect Context** (read prompt, history, and workspace files) $\rightarrow$
2. **Act** (call tool: `run_command("python train.py")`) $\rightarrow$
3. **Observe** (read tool output: `SyntaxError: line 14`) $\rightarrow$
4. **Revise** (generate patch, edit file, rerun) $\rightarrow$ Loop back to 1.

**What I want to say:** An agent operates in a continuous loop: Inspect, Act, Observe, Revise. It reads the current context, chooses a tool action, observes the result from the operating system, and decides what to do next. If a script crashes, it reads the traceback and modifies the code until the command exits successfully.

**Point / reveal:** Trace around the loop clockwise, highlighting the transition from error output to code edit.

**Transition:** But there is a silent trap in this loop.

### S1-07 · The danger of the successful exit code

**Proposed slide ID:** `day-4-s1-exit-code-zero` · **Time:** 16:30–20:00 (3:30)

**What is on slide:** Split view:
- Left (**Terminal output**): `Exit code: 0`, "Model trained successfully!", "Accuracy: 100%". Green checkmark.
- Right (**Inside the Python script**): validation data leaked into training, IDs misaligned. Red warning.
Banner: *"A clean run is an engineering observation, not scientific evidence."*

**What I want to say:** This is the central pitfall of coding agents. The agent loop is optimized to achieve an exit code of zero. If a script runs without errors and prints "Accuracy: 100%", the agent reports success. But whether the underlying science is valid—whether groups leaked, or IDs were joined properly—is completely invisible to the terminal exit code.

**Point / reveal:** Show the green terminal on the left first. Pause. Then reveal the red scientific error inside the code on the right.

**Transition:** How will we explore this today?

### S1-08 · Participation routes today: Operator or Observer

**Proposed slide ID:** `day-4-s1-participation-routes` · **Time:** 20:00–22:30 (2:30)

**What is on slide:** Two parallel, equally valid paths:
- Path 1 (**Observer**): Uses provided local text files, inspects pre-recorded genuine runs, audits code and fixtures by hand; 100% complete learning outcomes; zero accounts or payment.
- Path 2 (**Operator**): Uses existing local agent access in a clean development directory.

**What I want to say:** For today's activities, no one needs to sign up for a service, enter a credit card, or configure an API key. We provide a full Observation Route with genuine pre-recorded runs, authored fixtures, and completed audit scripts. Observers and operators answer the exact same scientific questions.

**Point / reveal:** Show both paths side by side, emphasizing that all core discussion questions are identical.

**Transition:** Before we see code, a quick intuition check.

### S1-09 · Check your intuition: Who defends the paper?

**Proposed slide ID:** `day-4-s1-check-intuition` · **Time:** 22:30–24:00 (1:30)

**What is on slide:** Multiple-choice card: *"An agent runs a script that achieves 99% accuracy on promoter prediction, but accidentally trains on validation sequences. Who committed the scientific error?"*
Options: A) The LLM provider; B) The tool harness; C) The researcher who submitted the paper. (Option C highlighted in blue).

**What I want to say:** If you present a model whose validation leaked, the error is yours. The tool only executed what it sampled from its context. You are the scientist responsible for the claim.

**Point / reveal:** Ask for a quick show of hands before lighting up Option C.

**Transition:** Now let's see what happens when an agent receives an ordinary, casual request.

### S1-10 · Section 1 wrap-up: Setting the stage

**Proposed slide ID:** `day-4-s1-wrapup` · **Time:** 24:00–25:00 (1:00)

**What is on slide:** Summary card: The agent executes; the researcher defends. Day 3 test remains sealed. An exit code of 0 does not prove validity. Transition prompt: *"What happens when our instructions are vague?"*

**What I want to say:** With the roles clear, let us inspect what an agent does when given a prompt typical of everyday user interactions.

**Point / reveal:** Highlight the transition prompt.

**Transition:** Section 2 begins with the vague prompt.

---

<a id="section-2"></a>

## 2. When instructions are vague: silent decisions and flaws · 25–50

**Story question:** What happens when we leave scientific choices unsaid, and how do flawed analyses hide behind successful execution?

**Exit understanding:** Analyze the vague prompt; list the dozen critical scientific choices it leaves open; inspect an authored flawed analysis fixture (`fixture.md`); identify group leakage, preprocessing leakage, inverted predictions, and biological overclaims.

**Teaching thread:** Start with the actual vague prompt string from `agent_workshop/vague-prompt.md`. Unpack its missing assumptions. Introduce the authored flawed fixture as a teaching tool. Walk through its four fatal flaws one by one. Conclude with why plausible prose is dangerous.

**Scope and delivery:** Students inspect `agent_workshop/fixture.md` and `flawed_analysis.py`. **Crucial distinction:** This fixture is deliberately authored teaching material, *not a real agent transcript or recording*. The instructor runs or reads the tables aloud; no student coding is required.

### S2-01 · The vague request

**Proposed slide ID:** `day-4-s2-vague-prompt` · **Time:** 25:00–27:00 (2:00)

**What is on slide:** Speech bubble containing the exact prompt from `agent_workshop/vague-prompt.md`:
> *"Can you build the best model to predict promoters from these DNA sequences and explain the biology?"*
Large question marks surround the prompt.

**What I want to say:** Here is a prompt typical of how people interact with AI assistants: "Can you build the best model to predict promoters from these DNA sequences and explain the biology?" It sounds simple and polite. But scientifically, it is completely empty.

**Point / reveal:** Show the speech bubble. Ask students to call out one missing piece of information.

**Transition:** Let us catalogue everything that was left unsaid.

### S2-02 · Unpacking the unsaid: The dozen silent decisions

**Proposed slide ID:** `day-4-s2-silent-decisions` · **Time:** 27:00–30:30 (3:30)

**What is on slide:** A grid of twelve missing scientific decisions:
1. Real biology vs simulation? 2. Prediction target label? 3. Unit of independence (groups)? 4. Split policy? 5. Permitted input features? 6. Primary metric? 7. Decision threshold? 8. Baseline for comparison? 9. Compute budget? 10. Prediction schema? 11. Reproducibility seed? 12. Evaluation boundary?

**What I want to say:** Look at everything this prompt left unsaid. What does "best" mean? Best ROC-AUC? Best precision? Best training speed? Which features? What is the split? Can related sequences cross splits? The model cannot leave these questions blank. It must make silent assumptions about every single one.

**Point / reveal:** Reveal the twelve boxes in three columns: Task & Data, Model & Metric, Evaluation & Integrity.

**Transition:** How does an agent typically resolve this ambiguity?

### S2-03 · How agents resolve ambiguity: The path of least resistance

**Proposed slide ID:** `day-4-s2-path-least-resistance` · **Time:** 30:30–33:30 (3:00)

**What is on slide:** Flowchart: Vague prompt $\rightarrow$ LLM samples most frequent GitHub training patterns $\rightarrow$ Random shuffle split (ignoring biological families) $\rightarrow$ Accuracy metric (ignoring class balance) $\rightarrow$ Overfitted complex model $\rightarrow$ Plausible biological hallucination.

**What I want to say:** When choices are omitted, the agent defaults to generic web patterns: `train_test_split(shuffle=True)` that breaks biological grouping, reporting raw accuracy even on imbalanced data, and generating fluent paragraphs about "promoter binding" on completely synthetic sequences.

**Point / reveal:** Trace the path from vague prompt to fluent hallucination.

**Transition:** To see how subtle these bugs can be, let us inspect a concrete example.

### S2-04 · Introducing the Authored Teaching Fixture

**Proposed slide ID:** `day-4-s2-fixture-intro` · **Time:** 33:30–36:30 (3:00)

**What is on slide:** Warning banner: *"DELIBERATELY FLAWED TEACHING FIXTURE — NOT A REAL AGENT TRANSCRIPT."* Text: Authored to illustrate four classic bioinformatic pitfalls in four minimal rows. Links to `agent_workshop/fixture.md` and `flawed_analysis.py`.

**What I want to say:** To teach you how to audit analyses, we authored a deliberately flawed teaching fixture in `agent_workshop/fixture.md`. This is a human-crafted teaching exercise, not an actual agent log. It contains four rows and four fatal scientific flaws. Let us inspect each flaw in turn.

**Point / reveal:** Emphasize the warning banner: this is an educational fixture, not observed agent output.

**Transition:** Flaw number one: look at the group IDs.

### S2-05 · Flaw 1: Group leakage across splits

**Proposed slide ID:** `day-4-s2-flaw-group-leakage` · **Time:** 36:30–39:30 (3:30)

**What is on slide:** Table showing four sample rows:
- `train-01 | group-a | ACGTACGT | 0 | train`
- `train-02 | group-b | TATAAATG | 1 | train`
- `validation-01 | group-a | ACGTACGA | 0 | validation`
- `validation-02 | group-c | TATAAATA | 1 | validation`
Red highlighted box connects `group-a` in train to `group-a` in validation.

**What I want to say:** Flaw number one: Group leakage. The researcher checked that `sample_id` was unique: `train-01` and `validation-01` are different strings. But look at `group_id`: both belong to `group-a`, differing by only a single nucleotide! The model simply memorizes the family variant, creating the illusion of generalization.

**Point / reveal:** Highlight the unique sample IDs in green (deceptive pass), then highlight `group-a` in bright red (leakage).

**Transition:** Flaw number two: look at where feature extraction happened.

### S2-06 · Flaw 2: Preprocessing leakage

**Proposed slide ID:** `day-4-s2-flaw-preprocessing` · **Time:** 39:30–42:30 (3:00)

**What is on slide:** Code line from `flawed_analysis.py`:
```python
vectorizer.fit(samples["sequence"])
```
Red arrow pointing to `samples["sequence"]`, which includes both train and validation rows before any split occurs.

**What I want to say:** Flaw number two: Preprocessing leakage. Look at the vectorizer call. The vocabulary is fitted on the entire DataFrame, including validation sequences. Even without labels, the model's feature space is informed by validation sequence words before training begins. A pipeline must fit vocabulary on training rows only.

**Point / reveal:** Point to `samples["sequence"]` and show the split happening *afterwards*.

**Transition:** Flaw number three: look at how predictions were matched to labels.

### S2-07 · Flaw 3: Inverted sample array join

**Proposed slide ID:** `day-4-s2-flaw-inverted-join` · **Time:** 42:30–46:00 (3:30)

**What is on slide:** Contrast of two tables:
- True labels: `[validation-01: 0, validation-02: 1]`
- Predictions: `[validation-02: 0.1, validation-01: 0.9]`
Positional pairing: `0 == (0.1 < 0.5) [True]`, `1 == (0.9 >= 0.5) [True]` $\rightarrow$ **100% Accuracy!**
Aligned by ID: `validation-01: 0 vs 0.9 [False]`, `validation-02: 1 vs 0.1 [False]` $\rightarrow$ **0% Accuracy!**

**What I want to say:** Flaw number three: Inverted array alignment. The prediction table had its rows reversed. Because the script compared numpy arrays by raw position (`y_true == y_pred`), it matched validation-01's label (0) with validation-02's prediction (0.1), claiming 100% accuracy! When aligned by sample ID, the real accuracy is 0.0.

**Point / reveal:** Animate the crossed connection lines. Show 1.0 accuracy turn into 0.0 accuracy when aligned by ID.

**Transition:** Flaw number four: what did the report claim?

### S2-08 · Flaw 4: Biological overclaiming and test boundary breach

**Proposed slide ID:** `day-4-s2-flaw-overclaim` · **Time:** 46:00–48:30 (2:30)

**What is on slide:** Quote card from fixture report:
> *"Accuracy is 100%, so the best promoter model has learned promoter biology. We can use the Day 3 test score to decide whether to keep this approach."*
Two red stamp marks: "Overclaim: Synthetic $\neq$ Biology" and "Violation: Post-hoc Test Tuning".

**What I want to say:** Flaw number four: The report concludes that the model "learned promoter biology" from four synthetic sequences, and proposes using the Day 3 test set to decide whether to keep the model. That violates both biological reality and our evaluation boundary.

**Point / reveal:** Stamp the "Overclaim" and "Violation" badges over the quote.

**Transition:** What is the overarching lesson of this fixture?

### S2-09 · The danger of plausible nonsense

**Proposed slide ID:** `day-4-s2-discussion` · **Time:** 48:30–50:00 (1:30)

**What is on slide:** Callout card: *"The script exits with code 0. The reported accuracy is 1.0. The text sounds authoritative. How many published analyses contain these exact flaws?"*

**What I want to say:** Reflect on this before the break. `flawed_analysis.py` runs cleanly in 0.2 seconds. It prints 100% accuracy and produces professional text. If you don't inspect the data joins and split logic, you would believe it.

**Point / reveal:** Leave the question on screen for break reflection.

**Transition:** After the break, we replace the vague prompt with a precise specification.

### Break · 50–60

**Proposed slide ID:** `day-4-break-1` · **Time:** 50:00–60:00 (10:00)

**What is on slide:** Ten-minute break. *"Next: Turning scientific intent into an unambiguous contract."*

**What I want to say:** Return at minute 60. We will see how to write a formal specification that prevents an agent from making these assumptions.

---

<a id="section-3"></a>

## 3. Specifying the experiment: contracts and boundaries · 60–80

**Story question:** How do we turn scientific intent into an unambiguous contract that binds an agent's implementation?

**Exit understanding:** Deconstruct `agent_workshop/precise-spec.md`; understand the five essential pillars of a machine learning specification (Task, Data, Protocol, Deliverables, Constraints); define explicit prediction schemas; and prevent post-hoc evaluation drift.

**Teaching thread:** Move from the failure of conversational chatting to formal specification. Walk through the five pillars in `precise-spec.md`. Emphasize that fixing the scientific design precedes writing code.

**Scope and delivery:** Students read `agent_workshop/precise-spec.md`. No coding or agent account required. Pairs discuss which requirement they would audit first.

### S3-01 · The solution to ambiguity: Scientific specification

**Proposed slide ID:** `day-4-s3-spec-concept` · **Time:** 60:00–62:00 (2:00)

**What is on slide:** Schematic: Research Question $\rightarrow$ Formal Specification Document $\rightarrow$ Agent Context $\rightarrow$ Constrained Implementation. Text: *"Repair the scientific request before touching code."*

**What I want to say:** How do we stop an agent from making dangerous assumptions? We don't write longer conversational chat prompts. We write a formal scientific specification document. We fix the scientific design before the agent writes a single line of code.

**Point / reveal:** Show the specification document sitting between the question and the code.

**Transition:** Let us open `agent_workshop/precise-spec.md`.

### S3-02 · Deconstructing `precise-spec.md`: The five pillars

**Proposed slide ID:** `day-4-s3-precise-spec-overview` · **Time:** 62:00–64:30 (2:30)

**What is on slide:** Overview diagram of `precise-spec.md` showing five pillars:
1. Task & Question; 2. Data & Partitions; 3. Modeling & Baseline; 4. Evaluation & Metrics; 5. Required Deliverables & Provenance.

**What I want to say:** In `agent_workshop/precise-spec.md`, we provide an explicit analysis contract. Let us walk through the five pillars that constrain the agent.

**Point / reveal:** Reveal the five pillars in order.

**Transition:** Pillar one: what data is allowed?

### S3-03 · Pillar 1: Explicit task and data bounds

**Proposed slide ID:** `day-4-s3-pillar-data` · **Time:** 64:30–67:30 (3:00)

**What is on slide:** Excerpt from `precise-spec.md`:
- Input files: `train.csv` (720 rows), `validation.csv` (240 rows).
- Explicit ban: `protected_test.csv` must NEVER be read or referenced.
- Grouping: `group_id` partitions must be respected; no cross-split leakage.

**What I want to say:** Pillar one specifies the exact files and bounds. It explicitly names `train.csv` and `validation.csv`, and includes an absolute prohibition: `protected_test.csv` does not exist for this experiment. Any attempt to touch test data is a contract violation.

**Point / reveal:** Highlight the explicit ban on test data in red.

**Transition:** Pillar two: what model is permitted?

### S3-04 · Pillar 2: Feature pipeline and training scope

**Proposed slide ID:** `day-4-s3-pillar-features` · **Time:** 67:30–70:30 (3:00)

**What is on slide:** Excerpt:
- Baseline: 4-mer count vocabulary fitted strictly on training sequences.
- Model: `LogisticRegression(C=1.0, max_iter=1000)`.
- Preprocessing: `StandardScaler` fitted on training rows only.

**What I want to say:** Pillar two removes model search ambiguity. We specify the baseline: 4-mer counts, logistic regression, training-only vocabulary fitting, and training-only feature standardization. The agent is not authorized to try 50 random neural network architectures.

**Point / reveal:** Highlight "training sequences only" for both vocabulary and scaling.

**Transition:** Pillar three: how will we measure success?

### S3-05 · Pillar 3: Evaluation policy and threshold

**Proposed slide ID:** `day-4-s3-pillar-evaluation` · **Time:** 70:30–73:30 (3:00)

**What is on slide:** Excerpt:
- Primary metric: Validation ROC-AUC.
- Supporting metric: Average Precision (PR-AUC).
- Binary classification threshold: strictly 0.5 (no post-hoc threshold searching).
- Baseline target: must match manual baseline (~0.802 ROC-AUC).

**What I want to say:** Pillar three locks the evaluation rules. Primary metric is ROC-AUC; supporting metric is Average Precision; decision threshold is fixed at 0.5. The agent is barred from tuning thresholds to artificially inflate accuracy.

**Point / reveal:** Underline the fixed threshold 0.5 and primary ROC-AUC.

**Transition:** Pillar four: what output files must be delivered?

### S3-06 · Pillar 4: Exact prediction schema

**Proposed slide ID:** `day-4-s3-pillar-schema` · **Time:** 73:30–76:30 (3:00)

**What is on slide:** Required CSV schema:
`sample_id,probability`
Rules: Header must match exactly; sample IDs must match validation split exactly; probabilities must be finite float numbers between 0.0 and 1.0; no missing or duplicated rows.

**What I want to say:** Pillar four defines the deliverable schema. Predictions must be written to `validation_predictions.csv` with exactly two columns: `sample_id` and `probability`. Storing the sample ID alongside the prediction makes defensive joins possible.

**Point / reveal:** Show the two-column table and tick off the four rules.

**Transition:** Pillar five: how do we track what was executed?

### S3-07 · Pillar 5: Provenance and run reports

**Proposed slide ID:** `day-4-s3-pillar-provenance` · **Time:** 76:30–78:30 (2:00)

**What is on slide:** Checklist of required metadata in `run_report.md`: package versions (`scikit-learn`, `numpy`), random seed, execution timestamp, hardware/CPU threads, compute duration, input file hashes, and explicit limitations.

**What I want to say:** Pillar five requires a provenance ledger. The agent must document package versions, random seeds, wall-clock timing, input SHA-256 hashes, and any observed limitations. Without provenance, code cannot be audited.

**Point / reveal:** Tick each metadata requirement.

**Transition:** Section 3 summary before moving to project instructions.

### S3-08 · Section 3 check: What did the spec achieve?

**Proposed slide ID:** `day-4-s3-wrapup` · **Time:** 78:30–80:00 (1:30)

**What is on slide:** Contrast: Vague prompt (12 open decisions) vs Precise specification (0 open decisions). Text: *"A specification turns an open-ended guess into a verifiable contract."*

**What I want to say:** By writing this specification, we eliminated every one of the twelve silent decisions. But where do project-wide rules live? That brings us to Section 4.

**Point / reveal:** Show the 12 open decisions collapse to 0.

**Transition:** Section 4: Giving instructions a job.

---

<a id="section-4"></a>

## 4. Giving instructions a job: AGENTS.md, skills, and actual runs · 80–100

**Story question:** How do we separate task specs from project rules and skills, and what did real agents do when run on these requests?

**Exit understanding:** Distinguish the three tiers of agent guidance: task specification (`spec.md`), persistent project instructions (`AGENTS.md`), and reusable procedures (skills); inspect the actual October 26 clean agent runs; understand why the vague run scored 0.904 while the specified run scored 0.802.

**Teaching thread:** Introduce the three-tier instruction pyramid. Read `example-project/AGENTS.md`. Explain skills. Open the genuine October 26 agent runs (`actual_runs/2026-10-26/`). Show the provocative score gap (0.904 vs 0.802). Unpack the modeling choices to show that different experiments, not prompt quality, caused the difference.

**Scope and delivery:** Open text files in `agent_workshop/example-project/` and `agent_workshop/actual_runs/2026-10-26/`. These are genuine recorded runs (`codex` / `gpt-6.1-sol`), not authored fixtures.

### S4-01 · The three tiers of agent instructions

**Proposed slide ID:** `day-4-s4-three-tiers` · **Time:** 80:00–82:30 (2:30)

**What is on slide:** Three-tier pyramid diagram:
1. **Specification** (`precise-spec.md`): Defines *this specific experiment* (data, baseline, metrics, outputs).
2. **Project Instructions** (`AGENTS.md`): Defines *persistent rules across all tasks* (coding style, no git pushes, test boundary).
3. **Skill** (`SKILL.md`): Provides a *reusable procedural workflow* (e.g., scientific-audit checklist and verification code).

**What I want to say:** Don't cram everything into one giant prompt. Organize instructions hierarchically: the Specification defines the experiment; `AGENTS.md` sets permanent repository guardrails; and a Skill gives the agent a reusable procedural recipe.

**Point / reveal:** Build the pyramid from bottom (AGENTS) to middle (Skill) to top (Specification).

**Transition:** What belongs in `AGENTS.md`?

### S4-02 · Inspecting `example-project/AGENTS.md`

**Proposed slide ID:** `day-4-s4-agents-md` · **Time:** 82:30–85:00 (2:30)

**What is on slide:** Excerpts from `agent_workshop/example-project/AGENTS.md`:
- Rule 1: Never access `protected_test.csv` or test splits.
- Rule 2: Never modify files outside your assigned workspace directory.
- Rule 3: Always verify unique IDs and join tables by ID.
- Rule 4: Report simulation findings without overclaiming biological discovery.

**What I want to say:** Look at `example-project/AGENTS.md`. These rules are loaded by the agent on every interaction. They establish persistent guardrails: respect boundaries, stay in your directory, never invent biological claims, and never peek at test data.

**Point / reveal:** Highlight the four rules in sequence.

**Transition:** And what is a skill?

### S4-03 · What is a Skill? Procedural expertise on demand

**Proposed slide ID:** `day-4-s4-skills-concept` · **Time:** 85:00–87:30 (2:30)

**What is on slide:** Diagram of a skill directory: `skills/scientific-audit/SKILL.md` containing instructions + `audit_script.py`. The agent reads the skill when asked to perform a verification or audit task.

**What I want to say:** A skill is a package of procedural instructions and tools for a specific recurring task. Our `scientific-audit` skill gives the agent the exact code and checklist required to verify split manifests, check group overlap, and audit predictions.

**Point / reveal:** Show the skill folder opening to reveal instructions and code.

**Transition:** Now let's see how real agents behaved with these instructions.

### S4-04 · Real agents in the wild: The October 26 actual runs

**Proposed slide ID:** `day-4-s4-actual-runs-intro` · **Time:** 87:30–90:00 (2:30)

**What is on slide:** Overview card: October 26, 2026 genuine runs. Two fresh contexts using `gpt-6.1-sol` via Codex. Context A received only the vague prompt. Context B received `precise-spec.md`, `AGENTS.md`, and the audit skill. Open `agent_workshop/actual_runs/2026-10-26/README.md`.

**What I want to say:** Now let's look at real agent behavior. On October 26, 2026, we ran two genuine delegated agent sessions with identical development inputs. Context A received only the vague prompt. Context B received the precise specification, `AGENTS.md`, and the audit skill.

**Point / reveal:** Highlight that both contexts started with byte-identical development datasets.

**Transition:** What scores did they achieve?

### S4-05 · The Scoreboard: Vague run (0.904) vs Specified run (0.802)

**Proposed slide ID:** `day-4-s4-score-comparison` · **Time:** 90:00–93:00 (3:00)

**What is on slide:** Bar chart showing Validation ROC-AUC:
- Vague Run: **0.904** (Average Precision 0.859)
- Specified Run: **0.802** (Average Precision 0.802)
Large question banner: *"Did the vague prompt produce a better model?!"*

**What I want to say:** Look at the scores! The vague run achieved a validation ROC-AUC of 0.904, while the specified run achieved 0.802. A superficial observer would say, "Look! Vague prompting is superior! Writing detailed specifications made the model worse!" Is that true?

**Point / reveal:** Show the bars, then display the provocative question banner. Ask the room for hypotheses.

**Transition:** Let us look inside the code of both runs.

### S4-06 · Looking under the hood: Why did the vague run score higher?

**Proposed slide ID:** `day-4-s4-under-the-hood` · **Time:** 93:00–96:30 (3:30)

**What is on slide:** Side-by-side autopsy:
- **Specified Run**: Followed the contract strictly. Fitted fixed 4-mer bag-of-words logistic regression baseline. Replicated manual baseline (0.802) within $10^{-12}$.
- **Vague Run**: Explored six model candidates! Ran 5-fold group CV. Found that counting the specific motif `TATAAATG` directly in the training set yielded a massive feature, and trained a custom model on that motif prior!

**What I want to say:** When we inspect the code, the mystery vanishes. The specified run did exactly what we asked: it implemented the fixed 4-mer baseline to establish a benchmark. The vague run, unconstrained by any baseline requirement, searched six different algorithms and discovered the planted `TATAAATG` motif!

**Point / reveal:** Contrast the two modeling decisions side by side.

**Transition:** What is the scientific takeaway from this comparison?

### S4-07 · A difference in experiments, not prompt quality

**Proposed slide ID:** `day-4-s4-diff-experiments` · **Time:** 96:30–99:00 (2:30)

**What is on slide:** Warning banner: *"Never infer prompt causality from confounded experiments."* Explanation: Different search spaces, different objectives, and different feature representations mean these runs conducted two entirely different scientific experiments.

**What I want to say:** This is a crucial lesson in AI evaluation: You cannot compare prompt effectiveness when the models are solving different optimization problems. The vague run was scientifically cautious—it used group CV and did not leak—but it answered a different question than the specified baseline.

**Point / reveal:** Underline that prompt quality was not isolated.

**Transition:** Section 4 wrap-up before the break.

### S4-08 · Section 4 check: Instructions guide, but human audits decide

**Proposed slide ID:** `day-4-s4-wrapup` · **Time:** 99:00–100:00 (1:00)

**What is on slide:** Summary card: Specifications define experiments; `AGENTS.md` defines rules; skills provide workflows. Real agents can produce valid code under both, but only an audit reveals what actually happened.

**What I want to say:** Instructions clarify expectations, but they do not prove scientific correctness. That requires an independent audit, which we will conduct after the break.

**Point / reveal:** Highlight the upcoming audit practical.

**Transition:** Break 2.

### Break · 100–110

**Proposed slide ID:** `day-4-break-2` · **Time:** 100:00–110:00 (10:00)

**What is on slide:** Ten-minute break. *"Next: Hands-on scientific audit with `06_scientific_audit.py` and the one-page checklist."*

**What I want to say:** Return at minute 110. We will run our automated audit tool and practice auditing claims independently of execution.

---

<a id="section-5"></a>

## 5. The scientific audit: evidence, consequence, and repair · 110–150

**Story question:** How do we systematically audit an ML analysis for data leakage, alignment errors, and unsupported claims?

**Exit understanding:** Execute the scientific audit code (`course_code/06_scientific_audit.py`); complete the one-page audit checklist (`instructor/audit-checklist.html`); trace evidence $\rightarrow$ consequence $\rightarrow$ repair; and formulate defensible scientific corrections without touching test data.

**Teaching thread:** Define scientific audit vs code check. Inspect `06_scientific_audit.py`. Run the audit on the authored fixture. Work through the printable checklist in pairs. Apply the Evidence $\rightarrow$ Consequence $\rightarrow$ Repair framework. Audit the clean October 26 runs. Discuss what code cannot audit.

**Scope and delivery:** Students run `course_code/06_scientific_audit.py` or inspect its output in `agent_workshop/worked-audit.md`. The checklist is in `instructor/audit-checklist.html`. No test data is touched.

### S5-01 · What is a scientific audit?

**Proposed slide ID:** `day-4-s5-audit-definition` · **Time:** 110:00–113:00 (3:00)

**What is on slide:** Magnifying glass over a codebase. Definition card from `GLOSSARY.md`:
> **Scientific audit**: An examination of whether an analysis answers the intended question with valid evaluation and supported conclusions, rather than merely producing working code.
*Avoid*: Code execution check when referring to scientific validity.

**What I want to say:** In `GLOSSARY.md`, we define a scientific audit not as checking if code compiles or runs without error. An audit asks: Did the evaluation isolate the intended question? Did groups leak? Were samples joined correctly? Are the claims supported by evidence?

**Point / reveal:** Highlight the contrast between "code works" and "claims are supported".

**Transition:** How do we automate these checks?

### S5-02 · Introducing `course_code/06_scientific_audit.py`

**Proposed slide ID:** `day-4-s5-audit-code-overview` · **Time:** 113:00–116:00 (3:00)

**What is on slide:** Code screenshot of `audit_predictions`: checking required columns (`sample_id`, `group_id`, `sequence`, `label`, `split`), validating uniqueness, detecting cross-split groups (`groupby("group_id")["split"].nunique()`), checking duplicate sequences, and validating one-to-one ID join.

**What I want to say:** Look at `course_code/06_scientific_audit.py`. It is a defensive audit engine. It checks whether any `group_id` appears in more than one split, whether identical sequences cross splits, and verifies that prediction IDs match evaluation split IDs one-to-one before recalculating ROC-AUC and AP.

**Point / reveal:** Point to the group overlap check, then the one-to-one ID join assertion.

**Transition:** Let us run it on the authored fixture from Section 2.

### S5-03 · Running the audit on the authored fixture

**Proposed slide ID:** `day-4-s5-audit-fixture-run` · **Time:** 116:00–119:30 (3:30)

**What is on slide:** Terminal output running the audit on `agent_workshop/fixture.md`:
`[FAIL] Overlapping groups detected across splits: {'group-a'}`
`[FAIL] Prediction alignment error: Positional accuracy = 1.0, Aligned accuracy = 0.0`
`[FAIL] Preprocessing leak: vocabulary fitted on 4 rows including validation`

**What I want to say:** Let us run the audit tool on the authored fixture. Immediately, the automated assertions fire: `group-a` is caught crossing between train and validation. The array alignment check reveals that positional accuracy is 1.0, but true ID-aligned accuracy is 0.0!

**Point / reveal:** Highlight each failure message in red.

**Transition:** Now you will perform the audit using our one-page checklist.

### S5-04 · Hands-on activity: The one-page audit checklist (119–125)

**Proposed slide ID:** `day-4-s5-checklist-activity` · **Time:** 119:30–125:00 (5:30)

**What is on slide:** Display of the printable audit checklist from `instructor/audit-checklist.html`. Five major auditing sections:
1. Split integrity; 2. Preprocessing scope; 3. Prediction alignment; 4. Metric & threshold policy; 5. Biological claim scope.
Timer: 5 minutes.

**What I want to say:** Open `instructor/audit-checklist.html` or look at your handout. In pairs, take five minutes to audit the claims in the fixture report against the checklist items. Mark each item as PASS, FAIL, or UNVERIFIED.

**Point / reveal:** Keep the five section headings visible and run the 5-minute timer.

**Transition:** Let us review the findings together.

### S5-05 · Reviewing the checklist findings

**Proposed slide ID:** `day-4-s5-checklist-review` · **Time:** 125:00–128:00 (3:00)

**What is on slide:** Completed checklist from `agent_workshop/worked-audit.md`:
- Split integrity: FAIL (cross-split group).
- Preprocessing: FAIL (vocabulary on all rows).
- Alignment: FAIL (reversed rows).
- Metrics: FAIL (unspecified accuracy).
- Biology: FAIL (unsupported promoter claim).

**What I want to say:** Every single section of the checklist failed. Notice that passing the syntax check told us nothing about these failures. Once you find failures, how do you report and repair them?

**Point / reveal:** Reveal the FAIL badges across the five sections.

**Transition:** We use the Evidence $\rightarrow$ Consequence $\rightarrow$ Repair framework.

### S5-06 · The Repair Framework: Evidence $\rightarrow$ Consequence $\rightarrow$ Repair

**Proposed slide ID:** `day-4-s5-repair-framework` · **Time:** 128:00–131:30 (3:30)

**What is on slide:** Three-column table:
1. **Observed Evidence** (e.g., `group-a` present in both train and validation splits).
2. **Scientific Consequence** (Evaluation measures family memorization, not sequence generalization).
3. **Specific Repair** (Re-split dataset by `group_id`, check overlap == 0, and refit model).

**What I want to say:** When an audit finds a defect, you must structure your response scientifically: Evidence $\rightarrow$ Consequence $\rightarrow$ Repair. What did you observe? What scientific claim is invalidated by that observation? And what concrete repair must be executed?

**Point / reveal:** Trace row 1 from observed evidence to consequence to repair.

**Transition:** How does this apply to real agent runs?

### S5-07 · Auditing the actual clean runs (131–136)

**Proposed slide ID:** `day-4-s5-audit-actual-runs` · **Time:** 131:30–136:00 (4:30)

**What is on slide:** Terminal output from `parent_audit.json` on the October 26 runs:
- `vague/`: 0 cross-split groups; 0 duplicate sequences; exact 240 validation IDs matched; validation ROC-AUC = 0.9041667 confirmed.
- `specified/`: 0 cross-split groups; 0 duplicate sequences; exact 240 validation IDs matched; validation ROC-AUC = 0.8019444 confirmed.

**What I want to say:** Now look at the audit of our actual October 26 agent runs. Both runs passed every single automated audit check! Neither agent fell into the trap of group leakage or array misalignment. The parent audit recomputed their predictions and confirmed their reported metrics to seven decimal places.

**Point / reveal:** Show the green PASS marks across all automated checks for both runs.

**Transition:** But can automated code check everything?

### S5-08 · What code cannot audit

**Proposed slide ID:** `day-4-s5-subtle-limitations` · **Time:** 136:00–139:30 (3:30)

**What is on slide:** Warning card: *"What code cannot audit."*
List of human-judgment requirements:
- Is the biological question sound?
- Does the simulated task reflect real genomic mechanisms?
- Was the baseline appropriate?
- Did prompt phrasing introduce subtle researcher bias?

**What I want to say:** Notice what the automated audit cannot do. It cannot tell you whether a 4-mer baseline is scientifically meaningful for your research question. It cannot tell you whether your simulated sequences mimic real mammalian promoters. Automated tools check consistency; human scientists judge validity.

**Point / reveal:** Highlight the four human-judgment items.

**Transition:** And how do we repair models without cheating?

### S5-09 · Repairing without cheating: The test boundary holds

**Proposed slide ID:** `day-4-s5-repair-without-cheating` · **Time:** 139:30–143:00 (3:30)

**What is on slide:** Flowchart: Defect found in development $\rightarrow$ Fix split or code $\rightarrow$ Refit on training $\rightarrow$ Re-evaluate on validation. Barrier block: *"Do NOT repair models by testing them against the Day 3 test set!"*

**What I want to say:** If your audit reveals an error, how do you repair it? You fix the code and re-evaluate on validation data. You never use the Day 3 test set to check if your repair worked. The test set remains historical evidence.

**Point / reveal:** Draw the repair cycle staying entirely inside the development split.

**Transition:** Section 5 summary before we look at automated platforms.

### S5-10 · Checkpoint: Audit mastered

**Proposed slide ID:** `day-4-s5-checkpoint` · **Time:** 143:00–146:00 (3:00)

**What is on slide:** Summary card: Automated checks verify data integrity; the checklist structures findings; human judgment evaluates claims. Up next: reserved 20-minute demonstration of automated bioinformatic workflows in Agentomics.

**What I want to say:** We have audited manual scripts, authored fixtures, and clean agent runs. Now, how do these lessons translate when automation scales up to complex, multi-step platforms?

**Point / reveal:** Highlight the upcoming demonstration.

**Transition:** Section 6 begins at minute 150.

### S5-11 · Transition buffer

**Proposed slide ID:** `day-4-s5-buffer` · **Time:** 146:00–150:00 (4:00)

**What is on slide:** Open discussion on audit experiences. Questions from students about checklist criteria or code checks.

**What I want to say:** Take four minutes for any questions about split leakage or alignment audits before we begin the platform demonstration.

**Point / reveal:** Open floor for questions.

**Transition:** Section 6: Automated platforms and responsibility.

---

<a id="section-6"></a>

## 6. Automated workflows and scientific responsibility · 150–180

**Story question:** How do we evaluate end-to-end automated platforms like Agentomics, and what must remain permanent human scientific responsibility?

**Exit understanding:** Observe and critique an automated bioinformatic workflow in Agentomics (minutes 150–170); identify input/split visibility and artifact tracking; articulate the contingency if live access is pending; and participate in the final 10-minute whole-course synthesis (minutes 170–180) across count, learn, reuse, and delegate.

**Teaching thread:** Introduce multi-step workflow platforms. Pose the three platform audit questions. Execute the 20-minute Agentomics demonstration (or contingency walkthrough). Transition at minute 170 to the protected 10-minute whole-course synthesis. End on the four-day progression and permanent human responsibility.

**Scope and delivery:** Minutes 150–170 are the instructor-led Agentomics demonstration. If actual platform access is unavailable, use the documented discussion contingency and mark the demonstration pending; never fabricate product behavior. Minutes 170–180 are strictly protected for whole-course synthesis.

### S6-01 · Automated platforms: Scaling up agent loops

**Proposed slide ID:** `day-4-s6-agentomics-intro` · **Time:** 150:00–153:00 (3:00)

**What is on slide:** Schematic of an automated workflow engine (Agentomics): Hypothesis input $\rightarrow$ Automated literature retrieval $\rightarrow$ Automated pipeline generation $\rightarrow$ Distributed execution $\rightarrow$ Report generation.

**What I want to say:** In our exercises, we ran isolated single-agent scripts. But the field is moving toward integrated platforms like Agentomics, which automate entire end-to-end research pipelines from literature retrieval to code execution and figure generation.

**Point / reveal:** Animate the multi-step pipeline from hypothesis to report.

**Transition:** What questions must we ask when inspecting such a platform?

### S6-02 · The three audit questions for automated platforms

**Proposed slide ID:** `day-4-s6-three-platform-questions` · **Time:** 153:00–156:00 (3:00)

**What is on slide:** Three inspection pillars:
1. **Where are the splits?** Can you see the exact sample IDs assigned to train, validation, and test?
2. **Where is the execution ledger?** Can you inspect the exact commands, random seeds, and package versions?
3. **Where are the predictions?** Can you download raw probability tables and recompute metrics independently?

**What I want to say:** When an automated system presents you with a finished paper or report, you must ask the same three questions we practiced today: Can I see the splits? Can I inspect the execution ledger? Can I download the raw prediction CSV and verify the join?

**Point / reveal:** Reveal the three inspection questions with magnifying glass icons.

**Transition:** Let us look inside the platform.

### S6-03 · Instructor Demonstration: Inside Agentomics (150–170)

**Proposed slide ID:** `day-4-s6-agentomics-demo` · **Time:** 156:00–166:00 (10:00)

**What is on slide:** Live demonstration screen / recorded interface walkthrough showing a real bioinformatic analysis in Agentomics. Callouts highlight experiment tracking, dataset upload, pipeline execution logs, and output artifacts.
*(Contingency note: If live platform access is pending, displays pre-recorded walkthrough or structured discussion of platform auditability with explicit pending label).*

**What I want to say:** Let us look at an actual workflow inside Agentomics. Notice where the platform exposes its intermediate artifacts. When the system fits a classifier, where does it record the split manifest? Can we verify that related gene families were partitioned into distinct folds?

**Point / reveal:** Walk through the interface live, pointing out the execution log and artifact download buttons.

**Transition:** How do our checklist criteria apply here?

### S6-04 · Auditing the Agentomics result (166–170)

**Proposed slide ID:** `day-4-s6-agentomics-audit` · **Time:** 166:00–170:00 (4:00)

**What is on slide:** Discussion grid applied to the demonstration: What evidence was visible? What was hidden inside the platform? Did the system provide cryptographic artifact hashes?

**What I want to say:** Let us apply our checklist to what we just saw. Which claims are directly supported by visible artifacts, and which require trusting the platform's internal logic? As scientists, we only trust what we can independently audit.

**Point / reveal:** Fill the grid based on student observations during the demo.

**Transition:** At minute 170, we enter the final ten minutes: whole-course synthesis.

---

### S6-05 · Final synthesis: The four-day journey (170–174)

**Proposed slide ID:** `day-4-s6-four-day-journey` · **Time:** 170:00–174:00 (4:00)

**What is on slide:** The complete four-day progression displayed across four panels:
1. **Day 1 · Count**: Handcrafted k-mers, linear models, decision thresholds, and leakage traps.
2. **Day 2 · Learn**: Neural networks, loss functions, convolutions, and positional pattern learning.
3. **Day 3 · Reuse**: Foundation embeddings, attention, cache integrity, and the sacred freeze gate.
4. **Day 4 · Delegate**: Coding agents, specifications, scientific audits, and human accountability.

**What I want to say:** We have reached the final ten minutes of our course. Look at the path we have traveled. On Day 1, we hand-counted k-mers. On Day 2, we taught convolutions to learn local patterns. On Day 3, we borrowed representations from foundation models and enforced a strict evaluation freeze. Today, on Day 4, we learned how to delegate coding to AI agents without surrendering scientific rigor.

**Point / reveal:** Light up the four day panels in sequence: Count $\rightarrow$ Learn $\rightarrow$ Reuse $\rightarrow$ Delegate.

**Transition:** What must always remain with the human researcher?

### S6-06 · What must remain human scientific responsibility?

**Proposed slide ID:** `day-4-s6-human-responsibility` · **Time:** 174:00–177:00 (3:00)

**What is on slide:** Center banner: *"The AI agent is an instrument, not an author."*
Four bullet points:
- The question is yours.
- The evaluation design is yours.
- The verification of split integrity is yours.
- The defense of the discovery is yours.

**What I want to say:** As you go forward into your master's research and careers, you will use AI coding assistants every day. Treat them as powerful instruments—like a high-throughput sequencer or a centrifuge. But never let the instrument formulate your evaluation, verify its own work, or take responsibility for the truth.

**Point / reveal:** Reveal each responsibility bullet with emphasis.

**Transition:** One closing question for everyone.

### S6-07 · What would you trust now? Final discussion & closing

**Proposed slide ID:** `day-4-s6-final-discussion` · **Time:** 177:00–180:00 (3:00)

**What is on slide:** Closing slide with links to all course repositories, slide decks, instructor guides, completed notebooks, and audit checklists.
Prompt: *"Name one claim you can now defend, and one check you will always perform before trusting an ML analysis."*

**What I want to say:** Thank you for your hard work over these four intensive days. To close: what is one check you will always perform before trusting a machine learning result in bioinformatics? Thank you all, and good luck with your research.

**Point / reveal:** Invite two or three parting responses from students before closing.

**Transition:** End of Day 4 and conclusion of the course.

---

<a id="workshop-plan"></a>

## Workshop plan

Day 4 practical work uses local text files under `agent_workshop/` and `course_code/06_scientific_audit.py`.

| Checkpoint | Student / Instructor Action | Classroom Delivery State |
| --- | --- | --- |
| 25–50: Vague prompt & fixture | Read `vague-prompt.md`; inspect `fixture.md`; predict failure modes. | Local text files; runs cleanly on any viewer. |
| 60–80: Precise specification | Read `precise-spec.md`; identify five pillars and required schema. | Text files; no execution required. |
| 80–100: Clean run inspection | Open `actual_runs/2026-10-26/README.md`; contrast vague (0.904) vs specified (0.802). | Fully audited local records available. |
| 110–135: Hands-on audit | Run `course_code/06_scientific_audit.py` on fixture and actual runs; fill out checklist. | Python code verified locally; instant execution. |
| 135–150: Repair discussion | Discuss Evidence $\rightarrow$ Consequence $\rightarrow$ Repair table. | Ungraded paired discussion. |
| 150–170: Agentomics demo | Instructor demonstration of Agentomics workflow and artifact tracking. | Instructor-led demonstration / contingency walkthrough. |
| 170–180: Course synthesis | Whole-class discussion: human scientific responsibility. | Protected 10-minute closing discussion. |

---

<a id="evidence-and-scope"></a>

## Evidence and scope

### Dataset and evaluation continuity

- **Development inputs only:** Day 4 operates strictly on development data (720 training, 240 validation sequences). Protected test files (`protected_test.csv`) are never supplied to agents or loaded during Day 4.
- **Authored fixture vs actual runs:** `agent_workshop/fixture.md` is an authored teaching fixture, not a recorded agent transcript. The October 26 runs (`agent_workshop/actual_runs/2026-10-26/`) are genuine recorded executions using `gpt-6.1-sol` via Codex.
- **Evaluation policy:** ADR 0002 is maintained. Revealed Day 3 test results are historical evidence and cannot be used for Day 4 agent model selection.
- **Scientific scope:** ADR 0001 is maintained. All sequence data is simulated; claims of real promoter prediction or biological discovery are explicitly prohibited.
