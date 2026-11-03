# Machine learning for bioinformatics

Four in-person English sessions for master's students, 180 minutes each including breaks. All required work and setup happen during contact time; no homework, grades or submissions.

- **Presentations:** [Slides/index.html](Slides/index.html) links the four independent offline day decks.
- **Plan Day 1:** [editable story](Slides/Day_1/story.md); [approved style and preferences](docs/course-wiki/teaching-preferences.md#style-approved--2026-11-03). Discuss the detailed story, then revise slides section by section.
- **Run the workflows:** [completed GitHub notebooks and Colab links](notebooks/README.md). Four notebooks cover six stages; [course_code/](course_code/) is the canonical Python source.
- **Teach and practice:** [instructor guide](instructor/guide.md), [scaffolded practicals](instructor/practicals.md), [separate answers](instructor/answers.md), and [printable audit checklist](instructor/audit-checklist.html).
- **Evidence and decisions:** [verification](instructor/verification/README.md), [course design history](docs/course-design.md), [dated wiki](docs/course-wiki/index.md), [glossary](GLOSSARY.md), and [ADRs](docs/adr/).
- **Day 4:** [agent workshop](agent_workshop/README.md), retained with genuine run evidence distinct from authored fixtures.

The course moves from k-mer classical models through CNNs and frozen DNA embeddings to agent-assisted analyses. Examples use simulated sequence classification; they do not establish real promoter prediction or a universal model ranking. Development uses validation; the Day 3 freeze and explicitly authorized test reveal are separate actions.

## GitHub notebooks and Colab

Yes—this delivery is agreed. Open the real notebook links/badges in [notebooks/README.md](notebooks/README.md); that is the single setup/runtime/access reference. The repo is private: students need access and Colab authorization. Live hands-on depth remains open; instructor demonstration with optional follow-along is a recommendation. The full runnable workflow and scaffolded exercises remain available. Actual Colab execution, full-session timing, genuine agent recording and the Agentomics demonstration remain unverified or pending as detailed in the verification record.

## Cleanup map · 2026-11-03

| Earlier location | Canonical home / treatment |
| --- | --- |
| `slides/index.html` | `Slides/index.html` navigation plus `Slides/Day_1/presentation.html` through `Day_4/presentation.html`; each contains only its own day. |
| `slides/day1-story.md` | `Slides/Day_1/story.md`, the active story; annotated `slides/teaching-outline.md` moved to `Slides/teaching-outline.md` with identical bytes. |
| `slides/day1-teaching-guide.md`, `slides/pilots/…` | `Slides/Day_1/previous-teaching-guide.md` (historical), `logistic-style-reference.html` (approved reference, not the full Day 1 deck). |
| `slides/qa.md`, `slides/assets/` | `Slides/qa.md`; the existing font is subset and embedded in each day HTML, with license retained in the HTML and `Slides/font-license.txt`. |
| `paste_ready/01…06.py`, its README/manifest | Replaced by four generated `notebooks/*.ipynb` and their metadata source hashes. Dependent stages 03–05 share one notebook; duplicate generated Python copies removed. |
| `course_code/README.md` | Consolidated into `notebooks/README.md`; the eight canonical Python modules and requirement files remain. |
| `instructor/exercises.md`, `instructor/day1-practical.md` | Merged into `instructor/practicals.md`; separate answers and four completed miniature scripts retained. |
| `docs/timed-course-plan.md` | Consolidated into `instructor/guide.md`; course-design interview history and detailed historical Day 1 cues retained. |
| `docs/*verification.md`, `docs/leakage-exercise.md`, `instructor/verification.md` | Grouped in `instructor/verification/`, with `README.md` as evidence index; unique reports retained. |
| `Initial_Chat_Log.txt` | `.scratch/ml-bioinformatics-course/initial-chat-log.txt`, preserved source history. |

The prior layout is also preserved in commit `ea59dd8`. Required agent rules, local issues, source reviews, glossary, accepted ADRs and wiki remain. The unrelated `agent_workshop/` data/code/history remain; only its functional links change if needed. No new archive hierarchy or parallel planning framework was added.
