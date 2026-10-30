# Scientific audit: actual simple-signal development run

This is an evidence-based review of the executed analysis, not a blanket scientific pass. The local scientific-audit skill and specification were read before implementation. Evidence: analysis.py, execution_output.txt, evaluation_report.json, validation_predictions_simple_signal_4mer_logreg.csv, verification.py, verification_results.json and verification_output.txt. No additional model was fitted during verification.

## 1. Fixed identities and group separation
- Claim: the supplied development split identities are preserved and group-disjoint.
- Observed evidence: 720 training samples in 720 groups; 240 validation samples in 240 groups. Training has 360/360 labels 0/1; validation 120/120. Unique sample IDs, no cross-split sample or group overlap, exact manifest ID coverage, and per-ID group/split equality all pass. All 960 supplied groups are singleton. Sorted-ID SHA256 values are recorded in evaluation_report.json.
- Consequence: no group leakage is detected under the supplied group definition. Unique sample IDs alone were not used as proof of group separation.
- Repair: none indicated for these inputs; mismatches raise before fitting, not silent filtering or resplitting.
- Remaining uncertainty: singleton groups do not prove biological independence; the generator source was not supplied. Independence is a simulation assumption, not an empirical biological result.

## 2. Training-only fitting and feature scope
- Claim: vocabulary and classifier learn from training only, using sequence only.
- Observed evidence: analysis.py calls vectorizer.fit_transform(train.sequence), vectorizer.transform(validation.sequence), classifier.fit(train_features, train.label.astype(int)), and predict_proba(validation_features). Features are character 4-mer counts, case preserved. Runtime shapes are (720,256) and (240,256); fitted sample count 720; classifier converged in 78 iterations with no recorded warnings. IDs, groups, split, label and simulation truth never enter the vectorizer.
- Consequence: no validation-fitted vocabulary, metadata leakage or truth-feature leakage is present in this source path. Truth inspection is an audit, not a model-selection experiment.
- Repair: none indicated. Preserve this fit/transform separation for future work.
- Remaining uncertainty: source tracing and recorded runtime shapes are evidence, not an independent system-call trace of the estimator. All 256 possible DNA 4-mers are represented, but vocabulary fitting remains training-only.

## 3. Prediction identity and numerical checks
- Claim: the persisted prediction table contains label-1 probabilities for exactly the validation IDs.
- Observed evidence: 240 unique sample_id,probability records; the code explicitly locates classifier.classes_ == 1. The CSV is reloaded and joined one-to-one on sample_id; coverage is exact; all probabilities are finite in [0,1]. Shuffling prediction rows leaves aligned labels/probabilities identical. Prediction SHA256: 0eecf328e119132014d6d2ee6ae858e0a3f4824817d165a5a6bbc14e3e979a79.
- Consequence: reported metrics use the persisted artifact, not unverified row-position matching.
- Repair: none indicated. Ten actual in-memory rejection probes cover duplicate/missing/extra prediction IDs, nonfinite/out-of-range probabilities, invalid DNA, invalid labels, incorrect split, manifest group mismatch and incorrect truth position. These are deliberately malformed copies, not changes to development data or illustrative model outputs.
- Remaining uncertainty: these probes are targeted, not exhaustive formal verification; source and input hashes are checked unchanged after execution.

## 4. Prespecified metrics and baseline comparison
- Claim: the fixed manual baseline is reproduced on the supplied simple-signal validation set.
- Observed evidence: configuration is printed before fitting/evaluation: ROC-AUC primary; threshold >=0.5; 4-mer counts; lowercase=False; logistic regression max_iter=2000 and random_state=2026. Installed defaults include lbfgs, L2, C=1, tol=0.0001. Only one classifier fit was executed; no hyperparameter/threshold/split search. ROC-AUC=0.8019444444444445 and AP=0.8024506156726241. User-supplied manual scores are 0.8019444444 and 0.8024506157; differences are +4.4444448121794267e-11 and -2.737587934120711e-11. Both match after rounding to ten decimal places. Independent pairwise-comparison ROC-AUC and threshold-grouped AP calculations reproduce the scores without sklearn metric functions.
- Consequence: the observed aggregate differences are consistent with supplied decimal rounding, not evidence of improved performance. No data or model was altered to match them.
- Repair: no numerical discrepancy requires repair. To establish prediction-level reproducibility, supply the manual source, dependency versions, full configuration, ID digest and predictions within the permitted boundary; do not tune this run to approximate missing artifacts.
- Remaining uncertainty: the user's same-identity assertion is not independently verified against a manual prediction artifact because none was supplied. Equal aggregate metrics do not prove identical probabilities or every manual implementation detail.

