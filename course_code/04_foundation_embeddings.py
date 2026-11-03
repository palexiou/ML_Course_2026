"""Frozen DNA embeddings with aligned caches and validation-only classification."""

from pathlib import Path
from time import perf_counter
from typing import Any
import hashlib
import json

import joblib
import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from transformers import AutoModelForMaskedLM, AutoTokenizer

from course_core import read_dataset, validation_metrics, write_json, file_hash

from course_inference import MODEL_ID, REVISION, POOLING, sequence_hashes, load_embedding_cache


def load_frozen_encoder() -> tuple[Any, Any]:
    torch.set_num_threads(2)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION, trust_remote_code=False, use_fast=False)
    model = AutoModelForMaskedLM.from_pretrained(MODEL_ID, revision=REVISION, code_revision=REVISION, trust_remote_code=True, use_safetensors=True)
    model.to(device="cpu", dtype=torch.float32)
    model.eval()
    model.requires_grad_(False)
    return tokenizer, model


def extract_embeddings(sequences: list[str], tokenizer: Any, model: Any, batch_size: int = 32) -> np.ndarray:
    if batch_size < 1 or not sequences or any(len(sequence) != 160 or set(sequence) - set("ACGT") for sequence in sequences):
        raise ValueError("Expected nonempty 160-bp ACGT sequences and a positive batch size")
    excluded = set(tokenizer.all_special_ids)
    batches = []
    with torch.inference_mode():
        for start in range(0, len(sequences), batch_size):
            encoded = tokenizer(sequences[start:start + batch_size], return_tensors="pt", padding=True, truncation=False)
            outputs = model(**encoded, output_hidden_states=True)
            mask = encoded["attention_mask"].bool()
            for token_id in excluded:
                mask &= encoded["input_ids"] != token_id
            if not mask.any(dim=1).all():
                raise ValueError("A sequence contains no poolable DNA tokens")
            hidden = outputs.hidden_states[-1]
            pooled = (hidden * mask.unsqueeze(-1)).sum(dim=1) / mask.sum(dim=1, keepdim=True)
            batches.append(pooled.cpu().numpy())
    return np.concatenate(batches)


def run_foundation(output_dir: str | Path = "course_output", live_example: bool = True) -> pd.DataFrame:
    root = Path(output_dir)
    if any((root / marker).exists() for marker in ("frozen_manifest.json", "test_results.json")):
        raise RuntimeError("This experiment is frozen or revealed. Use a new development directory instead of tuning it.")
    results, records = [], {}
    tokenizer, model = None, None
    for variant in ("simple", "interaction"):
        samples = read_dataset(root / "datasets" / variant)
        cache_path = root / "embeddings" / f"{variant}.npz"
        started = perf_counter()
        if cache_path.exists():
            load_embedding_cache(cache_path, samples)
        extracted = not cache_path.exists()
        live_seconds = None
        live = None
        if live_example or extracted:
            if model is None:
                load_started = perf_counter()
                tokenizer, model = load_frozen_encoder()
                print(f"Encoder load: {perf_counter() - load_started:.2f}s, CPU")
            live_started = perf_counter()
            live_samples = samples.loc[samples["split"] == "train"].head(2)
            live = extract_embeddings(live_samples["sequence"].tolist(), tokenizer, model)
            live_seconds = perf_counter() - live_started
            print(f"{variant}: live two-sequence extraction {live.shape}, {live_seconds:.3f}s")
            write_json(root / f"{variant}_live_example.json", {"model_id": MODEL_ID, "revision": REVISION, "pooling": POOLING, "sample_ids": live_samples["sample_id"].tolist(), "shape": list(live.shape), "seconds": live_seconds, "device": "cpu", "cache_used_for_this_example": False})
        if extracted:
            embeddings = extract_embeddings(samples["sequence"].tolist(), tokenizer, model)
            if live is not None and not np.allclose(live, embeddings[:2], atol=1e-4, rtol=1e-4):
                raise ValueError("Live and batched extraction disagree")
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(cache_path, sample_ids=samples["sample_id"].to_numpy(dtype=str), sequence_sha256=sequence_hashes(samples), embeddings=embeddings, model_id=np.array(MODEL_ID), revision=np.array(REVISION), pooling=np.array(POOLING), dataset_generation_sha256=np.array(samples.attrs["dataset_generation_sha256"]))
        features = load_embedding_cache(cache_path, samples)
        extraction_seconds = perf_counter() - started
        train_mask = samples["split"] == "train"
        validation_mask = samples["split"] == "validation"
        classifier = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000, random_state=2026))
        fit_started = perf_counter()
        classifier.fit(features[train_mask], samples.loc[train_mask, "label"])
        fit_seconds = perf_counter() - fit_started
        probabilities = classifier.predict_proba(features[validation_mask])[:, 1]
        metrics = validation_metrics(samples.loc[validation_mask, "label"], probabilities)
        results.append({"variant": variant, "method": "foundation", **metrics})
        destination = root / "models" / variant
        destination.mkdir(parents=True, exist_ok=True)
        joblib.dump(classifier, destination / "foundation.joblib")
        predictions = samples.loc[validation_mask, ["sample_id", "group_id", "label"]].copy()
        predictions["probability"] = probabilities
        predictions.to_csv(destination / "foundation_validation_predictions.csv", index=False)
        records[variant] = {"dataset_generation_sha256": file_hash(root / "datasets" / variant / "generation.json"), "cache": str(cache_path.relative_to(root)), "cache_created_this_run": extracted, "cache_load_or_extraction_seconds": extraction_seconds, "live_two_sequence_seconds": live_seconds, "classifier_fit_seconds": fit_seconds, "training_ids": samples.loc[train_mask, "sample_id"].tolist(), "validation_ids": samples.loc[validation_mask, "sample_id"].tolist(), "test_evaluated": False}
    result = pd.DataFrame(results)
    result.to_csv(root / "embedding_validation.csv", index=False)
    write_json(root / "embedding_run.json", {"model_id": MODEL_ID, "revision": REVISION, "pooling": POOLING, "license": "CC-BY-NC-SA-4.0", "device": "cpu", "torch_version": torch.__version__, "batch_size": 32, "runs": records, "limitation": "Frozen pretraining does not guarantee transfer to engineered motif order or real promoters. Pretraining overlap has not been audited."})
    print(result[["variant", "roc_auc", "average_precision"]].to_string(index=False))
    print("Validation only. Test labels were not scored. Full-data cache use and small live examples are recorded separately.")
    return result


if __name__ == "__main__":
    run_foundation()
