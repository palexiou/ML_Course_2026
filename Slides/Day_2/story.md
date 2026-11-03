# Day 2 story

**All six sections implemented for review — 2026-11-03.** The [opening](presentation.html#day-2-s1-welcome), [learning](presentation.html#day-2-s2-section), [DNA/detectors](presentation.html#day-2-s3-section), [prediction architecture](presentation.html#day-2-s4-section), [training/comparison](presentation.html#day-2-s5-section) and [representation control](presentation.html#day-2-s6-section) contain 12/14/16/14/14/14 slides plus two ten-minute breaks: **86 scenes**. The final build replaces all six legacy scenes; no old fixed-motif primary benchmarks remain in the deck. The combined notebook includes the guided readbacks and an end-Day-2 stop. [QA](../qa.md#day-2-sections-56--2026-11-03) records checks and limits; local verification does not establish Colab execution, projector readability or classroom pacing.

**Working title:** Learning useful features from DNA.

**The story:** Yesterday we chose k-mer counts and fitted predictors. Today we build from that familiar calculation to a neural network, understand how its weights learn, and give it ordered DNA so it can learn local features. We then inspect what that buys us, including a controlled case where a bag of counts cannot distinguish the labels.

**End-of-day understanding:** A neural network composes weighted calculations and nonlinearities; training adjusts its weights using a loss and gradients; a CNN shares local detectors across a positional input; pooling and the prediction head determine what information survives. More complex models do not automatically perform better, and representation choices set limits on what any predictor can recover.

**Delivery and style:** Carry over the approved Day 1 speaker-led style: one short title, one main visual, generous whitespace, blue/orange contrast, and detailed notes. Reveal one operation at a time. Preserve letters, labels and shapes so color is not the sole distinction. These are proposed focused beats, not a mandated final slide count. Notebook execution is **GitHub ipynb → Open in Colab**, with instructor demonstration and optional follow-along; no homework, coding from scratch or submission. Each practical is inside the timetable, including startup. Questions are conversations, not scored checks.

## Three-hour shape

| Minutes | Section | Main question | Teaching minutes |
| --- | --- | --- | --- |
| 0–25 | 1. From a predictor to a neural network | What do hidden layers add? | 25 |
| 25–50 | 2. How a network learns | How do labeled examples change the weights? | 25 |
| 50–60 | Break | | — |
| 60–90 | 3. From DNA to local pattern detectors | How does one filter scan a sequence? | 30 |
| 90–115 | 4. From local features to a sequence prediction | Keep the location, or summarize it? | 25 |
| 115–125 | Break | | — |
| 125–155 | 5. Train, inspect and compare | What did the fitted CNN learn? | 30 |
| 155–180 | 6. What the representation makes possible | What can counts never distinguish? | 25 |

**160 teaching minutes + 20 break minutes = 180 minutes.** There are 84 implemented content beats (12/14/16/14/14/14 across the six sections) and two separate break slides. All timings are suggested allocations, not measured pacing. This proposal keeps Day 1’s section rhythm and moves the old Day 2 second break from 100–110 to 115–125; both break slides now follow the revised timing. It replaces the earlier thirty-minute closing catch-all with explicit synthesis and discussion. The [historical guide](../../instructor/guide.md) and [annotated outline](../teaching-outline.md#day-2) remain unchanged; this timetable is for instructor review.

**Sections:** [1 · Networks](#section-1) · [2 · Learning](#section-2) · [3 · DNA and convolution](#section-3) · [4 · Prediction architecture](#section-4) · [5 · Notebook comparison](#section-5) · [6 · Representation limit](#section-6) · [Notebook plan](#notebook-plan) · [Evidence and scope](#evidence-and-scope)

<a id="section-1"></a>

## 1. From a predictor to a neural network · 0–25

**Story question:** Can we learn intermediate features as well as the final prediction?

**Exit understanding:** Connect a neuron to Day 1, explain nonlinear activations and hidden layers, and distinguish a hidden feature from a probability.

**Built review version:** twelve slides, in the order below. Native SVG illustrations include a DNA ribbon, lettered sequence/count tallies, weighted connections, circular neurons and function curves. The ReLU count slider, hidden-unit selector and three-step forward pass work offline. The counts and all weights are constructed teaching examples; no training or empirical comparison is run by these slides. Rebuild with `python tools/build_day2_section1.py`; speaking text comes from this section, with figure and interaction source under `tools/`. Detailed checks and limits are in [QA](../qa.md#day-2-section-1--2026-11-03).

### S1-01 · Learning the features

**Proposed slide ID:** `day-2-s1-welcome` · **Time:** 0:00–0:15 (0:15)

**What is on slide:** Day 2 title; an illustrated DNA ribbon flows into a network of circular neurons; a small four-day journey highlights Day 2.

**What I want to say:** Yesterday we chose what to count. Today we keep the DNA task and ask whether the model can learn useful features. We will build the idea one operation at a time.

### S1-02 · What did our counts remember?

**Proposed slide ID:** `day-2-s1-recap` · **Time:** 0:15–2:15 (2:00)

**What is on slide:** The familiar lettered DNA example becomes colored count tallies for TATA=2, AATG=1 and CGCG=3, with no position coordinates in the resulting counts.

**What I want to say:** Counts preserve which short words occur and how often. They discard absolute positions and much of the arrangement beyond each word. A forest can learn a different function of these counts, but cannot recover information absent from its input. Invite a couple of observations, without testing recall.

### S1-03 · Learn the features, then predict

**Proposed slide ID:** `day-2-s1-goal` · **Time:** 2:15–3:45 (1:30)

**What is on slide:** Two matched illustrated paths: chosen count bars → predictor → probability; positional DNA letters → learned feature bars → probability.

**What I want to say:** Feature engineering and representation learning describe how inputs to prediction are obtained. One-hot encoding will still be chosen by us; the useful intermediate detectors will be fitted. More parameters create possibilities, not a guarantee of improvement.

### S1-04 · Start with the calculation we know

**Proposed slide ID:** `day-2-s1-weighted-sum` · **Time:** 3:45–6:15 (2:30)

**What is on slide:** TATA=2, AATG=1, CGCG=3 → weighted contributions → z=1 → p(B)≈0.731.

**What I want to say:** Reuse the constructed Day 1 example: weights 0.6, 0.8, −0.2 and bias −0.4. We already understand a weighted sum and an output activation. A logistic predictor is a useful starting point for a network, rather than an unrelated method.

### S1-05 · An activation transforms the score

**Proposed slide ID:** `day-2-s1-activation` · **Time:** 6:15–8:45 (2:30)

**What is on slide:** A large sum symbol feeds a sigmoid curve: combine the inputs, then transform the score. The next slide introduces ReLU.

**What I want to say:** An activation is a function applied to a score. Sigmoid gives our final binary output a value between zero and one. Hidden units need not use sigmoid or represent probabilities. Introduce ReLU as max(0,z), without a catalogue of activation functions.

### S1-06 · ReLU keeps the positive part

**Proposed slide ID:** `day-2-s1-relu` · **Time:** 8:45–10:45 (2:00)

**What is on slide:** One large ReLU plot and a movable point; z=1 gives 1 and z=−0.2 gives 0.

**What I want to say:** For the same illustrative weights, increasing CGCG from 3 to 9 changes the score from 1 to −0.2; ReLU then gives zero. The point is the operation, not a biological claim about CGCG. The slider and two preset buttons move between these cases. The hidden feature can exceed one; it is not a probability.

### S1-07 · A hidden unit becomes a new feature

**Proposed slide ID:** `day-2-s1-hidden-unit` · **Time:** 10:45–13:15 (2:30)

**What is on slide:** The original counts feed one hidden unit; its activation is labeled h₁.

**What I want to say:** A hidden unit computes a weighted combination and an activation. Its value becomes an input to a later calculation. It need not correspond to a named motif, and hidden does not mean mysterious or inaccessible: we can inspect its computation.

### S1-08 · Several units learn different combinations

**Proposed slide ID:** `day-2-s1-hidden-layer` · **Time:** 13:15–15:45 (2:30)

**What is on slide:** Three count nodes fan into three circular hidden units. Buttons select h₁, h₂ or h₃, highlighting that unit’s incoming connections and showing its activation value.

**What I want to say:** Units in the same layer receive the same inputs but have their own weights and biases. They can respond to different combinations of counts. This fully connected example is an explanatory bridge; our later CNN will use local connections and share weights.

### S1-09 · Combine the features into a probability

**Proposed slide ID:** `day-2-s1-output` · **Time:** 15:45–18:15 (2:30)

**What is on slide:** A three-step trace reveals hidden activations 1, 1 and 0; their output weighted sum z=0.3; then sigmoid → p(B)≈0.574. Reset repeats the trace. Exact constructed weights are in instructor notes.

**What I want to say:** The final binary classifier converts hidden features to one logit, then to p(B); p(A)=1−p(B). Hidden activations are features, not separate votes or class probabilities. This is the network forward pass for one example.

### S1-10 · Why put a bend between layers?

**Proposed slide ID:** `day-2-s1-nonlinearity` · **Time:** 18:15–20:45 (2:30)

**What is on slide:** Two affine calculations collapse algebraically into one straight response; inserting ReLU creates a visible bend in the second response curve. No box pipeline is needed.

**What I want to say:** Stacking only affine transformations still gives an affine transformation. Nonlinearity allows a network to express functions unavailable to a single linear score on these inputs. This does not restore lost positional information or establish that a network is better than yesterday’s trees.

### S1-11 · More layers build on earlier features

**Proposed slide ID:** `day-2-s1-depth` · **Time:** 20:45–22:30 (1:45)

**What is on slide:** A small network gains one further hidden layer, with ample space between stages.

**What I want to say:** Depth refers to composing multiple learned transformations. Later units operate on earlier features. Keep the explanation concrete; do not introduce a taxonomy of every neural architecture or suggest each layer has a guaranteed biological interpretation.

### S1-12 · What would you want a feature to notice?

**Proposed slide ID:** `day-2-s1-discussion` · **Time:** 22:30–25:00 (2:30)

**What is on slide:** An open discussion prompt beside a short DNA strip.

**What I want to say:** Invite ideas: a related sequence pattern, its position, combinations, or alternatives. There is no answer key. Use the suggestions to separate what an input makes available from what training might learn, then ask how the weights are actually obtained.

<a id="section-2"></a>

## 2. How a network learns · 25–50

**Story question:** How do labeled examples change all of these weights?

**Exit understanding:** Follow prediction → loss → gradients → update; explain what backpropagation computes, how minibatches and epochs organize training, and why validation selects a checkpoint while inference uses fixed parameters.

**Implemented for review — 2026-11-03.** Fourteen slides across a proposed 25 minutes, followed by the separate 50–60 break. The instructor’s “OK go for it” authorizes this build from the expanded specification. The [learning section](presentation.html#day-2-s2-section) reuses the circular network and adds interactive loss/weight curves, backward sensitivity traces, one-weight descent, step-size trajectories, minibatch/epoch illustrations, a code walkthrough and validation checkpoint selection. Keep one short title and one focal visual, with explanatory detail in Notes. Rebuild with `python tools/build_day2_section2.py`; SAY/POINT/TRANSITION text comes from this section. Source and numerical provenance are in Notes; [QA](../qa.md#day-2-section-2--2026-11-03) records actual checks and limits.

**Teaching thread:** Keep Section 1’s counts `(2, 1, 3)`, hidden features `(1, 1, 0)` and output `z=0.3 → p(B)≈0.574`. Now supply an observed training label `B / y=1`. Follow one output weight before showing how the same gradient calculation reaches the hidden layers. This is a constructed fully connected example for understanding learning; the later practical trains a CNN on positional DNA. Both use the same forward/loss/backward/update pattern.

**Delivery:** The code walkthrough is instructor-led and works entirely on slides. Optional notebook follow-along does not require installation or a training run in this section. Mathematical derivations and a live parameter search are outside the proposed 25-minute sequence.

### S2-01 · Learning changes the weights

**Proposed slide ID:** `day-2-s2-section` · **Time:** 25:00–25:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** We can now follow a prediction through a network. We chose the previous weights so that we could understand the calculation. Training uses labeled examples to adjust those weights and biases.

**Point / reveal:** Pause on the title; connect directly to Section 1’s final question about how weights are obtained.

**Transition:** Which parts of the network are actually learned?

### S2-02 · The connections contain the parameters

**Proposed slide ID:** `day-2-s2-parameters` · **Time:** 25:15–26:30 (1:15)

**What is on slide:** The familiar circular network. Highlight one connection weight, then a neuron’s bias; briefly extend the highlight across hidden and output layers. Keep the input counts in place.

**What I want to say:** A connection has a weight; each neuron also has a bias. Hidden and output parameters are fitted together. In an actual network, weights generally start from randomized values and biases follow the initialization scheme. The input encoding, architecture and training settings remain choices made by us. Labels do not directly install named biological detectors.

**Point / reveal:** Touch one weight and its receiving neuron’s bias before showing the wider set. Keep parameter numbers in Notes rather than labeling every edge.

**Transition:** Before changing a parameter, use the current values to make a prediction.

### S2-03 · First, make a prediction

**Proposed slide ID:** `day-2-s2-forward` · **Time:** 26:30–28:00 (1:30)

**What is on slide:** Trace counts `(2, 1, 3)` → hidden features `(1, 1, 0)` → `z=0.3` → `p(B)≈0.574`. Then reveal the observed label `B / y=1` beside the output, with no arrow from the label into the input.

**What I want to say:** This is the same forward calculation as before. The label tells us which output we wanted for this training example; it is used to evaluate the prediction. At a 0.5 class threshold this prediction already calls B, but a correct class call does not mean there is no remaining loss or gradient. Training uses the continuous score, not just right/wrong class calls.

**Point / reveal:** Reveal the label only after the output. Leave the probability visible for the next slide.

**Transition:** How do we turn that prediction and label into a quantity we can reduce?

### S2-04 · A confident mistake costs more

**Proposed slide ID:** `day-2-s2-loss` · **Time:** 28:00–30:00 (2:00)

**What is on slide:** One large positive-label cross-entropy curve: horizontal axis `p(B)`, vertical axis loss. Mark `p=0.8 → 0.223` and `p=0.2 → 1.609`; move a third marker to the current `p≈0.574 → loss≈0.554`. Reveal one marker at a time.

**What I want to say:** Reuse Day 1’s loss idea briefly. For this positive example, loss is `−ln(p)`; a small probability for the true label costs more. For a negative example it is `−ln(1−p)`, so the preferred direction reverses. The same loss can judge the output of one neuron or a deep network. It is the training objective, distinct from validation ROC-AUC. Model probabilities are not automatically calibrated confidence.

**Point / reveal:** Follow the curve from the confident mistake to the better prediction, then locate our current example. Avoid plotting exactly at p=0, where this positive-label loss diverges.

**Transition:** We have a loss value. Which direction should a particular weight move?

### S2-05 · Which way should this weight move?

**Proposed slide ID:** `day-2-s2-gradient` · **Time:** 30:00–32:00 (2:00)

**What is on slide:** Highlight the output connection from h₁, labeled `v₁=1.2`, beside a plot of this example’s loss against v₁. Nudge the weight left to 1.1 and right to 1.3; the loss changes from approximately 0.554 to 0.598 or 0.513. Mark the negative local slope at 1.2.

**What I want to say:** Hold all other parameters fixed for this illustration. A gradient tells us how sensitive the loss is to a small change in a parameter. Here, increasing v₁ lowers this positive example’s loss, so its derivative is negative. With many parameters, the gradient contains one derivative for each. This local sensitivity is not a guarantee about every example or a large step. The network does not need to try all these nudges during actual training.

**Point / reveal:** Keep the selected edge lit while moving along the horizontal weight axis. Explicitly distinguish this plot from the previous probability-axis plot. Put the derivative calculation in Notes; slope intuition is sufficient on screen.

**Transition:** How can we compute those sensitivities for the whole network efficiently?

### S2-06 · Backpropagation reaches the earlier layers

**Proposed slide ID:** `day-2-s2-backprop` · **Time:** 32:00–34:00 (2:00)

**What is on slide:** Reuse the network positions. Fade the forward trace and reveal gradient arrows from the loss through the output calculation and into the hidden layer. Use a different arrow style as well as color, labeled “loss sensitivity”.

**What I want to say:** Backpropagation applies the chain rule through the operations already used in the forward pass. It computes loss derivatives for hidden parameters as well as output parameters, reusing intermediate calculations. It does not adjust weights by itself; the optimizer performs that next operation. Some derivatives can be zero—for example, through an inactive ReLU on this example. These are computational sensitivities, not biological explanations or causal attributions.

**Point / reveal:** Reveal the output sensitivity first, then extend backward into one hidden unit. Avoid a separate, reversed copy of the network or a full derivative tree.

**Transition:** Now we have gradients. How are they used to change the parameters?

### S2-07 · Use the gradient to take a step

**Proposed slide ID:** `day-2-s2-update` · **Time:** 34:00–36:00 (2:00)

**What is on slide:** Return to the one-weight loss curve. Show `weight ← weight − learning rate × gradient`; the point moves from `v₁=1.200` to approximately `1.243`, with loss falling from approximately `0.554` to `0.536`.

**What I want to say:** A basic gradient-descent step moves against the gradient. A negative derivative therefore increases this weight. The example uses learning rate 0.1 and changes just one weight to make the arithmetic visible. Real minibatch training updates many parameters together. Our supplied CNN uses Adam, which uses gradient history to adapt parameter updates; this plain descent example is a teaching bridge rather than an exact replay of Adam. A real optimization path need not reach a global minimum.

**Point / reveal:** Reveal the minus sign, the negative gradient, then the movement to the right. Leave detailed numerical substitution in Notes.

**Transition:** Even with the correct local direction, how far should we step?

### S2-08 · The step size matters

**Proposed slide ID:** `day-2-s2-rate` · **Time:** 36:00–37:30 (1:30)

**What is on slide:** A smooth bowl-shaped teaching loss curve with two paths from the same start: smaller steps approach the bottom; overly large steps jump across and grow. Reveal the paths in sequence, labeled directly.

**What I want to say:** Too small a learning rate can make learning slow; too large can make it unstable. This bowl is a constructed illustration of step size, not the loss curve for the previous one-example weight, whose loss kept decreasing as that weight increased. Neural training is higher dimensional, and minibatches also make paths noisy. The declared Adam learning rate in the supplied workflow is 0.002; 0.1 above was chosen only for visible arithmetic.

**Point / reveal:** State that the axes now represent a separate teaching objective. In the eventual build, L(w)=(w−1)² with start w=3, rates 0.2 and 1.1 gives reproducible approaching and expanding paths.

**Transition:** So far we have followed one example. How do we learn from the training set?

### S2-09 · One minibatch, one update

**Proposed slide ID:** `day-2-s2-batch` · **Time:** 37:30–39:00 (1:30)

**What is on slide:** Several small lettered training-sequence strips group into a minibatch; one compact trace leads to mean loss, gradients and an update. Reveal a different batch entering after the update.

**What I want to say:** Instead of updating separately for every example or waiting for the entire dataset, this workflow averages loss over a minibatch of up to 64 examples. Its gradient therefore combines their signals. Different examples can push a weight in different directions. One minibatch produces one optimizer step here; the next batch sees the updated weights. Batch size 64 is a chosen setting, not a requirement of neural networks.

**Point / reveal:** Keep individual sequence letters visible; avoid portraying a batch as one merged DNA sequence. Put batch size next to the group, not on each sequence.

**Transition:** When have we made one pass through the training set?

### S2-10 · An epoch is one pass through the data

**Proposed slide ID:** `day-2-s2-epoch` · **Time:** 39:00–40:30 (1:30)

**What is on slide:** The primary training rows form eleven groups of 64 and one final group of 16. A moving marker completes twelve updates; reshuffle the row order to begin a second pass. Reveal “1 epoch” after the first full pass.

**What I want to say:** An epoch is one pass through all training examples. With 720 primary training rows and batch size 64, the final batch has 16 examples, so each epoch has twelve updates. The code reshuffles training order each epoch and runs 24 epochs by default. An update and an epoch are different units. The paired order-control dataset has a different training count, so its number of batches differs.

**Point / reveal:** Follow one marker over all twelve groups, then return to the start in a different order. Keep the twelve groups simple so the diagram remains readable.

**Transition:** We can now recognize those operations in the working training code.

### S2-11 · Find the operations in the code

**Proposed slide ID:** `day-2-s2-walkthrough` · **Time:** 40:30–43:30 (3:00)

**What is on slide:** Five statements, highlighted one at a time, with short operation labels alongside the active line:

```python
optimizer.zero_grad()
logits = model(inputs[indices])
loss = nn.functional.binary_cross_entropy_with_logits(logits, labels[indices])
loss.backward()
optimizer.step()
```

**What I want to say:** Trace one already-selected minibatch; its enclosing loop and tensor setup stay in Notes. Clearing old gradients prevents unintended accumulation. The model computes logits; the logits-based binary cross-entropy handles the sigmoid relationship internally, so do not sigmoid these logits before this loss call. Backward computes gradients; step applies the optimizer update. Ask the audience to point to the line matching each operation, conversationally. This static excerpt is sufficient; running the full workflow is reserved for Section 5.

**Point / reveal:** Highlight forward, then loss, then backward, then update. Finally revisit zero_grad as preparation for the next batch. The canonical source combines the forward and loss calls on one line; separating them here changes presentation only.

**Transition:** If training loss keeps falling, should we automatically keep the last set of weights?

### S2-12 · Keep the checkpoint that validates best

**Proposed slide ID:** `day-2-s2-validation` · **Time:** 43:30–46:00 (2:30)

**What is on slide:** Two separate panels with a shared epoch axis: training loss and validation ROC-AUC. Training loss decreases while validation ROC-AUC rises and then declines. Mark the best validation epoch and its saved weights. These curves are teaching constructions; actual run history is deferred to Section 5.

**What I want to say:** Training loss alone cannot tell us whether predictions improve on held-out examples. Loss and ROC-AUC measure different things, so their numerical heights and any apparent crossing are not comparable. Our workflow evaluates validation ROC-AUC after each epoch, saves an improving checkpoint and restores the highest-scoring one, keeping the earlier epoch on a tie. It still runs the declared 24 epochs; checkpoint selection is not early stopping. Validation labels guide this selection, but never enter backpropagation. Test results remain outside development and every tuning decision.

**Point / reveal:** Read the training panel first, then the validation panel, then identify the chosen checkpoint. Suggested construction: epochs 1/8/16/24, training loss 0.66/0.61/0.54/0.48, validation ROC-AUC 0.62/0.66/0.64/0.63; select epoch 8. Store this provenance in Notes, with no claim that it is an observed course result.

**Transition:** Once we select the weights, what happens when a new sequence arrives?

### S2-13 · Fitting ends; inference applies

**Proposed slide ID:** `day-2-s2-inference` · **Time:** 46:00–47:30 (1:30)

**What is on slide:** A matched pair of small network illustrations: labeled training examples with changing connection values; a new input passing through the selected, fixed weights to a probability. Use a stationary weight marker for inference rather than a box labeled “frozen”.

**What I want to say:** Inference applies the learned computation to new inputs. It does not run loss.backward or optimizer.step. Our prediction function uses eval mode and a no-gradient inference context, then applies sigmoid to its output logits. Eval mode and disabling gradient tracking have different jobs; neither is itself a learning step. A normal prediction does not change the learned weights. Validation prediction also uses fixed weights during that evaluation, although its labels are then used to score and select a checkpoint.

**Point / reveal:** Keep the probability-producing path the same in both illustrations. Remove the label/loss/update branch from the inference side.

**Transition:** Which part of this process would you want to inspect before trusting the result?

### S2-14 · What would you check during learning?

**Proposed slide ID:** `day-2-s2-discussion` · **Time:** 47:30–50:00 (2:30)

**What is on slide:** One open discussion prompt beside a quiet sketch of a training trajectory: “What would you want to watch while this model learns?”

**What I want to say:** Invite observations or questions about prediction changes, loss, unstable steps, validation behavior or compute cost. There is no required answer order or scored check. Revisit the distinction between computing a gradient and applying an update if needed. End by returning to the DNA input: we now understand how weights learn, but what numbers should we give the model so that sequence order remains available?

**Point / reveal:** Let the audience lead the discussion. Keep a static overview of the learning trace available if it helps answer a question.

**Transition:** Take ten minutes; then encode DNA in position and build a local detector.

**Construction and code notes for this section:** Section 1’s output is `z=1.2×1−0.7×1+0.5×0−0.2=0.3`. For `y=1`, `p=0.5744425` and `loss=0.5543552`. With other parameters fixed, `z=v₁−0.9`; at v₁=1.1/1.2/1.3 the losses are approximately 0.598139/0.554355/0.513015. The derivative at 1.2 is `(p−y)h₁=−0.4255575`. A plain descent step with rate 0.1 gives `v₁=1.2425557`, `z=0.3425557`, `p≈0.5848112`, `loss≈0.5364662`. These hand calculations describe one example and one selected output weight; they are not an Adam training trace or a minibatch empirical result.

The source alignment is [fit_cnn](../../course_code/03_representations.py) for the actual Adam 0.002, mean logits-based loss, batch size 64, shuffled passes, 24 default epochs and earliest-best validation checkpoint; [predict_cnn](../../course_code/course_inference.py) supplies eval/no-gradient prediction and sigmoid. The epoch illustration uses a deterministic row permutation to make the order change visible; it does not replay Torch’s random permutation or identify real sample IDs. The code walkthrough is displayed from source, without executing training. No notebook modification, library setup or CNN architecture explanation is needed in this section. If short on time, omit numerical derivative substitution and the second step-size trajectory, retaining the backward/update distinction, minibatch/epoch distinction and validation selection.

### Break · 50–60

**What is on slide:** Only “Break · 10 minutes”.

**What I want to say:** Return in ten minutes. The break is separate from teaching allocations.

<a id="section-3"></a>

## 3. From DNA to local pattern detectors · 60–90

**Story question:** How can one learned detector look for the same pattern at many positions?

**Exit understanding:** Read the channel/position axes of one-hot DNA; compute one filter score and activation; explain a shared sliding detector and its feature map; distinguish that map from a sequence probability and the hand-built example from a learned filter.

**Implemented for review — 2026-11-03.** The instructor requested “Section 3 and then Section 4”. The [sixteen Section 3 slides](presentation.html#day-2-s3-section) follow the reviewed 30-minute sequence, including a five-minute interactive inspection in the HTML. They use lettered DNA, aligned channel tracks, a moving window and activation stems. The notebook’s additional guided cells remain proposed. Rebuild with `python tools/build_day2_sequence_slides.py 3`; speaking/pointing/transition text comes from this section. Numerical construction and canonical-source details are in Notes; [QA](../qa.md#day-2-sections-34--2026-11-03) records local checks.

**Teaching thread:** Keep the short sequence `ACCGTCCG` visible as it becomes a 4×8 one-hot array, enters a three-position detector and produces the six-position map `(0, 1, 0, 0, 0, 1)`. The detector assigns weight 1 to C/C/G in its three columns, zero elsewhere, bias −2 and ReLU. This deliberate exact-match construction explains the operation; it is not the primary PPM or a trained course filter. Reuse the familiar weighted-sum → activation calculation rather than introduce convolution as an unrelated black box.

**Scope and delivery:** Explain local feature extraction here. Pooling, flattening and the final sequence classifier remain Section 4; full training remains Section 5. The implemented HTML carries the complete interactive inspection without setup. The existing [Days 2–3 notebook](../../notebooks/03_representations.ipynb) contains canonical definitions; optional guided notebook follow-along remains planned. No homework, model training or scored exercise is required in this section.

### S3-01 · Read the sequence in place

**Proposed slide ID:** `day-2-s3-section` · **Time:** 60:00–60:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** Our network needs numbers. This time we will preserve the order of the DNA rather than collapse it into counts.

**Point / reveal:** Resume from Section 2’s closing question about what numbers should enter the model. Use the same quiet section-title treatment.

**Transition:** What goes wrong if we simply number the four bases?

### S3-02 · How should we encode a base?

**Proposed slide ID:** `day-2-s3-encoding-choice` · **Time:** 60:15–61:30 (1:15)

**What is on slide:** The letters A/C/G/T appear above positions 0/1/2/3 on a number line. Highlight the imposed distance from A to C versus A to T.

**What I want to say:** If a model treats these IDs as ordinary scalar values, it receives an ordering and distances we invented. That is not a useful default statement about base similarity. One-hot channels avoid this particular assumption. Integer IDs used to look up learned embeddings have a different role; save that representation discussion for Day 3.

**Point / reveal:** Show the two unequal distances, then return attention to the letters. Do not turn this into a taxonomy of every possible encoding.

**Transition:** Give each possible base its own indicator instead.

### S3-03 · One base, four channels

**Proposed slide ID:** `day-2-s3-one-base` · **Time:** 61:30–63:00 (1:30)

**What is on slide:** One large base letter beside four labeled A/C/G/T tracks. Select A, then C, G and T; a single indicator moves to the matching row, with its four-number column visible.

**What I want to say:** In A/C/G/T order, A is `(1,0,0,0)`, C is `(0,1,0,0)`, G is `(0,0,1,0)` and T is `(0,0,0,1)`. Exactly one channel is active for each known base. The four entries indicate which base we observed; they are not model probabilities or the A/B classes we predict. One-hot encoding itself learns no parameters.

**Point / reveal:** Change only the selected base and its column. Keep row labels fixed and visible; color is supplementary.

**Transition:** Put those columns beside one another in sequence order.

### S3-04 · Keep columns in sequence order

**Proposed slide ID:** `day-2-s3-sequence-matrix` · **Time:** 63:00–64:30 (1:30)

**What is on slide:** `A C C G T C C G` sits directly above its four channel tracks. Reveal the first few columns, then the complete 4×8 array. Mark positions 0–7 along the horizontal axis.

**What I want to say:** A row is a base channel; a column is a sequence position. The sequence order survives. Our eight-base example is 4×8; a full course sequence is 4×160, and a batch is batch×4×160. The implementation supplies channels before positions. These shapes describe the input, not a new predictive feature such as sample ID or class label.

**Point / reveal:** Follow the first A downward, then one C, then move horizontally across the columns. Keep the batch dimension in Notes until needed in the practical.

**Transition:** A neuron could read this entire array. What if we let it read just a small neighborhood?

### S3-05 · Give a neuron a local window

**Proposed slide ID:** `day-2-s3-local-window` · **Time:** 64:30–66:30 (2:00)

**What is on slide:** An outlined window encloses all four channels across the first three positions, `ACC`. Short weighted connections from those twelve entries meet a familiar sum-and-activation neuron; the remaining columns are muted.

**What I want to say:** This is the same weighted sum, bias and activation as before, now applied to a local piece of positional DNA. Width three means three adjacent positions, with all four base channels available. The window therefore contains twelve input entries, even though only three are active. Locality is an architecture choice. The real first convolution uses width seven; three makes the arithmetic visible.

**Point / reveal:** Outline the positions first, then all four channel rows. Avoid suggesting that the detector reads only one base channel at a time.

**Transition:** Which weights would make this neuron respond to CCG?

### S3-06 · A filter holds the local weights

**Proposed slide ID:** `day-2-s3-filter` · **Time:** 66:30–68:00 (1:30)

**What is on slide:** A 4×3 filter aligned to the channel tracks. Reveal a weight 1 at C in column 1, C in column 2 and G in column 3; other entries are zero. Place bias −2 beside the sum, followed by ReLU.

**What I want to say:** A filter is a set of weights, not a DNA string that the computer literally searches for. These particular weights reward C/C/G at the three local positions. The bias sets a response threshold for this construction. Unlike a PPM, filter columns need not sum to one and trained weights can be negative. We chose these simple weights to explain the mechanism; a fitted filter is not restricted to exact matching.

**Point / reveal:** Keep the A/C/G/T row order identical to the input. Use column positions within the filter, distinct from the sequence-start coordinate.

**Transition:** Align the filter with a CCG window and do the familiar calculation.

### S3-07 · Score one matching window

**Proposed slide ID:** `day-2-s3-score` · **Time:** 68:00–70:00 (2:00)

**What is on slide:** Move to the CCG window starting at position 1. Highlight the three nonzero products, then reveal `1+1+1−2=1`, followed by `ReLU(1)=1` and a single activation stem.

**What I want to say:** Multiply corresponding input entries and filter weights, sum them, add the bias, then apply ReLU. There are twelve products, but nine are zero here. The local score is 1 and the activation is 1. This output is a feature value, not the probability that the whole sequence belongs to B. General learned activations can exceed one.

**Point / reveal:** Reveal multiplication, sum/bias and activation in separate steps. Keep the CCG letters, selected columns and output stem aligned throughout.

**Transition:** What does the same filter do on a different window?

### S3-08 · ReLU turns this nonmatch off

**Proposed slide ID:** `day-2-s3-nonmatch` · **Time:** 70:00–71:30 (1:30)

**What is on slide:** Return the unchanged filter to `ACC`, starting at position 0. Its contributions become `0+1+0−2=−1`; the existing ReLU curve maps that score to zero.

**What I want to say:** Only the middle preferred base matches in this window. The score is −1 and the activation is zero. A two-position match would score zero and also produce zero with our chosen bias. That exact-match behavior follows from these deliberately chosen weights; a learned convolution can respond smoothly to a family of related patterns.

**Point / reveal:** Keep the filter weights visibly fixed while changing only the input entries and arithmetic. Point to the activation operation before replacing a negative score with zero.

**Transition:** Now repeat this one computation at every valid start.

### S3-09 · Move the window, reuse the weights

**Proposed slide ID:** `day-2-s3-move-window` · **Time:** 71:30–73:30 (2:00)

**What is on slide:** The same outlined filter moves across `ACCGTCCG` one position at a time. A small weight display stays stationary; a score marker moves with the window.

**What I want to say:** The input window changes while the filter’s weights and bias are shared across positions. We do not learn a separate CCG detector for each coordinate. This repeated local calculation is the convolutional operation. PyTorch uses the cross-correlation convention without reversing the filter; keep that terminology detail in Notes. Here the step between windows, or stride, is one.

**Point / reveal:** Advance through starts 0–5 with a Next window control in the eventual build. Leave the weights fixed on screen to make sharing visible.

**Transition:** Keep each activation at the position where it was produced.

### S3-10 · The detector leaves an activation map

**Proposed slide ID:** `day-2-s3-activation-map` · **Time:** 73:30–75:00 (1:30)

**What is on slide:** The six activations grow into a position-labeled stem plot under the DNA: `0,1,0,0,0,1`. Mark the two responding CCG windows and their zero-based starts 1 and 5.

**What I want to say:** One filter produces one feature map along the sequence. In this unpadded example, eight bases and width three give six valid windows: `8−3+1=6`. The horizontal map coordinate is the window’s start, not a class label. Calling this an activation map or feature map does not make it a complete explanation of a final prediction.

**Point / reveal:** Connect each stem to its window rather than to one arbitrarily chosen base. Keep position labels visible and use the same 0–5 convention throughout the miniature example.

**Transition:** If we move a pattern, what should happen to this local map?

### S3-11 · A moved pattern moves its response

**Proposed slide ID:** `day-2-s3-sharing` · **Time:** 75:00–77:00 (2:00)

**What is on slide:** Extend the strip with quiet flanking letters: `ACCGTCCGAAAA` above `AACCGTCCGAAA`. Highlight that both CCG sites moved one position to the right; the responding stems move from starts 1/5 to 2/6 under the same filter.

**What I want to say:** Shared weights apply the same local rule at another location. In this interior example, moving the sites moves the local responses. That is different from saying that the final sequence probability must remain unchanged: the later prediction head may use position. Padding and boundaries also matter. Keep pooling and the location-handling choice for Section 4.

**Point / reveal:** Move the letters and stems together; keep the filter unchanged. The extra flanking A bases keep both demonstrated sites inside valid windows, avoiding a cropped-site comparison.

**Transition:** We can use the same idea to produce several different local features.

### S3-12 · Several filters, several maps

**Proposed slide ID:** `day-2-s3-many-filters` · **Time:** 77:00–79:00 (2:00)

**What is on slide:** Return to `ACCGTCCG`. Reveal three separate filter/map tracks, using the same constructed rule for CCG, GTC and TCC. Keep filter labels beside their own maps.

**What I want to say:** Different filters have different parameter sets, but each set is shared over positions. Each produces one output channel. The three illustrative filters show different responses to the same input; the real first layer has sixteen learned output channels. Four input base channels and sixteen output feature channels play different roles. A channel is not guaranteed to represent a particular TF or a distinct biological mechanism.

**Point / reveal:** Reveal one new track at a time. In the eventual figure, align all maps to the same six starts: CCG peaks at 1/5, GTC at 3 and TCC at 4.

**Transition:** In practice, who chooses these filter values?

### S3-13 · The labels teach the filters

**Proposed slide ID:** `day-2-s3-learned-filters` · **Time:** 79:00–81:00 (2:00)

**What is on slide:** A local filter and its map connect forward toward a sequence output. A training label appears at the loss; a backward sensitivity trace reaches the filter’s weights, echoing Section 2.

**What I want to say:** The hand-built detector made the calculation easy to inspect. The real network starts from initialized weights and learns useful filters through the classification loss. A shared weight’s gradient combines contributions from its uses across positions and examples in the minibatch. Training supplies sequence class labels, not motif coordinates or the simulator’s PPM as target features. Learned responses may track useful sequence preferences, background effects or shortcuts.

**Point / reveal:** Reveal the label at the output side, then the backward trace to the filter. Do not animate a known CCG string or PPM being copied into the learned weights, or claim a fitted result without a run.

**Transition:** A later convolution can read these maps rather than the raw base channels.

### S3-14 · Build features from nearby features

**Proposed slide ID:** `day-2-s3-two-layers` · **Time:** 81:00–83:00 (2:00)

**What is on slide:** Several first-layer feature tracks feed one local second-layer window spanning five adjacent positions and all input feature channels. Underneath, highlight the corresponding eleven-position interval of an extended DNA strip.

**What I want to say:** The second layer combines nearby first-layer features, not just one isolated track. In our model, widths seven then five, with stride one and no dilation, give a nominal interior receptive field of eleven DNA positions: `7+(5−1)=11`. Five neighboring seven-base windows overlap; this is not seven times five. The second layer still produces sixteen channels. This is not a guaranteed fifteen-base motif detector; the later dense head can combine evidence from across the sequence.

**Point / reveal:** Show the overlap between the first and last contributing seven-base windows. Extend the short strip only to illustrate the eleven-position span; do not squeeze that span onto the eight-base toy input.

**Transition:** Our toy map had six positions. Why does the actual model retain 160?

### S3-15 · What happens at the sequence ends?

**Proposed slide ID:** `day-2-s3-padding` · **Time:** 83:00–85:00 (2:00)

**What is on slide:** The same eight-base array is shown first with complete width-three windows only, then with one ghost column on each side. The output count changes from six to eight. Label the ghost columns “zeros”, not a new base letter.

**What I want to say:** Without padding, only fully contained windows are evaluated. With one zero column on each side and stride one, this width-three example returns eight outputs. A padding column has zero in every channel; it is not an observed A, C, G or T. The actual layers use width seven/padding three and width five/padding two, so both preserve length 160. Edge responses use some artificial context. The miniature map uses window-start coordinates; the symmetrically padded maps align to sequence-position centers.

**Point / reveal:** Show an edge window containing padding, then an interior window. Keep exact output-length formulas in Notes; focus on what information the edge detector receives.

**Transition:** We can now inspect the input array and the detector response directly.

### S3-16 · See the matrix and the map

**Proposed slide ID:** `day-2-s3-notebook` · **Time:** 85:00–90:00 (5:00)

**What is on slide:** The same lettered sequence, one-hot tracks and map, with Change third base and Reset controls. Change C to T: `ACCGTCCG → ACTGTCCG`. Compare the local response before and after; the working notebook is linked from this story for optional code inspection.

**What I want to say:** Use the five-minute inspection in this slide: identify the axes, inspect the constructed detector output, change one base and compare. The original map is `(0,1,0,0,0,1)`; the changed map is `(0,0,0,0,0,1)`. The first CCG response disappears and the second remains. At most three width-three windows can include this changed interior base; not every affected window must change its post-ReLU activation. We have changed one teaching input, not retrained weights or changed the primary dataset. Ask what the audience notices, then stop before the full training workflow. The corresponding guided notebook cells remain planned, so the slide is the complete current activity.

**Point / reveal:** Allow roughly one minute to locate the input/map, one to identify axes, two to change the base and compare, and one to discuss/return. The slide controls require no notebook setup; use Reset to repeat the comparison.

**Transition:** We have local feature maps. Section 4 asks how to turn them into one sequence prediction.

**Construction notes for the eventual build:** A/C/G/T input rows for `ACCGTCCG` are `10000000`, `01100110`, `00010001`, `00001000`. The CCG filter rows are `(0,0,0)`, `(1,1,0)`, `(0,0,1)`, `(0,0,0)`; bias −2. At starts 0–5, windows are ACC/CCG/CGT/GTC/TCC/CCG, scores before ReLU are `−1,1,−1,−2,−1,1`, and activations are `0,1,0,0,0,1`. The GTC and TCC demonstration filters use the same one-at-preferred-base rule and bias, giving maps `0,0,0,1,0,0` and `0,0,0,0,1,0` respectively. These weights are chosen constructions, not biological measurements or learned parameters.

For the one-base change at zero-based position 2, affected starts are 0/1/2. The new first three windows are ACT/CTG/TGT; their scores are −1/0/−2. Only the activation at start 1 changes. The two extended shift examples have ten valid windows with responding starts 1/5 and 2/6; the extra flanks preserve both CCG sites. Symmetric zero padding of width one gives eight toy outputs; actual widths/padding 7/3 then 5/2 preserve 160 positions. For an interior second-layer output, five adjacent first-layer centers span eleven distinct input positions. All exact toy figures should be reproducible without a model fit.

**Source and implementation boundary:** [one_hot and SequenceCNN](../../course_code/course_inference.py) establish A/C/G/T channel order, batch×4×length input, stride-one convolutions, sixteen channels and actual widths/padding. The existing [notebook](../../notebooks/03_representations.ipynb) embeds those definitions, but the short detector visualization, mutation controls and lesson stop are proposed additions to its generation source, not existing cells. Keep them within that notebook rather than create another practical. No `run_representations()` call, model search or test scoring is needed for this checkpoint. If short on time, omit extra filter examples and numerical receptive-field detail before cutting the main one-hot/window/map progression or the guided input change.

<a id="section-4"></a>

## 4. From local features to a sequence prediction · 90–115

**Story question:** How does a set of position-wise responses become one sequence probability?

**Exit understanding:** Compute global maxima per channel; explain which spatial information flattening preserves; trace the model’s two branches into its dense prediction head; distinguish feature activations, a logit, a probability and a class call.

**Implemented for review — 2026-11-03.** The [fourteen Section 4 slides](presentation.html#day-2-s4-section) follow the reviewed 25-minute sequence, then the separate 115–125 break. Aligned response stems, labeled feature ribbons, circular neurons and staged branch reveals carry forward the illustrated style. Controls compare maxima, flatten channel rows, move a peak through position-specific weights, join both branches and trace the actual architecture. Rebuild after Section 3 with `python tools/build_day2_sequence_slides.py 4`; speaking/pointing/transition text comes from this section. [QA](../qa.md#day-2-sections-34--2026-11-03) records local checks and limits.

**Teaching thread:** Start with Section 3’s `ACCGTCCG` and its constructed CCG map `(0,1,0,0,0,1)`. Add the GTC and TCC tracks only when multiple channels are needed. Compare a strongest-response summary with the complete ordered values, then combine both as the actual course architecture does. The small maps illustrate readout operations; they are not outputs from a fitted course CNN.

**Scope and delivery:** This section explains the architecture and what information reaches the classifier. It does not run a training comparison or add a second notebook activity immediately after Section 3. Implemented controls operate on constructed maps in the slides; full notebook training and actual predictions remain Section 5. Technical shapes belong in Notes or a single staged reveal, not persistent subtitles.

### S4-01 · Make one prediction from the maps

**Proposed slide ID:** `day-2-s4-section` · **Time:** 90:00–90:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** Local maps can tell us where detectors respond. Our task still needs one probability per complete sequence.

**Point / reveal:** Resume from Section 3’s final map without reteaching the detector. Hold the section title briefly before the readout question.

**Transition:** We have a response at several positions. What should the classifier receive?

### S4-02 · Many positions, one output

**Proposed slide ID:** `day-2-s4-readout` · **Time:** 90:15–91:30 (1:15)

**What is on slide:** The six CCG response stems remain aligned with the lettered DNA. A single output circle labeled `p(B)` waits to the right, connected through a question mark.

**What I want to say:** These six numbers are local features, not six class probabilities. With multiple filters we have several such tracks. The prediction head is the part that combines features into the sequence-level output. Choosing what it receives affects the distinctions it can learn; saying “CNN” alone does not specify this step.

**Point / reveal:** Point along the positions, then to the single pending sequence output. Leave the connecting operation unresolved for the next slide.

**Transition:** One option is to keep only the strongest response in a track.

### S4-03 · Keep the strongest response

**Proposed slide ID:** `day-2-s4-global-max` · **Time:** 91:30–93:30 (2:00)

**What is on slide:** Sweep across the six response stems. Highlight both tied peaks, then collect the value `1` in a single output marker labeled “Global max”.

**What I want to say:** Global max pooling takes the maximum over all positions in one feature map. Here the result is 1, even though two positions reach it. It does not add the responses, count matches or average them. The returned value retains the strongest activation, while its coordinate and the rest of the track are absent from that value. “Global” means the whole position axis of this map.

**Point / reveal:** Keep both peaks highlighted until the single value appears. Do not draw an argmax coordinate or a count alongside the result unless explicitly discussing what was discarded.

**Transition:** With several filters, which axis do we reduce?

### S4-04 · Keep one maximum for each channel

**Proposed slide ID:** `day-2-s4-pool-channels` · **Time:** 93:30–95:00 (1:30)

**What is on slide:** Reveal the three CCG/GTC/TCC tracks from Section 3. Each track feeds its own maximum; the result is a three-value column `(1,1,1)`, with channel labels attached.

**What I want to say:** Pool across positions separately for each channel. We preserve which detector produced each strongest response; we do not take one maximum across every channel and position together. Three demonstration channels give three values. The actual second convolution has sixteen channels, so its global-max branch gives sixteen values per sequence.

**Point / reveal:** Follow one row to its value, then reveal the other rows. Keep the channel ordering fixed so the pooled column remains interpretable.

**Transition:** What happens if the response moves but its height stays the same?

### S4-05 · Moving a peak can leave the summary unchanged

**Proposed slide ID:** `day-2-s4-pooling-limit` · **Time:** 95:00–97:00 (2:00)

**What is on slide:** Move the first CCG activation from start 1 to start 2: `(0,1,0,0,0,1)` becomes `(0,0,1,0,0,1)`. Its maximum remains 1; the other tracks stay fixed. An optional reveal removes one tied peak and the maximum still remains 1.

**What I want to say:** These maps produce the same pooled vector. A deterministic classifier receiving only that identical vector cannot distinguish the two cases. The maximum also does not tell us whether one or several positions reached it. This is a map-level construction, not a claimed DNA mutation experiment. It does not prove that every globally pooled CNN loses every order relation: earlier contextual features, boundaries and padding can already encode some positional or relational cues.

**Point / reveal:** Let the stem move while the pooled marker remains stationary. Keep the other channel summaries visible but quiet, making their unchanged values clear.

**Transition:** What if we keep the response values in their original slots instead?

### S4-06 · Keep the responses in their slots

**Proposed slide ID:** `day-2-s4-flatten` · **Time:** 97:00–99:00 (2:00)

**What is on slide:** The three-by-six map gently unrolls into one feature ribbon. Retain small channel/position labels; reveal one whole channel row at a time, in CCG/GTC/TCC order.

**What I want to say:** Flattening changes shape, preserving the ordered entries. Our three tracks of six positions become eighteen values. The classifier can give a different weight to each channel-position slot. The array has no printed coordinate feature, but its fixed ordering makes location available. This generally gives the dense head more input weights than a pooled-only readout and can support reliance on fixed coordinates. No convolution or learned transformation happens during the reshape itself.

**Point / reveal:** Track one activation into its exact ribbon coordinate. Move the earlier peak and show that a different ribbon coordinate now holds the 1. Keep channel labels attached rather than merging all channels without boundaries.

**Transition:** How could a later neuron use that difference in slot?

### S4-07 · A neuron can weight locations differently

**Proposed slide ID:** `day-2-s4-position-weights` · **Time:** 99:00–100:30 (1:30)

**What is on slide:** Highlight the first track’s six ribbon slots feeding one hidden neuron. The two map cases give different weighted sums and ReLU outputs, while the pooled maximum remains the same.

**What I want to say:** The convolution shares its weights over positions; the dense head is free to use different weights for different slots. A useful distinction can therefore survive flattening and affect a hidden feature. This demonstrates what is representable, not what training necessarily learns. For this constructed neuron, use weights `(0,1.2,−0.4,0,0,0.3)` and bias −0.5: the original map gives score 1 and activation 1; the moved map gives score −0.6 and activation 0. These are hidden features, not class probabilities.

**Point / reveal:** Highlight the two location-specific coefficients as the stem moves. Put the complete coefficient row and substitution in Notes; reveal the sums only after the positional change is understood.

**Transition:** The supplied course model gives its head both the ordered map and the strongest-response summary.

### S4-08 · Use both branches in our model

**Proposed slide ID:** `day-2-s4-two-branches` · **Time:** 100:30–102:30 (2:00)

**What is on slide:** One stack of maps feeds a gently curving fork. The upper ribbon holds all flattened entries; the lower ribbon holds one maximum per channel. Join their ends into a single labeled feature ribbon.

**What I want to say:** This is one model with two readout branches, not two separately trained CNNs. Concatenation appends the maximum values after the flattened entries; it does not average or add the branches. The toy map gives eighteen flattened values plus three maxima, totaling twenty-one. The actual map gives 2560 plus sixteen, totaling 2576. The maxima are already computable from the complete map, so this branch adds an explicit summary rather than recovering information absent from flattening. Whether that choice helps requires evaluation.

**Point / reveal:** Reveal flattening, then pooling, then concatenation. Preserve the same channel colors/labels and the branch boundary in the joined ribbon.

**Transition:** What calculation consumes this joined feature vector?

### S4-09 · The head combines the sequence features

**Proposed slide ID:** `day-2-s4-dense-head` · **Time:** 102:30–104:00 (1:30)

**What is on slide:** The joined ribbon feeds a few representative circular hidden neurons, labeled as a 32-unit layer, followed by one output neuron marked `z`. Keep detailed dimensions in Notes.

**What I want to say:** We return to Section 1’s familiar mechanism: each hidden unit takes a weighted sum and bias, then ReLU. Here the inputs are the learned sequence features, and the supplied model has thirty-two hidden units. A final learned weighted sum produces one logit. Hidden units can combine evidence across distant slots because the flattened features from the whole sequence are available. The convolutional receptive field of eleven bases does not limit the complete classifier to an eleven-base input interval.

**Point / reveal:** Trace one connection into one hidden unit, then reveal the remaining layer and output. Use representative nodes rather than thirty-two densely drawn circles.

**Transition:** We already know how to turn that final score into a class probability.

### S4-10 · A logit becomes a probability

**Proposed slide ID:** `day-2-s4-output-probability` · **Time:** 104:00–105:30 (1:30)

**What is on slide:** Move the final scalar onto the familiar sigmoid curve. Reuse `z=0.3 → p(B)≈0.574`, then reveal a separate 0.5 decision marker and the class call B.

**What I want to say:** The architecture changed how we obtain features, but this final binary conversion is familiar. During inference we apply sigmoid once to the output logit; threshold 0.5 gives the course class call. During training, the logits-based cross-entropy handles the sigmoid relationship internally, so do not sigmoid before supplying its input. The 0.3 example is the earlier teaching construction, not a newly measured CNN prediction. A probability estimate is also distinct from a biological conclusion or guaranteed calibration.

**Point / reveal:** Reveal score, probability and class call in that order. Keep the threshold as a decision marker rather than another trainable network layer.

**Transition:** Now put the complete model together, using only operations we have already explained.

### S4-11 · Trace the complete route

**Proposed slide ID:** `day-2-s4-architecture` · **Time:** 105:30–107:30 (2:00)

**What is on slide:** One progressive illustration: lettered DNA → one-hot tracks → two local filter/map stages → the flatten/global-max fork → joined ribbon → hidden neurons → logit and sigmoid. Keep the already familiar fork and neuron positions stable.

**What I want to say:** Follow one sequence all the way through. Its input is 4×160; each convolution produces 16×160 after ReLU. The two branches give 2560 and sixteen values; concatenation gives 2576; the head gives thirty-two hidden activations and one logit. Include the batch dimension in Notes. The actual convolutions use widths seven and five, padding three and two, stride one; they do not shorten the position axis or include an intervening local-pooling layer.

**Point / reveal:** First trace the route without dimensions. Then reveal one shape at a time beside the active stage, avoiding an all-at-once wall of labels.

**Transition:** Which operations have parameters that training can change?

### S4-12 · Which parts are learned?

**Proposed slide ID:** `day-2-s4-learned-fixed` · **Time:** 107:30–109:00 (1:30)

**What is on slide:** Keep the complete route fixed. Highlight trainable convolution and dense weights/biases using both color and small parameter markers; leave encoding, ReLU, flattening, max pooling, concatenation and sigmoid in the neutral style.

**What I want to say:** Training fits convolution and dense parameters. The other operations follow fixed rules, although gradients flow through the computation to earlier weights. Pooling and flattening do not have their own fitted weights in this model. Choosing the encoding, architecture and training settings remains our responsibility. More trainable parameters do not guarantee a better validation result.

**Point / reveal:** Select each trainable stage in turn, then show them together. Refer back to Section 2’s backward trace rather than repeat its derivation.

**Transition:** What should we infer if one of the learned maps responds strongly to a sequence pattern?

### S4-13 · A detector is not automatically a motif

**Proposed slide ID:** `day-2-s4-motif-connection` · **Time:** 109:00–111:00 (2:00)

**What is on slide:** A probability-motif illustration and a scoring-filter illustration sit separately above a local response map, connected by a question mark. Label them “Base probabilities” and “Scoring weights”; use symbolic weights rather than claim a newly fitted filter.

**What I want to say:** The primary PPM defines base probabilities by site position; a convolution filter contains scoring weights and a bias. They have different meanings, lengths and constraints. Filter values can be negative and need not sum to one. A response map shows part of a fitted computation, not which biological mechanism generated the sequence or the complete contribution to the prediction. Inspect actual fitted responses and controlled changes before making interpretation claims; real TF binding requires biological evidence beyond this simulation.

**Point / reveal:** Compare what the entries mean, not whether two heatmaps look similar. Keep the primary PPM distinct from Section 3’s designed CCG detector.

**Transition:** Whether we retain or summarize position should depend on the question we want the model to answer.

### S4-14 · Would you keep the location?

**Proposed slide ID:** `day-2-s4-discussion` · **Time:** 111:00–115:00 (4:00)

**What is on slide:** Open discussion: “When might a pattern’s location matter? When would you want to ignore it?”

**What I want to say:** Invite biological examples, questions or modeling preferences without a marked answer. Discuss whether coordinates are aligned to a meaningful reference, what should survive a shift and how a different sampling setup might change that choice. Pooling emphasizes a strongest response; flattening leaves spatial distinctions available to the head. Neither is an automatic scientific winner. In the primary simulation, planting starts are uniform over valid positions for either class, so do not assume a fixed class-specific coordinate. Any benefit from this head must be evaluated. We now understand the architecture and can ask what it actually learns on the declared data.

**Point / reveal:** Reuse the movable map and two readout ribbons if they help the conversation. Participants can predict what a pooled value or flattened slot would do before any code runs. Keep the entire discussion inside these four minutes; no new notebook startup is required.

**Transition:** Take ten minutes, then run and inspect the actual workflow in Section 5.

**Construction notes for the eventual build:** The three demonstration map rows are CCG `(0,1,0,0,0,1)`, GTC `(0,0,0,1,0,0)` and TCC `(0,0,0,0,1,0)`. Pooling over positions gives `(1,1,1)`. Flatten in channel-major order, keeping all six CCG entries, then GTC, then TCC: eighteen entries. Appending the three maxima gives twenty-one. The moved-map comparison changes only the CCG row to `(0,0,1,0,0,1)` at the map level; no claim is made that a corresponding DNA edit leaves the other learned channels unchanged. Removing one tied maximum also preserves the pooled value.

For the single hidden-neuron illustration, apply weights `(0,1.2,−0.4,0,0,0.3)` to the CCG row and bias −0.5; all other feature coefficients are zero for this construction. The original row gives `1.2+0.3−0.5=1.0 → ReLU=1`; the moved row gives `−0.4+0.3−0.5=−0.6 → ReLU=0`. This demonstrates positional sensitivity in an available feature, not an observed training result or a full toy CNN forward pass. The later `z=0.3 → sigmoid(z)=0.5744425` example reuses the familiar output conversion independently; it is not derived from these six positional weights.

**Source and implementation boundary:** [SequenceCNN.forward and predict_cnn](../../course_code/course_inference.py) define the actual branches and output convention. For batch size N, input `(N,4,160)` becomes `(N,16,160)`, then flatten `(N,2560)` and `amax(dim=2)` `(N,16)`, concatenated along feature dimension 1 as `(N,2576)`. Dense/ReLU gives `(N,32)`; the final linear layer gives `(N,1)` and squeeze gives logits `(N,)`; inference sigmoid gives probabilities `(N,)`. Actual flattening preserves channel-major position order. The two branches share the same convolutional features and training loss. No architecture change, ablation, model fitting, notebook edit or test scoring is part of this spec. If short on time, omit numerical positional-weight substitution and optional dimension labels before cutting the pooling/flattening comparison, actual two-branch route or discussion.

### Break · 115–125

**What is on slide:** Only “Break · 10 minutes”.

**What I want to say:** Return in ten minutes. The break is separate from teaching allocations.

<a id="section-5"></a>

## 5. Train, inspect and compare · 125–155

**Story question:** What did this fitted CNN learn on the same classification problem?

**Exit understanding:** Connect the supplied training run to its loss history, selected weights and validation predictions; compare methods on matching data without assuming a winner.

**Implemented for review — 2026-11-03:** [fourteen slides](presentation.html#day-2-s5-section), 30 minutes. Rebuild with `python tools/build_day2_evaluation_slides.py`; empirical figures are bound to the [current local run](../../instructor/verification/day2-current.json). The practical includes four minutes for first notebook access/setup and five for computation. These are allocations requiring rehearsal. Use DNA strands, curves, response stems and probability dots rather than a sequence of box diagrams. Only the small configuration excerpt needs code. Plot the current run when available; the current local run is available for the revised primary PPM dataset. Actual Colab execution remains unverified.

### S5-01 · Train the sequence model

**Proposed slide ID:** `day-2-s5-section` · **Time:** 125:00–125:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** We have built the mechanism. Now follow a working model from training to a prediction and ask what it achieved.

**Point / reveal:** Pause on the title; no architecture recap panel.

**Transition:** What task are these weights learning?

### S5-02 · Back to our sequence task

**Proposed slide ID:** `day-2-s5-task` · **Time:** 125:15–126:45 (1:30)

**What is on slide:** Two lettered DNA strands, labels A/B and a small variable-site motif logo; one probability axis labeled p(B).

**What I want to say:** Return to the primary simulation: 160-base sequences, independently sampled 15-base PPM sites at random positions, planted with probability 0.95 for B and 0.05 for A. Neither label guarantees site presence or absence. There are 1,200 records; 720 train and 240 validation, with 240 test rows reserved. Today the CNN receives the letters through one-hot encoding. IDs and simulator truth remain metadata.

**Point / reveal:** Highlight the changing site letters and location, then the target probability.

**Transition:** Compare models on these same examples.

### S5-03 · Keep the comparison fair

**Proposed slide ID:** `day-2-s5-comparison` · **Time:** 126:45–128:00 (1:15)

**What is on slide:** The same DNA strand feeds count tallies for logistic regression/forest and positional channels for the CNN; all predictions align to one validation-row ruler.

**What I want to say:** Stage 03 refits all three methods on the same primary training rows and evaluates the same 240 validation IDs. Each classical vocabulary is learned on training only. Representation and predictor change together, so this is a workflow comparison, not a claim to isolate one architectural ingredient. Use ROC-AUC and AP; any displayed class calls use the declared 0.5 threshold.

**Point / reveal:** Keep row identities aligned as the two representations appear.

**Transition:** Open the single working notebook.

### S5-04 · Open the working notebook

**Proposed slide ID:** `day-2-s5-open-notebook` · **Time:** 128:00–132:00 (4:00)

**What is on slide:** One GitHub/Colab link or QR for the [combined notebook](../../notebooks/03_representations.ipynb), with a short route: setup → definitions → Day 2 checkpoint.

**What I want to say:** This is our first notebook startup today; Section 3 ran inside the slides. Open the GitHub ipynb in Colab, run setup and the required definitions. Access, downloads and a possible restart belong inside this allocation, not homework. Instructor demonstration is a complete route; following along is optional. The existing notebook contains Days 2–3, so do not use Run all. Guided checkpoints and the explicit Day 2 stop are included in the generated notebook.

**Point / reveal:** Demonstrate the exact selected-cell route, then return attention to the lesson.

**Transition:** Check the input, output and settings before starting.

### S5-05 · What will this run fit?

**Proposed slide ID:** `day-2-s5-configuration` · **Time:** 132:00–134:00 (2:00)

**What is on slide:** A one-hot strand labeled N×4×160 feeds one logit per sequence; alongside it, a compact actual configuration excerpt: Adam 0.002, batch 64, 24 epochs.

**What I want to say:** A/C/G/T are the four channels. The actual network uses 16 width-seven filters, then 16 width-five filters, both with ReLU and length-preserving padding. Flattened features and global maxima feed the 32-unit head and one logit. Training uses binary cross-entropy with logits; inference applies sigmoid once. This supplied CPU workflow uses two threads. Read the declared settings rather than inviting a parameter search. The run includes both primary and order-control variants; we will inspect the control in Section 6.

**Point / reveal:** Trace input to logit, then reveal sigmoid for inference; keep the full architecture in notes.

**Transition:** Let the supplied workflow learn the weights.

### S5-06 · Run the supplied workflow

**Proposed slide ID:** `day-2-s5-run` · **Time:** 134:00–139:00 (5:00)

**What is on slide:** One run cell and an honest running/completed status. While waiting, a light animation reconnects forward pass → loss → update.

**What I want to say:** Run stage 03 once in the normal course_output workspace with seed 2026 and 24 epochs. It fits both variants and all three methods; this five-minute allocation covers that complete call. Initially display only primary outputs. The current runner prints both variants even with show_plot=False, so the teaching cell captures its output and reads back the primary result. Do not rerun for a preferred ranking. If setup or computation overruns, switch to a compatible saved run and identify it as previous execution; if none exists, discuss the mechanism and leave the comparison pending.

**Point / reveal:** Identify the current execution state without manufacturing live progress or estimated timings.

**Transition:** What changed during those updates?

### S5-07 · Read the training loss

**Proposed slide ID:** `day-2-s5-history` · **Time:** 139:00–140:45 (1:45)

**What is on slide:** One large actual training-loss curve, with epoch on the horizontal axis and loss on the vertical axis.

**What I want to say:** Load models/simple/cnn_history.csv from this run. Lower loss means better fit to the training targets under this objective. Each epoch value averages minibatch losses measured as weights are updated, not a full-training-set evaluation at one fixed set of weights. Describe the observed curve, whether smooth, noisy or flat; do not insert a textbook overfitting shape as experimental evidence.

**Point / reveal:** Trace the actual first-to-last history; label both axes before discussing its shape.

**Transition:** Does the model also rank unseen validation examples usefully?

### S5-08 · Watch validation separately

**Proposed slide ID:** `day-2-s5-validation-history` · **Time:** 140:45–142:30 (1:45)

**What is on slide:** One actual validation ROC-AUC curve over the same 24 epochs, on its own labeled scale.

**What I want to say:** These labels do not contribute gradients, but their scores guide checkpoint selection. This is a different quantity from loss; there is no reason its numerical values or trajectory should match the training curve. Describe only what this run supports. Training continuing to improve while validation stalls would motivate investigation, but do not diagnose overfitting from an invented shape.

**Point / reveal:** Locate the observed best epoch without yet replacing the model by the final epoch.

**Transition:** Which weights do we retain?

### S5-09 · Keep the selected weights

**Proposed slide ID:** `day-2-s5-checkpoint` · **Time:** 142:30–144:00 (1:30)

**What is on slide:** The same validation curve with its earliest highest point marked; the selected weights feed a single prediction.

**What I want to say:** All 24 epochs run; this is not early stopping. Keep the highest validation ROC-AUC checkpoint, taking the earliest epoch in a tie. The saved cnn.pt holds weights and sequence length, not the selected epoch: derive that epoch from the earliest history maximum and verify that the reloaded model reproduces the saved probabilities. Validation selection makes these development results. Test results never guide this choice; the frozen comparison belongs on Day 3.

**Point / reveal:** Distinguish the final point from the selected point if they differ.

**Transition:** Use those fixed weights on one sequence.

### S5-10 · One sequence, one probability

**Proposed slide ID:** `day-2-s5-one-prediction` · **Time:** 144:00–147:00 (3:00)

**What is on slide:** One validation sequence ID and strand, its actual p(B) on a 0–1 axis, then its observed A/B label. A row selector is the only proposed control.

**What I want to say:** Start with the first validation row in saved order, rather than hand-picking a success. Reload the selected checkpoint, use evaluation/inference mode and apply sigmoid once. Join predictions and labels by sample ID. Reveal the label after the probability and discuss agreement or disagreement. Change the inspected row without refitting. An individual error and an individual success are both examples, not an estimate of general performance; probability output also does not establish calibration.

**Point / reveal:** Sequence → fixed model → probability → observed label; keep the 0.5 class-call marker secondary.

**Transition:** What happens inside the local detector stage for this same row?

### S5-11 · Inspect one response map

**Proposed slide ID:** `day-2-s5-response-map` · **Time:** 147:00–148:45 (1:45)

**What is on slide:** The same strand above one second-convolution post-ReLU channel, shown as activation stems against position. Default channel 0; an optional channel selector.

**What I want to say:** The guided readback helper extracts the 16×160 response map from the reloaded checkpoint. These cells are implemented and locally executed. Peaks show where that channel responds. They are neither a complete attribution nor evidence that the model discovered TF binding. Begin with channel 0 and disclose any changed channel, avoiding a search for a motif-looking success. Keep the same validation row and fitted weights; simulator truth is not an input to this calculation.

**Point / reveal:** Align strand positions with activation stems; describe the response actually observed, including weak or diffuse responses.

**Transition:** Move from one example to the whole validation set.

### S5-12 · Compare validation behavior

**Proposed slide ID:** `day-2-s5-results` · **Time:** 148:45–150:45 (2:00)

**What is on slide:** A single three-method dot plot; toggle ROC-AUC/AP while retaining method order and a labeled scale. Use blue, orange and purple plus method names/marker shapes.

**What I want to say:** Populate from this run's representation_validation.csv and aligned predictions for the primary variant. ROC-AUC asks about ranking across classes; AP emphasizes precision as positives are retrieved. Neither uses the 0.5 threshold. Confirm the same 240 validation IDs before comparing. Current Day 1 classical scores are context, not a substitute for matched stage 03 outputs. The current local CNN ROC-AUC/AP are 0.546528/0.555691; old fixed-motif scores do not enter this chart. A single split and seed do not establish a universal winner or statistical superiority.

**Point / reveal:** Show one metric at a time; let the actual ranking stand even if the CNN trails.

**Transition:** Performance is only one part of choosing a workflow.

### S5-13 · What did the computation buy?

**Proposed slide ID:** `day-2-s5-tradeoffs` · **Time:** 150:45–152:45 (2:00)

**What is on slide:** The three representations illustrated as counts or ordered strands, beside the observed performance and one clearly scoped runtime annotation; no invented per-model speed bars.

**What I want to say:** Consider predictive behavior, setup, computation, label availability and interpretation together. representation_run.json records aggregate elapsed seconds per variant, covering classical and CNN work; it does not measure CNN-only time or each method separately. Name device and scope if displaying it. These CPU observations cannot promise a Colab runtime or measure biological value. The CNN offers learned local features and positional readout, but this evidence decides whether those helped here.

**Point / reveal:** Connect each model to the representation it actually received; show timing only with its scope.

**Transition:** What experiment would make the result easier to understand?

### S5-14 · What would you investigate next?

**Proposed slide ID:** `day-2-s5-checkpoint-discussion` · **Time:** 152:45–155:00 (2:15)

**What is on slide:** One open prompt: “What would help you understand this result?”

**What I want to say:** Invite observations from the actual curves, predictions and comparison, without testing recall. More labeled examples or a controlled representation comparison may help. Separate proposed experiments from observed results and avoid a settings search aimed at making the CNN win. Next we isolate a distinction that no count-based predictor could recover, regardless of fitting effort.

**Point / reveal:** Leave the prompt alone while the audience discusses; keep suggestions in notes.

**Transition:** Same ingredients, different arrangement.

<a id="section-6"></a>

## 6. What the representation makes possible · 155–180

**Story question:** Can a more powerful predictor recover information that was discarded?

**Exit understanding:** Explain why paired equal bags force equal predictions, distinguish retained information from successful learning, and connect today's learned features to Day 3 reuse.

**Implemented for review — 2026-11-03:** [fourteen slides](presentation.html#day-2-s6-section), 25 minutes, including a five-minute notebook inspection and an open closing discussion. Carry one paired DNA illustration through swaps, counting, positional maps and predictions. This is a separate controlled variant, not a new interpretation of the primary PPM experiment. Construction gives a mathematical bag-model limit; actual CNN behavior requires current outputs.

### S6-01 · Same counts, different arrangement

**Proposed slide ID:** `day-2-s6-section` · **Time:** 155:00–155:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** Use a small controlled experiment to separate what information is available from what a model learns to use.

**Point / reveal:** Pause before showing the constructed pair.

**Transition:** Start with two related sequences.

### S6-02 · Swap the blocks

**Proposed slide ID:** `day-2-s6-pair` · **Time:** 155:15–157:00 (1:45)

**What is on slide:** Two 160-base DNA ribbons share the same background. Blue TATAAATG and orange CGGACGTC exchange two fixed slots; label B has the first order, A the reverse. Letters and labels distinguish the blocks beyond color.

**What I want to say:** Disclose the rule: B/1 has TATAAATG then CGGACGTC; A/0 has the reverse. These are fixed eight-base strings, deliberately distinct from the primary variable 15-base PPM sites. Each background produces an opposite-label pair. There are 240 groups/480 sequences; group splits are 144/48/48, or 288/96/96 rows. Partners always stay in the same split. Do not imply unrelated real biological classes.

**Point / reveal:** Animate the two blocks exchanging slots while the rest of the background stays fixed.

**Transition:** Will every short-word count really remain unchanged?

### S6-03 · The boundaries count too

**Proposed slide ID:** `day-2-s6-flanks` · **Time:** 157:00–158:45 (1:45)

**What is on slide:** Zoom into the matching wrapper GGGGGG + motif + CCCCCC. A four-letter window crosses each internal and outer boundary.

**What I want to say:** Swapping bare motifs could change boundary-spanning words. Here both blocks use the same six-base left/right flanks, so the outer boundary words remain unchanged. Each complete motif-containing block occurs once in both partners. Block starts are 32 and 80, motif starts 38 and 86, all zero-based; the blocks do not overlap. This construction preserves the entire overlapping 4-mer bag, not just a few selected counts.

**Point / reveal:** Slide one window across a motif/flank boundary and another across a block/background boundary.

**Transition:** Count all the windows, including these boundaries.

### S6-04 · Different strands, identical bags

**Proposed slide ID:** `day-2-s6-equal-bags` · **Time:** 158:45–160:15 (1:30)

**What is on slide:** The two strands become matching count profiles with a large equality sign. A reveal reads “all 4-mers,” rather than listing 256 columns.

**What I want to say:** A length-160 sequence has 157 overlapping four-base windows. Check equality using complete Counters before a training-fitted vocabulary removes any unseen words. This rules out a hidden count difference outside the few columns displayed on a slide. Both classical models then receive identical feature vectors for the partners.

**Point / reveal:** Align the two profiles; distinguish a full equality check from a three-feature visual excerpt.

**Transition:** What can a fitted model do with identical inputs?

### S6-05 · Same input, same prediction

**Proposed slide ID:** `day-2-s6-same-score` · **Time:** 160:15–161:45 (1:30)

**What is on slide:** One shared count profile feeds two identical probability markers, one labeled A and one B. One small expression: x₁=x₂ ⇒ f(x₁)=f(x₂).

**What I want to say:** Any fixed deterministic predictor acting only on this vector must give equal scores. More trees, a nonlinear count-based neural network or more training cannot restore the lost distinction. Across groups, scores may vary; within each opposite-label pair they must match. Sample IDs, labels and group metadata must not become extra predictive features.

**Point / reveal:** Keep the model unchanged as the partner label changes.

**Transition:** What does this imply for the whole balanced validation set?

### S6-06 · Why ranking stays at chance

**Proposed slide ID:** `day-2-s6-chance` · **Time:** 161:45–163:15 (1:30)

**What is on slide:** A small score-distribution illustration: each A dot has a B partner at the identical probability, then the two class distributions overlay. A single annotation: ROC-AUC = 0.5.

**What I want to say:** Every validation group contributes one label of each class with the same score. Therefore the complete score distributions match and ROC-AUC is exactly 0.5, including ties under the standard definition. This is a consequence of the construction, not a failure to tune enough. The dot illustration explains the argument; it is not a measured CNN output. The conclusion assumes complete opposite-label pairs and a predictor using only the equal bag representation.

**Point / reveal:** Reveal one dot's opposite-label partner, then all partners; avoid a second metric lecture.

**Transition:** Did the original ordered input also lose the distinction?

### S6-07 · Position makes the inputs different

**Proposed slide ID:** `day-2-s6-position-input` · **Time:** 163:15–165:00 (1:45)

**What is on slide:** The paired strands become four labeled one-hot tracks, with differences at the two motif slots highlighted.

**What I want to say:** Ordered one-hot input retains which bases occupy each position, so the two sequences are distinct inputs. The model has an available signal. That does not guarantee optimization finds a useful rule or that it will generalize beyond this construction. Avoid translating “can distinguish” into an invented performance claim.

**Point / reveal:** Keep position coordinates aligned while toggling between partners.

**Transition:** Which part of our network can use those locations?

### S6-08 · The prediction head matters

**Proposed slide ID:** `day-2-s6-position-head` · **Time:** 165:00–166:30 (1:30)

**What is on slide:** Matching local response peaks exchange positions; one view keeps their slots, another retains only each channel's maximum.

**What I want to say:** Reconnect to Section 4. Our width-seven then width-five convolutions have an eleven-base receptive field. They cannot jointly span these distant motifs. With matching wrappers, the local feature multiset is unchanged, so global maxima alone lose this particular fixed-slot cue. The actual network also flattens position-indexed features, allowing its head to use the distinction. This argument concerns this architecture/construction, not every pooled CNN. Response peaks are schematic here; actual maps require inference.

**Point / reveal:** Toggle preserved slots versus maxima; hold filter identities fixed.

**Transition:** Now inspect what the actual fitted methods did.

### S6-09 · Read the two experiments together

**Proposed slide ID:** `day-2-s6-paired-results` · **Time:** 166:30–168:30 (2:00)

**What is on slide:** One matched-method ROC-AUC comparison with a primary/control toggle. Keep method order, labeled markers and scale stable; mark the control's mathematical bag limit at 0.5.

**What I want to say:** Read both variants from the same current stage 03 run, which already fitted the control. The primary validation set has 240 records, the control 96; these are different questions, not a pooled score. Check observed bag scores against the expected chance limit and report the actual CNN score whether strong or weak. This current local run gives bag ROC-AUC/AP 0.5/0.5 and CNN 1.0/1.0 on the control; this remains one engineered fixed-slot experiment. If no compatible current output exists, show the proven bag limit and leave the empirical comparison pending; do not insert the old primary chart or promise a CNN victory.

**Point / reveal:** Reveal the construction-based expectation before the observed control points; distinguish their sources in notes.

**Transition:** Inspect the two predictions behind one of those pairs.

### S6-10 · Compare one pair in the notebook

**Proposed slide ID:** `day-2-s6-notebook` · **Time:** 168:30–173:30 (5:00)

**What is on slide:** One selected validation pair: strands → complete count equality → three methods' paired probabilities. A group selector is the only proposed control.

**What I want to say:** Use the first validation group in artifact order, with an optional different group; no new fitting. The guided cells join models/interaction/controlled_order_changes.csv to validation sequences by sample/group ID, assert two opposite labels, verify complete Counter equality, then display each method's two probabilities. Check bag-model equality with rtol=0 and atol=1e-12 for these saved float64 probabilities. If the check fails, investigate alignment/construction rather than explain it as neural learning. A CNN difference describes this fitted control model; its size or absence is observed evidence. Keep test rows out of the readback. These guided cells are implemented and locally executed; cross-file float32 CNN probabilities are checked at atol=1e-6, while bag equality remains atol=1e-12.

**Point / reveal:** Confirm the pair and equality before revealing predictions. Stop here rather than running stage 04 embeddings.

**Transition:** What if the blocks move beyond the two familiar slots?

### S6-11 · Would it work somewhere else?

**Proposed slide ID:** `day-2-s6-new-position` · **Time:** 173:30–175:00 (1:30)

**What is on slide:** Ghost marks show the old slots while the blocks move to unfamiliar positions; the output is a question mark.

**What I want to say:** This is a hypothetical next experiment, not another run promised today. Fixed-slot success does not establish arbitrary order, spacing, strand or regulatory grammar. Moving the blocks changes the data distribution and can expose positional reliance. Decide what invariances the intended biological task needs before changing construction or claiming generalization.

**Point / reveal:** Move the blocks without assigning a probability or success/failure label.

**Transition:** Representation choices express what distinctions we retain.

### S6-12 · Available information, learned use

**Proposed slide ID:** `day-2-s6-synthesis` · **Time:** 175:00–176:30 (1:30)

**What is on slide:** One DNA strand becomes count tallies, ordered base tracks and learned activation stems; a small eye marker highlights what each retains.

**What I want to say:** Counts retain short-word composition; positional inputs retain locations; learned local features transform the input, and their readout can retain or discard locations. A representation makes information available, fitting determines how it is used, and evaluation measures whether that helped for the task. Counts remain a useful inexpensive choice when the discarded distinctions are unnecessary. Greater model complexity cannot recover an absent distinction.

**Point / reveal:** Reveal the three representations one at a time; keep the biological task constant.

**Transition:** Which distinctions matter for the audience's own data?

### S6-13 · What would you keep for your data?

**Proposed slide ID:** `day-2-s6-discussion` · **Time:** 176:30–179:15 (2:45)

**What is on slide:** One audience prompt: “What information would you want your model to keep?”

**What I want to say:** Invite examples involving composition, location, alignment or interactions. Ask how labels, sample size and computational budget affect a useful representation. This is a conversation about participants' problems, not a test or submission. Keep suggested next experiments separate from today's demonstrated findings, and use this allocation for closing questions.

**Point / reveal:** Leave the prompt on screen; no answer list or busy takeaway panel.

**Transition:** Today we fitted features from our own labeled examples. Must we always start there?

### S6-14 · Can we borrow learned features?

**Proposed slide ID:** `day-2-s6-tomorrow` · **Time:** 179:15–180:00 (0:45)

**What is on slide:** A learned feature pattern moves from a larger collection of sequences onto our small task; Day 3 is highlighted.

**What I want to say:** Tomorrow we use a pretrained sequence model as a feature source and evaluate those features on our task. Pretraining can change what a representation captures; it does not guarantee improvement. Keep attention, contextual embeddings and the frozen test comparison for Day 3. End Day 2 before stage 04 in the combined notebook.

**Point / reveal:** Transfer the feature pattern; avoid starting a transformer architecture diagram.

**Transition:** Day 3: reuse representations, then assess the frozen workflows.

<a id="notebook-plan"></a>

## Notebook plan

Use the existing [03_representations.ipynb](../../notebooks/03_representations.ipynb), which also carries Day 3 stages. The [notebook guide](../../notebooks/README.md) owns access, setup and saved-work instructions. Do not add another overlapping notebook. Day 2 teaching cells are maintained in [day2_teaching.py](../../tools/day2_teaching.py), generated by [build_course.py](../../tools/build_course.py), and source/hash checked by [check_notebooks.py](../../tools/check_notebooks.py).

| Checkpoint | Student/instructor action | Current state |
| --- | --- | --- |
| Section 2 | Trace one weight change, distinguish minibatch/epoch, then follow the five-statement forward/loss/backward/update excerpt. | Implemented as slide illustrations and an interactive code highlight; canonical training code exists. No setup or training run required here. |
| Section 3 | Inspect one-hot axes and the constructed CCG map; change the third base from C to T and compare local responses. | Complete interactive slide activity implemented; one-hot notebook definitions exist, while additional guided detector/mutation cells and a lesson stop remain planned. |
| Section 4 | Compare pooling/flattening on the same constructed maps; trace both branches into the sequence head. | Slide controls and discussion implemented; no additional notebook startup or training activity. |
| Section 5 | Four-minute access/setup, inspect settings, run stage 03 once, then read primary loss/validation curves, selected checkpoint, one prediction/map and matched method metrics. | Implemented and locally executed: output capture, compatible-run reuse, identity/row checks, history/checkpoint readback, row/channel inspection and metrics. |
| Section 6 | Five-minute inspection of the first validation pair: verify identities/opposite labels and complete count equality, then reveal all three methods’ paired probabilities. | Implemented and locally executed: all 48 validation pairs checked, then the selected pair displayed without refitting. |
| End of Day 2 | Stop before stage 04 embeddings and stage 05 freeze. | Explicit stop added before stage 04; “Run all” still crosses day boundaries, so follow selected cells. |

**Opening and compute:** The current Section 3 checkpoint runs directly in the slides. Section 5 therefore includes the first notebook startup in its proposed four-minute opening allocation. A later guided notebook version of Section 3 would need to budget first access/setup within its activity and make Section 5 a return/check. No route assumes setup homework. Rehearse setup in the actual Colab runtime: installs, restarts and model training can overrun their allocations. Optional follow-along may become instructor demonstration without removing the conceptual walkthrough.

**Execution boundary:** The existing `run_representations()` call fits both variants and all three methods, and writes all their development results at once. Section 5 initially displays primary outputs; Section 6 reads the already-produced paired control. The runner prints both variants even with show_plot=False; the teaching cell captures that output before revealing only the primary artifacts. A compatible completed run is read again without refitting; incomplete or mismatched existing artifacts are rejected. Splitting their *presentation* does not imply separate completed runs. Keep one normal artifact directory for continuity into Day 3. No new runner, artifact copy or configuration search is needed merely to teach this sequence.

**Fallback:** Use one clearly identified, source-bound current run if live training fails or is slow. Display the dataset/settings identity and validation split, and distinguish previous execution from activity in the current classroom. The existing historical fixed-motif output is not a valid fallback for the new primary PPM comparison. If no compatible current CNN run exists, show the mechanism and report that the comparison is pending; do not fabricate a result. Shorten optional parameter-count details, extra base changes and architecture explorations before cutting the core inference/evaluation discussion.

<a id="evidence-and-scope"></a>

## Evidence and scope

### Dataset and evaluation continuity

- **Primary task:** the current [generator](../../course_code/course_core.py) uses a 15-position strictly positive PPM, independently sampled sites planted at a random valid location with probability 0.95 for B and 0.05 for A. Default labels are balanced; there are 1,200 sequences of length 160, with 720/240/240 training/validation/test rows. Use exactly this task for the primary Day 2 comparison. Do not revert to a single fixed word or present planting as deterministic label membership.
- **Order control:** `build_interaction_dataset()` deliberately remains separate: 240 paired groups, 480 sequences, with 144/48/48 groups (288/96/96 rows) across splits. Both partners stay together. Two fixed motifs and shared flanks guarantee equal 4-mer count vectors under the stated construction. This illustrates an information limit, not general biological grammar or universal superiority of CNNs.
- **Evaluation:** use the same IDs, labels and split within each variant, fitting vocabulary/model parameters on training only. ROC-AUC is primary, AP supports interpretation, and the class-call threshold remains 0.5. Validation selects the CNN checkpoint; test is never development feedback. The planned frozen test comparison remains on Day 3, following [ADR 0002](../../docs/adr/0002-validation-for-development-protected-test-comparison.md).
- **Scope of biology:** preserve [ADR 0001](../../docs/adr/0001-controlled-sequence-classification.md). This is controlled simulated sequence classification. Learned filters, validation behavior and counterfactual sensitivity are not evidence of real TF binding or regulatory causality.

### Sources for the eventual slide build

- [Original teaching intent](../teaching-outline.md#day-2): neuron → loss/optimization → one-hot DNA → convolution → position-aware architecture → comparison/control. This proposal expands that progression into focused slides and reduces repeated loss teaching now that Day 1 includes it.
- [Canonical training workflow](../../course_code/03_representations.py): Adam 0.002, minibatches 64, 24 CPU epochs, highest validation ROC-AUC checkpoint with earliest tie. [Shared inference](../../course_code/course_inference.py): A/C/G/T channels, convolution widths 7 and 5 with 16 channels and ReLU, flatten/global-max concatenation, 32-unit hidden head, one logit.
- [MALTAomics review](../../.scratch/ml-bioinformatics-course/maltaomics-source-review.md): the historical deep-learning lesson’s local detector and progressive one-hot/filter-map figures are useful teaching precedents. The instructor’s supplied transformer slides are a style/progression reference for nonlinearity and hidden layers; attention and contextual embeddings remain Day 3 material. Rebuild native figures in the approved style; retain attribution if source figures are reused.
- [Representation verification](../../instructor/verification/representations.md): documents the construction, architecture and earlier runs. Its primary 0.802/0.907/0.564 ROC-AUC values belong to the old fixed-motif generator and must not populate this revised primary chart. Its times and interaction scores are historical observations, not new classroom measurements.
- [Current Day 1 record](../../instructor/verification/day1-current.json): validation logistic ROC-AUC/AP 0.608333/0.607054 and forest 0.611875/0.597040 on the revised PPM dataset. This is current classical evidence, not a current CNN run or a substitute for matched stage 03 identities and artifacts.

### Implemented notebook readback contract for Sections 5–6

Keep lesson helpers in the existing notebook-generation source and regenerate the same combined notebook; do not copy scientific implementations or create a second practical. Read representation_run.json and generation.json identities before displaying results. Join saved validation predictions by variant/method/sample ID, checking exactly the matching validation rows and labels. Use the normal course_output directory for continuity into Day 3.

- **Primary history and checkpoint:** read models/simple/cnn_history.csv; derive the earliest maximum-validation epoch. Reload cnn.pt using the canonical architecture and check inference against representation_validation_predictions.csv with an explicitly documented float32 tolerance (rtol=0, atol=1e-6). The checkpoint itself does not store the epoch. Extract post-ReLU second-layer maps in evaluation/inference mode without refitting; defaults are the first validation row and channel 0.
- **Metrics and runtime:** read representation_validation.csv and reproduce ROC-AUC/AP from aligned probabilities. Record runtime as aggregate per variant from representation_run.json, not per method. No new measured neural ranking or runtime is established by this specification.
- **Paired inspection:** read models/interaction/controlled_order_changes.csv and join only validation sequences. Check complete overlapping 4-mer Counters, pair membership, opposite labels and within-pair bag-probability equality (rtol=0, atol=1e-12). Explain the exact ROC-AUC 0.5 consequence independently of the CNN result. Select alternate groups without training again.
- **Teaching boundary:** initially capture the full stage 03 output, display primary first, then read the already-generated control. Include the conspicuous end-Day-2 stop before stage 04/05; do not reveal or score test results. The notebook is generated and locally verified; publication and actual Colab execution remain pending.

### Verification and remaining rehearsal

Stage 03 was locally executed with the current generator, without a parameter search. The current record binds source/configuration identities, training history, selected epochs, aligned validation predictions, paired-bag equality, metrics and aggregate runtime. Guided cells and the Day 2 stop are generated and checked against their source; offline slide layout, interactions, navigation, notes, export and printing are verified in QA. Hosted Colab execution, timed classroom pacing and projector readability still require their own checks.

**All six sections are implemented for review.** The final build preserves the first 58 records (Sections 1–4 and both breaks) exactly and replaces six legacy scenes with the 28 reviewed Section 5–6 slides. All current anchors resolve; old source hashes redirect to corresponding concepts. Other-day HTML, scientific source, original annotations, glossary and ADRs are preserved. The generated Day 2 notebook was locally executed using training/validation only; no protected test scoring, commit or push occurred.

**Sections 5–6 specification update — 2026-11-03:** expanded to fourteen proposed slides each, retaining 30/25 minutes and the full-day 160 teaching + 20 break minutes. Every new beat specifies visible content, speaking notes, a pointing/reveal cue and a transition. This update changes planning only; HTML, notebook/source bytes, Sections 1–4 slide specifications and other-day stories are preserved. No training, notebook execution, protected test scoring, commit or push is part of this update.

**Sections 5–6 implementation — 2026-11-03:** notebook inspection cells and all 28 slides are built. The [current run](../../instructor/verification/day2-current.json) records seed2026/CPU2threads/24epochs, selected epochs 2 (primary) and 1 (control), complete validation-pair checks and source/artifact fingerprints. Primary logistic/forest/CNN ROC-AUC is 0.608333/0.611875/0.546528; control 0.5/0.5/1.0. The comparison was not tuned to change that ordering. Setup, hosted Colab behavior, timed pacing and projector review remain unverified; see [QA](../qa.md#day-2-sections-56--2026-11-03). This supersedes the earlier specification-only status above.
