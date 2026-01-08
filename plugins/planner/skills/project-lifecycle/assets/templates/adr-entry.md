# ADR Template

**MANDATORY:** Use this format for all Architecture Decision Records.

**Location:** `.cattoolkit/planning/{project-slug}/ADR.md`

## ADR Entry Format

```markdown
# ADR-{NUMBER}: {TITLE}

## Status

{ACCEPTED/SUPERSEDED/DEPRECATED}

## Context

{Business or technical context that prompted this decision}

## Decision

{What we decided to do}

## Options Considered

1. **{OPTION_1}**: {Description}
   - Pros: {Advantage 1}
   - Cons: {Disadvantage 1}

2. **{OPTION_2}**: {Description}
   - Pros: {Advantage 2}
   - Cons: {Disadvantage 2}

## Consequences

**Positive:**
- {Positive outcome 1}

**Negative:**
- {Negative outcome 1}

**Neutral:**
- {Neutral outcome 1}

## Date

{DATE}

## Decision Makers

{WHO_MADE_DECISION}
```

## MANDATORY Rules

- **MUST** use sequential numbering (ADR-001, ADR-002, etc.)
- **MUST** be append-only (NEVER delete entries)
- **MUST** include complete context and rationale
- **MUST** document alternatives considered
- **MUST** update status if superseded (link to new ADR)
