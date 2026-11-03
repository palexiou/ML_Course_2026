"""Guided Day 3 cells for the existing combined notebook; never reveal test scores."""
from pathlib import Path
from day2_teaching import emit

ROOT = Path(__file__).resolve().parents[1]


def before_workflow(factory, source_identity):
    return emit(factory, [
        ('markdown', 'day3-start', '''
            ## Day 3 · Run two sequences, then continue with the full cache

            **GitHub → Open in Colab → setup → shared definitions → stage 03/Day 2
            → stage 04 definitions → these cells.** Keep the same runtime and `course_output/`.
            A fresh runtime needs the completed Day 2 path first; Git contains no model/cache outputs.
            Instructor demo or optional follow-along; no submission. Do not use Run all.

            This checkpoint downloads about 224 MB of weights plus dependencies on first use.
            The pinned model executes custom Python (`trust_remote_code=True`); safetensors
            does not prevent that execution. Weights: CC-BY-NC-SA-4.0. Both model and code
            revisions are fixed. Local CPU execution is the baseline; Colab remains unverified.
        '''),
        ('code', 'day3-identity', 'd3_source_identity = ' + repr(source_identity) + '''
d3_root = Path("course_output")
if any((d3_root / name).exists() for name in ("frozen_manifest.json", "test_results.json")):
    raise RuntimeError("Frozen/revealed workspace: preserve it; do not restart development.")
d3_previous = json.loads((d3_root / "day2_teaching_identity.json").read_text())
assert d3_previous["sources"] == d3_source_identity, "Restore matching stage 03 outputs first"
d3_samples = {v: read_dataset(d3_root / "datasets" / v) for v in ("simple", "interaction")}
for d3_frame in d3_samples.values():
    assert d3_frame.loc[d3_frame.split.eq("test"), "label"].isna().all()
print("Current dataset identities checked. Test labels remain masked.")
'''),
        ('markdown', 'day3-live-guide', '''
            ### Section 3 · Two real training sequences

            Run the next cell once. It loads the pinned frozen encoder, inspects tokenisation,
            and extracts only the first two **training** sequences of each variant.
            Pause here to inspect shape, finiteness, and components. Coordinates are not named motifs.
            Timings exclude installation; first loading may include network download.
        '''),
        ('code', 'day3-live', '''
            from time import perf_counter
            import gc
            d3_started = perf_counter()
            d3_tokenizer, d3_encoder = load_frozen_encoder()
            d3_load_seconds = perf_counter() - d3_started
            d3_live = {}
            d3_live_records = {}
            print(f"Load (including download if needed): {d3_load_seconds:.2f}s")
            for d3_variant, d3_frame in d3_samples.items():
                d3_two = d3_frame.loc[d3_frame.split.eq("train")].head(2)
                d3_encoded = d3_tokenizer(d3_two.sequence.tolist(), return_tensors="pt", padding=True, truncation=False)
                assert tuple(d3_encoded["input_ids"].shape) == (2, 31)
                d3_started = perf_counter()
                d3_vectors = extract_embeddings(d3_two.sequence.tolist(), d3_tokenizer, d3_encoder)
                d3_seconds = perf_counter() - d3_started
                assert d3_vectors.shape == (2, 512) and np.isfinite(d3_vectors).all()
                d3_live[d3_variant] = d3_vectors
                d3_live_records[d3_variant] = {"sample_ids": d3_two.sample_id.tolist(), "seconds": d3_seconds, "shape": list(d3_vectors.shape), "token_count": 31}
                print(d3_variant, "two training sequences:", d3_vectors.shape, f"{d3_seconds:.3f}s")
                print("First eight components:\\n", np.round(d3_vectors[:, :8], 4))
            d3_figure, d3_axes = plt.subplots(1, 2, figsize=(11, 2.5))
            for d3_ax, d3_variant in zip(d3_axes, d3_live):
                d3_ax.imshow(d3_live[d3_variant][:, :16], cmap="RdBu_r", aspect="auto")
                d3_ax.set(title=d3_variant + " · first 16 components", xlabel="Coordinate", ylabel="Training row", yticks=[0, 1])
            d3_figure.tight_layout(); plt.show(); plt.close(d3_figure)
            # Release weights; the canonical full-cache workflow owns its own encoder loading.
            del d3_encoder, d3_tokenizer
            gc.collect()
            print("STOP: inspect the two vectors before continuing. No classifier or test scoring here.")
        '''),
        ('markdown', 'day3-full-guide', '''
            ### Continue · Extract or load the full cache

            The next cell runs the canonical stage 04 workflow **once**, then reuses a completed,
            source-matched run on repetition. `live_example=False` skips the optional example
            only when a full cache exists. **Without a cache it still loads the encoder and
            extracts all rows**, including an internal two-training-row consistency check.
            Our earlier live checkpoint is separate; do not describe a fresh-runtime run as cached-only.
            Test inputs may be embedded without accessing their masked labels or scoring them.
            Scaling and logistic regression fit on training rows only.
        '''),
    ])


