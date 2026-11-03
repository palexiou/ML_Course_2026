# Machine learning for bioinformatics

Four in-person English sessions for master's students: Monday-Thursday, 180 minutes each including breaks. All required work and setup happen during contact time; no homework, grades, or submissions.

## Start here

- **Code to paste into Colab:** [paste_ready/README.md](paste_ready/README.md). Six complete scripts; arrange cells manually as preferred.
- **Teaching and timing:** [instructor/guide.md](instructor/guide.md), [exercises](instructor/exercises.md), and [completed answers](instructor/answers.md).
- **Slides:** [slides/index.html](slides/index.html). Open the self-contained HTML file in a browser.
- **Plan the Day 1 story:** [six-section discussion draft](slides/day1-story.md); [approved style and instructor preferences](docs/course-wiki/teaching-preferences.md#style-approved--2026-11-03). Revise slides section by section after discussing the story.
- **Scientific audit:** [one-page printable checklist](instructor/audit-checklist.html) and [Day 4 agent kit](agent_workshop/README.md).
- **What actually passed:** [instructor/verification.md](instructor/verification.md). Local runs are distinguished from pending Colab, classroom live-agent, Agentomics, and classroom checks.
- **Canonical source and dependencies:** [course_code/README.md](course_code/README.md). Generated datasets, saved outputs, model checkpoints, and real embedding caches are in local ignored output directories, not inside the scripts.

The narrative moves from 4-mer logistic regression and random forest, through one-hot CNNs and frozen pretrained DNA embeddings, to specifying and auditing agent-assisted analyses. These are controlled simulated sequence-classification examples, not real promoter discovery or a promised model ranking. Test scores stay protected during development; Day 3 freeze and reveal are separate explicit actions.

Actual Colab verification and notebook presentation are the instructor's manual handoff. Actual agent run recordings and Agentomics access/materials must be supplied before claiming those demonstrations have been rehearsed. No authored fixture is represented as a recorded run.

## GitHub notebooks and Colab

Yes: completed `.ipynb` notebooks versioned in GitHub can open directly in Colab. Google's [GitHub integration example](https://colab.research.google.com/github/googlecolab/colabtools/blob/main/notebooks/colab-github-demo.ipynb) documents the URL and badge; its [FAQ](https://research.google.com/colaboratory/faq.html) explains storage and temporary runtimes. Checked 2026-11-03. Use `https://colab.research.google.com/github/OWNER/REPO/blob/BRANCH/path.ipynb`, encoding spaces and other special characters in each path component (retain directory slashes).

This checkout and tracked tree contain **no `.ipynb` files** as of the 2026-11-03 inventory, so there is no course notebook launch link to add yet. Existing completed workflows are [01_simple_signal.py](paste_ready/01_simple_signal.py), [02_split_leakage.py](paste_ready/02_split_leakage.py), and the [remaining paste-ready scripts](paste_ready/README.md). A `.py` URL is not a notebook launch URL. Recommended eventual delivery: completed GitHub notebooks with a Colab badge, alongside the retained scaffolded exercises. Notebook packaging and compulsory live follow-along remain undecided; the new proposal is instructor demonstration first, with optional follow-along.

Opening a GitHub notebook creates an editable view without overwriting its source. Run the setup and data-loading cells; save a copy in Drive to retain edits, or explicitly save to GitHub with write authorization. The execution VM and its local files are temporary. Opening a notebook does not clone its repository or provide adjacent data files: relative paths need an explicit download/clone/upload or generation step and a known working directory.

Concrete setup gaps from reading the existing scripts and [practical cells](instructor/day1-practical.md): Day 1 code 01 generates `simple_signal_output/` and fits both models before the later inspection cells can run; code 02 writes the separate `course_output/leakage/` experiment. Days 2–3 reuse `course_output/`, with generated datasets/models/caches ignored by Git. The first Day 3 encoder load downloads roughly 224 MB of weights plus dependencies; package compatibility and runtime persistence need rehearsal. Steps 3–5 must retain their shared files, and step 05 freezes before any separately authorized test reveal. No expensive workflow or test scoring was run for this documentation check.

The configured repository is `palexiou/ML_Course_2026`, branch `main`; authenticated GitHub metadata on 2026-11-03 reports it as **private**. Students need repository access and must authorize Colab to include private repositories, as Google's example explains. No repository visibility change is implied. Direct opening support is verified from documentation; end-to-end course execution in Colab is untested.
