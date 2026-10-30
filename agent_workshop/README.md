# Day 4 specification and scientific-audit kit

This is the integrated fourth day of the course, not a separate workshop. The required observation route works from these local text files without an agent account, internet service, or payment. All discussion is ungraded; nothing is submitted.

## Teaching sequence

1. Read [the vague prompt](vague-prompt.md). Predict the decisions an implementation would have to make.
2. Inspect [the manually authored flawed fixture](fixture.md) and its [runnable flawed analysis](flawed_analysis.py). It is deliberately flawed teaching material, **not a real agent transcript, recording, or evidence of agent behavior**.
3. Replace the request with [the precise specification](precise-spec.md).
4. Add [example project instructions](example-project/AGENTS.md) and [the reusable scientific skill](example-project/skills/scientific-audit/SKILL.md). These are teaching examples; they are not installed globally.
5. Compare the proposed repair with [worked audit answers](worked-audit.md), run the [completed audit exercise](../instructor/completed/day4_audit.py), and use the [one-page checklist](../instructor/audit-checklist.html).

The specification defines this experiment. AGENTS supplies persistent project constraints. The skill supplies a reusable audit procedure. Tools execute actions such as reading files and running Python. An agent loop chooses and repeats those actions using its context. None of these guarantees scientific validity.

## Observation route: no account

At 25–50, the instructor projects the fixture; students annotate the unspecified decisions and identify two concrete defects. At 60–100, students read the precise specification, project instructions, and skill, then say what each changes. At 110–150, students compare IDs and groups in the fixture tables, predict the two reported accuracies, complete the checklist, and explain the repairs. The instructor can run both Python files on one laptop or read the tables aloud if execution fails. The tables suffice to compute all answers by hand. Reveal the worked answers only after discussion.

Optional operators with existing agent access may run the precise request on development-only copies during the same time blocks. They must use a clean context and the same evidence questions. No signup or student-run Agentomics workflow is required. Do not send protected test data or private files to an agent service. If a live run succeeds unexpectedly, audit what it actually did; do not force it to reproduce the fixture's errors.

## Actual agent comparison: locally captured

The [October 26 actual runs and parent audit](actual_runs/2026-10-26/README.md) supply genuine code, reports, and logs for both requests. Neither run reproduced the authored fixture errors. Different objectives/features/search prevent a causal prompt-quality comparison. A short screen recording is still pending. For a new classroom run, use two fresh contexts/workspaces initialized with the same development inputs and tool permissions. The vague context receives only the vague prompt. The specified context receives the precise specification, example AGENTS, and scientific skill. Neither receives previous conversation, worked answers, test files, or the other's outputs. Record provider/model/version when available, date, tool versions, input hashes, complete prompts, loaded instructions, runtime, costs if exposed, commands, outputs, errors, and any intervention. Do not claim that the comparison isolates prompting if model/tool conditions differ.

Capture actual silent decisions from the resulting code and artifacts. Save both unedited runs and a short readable recording with sensitive material removed explicitly. Label those as actual previous runs with their dates and provenance. A stochastic comparison does not establish a causal guarantee that adding instructions prevents mistakes. The authored fixture cannot fill the actual-run evidence requirement.

## Evidence ledger

| Material | Status | Permitted use |
| --- | --- | --- |
| Authored fixture and completed audit | Supplied; see local verification record | Deterministic observation and scientific reasoning exercise |
| Vague/specification actual clean agent runs | Locally captured October 26; independently audited | Inspect real code, decisions, predictions, reports, and limitations; not a causal prompt-quality comparison |
| Short recorded agent run | Not supplied; pending instructor | Genuine previous-run contingency once available |
| Agentomics access, example, and recording | Not supplied; pending instructor | Actual instructor-led demonstration once available |
| Actual Colab check | Explicitly deferred to instructor | Record separately from local runs |

The final 30 minutes remain reserved: Agentomics 150–170, final discussion 170–180. Ask the instructor to provide actual access and a demonstration/recording exposing scientific decisions. Until then, the guide supplies a discussion contingency and marks the demonstration pending; it makes no claims about Agentomics capabilities or observed behavior.
