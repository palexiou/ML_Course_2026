# From language models to coding agents

The [HTML deck](../BioIT_AI_Eng.html) and [teaching story](../BioIT_AI_Eng_story.md)
follow the instructor's six-part sequence. This revision makes the accepted flow
more instructional: definitions, explanations, source examples, and practical
usage replace the earlier sparse, punchy style.

## Current structure: 49 slides

1. How LLMs work (02–08): training versus generation, system/user prompts,
   tokens, next-token generation, context, and the context window. Begin with
   the students' familiar copy-paste workflow.
2. Agents (10–12): an action/result loop, a real read-file command and returned
   coding rule, and a bounded inspection request with completion criteria.
3. Subagents (13–15): focused assignments, separate context, an illustrative
   Claude Code agent configuration, and context-management trade-offs.
4. Skills (17–22): definition, Matt's full grill-me/SKILL.md, annotated metadata
   and instruction body, excerpts from the shared grilling instructions,
   progressive loading, invocation, and optional references/scripts/assets.
5. Harnesses (23–27): the execution/session layer, Claude Code and Codex CLI,
   and T3 Code as an agent harness control surface. Three dedicated T3 slides
   explain starting a session, project/thread/worktree, and inspecting changes.
6. Matt Pocock's skills (29–37): grill-me, the instructor's routing table,
   the full Main Flow, and one slide per skill. A small independent DNA-validation
   example connects specification, ticket, implementation, and review.
7. Scientific coding in practice (39–48): ten explanatory slides follow a
   hypothetical patient-grouped gene-expression analysis. Students learn to state
   the scientific goal, supply relevant context, resolve choices, inspect small
   changes, check the evaluation, use known-answer checks, request run evidence,
   reproduce results, record decisions, and explain their conclusions.
8. Slide 49 contains only **Live Demo on Exercise 10**. No spec, app design,
   feature list, or scripted implementation is included. Develop it live.

Allow roughly 75–80 minutes including a 15-minute demo, or move more quickly through
the terminology for a one-hour session. The new applied section takes about
15 minutes and connects the vocabulary to practical scientific judgement.

## Design and delivery

Match the instructor's [Agentomics reference](../Alexiou_Agentomics_3.html):
white backgrounds, Newsreader serif text, JetBrains Mono labels and code, warm
beige panels with quiet borders, and restrained gold accents. Embedded fonts are
reused from the reference to preserve offline use. Retain explanatory headings
and the existing teaching content; the reference's sparse scientific-talk layout
does not replace the explanatory lesson structure.

`Alexiou_Agentomics_3.html` is a byte-for-byte copy from Downloads. Treat both the
copy and original as read-only. Their SHA-256 checksums were compared before and
after the style work. Define each concept on the slide, then give a concrete
example, comparison, or procedure. Notes add teaching cues and qualifications.

The fixed 1920 × 1080 stage scales uniformly on desktop and phones. All fonts,
styles, scripts, and notes are embedded in one offline HTML file. The next-token
button is explicitly illustrative, with no model call or invented probabilities.
Actual source excerpts and authored examples are labelled separately.

Controls: arrows/Space, Page Up/Down, Home/End, wheel, swipe, and slide picker.
N / Notes opens speaker notes; F toggles fullscreen; E enables text editing;
Escape finishes editing; Ctrl/Cmd+S downloads an edited HTML copy. Autosave has
a new version key to avoid applying text edits from an older slide order.

## Sources and verification

Use AI Hero's dictionary, the corrected mattpocock/skills repository, official
Claude Code and OpenAI skill documentation, T3 Code's own documentation, and
scikit-learn's explanations of data leakage and validation with grouped samples.
The full teaching script and source distinctions are in the story document.

The 48-slide revision passes local Chrome checks at 1280 × 720 and 390 × 844:
16:9 stage fit, content overflow, panel overlap, offline operation, navigation,
notes, token illustration, editing/autosave, export/reopening, and exact demo
text. Rendered screenshots were inspected as well. The displayed Python checks
were executed, including the expected failure for overlapping patient IDs and
the passing check for disjoint IDs. T3's separate HTML preview checker is blocked by the host's
AppArmor configuration; local Chrome provides browser verification.

An earlier Antigravity review covered an older version, not this revision.
Branch: BioIT_AI_Eng. No exercise changes, commits, pushes, deployment, or installs.

## Engagement revision

A native subagent scored all 44 original slides in
[slide-engagement-review.md](slide-engagement-review.md); 25 scored 8 or higher
on a subjective boredom scale. The [redesign map](engagement-redesign-map.md)
connects original critique numbers to the revised 49-slide order.

The revision adds four explanatory, illustrated section breaks (09, 16, 28, 38).
Instructional pages vary among feedback loops, context boundaries, annotated
source and folder diagrams, layered architecture, dialogue, specification and
ticket artifacts, a six-step workflow, scientific sample alignment, paired
patient partitions, an evidence bundle, and a reproducibility path. Native
SVG/HTML/CSS visuals remain crisp and embedded. The white Agentomics typography
and palette remain consistent. Teaching definitions and source distinctions are
retained, and slide 49 still contains only the requested demo title.

## Title slide

Slide 01 adds the Agentomics title composition and the exact original embedded
University of Malta, BioGeMT, and European Union logos. The sole presenter is
Panagiotis Alexiou. The teaching opening now starts at slide 02; the final live
demo is slide 49. Both Agentomics reference files remain unchanged.

The 49-slide version passes the desktop/mobile, offline, navigation, notes,
editing/autosave, export, and exact-demo-text checks. The three title logos load
offline and match the reference images exactly. See [title validation](title-validation.json).
