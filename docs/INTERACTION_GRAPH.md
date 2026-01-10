# Component Interaction: Decision Trees & Heuristics

This document provides decision-making guidance for component selection. For the visual interaction graph and complete specifications, see [CLAUDE.md](../CLAUDE.md#55-interaction-graph).

---

## Decision Tree: What to Use When

### 1. Atomic Task (security scan, code analysis)
- ✅ Forked Skill with `context: fork`
- ❌ Command wrapping a Skill

### 2. Multi-Phase Workflow (feature dev, project setup)
- ✅ Command orchestrating multiple Skills
- ❌ Single Skill with complex logic

### 3. Reusable Persona (security expert, code reviewer)
- ✅ Agent definition + Skill binding via `agent: [name]`
- ❌ Hardcoded instructions in multiple Skills

### 4. Simple Tool Restriction (read-only analysis)
- ✅ Skill with `allowed-tools: [Read, Grep]`
- ❌ Separate Agent with same restrictions

---

## Restrictions

| Component | Cannot Do |
|:----------|:----------|
| **Commands** | Execute atomic tasks (must orchestrate Skills) |
| **Skills** | Run without `context: fork` for complex execution |
| **Wrapper Commands** | Wrap single Skills (use Forked Skill instead) |
| **Empty Shell Agents** | Should be deleted (use `allowed-tools` in Skill) |
| **Built-in Agents** | Use Forked Skills for atomic tasks |
| **Hooks** | Trigger other hooks |

---

## MCP Integration

MCP (Model Context Protocol) servers provide external tool access:

```
Main Agent
    → Calls MCP tool (e.g., database query)
    → MCP Server executes externally
    → Returns result to Main Agent
```

MCP tools are subject to the same `tools` restrictions as native tools.
