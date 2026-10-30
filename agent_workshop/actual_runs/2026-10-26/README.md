# Actual development-only agent runs: October 26, 2026

These are genuine native delegated Codex / gpt-6.1-sol executions, not the [authored flawed fixture](../../fixture.md). Raw files in `vague/` and `specified/` are retained unchanged. No screen video was captured. Open their Python sources, predictions, execution logs, and run reports for the observation route.

## Inputs and requests

Both fresh contexts received identical development inputs: 720 training and 240 validation sequences, split manifest, simulation truth, and dataset description. The parent independently checked byte-identical SHA-256 hashes across the two folders; see [parent audit](parent_audit.json). Neither received course test data, the other context, or worked answers. The directory restriction was a prompt instruction, not an operating-system sandbox.

The vague scientific request was: "Can you build the best model to predict promoters from these DNA sequences and explain the biology?" The specified request required `specification.md`, `AGENTS.md`, and the supplied scientific-audit skill in its own folder, using the simple-signal 4-mer logistic-regression baseline. Read [specified instructions](specified/specification.md) and both raw reports for operational details and loaded instructions. The specified context received aggregate manual ROC-AUC/AP, but not the manual source, predictions, or package versions.

Both were restricted to their assigned folders and CPU tools: no other project directories, test files, model caches, network, paid services, or commits. Both received a technical apply-patch executable correction. The vague run first stopped and then resumed with that correction; this was a parent-orchestrator intervention, not a new scientific request. The vague raw report calls it user-supplied; that wording is preserved rather than rewriting the evidence. Package versions are recorded per run, not assumed identical; costs were not exposed. Full native conversation provenance remains in the course thread.

## Observed decisions and independent audit

| Run | Actual modeling decision | Validation ROC-AUC | Average precision |
|---|---|---:|---:|
| [Vague run](vague/run_report.md) | Six CPU candidates; training-only five-fold group cross-validation selected disclosed-motif logistic regression by pooled out-of-fold log loss | 0.9041667 | 0.8589000 |
| [Specified run](specified/run_report.md) | Fixed bag-of-4-mers logistic regression; no alternative-model search | 0.8019444 | 0.8024506 |

The parent recomputed metrics by sample ID with `06_scientific_audit.py`: exact validation coverage, no cross-split groups or duplicate sequences in these development inputs. The specified probabilities reproduce the manual baseline within 1e-12. The vague prediction column was renamed in memory only for the audit interface. The vague model uses the disclosed `TATAAATG` prior, not a discovered biological mechanism. Both reports distinguish the simulation from real promoter prediction.

A higher score does not show that vague prompts are better, or that specifications worsen models. The objectives, features, selection criterion, and search differ; this single stochastic pair is not a controlled prompt-quality experiment. The vague run did not reproduce the authored fixture's errors. Ask which choices were fixed, which were left open, and which evidence supports each claim. Saved-prediction agreement does not prove training correctness; inspect code, fitting scope, and limitations as well.

## Native provenance

Provider/model: `codex` / `gpt-6.1-sol`. Original task IDs share the prefix `node:delegated-task:command%3Amcp%3A1272a1ad-c9af-4127-a4d7-dae573b6a341%3Adelegate-task%3A`, followed by `course-actual-vague-run-20261026-1` or `course-actual-specified-run-20261026-1`. The resumed vague task uses the same command prefix with `thread-send%3Aactual-vague-apply-patch-intervention-1` instead of `delegate-task%3A...`. See the raw reports for commands, timestamps, versions, hashes, failures, and limitations.

These records support local code/report inspection without an agent account. A genuine short screen recording and playback check, instructor Colab checks, timed classroom rehearsal, and actual Agentomics demonstration remain pending. No course protected test labels were read for this comparison or parent audit.
