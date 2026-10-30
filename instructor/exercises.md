# Scaffolded practicals

Each task takes approximately 5–10 minutes inside its assigned teaching block. Paste the corresponding completed script into a working cell, replace the indicated lines with these scaffold lines, then fill them. `None` is an intentional missing-code marker, not a runnable answer. Separate completed scripts are linked in [answers](answers.md). No homework or submission is required.

## Day 1: fit on training, predict validation

Use `completed/day1_validation.py`. Its default miniature course dataset is self-contained and does not contain protected test samples. For the actual practical, replace the two development DataFrames with reads of supplied `train.csv` and `validation.csv`, retaining the same schema and assertions. Never read a combined file first.

Replace these three statements in the completed script:

```python
model.fit(None, None)
probabilities = model.predict_proba(None)[:, 1]
predictions = pd.DataFrame({"sample_id": None, "probability": probabilities})
```

Fill the training sequences, training labels, validation sequences, and validation IDs. Before running, predict which partition determines the k-mer vocabulary. After running, explain one false positive or false negative, or explain why none occurs in this tiny example. Would a good score establish real promoter recognition? Why does ROC-AUC not determine the threshold-0.5 confusion matrix?

Optional in-class extension: reason about precision and recall at a higher threshold without using test data or changing the frozen course policy.

## Day 2: what survives representation?

Use `completed/day2_representation.py`. Replace:

```python
probability = None
encoded = None
bags_equal = None
```

Compute sigmoid of the provided logit; encode the sequence characters against the A,C,G,T alphabet; compare the two `Counter` objects. Predict whether the two sequences have equal 4-mer counts and whether one-hot arrays match. Explain why a classifier receiving only identical bags cannot distinguish this pair. Which part of the actual CNN preserves position? Do not conclude that all CNNs learn general regulatory grammar.

Optional in-class extension: remove matching flanks in a disposable copy and inspect changed 4-mers. This is a different control, not a replacement course dataset.

## Day 3: align a cache before trusting it

Use `completed/day3_alignment.py`. This script has an explicitly synthetic two-feature cache for learning alignment; it is not output of a pretrained DNA model. Replace:

```python
aligned = None
training_features = None
validation_features = None
```

Reindex the cache by the metadata IDs, then select feature rows for each existing split. Predict why taking the first rows of the shuffled cache would fail. Which fields would you need to reproduce a real embedding cache? State what must be frozen before the instructor may read the protected test file.

Optional in-class extension: duplicate a cache ID or remove a row. Confirm the script rejects the cache rather than silently dropping samples. No test data is needed.

## Day 4: audit a running analysis

Read [the flawed fixture](../agent_workshop/fixture.md), without first opening the worked answers. Use `completed/day4_audit.py`; replace:

```python
overlap = None
aligned_predictions = None
```

Compute the intersection of training and validation group IDs and join predictions to validation labels by sample ID with one-to-one validation. Predict whether merely reversing the prediction-table rows should change a correct evaluation. Explain why fixing row order alone cannot repair the scientific claim. Use the printable checklist to name evidence needed before accepting the analysis.

Optional in-class extension: write one sentence for each distinction: specification, AGENTS, skill, and tool. Students without agent accounts use exactly the same fixture and questions.
