# Day 1 story — discussion draft

Proposed on 2026-11-03; pending instructor discussion. Edit this file to shape the narrative, then revise the actual slides **one section at a time**. This is the active Day 1 story source. The instructor's comments in [teaching-outline.md](teaching-outline.md#day-1) remain authoritative and untouched. Follow the [approved style and preferences](../docs/course-wiki/teaching-preferences.md#style-approved--2026-11-03), demonstrated by the [logistic pilot](pilots/day1-logistic-story.html).

The story connects a biological question to numerical features, a learned prediction, useful evaluation, a different model, and an explanation that transfers to new sequences. Teach every concept through explanation and discussion. Instructor demonstrations with optional student follow-along are a **delivery proposal**, not a decision to remove scaffolded practicals or completed notebooks. Execution is never a prerequisite for answering the checkpoints below.

## Three-hour shape

| Minutes | Section | Teaching minutes |
| --- | --- | --- |
| 0–25 | 1. Why ML, and what kinds of questions? | 25 |
| 25–50 | 2. DNA → feature table | 25 |
| 50–60 | Break | — |
| 60–90 | 3. How does a simple model make a prediction? | 30 |
| 90–115 | 4. What makes a prediction useful? | 25 |
| 115–125 | Break | — |
| 125–155 | 5. What changes with a tree or forest? | 30 |
| 155–180 | 6. What did it learn, and will it work on new sequences? | 25 |

Total: **160 teaching minutes + two 10-minute breaks = 180 minutes**. Questions and any demonstrations fit inside the section allocations; they are not extra activities. This proposal moves the second break from minute 100 to 115 and replaces the earlier dedicated opening startup block with a concept-first opening. The [accepted earlier timetable](../docs/timed-course-plan.md) remains historical authority until the instructor agrees to those changes. If everyone must execute, budget in-class startup explicitly before implementing the slide timings; no pre-course setup or homework is assumed.

## 1. Why ML, and what kinds of questions? · 0–25

**Story question:** What can a model help us ask about biological data?

**Exit understanding:** Students can name an input and a target, distinguish classification, regression, clustering and self-supervised learning, and locate this course's task on that map.

**Narrative beats:**

1. Open with the course: understand models, use working analyses, and explain predictions. Introduce Panagiotis Alexiou, ERA Chair, University of Malta; leave any personal research example for the instructor to supply.
2. Preview the four-day route: classical predictors → neural representations → pretrained representations → coding agents. Explain the expected outcomes and the absence of exams, homework and submissions.
3. Build the learning map progressively. Under supervised learning, explain classification with sample condition and regression with a measured quantity; under unsupervised learning, explain grouping expression profiles without condition labels. Give each branch its own explanatory moment.
4. Add self-supervised learning: predict hidden sequence content to learn useful features. This supplies the Day 3 bridge without teaching transformers yet.
5. Only then introduce promoter recognition as motivation and our simpler simulated DNA classification question. Ask an ungraded diagnostic about which metric names students recognize; definitions will come after the model.

**Specific visual/example:** One expanding learning-problem tree, highlighting one branch and its biological input/output example at a time. Finish on binary sequence classification.

**Observation checkpoint:** “Is predicting a numeric expression level the same kind of output as predicting one of two classes?” Ask for the output type, not an equation or code.

**Transition:** “We have a question and a target. What numbers can a model read from a DNA sequence?”

## 2. DNA → feature table · 25–50

**Story question:** How does a sequence become one row of model inputs?

**Exit understanding:** Students can trace overlapping k-mer windows into counts, separate features from labels and IDs, and explain why fitting and checking predictions need different examples.

**Narrative beats:**

1. Show the actual task's ingredients: 1,200 simulated 160-base sequences, class labels and a planted motif, `TATAAATG`. Planting probabilities 0.9 versus 0.1 make the signal informative but imperfect; background matches can also occur.
2. Zoom into the short worked sequence `TATACCGCGCGCGTATAAATG`. Slide a four-base window along it before naming the resulting features. This 21-base teaching sequence is a magnified example, distinct from the 160-base course data.
3. Build a count row: `TATA=2`, `AATG=1`, `CGCG=3`, alongside the other word columns. Explain 4⁴ = 256 possible words and L−k+1 windows: 18 in this short example, 157 in a course sequence. A training-fitted vocabulary may omit unseen words.
4. Add a label beside the row and an ID for tracking. The count vector stores how often, without explicitly retaining each occurrence's position; labels, IDs and simulation-truth fields stay outside the predictive features.
5. Give the data roles a purpose: training fits the vocabulary and model; validation checks new predictions and supports development choices. Briefly reserve the separate test partition for the fixed Day 3 comparison. The main split has 720/240/240 examples.

**Specific visual/example:** The short DNA string becomes overlapping windows, then a feature-table row. Keep the three selected count columns in fixed positions for the next section.

