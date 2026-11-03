"""Run the generated Day 4 audit notebook locally; no training, test access or agent calls."""
import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import tempfile
import time
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'agent_workshop/actual_runs/2026-10-26'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    notebook=json.loads((ROOT/'notebooks/06_scientific_audit.ipynb').read_text())
    workspace=Path(tempfile.mkdtemp(prefix='ml-day4-audit-'))
    os.chdir(workspace)
    ns: dict[str,Any]={'__name__':'day4_notebook_rehearsal'}
    times={}
    for cell in notebook['cells']:
        if cell['cell_type']=='code' and cell['id']!='setup':
            name=cell['id'];print('CELL',name,flush=True);started=time.perf_counter()
            exec(compile(''.join(cell['source']),name,'exec'),ns)
            times[name]=time.perf_counter()-started
    parent=json.loads((ARCHIVE/'parent_audit.json').read_text())
    for name,expected in parent['input_hashes'].items():
        for arm in ['vague','specified']:
            data=(ARCHIVE/arm/name).read_bytes()
            assert data==(ARCHIVE/('specified' if arm=='vague' else 'vague')/name).read_bytes()
            assert hashlib.sha256(data.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')).hexdigest()==expected,(arm,name)
    # All supplied previous-run files are immutable evidence; none is executed/refitted.
    sources=['tools/build_course.py','tools/day4_teaching.py','tools/rehearse_day4.py',
             'notebooks/06_scientific_audit.ipynb','agent_workshop/flawed_analysis.py',
             'agent_workshop/fixture.md','agent_workshop/precise-spec.md',
             'agent_workshop/example-project/AGENTS.md','agent_workshop/example-project/skills/scientific-audit/SKILL.md',
             'course_code/course_core.py','course_code/06_scientific_audit.py']
    sources.extend(str(p.relative_to(ROOT)) for p in ARCHIVE.rglob('*') if p.is_file())
    assert not list(workspace.rglob('*')), 'Audit lesson unexpectedly created runtime artifacts'
    record={
        'schema':1,'date':'2026-11-03','execution':'Executed generated Day 4 notebook locally in an empty temporary workspace; definitions and guided audit cells, setup skipped. No classifier fitting, agent rerun, network or course test access.',
        'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
        'environment':{'python':platform.python_version(),'platform':platform.platform(),'packages':{p:version(p) for p in ['numpy','pandas','scikit-learn']}},
        'cell_seconds':times,'fixture':{'positional_accuracy':ns['d4_positional'],'aligned_accuracy':ns['d4_aligned'],'audit':ns['d4_fixture_report']},
        'historical_actual_runs':ns['d4_actual_reports'],'original_agent_date':'2026-10-26',
        'original_provider_model':{'provider':parent['provider'],'model':parent['model']},
        'original_inputs_identical':True,'historical_hash_compatibility':'Current Git checkout files have LF endings; both arms are byte-identical. Reconstructed CRLF bytes match the archived Windows input SHA-256 values. Checkout hashes recorded separately.','archived_manual_prediction_max_abs_difference':parent['specified_manual_prediction_max_absolute_difference'],
        'scope':'Saved-prediction and identity checks, not proof of correct fitting, test-access history, biological validity or prompt causality. Original runs use historical fixed-motif data; not current PPM scores.',
        'test_evaluated':False,'new_agent_run':False,'colab_executed':False,'agentomics_demo_delivered':False,
        'agentomics_route':'Instructor requested audit-discussion fallback for now.',
    }
    (ROOT/'instructor/verification/day4-current.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    print('Day 4 local audit recorded; archive unchanged, no course test access.',flush=True)


if __name__=='__main__':main()
