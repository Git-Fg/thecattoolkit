# Environment Variables

## Available Variables in Command Hooks

When using `type: "command"`, the following environment variables are available to your script:

| Variable | Value | Description |
|----------|-------|-------------|
| `$CLAUDE_PROJECT_DIR` | Absolute path | Root directory of the current project (where `.claude` folder is) |
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path | Directory of the plugin containing the hook (only for plugin hooks) |
| `$ARGUMENTS` | JSON string | The input JSON (also available via stdin). Note: For command hooks, stdin is preferred. |

## Usage Examples

### Using Project Root
```bash
#!/bin/bash
# Log to project-specific file
echo "Event fired" >> "$CLAUDE_PROJECT_DIR/.claude/logs/events.log"
```

### Using Plugin Root
```bash
#!/bin/bash
# Execute a script from the plugin's scripts directory
"${CLAUDE_PLUGIN_ROOT}/scripts/validate-safety.sh"
```

### Note on Prompt Hooks
For `type: "prompt"` hooks, these variables are not directly available in the prompt string, except for `$ARGUMENTS` which is a placeholder replaced by the runtime.
