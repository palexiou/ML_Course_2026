# Completed notebooks and execution

The instructor agreed on 2026-11-03 to version completed notebooks in GitHub and open them through Colab. Use **GitHub-hosted completed `.ipynb` → Open in Colab → setup → selected teaching cells**. The instructor can demonstrate while students optionally follow along; no coding from scratch, homework or submission is required. The separate [scaffolded practicals](../instructor/practicals.md) and [instructor answers](../instructor/answers.md) are retained.

| Notebook | Open in Colab | Purpose |
| --- | --- | --- |
| [01_simple_signal.ipynb](01_simple_signal.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb) | Day 1: Section 3 probability/loss → Section 4 metrics → Section 5 paired forest comparison → Section 6 explanation; stop at each lesson boundary. |
| [02_split_leakage.ipynb](02_split_leakage.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/02_split_leakage.ipynb) | Separate related-sequence investigation; not the main course split. |
| [03_representations.ipynb](03_representations.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/03_representations.ipynb) | Days 2–3: stages 03 representations, 04 embeddings, then 05 freeze in one workspace. |
| [06_scientific_audit.ipynb](06_scientific_audit.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/06_scientific_audit.ipynb) | Day 4: authored fixture → STOP → fixture audit and rejection probes → genuine historical prediction readback; use the [agent kit](../agent_workshop/README.md) for source inspection. |

These links name real generated notebook files. Direct opening is supported by Google's [integration example](https://colab.research.google.com/github/googlecolab/colabtools/blob/main/notebooks/colab-github-demo.ipynb) and [FAQ](https://research.google.com/colaboratory/faq.html), checked 2026-11-03. End-to-end course execution in Colab remains unverified. The repository was private in authenticated metadata on that date: students need repository access and Colab's “Include Private Repos” authorization. No visibility change is implied.

## Day 1 Section 3: selected cells

Open the GitHub notebook using its Colab badge above, run **setup**, **shared definitions** and **stage 01 definitions**, then follow **Section 3** steps 1–5. The cells are complete and runnable:

1. Generate or verify the primary dataset in the normal `simple_signal_output/` directory; load **training and validation only**. The complete split is saved by the canonical generator, with settings/file identities checked. Test file bytes are only hashed for identity, never loaded as a tutorial table or scored.
2. Inspect one validation DNA record and its k-mer count row. Fit the vocabulary on training sequences only; labels and IDs never enter the features.
3. Fit logistic regression on training data; inspect coefficients, intercept and the class mapping **A=0, B=1**.
4. Compare `decision_function` with `counts · weights + bias`, then compare a stable sigmoid with `predict_proba`: **p=P(B=1)** and **P(A=0)=1−p**. Assertions check agreement.
5. Reveal that record's known label and calculate binary cross-entropy; inspect mean training data loss and confident correct/wrong examples. This is the data-loss term; the solver also uses L2 regularization.

The optional **one-weight gradient-descent illustration** plots actual logistic loss on four constructed, mixed-label records with fixed bias. A step table and numbered points show eight updates. It is separate from the DNA model, whose default solver is L-BFGS. Skip this optional cell to keep the main route short.

Students can change `s3_row_index` and rerun steps 2–5, inspect count × coefficient contributions, or compare toy step sizes `0.8` and `0.2`. These are small changes to working cells; no new exercise hierarchy or model search is needed. The instructor may select the core cells for a roughly five-minute demonstration **after setup**; this is a suggested route, not measured classroom timing or added lesson time.

At **STOP — end of the Section 3 path**, pause. Continue only when the instructor reaches the next lesson. **Run all crosses all teaching boundaries** and also fits the forest. The tutorial saves no extra model/data copies and does not replace complete-workflow records.

## Day 1 Sections 4–6: continue in the same notebook

- **Section 4:** run `s4-probabilities` once, then `s4-decisions` at 0.5. Read the matrix and calculate precision/recall from its counts. Try 0.8 or 0.3 by changing only `s4_threshold`; the probabilities and ROC-AUC stay fixed. No fitting occurs in these cells. Undefined precision is shown as NaN when no positive calls exist. Stop before the paired workflow.
- **Section 5:** run the complete `run-01` workflow once, then `s5-comparison`. It regenerates the same deterministic dataset and fits logistic regression and the 100-tree forest using the same training-fitted count vocabulary. Read ROC-AUC/AP and precision/recall on the same 240 validation rows. The helper joins predictions one-to-one by ID and checks labels and generation identity. Do not assume one model wins every metric.
- **Section 6:** run `s6-local-explanation`, optionally change `s6_row_index`, and explain one actual prediction. All contributions plus bias reproduce the verified probability; the displayed top features retain an explicit remainder. Then `s6-global-explanation` reads signed coefficients, non-directional forest impurity importance and expected internal-window PPM enrichment from the paired run. No refitting or test scoring is needed.

