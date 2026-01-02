---
description: MUST USE when building prompts that produce outputs for other prompts to consume, or when running multi-stage workflows (research -> plan -> implement). Secondary: creating prompt chains, pipeline workflows, or recursive prompt systems.
argument-hint: <task-description>
allowed-tools: Skill(create-meta-prompts)
---

# Instruction
The user wants to: $ARGUMENTS

1. Immediately invoke the `create-meta-prompts` skill.
2. Pass the user's request ($ARGUMENTS) into the skill invocation.
3. Do not attempt to gather requirements yourself; let the skill handle the intake process.
