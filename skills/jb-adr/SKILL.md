---
name: jb-adr
description: "Create and manage Markdown Architectural Decision Records (MADR). Use when documenting software design choices, tech stack decisions, architecture changes, or any decision that impacts code structure. Triggers on: 'adr', 'architectural decision', 'decision record', 'madr', 'design decision', 'tech decision', 'architecture decision'."
---

# MADR - Markdown Architectural Decision Records

Create structured ADRs to document important design decisions for coding projects.

## Quick Start

1. **Create new ADR**: Use template below in `docs/adr/`
2. **Name format**: `NNNN-title.md` (e.g., `0001-use-postgres.md`)
3. **Link from README**: Add to ADR index

## ADR Template (Minimal)

```markdown
# Title

## Status
Proposed | Accepted | Deprecated | Superseded by [NNNN](./NNNN-new-decision.md)

## Context
What is the issue motivating this decision?

## Decision
What is the change being proposed?

## Consequences
What becomes easier or harder because of this change?
```

## Full Template

For complex decisions, use the full template from `references/full-template.md`:
- Includes Options considered, Pros/Cons, Related decisions
- Load with: `read references/full-template.md`

## Naming Convention

- Use 4-digit numbering: `0001`, `0002`, ...
- Lowercase hyphenated titles
- Example: `0003-select-database.md`

## Best Practices

- One ADR per decision
- Write for future developers (explain why)
- Include pros/cons of options considered
- Link related ADRs
- Update status when superseded

## File Location

Store in `docs/adr/` or `adr/` at project root.
