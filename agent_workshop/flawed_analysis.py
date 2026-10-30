"""DELIBERATELY FLAWED, MANUALLY AUTHORED FIXTURE; not an agent run."""

from io import StringIO

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


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
vectorizer = CountVectorizer(analyzer="char", ngram_range=(4, 4), lowercase=False)
vectorizer.fit(samples["sequence"])
assert set(training["sample_id"]).isdisjoint(validation["sample_id"])
reported_accuracy = (validation["label"].to_numpy() == (predictions["probability"].to_numpy() >= 0.5)).mean()
print("MANUALLY AUTHORED, DELIBERATELY FLAWED FIXTURE; probabilities are invented.")
print("Misleading positional accuracy:", reported_accuracy)
print("Authored unsupported claim: unique sample IDs prove no leakage and this predicts real promoters.")
