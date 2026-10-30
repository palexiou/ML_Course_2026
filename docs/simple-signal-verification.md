# Simple-signal workflow: local verification

## Scope and review baseline

This record covers ticket 01 only: standalone code that the instructor can paste into Colab. It is not the full Day 1 practical or the four-day teaching package.

Starting commit: `341e48f07ef39862e5f9347e460b36389af06ae6`. The worktree was clean before implementation. The repository had acquired this initial commit after the earlier no-commit warning; no commit was created by this implementation.

The instructor requested manual Colab preparation instead of browser-operated Colab execution. Actual Colab verification remains a human handoff. The later request to develop all remaining materials authorizes downstream implementation while preserving unperformed checks; it does not make ticket 01 resolved.

## Delivered entry point

- `paste_ready/01_simple_signal.py`: current self-contained Python-cell entrypoint. `course_code/01_simple_signal.py` is now the canonical modular source and imports `course_core`; run it locally with its supporting module, not alone in Colab.
- `course_code/requirements.txt`: the four locally verified direct dependency versions.
- `course_code/README.md`: local execution, Colab setup guidance, output meanings, scientific limitations, and the manual Colab checklist.
- Running the entry point creates `simple_signal_output` in the working directory; generated artifacts are ignored by Git rather than committed as a second source of truth.

## Observed local results

Environment: Windows 11, Python 3.13.14, CPU execution without a GPU. Direct dependencies: NumPy 2.3.2, pandas 2.3.1, scikit-learn 1.7.2, Matplotlib 3.10.5. The fresh environment also recorded SciPy 1.18.1, joblib 1.6.0, and threadpoolctl 3.7.0 in the experiment metadata.

The fixed default seed 2026 generated 1,200 independent 160-base sequences, split into 720 training, 240 validation, and 240 protected test samples. Every partition has balanced labels. No sample or singleton group crosses partitions, and the default sequences are unique.

Observed validation results:

- Primary metric, ROC-AUC: 0.8019444444.
- Average precision: 0.8024506157, labeled AP rather than trapezoidal PR-AUC.
- Accuracy and balanced accuracy: 0.7416666667.
- Precision: 0.7377049180; recall: 0.75.
- Confusion matrix, rows true labels and columns predicted labels in order 0, 1: `[[88, 32], [30, 90]]`.
- Decision threshold: 0.5, fixed before fitting.

These are measured results for one configuration, not guaranteed scores for another dataset or environment. Validation planting fractions were 0.925 for label 1 and 0.1166666667 for label 0. A validation-only oracle using the deliberate planting flag had ROC-AUC 0.9041666667; that flag was not supplied to the model.

Separate development seeds 101, 102, and 103 produced validation ROC-AUC values 0.8058333333, 0.7565277778, and 0.7963194444. A no-planted-signal control at seed 101 produced ROC-AUC 0.5811805556 and AP 0.5694809648. The control is a finite-sample observation, not evidence of real predictive biology. These probes did not score the final course test set or change the fixed defaults.

The default normalized dataset hash is `515144fbfb7396f33c11198a16f67a25683bab1349ef7f12928726d1bf7cc2df`. Eight scientific artifacts were byte-identical across repeated runs in the original environment. In the fresh dependency environment, generated data, split identities, truth, coefficients, and aggregate metrics matched; tiny floating-point differences in probabilities need not be byte-identical across numerical-library environments.

## Execution and timing checks

A new virtual environment was created outside the repository and installed the supplied requirements without using system site-packages. Dependency installation/setup took approximately 171.5 seconds on this machine. Its standalone execution passed, and `pip check` reported no broken requirements.

The fresh run recorded approximately 39.70 seconds for first imports, 0.081 seconds for generation/splitting, 0.118 seconds for fitting, 0.032 seconds for validation evaluation, and 40.98 seconds total including imports and output generation. These are local measurements, not Colab or teaching-time estimates. Package setup is measured separately from script execution.

Headless verification used Matplotlib's Agg backend. The script saved the figure successfully; the default display call emitted the expected non-interactive-backend warning during the direct script run. In a headless programmatic run, use `show_plot=False`. The saved confusion-matrix, ROC, and precision-recall figure was visually inspected and readable.

## Verification performed

- A temporary end-to-end harness failed before the script existed, then passed after implementation through the actual standalone script entry point.
- Checked generated artifact presence, sample counts, unique identities, group separation, sequence length, label values, validation prediction alignment, probability ranges, and confusion-matrix totals.
- Checked that truth fields are not exported as model-input columns, that the vectorizer and classifier fit training sequences and labels only, and that the reported metrics refer only to validation samples.
- Checked reproducible generation and repeated scientific outputs, separate development seeds, and the no-planted-signal control.
- Verified actual local execution from a fresh virtual environment and checked installed dependency consistency.
- Typechecked the source with `mypy --ignore-missing-imports --check-untyped-defs`. Third-party libraries without typing information remain outside that check's coverage.
- Checked whitespace with Git and visually inspected the generated plot. No permanent test framework was added to this previously test-free repository; the one-off rehearsal harness is kept outside the repository.

## Independent code review

Two independent read-only reviews covered the starting commit through the final tracked changes and relevant untracked implementation files.

- Standards: zero findings; no concrete documented-standard breaches or material heuristic concerns. The reviewer checked source and documentation but did not rerun the experiment.
- Spec: zero actionable findings and no unasked scope expansion. The reviewer independently executed a focused temporary-directory check of validation row alignment, identities, group separation, ROC-AUC, AP, and confusion-matrix values. No test-set performance was evaluated.
- Both reviews identified the manual Colab check as explicitly pending, not as an already satisfied requirement. Ticket 01 remains ready-for-human, not resolved.

## Remaining verification

- Actual Colab execution, Colab package conflict checks, or Colab startup timing: instructor manual check pending.
- Any test-set performance evaluation: intentionally not performed.
- The related-sequence leakage exercise, CNN, pretrained embeddings, agent demonstration, full student notebooks, slides, or full course rehearsal: later tickets.

Use the manual Colab checklist in the standalone-code handoff to finish the outstanding check. A saved local plot or passing local run is not a Colab pass.
