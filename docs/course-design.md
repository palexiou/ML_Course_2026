# Course design

## Confirmed in interview round 1

- Audience: approximately 10-15 master's students in bioinformatics; attendance is compulsory.
- Students are comfortable with pandas, NumPy, and independent Python programming. Prior statistics and ML knowledge is uncertain and expected to be limited.
- Delivery is in person: four three-hour sessions, Monday through Thursday in one week, with breaks inside each session.
- All required learning takes place during contact time. No homework.
- Minimum outcomes: understand, apply, and scientifically audit an ML workflow. Independent implementation from scratch is not a required outcome.
- No grades, formal assessment, or required submissions.
- Preferred student activity: run working notebooks and complete selected missing code. Substantial implementation from scratch is not the default.
- The four-stage backbone is accepted as a starting point, not an immutable syllabus: classical ML, sequence CNNs, pretrained DNA embeddings, then coding agents and scientific audit.
- Day 4 includes LLMs, coding agents, and an instructor-led Agentomics demonstration. Students may try coding agents if they have access; otherwise they may watch.
- A standalone Day 4 workshop is deferred and outside the current scope.
- The core task is sequence classification using simulated DNA with planted motifs and known ground truth, not chromosome scanning. A controlled teaching example takes priority over biological realism.

## Confirmed in interview round 2

- Include a deliberately flawed analysis that students investigate and correct.
- Teach mathematics through a few equations connected to code and a simple prediction calculation; explain backpropagation conceptually rather than requiring derivations.
- Required practicals must run on Colab or a simple laptop, with Colab preferred.
- Agentomics is an instructor-led demonstration, not a required student run.
- Coding-agent access is optional; observing the demonstration must remain a valid participation mode.
- Ungraded questions and discussion during class are welcome. No exam or other formal assessment is required.

## Confirmed in interview round 3

- Model comparisons should teach what each representation exposes or discards, including handcrafted k-mer features versus one-hot sequence input. No universal performance ranking is required.
- A deliberately constructed interaction signal may illustrate differences between representations, provided the resulting lesson is not simply that CNNs are better.
- Multiple simulated datasets are allowed when useful. Their exact relationship and complexity remain undecided.
- Introduce the simulated signal in stages rather than placing every complication in the initial practical.
- Split leakage is the required failure investigation. A misleading shortcut may be an instructor demonstration or extension.
- On Day 3, demonstrate a small live embedding extraction, then use cached embeddings for the full dataset comparison. Fine-tuning is a conceptual contrast, not required training.
- Day 4 centers on specification and scientific audit: vague question, inspect silent decisions, add an explicit specification, add project instructions and a relevant skill, then compare and audit.
- Begin Day 1 with a short ungraded diagnostic discussion and provide optional extensions for faster students. The diagnostic is not an exam or submission.

## Format interview status

The course format is agreed. No format questions remain open. Technical choices must still be verified before expanding teaching materials.

## Confirmed in interview round 4

- Use controlled variants of one sequence-classification problem: simple motif signal, interaction signal, and a split-leakage exercise. Compare methods on the same variants rather than providing each method a favorable dataset.
- Motivate the task with promoter prediction, but explicitly describe the practical as a simplified simulation with known ground truth. It is not evidence of real promoter recognition.
- Use validation results for experimentation. Freeze the compared workflows before a planned test-set comparison on Day 3; do not tune against revealed test results. Day 4 audits the same evaluation boundary.
- Keep the intentionally flawed leakage exercise separate from the correct workflow.
- Days 1-3 use a 180-minute planning envelope: 10-minute opening, three 40-minute mixed teaching blocks, two 10-minute breaks, and 30 minutes for synthesis, questions, and buffer. Adapt Day 4 around the demonstration.
- Reserve the final 30 minutes of Day 4 for a 20-minute Agentomics demonstration and 10-minute final discussion.
- Deliver scaffolded notebooks and separate completed versions, simulated datasets and generation code, a one-page scientific-audit checklist, and course slides. These are reference resources, not required homework.

## Confirmed in interview round 5

- The proposed timed four-day structure is accepted.
- If time runs short, protect evaluation, student interpretation, leakage investigation, and scientific discussion. Shorten model explanations and optional experiments first; provide working random forest code.
- Saved outputs and a short recorded agent run are acceptable demonstration contingencies. Clearly distinguish live execution from inspection of a previous run.
- The instructor teaches alone.
- Teaching and materials are in English.
- Day 2 investigates representation differences without promising a CNN advantage; Day 3 uses frozen embeddings rather than a fine-tuning practical; Day 4 centers on specification and scientific audit.
- Agentomics retains its 20-minute instructor demonstration followed by 10 minutes of final discussion.
- Verify dataset variants, the small CNN, the pretrained model, and Colab execution before expanding the slides. Revise an experiment that does not demonstrate its intended lesson rather than manufacture a result.

## Confirmed in interview round 6

- Perform the Colab access check and setup during class. Do not require a pre-course access check.
- Reserve the opening 10 minutes of Day 1 for access and notebook startup. Move the brief diagnostic discussion into the first teaching block and shorten the introductory ML overview accordingly.

## Implementation handoff update

The instructor requested standalone Python code suitable for manually pasting into Colab and arranging there. Agent-operated Colab sign-in and presentation polishing are not prerequisites for this code handoff. Local execution is verified separately from the instructor's manual Colab check; no local result establishes Colab compatibility.

## Documentation status

Only confirmed choices are recorded as confirmed. Recommendations in interview questions are not accepted decisions. The controlled simulated sequence-classification task is recorded in ADR 0001. The standalone computational workflows, student snippets, completed answers, instructor guide, audit materials, and HTML slide implementation are developed for manual instructor review. See `instructor/verification.md` for actual local execution and pending checks. No actual Colab or full classroom readiness is inferred from implementation.
