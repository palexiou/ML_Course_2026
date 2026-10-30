# Four-day machine learning for bioinformatics course

Status: ready-for-agent

## Problem Statement

The instructor needs a coherent, classroom-ready course for approximately 10-15 master's students in bioinformatics, taught alone over four consecutive Monday-Thursday sessions of three hours each. Students are comfortable with Python, pandas, NumPy, and independent programming, but their statistics and ML knowledge is uncertain and expected to be limited.

An initial chat and HTML outline establish a promising narrative, but they are not a verified teaching package. The instructor needs executable scaffolded practicals, controlled scientific examples, an achievable timetable, slides, completed notebooks, and demonstration contingencies. Everything required must happen during contact time, including access checks and setup. There is compulsory attendance but no homework, exam, grades, or required submissions.

The central risk is producing a model survey that runs out of time or equates more sophisticated models with better science. Students must instead understand how representation choices affect what models can learn, apply valid experimental design, and scientifically audit both manual and agent-assisted analyses.

## Solution

Build an English-language, in-person course around one simulated DNA sequence-classification problem with controlled dataset variants and known ground truth. Motivate the task with promoter prediction while explicitly identifying the simulation as a simplified teaching example, not evidence of real promoter recognition.

Use four connected stages: handcraft k-mer features and evaluate classical models; learn features from one-hot sequences with a small CNN; reuse frozen pretrained DNA embeddings; then specify, delegate, and scientifically audit an agent-assisted workflow. Compare representations rather than promise a model ranking. Include a separate deliberately flawed split-leakage exercise.

Provide scaffolded notebooks and separate completed notebooks, the course dataset and generation code, course slides, a one-page scientific-audit checklist, and instructor guidance including timings and demonstration contingencies. Prefer Colab, with required practicals designed for Colab or a simple laptop and no student-owned GPU requirement. Student coding-agent access is optional; observation remains a complete participation mode. Close with a 20-minute instructor-led Agentomics demonstration and 10-minute discussion.

Before expanding teaching materials, verify the simulated examples, model behavior, dependency choices, execution costs, and Colab workflow. Validate the completed package through an end-to-end course rehearsal, the primary validation seam approved by the instructor.

## User Stories

