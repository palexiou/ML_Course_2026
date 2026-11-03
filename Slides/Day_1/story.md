# Day 1 story

Updated 2026-11-03: **all six Day 1 sections are implemented for review** in the [112-slide presentation](presentation.html). The instructor authorized specifying explainability and then building the remaining slides. The 24 Section 1 and 18 Section 2 records are preserved; Sections 3–6 follow the agreed story and approved blue/orange, low-density style. Two ten-minute breaks remain separate. Timings are editable speaking allocations, not a timed rehearsal. This is the active Day 1 story source; [teaching-outline.md](../teaching-outline.md#day-1) preserves the instructor's original annotations unchanged.

**Sections:** [1 · Introduction](#1-course-and-ml-introduction--025) · [2 · Sequence Regulatory Patterns](#section-2) · [3 · Logistic regression](#3-logistic-regression-on-k-mer-counts--6090) · [4 · Metrics](#4-what-makes-a-prediction-useful--90115) · [5 · Trees](#5-what-changes-with-a-tree-or-forest--125155) · [6 · Explainability](#6-explainability-what-did-the-model-learn--155180) · [Delivery notes](#delivery-and-teaching-source-notes)

The story connects a biological question to numerical features, a learned prediction, useful evaluation, a different model, and an explanation that transfers to new sequences. Teach every concept through explanation and discussion. The instructor agreed to completed notebooks in GitHub opening through Colab. Instructor demonstrations with optional student follow-along remain a **delivery proposal**; the level of hands-on work is open, and scaffolded practicals are retained. Execution is never a prerequisite for answering the checkpoints below.

## Three-hour shape

| Minutes | Section | Teaching minutes |
| --- | --- | --- |
| 0–25 | 1. Course and ML introduction | 25 |
| 25–50 | 2. Sequence Regulatory Patterns | 25 |
| 50–60 | Break | — |
| 60–90 | 3. Logistic regression on k-mer counts | 30 |
| 90–115 | 4. What makes a prediction useful? | 25 |
| 115–125 | Break | — |
| 125–155 | 5. What changes with a tree or forest? | 30 |
| 155–180 | 6. Explainability: what did the model learn? | 25 |

Total: **160 teaching minutes + two 10-minute breaks = 180 minutes**. Questions and any demonstrations fit inside the section allocations; they are not extra activities. This proposal moves the second break from minute 100 to 115 and replaces the earlier dedicated opening startup block with a concept-first opening. The [accepted earlier timetable](../../instructor/guide.md) remains historical authority until the instructor agrees to those changes. If everyone must execute, budget in-class startup explicitly before implementing the slide timings; no pre-course setup or homework is assumed.

## 1. Course and ML introduction · 0–25

**Implemented for instructor review, 2026-11-03:** [actual Day 1 opening](presentation.html#day-1-intro-welcome), 24 slides with detailed SAY, pointing and transition notes. This implements the instructor's latest explicit sequence and supersedes the earlier opening diagnostic/metric-familiarity question and mutually exclusive learning-tree proposal. It does not approve or redesign Sections 2–6.

**Purpose:** Welcome the group, state a concrete goal—understand, use and explain ML for biological data—and make learning from examples intelligible before introducing the DNA working example in Section 2.

**Narrative and rationale:**

1. **Welcome and goal.** Use the actual course title and supplied instructor identity: Panagiotis Alexiou, ERA Chair, University of Malta. The compact course GitHub link and real QR lead to the private repository; access requirements belong in notes. No invented research biography or separate bio slide.
2. **Four successive journey slides.** Keep all four days at identical coordinates, highlighting only one at a time. Day 1: classical ML and explaining a prediction; Day 2: neural representations/CNNs and learning useful features; Day 3: pretrained/foundation embeddings and reuse; Day 4: coding agents and specifying/auditing analyses. Other days remain legible gray. Relative deck links require the neighboring folders when exporting.
3. **What ML means, in three steps.** Learn useful patterns from data; fitting adjusts a model from a learning signal; applying uses the learned model on new input. Outputs can be predictions, representations or generated content. Do not suggest that every learning method needs externally labeled examples or that input during ordinary use updates model weights.
4. **One stable learning example.** Two expression measurements locate constructed cells. Externally supplied state labels illustrate supervised fitting; a fixed separator then predicts a new cell's state. Predicted and observed state are distinguished. Coordinates, labels, separator and new cell are invented teaching values, with provenance in notes, not claimed biological findings. Learning useful patterns must extend beyond remembering fitting examples.
5. **Training signal, then focused tasks.** Introduce supervised external targets, unsupervised structure without task labels, self-supervised targets formed from input, and reinforcement through actions/rewards. Classification and regression are supervised tasks, while clustering is an unsupervised task. Give categories, quantities, unlabeled grouping and compact representations their own visual moments. Representation learning can use several training signals.
6. **Generation and overlap.** Masking a word illustrates self-supervision, often grouped broadly under unsupervised learning. A text generator produces content; conditional image generation shows that external labels/paired conditions can coexist with generative objectives. Next-token language modeling explicitly combines self-supervised training with generative use. Reinforcement learning receives one brief interaction/reward slide; the notes distinguish this training setting from ordinary coding-agent tool use. Finish with common signal–task pairings explicitly described as overlapping, not exclusive. Deep learning, transfer learning and foundation models are overlapping descriptions, acknowledged in notes rather than added as beginner taxonomy siblings. Semi-supervised combinations are briefly acknowledged in notes.
7. **One open audience discussion.** Invite interests, experience and expectations: “Where could learning from data help in your own work? What would you want to understand about its output?” Invite a few voices, listen, connect to the course, and transition to the first DNA example. There is no expected answer, grading, hidden diagnostic, or metric-familiarity test.

**Suggested pacing:** 25 minutes total, including a two-minute closing discussion. Per-slide allocations are in instructor notes only; they are proposed speaking allocations, not measured rehearsal times.

| Slide | Title / stable anchor | Suggested allocation |
| --- | --- | --- |
| 1 | [Machine learning for bioinformatics](presentation.html#day-1-intro-welcome) | 0:45 |
| 2 | [Our goal](presentation.html#day-1-intro-goal) | 0:30 |
| 3 | [Day 1: classical ML](presentation.html#day-1-intro-day-1) | 0:30 |
| 4 | [Day 2: neural representations](presentation.html#day-1-intro-day-2) | 0:30 |
| 5 | [Day 3: pretrained embeddings](presentation.html#day-1-intro-day-3) | 0:30 |
| 6 | [Day 4: coding agents](presentation.html#day-1-intro-day-4) | 0:30 |
| 7 | [What is machine learning?](presentation.html#day-1-intro-what-is-ml) | 1:00 |
| 8 | [Fitting learns from examples](presentation.html#day-1-intro-fit) | 1:00 |
| 9 | [Using applies a learned model](presentation.html#day-1-intro-apply) | 1:00 |
| 10 | [Learn from labeled cells](presentation.html#day-1-intro-cell-examples) | 1:30 |
| 11 | [Apply it to a new cell](presentation.html#day-1-intro-new-cell) | 1:30 |
| 12 | [Where does the training signal come from?](presentation.html#day-1-intro-signals) | 1:00 |
| 13 | [Classification predicts a category](presentation.html#day-1-intro-classification) | 1:00 |
| 14 | [Regression predicts a quantity](presentation.html#day-1-intro-regression) | 1:00 |
| 15 | [Look for structure without task labels](presentation.html#day-1-intro-unsupervised) | 1:00 |
| 16 | [Clustering proposes groups](presentation.html#day-1-intro-clustering) | 1:00 |
| 17 | [Learn a useful representation](presentation.html#day-1-intro-representation) | 1:00 |
| 18 | [Create the target from the input](presentation.html#day-1-intro-self-supervised) | 1:30 |
| 19 | [Generative models produce content](presentation.html#day-1-intro-generation) | 1:15 |
| 20 | [Generation can be guided](presentation.html#day-1-intro-conditional-generation) | 1:00 |
| 21 | [One language model, two descriptions](presentation.html#day-1-intro-next-token) | 1:30 |
| 22 | [Reinforcement learning uses rewards](presentation.html#day-1-intro-reinforcement) | 1:30 |
| 23 | [Describe the signal and the task](presentation.html#day-1-intro-two-lenses) | 1:00 |
| 24 | [What would you like to explore?](presentation.html#day-1-intro-discussion) | 2:00 |

**Conceptual sources:** Original geometric diagrams and teaching examples, informed by [Dive into Deep Learning: introduction](https://d2l.ai/chapter_introduction/index.html), [masked-language pretraining](https://d2l.ai/chapter_natural-language-processing-pretraining/bert.html), [language models / next-token targets](https://d2l.ai/chapter_recurrent-neural-networks/language-model.html), [text generation](https://d2l.ai/chapter_recurrent-neural-networks/rnn-scratch.html), Goodfellow et al., [Deep Learning, ch. 20](https://www.deeplearningbook.org/contents/generative_models.html), Mirza and Osindero, [Conditional Generative Adversarial Nets](https://arxiv.org/abs/1411.1784), and Sutton and Barto, [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html). Source URLs and precise conceptual qualifications are retained in individual notes; no research-folder duplicate was added.

**Integration boundary:** The 24 slides replace the old opening records 1–12. The original first DNA record `day-1-slide-13` is now displayed as slide 25 and retains its stable anchor. This described the original Section 1 checkpoint. The later full Day 1 build replaced the historical remainder; all six sections now follow this story.

<a id="section-2"></a>

## 2. Sequence Regulatory Patterns · 25–50

**Review draft implemented — 2026-11-03.** The instructor authorized continuing Section 2 and implementing the revised sequence. The 18 slides below now exist in the [Day 1 deck](presentation.html#day-1-dna-section); implementation is for review, not approval of every wording or agent recommendation. This is the first DNA example, following Section 1. The new 15-position probability-motif decision supersedes the old fixed `TATAAATG` / 0.9–0.1 primary simulation; scientific code and notebook migration is owned separately and is not established by this slide edit.

**Story question:** How can variable regulatory sequence patterns become numerical inputs for a model that can infer a class on a new sequence?

**Exit understanding:** Distinguish a TF protein, its binding preferences and a motif representation; distinguish position probabilities from log-odds PWM scores; trace overlapping k-mers into a bag with multiplicity and then counts; read ID/count/label roles directly in a table; explain the different purposes of training, validation and test, with no test-guided development; identify fitting versus inference.

**Accepted structural revisions:** Exact splash **Sequence Regulatory Patterns** → three focused biology slides → working simulated task and labeled examples → transparent variable-site simulation → open representation discussion → persistent sequence/windows/bag/counts → pros and cons → concrete table → visible evaluation purposes and emphatic test boundary → brief CV concept → classifier/inference handoff. The instructor's nine feedback numbers referred to the earlier nine-part outline, not the previous fourteen beats. The separate abstract X/y/ID exposition is removed. Each surviving proposed content ID remains stable; new concepts have new IDs to keep old autosaves from overriding them.

**Agent recommendations, for review:** Use a brief conceptual CV slide within the existing allocation, optionally shortened to one sentence if discussion needs the time; retain the course's fixed development/test execution protocol. Defer bootstrap mechanics to Section 5's forest construction (sample training rows **with replacement**), with uncertainty uses later if needed. Teach counts before the model so its input is concrete; introduce logistic regression next as a transparent baseline, while explaining that representation/model choice is joint and iterative. These recommendations are not instructor-confirmed changes to the scientific protocol.

### S2-01 · Sequence Regulatory Patterns

**Slide ID:** `day-1-dna-section` · **Time:** 25:00–25:15 (0:15)

**What is on slide:** Only the exact section title, large and left aligned.

**What I want to say:** This is our first DNA example. We will connect regulatory sequence patterns to a supervised classification task, decide how to represent a sequence, and define what each evaluation partition is for.

**Point / transition:** The section title. First, why might a short DNA pattern matter?

### S2-02 · A protein can recognize a DNA pattern

**Slide ID:** `day-1-dna-motivation` · **Time:** 25:15–26:30 (1:15)

**What is on slide:** One oval labeled TF above a short highlighted DNA region; a nearby gene and transcription arrow. One quiet context sentence.

**What I want to say:** A transcription factor, or TF, is a protein; the motif is a sequence pattern, not the protein. A TF can bind a short DNA region and contribute to regulating transcription. The oval is deliberately a schematic protein. Binding also depends on accessibility, cofactors and cellular conditions. A motif match alone establishes neither binding nor promoter activity, and regulatory sites can occur outside promoters.

**Point / transition:** Oval → short binding site → gene. A TF usually tolerates more than one exact sequence.

### S2-03 · A motif describes binding preferences

**Slide ID:** `day-1-dna-binding-preferences` · **Time:** 26:30–27:45 (1:15)

**What is on slide:** One TF oval points to four aligned, related four-base site excerpts. Varying bases carry one accent color.

**What I want to say:** Imagine several independently observed sites bound by the same TF. Aligning them exposes preferred bases and positions that tolerate alternatives; that recurring preference is what we call a sequence motif here. These four short excerpts are invented to explain alignment, not measured sites of a named TF or samples of our course generator. A consensus would summarize the most common letters but hide the alternatives.

**Point / transition:** The shared columns, then the varying letters in those columns. A matrix can keep those alternatives instead of reducing the motif to a single word.

### S2-04 · From related sites to a position matrix

**Slide ID:** `day-1-dna-position-matrix` · **Time:** 27:45–29:15 (1:30)

**What is on slide:** A four-position probability matrix from the preceding alignment; an arrow leads to a clearly distinct signed-weight schematic labeled PWM: log-odds weights. No formula on screen.

**What I want to say:** Counting bases in each aligned column gives a position frequency matrix; dividing by the column total gives the probabilities shown on the left. Those raw probabilities are not log-odds weights. A scoring PWM compares a smoothed probability with a background frequency: positive means more favored than background, negative less. Raw zeros can occur in this four-site illustration because it is tiny; smoothing avoids taking a logarithm of zero. Our course generator instead uses a specified 15-position probability matrix with no zero entries and samples sites from it. We store probabilities for generation, not these log-odds scores.

**Point / transition:** One probability column sums to one; then point across to the signed weights, keeping the two meanings distinct. We can use such a probability model to create a controlled classification task.

### S2-05 · One sequence, one class

**Slide ID:** `day-1-dna-task` · **Time:** 29:15–30:15 (1:00)

**What is on slide:** Two schematic sequence cards with given labels 0 and 1, alongside a new sequence → classifier → class probability flow. Visible Simulated DNA.

**What I want to say:** Our supervised task is binary classification of an entire sequence, not a separate prediction at every base or chromosome scanning. Training examples pair a sequence with its assigned class, and a fitted model will infer a probability for another sequence. In the primary course dataset the classes are simulation labels, not experimental TF binding, promoter annotations or measured regulatory activity. These abbreviated cards are schematic, not generator records. Course sequences have 160 bases.

**Point / transition:** One sequence card and its given label, then the new-sequence arrow. Here is how we generate a statistical relationship between sequence and label.

### S2-06 · Plant variable sites, not one fixed word

**Slide ID:** `day-1-dna-signal` · **Time:** 30:15–32:00 (1:45)

**What is on slide:** The current canonical 15-position probability matrix leads to a new site. Zoom position 5 to A/C/G/T = 0.50/0.40/0.05/0.05, then show class-1 planting chance 0.95 and class-0 chance 0.05.

**What I want to say:** The instructor has changed the primary simulation: assign balanced class labels and generate backgrounds, then decide whether to plant a site with probability 0.95 for class 1 and 0.05 for class 0. For each planting, independently sample one nucleotide from each of 15 position distributions to obtain a fresh site and insert it at a uniformly random valid start. All four probabilities at each position are strictly positive, sum to one and have a maximum at least 0.5. The zoomed column is position 5 of the current canonical matrix: A/C/G/T = 0.50/0.40/0.05/0.05. The left heatmap shows all 15 columns; color intensity encodes probability, while the base order is A/C/G/T from top to bottom. Labels are not the planting flag: a class-1 sequence can have no insertion and class 0 can receive one. There is no one fixed secret word defining the signal, and incidental matches are possible. No biological conclusion follows from this simulation.

**Point / transition:** The four alternatives in one column, then 0.95 versus 0.05 and the random insertion location. Now we have sequences and labels. How could we present the sequences to a model?

### S2-07 · How could we represent a sequence?

**Slide ID:** `day-1-dna-numeric-features` · **Time:** 32:00–33:30 (1:30)

**What is on slide:** Two open prompts only: How could we present a sequence to a model? What information would we preserve?

**What I want to say:** Invite different representations and listen for what each retains. There is no expected correct answer: a student might preserve every position, emphasize local words, summarize composition, or suggest another approach. Ask them to describe the information they would keep. If useful, point to an imagined word near the start versus near the end, without teaching one-hot encoding or CNNs yet. We will try one representation whose input is easy to inspect.

**Point / transition:** Both prompts; gesture along an imagined sequence as students explain their choices. Let us try counting local words as a deliberately simple starting point.

### S2-08 · Keep one example in view

**Slide ID:** `day-1-dna-worked-sequence` · **Time:** 33:30–34:00 (0:30)

**What is on slide:** Only the approved 21-base string, large and evenly spaced, with a subtle position ruler.

**What I want to say:** This is a constructed 21-base counting demonstration, not a sample, consensus or binding site from the new 15-position generator. It has no assigned class label. Course sequences remain 160 bases long. Keep the same line in place as we build the representation; the selected counts will also carry into Section 3.

**Point / transition:** The ends of the complete short string. Choose a word length, then slide a window.

### S2-09 · Read a four-base word

**Slide ID:** `day-1-dna-first-window` · **Time:** 34:00–35:00 (1:00)

**What is on slide:** The unchanged sequence with positions 1–4 highlighted and TATA beneath. Small definition: k-mer = k-base word; k = 4.

**What I want to say:** A k-mer is a string of k bases. With k equal to four, our first window is TATA. This is a four-base word, not four separate single-base counts, and counting it does not fit a classifier.

**Point / transition:** Four highlighted bases, then the extracted TATA word. Move the start by just one base.

### S2-10 · Move one base at a time

**Slide ID:** `day-1-dna-overlapping-windows` · **Time:** 35:00–36:15 (1:15)

**What is on slide:** The same line with three successive extracted windows TATA, ATAC, TACC; their one-base shifts are indicated below it.

**What I want to say:** Starting at base 2 gives ATAC; starting at base 3 gives TACC. We move one base, not four. Adjacent windows share three letters. Continue to the last full window, AATG, starting at 18; there are 18 window occurrences altogether. This deterministic counting on one teaching example requires no learned vocabulary or data fitting.

**Point / transition:** Starts 1, 2 and 3 on the same line, then each word beneath. Collect every occurrence, including repeats.

### S2-11 · A bag of k-mers keeps repeats

**Slide ID:** `day-1-dna-bag-of-kmers` · **Time:** 36:15–37:30 (1:15)

**What is on slide:** The persistent sequence becomes 18 word tiles, rearranged in a bag; repeated TATA and CGCG tiles are visibly repeated.

**What I want to say:** A bag of k-mers is an inventory of word occurrences, with multiplicity. We no longer attach an absolute start position to each occurrence. Three CGCG tiles stay three occurrences, rather than one presence flag. Each tile still spells an ordered four-base word, and overlapping words can retain indirect context; we have not erased every trace of order.

**Point / transition:** The three separate CGCG tiles, and the two TATA tiles. Compress repeated occurrences into counts.

### S2-12 · Turn repeated words into counts

**Slide ID:** `day-1-dna-count-occurrences` · **Time:** 37:30–39:00 (1:30)

**What is on slide:** The same sequence above three selected columns: TATA = 2, AATG = 1, CGCG = 3. Quiet text says 18 windows counted; selected columns shown.

**What I want to say:** TATA occurs at starts 1 and 14, AATG at start 18, and CGCG at starts 6, 8 and 10. Overlap does not stop a window from counting. The selected columns sum to six, not 18, because other words have their own counts. The full vector has a consistent column for each vocabulary word; absent words get zero. There are 4^4 = 256 possible four-base words, while a learned vocabulary may omit words absent from training. These values are only the constructed counting example.

**Point / transition:** Each word header and count, preserving the order TATA, AATG, CGCG for Section 3. What have we gained, and what information is no longer explicit?

### S2-13 · What does this representation keep?

**Slide ID:** `day-1-dna-lost-position` · **Time:** 39:00–40:30 (1:30)

**What is on slide:** One balanced comparison: local word identity/frequency and fixed-size input; explicit positions/full arrangement omitted. One quiet line preserves local order within words.

**What I want to say:** The benefits are a fixed-size numeric vector and access to simple models, with local pattern identity and frequency visible in each column. Counts do not explicitly store absolute positions or the complete arrangement of occurrences. But each k-mer retains order within the word and overlapping words can constrain surrounding context, so do not say all order is lost. Choosing k changes what local pattern length is visible and the possible vocabulary grows as 4^k. Bigger k can make vectors sparse and require more data; smaller k can miss longer dependencies. Day 2 revisits position.

**Point / transition:** The two sides, then the local-order sentence. Across examples, these count vectors become a table.

### S2-14 · One sequence becomes one row

**Slide ID:** `day-1-dna-count-vector` · **Time:** 40:30–42:00 (1:30)

**What is on slide:** A concrete two-row table from the new primary training data: IDs shortened to …00001 and …00002, selected counts 2/1/1 and 1/0/2, with class labels 0 and 1 separated at the right. Small role labels explain each area; no abstract X/y slide.

**What I want to say:** We now switch from the unlabeled short counting demonstration to two actual 160-base simulated training records from the revised generator. Read across a row: the ID tracks which sequence it is and is not a predictive feature; the highlighted middle columns are sequence-derived counts; the class label at the right is the supplied answer during training. For a new prediction the model receives the sequence-derived counts, without the class answer. Full IDs are simple-2026-00001 and simple-2026-00002; the screen shortens them for space. Counts use each complete 160-base sequence, and the omitted columns have further counts. Planting flags, sampled sites, positions, groups and split metadata are not predictive inputs. These simulation labels are not measured biology.

**Point / transition:** The ID, highlighted count columns, then the separated class-label column. Before fitting any data-dependent representation, assign the data roles.

### S2-15 · Three sets, three purposes

**Slide ID:** `day-1-dna-training-validation` · **Time:** 42:00–45:00 (3:00)

**What is on slide:** A visible three-way diagram: TRAIN learns parameters and fitted preprocessing; VALIDATION guides development; TEST evaluates the frozen workflow. Split-before-fitting and the freeze boundary are explicit.

**What I want to say:** Training learns model parameters and any data-dependent vocabulary or preprocessing. Validation is where we assess development choices, including candidate models, hyperparameters and representations; threshold choices belong here too if the protocol permits them. Our course threshold remains fixed at 0.5, so this is not authorization to tune it. Distinguish an initial candidate choice from selecting among fitted candidates using validation. Split before fitting vocabulary or transforms; fit only on training rows, then apply the same mapping to held-out sequences. Test is reserved for the planned Day 3 final comparison after all compared workflows are frozen. Official test labels can be used then to calculate the final score; they cannot guide development. Course split sizes are 720 train, 240 validation, 240 test under the retained 60/20/20 design.

**Point / transition:** Read the purpose of each box, then the split-before-fitting line and freeze boundary. The test boundary deserves one unambiguous statement.

### S2-16 · Test results never guide development

**Slide ID:** `day-1-dna-test-boundary` · **Time:** 45:00–46:30 (1:30)

**What is on slide:** One emphatic statement: NO DECISION EVER MADE ON TEST. Beneath it, a small final-evaluation → report arrow has no return arrow to development.

**What I want to say:** No test result guides design, representation, preprocessing, model selection, hyperparameter tuning or threshold changes. A disappointing final score is still the final score: it does not grant permission to change the workflow and try the same test again. We can interpret and report the frozen result, including failure and limitations; that is different from using it to improve or select a model. The Day 3 comparison is planned and frozen before the reveal, and test performance does not select a preferred workflow afterward. Day 4 remains development-only. Opening test labels for the official final score is permitted by that gate; using them or test sequences to steer development is not.

**Point / transition:** The statement, then the one-way final-evaluation-to-report arrow. Cross-validation changes how development is checked, while leaving this boundary intact.

### S2-17 · Rotate development folds; keep test aside

**Slide ID:** `day-1-dna-cross-validation` · **Time:** 46:30–48:00 (1:30)

**What is on slide:** A three-row fold-rotation visual alternates training and validation; a separate TEST block remains untouched. No scores or new course execution steps.

**What I want to say:** Cross-validation repeats the training/validation roles across development folds, so a decision depends less on a single held-out development subset. This schematic uses three folds only to make rotation visible; it is not a change to the course’s fixed split protocol and is not a license to access test data. Refit vocabulary, transforms and the model using only that fold’s training rows, then validate on the held-out fold. We can summarize those validation outcomes for choices. Cross-validation is optional depth in this 25-minute section: if questions need the time, give this one-sentence takeaway and continue. Bootstrap sampling is a different idea: postpone its mechanics to Section 5’s forests, where training rows are sampled WITH replacement. It is neither a replacement test set nor the same operation as fold rotation.

**Point / transition:** The validation block moving across development folds, then the stationary test block. We have input features and an evaluation plan. Which classifier could turn counts into a probability?

### S2-18 · Which model can turn counts into a prediction?

**Slide ID:** `day-1-dna-ready-for-model` · **Time:** 48:00–50:00 (2:00)

**What is on slide:** The same selected count vector leads through classifier? to class probability. A quiet next-step line names logistic regression; no weights or performance claims.

**What I want to say:** We chose a binary output first. Representation and model are joint, iterative design choices, not a universal rule that one must always come first. In this teaching story counts come first so everyone can see what enters the classifier. Logistic regression is our proposed transparent baseline for Section 3: it learns a map from the count vector to a class probability, then a fixed threshold can produce a class. Trees later use the same features; later CNNs need an ordered representation that we will teach then. Choosing this first candidate is different from comparing models or tuning using validation, and test results never make that choice. Inference means fit the model using training data, then apply the fixed fitted preprocessing and model to a new sequence. We do not learn new weights in real time merely because a new sequence arrives. The following Section 3 weights are illustrative, not measured results of the revised generator. Take the full 50–60 break.

**Point / transition:** Counts, model box and probability output in that order. After the break, restore this count row and attach signed weights in Section 3.

### Section 2 teaching-source notes

**Timing and delivery:** The 18 allocations sum to **25:00**, minute 25–50, including the title, a 90-second open discussion, three biology slides totaling four minutes, and 90 seconds for conceptual CV. The 50–60 break remains separate; Section 3 starts at minute 60. These are proposed allocations, not a rehearsal. CV is optional depth, not extra time; shorten its explanation to protect student contributions. No mandatory Colab startup, model fitting, benchmark comparison or scientific result is part of this section.

**New authoritative dataset decision — 2026-11-03:** The primary controlled dataset is to use a **15-position nucleotide probability matrix**, with a fresh site sampled independently across positions for every planting. At every position, A/C/G/T probabilities are strictly positive, sum to one and have maximum at least 0.5; the instructor's example `0.50, 0.40, 0.05, 0.05` satisfies this. Plant at a uniformly random valid location with probability **0.95 conditional on class 1**, **0.05 conditional on class 0**. Retain the course's 1,200/160-base framing and fixed 60/20/20 split unless the scientific migration changes them explicitly. The label is assigned independently of the subsequent Bernoulli planting event conditional on that label; it is not identical to `motif_planted`. There is no fixed word whose presence defines all positives or whose absence defines all negatives. Variation in sampled sites is intentional, and positive probability for every base does not mean equal likelihood for every site.

**Canonical implementation dependency:** [SimulationConfig and generate_course_dataset](../../course_code/course_core.py) own the actual default matrix and generation semantics; [the simple-signal workflow](../../course_code/01_simple_signal.py) owns the training-fitted count vectorizer. At the initial inspection in this revision they still implemented the superseded eight-base fixed motif and 0.9/0.1 planting. A separate implementation agent owns their migration, notebooks, tests and scientific docs; this slide task does not claim that migration is finished or independently validated. The initial placeholder column was replaced by the actual canonical probability matrix after it became available during this revision. Old generator rows were discarded and regenerated for the new primary task; old primary-dataset scores remain invalid evidence for the new generator and are not shown in this section. A later read-only check found the revised canonical generator available and verified its 15×4 probability constraints, position 5, and two newly regenerated training records. This checks teaching inputs, not the full scientific migration or any predictive result. The source hash observed for that check is `34b397a9eec0191bd4f98201899eaf5a0385f8dd23c18affd4c2fb49fecaae55`; other scientific files and later code edits require their own validation. The visible heatmap uses the actual matrix (positions are rows in code, columns in the slide; bases remain A/C/G/T). Its zoom is real position 5, coinciding with the instructor example. The source table rows are recorded below.

**New primary training-table facts:** Regenerated from the observed source above without fitting or scoring. IDs on slide are shortened only for readability; snippets here show the first 20 bases, while counts use all 160 bases.

| sample_id | Sequence snippet | TATA | AATG | CGCG | label |
| --- | --- | --- | --- | --- | --- |
| simple-2026-00001 | `ACAATTCTATAGTCGTGCAG…` | 2 | 1 | 1 | 0 |
| simple-2026-00002 | `GCCATATAGACAGGGGCTGT…` | 1 | 0 | 2 | 1 |

Both full rows sum to 157. Neither is the 21-base demonstration. The equality of some counts with earlier examples does not establish unchanged sequences or provenance; all values above were rechecked against the revised generator.

**Matrix semantics and checked toy arithmetic:** S2-03 uses invented aligned four-position excerpts `ACGT`, `ACAT`, `ATGT`, `ACGA`, not empirical binding sites or course generator sites. In A/C/G/T row order their raw frequency counts are `(4,0,1,1)`, `(0,3,0,0)`, `(0,0,3,0)`, `(0,1,0,3)`; divide by four to obtain S2-04's position probabilities. Toy observed frequencies can be zero; the **course's generative probabilities cannot**. Do not conflate the two. The signed PWM panel is schematic, not a second numeric probability matrix. In notes, a scoring convention is `w(b,j) = log2(p(b,j)/q(b))`, with background `q(b)>0`; estimated probabilities require smoothing before a logarithm when observed counts are zero. For example, adding one count per base gives `p=(n+1)/8`; against uniform `q=0.25`, four/three/one/zero observed counts give weights approximately `1.322 / 1 / 0 / −1`. Keep that arithmetic off the projected slide. Position independence is a modeling assumption, not a claim that biological binding sites have no dependencies. A motif match, a predicted class and actual context-dependent TF binding/regulation are different observations.

**Exact counting demonstration:** `TATACCGCGCGCGTATAAATG` is a **constructed 21-base counting example**, not a consensus or sampled site of the new 15-position model. It has no assigned label. Preserve the same example and the selected column order `TATA`, `AATG`, `CGCG` into Section 3, whose weights are illustrative rather than measured from the revised simulation. The complete one-based window trace is a checking reference, not a production table:

```text
start   4-mer    start   4-mer    start   4-mer
  1     TATA       7     GCGC      13     GTAT
  2     ATAC       8     CGCG      14     TATA
  3     TACC       9     GCGC      15     ATAA
  4     ACCG      10     CGCG      16     TAAA
  5     CCGC      11     GCGT      17     AAAT
  6     CGCG      12     CGTA      18     AATG
```

`TATA=2`, `AATG=1`, `CGCG=3`, `GCGC=2`; one each of `AAAT`, `ACCG`, `ATAA`, `ATAC`, `CCGC`, `CGTA`, `GCGT`, `GTAT`, `TAAA`, `TACC`; `AAAA=0`. There are 14 distinct words and 18 occurrences. With length L and word length k there are `L−k+1` overlapping windows: 18 here, 157 for the 160-base course sequence. The theoretical vocabulary is `4^k`, hence 256 for k=4; the actual training-fitted vocabulary can omit unseen words. Apply that same fitted mapping to validation, test at the allowed final gate, and new inputs. The bag keeps multiplicity, local order within words, and some indirect context, while discarding explicit absolute positions and the full arrangement; it is not a bag of distinct presence flags or a unigram histogram. Reverse-complement handling is outside this section and is not silently guaranteed.

**Evaluation contract:** Split before fitting a vocabulary, learned transforms or classifier; learn each only on training rows. Deterministic counting of the standalone example can precede splitting because it estimates nothing from held-out data. Validation guides development; initial candidate choice, validation-based model selection and parameter fitting are different operations. If a protocol permits threshold tuning, it uses development data only; this course's threshold is fixed at 0.5. In conceptual CV, preprocessing is refitted inside each fold's training subset and the protected test remains outside every fold. No nested-CV detour or new execution protocol is proposed. Test results **never** guide design, representations, preprocessing, model selection, hyperparameters or threshold changes, including after disappointing performance. The permitted [Day 3 final comparison](../../docs/adr/0002-validation-for-development-protected-test-comparison.md) evaluates the frozen planned workflows, then reports/interprets their scores; it is not a model-selection round. Official labels may be opened at that gate to compute the final score. Day 4 remains development-only. No test was run or score inserted here.

**Model-choice teaching note:** Task/output comes first; representation and model are joint iterative design choices, not a universally ordered pipeline. Counts precede the first classifier in this story so its input is visible. Logistic regression is the proposed transparent candidate next; trees reuse the features, while later CNNs require an ordered representation taught on Day 2. Evaluation roles are defined before comparisons on validation. Inference means applying fitted preprocessing and the fitted classifier to a new sequence, not learning weights as that sequence arrives. No claim that logistic regression is always best or that a k-mer uniquely identifies the probabilistic motif is implied.

**Later-section dependency outside this implementation:** Sections 3–6 HTML teaching content and interactions remain preserved, with only the newly authorized figure palette changes. Their story text may be revised separately by the coordinating agent. Section 6 beat 2 still spells out the old fixed motif's five fragments; historical HTML `day-1-slide-50` makes the same obsolete primary-signal claim, and `day-1-slide-49` asks for words inside that fixed motif. Their later revision must interpret **distribution-derived sequence clues**, not membership in `TATAAATG` substrings; primary-dataset validation scores elsewhere also need regeneration before reuse. See the exact stale-content inventory in [QA](../qa.md#section-2-implementation--2026-11-03). The unchanged [annotated outline](../teaching-outline.md#day-1) and historical reports remain evidence of earlier intent, not an override of the latest instructor decision.

**Source and implementation boundary:** Original simple diagrams adapt the teaching precedents in the [reference review](../../docs/course-wiki/reference-materials.md) and the supplied genomics PDF's TF/regulation progression, without copying external artwork. The [approved logistic style](logistic-style-reference.html) supplies typography, palette and whitespace. The 18 new records replace historical `day-1-slide-13`–`day-1-slide-22`; aliases keep those older incoming links useful, while new IDs isolate stale local autosaves. At the Section 2 checkpoint, later records were retained apart from palette changes. The subsequent authorized build replaced Sections 3–6 and both break records; the first 42 Section 1/2 records remain preserved. New figures and the style reference use blue `#0072B2`, orange `#D55E00`, neutral context, and purple only where a third count track needs separation. White/navy layout is retained. Section 3 HTML was subsequently implemented under the full Day 1 build authorization. No scientific code, notebook, ADR, glossary or annotated-outline edit belongs to this implementation.

## 3. Logistic regression on k-mer counts · 60–90

<a id="section-3"></a>

**Implemented for instructor review — 2026-11-03.** These 16 slides incorporate the latest feedback: begin with the desired class probabilities, make the score-to-probability mapping interactive, and give loss and learning room to be explained. The former standalone regularization/model-complexity beat is removed. The HTML and guided notebook cells are implemented and locally rehearsed; actual Colab execution and classroom pacing remain unverified.

**Story question:** How can sequence counts become probabilities for class A or B, and how does learning find the weights that make those predictions?

**Exit understanding:** Trace counts → signed weighted contributions → sum and bias → score → probability; distinguish a probability from a thresholded decision and an observed label. Explain how labeled training examples produce loss, how average training loss supplies feedback for learning, and how a fitted model subsequently performs inference with fixed parameters. Validation checks performance and supports later development comparisons; test results never inform any choice.

**Visual direction:** Follow the [approved logistic reference](logistic-style-reference.html): one short title, one focal explanatory visual, generous whitespace and detailed speaking notes. Keep the same count positions through S3-04, then the same score through S3-06. Use blue `#0072B2` for model/reference structure, orange `#D55E00` for the active example or moving point, and gray for context, with direct labels and explicit signs. The sigmoid and loss landscape are separate visuals with different axes and purposes. Avoid repeated headers, takeaway bars and visible “Illustrative example” labels; retain all numerical provenance in notes.

### S3-01 · From counts to class probabilities

**Slide ID:** `day-1-lr-section` · **Time:** 60:00–61:30 (1:30)

**What is on slide:** One count row → a Predictor box → two complementary outputs: `P(class B | counts) = p` and `P(class A | counts) = 1 − p`, with `p + (1 − p) = 1`. Label class A = 0 and class B = 1 beside the outputs.

**What I want to say:** Before the break we represented a sequence by counts. What do we need from a model? Given that representation, we want an estimate of which of our two classes the sequence came from. We will call class B the positive class, encoded as 1, and use p for its estimated probability; the remaining probability belongs to class A, encoded as 0. These are mutually exclusive, exhaustive classes in this task. The model estimates class from counts; it does not directly measure TF binding.

**Point / transition:** Trace counts to the two outputs, showing that they add to one. Choose a simple predictor whose calculation we can open.

### S3-02 · A simple predictor

**Slide ID:** `day-1-lr-baseline` · **Time:** 61:30–62:30 (1:00)

**What is on slide:** Replace Predictor with Logistic regression. Enlarge the familiar selected columns `TATA: 2`, `AATG: 1`, `CGCG: 3`, with gray omitted columns and a small Selected features caption; retain the probability output.

**What I want to say:** Logistic regression takes a numeric vector and estimates a binary class probability. It is a useful first candidate because we can follow every calculation; its name does not make this a continuous-target regression task. Our actual classifier uses the full training-fitted vocabulary. For a worked example, we use just these three nonzero-weight features, setting all omitted weights to zero. The counts come from Section 2's constructed 21-base sequence, not a sampled 15-base planted site or a fitted course result.

**Point / transition:** Point to the selected features without implying that three columns are the full vector. Attach weights and work through an example.

### S3-03 · Multiply counts by weights

**Slide ID:** `day-1-lr-signed-contributions` · **Time:** 62:30–64:30 (2:00)

**What is on slide:** Reveal one aligned product at a time: `TATA: 2 × (+0.6) = +1.2`, `AATG: 1 × (+0.8) = +0.8`, `CGCG: 3 × (−0.2) = −0.6`. Label the columns Count, Weight and Contribution; gray the inactive products.

**What I want to say:** Multiply each count by its weight. Two occurrences with weight +0.6 contribute +1.2; three with weight −0.2 contribute −0.6. Positive and negative contributions move the score in opposite directions. In a fitted model the signed weights are learned from training examples; I chose these numbers so we can see the arithmetic. A sign describes this predictor's calculation, not biological activation or inhibition. Changing one input coordinate while holding others fixed is a statement about the model, not necessarily a possible DNA edit.

**Point / transition:** Count → weight → product for each row. The next operation is a sum.

### S3-04 · Sum, then add the bias

**Slide ID:** `day-1-lr-score` · **Time:** 64:30–66:30 (2:00)

**What is on slide:** The products feed a large sum: `1.2 + 0.8 − 0.6 = 1.4`. Reveal the bias `b = −0.4`, then `z = 1.4 − 0.4 = 1.0`. One compact rule reads `z = b + Σ wⱼxⱼ`.

**What I want to say:** Sum the weighted contributions and add the bias, also called the intercept. The bias is a shared starting offset, learned alongside the weights, rather than another word count. Our example produces a score of one. The same rule applies to every column in the actual fitted vocabulary. A score can be negative or greater than one, so we still need to turn it into a probability.

**Point / transition:** Trace the addition explicitly, ending at z = 1. Carry that value into the next visual.

### S3-05 · Move the score, see the probability

**Slide ID:** `day-1-lr-sigmoid` · **Time:** 66:30–69:00 (2:30)

**What is on slide:** One large sigmoid, horizontal axis Score z and vertical axis `p = P(B | counts)`. A score slider moves an orange point and its projection lines; update the numeric z, p and complementary `P(A | counts) = 1 − p`. Keep anchors `z = 0 → p = 0.5` and `z = 1 → p ≈ 0.731`; the only equation is `p = 1 / (1 + e^(−z))`.

**What I want to say:** The sigmoid maps our score to a number between zero and one. At z = 1, class B gets about 0.731 and class A about 0.269. Move toward zero, then toward negative scores and back: increasing z increases p, but the curve flattens near its ends. This control changes the supplied score to demonstrate the mapping; it does not train the model or alter learned weights. “Linear” describes the weighted score, while its probability mapping is curved.

**Point / transition:** Invite a prediction of the direction before moving the score; show zero and restore one. Proposed interaction: labeled slider from −6 to +6, step 0.1, initial value 1, with reset and numeric readout. While the slider has focus, arrow keys adjust it without triggering slide navigation. Static fallback uses the same zero/one/negative-score states. The next operation turns a probability into a decision.

### S3-06 · A probability becomes a decision

**Slide ID:** `day-1-lr-threshold` · **Time:** 69:00–70:00 (1:00)

**What is on slide:** A probability line keeps the point at `p ≈ 0.731`; a separator at 0.5 labels Below: A / 0 and At or above: B / 1. Keep a separate quiet slot `Observed label: unknown`.

**What I want to say:** The course uses p at least 0.5 to predict class B; otherwise it predicts A. Our worked example therefore predicts B. A probability, a predicted category and an observed label are different things. This constructed sequence has no assigned label, so we cannot say whether the decision is correct. An optional reveal moving only a hypothetical threshold to 0.8 would change the decision to A while preserving the probability; it does not change the course's fixed 0.5 rule.

**Point / transition:** Probability dot → separator → predicted category, then the unknown observed label. A simple reveal is sufficient; another interactive control is optional.

### S3-07 · After fitting, apply the model

**Slide ID:** `day-1-lr-inference` · **Time:** 70:00–71:00 (1:00)

**What is on slide:** A small Fitting complete marker precedes one forward path: New sequence → Fitted count mapping → Fixed weights and bias → Probability. No feedback arrow returns to the parameters.

**What I want to say:** Once a model is fitted, we can use it for inference. Count the new sequence with the same fitted vocabulary and feature order, then apply the fixed weights and bias. Its label is not required to produce a probability, and ordinary inference does not update the model. So far we have supplied the weights to explain prediction; now we need to explain the learning in machine learning.

**Point / transition:** Point to Fitting complete before tracing the forward path. Rewind to how those fitted parameters were obtained.

### S3-08 · Labels provide feedback

**Slide ID:** `day-1-lr-supervised-fit` · **Time:** 71:00–73:00 (2:00)

**What is on slide:** Several schematic training count rows with a separately labeled `y: A = 0 / B = 1` column enter a Fit box; shared Weights and Bias emerge. Reveal a feedback connection from Training probabilities + Known labels into that box.

**What I want to say:** Learning uses many examples paired with known labels. One shared set of weights and a bias must produce useful probabilities across those examples; we do not choose a separate model for each row. Training fits the count vocabulary and the classifier using training data only. The known labels supply feedback about its current probabilities. To turn that feedback into something an optimizer can use, we need a loss function.

**Point / transition:** Point first to the label column, then to the shared parameters. Use a separate labeled training example next; do not assign truth to the earlier 21-base sequence.

### S3-09 · Give a prediction a loss

**Slide ID:** `day-1-lr-binary-loss` · **Time:** 73:00–75:00 (2:00)

**What is on slide:** One explicitly labeled training example: `Known label: B / 1`, `p(B) = 0.9` → `Loss = −log(0.9) ≈ 0.105`. Reveal the name Binary cross-entropy and a short rule: Lower probability on the known label → larger loss.

**What I want to say:** Loss is a numerical cost for a prediction given its known label. For a true B example, binary cross-entropy is minus the natural log of p. For a true A example, it is minus the log of 1 − p, because that is the probability assigned to A. Putting 0.9 probability on the known class gives a small cost, about 0.105. This uses the probability itself, before any decision threshold; we are not counting correct and incorrect categories here.

**Point / transition:** Known label → probability assigned to that label → cost. Keep the label fixed and make the prediction confidently wrong.

### S3-10 · Confident mistakes cost more

**Slide ID:** `day-1-lr-confident-loss` · **Time:** 75:00–77:00 (2:00)

**What is on slide:** One comparison table, revealed by row: for Known B, `p(B) = 0.9 → loss 0.105` versus `p(B) = 0.1 → loss 2.303`; for Known A, the losses reverse. Column labels specify the same p(B) in both rows.

**What I want to say:** For a true B example, assigning only 0.1 probability to B costs about 2.303, much more than 0.105. If the known label is A, p(B) = 0.1 is the good prediction, because p(A) = 0.9. Confidence matters: assigning almost no probability to the known class is penalized especially strongly. These are constructed comparisons of predictions, not before-and-after fitting results. Learning seeks smaller loss across the training set, not just greater confidence in any one prediction.

**Point / transition:** Read the known label before each probability. The direction reverses with the label; now combine losses from many rows.

### S3-11 · Average over the training examples

**Slide ID:** `day-1-lr-mean-loss` · **Time:** 77:00–78:30 (1:30)

**What is on slide:** Several labeled training rows each produce a small loss tile, converging on `L = (ℓ₁ + … + ℓₙ) / n`. A two-tile reveal gives `(0.105 + 2.303) / 2 ≈ 1.204`.

**What I want to say:** Calculate a loss for each training example, then average those costs. This gives one quantity that summarizes how the current parameters predict the known training labels. The two-tile arithmetic is a small constructed example; the real fit combines all training rows. An update may help some rows and hurt others, so we look at the combined objective rather than requiring every example's loss to fall. We have a cost; now we need a way to adjust the weights.

**Point / transition:** Trace row losses into their average. Put a weight on one axis and that average loss on the other.

### S3-12 · Take a step downhill

**Slide ID:** `day-1-lr-optimization` · **Time:** 78:30–81:30 (3:00)

**What is on slide:** A separate simple loss landscape with horizontal axis One weight w and vertical axis Average training loss L. A blue curve has a finite low point; an orange current position, local slope marker and arrow show the next downhill direction. A Step button moves along a short prepared sequence and updates the loss readout; Reset returns to the start. A quiet label reads Other parameters held fixed; the compact rule is `w ← w − η × slope`.

**What I want to say:** Try a weight, compute the training probabilities and their average loss, then use the local slope to choose a direction toward lower loss. The derivative describes that slope; subtracting it moves in the opposite direction. The learning rate η sets the step size. With a suitably small step in this demonstration, the marker moves downhill. A step that is too large can overshoot; there is no promise that every update at any learning rate lowers loss. This one-weight view builds intuition: actual models adjust many weights and a bias. We seek a low objective, not a promise of zero loss; overlapping classes and noise can prevent perfect prediction.

**Point / transition:** Distinguish these axes from the earlier sigmoid: here we change a parameter and recompute loss across training rows. Use two or three Step presses within the allocation, then stop. Static fallback reveals the same arrows and positions. This illustrates gradient descent; the actual course fit uses a different optimizer, specified in the notes.

### S3-13 · Fit once, then predict

**Slide ID:** `day-1-lr-fit-predict` · **Time:** 81:30–82:30 (1:00)

**What is on slide:** Two phases, revealed sequentially in the same space: Training counts + Labels → Fit → Fitted parameters; then New counts → Fixed fitted parameters → Probability. Only the first phase has a learning loop.

**What I want to say:** During fitting, labels and loss help an optimizer find the parameters. During inference, those parameters stay fixed and labels are unnecessary. The count mapping is also fitted on training data and then reused. scikit-learn's fit performs the optimization for us; predict_proba applies what was learned. We can inspect those operations in the existing notebook.

**Point / transition:** Follow the training loop once, then remove its feedback arrow for inference. Switch to the proposed notebook checkpoint inside the next five minutes.

### S3-14 · Try one prediction

**Slide ID:** `day-1-lr-notebook-checkpoint` · **Time:** 82:30–87:30 (5:00)

**What is on slide:** One practical strip: Inspect a count row → Fit on TRAIN → Predict a validation row → Reproduce z, p and loss. Link the [GitHub-hosted 01_simple_signal.ipynb](https://github.com/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb) and its [Open in Colab](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb) route. Keep code details in notes.

**What I want to say:** Yes, we have an existing Day 1 notebook; a focused Section 3 tutorial is implemented in it. The classroom route is to open that GitHub notebook in Colab. In the proposed checkpoint, inspect one feature row, fit logistic regression on training sequences and labels only, then predict probabilities for held-out validation sequences. For one row, use the actual fitted full count vector, coefficients and intercept to reproduce z and its sigmoid probability. Finally, use that row's known label to calculate its binary loss. This last comparison assesses the prediction; it does not update the model on validation data.

**Point / transition:** Proposed five-minute allocation, replacing lecture time: 0:30 orient to the already-prepared Colab tutorial; 0:45 inspect a count row; 1:00 fit TRAIN-only and predict validation probabilities; 1:45 reproduce one full-vector z/p and its labeled loss; 1:00 discuss and return to slides. Instructor demonstration with optional follow-along is the pacing proposal; independent completion by every student is not assumed. Use only the focused logistic cells, leaving metric reports for Section 4 and forests for Section 5. If setup or fitting would consume the slot, show prepared views of the same operations and calculations. No extra startup block or live result is assumed.

### S3-15 · Check on held-out examples

**Slide ID:** `day-1-lr-validation` · **Time:** 87:30–89:00 (1:30)

**What is on slide:** Validation sequences → Fixed fitted predictor → Probabilities, meeting a separate Observed validation labels branch at Compare. A detached gray Test box reads Final frozen comparison only; test never guides choices.

**What I want to say:** Training loss describes the examples used to learn the model. Validation checks how predictions perform on held-out development examples and can support later comparisons. We do not feed validation labels back into this fit. Repeated development choices also adapt to validation, so it is not the final independent assessment. Test results never guide any representation, fitting, model, hyperparameter or threshold choice, even after the planned final frozen comparison.

**Point / transition:** Bring validation predictions and labels together, keeping the optimizer absent. Do not add model-complexity plots or metric definitions.

### S3-16 · From one prediction to many

**Slide ID:** `day-1-lr-validation-handoff` · **Time:** 89:00–90:00 (1:00)

**What is on slide:** One prediction's Probability + Known label expands into several aligned prediction/label pairs, with the single question What kinds of mistakes do we make?

**What I want to say:** One prediction produces a probability. Across many labeled examples, we will count types of mistakes and describe performance. That is the next question now that we understand how the model predicts and learns. Section 4 begins with the confusion matrix; no new method is hidden in this handoff.

**Point / transition:** Expand one row into several, allow a brief clarification within this minute, then continue directly to Section 4 at minute 90. There is no break between Sections 3 and 4; the next break is 115–125.

### Section 3 teaching-source notes

**Timing and scope:** The 16 allocations sum to **30:00**, minute 60–90: counts/probability mechanism and decision S3-01–06, 10:00; inference S3-07, 1:00; learning/loss/optimization and fit-versus-inference S3-08–13, 11:30; proposed notebook checkpoint S3-14, 5:00; validation and handoff S3-15–16, 2:30. Questions, interactions and the tutorial replace explanation within these allocations, not after them. These are proposed timings, not a rehearsal. Regularization/model complexity has no standalone slide or teaching beat. Confusion matrices and metric reports belong to Section 4, trees/forests to Section 5, detailed coefficient interpretation to Section 6.

**Worked-model provenance:** `TATACCGCGCGCGTATAAATG` is the same **constructed 21-base counting demonstration** as Section 2: overlapping counts are `TATA=2`, `AATG=1`, `CGCG=3`. It has no assigned label and is independent of the new 15-position primary motif PPM. The full representation has more columns; chosen weights `(+0.6, +0.8, −0.2)`, all omitted weights zero and bias `−0.4` define an exact reduced teaching model. Contributions `(+1.2, +0.8, −0.6)` sum to `1.4`; `z=1`, `p(B)=0.7310585786…`, `p(A)=0.2689414214…`. At z = 0 both probabilities are 0.5. Threshold 0.5 predicts B; hypothetical threshold 0.8 predicts A. These are constructed calculations, not fitted outputs from the new generator or evidence of model quality. Coefficient units depend on feature scale; correlated, overlapping counts and fixed sequence length constrain realizable changes. Coefficient signs do not establish biological causation.

**Probability and loss definitions:** Encode class A as `y=0` and class B as `y=1`; throughout, `p=P(B | counts)` is the model estimate and `1−p=P(A | counts)`. The score is `z=b+Σwⱼxⱼ` and `p=σ(z)`; optionally name `log[p/(1−p)]=z` in speaking notes without adding a log-odds slide. Binary cross-entropy uses natural logarithms: `ℓ(y,p)=−[y log(p)+(1−y)log(1−p)]`. For known B, p = 0.9 gives `0.1053605157…`, p = 0.1 gives `2.3025850930…`; for known A these losses reverse. Their two-example mean is `1.2039728043…`; round only the displayed result after calculation. S3-09–11 use separate constructed labeled examples, not the unlabeled sequence or a measured training history. Training averages loss over its examples before considering the implementation's penalty. Loss supplies fitting feedback; performance metrics and the course's selection criterion are explained in Section 4. A p of 0.731 is not a guarantee of correctness or demonstrated calibration, nor is it the simulator's planting probability conditioned on class.

**Downhill illustration and actual optimizer:** Specify S3-12's curve as a constructed one-parameter slice of logistic loss: four training examples with the displayed feature equal to 1, labels `(1,1,1,0)`, fixed bias 0 and all other contributions zero. Then `L(w)=−[3 log σ(w)+log(1−σ(w))]/4`, with derivative `σ(w)−0.75` and finite minimum at `w=log(3)`. Start at `w=−1` and use modest fixed learning rate `η=0.5` for a short prepared sequence of `w ← w−η(σ(w)−0.75)`; each displayed readout must be calculated from this function. This supplies genuine binary-loss geometry without pretending to plot the full fitted model or a new experiment. The nonzero minimum illustrates that conflicting labels at the same represented input cannot all be predicted perfectly. Do not claim every update, arbitrary step size or individual row's loss must improve. In the full model many weights and the bias move together; a plotted slice holds the others fixed. The actual [simple-signal pipeline](../../course_code/01_simple_signal.py) constructs `LogisticRegression(max_iter=2000)`: its default optimizer is **L-BFGS**, not vanilla gradient descent. Its actual objective is regularized (default L2 coefficient penalty); retain this as an implementation detail in notes, without a regularization sweep, complexity lesson or claim that fit follows the toy steps.

**Notebook checkpoint and publication boundary:** The existing local source artifact is [01_simple_signal.ipynb](../../notebooks/01_simple_signal.ipynb); classroom execution opens the **GitHub-hosted ipynb in Colab**, through the links in S3-14, rather than a local Jupyter/download/script-copy route. The focused Section 3 tutorial is implemented in that notebook and its builder and locally verified. The implementation/rehearsal record supersedes the earlier spec-only boundary. GitHub `main` at the supplied `f1f079d` checkpoint predates the uncommitted revised 15-position PPM/tutorial work. Local revisions must be published in the next authorized push before the classroom links can serve them; the main-branch link is not proof that revised content is already deployed. End-to-end course execution in Colab and the five-minute pacing remain unverified. Local checks are verification only. The [notebook guide](../../notebooks/README.md) owns access/setup details.

**Concrete tutorial teaching path:** Open the focused tutorial, inspect one full training-derived feature row and its column names, construct the canonical count/logistic pipeline, then call `pipeline.fit(train["sequence"], train["label"])` and `pipeline.predict_proba(validation["sequence"])`. With fitted class order `[0,1]`, column 1 supplies p(B); column 0 supplies p(A). Transform one validation sequence with the fitted count mapping and use **all** its fitted coefficients and the intercept to calculate `z=b+Σwⱼxⱼ`; compare `σ(z)` with predict_proba. Only after prediction, read that row's validation label and calculate the binary loss by hand or the tutorial's provided arithmetic cell. This demonstration does not fit on validation or turn validation loss into the training objective. Keep the known-label comparison paired to the same sample. Do not run the notebook's whole experiment workflow merely to reach this checkpoint: its forest fitting and metric reports belong later. A toy gradient-descent exercise, if supplied by the notebook agent, is optional depth replacing part of S3-12 or S3-14, not additional time or a claim about L-BFGS. Prepared fallback visuals follow the same full-vector path; label constructed or saved values by their actual origin. The local notebook rehearsal verified the current full-vector path.

**Canonical data and evaluation boundary:** Read-only inspection of [SimulationConfig and the generator](../../course_code/course_core.py) establishes 160-base independent uniform backgrounds, an explicit 15×4 primary motif PPM, a fresh independently sampled site per planting event and a uniformly random valid insertion start. Each position has positive probabilities summing to one and maximum at least 0.5. Planting probability is 0.95 given class B/1 and 0.05 given class A/0; planting truth is not the class label or a predictive feature. Both classes can generate overlapping sequence observations, so no zero-loss/perfect-prediction promise follows from the known generator. The actual pipeline uses character `CountVectorizer` with k = 4, `lowercase=False`, the full training-fitted vocabulary, and fixed decision threshold 0.5. Split before fitting vocabulary, learned preprocessing or model parameters; reuse them unchanged for inference. Validation supports development checks and later comparisons outside the parameter optimizer. Protected test data/results never inform any choice or fitting, including after the frozen final Day 3 scoring. The later local full-notebook rehearsal supplies the current paired validation evidence; no protected-test evaluation occurred.

**Sources and review status:** Follow [ADR 0001](../../docs/adr/0001-controlled-sequence-classification.md), [ADR 0002](../../docs/adr/0002-validation-for-development-protected-test-comparison.md), the [annotated teaching intent](../teaching-outline.md#day-1) and the [approved visual preferences](../../docs/course-wiki/teaching-preferences.md#style-approved--2026-11-03). The [logistic-regression API](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [model formulation](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression) and [log-loss definition](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html) are conceptual references; canonical local code determines course behavior. Slide IDs now resolve in the actual HTML. GitHub-to-Colab delivery is settled; instructor demonstration with optional follow-along is the proposed depth for this timing. No additional user decision is needed to make this revision concrete.

## 4. What makes a prediction useful? · 90–115

<a id="section-4"></a>

**Implemented for instructor review — 2026-11-03.** The instructor requested Section 4 planning, then agreed to a guided hands-on approach using existing validation predictions, confusion counts, precision/recall and a threshold change. The 16 slides below allocate **25 minutes**, including **five minutes in the existing GitHub → Colab notebook**. Detailed wording and the brief precision–recall/average-precision overview remain proposals. The subsequent build authorization covers the implemented HTML and focused notebook cells.

**Story question:** We can predict a probability. How do we tell whether those predictions are useful?

**Exit understanding:** Read actual versus predicted class in a confusion matrix; explain precision and recall through the groups they count; recognize an accuracy trap and what F1 summarizes; distinguish a threshold decision from ranking; interpret ROC-AUC and recognize the supporting positive-call perspective of precision–recall. Apply the main ideas to held-out validation predictions without refitting or accessing test results.

**Teaching approach:** One persistent batch of predictions develops into a confusion matrix, denominators, a moving threshold and curves. Use one short title and one focal visual per slide, blue/orange class markers and gray context, with detailed instructor cues below. No opening metric quiz or return to the superseded diagnostic. The 100-row constructed example makes the arithmetic readable; the notebook applies the same operations to the actual 240 validation rows. Do not imply those two batches have the same results.

### S4-01 · What makes a prediction useful?

**Slide ID:** `day-1-metrics-section` · **Time:** 90:00–90:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** We have learned to produce probabilities. Now we will compare those predictions with known outcomes, work out which mistakes matter and use the notebook to inspect them.

**Point / transition:** The title. Move from one prediction to a batch of validation examples.

### S4-02 · Compare predictions with observations

**Slide ID:** `day-1-metrics-observations` · **Time:** 90:15–91:15 (1:00)

**What is on slide:** A small excerpt from a prediction table: Sequence ID, Observed class, P(B), Predicted class. Reveal predicted class at threshold 0.5. Labels identify A = 0 and B = 1; show a correct and an incorrect example.

**What I want to say:** The observed label is supplied with the example; the predicted probability comes from the fitted model. Calling B when p is at least 0.5 gives a decision we can compare with that label. Positive means B, our class of interest, rather than a guarantee of real TF binding. The label is not the simulator's planting flag. These examples are constructed for teaching; the notebook will use our actual validation predictions. Keep each probability paired with its own sample and label.

**Point / transition:** Trace one row across the columns. Group all rows by observed and predicted class.

### S4-03 · Four possible outcomes

**Slide ID:** `day-1-metrics-confusion` · **Time:** 91:15–92:45 (1:30)

**What is on slide:** A large 2×2 confusion matrix, revealed one cell at a time. Rows are Observed A / Observed B; columns are Predicted A / Predicted B. Counts are `[[40, 10], [20, 30]]`. Introduce TN, FP, FN and TP beside their plain-language descriptions after establishing the axes.

**What I want to say:** Thirty B examples were called B: true positives. Ten A examples were called B: false positives. Twenty B examples were called A: false negatives. Forty A examples were called A: true negatives. True or false describes agreement with the observation; positive or negative describes the prediction. There are 100 examples, with 50 from each observed class. Every prediction belongs to exactly one cell.

**Point / transition:** Read the actual/predicted axis labels before naming cells. Keep this matrix in place for the next metric slides.

### S4-04 · How often were we right?

**Slide ID:** `day-1-metrics-accuracy` · **Time:** 92:45–93:30 (0:45)

**What is on slide:** The same matrix with only the two correct cells highlighted: `Accuracy = (30 + 40) / 100 = 70%`.

**What I want to say:** Accuracy is the fraction of all examples assigned the correct class. It is easy to understand, but it treats these two kinds of mistake equally and depends on the class mix. Seventy percent correct does not tell us how many useful B candidates we missed.

**Point / transition:** The diagonal and total. Change the class mix in a separate example.

### S4-05 · A high accuracy can miss every B

**Slide ID:** `day-1-metrics-imbalance` · **Time:** 93:30–94:45 (1:15)

**What is on slide:** A separate 100-marker population with 95 A and 5 B. An Always predict A rule gives `95% accuracy` and `0 of 5 B found`.

**What I want to say:** This is a different constructed population, not a change to our balanced course dataset. If B is rare, always predicting A can look impressive by accuracy while missing every B. The useful question depends on what we need the predictions for. This also explains why a headline score needs the population's class balance. Do not assign a precision value here: with no positive predictions its denominator is zero.

**Point / transition:** The five missed B markers. Return to the original 30/10/20/40 matrix and inspect the B calls.

### S4-06 · How many B calls were right?

**Slide ID:** `day-1-metrics-precision` · **Time:** 94:45–96:15 (1:30)

**What is on slide:** The original matrix, with the Predicted B column highlighted: 30 true positives and 10 false positives. `Precision = 30 / (30 + 10) = 75%`.

**What I want to say:** Of the 40 examples we called B, 30 really are B. Precision answers how trustworthy the positive-call list is in this population. If each selected sequence leads to a follow-up experiment, false positives consume some of that effort. The denominator is predicted positives. We are not yet asking how many of all the B examples we recovered.

**Point / transition:** Trace the highlighted column into its denominator. Next highlight a row instead.

### S4-07 · How many actual B did we find?

**Slide ID:** `day-1-metrics-recall` · **Time:** 96:15–97:45 (1:30)

**What is on slide:** The same matrix, now highlighting the Observed B row: 30 true positives and 20 false negatives. `Recall = 30 / (30 + 20) = 60%`.

**What I want to say:** There were 50 actual B examples and we found 30. Recall measures how much of the positive class we recovered; it is also called sensitivity or true-positive rate. Its denominator is actual positives. Precision and recall share the same numerator but ask about different groups. Both can matter when we prioritize sequences for follow-up.

**Point / transition:** Point to the row denominator, then the missed 20. Give those mistakes a practical consequence.

### S4-08 · Different mistakes have different costs

**Slide ID:** `day-1-metrics-error-costs` · **Time:** 97:45–98:45 (1:00)

**What is on slide:** Two branches from the same prediction workflow: False positive → unnecessary follow-up; False negative → missed candidate. Keep the biological scenario hypothetical.

**What I want to say:** A false positive and a false negative can have very different practical consequences. A small experimental budget may make wasted follow-up costly; an early discovery screen may put more weight on recovering candidates. Neither priority automatically gives a universal best metric. We should state the intended use before choosing how to judge or act on predictions.

**Point / transition:** Follow both branches. Introduce one common summary of precision and recall.

### S4-09 · F1 combines precision and recall

**Slide ID:** `day-1-metrics-f1` · **Time:** 98:45–99:45 (1:00)

**What is on slide:** Precision 0.75 and recall 0.60 feed a single F1 readout: `F1 = 2PR / (P + R) ≈ 0.667`. Reveal the equivalent count form `2TP / (2TP + FP + FN)` in the same space.

**What I want to say:** F1 is their harmonic mean: a low value for either precision or recall pulls the summary down. It is not their ordinary arithmetic average. Here it is two-thirds. It ignores true negatives and does not encode the actual cost of mistakes, so it is a summary with a particular focus rather than an automatic choice for every problem. Understanding what it combines matters more than memorizing the formula.

**Point / transition:** The two inputs and one summary. All these decision metrics depend on where we set the cutoff.

### S4-10 · Move the threshold

**Slide ID:** `day-1-metrics-threshold` · **Time:** 99:45–101:45 (2:00)

**What is on slide:** Fixed probability markers and a movable threshold, with the same confusion matrix updating alongside a compact precision/recall readout. Start at 0.5, then show 0.8 and 0.3. Use one integrated figure; move the readout between states rather than adding three panels. Static fallback uses three successive reveals.

**What I want to say:** No weights or probabilities change here. We only change the rule turning a probability into a call. At 0.5, precision is 75% and recall 60%. At 0.8 we make fewer positive calls: precision is 80% and recall 32% in this example. At 0.3 we recover more positives: precision is about 68.3% and recall 82%. Raising the threshold cannot increase positive-call count or recall on the same records, but precision need not improve at every step. These thresholds illustrate consequences; our recorded course comparison stays at the prespecified 0.5.

**Point / transition:** Move 0.5 → 0.8 → 0.3, then reset to 0.5. Keep the probability ordering in view.

### S4-11 · A ranking comes before a cutoff

**Slide ID:** `day-1-metrics-ranking` · **Time:** 101:45–103:00 (1:15)

**What is on slide:** The same examples sorted by P(B), with actual B and A markers. Remove the decision boundary, then reveal it again without moving any scores.

**What I want to say:** The model gives an ordering as well as a probability estimate. We can ask whether B examples tend to appear above A examples across the list, or ask which examples pass one particular cutoff. These are different properties. A new cutoff changes decisions while preserving the ordering. A ranking score alone does not tell us whether a numerical probability is well calibrated; calibration is outside this short section.

**Point / transition:** One B/A pair, then the entire list. Sweep the cutoff through this fixed ordering to draw a curve.

### S4-12 · Trace the ROC curve

**Slide ID:** `day-1-metrics-roc` · **Time:** 103:00–105:15 (2:15)

**What is on slide:** One ROC plot, built progressively from the threshold sweep. Label vertical axis True-positive rate (recall) and horizontal axis False-positive rate. Start with no positive calls at (0,0), mark threshold 0.5 at `(0.20, 0.60)`, and finish with all calls positive at (1,1). Show the small axis definition `FPR = FP / (FP + TN)` beside the horizontal axis.

**What I want to say:** Recall asks what fraction of B we recover; false-positive rate asks what fraction of actual A we incorrectly call B. At threshold 0.5 these are 30/50 and 10/50. Each threshold gives a point; moving it produces the ROC curve. Toward the upper left means recovering more B with fewer false alarms among A. The diagonal is a chance-ranking reference, not a guarantee that every finite random run lies on it. Tied scores move as a group.

**Point / transition:** Both denominators, then the selected point. Summarize the curve's ranking information with its area.

### S4-13 · Summarize ranking with ROC-AUC

**Slide ID:** `day-1-metrics-auc` · **Time:** 105:15–106:45 (1:30)

**What is on slide:** The same ROC curve with the area underneath shaded and `ROC-AUC = 0.784`. Briefly reveal a randomly selected B/A pair from the persistent score list.

**What I want to say:** Area under the ROC curve summarizes ranking across cutoffs. Equivalently, it measures how often a randomly selected B receives a higher score than a randomly selected A, with half credit for ties. This constructed list gives 0.784; that is not 78.4% accuracy or a result from our fitted DNA model. Perfect separation gives 1 and chance ranking has expected area 0.5. AUC does not choose a useful operating threshold or tell us the cost of errors. ROC-AUC is the course's primary validation comparison metric, chosen before fitting.

**Point / transition:** The area and the B/A pair. Return to the question of how useful the selected candidate list is.

### S4-14 · Keep the positive-call view

**Slide ID:** `day-1-metrics-pr` · **Time:** 106:45–108:15 (1:30)

**What is on slide:** A precision–recall curve from the same predictions: horizontal Recall, vertical Precision, with the 0.5 point at `(0.60, 0.75)`. A single compact readout names Average precision (AP). A gray prevalence reference is at 0.50 for this balanced teaching batch.

**What I want to say:** This view keeps our earlier questions on the axes: how many B did we find, and how many B calls were right? It is especially useful when positives are scarce. Average precision summarizes precision as recall increases, weighting each precision by the recall gained at that score cutoff. We will recognize AP as a supporting number in our reports; no derivation is needed now. It depends on the class mix, so always keep the population in mind. AP is not simply interchangeable with a trapezoidal area under this plot, and neither AP nor ROC-AUC is accuracy at 0.5.

**Point / transition:** The familiar precision/recall point. Keep this as a brief orientation; use the notebook time for the core confusion counts and threshold change. If pacing is tight, explain the axes and defer AP detail to report reading in Section 5.

### S4-15 · Inspect our validation predictions

**Slide ID:** `day-1-metrics-notebook` · **Time:** 108:15–113:15 (5:00)

**What is on slide:** A single practical sequence: Predictions → Confusion counts → Precision / Recall → Change cutoff. Link the [Day 1 notebook on GitHub](https://github.com/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb) and [Open in Colab](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb). Keep executable detail in the notebook and instructor notes.

**What I want to say:** We now apply the same calculations to the actual validation rows from Section 3. Reuse its fitted logistic regression and training-derived count mapping. Produce probabilities for the full validation table once, keep them attached to their observed labels, and calculate the confusion counts at 0.5. Read precision and recall from those counts, then compare them with the library calculation. Change only the cutoff to 0.8 or 0.3 and observe the new counts. The model has not learned anything new. These are exploratory validation decisions; we do not choose an official new threshold or touch test results.

**Point / transition:** Suggested five-minute path: 0:30 identify the validation rows and cached probabilities; 1:00 display the 0.5 matrix; 1:00 calculate and interpret precision/recall; 1:30 change a cutoff and compare counts; 1:00 confirm unchanged scores/ROC-AUC and describe one observed consequence. Working cells and small edits support follow-along. Instructor walkthrough is the equivalent fallback. Setup must already be complete from Section 3; if not, use prepared views within this allocation rather than adding startup time. This checkpoint is implemented as the focused Section 4 cells before the paired workflow.

### S4-16 · What would make this useful in your work?

**Slide ID:** `day-1-metrics-discussion` · **Time:** 113:15–115:00 (1:45)

**What is on slide:** One open prompt: “If you could follow up only a few predictions, what would matter to you?” A small candidate-list visual anchors the discussion.

**What I want to say:** Invite a couple of practical priorities rather than testing recall of formulas. A useful answer may involve missed candidates, follow-up cost, workload or the population we expect to encounter. There is no single correct metric without the intended use. We can now judge predictions; after the break we will try a model that asks a sequence of questions instead of adding weighted counts. It may make different mistakes, and we will compare it using the same validation framework.

**Point / transition:** Listen and connect the contributions to precision, recall or a decision consequence. Take the full **115–125** break. Do not promise that a forest will improve the score.

### Section 4 teaching-source notes

**Timing and priority:** The 16 allocations total **1,500 seconds / 25:00**, including the five-minute guided checkpoint and closing discussion. These are proposed allocations, not measured pacing. Core teaching is confusion counts → precision/recall → threshold consequences → ROC ranking. F1 is one brief summary; precision–recall/AP is orientation and can be shortened to protect the practical. No separate calibration, confidence-interval, regularization, model-complexity, cross-validation or bootstrapping lesson is added here. Sections 2 and 3 already establish development partitions and loss. Training loss guides fitting; these held-out summaries assess predictive behavior.

**Persistent constructed score batch:** Use exactly these score groups for all 100-row matrices, the threshold interaction and ROC/PR calculations. Each group has ten records with the same P(B); all IDs are distinct and scores/labels remain fixed. This is a constructed teaching batch, not the primary simulation's output, not an observed fit and not a continuation assigning truth to Section 3's unlabeled counting sequence. Keep provenance in notes rather than a repeated visible “Illustrative example” banner.

| P(B) | Observed B / 1 | Observed A / 0 |
| --- | --- | --- |
| 0.95 | 8 | 2 |
| 0.85 | 8 | 2 |
| 0.75 | 7 | 3 |
| 0.65 | 7 | 3 |
| 0.45 | 6 | 4 |
| 0.35 | 5 | 5 |
| 0.25 | 4 | 6 |
| 0.15 | 3 | 7 |
| 0.08 | 1 | 9 |
| 0.02 | 1 | 9 |

Call B when `p >= threshold`. Matrix rows are observed `[A, B]` and columns predicted `[A, B]`, matching `confusion_matrix(..., labels=[0, 1])`, so its array is `[[TN, FP], [FN, TP]]`:

| Threshold | TN | FP | FN | TP | Precision | Recall |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8 | 46 | 4 | 34 | 16 | 0.8000 | 0.3200 |
| 0.5 | 40 | 10 | 20 | 30 | 0.7500 | 0.6000 |
| 0.3 | 31 | 19 | 9 | 41 | 0.6833 | 0.8200 |

At 0.5: accuracy = 0.70, F1 = 2/3, FPR = 0.20, TPR = 0.60. Ranking summaries of the fixed scores are **ROC-AUC = 0.784** and **AP = 0.731384126984127**. The latter happens to be close to Section 3's sigmoid example but is an unrelated statistic from different constructed data. Threshold edits do not alter these ranking summaries. Group tied scores together when drawing curves; the no-positive-call endpoint has undefined precision, not precision zero. A plotting library may add a conventional endpoint with precision 1 and recall 0; do not present that as measured precision of an empty selection. The separate always-A example has 95 A / 5 B, matrix `[[95, 0], [5, 0]]`, accuracy 0.95 and recall 0. The actual course generator remains balanced and uses the accepted 15-position PPM with 0.95/0.05 class-conditional planting.

**Implemented notebook path, preserving the current source of truth:** Extend the generated [existing Day 1 notebook](../../notebooks/01_simple_signal.ipynb) through [tools/build_course.py](../../tools/build_course.py), not a second notebook or hand-maintained copy. The finished Section 3 tutorial already defines `s3_classifier`, `s3_x_validation` and `s3_validation`. Its `s3_probabilities` is a two-element class vector for **one row**, so it must not be used as the full batch. The Section 4 cells calculate `s4_probabilities = s3_classifier.predict_proba(s3_x_validation)[:, 1]` once, retain the same validation row order/IDs, then derive `s4_predictions = (s4_probabilities >= s4_threshold).astype(int)`. Begin at 0.5. Unpack `tn, fp, fn, tp = confusion_matrix(s3_validation['label'], s4_predictions, labels=[0, 1]).ravel()`, calculate the denominators and compare with scikit-learn. Handle zero denominators explicitly: teach undefined precision when no positive calls exist even if software uses a zero-division convention. Compute ROC-AUC from probabilities, not thresholded classes, and verify it is unchanged after cutoff edits. No model fit or vectorizer fit belongs in these cells.

The implemented focused cells are placed **after the Section 3 stop and before the combined logistic/forest workflow**, with a clear Section 4 stopping point. The dedicated Section 4 path reuses the fitted logistic model. Its later complete stage 01 cell also fits the forest and remains deferred to Section 5. Reuse the short tutorial's state and defer the complete canonical workflow/report to Section 5. Actual validation counts need not match the teaching matrix. Any prepared fallback must come from the actual named run, or explicitly be the constructed score batch. The Section 4 cells were executed locally; actual hosted Colab execution remains unverified. The [notebook guide](../../notebooks/README.md) owns setup/publication state; classroom use is GitHub ipynb → Colab, with revisions available after the next authorized push.

**Evaluation and interpretation:** Follow [ADR 0002](../../docs/adr/0002-validation-for-development-protected-test-comparison.md): no test results guide any development choice, including representations, preprocessing, model, hyperparameters, metric selection or thresholds. Section 4 uses validation only. The recorded comparison keeps threshold 0.5 and primary metric ROC-AUC, with AP supporting. F1 is taught here but is not currently a field exported by the canonical simple-signal metrics function; do not claim an existing F1 report. Validation performance estimates transfer to held-out rows under the sampled conditions; it is finite-sample evidence, and repeated adaptation to validation can also overfit it. The final frozen Day 3 test comparison remains separate. No past fixed-motif benchmark or assumed model ranking supplies a new primary-task result.

**Sources and review boundary:** Local [simple-signal metric implementation](../../course_code/01_simple_signal.py) and [shared evaluation helpers](../../course_code/course_core.py) determine course behavior. Definition references: scikit-learn [confusion matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html), [precision/recall/F1](https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics), [ROC-AUC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html), and [average precision](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html). Slide IDs now resolve in the actual HTML. The later build request supersedes the earlier story-only scope. No protected test scoring, commit or push was performed.

## 5. What changes with a tree or forest? · 125–155

<a id="section-5"></a>

**Teaching direction approved and implemented — 2026-11-03.** After requesting Section 5 planning, the instructor agreed to all eight summary beats and asked that learning the questions explicitly explain **separation of classes**. This supersedes the earlier wholly unreviewed status. The section contains **20 slides / 30 minutes**, including a five-minute guided notebook comparison; detailed wording and pacing remain editable. The later explicit build request authorized the HTML and notebook implementation now available for review. The existing story remains the only active slide-planning file.

**Story question:** What changes when a model asks a sequence of questions instead of adding weighted counts?

**Exit understanding:** Follow a tree from counts to a leaf probability; explain how feature/threshold questions separate training classes into less mixed groups; explain why tiny leaves can overfit; distinguish bootstrap sampling from random feature selection; explain forest probability averaging; compare the two models on the same held-out validation rows.

**Narrative:** Prediction first → learn the questions → recognize instability → build diverse trees → average their predictions → compare fairly. Now that the audience has seen fitting and evaluation, model complexity has a concrete purpose; it remains outside Section 3. Use the approved short-title/single-visual style, blue/orange class markers, gray context and progressive tree growth. A path interaction supports exploration, with no quiz or correctness score. Inference examples and training examples below are constructed teaching values, with provenance in notes rather than repeated visible disclaimers.

### S5-01 · From one question to a forest

**Slide ID:** `day-1-trees-section` · **Time:** 125:00–125:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** We keep the DNA representation and the evaluation framework. We change how the model turns those counts into a prediction.

**Point / transition:** The title. Bring back the familiar count row.

### S5-02 · Same counts, different model

**Slide ID:** `day-1-trees-counts` · **Time:** 125:15–126:00 (0:45)

**What is on slide:** The established selected counts `TATA = 2`, `AATG = 1`, `CGCG = 3` feed a tree-shaped model box and a P(B) output. Replace the weighted-sum box in place.

**What I want to say:** Logistic regression adds count × weight contributions and converts the score into a probability. A decision tree uses feature questions to send the same input down a path. The numerical representation has not gained any information; the prediction rule is different. The displayed counts are the same constructed sequence example, still without an assigned observed label.

**Point / transition:** The unchanged input. Open the tree box to reveal its first question.

### S5-03 · Ask the first question

**Slide ID:** `day-1-trees-root` · **Time:** 126:00–127:30 (1:30)

**What is on slide:** One root node asks `TATA ≥ 2?`, with clearly labeled Yes and No branches. Show count 2 entering and highlight the Yes branch. Leave the remaining tree concealed.

**What I want to say:** The first rule looks at one feature, not all counts at once. Two satisfies this question, so our example follows Yes. Another example with count one would go the other way. This is applying an already fitted rule; the question does not learn or change because a new sequence arrives.

**Point / transition:** Count, comparison and chosen edge. Follow the next question on that branch.

### S5-04 · The next question depends on the path

**Slide ID:** `day-1-trees-branch` · **Time:** 127:30–128:45 (1:15)

**What is on slide:** Grow the Yes branch into `CGCG < 2?`. The input has CGCG = 3, so highlight No. The earlier No branch from the root already ends at a leaf.

**What I want to say:** Which question we ask next depends on the earlier answer. Our example has three CGCG counts and follows No. Trees combine conditions along paths; a feature can matter in one part of the input space and not another. AATG is available but this small tree never uses it. We have reached a leaf.

**Point / transition:** Trace the two conditions in order. Reveal the training examples that supplied the leaf estimate.

### S5-05 · A leaf gives a probability

**Slide ID:** `day-1-trees-leaf` · **Time:** 128:45–130:15 (1:30)

**What is on slide:** The reached leaf contains four training markers: one B and three A. Reveal `P(B) = 1 / 4 = 0.25`, then a class-A call at the fixed 0.5 threshold.

**What I want to say:** In an ordinary unweighted classification tree, the training class proportions in the reached leaf supply its probabilities. One of these four training examples is B, giving 0.25. The new sequence's unknown label was not used. That fraction is a model estimate, not proof that its probabilities are calibrated or that four examples establish a biological frequency. This constructed tree and the earlier constructed logistic model disagree on this sequence; without its observed label we cannot declare either correct.

**Point / transition:** The one B out of four, then the decision. Try a nearby count row without changing the tree.

### S5-06 · Explore another path

**Slide ID:** `day-1-trees-paths` · **Time:** 130:15–131:30 (1:15)

**What is on slide:** The complete small tree and controls for TATA and CGCG counts. Keep the original 2/3 values as Reset. The other leaves show P(B) = 0.20 and 0.80. One active path and one probability readout update together.

**What I want to say:** Keep TATA at two and change CGCG from three to one: the path now reaches the 0.80 leaf. Then set TATA to one: the first question sends us to 0.20. The changed rows are hypothetical inputs, not new observations for the original sequence. Predictions can jump at split boundaries. These are feature thresholds inside a model; the final probability cutoff of 0.5 remains a separate decision rule.

**Point / transition:** Invite a suggested count change, follow the path and reset. The tree is fixed during this interaction. Now ask how training chose its questions.

### S5-07 · Separate classes with a question

**Slide ID:** `day-1-trees-fitting` · **Time:** 131:30–133:30 (2:00)

**What is on slide:** The constructed training examples appear as blue A / orange B markers on a count-space plot: horizontal TATA count, vertical CGCG count. Reveal a vertical boundary at TATA = 1.5, corresponding to `TATA ≥ 2?`, and shade the two resulting regions lightly. Label their class counts: 1 B / 4 A and 5 B / 4 A. The plot is the focal visual; retain labels and marker shapes as well as color.

**What I want to say:** The points are labeled training examples; their coordinates are two of the counts. We want a question that separates the classes into less mixed groups. This vertical boundary asks about TATA alone: the lower-count side is mostly A, while the other side contains a larger fraction of B. Neither side has to be perfectly pure. During fitting, the tree tries feature thresholds and measures their class separation; a person need not write every question. A question on CGCG would instead make a horizontal boundary. The labels guide these choices, so this is supervised learning, not clustering. This uses training class, not insertion truth, validation labels or test results. The learned model consists of the selected questions, branches and leaf proportions.

**Point / transition:** Point to a class marker, the boundary and the different class mixtures on its two sides. Connect the plot's regions to the tree's two branches. Compare alternative questions using the same parent examples.

### S5-08 · Choose a split that separates classes

**Slide ID:** `day-1-trees-split-quality` · **Time:** 133:30–135:30 (2:00)

**What is on slide:** Reveal two candidate partitions sequentially in the same space, using the same class markers. `AATG ≥ 1?` leaves both children with 3 B / 4 A. `TATA ≥ 2?` produces 1 B / 4 A and 5 B / 4 A. Make the changing class mixtures visually clear before optionally revealing a compact weighted-Gini readout, 0.490 versus 0.432. Gini arithmetic stays in notes; the visible teaching priority is class separation.

**What I want to say:** The first question leaves the same class proportions on both sides, so it gives us no useful class separation. The second makes one side predominantly A and the other richer in B. We prefer this improvement among these two candidate questions, then repeat within the branches to separate further where useful. Gini impurity quantifies how mixed the labels are; less mixed means lower impurity. Weighting by child size prevents treating a tiny pure child as the whole story. We do not need to memorize the formula. Real fitting searches many candidates greedily at each node. This comparison illustrates the criterion; it does not establish that our drawn root is the best among every possible split or globally optimal tree. Noisy or overlapping observations need not admit perfect separation, and forcing tiny pure leaves can overfit.

**Point / transition:** Same parent, then the two alternative partitions. Choose the better of these two candidates and repeat inside each child.

### S5-09 · Repeat within each branch

**Slide ID:** `day-1-trees-grow` · **Time:** 135:30–137:00 (1:30)

**What is on slide:** The constructed tree grows from its root to the CGCG split. Training counts follow their branches: root has 6 B / 8 A; root-No has 1 B / 4 A; root-Yes splits into 4 B / 1 A and 1 B / 3 A. Leaf probabilities appear last.

**What I want to say:** Training repeats the search using only the rows that reached each node. Different branches can choose different questions and finish at different depths. Prediction later follows one path through the completed tree. We can stop growing when limits are reached, a group is pure or no useful valid split remains. A tree's branch questions are learned during fitting, not manually edited for each validation row.

**Point / transition:** Trace training groups into leaves, then the original inference path. What happens if we keep making smaller groups?

### S5-10 · A tiny leaf can memorize a detail

**Slide ID:** `day-1-trees-overfit` · **Time:** 137:00–138:30 (1:30)

**What is on slide:** Zoom into a mixed leaf, then split it into tiny, purer groups. End on a one-example leaf showing a confident probability. A held-out marker remains outside the training group.

**What I want to say:** More questions can make training predictions look cleaner. But a one-example leaf estimates its class proportion from one record, so it may be very confident about an accidental detail. Overfitting means learning training-specific patterns that do not carry over to new examples. A lower training error alone does not establish a more useful predictor. The tiny-leaf picture is conceptual, not a measured training/validation result from our dataset.

**Point / transition:** The shrinking number of supporting examples. Show the simplest ways to limit this behavior.

### S5-11 · Limit how finely the tree divides

**Slide ID:** `day-1-trees-size` · **Time:** 138:30–139:45 (1:15)

**What is on slide:** The same growing tree stops at a depth boundary, then a second reveal keeps a proposed split from making too-small leaves. Label the two controls Maximum depth and Minimum leaf size.

**What I want to say:** Depth limits how many questions a path can ask; minimum leaf size limits how small the supporting training groups become. These are settings we choose before fitting, rather than parameters learned by the split search. Limits can reduce overfitting, but very restrictive limits can miss useful structure. Validation can inform development choices; the test never supplies that feedback. We are explaining the controls, not starting a parameter sweep or changing the recorded course defaults.

**Point / transition:** The stopped branch and retained group. A second difficulty is that small training changes can alter the tree itself.

### S5-12 · Small data changes can change a tree

**Slide ID:** `day-1-trees-instability` · **Time:** 139:45–141:00 (1:15)

**What is on slide:** A training pool is shown with one changed marker; the resulting schematic tree selects a different early split and sends a highlighted input to a different leaf.

**What I want to say:** Some candidate questions can be nearly tied. Changing a few training rows can change an early question and all the branches below it. A deep tree can therefore be unstable. This picture shows a possibility rather than a promised response to every changed row. It motivates combining several different trees instead of depending on just one.

**Point / transition:** The early split and altered path. Expand from one tree to several.

### S5-13 · Build a forest

**Slide ID:** `day-1-trees-forest` · **Time:** 141:00–141:45 (0:45)

**What is on slide:** One training pool feeds three differently shaped trees. Their outputs are present but the combining operation is still concealed.

**What I want to say:** A random forest builds many trees and combines their predictions. Repeating exactly the same tree would add little; we need useful differences between them. We create those differences in two ways: resampling training rows and varying the features considered during split selection.

**Point / transition:** The three different trees. First vary the rows.

### S5-14 · Resample training rows with replacement

**Slide ID:** `day-1-trees-bootstrap` · **Time:** 141:45–143:30 (1:45)

**What is on slide:** A miniature six-row training pool, IDs 1–6, is drawn into a same-sized bag `[1, 1, 3, 4, 4, 6]`; another tree receives `[2, 2, 3, 5, 6, 6]`. Reveal repeated IDs and omitted IDs one bag at a time.

**What I want to say:** Bootstrap sampling draws with replacement: after drawing a row, it remains available for the next draw. Each bag has six draws, so some training rows appear repeatedly and others are absent. The labels travel with their rows. These are resampled observations, not newly generated biological sequences or additional independent evidence. In the course forest, each tree draws a bag from the 720 training rows. Validation and test rows stay outside this sampling pool.

**Point / transition:** A repeated ID and an omitted ID. Explain bootstrapping here as a way to make training bags, without adding a confidence-interval lesson or out-of-bag evaluation detour. Next vary the available questions.

### S5-15 · Vary the features considered at each split

**Slide ID:** `day-1-trees-random-features` · **Time:** 143:30–144:45 (1:15)

**What is on slide:** A grid of k-mer feature names, with one subset highlighted for one node and a different subset highlighted for another node. Each subset feeds a feature/threshold search.

**What I want to say:** At each split, a random forest considers a random subset of candidate features and chooses a useful split among them. It is still using labels to select the question; it is not asking an arbitrary random question. The subset can change from node to node, rather than assigning each tree one permanent list of features. This helps trees differ even when some features are repeatedly strong. The course uses the square-root default for the candidate feature count.

**Point / transition:** The changing subset followed by the fitted question. Now send the same new count row through all trees.

### S5-16 · Average the tree probabilities

**Slide ID:** `day-1-trees-average` · **Time:** 144:45–146:15 (1:30)

**What is on slide:** The same count row enters three trees with outputs 0.25, 0.60 and 0.80. They converge on `P(B) = (0.25 + 0.60 + 0.80) / 3 = 0.55`. Reveal class B at threshold 0.5.

**What I want to say:** Each tree reaches a leaf and supplies its B probability. The scikit-learn forest averages those probabilities, then we apply the final cutoff. This teaching forest gives 0.55. It is not the fraction of trees whose individual hard decision was B: that would be two-thirds here. The first output reuses our small constructed tree; the other two are additional teaching trees. The actual course forest has 100 trees, not three.

**Point / transition:** Three leaf outputs, their mean and the separate decision. Explain what averaging can and cannot improve.

### S5-17 · Different trees can balance out

**Slide ID:** `day-1-trees-aggregation` · **Time:** 146:15–147:15 (1:00)

**What is on slide:** Several tree probability markers and their average on one 0–1 line. Use light individual markers and one clearly labeled mean.

**What I want to say:** Combining trees can reduce the variation caused by relying on a single unstable tree, especially when their errors are not identical. The trees share data and features, so they are not independent. Averaging cannot remove a bias they all share, fix leakage or recover sequence positions discarded by the count representation. Nor does it guarantee better validation performance than logistic regression.

**Point / transition:** The individual outputs and their mean. We need the evaluation framework to see what actually happened.

### S5-18 · Compare on the same examples

**Slide ID:** `day-1-trees-fair-comparison` · **Time:** 147:15–148:30 (1:15)

**What is on slide:** One shared training/validation split and count mapping feed two model boxes: Logistic regression and Random forest. Their outputs join at Same validation rows / Same metrics. A detached gray test box remains closed.

**What I want to say:** To compare models, hold the data generation, split identities, fitted count vocabulary and evaluation rules constant. The training rows fit both models; the same 240 validation rows assess them. Compare validation ROC-AUC as planned, AP as supporting, and precision/recall at the common 0.5 cutoff. A model may rank better yet have a different decision tradeoff at that cutoff. We do not choose which score to emphasize after seeing who wins, or open the test to settle a disappointing comparison.

**Point / transition:** The shared inputs and shared evaluation. Open the existing notebook workflow to inspect the actual comparison.

### S5-19 · Run and read the comparison

**Slide ID:** `day-1-trees-notebook` · **Time:** 148:30–153:30 (5:00)

**What is on slide:** One practical strip: Run paired workflow → Read validation comparison → Inspect one disagreement. Link the [existing Day 1 notebook on GitHub](https://github.com/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb) and its [Open in Colab](https://colab.research.google.com/github/palexiou/ML_Course_2026/blob/main/notebooks/01_simple_signal.ipynb) route.

**What I want to say:** This is the later complete stage 01 workflow that we deferred during Sections 3 and 4. It fits both models under the same defaults and writes their validation outputs. Read the actual two-row comparison and name its split and metric. Then inspect one validation sequence where their 0.5 decisions differ, if one exists. A disagreement is a concrete difference in behavior, not proof that a model is better overall. If no hard decisions disagree, inspect a probability difference instead. We leave feature-importance interpretation for Section 6.

**Point / transition:** Proposed allocation: 1:00 run or open the identified saved paired workflow; 1:00 read ROC-AUC/AP; 1:00 compare precision/recall at 0.5; 1:00 inspect one aligned row; 1:00 discuss one supported conclusion. Running is a guided demonstration or optional follow-along proposal, not a coding-from-scratch exercise. Setup is already complete; use provenance-checked prepared output if execution exceeds the slot. Notebook readback cells are implemented and a paired comparison was executed locally; current evidence is recorded below.

### S5-20 · What changed, and what did not?

**Slide ID:** `day-1-trees-handoff` · **Time:** 153:30–155:00 (1:30)

**What is on slide:** One connected workflow, DNA → Counts → Model → Probability → Evaluation. Highlight only the Model box, then reveal the next prompt: “Which sequence clues are the models using?”

**What I want to say:** We changed the prediction rule from a weighted sum to branching questions and then a forest. We retained the representation and fair evaluation. Both models can make a prediction, and we now have a vocabulary for comparing their behavior. Next we will inspect why a particular sequence received its prediction and which k-mers the models rely on. A score alone does not explain that.

**Point / transition:** The changed model box, then the count features. Continue straight into Section 6 at minute 155; no extra break or homework is added.

### Section 5 teaching-source notes

**Timing and scope:** The 20 allocations sum to **1,800 seconds / 30:00**, minute 125–155, including a proposed five-minute guided comparison. Speaking and exploration pauses are inside the allocations. The course's second break remains 115–125. Detailed Gini mathematics, pruning algorithms, entropy, regression trees, boosting, out-of-bag estimation, bootstrap confidence intervals and hyperparameter sweeps are outside this introductory section. Bootstrap mechanics are included here as recommended during Section 2 review. Unlike Section 3, this section has a concrete reason to introduce flexibility, overfitting and simple size controls. These are explanations, not newly selected course settings. Classroom pacing and Colab runtime remain unverified.

**Consistent constructed tree:** Root asks `TATA ≥ 2?`. No → leaf with 1 B / 4 A, P(B) = 0.20. Yes → `CGCG < 2?`. Yes → leaf with 4 B / 1 A, P(B) = 0.80. No → leaf with 1 B / 3 A, P(B) = 0.25. There are 14 training rows, 6 B / 8 A overall. Query `TATA=2, AATG=1, CGCG=3` therefore reaches 0.25. Changing only CGCG to 1 reaches 0.80; setting TATA to 1 reaches 0.20. The first query reuses the selected counts of the established 21-base sequence; alternate queries are hypothetical count rows, not alterations of that sequence with observed outcomes. There is no empirical class label for this query and no claim that these rules are fitted to the primary PPM dataset.

For reproducible teaching-source arithmetic, the constructed training rows are:

| ID | TATA | AATG | CGCG | Observed class |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | A / 0 |
| 2 | 0 | 0 | 1 | A / 0 |
| 3 | 1 | 0 | 2 | A / 0 |
| 4 | 1 | 1 | 3 | A / 0 |
| 5 | 1 | 0 | 4 | B / 1 |
| 6 | 2 | 0 | 0 | B / 1 |
| 7 | 2 | 0 | 1 | B / 1 |
| 8 | 3 | 1 | 0 | B / 1 |
| 9 | 3 | 1 | 1 | B / 1 |
| 10 | 4 | 0 | 1 | A / 0 |
| 11 | 2 | 1 | 2 | B / 1 |
| 12 | 2 | 1 | 3 | A / 0 |
| 13 | 3 | 1 | 3 | A / 0 |
| 14 | 4 | 1 | 4 | A / 0 |

Gini is `1 − p(A)^2 − p(B)^2`; the root is 24/49 ≈ 0.489796. Candidate `AATG ≥ 1` gives two size-seven groups each 3 B / 4 A, so weighted impurity remains 24/49. Candidate `TATA ≥ 2` gives weighted impurity `(5/14)×0.32 + (9/14)×(40/81) = 136/315 ≈ 0.431746`, an improvement of about 0.058050. This proves only that the second of these two candidates reduces impurity more. Do not claim it is the greedy optimum across every feature/threshold: the complete drawn tree is a teaching construction. Integer questions `TATA ≥ 2` and `CGCG < 2` correspond to model thresholds between counts 1 and 2 (often displayed as `≤ 1.5`, with branch directions adjusted).

**Probabilities and randomness:** The three-tree average is `(0.25+0.60+0.80)/3 = 0.55`, whereas hard-label vote fraction is 2/3. Use probability averaging to match `RandomForestClassifier.predict_proba`, followed by the course's separate fixed threshold. Our simple tree's unweighted leaf ratios are not calibrated confidence statements. In a bootstrapped tree repeated draws contribute their multiplicities to leaf class proportions; a leaf's weighted counts need not equal its unique row count. Bootstrap bags have the same number of draws as their training pool under the course's defaults, with replacement. The six-ID diagram is a separate miniature sampling demonstration, not a replacement of the 14-row tree table or the actual 720-row training set. Random feature subsets are selected per split; an algorithm may inspect more features when necessary to obtain a valid partition. Do not portray each tree as permanently limited to a fixed chosen subset, or the trees as statistically independent.

**Canonical implementation and paired comparison:** The [simple-signal workflow](../../course_code/01_simple_signal.py) uses `RandomForestClassifier(n_estimators=100, random_state=config.seed, n_jobs=2)` with its scikit-learn defaults, including bootstrap sampling, Gini splitting, square-root candidate feature count, no fixed maximum depth and minimum leaf size 1. If the fitted vocabulary has all 256 four-mers, the usual square-root subset has 16 features. The forest uses the same training-fitted vectorizer as logistic regression, and the shared default simulation/split is 1,200 sequences of length 160, 720/240/240 rows, the accepted 15-position strictly positive PPM and planting probabilities 0.95/0.05. Neither model receives IDs, split or planting truth as input. The paired fit was locally rehearsed under the existing defaults; no parameter search or test scoring followed.

The existing generated [Day 1 notebook](../../notebooks/01_simple_signal.ipynb) already has the paired full-workflow call; no new notebook is needed. Classroom execution is the GitHub ipynb opened in Colab. The workflow returns logistic metric values rather than model objects, so reading the forest comparison should use the written artifacts: `simple_signal_output/classical_validation.csv`, `validation_predictions.csv`, `random_forest_validation_predictions.csv` and `experiment_metadata.json`, with `generation.json` binding the current generator/data. All rows must belong to the same named run, settings and generation identity. The complete workflow regenerates its deterministic dataset and fits both models; it does not simply reuse the live Section 3 Python objects. Run it once at this checkpoint, or identify saved output explicitly. Preserve freeze/reveal safeguards. Local unpushed revisions will only be served by the `main` Colab link after the next authorized push; the [notebook guide](../../notebooks/README.md) owns publication/setup state.

For the proposed readback, select method, evaluation split, sample count, ROC-AUC, AP, precision and recall from `classical_validation.csv`, revealing only a few columns at a time. Both rows should say validation with 240 samples and threshold 0.5 under defaults. Pair prediction rows by `sample_id` with a one-to-one join; confirm observed labels agree and the ID sets match before comparing probabilities. The logistic prediction file includes a thresholded prediction; the forest file has probability but no prediction column, so derive its call with `probability >= 0.5`. Read rather than assume the winning model or direction of a metric difference. Coefficient and impurity-importance tables already exist but are reserved for Section 6. Notebook readback cells are implemented after the paired workflow.

**Evidence and review boundary:** The old fixed-motif ROC-AUC values 0.802/0.907 are historical and cannot be reused as results for the new primary generator. A Section 3 logistic-only smoke run does not establish a paired forest result either. The implemented deck uses the identified current paired run in [day1-current.json](../../instructor/verification/day1-current.json). Validation ROC-AUC/AP: logistic **0.608333/0.607054**, forest **0.611875/0.597040**. These are different perspectives on this one run, not evidence of universal superiority. One validation comparison does not establish a universal model ranking or real regulatory activity. Follow [ADR 0001](../../docs/adr/0001-controlled-sequence-classification.md), [ADR 0002](../../docs/adr/0002-validation-for-development-protected-test-comparison.md) and the existing [annotated teaching intent](../teaching-outline.md#day-1). Concept references: scikit-learn [decision trees](https://scikit-learn.org/stable/modules/tree.html) and [random-forest API](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html); canonical source and recorded package versions govern the actual run. Slide IDs now resolve in the HTML. The subsequent build request supersedes the earlier spec-only boundary; no protected test scoring, commit or push was performed.

## 6. Explainability: what did the model learn? · 155–180

<a id="section-6"></a>

**Specification and implementation authorized — 2026-11-03.** The instructor requested this specification and then implementation of the remaining Day 1 slides. This section has 16 focused slides / 25 minutes, including a five-minute guided notebook activity. The implemented content follows the approved style and updates the old fixed-word interpretation to the accepted 15-position probability pattern.

**Story question:** Which sequence clues drive a prediction, and how far does that explanation reach?

**Exit understanding:** Distinguish local contributions from global model summaries; reproduce a logistic prediction with its bias; read directional coefficients and non-directional forest impurity importance; relate actual features to probability-based motif enrichment; recognize correlated features, shortcut signals and the limit of a biological claim.

### S6-01 · Explain the prediction

**Slide ID:** `day-1-explain-section` · **Time:** 155:00–155:15 (0:15)

**What is on slide:** Only the section title.

**What I want to say:** We can compare models. Now ask which sequence clues drive their predictions, and what those clues mean.

**Point / transition:** Move from performance to explanation.

### S6-02 · One prediction or the whole model?

**Slide ID:** `day-1-explain-local-global` · **Time:** 155:15–156:45 (1:30)

**What is on slide:** One selected sequence beside a population of sequences; reveal Local and Global in turn.

**What I want to say:** A local explanation describes this prediction. A global summary describes the fitted model across features or examples. A coefficient and a forest importance answer different questions; neither alone is an explanation of every individual sequence.

**Point / transition:** Point to the single sequence, then the population.

### S6-03 · Count times weight explains a contribution

**Slide ID:** `day-1-explain-contributions` · **Time:** 156:45–158:15 (1:30)

**What is on slide:** The familiar counts and signed contributions: TATA +1.2, AATG +0.8, CGCG −0.6.

**What I want to say:** For this constructed logistic example, each count times its coefficient contributes to the score. Zero count gives zero contribution even when a coefficient is large. These are contributions in score/log-odds units, not independent percentage changes in probability.

**Point / transition:** Trace each count through its multiplication.

### S6-04 · Include the bias and the negative evidence

**Slide ID:** `day-1-explain-score` · **Time:** 158:15–159:15 (1:00)

**What is on slide:** A signed waterfall starts at bias −0.4, adds +1.2, +0.8 and −0.6, and ends at z=1 and p(B)≈0.731.

**What I want to say:** Explain the whole calculation, including the bias and features that lower the score. The sigmoid is nonlinear, so adding 0.6 to the score does not add 0.6 to the probability. This is the existing teaching example, not fitted DNA coefficients.

**Point / transition:** Follow the waterfall from bias to score.

### S6-05 · Coefficients summarize the fitted model

**Slide ID:** `day-1-explain-coefficients` · **Time:** 159:15–160:45 (1:30)

**What is on slide:** A signed coefficient chart from the actual paired run, with the selected words labeled.

**What I want to say:** A positive coefficient raises the B score as that count increases, holding the other features fixed; a negative one lowers it. A coefficient is not a local contribution until multiplied by the count. Use the full fitted vocabulary when reproducing a real prediction.

**Point / transition:** Compare a coefficient with its count-dependent contribution.

### S6-06 · A large coefficient needs context

**Slide ID:** `day-1-explain-coefficient-context` · **Time:** 160:45–162:00 (1:15)

**What is on slide:** The same coefficient is paired with zero and nonzero counts, then two overlapping words share a sequence fragment.

**What I want to say:** Counts vary across rows and k-mers correlate. A fitted coefficient is conditional on the other supplied features and on the fitting settings. Its magnitude is not a standalone biological effect or a universal feature ranking.

**Point / transition:** Point to the zero contribution and overlapping fragment.

### S6-07 · How forests summarize feature use

**Slide ID:** `day-1-explain-forest-importance` · **Time:** 162:00–163:30 (1:30)

**What is on slide:** A nonnegative forest impurity-importance bar chart from the same run.

**What I want to say:** This importance summarizes weighted impurity reductions credited to a feature across fitted trees, normalized by the implementation. It describes global split use, not whether the word raises or lowers P(B). It does not explain one forest prediction by itself.

**Point / transition:** Trace one split to the global summary.

### S6-08 · Importance has limits

**Slide ID:** `day-1-explain-importance-limits` · **Time:** 163:30–164:45 (1:15)

**What is on slide:** A feature-use bar with no positive/negative direction, alongside overlapping k-mer tracks.

**What I want to say:** These importances and linear coefficients have different meanings and scales. Correlated words can share credit. Impurity importance can favor features with more available split choices; it is not a causal effect or proof of TF binding.

**Point / transition:** Keep the missing direction explicit; return to the known simulator.

### S6-09 · Our pattern is a distribution

**Slide ID:** `day-1-explain-probability-pattern` · **Time:** 164:45–166:15 (1:30)

**What is on slide:** The actual 15-position A/C/G/T probability matrix, with one position and several possible bases highlighted.

**What I want to say:** The simulator samples a fresh site from this distribution at each planting. Every word has positive probability, so there is no single fixed word whose membership defines truth. Planting is 0.95 given B and 0.05 given A, and truth is not a model input.

**Point / transition:** Point to multiple possible bases at the same position.

### S6-10 · Which words are enriched by the pattern?

**Slide ID:** `day-1-explain-enrichment` · **Time:** 166:15–168:30 (2:15)

**What is on slide:** One four-base word is aligned against several internal positions of the PPM. Its expected internal-window probability is compared with uniform background 1/256.

**What I want to say:** For each possible internal start, multiply the four position probabilities for that word, then average over the 12 starts. Divide by 1/256 for background enrichment. This is an expected distribution-based clue, not a binary motif-membership flag or the expected whole-sequence count. Boundary windows and class mixtures are outside this summary.

**Point / transition:** Follow multiply → average → background comparison without requiring memorization.

### S6-11 · Compare explanation with the known signal

**Slide ID:** `day-1-explain-signal-comparison` · **Time:** 168:30–170:00 (1:30)

**What is on slide:** A few actual coefficient/importance rows are shown beside their expected word enrichment from the same configuration.

**What I want to say:** Look for agreement and disagreement rather than selecting only convenient words. A strongly used enriched word is consistent with the planted distribution, but overlapping features, finite samples and fitting choices affect which word receives credit. Enrichment alone does not determine the learned sign or importance.

**Point / transition:** Read one actual row without presupposing agreement.

### S6-12 · Overlapping words can share credit

**Slide ID:** `day-1-explain-correlated` · **Time:** 170:00–171:00 (1:00)

**What is on slide:** A short sequence is covered by overlapping four-base windows, with two related feature bars.

**What I want to say:** Neighboring k-mers are correlated because they overlap. Several features can describe parts of the same local pattern, so credit can move between them across fitted models. Do not add importance values and call the result a reconstructed biological mechanism.

**Point / transition:** Trace the shared bases across adjacent windows.

### S6-13 · Could a shortcut explain the prediction?

**Slide ID:** `day-1-explain-shortcut` · **Time:** 171:00–172:00 (1:00)

**What is on slide:** Related sequences cross a training/validation boundary; then whole families remain together.

**What I want to say:** A model can use family identity or batch signals instead of the intended regulatory clue. A new sample ID need not mean a new biological family. This is a brief separate hypothetical example; the primary independent-sequence simulation does not secretly contain those families. The leakage notebook remains an extension, not another full practical here.

**Point / transition:** Connect the transfer question to the split unit, then return to explanation.

### S6-14 · Explain one validation sequence

**Slide ID:** `day-1-explain-notebook` · **Time:** 172:00–177:00 (5:00)

**What is on slide:** A practical strip: Select a row → Inspect contributions → Check the reconstructed probability → Read global summaries. Include the existing GitHub/Open in Colab route.

**What I want to say:** Reuse the Section 3 fitted classifier and count mapping. For one actual validation row, compute all count×coefficient contributions plus bias and verify the resulting sigmoid matches predict_proba. Display the strongest contributions in both directions while retaining the full sum. Then inspect coefficients and forest importance from the paired Section 5 run, including expected internal-window word enrichment. Do not refit or inspect test labels.

**Point / transition:** Allocate 1 minute to select and reconstruct, 2 to explain signed contributions, and 2 to compare one global row and its distribution clue. Instructor demonstration or follow-along fits the same slot.

### S6-15 · Say what the explanation supports

**Slide ID:** `day-1-explain-discussion` · **Time:** 177:00–179:00 (2:00)

**What is on slide:** One open prompt: Which clue mattered here, and what would you still want to check?

**What I want to say:** Invite a description of one observed contribution or global feature and one practical limit. Accept different supported observations; this is discussion, not a metric quiz. An explanation describes the fitted predictor and its data context; causal biological claims require additional evidence.

**Point / transition:** Listen, connect to a model calculation and a biological limitation.

### S6-16 · What if position carries the answer?

**Slide ID:** `day-1-explain-tomorrow` · **Time:** 179:00–180:00 (1:00)

**What is on slide:** DNA → counts → learned prediction → evaluation → explanation, then a sequence with its positions retained points toward Day 2.

**What I want to say:** Today we built a connected workflow and learned to inspect it. Tomorrow we change the representation to retain sequence position and learn local features, while preserving the evaluation framework. Leave space for final questions; no homework.

**Point / transition:** Close Day 1 at minute 180.

### Section 6 teaching-source notes

Use all real model coefficients when reproducing a validation probability. Top-contribution views must retain an explicit remainder or report the verified full sum; the selected three-word teaching example stays separate. Empirical global plots come only from the current named paired training/validation run and its exact generator/configuration. Prefer a small directly labeled chart to an unreadable 256-feature plot. Expected internal-window probabilities average products over 15−4+1=12 starts, then divide by 4⁻⁴ for uniform-background enrichment; all values are positive. This is not whole-sequence expected frequency, class probability or causal evidence. No fixed TATAAATG membership claim survives in the primary interpretation. The separate family-memorization exercise is acknowledged without importing its results into this dataset. SHAP, LIME, permutation experiments and causal attribution are beyond this introductory 25-minute section. Classroom timing and actual Colab execution remain unverified; test labels are never used.

## Delivery and teaching-source notes

The short DNA/weights and 100-example matrix above are constructed teaching values, not fitted results. The count calculation gives 2, 1, 3; z=1 and p≈0.731058579. The short example has no invented observed label. Real course sequences have length 160; the motif simulation demonstrates a controlled signal, not empirical promoter recognition. Keep these origins and limitations in teaching source and detailed notes when adapting the figures.

For execution choices and verified GitHub-to-Colab support, see the [README delivery note](../../README.md#github-notebooks-and-colab). The subsequent cleanup packaged the completed workflows into GitHub notebooks generated from the canonical Python modules. Their setup, definition and execution cells can support either demonstration or follow-along; actual Colab execution remains unverified. The [practical guide](../../instructor/practicals.md) retains the existing inspection cells, scaffold and completed replacements; its slide numbers describe the earlier deck. Demonstration checkpoints above reference those resources without making student execution compulsory or cancelling the historical notebook-delivery agreement.

The instructor authorized the remaining Day 1 build on 2026-11-03 after the section reviews. All six sections now appear in the actual deck: 24 + 18 + 16 + 16 + 20 + 16 slides, plus two break slides = **112**. Dedicated notebook checkpoints cover Sections 3–6. The full generated notebook was run locally with training/validation only; publication, hosted Colab execution and classroom pacing remain separate checks. Keep the [earlier deck guide](previous-teaching-guide.md) as historical implementation evidence; it does not prescribe this draft's timings or slide count.
