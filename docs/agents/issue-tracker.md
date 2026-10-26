# Issue tracker: Local Markdown

Issues and specs live as Markdown files under `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`.
- The spec is `.scratch/<feature-slug>/spec.md`.
- Implementation tickets are separate files:
  `.scratch/<feature-slug>/issues/<NN>-<slug>.md`,
  numbered from `01`, never one combined tickets file.
- Record state with a `Status:` line near the top.
- New implementation-ready specs and tickets use
  `Status: ready-for-agent`.
- Use `docs/agents/triage-labels.md` for other triage states.
- Append comments and conversation history under `## Comments`.

## Publishing and fetching

When a skill says to publish to the issue tracker, create the
appropriate local Markdown file using these conventions.

When a skill says to fetch a ticket, read the referenced local file.
Do not create hosted issues unless the tracker configuration changes.

## Wayfinding operations

- Map: `.scratch/<effort>/map.md`, containing Notes,
  Decisions-so-far, and Fog.
- Child tickets: `.scratch/<effort>/issues/NN-<slug>.md`.
- Record ticket type with `Type: research`, `prototype`,
  `grilling`, or `task`.
- Record dependencies with `Blocked by: NN, NN`.
- A dependency is satisfied when its ticket is `Status: resolved`.
- Claim an open, unblocked ticket by setting `Status: claimed`
  before starting work.
- Resolve it by appending an `## Answer` section, setting
  `Status: resolved`, and adding a summary and link to the map.
