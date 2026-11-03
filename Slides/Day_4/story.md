# Day 4 story

**Implemented for instructor review — 2026-11-03.** All six sections are specified slide by slide. Each slide has an ID, a timing, the slide content, speaking notes, pointing/reveal guidance and a transition, following the format established in Day 2 and Day 3. The [Day 4 deck](presentation.html) implements these 53 content beats and two breaks. [QA](../qa.md#day-4-implementation--2026-11-03) records local checks and remaining limits. Titles, emphasis and pacing remain editable.

**Working title:** Specifying, delegating, and scientifically auditing machine learning workflows.

**The story:** Over the first three days, we hand-built models, explored deep architectures, evaluated pretrained embeddings, and protected our evaluation boundary. Today we confront a new collaborator: AI coding agents. Who owns the scientific claim when an agent writes the code? The agent executes; the researcher defends. We inspect what happens when an agent receives a vague request ("Build the best promoter model"), contrast an authored flawed teaching fixture with genuine recorded agent runs, and learn how to constrain agents using precise specifications, persistent project instructions (`AGENTS.md`), and reusable audit skills. Students perform a hands-on scientific audit using our audit checklist and code, discuss the evidence needed to audit an automated workflow during the reserved Agentomics fallback, and synthesize the four-day journey across count, learn, reuse, and delegate.

**End-of-day understanding:** Large language models predict tokens from context; agents use tool loops to read, edit, and execute code; vague requests leave choices about targets, splits and metrics unresolved; agents may ask for clarification or make assumptions; fluent code and 100% accuracy claims do not imply scientific validity; sample ID alignment and group split integrity must be verified independently; instructions and skills clarify expectations but do not guarantee truth; and all scientific claims remain the sole responsibility of the human scientist.

**Delivery and style:** Use the approved speaker-led style: one short title, one main visual, generous whitespace, blue `#0072B2` / orange `#D55E00` contrast, letters and shapes as well as colour, and detailed notes. Prefer explanatory illustrations (split diagrams, tool loops, document roles and audit evidence) to plain boxes. The required observation route works completely from local text files under `agent_workshop/` and Python scripts under `course_code/`, requiring no agent account, internet service, or payment. All discussion is ungraded. Practicals fit strictly within contact hours.

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

**160 teaching minutes + 20 break minutes = 180 minutes.** There are 53 content beats (10/9/8/8/11/7) and two break slides. All timings are suggested allocations, not measured pacing. The breaks stay at minutes 50–60 and 100–110. Section 6 explicitly protects the reserved 20-minute Agentomics slot using the selected audit-discussion fallback (150–170) and the final 10-minute whole-course synthesis (170–180), as recorded in [instructor/guide.md](../../instructor/guide.md#day-4--specify-delegate-and-audit).

**Sections:** [1 · Who owns the claim?](#section-1) · [2 · Vague prompts and fixtures](#section-2) · [3 · Precise specification](#section-3) · [4 · Instructions and actual runs](#section-4) · [5 · Scientific audit](#section-5) · [6 · Agentomics and responsibility](#section-6) · [Workshop plan](#workshop-plan) · [Evidence and scope](#evidence-and-scope)

---

<a id="section-1"></a>

## 1. Who owns the claim when an agent writes the code? · 0–25

**Story question:** When an AI coding agent generates and executes your analysis, who is responsible for the scientific claim?

**Exit understanding:** Define the division of responsibility between agent execution and human defense; recall the Day 3 evaluation boundary (any revealed Day 3 test result is historical evidence, never feedback for Day 4 agent development); distinguish an LLM from an agent; explain context windows, tools, and the agent loop; and understand why exit code 0 is an engineering observation, not scientific evidence.

**Teaching thread:** Start by asking who defends a scientific claim when software writes the code. Move through: the division of responsibility → the Day 3 test boundary → what an LLM does (predicting tokens in context) → what tools add → the agent loop → the danger of trusting a clean exit code → observation route access.

**Scope and delivery:** This section is conceptual and conversational: no code execution or accounts needed. Connect directly to the evaluation lessons of Days 1–3.

### S1-01 · The new collaborator

**Proposed slide ID:** `day-4-s1-welcome` · **Time:** 0:00–1:30 (1:30)

**What is on slide:** A researcher, a question document and a terminal are connected by a delegation arrow. The four-day progression is Count → Learn → Reuse → Delegate.

**What I want to say:** Welcome to Day 4. Over the past three days, you have manually engineered features, trained neural networks, extracted transformer embeddings, and sealed an evaluation test set. Today we step into the modern reality of computational biology: delegating implementation to AI coding agents.

**Point / reveal:** Point from question to researcher to delegated implementation; then follow the four-day progression.

**Transition:** But before we look at code, who stands behind the results?

### S1-02 · The agent executes. You defend.

**Proposed slide ID:** `day-4-s1-core-principle` · **Time:** 1:30–4:00 (2:30)

**What is on slide:** A terminal lists read/edit/execute and inspect/report. A researcher faces it. The two labels are “Implementation” and “Scientific responsibility”.

**What I want to say:** Here is the foundational rule of Day 4: The agent executes; the researcher defends. If an agent writes code that leaks validation data, misaligns sample IDs, or invents biological claims, you cannot tell a peer reviewer or an examination committee, "The AI wrote it." You own the claim.

**Point / reveal:** Point to implementation, then the researcher who remains responsible for the claim.

**Transition:** That responsibility begins with enforcing our evaluation boundary.

### S1-03 · The evaluation boundary still holds

**Proposed slide ID:** `day-4-s1-boundary-reminder` · **Time:** 4:00–7:00 (3:00)

**What is on slide:** Training + validation sit on one side of a barrier; protected evidence sits behind a lock. Caption: “No Day 4 selection against the Day 3 test”.

**What I want to say:** Whether the Day 3 reveal has happened or remains pending, its protected files and scores cannot guide new Day 4 agent development. If revealed, the result is historical evidence about frozen workflows. Today agents receive development inputs only. Do not open protected sequences, labels, caches, predictions or results to choose a new model.

**Point / reveal:** Trace development inputs to the barrier. Point to the locked evidence; do not load it.

**Transition:** To understand what an agent can do, we must understand how it works.

### S1-04 · Predict the next token

**Proposed slide ID:** `day-4-s1-llm-basics` · **Time:** 7:00–10:00 (3:00)

**What is on slide:** A constructed next-token distribution follows “Read this sequence …”. Below it, files/history feed application-supplied context. It is a teaching construction, not measured model probabilities.

**What I want to say:** A language model generates tokens conditioned on its context. Training can give it useful reasoning and coding capabilities, but plausible output is not evidence that a scientific claim is correct. The surrounding application can retain files, history or memory and retrieve them into context; a context window is not a claim that the application has no memory.

**Point / reveal:** Point to the constructed token alternatives, then the separate application-context arrow.

**Transition:** What transforms a text predictor into an active agent?

### S1-05 · Give the model tools

**Proposed slide ID:** `day-4-s1-what-is-agent` · **Time:** 10:00–13:00 (3:00)

**What is on slide:** An LLM connects to three tools: Read, Edit and Run. Caption: “A model uses tools and observes their results”.

**What I want to say:** What turns a language model into an agent? Tools. When we equip an LLM with structured function calls—reading local files, writing code to disk, running shell commands, and inspecting errors—it ceases to be a passive chatbot and becomes an autonomous software agent.

**Point / reveal:** Trace the LLM connections to Read, Edit and Run.

**Transition:** How does the agent decide what to do next?

### S1-06 · Inspect → act → observe → revise

**Proposed slide ID:** `day-4-s1-agent-loop` · **Time:** 13:00–16:30 (3:30)

**What is on slide:** An interactive circular diagram: Inspect → Act → Observe → Revise. The button highlights the next step and changes the descriptive readout; it does not replay a real agent.

**What I want to say:** An agent operates in a continuous loop: Inspect, Act, Observe, Revise. It reads the current context, chooses a tool action, observes the result from the operating system, and decides what to do next. If a script crashes, it reads the traceback and modifies the code until the command exits successfully.

**Point / reveal:** Click through the four loop steps. Explain that this is a constructed walkthrough.

**Transition:** But there is a silent trap in this loop.

### S1-07 · A clean run can still be wrong

**Proposed slide ID:** `day-4-s1-exit-code-zero` · **Time:** 16:30–20:00 (3:30)

**What is on slide:** A terminal reports exit code 0 and accuracy 100%. “Inspect what ran” reveals an authored example of group overlap and wrong row pairing. The display is not a real agent result.

**What I want to say:** An agent can stop after a command succeeds unless its task also requires scientific checks. Exit code zero only means that the program did not signal an execution error; it says nothing about split independence, ID joins or biological validity. Agents can run these checks when instructed, as the real runs later demonstrate. This failure mode is not an inevitable property of every agent.

**Point / reveal:** Pause at the successful terminal output; click “Inspect what ran” to reveal the authored defects.

**Transition:** How will we explore this today?

### S1-08 · Two ways to participate

**Proposed slide ID:** `day-4-s1-participation-routes` · **Time:** 20:00–22:30 (2:30)

**What is on slide:** Saved-evidence observation and optional operation with existing access appear side by side. Both use the same evidence questions; no agent account is required for the core lesson.

**What I want to say:** For today's activities, no one needs to sign up for a service, enter a credit card, or configure an API key. We provide a full Observation Route with genuine pre-recorded runs, authored fixtures, and completed audit scripts. Observers and operators answer the exact same scientific questions.

**Point / reveal:** Show both paths side by side, emphasizing that all core discussion questions are identical.

**Transition:** Before we see code, a quick intuition check.

### S1-09 · What would you defend?

**Proposed slide ID:** `day-4-s1-check-intuition` · **Time:** 22:30–24:00 (1:30)

**What is on slide:** Open discussion: “The code runs and the score looks excellent. What evidence would you need before putting your name on the result?”

**What I want to say:** Invite two or three contributions about splits, fitted preprocessing, identity and provenance. Connect each to a claim the researcher would have to defend. This is an audience conversation, not a scored question.

**Point / reveal:** Invite contributions; leave the discussion open. No multiple-choice answer.

**Transition:** Now let's see what happens when an agent receives an ordinary, casual request.

### S1-10 · What did we leave unsaid?

**Proposed slide ID:** `day-4-s1-wrapup` · **Time:** 24:00–25:00 (1:00)

**What is on slide:** “The agent executes. You defend.” followed by “What did the request leave unsaid?”

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

### S2-01 · “Build the best model”

**Proposed slide ID:** `day-4-s2-vague-prompt` · **Time:** 25:00–27:00 (2:00)

**What is on slide:** The exact vague request: “Can you build the best model to predict promoters from these DNA sequences and explain the biology?”

**What I want to say:** Read the exact prompt. It gives a broad ambition, but leaves the task, data independence, success criterion and evidence requirements unresolved. Invite one example of a decision the implementation would need to make.

**Point / reveal:** Read the request and invite one missing scientific decision.

**Transition:** Let us catalogue everything that was left unsaid.

### S2-02 · Twelve decisions still open

**Proposed slide ID:** `day-4-s2-silent-decisions` · **Time:** 27:00–30:30 (3:30)

**What is on slide:** Four decisions at a time, in three button-controlled sets. Task/data: label meaning, allowed files, related samples, split assignment. Model/success: representation, model/search, primary metric, threshold. Evaluation/provenance: selection boundary, protected evidence, outputs, defensible claims.

**What I want to say:** Look at everything this prompt left unsaid. What does "best" mean? Best ROC-AUC? Best precision? Best training speed? Which features? What is the split? Can related sequences cross splits? An agent can ask for clarification or state cautious assumptions. The scientific choices still need an explicit answer before a defensible experiment.

**Point / reveal:** Use “Next set of decisions” twice; discuss four decisions at a time.

**Transition:** How does an agent typically resolve this ambiguity?

### S2-03 · Assumptions become code

**Proposed slide ID:** `day-4-s2-path-least-resistance` · **Time:** 30:30–33:30 (3:00)

**What is on slide:** A fork from one vague request to several possible choices: split by row or group; accuracy or ROC-AUC; fixed baseline or model search. The branches end at different experiments, not a predetermined failure.

**What I want to say:** An underspecified request leaves room for assumptions, clarification or cautious defaults. Leakage and overclaiming are possible failures, not inevitable agent behavior. Our actual vague run later used training-only group CV and explicitly limited its biological claims. Inspect what happened rather than predicting failure from prompt length.

**Point / reveal:** Trace the branches to different possible experiments; failure is not predetermined.

**Transition:** To see how subtle these bugs can be, let us inspect a concrete example.

### S2-04 · An authored teaching fixture

**Proposed slide ID:** `day-4-s2-fixture-intro` · **Time:** 33:30–36:30 (3:00)

**What is on slide:** A four-row document accompanies “Invented probabilities”, “Not an agent transcript” and “Read → predict → audit”. The notebook contains the full authored fixture.

**What I want to say:** This is a deliberately authored four-row fixture with invented probabilities. It is not an agent transcript and no fitted model generated its probability table. It isolates group overlap, preprocessing scope, positional joins and unsupported claims so we can reason about them by hand.

**Point / reveal:** Point to “Invented probabilities” and “Not an agent transcript”.

**Transition:** Flaw number one: look at the group IDs.

### S2-05 · Different IDs, the same family

**Proposed slide ID:** `day-4-s2-flaw-group-leakage` · **Time:** 36:30–39:30 (3:00)

**What is on slide:** Training and validation samples are arranged in columns. A line connects the shared group-a. Caption: “Unique samples ≠ independent groups”. The full sequences and labels remain in the notebook.

**What I want to say:** The sample IDs are distinct, but group-a appears in both splits. New-group generalization is therefore unsupported. Related sequences can let a model exploit family similarity; the fixture has no fitted model, so we cannot claim to have observed memorization here.

**Point / reveal:** Trace group-a across the two columns, despite distinct sample IDs.

**Transition:** Flaw number two: look at where feature extraction happened.

### S2-06 · The vocabulary saw validation

**Proposed slide ID:** `day-4-s2-flaw-preprocessing` · **Time:** 39:30–42:30 (3:00)

**What is on slide:** The single source line vectorizer.fit(samples["sequence"]) and caption “Training + validation informed the vocabulary”.

**What I want to say:** Flaw number two: Preprocessing leakage. Look at the vectorizer call. The vocabulary is fitted on the entire DataFrame, including validation sequences. Even without labels, the model's feature space is informed by validation sequence words before training begins. A pipeline must fit vocabulary on training rows only.

**Point / reveal:** Point to samples["sequence"] and identify which rows it includes.

**Transition:** Flaw number three: look at how predictions were matched to labels.

### S2-07 · Right numbers, wrong samples

**Proposed slide ID:** `day-4-s2-flaw-inverted-join` · **Time:** 42:30–46:00 (3:30)

**What is on slide:** Labels: validation-01=0, validation-02=1. Prediction rows: validation-02→0.1, validation-01→0.9. Pairing by row gives 1.0 accuracy; joining by ID gives 0.0. A button traces the two joins.

**What I want to say:** Flaw number three: Inverted array alignment. The prediction table had its rows reversed. Because the script compared numpy arrays by raw position (`y_true == y_pred`), it matched validation-01's label (0) with validation-02's prediction (0.1), claiming 100% accuracy! When aligned by sample ID, the real accuracy is 0.0.

**Point / reveal:** Click “Join by sample ID”; follow the crossed lines and the 100% → 0% change.

**Transition:** Flaw number four: what did the report claim?

### S2-08 · The claim outruns the evidence

**Proposed slide ID:** `day-4-s2-flaw-overclaim` · **Time:** 46:00–48:30 (2:30)

**What is on slide:** Two unsupported statements: “Learned promoter biology” and “Choose using the Day 3 test”. Captions distinguish missing biological validation from a proposed misuse without an observed test read.

**What I want to say:** The authored report makes an unsupported biological claim and proposes selecting against the Day 3 test. The proposal violates our evaluation policy. No test-access log is supplied; do not turn the proposed misuse into an assertion that test data was actually read.

**Point / reveal:** Read each claim and its evidence limit. Distinguish proposed misuse from actual access.

**Transition:** What is the overarching lesson of this fixture?

### S2-09 · What would you inspect first?

**Proposed slide ID:** `day-4-s2-discussion` · **Time:** 48:30–50:00 (1:30)

**What is on slide:** Open prompt: “The script runs. Which evidence would you inspect first?”

**What I want to say:** A program can print a confident report while the evidence fails. This example deliberately runs cleanly. Invite a starting point for an audit; no measured runtime or claim about prevalence in published papers is needed.

**Point / reveal:** Leave the question on screen for break reflection.

**Transition:** After the break, we replace the vague prompt with a precise specification.

### Break · 50–60

**Proposed slide ID:** `day-4-break-1` · **Time:** 50:00–60:00 (10:00)

**What is on slide:** Ten-minute break. *"Next: Turning scientific intent into an unambiguous contract."*

**What I want to say:** Return at minute 60. We will see how to make the scientific choices explicit and checkable.

---

<a id="section-3"></a>

## 3. Specifying the experiment: contracts and boundaries · 60–80

**Story question:** How do we turn scientific intent into an unambiguous contract that binds an agent's implementation?

**Exit understanding:** Deconstruct `agent_workshop/precise-spec.md`; understand the five essential pillars of a machine learning specification (Task, Data, Protocol, Deliverables, Constraints); define explicit prediction schemas; and prevent post-hoc evaluation drift.

**Teaching thread:** Move from unresolved choices to a checkable experiment specification. Walk through the five pillars in `precise-spec.md`. Emphasize that fixing the scientific design precedes writing code.

**Scope and delivery:** Students read `agent_workshop/precise-spec.md`. No coding or agent account required. Pairs discuss which requirement they would audit first.

### S3-01 · Specify the experiment

**Proposed slide ID:** `day-4-s3-spec-concept` · **Time:** 60:00–62:00 (2:00)

**What is on slide:** A researcher passes an experiment specification to an implementation terminal.

**What I want to say:** Write the scientific decisions down before implementation, in a form that can be checked. A document can make the contract easier to reuse and review, but the file format or length does not guarantee compliance.

**Point / reveal:** Show the specification document sitting between the question and the code.

**Transition:** Let us open `agent_workshop/precise-spec.md`.

### S3-02 · Five parts of a contract

**Proposed slide ID:** `day-4-s3-precise-spec-overview` · **Time:** 62:00–64:30 (2:30)

**What is on slide:** Five numbered parts: question/scope; allowed data/partitions; fixed model/fitting; metrics/threshold; outputs/provenance/limitations.

**What I want to say:** In `agent_workshop/precise-spec.md`, we provide an explicit analysis contract. Let us walk through the five pillars that constrain the agent.

**Point / reveal:** Point down the five numbered parts.

**Transition:** Pillar one: what data is allowed?

### S3-03 · Name the allowed data

**Proposed slide ID:** `day-4-s3-pillar-data` · **Time:** 64:30–67:30 (3:00)

**What is on slide:** Two documents, train.csv and validation.csv, with protected test evidence behind a barrier and lock.

**What I want to say:** Pillar one specifies the exact files and bounds. It explicitly names `train.csv` and `validation.csv`, and includes an absolute prohibition: `protected_test.csv` does not exist for this experiment. Any attempt to touch test data is a contract violation.

**Point / reveal:** Point to the allowed files and the test barrier.

**Transition:** Pillar two: what model is permitted?

### S3-04 · Fit the stated baseline

**Proposed slide ID:** `day-4-s3-pillar-features` · **Time:** 67:30–70:30 (3:00)

**What is on slide:** 4-mer counts and LogisticRegression(C=1.0, max_iter=2000, random_state=2026). Caption: vocabulary and classifier fit on training only. There is no scaler.

**What I want to say:** The precise specification fixes the count/logistic baseline. The vectorizer and classifier fit on training rows only. Use 2,000 maximum iterations and seed 2026. Do not add a StandardScaler or search other models while claiming to reproduce this configuration; the frozen-embedding classifier on Day 3 used a different pipeline.

**Point / reveal:** Point to counts and LR settings; reinforce training-only vocabulary and classifier fitting.

**Transition:** Pillar three: how will we measure success?

### S3-05 · Declare how success is measured

**Proposed slide ID:** `day-4-s3-pillar-evaluation` · **Time:** 70:30–73:30 (3:00)

**What is on slide:** Ranking with ROC-AUC (AP supporting) and class calls at p ≥ 0.5 appear side by side. The decision policy is declared before evaluation.

**What I want to say:** Declare the metric and threshold policy before evaluation. AP is not trapezoidal PR-AUC. Historical 0.802 belongs to the October 26 fixed-motif input, not the current PPM baseline near 0.608. Matching a configuration means matching data and probabilities, not chasing a score.

**Point / reveal:** Underline the fixed threshold 0.5 and primary ROC-AUC.

**Transition:** Pillar four: what output files must be delivered?

### S3-06 · Keep identity beside probability

**Proposed slide ID:** `day-4-s3-pillar-schema` · **Time:** 73:30–76:30 (3:00)

**What is on slide:** A two-column sample_id/probability table with the authored validation values. Rules: unique IDs, exact coverage, finite p in [0,1].

**What I want to say:** Pillar four defines the deliverable schema. Predictions must be written to `validation_predictions.csv` with exactly two columns: `sample_id` and `probability`. Storing the sample ID alongside the prediction makes defensive joins possible.

**Point / reveal:** Point to the two columns, then the exact-ID and probability rules.

**Transition:** Pillar five: how do we track what was executed?

### S3-07 · Keep an execution record

**Proposed slide ID:** `day-4-s3-pillar-provenance` · **Time:** 76:30–78:30 (2:00)

**What is on slide:** An execution-record document with input/source hashes, settings/seed, versions/commands, timing/limitations.

**What I want to say:** Pillar five requires a provenance ledger. The agent must document package versions, random seeds, wall-clock timing, input SHA-256 hashes, and any observed limitations. Without provenance, code cannot be audited.

**Point / reveal:** Trace each provenance category to an artifact you could inspect.

**Transition:** Section 3 summary before moving to project instructions.

### S3-08 · Specified does not mean verified

**Proposed slide ID:** `day-4-s3-wrapup` · **Time:** 78:30–80:00 (1:30)

**What is on slide:** “Fewer hidden choices. More checkable commitments.” An experiment specification leads to an evidence checklist.

**What I want to say:** The specification makes major choices explicit, but cannot remove every ambiguity or guarantee a correct implementation. Ask which commitment the class would verify first.

**Point / reveal:** Point to explicit commitments and invite the first check; do not imply all uncertainty disappeared.

**Transition:** Section 4: Giving instructions a job.

---

<a id="section-4"></a>

## 4. Giving instructions a job: AGENTS.md, skills, and actual runs · 80–100

**Story question:** How do we separate task specs from project rules and skills, and what did real agents do when run on these requests?

**Exit understanding:** Distinguish three jobs for agent guidance: task specification (`spec.md`), persistent project instructions (`AGENTS.md`), and reusable procedures (skills); inspect the actual October 26 clean agent runs; understand why the vague run scored 0.904 while the specified run scored 0.802.

**Teaching thread:** Introduce the three documents and their distinct jobs. Read `example-project/AGENTS.md`. Explain skills. Open the genuine October 26 agent runs (`actual_runs/2026-10-26/`). Show the provocative score gap (0.904 vs 0.802). Unpack the modeling choices to show that the comparison does not isolate prompt quality because the feature choices and search differ.

**Scope and delivery:** Open text files in `agent_workshop/example-project/` and `agent_workshop/actual_runs/2026-10-26/`. These are genuine recorded runs (`codex` / `gpt-6.1-sol`), not authored fixtures.

### S4-01 · Give each instruction a job

**Proposed slide ID:** `day-4-s4-three-tiers` · **Time:** 80:00–82:30 (2:30)

**What is on slide:** Three neighbouring documents with different roles: experiment spec (this task), AGENTS.md (project guidance), SKILL.md (reusable procedure). This is a division of jobs, not a universal instruction-precedence pyramid.

**What I want to say:** Don't cram everything into one giant prompt. Give each document a job: the specification defines this experiment, AGENTS.md carries project guidance, and a skill describes a reusable procedure. Loading, scope and precedence depend on the tool; these documents are not an operating-system sandbox.

**Point / reveal:** Point to the three documents and their distinct jobs. This is not an instruction-precedence hierarchy.

**Transition:** What belongs in `AGENTS.md`?

### S4-02 · Project rules travel with the code

**Proposed slide ID:** `day-4-s4-agents-md` · **Time:** 82:30–85:00 (2:30)

**What is on slide:** A link opens the actual example project AGENTS.md. Caption: “Development only · fixed identities · supported claims”.

**What I want to say:** These example project instructions tell a compatible agent how to work in the isolated demonstration folder: keep development boundaries, preserve identities, fit on training only and qualify simulation claims. Loading and scope depend on the tool; instructions need verification and are not an operating-system sandbox.

**Point / reveal:** Open the linked actual project guidance, then point out its development and identity rules.

**Transition:** And what is a skill?

### S4-03 · A skill supplies a procedure

**Proposed slide ID:** `day-4-s4-skills-concept` · **Time:** 85:00–87:30 (2:30)

**What is on slide:** A SKILL.md document leads to Read the spec → Trace fitting + IDs → Check predictions → Report evidence + limits. This is an instruction procedure; the separate notebook supplies executable audit code.

**What I want to say:** A skill is a package of procedural instructions and tools for a specific recurring task. Our example scientific-audit skill describes an evidence procedure. The separate course audit function and handout supply executable checks and discussion structure.

**Point / reveal:** Trace the four procedural steps; distinguish the instructions from the separate audit code.

**Transition:** Now let's see how real agents behaved with these instructions.

### S4-04 · Two genuine previous runs

**Proposed slide ID:** `day-4-s4-actual-runs-intro` · **Time:** 87:30–90:00 (2:30)

**What is on slide:** The same development files branch to a vague request and specified baseline. Caption identifies genuine saved October 26 runs on the historical fixed-motif data.

**What I want to say:** These are genuine October 26 Codex/gpt-6.1-sol runs on the older fixed-motif inputs. Both fresh contexts had identical development files and operational restrictions; only one received the scientific specification, project guidance and audit skill. Both needed a technical apply-patch correction, and the vague run was resumed after that intervention. They are saved code and text records, not a video or a new live execution.

**Point / reveal:** Highlight that both contexts started with byte-identical development datasets.

**Transition:** What scores did they achieve?

### S4-05 · A higher score—for what task?

**Proposed slide ID:** `day-4-s4-score-comparison` · **Time:** 90:00–93:00 (3:00)

**What is on slide:** An interactive chart switches between ROC-AUC and average precision for the genuine historical runs. Vague: 0.9041667 / 0.8589; specified: 0.8019444 / 0.8024506. Caption identifies fixed-motif data and the uncontrolled prompt comparison.

**What I want to say:** Look at the scores! The vague run achieved a validation ROC-AUC of 0.904, while the specified run achieved 0.802. A superficial observer would say, "Look! Vague prompting is superior! Writing detailed specifications made the model worse!" Is that true?

**Point / reveal:** Show ROC-AUC, then switch to AP. Invite explanations before moving to the model choices.

**Transition:** Let us look inside the code of both runs.

### S4-06 · Different searches, different features

**Proposed slide ID:** `day-4-s4-under-the-hood` · **Time:** 93:00–96:30 (3:30)

**What is on slide:** Specified: fixed 4-mer/logistic baseline, no alternative search. Vague: six candidates; training-only five-fold group CV selected disclosed-motif logistic regression by pooled out-of-fold log loss. The motif prior TATAAATG was supplied in the dataset description.

**What I want to say:** The vague run used a disclosed fixed-motif prior; it did not discover a biological mechanism. It compared six candidates using training-only group CV. The specified run reproduced the fixed baseline; the archived parent comparison reports maximum probability difference 1.11e-16. Different features, objectives and searches explain why this is not an isolated prompt experiment.

**Point / reveal:** Contrast the two modeling decisions side by side.

**Transition:** What is the scientific takeaway from this comparison?

### S4-07 · This did not isolate prompt quality

**Proposed slide ID:** `day-4-s4-diff-experiments` · **Time:** 96:30–99:00 (2:30)

**What is on slide:** “Different features. Different search.” followed by “Prompt quality was not isolated.”

**What I want to say:** This is a crucial lesson in AI evaluation: You cannot compare prompt effectiveness when the models are solving different optimization problems. The saved vague-run code uses training-only group CV and the inspected identity checks pass. This supports a narrower conclusion than proving every possible leakage or access risk absent. It answered a different optimization question from the specified baseline.

**Point / reveal:** Underline that prompt quality was not isolated.

**Transition:** Section 4 wrap-up before the break.

### S4-08 · Now audit what actually happened

**Proposed slide ID:** `day-4-s4-wrapup` · **Time:** 99:00–100:00 (1:00)

**What is on slide:** “Instructions clarify the task.” followed by “Now audit what actually happened.”

**What I want to say:** Instructions clarify expectations, but they do not prove scientific correctness. That requires an independent audit, which we will conduct after the break.

**Point / reveal:** Point to the next audit activity.

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

### S5-01 · Follow the claim back to evidence

**Proposed slide ID:** `day-4-s5-audit-definition` · **Time:** 110:00–113:00 (3:00)

**What is on slide:** Claim → Artifacts → Checks, with document icons asking what is asserted, what supports it, and what remains unresolved.

**What I want to say:** In `GLOSSARY.md`, we define a scientific audit not as checking if code compiles or runs without error. An audit asks: Did the evaluation isolate the intended question? Did groups leak? Were samples joined correctly? Are the claims supported by evidence?

**Point / reveal:** Trace claim → artifacts → checks, then ask what remains unresolved.

**Transition:** How do we automate these checks?

### S5-02 · What the code checks

**Proposed slide ID:** `day-4-s5-audit-code-overview` · **Time:** 113:00–116:00 (3:00)

**What is on slide:** Five numbered audit checks: columns/identities; exact evaluation-ID coverage; finite probabilities; one-to-one ID join/metrics; cross-split groups and duplicate sequences.

**What I want to say:** Look at `course_code/06_scientific_audit.py`. It is a defensive audit engine. It checks whether any `group_id` appears in more than one split, whether identical sequences cross splits, and verifies that prediction IDs match evaluation split IDs one-to-one before recalculating ROC-AUC and AP.

**Point / reveal:** Point to ID coverage and the one-to-one join, then group separation.

**Transition:** Let us run it on the authored fixture from Section 2.

### S5-03 · Run the fixture audit

**Proposed slide ID:** `day-4-s5-audit-fixture-run` · **Time:** 116:00–119:30 (3:30)

**What is on slide:** A link to the completed GitHub → Colab notebook with the selected fixture-audit and negative-probe checkpoints. The live output is read in the notebook; preprocessing requires source inspection.

**What I want to say:** Run the guided fixture audit in the completed notebook. The function returns an evidence report; it does not parse Markdown or automatically infer preprocessing from prediction tables. The separate fit(samples["sequence"]) line supplies the preprocessing finding. Metrics after alignment remain scientifically compromised by leakage and invented probabilities.

**Point / reveal:** Open the notebook, run fixture audit and negative probes, and read the actual output.

**Transition:** Now you will perform the audit using our one-page checklist.

### S5-04 · Your audit, in pairs

**Proposed slide ID:** `day-4-s5-checklist-activity` · **Time:** 119:30–125:00 (5:30)

**What is on slide:** Five audit themes, a link to the real handout, and a five-minute start/pause/reset timer. Pairs mark PASS / FAIL / UNVERIFIED. The allocation includes 30 seconds for instructions.

**What I want to say:** Open `instructor/audit-checklist.html` or look at your handout. In pairs, take five minutes to audit the claims in the fixture report against the checklist items. Mark each item as PASS, FAIL, or UNVERIFIED.

**Point / reveal:** Keep the five section headings visible and run the 5-minute timer.

**Transition:** Let us review the findings together.

### S5-05 · Evidence found. Evidence missing.

**Proposed slide ID:** `day-4-s5-checklist-review` · **Time:** 125:00–128:00 (3:00)

**What is on slide:** A button cycles six findings, one at a time: four FAIL findings (group separation, training-only vocabulary, metric correspondence, biological claim scope) and two UNVERIFIED findings (fitted predictor provenance and actual test-access history).

**What I want to say:** Several defects are directly supported, while a fitted probability-generation procedure and test-access record are absent. Missing evidence is unverified, not proof of either correct behavior or a test read. Use evidence, consequence and repair for each finding.

**Point / reveal:** Cycle all six findings; distinguish observed failures from missing evidence.

**Transition:** We use the Evidence $\rightarrow$ Consequence $\rightarrow$ Repair framework.

### S5-06 · Evidence → consequence → repair

**Proposed slide ID:** `day-4-s5-repair-framework` · **Time:** 128:00–131:30 (3:30)

**What is on slide:** Three linked steps: evidence (group-a crosses splits) → consequence (new-group claim unsupported) → repair (group-respecting split + refit in the separate exercise). This is not evidence of observed memorization.

**What I want to say:** When an audit finds a defect, you must structure your response scientifically: Evidence $\rightarrow$ Consequence $\rightarrow$ Repair. What did you observe? What scientific claim is invalidated by that observation? And what concrete repair must be executed?

**Point / reveal:** Trace evidence → consequence → repair; avoid claiming observed memorization.

**Transition:** How does this apply to real agent runs?

### S5-07 · Recompute the archived predictions

**Proposed slide ID:** `day-4-s5-audit-actual-runs` · **Time:** 131:30–136:00 (4:30)

**What is on slide:** Current local readback of the historical predictions: each arm has 240 matching validation IDs, zero cross-split groups and zero duplicate sequences. ROC-AUC is 0.9041667 vague and 0.8019444 specified.

**What I want to say:** Our local readback independently joins all 240 validation predictions by ID for each historical arm, checks groups and duplicate sequences, and recomputes ROC-AUC/AP. These checks pass; neither run reproduced the authored fixture. This does not verify every fitting decision or access history: inspect the saved code, prompts and records for those.

**Point / reveal:** Point to exact IDs, zero overlap and independently recomputed metrics for both arms.

**Transition:** But can automated code check everything?

### S5-08 · What still needs judgment?

**Proposed slide ID:** `day-4-s5-subtle-limitations` · **Time:** 136:00–139:30 (3:30)

**What is on slide:** “The tables pass the checks.” followed by “Is the scientific question still sound?”

**What I want to say:** Notice what the automated audit cannot do. It cannot tell you whether a 4-mer baseline is scientifically meaningful for your research question. It cannot tell you whether your simulated sequences mimic real mammalian promoters. Automated checks can assist research judgment, but passing these table checks alone does not establish scientific validity.

**Point / reveal:** Invite a claim that still requires research judgment or additional evidence.

**Transition:** And how do we repair models without cheating?

### S5-09 · Repair inside development

**Proposed slide ID:** `day-4-s5-repair-without-cheating` · **Time:** 139:30–143:00 (3:30)

**What is on slide:** The inspect/act/observe/revise loop, fully visible. Caption: “Repair → refit → validation · keep the old test out”.

**What I want to say:** If your audit reveals an error, how do you repair it? You fix the code and re-evaluate on validation data. You never use the Day 3 test set to check if your repair worked. If revealed, the test result remains historical evidence about the frozen workflows; if not, keep it protected.

**Point / reveal:** Trace the development-only repair loop; preserve the main-course frozen comparison.

**Transition:** Section 5 summary before we look at automated platforms.

### S5-10 · What can you defend now?

**Proposed slide ID:** `day-4-s5-checkpoint` · **Time:** 143:00–146:00 (3:00)

**What is on slide:** “Defend one sentence.” followed by “Name the artifact that supports it.”

**What I want to say:** We have audited manual scripts, authored fixtures, and clean agent runs. Now, how do these lessons translate when automation scales up to complex, multi-step platforms?

**Point / reveal:** Invite one supported sentence and its artifact.

**Transition:** Section 6 begins at minute 150.

### S5-11 · Questions before the final session

**Proposed slide ID:** `day-4-s5-buffer` · **Time:** 146:00–150:00 (4:00)

**What is on slide:** Open discussion prompt: “What would you like to revisit?” with splits, fitting scope, identity and claim limits.

**What I want to say:** Take four minutes for questions about split leakage or alignment audits before the platform evidence discussion.

**Point / reveal:** Open floor for questions.

**Transition:** Section 6: Automated platforms and responsibility.

---

<a id="section-6"></a>

## 6. Automated workflows and scientific responsibility · 150–180

**Story question:** How do we evaluate end-to-end automated platforms like Agentomics, and what must remain permanent human scientific responsibility?

**Exit understanding:** Use the agreed Agentomics audit-discussion fallback (minutes 150–170) to identify required split, execution and prediction artifacts; keep product behavior unverified; and participate in the final 10-minute whole-course synthesis (minutes 170–180) across count, learn, reuse, and delegate.

**Teaching thread:** Introduce multi-step workflow platforms. Pose the three platform audit questions. Run the selected 20-minute evidence discussion; the actual product demonstration remains pending. Transition at minute 170 to the protected 10-minute whole-course synthesis. End on the four-day progression and permanent human responsibility.

**Scope and delivery:** Minutes 150–170 retain the reserved Agentomics slot, using the instructor-selected audit-discussion fallback. Mark the demonstration pending; no verified access, example or recording is supplied and no product behavior is asserted. Minutes 170–180 are strictly protected for whole-course synthesis.

### S6-01 · What should a platform expose?

**Proposed slide ID:** `day-4-s6-agentomics-intro` · **Time:** 150:00–153:00 (3:00)

**What is on slide:** A generic workflow schematic: question → data → execution → artifacts → claim. Caption: “Platform inspection plan”. No product interface or capability is asserted.

**What I want to say:** The instructor chose the audit-discussion fallback for the Agentomics slot. We have no verified product demonstration or recording. Use the next twenty minutes to decide what evidence a workflow platform would need to expose. This diagram is a generic inspection plan, not observed Agentomics behavior.

**Point / reveal:** Follow the generic question-to-claim workflow; no product behavior is asserted.

**Transition:** What questions must we ask when inspecting such a platform?

### S6-02 · Three evidence questions

**Proposed slide ID:** `day-4-s6-three-platform-questions` · **Time:** 153:00–156:00 (3:00)

**What is on slide:** Three evidence questions: Where are the split identities? Where is the execution record? Where are the raw predictions?

**What I want to say:** When an automated system presents you with a finished paper or report, you must ask the same three questions we practiced today: Can I see the splits? Can I inspect the execution ledger? Can I download the raw prediction CSV and verify the join?

**Point / reveal:** Point to the three evidence questions.

**Transition:** Use these questions to structure the fallback discussion.

### S6-03 · Agentomics · discussion fallback

**Proposed slide ID:** `day-4-s6-agentomics-demo` · **Time:** 156:00–166:00 (10:00)

**What is on slide:** “Agentomics demonstration pending” with the discussion prompt “What evidence would you need?” This uses the agreed fallback and does not show a product interface.

**What I want to say:** This is the agreed structured discussion fallback; no Agentomics workflow has been observed. In pairs, describe where you would look for dataset identity, fitted preprocessing, raw predictions and provenance, then say which conclusion must remain unverified if those artifacts are missing. Keep the ten-minute closing at 170.

**Point / reveal:** Facilitate the evidence discussion. Do not describe imagined UI buttons or product features as observed.

**Transition:** How do our checklist criteria apply here?

### S6-04 · Make the missing evidence visible

**Proposed slide ID:** `day-4-s6-agentomics-audit` · **Time:** 166:00–170:00 (4:00)

**What is on slide:** Three blank areas for “Evidence needed”, “Why it matters” and “Still unverified”. The discussion records requirements, not platform findings.

**What I want to say:** Turn each requested artifact into a verification question. With no demonstration, product capabilities remain unverified. Hashes help trace identities but do not by themselves prove correctness. At minute 170 close the platform discussion and move to the course synthesis.

**Point / reveal:** Collect required evidence and unanswered questions; no pass labels for an unobserved platform.

**Transition:** At minute 170, we enter the final ten minutes: whole-course synthesis.

---

### S6-05 · Count → learn → reuse → delegate

**Proposed slide ID:** `day-4-s6-four-day-journey` · **Time:** 170:00–174:00 (4:00)

**What is on slide:** Four native illustrations: count bars, a small neural network, a DNA helix and an agent terminal. The progression is Count → Learn → Reuse → Delegate. Caption asks where features come from and what evidence supports the claim.

**What I want to say:** We have reached the final ten minutes of our course. Look at the path we have traveled. On Day 1, we hand-counted k-mers. On Day 2, we taught convolutions to learn local patterns. On Day 3, we borrowed representations from foundation models and enforced a strict evaluation freeze. Today, on Day 4, we learned how to delegate coding to AI agents without surrendering scientific rigor.

**Point / reveal:** Follow the four-day illustrations from count to delegate.

**Transition:** What must always remain with the human researcher?

### S6-06 · The scientific responsibility stays yours

**Proposed slide ID:** `day-4-s6-human-responsibility` · **Time:** 174:00–177:00 (3:00)

**What is on slide:** A researcher surrounded by the question, the evaluation, the evidence and the final claim.

**What I want to say:** You can delegate implementation, design suggestions and checks, while keeping responsibility for the question, evidence and final claim. An agent can help audit code, but its own report is not independent proof. Use reproducible checks and independent review appropriate to the claim.

**Point / reveal:** Point around the four responsibilities held by the researcher.

**Transition:** One closing question for everyone.

### S6-07 · What will you check next?

**Proposed slide ID:** `day-4-s6-final-discussion` · **Time:** 177:00–180:00 (3:00)

**What is on slide:** “One claim you can defend. One check you will keep.” Links to all four days, completed notebooks and the audit checklist.

**What I want to say:** Thank you for your hard work over these four intensive days. To close: what is one check you will always perform before trusting a machine learning result in bioinformatics? Thank you all, and good luck with your research.

**Point / reveal:** Invite two or three parting responses from students before closing.

**Transition:** End of Day 4 and conclusion of the course.

---

<a id="workshop-plan"></a>

## Workshop plan

Day 4 practical work uses the [completed audit notebook](../../notebooks/06_scientific_audit.ipynb) via GitHub → Colab, plus local text files under `agent_workshop/` and `course_code/06_scientific_audit.py`. Setup → shared/stage 06 definitions → authored fixture → STOP; Section 5 resumes at fixture audit, negative probes and historical saved-prediction readback. No account with an agent service, training run or protected test access is needed.

| Checkpoint | Student / Instructor Action | Classroom Delivery State |
| --- | --- | --- |
| 25–50: Vague prompt & fixture | Read `vague-prompt.md`; inspect `fixture.md`; predict failure modes. | Local text files plus a completed notebook fixture checkpoint. |
| 60–80: Precise specification | Read `precise-spec.md`; identify five pillars and required schema. | Text files; no execution required. |
| 80–100: Historical run inspection | Open `actual_runs/2026-10-26/README.md`; contrast vague (0.904) vs specified (0.802). | Saved code/logs and current prediction/identity readback; not complete proof of scientific validity. |
| 110–135: Hands-on audit | Run the completed notebook fixture and historical saved-prediction audits; fill out the checklist. | Completed GitHub notebook checkpoints; local timings in the verification record, Colab not rehearsed. |
| 135–150: Repair discussion | Discuss Evidence $\rightarrow$ Consequence $\rightarrow$ Repair table. | Ungraded paired discussion. |
| 150–170: Agentomics slot | Structured discussion of the artifacts needed to audit an automated workflow. | Instructor-selected fallback; actual demonstration pending, not delivered. |
| 170–180: Course synthesis | Whole-class discussion: human scientific responsibility. | Protected 10-minute closing discussion. |

---

<a id="evidence-and-scope"></a>

## Evidence and scope

### Dataset and evaluation continuity

- **Development inputs only:** The historical agent packet contains 720 training and 240 validation sequences. The separate authored fixture has two training and two validation rows. Protected course test files/results are absent from the guided Day 4 payload and were not loaded by the local rehearsal.
- **Authored fixture vs actual runs:** `agent_workshop/fixture.md` is an authored teaching fixture, not a recorded agent transcript. The October 26 runs (`agent_workshop/actual_runs/2026-10-26/`) are genuine recorded executions using `gpt-6.1-sol` via Codex.
- **Evaluation policy:** ADR 0002 is maintained. Revealed Day 3 test results are historical evidence and cannot be used for Day 4 agent model selection.
- **Scientific scope:** ADR 0001 is maintained. All sequence data is simulated; these results do not establish real promoter prediction or biological discovery.
