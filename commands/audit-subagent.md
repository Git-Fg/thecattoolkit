---
description: Audit subagent configuration for role definition, prompt quality, tool selection, XML structure compliance, and effectiveness
argument-hint: <subagent-path>
---

## Context

File existence: ! `test -f "$ARGUMENTS" && echo "EXISTS" || echo "NOT_FOUND"`
Git status: ! `git status --short "$ARGUMENTS" 2>/dev/null || echo "NOT_TRACKED"`

## Objective

Invoke the subagent-auditor subagent to audit the subagent at $ARGUMENTS for compliance with best practices, including Markdown structure standards.

This ensures subagents follow proper structure, configuration, Markdown formatting, and implementation patterns.

## Process

1. Invoke subagent-auditor subagent
2. Pass subagent path: $ARGUMENTS
3. Subagent will read best practices and evaluate the configuration
4. Review detailed findings with file:line locations, compliance scores, and recommendations

## Success Criteria

- Subagent invoked successfully
- Arguments passed correctly to subagent
