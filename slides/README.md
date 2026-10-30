# Four-day teaching deck

Open `index.html` in a current browser. The deck uses the original blue/white visual language and a fixed 1920x1080 stage, uniformly scaled and letterboxed on desktop and mobile. The font is local; no CDN or build step is needed. Keep the repository layout for relative exercise and standalone Python links. Serve the repository root, not only `slides/`, when using HTTP.

- Arrow keys, Space, Page Up/Down: previous/next; Home/End: first/last.
- Keys 1-4 or the day selector: jump to a day. Hash links support `#day-3` and `#slide-12`.
- Swipe horizontally or use the throttled mouse wheel to navigate.
- N or Notes: instructor notes, expected answers, transitions, timing, and contingency guidance.
- E or the top-left hover/click area: editable text. Escape exits editing/notes. Edits autosave to this browser; a visible warning appears if storage fails.
- More > Save HTML: export edits into an HTML copy. Keep the copy inside `slides/` with `assets/` so the font and course links resolve. Browser storage is not a repository edit.
- More > Full screen: request browser fullscreen. Print renders one fixed-size slide per page.

Text editing is for wording, not layout changes or code changes. Edited blocks become plain text. Avoid pasting excess text; verify that edited content still fits. Reduced-motion preference disables animations and limits transitions. Only the active slide is exposed to keyboard and assistive-technology navigation; slide changes are announced.

## Teaching and evidence boundaries

60 slides, four 180-minute teaching allocations. They are a teaching plan, not a completed classroom rehearsal. Day 1 starts with ten minutes of in-class access/startup. Every day includes 50-60 and 100-110 breaks. Day 3 freezes with standalone 05 before the explicit instructor-authorized reveal. Day 4 reserves 150-170 for the actual Agentomics demonstration and 170-180 for final discussion.

All reported scores are default **validation** results. There are no test scores in the deck, and creating or viewing slides never executes course code. Frozen label-independent embedding extraction can read and cache test input sequences; that does not authorize test-label access or test-guided selection. Day 4 remains development-only even after a planned Day 3 reveal.

The authored Day 4 fixture is not an observed agent failure. The actual vague and specified runs completed on October 26, 2026; both were scientifically cautious. The vague run used training-only group cross-validation, compared six candidates by log loss, and reported a disclosed TATAAATG motif logistic-regression model (validation ROC-AUC 0.9041667). The specified run reproduced the bag-of-4-mers logistic-regression baseline (0.8019444). Different objectives, features, and search make this unsuitable as a causal prompt-quality comparison. Both used the same provider/model and technical boundary, not a sandbox; the vague run required a technical apply_patch intervention. Their raw reports are linked in the deck. A genuine screen recording, Agentomics access/materials/demo, Colab execution, and full-session rehearsal remain pending. The Agentomics allocation explicitly reports that missing requirement rather than inventing features or claiming a substitute discussion completes the demo.

Primary local references: `../docs/timed-course-plan.md`, `../docs/course-design.md`, `../docs/foundation-embedding-verification.md`, `../instructor/guide.md`, `../agent_workshop/worked-audit.md`, and the actual `../course_code/` contracts. Student links use `../paste_ready/` standalone code, not a notebook interface.

See `qa.md` for browser verification results and limits.
