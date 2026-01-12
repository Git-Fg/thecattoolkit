# Hook Configuration Reference

## Hooks Configuration File

The `hooks/hooks.json` file defines all hook configurations for a plugin.

## File Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate file operations"
          }
        ]
      }
    ],
    "PostToolUse": [],
    "Stop": [],
    "SessionStart": [],
    "SessionEnd": [],
    "UserPromptSubmit": [],
    "SubagentStop": []
  }
}
```

## Configuration Options

### Matcher Patterns

- **Exact match:** `"Write"`
- **Multiple:** `"Write|Edit|Read"`
- **Wildcard:** `"*"`
- **Regex:** `"mcp__.*__delete.*"`

### Hook Types

- **prompt:** LLM-driven validation
- **command:** Bash script execution

## Plugin Directory Structure

```
plugin/
├── hooks/
│   └── hooks.json          # Hook configuration
├── scripts/                # Command hook scripts
│   ├── validate.sh
│   └── notify.sh
└── SKILL.md
```

## Validation

Validate configuration:

```bash
# Check JSON syntax
jq . hooks/hooks.json

# Validate structure
jq '.hooks | keys' hooks/hooks.json
```
