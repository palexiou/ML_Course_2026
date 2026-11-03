# Frozen DNA embedding verification

## Checkpoint and source

- Model: `InstaDeepAI/nucleotide-transformer-v2-50m-multi-species`.
- Model and executable-code revision: `81b29e5786726d891dbf929404ef20adca5b36f1`.
- Model license: CC-BY-NC-SA-4.0. The custom code files carry their own Apache-2.0 notices; that does not change the weight license.
- Downloaded `model.safetensors`: 223,642,688 bytes. Expected SHA-256: `17e75af297556ea56828716d8aa539e8f12b8b625547204b74171ab91aa33569`.
- Public, ungated checkpoint; no account or API key was required for the local download.
- Official pinned model card: <https://huggingface.co/InstaDeepAI/nucleotide-transformer-v2-50m-multi-species/blob/81b29e5786726d891dbf929404ef20adca5b36f1/README.md>.
- Pinned config and source live in the same repository revision: `config.json`, `tokenizer_config.json`, `esm_config.py`, and `modeling_esm.py`.

The web research was checked against the downloaded official files. `esm_config.py` and `modeling_esm.py` import standard-library, PyTorch, and Transformers modules. Inspection found no obvious process-launch or network-client calls. This is source inspection, not a sandbox or security guarantee. `trust_remote_code=True` is required for the custom masked-language-model architecture, with both revisions pinned. Safetensors avoids pickle-based weight loading but does not prevent executable model code from running. Only load the course's locally created joblib model files; joblib artifacts from untrusted sources can also execute code.

## Representation contract

Use `AutoModelForMaskedLM`, not an unregistered `AutoModel` mapping or a superficially similar built-in ESM architecture. The model uses custom SwiGLU layers. The built-in ESM tokenizer is loaded with `trust_remote_code=False` and `use_fast=False`.

For these 160-base unambiguous sequences, tokenization yields 26 non-overlapping six-mers, four single-base tokens, and CLS: 31 tokens. No truncation is permitted. The model card describes a 1,000-token training length, while tokenizer/configured position limits are larger; these are distinct facts, immaterial at 31 tokens. Mean pooling uses the last hidden layer and excludes all special IDs and padding. The mask is derived from input IDs, avoiding the ESM tokenizer's EOS special-mask mismatch when EOS is disabled. Embeddings have 512 components.

All weights remain frozen, `eval()` is used, and extraction runs under `torch.inference_mode()`. Labels are not passed to extraction. Cache rows include sample IDs, sequence hashes, model ID, revision, and pooling policy. Loading checks these fields, enforces exact identity coverage and finite `(n, 512)` values, and aligns by sample ID rather than trusting row order. Standardization and logistic regression are fitted on training embeddings only. Validation scores are used for the development comparison. Test embeddings are cached without scoring test labels.

## Actual local run ? October 26, 2026

Windows, Python 3.13.14, PyTorch 2.10.0+cpu, Transformers 4.57.1, CPU with two PyTorch threads, dynamic padding, batch size 32. No GPU or paid service. Direct dependency pins are in `course_code/requirements-ml.txt`.

The initial entrypoint loaded the encoder in 2.60 seconds from downloaded weights. Live two-sequence extraction took 0.226 seconds for simple-signal and 0.187 seconds for interaction-signal, excluding installation/download. Full extraction plus cache validation took 77.62 seconds for 1,200 simple-signal rows and 31.76 seconds for 480 interaction-signal rows. Original costs are preserved in `course_output/embedding_extraction_record.json`; the latest `embedding_run.json` may record a cache-based run instead. First weight download took approximately nine seconds on this connection, not a classroom network estimate. Peak memory was not measured.

The current default demonstrates a fresh two-sequence extraction on training inputs even when full-data caches exist, then uses those caches for classification. Separate `*_live_example.json` files record identities, revision, pooling, and timing. For the explicitly cached-only contingency, call `run_foundation(live_example=False)`; do not describe that route as a live extraction.

