---
description: "Execute with checkpoints (HITL Mode). Human use only."
disable-model-invocation: true
argument-hint: No arguments required - will prompt for validation at checkpoints
---

# INTERACTIVE RUN
1. **Context**: You are in Human-in-the-Loop Mode.
2. **Action**: Invoke agent `sys-builder/agents/director`.
   - **Instruction**: "Create PLAN.md. STOP and use `AskUserQuestion` to validate the plan before exiting."
3. **Action**: Upon approval, invoke agent `sys-builder/agents/worker` to execute.
