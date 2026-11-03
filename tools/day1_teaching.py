"""Focused Day 1 notebook checkpoints around the canonical paired workflow."""
from textwrap import dedent


def emit(factory, content):
    return [factory(kind, dedent(source).strip() + "\n", name) for kind, name, source in content]


def before_workflow(factory):
    return emit(factory, [
        ("markdown", "section-4", """
            ## Section 4: inspect validation predictions

            Continue from Section 3 in this same Colab runtime. Use its fitted model;
            no new fitting is needed. Run the two working cells below, change only
            `s4_threshold`, and explain what happens to the calls. The recorded course
            comparison remains at 0.5. No test table or planting truth is loaded.
        """),
        ("code", "s4-probabilities", """
            # One probability per validation row, in the same row order.
            s4_probabilities = s3_classifier.predict_proba(s3_x_validation)[:, 1]
            s4_rows = s3_validation[["sample_id", "label"]].copy()
            s4_rows["probability"] = s4_probabilities
            assert s4_rows.sample_id.is_unique
            s4_reference_auc = roc_auc_score(s4_rows.label, s4_probabilities)
            print(s4_rows.head().to_string(index=False))
            print("ROC-AUC from probabilities:", round(s4_reference_auc, 4))
        """),
        ("code", "s4-decisions", """
            from sklearn.metrics import f1_score

            s4_threshold = 0.5  # Then try 0.8 or 0.3; rerun this cell only.
            s4_predictions = (s4_probabilities >= s4_threshold).astype(int)
            s4_matrix = confusion_matrix(s4_rows.label, s4_predictions, labels=[0, 1])
            s4_tn, s4_fp, s4_fn, s4_tp = s4_matrix.ravel()
            s4_precision = s4_tp / (s4_tp + s4_fp) if s4_tp + s4_fp else float("nan")
            s4_recall = s4_tp / (s4_tp + s4_fn) if s4_tp + s4_fn else float("nan")
            print("Rows = observed A/B; columns = predicted A/B")
            print(s4_matrix)
            print(f"TP={s4_tp}; FP={s4_fp}; FN={s4_fn}; TN={s4_tn}")
            print(f"Precision = TP/(TP+FP) = {s4_precision:.4f}")
            print(f"Recall = TP/(TP+FN) = {s4_recall:.4f}")
            if s4_tp + s4_fp:
                np.testing.assert_allclose(s4_precision, precision_score(s4_rows.label, s4_predictions))
            else:
                print("No positive calls: precision is undefined (NaN), not observed zero.")
            np.testing.assert_allclose(s4_recall, recall_score(s4_rows.label, s4_predictions))
            print("F1:", round(f1_score(s4_rows.label, s4_predictions, zero_division=0), 4))
            s4_auc = roc_auc_score(s4_rows.label, s4_probabilities)
            assert s4_auc == s4_reference_auc  # Decisions change; scores/ranking do not.
            print("Unchanged ROC-AUC:", round(s4_auc, 4))
            ConfusionMatrixDisplay(s4_matrix, display_labels=["A / 0", "B / 1"]).plot(
                cmap="Blues", colorbar=False)
            plt.title(f"Validation calls at threshold {s4_threshold}")
            plt.show()
            plt.close("all")
        """),
        ("markdown", "section-4-stop", """
            **STOP — end of Section 4.** Describe one changed count after moving the
            threshold. This is a decision-rule exploration, not a new fitted model or
            an official replacement of the 0.5 threshold. Empty positive selections
            have undefined precision; libraries may use a zero-division convention.

            ## Section 5: compare logistic regression and random forest

            At the instructor's comparison checkpoint, run the **complete stage 01
            workflow immediately below once**. It regenerates the same deterministic
            primary dataset and fits both models, writing their normal artifacts.
            It does not reuse the live Section 3 classifier object. The forest uses
            100 trees, bootstrapped training rows, and random feature candidates per split.
            Validation supports comparison; test results are not scored. Read the
            paired outputs in the cells after the workflow. Setup is already complete.
            **Run all also runs this paired workflow.**
        """),
    ])


