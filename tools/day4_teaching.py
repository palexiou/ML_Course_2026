"""Completed Day 4 audit checkpoints; embeds only historical development inputs."""
import base64
import hashlib
import json
from pathlib import Path
import zlib
from day2_teaching import emit

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'agent_workshop/actual_runs/2026-10-26'


def archive_payload():
    names = ['vague/train.csv', 'vague/validation.csv', 'vague/validation_predictions.csv',
             'specified/validation_predictions_simple_signal_4mer_logreg.csv', 'parent_audit.json']
    files = {n: (ARCHIVE/n).read_bytes().decode('utf-8') for n in names}
    payload = {'files': files, 'sha256': {n: hashlib.sha256((ARCHIVE/n).read_bytes()).hexdigest() for n in names}}
    return base64.b64encode(zlib.compress(json.dumps(payload).encode(), level=9)).decode()


def teaching_cells(factory):
    return emit(factory, [
        ('markdown', 'day4-start', '''
            ## Day 4 · Scientific audit, with or without an agent account

            **GitHub → Open in Colab → setup → shared definitions → stage 06 definitions
            → these checkpoints.** Instructor demonstration or optional follow-along;
            no account with an agent service, new model training, submission or homework.
            Pause at each STOP. The notebook is self-contained: opening GitHub does not clone files.

            First inspect an **authored flawed fixture**. Its probabilities are invented,
            not a recorded model run. Later, recompute saved predictions from the genuine
            **October 26 historical fixed-motif agent runs**. Those data differ from today's
            15-position PPM task; scores are not a comparison with the current Days 1–3 models.
            Protected course test files/results are never included or opened.
        '''),
        ('code', 'day4-fixture', (ROOT/'agent_workshop/flawed_analysis.py').read_text()),
        ('markdown', 'day4-stop-inspect', '''
            **STOP · Section 2:** inspect `samples` and `predictions` above before auditing.
            Which group crosses the split? Where was the vocabulary fitted? Which sample
            owns each probability? The fixture has no fitted classifier behind these numbers.
            Its claim of 100% positional accuracy is deliberately misleading.

            At **Section 5**, continue below. If watching the demonstration, discuss the
            tables with a partner. There is no scored quiz.
        '''),
        ('code', 'day4-fixture-audit', '''
            d4_training = samples.loc[samples.split.eq("train")]
            d4_validation = samples.loc[samples.split.eq("validation")]
            d4_joined = d4_validation[["sample_id", "label"]].merge(predictions, on="sample_id", validate="one_to_one")
            d4_positional = float((d4_validation.label.to_numpy() == (predictions.probability.to_numpy() >= 0.5)).mean())
            d4_aligned = float((d4_joined.label == (d4_joined.probability >= 0.5)).mean())
            d4_fixture_report = audit_predictions(samples, predictions, claimed_metrics={"accuracy": 1.0})
            assert d4_positional == 1.0 and d4_aligned == 0.0
            assert d4_fixture_report["cross_split_group_count"] == 1
            assert d4_fixture_report["claim_disagreements"]
            print("AUTHORED FIXTURE, not an observed agent result")
            print("Cross-split groups:", sorted(set(d4_training.group_id) & set(d4_validation.group_id)))
            print("Misleading positional accuracy:", d4_positional, "ID-aligned accuracy:", d4_aligned)
            print(d4_joined.to_string(index=False))
            print("Metric disagreement:", d4_fixture_report["claim_disagreements"])
            print("MANUAL code inspection: vectorizer.fit(samples['sequence']) includes validation rows.")
            print("The prediction-table audit cannot infer preprocessing scope or prove whether a test was accessed.")
            print("Repairing the join does not repair group leakage or create a credible model comparison.")
        '''),
        ('markdown', 'day4-negative-guide', '''
            ### Reject invalid prediction tables

            Reversing row order should leave ID-aligned metrics unchanged. Missing, duplicate,
            unexpected IDs and nonfinite/out-of-range probabilities must be rejected.
            These are in-memory corruptions of the small fixture, never protected data.
        '''),
        ('code', 'day4-negative-probes', '''
            d4_reordered = audit_predictions(samples, predictions.iloc[::-1])
            assert d4_reordered["metrics"] == d4_fixture_report["metrics"]
            d4_invalid = {
                "duplicate ID": pd.concat([predictions, predictions.iloc[:1]], ignore_index=True),
                "missing ID": predictions.iloc[:1].copy(),
                "unexpected ID": predictions.assign(sample_id=["unexpected", "validation-01"]),
                "nonfinite probability": predictions.assign(probability=[np.nan, 0.9]),
                "out-of-range probability": predictions.assign(probability=[1.2, 0.9]),
            }
            for d4_name, d4_bad in d4_invalid.items():
                try:
                    audit_predictions(samples, d4_bad)
                except ValueError as d4_error:
                    print("Rejected", d4_name, "→", d4_error)
                else:
                    raise AssertionError("Invalid predictions accepted: " + d4_name)
            print("Shuffling valid rows preserves the ID-aligned result.")
        '''),
        ('markdown', 'day4-archive-guide', '''
            ### Genuine previous runs · October 26, 2026

            The following compressed payload contains the exact archived **training and
            validation CSVs, saved predictions and parent audit**. It contains no test file,
            model weights or executable remote code. Hashes identify the supplied bytes;
            they do not establish correct training. Git has stored LF line endings; the original Windows input hashes are matched separately by reconstructing CRLF. Both agents received identical development
            files; the two model choices and search spaces differ.

            Raw source, full prompts, reports and intervention notes remain in
            [the evidence packet](https://github.com/palexiou/ML_Course_2026/tree/main/agent_workshop/actual_runs/2026-10-26).
            The vague run used a **disclosed motif prior**, not biological discovery.
            Recomputing historical saved predictions does not rerun an agent or fit a model.
        '''),
        ('code', 'day4-archive-data', '''import base64, hashlib, zlib
from io import StringIO
# Exact development-only archive bytes; decoded data is never executed.
d4_payload_b64 = ''' + repr(archive_payload()) + '''
d4_archive = json.loads(zlib.decompress(base64.b64decode(d4_payload_b64)))
for d4_name, d4_text in d4_archive["files"].items():
    assert hashlib.sha256(d4_text.encode()).hexdigest() == d4_archive["sha256"][d4_name]
d4_historical_train = pd.read_csv(StringIO(d4_archive["files"]["vague/train.csv"]))
d4_historical_validation = pd.read_csv(StringIO(d4_archive["files"]["vague/validation.csv"]))
d4_historical = pd.concat([d4_historical_train, d4_historical_validation], ignore_index=True)
assert d4_historical_train.split.eq("train").all() and len(d4_historical_train) == 720
assert d4_historical_validation.split.eq("validation").all() and len(d4_historical_validation) == 240
assert set(d4_historical.split) == {"train", "validation"}
d4_parent = json.loads(d4_archive["files"]["parent_audit.json"])
for d4_name in ["train.csv", "validation.csv"]:
    assert hashlib.sha256(d4_archive["files"]["vague/" + d4_name].replace("\\r\\n", "\\n").replace("\\n", "\\r\\n").encode()).hexdigest() == d4_parent["input_hashes"][d4_name]
print("Historical fixed-motif packet: 720 training, 240 validation; checkout hashes verified; original Windows hashes matched after explicit CRLF reconstruction.")
'''),
        ('code', 'day4-actual-audit', '''
            d4_paths = {
                "vague": "vague/validation_predictions.csv",
                "specified": "specified/validation_predictions_simple_signal_4mer_logreg.csv",
            }
            d4_actual_reports = {}
            for d4_arm, d4_path in d4_paths.items():
                d4_predictions = pd.read_csv(StringIO(d4_archive["files"][d4_path]))
                if d4_arm == "vague":
                    # Adapter only; raw archive bytes are unchanged.
                    d4_predictions = d4_predictions.rename(columns={"probability_label_1": "probability"})
                d4_claimed = d4_parent["arms"][d4_arm]["metrics"]
                d4_report = audit_predictions(d4_historical, d4_predictions, claimed_metrics=d4_claimed)
                assert not d4_report["claim_disagreements"]
                assert d4_report["cross_split_group_count"] == 0
                assert d4_report["cross_split_duplicate_sequence_count"] == 0
                assert len(d4_predictions) == 240
                d4_actual_reports[d4_arm] = d4_report
                print(d4_arm, "· exact validation IDs; groups/duplicate sequences do not cross")
                print("ROC-AUC:", round(d4_report["metrics"]["roc_auc"], 7), "AP:", round(d4_report["metrics"]["average_precision"], 7))
            print("Neither run reproduced the authored fixture's errors.")
            print("Different features/search/objectives: this does not isolate prompt quality.")
            print("Training correctness, biological scope and access history still require manual evidence.")
        '''),
        ('markdown', 'day4-findings', '''
            ### Evidence → consequence → repair

            Discuss one finding with your partner:

            - **Evidence:** `group-a` crosses train/validation. **Consequence:** independent-group
              generalization is unsupported. **Repair:** for this separate exercise, obtain enough
              data, split by group, refit and evaluate on development data. Preserve the main-course manifest.
            - **Evidence:** vocabulary fitted on all four rows. **Consequence:** validation inputs
              informed learned preprocessing. **Repair:** fit the pipeline on training only; this
              finding alone does not quantify its effect on the score.
            - **Evidence:** probabilities are reversed by ID. **Consequence:** 100% positional
              accuracy attaches predictions to the wrong samples. **Repair:** exact one-to-one join;
              ID-aligned accuracy is 0%, without repairing the other defects.

            **STOP:** no model fitting, test scoring or new agent service is needed. Complete the
            [audit checklist](https://github.com/palexiou/ML_Course_2026/blob/main/instructor/audit-checklist.html)
            with PASS / FAIL / UNVERIFIED, then defend one supported sentence. The Agentomics slot
            uses the agreed audit-discussion fallback; no platform demo has been verified.
        '''),
    ])
