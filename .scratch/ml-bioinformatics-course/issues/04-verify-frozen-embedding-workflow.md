# 04: Verify the frozen-embedding workflow

**What to build:** A runnable frozen-embedding comparison using a suitable pretrained DNA model, a small live extraction, provenance-tracked cached full-data embeddings, and a simple classifier on the same verified dataset variants and split identities used by earlier representations.

**Blocked by:** 03: Verify the interaction-signal and CNN comparison.

**Status:** ready-for-agent

- [ ] Select and verify a pretrained DNA model using its authoritative documentation and model information, including access, licensing conditions, dependencies, input limits, and runtime requirements.
- [ ] Record the model revision, tokenization, sequence handling, embedding layer/pooling choices, and extraction settings needed to reproduce the representation.
- [ ] Execute a small live extraction in actual Colab and measure setup and extraction time; local-only execution or successful cached classification does not satisfy this check.
- [ ] Produce cached full-data embeddings for the verified simple-signal and interaction-signal dataset variants, with reproducible provenance and explicit sample correspondence.
- [ ] Verify sequence-to-embedding row alignment and preserve each variant's existing split identities; do not allow labels or evaluation-fitted preprocessing to enter the representation workflow.
- [ ] Train and validate a simple classifier on the frozen embeddings and compare it with the earlier workflows using the agreed metric policy without revealing the protected test results.
- [ ] Demonstrate the cached practical in the supported classroom environment and record its setup and classifier-training costs separately from full extraction costs.
- [ ] Keep frozen embeddings as the required practical; explain fine-tuning only as a contrast rather than adding a mandatory training workflow.
- [ ] Record observed behavior and transfer limitations without promising improvement over k-mer or CNN representations or claiming absence of pretraining overlap without evidence.
- [ ] Deliver reproducible extraction and classification, cached artifacts, clearly identified saved outputs, and a verification record. Report any required access or runtime blocker promptly rather than silently dropping the live extraction.
