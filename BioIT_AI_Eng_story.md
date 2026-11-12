# From language models to coding agents

## Teaching purpose and story

This lecture is for MSc Bioinformatics students who understand Python and mostly
use LLMs by copying code between a chat and their notebooks. Begin with that
familiar workflow, then explain what changes when the surrounding software lets
a model read files, request actions, and use the returned evidence.

The story builds six layers in order:

1. **LLM:** generates text using learned parameters and the current context.
2. **Agent:** uses a model, instructions, and tools in an action/result loop.
3. **Subagent:** handles a focused assignment in a separate conversation context.
4. **Skill:** supplies reusable instructions and optional supporting resources.
5. **Harness:** manages the session and executes permitted tool requests.
6. **Working process:** Matt Pocock's skills apply these pieces to clarification,
   specification, implementation, review, and improvement.

The objective is practical understanding: students should be able to explain the
parts, recognise them in a coding tool, give a bounded request, invoke a skill,
and assess the work produced. A final applied section connects those concepts
to scientific judgement, evidence, and reproducibility.

The revised deck has **49 slides**. Its style follows the instructor's
`Alexiou_Agentomics_3.html`: white backgrounds, Newsreader serif text, JetBrains
Mono labels and code, warm beige panels, fine neutral rules, and restrained gold
accents. Definitions remain visible, while process maps, annotated source files, scientific diagrams, and four illustrated section breaks vary the composition. The reference
HTML is copied into this folder byte-for-byte; neither it nor the Downloads
original is edited. Each concept has a definition and
an explanation, concrete example, or short procedure. Speaker notes add teaching
cues and qualifications; essential definitions are visible on the slide itself.

The examples use sequence validation to connect the layers without prescribing
the live demonstration. They distinguish actual source material from authored
teaching examples. The real `grill-me/SKILL.md` is shown in full, followed by
excerpts from the shared `grilling` instructions it loads.

**Exercise 10 has exactly one slide, with only “Live Demo on Exercise 10” visible.**
Develop it live with the class. No specification, interface plan, feature list,
scripted implementation, or completed application is prepared in this deck.

The final applied section follows one hypothetical gene-expression analysis with
several samples per patient. It asks how to evaluate predictions for unseen
patients, then connects the brief, context, decisions, changes, checks, and
methods record. No actual patient data or performance results are presented.

## Sequence and pacing

| Part | Slides | Learning question | Suggested time |
| --- | --- | --- | ---: |
| Title | 01 | Introduce the lecture and presenter. | 1 min |
| How LLMs work | 02–08 | How do instructions and context become generated text? | 10 min |
| Agents (transition 09) | 10–12 | What changes when the model can request real actions? | 5 min |
| Subagents | 13–15 | Why delegate a focused task with separate context? | 5 min |
| Skills (transition 16) | 17–22 | What is in a skill, and how do I use it? | 9 min |
| Harnesses and T3 Code | 23–27 | What runs the actions, and where do I inspect them? | 7 min |
| Matt's skills and Main Flow (transition 28) | 29–37 | How does an idea become checked work? | 9 min |
| Scientific coding in practice (transition 38) | 39–48 | What evidence lets us trust this analysis? | 15 min |
| Live demonstration | 49 | Live Demo on Exercise 10 | 15+ min |

The expanded material, including short section transitions, takes roughly 75–80 minutes with a 15-minute demonstration.
For a one-hour session, move more quickly through the terminology and use the
applied section as discussion rather than reading every slide aloud. Explain all
six Main Flow skills, but use a focused subset during the live demonstration.

## Teaching choices and best practices

- Start with what students already do, then introduce one new layer at a time.
- Define terms before relying on them. Distinguish the model's text from an
  action executed by software and an actual returned result.
- Use small, relevant context: the code, error, example inputs, and the goal.
  Save decisions in project files so they can be read again later.
- Give agents bounded tasks with a clear scope and observable completion.
- Explain separate subagent context without suggesting a separate filesystem.
  Context separation does not imply file isolation.
- Show the skill file itself: YAML metadata, the Markdown instruction body,
  and optional references, scripts, and assets. Loading a skill does not itself
  spawn a subagent or retrain a model.
- Show user-facing invocation syntax and explain that it depends on the harness.
- Review the actual changed files and relevant behaviour. Agent reports and
  independent reviews support judgement; inspect their evidence.
- Use only as much process as the task needs. The routing table provides
  alternative ways to clarify uncertainty, rather than compulsory stages.

## Visual teaching and pacing

The [subagent critique](.frontend-slides/slide-engagement-review.md) scores all
44 original slides using a subjective boredom rubric. The main issue was the
repeated definition-plus-two-columns composition; 25 original slides scored 8 or
higher. The scores are editorial judgements, not measured student attention.

The revision keeps the established conceptual order and uses different visual
forms for different teaching jobs:

- Compare familiar copy/paste with the tool-connected workflow at the opening.
- Draw boundaries and feedback: available context, agent actions, delegated
  context, harness execution, and returned evidence.
- Show readable artifacts: real skill metadata/body, package folders,
  specification, ticket, Python checks, and methods note.
- Follow Main Flow through its outputs; each of its six skills still has its
  own explanatory slide. The same small DNA policy connects the examples.
- Show patient/sample alignment and paired partition diagrams. The scientific
  example asks about unseen patients without inventing performance results.
- Use illustrated transitions at 09, 16, 28, and 38. Each states the question
  that the next section answers. Slide 48 asks students to justify a claim
  before the unscripted live demonstration.

All illustrations are authored SVG or HTML/CSS diagrams. Conceptual software
views are labelled; none is presented as an actual T3 screenshot. Definitions
and practical explanations remain part of the visible slides.

## Slide-by-slide teaching script

### 01 — AI Engineering

**Title slide:** BioIT / MSc Bioinformatics. AI Engineering — From language models to scientific coding agents.

**Presenter:** Panagiotis Alexiou. University of Malta.

**Visual form:** Agentomics title composition: centered serif title, gold monospace kicker, and the original embedded University of Malta, BioGeMT, and European Union logos. The Agentomics source file remains unchanged.

