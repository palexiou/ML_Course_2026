# Completed notebooks and execution

The instructor agreed on 2026-11-03 to version completed notebooks in GitHub and open them through Colab. Use **GitHub-hosted completed `.ipynb` → Open in Colab → setup → selected teaching cells**. The instructor can demonstrate while students optionally follow along; no coding from scratch, homework or submission is required. The separate [scaffolded practicals](../instructor/practicals.md) and [instructor answers](../instructor/answers.md) are retained.

| Notebook | Open in Colab | Purpose |
| --- | --- | --- |
| [01_simple_signal.ipynb](01_simple_signal.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb) | Day 1: Section 3 probability/loss → Section 4 metrics → Section 5 paired forest comparison → Section 6 explanation; stop at each lesson boundary. |
| [02_split_leakage.ipynb](02_split_leakage.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/02_split_leakage.ipynb) | Separate related-sequence investigation; not the main course split. |
| [03_representations.ipynb](03_representations.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/03_representations.ipynb) | Days 2–3: stages 03 representations, 04 embeddings, then 05 freeze in one workspace. |
| [06_scientific_audit.ipynb](06_scientific_audit.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/06_scientific_audit.ipynb) | Day 4 audit definitions; use the actual [agent kit](../agent_workshop/README.md) and practical. |

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

## Run and retain work

1. Open the GitHub-hosted notebook with its **Open in Colab** badge, run setup, then its normal definition cells and the cells selected by the instructor. For Day 1 Section 3, follow the short path above and stop before the full workflow. Setup installs missing direct packages at the locally rehearsed versions and prints existing versions; it does not silently replace installed packages. Rehearse compatibility and restart behavior in the actual classroom runtime. No account check or setup is homework.
2. Opening a GitHub notebook creates an editable view without overwriting its source. Save a copy in Drive to retain edits, or explicitly save to GitHub with write authorization. The execution VM and its files are temporary. A new notebook does not clone the repository or supply adjacent data files.
3. The notebooks bundle their Python dependencies and generate their datasets. Day 1 uses `simple_signal_output/`; the separate leakage exercise writes `course_output/leakage/`. The combined Days 2–3 notebook keeps stages 03–05 in one working directory. On a recycled runtime, rerun stage 03 before stage 04, or restore the complete provenance-checked `course_output/` artifacts explicitly. Saving the notebook alone does not save those artifacts.
4. Stage 04 defaults to a small live extraction plus verified full-data caches where available. A first run needs internet and approximately 224 MB of pinned NT-v2 weights plus libraries. CPU/two-thread behavior is the local baseline; no GPU, API key or paid agent account is required. The checkpoint uses custom Python code and a **CC-BY-NC-SA-4.0** license; see [model provenance and limits](../instructor/verification/embeddings.md).
5. Stage 05 **freezes only**. No executable reveal cell is included. The separate instructor-authorized `reveal_test(confirmation="REVEAL THE FROZEN TEST RESULTS")` call belongs at the planned Day 3 comparison. Keep notebook source history: freeze fingerprints inference code. Do not delete markers or rerun development to disguise post-reveal tuning. A new directory cannot make inspected test data independent again.

Saved outputs, model checkpoints, embedding caches and pretrained weights are not in Git or notebook outputs. Label restored results as previous execution. For cached-only stage 04, load definitions and call `run_foundation(live_example=False)` before freeze; this is not live extraction. No notebook in this repository contains saved execution outputs or test scores.

## Canonical source and rebuilding

Edit [course_code/](../course_code/), then run `python tools/build_course.py` from the repository root. Section 3 teaching cells live in `section3_cells()` in [the builder](../tools/build_course.py); Sections 4–6 live in [day1_teaching.py](../tools/day1_teaching.py). Edit those sources and rebuild. The four notebooks are generated delivery artifacts, replacing the six duplicated paste-ready `.py` copies. Each notebook records hashes of its exact source modules in `metadata.course_sources`; Day 1 also binds its teaching source with `metadata.course_teaching_sources`. The checker verifies exact canonical definitions and exact teaching cells and lesson order, including the paired workflow boundary. Normal definition cells preserve source history for freeze; no dynamic `exec` loader or repository import is required.

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
