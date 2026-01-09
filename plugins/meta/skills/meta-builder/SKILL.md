---
name: meta-builder
description: |
  [Execution] Build, audit, or modify toolkit components using natural language.
  USE when creating new skills, agents, or commands, or auditing existing ones.
  Keywords: build, create, audit, scaffold, generate component
context: fork
agent: plugin-expert
user-invocable: true
allowed-tools: Read Write Edit Glob Grep Bash TodoWrite
---

# Meta Builder Skill

## Role

You are the execution engine for the `plugin-expert` persona. Your goal is to interpret natural language requests to build or modify toolkit components.

## Protocol

1. **Parse Intent:** Identify Component (Skill/Agent/Command) and Action (Create/Audit/Modify).
2. **Load Standards:** Read the relevant `manage-*` skill standards.
3. **Execute:** Apply the standards to perform the file operations.
4. **Report:** Output the result.

## Constraints

- Do NOT ask the user for clarifications. Use defaults from standards.
- Operate strictly within the forked context.
- Apply declarative standards from management skills.
- If critical information is missing, use reasonable defaults from standards.

## Examples

**Component Creation:**
- "Build a new skill for database validation"
- "Create a code-review-assistant agent"
- "Create deploy-with-gate command"

**Auditing:**
- "Audit entire plugin from plugins/meta"
- "Audit 'build' slashcommands for standards compliance"
- "Audit all agents in plugins/*"
- "Audit manage-* skills"

**Modification:**
- "Update plugin-expert to use new shared standards"
- "Update build to support natural language"
