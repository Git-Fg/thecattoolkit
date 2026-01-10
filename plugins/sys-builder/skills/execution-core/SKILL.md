---
name: execution-core
description: |
  USE to apply universal behavioral standards for autonomous agents.
  Defines Uninterrupted Flow, Self-Verification, Auth-Gates, and Handoff protocols.
user-invocable: false
allowed-tools: Bash, Edit, Read, Write, Glob, Grep
---

# Execution Core Standards

## Core Purpose

**This skill defines universal behavioral protocols for autonomous agent execution.**

It answers: "HOW should agents behave?" (not "WHAT should they do").

## Skill Contents

**Behavioral Protocols:**
- `references/observation-points.md` - Self-verification and evidence collection
- `references/auth-gates.md` - Authentication error handling
- `references/handoff-protocol.md` - Standard handoff format
- `references/execution-protocol.md` - Universal worker execution steps

## Core Behavioral Standards

### 1. Uninterrupted Flow

Agents execute autonomously without pausing for human input.

**Protocol:** `references/observation-points.md`

- Agents execute tasks sequentially
- Verify success programmatically via CLI
- Log results in structured format
- Continue to next task without waiting

### 2. Self-Verification

Every task must be verified automatically.

**Standard Pattern:**
```markdown
**Self-Verification Results:**
✓ [Verification 1 passed]
✓ [Verification 2 passed]

Next: Continue to next task
```

### 3. Authentication Gates

Authentication errors are NORMAL, not failures.

**Protocol:** `references/auth-gates.md`

1. **Recognize** auth gate (401, 403, "not authenticated")
2. **STOP** execution (don't retry in loop)
3. **Create** HANDOFF.md with exact steps
4. **EXIT** process
5. **Resume** after human provides credentials

### 4. Handoff Protocol

Standard format for pausing execution.

**Protocol:** `references/handoff-protocol.md`

Use for:
- Authentication gates
- Critical failures
- Ambiguous requirements
- Missing dependencies

**Format:**
```markdown
# HANDOFF Required

**Reason**: [AUTH_GATE | CONFLICT | AMBIGUOUS]

**What Happened**: [Description]

**What You Need to Do**: [Specific action]

**Verification**: [How to confirm fix]

**Next Step**: Restart execution after [action]
```

## Usage in Other Skills

Skills reference execution-core for behavioral standards:

**Example from project-strategy:**
```
Use execution-core observation-points for self-verification
Use execution-core auth-gates for authentication handling
```

**Example from software-engineering:**
```
Apply execution-core verification protocols during TDD
Use execution-core handoff format for blockers
```

## Key Principles

1. **Behavioral Consistency:** All builder operations use same execution standards
2. **Self-Sufficiency:** Agents verify own work programmatically
3. **Evidence Collection:** All actions logged with verification
4. **Non-Blocking:** No waiting loops or human checkpoints
5. **Clear Handoffs:** Standard format when pausing execution

## 5. Human Interaction Policy (AskUserQuestion)

To ensure Uninterrupted Flow, the following policy applies to human interaction:

- **Execution Phase Workers (e.g., Worker Agent):** `AskUserQuestion` is **STRICTLY PROHIBITED**. Workers must operate autonomously or use the Handoff Protocol if blocked.
- **Planning Phase Coordinators (e.g., Director, Orchestrator):** `AskUserQuestion` is **ALLOWED** for requirements gathering and clarification before execution begins.

This policy ensures that heavy implementation tasks are never interrupted, while initial discovery remains interactive.

## Standards Hierarchy

Execution-core sits at the BASE of the behavioral stack:

```
execution-core (HOW to behave)
    ↓
project-strategy (WHAT documents to create)
software-engineering (WHAT code patterns to use)
    ↓
director/worker agents (Execute using these standards)
```

**Critical:** Execution-core is UNIVERSAL. All builder agents must follow these behavioral protocols.
