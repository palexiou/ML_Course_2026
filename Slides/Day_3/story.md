# Day 3 story

**Section-by-section breakdown for instructor review — 2026-11-03.** All six sections are specified slide by slide. Each slide has an ID, a timing, the slide content, speaking notes, pointing/reveal guidance and a transition, following the [Day 2 story](../Day_2/story.md) format. These are discussion beats, not implemented slides. The [current Day 3 deck](presentation.html) still holds its 15 earlier scenes. Titles, emphasis and pacing remain editable.

**Working title:** Borrowing learned representations, then opening the sealed test.

**The story:** Yesterday we trained a CNN to learn its own local detectors from our labelled DNA. Today we ask whether useful features can be learned *before* seeing our labels. We build the idea of an embedding, then transfer learning and self-supervised masking, then attention and contextual token vectors. Next we extract real vectors from a pinned Nucleotide Transformer and discover that a cache with the right shape can still describe the wrong samples. We compare all four workflows on validation data, discuss domain shift and the genome-scale frontier, and finally freeze every decision before opening the protected test set once.

**End-of-day understanding:** An embedding is a learned numerical representation. Self-supervised pretraining produces representations without our labels, but towards a different objective. Attention mixes information across positions, so the same token can receive different vectors in different contexts. A frozen encoder plus a small, training-fitted classifier is a specific, reproducible representation contract. Cache rows must be aligned by sample identity, never by row position. Borrowed features do not win by default. A revealed test result is historical evidence that cannot guide further tuning.

**Delivery and style:** Use the approved speaker-led style: one short title, one main visual, generous whitespace, blue `#0072B2` / orange `#D55E00` contrast, letters and shapes as well as colour, and detailed notes. Following the Day 2 direction, prefer illustrations (DNA ribbons, token tiles, attention arcs, vector strips, scatter clusters) to box diagrams. Notebook work is **GitHub ipynb → Open in Colab**, with instructor demonstration and optional follow-along. There is no homework or submission. Questions are conversations, not scored checks.

**Reference deck:** The instructor supplied an earlier deck, *Introduction to Foundation Models and Self-Supervised Learning in Biology* (2026), as a style and progression source. These beats reuse its ideas: the learned/compact/semantic embedding definition, the broad → specific transfer diagram, the characters → k-mers → learned-token progression, the contextualised `ATG` example, the `[MASK]` → `ATG` puzzle, the DNABERT architecture and AlphaGenome. Rebuild these figures natively in the approved style. Third-party figures (DNABERT, Zeiler & Fergus, AlphaGenome) keep their citations if reused directly.

## Three-hour shape

| Minutes | Section | Main question | Teaching minutes |
| --- | --- | --- | --- |
| 0–25 | 1. From trained detectors to borrowed representations | Can useful features be learned before seeing our labels? | 25 |
| 25–50 | 2. Attention and contextual embeddings | How does a transformer turn a sequence into one vector? | 25 |
| 50–60 | Break | | — |
| 60–80 | 3. Small live extraction and provenance | What does the encoder actually output, and at what cost? | 20 |
| 80–100 | 4. The cache audit: identity, alignment, classification | What if the vectors meet the wrong rows? | 20 |
| 100–110 | Break | | — |
| 110–140 | 5. Validation comparison across representations | When do borrowed features help, and when not? | 30 |
| 140–180 | 6. The evaluation boundary: freeze and reveal | How do we open the test set once and defend the result? | 40 |

