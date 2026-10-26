# Domain docs

## Layout

This is a single-context repository:

- `GLOSSARY.md` defines domain terminology.
- `docs/adr/` records consequential decisions.

Preserve the existing glossary and ADRs.

## Before exploring

Read the root glossary and ADRs relevant to the work.

If a root `GLOSSARY-MAP.md` is introduced later, follow it
to the relevant context glossaries and ADRs.

If domain documentation is absent, proceed without requiring
its creation. Domain modeling creates it when terms or
decisions are actually resolved.

## Vocabulary

Use canonical glossary terms in specifications, tickets,
documentation, and tests. Avoid synonyms explicitly discouraged
by the glossary.

If a needed concept is missing, identify the gap rather than
silently inventing competing terminology.

## Decision conflicts

Explicitly flag any proposal that conflicts with an existing
ADR. Do not silently override an accepted decision.
