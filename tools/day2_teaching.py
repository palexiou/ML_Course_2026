"""Guided Day 2 inspection cells for the existing combined Days 2–3 notebook."""
from textwrap import dedent
import json


def emit(factory, content):
    return [factory(kind, dedent(source).strip() + '\n', name) for kind, name, source in content]


def before_workflow(factory, source_identity):
    return emit(factory, [
        ('markdown', 'day2-section-5', '''
            ## Day 2 · Section 5: train, inspect and compare

            Route: **GitHub → Open in Colab → setup → shared definitions → stage 03 definitions
            → this checkpoint**. Instructor demonstration and optional follow-along are both valid.
            Setup and computation are inside the lesson; timings require classroom rehearsal.
            Do not run all: stages 04–05 belong to Day 3. No homework or submission.

            Run the supplied workflow **once**, then inspect without refitting. It fits three
            methods on both dataset variants. Initially we display only the primary PPM experiment.
            The declared CPU run is seed 2026, 24 epochs, batch 64, Adam 0.002, two threads.
            One-hot input is N×4×160 in A/C/G/T order; one logit per sequence, sigmoid at inference.
        '''),
        ('code', 'day2-run-identity', 'd2_source_identity = ' + repr(source_identity) + '\nd2_root = Path("course_output")\n'),
    ])


RUN_SOURCE = dedent('''
    # Re-running this cell reads a completed compatible run; it does not fit again.
    from contextlib import redirect_stdout
    import io

    if any((d2_root / name).exists() for name in ("frozen_manifest.json", "test_results.json")):
        raise RuntimeError("This workspace is frozen/revealed; do not restart development here.")
    d2_identity_path = d2_root / "day2_teaching_identity.json"
    d2_identity = {"sources": d2_source_identity, "seed": 2026, "epochs": 24}
    if (d2_root / "representation_run.json").exists():
        if not d2_identity_path.exists() or json.loads(d2_identity_path.read_text()) != d2_identity:
            raise ValueError("Existing run has a different or missing teaching identity. Preserve it; restore a complete compatible run or use a fresh runtime.")
        print("Reading the existing completed run; no fitting repeated.")
    else:
        if d2_root.exists() and any(d2_root.iterdir()):
            raise ValueError("Incomplete/existing workspace: preserve it and use a fresh runtime.")
        print("Running stage 03 once (both variants); inspect primary results first.")
        with redirect_stdout(io.StringIO()):
            run_representations(output_dir=d2_root, seed=2026, epochs=24, show_plot=False)
        write_json(d2_identity_path, d2_identity)
        print("Stage 03 complete. Validation only; continue below.")
''').strip() + '\n'


