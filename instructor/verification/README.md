# Local rehearsal and instructor handoff

Current compatibility note (2026-11-03): the primary dataset now uses the 15-position PPM, 0.95/0.05 planting and metadata schema 2. Earlier fixed-string scores, primary caches and freeze evidence below are historical, not verification of this generator. See the current check entry at the end and [parameter/migration guide](../../notebooks/README.md#primary-generator-and-saved-artifact-compatibility--2026-11-03). Genuine agent-run evidence is preserved unchanged.

2026-11-03 navigation: [simple signal](simple-signal.md), [separate leakage](leakage.md), [representations](representations.md), [frozen embeddings](embeddings.md), and [presentation checks](../../Slides/qa.md). These retain historical run evidence; the notebook packaging checks below are separate.

Date: October 26, 2026. This is a **locally executed development handoff, not a classroom-ready certification**. The user requested all development now, with manual Colab arrangement and checks later. Unperformed checks below remain unperformed; downstream implementation does not imply that its original manual gates passed.

## Passed local checks

| Check | Evidence / scope |
|---|---|
| Simple-signal experiment | 1,200 simulated 160-base sequences, stable 720/240/240 splits; logistic regression plus random forest; validation curves, predictions, coefficients/importance, metadata. |
| Leakage investigation | Default and seeds 101/102/103; related-group overlap visible and removed by group split; separate from course test data. See `docs/leakage-exercise.md`. |
| Representation control | Both variants, all three models, three separate development seeds; paired 4-mer equality and position-aware CNN construction. See `docs/representation-verification.md`. |
| Real frozen DNA model | Official pinned NT-v2-50M safetensors downloaded; weight size and SHA-256 verified; genuine CPU extraction for all 1,680 sequences; aligned 512-dimensional caches. See `docs/foundation-embedding-verification.md`. |
| Embedding provenance and alignment | Exact ID coverage, shuffled-row realignment, sequence-hash mismatch rejection, finite shape check, training-only standardization/classifier fitting. No labels enter extraction. |
| Cached classroom route | Fresh two-sequence extraction still executes with full-data caches present. Separately exercised cached-only route without loading the encoder; that route is not called live extraction. |
| Freeze / reveal contract | Freeze alone produces no test scores. Independent miniature fixture exercises explicit confirmation, artifact tamper rejection, inference-change rejection, validation-prediction binding, one-time reveal, and post-freeze/post-reveal retraining guards. |
| Protected-label boundary | Development reader omits test labels. Validation audit accepts that representation without requiring test labels. Unlabeled per-sequence test-input extraction is permitted; test fitting/scoring is not. |
| Audit and exercises | All four completed exercises execute. Authored fixture gives positional accuracy 1.0 but ID-aligned accuracy 0.0, with one overlapping group. Audit rejects malformed predictions and is row-order invariant. |
| Paste-ready independence | Six generated files executed in order in an isolated directory using a freshly installed Python environment, without repository modules or `PYTHONPATH`. Step 05 froze only; step 06 loaded audit definitions. |
| Notebook-style source capture | Inference-source fingerprinting exercised in an IPython cell with stored source history. This is not an actual Colab check. |
| Typechecking | `python -m mypy course_code tools instructor/completed --ignore-missing-imports --check-untyped-defs`: 13 source files pass after the source-binding and masked-label fixes. |
| Printable checklist | Browser visual inspection and A4-equivalent layout: content height 994.16 CSS px within 1,024.25 usable CSS px at 184 mm content width. Actual printer/PDF settings still require instructor check. |

The actual course's protected test results have **not** been calculated. Miniature contract-fixture scores are not course results and are not delivered as scientific evidence. No `course_output/test_results.json` exists at handoff. The main saved outputs remain unfrozen so the instructor can rehearse development; freeze explicitly only once the desired classroom workflow is fixed.

## Fresh local environment and measured execution

Windows, Python 3.13.14, CPU PyTorch 2.10.0+cpu, no GPU, no model API key. New virtual environment with exact direct versions from `course_code/requirements-ml.txt`; PyTorch was installed from the official CPU wheel index. Transitive versions are saved in `course_output/fresh_packages.txt`. Installation used the network and existing pip download caches; this was not an offline or first-ever network test. Installation time for this combined environment was not instrumented. The earlier baseline-only fresh setup took 171.5 seconds; do not treat that as the full deep-learning setup cost.

Six separate fresh-environment processes, including imports:

| File | Seconds | Result |
|---|---:|---|
| `01_simple_signal.py` | 41.43 | Passed; logistic regression and random forest, validation only |
| `02_split_leakage.py` | 2.30 | Passed; separate split comparison |
| `03_representations.py` | 34.86 | Passed; both variants and all three models |
| `04_foundation_embeddings.py` | 12.39 | Passed; small live extractions, verified full-data caches, validation classification |
| `05_frozen_comparison.py` | 3.91 | Passed; freeze only, no reveal |
| `06_scientific_audit.py` | 1.53 | Passed; function-loading entrypoint |

These are machine/process measurements, not observed teaching duration, installation guarantees, or Colab timings. The original full extraction took 77.62 seconds for simple-signal and 31.76 seconds for interaction-signal, plus encoder loading and download. Preserve `embedding_extraction_record.json` separately from later cache-based run records. Peak memory and accelerator comparisons were not measured.

Temporary verification locations (not required classroom inputs):

- Fresh environment: `C:/Users/panal/AppData/Local/Temp/ml-course-fresh-2mxohchv/venv`.
- Standalone rehearsal and logs: `C:/Users/panal/AppData/Local/Temp/ml-course-paste-rehearsal-7kyylmek`.
- Three-seed representation development: `C:/Users/panal/AppData/Local/Temp/ml-course-development-keipujfd`.
- Three-seed leakage development: `C:/Users/panal/AppData/Local/Temp/ml-course-leakage-kvf10udg`.
- Initial contract fixture: `C:/Users/panal/AppData/Local/Temp/ml-course-verification-i12k4h47`.
- Updated source/prediction freeze checks, IPython source capture, cached-only route: `C:/Users/panal/AppData/Local/Temp/ml-course-final-contract-a8537zmn`.

## Saved-output route

Keep `simple_signal_output/` and `course_output/` with the classroom copy. These generated local directories are ignored by Git and are **not** inside the paste-ready Python files. Transfer them explicitly to Colab if using the cache contingency. The main model weights are in the Hugging Face cache, not bundled. Required real embedding caches are approximately 2.34 MB and 0.94 MB; they are distinct from the 223.64 MB model weights. A new runtime needs model access for the small live example, even if full-data caches are supplied.

For expensive steps, open saved validation tables/plots and provenance first, label them as previous local runs, then use the short completed exercise. For cached-only embedding classification load definitions and call `run_foundation(live_example=False)` before freeze. Do not rename synthetic alignment examples as pretrained embeddings or omit a failed live step from the rehearsal record.

## Not run / pending instructor

- Actual Colab package resolution, cell layout/restart behavior, CPU memory, extraction, cached practical, and all student-facing entrypoints.
- A complete timed 180-minute rehearsal of each day, projector readability, printing, actual room/network conditions, and solo-teaching transitions. The guide supplies allocations, breaks, buffer, and cut-first priorities; it is not a measured classroom run.
- The planned actual course test reveal. The evaluator is tested on independent fixtures, but course outcomes intentionally remain protected for the instructor's planned comparison.
- Actual Agentomics access, chosen example, live rehearsal, and a genuine recording. The reserved slot remains 150-170 minutes on Day 4, followed by final discussion 170-180. Supply actual materials; the discussion contingency is not completion of that demonstration.
- A genuine short agent screen recording and its playback check. Actual development-only delegated agent comparisons are captured and independently audited in `agent_workshop/actual_runs/2026-10-26/`; authored fixtures are never substituted for those records.

## Review ledger

Initial independent Standards review found three actionable issues: incomplete freeze inventory/source binding, stale standalone-entrypoint documentation, and missing verification links. Initial independent Spec review found two: cached runs skipped the small live example, and the audit rejected masked protected labels. All five have implementation/documentation corrections and focused local checks. Final independent re-review is pending; do not read this ledger as a passed final review until updated.

No commits or pushes were created by this implementation.

## Packaging checks — 2026-11-03

The [cleanup map](../../README.md#cleanup-map--2026-11-03) supersedes the earlier paste-only delivery paths without rewriting the dated evidence above. Four generated [completed notebooks](../../notebooks/README.md) cover the same six workflow stages; stages 03–05 share one notebook to preserve their workspace. No canonical scientific Python module, requirement file or miniature solution changed from `palexiou/ML_Course_2026@ea59dd8`.

- `python -m mypy course_code tools instructor/completed --ignore-missing-imports --check-untyped-defs`: all 13 source files passed.
- All notebook code cells compiled; source-module hashes matched; generation was deterministic; cells contain no saved outputs, execution counters or executable `reveal_test` call. No local repository imports remain in the delivered definition cells.
- In fresh temporary working directories, the actual notebook definition/workflow cells for 01, 02 and 06 executed successfully without repository imports. Day 1 generated its development artifacts; its metadata confirmed no protected-test evaluation. The separate leakage metadata confirmed no course test data. The audit notebook loaded definitions. Setup cells were not run: existing local packages were used, without installation/downloads.
- All four distinct completed miniature exercises executed successfully. The combined 03–05 notebook passed syntax/source-binding checks; heavy CNN/pretrained workflows and actual freeze execution were not rerun. Their scientific source is unchanged, and their earlier execution evidence above remains separately dated.
- [Per-day deck checks](../../Slides/qa.md#later-2026-11-03-restructure-verification) passed offline layout/navigation/notes/interaction/export/print checks. Repository Markdown links and heading anchors passed; annotated outline and initial interview bytes were preserved.

No actual Colab execution, Google/GitHub sign-in, classroom timing or model-download rehearsal is claimed. Private-repository access remains required. No protected course test outcomes were scored or displayed. Screenshots, datasets from local checks, execution logs, PDFs and temporary tooling remain outside Git under `/tmp/ml-course-restructure/`; no new course data or model artifacts were added.

## Primary PPM checks — 2026-11-03

- `python -m unittest discover -s tests -v`: 11 checks passed, covering invalid matrices/probabilities, immutable array input, repeatability, IDs/labels/splits, insertion truth, endpoint starts, variable sites, 16,000-record planting/marginal checks, independently calculated and normalized four-mer expectations, generation fingerprints, legacy metadata, stale caches/run records, and interaction-control bag equality/metadata migration.
- Cache and freeze metadata tests compile the exact pure contract functions without neural-package imports. The freeze fixture uses synthetic embeddings and placeholder inventory files with an explicitly stubbed neural inference identity; it never runs inference or reveal. PyTorch is absent in this environment, so full neural source capture and the integrated freeze workflow were not rerun.
- `python -m mypy course_code tools instructor/completed --ignore-missing-imports --check-untyped-defs`: all 14 source files passed. `python tools/build_course.py` rebuilt all four notebooks; `python tools/check_notebooks.py` passed syntax, source hashes, exact embedded definitions, empty outputs and absence of executable reveal calls. Notebook 02 remains byte-identical because it has its own independent generator.
- The actual generated notebook 01 definition cells ran locally with its default configuration, existing packages and a headless plotting backend. Logistic regression and forest fitted training data and produced validation-only outputs for 240 records. The primary logistic-regression validation ROC-AUC was 0.6083333333 and AP 0.6070544315; these measured values did not trigger matrix or model tuning. Both feature tables contained all 256 four-mers with expected motif-window probabilities summing to one. No test metrics were computed; the development reader masked test labels.
- Safe smoke artifacts are outside Git at `/tmp/ml-course-ppm-validation-k7y88y67/`, including both models' validation tables. Default settings SHA-256: `78289cdd63a7bc544a5cc56c769de474f9646a268e4219bb485840480e92056b`; generated dataset SHA-256: `1bdae61d1e01adfd420138a451ba3e0a4b56ac1993d976754c4dd0a68c451ec7`. Sequence bytes/truth change under the new RNG consumption; seed-controlled labels, IDs and split identities are retained.

No saved datasets or frozen manifests existed in this checkout before these checks. Earlier primary outputs must be regenerated under the new contracts before use; stages 03–05, CNN/embedding training and actual Colab execution remain unverified for this revision. The family-memorization lesson, fixed-position interaction strings and distinct miniature fixtures remain intentionally separate. No historical agent results, protected test outcomes, slide/wiki files, commits or pushes were changed by this implementation.

## Guided Section 3 notebook checks — 2026-11-03

The existing [Day 1 notebook](../../notebooks/01_simple_signal.ipynb) now has a selected-cell route before its unchanged complete stage 01 call. Classroom delivery is GitHub `.ipynb` → Open in Colab → setup → definitions → Section 3 steps 1–5 → STOP. The optional one-weight gradient-descent illustration can be skipped. The complete later workflow still generates validation metrics and fits the forest; Run all crosses that boundary.

- `python -m unittest discover -s tests -v`: 12 tests passed, including the new generated-notebook integration check. The focused Section 3 test also passed after adding checks of both suggested student edits (validation row 1 and toy step size 0.2).
- The actual generated setup, shared/stage definitions and all six Section 3 code cells executed from an empty temporary working directory, with existing local packages and no installation. Python 3.13.5; NumPy 2.3.3, pandas 2.3.3, scikit-learn 1.7.2, SciPy 1.16.2, Matplotlib 3.10.7. This verifies a clean workspace, not a fresh dependency installation or Colab runtime.
- Only training/validation CSV reads were permitted during the tutorial. Tests forbade the full workflow, forest fitting and validation ROC-AUC/AP summaries. The fixed canonical split supplied 720 training and 240 validation records with disjoint sample/group IDs; all 256 training-vocabulary four-mers were sequence-only features. Canonical generation saved the complete split, and protected-test file bytes were hashed for artifact identity only. No test table was loaded for teaching, no test predictions/metrics were produced, and no reveal ran.
- Independent overlapping-window counts, a separately summed dot product and sigmoid, class order `[0, 1]`, one-record binary cross-entropy and mean training data loss matched the delivered calculations. Rerunning preparation reused identical canonical artifact hashes; the tutorial created only the six canonical dataset files, with no duplicate data/model exports or replacement stage metadata.
- For the optional constructed, nonseparable example, analytic gradients agreed with central finite differences at three weights. All eight default updates decreased actual mean logistic loss; the suggested smaller step size also decreased loss with slower progress. This illustration is separate from the DNA fit and explicitly identifies that fit's default L-BFGS solver. The plot executed with the headless Agg backend (its expected non-interactive `show` warning is not a Colab rendering check); no new plotting dependency was needed.
- `python tools/check_notebooks.py` passed syntax for every notebook code cell, canonical module hashes/exact definitions, the Day 1 teaching-source hash/exact cells/order, empty saved outputs and absence of executable reveal calls. Regeneration was byte-identical for all four notebooks. `python -m mypy course_code tools instructor/completed --ignore-missing-imports --check-untyped-defs` passed all 14 source files; `git diff --check` passed.

No generator, model defaults, scientific runtime modules or earlier stage return/metadata contracts were changed for this tutorial. No heavy CNN/embedding stages or full old pipeline were rerun. These checks establish runnable teaching calculations, not a new scientific performance conclusion. Actual Colab execution and classroom duration remain unverified. The new local notebook content and primary generator require the next push before the `main` Colab badge includes them; this implementation made no commit or push.

## Complete Day 1 teaching path — 2026-11-03

The instructor's later full Day 1 build authorization supersedes the Section 3-only rehearsal scope above. The generated notebook now has separate Sections 3–6 checkpoints and stops. All code cells (apart from package installation, already satisfied locally) were executed in a fresh working directory. The focused metrics path does not refit; the paired stage 01 workflow is deferred to Section 5; Section 6 includes exact full-vector contribution reconstruction, an explicit remainder for displayed top contributions and current PPM-derived enrichment. No protected test table was read by the teaching cells and no protected test score was calculated.

The source-bound [current record](day1-current.json) is the empirical input for the Day 1 HTML figures: logistic validation ROC-AUC **0.608333**, AP **0.607054**; forest ROC-AUC **0.611875**, AP **0.597040**, 240 identical validation rows and fixed threshold 0.5. No tuning followed this observation. The record includes full-precision values, generation identity, source/package information and produced-file hashes. Temporary full artifacts/execution logs are in `/tmp/ml-day1-final/execution/`.

`python -m unittest discover -s tests` passes 13 tests, including the end-to-end Day 1 lesson path, refit guards during metrics, threshold extremes/undefined precision, paired-row identity and alternate local explanation rows. `python tools/check_notebooks.py` validates all exact generated cells, hashes, syntax and empty saved outputs. Mypy passes 16 source files. [Presentation QA](../../Slides/qa.md#full-day-1-implementation--2026-11-03) records offline visuals/interactions/export/printing separately. Actual Colab execution, classroom timing and projector behavior remain unverified. The revisions remain uncommitted/unpushed.

## Day 2 teaching path and current CNN comparison — 2026-11-03

The [current representation record](representations.md#current-ppm-rehearsal--2026-11-03) and [source-bound evidence](day2-current.json) now cover local stage 03 execution on the revised PPM generator, guided Sections 5–6 readbacks, checkpoint/map inspection and the paired control. No neural ranking was prescribed or tuned; protected test results remain uncalculated. The [QA record](../../Slides/qa.md#day-2-sections-56--2026-11-03) owns detailed notebook/browser checks and remaining Colab/classroom limits. Reproduce using `MPLBACKEND=Agg python tools/rehearse_day2.py`; a complete compatible workspace can be reused with `--workspace PATH`. Historical “PyTorch absent / heavy stage 03 not rerun” statements above describe earlier checks and are superseded for this local stage 03 rehearsal only; embeddings/freeze/Colab readiness are not newly established.
