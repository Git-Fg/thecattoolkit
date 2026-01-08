---
description: |
  [Execution] Orchestrate the creation or audit of a toolkit component (Skill, Agent, Command). Use /expert for ad-hoc maintenance tasks.
  <example>
  Context: User wants to create a component
  user: "Build a new skill for database validation"
  assistant: "I'll orchestrate the creation of a database validation skill using the manage-skills standards."
  </example>
  <example>
  Context: Component audit
  user: "Build audit our agents for compliance"
  assistant: "I'll use the build command to audit agent configurations against standards."
  </example>
  <example>
  Context: Structured component creation
  user: "Build command create new-review"
  assistant: "I'll orchestrate creating a new review command using the manage-commands standards."
  </example>
allowed-tools: Task, Read, Glob, Grep, Skill(manage-skills), Skill(manage-commands), Skill(manage-subagents), Skill(manage-hooks)
argument-hint: [type] [name] [intent]
disable-model-invocation: true
---

# Component Orchestrator

## Analysis

Interpret arguments:
- Type: $1 (skill | agent | command)
- Name: $2
- Intent: $3 (create | audit)

If arguments are missing, use defaults based on the request context.

## Context Gathering

Locate the relevant management skill for the component type:
- If type is `skill`: Consult `manage-skills`
- If type is `agent`: Consult `manage-subagents`
- If type is `command`: Consult `manage-commands`
- If type is `hook`: Consult `manage-hooks`

Identify existing similar components as reference patterns to ensure structural consistency.

## 3. The Envelope (Triangle Phase)

Launch the `plugin-expert` subagent with the following flat semantic structure:

<assignment>
Perform operation '$3' on component '$2' of type '$1'.
</assignment>

<context>
You MUST read and adhere to the architecture and quality standards from the applicable management skill.
Use templates from the skill's assets as your baseline.
</context>

<constraints>
- Work in Background/Async mode if possible.
- NO USER INTERACTION. Assume default values if unspecified.
- Persist all results to disk immediately.
</constraints>

## 4. Report Results

Return the agent's findings to the user with clear explanation of what was accomplished and any relevant findings from the standards application.
