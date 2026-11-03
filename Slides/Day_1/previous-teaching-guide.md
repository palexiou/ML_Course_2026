# Day 1: expanded teaching guide

**Historical deck reference — marked 2026-11-03.** Superseded as the active narrative-planning entry by [day1-story.md](story.md), whose six-section timing is proposed pending discussion. The cues below document the earlier deck implementation and remain useful when inspecting it; they are not a fixed slide count or the new production style. Retained in place to preserve source-report and deck links. Follow the [approved style](../../docs/course-wiki/teaching-preferences.md#style-approved--2026-11-03) for future revisions.

Built from your Day 1 comments in [teaching-outline.md](../teaching-outline.md). That annotated document is preserved. This guide matches the rebuilt Day 1 section of [index.html](presentation.html#day-1).

There are 62 slides across 180 minutes. Most explanations use several slides over a ten-minute block; practical and break slides stay up while the activity takes place. Timings are flexible teaching allocations, not an automatic advance or a completed rehearsal. Use **N / Notes** for the same speaking cues inside the presentation, or use the slide selector to jump to a topic.

The instructor introduction uses the supplied name and position: **Panagiotis Alexiou, ERA Chair, University of Malta**. No research biography has been invented.

## Sequence

| Minutes | Teaching block | Slides |
| --- | --- | --- |
| 0–10 | Course, instructor, outcomes, notebook startup | 1–4 |
| 10–16 | Inputs/targets and an ungraded metric diagnostic | 5–6 |
| 16–28 | Learning map and individual learning problems | 7–12 |
| 28–36 | Biological motivation and controlled simulation | 13–16 |
| 36–50 | K-mers, count vectors, and practical A | 17–22 |
| 50–60 | Break | 23 |
| 60–70 | Training, validation, and test | 24–27 |
| 70–80 | Logistic regression: score, sigmoid, decision, fitting | 28–31 |
| 80–94 | Confusion matrix, metrics, and threshold demonstration | 32–39 |
| 94–100 | Fit and inspect predictions in practical B | 40–41 |
| 100–110 | Break | 42 |
| 110–122 | Trees, interactive path, overfitting, and forests | 43–46 |
| 122–140 | Fair comparison and feature interpretation | 47–51 |
| 140–150 | Why related samples can make a score misleading | 52–54 |
| 150–175 | Step-by-step leakage investigation | 55–60 |
| 175–180 | Recap and link to Day 2 | 61–62 |

## Teaching cues

### D1 · 01 — Machine learning for bioinformatics

**Timing:** 0–2 · welcome · **Original outline section:** 01

**On the slide:** From biological questions to models you can explain. Understand → apply → interpret

**Say / explain:** Welcome the group. Explain that the course is an introduction for students comfortable with Python, with no assumption of prior ML expertise. We will build and inspect working analyses, starting from familiar data structures.

**Transition:** Introduce yourself and why you are leading the course.

### D1 · 02 — Panagiotis Alexiou

**Timing:** 2–4 · your instructor · **Original outline section:** 01

**On the slide:** ERA Chair · University of Malta Biological questions. Computational tools. Careful interpretation.

**Say / explain:** Introduce yourself as Panagiotis Alexiou, ERA Chair at the University of Malta. Connect the course to the skills you want students to gain: framing a biological question, running a model, and interpreting its evidence. If useful, add one brief example from your own work; no research biography has been assumed.

**Transition:** Tell students what they should be able to do by the end.

### D1 · 03 — By the end, you should be able to…

**Timing:** 4–6 · course goals · **Original outline section:** 01

**On the slide:** One connected workflow across four days. Choose Turn a biological question into an ML task. Build Use classical, neural, and pretrained models. Explain Interpret predictions and audit an analysis.

**Say / explain:** Walk through the three outcomes. Preview the four days: classical models; neural networks; pretrained representations; coding agents. Explain that the practicals provide working code and short exercises. There is no exam, homework, or required submission.

**Ask:** Which of these is most unfamiliar?

**Expected answer:** Use responses to set your emphasis; this is not an assessment.

**Transition:** Open the execution environment together.

### D1 · 04 — Open your working notebook

**Timing:** 6–10 · startup · **Original outline section:** 01

**On the slide:** Practical work happens in Colab. 1 Open a blank Colab notebook. 2 Run print("Ready for ML") . 3 Open the Day 1 practical and check the imports.

**Say / explain:** Allow four minutes for access and a tiny code cell. Use the practical’s setup instructions to check NumPy, pandas, scikit-learn, and matplotlib. Students with access problems can follow your projected notebook. Do not start explaining model results during setup.

**Ask:** Can everyone run one cell, or follow the projected notebook?

**Expected answer:** A running or observation route is enough to continue.

**Transition:** Before any models, establish what we mean by an example and a target.

### D1 · 05 — What does one training example look like?

**Timing:** 10–12 · starting vocabulary · **Original outline section:** 02

**On the slide:** An input paired with an answer we want to predict. Input: x A sequence, an image, or a gene-expression profile. Target: y A category or a measured quantity.

**Say / explain:** Explain sample, feature, and target with a familiar biological example such as a sample’s expression measurements and condition. Inputs are available to the predictor. The target is the answer used to teach or evaluate it. Do not introduce sequence simulation yet.

**Ask:** For predicting a sample’s condition, what is x and what is y?

**Expected answer:** Expression measurements are inputs; condition is the target.

**Transition:** Show some model scores and ask what the class already recognizes.

### D1 · 06 — What do these numbers tell you?

**Timing:** 12–16 · diagnostic · **Original outline section:** 02

**On the slide:** Illustrative classifier · 100 examples · we will unpack this later. Accuracy 70% Precision 75% Recall 60% F1 67%

**Say / explain:** Ask which metric names students recognize and what they think each describes. Do not expect correct definitions. The values come from one consistent teaching example: TP 30, FP 10, FN 20, TN 40. We will revisit the same numbers rather than introduce a new puzzle later.

**Ask:** Could two of these numbers tell different stories about the same classifier?

**Expected answer:** Yes. They count different subsets of predictions and labels. Accept uncertainty and return to this after the confusion matrix.

**Transition:** Place classification within the wider map of ML.

### D1 · 07 — Start with the kind of question

**Timing:** 16–18 · ML map · **Original outline section:** 03

**On the slide:** A small map of machine learning. Machine learning Supervised Learn from inputs + targets Unsupervised Find structure in inputs Classification A category Regression A quantity Clustering Groups of samples Dimensionality reduction A smaller representation

**Say / explain:** Walk down the tree once. Supervised learning uses a supplied target. Unsupervised learning looks for structure without that target. Classification, regression, clustering, and dimensionality reduction will each get their own example. This is a useful introductory map rather than an exhaustive taxonomy.

**Transition:** Start with supervised classification.

### D1 · 08 — Classification predicts a category

**Timing:** 18–20 · classification · **Original outline section:** 03

**On the slide:** Supervised learning · examples come with labels. Input Gene-expression measurements for a sample. Target Condition A or condition B.

**Say / explain:** Use two known conditions as the example. Explain binary versus multiclass classification and that a model can produce probabilities before selecting a class. The labels are observations supplied to the learning procedure, not groups it discovers on its own.

**Ask:** Is predicting a treatment-response class classification?

**Expected answer:** Yes, if the response is represented by defined categories.

**Transition:** Change the target from a category to a quantity.

### D1 · 09 — Regression predicts a quantity

**Timing:** 20–22 · regression · **Original outline section:** 03

**On the slide:** Supervised learning · the target is numeric. Input feature Measured expression

**Say / explain:** Use the plotted points as an illustration of a continuous target. The fitted line summarizes a relationship and makes a prediction for a new input. The drawing is not a course experiment. The key distinction from classification is the meaning of the target, not which software function is called.

**Ask:** Would predicting a concentration be classification or regression?

**Expected answer:** Regression, if concentration is the numeric target.

**Transition:** Now remove the supplied target labels.

### D1 · 10 — Clustering looks for groups

**Timing:** 22–24 · clustering · **Original outline section:** 03

**On the slide:** Unsupervised learning · no condition labels are supplied.

**Say / explain:** Explain clustering using expression profiles that resemble one another. A grouping algorithm can find structure without being told condition labels. Discuss that a cluster can reflect biology, batch, or another source of similarity. It does not automatically become a verified cell type.

**Ask:** If clusters match experimental batches, is that necessarily biology?

**Expected answer:** No; structure can reflect technical effects.

**Transition:** Another unsupervised task makes a high-dimensional input easier to inspect.

### D1 · 11 — Summarize many features in fewer dimensions

**Timing:** 24–26 · dimensionality reduction · **Original outline section:** 03

**On the slide:** Example: visualize expression profiles. 20,000 measurements → 2 coordinates An illustrative dimensionality-reduction step, such as PCA.

**Say / explain:** Explain why we sometimes summarize many correlated measurements using fewer coordinates. A two-dimensional plot is useful for inspection but cannot preserve every relationship in the original data. Clustering assigns groups; dimensionality reduction changes the representation.

**Ask:** Does a two-dimensional plot show all differences between samples?

**Expected answer:** No. What is retained depends on the method and settings.

**Transition:** Introduce the learning setup that will make Day 3 possible.

### D1 · 12 — Create a learning target from the input

**Timing:** 26–28 · self-supervision · **Original outline section:** 03

**On the slide:** Self-supervised pretraining · a preview of Day 3. DNA context: … ACGTAC [MASK] GGATCC … Target: the token hidden by the mask

**Say / explain:** Explain that the original sequence supplies the missing-token target. Self-supervision still has an objective and targets; they are constructed from the inputs. Later we can use the learned features in a supervised classifier. This is a conceptual sketch, not exact model tokenization.

**Transition:** Choose a single biological motivation for our supervised practical.

### D1 · 13 — Our practical: classify DNA sequences

**Timing:** 28–30 · biological motivation · **Original outline section:** 04

**On the slide:** Promoter prediction motivates the question. DNA sequence → class 0 or class 1

**Say / explain:** Now introduce promoter recognition as motivation. Explain that real promoter prediction would need measured or annotated biological labels. Our controlled simulation is simpler: we know which signal was planted and can test what the models use. This lets the course focus on the ML workflow.

**Ask:** Why might known ground truth be helpful when learning to interpret a model?

**Expected answer:** It gives us a specific explanation to compare with the model’s behavior.

**Transition:** Show exactly what one row in our course dataset contains.

### D1 · 14 — One row, three different roles

**Timing:** 30–32 · data rows · **Original outline section:** 04

**On the slide:** Illustrative row from the type of table we will use. sample_id A handle for matching records. sequence The input the classifier reads. label The answer: 0 or 1.

**Say / explain:** Point to each field. The sequence becomes model input; the label is used for fitting and evaluation; the ID keeps records aligned. Group and split fields describe experimental organization. They are not additional predictive features. This gives a concrete purpose to the earlier data-inspection practical.

**Ask:** Should sample_id be a feature just because it is in the table?

**Expected answer:** No. Its job is identity, not the biological prediction.

**Transition:** Explain how those sequences and labels are generated.

### D1 · 15 — Plant a clue more often in one class

**Timing:** 32–34 · simulation · **Original outline section:** 04

**On the slide:** 1,200 sequences · 160 bases · 600 examples per class. Class 1 Plant TATAAATG with probability 0.9. Class 0 Plant TATAAATG with probability 0.1.

**Say / explain:** Start with uniform random DNA backgrounds and balanced sampled labels. Plant the motif at a random position with the class-dependent probability shown. These probabilities make the task learnable without making the label a perfect motif-presence rule.

**Transition:** Ask what the noise means for an ideal motif detector.

### D1 · 16 — A perfect detector can still make a wrong prediction

**Timing:** 34–36 · label noise · **Original outline section:** 04

**On the slide:** Class label and motif presence are related, but different. Which examples would a motif-only rule misclassify?

**Say / explain:** Ask the students to identify the two kinds of exceptions. Also explain that random background can contain an incidental motif match. This separates the input signal, simulation truth, and class label before discussing predictions or metrics.

**Ask:** Would motif detection guarantee 100% classification accuracy?

**Expected answer:** No, because the planting probabilities are not zero and one.

**Transition:** Turn the sequence into a numeric representation.

### D1 · 17 — Move a window along the sequence

**Timing:** 36–38 · k-mers · **Original outline section:** 05

**On the slide:** A 4-mer is a word of four bases. ACGTAC ACGT window 1 CGTA window 2 GTAC window 3

**Say / explain:** Read the three windows from left to right. Generalize to L−k+1 overlapping windows. The choice of k sets the length of local patterns we can count. No model has been fitted yet; we are defining an input representation.

**Ask:** How many 4-mer windows are in ACGTAC?

**Expected answer:** Three.

**Transition:** Combine the windows into a fixed-length count vector.

### D1 · 18 — Count each possible DNA word

**Timing:** 38–40 · feature vectors · **Original outline section:** 05

**On the slide:** Four bases and four positions give 4⁴ = 256 possible words. ACGT 1 CGTA 1 GTAC 1 Other 4-mers 0

**Say / explain:** Keep the ACGTAC example. Explain that each feature column corresponds to one word and its value is the occurrence count. A fixed complete 4-mer alphabet has 256 possible columns; the implementation’s training-fitted vocabulary can omit unseen words. This representation can be used by several different classifiers.

**Transition:** Explain the meaning of a bag representation.

### D1 · 19 — A count does not tell you the position

**Timing:** 40–43 · representation · **Original outline section:** 05

**On the slide:** “Three occurrences” does not say where they happened. Sequence → bag of 4-mer counts

**Say / explain:** Point out the concrete distinction: the vector answers how often a word appears, not at which base it begins. Do not claim that every motif shift preserves all counts, because boundary windows may change. Day 2 will build a controlled pair with exactly equal bags.

**Ask:** If a vector says TATA appears three times, can we recover the three starting positions?

**Expected answer:** No; those positions are not stored in the count vector.

**Transition:** Switch from slides to the notebook and inspect these objects directly.

### D1 · 20 — Open the data in Colab

**Timing:** 43–45 · practical A · **Original outline section:** 06

**On the slide:** The slides give instructions; the notebook runs the code. Switch to Colab Run Practical A, steps 1–2: generate the course data and display the training table. Open the Day 1 practical ↗

**Say / explain:** Make the environment switch explicit. In the practical guide, paste the complete standalone code 01 into a notebook cell and run it once, then execute the short inspection cell. It saves both classical models already; tell students we are looking at the data now and will explain the outputs later. Label previous saved outputs if live execution fails.

**Ask:** Which field is the model input, and which is the target?

**Expected answer:** sequence is the input; label is the target; sample_id tracks the row.

**Transition:** Give students a second small task on the counts.

### D1 · 21 — Inspect the words in one sequence

**Timing:** 45–48 · practical A · **Original outline section:** 06

**On the slide:** Stay in Colab · Practical A, step 3. Switch to Colab Count its 4-mers. Inspect the most frequent words. Check that all counts sum to 157. Open the Day 1 practical ↗

**Say / explain:** Use the Counter cell provided in the guide. Students should inspect a short list of word/count pairs and verify the window total. This activity is data inspection, not another model-fitting task. If setup is delayed, work through the short six-base example together.

**Ask:** Why can the number of distinct 4-mers be smaller than 157?

**Expected answer:** The same word can occur more than once.

**Transition:** Return to the slides and connect x to y.

### D1 · 22 — We now have an input and a target

**Timing:** 48–50 · checkpoint · **Original outline section:** 06

**On the slide:** Back to the slides. x A vector of 4-mer counts. y The sequence’s class label.

**Say / explain:** Ask a student to describe one training example in words. Make sure count vector and target label are clear. Close the first block with the need to evaluate on examples that did not fit the model.

**Ask:** What do we want the model to learn from x?

**Expected answer:** A relationship that helps predict y for new examples.

**Transition:** Take the scheduled break.

### D1 · 23 — Break

**Timing:** 50–60 · break · **Original outline section:** 07

**On the slide:** 10 minutes Back at minute 60

**Say / explain:** Take the full ten-minute break. Check that the next notebook cells are accessible.

**Transition:** Resume with why we need held-out examples.

### D1 · 24 — A model can remember its examples

**Timing:** 60–62 · evaluation · **Original outline section:** 08

**On the slide:** A training score alone cannot tell us how it handles new data. Fit Use examples to choose model parameters. Evaluate Check predictions on other examples.

**Say / explain:** Use the analogy of memorizing answers to practice questions. A model may fit useful patterns or idiosyncrasies. We need separated roles for data so model development and final comparison are interpretable.

**Ask:** What is missing if I only report the training score?

**Expected answer:** Evidence about performance on held-out examples.

**Transition:** Assign the first role: training.

### D1 · 25 — Training data teach the model

**Timing:** 62–65 · training · **Original outline section:** 08

**On the slide:** 720 sequences in this course split. Training x + training y → fitted parameters

**Say / explain:** Explain fitting with features and labels. Parameters include logistic-regression weights and tree split rules. A learned vocabulary or scaler is also part of the fitted workflow, so it uses training data only. A fixed full alphabet is different from a vocabulary learned from observations.

**Transition:** Assign the second role: validation.

### D1 · 26 — Validation helps us make development choices

**Timing:** 65–68 · validation · **Original outline section:** 08

**On the slide:** 240 different sequences. Predict → compare → revise

**Say / explain:** Use validation to compare configurations and model families. It is not used to fit the model parameters directly in this practical, but choices based on it still adapt the analysis to those examples. That is why it is not the final independent comparison.

**Ask:** If I pick a model using validation scores, has validation influenced my workflow?

**Expected answer:** Yes; it influenced selection, even though model fitting used training rows.

**Transition:** Reserve a third partition for the planned final comparison.

### D1 · 27 — Test data answer the final, fixed question

**Timing:** 68–70 · test · **Original outline section:** 08

**On the slide:** The same split is reused for all representations. Training 720 Validation 240 Test 240

**Say / explain:** Summarize the three roles using the 60/20/20 bar. The test is kept out of today’s development feedback. Related sequences must remain together when the dataset contains them. Keep this brief; the point is a consistent evaluation protocol.

**Transition:** Build a first classifier from the count vector.

### D1 · 28 — Each feature contributes to a score

**Timing:** 70–73 · linear score · **Original outline section:** 09

**On the slide:** Illustrative weights and counts · not a fitted course result. TATA 2 × 0.6 +1.2 AATG 1 × 0.8 +0.8 CGCG 3 × −0.2 −0.6 Bias starting offset −0.4 Total score z = 1.0

**Say / explain:** Walk left to right through feature count multiplied by weight, then add the intercept. Positive weights increase the score; negative weights decrease it, holding other features fixed. These numbers are a worked illustration. No course-model coefficients are being claimed.

**Ask:** What happens to this score if the TATA count increases by one?

**Expected answer:** It increases by 0.6 with the other features fixed.

**Transition:** Turn the unrestricted score into a number between zero and one.

### D1 · 29 — Turn the score into a probability

**Timing:** 73–76 · sigmoid · **Original outline section:** 09

**On the slide:** Move the score and follow the sigmoid curve. Interactive sigmoid plot: change the linear score and observe the probability. Starts at z=1, p≈0.731.

**Say / explain:** Begin at z=1, giving p about 0.731. Move to zero, then a negative score, then a large positive score. Point to the curve rather than derive it. A sigmoid gives a model probability estimate; this does not guarantee perfect calibration on real data.

**Ask:** What probability do we get when the score is zero?

**Expected answer:** 0.5.

**Transition:** Choose a threshold to turn the probability into a class prediction.

### D1 · 30 — Probability first. Decision second.

**Timing:** 76–78 · decision · **Original outline section:** 09

**On the slide:** Our main workflow uses a threshold of 0.5. p = 0.73 ≥ 0.5 → predict class 1

**Say / explain:** Explain that the same probability can lead to a different decision under a different threshold. For now keep 0.5 fixed in the course workflow. Soon we will move a threshold on a separate illustrative example to see how different error counts change.

**Ask:** Would p=0.73 predict class 1 with threshold 0.8?

**Expected answer:** No; it would predict class 0 under that rule.

**Transition:** Explain where the weights came from.

### D1 · 31 — How do we get those weights?

**Timing:** 78–80 · fitting · **Original outline section:** 09

**On the slide:** The fitting procedure uses training examples and their labels. 1 Compute probabilities with the current weights. 2 Measure prediction error using a loss. 3 Update weights to reduce that loss.

**Say / explain:** Give the conceptual fitting loop without deriving gradients. Logistic regression is a learned model, not a set of manually supplied motif rules. Day 2 will expand loss and optimization. Now we need language to describe the errors in the predictions.

**Transition:** Return to the four numbers from the opening discussion.

### D1 · 32 — Count the four possible outcomes

**Timing:** 80–82 · confusion matrix · **Original outline section:** 10

**On the slide:** One illustrative classifier · 100 examples · 50 positives. Actual + / Predicted + 30 TP Actual + / Predicted − 20 FN Actual − / Predicted + 10 FP Actual − / Predicted − 40 TN

**Say / explain:** Read the actual and predicted labels of each cell aloud. There are 50 actual positives: 30 found and 20 missed. There are 50 actual negatives: 10 false alarms and 40 correct negatives. All metric definitions in the next slides use this same example.

**Ask:** Which cell counts an actual positive that the model missed?

**Expected answer:** False negatives: 20.

**Transition:** Count all correct predictions for accuracy.

### D1 · 33 — Accuracy: how often are we correct?

**Timing:** 82–84 · accuracy · **Original outline section:** 10

**On the slide:** Count the correct predictions among all examples. Actual + / Predicted + 30 TP Actual + / Predicted − 20 FN Actual − / Predicted + 10 FP Actual − / Predicted − 40 TN (30 + 40) / 100 = 70%

**Say / explain:** Highlight both correct cells. Reconnect this 70% to the opening dashboard. Explain with a brief counterexample that if 99 of 100 samples are negative, always predicting negative gets 99% accuracy while missing every positive.

**Ask:** Would high accuracy alone guarantee that we find the positives?

**Expected answer:** No; class balance and the pattern of errors matter.

**Transition:** Focus on the examples we predicted positive.

### D1 · 34 — Precision: can we trust a positive call?

**Timing:** 84–86 · precision · **Original outline section:** 10

**On the slide:** Of 40 predicted positives, 30 are actually positive. Actual + / Predicted + 30 TP Actual + / Predicted − 20 FN Actual − / Predicted + 10 FP Actual − / Predicted − 40 TN 30 / (30 + 10) = 75%

**Say / explain:** Highlight the predicted-positive cells. Phrase the question as: if the model sends a sample for follow-up, how often is that call right? Precision cares about false alarms among positive calls. This is a useful question when follow-up experiments cost time or money.

**Ask:** Which error reduces precision?

**Expected answer:** False positives.

**Transition:** Now start from all the truly positive examples.

### D1 · 35 — Recall: how many positives did we find?

**Timing:** 86–88 · recall · **Original outline section:** 10

**On the slide:** Of 50 actual positives, 30 were found. Actual + / Predicted + 30 TP Actual + / Predicted − 20 FN Actual − / Predicted + 10 FP Actual − / Predicted − 40 TN 30 / (30 + 20) = 60%

**Say / explain:** Highlight the actual-positive cells. Phrase this as coverage of the positives we hoped to detect. Compare the denominator with precision: all actual positives rather than all predicted positives. Discuss missed candidates as the motivating error.

**Ask:** Which error reduces recall?

**Expected answer:** False negatives.

**Transition:** Combine precision and recall into a single summary.

### D1 · 36 — F1 combines precision and recall

**Timing:** 88–90 · F1 · **Original outline section:** 10

**On the slide:** The harmonic mean gives weight to the weaker of the two. 2 × 0.75 × 0.60 / (0.75 + 0.60) = 0.667 ≈ 67%

**Say / explain:** Use the same precision and recall values from the last two slides. Explain that F1 is not their simple arithmetic average and does not use true negatives. It is one summary, not a replacement for the error counts or the biological costs of mistakes.

**Ask:** What important part of the confusion matrix does F1 leave out?

**Expected answer:** True negatives.

**Transition:** Separate ranking quality from a particular decision threshold.

### D1 · 37 — ROC looks across thresholds

**Timing:** 90–91 · ROC · **Original outline section:** 10

**On the slide:** True-positive rate versus false-positive rate. A curve calculated from the same illustrative 100-example score set, with named axes and the reference baseline.

**Say / explain:** Use the curve from the same illustrative 100-example score set. Explain recall on the vertical axis and the fraction of negatives called positive on the horizontal axis. Moving the threshold traces a curve. ROC-AUC summarizes ranking and gives half credit to ties; 0.5 is the chance-ranking reference.

**Transition:** Show a second view focused on positive calls.

### D1 · 38 — Precision–recall focuses on positive calls

**Timing:** 91–92 · precision–recall · **Original outline section:** 10

**On the slide:** Read this alongside the class balance. A curve calculated from the same illustrative 100-example score set, with named axes and the reference baseline.

**Say / explain:** Point to precision on the vertical axis and recall on the horizontal axis. Explain that retrieving more positives can include additional false alarms. Average precision is a supporting metric in our code. The example is balanced; in an imbalanced task the positive fraction changes the reference level.

**Transition:** Let students predict how changing the threshold affects the confusion matrix.

### D1 · 39 — Move the threshold. Watch the errors change.

**Timing:** 92–94 · threshold demonstration · **Original outline section:** 10

**On the slide:** Same 100 illustrative scores · the classifier itself stays fixed. Interactive probability plot with a threshold slider and live confusion counts, accuracy, precision, recall, and F1. The default reproduces the opening metric example.

**Say / explain:** Start at 0.5 to reproduce TP 30, FP 10, FN 20, TN 40 and the opening metrics. Raise and lower the threshold. Explain that recall cannot rise when the threshold rises on fixed scores, while precision is not guaranteed to change monotonically. This is a separate teaching example; the course threshold remains 0.5.

**Ask:** As we raise the threshold, do we call more or fewer samples positive?

**Expected answer:** Fewer or the same number. Recall can fall; false positives cannot increase.

**Transition:** Use the notebook to inspect actual course predictions.

### D1 · 40 — Fit in the notebook, then predict validation

**Timing:** 94–97 · practical B · **Original outline section:** 11

**On the slide:** The slide is a checklist for what to do in Colab. Switch to Colab Open Practical B. Complete the training input, training labels, validation input, and sample IDs. Open the Day 1 practical ↗

**Say / explain:** Run the short scaffold on the actual course train.csv and validation.csv already produced in Practical A. Students replace the four None placeholders. The completed answer is below a fold in the guide. This is notebook work, not an editable Python cell on the slide.

**Ask:** Which data determine the fitted 4-mer vocabulary?

**Expected answer:** Only the training sequences passed to fit.

**Transition:** Inspect the resulting prediction table together.

### D1 · 41 — Explain one prediction

**Timing:** 97–100 · practical B · **Original outline section:** 11

**On the slide:** Stay in Colab · look at the ID, true label, probability, and decision. 1 Find a false positive or a false negative. 2 Describe it using actual and predicted labels. 3 Read the confusion matrix at threshold 0.5.

**Say / explain:** Choose one row from the actual course predictions. Have a student name its error type and relate it to the matrix. If no error is found in the first rows, filter the table for mismatches. Keep the test file closed. The aim is to connect the metric vocabulary to a concrete record.

**Transition:** Take the second break, then change the classifier while keeping the features.

### D1 · 42 — Break

**Timing:** 100–110 · break · **Original outline section:** 12

**On the slide:** 10 minutes Back at minute 110

**Say / explain:** Take the scheduled break.

**Transition:** Resume with a decision tree.

### D1 · 43 — A tree asks a sequence of questions

**Timing:** 110–113 · decision trees · **Original outline section:** 13

**On the slide:** Each answer chooses the next branch. Is the TATA count at least 2?

**Say / explain:** Contrast the weighted sum with a series of threshold questions. Each internal node asks about a feature; a path leads to a leaf with a prediction. Introduce the next slide as an invented small tree used to understand the mechanism, not a recovered tree from the fitted forest.

**Ask:** Could a second question depend on the answer to the first?

**Expected answer:** Yes. The path can combine conditions on features.

**Transition:** Let the class choose counts and follow a path.

### D1 · 44 — You choose the sequence’s counts

**Timing:** 113–117 · walk a tree · **Original outline section:** 13

**On the slide:** Illustrative tree · choose values, then reveal each decision. Choose TATA and CGCG counts, then reveal one split at a time in an illustrative decision tree. Reset and try a different path.

**Say / explain:** Ask the class to choose counts between zero and five. Before each click, ask which branch will be taken. Start at TATA at least 2. If yes, ask whether CGCG is below 2. The three leaves have illustrative probabilities 0.2, 0.9, and 0.55. Show a second path with a different input.

**Ask:** Which branch will the current counts take?

**Expected answer:** For TATA=2 and CGCG=1, follow yes then yes to p=0.90. For TATA below 2, stop at p=0.20.

**Transition:** Discuss why a more detailed tree can become too specific.

### D1 · 45 — A very detailed tree can memorize training data

**Timing:** 117–120 · overfitting · **Original outline section:** 13

**On the slide:** More branches can capture patterns—or accidental details. Training A deeper tree can fit more of the observed labels. Validation New examples test whether those rules transfer.

**Say / explain:** Describe splitting repeatedly until tiny groups or individual samples remain. The resulting rules may exploit noise. Explain that tree depth and other settings are chosen using development evidence, not test scores. Avoid implying that every deep tree overfits by the same amount.

**Ask:** Why might perfect training accuracy fail to carry over?

**Expected answer:** The rules can fit accidental detail in the training examples.

**Transition:** A forest combines trees trained differently.

### D1 · 46 — A forest averages many trees

**Timing:** 120–122 · random forests · **Original outline section:** 13

**On the slide:** Different training resamples and feature choices diversify the trees. Tree probabilities 0.2 · 0.9 · 0.7 · 0.8 · 0.6 Average 0.64 → class 1 at threshold 0.5

**Say / explain:** Explain bootstrap sampling and considering random subsets of features at splits. In the implementation, class probabilities are averaged across trees. The example arithmetic is illustrative. Averaging can reduce instability, but validation still decides what happened in this experiment.

**Transition:** Make the comparison with logistic regression fair.

### D1 · 47 — Change the classifier. Keep the experiment fixed.

**Timing:** 122–125 · fair comparison · **Original outline section:** 14

**On the slide:** Both models receive the same 4-mer representation. Shared Training rows, validation rows, features, and metrics. Different Linear weighted score versus an ensemble of trees.

**Say / explain:** Show the saved classical comparison table or the practical guide’s cell. Both methods use the same training-fitted vectorizer and validation identities. This helps attribute the observed difference to the fitted workflows rather than changing the data underneath them.

**Ask:** Would two scores on different validation samples be the same comparison?

**Expected answer:** No; the data difference can affect the scores.

**Transition:** Read the actual recorded validation result.

### D1 · 48 — What changed when we used a forest?

**Timing:** 125–130 · validation result · **Original outline section:** 14

**On the slide:** Recorded local validation · simple-signal variant · ROC-AUC. Logistic regression 0.802 Random forest 0.907 0 ROC-AUC · zero-to-one scale 1

**Say / explain:** Read the metric, partition, and variant before interpreting the bars. Ask students to say what the result supports. It supports better observed validation ranking for this fitted forest here. It does not mean every forest beats every linear model. If their run differs, report its actual output and configuration.

**Ask:** Does 0.907 mean 90.7% of thresholded predictions are correct?

**Expected answer:** No. ROC-AUC is a ranking metric, not threshold-0.5 accuracy.

**Transition:** Inspect what information may drive the predictions.

### D1 · 49 — Which words mattered to the model?

**Timing:** 130–134 · feature importance · **Original outline section:** 14

**On the slide:** Open the coefficient and importance tables from Practical C. Switch to Colab Inspect the top 4-mers for logistic regression and random forest. Look for words inside the planted motif. Open the Day 1 practical ↗

**Say / explain:** Use the actual kmer_coefficients.csv and random_forest_importance.csv. Explain that a coefficient’s sign gives direction in the linear score, while the forest’s impurity-based importance has no positive/negative direction. Do not compare their numeric scales directly. Correlated overlapping words can share predictive information.

**Ask:** What would motif-related high-ranking words suggest?

**Expected answer:** That the model may be using parts of the planted signal; it is supporting evidence, not proof of a biological mechanism.

**Transition:** Spell out the words we expect inside the known motif.

### D1 · 50 — One motif supplies several overlapping features

**Timing:** 134–138 · known signal · **Original outline section:** 14

**On the slide:** Our planted motif is TATAAATG. TATAAATG TATA · ATAA · TAAA · AAAT · AATG

**Say / explain:** Connect the feature tables to these five words. A model need not assign all importance to one word or recover exactly this list. Words overlap and may occur in background sequences. This makes feature importance easier to discuss without assuming each feature corresponds to a separate biological process.

**Ask:** If two important words overlap, are they independent biological discoveries?

**Expected answer:** No. They may reflect the same planted motif.

**Transition:** Have students formulate a narrow conclusion from the evidence.

### D1 · 51 — Say exactly what the result supports

**Timing:** 138–140 · interpretation · **Original outline section:** 14

**On the slide:** Complete both sentences. “In this experiment, we observed…” “We have not yet shown…”

**Say / explain:** Invite one pair to say the forest had higher validation ROC-AUC and another to state a limitation such as simulation realism or dependence on this configuration. If the answer is vague, point back to a specific table or feature list. This is discussion, not a written assessment.

**Ask:** What is one claim you can support and one you cannot?

**Expected answer:** Supported: observed validation ranking here. Unsupported: universal superiority or real promoter recognition.

**Transition:** Now ask whether the validation examples truly represent new cases.

### D1 · 52 — A good score needs the right kind of “new”

**Timing:** 140–144 · why question a score · **Original outline section:** 15

**On the slide:** Imagine training on a sequence and validating on its near-copy. What we want Performance on genuinely new sequence families. What we might measure Recognition of relatives already seen in training.

**Say / explain:** This is the concrete explanation behind questioning a score. Use two nearly identical DNA sequences from one family. If one is in training and the other in validation, a model may recognize the family background. Explain the concern before introducing any new dataset.

**Ask:** Would a different ID make a near-copy independent?

**Expected answer:** No. Identity and relatedness are different properties.

**Transition:** Show the family relationship visually.

### D1 · 53 — Two rows can belong to one family

**Timing:** 144–147 · related samples · **Original outline section:** 15

**On the slide:** Illustrative families A, B, and C. Family A A₁ A₂ Family B B₁ B₂ Family C C₁ C₂

**Say / explain:** Explain a family as a shared background with small sequence mutations. Connect to homologous sequences or related samples as motivating analogies without claiming the simulation reproduces them. A new member of an old family is not the same evaluation target as a new family.

**Transition:** State the question the next exercise is designed to answer.

### D1 · 54 — Let’s test whether relatives inflate the score

**Timing:** 147–150 · bridge to the exercise · **Original outline section:** 15

**On the slide:** Same question, now a controlled investigation. 1 Give each family a random label. 2 Let relatives cross a row-level split. 3 Repeat with entire families held out.

**Say / explain:** Explain why this construction is useful: the family label has no transferable relation to its random background. Any strong result with overlapping families can therefore be investigated as family recognition. Announce that the exercise is separate from the main motif task and does not change its split.

**Ask:** What do you predict will happen when entire families are held out?

**Expected answer:** Performance should generally move toward chance; an exact finite-sample score is not guaranteed.

**Transition:** Introduce the small nearest-neighbor model used to expose the effect.

### D1 · 55 — Use the nearest known sequence as a guide

**Timing:** 150–154 · leakage setup · **Original outline section:** 16

**On the slide:** Separate dataset · related sequences share a random family label. Validation sequence → nearest training sequence → its label

**Say / explain:** Briefly explain nearest neighbor so the new algorithm does not appear unexplained. The model finds the closest training sequence by cosine distance in the count representation and uses its label. Related backgrounds make family members close. No motif-to-label rule was planted in this exercise.

**Transition:** First split individual rows and inspect family overlap.

### D1 · 56 — A new row can still be an old family

**Timing:** 154–158 · row split · **Original outline section:** 16

**On the slide:** Flawed split for a question about unseen families. Training A₁ B₁ C₁ Validation A₂ B₂ C₂

**Say / explain:** Read across each family’s two members. Validation rows have different IDs, but close relatives remain in training. The neighbor can recognize the family and transfer its random label. Ask students to identify the overlap before showing a score.

**Ask:** Which family is entirely unseen in validation?

**Expected answer:** None of the illustrated families.

**Transition:** Change the unit of splitting from rows to whole families.

### D1 · 57 — Hold out complete families

**Timing:** 158–162 · group split · **Original outline section:** 16

**On the slide:** Corrected split for predicting new families. Training A₁ A₂ B₁ B₂ Validation C₁ C₂

**Say / explain:** Show that all members of A and B are in training and C is held out. The label of C is randomly assigned and unrelated to A or B. This evaluation matches the desired transfer question. Keep the model type and feature construction comparable across the two strategies.

**Transition:** Run or inspect the two actual strategies.

### D1 · 58 — Compare both splits in Colab

**Timing:** 162–168 · practical D · **Original outline section:** 16

**On the slide:** The main course split stays fixed; this is a separate exercise. Switch to Colab Run Practical D with code 02. Inspect overlapping group counts, then the two balanced-accuracy values. Open the Day 1 practical ↗

**Say / explain:** Run the provided standalone leakage script or inspect clearly labeled saved outputs. Follow the practical guide to read metrics_comparison.csv. Balanced accuracy is the declared primary metric for this separate exercise; it is not the ROC-AUC used in the main representation comparison. Inspect the nearest-training-family evidence if time allows.

**Ask:** Which strategy has zero overlapping groups?

**Expected answer:** The group split.

**Transition:** Compare the recorded result with the prediction made before running.

### D1 · 59 — The split changes what the score means

**Timing:** 168–172 · leakage result · **Original outline section:** 16

**On the slide:** Recorded local run · seed 2026 · balanced accuracy. Random row split 1.000 Family group split 0.516 0 Balanced accuracy · zero-to-one scale 1

**Say / explain:** Describe the observed result precisely: the flawed row split has 197 overlapping groups and perfect balanced accuracy in the saved seed-2026 run; the corrected group split has zero overlap and balanced accuracy around 0.516. Other runs need not land exactly at chance. The important evidence is the changed family boundary.

**Ask:** Did the group split make the biological task worse?

**Expected answer:** It changed the evaluation to match transfer to unseen families; the original score answered a different question.

**Transition:** Explain the mechanism in one sentence.

### D1 · 60 — It learned to recognize relatives

**Timing:** 172–175 · explain the failure · **Original outline section:** 16

**On the slide:** Random family labels do not provide a general rule for unseen families. Family recognition ≠ transfer to a new family

**Say / explain:** Ask a student to explain why the first score was high despite random labels. Relatives carry the family background and label across the split. The correction removes that route. Link back to the earlier “what did the model learn?” question so this feels like the conclusion of the same reasoning.

**Ask:** What should we inspect before trusting a strong score on sequence data?

**Expected answer:** Relatedness and group overlap, as well as sample IDs and fitting scope.

**Transition:** Summarize the complete Day 1 workflow.

### D1 · 61 — Today’s workflow, from input to explanation

**Timing:** 175–178 · recap · **Original outline section:** 16

**On the slide:** One question → one representation → one defensible comparison. 1 Define the input, target, and unit of evaluation. 2 Represent DNA with k-mer counts and fit on training data. 3 Read validation metrics and inspect what drives predictions.

**Say / explain:** Recap classification, k-mer features, logistic regression, random forest, metric definitions, and the separate leakage lesson. Invite a short question or point of confusion. If time was lost earlier, protect this explanation rather than opening an optional extra model.

**Transition:** Close with a question that leads directly to Day 2.

### D1 · 62 — What if position carries the answer?

**Timing:** 178–180 · next time · **Original outline section:** 16

**On the slide:** Tomorrow: one-hot DNA and learned features. How could we keep information that a bag of words discards?

**Say / explain:** Return to the fact that count vectors omit explicit positions. Day 2 will change the representation and learn local features with a CNN while retaining the same evaluation discipline. Leave the remaining time for final questions and remind students that no homework is required.

**Transition:** End Day 1.
