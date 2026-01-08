# Example: Git-Only Command (Restricted)

A secure command that only allows specific git operations using tool restrictions.

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git commit:*)
description: Git workflow command
---

## Objective
Perform git operations safely with tool restrictions.

This prevents running arbitrary bash commands while allowing necessary git operations.

## Context
Current git state: ! `git status`

## Process
1. Review git status
2. Perform git operations
3. Verify changes

## Success Criteria
- Git operations completed successfully
- No arbitrary commands executed
- Repository state as expected
```
