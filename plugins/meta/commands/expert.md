---
description: |
  [Personas] General delegation for system maintenance. Applies declarative standards to fix or refactor AI components.
  <example>
  Context: User needs infrastructure maintenance
  user: "Expert audit our plugin configuration"
  assistant: "I'll delegate to the plugin-expert to audit the infrastructure using applicable standards."
  </example>
  <example>
  Context: Ad-hoc technical task
  user: "Expert fix our agent frontmatter"
  assistant: "I'll use the expert command for agent metadata fixes using manage-subagents standards."
  </example>
  <example>
  Context: System troubleshooting
  user: "Expert why our hooks aren't triggering"
  assistant: "I'll delegate for hook troubleshooting using manage-hooks standards."
  </example>
allowed-tools: Task, Read, Glob, Grep, Skill(manage-skills), Skill(manage-commands), Skill(manage-subagents), Skill(manage-hooks), Skill(manage-styles)
argument-hint: [task description]
disable-model-invocation: true
---

# Expert Delegation Orchestrator

## Analysis

Interpret the request: $ARGUMENTS

If intent or target component is ambiguous, make reasonable assumptions based on context.

## Context Gathering

Map the relevant management skill and locate the target component if specified. Search through existing `plugins/meta/skills/` to identify the authoritative standards for the requested task.

## 3. The Envelope (Triangle Phase)

Launch the `plugin-expert` subagent with the following flat semantic structure:

<assignment>
Refactor or fix the component based on: $ARGUMENTS
Work autonomously. If blocked, create HANDOFF.md and terminate.
</assignment>

<context>
Directly consult the applicable management skill for standards.
Examine the target component configuration and current implementation.
</context>

<constraints>
- NO USER INTERACTION.
- If blocked, create HANDOFF.md and terminate.
- Use relative paths from skill root for internal references.
- Preserve atomic independence of all components.
</constraints>

## 4. Report Results

Return the agent's findings with:
- What was accomplished
- Standards applied
- Issues found and fixed
- Any HANDOFF.md created
