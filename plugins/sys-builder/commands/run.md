---
description: "Execute autonomously (Batch Mode). Human use only."
disable-model-invocation: true
argument-hint: No arguments required - runs with standard assumptions
---

# BATCH RUN
1. **Context**: You are now in Non-Blocking Mode.
2. **Action**: Invoke agent `sys-builder/agents/director` with prompt: "Analyze context and create PLAN.md without user interruption. Make standard assumptions."
3. **Action**: Invoke agent `sys-builder/agents/worker` to execute `PLAN.md`.
