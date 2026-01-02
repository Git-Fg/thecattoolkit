---
description: MUST USE when creating specialized AI agents, setting up delegation tools, or configuring autonomous workers. Secondary: learning agent architecture, understanding tool restrictions, or optimizing agent prompts.
argument-hint: [agent idea or description]
allowed-tools: Skill(create-subagents)
---

# Instruction
The user wants to: $ARGUMENTS

1. Immediately invoke the `create-subagents` skill.
2. Pass the user's request ($ARGUMENTS) into the skill invocation.
3. Do not attempt to gather requirements yourself; let the skill handle the intake process.
