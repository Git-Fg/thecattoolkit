# Frontmatter Standards

## Overview

The YAML frontmatter is the PRIMARY mechanism for skill discovery. Claude reads only the `name` and `description` fields at startup to determine when to use a skill.

## Critical Constraints

| Field | Required | Constraints | Runtime Crash if Invalid |
|:---|:---:|:---|:---|
| **name** | ✓ | 1-64 chars, lowercase, hyphens only, must match directory | **CRASH** |
| **description** | ✓ | 1-1024 chars, single line only | **CRASH** |

## Required Fields

### name

**Constraints:**
- 1-64 characters
- Lowercase letters, numbers, and hyphens only
- No consecutive hyphens (`--`)
- No leading or trailing hyphens
- Must match directory name exactly

**Valid:** `pdf-processing`, `data-analysis-v2`, `code-review`
**Invalid:** `PDF_Processing`, `-helper`, `tool--kit`, `my_skill`

### description

**Constraints:**
- 1-1024 characters
- Single line only (no `>` or `|` YAML multiline syntax)
- Must describe both WHAT the skill does and WHEN to use it
- Should include specific keywords for discovery

**Best Practice:** Start with Modal + "USE when" pattern:
- `MUST USE when` - Critical internal standards
- `SHOULD USE when` - Recommended patterns
- `PROACTIVELY USE when` - Autonomous discovery
- `USE when` - General capability

**Good Example:**
```yaml
description: "Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction."
```

**Bad Example:**
```yaml
description: "A skill that helps with PDFs."  # Too vague, no trigger terms
```

## Optional Fields

### allowed-tools

Restricts tool access during skill activation. If omitted, no restriction.

**Syntax (comma-separated):**
```yaml
allowed-tools: Read, Write, Bash(git:*)
```

**Syntax (YAML list):**
```yaml
allowed-tools:
  - Read
  - Grep
  - Glob
```

**Tool Restrictions:**
- Use parentheses for specific commands: `Bash(git:*)`, `Bash(npm:test)`
- Do NOT use brackets: `Bash[git]` is invalid

### model

Model to use when this skill is active (e.g., `claude-sonnet-4-20250514`). Defaults to conversation's model.

**Note:** Best practice is to omit this field to allow runtime/CLI to determine the model.

### context

Set to `fork` to run the skill in a forked sub-agent context with its own conversation history.

### agent

Specify which agent type to use when `context: fork` is set (e.g., `Explore`, `Plan`, `general-purpose`). Only applicable with `context: fork`.

### user-invocable

Controls whether the skill appears in the slash command menu. Does NOT affect automatic discovery.

| Value | Slash Menu | Skill Tool | Auto-Discovery | Use Case |
|:-----|:----------|:-----------|:---------------|:---------|
| `true` (default) | Visible | Allowed | Yes | Skills users invoke directly |
| `false` | Hidden | Allowed | Yes | Skills for Claude only |

**Note:** To block programmatic invocation via the `Skill` tool, use `disable-model-invocation: true` in commands instead.

### hooks

Define hooks scoped to this skill's lifecycle. Supports `PreToolUse`, `PostToolUse`, and `Stop` events.

**Example:**
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
```

## Discovery Pattern (The 2026 Standard)

The `description` field is how Claude decides when to apply your skill. It must answer two questions:

1. **What does this skill do?** List specific capabilities
2. **When should Claude use it?** Include trigger terms users would mention

### Modal Tiers

| Tier | Modal | Use Case | Example |
|:-----|:------|:---------|:--------|
| **Critical** | `MUST USE when` | Non-optional internal standards | "MUST USE when validating all code changes" |
| **Advisory** | `SHOULD USE when` | Recommended but situational | "SHOULD USE when designing new systems" |
| **Proactive** | `PROACTIVELY USE when` | Intent-assertive discovery | "PROACTIVELY USE when planning projects" |
| **Direct** | `USE when` | Primary entry point | "USE when processing PDF files" |
| **Role-Based** | `SHOULD USE when [ACTION]` | Agent persona descriptions | "SHOULD USE when orchestrating workflows" |

## Validation Checklist

- [ ] Name matches directory name exactly
- [ ] Name is 1-64 chars, lowercase, hyphens only
- [ ] No consecutive hyphens or leading/trailing hyphens
- [ ] Description is 1-1024 chars, single line
- [ ] Description starts with Modal + "USE when" pattern
- [ ] Description includes relevant keywords
- [ ] Optional fields use correct syntax
- [ ] `allowed-tools` uses parentheses for restrictions, not brackets
