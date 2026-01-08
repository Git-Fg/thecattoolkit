# Example: Simple Git Commit

A minimalist git commit command without extensive context loading.

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Objective
Create a commit for current changes.

## Context
Current changes: ! `git status`

## Process
1. Review changes
2. Stage files
3. Create commit

## Success Criteria
- Changes committed successfully
```
