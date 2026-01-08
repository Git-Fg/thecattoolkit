---
description: [VERBS] Delegate to the {AGENT_NAME} agent for {PURPOSE}.
allowed-tools: Task, Read, Glob, Grep
argument-hint: [{ARG_HINT}]
disable-model-invocation: true
---

Task the `{AGENT_NAME}` agent with: $ARGUMENTS

This provides {BENEFIT}.

Important: The context provided to the Agent must be exhaustive and cover all relevant information. It starts with a fully-clean slate, like a child - it's better to give it too much context than not enough.