The generated Day 1 notebook was executed locally from a clean working directory through all these checkpoints, including the paired workflow and alternate-row explanations. The [current validation record](../instructor/verification/day1-current.json) binds the figures to generator, source and artifact hashes. This local rehearsal is not hosted Colab execution or a classroom timing rehearsal.

**Delivery state (2026-11-03):** the Sections 3–6 teaching path and revised primary generator are local changes awaiting the next push. The `main` Colab badge currently opens the previously published notebook; it will include these revisions after that push. Local execution verifies the generated cells; actual Colab execution and classroom timing remain unverified.

## Day 2 Sections 5–6: selected cells

Open [03_representations.ipynb](03_representations.ipynb) through its Colab badge, run **setup → both shared definition cells → stage 03 definitions → Day 2 Section 5**. The guided path is complete working code for instructor demonstration or optional follow-along:

1. Run stage 03 once. It captures the full two-variant output so the primary experiment is introduced first. Repeating the cell reads a compatible completed run without refitting; incomplete, mismatched, frozen or revealed workspaces are rejected.
2. Check source/generation identities, matching validation IDs/labels, recomputed ROC-AUC/AP and checkpoint inference. Read actual training-loss and validation-ROC-AUC histories, marking the earliest best validation epoch after all 24 epochs.
3. Inspect one validation sequence and one second-convolution post-ReLU response channel. Change only the row/channel and rerun the inspection cell; do not fit again. A response map is not attribution or biological proof.
4. At Section 6, inspect one opposite-label control pair. All 48 validation pairs have complete overlapping 4-mer Counter equality and matching bag-model probabilities checked; choose another group without refitting.
5. **STOP at “end of Day 2,” before stage 04.** Run all would cross into Day 3 embeddings/freeze. Retain the complete course_output workspace for Day 3.

Teaching cells live in [day2_teaching.py](../tools/day2_teaching.py), integrated by the existing builder and hash/exact-cell checked. The [current local record](../instructor/verification/day2-current.json) supplies the slide figures. Local setup dependencies were already satisfied for execution; actual Colab startup, downloads and classroom timing remain unverified. These revisions are local until the next push; the main-branch Colab badge includes them after publication.

## Day 3: continue the same notebook

Keep the Day 2 runtime or restore its complete matching `course_output/`. Otherwise rerun the Day 2 path first. Then run **stage 04 definitions → Day 3 identity → live checkpoint**. This extracts two training sequences per variant, checks 31 tokens and `(2, 512)` finite vectors, prints components/timings, and pauses.

Continue with **full cache → cache readback → synthetic alignment and failure checks → four-workflow validation comparison**. Full-cache creation uses the canonical stage 04 function. With no cache, it loads the model and extracts all rows (including an internal two-row consistency check); `live_example=False` alone does not make it cached-only. Repeating a completed, source-matched stage 04 cell reads the saved run without fitting again. Scaling statistics and validation predictions are checked against the exact training/validation identities. Test labels stay masked; caching their inputs is label-independent.

At **STOP before freeze**, complete the instructor checklist. Stage 05 freezes only; its separate reveal remains absent from executable cells. The slide deck can load `test_results.json` after the instructor's authorised classroom reveal; importing runs no model and does not independently verify the freeze manifest.

[Day 3 teaching source](../tools/day3_teaching.py) and [current local verification](../instructor/verification/day3-current.json) record actual execution, including a freeze-only check in a copied workspace. Local extraction/checks took 36.08 s / 14.10 s for the two variants in the initial current run. Hosted Colab, classroom download cost, pacing and the planned reveal remain unverified. **These Day 3 notebook changes are local until pushed**; the main-branch Colab link includes them after publication.

## Day 4: guided audit

Open [06_scientific_audit.ipynb](06_scientific_audit.ipynb) via GitHub → Colab. Run **setup → shared definitions → stage 06 definitions → run-06 → Day 4 fixture**, then **STOP for Section 2 inspection**. At Section 5, continue with **fixture audit → negative prediction probes → archive data → actual-run audit → findings**. Completed cells support instructor demonstration or optional follow-along; no submission or agent account is needed.

