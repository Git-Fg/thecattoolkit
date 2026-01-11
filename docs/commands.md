# Commands Reference

Complete reference for Commands: Shortcuts & AI Macros in the Cat Toolkit.

---

## The Mental Model

```
Command = Macro / Shortcut
├─ Human types: /deploy
├─ AI invokes: SlashCommand(deploy, args)
└─ Claude executes: pre-deploy-check skill → build skill → deploy skill → post-deploy-test skill
```

---

## Two Audiences

Commands serve two distinct audiences with different purposes and configurations.

### 1. For Humans (Zero-Token Retention)

| Aspect | Detail |
|:-------|:--------|
| **Purpose** | Manual invocation only |
| **Benefit** | With `disable-model-invocation: true`, the command description is **excluded from the Skill Tool's ~15k character budget** |
| **Result** | Zero passive context cost—Claude doesn't know it exists until you invoke it manually |
| **Use Cases** | Heavy playbooks, interactive wizards, personal shortcuts |

### 2. For AI (Context Macros)

| Aspect | Detail |
|:-------|:--------|
| **Purpose** | Standardized interfaces for complex tools |
| **Benefit** | Reduces hallucination by abstracting complex Skill schemas into simple CLI-style arguments |
| **Rule** | If a Command abstracts parameters significantly, expose it to the model |
| **Control** | Use `disable-model-invocation: false` (default) to allow programmatic invocation via Skill tool |
| **Use Cases** | Multi-skill workflows, standardized interfaces, complex tool wrappers |

---

## Command-Skill Pattern

Create a command that simply points to a Skill via `allowed-tools: [Skill(name)]`. This forces the model to "Global Orientation" on that specific skill without context pollution.

**Why this pattern matters:**
- Commands become lightweight wrappers
- Skills remain semantically discoverable
- Zero-token retention for heavy workflows
- Clean separation of concerns

---

## Command Recipes (Three Types)

### 1. Safe Read-Only

**Use when:** You need read-only analysis without modifications.

```yaml
---
description: "Analyze project structure"
allowed-tools: [Read, Grep]
---
```

**Characteristics:**
- No write operations
- No execution risks
- Safe for autonomous invocation

### 2. Autonomous Agent Wrapper

**Use when:** You need self-contained analysis that outputs structured data.

```yaml
---
description: "Autonomous code review"
allowed-tools: [Read, Grep, Glob]
---
Analyze codebase. Output JSON. DO NOT ask questions.
```

**Characteristics:**
- Fully autonomous
- Structured output (JSON)
- No user interaction required

### 3. User Interactive (Wizard)

**Use when:** You need to guide users through complex workflows.

```yaml
---
description: "Project scaffolding wizard"
disable-model-invocation: true  # Human-only: Skill tool cannot invoke
---
Guide user through setup. Ask for template preference.
```

**Characteristics:**
- Interactive by design
- `disable-model-invocation: true` (human-only)
- Wizard-style guidance

---

## When Commands Are Useful

| Pattern | Description | Example |
|:--------|:------------|:--------|
| **Multi-skill workflow** | Sequences multiple Skills in order | `/release` → version-bump → build → deploy → notify |
| **Interactive wizard** | Guides users through complex setups | `/scaffold` → project setup wizard |
| **Shortcut / Alias** | Quick access to specific Skills | `/think` → thinking-frameworks skill |

---

## 2026 Rule (Aliases)

> **Commands are excellent for creating Shortcuts** (e.g., `/think`) to specific skills. This avoids semantic ambiguity and ensures zero-token invocation.

**Why aliases matter:**
- Natural language can be ambiguous
- Slash commands are deterministic
- Zero cost to invoke (with `disable-model-invocation: true`)

---

## 2026 Doctrine: Zero-Token Retention

> **Zero-Token Retention:** Use Commands with `disable-model-invocation: true` as deterministic entry points for humans. Such commands are **excluded from the Skill Tool's ~15k character budget**, consuming 0 passive tokens until manually invoked.
>
> This is critical for **Anti-Context Rot**: Heavy playbooks (`/release`, `/setup`) won't pollute the model's limited attention span, keeping the Skill budget available for discoverable intelligent skills.

### Execution vs Retention

| Cost Type | When `disable-model-invocation: true` | When `false` (default) |
|:----------|:--------------------------------------|:-----------------------|
| **Retention (passive)** | **0 tokens** — excluded from Skill Tool budget | Standard — consumes part of ~15k char budget |
| **Execution (active)** | Standard — consumes tokens when running | Standard — consumes tokens when running |

