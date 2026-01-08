# Example: Specific Bash Commands

Restrict Bash execution to specific npm scripts like test and lint.

```markdown
---
allowed-tools: Bash(npm test:*), Bash(npm run lint:*)
description: Run project checks
---

## Objective
Run project quality checks (tests and linting).

This ensures code quality while restricting to specific npm scripts.

## Testing
Tests: ! `npm test`
Lint: ! `npm run lint`

## Process
1. Run tests and capture results
2. Run linting and capture results
3. Analyze both outputs
4. Report on pass/fail status
5. Provide specific failure details if any

## Success Criteria
- All tests passing
- No lint errors
- Clear report of results
- Or specific failures identified with details
```