The fixture has four authored rows and invented probabilities. Its 100% positional accuracy becomes 0% after the correct ID join; group overlap and validation-informed vocabulary remain separate defects. Reordered valid prediction rows preserve the aligned result, while missing/duplicate/unexpected IDs and invalid probabilities are refused. The notebook embeds only development CSVs and saved predictions from the genuine October 26 fixed-motif runs, plus their parent audit. It decodes data, without executing archive code or fitting models. Historical ROC-AUC is 0.904167 vague / 0.801944 specified; this is distinct from the current PPM task and does not isolate prompt quality.

[Teaching source](../tools/day4_teaching.py) is checked against exact generated cells and hashes. [Local evidence](../instructor/verification/day4-current.json) records clean-workspace execution with existing dependencies; no course test data or results were accessed. The Agentomics slot uses the instructor-selected audit-discussion fallback. **New Day 4 cells are local until pushed**; hosted Colab setup/execution and classroom pacing remain unverified.

## Run and retain work

1. Open the GitHub-hosted notebook with its **Open in Colab** badge, run setup, then its normal definition cells and the cells selected by the instructor. For Day 1 Section 3, follow the short path above and stop before the full workflow. Setup installs missing direct packages at the locally rehearsed versions and prints existing versions; it does not silently replace installed packages. Rehearse compatibility and restart behavior in the actual classroom runtime. No account check or setup is homework.
2. Opening a GitHub notebook creates an editable view without overwriting its source. Save a copy in Drive to retain edits, or explicitly save to GitHub with write authorization. The execution VM and its files are temporary. A new notebook does not clone the repository or supply adjacent data files.
3. The notebooks bundle their Python dependencies and generate their datasets. Day 1 uses `simple_signal_output/`; the separate leakage exercise writes `course_output/leakage/`. The combined Days 2–3 notebook keeps stages 03–05 in one working directory. On a recycled runtime, rerun stage 03 before stage 04, or restore the complete provenance-checked `course_output/` artifacts explicitly. Saving the notebook alone does not save those artifacts.
4. Stage 04 defaults to a small live extraction plus verified full-data caches where available. A first run needs internet and approximately 224 MB of pinned NT-v2 weights plus libraries. CPU/two-thread behavior is the local baseline; no GPU, API key or paid agent account is required. The checkpoint uses custom Python code and a **CC-BY-NC-SA-4.0** license; see [model provenance and limits](../instructor/verification/embeddings.md).
5. Stage 05 **freezes only**. No executable reveal cell is included. The separate instructor-authorized `reveal_test(confirmation="REVEAL THE FROZEN TEST RESULTS")` call belongs at the planned Day 3 comparison. Keep notebook source history: freeze fingerprints inference code. Do not delete markers or rerun development to disguise post-reveal tuning. A new directory cannot make inspected test data independent again.

Saved outputs, model checkpoints, embedding caches and pretrained weights are not in Git or notebook outputs. Label restored results as previous execution. For cached-only stage 04, restore a compatible full cache first, then load definitions and call `run_foundation(live_example=False)` before freeze. Without a cache that call still extracts all rows; it is not a cached-only route. No notebook in this repository contains saved execution outputs or test scores.

## Canonical source and rebuilding

Edit [course_code/](../course_code/), then run `python tools/build_course.py` from the repository root. Section 3 teaching cells live in `section3_cells()` in [the builder](../tools/build_course.py); Sections 4–6 live in [day1_teaching.py](../tools/day1_teaching.py). Edit those sources and rebuild. The four notebooks are generated delivery artifacts, replacing the six duplicated paste-ready `.py` copies. Each notebook records hashes of its exact source modules in `metadata.course_sources`; Days 1–4 also bind their teaching source with `metadata.course_teaching_sources`. The checker verifies exact canonical definitions and exact teaching cells and lesson order, including the paired workflow boundary. Normal definition cells preserve source history for freeze; no dynamic `exec` loader or repository import is required.

For maintainers' local verification, the six numbered Python modules remain entrypoints. Classroom execution uses the GitHub/Colab route above. `course_core.py` owns simulation, identity, metrics and dataset validation; `course_inference.py` owns shared CNN inference and embedding-cache alignment. Keep these supporting modules beside the numbered scripts. Python 3.11+ is required. Exact locally rehearsed direct versions are in [base requirements](../course_code/requirements.txt) and [ML requirements](../course_code/requirements-ml.txt). Maintainer execution example:

