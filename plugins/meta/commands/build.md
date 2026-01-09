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

## State Check (Idempotency)

Before delegating, check if this operation has already been completed:

1. **Read cache**: Load `.cattoolkit/state/build-cache.json`
2. **Generate operation key**: Create fingerprint from `$1` (type), `$2` (name), `$3` (intent)
3. **Check cache**: Does this key exist with a completion status?
4. **If cached and completed**: Return message: "Operation `$2` ($1) was already completed on [timestamp]. No changes needed."
5. **If not cached**: Proceed with delegation and update cache after completion.

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

## 5. Update Cache (Post-Execution)

After successful completion:

1. **Generate operation key**: Create fingerprint from `$1`, `$2`, `$3`
2. **Update cache**: Append to `.cattoolkit/state/build-cache.json`:
   ```json
   {
     "operations": {
       "operation_key": {
         "type": "$1",
         "name": "$2",
         "intent": "$3",
         "timestamp": "[current timestamp]",
         "status": "completed"
       }
     },
     "lastUpdated": "[current timestamp]"
   }
   ```
3. **Persist**: Save updated cache to disk