1. As an instructor, I want four connected sessions, so that students build one coherent understanding rather than attend unrelated model tutorials.
2. As an instructor, I want each session to fit three hours including breaks, so that the course is deliverable within its allocated contact time.
3. As an instructor teaching alone, I want self-contained practical instructions, so that I can support 10-15 students without relying on teaching assistants.
4. As a student, I want all teaching and materials in English, so that terminology stays consistent throughout the course.
5. As a student, I want access checks and setup during class, so that participation does not depend on pre-course preparation.
6. As a student, I want no required homework, so that the course's essential outcomes are achievable during contact time.
7. As a student with limited ML knowledge, I want a short conceptual introduction, so that I can follow the practicals without an assumed advanced ML background.
8. As an instructor, I want a brief ungraded diagnostic discussion, so that I can adapt explanations to the cohort's prior knowledge.
9. As a student, I want ungraded questions and discussion, so that I can check my understanding without an exam or submission.
10. As a student, I want working notebooks with selected missing code, so that I can make meaningful changes without implementing an entire pipeline from scratch.
11. As a faster student, I want optional extensions, so that I can explore further without changing the core requirements for everyone.
12. As a student, I want separate completed notebooks, so that I can review the whole workflow after class.
13. As a student, I want a familiar biological motivation, so that the ML problem has a meaningful context.
14. As a student, I want the simulation's limitations stated explicitly, so that I do not confuse a controlled demonstration with real biological discovery.
15. As an instructor, I want reproducible course dataset generation, so that I can regenerate and inspect the scientific teaching examples.
16. As a student, I want a simple-signal dataset variant, so that I can first understand the complete workflow without multiple simultaneous complications.
17. As a student, I want an interaction-signal dataset variant, so that I can investigate how representation choices affect access to predictive information.
18. As an instructor, I want the interaction signal verified with the chosen models, so that the example demonstrates its intended lesson rather than an assumed CNN advantage.
19. As a student, I want methods compared on the same dataset variants, so that differences are not manufactured by giving each method a favorable task.
20. As a student, I want to identify samples, labels, features, and prediction targets, so that I can formulate the ML experiment clearly.
21. As a student, I want a concise map of supervised, unsupervised, and self-supervised learning, so that I can locate the course methods within ML.
22. As a student, I want classification distinguished from regression, so that I understand why this task uses a classifier.
23. As a student, I want to inspect sequences and labels before modeling, so that I can recognize the data underlying a numerical feature matrix.
24. As a student, I want to construct k-mer features, so that I understand the decisions involved in handcrafted representations.
25. As a student, I want a logistic regression baseline, so that a simple model anchors later comparisons.
26. As a student, I want a short explanation of decision trees and random forests with working code, so that I can compare a tree ensemble without spending the session implementing it.
27. As a student, I want clear training, validation, and test roles, so that I can distinguish fitting, model development, and final evaluation.
28. As a student, I want validation-based comparison during experimentation, so that test results do not guide model development.
29. As a student, I want the same split identities across representations for each dataset variant, so that model comparisons answer the same prediction question.
30. As a student, I want interpretable predictions, metrics, and curves, so that I can explain more than a single performance number.
31. As a student, I want to compare feature importance with known simulation truth, so that I can question whether a model used the intended signal.
32. As a student, I want a separate split-leakage investigation, so that I can discover and correct an invalid evaluation.
33. As a student, I want to connect linear prediction to a neuron and an activation, so that neural networks build on ideas I already encountered.
34. As a student, I want to calculate one simple prediction, so that equations connect to executable code.
35. As a student, I want loss and optimization explained without required backpropagation derivations, so that I understand training at the intended mathematical depth.
36. As a student, I want one-hot DNA input, so that I can contrast a sequence representation with handcrafted k-mer features.
37. As a student, I want to train a small CNN, so that I experience representation learning on the course dataset.
38. As a student, I want to inspect responses to controlled sequence changes, so that interpretation is tied to evidence rather than architecture labels.
39. As a student, I want performance, computational cost, and interpretability compared, so that I do not assume a more complex model is universally preferable.
40. As a student, I want attention, pretraining, and embeddings explained conceptually, so that the pretrained workflow is not a black box.
41. As a student, I want a small live embedding extraction, so that I can see how sequence input becomes a reusable numerical representation.
42. As a student, I want cached embeddings for the full practical, so that expensive extraction does not consume the teaching session.
43. As a student, I want a simple classifier on frozen embeddings, so that I can compare transferred features with earlier representations.
44. As a student, I want transfer, domain shift, and pretraining-overlap risks discussed, so that I can qualify conclusions from pretrained models.
45. As a student, I want a planned test comparison after workflows are frozen, so that I can experience final evaluation without tuning against it.
46. As a student, I want LLM context, tools, agents, project instructions, and skills distinguished, so that I understand the components of agent-assisted coding.
47. As a student, I want to inspect an agent's response to a vague scientific question, so that I notice decisions it made without explicit instructions.
48. As a student, I want to compare that response with an explicitly specified workflow, so that I understand the value of scientific constraints.
49. As a student, I want to see project instructions and a relevant skill added, so that I understand their role beyond the initial request.
50. As a student, I want a scientific audit of agent outputs, so that working code is not mistaken for a valid analysis.
51. As a student without coding-agent access, I want to observe and discuss the same demonstration, so that I can achieve the learning outcomes without buying access.
52. As a student with coding-agent access, I want optional opportunities to try selected steps, so that I can apply the demonstrated workflow.
53. As an instructor, I want saved outputs and a short recorded agent run, so that external-service failures do not eliminate the scientific discussion.
54. As a student, I want previous-run outputs identified honestly, so that I can distinguish live execution from demonstration evidence.
55. As a student, I want an Agentomics example connected to the course's decisions, so that workflow automation reinforces rather than replaces the scientific lessons.
56. As an instructor, I want clear scope-reduction priorities, so that delays do not remove evaluation, interpretation, or scientific audit.
57. As a student, I want a one-page scientific-audit checklist, so that I can reuse the course's evaluation principles in later work.
58. As an instructor, I want slides aligned with the actual notebooks and timetable, so that the teaching package has consistent terminology and transitions.
59. As an instructor, I want a fresh-environment rehearsal and actual Colab verification, so that compatibility claims rest on execution rather than assumption.
60. As an instructor, I want execution times and material limitations recorded, so that I can distinguish verified classroom behavior from work still needing validation.

## Implementation Decisions

### Course contract and scope

