# Completed notebooks and execution

The instructor agreed on 2026-11-03 to version completed notebooks in GitHub and open them through Colab. Demonstration versus student follow-along remains open. The separate [scaffolded practicals](../instructor/practicals.md) and [instructor answers](../instructor/answers.md) are retained; no homework or submission is required.

| Notebook | Open in Colab | Purpose |
| --- | --- | --- |
| [01_simple_signal.ipynb](01_simple_signal.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb) | Day 1: simulate DNA, fit logistic regression and forest, inspect validation and importance. |
| [02_split_leakage.ipynb](02_split_leakage.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/02_split_leakage.ipynb) | Separate related-sequence investigation; not the main course split. |
| [03_representations.ipynb](03_representations.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/03_representations.ipynb) | Days 2–3: stages 03 representations, 04 embeddings, then 05 freeze in one workspace. |
| [06_scientific_audit.ipynb](06_scientific_audit.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/06_scientific_audit.ipynb) | Day 4 audit definitions; use the actual [agent kit](../agent_workshop/README.md) and practical. |

These links name real generated notebook files. Direct opening is supported by Google's [integration example](https://colab.research.google.com/github/googlecolab/colabtools/blob/main/notebooks/colab-github-demo.ipynb) and [FAQ](https://research.google.com/colaboratory/faq.html), checked 2026-11-03. End-to-end course execution in Colab remains unverified. The repository was private in authenticated metadata on that date: students need repository access and Colab's “Include Private Repos” authorization. No visibility change is implied.

## Run and retain work

1. Open the notebook, run setup, then its normal definition and workflow cells. Setup installs missing direct packages at the locally rehearsed versions and prints existing versions; it does not silently replace installed packages. Rehearse compatibility and restart behavior in the actual classroom runtime. No account check or setup is homework.
2. Opening a GitHub notebook creates an editable view without overwriting its source. Save a copy in Drive to retain edits, or explicitly save to GitHub with write authorization. The execution VM and its files are temporary. A new notebook does not clone the repository or supply adjacent data files.
3. The notebooks bundle their Python dependencies and generate their datasets. Day 1 uses `simple_signal_output/`; the separate leakage exercise writes `course_output/leakage/`. The combined Days 2–3 notebook keeps stages 03–05 in one working directory. On a recycled runtime, rerun stage 03 before stage 04, or restore the complete provenance-checked `course_output/` artifacts explicitly. Saving the notebook alone does not save those artifacts.
4. Stage 04 defaults to a small live extraction plus verified full-data caches where available. A first run needs internet and approximately 224 MB of pinned NT-v2 weights plus libraries. CPU/two-thread behavior is the local baseline; no GPU, API key or paid agent account is required. The checkpoint uses custom Python code and a **CC-BY-NC-SA-4.0** license; see [model provenance and limits](../instructor/verification/embeddings.md).
5. Stage 05 **freezes only**. No executable reveal cell is included. The separate instructor-authorized `reveal_test(confirmation="REVEAL THE FROZEN TEST RESULTS")` call belongs at the planned Day 3 comparison. Keep notebook source history: freeze fingerprints inference code. Do not delete markers or rerun development to disguise post-reveal tuning. A new directory cannot make inspected test data independent again.

Saved outputs, model checkpoints, embedding caches and pretrained weights are not in Git or notebook outputs. Label restored results as previous execution. For cached-only stage 04, load definitions and call `run_foundation(live_example=False)` before freeze; this is not live extraction. No notebook in this repository contains saved execution outputs or test scores.

## Canonical source and rebuilding

Edit [course_code/](../course_code/), then run `python tools/build_course.py` from the repository root. The four notebooks are generated delivery artifacts, replacing the six duplicated paste-ready `.py` copies. Each notebook records hashes of its exact source modules in `metadata.course_sources`. Normal definition cells preserve source history for freeze; no dynamic `exec` loader or repository import is required.

The six numbered Python modules remain the local entrypoints. `course_core.py` owns simulation, identity, metrics and dataset validation; `course_inference.py` owns shared CNN inference and embedding-cache alignment. Keep these supporting modules beside the numbered scripts. Python 3.11+ is required. Exact locally rehearsed direct versions are in [base requirements](../course_code/requirements.txt) and [ML requirements](../course_code/requirements-ml.txt). Local execution example:

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
