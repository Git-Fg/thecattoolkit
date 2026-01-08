---
description: |
  Shortcut to invoke the project-analysis skill for AI rule synchronization.
  <example>
  Context: User needs to sync AI rules
  user: "Sync our AI rules with the current codebase"
  assistant: "I'll load the project-analysis skill to audit and sync rules."
  </example>
  <example>
  Context: Rules compliance check
  user: "Audit our CLAUDE.md against current practices"
  assistant: "I'll use the sync-rules command for gap analysis."
  </example>
  <example>
  Context: Keeping documentation current
  user: "Update our AI rules to match recent changes"
  assistant: "I'll delegate for AI rules synchronization."
  </example>
allowed-tools: Skill(project-analysis)
argument-hint: [project-path (optional)]
---

Invoke the `project-analysis` skill with sync-rules workflow to: $ARGUMENTS

The skill's sync-rules standard audits AI rule files (CLAUDE.md, etc.) against the current codebase state, identifies discrepancies, and proposes updates.

Reference: `skills/project-analysis/references/sync-rules.md`
