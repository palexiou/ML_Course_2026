# Course practicals

Use the completed [notebooks](../notebooks/README.md) for demonstrations or follow-along. Hands-on depth remains open; the questions work by observation. Separate [instructor answers](answers.md) and miniature completed scripts are retained.

## Day 1: inspect, fit and interpret the course data


2026-11-03 navigation note: these retained cells and slide numbers support the earlier deck. The [proposed Day 1 story](../Slides/Day_1/story.md) offers instructor demonstrations with optional follow-along; compulsory student execution remains undecided. The existing inspection, scaffold and answer cells are retained; actual Colab execution remains unverified. See the [GitHub/Colab delivery note](../README.md#github-notebooks-and-colab) for notebook delivery and runtime requirements.

Keep this guide beside a Colab notebook. The presentation tells you when to switch here. Python runs in the notebook; the slide itself is a visual explanation or activity prompt.

## Setup — slides 1–4

Open completed notebook 01 using its Colab badge in the notebook guide, or use an existing notebook for these short cells:

```python
print("Ready for ML")
import numpy as np
import pandas as pd
import sklearn
import matplotlib
```

Use the completed notebook's setup cell and the notebook guide for packages and restart guidance. Setup takes place during class; if access fails, follow the projected notebook and discuss the same questions.

## Practical A — slides 20–22: inspect the data and count words

### 1. Run the supplied workflow once

Open [completed notebook 01](../notebooks/01_simple_signal.ipynb) and run setup, definitions and its workflow cell. It creates `simple_signal_output/`, fits both classical models, and displays validation outputs. We will interpret those outputs later in the lesson. It does not evaluate the protected test partition.

Keep using this notebook and working directory during Day 1. Running this step again regenerates its outputs; it is not necessary for each later cell.

### 2. Inspect one example

```python
import pandas as pd

train = pd.read_csv("simple_signal_output/train.csv")
validation = pd.read_csv("simple_signal_output/validation.csv")
display(train[["sample_id", "sequence", "label"]].head())
print("Training rows:", len(train))
print("Validation rows:", len(validation))
print("Sequence lengths:", train["sequence"].str.len().unique())
```

Identify the input, target, and sample identity. Expected default sizes: 720 training rows, 240 validation rows, and sequence length 160. Use these development partitions throughout the practical.

### 3. Count overlapping 4-mers

```python
from collections import Counter

sequence = train.iloc[0]["sequence"]
k = 4
counts = Counter(sequence[start:start + k]
                 for start in range(len(sequence) - k + 1))
print("First 30 bases:", sequence[:30])
print("Most frequent 4-mers:", counts.most_common(8))
print("Total windows:", sum(counts.values()))
print("Distinct observed words:", len(counts))
```

Expected window total: 157. Explain why the number of distinct words can be smaller and why the count vector does not record their starting positions. Then return to slide 22.

## Practical B — slides 40–41: fit and inspect predictions

The following cell deliberately contains four `None` placeholders. Replace them before running it. The input and output variable names are supplied so the task is about the data roles.

```python
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, roc_auc_score

train = pd.read_csv("simple_signal_output/train.csv")
validation = pd.read_csv("simple_signal_output/validation.csv")
model = Pipeline([
    ("kmers", CountVectorizer(analyzer="char", ngram_range=(4, 4),
                             lowercase=False)),
    ("classifier", LogisticRegression(max_iter=2000)),
])

model.fit(None, None)  # training sequences, then training labels
probabilities = model.predict_proba(None)[:, 1]  # validation sequences
predictions = pd.DataFrame({
    "sample_id": None,  # validation sample IDs in prediction order
    "probability": probabilities,
})

evaluated = validation[["sample_id", "label"]].merge(
    predictions, on="sample_id", validate="one_to_one"
)
evaluated["prediction"] = (evaluated["probability"] >= 0.5).astype(int)
display(evaluated.head())
display(evaluated.loc[evaluated["prediction"] != evaluated["label"]].head())
print("Validation ROC-AUC:", roc_auc_score(
    evaluated["label"], evaluated["probability"]
))
print("Confusion matrix: rows = true, columns = predicted; class order [0, 1]")
print(confusion_matrix(evaluated["label"], evaluated["prediction"], labels=[0, 1]))
```

Choose one mismatched prediction. State its sample ID, true label, predicted class, and whether it is a false positive or a false negative. The scikit-learn matrix orders classes `[0, 1]`, giving `[[TN, FP], [FN, TP]]`; the teaching slides explicitly label their cells in a different arrangement.

<details>
<summary>Completed replacements</summary>

```python
model.fit(train["sequence"], train["label"])
probabilities = model.predict_proba(validation["sequence"])[:, 1]
predictions = pd.DataFrame({
    "sample_id": validation["sample_id"],
    "probability": probabilities,
})
```

Only the training sequences fit the vocabulary. The validation sequences are transformed using that already-fitted vocabulary. IDs keep the predictions aligned with the labels.

</details>

## Practical C — slides 47–50: compare and interpret

The random forest was already fitted by code 01. Inspect the shared validation comparison and feature tables:

```python
import pandas as pd

comparison = pd.read_csv("simple_signal_output/classical_validation.csv")
display(comparison[["method", "roc_auc", "average_precision"]])

coefficients = pd.read_csv("simple_signal_output/kmer_coefficients.csv")
importance = pd.read_csv("simple_signal_output/random_forest_importance.csv")
display(coefficients.head(10))
display(importance.head(10))

motif = "TATAAATG"
motif_words = {motif[start:start + 4] for start in range(len(motif) - 3)}
print("4-mers inside the planted motif:", sorted(motif_words))
```

Find words that overlap the known planted motif. Explain what that supports and what it cannot establish. Logistic-regression coefficients have a direction; forest impurity importance does not indicate whether a word raises or lowers the class-1 prediction. Their numeric scales are different.

## Practical D — slides 58–60: investigate related-sequence leakage

Open [completed notebook 02](../notebooks/02_split_leakage.ipynb) and run its setup, definitions and workflow cell. This is a separate dataset and experiment. Then inspect:

```python
import pandas as pd

leakage = pd.read_csv("course_output/leakage/metrics_comparison.csv")
display(leakage[["split", "group_overlap_count", "balanced_accuracy"]])
```

Explain which evaluation allows related families across the boundary and which holds out entire families. This exercise uses **balanced accuracy**, the mean of recall for each class. Its displayed values should not be compared directly with the main experiment's ROC-AUC.

The seed-2026 saved local run has 197 overlapping groups and balanced accuracy 1.000 for the row split, versus zero overlapping groups and 0.516 for the group split. Read the actual output of your own run. If the instructor uses saved results, identify them as previous execution.

## Short selected-code exercises


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
