# Deliberately flawed, manually authored analysis fixture

**NOT A REAL AGENT TRANSCRIPT.** These rows, probabilities, code, and claims were authored for teaching. They are not saved outputs of an agent or Agentomics. The probabilities are invented to expose a row-alignment error; they are not model predictions. This fixture has no protected test data.

## Evidence packet

| sample_id | group_id | sequence | label | split |
| --- | --- | --- | --- | --- |
| train-01 | group-a | ACGTACGT | 0 | train |
| train-02 | group-b | TATAAATG | 1 | train |
| validation-01 | group-a | ACGTACGA | 0 | validation |
| validation-02 | group-c | TATAAATA | 1 | validation |

| sample_id | probability |
| --- | --- |
| validation-02 | 0.1 |
| validation-01 | 0.9 |

[Runnable flawed analysis](flawed_analysis.py) fits a vocabulary on all development sequences, checks sample-ID separation only, and compares label and probability arrays by position. Its authored claim is:

> Accuracy is 100%, so the best promoter model has learned promoter biology. Unique sample IDs prove there is no leakage. We can use the Day 3 test score to decide whether to keep this approach.

No model, real probability-generation procedure, extraction provenance, or actual test access log is supplied. A missing record is not proof that a test was read; the proposed use of the Day 3 score is itself contrary to the evaluation policy.

## Student questions

1. Which independence unit crosses the split despite unique sample IDs?
2. Which operation learns from validation data? Is this as direct as fitting on validation labels?
3. What happens to accuracy after joining by sample ID? Does that repair leakage?
4. Which metric, baseline, and provenance evidence is absent?
5. What does the simulation permit us to claim, and what does the authored report overclaim?
6. What would you repair in this separate exercise? What must remain fixed in the main course comparison?
7. Can Day 3 test results choose this new model? Explain why or why not.

Discuss before opening [worked answers](worked-audit.md). The code runs successfully by design; that is the scientific-audit lesson.