**Teaching notes:** Introduce the lecture, then advance to the familiar copy-paste workflow.

### 02 — From copy-paste to coding agents

**Definition / framing:** A coding assistant can do more than suggest snippets. In this lecture we will see how a language model becomes a system that can inspect files, use tools, and follow a working process.

**Visual form:** opening map

Today · you carry the context

Chat

Ask for Python

 → Notebook

Paste → run → copy the error

With an agent · tools connect the loop

Conversation

State the goal

 → Project + tools

Read → edit → run → inspect

The researcher still directs the work

You choose the scientific question and judge the result. The change is who moves information between the conversation and the code.

**Teaching notes:** Connect to the MSc students’ existing Python and copy-paste experience. The current flow is useful; explain how an agent changes who transfers information and performs actions. The instructor still owns the purpose, important decisions, and acceptance of results.

Source: [AI Hero · Dictionary](https://www.aihero.dev/ai-coding-dictionary).

### 03 — What is a language model?

**Definition / framing:** A large language model (LLM) is a trained model that generates text from the information supplied to it. Code is one kind of text it can generate.

**Visual form:** two processes

Training · parameters change

Training data

Examples of text and code

 → Learning

Adjust model parameters

Using the model · a normal request

Context

Instructions + relevant information

 → Trained model

Generate a response

Reading your notebook supplies context for a request; it does not normally retrain the model.

**Teaching notes:** Distinguish training from inference without explaining transformer internals. A model can produce useful behaviour while still generating unsupported statements. The LLM helping write code and a scientific classifier have different jobs.

Source: [AI Hero · Dictionary](https://www.aihero.dev/ai-coding-dictionary).

### 04 — System prompts and user prompts

**Definition / framing:** A prompt gives instructions or a request to the model. Message roles distinguish standing application guidance from what the user is asking for now.

**Visual form:** artifact and explanation

System prompt · teaching example

```
You are a Python teaching assistant.
Explain your reasoning clearly.
Do not change files unless asked.
```

User prompt · concrete request

```
Explain this validation check:

assert dataset["sequence"].str.fullmatch(
    "[ACGT]{100}"
).all()

Which inputs would fail it?
```

**Teaching notes:** The Python expression is from Exercise 2’s load-data cell, reformatted across lines. The example prompts are authored teaching examples, not a captured system prompt or live run. Applications can also provide developer messages and tool results; roles are not interchangeable. The assertion expects every sequence to be exactly 100 A/C/G/T characters.

Source: [AI Hero · Dictionary](https://www.aihero.dev/ai-coding-dictionary).

### 05 — What is a token?

**Definition / framing:** A token is a piece of text used by the model. A token can be a whole word, part of a word, punctuation, or whitespace; tokens are not the same as words.

**Visual form:** explanatory comparison

Illustrative text split

predictions.
The exact boundaries depend on the tokenizer. This split is an illustration, not a measured result.

Why this matters in practice

Your messages, code, file contents, tool results, and generated response all use tokens. A long sequence string or a large CSV can take substantial space even if it looks like “one item”.

**Teaching notes:** Do not claim the illustrative split is an actual encoding. Relate tokens to the practical cost of supplying large files. A nucleotide is not necessarily one token. Exact counts require the tokenizer used by the chosen model.

Source: [AI Hero · Dictionary](https://www.aihero.dev/ai-coding-dictionary).

### 06 — How next-token generation works

**Definition / framing:** An autoregressive LLM repeatedly predicts possible next tokens, chooses one using a decoding procedure, appends it, and uses the extended text to predict again.

**Visual form:** generation stage

Current text · illustrative continuation

Read the

[Button: Next token →]

Repeat for each token

Predict possible next tokens → choose one → append it → predict again using the extended text.

This fixed illustration makes no model call. Actual decoding need not choose the single most likely token.

Fluent code is still generated text. It has not been executed or checked merely because the model produced it.

**Teaching notes:** Use the button to append notebook and then punctuation to the fixed sentence. No probabilities are invented. The actual loop uses a distribution over next tokens, not a fixed list of word choices. Ask: does generating “I read the file” establish that the file was read? Tools provide that evidence later.

Source: [AI Hero · Dictionary](https://www.aihero.dev/ai-coding-dictionary).

### 07 — What belongs in the context?

**Definition / framing:** Context is the information available to the model for the current request: instructions, conversation, and any file contents or tool results that have been supplied.

**Visual form:** context container

Available to this request

Instructions

Goal, constraints, coding rules

Conversation

Relevant questions and decisions

Code + examples

Validation cell and a few sequences

Tool results

The actual error or returned output

On disk ≠ in context

A repository can contain thousands of files. The model only uses file contents that have been supplied; an agent can request the relevant files with tools.

**Teaching notes:** A repository existing on disk does not mean every file is in the request. An agent can use tools to read what is needed. A hallucination is an unsupported or invented claim; check consequential claims against actual sources.

Source: [AI Hero · Dictionary](https://www.aihero.dev/ai-coding-dictionary).

### 08 — The context window and longer tasks

**Definition / framing:** The context window is the finite amount of information a model request can hold, measured in tokens. Available capacity depends on the model and the surrounding software.

**Visual form:** context window

A finite context window · schematic, not to scale

InstructionsConversationRead filesTool results
Longer work → summarise or omit older material to fit

Important decisions can disappear from the active request or lose detail in a summary.

Save requirements in project files. Ask a new session to read them before continuing.

**Teaching notes:** Distinguish the context window from persistent memory and from training. Summaries can lose detail; saving a decision makes it recoverable, but the agent must still read it. Avoid invented percentages or model capacity claims.

Source: [AI Hero · Dictionary](https://www.aihero.dev/ai-coding-dictionary).

### 09 — From generated text to actions

**Section transition.** How does a model work with files and tools?

We will follow a tool request through execution and feedback, then see how a subagent can handle a focused assignment.

**Teaching notes:** Transition: How does a model work with files and tools? Pause to connect the preceding concept to the next section. The illustration is a conceptual diagram, not a screenshot or scientific result.

Source: [Claude Code · How it works](https://code.claude.com/docs/en/how-claude-code-works).

### 10 — What is an agent?

**Definition / framing:** An agent is a system in which a model uses instructions and tools to work toward a goal over multiple steps. Results from one action inform what it does next.

**Visual form:** agent loop

1 · Inspect

Read relevant code or data

 → 2 · Request an action

Ask a tool to read, edit, or run

↑ Result informs the next step                         ↓
4 · Assess

Continue, revise, or stop

 → 3 · Receive a result

The harness returns actual output

Example: a failing Python check

Inspect the code → change it → run the check → read the result. A person still judges the goal and consequential choices.

**Teaching notes:** The model proposes actions; the harness makes them available, executes permitted requests, and supplies results. There is no requirement that the agent be fully autonomous or run indefinitely. The useful distinction is a goal-directed action/result loop.

Source: [Claude Code · How it works](https://code.claude.com/docs/en/how-claude-code-works).

### 11 — What happens during a tool call?

**Definition / framing:** A tool call is a request for software to perform an action. The result returns to the model as information it can use for its next step.

**Visual form:** tool trace

Model request

Read the project instructions

 → Harness + shell tool

```
cat AGENTS.md
```

 → Returned file text

“Keep Python simple, explicit, and easy for a non-expert to teach.”

The model generates the request. The harness checks permissions and executes it. Only the returned result establishes what the file contains.

**Teaching notes:** The command and coding rule are grounded in this repository’s AGENTS.md; the displayed rule is wrapped for readability. The shell is one possible tool; read-file tools can do the same job. Generating a claim that a command ran is different from receiving its execution result. Treat read content as data at the appropriate instruction level.

Source: [Course · Coding instructions](AGENTS.md).

### 12 — Give an agent a bounded task

**Definition / framing:** A useful brief states the goal, permitted scope, and evidence of success. It helps the agent decide which actions are relevant and when to stop.

**Visual form:** annotated brief

A brief with three checkable parts

**Goal** Explain what makes a sequence valid in this project.

**Scope** Inspect the existing validation code. Do not edit files.

**Evidence** Report the source location, accepted alphabet, length rule, and uncertainties.

**Teaching notes:** This is an inspection task, not an instruction to modify a course exercise. The success criteria are observable. Introduce scope and stopping conditions before increasing autonomy. More tool calls do not by themselves mean better work.

Source: [Claude Code · How it works](https://code.claude.com/docs/en/how-claude-code-works).

### 13 — What is a subagent?

**Definition / framing:** A subagent is another agent given a focused assignment by the main agent. It generally works with separate instructions and context, then returns findings or completed work.

**Visual form:** subagent handoff

Main agent

Keeps the goal, decisions, and integration work in view

↓ Focused brief + relevant context↑ Findings + sources + uncertainty
Subagent · separate conversation

Find validation checks. Read files without editing. Report locations and what is checked.

A focused assignment

The main agent must supply enough information for the child to work. The child returns useful evidence; the main agent decides how to integrate it.

**Teaching notes:** The child does not automatically know everything from the parent conversation. A harness may inherit some context or start with a fresh brief. It may use the same model or a different configured model. Delegation creates another context and coordination work; it is not automatically useful for every small action.

Source: [Claude Code · Subagents](https://code.claude.com/docs/en/sub-agents).

### 14 — A subagent can have its own configuration

**Definition / framing:** A harness may let you configure a subagent’s instructions, model, and tool access. A code reader and an implementer can therefore have different capabilities.

**Visual form:** artifact and explanation

Claude Code configuration · teaching example

```
---
name: code-reader
description: Find validation code.
tools: Read, Glob, Grep
model: inherit
---
Report relevant files and checks.
Do not edit files.
```

What the fields control

- name / description: identify the role and when it is useful.
- tools: choose the available tool set.
- model: inherit the parent’s model here.
- Body: give the task-specific instructions.

**Teaching notes:** This is an illustrative Claude Code subagent definition, not a configured agent in this repository. A project definition can live under .claude/agents/. Syntax and supported controls vary by harness. Separate context does not create a separate filesystem or checkout; multiple agents may share files.

Source: [Claude Code · Subagents](https://code.claude.com/docs/en/sub-agents).

### 15 — Why delegate into a separate context?

**Definition / framing:** A subagent can inspect lengthy files or logs without placing the entire exploration in the main conversation. It returns the evidence needed for the next decision.

**Visual form:** context handoff

Subagent exploration

Notebook cells

Read the relevant inputs

Search results

Locate validation code

Logs

Inspect the failure

 → Useful return

Rules + source locations + open questions

The main conversation receives the findings rather than every search result. This preserves room for the overall task.

Summaries can omit detail. Delegation adds coordination, and separate contexts do not isolate concurrent edits to shared files.

**Teaching notes:** This makes context management concrete without claiming that delegation is free or always reduces total tokens. Keep the main context focused, but retain a route back to source evidence.

Source: [Claude Code · Subagents](https://code.claude.com/docs/en/sub-agents).

### 16 — Procedures the agent can read

**Section transition.** How do we give a recurring task a repeatable method?

A skill is a readable package of instructions. We will open a real skill, follow how it is loaded, and place it inside the surrounding software.

**Teaching notes:** Transition: How do we give a recurring task a repeatable method? Pause to connect the preceding concept to the next section. The illustration is a conceptual diagram, not a screenshot or scientific result.

Source: [Claude Code · Skills](https://code.claude.com/docs/en/skills).

### 17 — What is a skill?

**Definition / framing:** A skill is a reusable package of instructions for a type of task. Its main file, SKILL.md, describes when the skill is useful and how the agent should approach the work.

**Visual form:** skill document

Reusable procedure

SKILL.md

Name + description
Instructions + decision rules
Links to optional resources

A practical example

A review skill can tell the agent what to inspect, which questions to ask, and how to report findings. You can read and adapt that procedure instead of repeating it in every conversation.

**Teaching notes:** A skill provides guidance; it is not new model training and it is not automatically a separate agent. Tools still perform executable actions. The following slides inspect real files from Matt Pocock’s repository, then show how discovery and invocation work.

Source: [Claude Code · Skills](https://code.claude.com/docs/en/skills).

### 18 — Anatomy of a real SKILL.md file

**Definition / framing:** This is Matt Pocock’s actual grill-me skill. The YAML block between the --- lines is metadata; the text below it is the instruction body.

**Visual form:** annotated source

Actual grill-me/SKILL.md · complete file

```
---
name: grill-me
description: A relentless interview to sharpen a plan or design.
disable-model-invocation: true
---
```

```
Call the Skill tool with "grilling".
```

01 · YAML metadata

Name identifies the skill; description explains its purpose. The explicit-invocation control requires the user to select it where supported.

02 · Markdown instructions

This small wrapper loads the shared grilling procedure. Loading a skill does not itself spawn a subagent.

**Teaching notes:** Source checked 11 November 2026; this full file is shown verbatim apart from trailing whitespace. The flag is documented by Claude Code; controls and equivalent behaviour vary by harness. This small wrapper loads another skill’s instructions. It does not spawn a subagent just because another skill is mentioned.

Source: [Matt Pocock · grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md).

### 19 — The shared instructions explain the behaviour

**Definition / framing:** The grill-me wrapper loads grilling, which contains the interview procedure. The agent follows these instructions in the conversation rather than learning a new capability through training.

**Visual form:** artifact and explanation

Excerpts from grilling/SKILL.md

```
Interview the user relentlessly until you reach a shared understanding.

Word each question so "yes" accepts your recommended answer.
```

What the user experiences

- Questions are organised into rounds.
- Recommendations help make decisions explicit.
- The agent waits for answers before dependent questions.
- The user confirms the shared understanding.

**Teaching notes:** The two quoted sentences are exact excerpts, not one continuous block of the source. Explain the full procedure from the actual grilling skill: work a design tree, ask the settled frontier, wait for answers, and do not implement before shared understanding is confirmed. We are describing the skill, not invoking it on this presentation request.

Source: [Matt Pocock · grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md).

### 20 — How a skill gets loaded

**Definition / framing:** Skills commonly use progressive loading: a short description helps selection, the full instructions are read when the skill is chosen, and supporting material is loaded as needed.

**Visual form:** progressive loading

1 · Discover

Name + short description

 → 2 · Load

Read the selected SKILL.md

 → 3 · Consult

Read linked resources as needed

An installation may contain many skills. Their descriptions help the harness or model select relevant instructions.

Reading every skill and reference for every request would consume context. Progressive loading brings in detail when it is useful.

**Teaching notes:** This is supported by the official OpenAI Docs skill guide and Claude Code skills documentation. Initial discovery limits and invocation details are product-specific. Do not claim that every installed skill is fully loaded, or always visible, on every request.

Source: [OpenAI Docs · Skills](https://learn.chatgpt.com/docs/build-skills).

### 21 — How you ask to use a skill

**Definition / framing:** Install or make the skill available to your harness, then invoke it in your request. Invocation syntax and automatic selection depend on the application and the skill’s configuration.

**Visual form:** artifact and explanation

Examples for an installed grill-me skill

```
Claude Code:
/grill-me

Codex CLI / IDE:
$grill-me

Then describe the idea to discuss.
```

A useful first-use check

- Confirm the intended skill was found.
- Read its instructions so you know what to expect.
- Provide the project or question it needs.
- Some skills require explicit invocation.

**Teaching notes:** These invocation examples are supported by the current Claude Code and official OpenAI Docs skill guidance. We do not install or execute a skill here. A generic model-invoked skill may also be selected by the agent, but Matt’s user-invoked wrappers deliberately require a user request in supporting harnesses.

Source: [OpenAI Docs · Skills](https://learn.chatgpt.com/docs/build-skills).

### 22 — What else can be in a skill folder?

**Definition / framing:** A skill can link to reference documents, executable helpers, and assets. These are optional; an instruction-only skill can be useful on its own.

**Visual form:** annotated folder

Illustrative package

```
my-skill/
├── SKILL.md
├── references/
│   └── checklist.md
├── scripts/
│   └── check_inputs.py
└── assets/
    └── report-template.html
```

Instructions

SKILL.md can be useful on its own.

Supporting material

References explain; assets supply reusable material.

Executable helpers

Scripts act only when run with tools. A skill does not bypass permissions.

**Teaching notes:** The directory tree is an illustrative package, not a new skill or file hierarchy created in this course. Distinguish an instruction file from executable code and from a template. Script execution can have side effects; read what it does and rely on the harness’s controls.

Source: [Claude Code · Skills](https://code.claude.com/docs/en/skills).

### 23 — What is an agent harness?

**Definition / framing:** A harness is the software around the model that manages the conversation, supplies tools, runs permitted actions, and returns their results to continue the agent loop.

**Visual form:** harness boundary

Harness · software managing the agent session

Context

Instructions + conversation

 → Model

Generate text + tool requests

 → Tools

Execute permitted actions

←   Returned results become context for the next model request

Around the model, the harness manages sessions, permissions, continuation, and stopping. Claude Code and Codex CLI are examples.

**Teaching notes:** The term describes a practical software role, not one universal product architecture. Harnesses may include their own terminal or editor interface. The underlying model generates text/tool requests; the surrounding runtime connects those requests to the environment.

Source: [Claude Code · How it works](https://code.claude.com/docs/en/how-claude-code-works).

### 24 — Models, harnesses, and T3 Code

**Definition / framing:** These names refer to different layers. Claude Code and Codex CLI are coding-agent harness examples; T3 Code describes itself as a control surface for supported agent harnesses.

**Visual form:** layer stack

**Control surface** T3 Code: organise projects, threads, agents, and review views.

**Harness** Claude Code or Codex CLI: manage the session and permitted actions.

**Model** The configured language model: generate text and tool requests.

These are different layers. T3 Code describes itself as a control surface for supported agent harnesses.

**Teaching notes:** T3 Code’s own README uses agent harness control surface and lists supported installed agents. Do not describe T3 as a third underlying model or assume it provides credentials/models by itself. Product boundaries can overlap; this conceptual table explains responsibilities rather than exhaustive internals.

Source: [T3 Code · Documentation](https://github.com/pingdotgg/t3code).

### 25 — T3 Code: start a working session

**Definition / framing:** T3 Code brings a project and its agent conversations into one interface. The connected agent system provides the model and tools used to work on the files.

**Visual form:** session sequence

Repository

Choose the intended folder

 → Agent

Choose a configured agent

 → Conversation

Describe a bounded task

An example first request

“Inspect the sequence-validation cell in this notebook. Explain its rules and source location before proposing changes.”

Conceptual session map, not a screenshot. Confirm the working folder and constraints before the agent acts.

**Teaching notes:** This is the first of three dedicated T3 Code slides. It uses practical workflow descriptions rather than fabricated screenshots or provider-specific setup promises. Existing installation and configuration are prerequisites to demonstrating a live session.

Source: [T3 Code · Documentation](https://github.com/pingdotgg/t3code).

### 26 — T3 Code: project, thread, and worktree

**Definition / framing:** These organise different things: a project identifies the codebase, a thread holds a task’s conversation, and a worktree provides a separate Git working directory.

**Visual form:** project structure

Project · the repository

Thread A

Conversation about input checks

Worktree A

Separate working directory

Thread B

Conversation about documentation

Worktree B

Separate working directory

Conceptual example: a thread can use a separate worktree when isolation is needed. A new thread alone does not create a separate checkout; check the actual working directory.

**Teaching notes:** This is T3 slide two of three. A new thread alone does not isolate files. A branch is not a runtime sandbox, and separate context does not guarantee separate working directories. Use worktrees only when they help the actual task.

Source: [T3 Code · Documentation](https://github.com/pingdotgg/t3code).

### 27 — T3 Code: inspect the work produced

**Definition / framing:** Use the workspace to inspect changed files and test actual behaviour. A completion message is the agent’s report; accepting the change requires evidence about the result.

**Visual form:** review workbench

Read the actual changes

```
- split individual samples
+ split by patient identity
+ check patient overlap
```

Conceptual diff; inspect real code and new untracked files.

Scope

Only the relevant files and behaviour?

Checks

What ran, and what did it return?

Behaviour

Can you reproduce the claimed result?

**Teaching notes:** This is the third dedicated T3 Code slide. Explain that permission settings govern actions, not scientific correctness. A diff, a successful command, and a generated plot each provide different evidence. No source-control command or commit is executed by these slides.

Source: [T3 Code · Documentation](https://github.com/pingdotgg/t3code).

### 28 — From an idea to checked work

**Section transition.** Which decisions and evidence connect the steps?

Matt’s skills provide a practical example: clarify the need, capture the agreement, implement a bounded change, then review and learn.

**Teaching notes:** Transition: Which decisions and evidence connect the steps? Pause to connect the preceding concept to the next section. The illustration is a conceptual diagram, not a screenshot or scientific result.

Source: [Matt Pocock · grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md).

### 29 — Matt’s grill-me: clarify an idea

**Definition / framing:** Grill-me uses an interview to turn an unclear intention into explicit decisions. It is useful when you know what you want to achieve but have not worked through the details.

**Visual form:** interview story

Researcher

“I want a colleague to use my analysis.”

grill-me

Who is the user? What useful outcome do they need? Which decisions are still open?

Shared understanding

An explicit user, outcome, and small first step — before choosing what to build.

**Teaching notes:** Refer back to the actual SKILL.md and shared grilling instructions already shown. The skill recommends answers; the user decides. It should not silently turn a suggested feature into an agreed requirement. This is a generic teaching example, not a prewritten live-demo brief.

Source: [Matt Pocock · grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md).

### 30 — Choose the skill by where the answers are

**Definition / framing:** Different uncertainties need different ways of finding answers. Choose the starting point that fits what is missing, rather than running every skill in sequence.

**Visual form:** explanatory comparison

| The answers are in… | Reach for |
| --- | --- |
| Your own head, unsharpened | grill-me |
| The codebase | grill-with-docs |
| Someone else’s head | to-questionnaire |
| Nobody’s head yet, the question needs something to react to | prototype |

**Teaching notes:** The routing table is the instructor’s supplied wording. Ask the user to clarify a goal, inspect code to learn what exists, ask another person for their needs, or prototype when a decision needs something concrete to react to. These are alternatives, not mandatory preliminary stages.

Source: [AI Hero · Skills](https://www.aihero.dev/skills).

### 31 — Matt’s Main Flow: idea to checked work

**Definition / framing:** This sequence connects familiar engineering habits. Each step produces something the next step can use; use only as much process as the task needs.

**Visual form:** artifact journey

01grill-with-docs

Agreed facts + decisions

→
02to-spec

Reviewable agreement

→
03to-tickets

Bounded work + dependencies

↙
04implement

Code + executed checks

→
05code-review

Findings to address

→
06retro

Proposed improvements

→

Each step leaves something the next step can use. Return to clarification when a decision changes, and use only as much process as the task needs.

**Teaching notes:** The full Main Flow is shown here before six individual skill slides. This teaches the flow; it does not invoke it on the presentation or mandate every command during the demo. Different installed versions may have setup and publishing requirements; inspect the actual instructions before use.

Source: [AI Hero · Skills](https://www.aihero.dev/skills).

### 32 — grill-with-docs: understand the project

**Definition / framing:** This skill combines clarification with reading the codebase and recording shared terminology and decisions. It helps prevent guesses about what already exists or what the project’s terms mean.

**Visual form:** discovery board

Read the project

Find the existing check

Where is validation performed?

Clarify the meaning

What does “valid sequence” mean here?

Record what is agreed

Capture shared terms in a glossary and meaningful decisions in project notes.

Actual wrapper instruction

```
Call the Skill tool twice, for
"grilling" and "domain-modeling".
```

**Teaching notes:** The sentence is from Matt’s actual grill-with-docs wrapper, wrapped onto two lines for display. It loads the shared grilling and domain-modeling skills. Inspect facts in the repository rather than asking the user to guess them. No project glossary or ADR is created by this teaching slide.

Source: [Matt Pocock · grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md).

### 33 — to-spec: write down the agreement

**Definition / framing:** A specification describes the behaviour already agreed in the conversation. Matt’s to-spec synthesises those decisions so implementation and review share the same reference.

**Visual form:** spec artifact

A small specification · teaching example

DNA sequence validation

**Accept** Non-empty, uppercase A/C/G/T.

**Reject** Empty input or other symbols.

**Return** True or False for a sequence string.

**Verify** Valid, empty, and invalid cases.

Capture the agreement

to-spec synthesises decisions already made in the conversation. Make the scope and edge cases explicit so implementation and review use the same reference.

**Teaching notes:** This specification is an independent teaching example, not an Exercise 10 plan or a new course exercise. Clarify policy first; for instance, lowercase and ambiguous bases might need different rules in a real analysis. The current to-spec description synthesises an existing conversation. Its installed version may publish to a configured tracker; explain the destination before invoking it.

Source: [Matt Pocock · Skills](https://github.com/mattpocock/skills).

### 34 — to-tickets: make a checkable increment

**Definition / framing:** A ticket is a bounded piece of work with an observable result. Good tickets connect inputs, user-visible behaviour, and a way to check completion; dependencies make the order clear.

**Visual form:** ticket artifact

Ticket · depends on agreed validation policy

Add sequence validation

Input

One sequence string

Output

True or False, per the spec

Acceptance

Valid, empty, and invalid-symbol examples

This is one complete, checkable increment. It can be implemented and exercised on its own, rather than becoming a disconnected list of coding chores.

**Teaching notes:** This is a complete first increment under the teaching specification, not a prescription for the live demo. Matt’s to-tickets supports explicit blocking relationships and destinations such as local files or an issue tracker; those depend on configuration.

Source: [Matt Pocock · Skills](https://github.com/mattpocock/skills).

### 35 — implement: build and verify the behaviour

**Definition / framing:** Implementation turns the agreed task into code, runs appropriate checks, and uses their results to guide changes. Keep the work small enough to understand and review.

**Visual form:** artifact and explanation

Runnable Python · teaching example

```
def is_dna(sequence):
    if not sequence:
        return False
    return set(sequence) <= set("ACGT")

assert is_dna("ACGT")
assert not is_dna("")
assert not is_dna("ACNX")
```

What the checks establish

- An uppercase A/C/G/T string is accepted.
- Empty input is rejected.
- Unsupported symbols are rejected.
- These checks support this small specification, not every possible input type.

**Teaching notes:** The Python is a deliberately small independent example shown in the lecture, not a change to a notebook. The initial if statement rejects empty input and the set comparison checks allowed symbols. Inputs are specified as strings. Appropriate checks matter more than a claim that implementation is complete. Matt’s implement uses its configured TDD and review workflow; do not imply these three assertions alone cover every requirement in a real project.

Source: [Matt Pocock · Skills](https://github.com/mattpocock/skills).

### 36 — code-review: check two different questions

**Definition / framing:** Matt’s review skill separates conformance to project standards from conformance to the specification. It can delegate these two reviews to separate subagents and aggregate their findings.

**Visual form:** review lenses

Lens 01 · Standards

How was it written?

Compare with the documented project rules. Here: keep Python simple, explicit, and easy to teach.

Lens 02 · Specification

Did it meet the agreement?

Check the agreed acceptance and rejection cases. Identify missing requirements and unwanted behaviour.

Matt’s skill can delegate the lenses to separate subagents. Choose a fixed Git comparison point and inspect new files too; ask for findings tied to code and requirements.

**Teaching notes:** The standards example is grounded in AGENTS.md. Matt’s code-review operates from a fixed Git comparison point and a spec source. The current lecture HTML is untracked, so do not pretend a normal diff-based review covered it. Independent agent opinions are not proof; inspect source evidence and run relevant checks.

Source: [Matt Pocock · Skills](https://github.com/mattpocock/skills).

### 37 — retro: improve the next session

**Definition / framing:** A retrospective examines what actually happened and proposes improvements to the agent’s working environment, instructions, checks, or tooling. Useful changes address observed friction.

**Visual form:** retro causal chain

Observed friction

We repeatedly clarified whether empty input was valid.

 → Proposed improvement

Record alphabet, case, empty-input, and output policies before coding.

 → Next session

Review the proposal before adding it to project guidance.

A retrospective uses what actually happened to improve instructions, checks, or tools. A concrete observed problem gives the proposal a reason.

**Teaching notes:** This is a hypothetical observation illustrating the method, not a claim about the actual live demo. Matt’s retro suggests environment/process improvements after a session. Keep the recommendation tied to evidence; avoid accumulating rules for problems that never occurred.

Source: [Matt Pocock · Skills](https://github.com/mattpocock/skills).

### 38 — Scientific judgement still matters

**Section transition.** What would make the analysis answer our question?

A hypothetical dataset with repeated samples per patient connects the workflow to evaluation design, evidence, and reproducibility.

**Teaching notes:** Transition: What would make the analysis answer our question? Pause to connect the preceding concept to the next section. The illustration is a conceptual diagram, not a screenshot or scientific result.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 39 — Define the scientific question first

**Definition / framing:** A useful request explains the population, the outcome, and what you want to learn. These choices determine whether the code will answer the scientific question.

**Visual form:** scientific question

Hypothetical gene-expression study

[Illustration: One patient]

One patient → several samples

What do we want to predict?

The condition of patients the model has never seen. New samples from a familiar patient answer a different question. Ask the agent to inspect patient links and the current split before changing code.

**Teaching notes:** Introduce this as a hypothetical worked example, independent of the live demonstration. No patient data or model results are supplied. Ask students to identify the unit of generalisation: a patient, not simply a row. Connect this scientific brief to the earlier to-spec slide. The researcher establishes the purpose; an LLM can help express and implement it.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 40 — Give the assistant relevant evidence

**Definition / framing:** The assistant needs enough information to understand the data and existing analysis. A short schema, relevant code, and representative inputs are often more useful than an entire dataset.

**Visual form:** schema and matrix

Illustrative sample metadata

| sample_id | patient_id | condition |
| --- | --- | --- |
| S01 | P01 | case |
| S02 | P01 | case |
| S03 | P02 | control |

Each row is a sample; patients can repeat.

↔sample_id

Expression matrix · schematic

Sample identities must align across inputs.

Supply the join code, split code, column meanings, and representative inputs. Ask for file or cell references and missing information; the whole dataset is rarely the best starting context.

**Teaching notes:** The three rows are invented metadata, not clinical data or an actual course dataset. They illustrate grouping only and are far too small for modelling. Include the expression-matrix orientation and the mapping between rows and sample identifiers when working with real files. Giving an agent a folder does not put every file into context. Keep examples appropriate for the computing environment and use an illustrative schema when raw data are unnecessary.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 41 — Resolve analysis choices before coding

**Definition / framing:** When a request leaves a scientific choice open, an assistant may fill in the gap. Ask it to surface assumptions so you can agree on the analysis before those choices become code.

**Visual form:** decision gates

Partition

Will every sample from a patient stay together?

Data policy

How are missing measurements and unknown labels handled?

Evaluation

Which metric and model-selection procedure match the question?

Ask: “List unresolved choices, explain their effects, and recommend an approach. Wait for agreement on choices that change the analysis.” Keep held-out test data out of model selection.

**Teaching notes:** Connect this to grill-me for a decision in the researcher’s head and grill-with-docs for facts in the codebase. Not every technical detail needs a meeting; the point is to expose decisions that affect the scientific interpretation. A held-out test set is for final evaluation after choices are made using training data and appropriate validation. Do not claim that invoking a skill guarantees a sound study design.

Source: [scikit-learn · Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html).

### 42 — Make one change you can inspect

**Definition / framing:** A small complete change is easier to understand, check, and reverse. State the behaviour you want, the files or cells in scope, and how you will recognise completion.

**Visual form:** scope boundary

This increment · inspect and verify together

Split logic

Keep all samples from each patient in one partition.

 → Overlap check

Derive patient IDs from the actual split and check separation.

Preserve in this change

The existing model and evaluation metric. Show the affected cells before expanding the scope.

Read the changed code, run the relevant cells, and inspect the partition summary. Save an understood change in version control before beginning another increment.

**Teaching notes:** The request is a teaching example, not a prepared plan for Exercise 10. A complete increment might include both the split and its verification, but need not refactor the notebook, tune the model, and build an interface at once. Existing notebook state can conceal dependencies: rerun from a clean kernel when checking the completed analysis. The instructor’s repository policy still requires explicit permission before this assistant commits anything.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 43 — Check what your evaluation measures

**Definition / framing:** A program can run without errors while its evaluation answers the wrong question. The way you partition observations must match the kind of future prediction you want to assess.

**Visual form:** patient split

Sample split · patient overlap

**Training** P01 · S01P02 · S03
**Test** P01 · S02P03 · S05

P01 appears on both sides. The score cannot establish performance on entirely unseen patients.

Group split · patients kept together

**Training** P01 · S01P01 · S02
**Test** P02 · S03P03 · S05

Each patient stays in one partition. Use patient groups in validation as well.

Illustrative IDs only. Patient separation addresses overlap; preprocessing, batches, and other leakage need separate checks. Fit learned preprocessing on training data, within each validation fold.

**Teaching notes:** This is a possible failure mechanism, not a claim that a particular model memorised identities or achieved a particular score. The correct split depends on the intended use. If deployment involves new sites, dates, or batches, further separation may be needed. Learned preprocessing must be fitted using training data only, including within each validation fold. Group-aware splitting does not guarantee balanced classes or representative test data. The scikit-learn grouped-data example explicitly discusses multiple samples per patient.

Source: [scikit-learn · Grouped validation](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).

### 44 — Use examples with known answers

**Definition / framing:** A check is useful when you can say in advance what should happen and why. Small examples help expose a mistake that a plausible explanation or a high performance score can hide.

**Visual form:** known answer

Illustrative example · this assertion must fail

```
train_patients = {"P01", "P02"}
test_patients = {"P02", "P03"}

assert train_patients.isdisjoint(
    test_patients
)
```

Expected outcome · reasoned from the inputs

P01**P02** P03
P02 is in both sets. Replacing the test set with {"P03", "P04"} makes the sets disjoint.

For the real analysis, derive IDs from the actual partition metadata. A passing overlap check does not validate the whole analysis.

**Teaching notes:** Explain that isdisjoint returns True only when two sets have no shared members. This deliberately failing example is displayed as such; it is not a claimed passing check. Compare it with test_patients = {"P03", "P04"}, which should pass. Both outcomes are verified outside the course notebooks. Other scientific checks may include sample alignment, units, class counts, and preprocessing fitted on training data only.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 45 — Ask for evidence of completed work

**Definition / framing:** An agent’s completion message summarises its work. To decide whether the result is acceptable, inspect the changes and the observations that support its claims.

**Visual form:** evidence tray

Changed files

Read the actual code, including new files outside the normal diff.

Executed checks

Inspect the commands or cells and their returned results.

Limits

Ask what was not checked and which assumptions remain open.

Ask for the changed split logic, patient-overlap check, actual outputs, and unresolved scientific choices. A second LLM’s agreement still needs supporting evidence.

**Teaching notes:** No run output or passing analysis is invented here. Refer back to the agent tool-call slide: requesting an action, receiving its result, and summarising it are different events. A code-review skill can help find issues, but independent reviewers can share an assumption. Compare the diff with the agreed request, run relevant checks yourself, and assess whether their results support the claim.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 46 — Record how the result was produced

**Definition / framing:** A reproducible analysis has a recoverable path from identified inputs to outputs. Someone should be able to run the saved code without reconstructing your chat or your notebook’s hidden state.

**Visual form:** reproducibility path

Identified inputs

Data version + saved patient split

 → Recorded recipe

Code, packages, config, seeds

 → Clean rerun

Restart → run in order → inspect outputs

Save the command or cell order and the produced outputs. Another researcher should not need to reconstruct your chat or hidden notebook state.

Investigate missing dependencies or unexpected differences. A random seed helps; it does not guarantee identical results across every machine.

**Teaching notes:** Distinguish reproducibility of the analysis from reproducing the exact LLM conversation. Preserve the accepted code and methodological decisions. Fixed seeds alone do not cover changes in data, library versions, hardware, nondeterministic operations, or repeated notebook state. Saving actual patient split assignments can be more robust than assuming a seed recreates them after data ordering changes. Do not ask the agent to expose raw patient identifiers in a public report.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 47 — Keep decisions with the analysis

**Definition / framing:** Code shows what was implemented, but may not explain why it was chosen. Record important methodological decisions in the project so a future reader or agent can recover the reasoning.

**Visual form:** artifact and explanation

Illustrative methods note

```
Question: predict for unseen patients.
Grouping: patient_id.
Rule: no patient crosses partitions.
Preprocessing: fit on training only.
Metric: balanced accuracy.
Reason: equal weight per class recall.
Rationale: repeated patient samples
may share patient-specific patterns.
```

Use a short project record

Balanced accuracy averages recall across classes. Keep the question, assumptions, and reasons beside the code in a README or methods note. Update this record when a decision changes, and ask a new agent session to read it before continuing.

**Teaching notes:** The metric and rationale are illustrative agreed choices, not a universal recommendation. Balanced accuracy averages recall across classes; choose a metric that matches the scientific goal and state whether performance is summarised per sample or per patient. Record the actual validation strategy as well. A chat log can be useful history but is difficult to treat as the current agreement. Connect this slide to context management, to-spec, and retro. No scientific methods file is created by this teaching example.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 48 — Explain why you trust the analysis

**Definition / framing:** Using an assistant well includes understanding the decisions that support the result. You should be able to explain the analysis, reproduce its behaviour, and describe what the checks establish.

**Visual form:** discussion close

Discussion · before we open Exercise 10

The agent reports better accuracy.
What would you inspect?

Question

Does the evaluation match the intended patients?

Evidence

Which code and run results support the claim?

Uncertainty

What remains unchecked?

Ask the assistant to explain unfamiliar code with small examples. You should be able to explain the accepted analysis and justify its decisions.

**Teaching notes:** Close the practical section with a short discussion: if an agent reports improved accuracy after a split change, what would you inspect before accepting the claim? Useful answers include the split definition, patient overlap, class composition, preprocessing, metric, and actual run evidence. These are prompts for discussion, not a scripted live demonstration. Students need not memorise syntax; the goal is an explainable workflow and informed scientific judgement.

Source: [Worked example · scientific coding](BioIT_AI_Eng_story.md).

### 49 — Live Demo on Exercise 10

**Teaching notes:** Develop Exercise 10 live. No specification, interface plan, features, or completed application are included in these slides.

## Source and example distinctions

- Slides 39–48 use a hypothetical patient-grouped analysis. The schema, prompts,
  and methods note are illustrative; no course analysis is implemented. The
  grouped-splitting and leakage explanations are supported by the linked
  scikit-learn documentation. The intentionally overlapping patient sets fail
  the displayed check; a disjoint comparison passes. Both outcomes were checked.

- The complete `grill-me/SKILL.md` and excerpts from `grilling/SKILL.md` come from
  the corrected **mattpocock/skills** repository. Excerpts are labelled; they are
  not presented as a complete procedure. Check installed versions for changes.
- The sequence assertion on slide 04 comes from `exercise_2.ipynb`. The system
  and user prompts surrounding it are authored teaching examples.
- `AGENTS.md` supplies the concrete read-file example and the teaching-code rule.
- The Claude Code subagent YAML is illustrative. It is not a configured agent
  added to the repository. Exact fields and controls differ between harnesses.
- The optional skill-folder layout illustrates the convention; it is not claimed
  to be the folder structure of Matt's small `grill-me` wrapper.
- The DNA specification, ticket, Python function, and retrospective observation
  are independent teaching examples. They are not Exercise 10 requirements or
  an additional course exercise. The displayed Python assertions were executed.
- Token boundaries and next-token continuation are explicitly illustrative.
  The button makes no model call and displays no invented probabilities.
- Claude Code and Codex CLI are harness examples. T3 Code describes itself as an
  **agent harness control surface**, rather than an underlying language model.
- An earlier Antigravity critique concerned an older version of the deck; it is
  not validation of this instructional revision.

## Delivery and verification

`BioIT_AI_Eng.html` is a single offline file with embedded fonts, CSS, JavaScript,
and speaker notes. Its 1920 × 1080 stage scales uniformly to desktop and phones.

Use arrows or Space to advance, Home/End to jump, the picker to select a slide,
and N / Notes for speaker notes. E enables text editing; Escape finishes editing.
Ctrl/Cmd+S downloads an edited HTML copy. Browser autosave uses a new version key
so edits from the older slide order are not restored into this one.

The revised 49-slide deck was checked in local Chrome at 1280 × 720 and
390 × 844. Checks cover stage fit, content overflow, panel overlap, offline use,
navigation, notes, the token illustration, text editing/autosave, HTML export
and reopening, and the exact text of the Exercise 10 slide. Rendered screenshots of all slides were also visually inspected. The original-slide critique and final-number mapping are stored in `.frontend-slides/`. T3's separate HTML preview checker is unavailable because of
the host's AppArmor sandbox configuration; this does not affect the standalone
HTML or the local Chrome checks.

No notebooks or exercise applications were changed. No commit, push, deployment,
or skill installation was performed.
