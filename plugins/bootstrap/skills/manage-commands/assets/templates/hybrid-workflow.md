---
description: [Personas] Background agent work with foreground coordination for {PURPOSE}.
allowed-tools: Task, {ADDITIONAL_TOOLS}
argument-hint: [{ARG_HINT}]
disable-model-invocation: true
---

## Objective
{OBJECTIVE_DESCRIPTION}

## Background Task
Spawn a background agent to handle: {BACKGROUND_TASK_DESCRIPTION}

Provide exhaustive context:
- Task objectives and scope
- Relevant project background
- Expected output format

The agent should work asynchronously while you continue with other tasks.

## Foreground Work
While the background agent runs, complete these tasks:
1. {FOREGROUND_TASK_1}
2. {FOREGROUND_TASK_2}
3. {FOREGROUND_TASK_3}

## Synthesis
Once foreground work is complete, retrieve and synthesize the background agent's results with your findings into:
{EXPECTED_OUTPUT_FORMAT}
