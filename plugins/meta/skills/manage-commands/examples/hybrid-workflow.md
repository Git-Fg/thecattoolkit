# Example: Hybrid Workflow (Foreground + Background)

Run a quick foreground review while a deep background analysis processes.

```markdown
---
description: Quick review while deep analysis runs
argument-hint: [path]
allowed-tools: Task
---

Spawn a background agent to deeply analyze: $ARGUMENTS
Focus on: architecture patterns, dependencies, code quality

While it runs, do a quick review of:
- Main entry points
- Error handling
- Obvious issues

When background analysis completes, synthesize both findings.
```
