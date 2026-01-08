# Example: Single Background Agent

Spawn a background agent to perform analysis without blocking the main session.

```markdown
---
description: Analyze code in background
argument-hint: [path-to-analyze]
allowed-tools: Task
disable-model-invocation: true
---

Spawn a background agent to analyze: $ARGUMENTS

Provide exhaustive context:
- What you're analyzing (e.g., security, performance)
- Scope and boundaries
- Expected output format
```
