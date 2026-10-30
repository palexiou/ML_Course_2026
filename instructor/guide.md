# Instructor guide

Four English-language sessions for 10–15 master's students, taught by one instructor. Each session is 180 minutes including breaks. All required learning and setup happen in class. There is no homework, exam, grading, or required submission. Questions below are ungraded discussion prompts.

## Start here

- [Scaffolded practicals](exercises.md): short selected-code tasks, one per day, with interpretation questions.
- [Completed answers](answers.md): explanations and links to separate, pasteable Python scripts.
- [One-page scientific-audit checklist](audit-checklist.html): open in a browser and print A4 portrait at 100%, with browser headers and footers disabled.
- [Day 4 kit](../agent_workshop/README.md): vague prompt, precise specification, example project instructions, scientific skill, deliberately flawed fixture, audit answers, and observation route.
- [Verification record](verification.md): distinguishes local checks from outstanding classroom verification.
- Existing model implementations: [simple signal](../course_code/01_simple_signal.py), [separate leakage investigation](../course_code/02_split_leakage.py), [representations](../course_code/03_representations.py). Use generated [paste-ready code](../paste_ready/README.md) for one-cell copying. Local verification is recorded separately; it does not establish Colab compatibility.

The current handoff is standalone code for the instructor to paste into Colab. It is not notebook UI work. Each completed exercise runs as one cell without repository imports. The instructor arranges the cells manually; actual Colab execution is explicitly deferred. The short exercises supplement the model practicals; a successful exercise is not evidence that the full model or embedding workflow has been rehearsed.

## Scientific contract and current integration issues

The course dataset is simulated DNA for binary sequence classification, motivated by promoter prediction. It is not evidence of real promoter recognition. Use the terms course dataset, dataset variant, scaffolded practical, and scientific audit consistently.

Dataset interface: `sample_id,group_id,sequence,label,split`. IDs are unique; labels are 0 or 1; split is `train`, `validation`, or `test`; related sequences stay in one split. Prediction interface: `sample_id,probability`, with probability referring to label 1. Join predictions by sample ID, never by incidental row order. IDs, groups, split, and simulation truth are audit metadata, not model features.

Training fits learned transformations and model parameters. Validation guides development. Primary comparison metric is ROC-AUC; report average precision, class balance, and threshold-0.5 confusion matrices as supporting views. Average precision is not trapezoidal PR-AUC. The existing separate leakage investigation uses balanced accuracy as its primary metric; disclose this and do not mix it into the main representation ranking.

Keep protected test labels, scores, predictions, and outcome plots out of model development. Generation creates all labels before exporting partitions. Development readers omit the protected label column. A frozen, label-independent encoder may compute embeddings for test input sequences without fitting on those sequences; this is not a test-score reveal. Simulation-truth inspection during development must be restricted to training and validation IDs. The planned Day 3 reveal is the only scoring step. File separation and hashes are accident guards, not adversarial access security.

The integrated leakage outputs use `group_id`, `split` (`train`/`validation`), and `probability`. Its comparison-table `split` field names the flawed/corrected strategy; its per-sample manifest records train/validation membership. Do not merge this isolated dataset into the main representation comparison.

The interaction dataset variant is a deliberately engineered **fixed-position motif-order control**. It swaps `TATAAATG` and `CGGACGTC` between blocks starting at zero-based positions 32 and 80. Each block has six G bases before the motif and six C bases after it. Paired sequences share background and have identical 4-mer counts, opposite labels, and the same group ID. The matching flanks preserve the bag of 4-mers. Motif starts are 38 and 86, not 32 and 80. The CNN concatenates flattened convolution features with global maximum features, retaining position. Global pooling alone can discard this cue. This does not establish general regulatory grammar, position-invariant order learning, or universal CNN superiority.

## Before teaching: instructor preparation, not student homework

