---
description: |
  [Execution] Build, audit, or modify toolkit components using natural language. Works for both humans and AI agents.
  <example>
  user: "Build a new skill for database validation"
  user: "Build audit entire plugin from plugins/meta"
  user: "Build audit 'build' slashcommands"
  user: "Build agent update plugin-expert to use new standards"
  </example>
allowed-tools: Task
argument-hint: [natural language request]
disable-model-invocation: false
---

# Natural Language Component Builder

## How It Works

This command uses **natural language** to handle any component operation:
- Human-readable requests
- AI agent-friendly
- Flexible syntax

**The agent will:**
- Parse your natural language request
- Determine what needs to be done
- Check existing state intelligently
- Apply appropriate standards
- Report clear results

## Examples

**Component Creation:**
- "Build a new skill for database validation"
- "Build agent create code-review-assistant"
- "Build command create deploy-with-gate"

**Auditing:**
- "Build audit entire plugin from plugins/meta"
- "Build audit 'build' slashcommands for standards compliance"
- "Build agent audit all agents in plugins/*"
- "Build skill audit manage-* skills"

**Modification:**
- "Build agent update plugin-expert to use new shared standards"
- "Build command update build to support natural language"

## Delegate

Launch the `plugin-expert` subagent with the full request:

$ARGUMENTS

Use your intelligence to parse this request and determine the appropriate action. Apply declarative standards from relevant management skills. Check existing state and only do work that's actually needed.

- Work autonomously
- NO USER INTERACTION
- Use intelligence to interpret natural language

## Report

Return the agent's findings to the user.
