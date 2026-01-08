# Example: Conditional Deployment Gate

Deploy only if automated tests pass using conditional execution.

```markdown
---
description: Deploy if tests pass
allowed-tools: Bash(npm test:*), Bash(npm run deploy:*)
---

## Objective
Deploy to production only if all tests pass.

This ensures deployment safety through automated testing gates.

## Context
Test results: ! `npm test`

## Process
1. Review test results
2. If all tests passed, proceed to deployment
3. If any tests failed, report failures and abort
4. Monitor deployment process
5. Confirm successful deployment

## Success Criteria
- All tests verified passing
- Deployment executed only on test success
- Deployment confirmed successful
- Or deployment aborted with clear failure reasons
```