def after_workflow(factory):
    return emit(factory, [
        ('markdown', 'day2-readback-guide', '''
            ### Read the primary run

            Check dataset/source identity and row alignment before interpreting the result.
            Training loss averages minibatch losses during updates. Validation ROC-AUC selects
            the earliest highest-scoring epoch after **all 24 epochs**, not early stopping.
            Test labels/results do not guide any decision. File hashes verify identity only.
        '''),
        ('code', 'day2-readback', '''
            from collections import Counter
            import joblib

            d2_run = json.loads((d2_root / "representation_run.json").read_text())
            assert d2_run["seed"] == 2026 and d2_run["device"] == "cpu"
            assert json.loads(d2_identity_path.read_text()) == d2_identity
            d2_metrics = pd.read_csv(d2_root / "representation_validation.csv")
            d2_predictions = pd.read_csv(d2_root / "representation_validation_predictions.csv")
            d2_data = {}
            d2_models = {}
            d2_histories = {}
            d2_selected = {}
            d2_methods = ["logistic_regression", "random_forest", "cnn"]
            assert set(d2_metrics.variant) == {"simple", "interaction"}
            assert set(d2_predictions.variant) == {"simple", "interaction"}
            for d2_variant, d2_size in [("simple", 240), ("interaction", 96)]:
                d2_dataset_dir = d2_root / "datasets" / d2_variant
                d2_generation = validate_generation(d2_dataset_dir)
                d2_record = d2_run["runs"][d2_variant]
                assert d2_record["dataset_generation_sha256"] == file_hash(d2_dataset_dir / "generation.json")
                # Generation digest binds complete saved files; run dataset hash has masked test labels.
                assert not d2_record["test_evaluated"] and d2_record["cnn_epochs"] == 24
                assert d2_record["cnn_selection"] == "highest validation ROC-AUC, earliest tie"
                if d2_variant == "simple":
                    assert d2_generation["settings_sha256"] == settings_fingerprint(simulation_settings(SimulationConfig()))
                else:
                    assert d2_generation["settings"] == {"seed": 2026, "pair_count": 240, "positions": [32, 80], "matching_flanks": 6, "lesson": "fixed-position motif order, not universal CNN superiority"}
                d2_train = pd.read_csv(d2_dataset_dir / "train.csv")
                d2_validation = pd.read_csv(d2_dataset_dir / "validation.csv")
                assert d2_train.sample_id.tolist() == d2_record["training_ids"]
                assert d2_validation.sample_id.tolist() == d2_record["validation_ids"]
                assert d2_validation.sample_id.is_unique and len(d2_validation) == d2_size
                assert d2_validation.split.eq("validation").all()
                d2_data[d2_variant] = d2_validation
                d2_variant_metrics = d2_metrics.loc[d2_metrics.variant.eq(d2_variant)]
                assert len(d2_variant_metrics) == 3 and set(d2_variant_metrics.method) == set(d2_methods)
                assert d2_variant_metrics.evaluation_split.eq("validation").all()
                for d2_method in d2_methods:
                    d2_saved = d2_predictions.loc[d2_predictions.variant.eq(d2_variant) & d2_predictions.method.eq(d2_method)]
                    assert len(d2_saved) == d2_size and d2_saved.sample_id.is_unique
                    d2_aligned = d2_validation[["sample_id", "group_id", "label"]].merge(d2_saved, on="sample_id", validate="one_to_one", suffixes=("", "_saved"))
                    assert len(d2_aligned) == d2_size
                    assert d2_aligned.label.eq(d2_aligned.label_saved).all()
                    assert d2_aligned.group_id.eq(d2_aligned.group_id_saved).all()
                    d2_recomputed = validation_metrics(d2_aligned.label, d2_aligned.probability)
                    d2_metric = d2_variant_metrics.loc[d2_variant_metrics.method.eq(d2_method)].iloc[0]
                    assert d2_metric.sample_count == d2_size and d2_metric.decision_threshold == 0.5
                    for d2_key in ["roc_auc", "average_precision"]:
                        np.testing.assert_allclose(d2_recomputed[d2_key], d2_metric[d2_key], rtol=0, atol=1e-12)
                d2_history = pd.read_csv(d2_root / "models" / d2_variant / "cnn_history.csv")
                assert d2_history.epoch.tolist() == list(range(1, 25))
                assert np.isfinite(d2_history.to_numpy()).all()
                d2_selected[d2_variant] = int(d2_history.loc[d2_history.validation_roc_auc.idxmax(), "epoch"])
                d2_histories[d2_variant] = d2_history
                d2_checkpoint = torch.load(d2_root / "models" / d2_variant / "cnn.pt", map_location="cpu", weights_only=True)
                assert d2_checkpoint["sequence_length"] == 160
                d2_model = SequenceCNN(160)
                d2_model.load_state_dict(d2_checkpoint["state_dict"])
                d2_models[d2_variant] = d2_model.eval()
                d2_saved_cnn = d2_predictions.loc[d2_predictions.variant.eq(d2_variant) & d2_predictions.method.eq("cnn")].set_index("sample_id").loc[d2_validation.sample_id, "probability"]
                np.testing.assert_allclose(predict_cnn(d2_model, d2_validation.sequence), d2_saved_cnn, rtol=0, atol=1e-6)
                d2_saved_auc = d2_variant_metrics.loc[d2_variant_metrics.method.eq("cnn"), "roc_auc"].iloc[0]
                np.testing.assert_allclose(d2_history.validation_roc_auc.max(), d2_saved_auc, rtol=0, atol=1e-12)
            print("Source and generation identities checked; matching validation rows and metrics verified.")
            print("Primary selected epoch:", d2_selected["simple"], "of 24 (earliest highest validation ROC-AUC)")
            print("Primary metrics:")
            print(d2_metrics.loc[d2_metrics.variant.eq("simple"), ["method", "roc_auc", "average_precision"]].to_string(index=False))
            print("CPU aggregate primary-workflow seconds (all three methods):", round(d2_run["runs"]["simple"]["seconds"], 2))
        '''),
        ('code', 'day2-history', '''
            d2_history = d2_histories["simple"]
            d2_figure, d2_axes = plt.subplots(1, 2, figsize=(11, 3.5))
            for d2_axis, d2_key, d2_title, d2_color in zip(d2_axes, ["training_loss", "validation_roc_auc"], ["Training loss", "Validation ROC-AUC"], ["#0072B2", "#D55E00"]):
                d2_axis.plot(d2_history.epoch, d2_history[d2_key], color=d2_color, marker="o", markersize=3)
                d2_axis.axvline(d2_selected["simple"], color="#697782", linestyle="--", label="Selected epoch")
                d2_axis.set(xlabel="Epoch", ylabel=d2_title)
            d2_axes[1].legend()
            d2_figure.tight_layout()
            plt.show()
            plt.close(d2_figure)
        '''),
        ('markdown', 'day2-inference-guide', '''
            ### Inspect a prediction, then one response channel

            Start at row 0 and channel 0. Change `d2_row_index` or `d2_channel` and rerun
            **only the next cell**; fitted weights stay fixed. The stems show second-convolution
            post-ReLU responses at sequence positions, not attribution or biological proof.
            An error or a success on one record does not estimate general performance.
        '''),
        ('code', 'day2-inference', '''
            d2_row_index = 0
            d2_channel = 0
            assert 0 <= d2_row_index < len(d2_data["simple"]) and 0 <= d2_channel < 16
            d2_row = d2_data["simple"].iloc[d2_row_index]
            with torch.inference_mode():
                d2_inputs = one_hot([d2_row.sequence])
                d2_probability = float(torch.sigmoid(d2_models["simple"](d2_inputs))[0])
                d2_response = d2_models["simple"].filters(d2_inputs)[0].numpy()
            d2_reference = d2_predictions.loc[d2_predictions.variant.eq("simple") & d2_predictions.method.eq("cnn") & d2_predictions.sample_id.eq(d2_row.sample_id), "probability"].item()
            np.testing.assert_allclose(d2_probability, d2_reference, rtol=0, atol=1e-6)
            print("Validation ID:", d2_row.sample_id, "sequence:", d2_row.sequence)
            print(f"P(B)={d2_probability:.6f}; observed {'B' if d2_row.label else 'A'}; fixed cutoff 0.5")
            plt.figure(figsize=(11, 3))
            plt.vlines(np.arange(160), 0, d2_response[d2_channel], color="#0072B2")
            plt.xlabel("Position (zero-based)")
            plt.ylabel(f"Channel {d2_channel} response")
            plt.tight_layout()
            plt.show()
            plt.close("all")
        '''),
        ('markdown', 'day2-section-6', '''
            ## Day 2 · Section 6: same counts, different arrangement

            The separate engineered control uses fixed TATAAATG / CGGACGTC blocks, matching
            six-base flanks and shared backgrounds. Partners swap slots and labels but remain
            in the same split. Complete overlapping four-mer equality forces equal scores for
            any fixed bag-only predictor; balanced opposite-label pairs imply ROC-AUC 0.5.
            Position-aware input retains a distinction, but actual learning is an observed result.

            The stage 03 run already produced these models; **do not train again**.
            This is a five-minute inspection, not a new architecture search.
        '''),
        ('code', 'day2-pair', '''
            d2_group_index = 0  # Optional: change the group, rerun this cell only.
            d2_control = pd.read_csv(d2_root / "models" / "interaction" / "controlled_order_changes.csv")
            assert d2_control.sample_id.is_unique and len(d2_control) == 96
            d2_pairs = d2_data["interaction"].merge(d2_control, on=["sample_id", "group_id", "label"], validate="one_to_one")
            assert len(d2_pairs) == 96
            d2_pair_groups = list(d2_pairs.groupby("group_id", sort=False))
            assert len(d2_pair_groups) == 48
            for d2_group_id, d2_pair in d2_pair_groups:
                assert len(d2_pair) == 2 and set(d2_pair.label) == {0, 1}
                d2_bags = [Counter(seq[i:i+4] for i in range(len(seq)-3)) for seq in d2_pair.sequence]
                assert d2_bags[0] == d2_bags[1] and sum(d2_bags[0].values()) == 157
                for d2_method in d2_methods:
                    d2_reference = d2_predictions.loc[d2_predictions.variant.eq("interaction") & d2_predictions.method.eq(d2_method)].set_index("sample_id").loc[d2_pair.sample_id, "probability"]
                    np.testing.assert_allclose(d2_pair[f"{d2_method}_probability"], d2_reference, rtol=0, atol=1e-6 if d2_method == "cnn" else 1e-12)
                    if d2_method != "cnn":
                        np.testing.assert_allclose(d2_pair[f"{d2_method}_probability"].iloc[0], d2_pair[f"{d2_method}_probability"].iloc[1], rtol=0, atol=1e-12)
            for d2_method in d2_methods[:2]:
                np.testing.assert_allclose(validation_metrics(d2_pairs.label, d2_pairs[f"{d2_method}_probability"])["roc_auc"], 0.5, rtol=0, atol=1e-12)
            assert 0 <= d2_group_index < len(d2_pair_groups)
            d2_group_id, d2_pair = d2_pair_groups[d2_group_index]
            print("Group:", d2_group_id, "— opposite labels; all 157 four-mer windows give identical complete Counters.")
            print(d2_pair[["sample_id", "label", "logistic_regression_probability", "random_forest_probability", "cnn_probability"]].to_string(index=False))
            for d2_record in d2_pair.itertuples():
                print("B" if d2_record.label else "A", d2_record.sequence)
            print("Observed control metrics:")
            print(d2_metrics.loc[d2_metrics.variant.eq("interaction"), ["method", "roc_auc", "average_precision"]].to_string(index=False))
            print("Fixed-slot control only: no claim about arbitrary position, strand or biological grammar.")
        '''),
        ('markdown', 'day2-stop', '''
            # STOP — end of Day 2

            Discuss what information your own task should retain. Keep this runtime and its
            complete `course_output/` artifacts for Day 3; saving the notebook alone does not
            save runtime files. The figures above are validation development evidence.
            No test results have been calculated or used to guide a choice.

            **Do not continue to stage 04 embeddings or stage 05 freeze today.**
            Those belong to Day 3. Run all would cross this teaching boundary.
            The next lesson asks whether we can reuse features learned before our task.
        '''),
    ])
