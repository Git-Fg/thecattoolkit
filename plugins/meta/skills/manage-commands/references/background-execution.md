# Background Execution Patterns for Commands

## Overview

Commands can delegate to subagents with background execution for asynchronous task processing. This enables launching long-running work while allowing the user to continue working.

## Key Principle

> **Commands delegate, agents execute.** Commands provide context and instructions for background agents to work autonomously.

---

## Core Patterns

### 1. Single Background Agent
Delegate a single long-running task to a background agent.

```yaml
---
description: Analyze codebase architecture in background
argument-hint: [path-to-analyze]
allowed-tools: Task
disable-model-invocation: true
---

Spawn a background agent to analyze: $ARGUMENTS

**Provide exhaustive context including:**
- What the code does
- Goal (e.g., security, performance)
- Scope and boundaries
- Expected output format
```

### 2. Parallel Fan-Out
Launch multiple background agents simultaneously for independent tasks.

```yaml
---
description: Parallel security and performance analysis
argument-hint: [module]
allowed-tools: Task
disable-model-invocation: true
---

Spawn 2 background agents in parallel:
- Agent 1: Analyze $ARGUMENTS for security vulnerabilities
- Agent 2: Analyze $ARGUMENTS for performance bottlenecks

Synthesize both reports when complete.
```

### 3. Hybrid Foreground/Background
Launch background agents, then do foreground work while waiting.

```yaml
---
description: Background analysis with foreground prep work
allowed-tools: Task, Read, Edit
---

Task the code-explorer agent to analyze in background.
While background agent runs:
1. Review existing documentation
2. Prepare integration plan
```

---

## Permission & Security

### Background Safety
Ensure the target agent is "background safe":
1. **Read-only tools** (Read, Grep, Glob) are always safe.
2. **Bash execution** is NOT safe for background (requires manual approval).
3. **File operations** require pre-approval or explicit design for background.

### Tool Restrictions
Commands should focus on delegation. Use `allowed-tools: Task` to restrict the command to delegation only.

---

## Context Provisioning

Agents start with fresh context. Commands MUST provide:
- **Background**: Project/codebase context.
- **Goal**: Clear objective.
- **Constraints**: Limitations or requirements.
- **Expected Output**: Specific format needed.

---

## Error Handling

If a background agent fails or gets stuck:
1. Inform the user the background task encountered issues.
2. Suggest an alternative (foreground execution).
3. Provide partial results if available.
