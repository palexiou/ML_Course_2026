"""Audit a manually authored fixture; this is not a real agent transcript."""

from io import StringIO

import pandas as pd


samples = pd.read_csv(StringIO("""sample_id,group_id,sequence,label,split
train-01,group-a,ACGTACGT,0,train
train-02,group-b,TATAAATG,1,train
validation-01,group-a,ACGTACGA,0,validation
validation-02,group-c,TATAAATA,1,validation
"""))
predictions = pd.read_csv(StringIO("""sample_id,probability
validation-02,0.1
validation-01,0.9
"""))
training = samples.loc[samples["split"] == "train"]
validation = samples.loc[samples["split"] == "validation"]
assert samples["sample_id"].is_unique
assert predictions["sample_id"].is_unique
assert set(predictions["sample_id"]) == set(validation["sample_id"])
assert predictions["probability"].between(0, 1).all()
overlap = set(training["group_id"]) & set(validation["group_id"])
aligned_predictions = validation[["sample_id", "label"]].merge(predictions, on="sample_id", validate="one_to_one")
positional_accuracy = (validation["label"].to_numpy() == (predictions["probability"].to_numpy() >= 0.5)).mean()
aligned_accuracy = (aligned_predictions["label"] == (aligned_predictions["probability"] >= 0.5)).mean()
assert overlap == {"group-a"}
assert positional_accuracy == 1.0
assert aligned_accuracy == 0.0
print("MANUALLY AUTHORED FIXTURE, NOT AN AGENT RUN")
print("Overlapping groups:", sorted(overlap))
print("Invalid positional accuracy:", positional_accuracy)
print("ID-aligned accuracy:", aligned_accuracy)
print("Neither score fixes group leakage. Repair the separate experiment and refit.")
