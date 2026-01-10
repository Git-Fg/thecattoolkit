# Hook Implementation Recipes

This document provides practical code examples for hook implementation. For complete specifications and event reference, see [CLAUDE.md](../CLAUDE.md#52-hooks-governance).

---

## Hook Types

### Command Hooks (Deterministic)

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

### Prompt Hooks (Context-Aware)

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

## Hook Input/Output Protocol

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

## Security Implementation: Validation Script

```bash
#!/bin/bash
# validate.sh - Secure hook implementation

# Read stdin as JSON
INPUT=$(cat)

# Validate JSON structure
if ! echo "$INPUT" | jq -e . >/dev/null 2>&1; then
  echo '{"continue": false, "systemMessage": "Invalid JSON input"}'
  exit 1
fi

# Extract and validate tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Security check: prevent path traversal
if [[ "$FILE_PATH" == *".."* ]]; then
  echo '{"continue": false, "systemMessage": "Path traversal detected"}'
  exit 2
fi

# All checks passed
echo '{"continue": true, "systemMessage": "Operation validated"}'
exit 0
```

---

## Validation Checklist

- [ ] **Input Validation:** Validate all parameters from `TOOL_INPUT` or `FILE_PATH`
- [ ] **Timeout Protection:** Set reasonable timeouts for command hooks
- [ ] **Error Handling:** Handle failures gracefully with proper exit codes
- [ ] **Path Security:** Use `${CLAUDE_PLUGIN_ROOT}` for all file paths
- [ ] **Permission Awareness:** Understand inherited permission restrictions
- [ ] **Audit Trail:** Log significant operations for security review