**160 teaching minutes + 20 break minutes = 180 minutes.** There are 65 content beats (11/12/9/7/12/14) and two break slides. All timings are suggested allocations, not measured pacing. The breaks stay at 50–60 and 100–110. Section 6 keeps the [instructor guide](../../instructor/guide.md#day-3--reuse-a-pretrained-representation)'s protected blocks: freeze checklist at 140–150, single reveal at 150–165, interpretation at 165–175, recap at 175–180. **One proposed deviation from the guide:** live extraction and provenance take 60–80 instead of 60–75, and the alignment practical starts at about 89:30. This is for instructor review; the guide and [annotated outline](../teaching-outline.md#day-3--pretraining-and-frozen-embeddings) are unchanged.

**Sections:** [1 · Borrowed representations](#section-1) · [2 · Attention and embeddings](#section-2) · [3 · Live extraction](#section-3) · [4 · Cache audit](#section-4) · [5 · Comparison](#section-5) · [6 · Freeze and reveal](#section-6) · [Notebook plan](#notebook-plan) · [Evidence and scope](#evidence-and-scope)

<a id="section-1"></a>

## 1. From trained detectors to borrowed representations · 0–25

**Story question:** Can useful sequence features be learned before seeing our course labels?

**Exit understanding:** Connect Day 2's trained filters to transfer learning. Define an embedding as learned, compact and semantic. Explain self-supervised masking and how its objective differs from ours. Distinguish frozen extraction from fine-tuning. Keep the evaluation rules unchanged.

**Teaching thread:** Start from Day 2's final question, "Can we borrow features already learned?". Build the ideas in order: embedding → transfer → self-supervision → masking → objective mismatch → frozen versus fine-tuned. The Dog/Cat/Bird clusters from the reference deck give an intuitive picture of an embedding before any DNA model appears.

**Scope and delivery:** This section is conceptual only: no notebook and no setup. Attention mechanics belong to Section 2 and real vectors to Section 3. Fine-tuning is a conceptual contrast, not a practical.

### S1-01 · Can we borrow features?

**Proposed slide ID:** `day-3-s1-welcome` · **Time:** 0:00–1:30 (1:30)

**What is on slide:** Day 3 title. One illustrated DNA ribbon feeds three paths: Day 1 count bars, Day 2 sliding detector, and a new pretrained encoder whose path continues to "our small classifier". The four-day journey highlights Day 3.

**What I want to say:** On Day 1 we chose what to count. On Day 2 the CNN learned its own detectors, but only from our 720 training sequences. Today we ask a third question: could the features come from a model that has already read far more DNA than we have?

**Point / reveal:** Reveal the three paths left to right. Keep the encoder path greyed until the final sentence.

**Transition:** First, what did the CNN's parameters actually learn from?

### S1-02 · What did we train yesterday?

**Proposed slide ID:** `day-3-s1-recap` · **Time:** 1:30–3:30 (2:00)

**What is on slide:** Two matched illustrated routes: 4-mer counts → logistic weights → probability, and one-hot DNA → learned filters → pooling/head → probability. Orange markers show every place where parameters were fitted to our labels.

**What I want to say:** Yesterday every filter weight started random and was adjusted using our training labels only. The detectors were tailored to this task, but they knew nothing about DNA outside these sequences. Invite a couple of answers: what would help if we had only 50 labelled sequences?

**Point / reveal:** Light up the orange "fitted here" markers one route at a time.

**Transition:** If features can be learned elsewhere, what exactly would we be borrowing?

### S1-03 · An embedding is a learned representation

**Proposed slide ID:** `day-3-s1-what-is-embedding` · **Time:** 3:30–5:30 (2:00)

**What is on slide:** Reference-deck idea rebuilt natively: Dog, Cat and Bird images → a short vector strip of numbers → a 2-D scatter with three labelled clusters. Three labels underneath: **Learned** from data; **Compact** — many inputs, one fixed-length vector; **Semantic** — similar inputs land close together.

**What I want to say:** An embedding is a list of numbers that a model learned to produce for each input. Nobody wrote the rules: training arranged the space so that similar inputs end up near each other. Count features were coordinates we designed; embedding coordinates are learned, so a single dimension rarely has a human name.

**Point / reveal:** Show the inputs, then the vector, then the clusters. Point out that the axes are labelled only "Dim 1 / Dim 2".

**Transition:** How would such a space help our small DNA task?

### S1-04 · Learn broadly, then adapt

**Proposed slide ID:** `day-3-s1-transfer-concept` · **Time:** 5:30–7:30 (2:00)

**What is on slide:** The reference deck's two-row transfer diagram, rebuilt natively. Orange top row: broad DNA → generic data → pretrained network → generic task. A dashed arrow passes the network down. Blue bottom row: our sequences → pretrained backbone + small task head → Class A / Class B.

**What I want to say:** Transfer learning trains a large network once on broad data, then reuses that backbone for a specific task. Only a small head needs our labels. In biology, labelled data is scarce and sequences are plentiful, which is why this pattern is so attractive.

**Point / reveal:** Reveal the top row, then the dashed transfer arrow, then the head. Orange marks borrowed parts; blue marks what our labels train.

**Transition:** But how does the top row learn anything without labels?

### S1-05 · Labels from people, or targets from the data

**Proposed slide ID:** `day-3-s1-supervision` · **Time:** 7:30–10:00 (2:30)

**What is on slide:** Two cards with sequence illustrations. Supervised: sequence + label B → loss. Self-supervised: sequence alone → part hidden → the hidden part becomes the target.

**What I want to say:** Supervised learning needs a label from outside the sequence, like our A/B classes. Self-supervised learning builds its target from the input itself, so any sequence can be used. Pretraining therefore needs no promoter assays and no course labels.

**Point / reveal:** Show supervised first. Then animate one piece of the sequence moving out of the right card to become the target.

**Transition:** The most common way to hide a piece is called masking.

### S1-06 · Hide a token, predict it from context

**Proposed slide ID:** `day-3-s1-masked-lm` · **Time:** 10:00–12:30 (2:30)

**What is on slide:** The reference deck's puzzle: `ACG` `TCC` `[MASK]` `GCT` `GAA` → "predict the missing token" → `ATG`. Beside it, a small bar chart of model probabilities over several candidate tokens, with `ATG` tallest. The label reads "self-supervised learning".

**What I want to say:** In masked language modelling, we hide some tokens and train the model to predict them from the surrounding tokens. The model outputs probabilities over its vocabulary, not a certain answer. The loss rewards a high probability for the true hidden token. This is a conceptual illustration: three-letter tokens and these probabilities are not output from our checkpoint, whose tokens are mostly six-mers (Section 2).

**Point / reveal:** Mask the tile first and pause for student guesses. Then reveal the probability bars, then the true token.

**Transition:** Why would solving millions of these puzzles produce useful features?

### S1-07 · What masking can teach

**Proposed slide ID:** `day-3-s1-what-is-learned` · **Time:** 12:30–15:00 (2:30)

**What is on slide:** Three illustrated levels: local composition and short-word statistics; recurring patterns and their neighbours; longer-range regularities. Each level uses a highlighted DNA ribbon. A caption reads "what *can* help prediction — not a guarantee of what a given model learned".

**What I want to say:** To predict hidden tokens well, it helps to capture composition, recurring motifs and dependencies between distant positions. Whatever helps the prediction can end up stored in the internal representation. Which of these a particular model actually captures is an empirical question.

**Point / reveal:** Reveal the levels bottom-up, with a widening highlight on the ribbon.

**Transition:** And the prediction it was trained for is not ours.

### S1-08 · Their question is not our question

**Proposed slide ID:** `day-3-s1-objective-mismatch` · **Time:** 15:00–18:00 (3:00)

**What is on slide:** Two speech bubbles over the same sequence. Pretraining asks, "Which token is hidden here?" Our course asks, "Is this simulated sequence A or B?" A gap between them is labelled "transfer?".

**What I want to say:** The encoder was trained to reconstruct natural genomes, not to separate our simulated classes. Its features may help, may be irrelevant, or may even emphasise unrelated properties. Ask students to predict one reason transfer might fail here; we will test that prediction in Section 5.

**Point / reveal:** Show both bubbles, then the question mark gap. Leave student predictions visible.

**Transition:** If we do borrow the encoder, how much of it do we change?

### S1-09 · Frozen or fine-tuned

**Proposed slide ID:** `day-3-s1-frozen-vs-finetuned` · **Time:** 18:00–21:00 (3:00)

**What is on slide:** Two illustrated pipelines. Frozen: encoder with a padlock → fixed vector → trainable small classifier (blue). Fine-tuned: unlocked encoder with gradient arrows flowing back through every layer.

**What I want to say:** Fine-tuning lets our task loss update some or all encoder weights. Frozen extraction locks the encoder: it becomes a fixed function from sequence to vector, and only the small classifier learns from our labels. Ask: which part sees the course labels in each case?

**Point / reveal:** Animate the gradient arrows stopping at the padlock in the frozen route, and flowing through in the fine-tuned route.

**Transition:** Why does this course use the frozen route?

### S1-10 · Why frozen here

**Proposed slide ID:** `day-3-s1-why-frozen` · **Time:** 21:00–23:30 (2:30)

**What is on slide:** Three illustrated reasons. Computation: CPU-sized, no GPU or paid service. Overfitting risk: about 50 million weights against 720 labelled training rows. Clear comparison: we assess the borrowed representation itself.

**What I want to say:** Updating tens of millions of weights with 720 labelled examples risks overfitting and needs more compute than a classroom laptop. Freezing also makes the comparison cleaner: we test how informative the borrowed vectors are next to counts and the CNN. Fine-tuning remains a valid tool in other settings; it is simply not today's practical.

**Point / reveal:** Reveal the three reasons in turn.

**Transition:** One final check before we open the encoder.

### S1-11 · Do we still need a test set?

**Proposed slide ID:** `day-3-s1-check-question` · **Time:** 23:30–25:00 (1:30)

**What is on slide:** Question: "The encoder read billions of bases. Do we still need protected test data for our classifier?" Options: A) No — it has already generalised; B) Yes — our classifier learns from our labels and must be judged on unseen samples.

**What I want to say:** Pretraining changes where the features come from. It does not change the rules of evaluation. The classifier is fitted on our training rows, so validation and the protected test keep exactly the roles they had on Days 1–2.

**Point / reveal:** Take a show of hands, then reveal B.

**Transition:** So how does a transformer actually turn our DNA into a vector?

<a id="section-2"></a>

## 2. Attention and contextual embeddings · 25–50

**Story question:** How does a transformer encoder turn ordered DNA into one fixed-length vector?

**Exit understanding:** Explain tokenisation choices and our checkpoint's 31 tokens. Explain attention as a weighted combination that lets context change a token's vector. State that attention weights are not causal evidence. Describe the last hidden layer, mean pooling and the representation contract. Name the parts of the downstream classifier.

**Teaching thread:** Keep one tokenised sequence visible as it becomes token tiles, then contextual vectors, then one pooled 512-number strip, then a probability. The reference deck's `ATG` example motivates context before any arithmetic.