1. Assemble only development CSVs, code, dependency instructions, and labeled saved development outputs in the student folder. Keep protected test material separately. Check projector, local copies, and printing. Never ask students to obtain accounts before class.
2. Rehearse the locally verified model workflows in the intended classroom environment. Record measured setup, training, extraction, and discussion times separately. Timetable arithmetic is not a rehearsal.
3. Keep a local copy of these four completed exercise scripts. Their minimal packages are NumPy, pandas, and scikit-learn; Days 2 and 3 need only NumPy and pandas. Try imports first; install missing packages in class with `%pip install numpy pandas scikit-learn`, then restart if requested. Record actual versions; do not assert compatibility from an unrun environment.
4. Prepare provenance-labeled previous-run model outputs only if actual artifacts exist. The representation outputs under `course_output/` are locally verified validation artifacts, not a completed Colab or classroom rehearsal. Verify their run and dataset correspondence before projection.
5. Obtain the actual pretrained model/extraction handoff, immutable revision, tokenizer, pooling, sequence handling, package versions, cache alignment, and measured small extraction. The pinned checkpoint and real full aligned caches are locally verified; see [embedding verification](../docs/foundation-embedding-verification.md). Colab costs remain unmeasured. The Day 3 miniature cache exercise is explicitly synthetic, not pretrained DNA output.
6. Review the [two actual agent runs and parent audit](../agent_workshop/actual_runs/2026-10-26/README.md). Obtain instructor agent access if a live rerun is desired, a short screen recording, and actual Agentomics demonstration access/materials. The recording and Agentomics inputs remain pending. Do not advertise the hand-authored fixture as a recorded agent run. See the Day 4 kit's evidence ledger.

## Teaching alone

Project the task and stopping point before circulating. Use pairs for discussion if students want, while keeping individual participation possible. Ask for hands at each checkpoint: running, interpreting, or needing help. Handle a shared problem once on the projector; after two minutes on an individual setup problem, move that student to the projected observation route and revisit during the break. Do not leave the class waiting on one installation.

Give two minutes to predict before running code and two minutes to explain the output afterward. Display the completed code at the checkpoint so syntax trouble does not consume interpretation time. Faster students take the optional extension in class; it is never homework. Read sample/group overlap aloud rather than accepting a high score as proof of correctness.

Keep a visible clock. At minutes 45, 95, and 145 announce five minutes to the checkpoint. Breaks remain at 50–60 and 100–110. Stop slow external requests after five minutes and label the failure. Use verified previous-run evidence if available; otherwise use the labeled conceptual exercise and record that the model step was not completed.

## Day 1 — Define and evaluate the experiment

Outcome: explain and apply the classical workflow using validation for development.

| Minutes | Instructor and student actions | Checkpoint / transition |
| --- | --- | --- |
| 0–10 | Check Colab access in class, paste startup imports, run a tiny cell. Offer local code or projector observation immediately for access failures. | Everyone has an execution or observation route; no pre-course setup assumed. |
| 10–20 | Ask: what is a sample, label, feature, and prediction? What would a probability of 0.8 mean? Motivate promoter prediction while naming the simulation. | A prediction is for a sequence; 0.8 is a model score, not proof of function. |
| 20–35 | Contrast classification with continuous regression. Map supervised labels, unsupervised structure, and self-supervised prediction from input. Inspect development sequences and noisy motif planting. | The simple signal is probabilistic, not a perfect motif rule. |
| 35–50 | Count overlapping 4-mers; discuss lost position. Begin Day 1 selected-code exercise. | Features are counts; fit the vocabulary on training only. |
| 50–60 | Break. | |
| 60–80 | Establish fixed sample/group split identities. Fit logistic regression from the working model code after integration checks. | Ask why validation cannot be training data and why test stays unread. |
| 80–100 | Finish Day 1 exercise; interpret probability, threshold, confusion matrix, ROC-AUC and average precision. Use ROC and precision-recall curves from verified model outputs if available. | Change threshold conceptually, without selecting it on test. |
| 100–110 | Break. | |
| 110–125 | Explain one tree split and forest averaging; provide working random forest code. | No implementation of a forest from scratch. |
| 125–150 | Compare validation results on identical IDs; inspect feature importance versus development simulation truth. | Correlated k-mers can share importance; importance is not causal evidence. |
| 150–165 | Separate leakage investigation: show row-disjoint but group-overlapping evaluation; students identify the flaw before the correction. | Keep its dataset and outputs out of the main comparison. |
| 165–175 | Show corrected group split and measured outputs; discuss independent-group generalization. | The score need not fall by a promised amount. |
| 175–180 | Recap and buffer: representation, split, evidence. | “Tomorrow we change the representation, not the evaluation boundary.” |

Leakage short route if delayed: 150–154 inspect overlap, 154–160 propose group split, 160–168 inspect corrected overlap and existing outputs, 168–175 discuss why the old claim fails, 175–180 recap. Do not cut the investigation itself. If upstream outputs are unavailable, the Day 4 fixture's overlap table supplies an explicitly hand-authored diagnosis example, not a completed leakage experiment.

## Day 2 — Learn the representation

Outcome: distinguish handcrafted and learned representations without a universal ranking.

