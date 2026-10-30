# Example teaching-project instructions

These instructions apply to an isolated course demonstration workspace.

- Keep the scientific question, dataset variant, and fixed sample/group split identities from the supplied specification.
- Use `sample_id,group_id,sequence,label,split` for data and `sample_id,probability` for predictions. Treat metadata as metadata, not input features.
- Open development inputs only. Do not open protected test files or test caches during development. Day 3 reveal requires an explicit recorded freeze and instructor authorization; later agent work cannot reuse revealed test results as fresh evaluation.
- Keep the intentionally flawed leakage exercise separate from the correct workflow. Correct its group split locally without replacing the main-course split manifest.
- Fit learned preprocessing on training only. Match predictions and cached features by sample ID and reject missing/duplicate IDs.
- Use the scientific-audit skill at `skills/scientific-audit/SKILL.md` when reviewing the analysis; return evidence and unresolved issues, not just a pass label.
- Distinguish code execution from scientific validity. Label manually authored examples, actual live runs, and actual previous runs accurately.
- Explain simulation limitations; do not claim real promoter recognition, general regulatory grammar, or universal model superiority.
- Ask about consequential scientific changes. Do not silently change data, metrics, or evaluation boundaries to improve a result.
- Write clear standalone code with descriptive variable names and no inline code comments. Do not commit or push unless explicitly requested.
