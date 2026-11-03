"""Build completed, self-contained notebooks from the canonical course modules."""

import ast
import hashlib
import json
from pathlib import Path
from textwrap import dedent
from day1_teaching import before_workflow, after_workflow
import day2_teaching
import day3_teaching
import day4_teaching

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "course_code"
DESTINATION = ROOT / "notebooks"


def without_local_imports(path: Path, remove_main: bool = False) -> str:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    excluded: set[int] = set()
    for node in ast.parse(source).body:
        local_import = isinstance(node, ast.ImportFrom) and node.module in {"course_core", "course_inference"}
        main_guard = isinstance(node, ast.If) and ast.unparse(node.test) == "__name__ == '__main__'"
        if local_import or (remove_main and main_guard):
            excluded.update(range(node.lineno - 1, node.end_lineno or node.lineno))
    return "".join(line for index, line in enumerate(lines) if index not in excluded).strip() + "\n"


def cell(kind: str, source: str, name: str) -> dict:
    result: dict = {"cell_type": kind, "id": name, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        compile(source, name, "exec")
        result.update(execution_count=None, outputs=[])
    return result


def requirements(advanced: bool) -> list[str]:
    paths = [SOURCE / "requirements.txt"]
    if advanced:
        paths.append(SOURCE / "requirements-ml.txt")
    return [line for path in paths for line in path.read_text().splitlines()
            if line and not line.startswith(("-r", "#"))]


def section3_cells() -> list[dict]:
    """The short teaching route; canonical stage 01 remains a separate later run."""
    content = [
        ("markdown", "section-3", r"""
            ## Section 3: from DNA counts to probability and loss

            Open this completed GitHub notebook with **Open in Colab**, run **setup** and
            the two **definition** cells above, then run the five steps below in order.
            An instructor can select these cells for a roughly five-minute demonstration
            after setup; students may follow along or try the small changes suggested here.
            No coding from scratch or submission is required. Setup time is separate;
            this is a suggested route, not a measured classroom timing.

            We use **TRAIN / VALIDATION ONLY**. Predict one validation record before
            revealing its known label, then ask how much loss that prediction incurs.
            Stop at the marked boundary before validation metrics and forests.
        """),
        ("markdown", "s3-data-guide", r"""
            ### 1. Prepare the same primary dataset

            Use the canonical 15-position probability motif, 0.95/0.05 planting and
            160-base sequences. The generator saves the complete fixed split in the normal
            `simple_signal_output/` location. Only training and validation tables are
            loaded for this lesson; test file bytes are hashed solely to check identity.
            Existing artifacts must match the canonical configuration and file hashes.
        """),
        ("code", "s3-data", r"""
            s3_config = SimulationConfig()
            s3_destination = Path("simple_signal_output")
            if any((s3_destination / marker).exists()
                   for marker in ("frozen_manifest.json", "test_results.json")):
                raise RuntimeError("This experiment is frozen or revealed. Use a new development directory.")
            if not (s3_destination / "generation.json").exists():
                if s3_destination.exists() and any(s3_destination.iterdir()):
                    raise ValueError("Existing artifacts lack generation identity; preserve them and use a fresh runtime.")
                s3_generated, s3_truth = generate_course_dataset(s3_config)
                s3_generated = assign_splits(s3_generated, s3_config.seed)
                save_dataset(s3_destination, s3_generated, s3_truth, simulation_settings(s3_config))
                del s3_generated, s3_truth
            s3_generation = validate_generation(s3_destination)
            assert s3_generation["settings_sha256"] == settings_fingerprint(simulation_settings(s3_config))
            s3_train = pd.read_csv(s3_destination / "train.csv")
            s3_validation = pd.read_csv(s3_destination / "validation.csv")
            assert s3_train["split"].eq("train").all()
            assert s3_validation["split"].eq("validation").all()
            assert set(s3_train.sample_id).isdisjoint(s3_validation.sample_id)
            assert set(s3_train.group_id).isdisjoint(s3_validation.group_id)
            print(f"TRAIN: {len(s3_train)}; VALIDATION: {len(s3_validation)}. No test table loaded.")
            print("Settings SHA-256:", s3_generation["settings_sha256"])
            print("Generation SHA-256:", file_hash(s3_destination / "generation.json"))
        """),
        ("markdown", "s3-counts-guide", r"""
            ### 2. Inspect DNA and its count row

            Fit the vocabulary on **training sequences only**; transform validation with
            that same vocabulary. Only DNA enters the vectorizer: labels, IDs, groups,
            split and planting truth are excluded. The model uses every count, including
            zeros; we display ten nonzero entries to keep the row readable.

            Optional: change `s3_row_index` to `1`, then rerun this step and steps 3–5.
            Which counts and probability change? Keep model and dataset settings fixed.
        """),
        ("code", "s3-counts", r"""
            s3_vectorizer = CountVectorizer(
                analyzer="char", ngram_range=(s3_config.kmer_length, s3_config.kmer_length),
                lowercase=False,
            )
            s3_x_train = s3_vectorizer.fit_transform(s3_train["sequence"])
            s3_x_validation = s3_vectorizer.transform(s3_validation["sequence"])
            s3_words = s3_vectorizer.get_feature_names_out()
            s3_row_index = 0  # Optional: try another validation row; rerun steps 2–5.
            s3_record = s3_validation.iloc[s3_row_index]
            s3_x_row = s3_x_validation[s3_row_index]
            s3_count_row = pd.Series(s3_x_row.toarray().ravel(), index=s3_words, name="count")
            print("Validation ID (metadata only):", s3_record["sample_id"])
            print("DNA:", s3_record["sequence"])
            print(f"{len(s3_words)} training-vocabulary features; count sum = {s3_count_row.sum()}")
            print(s3_count_row[s3_count_row > 0].head(10).to_string())
        """),
        ("markdown", "s3-fit-guide", r"""
            ### 3. Learn the weights from training labels

            Each k-mer gets a coefficient; the intercept is the bias. A positive
            coefficient raises the score for class B when that count increases and
            other counts stay fixed. These learned associations are not causal evidence.
            We keep the same logistic-regression defaults as the complete workflow.
        """),
        ("code", "s3-fit", r"""
            s3_classifier = LogisticRegression(max_iter=2000)
            s3_classifier.fit(s3_x_train, s3_train["label"])
            assert s3_classifier.classes_.tolist() == [0, 1]
            s3_coefficients = pd.Series(s3_classifier.coef_[0], index=s3_words, name="weight")
            print("Class mapping: A = 0, B = 1; predict_proba columns:", s3_classifier.classes_)
            print("Intercept (bias):", s3_classifier.intercept_[0])
            print("First ten coefficients in vocabulary order:")
            print(s3_coefficients.head(10).to_string())
        """),
        ("markdown", "s3-prediction-guide", r"""
            ### 4. Reproduce one prediction by hand

            The score is $z = x \cdot w + b$. The sigmoid turns it into
            $p = P(B=1) = 1/(1+e^{-z})$; $P(A=0) = 1-p$.
            `decision_function` returns $z$; `predict_proba` returns both probabilities
            in `classes_` order. `expit` is a numerically stable sigmoid.

            Optional: inspect `s3_count_row * s3_coefficients` to see the individual
            contributions. Can you explain why a zero count contributes zero?
        """),
        ("code", "s3-prediction", r"""
            from scipy.special import expit

            s3_probabilities = s3_classifier.predict_proba(s3_x_row)[0]
            s3_score = float(s3_classifier.decision_function(s3_x_row)[0])
            s3_manual_z = float(s3_count_row.to_numpy() @ s3_classifier.coef_[0]
                                + s3_classifier.intercept_[0])
            s3_manual_p = float(expit(s3_manual_z))
            np.testing.assert_allclose(s3_manual_z, s3_score, rtol=1e-10, atol=1e-12)
            np.testing.assert_allclose([1 - s3_manual_p, s3_manual_p], s3_probabilities,
                                       rtol=1e-10, atol=1e-12)
            print(f"decision_function z = {s3_score:.6f}; manual x·w+b = {s3_manual_z:.6f}")
            print(f"predict_proba: P(A=0) = {s3_probabilities[0]:.6f}; P(B=1) = {s3_probabilities[1]:.6f}")
            print(f"Manual sigmoid(z) = {s3_manual_p:.6f}. Known label is revealed next.")
        """),
        ("markdown", "s3-loss-guide", r"""
            ### 5. Compare the prediction with the known label: loss

            For $y \in \{0,1\}$, binary cross-entropy is
            $L = -[y\log(p) + (1-y)\log(1-p)]$ (natural logarithms).
            If $y=1$, this is $-\log(p)$; if $y=0$, it is $-\log(1-p)$.
            A confident correct prediction has small loss; a confident wrong prediction
            has large loss. `logaddexp(0, z) - y*z` evaluates the same loss stably.

            Training averages this loss across records. Below we inspect its **data-loss
            part**; scikit-learn also applies its default L2 regularization penalty to
            the weights. Mean training loss is not a claim of generalization.
            We leave validation performance summaries for Section 4.
        """),
        ("code", "s3-loss", r"""
            from sklearn.metrics import log_loss

            s3_y = int(s3_record["label"])  # Reveal the observed label after predicting.
            s3_row_loss = float(np.logaddexp(0.0, s3_manual_z) - s3_y * s3_manual_z)
            s3_sklearn_row_loss = log_loss([s3_y], [s3_probabilities], labels=s3_classifier.classes_)
            np.testing.assert_allclose(s3_row_loss, s3_sklearn_row_loss, rtol=1e-10, atol=1e-12)
            s3_train_z = s3_classifier.decision_function(s3_x_train)
            s3_mean_training_loss = float(np.mean(
                np.logaddexp(0.0, s3_train_z) - s3_train["label"].to_numpy() * s3_train_z
            ))
            np.testing.assert_allclose(s3_mean_training_loss, log_loss(
                s3_train["label"], s3_classifier.predict_proba(s3_x_train), labels=s3_classifier.classes_
            ), rtol=1e-10, atol=1e-12)
            print(f"Observed class: {'B' if s3_y else 'A'} ({s3_y}); this prediction's loss: {s3_row_loss:.6f}")
            print(f"Mean TRAINING data loss: {s3_mean_training_loss:.6f} (excludes L2 penalty)")
            print("Constructed examples, both with observed label B=1:")
            print(pd.DataFrame({
                "prediction": ["confident correct", "confident wrong"],
                "P(B=1)": [0.95, 0.05],
                "loss = -log(p)": -np.log([0.95, 0.05]),
            }).to_string(index=False))
        """),
        ("markdown", "s3-gradient-guide", r"""
            ### Optional: illustrate gradient descent on one weight

            This is a small **constructed training example**, separate from the DNA fit.
            Four records share one input feature $x$; both labels occur at $x=1$,
            so no weight can perfectly separate them. Bias is fixed at zero.
            The curve is actual mean logistic data loss as the single weight varies;
            its minimum is finite and above zero.

            Each update subtracts `learning_rate * gradient`: the negative gradient
            points downhill locally. The orange numbered points show successive updates.
            Optional: change `s3_learning_rate` from `0.8` to `0.2`, rerun, and compare
            progress over eight updates. Too large a step can overshoot or increase loss.
            This is not a learning-rate search on course validation data.

            The DNA model has many weights plus a bias. Its scikit-learn default solver
            is **L-BFGS**, not the vanilla gradient-descent loop illustrated here.
        """),
        ("code", "s3-gradient", r"""
            s3_toy_x = np.array([1.0, 1.0, 2.0, 2.0])
            s3_toy_y = np.array([0.0, 1.0, 1.0, 1.0])
            s3_fixed_bias = 0.0

            def s3_toy_loss(weight):
                z = weight * s3_toy_x + s3_fixed_bias
                return float(np.mean(np.logaddexp(0.0, z) - s3_toy_y * z))

            def s3_toy_gradient(weight):
                z = weight * s3_toy_x + s3_fixed_bias
                return float(np.mean((expit(z) - s3_toy_y) * s3_toy_x))

            s3_learning_rate = 0.8
            s3_weight = -2.0
            s3_steps = []
            for s3_step in range(9):
                s3_gradient = s3_toy_gradient(s3_weight)
                s3_steps.append({"step": s3_step, "weight": s3_weight,
                                 "loss": s3_toy_loss(s3_weight), "gradient": s3_gradient})
                if s3_step < 8:
                    s3_weight -= s3_learning_rate * s3_gradient
            s3_step_table = pd.DataFrame(s3_steps)
            print(s3_step_table.to_string(index=False, float_format=lambda value: f"{value:.4f}"))
            s3_weight_grid = np.linspace(-3.0, 4.0, 250)
            s3_figure, s3_ax = plt.subplots(figsize=(7, 3.8))
            s3_ax.plot(s3_weight_grid, [s3_toy_loss(w) for w in s3_weight_grid],
                       color="#0072B2", linewidth=2, label="Mean logistic loss (constructed data)")
            s3_ax.plot(s3_step_table.weight, s3_step_table.loss, "o--", color="#D55E00",
                       markersize=5, label="Negative-gradient updates")
            for s3_index in (0, 1, 2, 8):
                s3_point = s3_step_table.iloc[s3_index]
                s3_ax.annotate(str(s3_index), (s3_point.weight, s3_point.loss),
                               xytext=(5, 7), textcoords="offset points", color="#D55E00")
            s3_ax.set(xlabel="One weight (bias fixed at zero)", ylabel="Mean binary cross-entropy",
                      title="Training means moving toward lower loss")
            s3_ax.grid(axis="y", color="#dddddd", linewidth=0.6)
            s3_ax.spines[["top", "right"]].set_visible(False)
            s3_ax.legend(frameon=False, fontsize=9)
            s3_figure.tight_layout()
            plt.show()
            plt.close(s3_figure)
        """),
        ("markdown", "section-3-stop", r"""
            ## STOP — end of the Section 3 path

            You have followed DNA → counts → learned weights → score → probability → loss.
            Pause here during Section 3; the optional gradient illustration can be skipped.

            ## Next: Section 4 validation metrics

            Continue to the focused Section 4 cells below when the instructor reaches
            that lesson. They reuse this fitted model and do not train the forest.
            Stop again at the Section 4 boundary. The later complete stage 01 workflow
            belongs to Section 5 and preserves its normal metadata/return contract.
            **Run all also runs that later paired workflow.** No protected test result
            is scored. The optional gradient illustration above can be skipped.
        """),
    ]
    return [cell(kind, dedent(source).strip() + "\n", name) for kind, name, source in content]


def build() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    titles = {
        "01": "Day 1: DNA counts, logistic regression and random forest",
        "02": "Day 1: separate related-sequence leakage investigation",
        "03": "Days 2–3: representations, frozen embeddings and freeze",
        "04": "Day 3: frozen DNA embeddings",
        "05": "Day 3: freeze the comparison",
        "06": "Day 4: scientific-audit functions",
    }
    actions = {
        "01": "run_experiment()\n",
        "02": "run()\n",
        "03": "run_representations()\n",
        "04": "run_foundation()\n",
        "05": "freeze_workflows()\n",
        "06": 'print("Audit functions loaded. Call audit_predictions(samples, predictions).")\n',
    }
    for script in sorted(SOURCE.glob("[0-9][0-9]_*.py")):
        number = script.name[:2]
        if number in {"04", "05"}:
            continue
        workflows = [script] if number != "03" else [script, SOURCE / "04_foundation_embeddings.py", SOURCE / "05_frozen_comparison.py"]
        dependencies = [] if number == "02" else [SOURCE / "course_core.py"]
        if number in {"03", "04", "05"}:
            dependencies.append(SOURCE / "course_inference.py")
        sources = [*dependencies, *workflows]
        hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
        intro = (f"# {titles[number]}\n\nCompleted workflow generated from `course_code/`; "
                 "edit the canonical Python modules and rebuild with `python tools/build_course.py`.\n\n"
                 "Run setup, definition cells, then the workflow cell. Each notebook contains its Python dependencies; "
                 "opening it does not clone the repository. This is controlled simulated DNA classification, "
                 "not real promoter discovery. Student follow-along is optional pending the instructor's delivery choice.\n\n"
                 "See [execution and access instructions](https://github.com/palexiou/ML_Course_2026/blob/main/notebooks/README.md) "
                 "and the separate scaffolded practicals and instructor answers. Save a Drive copy to retain edits.\n")
        if number in {"01", "03"}:
            intro += ("\nThe primary dataset samples a fresh 15-base site from a fixed positive-entry PPM at each planting event "
                      "(0.95 for positives, 0.05 for negatives), at a uniform valid forward-strand start. "
                      "Defaults: 1,200 balanced 160-base sequences, seed 2026, 720/240/240 splits. "
                      "Old fixed-string datasets/caches need regeneration; see the notebook guide. "
                      "The fixed-position interaction and family-memorization controls retain separate rules.\n")
        if number == "03":
            intro = intro.replace("Run setup, definition cells, then the workflow cell.", "Run setup, shared definitions and stage 03 definitions, then the Day 2 checkpoints below.")
            intro = intro.replace("Student follow-along is optional pending the instructor's delivery choice.", "Students may follow along or watch the instructor demonstration.")
            intro += "\n[Open in Colab](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/03_representations.ipynb)\n"
            intro += ("\nThis notebook keeps stages 03–05 in **one runtime and working directory**, preserving `course_output/`. Run stage 03 on Day 2; continue with stages 04 and 05 on Day 3. "
                      "Alternatively transfer the required provenance-checked outputs explicitly; Git does not contain them.\n")
        if number == "03":
            intro = intro.replace("Run setup, definition cells, then the workflow cell.", "Run setup, shared definitions and stage 03 definitions, then the Day 2 checkpoints below.")
            intro = intro.replace("Student follow-along is optional pending the instructor's delivery choice.", "Students may follow along or watch the instructor demonstration.")
            intro += "\n[Open in Colab](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/03_representations.ipynb)\n"
            intro += ("\nThe first encoder load needs internet and about 224 MB of weights plus libraries. "
                      "The pinned checkpoint uses custom model code and has a CC-BY-NC-SA-4.0 license. "
                      "The default performs a small live extraction and reuses verified caches if supplied. "
                      "For an explicitly labeled cached-only contingency, change the stage 04 workflow call to "
                      "`run_foundation(live_example=False)` **before** freeze.\n")
        if number == "03":
            intro = intro.replace("Run setup, definition cells, then the workflow cell.", "Run setup, shared definitions and stage 03 definitions, then the Day 2 checkpoints below.")
            intro = intro.replace("Student follow-along is optional pending the instructor's delivery choice.", "Students may follow along or watch the instructor demonstration.")
            intro += "\n[Open in Colab](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/03_representations.ipynb)\n"
            intro += ("\n**Stage 05 freezes only.** It does not reveal test results. Run stage 03 on Day 2 and continue stages 04–05 on Day 3; Run all would execute all three stages. "
                      "No executable reveal cell is included: the instructor must separately authorize "
                      "`reveal_test(confirmation=\"REVEAL THE FROZEN TEST RESULTS\")` at the planned comparison. "
                      "Do not delete freeze/reveal markers to permit further tuning.\n")
        if number == "01":
            intro = intro.replace(f"# {titles[number]}\n\n", f"# {titles[number]}\n\n"
                                  "[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
                                  "(https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb)\n\n")
            intro = intro.replace("Run setup, definition cells, then the workflow cell.",
                                  "Run setup and both definition cells, then follow the selected Section 3 cells below.")
            intro = intro.replace("Student follow-along is optional pending the instructor's delivery choice.",
                                  "Students may follow along at selected cells or watch the instructor demonstration.")
            intro += ("\n**Classroom route:** GitHub notebook → Open in Colab → setup → definition cells → "
                      "selected Section 3 cells below. Stop before the later full workflow; "
                      "Run all would also fit the forest and print validation metrics. "
                      "The short path is complete working code for an instructor demo or optional student follow-along.\n")
        specs = requirements(number in {"03", "04", "05"})
        setup = ("# Install missing direct dependencies only; existing packages are not silently replaced.\n"
                 "# Exact locally rehearsed versions below are a baseline, not verified Colab compatibility.\n"
                 "from importlib.metadata import PackageNotFoundError, version\n"
                 "import subprocess\nimport sys\n"
                 f"requirements = {specs!r}\n"
                 "missing = []\n"
                 "for requirement in requirements:\n"
                 "    package, expected = requirement.split('==')\n"
                 "    try:\n"
                 "        installed = version(package)\n"
                 "        print(f'{package}: {installed} (local baseline {expected})')\n"
                 "    except PackageNotFoundError:\n"
                 "        missing.append(requirement)\n"
                 "if missing:\n"
                 "    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])\n"
                 "    print('If prompted, restart the runtime, then rerun this notebook from the top.')\n")
        cells = [cell("markdown", intro, "introduction"), cell("code", setup, "setup")]
        for index, path in enumerate(dependencies):
            cells.append(cell("code", without_local_imports(path, remove_main=True), f"shared-definitions-{index}"))
        for workflow in workflows:
            stage = workflow.name[:2]
            stage_guide = ("Run the definition cell, then follow Section 3 below; leave the complete workflow for later. "
                           if number == "01" else
                           "Run the definition cell, then the workflow cell when the instructor reaches this stage. ")
            cells.append(cell("markdown", f"## Stage {stage}: {titles[stage]}\n\n"
                              + stage_guide +
                              "Definitions do not train models. Generated outputs are temporary runtime files.\n",
                              f"stage-{stage}"))
            cells.append(cell("code", without_local_imports(workflow, remove_main=True), f"definitions-{stage}"))
            if number == "01":
                cells.extend(section3_cells())
                cells.extend(before_workflow(cell))
            if number == "03" and stage == "03":
                cells.extend(day2_teaching.before_workflow(cell, hashes))
                cells.append(cell("code", day2_teaching.RUN_SOURCE, "run-03"))
                cells.extend(day2_teaching.after_workflow(cell))
            elif number == "03" and stage == "04":
                cells.extend(day3_teaching.before_workflow(cell, hashes))
                cells.append(cell("code", day3_teaching.RUN_SOURCE, "run-04"))
                cells.extend(day3_teaching.after_workflow(cell))
            else:
                cells.append(cell("code", actions[stage], f"run-{stage}"))
            if number == "01":
                cells.extend(after_workflow(cell))
            if number == "06":
                cells.extend(day4_teaching.teaching_cells(cell))
        notebook: dict = {
            "cells": cells,
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python"},
                "colab": {"name": script.stem + ".ipynb", "provenance": []},
                "course_sources": hashes,
            },
            "nbformat": 4, "nbformat_minor": 5,
        }
        if number == "01":
            notebook["metadata"]["course_teaching_sources"] = {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                for name in ("tools/build_course.py", "tools/day1_teaching.py")
            }
        if number == "03":
            notebook["metadata"]["course_teaching_sources"] = {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                for name in ("tools/build_course.py", "tools/day2_teaching.py", "tools/day3_teaching.py", "instructor/completed/day3_alignment.py")
            }
        if number == "06":
            notebook["metadata"]["course_teaching_sources"] = {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                for name in ("tools/build_course.py", "tools/day4_teaching.py", "agent_workshop/flawed_analysis.py")
            }
        (DESTINATION / (script.stem + ".ipynb")).write_text(
            json.dumps(notebook, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built four completed notebooks (six workflow stages) in {DESTINATION}")


if __name__ == "__main__":
    build()
