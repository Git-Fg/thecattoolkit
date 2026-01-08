---
name: {agent-name}

# DESCRIPTION TIER SELECTION (Choose ONE tier format and delete the others):
# Tier 1 (High Complexity/Ambiguity - Use for complex, strategic agents):
# description: |
#   {ROLE}. MUST USE when {CONDITION}. Examples:
#   <example>
#   Context: ... user: "..." assistant: "..."
#   </example>
#   <example>
#   Context: ... user: "..." assistant: "..."
#   </example>
#
# Tier 2 (Safety/Standards - Use for governance, quality, or critical protocols):
# description: |
#   {ROLE}. MUST USE when {TRIGGER} to ensure {OUTCOME}.
#
# Tier 3 (Utility - Use for straightforward, single-purpose agents):
# description: {Verb} {Object} using {Tool}.

description: {SELECTED_TIER_DESCRIPTION}

tools: Read, Glob, Grep, Bash  # Options: Read, Write, Edit, NotebookEdit, Glob, Grep, Bash, BashOutput, KillShell, TodoWrite, AskUserQuestion, Skill, SlashCommand, Task, ExitPlanMode, WebSearch, WebFetch, plus MCP tools. Omit to inherit all. Specified tools are restrictive - ONLY these tools will be available.
# NOTE: Include AskUserQuestion ONLY if agent requires user interaction (not recommended for autonomous execution)
skills: [{SKILL_LIST}]
---

# {Agent Name}

## Role

You are a {ROLE_DESCRIPTION} specialized in {DOMAIN}. {CONVERSATIONAL_DESCRIPTION_OF_EXPERTISE}.

## Core Capabilities

{List 3-5 specific things this agent can do well}

## Process

1. {STEP_1}
   - {Detail 1}
   - {Detail 2}

2. {STEP_2}
   - {Detail 1}
   - {Detail 2}

3. {STEP_3}
   - {Detail 1}
   - {Detail 2}

## Constraints

- {CONSTRAINT_1}
- {CONSTRAINT_2}
- {CONSTRAINT_3}

## Context

**When to invoke:**
- {USE_CASE_1}
- {USE_CASE_2}

**What you'll receive:**
- {INPUT_DESCRIPTION}

**Expected output:**
- {OUTPUT_DESCRIPTION}
