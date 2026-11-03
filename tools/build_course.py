"""Build completed, self-contained notebooks from the canonical course modules."""

import ast
import hashlib
import json
from pathlib import Path

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
        if number == "03":
            intro += ("\nThis notebook keeps stages 03–05 in **one runtime and working directory**, preserving `course_output/`. Run stage 03 on Day 2; continue with stages 04 and 05 on Day 3. "
                      "Alternatively transfer the required provenance-checked outputs explicitly; Git does not contain them.\n")
        if number == "03":
            intro += ("\nThe first encoder load needs internet and about 224 MB of weights plus libraries. "
                      "The pinned checkpoint uses custom model code and has a CC-BY-NC-SA-4.0 license. "
                      "The default performs a small live extraction and reuses verified caches if supplied. "
                      "For an explicitly labeled cached-only contingency, change the stage 04 workflow call to "
                      "`run_foundation(live_example=False)` **before** freeze.\n")
        if number == "03":
            intro += ("\n**Stage 05 freezes only.** It does not reveal test results. Run stage 03 on Day 2 and continue stages 04–05 on Day 3; Run all would execute all three stages. "
                      "No executable reveal cell is included: the instructor must separately authorize "
                      "`reveal_test(confirmation=\"REVEAL THE FROZEN TEST RESULTS\")` at the planned comparison. "
                      "Do not delete freeze/reveal markers to permit further tuning.\n")
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
            cells.append(cell("markdown", f"## Stage {stage}: {titles[stage]}\n\n"
                              "Run the definition cell, then the workflow cell when the instructor reaches this stage. "
                              "Definitions do not train models. Generated outputs are temporary runtime files.\n",
                              f"stage-{stage}"))
            cells.append(cell("code", without_local_imports(workflow, remove_main=True), f"definitions-{stage}"))
            cells.append(cell("code", actions[stage], f"run-{stage}"))
        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python"},
                "colab": {"name": script.stem + ".ipynb", "provenance": []},
                "course_sources": hashes,
            },
            "nbformat": 4, "nbformat_minor": 5,
        }
        (DESTINATION / (script.stem + ".ipynb")).write_text(
            json.dumps(notebook, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built four completed notebooks (six workflow stages) in {DESTINATION}")


if __name__ == "__main__":
    build()