## 5. Threshold metrics and class limitations
- Claim: fixed-threshold validation classification performance is fully reported.
- Observed evidence: 50% positives in both splits; accuracy=balanced accuracy=0.7416666666666667, precision=0.7377049180327869, recall=0.75. Confusion matrix [[88,32],[30,90]], rows true [0,1], columns predicted [0,1]. Independent boolean counts reproduce that matrix. A single-class in-memory probe confirms ROC-AUC, AP and balanced accuracy are withheld with a limitation rather than invented; undefined precision/recall denominators use a documented zero policy.
- Consequence: ranking and threshold-specific outcomes are distinct and the threshold was not optimized on validation.
- Repair: none indicated for these balanced data.
- Remaining uncertainty: no confidence interval, calibration analysis or population-level biological generalization estimate was prespecified or claimed. This is one fixed simulated validation sample.

## 6. Test boundary and actual execution
- Claim: this new run has development-only evidence.
- Observed evidence: opened only the named workspace instructions, local audit skill, supplied development files, created source/reports and own outputs. The manifest contains only train/validation. No protected test, other run output, model cache, parent course document, network call, paid service, commit or push was used in this session. Package imports and installed apply_patch/Python runtime execution were required local CPU tools, not external data reads. The supplied manual aggregate metrics came from the user, not a historical run directory.
- Consequence: results are validation evidence only. There is no new independent test estimate and no basis to claim historical manual test integrity from this session.
- Repair: any independent test requires a separately agreed experiment. Revealed historical test data cannot be reused as fresh agent evaluation. No new experiment is authorized by this audit.
- Remaining uncertainty: no instructor freeze/reveal record or historical access log was supplied. This report is a session action record, not a forensic filesystem-access monitor.

## 7. Simulation interpretation and unavailable variant
- Claim: learned discrimination is limited to the supplied simple-signal simulation.
- Observed evidence: all sequences are uppercase A/C/G/T, length 160; truth IDs cover development exactly, planted starts/flags are valid and indicated motifs match TATAAATG. Observed planting fractions: training label 0=0.11388888888888889, label 1=0.8972222222222223; validation label 0=0.11666666666666667, label 1=0.925. Supplied description states nominal 0.1/0.9 planting and uniform background with seed 2026. Nominal rates were not forced onto finite samples.
- Consequence: results support validation discrimination in a deliberately motif-biased simulation, not real promoter recognition, regulatory discovery, general grammar, or universal model superiority.
- Repair: retain this interpretation. Do not silently add unavailable variants or synthetic pretrained embeddings.
- Remaining uncertainty: generator source and real-world data were not supplied. The interaction variant was not executed: its specified fixed-position motif-order control has matching flanks and identical 4-mer bags; identical feature vectors cannot be distinguished by this baseline even when labels differ. A position-preserving architecture can access discarded order information, but no CNN/pretrained-model advantage is established here.

## 8. Engineering status and remaining process limitation
- Claim: the requested local implementation and verification actually ran.
- Observed evidence: Python 3.13.14, numpy 2.3.2, pandas 2.3.1, scipy 1.16.1, scikit-learn 1.7.2, threadpoolctl 3.6.0; actual source/input/prediction hashes recorded. Baseline exit code 0; process wall time 1.4425887 s; internal analysis-through-evaluation time 0.22845649998635054 s. Verification exit code 0; process wall time 1.2812397 s; internal verification 0.10911820002365857 s. Source was edited using the actual apply_patch runtime after Windows wrapper argument failures.
- Consequence: runnable source, predictions and actual evidence exist; execution success does not remove scientific limitations above.
- Repair: an in-directory coding skill copy was requested because reading the installed external coding skill would violate the user's execution boundary. No external instructions or project files were substituted. Provide a permitted copy if compliance with that additional skill must be reviewed.
- Remaining uncertainty: external coding-skill compliance cannot be certified. The local AGENTS.md and scientific-audit skill were followed; manual provenance and historical test-access evidence remain unavailable.
