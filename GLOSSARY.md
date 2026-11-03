# Machine Learning for Bioinformatics

Terminology for the course and its teaching activities.

## Language

**Course dataset**:
The collection of simulated DNA sequences, classification labels, and known ground truth used for the course's sequence-classification task, including its controlled variants.
_Avoid_: Chromosome-scanning dataset when referring to the core task

**Dataset variant**:
A controlled version of the course dataset designed to expose a particular sequence signal or evaluation failure while retaining the same sequence-classification framing.
_Avoid_: Unrelated biological task when referring to a controlled version

**Scaffolded practical**:
A course activity in which students run working notebooks, complete selected missing code, and interpret results rather than implement an entire analysis from scratch.
_Avoid_: Coding-from-scratch exercise when referring to this activity

**Scientific audit**:
An examination of whether an analysis answers the intended question with valid evaluation and supported conclusions, rather than merely producing working code.
_Avoid_: Code execution check when referring to scientific validity

**Primary motif PPM (position probability matrix)**:
The position-specific base probabilities defining the variable regulatory pattern in the primary course dataset; each planted site is an independent sequence sampled from that distribution. “PWM” is informal course shorthand here; a technical position weight matrix contains log-odds scores relative to a background distribution.

**Planted site**:
A sequence deliberately inserted by the simulator, with a known insertion position. Planting truth records the generating event, not a consensus match or a motif-scan threshold.
