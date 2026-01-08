# Example: Read-Only Analysis

A safe analysis command with no write or execution permissions.

```markdown
---
allowed-tools: [Read, Grep, Glob]
description: Analyze codebase
argument-hint: [search pattern]
---

## Objective
Search codebase for pattern: $ARGUMENTS

This provides safe codebase analysis without modification or execution permissions.

## Process
1. Use Grep to search for pattern across codebase
2. Analyze findings
3. Identify relevant files and code sections
4. Provide summary of results

## Success Criteria
- Pattern search completed
- All matches identified
- Relevant context provided
- No files modified
```