- Deliver four in-person, English-language sessions on consecutive Monday-Thursday days, each 180 minutes including breaks, for approximately 10-15 master's students with compulsory attendance.
- Assume Python, pandas, NumPy, and independent programming ability, but limited and uneven statistics and ML knowledge. Target understanding, application, and scientific audit rather than independent implementation of every model.
- Require no homework, exam, grades, or submissions. Incorporate ungraded diagnostic questions, prediction questions, and interpretation discussions during class.
- Design for one instructor. Scaffolded practicals use working notebooks, selected missing code, and optional extensions; substantial blank-page implementation is not the default.
- Keep materials usable in Colab or on a simple laptop, with Colab the preferred classroom platform. Do not require students to own a GPU or pay for a coding agent. Verify rather than assume the supported runtime conditions.
- Complete access checks and setup during class; do not require a pre-course access check.

### Course dataset and experimental protocol

- Use simulated DNA sequence classification with planted signals and known ground truth. Promoter prediction is the motivation, not a claim that the simulation reproduces real promoter biology. Preserve the accepted controlled-simulation decision.
- Build controlled dataset variants within the same framing: a simple motif signal, an interaction signal, and a separate split-leakage exercise. Introduce complexity progressively. A misleading-shortcut demonstration is optional, not another required practical.
- Compare methods on the same applicable dataset variants. Deliberately constructed representation demonstrations must disclose their construction and limits; no universal ordering of classical models, CNNs, and pretrained embeddings is required.
- Select the interaction signal and CNN jointly through preliminary experiments. Verify that the chosen representation and architecture actually expose the intended distinction. Do not assume the word CNN guarantees the desired behavior.
- Preserve reproducible sample identities, labels, generation settings, seeds, and relevant related-sequence groups. Supply enough generation information to inspect the known ground truth and reproduce the examples without prescribing a particular storage schema now.
- Define and retain training, validation, and test identities for each dataset variant across representations. Correct workflows keep relevant groups separate and fit learned preprocessing using training data only.
- Use validation results for experimentation. Freeze workflows, selection decisions, and any decision thresholds before the planned Day 3 test comparison. Do not tune against revealed test results, consistent with the accepted protected-test decision.
- Keep the intentionally invalid split-leakage exercise separate from the correct workflow so its data handling and misleading results cannot silently become the comparison baseline.
- Day 4 audits adherence to the same evaluation boundary. Previously revealed test results remain demonstration evidence, not a fresh independent test for newly tuned agent models.
- Specify suitable metrics before evaluating models. Cover prediction-level interpretation, confusion matrices, ROC and precision-recall views, and the consequences of class balance; finalize the primary comparison metric during technical verification rather than inventing an unagreed metric policy here.

### Daily teaching structure

- Day 1 reserves minutes 0-10 for Colab access and notebook startup. Minutes 10-50 combine the short diagnostic, simulated promoter motivation, a concise ML map, sequence inspection, and k-mer features. After a 10-minute break, minutes 60-100 establish the split protocol and logistic regression. After another 10-minute break, minutes 110-150 introduce trees and random forests and compare validation results and feature importance. Minutes 150-180 cover the separate leakage investigation, discussion, recap, and buffer.
- Day 2 uses minutes 0-10 for recap; 10-50 for linear prediction, neurons, activations, loss, optimization, a simple calculation, and one-hot DNA; 50-60 for a break; 60-100 for convolution, pooling, and a small CNN practical; 100-110 for a break; 110-150 for the interaction comparison and controlled sequence changes; and 150-180 for interpretation, questions, and buffer.
- Day 3 uses minutes 0-10 for recap; 10-50 for attention, pretraining, embeddings, and frozen versus fine-tuned representations; 50-60 for a break; 60-100 for small live extraction and full-data cached-embedding classification; 100-110 for a break; 110-150 for validation comparisons, costs, transfer risks, and freezing workflows; and 150-180 for the planned test comparison, synthesis, and buffer.
- Day 4 uses minutes 0-10 for recap; 10-50 for LLM fundamentals, agent components, a vague request, and inspection of silent decisions; 50-60 for a break; 60-100 for the explicit specification, project instructions, a relevant skill, and clean-run comparison; 100-110 for a break; 110-150 for scientific audit; 150-170 for the instructor-led Agentomics demonstration; and 170-180 for final discussion.
- Treat timings as a teaching envelope, not evidence that execution already fits. If delays occur, shorten architecture explanations and optional experiments before removing evaluation, student interpretation, the leakage investigation, or scientific discussion. Provide working random forest code rather than requiring its implementation.

