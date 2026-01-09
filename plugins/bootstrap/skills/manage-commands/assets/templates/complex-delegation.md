---
description: [Personas] Launch single or parallel background agents for {PURPOSE}.
allowed-tools: Task
argument-hint: [{ARG_HINTS}]
disable-model-invocation: true
---

## Objective
Delegate to specialized agent(s) in background for: $ARGUMENTS

## Single Agent Pattern
Spawn a background agent to handle the task:
- Agent: `{AGENT_NAME}`

## Parallel Fan-Out Pattern
Spawn multiple background agents in parallel:
- Agent 1: `{AGENT_1_NAME}` to handle {TASK_1}
- Agent 2: `{AGENT_2_NAME}` to handle {TASK_2}

## Context Requirements
⚠️ **CRITICAL**: Background agents start with fresh context. You MUST provide:
- Exhaustive project/codebase context
- Specific objectives and constraints
- Expected output format

Report back when complete.
