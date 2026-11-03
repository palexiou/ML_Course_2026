# Four-day teaching deck

Open `index.html` in a current browser. The deck uses the original blue/white visual language and a fixed 1920x1080 stage, uniformly scaled and letterboxed on desktop and mobile. The font is local; no CDN or build step is needed. Keep the repository layout for relative exercise and standalone Python links. Serve the repository root, not only `slides/`, when using HTTP.

- Arrow keys, Space, Page Up/Down: previous/next; Home/End: first/last.
- Keys 1-4 or the day selector: jump to a day. The slide selector jumps by title. Hash links support `#day-3`, a stable day-local address such as `#day-1-slide-29`, and global addresses such as `#slide-12`.
- Swipe horizontally or use the throttled mouse wheel to navigate.
- N or Notes: instructor notes, expected answers, transitions, timing, and contingency guidance.
- E or the top-left hover/click area: editable text. Escape exits editing/notes. Edits autosave to this browser; a visible warning appears if storage fails.
- More > Save HTML: export edits into an HTML copy. Keep the copy inside `slides/` with `assets/` so the font and course links resolve. Browser storage is not a repository edit.
- More > Full screen: request browser fullscreen. Print renders one fixed-size slide per page.

Text editing is for wording, not layout changes or code changes. Edited blocks become plain text. Avoid pasting excess text; verify that edited content still fits. Reduced-motion preference disables animations and limits transitions. Only the active slide is exposed to keyboard and assistive-technology navigation; slide changes are announced.

## Teaching and evidence boundaries

106 slides: 62 for Day 1, 15 for Day 2, 15 for Day 3, and 14 for Day 4. Four 180-minute teaching allocations remain a plan, not a completed classroom rehearsal. Day 1 opens with the course, instructor, outcomes, and in-class notebook startup. Every day includes 50-60 and 100-110 breaks. Day 3 freezes with standalone 05 before the explicit instructor-authorized reveal. Day 4 reserves 150-170 for the actual Agentomics demonstration and 170-180 for final discussion.

## Narrative and teaching detail

Day 1 was expanded from the instructor's comments in [teaching-outline.md](teaching-outline.md). The annotated outline is preserved. The matching [Day 1 teaching guide](day1-teaching-guide.md) supplies the new slide sequence, timings, explanations, class questions, expected answers, and transitions. The [Day 1 notebook instructions](../instructor/day1-practical.md) make the switches to Colab explicit and provide the actual inspection, fitting, and interpretation cells.

Most Day 1 explanation slides take one to three minutes. Practical slides stay up while students work. A ten-minute topic therefore spans several visible teaching steps. The opening introduces Panagiotis Alexiou, ERA Chair at the University of Malta, before the biological example. The lesson has separate learning-problem slides, a worked logistic-regression sequence, individual metric definitions, and a gradual introduction to the related-sequence investigation.

Three local interactive examples support the explanations:

- Day 1 slide 29: vary the linear score and inspect the sigmoid probability.
- Day 1 slide 39: move a threshold across 100 illustrative scores and inspect the error counts and metrics.
- Day 1 slide 44: choose feature counts and follow an illustrative decision tree one split at a time.

These examples use declared teaching values; they do not run course models or alter the course's threshold policy. The metric dashboard, confusion matrix, and threshold demonstration all use the same example (TP 30, FP 10, FN 20, TN 40 at threshold 0.5). Interaction controls work with the mouse or keyboard; slide navigation does not intercept input-field arrow keys.

The overall four-day progression is:

1. Learn the ML vocabulary, build classical predictors, and interpret their evaluation.
2. What if our features hide the answer?
3. Can a pretrained model give us better features?
4. What changes when an agent runs the experiment?

Scenes move from a question to a prediction, experiment, and result. Keep the question on screen while students discuss; open linked code when it is time to run the experiment. Result charts show recorded local validation ROC-AUC on a common zero-to-one axis. Three decimal places are display rounding; the full recorded values remain in the technical reference.

Press **N** or select **Notes** for instructor guidance. Day 1 gives **Say / explain**, **Ask the class**, **Expected answer**, and **Next slide** cues where applicable. Days 2–4 retain expandable **Technical reference** sections with detailed explanations, equations, model settings, caveats, and activity instructions. Notes are excluded from slide printing. Arrow keys scroll the notes rather than changing the slide; N or Escape returns to the presentation.

Day-local slide numbers appear in the header and slide selector. Global slide numbers shifted when Day 1 expanded; use day-local links for new references. This edition uses a new local-edit storage key so edits to the earlier 60-slide deck cannot overwrite unrelated new text. Keep an exported copy of any older browser edits you need.

All reported scores are default **validation** results. There are no test scores in the deck, and creating or viewing slides never executes course code. Frozen label-independent embedding extraction can read and cache test input sequences; that does not authorize test-label access or test-guided selection. Day 4 remains development-only even after a planned Day 3 reveal.

The authored Day 4 fixture is not an observed agent failure. The actual vague and specified runs completed on October 26, 2026; both were scientifically cautious. The vague run used training-only group cross-validation, compared six candidates by log loss, and reported a disclosed TATAAATG motif logistic-regression model (validation ROC-AUC 0.9041667). The specified run reproduced the bag-of-4-mers logistic-regression baseline (0.8019444). Different objectives, features, and search make this unsuitable as a causal prompt-quality comparison. Both used the same provider/model and technical boundary, not a sandbox; the vague run required a technical apply_patch intervention. Their raw reports are linked in the deck. A genuine screen recording, Agentomics access/materials/demo, Colab execution, and full-session rehearsal remain pending. The Agentomics allocation explicitly reports that missing requirement rather than inventing features or claiming a substitute discussion completes the demo.

Primary local references: `../docs/timed-course-plan.md`, `../docs/course-design.md`, `../docs/foundation-embedding-verification.md`, `../instructor/guide.md`, `../agent_workshop/worked-audit.md`, and the actual `../course_code/` contracts. Student links use `../paste_ready/` standalone code, not a notebook interface.

See `qa.md` for browser verification results and limits.