### Notebooks, demonstrations, and teaching artifacts

- Deliver scaffolded notebooks and distinct completed notebooks, the course dataset and generation code, course slides, the one-page scientific-audit checklist, and instructor guidance for transitions, timings, contingencies, and scope reductions.
- Day 1 includes logistic regression and random forest on k-mer features. Day 2 includes a small CNN on one-hot DNA. Day 3 includes a simple classifier on frozen pretrained DNA embeddings. The same experiment framing carries across these workflows.
- Use a few equations connected to code and one simple prediction calculation. Explain backpropagation conceptually; derivations are not required exercises.
- On Day 3, perform a small live embedding extraction, then use cached embeddings for the full comparison. Preserve sample-to-embedding correspondence and model/extraction provenance. Fine-tuning is a conceptual contrast, not a required training practical.
- Day 4 centers on specification and scientific audit, not comprehensive agent operation. Contrast a vague question with an explicit specification, project instructions, and a relevant scientific skill. Use clean demonstration runs so prior prompts and results do not silently explain the comparison.
- Allow optional student agent participation when access exists. Ensure the observation route includes the same decisions, outputs, and audit questions; no student-run Agentomics workflow is required.
- Prepare saved outputs for expensive or external-service steps and a short recorded agent run. Clearly label previous-run evidence. Saved outputs preserve interpretation and discussion when execution fails; they do not count as successful live execution or verified compatibility.
- Make the Agentomics demonstration connect back to split integrity, experimentation, reproducibility, and scientific audit. Do not introduce another required platform for students to learn.
- Use the existing HTML as an outline and source of narrative, not as an authoritative specification. Expand and align the slides only after the technical examples have been verified. Use the installed frontend-slides workflow when producing the HTML presentation; the final visual direction is not selected by this spec.

### Technical verification before material expansion

- Verify generation settings, dataset size and sequence length, interaction construction, CNN architecture, dependency versions, pretrained model access and licensing conditions, tokenization, embedding extraction, and runtime requirements before claiming classroom readiness.
- Resolve routine implementation details through small, reproducible experiments. Do not silently change the agreed task, learning outcomes, protected-test policy, participation requirements, or contact-time budget to accommodate a preferred technology.
- Establish development examples for technical calibration without adapting course models to the final course test results. Record the selected configuration and reproducible provenance.
- Report genuine capability or access blockers promptly. If a required live step cannot meet the agreed constraints, request a scope decision rather than silently replacing it with saved results and declaring validation complete.

## Testing Decisions

### Primary seam and prior art

- The instructor approved one primary seam: an end-to-end course rehearsal through the delivered notebooks and teaching materials. Validate public inputs, outputs, student tasks, and instructor-visible behavior rather than internal function structure.
- The repository currently contains planning documents, terminology, decisions, and tracker configuration; there is no existing application or executable test suite to extend. The accepted timetable and two domain decisions provide acceptance criteria, not prior executable coverage.
- Test the course dataset generator, representation/model workflows, comparison outputs, scientific-audit activity, and presentation through this rehearsal. Add lower-level checks only where they materially protect a scientific invariant or diagnose a failure; do not prescribe a speculative testing framework.

### Rehearsal acceptance criteria

