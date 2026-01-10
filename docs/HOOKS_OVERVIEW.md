# Hook Implementation Guide

Complete reference for hook implementation, including I/O protocol, safety standards, and validation scripts.

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

## Safety Standards

Hooks must follow these safety standards for secure and portable implementation:

### Portability
- **Always use `${CLAUDE_PLUGIN_ROOT}`** for script paths
- Never hardcode absolute paths or assume installation location
- Use `${CLAUDE_PLUGIN_ROOT}/scripts/your-script.py` instead of `/usr/local/bin/your-script`

### Input Hygiene
- **Read stdin as JSON** and validate with `jq` before processing
- Quote ALL variables to prevent injection attacks
- Validate all parameters from `tool_input`

### Output Protocol
- **Return valid JSON** on stdout
- **Exit code `0`** for success (continue)
- **Exit code `2`** for blocking errors
- Set reasonable timeouts for command hooks

### Security Checklist
- [ ] Validate all parameters from `TOOL_INPUT`
- [ ] Use `${CLAUDE_PLUGIN_ROOT}` for all file paths
- [ ] Handle failures with proper exit codes
- [ ] Log significant operations for security review

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

# Validate JSON input
if ! echo "$INPUT" | jq -e . >/dev/null 2>&1; then
  echo '{"continue": false, "systemMessage": "Invalid JSON input"}'
  exit 1
fi

# Extract and validate file path
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Prevent path traversal
if [[ "$FILE_PATH" == *".."* ]]; then
  echo '{"continue": false, "systemMessage": "Path traversal detected"}'
  exit 2
fi

# Success
echo '{"continue": true, "systemMessage": "Operation validated"}'
exit 0
```

---

## Hook Event Reference

| Hook | Trigger | Use Case |
|:-----|:--------|:---------|
| `SessionStart` | New session begins | Initialize environment, load config |
| `UserPromptSubmit` | Before prompt processing | Add context, validate intent |
| `PreToolUse` | Before tool execution | Validate input, enforce policies |
| `PermissionRequest` | Permission dialog shown | Add context to permission prompts |
| `PostToolUse` | After tool success | Log operations, trigger side effects |
| `Notification` | System notifications | Filter/route notifications |
| `Stop` | Main agent finishes | Cleanup, generate reports |
| `SubagentStop` | After task completion | Aggregate subagent results |
| `PreCompact` | Before context compaction | Prepare context for compaction |
| `SessionEnd` | Session ends | Final cleanup, persist state |

---

## Validation Scripts

### Validate hooks.json

```bash
python3 plugins/meta/skills/manage-hooks/assets/scripts/hook-tester.py hooks.json
```

**Checks:**
- Valid hook events
- Required fields present
- JSON syntax
- Matcher patterns