| Minutes | Instructor and student actions | Checkpoint / transition |
| --- | --- | --- |
| 0–10 | Recall what bag-of-4-mer counts preserve and discard. | Presence/count is not absolute location. |
| 10–25 | Connect weighted sum plus bias to sigmoid probability; calculate sigmoid(1) ≈ 0.731. | Link the equation to a single prediction. |
| 25–40 | Explain loss, optimization, and backpropagation as assigning parameter updates through the computation. | No derivative exercise. |
| 40–50 | Complete one-hot portion of Day 2 exercise; inspect shape and channel ordering A,C,G,T. | Sequence length and channel count are different axes. |
| 50–60 | Break. | |
| 60–75 | Explain convolution windows, shared filters, and pooling. Show the actual position-preserving CNN architecture. | Flattening preserves positional information. |
| 75–100 | Train the small CNN on the simple-signal variant using the integrated implementation, or inspect labeled previous-run evidence. | Record runtime and validation checkpoint selection; no test reads. |
| 100–110 | Break. | |
| 110–125 | Build the fixed-position motif-order pair in Day 2 exercise; compare its 4-mer counts. | Equal bags, opposite labels. |
| 125–140 | Compare classical and CNN validation responses on the same interaction IDs and paired sequence changes. | A response difference shows sensitivity under this control only. |
| 140–150 | Explain fixed blocks, matching flanks, and CNN flattening; students state the limited conclusion. | Do not call this general regulatory grammar. |
| 150–165 | Discuss performance, computation cost, and interpretation limits across both variants. | A more costly representation need not be better. |
| 165–180 | Questions, extension if time, and buffer. | “Can we reuse features learned before this task?” |

If training is slow, cut extra epochs and optional architecture exploration only before freezing that run's declared configuration; do not change configurations merely to get a favorable ranking. Prefer previously verified outputs over last-minute unvalidated architecture changes. A failed live run remains failed even if a plot is available.

## Day 3 — Reuse a pretrained representation

Outcome: audit frozen-embedding alignment and distinguish development from final evaluation.

| Minutes | Instructor and student actions | Checkpoint / transition |
| --- | --- | --- |
| 0–10 | Recall learned versus handcrafted features. | Frozen features can be new to this classifier but learned elsewhere. |
| 10–25 | Explain attention as context-dependent weighting, with a short sequence example. | Attention weights alone do not establish biological causality. |
| 25–40 | Explain self-supervised pretraining, numerical embeddings, and frozen extraction. | Classifier fitting changes its parameters, not a frozen encoder. |
| 40–50 | Contrast fine-tuning conceptually; identify tokenizer, model revision, layer, and pooling choices. | No required fine-tuning run. |
| 50–60 | Break. | |
| 60–75 | Run the supplied, verified small extraction on development sequences only; measure it separately. | If the extraction handoff is unavailable, mark this step pending; never relabel synthetic features. |
| 75–100 | Complete Day 3 cache-alignment exercise, then fit the actual cached-feature classifier when its verified cache is available. | Match IDs exactly before joining; training-only learned preprocessing. |
| 100–110 | Break. | |
| 110–125 | Compare validation results, costs, and interpretations across the same variants and split identities. | Compare available evidence; missing methods remain missing. |
| 125–140 | Discuss transfer, domain shift, and unknown pretraining overlap. | No evidence of overlap is not proof of no overlap. |
| 140–150 | Explicitly freeze every compared workflow using the checklist below. | Announce freeze before authorizing any test read. |
| 150–165 | Reveal and score the protected test once using frozen workflows, if integration prerequisites pass. | No edits or model selection in response to these results. |
| 165–175 | Interpret discrepancy from validation, sampling uncertainty, and simulation limits. | A result can disappoint without justifying tuning. |
| 175–180 | Recap and buffer. | “Tomorrow we audit whether an agent preserves these decisions.” |

Freeze/reveal checklist, performed aloud at 140–150:

1. Record dataset variant, development-file hashes, immutable sample/group split manifest, seed, package versions, and code revision or source hashes. Confirm no prior test reads.
2. Record trained model/checkpoint and preprocessing artifact hashes, CNN validation-selection policy, embedding revision/tokenization/pooling/cache correspondence, metric policy, and fixed threshold 0.5. Freeze the list of methods being compared; do not add a test-selected winner.
3. Save validation predictions using `sample_id,probability` for each method/variant and freeze all development decisions. Prepare an empty test prediction destination and the fixed inference procedure. Test predictions themselves can only be created after reveal; do not read test sequences in order to “freeze predictions” early.
4. Record instructor name, timestamp, and explicit reveal authorization. Only then release protected test inputs and labels to the fixed inference/evaluation procedure. Write test predictions and results with provenance; archive them without overwriting development evidence.
5. If any prerequisite is missing, do not reveal. Record the comparison as not run and discuss the boundary using development evidence. After reveal, further tuning would require a new independent evaluation, not rebranding the same test as fresh.