**Scope and delivery:** This section is conceptual, using small worked numbers only. Detailed transformer mechanics (normalisation, feed-forward details, positional-encoding variants) are a cut priority. Real vectors appear in Section 3.

### S2-01 · Every position can look at every other

**Proposed slide ID:** `day-3-s2-borrowing-context` · **Time:** 25:00–27:00 (2:00)

**What is on slide:** Left: Day 2's detector window covers a few neighbouring bases. Right: the same sequence with arcs from one token to every other token, thicker arcs for stronger weights.

**What I want to say:** A convolution filter sees a fixed local window, and distant relationships need several layers. In a transformer layer, each position can draw information from every other position, with learned weights that depend on the content.

**Point / reveal:** Show the window, then fade it and draw the arcs.

**Transition:** But first we must decide what counts as one position.

### S2-02 · From letters to tokens

**Proposed slide ID:** `day-3-s2-tokenization-progression` · **Time:** 27:00–29:30 (2:30)

**What is on slide:** The reference deck's progression: characters `A T G C T A A G C T` → k-mers `ATG CTA AGC` → learned tokens `ATGC TAA GCT`. Arrow above: "larger tokens → shorter sequences".

**What I want to say:** A transformer works on tokens. Single bases give long sequences. Fixed k-mers or learned subword tokens give fewer, larger tokens. Shorter token sequences make attention much cheaper, because every token interacts with every other token. Different DNA models make different choices.

**Point / reveal:** Reveal left to right, with the token count shrinking under each panel.

**Transition:** What does our checkpoint do with a 160-base sequence?

### S2-03 · Our sequence becomes 31 tokens

**Proposed slide ID:** `day-3-s2-our-tokens` · **Time:** 29:30–31:00 (1:30)

**What is on slide:** A 160-base ribbon is cut into 26 non-overlapping six-base tiles, then four single-base tiles, preceded by a `CLS` tile. Total: 31.

**What I want to say:** For our unambiguous 160-base sequences, the pinned tokenizer produces 26 six-mers, four single-base tokens and one CLS token. Nothing is truncated. Notice that these six-mers are tiled, not overlapping like our Day 1 counts.

**Point / reveal:** Count 6 × 26 = 156 aloud, then add the 4 leftover bases and the CLS tile.

**Transition:** Now, how can context change what a token means?

### S2-04 · Context changes a token's vector

**Proposed slide ID:** `day-3-s2-atg-context-example` · **Time:** 31:00–34:00 (3:00)

**What is on slide:** The reference deck's example. `CCA GGC TCC [ATG] GCT GAA CTG TAA`, bracketed as "5′ UTR tokens" and "coding context". Step 1: `ATG` with a "generic embedding" strip. Step 2: attention arcs from `ATG` to its neighbours. Step 3: a "contextualised embedding" strip with the tick "start codon".

**What I want to say:** On its own, the input vector for `ATG` is the same wherever `ATG` appears. After attention it also contains information from its context, so an `ATG` followed by an open reading frame can be represented differently from an `ATG` elsewhere. This is a conceptual illustration with codon-sized tokens and invented numbers. It shows the idea of contextual vectors, not an inspected neuron in our checkpoint.

**Point / reveal:** Use three steps: generic vector, arcs, contextual vector. Keep the numbers small and labelled "illustrative".

**Transition:** How are those arcs turned into a new vector?

### S2-05 · Attention is a weighted average

**Proposed slide ID:** `day-3-s2-attention-intuition` · **Time:** 34:00–36:00 (2:00)

**What is on slide:** Two tokens with values 2 and 6 and weights 0.75 and 0.25. The calculation `0.75 × 2 + 0.25 × 6 = 3` builds step by step. Weights are non-negative and sum to 1.

**What I want to say:** Attention turns relevance scores into weights that sum to one, then averages the other tokens' values with those weights. Ask students to compute the result before revealing it: 1.5 + 1.5 = 3. Real models average vectors, not single numbers, and repeat this in several heads and layers.

**Point / reveal:** Show the weights, pause for the answer, reveal 3.

**Transition:** Where do the weights come from?

### S2-06 · Queries, keys and values

**Proposed slide ID:** `day-3-s2-qkv-concept` · **Time:** 36:00–38:00 (2:00)

**What is on slide:** One token emits three coloured arrows: query ("what am I looking for?"), key ("what do I offer?") and value ("what do I pass on?"). Matching query/key pairs produce large scores; softmax turns the scores into weights.

**What I want to say:** Each token computes a query, a key and a value using learned weights. A query that matches another token's key gives a high score. Softmax converts the scores into the weights we just used, and the values are what gets averaged. This is the intuition; we will not derive the matrix form.

**Point / reveal:** Highlight one query–key pair, then its weight, then its value flowing into the output.

**Transition:** Can we read biology directly from those weights?

### S2-07 · Attention weights are not explanations

**Proposed slide ID:** `day-3-s2-attention-caution` · **Time:** 38:00–39:30 (1:30)

**What is on slide:** An attention heatmap with one bright cell, crossed through by the caption "high weight ≠ biological cause".

**What I want to say:** A large attention weight shows where information flowed in one head of one layer. It does not show that this position causes the biological outcome. Many heads and layers interact, and later operations transform the result. Causal claims need perturbation and independent biological evidence.

**Point / reveal:** Show the heatmap, then the caption.

**Transition:** Now stack these layers into a full encoder.

### S2-08 · Stack the layers

**Proposed slide ID:** `day-3-s2-ntv2-architecture` · **Time:** 39:30–42:00 (2:30)

**What is on slide:** An illustrated encoder: token tiles plus positional information → repeated attention + feed-forward blocks → one contextual 512-number strip per token. A credit line: architecture after DNABERT (Ji et al., *Bioinformatics* 2021), and the Nucleotide Transformer v2 checkpoint we use.

**What I want to say:** DNABERT showed the BERT-style recipe for DNA: tokenise, add position information, pass through repeated attention blocks, pretrain by masking. Our checkpoint, Nucleotide Transformer v2 with about 50 million parameters, follows this encoder pattern with its own custom layers. Its last layer gives a 512-number vector for each of the 31 tokens.

**Point / reveal:** Build the stack one block at a time. Keep the 31 token columns aligned from bottom to top.

**Transition:** We have 31 vectors, but the classifier needs one.

### S2-09 · Average the DNA tokens

**Proposed slide ID:** `day-3-s2-mean-pooling` · **Time:** 42:00–44:30 (2:30)

**What is on slide:** A 31 × 512 grid with the CLS column greyed out. The remaining 30 columns are averaged into one 512-number strip.

**What I want to say:** We take the last hidden layer and average the vectors of the DNA tokens, excluding CLS and any padding. Every sequence now has exactly 512 numbers. Averaging is a choice, and Slide S2-12 asks what it might lose.

**Point / reveal:** Grey out CLS, then collapse the columns into one strip.

**Transition:** Every one of these choices must be written down.

### S2-10 · The representation contract

**Proposed slide ID:** `day-3-s2-representation-contract` · **Time:** 44:30–46:30 (2:00)

**What is on slide:** A short contract card. Model: `InstaDeepAI/nucleotide-transformer-v2-50m-multi-species`. Revision: `81b29e5…` (full hash in Notes). Layer: last hidden state. Pooling: mean, excluding special tokens and padding. Output: 512 numbers per sequence.

