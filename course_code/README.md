# Course code

For manual Colab pasting, start with [paste-ready instructions](../paste_ready/README.md), not these modular sources. Six generated files contain their supporting modules and require no repository imports. The instructor arranges cells and checks Colab manually.

## Local execution

Use Python 3.11 or newer. Steps 1?2 use `requirements.txt`; later steps use `requirements-ml.txt`. These are exact locally checked direct versions, not a claim that changing Colab's preinstalled environment is necessary. Try imports first. For CPU-only local PyTorch, install torch from its official CPU wheel index first if the default wheel would install accelerator libraries.

```powershell
python -m pip install -r course_code/requirements-ml.txt
python course_code/01_simple_signal.py
python course_code/02_split_leakage.py
python course_code/03_representations.py
python course_code/04_foundation_embeddings.py
python course_code/05_frozen_comparison.py freeze
```

The first two scripts are separate Day 1 practicals. Script 03 regenerates the same simple-signal identities plus the interaction-signal dataset and fits three methods. Script 04 reuses those identities for real frozen DNA embeddings and a training-fitted classifier. Script 05 freezes without calculating test scores. Only at the planned Day 3 reveal use:

```powershell
python course_code/05_frozen_comparison.py reveal --confirm "REVEAL THE FROZEN TEST RESULTS"
```

Script 06 provides `audit_predictions(samples, predictions)` and a file-based CLI; see `python course_code/06_scientific_audit.py --help`. It recomputes evidence, checks cross-split groups/duplicate sequences, and flags metric disagreements. It cannot prove that preprocessing was training-only or that biological claims are valid.

## Scientific and artifact boundaries

- Simulated 160-base DNA classification, not real promoter recognition or chromosome scanning. Deliberate motif insertion is noisy; incidental background matches can occur.
- Primary comparison metric: validation ROC-AUC, declared before fitting. Supporting average precision is not trapezoidal PR-AUC. Threshold metrics use 0.5. The isolated leakage exercise declares balanced accuracy primary.
- Data: `sample_id, group_id, sequence, label, split`. Groups never cross main-course splits. IDs, groups, split, and simulation truth are never model features.
- `course_core.py` owns simulation, split identity, metrics, and dataset validation. `course_inference.py` owns CNN inference and embedding-cache alignment shared by development and final comparison.
- Development readers omit protected test labels. Frozen, label-independent per-sequence extraction may read test input sequences but never fits on them. Only script 05 explicitly reads and scores test labels. Generation creates labels before exporting teaching partitions; that is not model evaluation. File separation is a convention, not access security.
- Scripts 03 and 04 refuse to retrain after freeze or reveal markers. Hashes reject changed frozen artifacts. Do not delete markers to disguise test-guided tuning; subsequent independent evaluation requires genuinely independent data.
- The CNN preserves position through flattened convolution features. Matching flanks and fixed motif-block positions make paired 4-mer bags identical in the interaction control. This demonstrates discarded information, not generic CNN superiority or learned biological grammar.

## Outputs and contingencies

`simple_signal_output/` contains Day 1 curves, predictions, coefficients, random-forest importance, comparison metrics, and generation metadata. `course_output/leakage/` contains the separate family-memorization experiment. `course_output/` contains shared datasets, models, validation predictions, plots, caches, and provenance. These generated local outputs are ignored by Git; preserve or transfer them separately for saved-output contingencies. They are not embedded in paste-ready code. Pretrained weights remain in the Hugging Face cache.

See [local rehearsal](../instructor/verification.md), [simple signal](../docs/simple-signal-verification.md), [representations](../docs/representation-verification.md), and [foundation embeddings](../docs/foundation-embedding-verification.md). Colab checks, actual clean agent runs/recording, and the actual Agentomics demonstration remain separate instructor checks.

Rebuild after edits: `python tools/build_course.py`. Do not edit canonical and generated copies by hand.
