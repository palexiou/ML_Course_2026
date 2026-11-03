"""Check generated notebook syntax and exact canonical source correspondence."""

import ast
import hashlib
import json

from build_course import DESTINATION, ROOT, SOURCE, section3_cells, without_local_imports, cell as make_cell
from day1_teaching import before_workflow, after_workflow
import day2_teaching
import day3_teaching
import day4_teaching


def check() -> None:
    paths = sorted(DESTINATION.glob("*.ipynb"))
    assert len(paths) == 4, "Expected four completed notebooks"
    for path in paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if path.name == "01_simple_signal.ipynb":
            teaching_sources = notebook["metadata"]["course_teaching_sources"]
            assert set(teaching_sources) == {"tools/build_course.py", "tools/day1_teaching.py"}, path
            for name, expected_hash in teaching_sources.items():
                assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected_hash, (path, name)
            teaching = section3_cells() + before_workflow(make_cell)
            start = next(i for i, cell in enumerate(notebook["cells"]) if cell["id"] == "section-3")
            assert notebook["cells"][start:start + len(teaching)] == teaching, "Sections 3–4 cells differ from builder"
            assert notebook["cells"][start - 1]["id"] == "definitions-01", path
            assert notebook["cells"][start + len(teaching)]["id"] == "run-01", path
            assert notebook["cells"][start + len(teaching) + 1:] == after_workflow(make_cell), path
        if path.name == "03_representations.ipynb":
            for name, expected_hash in notebook["metadata"]["course_teaching_sources"].items():
                assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected_hash, (path, name)
            start = next(i for i, c in enumerate(notebook["cells"]) if c["id"] == "day2-section-5")
            expected = (day2_teaching.before_workflow(make_cell, notebook["metadata"]["course_sources"])
                        + [make_cell("code", day2_teaching.RUN_SOURCE, "run-03")]
                        + day2_teaching.after_workflow(make_cell))
            assert notebook["cells"][start:start+len(expected)] == expected, "Day 2 teaching cells differ"
            assert notebook["cells"][start-1]["id"] == "definitions-03"
            assert notebook["cells"][start+len(expected)]["id"] == "stage-04"
            start = next(i for i, c in enumerate(notebook["cells"]) if c["id"] == "day3-start")
            expected = (day3_teaching.before_workflow(make_cell, notebook["metadata"]["course_sources"])
                        + [make_cell("code", day3_teaching.RUN_SOURCE, "run-04")]
                        + day3_teaching.after_workflow(make_cell))
            assert notebook["cells"][start:start+len(expected)] == expected, "Day 3 teaching cells differ"
            assert notebook["cells"][start-1]["id"] == "definitions-04"
            assert notebook["cells"][start+len(expected)]["id"] == "stage-05"
        if path.name == "06_scientific_audit.ipynb":
            for name, sha in notebook["metadata"]["course_teaching_sources"].items():
                assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha, (path, name)
            start = next(i for i, c in enumerate(notebook["cells"]) if c["id"] == "day4-start")
            assert notebook["cells"][start:] == day4_teaching.teaching_cells(make_cell), "Day 4 teaching cells differ"
        sources = notebook["metadata"]["course_sources"]
        embedded = []
        for name, expected_hash in sources.items():
            source = SOURCE / name
            assert hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash, (path, name)
            embedded.append(without_local_imports(source, remove_main=True))
        definitions = []
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            code = "".join(cell["source"])
            compile(code, f"{path.name}:{cell['id']}", "exec")
            assert cell["execution_count"] is None and cell["outputs"] == [], path
            tree = ast.parse(code)
            assert not any(isinstance(node, ast.ImportFrom) and node.module in
                           {"course_core", "course_inference"} for node in ast.walk(tree)), path
            assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                           and node.func.id == "reveal_test" for node in ast.walk(tree)), path
            if "definitions" in cell["id"]:
                definitions.append(code)
        assert sorted(definitions) == sorted(embedded), f"Embedded source differs: {path}"
    print("Four notebooks: syntax, hashes, exact source/Day 1–4 teaching cells, empty outputs and no reveal calls passed")


if __name__ == "__main__":
    check()
