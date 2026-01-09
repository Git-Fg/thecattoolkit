# Agentic Runtime Hooks & Lifecycle

## 1. The Governance Layer

Hooks are the **Governance Layer** of the Agentic Runtime. They run *outside* the model's context, ensuring safety, compliance, and automated housekeeping.

**Location:** `plugins/<plugin>/hooks/hooks.json`

---

## 2. Native Lifecycle Events

| Event | Timing | Use Case |
|:------|:-------|:---------|
| **SessionStart** | New session begins | Initial context setup, welcome messages |
| **UserPromptSubmit** | Before prompt processing | Auto-activate skills, inject context |
| **PreToolUse** | Before tool execution | Block risky ops, modify inputs, safety checks |
| **PermissionRequest** | Permission dialog shown | Permission handling |
| **PostToolUse** | After tool success | Run linters, formatters, automated testing |
| **Notification** | System notifications | External alerting/logging |
| **Stop** | Main agent finishes | Final cleanup, session summary |
| **SubagentStop** | After subagent completes | Synthesis, teardown of specialized agents |
| **PreCompact** | Before context compaction | Protect critical history from truncation |
| **SessionEnd** | Session ends | Final state cleanup |

**Note:** `SubagentStart` does NOT exist—only `SubagentStop`.

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
