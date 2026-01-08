---
description: [Personas] Delegate to the {AGENT_NAME} agent in background for {PURPOSE}.
allowed-tools: Task
argument-hint: [{ARG_HINT}]
disable-model-invocation: true
---

Spawn a background agent to handle: $ARGUMENTS

Delegate to the `{AGENT_NAME}` agent with exhaustive context.

This provides {BENEFIT} while you continue working.

⚠️ **CRITICAL**: The context provided to the Agent must be exhaustive and cover all relevant information. Background agents start with fresh context and cannot easily ask for clarification.

Include in the task:
- What you're trying to achieve
- Relevant background about the code/project
- Specific focus areas or concerns
- Expected output format

The agent should work asynchronously and report back when complete.
