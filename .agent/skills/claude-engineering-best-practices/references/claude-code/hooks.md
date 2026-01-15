# Hooks System — Stable Patterns

Hooks provide event-driven automation and control points throughout Claude Code's execution lifecycle.

## Core Concepts

### What Hooks Do
- **Intercept**: Observe actions before/after they happen
- **Validate**: Check safety/compliance
- **Modify**: Alter inputs or add context
- **Log**: Record events for audit/analysis
- **Block**: Prevent dangerous operations

### Stable Architecture
```
Hook Event → Matcher → [Multiple Hooks] → Decision/Output
```

## Hook Events (Stable List)

### PreToolUse
**When**: After parameters created, before execution
**Purpose**: Validate/modify tool calls
**Common matchers**: `Bash`, `Write`, `Edit`, `Read`, `Task`

**Pattern**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "validator.sh"
          }
        ]
      }
    ]
  }
}
```

### PostToolUse
**When**: After successful tool execution
**Purpose**: Log, validate results, trigger follow-ups
**Pattern**: Same as PreToolUse

### SessionStart
**When**: Session begins (startup/resume/clear/compact)
**Purpose**: Initialize context, set up environment
**Matcher types**: `startup`, `resume`, `clear`, `compact`

**Pattern**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "init.sh"
          }
        ]
      }
    ]
  }
}
```

### Stop
**When**: Main agent attempts to stop
**Purpose**: Validate if work is complete
**Can block**: Yes, prevents stoppage

### SubagentStop
**When**: Subagent (Task) attempts to stop
**Purpose**: Validate subagent completion
**Can block**: Yes

### Notification
**When**: Claude Code sends notifications
**Matcher types**: `permission_prompt`, `idle_prompt`, `auth_success`

### UserPromptSubmit
**When**: User submits prompt
**Purpose**: Validate/add context to prompts
**Can block**: Yes, prevents prompt processing

### PreCompact
**When**: Before conversation compaction
**Matcher types**: `manual`, `auto`

### SessionEnd
**When**: Session ends
**Purpose**: Cleanup, save state, log statistics

### PostToolUseFailure
**When**: Tool execution fails
**Purpose**: Error handling, recovery

### PermissionRequest
**When**: Permission dialog shown
**Purpose**: Auto-approve/deny permissions

## Hook Types

### Command Hooks
Execute bash commands/scripts
```json
{
  "type": "command",
  "command": "script.sh",
  "timeout": 30
}
```

**Best for**:
- Validation scripts
- File operations
- System commands
- Deterministic checks

### Prompt Hooks (Advanced)
Use LLM to evaluate decisions
```json
{
  "type": "prompt",
  "prompt": "Evaluate: $ARGUMENTS\nDecide if safe to proceed.",
  "timeout": 30
}
```

**Best for**:
- Context-aware decisions
- Natural language evaluation
- Complex criteria

**Response format**:
```json
{
  "ok": true,
  "reason": "Explanation"
}
```

## Matcher Patterns

### Simple Match
```json
"matcher": "Bash"
```
Matches exactly: tool name must be "Bash"

### Regex Match
```json
"matcher": "Write|Edit"
```
Matches: "Write" OR "Edit"

### Wildcard
```json
"matcher": "*"
```
Matches: all tools

### Empty Matcher
```json
"matcher": ""
```
Matches: all tools (for events without matchers like SessionStart)

## Common Patterns

### Pattern 1: Input Validation
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "validate-command.sh"
          }
        ]
      }
    ]
  }
}
```

**Validator script pattern**:
```bash
#!/bin/bash
read input  # JSON from stdin
# Validate command
if command_looks_dangerous "$command"; then
  echo "Dangerous command detected" >&2
  exit 2  # Block
fi
exit 0  # Allow
```

### Pattern 2: Output Logging
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "log-file-change.sh"
          }
        ]
      }
    ]
  }
}
```

### Pattern 3: Security Validation
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate security: $ARGUMENTS\nBlock if contains: rm -rf, sudo, > /etc/"
          }
        ]
      }
    ]
  }
}
```

### Pattern 4: Context Injection
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "load-context.sh"
          }
        ]
      }
    ]
  }
}
```

**Context injection script**:
```bash
#!/bin/bash
# Output to stdout becomes context
echo "Project context: Using Node.js 20, TypeScript 5"
echo "Recent changes: Feature X merged yesterday"
```

### Pattern 5: Smart Stopping
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Analyze: $ARGUMENTS\nIs all requested work complete?"
          }
        ]
      }
    ]
  }
}
```

## Environment Variables

Available in all hooks:

- `$CLAUDE_PROJECT_DIR`: Project root (absolute path)
- `$CLAUDE_CODE_REMOTE`: "true" if remote, empty if local
- `$CLAUDE_ENV_FILE`: Session environment file (SessionStart only)

### Using Environment Variables
```bash
#!/bin/bash
# Use in commands
echo "Working in: $CLAUDE_PROJECT_DIR"
echo "Is remote: $CLAUDE_CODE_REMOTE"

# Persist environment (SessionStart only)
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
```

## Input/Output Contract

### Input (via stdin)
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/dir",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "ls -la",
    "description": "List files",
    "timeout": 120000
  },
  "tool_use_id": "toolu_01ABC..."
}
```

### Output Methods

