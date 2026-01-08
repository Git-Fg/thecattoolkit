# Example: Staged Background Work

Sequential background tasks with dependencies.

```markdown
---
description: Research then document
argument-hint: [topic]
allowed-tools: Task
---

Stage 1: Spawn background agent to research: $ARGUMENTS
Wait for completion.

Stage 2: Using research findings, generate documentation
```
