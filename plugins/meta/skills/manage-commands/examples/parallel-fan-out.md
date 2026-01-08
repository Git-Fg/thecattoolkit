# Example: Parallel Fan-Out

Spawn multiple agents to perform independent tasks in parallel.

```markdown
---
description: Parallel security and performance analysis
argument-hint: [module]
allowed-tools: Task
disable-model-invocation: true
---

Spawn 2 background agents in parallel:
- Agent 1: Analyze $ARGUMENTS for security vulnerabilities
- Agent 2: Analyze $ARGUMENTS for performance bottlenecks

Provide each agent with:
- Specific focus area
- Relevant context
- Expected output format

Synthesize both reports when complete.
```
