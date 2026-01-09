# Agentic Runtime Hooks & Lifecycle

## 1. The Governance Layer

Hooks are the **Governance Layer** of the Agentic Runtime. They run *outside* the model's context, ensuring safety, compliance, and automated housekeeping.

**Location:** `plugins/<plugin>/hooks/hooks.json`

---

## 2. Native Lifecycle Events

| Event | Timing | Use Case | Component-Scoped Support |
|:------|:-------|:---------|:-------------------------|
| **SessionStart** | New session begins | Initial context setup, welcome messages | ❌ Global hooks only |
| **UserPromptSubmit** | Before prompt processing | Auto-activate skills, inject context | ❌ Global hooks only |
| **PreToolUse** | Before tool execution | Block risky ops, modify inputs, safety checks | ✅ All components |
| **PermissionRequest** | Permission dialog shown | Permission handling | ❌ Global hooks only |
| **PostToolUse** | After tool success | Run linters, formatters, automated testing | ✅ All components |
| **Notification** | System notifications | External alerting/logging | ❌ Global hooks only |
| **Stop** | Main agent finishes | Final cleanup, session summary | ✅ All components |
| **SubagentStart** | Subagent starts | Initialize sub-environment or logging | ❌ Global hooks only |
| **SubagentStop** | After subagent completes | Synthesis, teardown of specialized agents | ❌ Global hooks only |
| **PreCompact** | Before context compaction | Protect critical history from truncation | ❌ Global hooks only |
| **SessionEnd** | Session ends | Final state cleanup | ❌ Global hooks only |

**Note:** Skills, Agents, and Slash Commands can define hooks scoped to their lifecycle using frontmatter. These component-scoped hooks support only `PreToolUse`, `PostToolUse`, and `Stop` events. Global hooks (defined in hooks.json) support all events.

---

## 3. Hook Types

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

**Prompt hooks** use LLM reasoning to decide whether to proceed or inject information.
**Command hooks** are deterministic—use for performance or strict validation.

---

## 4. Hook Input/Output

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

## 5. Best Practices

### Portability
Always use `${CLAUDE_PLUGIN_ROOT}` for script paths:
```json
"command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/validate.py\""
```

### Prompt-First Strategy
Prefer **Prompt-Based Hooks** (injecting instructions) over hard-blocking:
- **Good:** Inject "Do not delete files without asking" into the system prompt
- **Necessary:** Hard-block `rm -rf /` in `PreToolUse`

### Performance
Hooks run on every interaction—keep them fast (<100ms).

---

## 6. Signal Extraction Pattern (Optional)

When a Hook needs to detect a specific state from model output, **XML signals** provide reliable extraction:

**Instruction (in Command):**
```markdown
When you have fully satisfied the requirements, output `<promise>COMPLETE</promise>`.
```

**Detection (in hook script):**
```bash
PROMISE=$(echo "$LAST_OUTPUT" | grep -oP '(?<=<promise>).*(?=</promise>)')
if [[ "$PROMISE" == "COMPLETE" ]]; then
  exit 0
fi
```

**Why XML for signals?**
- **Unambiguous boundaries:** Regex can match `<tag>...</tag>` precisely
- **Machine parseable:** Allows extraction of structured data like `<score>85</score>`

**Note:** This pattern is for **hook signal extraction only**, not for structuring Commands or Skills.

---

## 7. Hook Security Considerations

### Permission Inheritance in Hooks

Hooks inherit permissions from their parent component:

```yaml
# Agent with restricted permissions
---
name: secure-scanner
description: "Secure code scanner"
permissionMode: plan  # Read-only mode
tools: [Read, Grep]  # Limited tools
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "./validate-read.sh"
---

# Result: Hook inherits the agent's plan mode and Read+Grep restrictions
```

### Input Hygiene Standards

Command hooks MUST read stdin as JSON and validate inputs:

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

### Dangerous Hook Patterns

```yaml
# ❌ DANGEROUS - Hook bypasses permission system
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "rm -rf /"  # No validation, no safety checks

# ✅ SECURE - Hook with proper validation
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "./validate-write.sh $TOOL_INPUT"  # Validates input
          timeout: 30  # Prevents long-running operations
```

### Hook Validation Checklist

- [ ] **Input Validation:** Validate all parameters from `TOOL_INPUT` or `FILE_PATH`
- [ ] **Timeout Protection:** Set reasonable timeouts for command hooks
- [ ] **Error Handling:** Handle failures gracefully with proper exit codes
- [ ] **Path Security:** Use `${CLAUDE_PLUGIN_ROOT}` for all file paths
- [ ] **Permission Awareness:** Understand inherited permission restrictions
- [ ] **Audit Trail:** Log significant operations for security review

### Component-Scoped Hook Security

Component-scoped hooks inherit parent permissions:

```yaml
# Skill with hook
---
name: file-analyzer
description: "Analyzes file contents"
permissionMode: plan  # Read-only
allowed-tools: [Read]
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "./scan-file.sh $TOOL_INPUT"
---

# Result: Hook inherits plan mode and Read-only restriction
```
