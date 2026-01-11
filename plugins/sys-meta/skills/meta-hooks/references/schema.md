# Hook Schema Reference

## JSON Structure

Hooks are configured in `hooks.json` files. The schema supports events, matchers, and hook definitions.

## Top-Level Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matchers": ["matcher1", "matcher2"],
        "hooks": [
          {
            "type": "command|prompt",
            "command": "...",
            "prompt": "...",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Configuration Locations

| Scope | Location | Use Case |
|:------|:----------|:---------|
| **User** | `~/.claude/settings.json` | Personal hooks |
| **Project** | `.claude/settings.json` | Team-shared hooks |
| **Local** | `.claude/settings.local.json` | Personal overrides |
| **Plugin** | `plugins/*/hooks/hooks.json` | Plugin hooks |

## Event Object Structure

### Basic Event

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [...]
      }
    ]
  }
}
```

### Event with Matchers

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matchers": ["startup", "resume"],
        "hooks": [...]
      }
    ]
  }
}
```

### Tool-Specific Event

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [...]
      }
    ]
  }
}
```

## Hook Definition Structure

### Command Hook

```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/script.sh",
  "timeout": 30
}
```

**Fields:**
- `type` (required): `"command"`
- `command` (required): Script to execute
- `timeout` (optional): Timeout in seconds (default: varies)

### Prompt Hook

```json
{
  "type": "prompt",
  "prompt": "Evaluate if action is safe: $ARGUMENTS",
  "timeout": 30
}
```

**Fields:**
- `type` (required): `"prompt"`
- `prompt` (required): Prompt for LLM evaluation
- `timeout` (optional): Timeout in seconds

## Environment Variables

### Available in All Hooks

| Variable | Description | Example |
|:----------|:-------------|:--------|
| `$CLAUDE_PROJECT_DIR` | Project root directory | `/Users/user/project` |
| `${CLAUDE_PROJECT_DIR}` | Same as above (alternative syntax) | `/Users/user/project` |

### Plugin-Specific Hooks Only

| Variable | Description | Example |
|:----------|:-------------|:--------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin root directory | `/path/to/plugin` |

### SessionStart Hooks Only

| Variable | Description | Usage |
|:----------|:-------------|:------|
| `$CLAUDE_ENV_FILE` | Environment file path | Write to persist env vars |

## Tool Argument Substitution

In `PreToolUse` and `PostToolUse` hooks, access tool arguments:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Tool: $TOOL_NAME, Args: $ARGUMENTS'",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Complete Example

### Project-Level Hooks

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matchers": ["startup"],
        "hooks": [
          {
            "type": "command",
            "command": ".claude/scripts/init-env.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/scripts/bash-safety.sh",
            "timeout": 15
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if file write is safe. Path: $ARGUMENTS. Return JSON with ok field.",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/scripts/cleanup.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Plugin-Level Hooks

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/guard.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

## Validation

### Schema Validation Checklist

- [ ] Valid JSON syntax
- [ ] Top-level `hooks` object exists
- [ ] Event names are valid
- [ ] Hook definitions have `type` field
- [ ] Command hooks have `command` field
- [ ] Prompt hooks have `prompt` field
- [ ] Timeout values are reasonable
- [ ] Environment variables use correct syntax
- [ ] Plugin hooks use `${CLAUDE_PLUGIN_ROOT}`
- [ ] File paths use absolute paths or correct env vars

### Common Schema Errors

| Error | Cause | Fix |
|:------|:------|:-----|
| Invalid JSON | Syntax error | Fix JSON syntax |
| Unknown event | Typo in event name | Use correct event name |
| Missing type | Hook definition incomplete | Add `type` field |
| Wrong env var | `${CLAUDE_PROJECT_DIR}` in plugin hook | Use `$CLAUDE_PROJECT_DIR` or `${CLAUDE_PROJECT_DIR}` |
| Path traversal | `../other-plugin/script.sh` | Use absolute paths or env vars |

## Best Practices

1. **Use absolute paths** or environment variables
2. **Set timeouts** to prevent hanging hooks
3. **Use ${CLAUDE_PLUGIN_ROOT}** in plugin hooks
4. **Keep hooks fast** - they block execution
5. **Test exit codes** - verify blocking behavior
6. **Log failures** - capture stderr for debugging
7. **Document hooks** - add comments in JSON
