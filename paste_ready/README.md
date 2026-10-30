# Paste-ready course code

These generated files contain their local dependencies in one file. Copy a complete file into a Colab Python cell, then run it. You can split the cell into smaller cells later. Do not copy the modular files in `course_code/` without their supporting modules.

No Colab session was used for this handoff. Dependency compatibility, setup time, and rendering in your Colab runtime remain your manual checks. All setup belongs in contact time, not homework.

## Execution order

1. `01_simple_signal.py`: standalone Day 1 simulation and logistic regression. Produces `simple_signal_output/`; no protected test scoring.
2. `02_split_leakage.py`: separate Day 1 leakage investigation. It does not reuse or reveal the course test data.
3. `03_representations.py`: Day 2, generates the shared two-variant dataset and trains logistic regression, random forest, and the position-aware CNN. Produces `course_output/`.
4. `04_foundation_embeddings.py`: Day 3, uses the dataset from step 3. Downloads the pinned DNA model on the first run, demonstrates a fresh two-sequence extraction, fits the simple classifier, and scores validation only. Existing full-data caches are verified and reused, while the small live example still runs. For a clearly labeled cached-only contingency, call `run_foundation(live_example=False)` after loading the definitions.
5. `05_frozen_comparison.py`: first execution **freezes only**. It does not calculate test scores. Discuss expected outcomes before a second cell explicitly calls:

```python
reveal_test(confirmation="REVEAL THE FROZEN TEST RESULTS")
```

6. `06_scientific_audit.py`: Day 4, loads audit functions without opening files. Use the authored fixture and examples in `../agent_workshop/` and `../instructor/`.

Run steps 3?5 in the same working directory, preserving `course_output/`. Freeze binds model/data/cache/configuration/validation-prediction hashes and inference/metric source and package versions. Use normal notebook cells that preserve source history; an uninspectable dynamically executed function is rejected rather than silently left unfrozen. Neither deleting a marker nor changing a directory makes a previously inspected test set independent again. A fresh directory is appropriate for genuinely separate development data, not for concealing test-guided changes.

## Dependencies and runtime

Try imports first in Colab. If a dependency is missing, install it in a separate setup cell. The exact locally verified direct versions are in `../course_code/requirements.txt` for steps 1?2 and `../course_code/requirements-ml.txt` for steps 3?6. Restart the runtime when package changes require it. Do not repeatedly reinstall packages during class.

The locally verified execution uses CPU and two PyTorch threads. No GPU, API key, or paid agent account is required for steps 1?6. First DNA-model download needs internet and about 224 MB for weights, plus libraries/cache storage. The checkpoint is **CC-BY-NC-SA-4.0**, not an unrestricted commercial model. Loading its pinned custom Python implementation executes remote code: the source was inspected locally, but this is not a security guarantee. See `../docs/foundation-embedding-verification.md`.

The script defaults perform the completed workflow. For missing-code practice, use the short student snippets and separate answers in `../instructor/`. Questions and discussion are formative, not assessed submissions.

## Rebuild

Do not edit these generated Python files as the canonical source. Edit `../course_code/`, then run `python tools/build_course.py` from the project root. `source_manifest.json` records source hashes. The files are self-contained code, not bundled datasets or model weights; preserve the output directory separately for saved-output contingencies.
