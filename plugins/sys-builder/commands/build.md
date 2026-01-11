---
description: "Shortcut: Execute the current phase in ROADMAP.md."
argument-hint: "<optional phase name>"
allowed-tools: [Skill(manage-planning), Task]
disable-model-invocation: true
---

# Build Orchestrator

Invoke `manage-planning` in **Execution Protocol**.

**Goal:** Read the active plan and dispatch `worker` agents to implement it.

**Execution Logic:**
1. Load ROADMAP.md and identify active phase
2. Check for HANDOFF.md to resume interrupted work
3. Execute simple tasks (<3 files) inline in main thread
4. Delegate complex tasks to `worker` agents
5. Verify results and update state

**Constraint:** Do not ask for permission between tasks unless the plan explicitly requires it. Execute in Uninterrupted Flow.