RUN_SOURCE = '''# Canonical stage 04: validation only; no refitting when this completed cell is rerun.
d3_identity = {"sources": d3_source_identity, "generations": {v: f.attrs["dataset_generation_sha256"] for v, f in d3_samples.items()}}
d3_identity_path = d3_root / "day3_teaching_identity.json"
if any((d3_root / name).exists() for name in ("frozen_manifest.json", "test_results.json")):
    raise RuntimeError("Frozen/revealed workspace: do not restart development.")
if (d3_root / "embedding_run.json").exists():
    if not d3_identity_path.exists() or json.loads(d3_identity_path.read_text()) != d3_identity:
        raise ValueError("Missing/different Day 3 identity: preserve outputs and restore a complete matching run.")
    print("Reading completed stage 04; no extraction or fitting repeated.")
else:
    run_foundation(output_dir=d3_root, live_example=False)
    write_json(d3_identity_path, d3_identity)
'''


def after_workflow(factory):
    alignment = (ROOT / 'instructor/completed/day3_alignment.py').read_text()
    return emit(factory, [
        ('markdown', 'day3-cache-guide', '''
            ### Inspect and verify the real cache

            Generation identity, IDs, per-sequence hashes, revision, pooling, dimensions and
            finiteness are checked before use. `load_embedding_cache` returns rows in dataset
            order, not disk order. Classifier readback checks matching validation IDs and labels.
        '''),
        ('code', 'day3-readback', '''
            d3_run = json.loads((d3_root / "embedding_run.json").read_text())
            assert json.loads(d3_identity_path.read_text()) == d3_identity
            assert d3_run["model_id"] == MODEL_ID and d3_run["revision"] == REVISION and d3_run["pooling"] == POOLING
            d3_metrics = pd.read_csv(d3_root / "embedding_validation.csv")
            assert len(d3_metrics) == 2 and set(d3_metrics.variant) == set(d3_samples)
            for d3_variant, d3_frame in d3_samples.items():
                d3_record = d3_run["runs"][d3_variant]
                assert not d3_record["test_evaluated"]
                assert d3_record["dataset_generation_sha256"] == d3_frame.attrs["dataset_generation_sha256"]
                for d3_split, d3_key in [("train", "training_ids"), ("validation", "validation_ids")]:
                    assert d3_record[d3_key] == d3_frame.loc[d3_frame.split.eq(d3_split), "sample_id"].tolist()
                d3_features = load_embedding_cache(d3_root / "embeddings" / f"{d3_variant}.npz", d3_frame)
                d3_training = d3_frame.split.eq("train").to_numpy()
                d3_validation = d3_frame.loc[d3_frame.split.eq("validation")]
                np.testing.assert_allclose(d3_live[d3_variant], d3_features[d3_training][:2], atol=1e-4, rtol=1e-4)
                d3_classifier = joblib.load(d3_root / "models" / d3_variant / "foundation.joblib")
                np.testing.assert_allclose(d3_classifier[0].mean_, d3_features[d3_training].mean(axis=0, dtype=np.float64), atol=1e-12)
                d3_saved = pd.read_csv(d3_root / "models" / d3_variant / "foundation_validation_predictions.csv")
                assert d3_saved.sample_id.is_unique and set(d3_saved.sample_id) == set(d3_validation.sample_id)
                d3_saved = d3_saved.set_index("sample_id").loc[d3_validation.sample_id]
                assert d3_saved.label.tolist() == d3_validation.label.tolist()
                assert d3_saved.group_id.tolist() == d3_validation.group_id.tolist()
                d3_probability = d3_classifier.predict_proba(d3_features[d3_frame.split.eq("validation")])[:, 1]
                np.testing.assert_allclose(d3_probability, d3_saved.probability, atol=1e-12, rtol=0)
                d3_recomputed = validation_metrics(d3_validation.label, d3_probability)
                d3_metric = d3_metrics.loc[d3_metrics.variant.eq(d3_variant)].iloc[0]
                assert d3_metric.evaluation_split == "validation" and d3_metric.decision_threshold == 0.5
                assert d3_metric.sample_count == len(d3_validation)
                for d3_key in ["roc_auc", "average_precision"]:
                    np.testing.assert_allclose(d3_recomputed[d3_key], d3_metric[d3_key], atol=1e-12, rtol=0)
                print(d3_variant, "cache:", d3_features.shape, "ID-aligned; validation only")
            print(d3_metrics[["variant", "method", "roc_auc", "average_precision"]].to_string(index=False))
        '''),
        ('markdown', 'day3-alignment-guide', '''
            ### Section 4 · Repair a synthetic join

            Predict what taking the first cache rows would do, then run the completed example.
            These two-feature numbers are **synthetic**, not output from the encoder.
            Work in pairs or follow the demonstration; nothing is submitted.
        '''),
        ('code', 'day3-alignment', alignment),
        ('code', 'day3-alignment-failures', '''
            # Reordering is harmless after joining by ID. Missing/duplicate IDs must stop.
            def d3_align(requested, cached):
                if not requested.sample_id.is_unique or not cached.sample_id.is_unique:
                    raise ValueError("Duplicate sample ID")
                if set(requested.sample_id) != set(cached.sample_id):
                    raise ValueError("Missing/unexpected sample ID")
                return cached.set_index("sample_id").loc[requested.sample_id]
            pd.testing.assert_frame_equal(d3_align(metadata, cache), d3_align(metadata, cache.iloc[::-1]))
            for d3_bad in [cache.iloc[:-1], pd.concat([cache, cache.iloc[:1]])]:
                try:
                    d3_align(metadata, d3_bad)
                except ValueError as d3_error:
                    print("Stopped as intended:", d3_error)
                else:
                    raise AssertionError("Identity failure was not rejected")
            print("Positional pairing would start with", cache.sample_id.iloc[0], "instead of", metadata.sample_id.iloc[0])
        '''),
        ('markdown', 'day3-comparison-guide', '''
            ### Section 5 · Same validation rows, four workflows

            These readbacks use the current generated data and saved validation predictions.
            Make a prediction before running. No tuning follows this comparison during rehearsal.
            ROC-AUC is primary; AP supports interpretation. This is a simulation, not promoter validation.
        '''),
        ('code', 'day3-comparison', '''
            d3_comparison = pd.concat([d2_metrics, d3_metrics], ignore_index=True)
            assert len(d3_comparison) == 8 and d3_comparison.evaluation_split.eq("validation").all()
            d3_methods = ["logistic_regression", "random_forest", "cnn", "foundation"]
            d3_names = ["Counts + LR", "Counts + forest", "CNN", "Frozen NT + LR"]
            d3_figure, d3_axes = plt.subplots(1, 2, figsize=(12, 4))
            for d3_ax, d3_variant in zip(d3_axes, ["simple", "interaction"]):
                d3_table = d3_comparison.loc[d3_comparison.variant.eq(d3_variant)].set_index("method").loc[d3_methods]
                d3_ax.barh(d3_names, d3_table.roc_auc, color=["#0072B2", "#D55E00", "#7B4FA3", "#697782"])
                d3_ax.axvline(0.5, color="black", linestyle="--", linewidth=1)
                d3_ax.set(xlim=(0, 1), xlabel="Validation ROC-AUC", title=d3_variant)
            d3_figure.tight_layout(); plt.show(); plt.close(d3_figure)
            print(d3_comparison[["variant", "method", "sample_count", "roc_auc", "average_precision"]].to_string(index=False))
            print("No universal ranking. No protected test scores calculated.")
        '''),
        ('markdown', 'day3-stop-before-freeze', '''
            ## STOP · Section 6 requires the instructor's freeze checklist

            All datasets/splits, four workflows, preprocessing, checkpoint policy, embedding
            contract/cache, validation predictions, metric policy and threshold must be fixed.
            Record the instructor's name, time and authorization in the class notes. If anything
            is missing, stop. The next **stage 05** cell writes a freeze only; it does not reveal.

            The planned reveal is a **separate instructor action**, deliberately absent from
            executable notebook cells. Do not remove a guard or marker to permit a rerun.
            After the planned reveal, report the fixed results; new tuning needs fresh data.
        '''),
    ])