**Key insight:** The zero-token benefit is **passive retention only**. Execution always costs tokens.

---

## Command-Skill Pattern: Complete Example

### Command (Human-Only Entry Point)

```yaml
# commands/heavy-workflow.md
---
description: "Complex workflow for humans only"
# Zero-retention: This description is EXCLUDED from Skill Tool's ~15k char budget
disable-model-invocation: true
allowed-tools: [Skill(builder-core)]
---

# Plan Initialization

Invoke the builder-core skill to initialize a Standard Plan.
```

### Skill (AI-Discoverable, Hidden from Menu)

```yaml
# skills/builder-core/SKILL.md
---
name: builder-core
user-invocable: false  # Hidden from / menu (accessible via /plan command)
description: "PROACTIVELY USE when planning or executing projects..."
---
```

### The Golden Rule

> **When a Command wraps a Skill, set `user-invocable: false` on the Skill to hide it from the `/` menu while maintaining semantic discovery for the AI.**

This ensures:
- Humans access via `/plan` command (zero retention)
- AI discovers via semantic description (when needed)
- Clean `/` menu without clutter

---

## Command that Orchestrates Multiple Skills

```markdown
<!-- commands/release.md -->
---
description: "Orchestrates the complete release workflow"
allowed-tools: [Skill, Bash]
---

# Release Workflow

You are orchestrating a release. Execute these skills in sequence:

1. **version-bump**: Increment version based on commit history
2. **run-tests**: Execute full test suite
3. **build-artifacts**: Create production builds
4. **deploy**: Push to production environment
5. **notify**: Send release notifications

DO NOT ask for confirmation. Proceed autonomously.
```

**Characteristics:**
- Multi-skill orchestration
- Autonomous execution
- No user prompts
- Sequential skill invocation

---

## Command Frontmatter Reference

```yaml
---
description: "Orchestrate X workflow"  # Semantic matching for discovery
allowed-tools: [Skill, Bash, Read]     # Restricts which tools this command can use
disable-model-invocation: false        # true = human-only command (Skill tool cannot invoke)
---
```

| Field | Purpose | Default |
|:-----|:--------|:--------|
| `description` | Semantic matching for discovery | Required |
| `allowed-tools` | Restricts which tools the command can access | All tools |
| `disable-model-invocation` | Controls whether Skill tool can invoke + Zero-Token Retention | `false` |

> **IMPORTANT:** `permissionMode` is **NOT valid** in Command frontmatter. This field is exclusive to Agents. Commands inherit permissions from the calling context. Use `allowed-tools` to restrict which tools the command can access.

---

## Quick Reference: Command Decision Matrix

| Scenario | Use Command? | Type | Configuration |
|:---------|:-------------|:-----|:--------------|
| Heavy playbook I want zero-retention | ✓ | Human-only | `disable-model-invocation: true` |
| Standardized interface for complex tool | ✓ | AI-accessible | `disable-model-invocation: false` |
| Alias to avoid semantic ambiguity | ✓ | Either | Depends on use case |
| Simple one-shot task | ✗ | Use Skill directly | N/A |
| Task needs AI semantic discovery | ✗ | Use Skill directly | N/A |

---

## Common Command Patterns

### 1. Release Workflow
```yaml
---
description: "Orchestrate complete release process"
allowed-tools: [Skill, Bash]
disable-model-invocation: false
---
Execute: version-bump → tests → build → deploy → notify
```

### 2. Interactive Wizard
```yaml
---
description: "Interactive project scaffolding"
disable-model-invocation: true
---
Guide user through template selection and setup.
```

### 3. Analysis Shortcut
```yaml
---
description: "Quick codebase analysis"
allowed-tools: [Skill(analyzer)]
disable-model-invocation: true
---
Invoke analyzer skill for comprehensive audit.
```

---

## Visibility: disable-model-invocation vs user-invocable

| Field | Scope | Purpose | Effect |
|:-----|:------|:--------|:-------|
| `disable-model-invocation` | Commands only | Blocks Skill tool invocation + Zero-Token Retention | Excludes from ~15k budget when `true` |
| `user-invocable` | Skills only | Controls `/` menu visibility | Hides from UI when `false` |

**Key distinction:**
- `disable-model-invocation` = Command visibility + **Zero-Token Retention**
- `user-invocable` = Skill UI visibility only (no retention impact)