def after_workflow(factory):
    return emit(factory, [
        ("code", "s5-comparison", """
            s5_comparison = pd.read_csv(s3_destination / "classical_validation.csv")
            assert s5_comparison.evaluation_split.eq("validation").all()
            assert s5_comparison.sample_count.eq(len(s3_validation)).all()
            assert s5_comparison.decision_threshold.eq(0.5).all()
            print(s5_comparison[["method", "roc_auc", "average_precision", "precision", "recall"]]
                  .to_string(index=False))
            print("Same validation rows; same 0.5 cutoff; ROC-AUC was prespecified.")
            s5_lr = pd.read_csv(s3_destination / "validation_predictions.csv")
            s5_rf = pd.read_csv(s3_destination / "random_forest_validation_predictions.csv")
            assert set(s5_lr.sample_id) == set(s5_rf.sample_id) == set(s3_validation.sample_id)
            s5_paired = s5_lr.merge(s5_rf, on="sample_id", suffixes=("_lr", "_rf"),
                                    validate="one_to_one")
            assert s5_paired.label_lr.eq(s5_paired.label_rf).all()
            s5_paired["prediction_rf"] = (s5_paired.probability_rf >= 0.5).astype(int)
            s5_disagreements = s5_paired[s5_paired.prediction != s5_paired.prediction_rf]
            s5_example = s5_disagreements.head(1) if len(s5_disagreements) else s5_paired.head(1)
            print("One decision disagreement (or one probability comparison if none):")
            print(s5_example[["sample_id", "label_lr", "probability_lr", "probability_rf"]]
                  .to_string(index=False))
            # Verify the regenerated paired workflow has the same development data.
            s5_generation = validate_generation(s3_destination)
            assert s5_generation == s3_generation
            s5_ordered = s3_validation[["sample_id", "label"]].merge(
                s5_lr, on="sample_id", validate="one_to_one", suffixes=("_tutorial", "_run"))
            assert s5_ordered.label_tutorial.eq(s5_ordered.label_run).all()
            np.testing.assert_allclose(s5_ordered.probability, s4_probabilities, atol=1e-10)
        """),
        ("markdown", "section-5-stop", """
            **STOP — end of Section 5.** Describe what the observed comparison supports,
            without assuming the forest wins or claiming a universal model ranking.
            Feature-importance interpretation belongs to the next section.

            ## Section 6: explain a validation prediction

            Reuse the Section 3 fitted classifier and count mapping for a local
            explanation. Read the paired workflow's global coefficient/importance
            tables afterward. No refitting, test scoring or extra data copy is needed.
        """),
        ("code", "s6-local-explanation", """
            from scipy.special import expit

            s6_row_index = 0  # Optional: select another validation row and rerun.
            s6_record = s3_validation.iloc[s6_row_index]
            s6_counts = s3_x_validation[s6_row_index].toarray().ravel()
            s6_weights = s3_classifier.coef_[0]
            s6_bias = float(s3_classifier.intercept_[0])
            s6_contributions = s6_counts * s6_weights
            s6_z = float(s6_bias + s6_contributions.sum())
            s6_p = float(expit(s6_z))
            np.testing.assert_allclose(s6_p,
                s3_classifier.predict_proba(s3_x_validation[s6_row_index])[0, 1], atol=1e-12)
            s6_table = pd.DataFrame({"kmer": s3_words, "count": s6_counts,
                                    "coefficient": s6_weights, "contribution": s6_contributions})
            s6_top = s6_table.loc[s6_table.contribution.abs().nlargest(8).index]
            s6_remainder = float(s6_contributions.sum() - s6_top.contribution.sum())
            print("Validation ID:", s6_record.sample_id)
            print(s6_top.sort_values("contribution").to_string(index=False))
            print(f"Bias {s6_bias:.6f}; other contributions {s6_remainder:.6f}")
            print(f"FULL sum z={s6_z:.6f}; sigmoid P(B)={s6_p:.6f}")
            s6_view = s6_top.sort_values("contribution")
            plt.figure(figsize=(8, 4))
            plt.barh(s6_view.kmer, s6_view.contribution,
                     color=["#D55E00" if value >= 0 else "#0072B2"
                            for value in s6_view.contribution])
            plt.axvline(0, color="#697782", linewidth=1)
            plt.xlabel("Contribution to score (count × coefficient)")
            plt.title("Selected contributions; full sum includes all features and bias")
            plt.tight_layout()
            plt.show()
            plt.close("all")
        """),
        ("code", "s6-global-explanation", """
            s6_coefficients = pd.read_csv(s3_destination / "kmer_coefficients.csv")
            s6_importance = pd.read_csv(s3_destination / "random_forest_importance.csv")
            s6_columns = ["kmer", "motif_window_probability", "motif_vs_background_enrichment"]
            print("Signed global coefficients; not count-dependent local contributions:")
            print(s6_coefficients[["coefficient"] + s6_columns].head(6).to_string(index=False))
            print("Nonnegative global forest impurity importance; no positive/negative direction:")
            print(s6_importance[["importance"] + s6_columns].head(6).to_string(index=False))
            print("Enrichment = mean internal PPM-window probability / (1/256).")
            print("It excludes boundary windows and class mixtures; it is not a causal claim.")
            assert s6_importance.importance.ge(0).all()
            np.testing.assert_allclose(s6_importance.importance.sum(), 1.0)
            np.testing.assert_allclose(s6_coefficients.motif_window_probability.sum(), 1.0)
            print("Discuss: which clue mattered here, and what would you still want to check?")
        """),
        ("markdown", "day-1-end", """
            **End of Day 1.** You followed DNA → counts → fitting → probabilities →
            evaluation → explanation. Coefficients, local contributions, forest importance
            and distribution-derived enrichment have different meanings and scales.
            None establishes a real regulatory mechanism. Related families or batch
            effects require appropriate evaluation; the separate leakage notebook is an
            extension. Tomorrow we keep sequence position and learn representations.
            No homework is required. No protected test result was calculated here.
        """),
    ])
