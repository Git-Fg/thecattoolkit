# Skill Frontmatter Standard

This document defines The Cat Toolkit's skill frontmatter standards. For complete specifications, see [CLAUDE.md](../CLAUDE.md#skill-protocol-layer).

## Universal Frontmatter Schema

We adopt a **Native-First Schema** using Claude Code's native schema as the baseline for our skills.

### Gold Standard Header

Every skill in `thecattoolkit` should follow this header pattern:

```yaml
---
name: my-skill-name
description: >
  A concise, action-oriented description of what this skill does.
  CRITICAL: This text is used for "Semantic Intent Matching".
  Keep it under 1024 characters.
context: fork         # Recommended for complex tasks
allowed-tools:        # Explicit tool permissions
  - Read
  - Write
  - Bash
model: sonnet         # Optional: model specification

hooks:                # Optional: lifecycle automation
  PreToolUse: "validate-input"
  PostToolUse: "log-operation"
  Stop: "cleanup"
---
```

## Field Reference

| Field | Required | Description |
|:------|:---------|:------------|
| `name` | **Yes** | Skill name. Lowercase letters, numbers, hyphens only (max 64 chars). Must match directory name. |
| `description` | **Yes** | What the Skill does and when to use it (max 1024 chars). Claude uses this for semantic matching. |
| `allowed-tools` | No | Tools Claude can use without asking permission. |
| `context` | No | Set to `fork` to run in isolated sub-agent context. |
| `agent` | No | Agent type for forked context. |
| `user-invocable` | No | Controls slash command menu visibility. Default: `true`. |
| `disable-model-invocation` | No | Blocks programmatic invocation via `Skill` tool. |
| `model` | No | Model to use (`sonnet`, `opus`, `haiku`, or `'inherit'`). |
| `hooks` | No | Hooks scoped to Skill lifecycle. |

## Understanding `context: fork`

The `context: fork` field enables skills to run in **complete isolation** from the main conversation.

### What is Fork Context?

When a skill uses `context: fork`, it **spawns a completely isolated sub-agent** with:

- ✅ **Separate conversation history** - The forked agent has its own context window
- ✅ **Zero context pollution** - Main conversation remains clean
- ✅ **Autonomous execution** - Operates independently without main thread interference
- ✅ **Automatic result merging** - Results seamlessly integrate back to main conversation

### Isolation Behavior

| Aspect | Isolated in Fork | Shared with Main |
|:-------|:-----------------|:-----------------|
| **Conversation History** | ✅ Separate | ❌ |
| **Context Window** | ✅ Fresh | ❌ |
| **Task Memory** | ✅ Independent | ❌ |
| **Filesystem** | ❌ Same | ✅ |
| **Environment Variables** | ❌ Same | ✅ |
| **MCP Tools** | ❌ Same (unless restricted) | ✅ |
| **Git State** | ❌ Same | ✅ |

### When to Use `context: fork`

**✅ USE when:**
- Complex multi-step operations (>10 steps)
- Long-running analysis that would bloat main context
- Token conservation is critical
- Need parallel execution
- Specialized workflows requiring isolation

**❌ AVOID when:**
- Simple, single-step operations (<5 steps)
- Need user interaction during execution
- Require tight integration with main conversation

### The `agent` Field

The `agent` field works **only with `context: fork`** to specify sub-agent type:

```yaml
---
name: my-skill
description: Complex codebase analysis
context: fork
agent: Explore       # Fast, read-only exploration
model: opus         # Powerful model for complex reasoning
---

# Available agent types:
# - general-purpose: Capable agent for complex tasks
# - Explore: Fast, read-only exploration
# - Plan: Specialized for planning workflows
# - Custom: From .claude/agents/ directory
```

### Example: Comprehensive Security Audit

```yaml
---
name: comprehensive-security-audit
description: Performs thorough security analysis across entire codebase
context: fork
agent: general-purpose
model: opus
allowed-tools: Read, Grep, Glob, Bash
---

# Security Audit Skill
# Purpose: Analyze codebase security without cluttering main conversation
#
# This skill will:
# 1. Scan hundreds of files in isolation
# 2. Analyze authentication patterns
# 3. Check for vulnerabilities
# 4. Generate detailed report
# 5. Merge results back to main thread
#
# Main conversation stays pristine throughout!
```

## Description Best Practices

Since `description` is the *only* semantic signal shared by ALL frameworks, it must be engineered perfectly.

**Do:**
- Use imperative verbs ("Extract", "Analyze", "Generate")
- Mention specific file types or contexts ("...from PDF files", "...in the `src` directory")
- Include "trigger keywords" (e.g., "Use this when the user asks to debug")

**Don't:**
- Write vague marketing copy ("The best skill for coding")
- Exceed 1024 characters (strict limit for Claude Code)
- Put critical instructions in the description (put them in the Body)

## SKILL.md Body Structure

To support all frameworks, the body should follow a standard "Instructional" format.

```markdown
# [Skill Name]

## Purpose
Brief explanation of the goal.

## Instructions
1. Step one...
2. Step two...

## Examples
User: "Fix the bug"
Assistant: [Action]
```

**For complete specifications:**
- Skill system overview → [CLAUDE.md PART IV](../CLAUDE.md#part-iv-skill-protocol-layer)
- Discovery tiering → [CLAUDE.md Skill Discovery](../CLAUDE.md#skill-protocol-layer)
- Permission system → [CLAUDE.md PART V.1](../CLAUDE.md#51-permission-system)
- Progressive disclosure → [CLAUDE.md Skill Loading](../CLAUDE.md#part-iv-skill-protocol-layer)