- Execute completed notebooks in order from a fresh supported environment with documented dependency setup and no pre-existing hidden variables or unrecorded files. Clearly distinguish intentional exercise placeholders in student notebooks from errors in completed notebooks.
- Check that student exercises have matching completed answers and that the observation route for Day 4 exposes the necessary materials without requiring agent credentials.
- Verify actual Colab execution. A local run may establish laptop behavior but must not be reported as Colab validation. Record the actual runtime, accelerator use if any, dependency setup, extraction/training time, and limits observed.
- Record measured execution times against each teaching block, leaving time for explanations and student work. If setup or required computation does not fit, revise within the agreed scope or report the required decision; do not declare the timetable validated based only on its arithmetic.
- Regenerate the course dataset and verify identities, labels, intended signal, related-sequence groups, and known ground truth. Verify the intended representation experiment across documented seeds or repeated runs sufficient to distinguish the intended lesson from an accidental result; choose justified tolerances during verification, not arbitrary score guarantees.
- Check sample identity and split consistency across k-mer, one-hot, and embedding workflows, including cached embedding row alignment. Correct workflows must not reuse training groups as validation/test groups or fit learned preprocessing on evaluation data.
- Verify that experimentation uses validation results and that the planned test comparison consumes frozen workflows. Inspect notebook outputs and execution order to confirm that earlier sessions do not disclose development-guiding test results.
- Demonstrate the leakage exercise through observable related-sequence overlap in the flawed split and its absence after correction. Explain the measured performance effect without guaranteeing a particular numerical drop. Any intended scientific lesson must be supported by the actual run.
- Compare metrics, predictions, and controlled sequence responses against independently justified simulation expectations. Do not test merely that one model beats another or that the code prints a desired conclusion.
- Verify small live embedding extraction against the recorded extraction configuration and confirm that cached full-data embeddings have the matching provenance. If live extraction is not verified, mark that requirement unverified even when cached classification succeeds.
- Rehearse the vague-request and specified-request agent demonstrations and audit their actual outputs. Do not require every stochastic live run to reproduce the same failure; use clearly identified saved or recorded evidence when necessary for a reliable discussion.
- Exercise the saved-output contingency path separately from successful live execution. Confirm that outputs are available, correspond to the documented experiment, and support the planned audit and interpretation questions.
- Scientifically audit engineering success, split integrity, metric selection, baseline comparison, reproducibility, and interpretation against known simulation truth. Previously revealed test results must not be portrayed as independent evidence for post-reveal tuning.
- Render the slides in a browser and visually inspect content, equations, labels, readability, navigation, and overflow. Verify agreement with the notebook terminology, approved sequence, breaks, and final Agentomics allocation. Inspect the one-page checklist for both content coverage and readable layout.
- Deliver a concise rehearsal record distinguishing checks passed, failed, not run, and blocked. Course readiness requires the required checks, not merely the existence of a rehearsal report. Recorded outputs and local-only runs must not conceal missing live or Colab verification.

## Out of Scope

- A standalone Day 4 workshop or an eight-session version of the course.
- Homework, exams, grading, compulsory submissions, or an assumed pre-course setup task.
- Requiring students to implement full pipelines or a CNN from scratch, derive backpropagation, purchase agent access, or own a GPU.
- A chromosome-scanning implementation, a real-data promoter-discovery benchmark, or claims of biological discovery from simulated results.
- A guaranteed ranking in which the CNN or pretrained embeddings must beat classical models.
- Full pretrained-model fine-tuning, comprehensive transformer mathematics, or a broad survey of ML algorithms.
- Mandatory student coding-agent execution, student-run Agentomics, or comprehensive training in a particular agent platform.
- Additional mandatory shortcut/domain-shift practicals beyond the agreed core; these remain optional demonstrations or extensions.
- Production hosting, a web application, custom authentication, a new notebook platform, or an Agentomics integration.
- A mandatory PowerPoint or PDF companion; the agreed slide deliverable is an HTML presentation.
- Selecting a final visual style, exact dataset parameters, a particular pretrained model, or a fixed metric policy without technical verification.
- Claiming the teaching package is implemented or validated merely because this spec is published. This request publishes a spec, not teaching materials or implementation tickets.

## Further Notes

- Implementation handoff update: the instructor subsequently requested standalone Python code to paste into Colab and arrange manually. Agent-operated Colab execution is not a prerequisite for the code handoff; actual Colab verification is an instructor-performed check, recorded separately from local verification. No unrun Colab check may be reported as passed, and no full notebook presentation work is required for the current standalone-code handoff.

- This spec synthesizes the completed course-format interview and the instructor's subsequent approval of the validation seam. No further format interview is required to begin the defined technical verification.
- Preserve the canonical meanings of course dataset, dataset variant, scaffolded practical, and scientific audit. Preserve the accepted decisions on controlled simulated sequence classification and validation-based development with a protected test comparison.
- The original conversation and supplied HTML are design inputs. Later explicit interview decisions take precedence over assumptions or additional deliverables introduced in that outline.
- Technical verification is implementation work still to be done. The ready-for-agent state means this scope is specified and ready to be worked on, not that a pretrained model, runtime, dataset configuration, or classroom execution has already been verified.
- Any implementation work that changes consequential scope, data meaning, compatibility, or participation requirements must return to the instructor for a decision. Routine reversible details should be resolved through the agreed constraints and measured evidence.
