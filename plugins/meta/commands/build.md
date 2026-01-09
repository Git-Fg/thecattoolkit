---
description: |
  [Execution] Orchestrate the creation or audit of a toolkit component (Skill, Agent, Command, Hook).
  <example>
  Context: User wants to create a component
  user: "Build a new skill for database validation"
  assistant: "I'll orchestrate the creation of a database validation skill using the manage-skills standards."
  </example>
allowed-tools: Task, Read, Glob, Grep, Bash, Skill(manage-skills), Skill(manage-commands), Skill(manage-subagents), Skill(manage-hooks), Skill(manage-styles)
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

## Smart Idempotency Check

Before delegating, use intelligent filesystem checks to determine if work is needed:

1. **For 'create' intent:**
   - **Skill**: Check if `plugins/*/skills/$2/SKILL.md` exists and has valid structure
   - **Agent**: Check if `plugins/*/agents/$2.md` exists and has valid YAML frontmatter
   - **Command**: Check if `plugins/*/commands/$2.md` exists and has valid frontmatter
   - **Hook**: Check if `plugins/*/hooks/scripts/$2*` exists
   - **If exists and valid**: Return message: "`$2` ($1) already exists and is valid. No changes needed."
   - **If doesn't exist or invalid**: Proceed with creation/update

2. **For 'audit' intent:**
   - Always proceed (auditing is idempotent by nature)
   - Report current state and findings

3. **For 'update' intent:**
   - Check current state vs requested changes
   - Only update if differences are detected
   - Report what changed or that no changes were needed

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

Return the agent's findings to the user with clear explanation of what was accomplished and any relevant findings from the standards application. Include whether the operation was:
- **Created**: "Created new $2 $1"
- **Already existed**: "$2 $1 already exists and is valid"
- **Updated**: "Updated $2 $1 with [specific changes]"
- **Audited**: "Audit complete for $2 $1 - [findings]"