**What I want to say:** "The embedding" is not one universal thing. A different revision, layer or pooling rule gives different numbers and potentially different conclusions. Our code records this contract, and the cache in Section 3 stores it beside every vector.

**Point / reveal:** Reveal one line at a time.

**Transition:** What learns from our labels?

### S2-11 · The small classifier on top

**Proposed slide ID:** `day-3-s2-downstream-head` · **Time:** 46:30–48:30 (2:00)

**What is on slide:** DNA → padlocked encoder → 512-number strip → standardise → logistic regression → P(B). The last two steps are marked "fitted on training rows only".

**What I want to say:** Only the scaling and the logistic regression learn from labels. Like Day 1's pipeline, both are fitted on training rows, and validation is transformed using the training statistics. The code uses `StandardScaler` and `LogisticRegression(C=1.0, max_iter=2000)`.

**Point / reveal:** Show the padlock first, then highlight the two trainable steps in blue.

**Transition:** Before the break: what might this pipeline miss?

### S2-12 · What might averaging lose?

**Proposed slide ID:** `day-3-s2-discussion` · **Time:** 48:30–50:00 (1:30)

**What is on slide:** Two sequences with the same motifs in swapped positions, both averaged into strips. Question: "What could two different sequences share after averaging?"

**What I want to say:** Contextual vectors can carry positional information before pooling, but averaging still compresses 30 vectors into one. Invite predictions about the order-control variant from Day 2; we will check them against actual validation results in Section 5.

**Point / reveal:** Show both sequences, then their strips. Leave the question open.

**Transition:** After the break we will run the encoder ourselves.

### Break · 50–60

**Proposed slide ID:** `day-3-break-1` · **Time:** 50:00–60:00 (10:00)

**What is on slide:** Ten-minute break. "Next: run the encoder on two sequences, then load the rest."

**What I want to say:** Return at minute 60. We will see real vectors, what loading this model involves, and what each step costs.

<a id="section-3"></a>

## 3. Small live extraction and provenance · 60–80

**Story question:** What does the encoder actually output, and what are we trusting when we load it?

**Exit understanding:** Describe pinned loading, custom code execution and the licence. Observe a real two-sequence extraction and its `(2, 512)` output. Separate encoder cost from classifier cost. Name what an embedding cache must store.

**Teaching thread:** "Run two, reuse the rest." A live extraction makes the vectors concrete. A provenance-checked cache keeps the session manageable.

**Scope and delivery:** The instructor demonstrates; students may follow along in the [Days 2–3 notebook](../../notebooks/03_representations.ipynb). First use downloads roughly 224 MB of weights and needs internet. **Caches are not in Git:** if no compatible cache is restored, `run_foundation()` extracts every row. If extraction cannot run, label the route as cached-only (`run_foundation(live_example=False)`), not live.

### S3-01 · Run two, reuse the rest

**Proposed slide ID:** `day-3-s3-roadmap` · **Time:** 60:00–61:30 (1:30)

**What is on slide:** Two lanes. Live: two training sequences → encoder → two 512-number strips. Cache: all rows → stored vectors with sample IDs and hashes → classifier.

**What I want to say:** We first watch the encoder process two sequences, so the vectors are real rather than abstract. Then we use a stored, checked set of vectors for every row, keeping extraction separate from classification.

**Point / reveal:** Reveal the live lane, then the cache lane.

**Transition:** Open the notebook.

### S3-02 · Open the stage 04 cells

**Proposed slide ID:** `day-3-s3-notebook-open` · **Time:** 61:30–64:00 (2:30)

**What is on slide:** The notebook's stage 04 heading and the `run_foundation()` call. Callouts: two CPU threads, batch size 32, and "rerun stage 03 first on a recycled runtime".

**What I want to say:** Stage 04 sits in the same notebook as yesterday's CNN, because it reuses the same datasets and split identities. On a fresh Colab runtime, stage 03 must run first or its artifacts must be restored. Local CPU execution is the rehearsed baseline; hosted Colab execution has not yet been checked.

**Point / reveal:** Point to the call, then the thread/batch settings.

**Transition:** What happens when that cell loads the model?

### S3-03 · What are we actually loading?

**Proposed slide ID:** `day-3-s3-remote-code-security` · **Time:** 64:00–67:00 (3:00)

**What is on slide:** The loading line with `revision=…`, `code_revision=…`, `trust_remote_code=True` and `use_safetensors=True` highlighted. Two notes: "safetensors: weights without pickle" and "remote code: Python from the model repository runs here".

**What I want to say:** This checkpoint needs custom Python code from its repository, so loading it runs that code on our machine. Safetensors avoids pickle-based weight loading but does not stop that code from running. We pin both the model and code revisions, and the custom files were inspected. Inspection is not a security guarantee. The same caution applies to joblib model files from untrusted sources.

**Point / reveal:** Highlight one argument at a time and say what it does and does not protect.

**Transition:** Code safety is one question; permission to use the model is another.

### S3-04 · Check the licence

**Proposed slide ID:** `day-3-s3-licensing` · **Time:** 67:00–68:30 (1:30)

**What is on slide:** Licence card: weights CC-BY-NC-SA-4.0, with icons for attribution, non-commercial and share-alike. Footnote: the custom code files carry their own Apache-2.0 notices.

**What I want to say:** These weights are licensed for non-commercial use with attribution and share-alike terms. That suits this course, but check the licence before any other use. Reading the licence is part of choosing a representation.

**Point / reveal:** Reveal the three icons.

**Transition:** Now run it.

### S3-05 · Two sequences in, two vectors out

**Proposed slide ID:** `day-3-s3-live-forward` · **Time:** 68:30–71:30 (3:00)

**What is on slide:** An empty output panel that is filled live by the notebook: encoder load time and "two-sequence extraction (2, 512)" for each variant. A side note gives the October 26 local reference: load 2.60 s; extraction 0.226 s and 0.187 s, excluding download.

**What I want to say:** The cell takes the first two *training* sequences, tokenises them, runs the frozen encoder without gradients, pools, and prints the shape and time. The October 26 times come from one local CPU run; today's Colab times will differ.

**Point / reveal:** Run the cell and read the printed shape. Do not prefill classroom timings.

**Transition:** What do these 512 numbers look like?

### S3-06 · Look at the vectors

**Proposed slide ID:** `day-3-s3-inspect-vectors` · **Time:** 71:30–73:30 (2:00)

**What is on slide:** The first few components of the two live vectors, printed from the notebook as a short heat strip. Checklist: shape (2, 512), all finite.

**What I want to say:** These are dense, continuous numbers. Unlike a count column, no single dimension means "contains TATA". We judge them by what a classifier can do with them, not by reading individual coordinates.

**Point / reveal:** Show the strip, then tick the shape and finiteness checks.

**Transition:** Two sequences were quick. What about all of them?

### S3-07 · Encoder cost versus classifier cost

**Proposed slide ID:** `day-3-s3-compute-scaling` · **Time:** 73:30–76:00 (2:30)

**What is on slide:** Two bars from the October 26 local CPU run: full extraction plus validation 77.62 s for 1,200 rows and 31.76 s for 480 interaction rows. Classifier fit time is shown from today's printed record. Footnote: "one local run; Colab and classroom network not measured".

