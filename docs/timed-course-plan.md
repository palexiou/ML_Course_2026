# Proposed timed course plan

Status: teaching structure and in-class setup policy accepted. All times are elapsed minutes within a three-hour session. The exact simulation and model configurations remain to be verified experimentally before expanding teaching materials.

## Day 1: Define and evaluate the experiment

| Minutes | Activity |
| --- | --- |
| 0-10 | Check Colab access, open the supplied notebook, and run its startup cell. |
| 10-50 | Brief ungraded diagnostic discussion; motivate the simulated promoter task; introduce a shortened ML map; inspect sequences and labels; construct k-mer features. |
| 50-60 | Break. |
| 60-100 | Establish training, validation, and protected test identities; train logistic regression; interpret validation predictions and metrics. |
| 100-110 | Break. |
| 110-150 | Introduce decision trees and random forests; compare validation results; inspect feature importance against the planted signal. |
| 150-180 | Short separate split-leakage investigation, discussion, recap, and buffer. |

Outcome: students can explain and run the complete classical workflow without consulting test results for development.

## Day 2: Learn the representation

| Minutes | Activity |
| --- | --- |
| 0-10 | Recap: what information did k-mer features expose or discard? |
| 10-50 | Connect linear prediction to neurons, activations, loss, and optimization; calculate one prediction; introduce one-hot DNA. |
| 50-60 | Break. |
| 60-100 | Explain convolution and pooling; complete selected notebook code and train a small CNN on the simple-signal variant. |
| 100-110 | Break. |
| 110-150 | Compare classical models and the CNN on the interaction variant; inspect model responses to controlled sequence changes. |
| 150-180 | Discuss representation, model behavior, cost, and limits of interpretation; questions and buffer. |

Outcome: students can distinguish handcrafted from learned representations without inferring a universal model ranking. The CNN and interaction signal must be checked together before teaching.

## Day 3: Reuse a pretrained representation

| Minutes | Activity |
| --- | --- |
| 0-10 | Recap: which decisions would change if features were learned before our task? |
| 10-50 | Explain attention conceptually, pretraining, embeddings, frozen representations, and the contrast with fine-tuning. |
| 50-60 | Break. |
| 60-100 | Extract embeddings for a small example; use cached embeddings for the full dataset and fit a simple classifier. |
| 100-110 | Break. |
| 110-150 | Compare validation results, costs, and interpretation across representations; discuss transfer and leakage; freeze workflows and predictions. |
| 150-180 | Reveal the planned test comparison, discuss what the evidence supports, recap, and buffer. No tuning against test results. |

Outcome: students can run and interpret the frozen-embedding workflow and distinguish model development from final evaluation.

## Day 4: Specify, delegate, and audit

| Minutes | Activity |
| --- | --- |
| 0-10 | Recap the scientific specification and evaluation boundary. |
| 10-50 | Explain LLM context, tools, agent loops, project instructions, and skills; show the agent's response to a vague question and inspect silent decisions. |
| 50-60 | Break. |
| 60-100 | Add an explicit analysis specification, project instructions, and a relevant skill; compare clean-run behavior. Students may participate if they have access or observe. |
| 100-110 | Break. |
| 110-150 | Scientifically audit the agent's analysis against the manual workflow and known simulation truth; distinguish execution success from valid inference. |
| 150-170 | Instructor-led Agentomics demonstration connecting back to the same decisions and audit criteria. |
| 170-180 | Final questions and course synthesis. |

Outcome: students can specify and audit an agent-assisted analysis without requiring paid agent access.

## Delivery rules

- Protect evaluation, student interpretation, leakage investigation, and scientific discussion when time runs short. Shorten model explanations and optional experiments first; provide working random forest code.
- Prepare saved outputs for expensive or external-service steps and a short recorded agent run. Clearly identify previous-run outputs rather than presenting them as live execution.
- Design for one instructor teaching alone.
- Slides, notebooks, and classroom teaching are in English.
- Perform access checks and setup during class; no pre-course access check is required. Reserve the opening 10 minutes of Day 1 for notebook startup and shorten the introductory overview to accommodate the diagnostic discussion in the first teaching block.
