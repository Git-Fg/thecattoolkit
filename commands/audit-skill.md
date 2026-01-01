---
description: Audit skill for YAML compliance, pure XML structure, progressive disclosure, and best practices
argument-hint: <skill-path>
---

## Context

Skill files: ! `find "$ARGUMENTS" -name "*.md" -type f | head -20`
Git status: ! `git status --short "$ARGUMENTS" 2>/dev/null || echo "NOT_TRACKED"`

## Objective

Invoke the skill-auditor subagent to audit the skill(s) at $ARGUMENTS for compliance with Agent Skills best practices.

This ensures skills follow proper structure (pure XML, required tags, progressive disclosure) and effectiveness patterns.

This ensures referenced files follow proper structure and effectiveness patterns.

This ensures files from the Skill(s) folder are properly integrated and referenced with relative path within the Skill(s) markdown file.

## Process

1. Invoke skill-auditor subagent
2. Pass skill path: $ARGUMENTS
3. Subagent will read best practices and evaluate the skill
4. Subagent checks all related files in skill directory
5. Review detailed findings with file:line locations and recommendations

## Success Criteria

- Subagent invoked successfully
- Arguments passed correctly to subagent
- Audit includes XML structure evaluation
- Audit includes actionable suggestions
