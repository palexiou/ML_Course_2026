# Day 1 story — discussion draft

Updated 2026-11-03: the instructor agreed the six-section topic sequence below. Detailed beats and timings remain editable for discussion. Edit this file to shape the narrative, then revise the actual slides **one section at a time**. This is the active Day 1 story source. The instructor's comments in [teaching-outline.md](../teaching-outline.md#day-1) remain authoritative and untouched. Follow the [approved style and preferences](../../docs/course-wiki/teaching-preferences.md#style-approved--2026-11-03), demonstrated by the [logistic pilot](logistic-style-reference.html).

The story connects a biological question to numerical features, a learned prediction, useful evaluation, a different model, and an explanation that transfers to new sequences. Teach every concept through explanation and discussion. The instructor agreed to completed notebooks in GitHub opening through Colab. Instructor demonstrations with optional student follow-along remain a **delivery proposal**; the level of hands-on work is open, and scaffolded practicals are retained. Execution is never a prerequisite for answering the checkpoints below.

## Three-hour shape

| Minutes | Section | Teaching minutes |
| --- | --- | --- |
| 0–25 | 1. Course and ML introduction | 25 |
| 25–50 | 2. DNA → feature table | 25 |
| 50–60 | Break | — |
| 60–90 | 3. Logistic regression on k-mer counts | 30 |
| 90–115 | 4. What makes a prediction useful? | 25 |
| 115–125 | Break | — |
| 125–155 | 5. What changes with a tree or forest? | 30 |
| 155–180 | 6. Explainability: what did the model learn? | 25 |

Total: **160 teaching minutes + two 10-minute breaks = 180 minutes**. Questions and any demonstrations fit inside the section allocations; they are not extra activities. This proposal moves the second break from minute 100 to 115 and replaces the earlier dedicated opening startup block with a concept-first opening. The [accepted earlier timetable](../../instructor/guide.md) remains historical authority until the instructor agrees to those changes. If everyone must execute, budget in-class startup explicitly before implementing the slide timings; no pre-course setup or homework is assumed.

## 1. Course and ML introduction · 0–25

**Story question:** What can a model help us ask about biological data?

**Exit understanding:** Students can name an input and a target, distinguish classification, regression, clustering and self-supervised learning, and identify which kind of question a model is answering. The DNA working example first appears in section 2.

**Narrative beats:**

1. Open with the course: understand models, use working analyses, and explain predictions. Introduce Panagiotis Alexiou, ERA Chair, University of Malta; leave any personal research example for the instructor to supply.
2. Preview the four-day route: classical predictors → neural representations → pretrained representations → coding agents. Explain the expected outcomes and the absence of exams, homework and submissions.
3. Build the learning map progressively. Under supervised learning, explain classification with sample condition and regression with a measured quantity; under unsupervised learning, explain grouping expression profiles without condition labels. Give each branch its own explanatory moment.
4. Add self-supervised learning with a familiar missing-word prediction example. Explain how a training target can come from the input itself, without introducing the DNA working example.
5. Ask an ungraded diagnostic about which metric names students recognize; definitions will come after the model. Close on choosing the kind of ML question before choosing an algorithm. Biological DNA motivation belongs in section 2.

**Specific visual/example:** One expanding learning-problem tree, highlighting one branch and its biological input/output example at a time. Finish on a general input → task → output map; introduce the DNA working example only in section 2.

**Observation checkpoint:** “Is predicting a numeric expression level the same kind of output as predicting one of two classes?” Ask for the output type, not an equation or code.

**Transition:** “We have a map of ML questions. Next we will build one working example from input to model.”

## 2. DNA → feature table · 25–50

**Story question:** How does a sequence become one row of model inputs?

**Exit understanding:** Students can trace overlapping k-mer windows into counts, separate features from labels and IDs, and explain why fitting and checking predictions need different examples.

**Narrative beats:**

1. **First introduce the DNA working example here.** Motivate sequence classification with promoter recognition, then show the actual task's ingredients: 1,200 simulated 160-base sequences, class labels and a planted motif, `TATAAATG`. Planting probabilities 0.9 versus 0.1 make the signal informative but imperfect; background matches can also occur.
2. Zoom into the short worked sequence `TATACCGCGCGCGTATAAATG`. Slide a four-base window along it before naming the resulting features. This 21-base teaching sequence is a magnified example, distinct from the 160-base course data.
3. Build a count row: `TATA=2`, `AATG=1`, `CGCG=3`, alongside the other word columns. Explain 4⁴ = 256 possible words and L−k+1 windows: 18 in this short example, 157 in a course sequence. A training-fitted vocabulary may omit unseen words.
4. Add a label beside the row and an ID for tracking. The count vector stores how often, without explicitly retaining each occurrence's position; labels, IDs and simulation-truth fields stay outside the predictive features.
5. Give the data roles a purpose: training fits the vocabulary and model; validation checks new predictions and supports development choices. Briefly reserve the separate test partition for the fixed Day 3 comparison. The main split has 720/240/240 examples.

