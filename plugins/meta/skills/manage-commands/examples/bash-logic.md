# Example: Bash Logic + Dynamic Context

These examples demonstrate how to combine complex bash logic with dynamic context gathering to create robust, conditional workflows.

## 1. Canonical Git Commit
The production-grade pattern for creating git commits with full repository awareness, branch context, and recent history.

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Objective
Create a git commit for current changes following repository conventions.

## Context
- Current git status: ! `git status`
- Current git diff (staged and unstaged changes): ! `git diff HEAD`
- Current branch: ! `git branch --show-current`
- Recent commits: ! `git log --oneline -10`

## Process
1. Review staged and unstaged changes
2. Stage relevant files with git add
3. Write commit message following recent commit style
4. Create commit

## Success Criteria
- All relevant changes staged
- Commit message follows repository conventions
- Commit created successfully
```

## 2. Conditional Deployment Gate
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
