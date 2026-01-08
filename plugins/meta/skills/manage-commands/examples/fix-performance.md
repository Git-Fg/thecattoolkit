# Example: Analysis -> Action (Chained)

A sequential command that performs analysis and then implements fixes.

```markdown
---
description: Analyze and fix performance issues
argument-hint: [file-path]
---

## Objective
Analyze and fix performance issues in @ $ARGUMENTS.

This provides end-to-end performance improvement from analysis through verification.

## Process
1. Analyze @ $ARGUMENTS for performance issues
2. Identify top 3 most impactful optimizations
3. Implement the optimizations
4. Verify improvements with benchmarks

## Verification
Before completing:
- Benchmarks run showing performance improvement
- No functionality regressions
- Code quality maintained

## Success Criteria
- Performance issues identified and fixed
- Measurable performance improvement
- Benchmarks confirm gains
- No regressions introduced
```
