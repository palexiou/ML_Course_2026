"""Execute Day 3 guided notebook cells locally, validation only; rehearse freeze in a copy."""
from pathlib import Path
from typing import Any
import argparse
import hashlib
import json
import linecache
import os
import platform
import shutil
import tempfile
import time
from importlib.metadata import version

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True, help='Completed, compatible Day 2 workspace; no frozen/revealed markers.')
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    os.chdir(workspace)
    notebook = json.loads((ROOT / 'notebooks/03_representations.ipynb').read_text())
    ns: dict[str, Any] = {'__name__': 'day3_local_rehearsal'}
    started = time.perf_counter()
    active = False
    for cell in notebook['cells']:
        name = cell['id']
        if name == 'day3-start':
            active = True
        # Definitions are source-cached as in IPython, so inspect.getsource works at freeze.
        selected = 'definitions' in name or name in {'day2-run-identity', 'run-03', 'day2-readback'} or active
        if name == 'stage-05':
            break
        if cell['cell_type'] == 'code' and selected and name != 'setup':
            print('CELL', name, flush=True)
            source = ''.join(cell['source'])
            filename = '<course-notebook-' + name + '>'
            linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
            exec(compile(source, filename, 'exec'), ns)
    # Re-running completed stage 04 must not extract or fit a second time.
    cell = next(c for c in notebook['cells'] if c['id'] == 'run-04')
    exec(compile(''.join(cell['source']), '<repeat-run-04>', 'exec'), ns)
    # Freeze guard rehearsal is separate from the development workspace; never reveal.
    freeze_workspace = Path(tempfile.mkdtemp(prefix='ml-day3-freeze-only-'))
    shutil.copytree(workspace / 'course_output', freeze_workspace / 'course_output')
    for name in ['definitions-05', 'run-05']:
        cell = next(c for c in notebook['cells'] if c['id'] == name)
        source = ''.join(cell['source'])
        filename = '<course-notebook-' + name + '>'
        linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
        os.chdir(freeze_workspace)
        exec(compile(source, filename, 'exec'), ns)
    try:
        ns['freeze_workflows']()
    except FileExistsError:
        print('Second freeze refused as intended.', flush=True)
    else:
        raise AssertionError('Existing freeze was overwritten')
    assert not (freeze_workspace / 'course_output/test_results.json').exists()
    assert not (workspace / 'course_output/test_results.json').exists()
    os.chdir(workspace)
    sources = ['notebooks/03_representations.ipynb', 'tools/build_course.py', 'tools/day3_teaching.py', 'tools/rehearse_day3.py', 'instructor/completed/day3_alignment.py', *['course_code/' + x for x in notebook['metadata']['course_sources']]]
    model_snapshot = Path.home() / '.cache/huggingface/hub/models--InstaDeepAI--nucleotide-transformer-v2-50m-multi-species/snapshots/81b29e5786726d891dbf929404ef20adca5b36f1'
    config = json.loads((model_snapshot / 'config.json').read_text())
    weight_path = model_snapshot / 'model.safetensors'
    record = {
        'schema': 1, 'date': '2026-11-03',
        'execution': 'Generated Day 3 notebook, local CPU2threads; current stage03 reused, stage04 validation only. No tuning or reveal. Freeze tested separately in a copied workspace.',
        'source_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources},
        'environment': {'python': platform.python_version(), 'platform': platform.platform(), 'packages': {p: version(p) for p in ['torch', 'transformers', 'numpy', 'pandas', 'scikit-learn', 'scipy', 'matplotlib', 'huggingface-hub', 'tokenizers', 'safetensors', 'einops']}},
        'workspace': str(workspace), 'freeze_only_workspace': str(freeze_workspace),
        'freeze_artifact_count': len(ns['json'].loads((freeze_workspace / 'course_output/frozen_manifest.json').read_text())['artifacts']),
        'encoder_config': {k: config[k] for k in ['hidden_size', 'num_hidden_layers', 'num_attention_heads', 'position_embedding_type']},
        'weight_sha256': hashlib.sha256(weight_path.read_bytes()).hexdigest(), 'weight_bytes': weight_path.stat().st_size,
        'load_seconds': ns['d3_load_seconds'], 'live': ns['d3_live_records'],
        'live_components': {v: arr[:, :16].tolist() for v, arr in ns['d3_live'].items()},
        'run': ns['d3_run'], 'metrics': ns['d3_comparison'].to_dict('records'),
        'rehearsal_wall_seconds': time.perf_counter() - started,
        'test_evaluated': False, 'colab_executed': False,
    }
    record['artifact_sha256'] = {str(p.relative_to(workspace / 'course_output')): hashlib.sha256(p.read_bytes()).hexdigest() for p in (workspace / 'course_output').rglob('*') if p.is_file() and p.suffix in {'.json', '.csv', '.npz', '.pt', '.joblib'}}
    (ROOT / 'instructor/verification/day3-current.json').write_text(json.dumps(record, indent=2, allow_nan=False) + '\n')
    print('Day 3 evidence recorded; no protected test scores calculated.', flush=True)


if __name__ == '__main__':
    main()
