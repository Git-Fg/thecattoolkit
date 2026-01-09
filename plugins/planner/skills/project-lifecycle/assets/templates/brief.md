# Brief Template

## MANDATORY USAGE

**YOU MUST USE THIS TEMPLATE** when creating `.cattoolkit/planning/{project-slug}/BRIEF.md`.

**Scoped Folder:** ALWAYS use scoped project folder `{project-slug}` (e.g., `user-auth-system`)

**Related Files:**
- `@.cattoolkit/planning/{project-slug}/ROADMAP.md` - Project roadmap
- `@.cattoolkit/planning/{project-slug}/ADR.md` - Architecture Decision Records (created by Architect plugin)
- `@.cattoolkit/planning/{project-slug}/ISSUES.md` - Deferred enhancements

## Greenfield Brief (v1.0)

```markdown
# [Project Name]

**One-liner**: [What this is in one sentence]

## Problem

[What problem does this solve? Why does it need to exist?
2-3 sentences max.]

## Success Criteria

How we know it worked:

- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Constraints

[Any hard constraints: tech stack, timeline, budget, dependencies]

- [Constraint 1]
- [Constraint 2]

## Out of Scope

What we're NOT building (prevents scope creep):

- [Not doing X]
- [Not doing Y]
```

## MANDATORY Guidelines

- **MUST** keep under 50 lines
- **MUST** have measurable/verifiable success criteria
- **MUST** define out of scope to prevent "while we're at it" creep
- This is the ONLY human-focused document

## Brownfield Brief (v1.1+)

**YOU MUST** update BRIEF.md to include current state after shipping v1.0:

```markdown
# [Project Name]

## Current State (Updated: YYYY-MM-DD)

**Shipped:** v[X.Y] [Name] (YYYY-MM-DD)
**Status:** [Production / Beta / Internal / Live with users]
**Users:** [If known: "~500 downloads, 50 DAU" or "Internal use only" or "N/A"]
**Feedback:** [Key themes from user feedback, or "Initial release, gathering feedback"]
**Codebase:**
- [X,XXX] lines of [primary language]
- [Key tech stack: framework, platform, deployment target]
- [Notable dependencies or architecture]

**Known Issues:**
- [Issue 1 from v1.x that needs addressing]
- [Issue 2]
- [Or "None" if clean slate]

## v[Next] Goals

**Vision:** [What's the goal for this next iteration?]

**Motivation:**
- [Why this work matters now]
- [User feedback driving it]
- [Technical debt or improvements needed]

**Scope (v[X.Y]):**
- [Feature/improvement 1]
- [Feature/improvement 2]
- [Feature/improvement 3]

**Success Criteria:**
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

**Out of Scope:**
- [Not doing X in this version]
- [Not doing Y in this version]

---

<details>
<summary>Original Vision (v1.0 - Archived for reference)</summary>

**One-liner**: [What this is in one sentence]

## Problem

[What problem does this solve? Why does it need to exist?]

## Success Criteria

How we know it worked:
- [x] [Outcome 1] - Achieved
- [x] [Outcome 2] - Achieved
- [x] [Outcome 3] - Achieved

## Constraints

- [Constraint 1]
- [Constraint 2]

## Out of Scope

- [Not doing X]
- [Not doing Y]

</details>
```

## Brownfield MANDATORY Guidelines

**MANDATORY Triggers for Update:**
- After completing each milestone (v1.0 → v1.1 → v2.0)
- When starting new phases after a shipped version

**Current State MUST capture:**
- What shipped (version, date)
- Real-world status (production, beta, etc.)
- User metrics (if applicable)
- User feedback themes
- Codebase stats (LOC, tech stack)
- Known issues needing attention

**Next Goals MUST capture:**
- Vision for next version
- Why now (motivation)
- What's in scope
- What's measurable
- What's explicitly out

**Original Vision:**
- Collapsed in `<details>` tag
- Reference for "where we came from"
- Shows evolution of product thinking
- Checkboxes marked [x] for achieved goals

This structure makes all new plans brownfield-aware automatically because they read BRIEF and see:
- "v1.0 shipped"
- "2,450 lines of existing Swift code"
- "Users reporting X, requesting Y"
- Plans naturally reference existing files in @context