```bash
python -m pip install -r course_code/requirements-ml.txt
python course_code/01_simple_signal.py
python course_code/02_split_leakage.py
python course_code/03_representations.py
python course_code/04_foundation_embeddings.py
python course_code/05_frozen_comparison.py freeze
```

The scripts' generated outputs are relative to the working directory; keep one working directory for stages 03–05. The CPU PyTorch wheel index can avoid unwanted accelerator libraries for a local CPU-only installation. The full [verification record](../instructor/verification/README.md) distinguishes local evidence, synthetic exercises, and pending Colab/classroom checks.

## Evaluation and interpretation

Use controlled simulated DNA classification, not claims of real promoter recognition. Training fits vocabulary/scaling/model parameters; validation supports development, with ROC-AUC primary, average precision supporting, and threshold 0.5. The separate leakage experiment uses balanced accuracy. IDs, groups, split and simulation truth are metadata, never predictive features. Join predictions to labels by sample ID.

Development readers omit protected test labels. Frozen label-independent extraction may read test inputs without fitting on them; only the authorized reveal scores their labels. Freeze binds artifact/configuration/source/package identities and validation predictions. Hashes and file separation guard accidents, not adversarial access. The fixed-position motif-order control preserves paired 4-mer bags while the CNN retains position through flattened features; it does not establish a universal model ranking or biological grammar. Interpretation compares coefficients/importance with known simulation truth, not causal biological evidence.


## Primary generator and saved-artifact compatibility — 2026-11-03

The primary dataset uses the explicit `DEFAULT_MOTIF_PPM` in [course_core.py](../course_code/course_core.py): 15 rows in A/C/G/T order, every entry positive, every row summing to one, and a leading probability of at least 0.5 (including a 0.50/0.40/0.05/0.05 row). A fresh site is sampled independently at each planted record, then overwrites 15 bases at a uniformly random valid start, including either boundary. Planting is Bernoulli 0.95 for positives and 0.05 for negatives, not a rule inferred from sequence scanning. The background is independent uniform DNA. Defaults remain 1,200 balanced records, length 160, seed 2026, and stratified 720/240/240 splits. IDs, labels and split membership retain their previous seed-controlled construction; changed sampling consumes a different RNG stream, so sequence bytes and truth change. No reverse complements are added.

The matrix is a **position probability matrix (PPM)**. A technical PWM would contain log-odds scores, here `log2(PPM / 0.25)` against uniform background. No log-odds matrix is used to generate DNA. `simulation_truth.csv` contains insertion flags, nullable starts and independently sampled sites for instructor inspection; `generation.json` records all generator parameters. These fields are never classifier inputs. Unplanted records have no recorded start or site, even if their background happens to resemble the pattern.

Both feature tables retain their filenames and weight columns and now add `motif_window_probability` and `motif_vs_background_enrichment`. For a word of length k, the first is the sum of its probability products across the 15−k+1 wholly internal motif windows, divided by that window count. The second divides this average by background probability 4⁻ᵏ (1/256 for 4-mers). Across all 256 four-base words the first column sums to one. This excludes site-boundary windows and the class mixture, so it is not expected whole-sequence frequency or evidence of causality. Every word has nonzero probability; the former binary `within_planted_motif` column is removed. Annotations are undefined for k > 15.

Dataset metadata schema 2 hashes the complete settings (including matrix, base order, planting probabilities, seed and algorithm version) and every saved dataset file. Development loading rejects earlier metadata. Representation and embedding run records bind the generation file; caches additionally bind generation identity, sequence hashes and sample IDs; freeze checks these identities and records the current generator contract. Old checkpoints, caches and frozen manifests cannot silently pass as the new primary dataset. Preserve historical results, but regenerate stages 03–05 in a new development directory before a new comparison; old primary embeddings require fresh extraction. Heavy stages have not been rerun for this change. The separate family-memorization and fixed-position interaction lessons keep their own generating rules, including the interaction variant's two fixed eight-base strings. Miniature practical fixtures are deliberately distinct from the primary generator.

Rebuild notebooks with `python tools/build_course.py`; verify source hashes, embedded definitions and syntax with `python tools/check_notebooks.py`. Focused scientific contracts use standard-library unittest: `python -m unittest discover -s tests`. These are local checks; actual Colab execution remains unverified.
