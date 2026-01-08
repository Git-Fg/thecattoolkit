---
description: [Personas] Launch parallel background agents for {PURPOSE}.
allowed-tools: Task
argument-hint: [{ARG_HINT_1}] [{ARG_HINT_2}] [{ARG_HINT_3}]
disable-model-invocation: true
---

Spawn {NUMBER} background agents in parallel:

Agent 1: `{AGENT_1_NAME}` agent to handle {TASK_1_DESCRIPTION}
Agent 2: `{AGENT_2_NAME}` agent to handle {TASK_2_DESCRIPTION}
Agent 3: `{AGENT_3_NAME}` agent to handle {TASK_3_DESCRIPTION}

⚠️ **CRITICAL**: Each agent needs exhaustive, self-contained context including:
- Specific task and objectives
- Relevant background information
- Expected output format
- Any constraints or requirements

Report back when all agents complete with synthesized results.

Note: Resource usage scales with parallel agents. Be mindful of system limitations.
