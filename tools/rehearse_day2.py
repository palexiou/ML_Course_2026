"""Execute the generated Day 2 lesson and refresh source-bound offline slide evidence.

Uses training/validation only; stops before stage 04. Package setup is skipped
because this maintainer command expects installed dependencies.
"""
from pathlib import Path
import argparse
import tempfile
from typing import Any
import os,json,time,hashlib,platform,sys
from importlib.metadata import version
ROOT=Path(__file__).resolve().parents[1]
nb=json.loads((ROOT/"notebooks/03_representations.ipynb").read_text())
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--workspace", type=Path, help="Reuse a complete compatible course_output here; defaults to a fresh temporary directory.")
args=parser.parse_args()
workspace=(args.workspace or Path(tempfile.mkdtemp(prefix="ml-day2-rehearsal-"))).resolve()
workspace.mkdir(parents=True,exist_ok=True)
training_run_reused=(workspace/"course_output/representation_run.json").exists()
os.chdir(workspace)
ns: dict[str, Any]={"__name__":"day2_classroom_rehearsal"}
started=time.perf_counter()
for cell in nb["cells"]:
    if cell["id"]=="stage-04":break
    if cell["cell_type"]=="code" and cell["id"]!="setup":
        print("CELL",cell["id"],flush=True)
        exec(compile("".join(cell["source"]),cell["id"],"exec"),ns)
# Rerun selection cells only to verify no second fit.
for name in ["run-03", "day2-inference", "day2-pair"]:
    cell=next(c for c in nb["cells"] if c["id"]==name)
    exec(compile("".join(cell["source"]),name,"exec"),ns)
# Portable source-bound evidence for offline slides; no model runs in HTML.
record: dict[str, Any]={"schema":1,"date":"2026-11-03","execution":"Locally executed generated Day 2 notebook, training/validation only; Colab and classroom timing unverified.","source_sha256":{str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ["notebooks/03_representations.ipynb","tools/build_course.py","tools/day2_teaching.py","tools/rehearse_day2.py", *["course_code/"+x for x in nb["metadata"]["course_sources"]]]},"environment":{"python":platform.python_version(),"platform":platform.platform(),"packages":{x:version(x) for x in ["torch","numpy","pandas","scikit-learn","scipy","matplotlib","joblib"]}},"run":ns["d2_run"],"metrics":ns["d2_metrics"].to_dict("records"),"selected_epochs":ns["d2_selected"],"histories":{k:v.to_dict("records") for k,v in ns["d2_histories"].items()},"primary_examples":[],"control_pairs":[],"test_evaluated":False}
record["task_examples"] = [ns["d2_data"]["simple"].loc[ns["d2_data"]["simple"].label.eq(label), ["sample_id","label","sequence"]].iloc[0].to_dict() for label in [0,1]]
for row in ns["d2_data"]["simple"].head(3).itertuples():
    with ns["torch"].inference_mode():
        inputs=ns["one_hot"]([row.sequence]);model=ns["d2_models"]["simple"]
        probability=float(ns["torch"].sigmoid(model(inputs))[0]);maps=model.filters(inputs)[0].numpy()
    record["primary_examples"].append({"sample_id":row.sample_id,"label":row.label,"sequence":row.sequence,"probability":probability,"responses":maps.tolist()})
for group,pair in ns["d2_pair_groups"][:3]:
    record["control_pairs"].append({"group_id":group,"records":pair[["sample_id","label","sequence","logistic_regression_probability","random_forest_probability","cnn_probability"]].to_dict("records"),"complete_4mer_counts_equal":True})
record["artifact_sha256"]={str(p.relative_to(workspace/"course_output")):hashlib.sha256(p.read_bytes()).hexdigest() for p in (workspace/"course_output").rglob("*") if p.is_file() and p.suffix in {".json",".csv",".pt",".joblib"}}
record["rehearsal_wall_seconds"]=time.perf_counter()-started
record["training_run_reused"]=training_run_reused
record["workspace"]=str(workspace)
(ROOT/"instructor/verification/day2-current.json").write_text(json.dumps(record,indent=2,allow_nan=False)+"\n")
print("EVIDENCE",record["selected_epochs"],record["rehearsal_wall_seconds"],flush=True)
