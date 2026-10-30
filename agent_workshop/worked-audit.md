# Worked scientific audit of the authored fixture

This answer audits the supplied teaching fixture. It is not a report about an observed agent run. [The completed audit code](../instructor/completed/day4_audit.py) reproduces its group and alignment findings without opening any test file.

| Claim or operation | Observed evidence | Consequence | Repair / remaining uncertainty |
| --- | --- | --- | --- |
| Unique sample IDs prove independence | `group-a` appears in both train and validation despite distinct sample IDs | The evaluation includes a related sequence; new-group generalization is unsupported | In the separate exercise, split by group, check overlap, and refit. Preserve the main course's fixed manifest. |
| Vocabulary can be fitted before partitioning | `vectorizer.fit(samples["sequence"])` includes validation sequences | Learned preprocessing sees evaluation inputs; this violates the training-only protocol even without validation labels | Fit the pipeline on training only. This defect alone does not prove it caused the full score difference. |
| Accuracy is 1.0 | Validation labels are `[0,1]`, but probabilities `[0.1,0.9]` belong to IDs in reverse order | Positional comparison attaches scores to the wrong samples | Join by ID after exact coverage and uniqueness checks. Correctly aligned probabilities are `[0.9,0.1]`, giving 0.0 accuracy. |
| The best model was found | No fitted predictor, justified comparison, or provenance generates these probabilities | Authored scores cannot establish a model ranking | Obtain actual predictions, source/configuration, versions, seeds, timing, and an identical-ID manual baseline. |
| Accuracy establishes performance | Only an invalid accuracy is shown, without declared metric policy | Ranking, threshold behavior, prevalence, and uncertainty are unexamined | Use the declared ROC-AUC policy and supporting average precision/confusion matrix; with two rows, estimates are highly unstable. |
| Learned promoter biology | The examples are authored simulated sequences, with no biological validation | Real promoter recognition and biological causality are unsupported | State the limited simulated question; inspect known ground truth without treating feature importance as causal. |
| Day 3 test can choose this approach | The claim proposes post-reveal test-guided selection | The old test would become development feedback | Keep the agent model validation-only. A new independent evaluation would require a separately agreed experiment. |

The code's successful execution is an engineering observation. The scientific conclusion fails. Correcting alignment does not repair group leakage, preprocessing leakage, missing provenance, or the biological overclaim. Do not “fix” the invented probabilities to produce a good score.

## Worked repair sequence

1. Replace the vague objective with the precise specification. For the actual main course, use the fixed development partitions and validate them. For this separate leakage exercise, rebuild a group-respecting development split on sufficient data with both classes, then refit; these four rows do not support a serious performance comparison.
2. Fit the 4-mer/logistic-regression pipeline on training sequences and labels only. Report actual classifier probabilities for validation IDs; do not reuse the invented fixture table.
3. Check unique IDs and exact prediction coverage; join by ID. Record metrics and threshold policy before evaluation and compare with the manual baseline on the same IDs and dataset variant.
4. Save source, configuration, input/model hashes, package versions, seed, timing, predictions, and observed failures. Actual clean-run and recording evidence remains pending.
5. Audit all claims using the checklist. Keep Day 3 test results historical and unavailable for selection. Report only supported simulation conclusions.

## What the added instructions can and cannot establish

The specification removes ambiguous choices for this analysis. AGENTS repeats the project-wide evaluation and interface constraints. The skill directs evidence-based inspection. Tools can implement and check those choices. The authored repair illustrates intended behavior; only actual clean runs can show what an agent did, and even those do not guarantee future validity.

For the fixed-position motif-order control, a correct interpretation is: paired inputs have identical bag-of-4-mer representations but different ordered positions, and the implemented CNN retains position through flattening. It is incorrect to conclude that all CNNs learn arbitrary motif grammar, that embeddings must win, or that the simulation proves promoter function.