**What I want to say:** Extraction is the expensive step and scales with the number of sequences. Fitting a logistic regression on 512 numbers per row is comparatively cheap. That asymmetry is why we compute vectors once, store them and check them, rather than re-extracting for every experiment.

**Point / reveal:** Reveal the extraction bar first, then the classifier fit.

**Transition:** But a stored file is only useful if we can trust what it describes.

### S3-08 · What a cache must remember

**Proposed slide ID:** `day-3-s3-cache-contract` · **Time:** 76:00–78:30 (2:30)

**What is on slide:** A labelled drawer diagram of one cache file: sample IDs, a sequence hash per row, the embedding matrix, model ID, revision, pooling rule and dataset generation identity.

**What I want to say:** The cache stores more than numbers. It stores which sample each row belongs to, a fingerprint of that sample's sequence, the representation contract, and which generated dataset it came from. Without those, a matrix of the right size is unverifiable.

**Point / reveal:** Open the drawers one at a time.

**Transition:** Pause on what we have before testing it.

### S3-09 · Checkpoint: real vectors, recorded provenance

**Proposed slide ID:** `day-3-s3-checkpoint` · **Time:** 78:30–80:00 (1:30)

**What is on slide:** Three ticks: live vectors produced; contract recorded; cost separated. Then the question: "What could go wrong when we join vectors to labels?"

**What I want to say:** We have seen how the vectors are made. The remaining danger is quieter: attaching the right vectors to the wrong samples.

**Point / reveal:** Tick each item, then show the question.

**Transition:** Let's see how that happens.

<a id="section-4"></a>

## 4. The cache audit: identity, alignment, classification · 80–100

**Story question:** What happens if correctly shaped vectors are joined to the wrong rows?

**Exit understanding:** Explain why equal shapes do not prove correct correspondence. List the checks that `load_embedding_cache` performs. Align by sample ID in the practical. Fit the classifier on training rows only. Stop rather than impute when identity fails.

**Teaching thread:** Keep a two-row example visible, with requested order A, B and cache order B, A. It anticipates the Day 4 prediction-alignment audit.

**Scope and delivery:** The guided practical uses [`completed/day3_alignment.py`](../../instructor/completed/day3_alignment.py) and its [scaffold](../../instructor/practicals.md#day-3-align-a-cache-before-trusting-it). Its two-feature cache is explicitly synthetic, not encoder output. The stage 04 classifier cell then uses the real cache when one is available.

### S4-01 · Right shape, wrong sample

**Proposed slide ID:** `day-3-s4-silent-failure` · **Time:** 80:00–82:00 (2:00)

**What is on slide:** The sequence table (A, B, C) and the cache rows (C, A, B) are placed side by side and joined by position. The shape check is green while the identity check is red.

**What I want to say:** A crash tells you something is wrong. A silent misalignment does not. If the cache was saved in a different order, gluing rows together by position runs without error and attaches every vector to the wrong sample.

**Point / reveal:** Show the positional join, then reveal the mismatched IDs.

**Transition:** What does that do to a model?

### S4-02 · Two rows, swapped

**Proposed slide ID:** `day-3-s4-two-row-example` · **Time:** 82:00–84:30 (2:30)

**What is on slide:** Requested order A (label A), B (label B); cache order B, A. The positional join gives A the vector for B and vice versa. Two consequences follow: training learns from mismatched pairs, and evaluation scores the wrong samples.

**What I want to say:** If training rows are mismatched, the classifier learns from pairs that do not exist. If validation rows are mismatched, every reported score refers to the wrong samples. Reordering itself is fine: shuffled rows are harmless when we align by ID. Silent positional pairing is the problem.

**Point / reveal:** Draw the crossed connecting lines, then label both consequences.

**Transition:** How does our code prevent it?

### S4-03 · Five checks before any vector is used

**Proposed slide ID:** `day-3-s4-cache-rules` · **Time:** 84:30–87:30 (3:00)

**What is on slide:** Five illustrated checks: 1) the dataset generation identity matches; 2) sample IDs are unique and cover the dataset exactly; 3) model, revision and pooling match the contract; 4) each ID's sequence hash matches; 5) the result has shape (n, 512) with all finite values.

**What I want to say:** `load_embedding_cache` performs all five checks and raises an error if any fails. Rows are then selected by sample ID in the order the dataset requests. A modified sequence, a missing ID, a duplicate or the wrong model stops the analysis.

**Point / reveal:** Tick the checks one by one.

**Transition:** Here is how the reordering is done.

### S4-04 · Select rows by ID

**Proposed slide ID:** `day-3-s4-code-inspection` · **Time:** 87:30–89:30 (2:00)

**What is on slide:** A short excerpt: `positions = pd.Index(ids).get_indexer(samples["sample_id"])`, followed by the hash comparison and `cache["embeddings"][positions]`.

**What I want to say:** The code looks up each requested sample ID in the cache and takes that row. It never assumes that row 0 means sample 0. The hash comparison then confirms that the sequence behind each ID is the one we expect.

**Point / reveal:** Trace sample B through the lookup to its row.

**Transition:** Now try it yourselves on a small cache.

### S4-05 · Practical: repair the join

**Proposed slide ID:** `day-3-s4-alignment-practical` · **Time:** 89:30–94:30 (5:00)

**What is on slide:** Steps: reindex the synthetic cache by metadata IDs; select rows per split; predict what taking the first rows would do. Optional: duplicate or remove an ID and confirm the script refuses. Label: "synthetic two-feature cache, not model output".

**What I want to say:** Work in pairs or follow the demonstration. Predict the failure before running. Then confirm that a reordered cache gives the same aligned features, and that a missing or duplicated ID stops the script instead of silently dropping a sample.

**Point / reveal:** Show the steps, and keep a visible timer.

**Transition:** With alignment checked, fit the real classifier.

### S4-06 · Fit on training rows only

**Proposed slide ID:** `day-3-s4-training-only` · **Time:** 94:30–97:30 (3:00)

**What is on slide:** Split bars: training 720, validation 240, protected test 240 (padlocked). `fit` is shown on training only; `predict_proba` on validation. The notebook's printed validation ROC-AUC and AP fill an empty panel.

**What I want to say:** Scaling and logistic regression learn from the 720 training rows. Validation vectors are only transformed and scored. Test vectors exist in the cache but are not scored here, and the printout says so. Read today's printed numbers; we interpret them alongside the other workflows in Section 5.

**Point / reveal:** Animate the padlock staying closed while the validation panel fills.

**Transition:** What if the check had failed?

### S4-07 · Missing vector? Stop

**Proposed slide ID:** `day-3-s4-never-invent` · **Time:** 97:30–100:00 (2:30)

**What is on slide:** A stop sign over two tempting fixes, "fill with zeros" and "use the mean vector". Caption: "Identity failure means the pipeline failed."

**What I want to say:** Do not invent vectors to make the code run. A missing or ambiguous identity means something upstream changed. Stop, find the cause, and regenerate the cache with recorded provenance. Discuss briefly: why is stopping better than guessing here?

**Point / reveal:** Cross out each tempting fix in turn.

**Transition:** After the break we compare all four workflows.

### Break · 100–110

**Proposed slide ID:** `day-3-break-2` · **Time:** 100:00–110:00 (10:00)

