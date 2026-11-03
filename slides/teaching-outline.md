# Four-day course: editable slide and speaking outline

This is a review draft of the current 60-slide presentation, including the break slides. It makes the current teaching assumptions explicit so you can correct them before we rebuild the HTML.

For each slide, **On the slide** summarizes the current visual content. **What I want to say (draft)** proposes the spoken explanation, based on the existing deck and instructor notes; it is not a claim that your intended teaching content has already been agreed.

Edit either paragraph directly. Change titles, move or remove sections, and add slides wherever needed. Your amended version of this document will be the content source for the next HTML revision. The current slide numbers and timing allocations are included only to help you navigate and compare.

## Days

- [Day 1: Classical models and evaluation](#day-1)
- [Day 2: Neural networks and learned representations](#day-2)
- [Day 3: Pretraining and frozen embeddings](#day-3)
- [Day 4: Coding agents and scientific audit](#day-4)

<a id="day-1"></a>

## Day 1 — Classical models and evaluation

Current duration: 180 minutes, including two ten-minute breaks.

### Slide 01 — Can a machine recognize a promoter?

Day 1, slide 1 · Current timing: 0–10 · startup

**On the slide:** Opening question about promoter recognition; DNA → prediction → evidence; four stages of the course: count, learn, reuse, audit. A link points to the first code file for in-class startup.

**What I want to say (draft):** Introduce the biological motivation and the route through the four days. We will use a controlled simulated DNA classification problem so we can inspect what models learn. Explain that successful prediction in this simulation does not establish real promoter recognition. Help students start Colab during class.

--- I think that the first slide should be much more general. What is this course about, what are we expected to learn. I would not open with a promoter recognition problem. Also I would like to have 1 slide that outlines who the instructor is (me) and why I am teaching this course.

### Slide 02 — What would convince you?

Day 1, slide 2 · Current timing: 10–16 · diagnostic

**On the slide:** A hypothetical classifier reports 95% accuracy. Two questions ask what the samples and labels are, and how the model was tested.

**What I want to say (draft):** Use this as an ungraded opening discussion to learn what students already know. Ask what 95% accuracy would mean and what information is missing. Introduce samples, labels, prediction, and generalization through their answers rather than assuming prior ML knowledge.

--- This sounds a bit too deep into the heat for a random class of students. OK, maybe as an ungraded opening discussion it makes sense. But is just 95% accuracy a good enough question? what if we showed accuracy, precision, recall, F1 etc and asked how to interpret these?

### Slide 03 — What are we asking the machine to do?

Day 1, slide 3 · Current timing: 16–24 · ML map

**On the slide:** Three kinds of question: classify a sample, predict a quantity, or discover similarity. A fourth example introduces learning by predicting a missing part of the input.

**What I want to say (draft):** Distinguish supervised classification from regression, unsupervised structure discovery, and self-supervised learning. Give a simple biological example of each. Locate our course task within supervised binary classification, and explain that Day 3 will borrow features learned using a different objective.

--- so this has to do with supervised/unsupervised etc. I would do one slide for each. Maybe one initial slide that would show the 'tree' of supervised vs unsupervised and then the differnece branches being classification, regression, clustering etc.

### Slide 04 — Plant a clue. Add uncertainty.

Day 1, slide 4 · Current timing: 24–34 · simulation

**On the slide:** The simple-signal dataset: 1,200 simulated DNA sequences of length 160, with balanced classes. The same motif is planted with probability 0.9 in class 1 and 0.1 in class 0.

**What I want to say (draft):** Explain how the simulation generates the sequences and labels. The motif is an informative clue, not a perfect definition of the label. Ask whether even a perfect detector would classify every sequence correctly. Distinguish deliberate planting from an incidental motif occurrence in random background DNA.

--- OK this makes sense to me.

### Slide 05 — Let’s count short DNA words.

Day 1, slide 5 · Current timing: 34–42 · representation

**On the slide:** An example splits ACGTAC into overlapping 4-mers. A 160-base sequence becomes a vector over 256 possible DNA words. A short caption contrasts composition with location.

**What I want to say (draft):** Show how a sequence becomes a numeric input that a classical classifier can use. Explain overlapping windows and why there are 4⁴ possible 4-mers. Counts can expose short patterns, including pieces of a longer motif, but they do not explicitly record where each occurrence was found.

--- OK this makes sense, we are talking k-mers here

### Slide 06 — What did we lose?

Day 1, slide 6 · Current timing: 42–50 · practical

**On the slide:** A practical prompt links to code 01: inspect sequences and labels, then count 4-mers. The discussion asks whether the count vector reveals motif location.

**What I want to say (draft):** Walk through the data before modeling: one row, its sequence, its label, and its identity. Have students inspect the input and describe the representation in their own words. Ask what information is retained and what is discarded. Keep IDs and simulation-truth fields separate from predictive features.

--- not sure what this is about

### Slide 07 — Break · 10 minutes

Day 1, slide 7 · Current timing: 50–60 · break

**On the slide:** A ten-minute break, with the question “What would a fair test look like?” introducing the next block.

**What I want to say (draft):** Take the full break and return at minute 60. The next block will explain how we separate fitting, development, and final evaluation.

--- OK I guess. make it less busy.

### Slide 08 — Keep one answer sealed.

Day 1, slide 8 · Current timing: 60–70 · evaluation design

**On the slide:** Three data partitions: 720 training sequences, 240 validation sequences, and 240 protected test sequences. Each partition has one stated job.

**What I want to say (draft):** Explain why evaluating on the examples used for fitting can mislead us. Training fits parameters and learned preprocessing; validation supports development and comparison; the test is reserved for the planned Day 3 comparison. Keep split identities fixed across representations, and keep related samples together where applicable.

--- train, validation ,test OK good

### Slide 09 — Turn counts into a prediction.

Day 1, slide 9 · Current timing: 70–80 · logistic regression

**On the slide:** A weighted sum of counts produces a score, and a sigmoid turns the score into a class-1 probability. A question asks which DNA words push toward class 1.

**What I want to say (draft):** Introduce logistic regression as a useful first classifier. Explain features, weights, and the intercept with a small example. Describe how changing a count can change the model score. A coefficient describes this fitted predictor; correlated motif fragments make biological interpretation more complicated.

--- I would like to have something more visually appealing here.

### Slide 10 — A ranking is not a decision.

Day 1, slide 10 · Current timing: 80–90 · metrics

**On the slide:** A side-by-side comparison separates ranking, measured by ROC-AUC, from decisions, described using precision and recall. The default decision threshold is 0.5.

**What I want to say (draft):** Explain what predicted probabilities, thresholds, and a confusion matrix tell us. Walk through true positives, false positives, false negatives, and true negatives with a small example. Introduce ROC and precision–recall views, including average precision. Explain why class balance matters and why changing a threshold does not change ROC-AUC. ROC-AUC is the main comparison metric for this course.

--- do I need to explain what is precision, recall etc?

### Slide 11 — Your turn: fit, then predict.

Day 1, slide 11 · Current timing: 90–100 · practical

**On the slide:** Two lines of code fit the pipeline on training sequences and predict probabilities on validation sequences. A link opens the Day 1 exercise.

**What I want to say (draft):** Connect the evaluation protocol to executable code. Students complete the small prediction step and explain which rows were used for fitting. Keep predictions attached to sample IDs. Explain why learned vocabulary or scaling should be fitted using training data only, even when the transform does not use labels.

--- are we working on the slide here?

### Slide 12 — Break · 10 minutes

Day 1, slide 12 · Current timing: 100–110 · break

**On the slide:** A ten-minute break. The next question is whether a random forest will improve on the linear baseline.

**What I want to say (draft):** Take the break and return at minute 110. We will keep the same representation and evaluation protocol while changing the classifier.

--- OK

### Slide 13 — What if one rule is not enough?

Day 1, slide 13 · Current timing: 110–122 · trees and forests

**On the slide:** A diagram moves from one threshold question to a decision tree and then to a forest averaging many trees.

**What I want to say (draft):** Explain how a tree partitions feature space by asking successive questions. A forest combines differently trained trees, which can reduce the instability of a single tree. Use the provided implementation rather than building one from scratch. More flexibility can capture useful relationships, but it can also fit noise.

--- Make this an interactive thing maybe?

### Slide 14 — The forest ranks better. What follows?

Day 1, slide 14 · Current timing: 122–140 · compare and interpret

**On the slide:** A validation ROC-AUC chart for the simple-signal variant: approximately 0.802 for 4-mer logistic regression and 0.907 for the random forest. A prompt asks about important 4-mers.

**What I want to say (draft):** Read the chart with the students: the forest ranks examples better in this recorded run. Inspect coefficients or feature importance and compare them with the planted motif. Ask students to give one supported conclusion and one overclaim. These validation results do not establish a universal ranking or real promoter recognition.

--- OK I guess?

### Slide 15 — Try to break your explanation.

Day 1, slide 15 · Current timing: 140–150 · consolidate

**On the slide:** The proposed explanation is that the classifier learned the planted signal. Students are asked what would make them doubt it; prompts mention feature importance, IDs, related samples, and shortcuts.

**What I want to say (draft):** Show how an explanation can be questioned using evidence. Important motif-related features are suggestive, but we should also look for alternative routes to a high score. Discuss how label-associated IDs or related samples across splits could produce misleading success. Use this to introduce the separate leakage investigation.

--- I am not sure what to say here honestly, need more explanation

### Slide 16 — What if it recognized the family?

Day 1, slide 16 · Current timing: 150–180 · leakage, discussion, buffer

**On the slide:** A separate experiment contrasts random row splitting with holding out entire families of related sequences. Family labels are randomly assigned. A link opens code 02.

**What I want to say (draft):** Ask students to predict what happens when relatives appear on both sides of a split. Run or inspect the exercise, check group overlap, and compare the corrected group split. Explain that family recognition can look predictive without transferring to unseen families. Keep this dataset separate from the main comparison, then recap Day 1.

--- that jumps to a new question.

I think 10 mins per slide is a bit too much?

==== to HERE === edit above

<a id="day-2"></a>

## Day 2 — Neural networks and learned representations

Current duration: 180 minutes, including two ten-minute breaks.

### Slide 17 — What if the features hide the answer?

Day 2, slide 1 · Current timing: 0–10 · recap

**On the slide:** Day 2 opens with “Same words. Different positions.” The question is whether a bag of words can distinguish them.

**What I want to say (draft):** Recall what yesterday’s features retained and discarded. Introduce representation learning as a way to change what the classifier can use. We will compare methods on the same dataset variants and split identities, so any apparent improvement needs to be interpreted in that shared experimental setting.

### Slide 18 — Start with a familiar calculation.

Day 2, slide 2 · Current timing: 10–20 · neuron

**On the slide:** A worked neuron computes z = 0.5 × 2 − 1 × 1 + 0.2 and applies ReLU. Students then change the second input.

**What I want to say (draft):** Connect a neuron to the weighted sum already seen in logistic regression. Explain the role of an activation and why stacking only linear transformations would still give a linear transformation. Work through both input examples. Relate hidden activations to the final logit and its sigmoid probability without requiring a derivative calculation.

### Slide 19 — A confident mistake should hurt.

Day 2, slide 3 · Current timing: 20–30 · loss

**On the slide:** For an actual positive, p = 0.8 gives loss about 0.223, while p = 0.2 gives loss about 1.609. The displayed formula is loss = −log(p) for y = 1.

**What I want to say (draft):** Introduce loss as the quantity training tries to reduce. Use the two predictions to explain why confident mistakes are penalized strongly. Briefly explain binary cross-entropy for both labels. Distinguish training loss from validation ROC-AUC, and explain that the implemented logits-based loss already handles the sigmoid internally.

### Slide 20 — How does the model improve?

Day 2, slide 4 · Current timing: 30–40 · optimization

**On the slide:** A loop shows prediction, backpropagation, and parameter updates. The discussion asks what to do when training improves but validation worsens.

**What I want to say (draft):** Explain forward computation, gradients, optimizer steps, minibatches, and epochs at a conceptual level. Backpropagation efficiently computes how the loss changes with parameters; it does not explain biology. Use training and validation behavior to introduce overfitting and the reason for selecting a saved epoch using validation evidence.

### Slide 21 — Keep the bases in their places.

Day 2, slide 5 · Current timing: 40–50 · one-hot DNA

**On the slide:** A one-hot matrix for ACGT, with base channels as rows and positions as columns. The full sequence shape is 4 × 160.

**What I want to say (draft):** Show how each base becomes a column with one active channel. Explain why assigning A, C, G, and T the numbers 0, 1, 2, and 3 would introduce an arbitrary numerical ordering. Ask students to encode a short sequence and identify the axes. One-hot encoding preserves order but is itself a fixed representation.

### Slide 22 — Break · 10 minutes

Day 2, slide 6 · Current timing: 50–60 · break

**On the slide:** A ten-minute break introduces a local detector that will scan the sequence.

**What I want to say (draft):** Return at minute 60. We will use the positional DNA representation as input to a small convolutional network.

### Slide 23 — Slide one detector across the DNA.

Day 2, slide 7 · Current timing: 60–73 · convolution

**On the slide:** A detector window moves along a short DNA sequence. The question is why the same weights are reused at different positions.

**What I want to say (draft):** Explain convolution as applying a learned local pattern detector repeatedly along the sequence. Discuss filters, activation maps, and weight sharing. The supplied model has two convolutional layers; exact sizes are available in the technical reference. A filter response may be useful for prediction without being a verified biological motif.

### Slide 24 — Notice a pattern. Remember where.

Day 2, slide 8 · Current timing: 73–84 · architecture

**On the slide:** The CNN’s convolution features feed two branches: flattening, which retains location, and global max pooling, which summarizes the strongest activation anywhere. A classifier combines them.

**What I want to say (draft):** Explain how the handling of position changes what a CNN can represent. This course model deliberately keeps a flattened positional map alongside global maxima. A global-max-only model would discard the cue used in our later construction. The architecture therefore matters more than the generic label “CNN”.

### Slide 25 — Will learning features help here?

Day 2, slide 9 · Current timing: 84–100 · practical

**On the slide:** A practical links to code 03 and asks students to inspect one-hot inputs, train the supplied CNN, and read the validation result. Students predict the outcome first.

**What I want to say (draft):** Run the simple-signal CNN practical with the provided implementation and a small selected-code task. Ask whether a larger model must beat a simple baseline on 720 training sequences. Inspect validation predictions and the saved epoch. If live computation is slow, use clearly identified previous outputs and discuss what was actually executed.

### Slide 26 — Break · 10 minutes

Day 2, slide 10 · Current timing: 100–110 · break

**On the slide:** A ten-minute break introduces a problem the bag of 4-mers cannot solve.

**What I want to say (draft):** Return at minute 110. The next construction will isolate missing information in the representation rather than simply add a more complicated model.

### Slide 27 — Two sequences. Same ingredients.

Day 2, slide 11 · Current timing: 110–123 · interaction construction

**On the slide:** Two paired sequences swap TATAAATG and CGGACGTC between motif starts 38 and 86. They share background and matching flanks, and each pair stays within one split.

**What I want to say (draft):** Explain the interaction-signal variant as a deliberately engineered fixed-position motif-order control. Matching flanks make the swap preserve every 4-mer count. The labels differ according to the construction. Distinguish motif starts from block starts at 32 and 80, and make clear that this is a teaching control rather than realistic promoter grammar.

### Slide 28 — The bag sees the same input twice.

Day 2, slide 12 · Current timing: 123–132 · representation proof

**On the slide:** An equality states that the two sequences have identical 4-mer bags. The consequence is “Same vector → same score,” despite opposite labels.

**What I want to say (draft):** Reason through the representation limit before seeing model results. A deterministic classifier cannot distinguish two identical input vectors, regardless of the number of trees or hyperparameter searches. Balanced pairs with opposite labels give chance ranking for this representation. The position-aware CNN has access to information the bag removed.

### Slide 29 — The winner depends on the question.

Day 2, slide 13 · Current timing: 132–140 · observed validation

**On the slide:** A validation ROC-AUC chart compares logistic regression, random forest, and the position-aware CNN on both variants. Simple-signal scores are about 0.802, 0.907, and 0.564; interaction scores are 0.5, 0.5, and 1.0.

**What I want to say (draft):** Interpret both columns together. The CNN solves the constructed positional task yet performs poorly on this noisy simple-signal run. The result illustrates the interaction between task, representation, architecture, and training. It does not show that CNNs always win or establish a biological mechanism.

### Slide 30 — Swap the motifs. Predict the response.

Day 2, slide 14 · Current timing: 140–150 · controlled changes

**On the slide:** The motif-swap diagram appears again with a Day 2 exercise: check equal 4-mer vectors and compare model predictions.

**What I want to say (draft):** Have students predict the effect of swapping the controlled motif blocks before inspecting probabilities. Equal bag inputs force the classical predictor to give equal scores. The CNN’s observed response reveals sensitivity of this fitted predictor to the construction. Treat new positions or other perturbations as additional experiments, not already established results.

### Slide 31 — Which representation would you choose?

Day 2, slide 15 · Current timing: 150–180 · synthesis and buffer

**On the slide:** A comparison contrasts cheap count features that lose position with learned local features that can preserve it. The final question asks whether features can be borrowed from elsewhere.

**What I want to say (draft):** Summarize the tradeoffs among predictive behavior, computational cost, and interpretation. Ask when students would prefer the simpler model and what evidence their choice would require. Finish with the idea that features might be learned before our particular classification task, introducing Day 3.

<a id="day-3"></a>

## Day 3 — Pretraining and frozen embeddings

Current duration: 180 minutes, including two ten-minute breaks.

### Slide 32 — What if the features were already learned?

Day 3, slide 1 · Current timing: 0–10 · recap

**On the slide:** Day 3 opens with a pipeline: our DNA sequences → frozen pretrained encoder → small classifier using our labels.

**What I want to say (draft):** Recall yesterday’s distinction between a fixed input encoding and learned features. Introduce the possibility of reusing a representation trained on other sequences. Ask what information might transfer and what might fail to transfer. The train/validation/test roles remain the same.

### Slide 33 — Hide a piece. Ask the model to recover it.

Day 3, slide 2 · Current timing: 10–20 · pretraining

**On the slide:** A masked-token example contrasts the pretraining question, “Which token is missing?”, with the course question, “Which simulated class is this?”

**What I want to say (draft):** Explain how self-supervision gets a target from the input without manually assigning the downstream labels. Predicting missing sequence pieces can produce contextual features, but the pretraining objective differs from our classification objective. The masking example is conceptual, not a recorded model prediction or exact tokenizer output.

### Slide 34 — A token can borrow context.

Day 3, slide 3 · Current timing: 20–30 · attention

**On the slide:** Attention is summarized as finding relevance, weighting evidence, and combining values. A numerical exercise asks for 0.75 × 2 + 0.25 × 6.

**What I want to say (draft):** Explain queries, keys, values, and a weighted combination at an intuitive level. Work through the example, whose answer is 3, then explain that real models combine vectors using multiple heads and layers. Attention supports context-dependent representations; an attention weight alone is not evidence of biological causality.

### Slide 35 — Borrow the encoder. Train the classifier.

Day 3, slide 4 · Current timing: 30–40 · frozen versus fine-tuned

**On the slide:** A fixed pretrained encoder is contrasted with the trainable downstream classifier. Students are asked which part sees the course labels.

**What I want to say (draft):** Explain our frozen-embedding practical: extract vectors without updating the encoder, then fit scaling and logistic regression using training labels. Contrast this with fine-tuning, where task loss updates some or all encoder weights. Separately distinguish freezing encoder weights from freezing all analysis choices before final evaluation.

### Slide 36 — What comes out of the encoder?

Day 3, slide 5 · Current timing: 40–50 · representation contract

**On the slide:** The embedding pipeline is 160 DNA bases → contextual token vectors → 512 numbers. It names the pinned NT-v2 50M model and last-layer content-token mean pooling.

**What I want to say (draft):** Explain tokenization, contextual hidden vectors, and pooling into one vector per sequence. Describe the model revision and pooling rule as part of the representation definition. Ask what averaging might discard. For these inputs, the tokenizer produces 31 tokens including CLS; mean pooling excludes special tokens and padding.

### Slide 37 — Break · 10 minutes

Day 3, slide 6 · Current timing: 50–60 · break

**On the slide:** A ten-minute break leads into live extraction for two sequences, followed by the full-data cache.

**What I want to say (draft):** Return at minute 60. The practical will show how vectors are produced before using stored vectors to keep the session manageable.

### Slide 38 — Run two. Reuse the rest.

Day 3, slide 7 · Current timing: 60–70 · execution and provenance

**On the slide:** Three steps: a small live extraction, a verified full-data embedding cache, and a classifier fitted on training rows. A link opens code 04.

**What I want to say (draft):** Run a small extraction so students can inspect actual encoder outputs. Then use the aligned full-data cache and fit the downstream pipeline. Separate extraction cost from classifier cost. Identify previous outputs honestly; if extraction cannot run, the cached-only contingency is useful but does not count as live extraction.

### Slide 39 — What are we actually loading?

Day 3, slide 8 · Current timing: 70–80 · loading safely

**On the slide:** Two reminders: pin model/code revisions and pooling for reproducibility; inspect custom code and the model license before reuse.

**What I want to say (draft):** Explain the actual loading decision for this checkpoint, which executes pinned custom Python code. Safetensors changes how weights are stored but does not prevent that code execution. Mention the CC-BY-NC-SA-4.0 license and the need to check suitability for other uses. Keep this explanation tied to the practical’s concrete dependency choices.

### Slide 40 — Right vector. Wrong sequence.

Day 3, slide 9 · Current timing: 80–90 · cache audit

**On the slide:** Requested sample order A, B is contrasted with cache order B, A. The question asks what to check before combining sequences, embeddings, and labels.

**What I want to say (draft):** Explain that a matrix with the expected dimensions can still describe the wrong samples. Require unique IDs and exact coverage, check the sequence hash for each ID, and verify model/pooling provenance and finite vector shape. Shuffled rows are acceptable if alignment is done correctly; silent positional pairing is the problem.

### Slide 41 — Repair the join.

Day 3, slide 10 · Current timing: 90–100 · practical

**On the slide:** A practical asks students to align embeddings by ID and fail clearly on missing or duplicate samples. A discussion contrasts stopping with guessing a missing vector.

**What I want to say (draft):** Work through the Day 3 alignment exercise. Explain why reordering the cache should not change the correctly aligned features. Missing or ambiguous identity should stop the analysis rather than trigger invented data. Fit learned scaling only on training rows after alignment.

### Slide 42 — Break · 10 minutes

Day 3, slide 11 · Current timing: 100–110 · break

**On the slide:** A ten-minute break before comparing all representations. The question is whether borrowed features will win.

**What I want to say (draft):** Return at minute 110. Ask students to make a prediction before showing the comparison, then use the results to discuss when transfer helps.

### Slide 43 — Borrowed features do not win by default.

Day 3, slide 12 · Current timing: 110–125 · validation comparison

**On the slide:** The validation chart adds frozen NT-v2 embeddings plus logistic regression to the earlier three methods. Embedding ROC-AUC is about 0.618 on simple-signal and 0.800 on interaction-signal.

**What I want to say (draft):** Compare methods on the same variant and split identities. Pretrained features distinguish the engineered order task imperfectly but do not dominate either task. Discuss extraction and training costs, reproducibility, interpretation, and the target question alongside scores. The current result is evidence about these configurations, not a general ranking of representation families.

### Slide 44 — Would this work on real promoters?

Day 3, slide 13 · Current timing: 125–138 · transfer and limits

**On the slide:** A question asks whether the simulation results would transfer to real promoters. Two prompts cover population/task mismatch and independent biological measurements.

**What I want to say (draft):** Discuss domain shift across organisms, genomic contexts, sequence lengths, and learning objectives. The chosen checkpoint’s documented pretraining genomes exclude plants and viruses, and pretraining overlap has not been audited here. Explain what additional biological data and independent evaluation would be needed before making a real promoter claim.

### Slide 45 — Make your prediction. Then freeze.

Day 3, slide 14 · Current timing: 138–150 · freeze gate

**On the slide:** A three-step gate checks artifacts and identities, freezes the full workflow, and asks students to predict the final outcome. Code 05 freezes without revealing scores.

**What I want to say (draft):** Stop model development and record preprocessing, model configurations, selection decisions, metrics, and thresholds. Verify provenance and split identities before freezing. Ask students what they expect on the held-out test and why. Explain that the first execution records the frozen analysis without calculating test scores.

### Slide 46 — Now open the sealed answer.

Day 3, slide 15 · Current timing: 150–180 · explicit reveal and synthesis

**On the slide:** An explicit reveal_test call opens the planned comparison after the instructor gate. Students are asked what surprised them and what they can conclude. No test values are prefilled.

**What I want to say (draft):** If the frozen checks pass, execute the planned reveal and interpret the actual output together. Discuss differences from validation without changing settings to improve the revealed test result. Explain that this same test cannot become fresh independent evidence for later tuning, including on Day 4. If prerequisites fail, leave the reveal unrun.

<a id="day-4"></a>

## Day 4 — Coding agents and scientific audit

Current duration: 180 minutes, including two ten-minute breaks.

### Slide 47 — Who owns the claim when an agent writes the code?

Day 4, slide 1 · Current timing: 0–10 · recap

**On the slide:** Day 4 asks who owns the scientific claim when an agent writes the code. The main statement assigns execution to the agent and defense of the experiment to the researcher.

**What I want to say (draft):** Connect agent-assisted coding to the course’s previous experiments. Ask which choices and checks the researcher must preserve when delegating execution. Explain that students may participate using available access or observe the same prompts, code, and results; paid access is not required.

### Slide 48 — What did we leave unsaid?

Day 4, slide 2 · Current timing: 10–20 · context

**On the slide:** The vague request “Build the best model” is unpacked into population, metric, and evaluation questions.

**What I want to say (draft):** Explain that a language model works with supplied or retrieved context, and missing scientific choices still have to be resolved somehow. Discuss the task, population, target, features, splits, fitting rules, metrics, and evidence that should be explicit. Fluent output does not establish that these choices match the researcher’s intention.

### Slide 49 — An agent can act on its assumptions.

Day 4, slide 3 · Current timing: 20–30 · agent loop

**On the slide:** An agent loop moves through inspecting context, acting with a tool, observing the result, and revising or reporting. A question asks where to stop if an input is wrong.

**What I want to say (draft):** Distinguish the language model from an agent that can use tools to read, edit, and execute. Explain how observations feed subsequent actions. A wrong assumption can propagate through a perfectly functioning loop. Instructions should require stopping or reporting when inputs fail checks; code and artifacts let us inspect what actually happened.

### Slide 50 — Ask vaguely. Inspect the choices.

Day 4, slide 4 · Current timing: 30–40 · vague request

**On the slide:** A shortened vague request introduces a link to the actual saved vague-run report. Students inspect feature choice, metrics, search, and biological claims.

**What I want to say (draft):** Read the actual prompt and identify decisions it left open before showing the run’s choices. This run compared six candidates using training-only group cross-validation and log loss, then chose a model using the disclosed motif. It was scientifically cautious. Discuss its real decisions and the recorded technical intervention without pretending it made the authored fixture’s mistakes.

### Slide 51 — This one runs. Its claim still fails.

Day 4, slide 5 · Current timing: 40–50 · inspect the fixture

**On the slide:** A separate authored flawed-analysis fixture asks students to find evidence of a misleading result. Hints mention related groups crossing splits and reordered predictions.

**What I want to say (draft):** Clearly identify this as a teaching exercise, not an observed agent failure. Have students inspect group leakage, vocabulary fitting before splitting, prediction/label misalignment, and an unsupported promoter-biology claim. Ask for the evidence and consequence of each defect before proposing repairs.

### Slide 52 — Break · 10 minutes

Day 4, slide 6 · Current timing: 50–60 · break

**On the slide:** A ten-minute break introduces the need to make scientific choices explicit before requesting another analysis.

**What I want to say (draft):** Return at minute 60. We will separate a precise specification from reusable project instructions and an audit procedure.

### Slide 53 — Specify the experiment.

Day 4, slide 7 · Current timing: 60–73 · specification

**On the slide:** A specification groups requirements into question/data/features, protocol/splits/metrics, and evidence/predictions/provenance. A link opens the precise specification.

**What I want to say (draft):** Walk through the analysis specification and explain how each requirement can be checked. Fix the simulated task, training-only fitting, development partitions, primary ROC-AUC, supporting metrics, threshold, and deliverables. Keep the agent task development-only, including after the Day 3 test has been revealed. Ask pairs to choose one requirement and describe an independent verification.

### Slide 54 — Give each instruction a job.

Day 4, slide 8 · Current timing: 73–85 · instructions and skill

**On the slide:** Three instruction types are distinguished: a specification for this analysis, AGENTS.md for project constraints, and a skill for a reusable audit procedure. Links open the supplied examples.

**What I want to say (draft):** Show the actual files and explain their different roles. Task-specific data and outputs belong in the specification; persistent project boundaries belong in project instructions; a reusable checking procedure belongs in a skill. These can make expected behavior clearer and more inspectable, but do not guarantee compliance or scientific validity.

### Slide 55 — The vague run scored higher. Why?

Day 4, slide 9 · Current timing: 85–100 · actual-run comparison

**On the slide:** A validation ROC-AUC chart compares the actual vague run, about 0.904, with the specified fixed 4-mer baseline, about 0.802. A question asks whether this compares prompts or different experiments.

**What I want to say (draft):** Explain that the vague run used different features, objectives, and search from the specified run. Both were scientifically cautious, and the specified run reproduced the requested baseline. Their score difference cannot establish that vague prompts are better or that specifications harm performance. Inspect the artifacts to discuss which decisions were constrained and which remained open.

### Slide 56 — Break · 10 minutes

Day 4, slide 10 · Current timing: 100–110 · break

**On the slide:** A ten-minute break introduces “Evidence → consequence → repair.”

**What I want to say (draft):** Return at minute 110. The next activity applies one scientific standard to both manual and agent-written analyses.

### Slide 57 — Join by ID. Then judge the predictions.

Day 4, slide 11 · Current timing: 110–130 · scientific audit

**On the slide:** An authored two-row example has labels ordered v1, v2 and predictions ordered v2, v1. Pairing by position appears 100% accurate; aligning by ID gives 0%.

**What I want to say (draft):** Work through the join explicitly so students can see how plausible probabilities produce a false result. Equal array length is not enough. Use the audit code and checklist to require exact prediction coverage, uniqueness, and correct identity alignment. Correcting this join fixes one defect, not every other problem in the analysis.

### Slide 58 — Repair the experiment before the score.

Day 4, slide 12 · Current timing: 130–150 · repair and interpretation

**On the slide:** A repair framework asks what failed, which claim becomes unsupported, and what needs to be rerun. A link opens the scientific-audit checklist.

**What I want to say (draft):** Lead the audit across split integrity, training-only preprocessing, prediction identity, declared metrics and baselines, reproducibility, and scientific claims. Ask students to connect every finding to evidence and a specific repair. Refit when needed rather than inventing replacement scores. Preserve time for the final demonstration and discussion.

### Slide 59 — Follow the evidence through Agentomics.

Day 4, slide 13 · Current timing: 150–170 · reserved demonstration

**On the slide:** A reserved twenty-minute Agentomics demonstration asks where the question, executed workflow, and supporting evidence become visible. Actual preparation is explicitly marked pending.

**What I want to say (draft):** Use an actual instructor-prepared Agentomics example to connect automation with the choices covered in the course. Show the real workflow and artifacts, then apply the same audit questions. The specific walkthrough remains to be supplied because access, example, materials, and rehearsal are pending; the current slide does not describe verified product behavior.

### Slide 60 — What would you trust now?

Day 4, slide 14 · Current timing: 170–180 · final discussion

**On the slide:** The course ends with four stages: count, learn, reuse, delegate. Students name one claim they can defend and one limitation they would report. Links lead to code, exercises, and answers.

**What I want to say (draft):** Use the final ten minutes for students’ conclusions and questions. Revisit how representations change accessible information, how evaluation supports generalization claims, and how delegation changes execution while leaving scientific responsibility with the researcher. Ask what students would now check before trusting an analysis and what remains unclear.