**Specific visual/example:** The short DNA string becomes overlapping windows, then a feature-table row. Keep the three selected count columns in fixed positions for the next section.

**Optional demonstration / observation checkpoint:** Use [Practical A](../../instructor/practicals.md#practical-a--slides-2022-inspect-the-data-and-count-words) to inspect a row and count windows, or do the same on the visual. Ask: “Can this row tell us where each TATA starts?” Expected answer: the count alone cannot.

**Transition:** “The row contains evidence. How does a fitted model combine it into a prediction?” Then take the full 50–60 break.

## 3. Logistic regression on k-mer counts · 60–90

**Story question:** How does logistic regression turn k-mer counts into a probability and then a class?

**Exit understanding:** Students can work through count × weight, bias, score, sigmoid and threshold, and distinguish applying fixed weights from learning those weights.

**Narrative beats:**

1. Restore the same count row and attach signed weights: +0.6, +0.8 and −0.2. A positive contribution raises the score; a negative one lowers it, holding other features fixed.
2. Reveal products +1.2, +0.8 and −0.6, then the bias −0.4. Add them to obtain z=1. The reduced worked model assigns zero weight to the other features, rather than pretending those words do not exist.
3. Carry z=1 onto an enlarged sigmoid: p=1/(1+exp(−z))≈0.731. Explain what happens at z=0 and why a raw score differs from a model probability.
4. Carry the same probability onto a threshold line. At 0.5 the decision is class 1; at a hypothetical 0.8 it would be class 0. A predicted label is not the unknown observed label, and the probability is not a guarantee of correctness.
5. Rewind to fitting: training examples and their labels supply a loss; optimization changes weights and bias to reduce that loss. Validation checks predictions afterwards. Connect this loop to `fit` and `predict_proba`; leave gradient derivations for outside this introduction.

**Specific visual/example:** The [seven-step pilot sequence](logistic-style-reference.html), with a stable count/weight layout and one focal operation at each step. Production wording follows the approved style source.

**Optional demonstration / observation checkpoint:** Ask “What happens to z if TATA increases by one?” Answer: +0.6 with other counts fixed. An instructor may vary the existing sigmoid control or show the completed replacements in [Practical B](../../instructor/practicals.md#practical-b--slides-4041-fit-and-inspect-predictions); everyone can explain the same calculation without running it.

**Transition:** “We can make a prediction. Across many sequences, how do we describe what it gets right and wrong?”

## 4. What makes a prediction useful? · 90–115

**Story question:** Which errors matter, and what do the metrics count?

**Exit understanding:** Students can read a confusion matrix, explain precision, recall and F1 using their denominators, and separate thresholded decisions from ranking and generalization.

**Narrative beats:**

1. Return to the diagnostic numbers through one 100-example matrix: TP=30, FP=10, FN=20, TN=40. Establish actual versus predicted labels before using abbreviations. Accuracy is (30+40)/100=70%.
2. Highlight predicted positives: precision=30/(30+10)=75%. Connect false positives to unnecessary follow-up experiments.
3. Highlight actual positives: recall=30/(30+20)=60%. Connect false negatives to missed candidates. Combine the same values with F1=2PR/(P+R)=2/3; explain that F1 omits true negatives.
4. Move a threshold on fixed probabilities. Raising it calls fewer or the same number positive, cannot increase recall or false-positive count, and does not guarantee a monotonic precision change. Class balance explains why accuracy alone may conceal missed positives.
5. Distinguish a ranking curve from one threshold's errors: name ROC axes and validation ROC-AUC as the main comparison measure, with average precision supporting the positive-call view. Ask whether these predictions came from fitting examples or held-out examples; generalization concerns the latter.

**Specific visual/example:** Reuse the same matrix, highlighting only the cells in each numerator and denominator. The threshold demonstration uses the same fixed 100 scores and reproduces the matrix at 0.5; it does not change the course's 0.5 execution policy.

**Observation checkpoint:** Describe one false negative in words, then ask whether ROC-AUC=0.9 means 90% accuracy. Answer: it measures ranking, not accuracy at one threshold. Actual validation rows can be inspected with Practical B if useful.

**Transition:** “We have a way to judge predictions. What changes if the model asks a sequence of questions instead of adding contributions?” Then take the full 115–125 break.

## 5. What changes with a tree or forest? · 125–155

**Story question:** How can branching rules use the same features differently?

**Exit understanding:** Students can follow a tree path, describe how training selects useful splits, explain overfitting and forest aggregation, and compare models on the same validation examples.

**Narrative beats:**

1. Keep the same k-mer counts, but ask `TATA ≥ 2?`, followed on one branch by `CGCG < 2?`. Walk one example to a leaf, letting the class choose each branch before revealing it.
2. Show a small labeled training table behind a candidate split. Explain that fitting searches feature/threshold questions that separate the training labels into purer subsets; our drawn tree is a teaching construction, not an extracted course tree.
3. Grow a few more branches until the leaves describe tiny groups. Contrast a cleaner training fit with uncertain behavior on new rows: extra flexibility can fit accidental details.
4. Build several trees using resampled training rows and random feature choices. Average their class probabilities, consistent with the actual forest implementation. Aggregation can reduce instability; it does not promise superiority.
5. Compare the completed logistic and forest workflows using the same features, training/validation identities and metrics. Read the actual validation comparison if shown; give its dataset/configuration context and explain one observed difference without declaring a universal winner.

**Specific visual/example:** A progressively revealed tree for the same selected counts, followed by several trees feeding one mean probability. Use the existing path interaction if it supports the explanation.

**Optional demonstration / observation checkpoint:** Ask the class to choose another path, then predict how a tiny leaf could mislead on new data. [Practical C](../../instructor/practicals.md#practical-c--slides-4750-compare-and-interpret) can supply the saved validation comparison; identify saved execution as such.

**Transition:** “Both models can predict. Which sequence clues are they actually using, and what counts as a new sequence?”

## 6. Explainability: what did the model learn? · 155–180

**Story question:** Which sequence features drive the prediction, and how can we explain their contribution?

**Exit understanding:** Students can explain a local logistic-regression prediction, read coefficient and forest-importance evidence, connect overlapping k-mers to the planted signal, and state a relevant limit on that explanation.

**Narrative beats:**

1. Return to the same worked prediction. Show count × signed weight for each selected k-mer and the bias: which feature pushes this prediction up, which pushes it down, and by how much? Distinguish explaining one prediction from summarizing a model across examples.
2. Highlight the motif's overlapping words, `TATA`, `ATAA`, `TAAA`, `AAAT`, `AATG`, beside the actual coefficient table. Interpret the coefficient sign with the other features held fixed; connect it to the earlier weighted-score mechanism rather than presenting an unexplained importance plot.
3. Inspect the forest's feature importances. These summarize how features contributed to fitted splits; they do not give a positive/negative direction or use the same scale as linear coefficients. Overlapping, correlated words can share credit. Compare both models' evidence with the planted motif; predictor importance is not proof of a biological mechanism.
4. Briefly ask whether the explanation would transfer. A near-copy from a training family or a label-associated batch can offer a shortcut. Use one related-sequence drawing to distinguish a new ID from a new family, then return to the intended motif signal. The separate [leakage notebook](../../notebooks/02_split_leakage.ipynb) remains available as a demonstration/extension; the section's main topic is explainability, not a second full audit lesson.
5. Have students explain one contribution or important word in a sentence and give one limit. Recap the connected workflow, then ask what the count vector discarded: Day 2 keeps sequence position and learns features from one-hot DNA.

**Specific visual/example:** A signed contribution view for the same logistic prediction, developed into a labeled coefficient/importance comparison with the known motif's overlapping words highlighted. Use actual fitted tables for empirical claims; keep the worked numbers separate in notes.

**Optional demonstration / observation checkpoint:** Inspect the coefficient and forest-importance tables from [Practical C](../../instructor/practicals.md#practical-c--slides-4750-compare-and-interpret), or explain a prepared view. Ask: “Does a high forest importance tell us whether a word raises the class-1 probability?” Answer: no; that importance has no direction. A brief family-near-copy example can qualify generalization without displacing the explanation.

**Transition:** “Tomorrow we change what the model can see, while keeping the biological question recognizable.” No homework follows.

## Delivery and teaching-source notes

The short DNA/weights and 100-example matrix above are constructed teaching values, not fitted results. The count calculation gives 2, 1, 3; z=1 and p≈0.731058579. The short example has no invented observed label. Real course sequences have length 160; the motif simulation demonstrates a controlled signal, not empirical promoter recognition. Keep these origins and limitations in teaching source and detailed notes when adapting the figures.

For execution choices and verified GitHub-to-Colab support, see the [README delivery note](../../README.md#github-notebooks-and-colab). The subsequent cleanup packaged the completed workflows into GitHub notebooks generated from the canonical Python modules. Their setup, definition and execution cells can support either demonstration or follow-along; actual Colab execution remains unverified. The [practical guide](../../instructor/practicals.md) retains the existing inspection cells, scaffold and completed replacements; its slide numbers describe the earlier deck. Demonstration checkpoints above reference those resources without making student execution compulsory or cancelling the historical notebook-delivery agreement.

Refine section 1 first. Once its detailed story is agreed, revise that section's slides and detailed notes using the approved pilot style, check them, and then move to section 2. Keep the [earlier deck guide](previous-teaching-guide.md) as historical implementation evidence; it does not prescribe this draft's timings or slide count.