**What is on slide:** Ten-minute break. "Before we return: will borrowed features win?"

**What I want to say:** Return at minute 110. Make a prediction now; we will check it against validation evidence.

<a id="section-5"></a>

## 5. Validation comparison across representations · 110–140

**Story question:** When do borrowed features help, and when do they not?

**Exit understanding:** Compare four workflows on the same variants and validation identities. Weigh cost, interpretability and reproducibility alongside scores. Explain plausible reasons transfer may not help. Discuss domain shift and unaudited pretraining overlap. Place the genome-scale frontier in context. Reject a universal ranking.

**Teaching thread:** "Predict, then compare." Students commit to a prediction before each chart. Charts show only matched, source-bound validation results.

**Scope and delivery:** Validation only, with no test data. **Primary-variant CNN and embedding values must come from a current matched run of stages 03–04** on the revised PPM generator. The historical fixed-motif values (for example, embedding 0.618) are not reused for that chart. If no current run exists, the chart shows "pending" instead of numbers.

### S5-01 · Make your prediction

**Proposed slide ID:** `day-3-s5-predict` · **Time:** 110:00–111:30 (1:30)

**What is on slide:** Two empty panels, Primary PPM task and Order control. Students place four markers (counts + logistic, counts + forest, CNN, frozen embedding) where they expect validation ROC-AUC to land.

**What I want to say:** Commit to a guess for each task before seeing anything. We will come back to these guesses.

**Point / reveal:** Leave the panels blank, with the predictions visible.

**Transition:** First, are these comparisons fair?

### S5-02 · Same rows, four workflows

**Proposed slide ID:** `day-3-s5-four-workflows` · **Time:** 111:30–113:30 (2:00)

**What is on slide:** Four illustrated workflow icons sharing one split bar: same training rows, same validation IDs, same metric (ROC-AUC primary, AP supporting) and threshold 0.5 for class calls.

**What I want to say:** Within each variant, all four workflows use the same split identities and the same metric policy. Only then do score differences describe the representations rather than different data.

**Point / reveal:** Draw the four workflows onto one shared split bar.

**Transition:** The primary task first.

### S5-03 · Primary task: validation comparison

**Proposed slide ID:** `day-3-s5-primary-results` · **Time:** 113:30–117:00 (3:30)

**What is on slide:** Validation ROC-AUC and AP for the four workflows on the revised PPM task. Day 1's current classical values are logistic 0.608 / 0.607 and forest 0.612 / 0.597 ([record](../../instructor/verification/day1-current.json)). CNN and embedding values come from the current stages 03–04 run, or are marked "pending".

**What I want to say:** This task has a variable, noisy motif and moderate classical scores. Compare the bars against your predictions. With 240 validation rows, small gaps are within ordinary sampling variation, so do not read every decimal as a ranking.

**Point / reveal:** Reveal each workflow's bar beside the student's prediction marker.

**Transition:** Now the task built so that counts cannot succeed.

### S5-04 · Order control: what counts cannot see

**Proposed slide ID:** `day-3-s5-interaction-results` · **Time:** 117:00–120:00 (3:00)

**What is on slide:** Validation ROC-AUC on the paired order variant. Historical October 26 local runs: counts + logistic 0.500, counts + forest 0.500, CNN 1.000, frozen embedding 0.800. Label: "historical runs — confirm with the current matched run before presenting them as today's evidence".

**What I want to say:** Paired sequences have identical 4-mer counts, so any count-based model is at chance by construction. The position-keeping CNN separated them in that run. The frozen embeddings, though averaged, still carried useful order information in that run, short of the CNN. That fits Section 2's question about averaging: pooling compressed the context but did not erase it here.

**Point / reveal:** Reveal the count bars first, then the CNN, then the embeddings.

**Transition:** A score is only one column of the decision.

### S5-05 · Beyond the score

**Proposed slide ID:** `day-3-s5-tradeoff-table` · **Time:** 120:00–122:30 (2:30)

**What is on slide:** A compact four-column comparison: what the input keeps (counts / positions / pooled context), what is fitted on our labels, relative compute, how it can be inspected, and external dependencies (none / none / 224 MB pinned weights and licence).

**What I want to say:** Counts are cheap and their coefficients are readable. The CNN needs training but its filters can be inspected. Embeddings depend on a large external model, a licence and a cache contract, and their dimensions are not directly readable. Which column matters most depends on the question.

**Point / reveal:** Reveal one column at a time. No numbers are invented for compute; refer to recorded timings.

**Transition:** Why didn't the large model simply dominate?

### S5-06 · Why borrowed features may not win

**Proposed slide ID:** `day-3-s5-why-not-crush` · **Time:** 122:30–125:00 (2:30)

**What is on slide:** Four illustrated reasons: a different training objective; mean pooling compresses positions; a linear head on frozen features; synthetic sequences unlike the pretraining data.

**What I want to say:** These are plausible reasons, not proven causes for our results. Ask which one students' predictions relied on. Testing any of them would need a new, separately planned development experiment, never the test set.

**Point / reveal:** Reveal the reasons one at a time and invite votes.

**Transition:** The last reason deserves a closer look.

### S5-07 · Domain shift

**Proposed slide ID:** `day-3-s5-domain-shift` · **Time:** 125:00–128:00 (3:00)

**What is on slide:** An illustrated "pretraining world" of genomes from many species, with plants and viruses marked as excluded according to the model card. A separate island holds simulated sequences with planted motifs.

**What I want to say:** The model card states that plants and viruses were excluded from this checkpoint's pretraining genomes. That matters for a plant-motivated example. Our simulated sequences are also unlike natural genomes. A representation learned from one distribution may transfer poorly to another, in organism, genomic context, sequence length or objective.

**Point / reveal:** Show the pretraining world, then the excluded groups, then the simulated island.

**Transition:** There is a less visible risk too.

### S5-08 · Did it already see the answer?

**Proposed slide ID:** `day-3-s5-pretraining-leakage` · **Time:** 128:00–130:30 (2:30)

**What is on slide:** Two overlapping sets: pretraining sequences and an evaluation set, with a question mark on the overlap. Caption: "No evidence of overlap is not proof of no overlap."

**What I want to say:** For real genomic benchmarks, evaluation loci may have been part of the pretraining genomes. We have not audited overlap for this checkpoint and do not claim none exists. Our simulated sequences make exact overlap unlikely, but a real-data claim would need the audit.

**Point / reveal:** Show the two sets, then the overlap, then the caption.

**Transition:** Where is this field heading?

### S5-09 · From 160 bases to a megabase

**Proposed slide ID:** `day-3-s5-alphagenome-horizon` · **Time:** 130:30–134:00 (3:30)

**What is on slide:** From the reference deck: AlphaGenome takes 1 Mb of input and predicts many functional tracks (RNA-seq, CAGE, DNase/ATAC, histone marks, TF binding, splicing, contact maps), with variant effects scored as alternative minus reference. Citation: *Advancing regulatory variant effect prediction with AlphaGenome*.

**What I want to say:** At the frontier, sequence models read much longer windows and predict many measured genomic tracks, then score variants by comparing predictions for the reference and alternative sequences. These are the authors' reported results on real data. They are not something we reproduce today. The questions we practised still apply: what were the training and evaluation splits, what was held out, and what independent evidence supports a variant claim?

