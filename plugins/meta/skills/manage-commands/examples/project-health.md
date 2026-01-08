# Example: Dynamic Environment Loading (Project Health)

Run multiple bash commands to inject project health context.

```markdown
---
description: Check project status
---

## Objective
Provide a comprehensive project health summary.

This helps understand current project state across git, dependencies, and tests.

## Context
- Git: ! `git status --short`
- Node: ! `npm list --depth=0 2>/dev/null | head -20`
- Tests: ! `npm test -- --listTests 2>/dev/null | wc -l`

## Process
1. Analyze git status for uncommitted changes
2. Review npm dependencies for issues
3. Check test coverage
4. Identify potential problems
5. Provide actionable recommendations

## Success Criteria
- All metrics checked
- Current state clearly described
- Issues identified
- Recommendations provided
```
