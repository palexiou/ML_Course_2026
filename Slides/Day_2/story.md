# Day 2 story

**Sections 1–2 implemented for review — 2026-11-03; Sections 3–6 remain discussion drafts.** The instructor authorized both builds after reviewing their breakdowns, carrying forward the request for illustrations with less reliance on boxes. The [opening](presentation.html#day-2-s1-welcome) has twelve slides; the [learning section](presentation.html#day-2-s2-section) has fourteen slides followed by the 50–60 break. The ten later HTML scenes retain their earlier content, timings and historical benchmark values; the retained one-hot scene follows the new break. This 37-scene mixed review deck does not implement the complete timetable below or establish classroom readiness. Section titles, emphasis and pacing remain editable.

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

**160 teaching minutes + 20 break minutes = 180 minutes.** There are 74 content beats (26 implemented across Sections 1–2, the remainder proposed) and two separate break slides. All timings are suggested allocations, not measured pacing. This proposal keeps Day 1’s section rhythm and moves the old Day 2 second break from 100–110 to 115–125; the retained later HTML still uses the old second-break timing. It replaces the earlier thirty-minute closing catch-all with explicit synthesis and discussion. The [historical guide](../../instructor/guide.md) and [annotated outline](../teaching-outline.md#day-2) remain unchanged; this timetable is for instructor review.

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

**Discussion spec — expanded 2026-11-03.** Sixteen proposed slides across 30 minutes, including a five-minute guided inspection. This expands the earlier thirteen-beat outline; the new Section 3 HTML and notebook checkpoint are not implemented. Keep Sections 1–2’s short titles, generous space and illustrative style. Use lettered DNA, aligned channel tracks, a moving window and growing activation stems. A matrix is appropriate when explaining an array; repeated enclosing boxes are unnecessary.

**Teaching thread:** Keep the short sequence `ACCGTCCG` visible as it becomes a 4×8 one-hot array, enters a three-position detector and produces the six-position map `(0, 1, 0, 0, 0, 1)`. The detector assigns weight 1 to C/C/G in its three columns, zero elsewhere, bias −2 and ReLU. This deliberate exact-match construction explains the operation; it is not the primary PPM or a trained course filter. Reuse the familiar weighted-sum → activation calculation rather than introduce convolution as an unrelated black box.

**Scope and delivery:** Explain local feature extraction here. Pooling, flattening and the final sequence classifier remain Section 4; full training remains Section 5. The inspection can be instructor-led with optional follow-along in the existing [Days 2–3 notebook](../../notebooks/03_representations.ipynb). Slides must also carry the complete tiny example if access/setup is slow. No homework, model training or scored exercise is required in this section.

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

**What is on slide:** A compact link to the existing notebook and the same lettered sequence, one-hot tracks and map. Change the third base from C to T: `ACCGTCCG → ACTGTCCG`. Highlight the nearby windows and compare the two maps.

**What I want to say:** Proposed five-minute guided cells: inspect the axes, run the constructed detector once, change one base and compare. The original map is `(0,1,0,0,0,1)`; the changed map is `(0,0,0,0,0,1)`. The first CCG response disappears and the second remains. At most three width-three windows can include this changed interior base; not every affected window must change its post-ReLU activation. We have changed one teaching input, not retrained weights or changed the primary dataset. Ask what the audience notices, then stop before the full training workflow.

**Point / reveal:** Allow roughly one minute to open/locate the checkpoint, one to run and identify axes, two to change the base and compare, and one to discuss/return. If setup consumes the allocation, use the complete slide example. No participant setup is assumed before class.

**Transition:** We have local feature maps. Section 4 asks how to turn them into one sequence prediction.

**Construction notes for the eventual build:** A/C/G/T input rows for `ACCGTCCG` are `10000000`, `01100110`, `00010001`, `00001000`. The CCG filter rows are `(0,0,0)`, `(1,1,0)`, `(0,0,1)`, `(0,0,0)`; bias −2. At starts 0–5, windows are ACC/CCG/CGT/GTC/TCC/CCG, scores before ReLU are `−1,1,−1,−2,−1,1`, and activations are `0,1,0,0,0,1`. The GTC and TCC demonstration filters use the same one-at-preferred-base rule and bias, giving maps `0,0,0,1,0,0` and `0,0,0,0,1,0` respectively. These weights are chosen constructions, not biological measurements or learned parameters.

For the one-base change at zero-based position 2, affected starts are 0/1/2. The new first three windows are ACT/CTG/TGT; their scores are −1/0/−2. Only the activation at start 1 changes. The two extended shift examples have ten valid windows with responding starts 1/5 and 2/6; the extra flanks preserve both CCG sites. Symmetric zero padding of width one gives eight toy outputs; actual widths/padding 7/3 then 5/2 preserve 160 positions. For an interior second-layer output, five adjacent first-layer centers span eleven distinct input positions. All exact toy figures should be reproducible without a model fit.

**Source and implementation boundary:** [one_hot and SequenceCNN](../../course_code/course_inference.py) establish A/C/G/T channel order, batch×4×length input, stride-one convolutions, sixteen channels and actual widths/padding. The existing [notebook](../../notebooks/03_representations.ipynb) embeds those definitions, but the short detector visualization, mutation controls and lesson stop are proposed additions to its generation source, not existing cells. Keep them within that notebook rather than create another practical. No `run_representations()` call, model search or test scoring is needed for this checkpoint. If short on time, omit extra filter examples and numerical receptive-field detail before cutting the main one-hot/window/map progression or the guided input change.

<a id="section-4"></a>

## 4. From local features to a sequence prediction · 90–115

**Story question:** How does a set of position-wise responses become one sequence probability?

**Exit understanding:** Distinguish global max pooling from flattening, trace the actual two-branch architecture, and explain what information its head can use.

### S4-01 · Make one prediction from the maps

**Proposed slide ID:** `day-2-s4-section` · **Time:** 90:00–90:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** Local maps can tell us where detectors respond. Our task still needs one probability per complete sequence.

### S4-02 · Many positions, one output

**Proposed slide ID:** `day-2-s4-readout` · **Time:** 90:15–92:00 (1:45)

**What is on slide:** A single feature map spans the DNA; one p(B) box waits at the right.

**What I want to say:** We must decide how to combine positions and channels. This is an architecture choice with consequences for what the final classifier sees. Convolution alone does not specify that choice.

### S4-03 · Keep the strongest response

**Proposed slide ID:** `day-2-s4-global-max` · **Time:** 92:00–94:30 (2:30)

**What is on slide:** The vector 0,1,0,0,0,1 collapses to its maximum, 1.

**What I want to say:** Global max pooling gives one number per channel, describing the strongest activation anywhere in that map. This loses the location of that maximum, how many tied peaks occurred and the rest of the spatial pattern. It is not local pooling or an average.

### S4-04 · Moving a peak can leave the summary unchanged

**Proposed slide ID:** `day-2-s4-pooling-limit` · **Time:** 94:30–97:00 (2:30)

**What is on slide:** Two constructed maps have their 1 at different positions and the same maximum.

**What I want to say:** The summary is identical for these maps. A classifier receiving only those pooled values cannot distinguish them. This map-level example does not prove that every convolutional architecture with global pooling is blind to every order relation: sufficiently contextual local features can encode relations before pooling.

### S4-05 · Keep the responses in their slots

**Proposed slide ID:** `day-2-s4-flatten` · **Time:** 97:00–99:30 (2:30)

**What is on slide:** A small channel×position map unrolls into a labeled row, preserving order.

**What I want to say:** Flattening changes shape without fitting or pooling. Each channel-position slot gets its own coordinate in the classifier input. This makes location available to the dense head, increases its parameter count, and makes fixed-length positional shortcuts possible.

### S4-06 · Use both summaries in our model

**Proposed slide ID:** `day-2-s4-two-branches` · **Time:** 99:30–102:30 (3:00)

**What is on slide:** One feature map branches into Flatten and Global max; their output rows concatenate.

**What I want to say:** Our existing model keeps the flattened position-bearing map and a strongest-response summary. It does not choose between two separately trained CNNs. We should explain this specific architecture before using its behavior as evidence about position.

### S4-07 · Trace the complete route

**Proposed slide ID:** `day-2-s4-architecture` · **Time:** 102:30–105:00 (2:30)

**What is on slide:** DNA → one-hot → two convolution/ReLU blocks → two branches → dense/ReLU → output.

**What I want to say:** Reveal one operation at a time, with technical sizes in notes. The input is 4×160, maps are 16×160, flattening gives 2560 values, pooling gives 16, concatenation gives 2576, the hidden head gives 32, and the output gives one logit. Padding preserves map length. Show the diagram without every shape label at once.

### S4-08 · A logit becomes a probability

**Proposed slide ID:** `day-2-s4-output-probability` · **Time:** 105:00–107:30 (2:30)

**What is on slide:** The final scalar z passes through sigmoid to p(B), then a separate threshold box appears.

**What I want to say:** The same final operation as Day 1 returns. During training, binary_cross_entropy_with_logits combines sigmoid and cross-entropy numerically; do not sigmoid first and then pass probabilities into that logits-based loss. During inference, apply sigmoid to the output once. Threshold 0.5 turns a score into a class call.

### S4-09 · Which parts are learned?

**Proposed slide ID:** `day-2-s4-learned-fixed` · **Time:** 107:30–109:30 (2:00)

**What is on slide:** The same diagram highlights convolution and dense weights; encoding, ReLU, flattening and pooling stay unhighlighted.

**What I want to say:** Convolution and dense layers have trainable parameters. One-hot encoding, ReLU, flattening, concatenation and max pooling are fixed operations, although gradients pass through the differentiable computation to earlier weights. Choosing the architecture is separate from fitting its parameters.

### S4-10 · A detector is not automatically a motif

**Proposed slide ID:** `day-2-s4-motif-connection` · **Time:** 109:30–112:00 (2:30)

**What is on slide:** A PPM and a learned filter appear separately, connected by a question mark.

**What I want to say:** The primary PPM is a normalized probability distribution at each site position; a convolution filter is a set of learned scoring weights. They have different meanings and need not resemble each other directly. Inspection and controlled changes can provide evidence about a fitted detector; a bright map alone is not TF-binding proof.

### S4-11 · Would you keep the location?

**Proposed slide ID:** `day-2-s4-discussion` · **Time:** 112:00–115:00 (3:00)

**What is on slide:** Open discussion: “When might a pattern’s location matter? When would you want to ignore it?”

**What I want to say:** Invite biological examples and modeling preferences without a marked answer. Connect them to pooling and flattening. Fixed-coordinate learning can be appropriate in an aligned task but fragile under a changed setup. We now know what we will train and what information it can use.

### Break · 115–125

**What is on slide:** Only “Break · 10 minutes”.

**What I want to say:** Return in ten minutes. The break is separate from teaching allocations.

<a id="section-5"></a>

## 5. Train, inspect and compare · 125–155

**Story question:** What did this fitted CNN learn on the same classification problem?

**Exit understanding:** Follow a working training run, read its selected epoch and validation predictions, and compare methods on matching data without assuming a winner.

### S5-01 · Train the sequence model

**Proposed slide ID:** `day-2-s5-section` · **Time:** 125:00–125:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** We have explained the architecture. Now use the working notebook to connect its inputs, training history and predictions.

### S5-02 · Keep the comparison fair

**Proposed slide ID:** `day-2-s5-comparison` · **Time:** 125:15–128:00 (2:45)

**What is on slide:** Logistic regression, forest and CNN share the primary training/validation rows; their representations differ.

**What I want to say:** Use the same primary PPM dataset and split identities, with ROC-AUC and AP and a fixed 0.5 decision threshold. Baselines in this workflow are refitted on its dataset, not imported from an unidentified run. The model and representation change together; the comparison does not isolate every possible architectural effect.

### S5-03 · Open the working notebook

**Proposed slide ID:** `day-2-s5-open-notebook` · **Time:** 128:00–131:00 (3:00)

**What is on slide:** GitHub ipynb → Open in Colab → Day 2 checkpoint, with a compact link or QR.

**What I want to say:** Budget access, setup and selected definitions here, within class time. Use the existing combined notebook rather than a second copy. Its setup can need downloads and a restart; three minutes is a proposed allocation, not a measured promise. Instructor demonstration remains a complete participation route.

### S5-04 · Run the supplied training workflow

**Proposed slide ID:** `day-2-s5-run` · **Time:** 131:00–136:00 (5:00)

**What is on slide:** A minimal run cell beside a live progress/status area; no wall of implementation code.

**What I want to say:** The existing stage 03 workflow fits classical baselines and a CNN on both primary and order-control datasets. Run it once; initially reveal only the primary result. Do not claim the notebook currently stops after each lesson: the proposed inspection cells still need to be added. Keep 24 epochs and the declared settings for the comparison, rather than rerun until a preferred result appears.

### S5-05 · Read what changed during training

**Proposed slide ID:** `day-2-s5-history` · **Time:** 136:00–140:00 (4:00)

**What is on slide:** Actual primary training-loss history and validation-ROC-AUC history in separate panels.

**What I want to say:** Identify the epochs and what each panel measures. Per-epoch training loss averages minibatch losses during updates; it is not a fixed-weight evaluation of the entire training set. Discuss learning, a plateau or instability using the actual run. Never invent a clean overfitting curve and present it as this run.

### S5-06 · Which fitted weights are we using?

**Proposed slide ID:** `day-2-s5-checkpoint` · **Time:** 140:00–143:00 (3:00)

**What is on slide:** The best validation epoch is marked and its checkpoint feeds inference.

**What I want to say:** The code retains the highest validation ROC-AUC epoch, earliest tie. The chosen checkpoint may not be the last epoch. Validation is being used for development, so these results remain development evidence. The protected test remains untouched until the planned Day 3 frozen comparison.

### S5-07 · Compare more than one metric

**Proposed slide ID:** `day-2-s5-results` · **Time:** 143:00–146:00 (3:00)

**What is on slide:** Primary validation ROC-AUC and AP, revealed separately for the three methods.

**What I want to say:** Populate from the newly rehearsed stage 03 output, not the old fixed-motif chart. Confirm the same 240 validation IDs before comparing. Day 1 has current logistic/forest evidence, but not a new CNN result. Read the observed tradeoffs without promising neural improvement or tuning to a preferred ordering.

### S5-08 · Inspect one sequence prediction

**Proposed slide ID:** `day-2-s5-one-prediction` · **Time:** 146:00–149:00 (3:00)

**What is on slide:** One validation ID, predicted p(B), observed label and its labeled feature map.

**What I want to say:** Use the selected checkpoint on a validation sequence. Change the inspected row, not the trained weights. A map shows model response at positions; it is not by itself a complete attribution or a discovered biological mechanism. This inspection need not open simulation truth as a predictive input.

### S5-09 · What did the extra computation buy?

**Proposed slide ID:** `day-2-s5-tradeoffs` · **Time:** 149:00–152:30 (3:30)

**What is on slide:** A small comparison of observed validation behavior, measured runtime and representation.

**What I want to say:** Discuss whether the evidence justifies this model for this task, including setup, sample size and interpretation. Runtime must name the machine and scope; historical CPU timings do not establish Colab timing for the new generator. If a saved verified run is used, label it as previous execution.

### S5-10 · What would you investigate next?

**Proposed slide ID:** `day-2-s5-checkpoint-discussion` · **Time:** 152:30–155:00 (2:30)

**What is on slide:** An open prompt: “What would help you understand this result?”

**What I want to say:** Invite ideas such as more training examples, independent development comparisons or a controlled input change. Separate a scientific next experiment from changing settings until the CNN wins. Transition to a construction where we can reason about the representation before looking at any scores.

<a id="section-6"></a>

## 6. What the representation makes possible · 155–180

**Story question:** Can a more powerful predictor recover information that was discarded?

**Exit understanding:** Explain the equal-bag limit, inspect the position-aware model on paired controls, and connect learned features to Day 3 reuse.

### S6-01 · Same counts, different arrangement

**Proposed slide ID:** `day-2-s6-section` · **Time:** 155:00–155:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** End with a small controlled problem that isolates the information in the representation.

### S6-02 · Swap the blocks, keep the ingredients

**Proposed slide ID:** `day-2-s6-pair` · **Time:** 155:15–157:30 (2:15)

**What is on slide:** One shared DNA background; two highlighted blocks exchange their two fixed positions.

**What I want to say:** This is a separate deliberately engineered dataset variant. It uses two fixed eight-base strings, TATAAATG and CGGACGTC, with matching flanks, not newly sampled primary PPM sites. Positive and negative partners swap their order. Their label rule and construction are disclosed, and partners stay in the same split.

### S6-03 · The boundaries count too

**Proposed slide ID:** `day-2-s6-flanks` · **Time:** 157:30–160:00 (2:30)

**What is on slide:** Each block expands to GGGGGG + motif + CCCCCC; crossing 4-mer windows are highlighted.

**What I want to say:** Simply swapping motifs need not preserve every overlapping word: boundaries matter. Six-base matching flanks make the boundary words identical in this construction, while each complete block appears once in both partners. Block starts are 32 and 80; motif starts are 38 and 86, all zero-based.

### S6-04 · The bag sees exactly the same input

**Proposed slide ID:** `day-2-s6-equal-bags` · **Time:** 160:00–163:00 (3:00)

**What is on slide:** Different DNA strings converge to identical complete 4-mer count rows.

**What I want to say:** Prove the representation limit before empirical results. A deterministic predictor given the same feature vector returns the same score. More trees or a neural network trained on that identical count representation cannot separate the partners. With balanced complete opposite-label pairs, the bag-score distribution is identical by class, giving ROC-AUC 0.5.

### S6-05 · The positional input is different

**Proposed slide ID:** `day-2-s6-position-input` · **Time:** 163:00–165:30 (2:30)

**What is on slide:** One-hot columns differ at the exchanged blocks; the flattened feature slots are highlighted.

**What I want to say:** The position-aware network can use information that counts removed. This establishes an available signal, not guaranteed learning or a universal CNN ranking. Its flattened head matters. Our two-convolution local receptive field is too short to jointly span the distant swapped motifs; a global-max-only head would lose this particular fixed-slot cue.

### S6-06 · Read the two experiments together

**Proposed slide ID:** `day-2-s6-paired-results` · **Time:** 165:30–168:00 (2:30)

**What is on slide:** Two panels, primary PPM and fixed-position control; methods stay in the same order.

**What I want to say:** Use current source-bound validation outputs for both. The historical interaction run was solved by this architecture, but that is not a newly executed result. The bag’s chance limit follows from the checked construction; actual CNN scores come from the new run. The two variants ask different questions and have different sample counts.

### S6-07 · Compare one pair of predictions

**Proposed slide ID:** `day-2-s6-notebook` · **Time:** 168:00–173:00 (5:00)

**What is on slide:** Notebook checkpoint: partner IDs → equal counts → model probabilities for each partner.

**What I want to say:** Inspect a validation pair from stage 03 output; join by sample/group identity and verify opposite labels. Confirm complete Counter equality and compare each model’s response. Both bag-model predictions should match within a declared numeric tolerance. Any CNN difference describes this fitted model on this control. Do not expose test rows or launch a model search.

### S6-08 · Would it work somewhere else?

**Proposed slide ID:** `day-2-s6-new-position` · **Time:** 173:00–175:00 (2:00)

**What is on slide:** The same blocks move to unfamiliar slots, with a question mark over the output.

**What I want to say:** This is a proposed extension, not a result already demonstrated. Fixed-slot success does not establish arbitrary spacing, strand, position or regulatory grammar. A counterfactual outside the training construction can expose reliance on position, but it also changes the input distribution.

### S6-09 · Representation decides what is available

**Proposed slide ID:** `day-2-s6-synthesis` · **Time:** 175:00–177:30 (2:30)

**What is on slide:** Three simple rows: count features, positional one-hot, learned convolution features.

**What I want to say:** Separate what each representation retains from what the fitted model uses. Counts can be an excellent inexpensive choice; a larger predictor cannot recover an omitted distinction. Convolution learns local features; the head determines how their locations are combined. Evaluation decides whether that helps for the intended task.

### S6-10 · What would you choose for your data?

**Proposed slide ID:** `day-2-s6-discussion` · **Time:** 177:30–179:15 (1:45)

**What is on slide:** An open audience discussion prompt, with one quiet reminder of cost and available labels.

**What I want to say:** Invite participants to relate the day to their own data: useful invariances, available labels, alignment and computational budget. Keep this a discussion rather than a quiz. Questions are included in the section’s allocation.

### S6-11 · Can we borrow features already learned?

**Proposed slide ID:** `day-2-s6-tomorrow` · **Time:** 179:15–180:00 (0:45)

**What is on slide:** Train features from scratch → reuse a pretrained encoder, with Day 3 highlighted.

**What I want to say:** Today’s features were learned from our labeled training examples. Tomorrow we ask what happens if a model has already learned from many sequences before our task. Introduce pretraining and reuse without starting the transformer lesson here.

<a id="notebook-plan"></a>

## Notebook plan

Use the existing [03_representations.ipynb](../../notebooks/03_representations.ipynb), which also carries Day 3 stages. The [notebook guide](../../notebooks/README.md) owns access, setup and saved-work instructions. Do not add another overlapping notebook. Proposed Day 2 teaching cells should be maintained in the notebook-generation source, following Day 1’s stop-and-inspect pattern.

| Checkpoint | Student/instructor action | Current state |
| --- | --- | --- |
| Section 2 | Trace one weight change, distinguish minibatch/epoch, then follow the five-statement forward/loss/backward/update excerpt. | Implemented as slide illustrations and an interactive code highlight; canonical training code exists. No setup or training run required here. |
| Section 3 | Inspect one-hot axes and the constructed CCG map; change the third base from C to T and compare local responses. | One-hot definitions exist; guided detector/mutation cells and a lesson stop are proposed, with a complete slide-based route if setup is slow. |
| Section 5 | Setup, run stage 03 once, inspect primary history, selected checkpoint and matched validation predictions. | Complete stage 03 workflow exists; lesson-specific readback and stop cells are proposed. |
| Section 6 | Verify a validation pair’s complete count equality and inspect paired probabilities. | Generator, equality assertion and controlled prediction artifact exist; guided readback cells are proposed. |
| End of Day 2 | Stop before stage 04 embeddings and stage 05 freeze. | The combined notebook needs an explicit teaching stop; “Run all” crosses day boundaries. |

**Opening and compute:** Section 3’s five-minute checkpoint includes opening/setup if it is the first live notebook visit. Section 5’s three-minute opening allocation is then a return/check; if Section 3 is demonstrated statically, Section 5 becomes the first startup. Neither route assumes setup homework. Rehearse setup in the actual Colab runtime: installs, restarts and model training can overrun their allocations. Optional follow-along may become instructor demonstration without removing the conceptual walkthrough.

**Execution boundary:** The existing `run_representations()` call fits both variants and all three methods, and writes all their development results at once. Section 5 initially displays primary outputs; Section 6 reads the already-produced paired control. Splitting their *presentation* does not imply separate completed runs. Keep one normal artifact directory for continuity into Day 3. No new runner, artifact copy or configuration search is needed merely to teach this sequence.

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

### Before implementation is called verified

Rehearse stage 03 with the current generator and record source/configuration identities, training history, selected epoch, row alignment, paired-bag equality, validation metrics and computation scope. No tuning should be performed merely to obtain a preferred ranking. Add guided notebook cells and explicit stops, then check the generated notebook against canonical source. Verify the hand calculations, shape labels and eventual interactive controls offline, plus the normal slide navigation, notes/export/print behavior. Hosted Colab execution, timed classroom pacing and projector readability require their own checks.

**Sections 1–2 are implemented for review.** Sections 3–6 remain proposed; their new slide IDs do not resolve in the retained later HTML scenes. The Section 2 build preserves Section 1’s twelve records and ten later legacy records, replacing the old loss/optimization scenes and putting the new 50–60 break before the retained one-hot scene. Other-day decks, notebooks, scientific code, original annotations, glossary and ADRs are preserved. No training, protected test scoring, commit or push was performed for this slide build.