**Point / reveal:** Show the input window, then the output tracks, then the reference-versus-alternative comparison.

**Transition:** So would our result say anything about real promoters?

### S5-10 · Would this work on real promoters?

**Proposed slide ID:** `day-3-s5-real-promoters` · **Time:** 134:00–136:30 (2:30)

**What is on slide:** Two prompts: "What differs between our task and real promoters?" and "What independent measurements would you need?"

**What I want to say:** Our dataset is a controlled simulation. These results teach evaluation and representation; they are not evidence of real promoter prediction. A real claim would need real sequences, biologically measured labels, an appropriate split such as by chromosome or gene family, an overlap check and independent evaluation.

**Point / reveal:** Collect two or three answers per prompt.

**Transition:** No single winner then. Time to stop developing.

### S5-11 · No universal best model

**Proposed slide ID:** `day-3-s5-no-free-lunch` · **Time:** 136:30–138:00 (1:30)

**What is on slide:** Three short pairings: counts for cheap, readable baselines; a CNN when position matters and labels suffice; embeddings when transfer is plausible and its dependencies are acceptable.

**What I want to say:** The choice depends on the signal, the data, the compute and what you need to explain. These results describe these configurations on these simulations, not a ranking of representation families.

**Point / reveal:** Reveal the three pairings together.

**Transition:** Development ends here.

### S5-12 · Ready to freeze

**Proposed slide ID:** `day-3-s5-freeze-readiness` · **Time:** 138:00–140:00 (2:00)

**What is on slide:** Checklist: all four workflows fitted on both variants; validation predictions saved by sample ID; no test labels scored; no further changes.

**What I want to say:** Every decision so far was made with validation data. From this point no more changes are allowed, and we write that down.

**Point / reveal:** Tick each item.

**Transition:** Why write it down at all?

<a id="section-6"></a>

## 6. The evaluation boundary: freeze and reveal · 140–180

**Story question:** How do we open the protected test set once and defend what it shows?

**Exit understanding:** Perform the freeze checklist. Explain what the freeze code records and checks. Make and record a prediction. Run the authorised single reveal. Compare test with validation without tuning. State that the revealed test cannot guide later changes, including on Day 4. Name what the simulation does and does not support.

**Teaching thread:** Follow [ADR 0002](../../docs/adr/0002-validation-for-development-protected-test-comparison.md) and the guide's [freeze/reveal checklist](../../instructor/guide.md#day-3--reuse-a-pretrained-representation). The freeze completes before minute 150; the reveal starts at 150.

**Scope and delivery:** The notebook's stage 05 **freezes only**. The reveal is a separate, instructor-authorised `reveal_test(confirmation="REVEAL THE FROZEN TEST RESULTS")` call. **No test values are prefilled on any slide**; result panels are filled from the live output. If any prerequisite fails, the reveal stays unrun, the slides show the "not revealed" variant, and the time goes to discussing the boundary using development evidence.

### S6-01 · The test set is opened once

**Proposed slide ID:** `day-3-s6-cardinal-rule` · **Time:** 140:00–141:30 (1:30)

**What is on slide:** A sealed envelope labelled "protected test: 240 primary + 96 order-control rows", and the caption "one planned opening".

**What I want to say:** The test estimates how fixed workflows perform on samples that played no part in any decision. If we looked, changed something and looked again, the test would become development data.

**Point / reveal:** Show the envelope, then the caption.

**Transition:** Good intentions are not enough; we keep a record.

### S6-02 · Why a written freeze

**Proposed slide ID:** `day-3-s6-why-protocol` · **Time:** 141:30–143:00 (1:30)

**What is on slide:** Contrast between "I didn't change anything" and a manifest with hashes, settings and a timestamp.

**What I want to say:** A written freeze makes the claim checkable. It records exactly what was compared, so a later change is visible. Our hashes guard against accidents; they are not a security system against deliberate tampering.

**Point / reveal:** Show the two sides together.

**Transition:** Let's go through the checklist aloud.

### S6-03 · Freeze checklist, aloud

**Proposed slide ID:** `day-3-s6-checklist-aloud` · **Time:** 143:00–146:30 (3:30)

**What is on slide:** The guide's five items, condensed. 1) Dataset variants, split identities and code/source fingerprints; no prior test reads. 2) Models, preprocessing, CNN checkpoint policy, embedding contract and cache, ROC-AUC primary, threshold 0.5, and the fixed list of four methods. 3) Validation predictions saved by sample ID. 4) Instructor name, time and explicit authorisation. 5) If anything is missing, do not reveal.

**What I want to say:** Read each item aloud and confirm it with the class. The list of methods is fixed now; we will not add a test-chosen winner later.

**Point / reveal:** Tick the items live. Record the authorisation on the slide or in Notes.

**Transition:** What does the code check for us?

### S6-04 · What the freeze records

**Proposed slide ID:** `day-3-s6-code-freeze` · **Time:** 146:30–148:00 (1:30)

**What is on slide:** `freeze_workflows()` steps. It checks dataset generation identities, development IDs and caches, and "no previous test evaluation". It hashes 32 development artifacts. It fingerprints inference source and package versions. It writes `frozen_manifest.json` with the method list, ROC-AUC and 0.5.

**What I want to say:** The freeze refuses to run if development records disagree with the datasets or report a previous test read. It writes the manifest once and will not overwrite it.

**Point / reveal:** Highlight the steps in order.

**Transition:** Before we run it, everyone commits to a prediction.

### S6-05 · Predict, then freeze

**Proposed slide ID:** `day-3-s6-freeze-executed` · **Time:** 148:00–150:00 (2:00)

**What is on slide:** A prediction card for each student (which workflow on which variant, and why), then the live freeze output: "Frozen. Test results have NOT been calculated."

**What I want to say:** Write your prediction first. Then we freeze. From this moment the compared workflows are fixed.

**Point / reveal:** Collect predictions, then run the freeze cell and read the message aloud.

**Transition:** At minute 150, the authorised reveal.

### S6-06 · The authorised reveal

**Proposed slide ID:** `day-3-s6-reveal-call` · **Time:** 150:00–153:00 (3:00)

**What is on slide:** The call `reveal_test(confirmation="REVEAL THE FROZEN TEST RESULTS")`. Its guards are listed: refuses without the exact phrase; refuses if a result already exists; refuses if any frozen artifact, inference source or package version changed.

**What I want to say:** The function re-checks the freeze before reading test labels. Then it scores all four frozen workflows on both variants, saves the predictions and results, and refuses to run a second time.

**Point / reveal:** Show the guards, then run the call. If it refuses, switch to the "not revealed" variant and do not work around the guard.

**Transition:** Read the result together.

### S6-07 · Read the test table

**Proposed slide ID:** `day-3-s6-test-results-table` · **Time:** 153:00–158:00 (5:00)

**What is on slide:** An empty eight-row table (2 variants × 4 methods; ROC-AUC, AP), filled from the printed output. Nothing is prefilled.

**What I want to say:** Read each row against your written prediction. Which surprised you? Name the observation first; explanations come next.

**Point / reveal:** Fill the rows from the output, one variant at a time.

**Transition:** How do these compare with validation?

### S6-08 · Validation beside test

**Proposed slide ID:** `day-3-s6-validation-vs-test` · **Time:** 158:00–162:00 (4:00)

