---
name: create-meta-prompt
description: Create multi-stage meta-prompts for Claude→Claude pipelines (research → plan → implement). Use when building workflows where outputs feed into subsequent prompts.
argument-hint: <task description>
allowed-tools: [Task]
---

Invoke @prompt-architect with input: $ARGUMENTS

**Meta-Prompt Mode**: The user explicitly wants a Multi-Stage Meta-Prompt workflow.

The subagent will:
1. Skip complexity assessment (user has chosen meta-prompt mode)
2. Use create-meta-prompts skill for chain detection and execution
3. Generate research/plan/do prompts using plan-patterns and research-patterns
4. Create .prompts/ directory structure with SUMMARY.md requirements