| Variant | Validation ROC-AUC | Validation average precision |
|---|---:|---:|
| Simple-signal | 0.618333 | 0.624822 |
| Interaction-signal | 0.800347 | 0.757830 |

These are actual validation results, not a promised ranking. No protected course test scores were calculated during implementation. The primary metric is ROC-AUC; average precision is not called trapezoidal PR-AUC. Threshold-based metrics use 0.5.

## Interpretation and outstanding checks

The card states that plants and viruses were excluded from this checkpoint's pretraining genomes. That is particularly relevant to a plant-motivated teaching example. We have not audited pretraining overlap, and we do not claim none exists. Neither successful transfer on artificial motif order nor failure on a small noisy motif task establishes real promoter utility. Fine-tuning is a conceptual contrast, not a required practical.

**Actual Colab execution, Colab setup/extraction costs, classroom network behavior, and instructor full-session rehearsal are not run.** The user will paste and arrange code manually in Colab. Local success is not a claim that those checks passed. A cached practical is a separately labeled contingency, not evidence of a fresh live extraction.

## Current PPM lesson verification — 2026-11-03

The [current source-bound record](day3-current.json) supersedes the October 26 primary fixed-motif values **for current slide comparisons**. The earlier run remains historical evidence. The generated combined notebook's Day 3 path executed locally using the compatible, already-fitted current stage 03 outputs; no configuration search or retuning followed.

| Variant | Frozen NT + logistic validation ROC-AUC | Average precision |
| --- | ---: | ---: |
| Current primary 15-position PPM | 0.496597 | 0.545287 |
| Fixed-slot paired order control | 0.800347 | 0.757830 |

The record includes all four matched workflows, scientific/notebook/teaching source hashes, dataset generation identities, artifact hashes, exact package versions and actual training-vector excerpts. The downloaded weight SHA-256 matched the expected value above. The pinned config confirms 12 layers, 16 heads, hidden width 512 and rotary position encoding. Model and code revisions remain pinned; custom-code source hashes were inspected against the pinned snapshot. No scientific defaults changed.

A separate small live checkpoint extracts the first two training sequences of each variant, verifies 31 tokens and finite `(2, 512)` outputs, and pauses. The canonical full-cache call then extracts or reuses every row; absent caches cause extraction even with `live_example=False`. Its initial current local extraction/cache-check times were **36.078 s** for 1,200 primary rows and **14.105 s** for 480 control rows; classifier fits were **0.091 s** and **0.020 s**. These wall times include the canonical internal consistency example and cache checks; they are not raw forward-only throughput or Colab estimates. First weight download/setup are separate. Later notebook readbacks reused the completed run without refitting, so the initial extraction timings remain in `embedding_run.json`.

Readback verified training-only scaler means (float64 accumulation), matching validation sample IDs/groups/labels, saved/recomputed probabilities and ROC-AUC/AP, and agreement between live and batched vectors. Synthetic alignment checks accept reordered rows and reject missing/duplicate IDs. A separate copy of the development workspace successfully ran the notebook's freeze, captured all 32 artifacts and source/package identities, and refused a second freeze. **The reveal was never called; no protected course test results were calculated.** The development workspace itself remains unfrozen.

Reproduce locally with `MPLBACKEND=Agg python tools/rehearse_day3.py --workspace /path/to/compatible/day2-workspace`. Dependencies and pinned weights must be available; the script expects the complete Day 2 workspace. It writes the source-bound record and tests freeze in a separate temporary copy. The [67-scene deck](../../Slides/Day_3/presentation.html) builds from this record with `python tools/build_day3_slides.py`. [Slide QA](../../Slides/qa.md#day-3-implementation--2026-11-03) covers the offline lesson controls and empty test-result defaults.

**Hosted Colab execution, setup/download cost on the classroom network, projector readability, measured teaching pace and the authorised classroom test reveal remain unverified.** Main-branch Colab links include the new teaching cells only after publication.
