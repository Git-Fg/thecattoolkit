---
name: {SKILL_NAME}
# Enhanced Pattern (minimal skills are typically toolkit infrastructure):
description: "{BRIEF_CAPABILITY}. MUST Use when {INTERNAL_STANDARD}."
# Note: Minimal skills are usually internal, so Enhanced pattern with MUST is common.
# For public internal utilities, use Standard: "{CAPABILITY}. Use when {TRIGGERS}."
allowed-tools: [{ALLOWED_TOOLS}]
disable-model-invocation: true
user-invocable: false
---

# {HUMAN_READABLE_NAME}

## Purpose

Internal utility skill that {core function}. Automatically activated by {trigger mechanism}.

## Activation

**Trigger:** {Hook event or condition}
**Method:** {Hook-based | Called by other skills | Passive monitoring}

## Implementation

```{language}
# Core logic
{minimal_implementation}
```

## Integration

### Hook Configuration (if hook-based)

```json
{
  "hooks": {
    "{event}": [
      {
        "matcher": "{tool_or_pattern}",
        "hooks": [{
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/{script}.sh"
        }]
      }
    ]
  }
}
```

### Called By (if sub-skill)

- {calling_skill_1}
- {calling_skill_2}

## Configuration

```yaml
# Optional configuration
{option}: {default_value}
```

## Behavior

**On activation:**
1. {Action 1}
2. {Action 2}
3. {Return result or exit silently}

**Exit codes (if hook-based):**
- `0` - Success, proceed
- `1` - Warning, proceed with message
- `2` - Block operation

---

**Note:** This is an internal skill. Not user-invocable. Uses `disable-model-invocation: true` to prevent semantic discovery.
