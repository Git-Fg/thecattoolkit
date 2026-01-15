---
name: adhering-standards
description: "Provides System Authority on 2026 Universal Agentic Runtime standards for all plugin components. MUST Use when auditing or managing plugin components (Skills, Commands, Agents). Do not use for creating new components, development tasks, or routine maintenance."
allowed-tools: [Read, Write, Edit, Bash(ls:*), Bash(grep:*), Bash(cat:*), Bash(find:*), Glob, Grep]
---

# Toolkit Registry Standards



## Quick Reference

| Component | Purpose | Entry Trigger |
|:----------|:--------|:--------------|
| **Skills** | Knowledge injection, reusable workflows | "Create a skill for X", "Audit skill Y" |
| **Commands** | Orchestration shortcuts, multi-skill workflows | "Create a command for X", "Audit command Y" |
| **Agents** | Persona binding, isolated context execution | "Create an agent for X", "Audit agent Y" |

## Core Standards

### Component Management

**For detailed specifications, see:** `references/full-spec.md`

**Key Standards:**
- Skills: USE when patterns, allowed-tools, progressive disclosure
- Commands: disable-model-invocation, argument-hint, orchestration focus
- Agents: Persona binding, tool restrictions, no AskUser in workers

### Validation Protocol

All components MUST pass validation before use. See `references/validation.md` for complete validation protocol.


