# Claude Code Hooks & Lifecycle

## 1. The Governance Layer

Hooks are the **Governance Layer** of the Agentic Runtime. They run *outside* the model's context, ensuring safety, compliance, and automated housekeeping.

Usage: `plugins/<plugin>/hooks/hooks.json`

---

## 2. Native Lifecycle Events

The runtime exposes several critical events that allow you to "Hook" into the cognition loop.

| Event | Timing | Use Case |
|:------|:-------|:---------|
| **SessionStart** | When a new session begins | Initial context setup, welcome messages. |
| **UserPromptSubmit**| Before prompt processing | Auto-activate skills, inject context. |
| **PreToolUse** | Before tool execution | Block risky ops, modify inputs, safety checks. |
| **PostToolUse** | After tool success | Run linters, formatters, automated testing. |
| **Stop** | When the main agent stops | Final cleanup, session summary. |
| **SubagentStop** | After agent task completion| Synthesis, teardown of specialized agents. |
| **PreCompact** | Before context compaction | Protect critical history from being truncated. |
| **Notification** | On system notifications | Integrate with external alerting/logging. |

---

## 3. Reference Architecture

The Cat Toolkit uses a "Reference Architecture" (Zero-Install) pattern.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "command": "python3 \"${CLAUDE_PLUGIN_ROOT}/plugins/guard-rail/hooks/verify_safety.py\""
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "prompt",
        "prompt": "Before executing any destructive file operation, explain the consequences and confirm intent."
      }
    ]
  }
}
```

- **`${CLAUDE_PLUGIN_ROOT}`**: Points to the internal cache where your plugin resides. **Hooks MUST use this variable** for portability; never use absolute or exit-relative paths.
- **Isolation**: Scripts should read from `stdin` as JSON, validate inputs (e.g., using `jq`), and return valid JSON to `stdout` (`continue`, `systemMessage`).

### Prompt-Based Hooks (Context-Aware)
Hooks can be natural language prompts rather than just shell commands. This allows for LLM-driven validation logic or context injection.
- **Type**: Set `"type": "prompt"` in `hooks.json`.
- **Logic**: Research indicates that `"type": "prompt"` uses an LLM decision (Context-Aware) to determine whether to proceed or inject information, versus `"type": "command"` which is Deterministic.
- **Purpose**: Use for logic requiring reasoning (e.g., "Review this code for security vulnerabilities before allowing the commit").

---

## 4. Best Practices

### The "Prompt-First" Strategy
Prefer **Prompt-Based Hooks** (injecting instructions) over **Hard-Blocking Hooks** where possible.
- **Good:** Injecting "Do not delete files without asking" into the system prompt.
- **Necessary:** Hard-blocking `rm -rf /` in `PreToolUse`.

### Performance
Hooks run on *every* interaction.
- Keep them fast (<100ms).
- Use `is_safe_read()` and avoid heavy computations.

### The XML Signaling Pattern
When a Hook needs to detect a specific state (e.g., "Task Complete" or "Error Found") inside the model's output, **do not rely on natural language**. It is too variable.

Instead, instruct the Agent to output an XML Signal, and use Regex in your hook to catch it.

**The "Ralph Wiggum" Pattern (Loop Termination):**

1.  **Instruction (in Command/Prompt):**
    > "When you have fully satisfied the requirements, output `<promise>COMPLETE</promise>`."

2.  **Detection (in `stop-hook.sh`):**
    ```bash
    # Extract text between XML tags
    PROMISE=$(echo "$LAST_OUTPUT" | perl -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s')
    
    if [[ "$PROMISE" == "COMPLETE" ]]; then
      exit 0 # Allow stop
    fi
    ```

**Why XML?**
*   **Unambiguous Boundaries:** Regex can match `<tag>...</tag>` precisely, ignoring surrounding chatter.
*   **Machine Parseable:** Allows extraction of structured data (e.g., `<score>85</score>`) by validation scripts.
