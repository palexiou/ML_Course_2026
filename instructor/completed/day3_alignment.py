"""Standalone alignment exercise using explicitly synthetic features."""

from io import StringIO

import numpy as np
import pandas as pd


metadata = pd.read_csv(StringIO("""sample_id,group_id,sequence,label,split
train-01,group-01,ACGT,0,train
train-02,group-02,TATA,1,train
validation-01,group-03,CGCG,0,validation
validation-02,group-04,ATAT,1,validation
"""))
cache = pd.read_csv(StringIO("""sample_id,feature_0,feature_1
validation-02,40,4
train-02,20,2
validation-01,30,3
train-01,10,1
"""))
assert metadata["sample_id"].is_unique
assert cache["sample_id"].is_unique
assert set(cache["sample_id"]) == set(metadata["sample_id"])
assert set(metadata["split"]) == {"train", "validation"}
assert metadata.groupby("group_id")["split"].nunique().max() == 1
aligned = cache.set_index("sample_id").loc[metadata["sample_id"]]
assert aligned.index.tolist() == metadata["sample_id"].tolist()
features = aligned[["feature_0", "feature_1"]].to_numpy()
assert np.isfinite(features).all()
training_features = features[metadata["split"].to_numpy() == "train"]
validation_features = features[metadata["split"].to_numpy() == "validation"]
assert training_features[:, 0].tolist() == [10, 20]
assert validation_features[:, 0].tolist() == [30, 40]
print("SYNTHETIC CACHE: these numbers are not pretrained DNA embeddings.")
print(aligned.to_string())
print("Training shape:", training_features.shape, "Validation shape:", validation_features.shape)
print("Freeze models, preprocessing, selection, metric policy, and inference before test reveal.")
