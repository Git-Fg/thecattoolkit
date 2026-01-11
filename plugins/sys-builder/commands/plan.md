---
description: "Shortcut: Initialize or update the project plan."
argument-hint: "<planning request>"
allowed-tools: [Skill(manage-planning)]
disable-model-invocation: true
---

# Plan Orchestrator

Invoke `manage-planning` in **Planning Mode**.

**Goal:** Translate user request ("$ARGUMENTS") into structured plan files in `.cattoolkit/planning/`.

**Output:**
- BRIEF.md (project definition)
- DISCOVERY.md (codebase analysis, if needed)
- ROADMAP.md (multi-phase overview)
- Phase plan files in `phases/` directories

**Constraint:** Follow 2026 Inline-First standards. Use parallel exploration only for massive projects (>50 files OR >5 subdirectories).
