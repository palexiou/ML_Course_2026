"""Standalone miniature development-only fixture, not the primary PPM simulator."""

from io import StringIO

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, confusion_matrix, roc_auc_score
from sklearn.pipeline import Pipeline


development_csv = """sample_id,group_id,sequence,label,split
train-01,group-01,AAAATATAAATGCCCC,1,train
train-02,group-02,CCCCTATAAATGAAAA,1,train
train-03,group-03,GGGGTATAAATGTTTT,1,train
train-04,group-04,TTTTTATAAATGGGGG,1,train
train-05,group-05,AAAACGCGCGCGCCCC,0,train
train-06,group-06,CCCCCGCGCGCGAAAA,0,train
train-07,group-07,GGGGCGCGCGCGTTTT,0,train
train-08,group-08,TTTTCGCGCGCGGGGG,0,train
validation-01,group-09,ACACTATAAATGCACA,1,validation
validation-02,group-10,CACACGCGCGCGACAC,0,validation
validation-03,group-11,GTGTTATAAATGTGTG,1,validation
validation-04,group-12,TGTGCGCGCGCGGTGT,0,validation
"""
development = pd.read_csv(StringIO(development_csv))
training = development.loc[development["split"] == "train"].copy()
validation = development.loc[development["split"] == "validation"].copy()
assert development["sample_id"].is_unique
assert set(development["split"]) == {"train", "validation"}
assert set(training["group_id"]).isdisjoint(validation["group_id"])
model = Pipeline([
    ("kmers", CountVectorizer(analyzer="char", ngram_range=(4, 4), lowercase=False)),
    ("classifier", LogisticRegression(max_iter=2000, random_state=2026)),
])
model.fit(training["sequence"], training["label"])
probabilities = model.predict_proba(validation["sequence"])[:, 1]
predictions = pd.DataFrame({"sample_id": validation["sample_id"], "probability": probabilities})
evaluated = validation[["sample_id", "label"]].merge(predictions, on="sample_id", validate="one_to_one")
print("Miniature authored development example; not the full course experiment.")
print(predictions.to_string(index=False))
print("Validation ROC-AUC:", roc_auc_score(evaluated["label"], evaluated["probability"]))
print("Validation average precision:", average_precision_score(evaluated["label"], evaluated["probability"]))
print("Confusion matrix at 0.5 (rows=true, columns=predicted; labels 0,1):")
print(confusion_matrix(evaluated["label"], evaluated["probability"] >= 0.5, labels=[0, 1]))