**Optional demonstration / observation checkpoint:** Use [Practical A](../instructor/day1-practical.md#practical-a--slides-2022-inspect-the-data-and-count-words) to inspect a row and count windows, or do the same on the visual. Ask: “Can this row tell us where each TATA starts?” Expected answer: the count alone cannot.

**Transition:** “The row contains evidence. How does a fitted model combine it into a prediction?” Then take the full 50–60 break.

## 3. How does a simple model make a prediction? · 60–90

**Story question:** How do counts become a probability and then a class?

**Exit understanding:** Students can work through count × weight, bias, score, sigmoid and threshold, and distinguish applying fixed weights from learning those weights.

**Narrative beats:**

1. Restore the same count row and attach signed weights: +0.6, +0.8 and −0.2. A positive contribution raises the score; a negative one lowers it, holding other features fixed.
2. Reveal products +1.2, +0.8 and −0.6, then the bias −0.4. Add them to obtain z=1. The reduced worked model assigns zero weight to the other features, rather than pretending those words do not exist.
3. Carry z=1 onto an enlarged sigmoid: p=1/(1+exp(−z))≈0.731. Explain what happens at z=0 and why a raw score differs from a model probability.
4. Carry the same probability onto a threshold line. At 0.5 the decision is class 1; at a hypothetical 0.8 it would be class 0. A predicted label is not the unknown observed label, and the probability is not a guarantee of correctness.
5. Rewind to fitting: training examples and their labels supply a loss; optimization changes weights and bias to reduce that loss. Validation checks predictions afterwards. Connect this loop to `fit` and `predict_proba`; leave gradient derivations for outside this introduction.

**Specific visual/example:** The [seven-step pilot sequence](pilots/day1-logistic-story.html), with a stable count/weight layout and one focal operation at each step. Production wording follows the approved style source.

**Optional demonstration / observation checkpoint:** Ask “What happens to z if TATA increases by one?” Answer: +0.6 with other counts fixed. An instructor may vary the existing sigmoid control or show the completed replacements in [Practical B](../instructor/day1-practical.md#practical-b--slides-4041-fit-and-inspect-predictions); everyone can explain the same calculation without running it.

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

**Optional demonstration / observation checkpoint:** Ask the class to choose another path, then predict how a tiny leaf could mislead on new data. [Practical C](../instructor/day1-practical.md#practical-c--slides-4750-compare-and-interpret) can supply the saved validation comparison; identify saved execution as such.

**Transition:** “Both models can predict. Which sequence clues are they actually using, and what counts as a new sequence?”

## 6. What did it learn, and will it work on new sequences? · 155–180

**Story question:** Does the model use the intended signal in a way that transfers?

**Exit understanding:** Students can connect important k-mers to the planted signal, distinguish predictor evidence from a biological mechanism, and explain why relatives crossing a split can inflate apparent generalization.

**Narrative beats:**

1. Highlight the motif's overlapping words, `TATA`, `ATAA`, `TAAA`, `AAAT`, `AATG`, beside coefficient/importance evidence. Linear coefficients have a direction; forest impurity importances do not. Their scales are different and correlated words may share credit.
2. Make the alternative explanation concrete: a validation sequence nearly copies a training sequence's family background. A new ID need not mean a new family. An ID or batch correlated with labels could also supply a shortcut if admitted as input; our intended feature row contains only sequence counts.
3. Introduce the separate controlled leakage exercise through that question. Family A's related sequences share a randomly assigned label; family B's share another. A row split puts relatives on both sides, while a group split holds out entire families. Explain nearest-neighbor matching briefly before showing its behavior.
4. Predict the outcome, then inspect family overlap and the comparison, either through [Practical D](../instructor/day1-practical.md#practical-d--slides-5860-investigate-related-sequence-leakage) or a clearly identified saved run. The group-held-out result answers transfer to unseen families; the exercise uses balanced accuracy, unlike the main ROC-AUC comparison. No exact chance score is promised.
5. Recap the connected workflow: question → inputs/labels → features → fitting → held-out predictions → metrics → interpretation. End by asking what the count vector discarded: Day 2 keeps sequence position and learns features from one-hot DNA.

**Specific visual/example:** One family drawing with A₁/A₂ and B₁/B₂ placed across a row split, then moved together under a group split. Connect it to a near-copy sequence pair before introducing any second dataset.

**Observation checkpoint:** “Would renaming A₂ make it independent of A₁?” Answer: no; the relationship survives the ID change. Ask each pair for one model operation they can explain and one question about tomorrow's representation.

**Transition:** “Tomorrow we change what the model can see, while keeping the biological question recognizable.” No homework follows.

## Delivery and teaching-source notes

The short DNA/weights and 100-example matrix above are constructed teaching values, not fitted results. The count calculation gives 2, 1, 3; z=1 and p≈0.731058579. The short example has no invented observed label. Real course sequences have length 160; the motif simulation demonstrates a controlled signal, not empirical promoter recognition. Keep these origins and limitations in teaching source and detailed notes when adapting the figures.

For execution choices and verified GitHub-to-Colab support, see the [README delivery note](../README.md#github-notebooks-and-colab). On 2026-11-03 this checkout contained completed `.py` workflows but no notebook cells or `.ipynb` files to inspect. The [practical guide](../instructor/day1-practical.md) retains the existing inspection cells, scaffold and completed replacements; its slide numbers describe the earlier deck. Demonstration checkpoints above reference those resources without making student execution compulsory or cancelling the historical notebook-delivery agreement.

Discuss section 1 first. Once its story is agreed, revise that section's slides and detailed notes using the approved pilot style, check them, and then move to section 2. Keep the [earlier deck guide](day1-teaching-guide.md) as historical implementation evidence; it does not prescribe this draft's timings or slide count.
