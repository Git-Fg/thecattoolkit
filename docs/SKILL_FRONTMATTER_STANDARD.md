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

## Discovery Tiering Matrix

> [!IMPORTANT]
> The tiers below are **pattern guidance** for writing effective descriptions. Do NOT include `[Tier X: Name]` as a literal prefix in the description field.

| Tier | Use Case | Pattern |
|:-----|:---------|:--------|
| **1: High Fidelity** | Complex/fuzzy tasks, LLM capability overlap | `[MODAL] when [CONDITION]. Examples: <example>...` |
| **2: High Gravity** | Safety-critical, governance, mandatory protocols | `[MODAL] USE when [CONDITION].` |
| **3: Utility** | Single-purpose, self-documenting utilities | `{Action Verb} + {Object} + {Purpose}` |

**Selection Rules:**
1. >40% overlap with built-in tools → Tier 1
2. Governance/safety layer → Tier 2
3. Self-documenting name → Tier 3

---

## Description Best Practices

Since `description` is the *only* semantic signal for discovery, it must be engineered perfectly.

**Do:**
- Use imperative verbs ("Extract", "Analyze", "Generate")
- Mention specific file types or contexts ("...from PDF files", "...in the `src` directory")
- Include "trigger keywords" (e.g., "Use this when the user asks to debug")

**Don't:**
- Write vague marketing copy ("The best skill for coding")
- Exceed 1024 characters (strict limit for Claude Code)
- Put critical instructions in the description (put them in the Body)

---

## Complete Specifications

For detailed explanations of WHY these patterns exist, see:
- **Skill system overview** → [CLAUDE.md PART IV](../CLAUDE.md#part-iv-skill-protocol-layer)
- **`context: fork` semantics** → [CLAUDE.md Law 2](../CLAUDE.md#law-2-the-law-of-atomic-capabilities)
- **Permission system** → [CLAUDE.md PART V.1](../CLAUDE.md#51-permission-system)
- **Progressive disclosure** → [CLAUDE.md Section 4.3](../CLAUDE.md#43-progressive-disclosure)