## Day 4 — Specify, delegate, and audit

Outcome: specify an analysis and scientifically audit its evidence with or without agent access. The folder name `agent_workshop` is the integrated Day 4 kit, not a new standalone workshop.

| Minutes | Instructor and student actions | Checkpoint / transition |
| --- | --- | --- |
| 0–10 | Recall the objective and Day 3 freeze/reveal boundary. | Revealed test results are historical evidence, not new feedback for development. |
| 10–25 | Distinguish LLM context, tools that read/run/edit, an agent loop, persistent project instructions, and reusable skills. | A specification defines this analysis; instructions set project constraints; a skill gives a reusable procedure. |
| 25–40 | Present the vague prompt. Inspect the saved actual vague-run code/report; contrast it with the separately labeled hand-authored flawed fixture. | List decisions that the vague prompt left unspecified. |
| 40–50 | Students identify missing evidence and predict failure modes. | A successful script is not a valid scientific conclusion. |
| 50–60 | Break. | |
| 60–75 | Read the precise specification and justify its inputs, split policy, metrics, outputs, and limits. | Repair the scientific request before touching implementation. |
| 75–90 | Add example AGENTS and scientific skill. Inspect the saved specified-run code/report. Compare its fixed baseline objective with the vague run; do not infer a causal prompt-quality effect. | Instructions can reduce ambiguity; they do not guarantee validity. |
| 90–100 | Observation route and optional operators answer the same evidence questions. | No account or paid service is required. |
| 100–110 | Break. | |
| 110–125 | Complete Day 4 audit code and one-page checklist. | Detect group overlap and prediction misalignment independently. |
| 125–140 | Compare claims with code, manual workflow, and known simulation construction. | Separate observed evidence from assertions and absent provenance. |
| 140–150 | Discuss repair plan, remaining uncertainty, and the test boundary. | Do not tune agents against the revealed Day 3 test. |
| 150–170 | Reserved instructor-led Agentomics demonstration: question (3 min), actual workflow/evidence (10 min), audit (7 min). | Actual access/materials and recording are pending instructor; no product behavior is asserted here. |
| 170–180 | Final discussion: what must remain human scientific responsibility? Which evidence would change your conclusion? | Preserve the full 10 minutes. |

For Agentomics, obtain actual materials before teaching. Select a real example that exposes input/split choices, experiment tracking, and supporting evidence, then ask which of those can actually be inspected. If access fails, use a genuine labeled recording if supplied. If neither exists, keep the 20-minute slot for discussing what evidence an automation demonstration would need, explicitly mark the demonstration not delivered, and retain the final 10-minute discussion. This is an honest contingency, not completion of the Agentomics requirement.

## Cut priorities and recovery

Cut first: optional extensions, extra hyperparameter trials, detailed architecture diagrams, full transformer mechanics, and student implementation of the random forest. Use completed code to recover syntax time. Then shorten the introductory ML map and repeated model explanations. Protect breaks, evaluation, student interpretation, the leakage investigation, scientific audit, the reserved Agentomics 20 minutes, and final discussion 10 minutes. Never move unfinished essentials into homework.

| Failure | Immediate one-instructor response | Evidence label / remaining obligation |
| --- | --- | --- |
| Colab/account/install problem | Project code and outputs; students predict and audit in pairs or individually. Try local execution only if already available. | Observation is valid participation; Colab execution remains unverified. |
| Slow/failed CNN | Inspect an existing provenance-checked validation run; continue the fixed-position motif-order exercise. | Previous-run output, not a live success. |
| Missing embedding cache/model access | Run the explicit synthetic alignment exercise and discuss extraction requirements. | Actual pretrained extraction/classification remains pending. |
| Missing agent account/service | Inspect saved actual-run code/reports and parent audit, plus the separate authored fixture. | Actual previous runs are not screen recordings; authored fixture is not an agent transcript. |
| Missing Agentomics access/recording | Ask instructor to supply actual access/materials before class; use the discussion contingency if necessary. | Actual demonstration pending/not delivered. |
| Test integrity or freeze failure | Stop reveal; preserve files and record the issue. | No independent test claim. |

Close each day with one spoken claim and one limitation per pair or volunteer, with no collection or grading. The course is not classroom-verified until its outstanding integration and rehearsal checks pass.
