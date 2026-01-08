# Example: Commit with Full Context

Create a git commit that is aware of the current repository state, recent history, and diffs.

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