#### Method 1: Exit Code Only
- `exit 0`: Success/allow
- `exit 2`: Block with stderr message
- `exit N`: Non-blocking error (shown in verbose mode)

#### Method 2: JSON Output (Exit 0)
```json
{
  "continue": true,
  "stopReason": "Message if continue=false",
  "suppressOutput": false,
  "systemMessage": "Warning message"
}
```

#### Method 3: Event-Specific (Exit 0)
**PreToolUse**:
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Why",
    "updatedInput": {
      "field": "modified value"
    }
  }
}
```

**UserPromptSubmit**:
```json
{
  "decision": "block",
  "reason": "Why blocked",
  "hookSpecificOutput": {
    "additionalContext": "Context to add"
  }
}
```

## Best Practices

### 1. Keep Hooks Fast
- Default timeout: 60 seconds
- Use timeouts: `{"timeout": 30}`
- Parallel execution: Multiple hooks run simultaneously

### 2. Validate Inputs
```bash
#!/bin/bash
# Always validate input
if ! read input; then
  echo "No input received" >&2
  exit 1
fi

# Parse and validate
command=$(echo "$input" | jq -r '.tool_input.command')
if [ -z "$command" ]; then
  echo "Empty command" >&2
  exit 2
fi
```

### 3. Quote Variables
```bash
# Good
echo "Path: $CLAUDE_PROJECT_DIR"
cp "$file" "$dest"

# Bad (breaks on spaces/special chars)
echo Path: $CLAUDE_PROJECT_DIR
cp $file $dest
```

### 4. Use Absolute Paths
```bash
# Good
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$script_dir/helpers/validate.sh"

# Bad (depends on current directory)
./helpers/validate.sh
```

### 5. Handle Errors Gracefully
```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Your validation logic here

exit 0  # Explicit success
```

### 6. Log for Debugging
```bash
#!/bin/bash
exec 1> >(tee -a /tmp/hook.log)
exec 2>&1
echo "[$(date)] Hook started"
echo "[$(date)] Input: $input"
echo "[$(date)] Hook completed"
```

### 7. Prevent Circular Hooks
```bash
#!/bin/bash
# Check if already in hook
if [ -n "${IN_HOOK:-}" ]; then
  exit 0  # Prevent recursion
fi
export IN_HOOK=1
```

## Anti-Patterns (Avoid)

❌ **No validation**: Scripts that don't check inputs
❌ **Silent failures**: Exit 0 on error
❌ **Blocking operations**: Long-running hooks without timeout
❌ **Circular dependencies**: Hook A triggers hook B triggers A
❌ **Overly broad matchers**: `*` when specific tools needed
❌ **No error handling**: Missing `set -euo pipefail`
❌ **Hardcoded paths**: Using `$PWD` instead of env vars

## Security Patterns

### Pattern 1: Path Traversal Protection
```bash
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
if [[ "$file_path" == *".."* ]]; then
  echo "Path traversal attempt detected" >&2
  exit 2
fi
```

### Pattern 2: Command Allowlist
```bash
command=$(echo "$input" | jq -r '.tool_input.command')
if [[ "$command" =~ ^(ls|cat|grep|find)\ .* ]]; then
  exit 0  # Allowed
else
  echo "Command not in allowlist: $command" >&2
  exit 2  # Block
fi
```

### Pattern 3: File Type Validation
```bash
file_path=$(echo "$input" | jq -r '.tool_input.file_path')
ext="${file_path##*.}"
case "$ext" in
  md|txt|json|yaml|yml) exit 0 ;;  # Allowed
  *) echo "File type not allowed: $ext" >&2; exit 2 ;;
esac
```

## Debugging Hooks

### Enable Debug Output
```bash
claude --debug
```

Shows:
- Which hooks matched
- Hook execution status
- Output/errors

### Test Hooks Manually
```bash
# Create test input
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | bash hook.sh

# Check exit code
echo $?
```

### Common Issues
| Symptom | Cause | Fix |
|---------|-------|-----|
| Hook not running | Wrong event name | Check case sensitivity |
| Matcher not matching | Wrong tool name | Verify exact name |
| Timeout errors | Hook too slow | Add timeout, optimize |
| No output | Exit code != 0 | Check stderr |
| Infinite loop | Circular hooks | Add guard variables |

## Configuration Locations

### User Hooks
`~/.claude/settings.json`

### Project Hooks
`.claude/settings.json`

### Local Hooks
`.claude/settings.local.json`

### Plugin Hooks
`plugin/hooks/hooks.json`

**Merging**: Plugin hooks merged with user/project hooks

## Volatile Details (Look Up)

These change frequently:
- Exact JSON field names in input/output
- New hook events (check latest docs)
- Prompt hook response schema
- Timeout defaults

**Always verify**: Use `curl -sL https://code.claude.com/docs/en/hooks.md | rg pattern`

---

## Official Documentation Links

- **Hooks Reference**: https://code.claude.com/docs/en/hooks.md
- **Hooks Guide**: https://code.claude.com/docs/en/hooks-guide
- **Plugin Components Reference**: https://code.claude.com/docs/en/plugins-reference.md
- **Settings & Configuration**: https://code.claude.com/docs/en/settings.md
- **Claude Code Overview**: https://code.claude.com/docs/en/overview

### Verification
Last verified: 2026-01-13
