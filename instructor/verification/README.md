# Local rehearsal and instructor handoff

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
