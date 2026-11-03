# Day 1: notebook instructions

Keep this guide beside a Colab notebook. The presentation tells you when to switch here. Python runs in the notebook; the slide itself is a visual explanation or activity prompt.

## Setup — slides 1–4

Open a blank notebook in Colab and run:

```python
print("Ready for ML")
import numpy as np
import pandas as pd
import sklearn
import matplotlib
```

If an import is missing, install the missing package in a separate cell. For example, `%pip install numpy pandas scikit-learn matplotlib`. Follow Colab's restart prompt if one appears. Setup takes place during class. If access fails, follow the instructor's notebook and discuss the same questions.

## Practical A — slides 20–22: inspect the data and count words

### 1. Run the supplied workflow once

Open [standalone code 01](../paste_ready/01_simple_signal.py), copy the **whole file** into a Python cell, and run it. It creates `simple_signal_output/`, fits both classical models, and displays validation outputs. We will interpret those outputs later in the lesson. It does not evaluate the protected test partition.

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

Open [standalone code 02](../paste_ready/02_split_leakage.py), paste the whole file into a new cell, and run it. This is a separate dataset and experiment. Then inspect:

```python
import pandas as pd

leakage = pd.read_csv("course_output/leakage/metrics_comparison.csv")
display(leakage[["split", "group_overlap_count", "balanced_accuracy"]])
```

Explain which evaluation allows related families across the boundary and which holds out entire families. This exercise uses **balanced accuracy**, the mean of recall for each class. Its displayed values should not be compared directly with the main experiment's ROC-AUC.

The seed-2026 saved local run has 197 overlapping groups and balanced accuracy 1.000 for the row split, versus zero overlapping groups and 0.516 for the group split. Read the actual output of your own run. If the instructor uses saved results, identify them as previous execution.
