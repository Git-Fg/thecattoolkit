---
name: sys-builder-core
description: "Core methodology and routing logic for Sys-Builder. PROACTIVELY Use when analyzing complex engineering tasks to determine the appropriate execution pattern. Auto-activates on 'plan', 'architect', 'refactor', 'audit'."
context: fork
agent: director
---

# Sys-Builder Methodology

## 1. Analyze
Before acting, classify the request:
- **Atomic**: Simple fix? -> Do it directly.
- **Complex**: Architecture/Refactor? -> Use the **Director/Worker** pattern.

## 2. Routing (The "Buttons")
Do not execute heavy workflows yourself. Instruct the user to run the appropriate command:

- **For Autonomous Execution (Batch)**:
  > "I have analyzed the requirements. Please run `/sys-builder:run` to execute this autonomously."

- **For Collaborative Planning (Interactive)**:
  > "This requires architectural decisions. Please run `/sys-builder:run-interactive` so we can validate the plan together."

## 3. References
(See `references/methodology.md` for detailed decision trees)