**What is on slide:** Paired bars for each workflow (validation from the saved development records, test from the reveal) on the same scale, with the row counts labelled: 240/240 primary and 96/96 order control.

**What I want to say:** Test results can be lower or higher than validation. Validation guided choices such as the CNN checkpoint, so it can be optimistic, and with 240 or 96 rows both estimates carry real sampling variation. A large, unexplained drop would prompt an audit of the pipeline, not a retuning.

**Point / reveal:** Reveal one workflow's pair at a time.

**Transition:** What surprised you most?

### S6-09 · Surprises and explanations

**Proposed slide ID:** `day-3-s6-surprises` · **Time:** 162:00–165:00 (3:00)

**What is on slide:** Two columns, "What we observed" and "Possible explanations". Explanations stay labelled as hypotheses.

**What I want to say:** Collect two or three observations. For each, offer explanations, and say what new, separately planned experiment could test them on fresh data.

**Point / reveal:** Write the students' contributions into the columns.

**Transition:** And if your favourite workflow lost?

### S6-10 · Disappointment is a result

**Proposed slide ID:** `day-3-s6-what-if-lost` · **Time:** 165:00–168:00 (3:00)

**What is on slide:** A fork. Wrong: change a setting, re-score the same test. Right: report the frozen result, its uncertainty and its limits.

**What I want to say:** Changing a setting after seeing test scores, then reporting the new test score, turns the test into development feedback. The honest report is what the frozen workflows achieved. A follow-up idea needs new independent data.

**Point / reveal:** Show the wrong path crossed out, then the right path.

**Transition:** This holds beyond today.

### S6-11 · A one-way gate

**Proposed slide ID:** `day-3-s6-oneway-gate` · **Time:** 168:00–171:00 (3:00)

**What is on slide:** A turnstile: development → reveal → historical evidence, with no arrow back. The Day 4 icon sits behind the same barrier.

**What I want to say:** These test results are now historical. They cannot become training data, validation data, or a target for tomorrow's agent-written analysis. Day 4 audits whether an agent respects exactly this boundary.

**Point / reveal:** Animate the turnstile, then the barrier in front of the Day 4 icon.

**Transition:** So what can we actually conclude?

### S6-12 · What we can claim

**Proposed slide ID:** `day-3-s6-claims` · **Time:** 171:00–175:00 (4:00)

**What is on slide:** Two columns. Supported: how these frozen configurations performed on these held-out simulated samples. Not supported: real promoter prediction, biological mechanism, or a general ranking of representation families.

**What I want to say:** Following [ADR 0001](../../docs/adr/0001-controlled-sequence-classification.md), this is controlled simulated classification. The claim is narrow and defensible. Ask each student for one supported sentence.

**Point / reveal:** Fill both columns, with students' sentences going into "supported".

**Transition:** Let's recap the day.

### S6-13 · Day 3 recap and tomorrow

**Proposed slide ID:** `day-3-s6-synthesis` · **Time:** 175:00–178:00 (3:00)

**What is on slide:** Five icons: embedding/transfer; attention/context; contract and live extraction; alignment by ID; freeze and single reveal. A preview line reads "Tomorrow: when an agent writes the code, who owns the claim?"

**What I want to say:** Borrowed representations change where features come from, not the evidence we need. Tomorrow we hand the coding to an agent and check whether these same choices survive.

**Point / reveal:** Reveal the icons in story order, then the preview.

**Transition:** Questions.

### S6-14 · Questions and buffer

**Proposed slide ID:** `day-3-s6-buffer` · **Time:** 178:00–180:00 (2:00)

**What is on slide:** Open questions, with links to the notebook guide, stage 04 source and the instructor guide.

**What I want to say:** Use the remaining time for questions about pretraining, alignment or the freeze.

**Point / reveal:** None.

**Transition:** End of Day 3.

<a id="notebook-plan"></a>

## Notebook plan

| Checkpoint | Student/instructor action | Current state |
| --- | --- | --- |
| Section 3 | Run `run_foundation()`: live two-training-sequence extraction, shape (2, 512), printed timings. | Stage 04 code exists in the [Days 2–3 notebook](../../notebooks/03_representations.ipynb); verified locally on October 26. A lesson-specific stop after the live example is proposed. |
| Section 3 contingency | `run_foundation(live_example=False)` with a restored, compatible cache. | Exists; must be labelled cached-only, not live. |
| Section 4 | Synthetic alignment practical, then cache-backed classifier with printed validation metrics. | [`day3_alignment.py`](../../instructor/completed/day3_alignment.py) and its scaffold exist; the classifier is part of `run_foundation()`. |
| Section 5 | Read matched validation results for four workflows on both variants. | Requires a current stages 03–04 run on the revised generator; a readback cell is proposed. |
| Section 6 | Stage 05 `freeze_workflows()`; separate instructor `reveal_test(...)`. | Freeze exists in the notebook; the reveal is deliberately not a notebook cell. |

**Cache availability:** caches, models and outputs are not in Git or the notebooks. A fresh Colab runtime has no cache, so `run_foundation()` extracts every row (77.62 s + 31.76 s locally on October 26; Colab not measured). Before class, either rehearse that cost or restore a provenance-checked `course_output/` explicitly and label it as previous execution.

<a id="evidence-and-scope"></a>

## Evidence and scope

### Dataset and evaluation continuity

- **Primary task:** the revised 15-position PPM generator with planting probability 0.95/0.05; 1,200 sequences of 160 bases; 720/240/240 split. **Order control:** 240 paired groups (480 sequences), 288/96/96 rows, with partners kept together.
- **Representation:** the frozen NT-v2 50M checkpoint at revision `81b29e5786726d891dbf929404ef20adca5b36f1`. Weights are CC-BY-NC-SA-4.0. Pooling is the last-layer mean excluding special tokens and padding, giving 512 components. Tokenisation yields 31 tokens per sequence. See [embedding verification](../../instructor/verification/embeddings.md).
- **Evaluation:** ROC-AUC primary, AP supporting, threshold 0.5. Fitting uses training rows only; validation is for development; one planned test reveal after freeze ([ADR 0002](../../docs/adr/0002-validation-for-development-protected-test-comparison.md)).

### Values that may and may not appear on slides

- October 26 local measurements may appear when labelled as such: encoder load 2.60 s; live extraction 0.226/0.187 s; full extraction 77.62/31.76 s; about 224 MB of weights.
- Order-control validation ROC-AUC from historical October 26 runs: counts 0.500, CNN 1.000, embedding 0.800. Show these as historical until a current matched run confirms them.
- Primary-task embedding 0.618 and CNN/forest values in [representations.md](../../instructor/verification/representations.md) belong to the old fixed-motif generator. **Do not use them** for the revised primary chart.
- Test values: none exist yet. Never prefill them.
- Reference-deck figures (AlphaGenome, DNABERT, Zeiler & Fergus) report the authors' results, with citations; they are not course evidence.

### Before implementation is called verified

Run stages 03–04 with the current generator and record source and configuration identities, then build the Section 5 charts from that record. Check the layer count and other architecture details for S2-08 against the pinned `config.json` before stating them on a slide. Rehearse extraction cost and cache restoration in the actual Colab runtime. Verify the slide interactions offline, plus navigation, notes, export and print. Hosted Colab execution, timed pacing and the actual reveal need their own checks.
