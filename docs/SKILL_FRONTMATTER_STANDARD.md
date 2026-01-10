# Skill Frontmatter Standard

Technical YAML schema for skill frontmatter. For complete specifications and Discovery Tiering Matrix, see [CLAUDE.md](../CLAUDE.md#part-iv-skill-protocol-layer).

---

## Universal Frontmatter Schema

```yaml
---
name: my-skill-name
description: >
  USE when [condition].
  A concise, action-oriented description.
  Max 1024 characters.
context: fork
allowed-tools:
  - Read
  - Write
  - Bash
model: sonnet
hooks:
  PreToolUse: "validate-input"
  PostToolUse: "log-operation"
  Stop: "cleanup"
---
```

---

## Field Reference

| Field | Required | Constraints |
|:------|:---------|:------------|
| `name` | **Yes** | Max 64 chars, lowercase letters/numbers/hyphens only. Must match directory name. |
| `description` | **Yes** | Max 1024 chars. Used for semantic matching. "USE when" as first sentence. |
| `allowed-tools` | No | Tools Claude can use without asking permission. |
| `context` | No | Set to `fork` to run in isolated sub-agent context. |
| `agent` | No | Agent type for forked context. |
| `user-invocable` | No | Controls slash command visibility. Default: `true`. Only specify if `false`. |
| `disable-model-invocation` | No | Blocks programmatic invocation via `Skill` tool. |
| `model` | No | `sonnet`, `opus`, `haiku`, or `'inherit'`. |
| `hooks` | No | Hooks scoped to Skill lifecycle (`PreToolUse`, `PostToolUse`, `Stop` only). |

---

## Field Constraints

### `name`
- **Pattern:** `^[a-z0-9-]+$`
- **Max Length:** 64 characters
- **Must Match:** Directory name containing SKILL.md

### `description`
- **Max Length:** 1024 characters
- **Format:** "USE when [condition]." as first sentence for optimal discovery
- **Content:** Action verbs, specific contexts, trigger keywords

### `allowed-tools`
- **Format:** Comma-delimited string or YAML array
- **Supports:** Granular patterns like `Bash(git add:*)`

### `context`
- **Values:** `fork` or omit for inline execution
- **Effect:** When set to `fork`, runs in isolated sub-agent with own context window

### `model`
- **Values:** `sonnet`, `opus`, `haiku`, `'inherit'`
- **Default:** Inherits from parent context if omitted

---

## Complete Specifications

- **Skill system overview** → [CLAUDE.md PART IV](../CLAUDE.md#part-iv-skill-protocol-layer)
- **Discovery Tiering Matrix** → [CLAUDE.md Section 4.4](../CLAUDE.md#44-discovery-tiering-matrix)
- **Permission system** → [CLAUDE.md PART V.1](../CLAUDE.md#51-permission-system)
