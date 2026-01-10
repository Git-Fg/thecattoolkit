# Hook Implementation Recipes

Code examples for hook implementation. For event reference and specifications, see [CLAUDE.md](../CLAUDE.md#52-hooks-governance).

---

## Hook Types

### Command Hook (Deterministic)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/verify_safety.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Prompt Hook (Context-Aware)

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Before executing any destructive file operation, explain the consequences and confirm intent."
          }
        ]
      }
    ]
  }
}
```

---

## Input/Output Protocol

**Input (JSON via stdin):**
```json
{
  "session_id": "abc123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

**Output:**
- Exit code `0` = Success (continue)
- Exit code `2` = Block action

Optional JSON response:
```json
{
  "continue": true,
  "systemMessage": "Operation validated"
}
```

---

## Validation Script Template

```bash
#!/bin/bash
# validate.sh - Secure hook implementation

INPUT=$(cat)

if ! echo "$INPUT" | jq -e . >/dev/null 2>&1; then
  echo '{"continue": false, "systemMessage": "Invalid JSON input"}'
  exit 1
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$FILE_PATH" == *".."* ]]; then
  echo '{"continue": false, "systemMessage": "Path traversal detected"}'
  exit 2
fi

echo '{"continue": true, "systemMessage": "Operation validated"}'
exit 0
```

---

## Validation Checklist

- [ ] Validate all parameters from `TOOL_INPUT`
- [ ] Set reasonable timeouts for command hooks
- [ ] Handle failures with proper exit codes
- [ ] Use `${CLAUDE_PLUGIN_ROOT}` for all file paths
- [ ] Log significant operations for security review
