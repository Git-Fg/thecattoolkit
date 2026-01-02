---
description: MUST USE when working with SKILL.md files, authoring new skills, or improving existing skills. Secondary: understanding skill structure, learning skill patterns, or auditing skills for best practices.
allowed-tools: Skill(create-agent-skills)
argument-hint: [description of skill to build]
---

# Instruction
The user wants to: $ARGUMENTS

1. Immediately invoke the `create-agent-skills` skill.
2. Pass the user's request ($ARGUMENTS) into the skill invocation.
3. Do not attempt to gather requirements yourself; let the skill handle the intake process.
