"""Build self-contained paste-ready scripts from the canonical course modules."""

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "course_code"
DESTINATION = ROOT / "paste_ready"


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


def build() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    source_hashes = {}
    for script in sorted(SOURCE.glob("[0-9][0-9]_*.py")):
        dependencies = [] if script.name.startswith("02_") else [SOURCE / "course_core.py"]
        if script.name[:2] in {"03", "04", "05"}:
            dependencies.append(SOURCE / "course_inference.py")
        pieces = [without_local_imports(path) for path in dependencies]
        pieces.append(without_local_imports(script, remove_main=script.name[:2] in {"05", "06"}))
        if script.name.startswith("05_"):
            pieces.append('if __name__ == "__main__":\n    freeze_workflows()\n')
        if script.name.startswith("06_"):
            pieces.append('if __name__ == "__main__":\n    print("Audit functions loaded. Call audit_predictions(samples, predictions).")\n')
        bundled = '\n\n'.join(pieces)
        compile(bundled, script.name, "exec")
        (DESTINATION / script.name).write_text(bundled, encoding="utf-8")
        for path in [*dependencies, script]:
            source_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    (DESTINATION / "source_manifest.json").write_text(json.dumps(source_hashes, indent=2) + "\n", encoding="utf-8")
    print(f"Built six paste-ready scripts in {DESTINATION}")


if __name__ == "__main__":
    build()
