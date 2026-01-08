# Architecture Decision Records (ADR) Format

## Purpose

Track architectural decisions with context and rationale.

## Template

```markdown
## ADR-XXX: [Decision Title]

**Date:** YYYY-MM-DD
**Phase:** [Phase Name]

### Decision

[What was decided - concise statement]

### Context

**Current task:** [task name]
**Discovery:** [what prompted this]
**Proposed change:** [architectural modification]

### Rationale

[Why this decision was made]

### Alternatives Considered

[Other approaches evaluated]

### Consequences

**Positive:**
- [Expected benefits]

**Negative:**
- [Trade-offs or drawbacks]

**Impact:**
- [What this affects]
```

## Creation Protocol

**When Rule 4 (Architectural Change) applies during execution:**

1. **Auto-increment**: Count existing ADR entries and add 1
2. **Append**: Add to bottom of ADR.md (never delete or modify old entries)
3. **File location**: `.cattoolkit/planning/{project-slug}/ADR.md`

## Numbering

Auto-increment from existing entries:

```bash
# Count existing ADRs
grep -c "^## ADR-" .cattoolkit/planning/{project-slug}/ADR.md

# Next number = count + 1
```

## Append-Only Rule

**Never:**
- Delete old ADR entries
- Modify past decisions
- Reorder entries

**Always:**
- Add new entries at the bottom
- Reference previous ADRs if reversing/updating
- Preserve complete history

## Example

```markdown
## ADR-001: Use PostgreSQL instead of MongoDB

**Date:** 2025-01-08
**Phase:** 01-foundation

### Decision

Use PostgreSQL as the primary database with Prisma ORM.

### Context

**Current task:** Setting up database schema
**Discovery:** Evaluating database options for user authentication system
**Proposed change:** Choose between PostgreSQL and MongoDB

### Rationale

PostgreSQL offers:
- Strong relational data integrity (user sessions must relate to users)
- ACID transactions for critical auth operations
- Better tooling and ecosystem for Prisma
- SQL is more familiar for maintenance

### Alternatives Considered

1. **MongoDB**: Rejected due to weaker relational guarantees
2. **SQLite**: Rejected due to single-writer limitation

### Consequences

**Positive:**
- Strong data integrity for user accounts
- Excellent Prisma support
- Easy to scale vertically

**Negative:**
- Requires separate database server
- More complex setup than SQLite

**Impact:**
- Database configuration in Phase 1
- All data models use relational schema
- Future migrations required for schema changes
```

## When to Create ADR

Create ADR for:

- **Technology stack changes** (frameworks, databases)
- **Major architectural patterns** (auth strategy, state management)
- **Breaking API changes** (protocol changes, data format changes)
- **Infrastructure additions** (caching, message queues)
- **Significant refactors** (directory structure, module organization)

**Do NOT create ADR for:**

- Routine bug fixes
- Implementation details
- Minor optimizations
- Code style preferences
