---
name: hook-development
description: USE when user asks to "create a hook", "add a PreToolUse/PostToolUse/Stop hook", "validate tool use", "implement prompt-based hooks", "use ${CLAUDE_PLUGIN_ROOT}", "set up event-driven automation", "block dangerous commands", or mentions hook events (PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification). Provides comprehensive guidance for creating and implementing Claude Code plugin hooks with focus on advanced prompt-based hooks API and official documentation.
---

# Hook Development for Claude Code Plugins

## Overview

Hooks are the **security and automation layer** of Claude Code. They intercept events throughout the session lifecycle to validate operations, enforce policies, add context, and integrate with external systems.

**Key capabilities:**
- Intercept and validate tool calls before execution (PreToolUse)
- React to and analyze tool results (PostToolUse)
- Validate task completion (Stop, SubagentStop)
- Load project context at session start (SessionStart)
- Clean up resources at session end (SessionEnd)
- Validate user input (UserPromptSubmit)
- Add context before compaction (PreCompact)
- React to notifications (Notification)

## Hook Types

### Prompt-Based Hooks (LLM-Driven)

Use natural language for intelligent, context-aware validation:

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this tool use is appropriate: $TOOL_INPUT",
  "timeout": 30
}
```

**How it works:**
1. Hook receives structured event data
2. LLM analyzes the event using natural language reasoning
3. Returns structured JSON decision
4. Decision influences Claude Code behavior

**Supported events:** Stop, SubagentStop, UserPromptSubmit, PreToolUse

**Benefits:**
- Context-aware decisions based on full event data
- Handles edge cases without hardcoding
- Natural language criteria (easier to understand and modify)
- Adapts to new scenarios without code changes
- Better for complex validation logic

### Command Hooks (Bash-Driven)

Execute deterministic bash scripts for fast, reliable checks:

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 60
}
```

**How it works:**
1. Hook receives JSON event data via stdin
2. Bash script processes the data
3. Script outputs structured JSON decision
4. Claude Code acts on the decision

**Use cases:**
- Fast deterministic validations (< 100ms)
- File system operations and checks
- External tool integration
- Performance-critical validation
- Simple pattern matching

## Hook Configuration

### Plugin Hooks (hooks.json Format)

For plugin-specific hooks in `hooks/hooks.json`:

```json
{
  "description": "Security and validation hooks for the plugin",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate file write safety. Check for system paths, credentials, and path traversal."
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify task completion. Check that tests were run if code was modified."
          }
        ]
      }
    ]
  }
}
```

**Structure:**
- `description` (optional) - Human-readable explanation
- `hooks` (required) - Container for hook event definitions
- Events defined inside `hooks` object

### Settings Format (User-Level)

For user settings in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate file write operations"
          }
        ]
      }
    ]
  }
}
```

**Structure:**
- No description field
- Events at root level
- Merged with plugin hooks

### Hybrid Approach (Recommended)

Combine both plugin hooks and user settings:

**Plugin provides:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Plugin-level file validation"
          }
        ]
      }
    ]
  }
}
```

**User adds:**
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "User-level completion check"
          }
        ]
      }
    ]
  }
}
```

Both sets of hooks run in parallel.

## Hook Events Reference

### PreToolUse

**When:** Before any tool executes
**Purpose:** Approve, deny, or modify tool calls
**Decision:** `permissionDecision` (allow/deny/ask) or `updatedInput`

**Example - File Write Validation:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze file_path and content. Check: 1) Not system directories (/etc, /sys) 2) Not credential files (.env, secrets) 3) No path traversal (../) 4) Content doesn't expose secrets. Return JSON with decision and explanation."
        }
      ]
    }
  ]
}
```

**Input data:**
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

**Output formats:**

**Permission decision:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow",
    "reason": "File write is safe"
  }
}
```

**Modified input:**
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow",
    "updatedInput": {
      "content": "modified content"
    }
  }
}
```

**System message:**
```json
{
  "systemMessage": "Additional context for Claude"
}
```

### PostToolUse

**When:** After tool completes
**Purpose:** React to results, log, provide feedback
**Decision:** None (informational only)

**Example - Edit Result Analysis:**
```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze the edit result for potential issues: syntax errors, breaking changes, security concerns. Provide feedback if issues detected."
        }
      ]
    }
  ]
}
```

**Output:**
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Analysis results or feedback"
}
```

**Exit codes:**
- `0` - Success, output shown in transcript
- `2` - Blocking error, stderr fed back to Claude

### Stop

**When:** Main agent considers stopping
**Purpose:** Validate task completeness
**Decision:** `decision` (approve/block)

**Example - Completion Validation:**
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Review transcript at $TRANSCRIPT_PATH. Verify: 1) Tests ran after code changes 2) Build succeeded 3) User questions answered 4) All tasks complete. Return 'approve' or 'block' with reason."
        }
      ]
    }
  ]
}
```

**Output:**
```json
{
  "decision": "approve",
  "reason": "All checks passed",
  "systemMessage": "Completion summary"
}
```

### SubagentStop

**When:** Subagent completes
**Purpose:** Validate subagent task completion
**Decision:** Similar to Stop

**Example:**
```json
{
  "SubagentStop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verify subagent completed its task successfully"
        }
      ]
    }
  ]
}
```

### UserPromptSubmit

**When:** User submits prompt
**Purpose:** Add context, validate, or block input
**Decision:** None (contextual only)

**Example - Security Guidance:**
```json
{
  "UserPromptSubmit": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "If prompt discusses authentication, API keys, or security, provide relevant security guidance and best practices."
        }
      ]
    }
  ]
}
```

### SessionStart

**When:** Claude Code session begins
**Purpose:** Load context, set environment
**Decision:** None (setup only)

**Example - Project Detection:**
```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
        }
      ]
    }
  ]
}
```

**Special feature - Environment persistence:**
```bash
#!/bin/bash
# Write to $CLAUDE_ENV_FILE to persist environment variables
echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
echo "export USES_TYPESCRIPT=true" >> "$CLAUDE_ENV_FILE"
```

### SessionEnd

**When:** Session ends
**Purpose:** Cleanup, logging, state preservation
**Decision:** None (cleanup only)

### PreCompact

**When:** Before context compaction
**Purpose:** Add critical info to preserve
**Decision:** None (contextual only)

### Notification

**When:** Claude sends notifications
**Purpose:** React to notifications
**Decision:** None (reactive only)

## Input/Output Formats

### Standard Input (All Hooks)

All hooks receive JSON via stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/directory",
  "permission_mode": "ask|allow|bypass",
  "hook_event_name": "PreToolUse"
}
```

**Event-specific fields:**

**PreToolUse/PostToolUse:**
```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "..."
  },
  "tool_result": {
    "success": true
  }
}
```

**UserPromptSubmit:**
```json
{
  "user_prompt": "User's message text"
}
```

**Stop/SubagentStop:**
```json
{
  "reason": "Why stopping"
}
```

### Standard Output Format

**For prompt hooks:**
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

**For command hooks (same format):**
```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Analysis complete"
}
```

### Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| `0` | Success | Continue, show stdout in transcript |
| `1` | Non-blocking error | Continue, log error, show stderr |
| `2` | Blocking error | Halt operation, feed stderr to Claude |
| `124` | Timeout | Operation timed out |

## Environment Variables

Available in command hooks:

- `$CLAUDE_PROJECT_DIR` - Project root directory
- `$CLAUDE_PLUGIN_ROOT` - Plugin directory (use for portability)
- `$CLAUDE_ENV_FILE` - SessionStart only: persist env vars
- `$CLAUDE_CODE_REMOTE` - Set if running remotely

**Always use `${CLAUDE_PLUGIN_ROOT}` for portability:**
```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

**SessionStart environment persistence:**
```bash
#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" || exit 1

# Detect project type
if [ -f "package.json" ]; then
  echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
fi

# Persist variable for session
echo "export DETECTED_FRAMEWORK=react" >> "$CLAUDE_ENV_FILE"
```

## Matchers

### Tool Name Matching

**Exact match:**
```json
"matcher": "Write"
```

**Multiple tools:**
```json
"matcher": "Write|Edit|Read"
```

**Wildcard (all tools):**
```json"matcher": "*"
```

**Regex patterns:**
```json
"matcher": "mcp__.*__delete.*"  // All MCP delete tools
"matcher": "Bash.*init"         // Bash commands matching pattern
```

### Common Patterns

```json
// All file operations
"matcher": "Read|Write|Edit"

// All Bash commands
"matcher": "Bash"

// All MCP tools
"matcher": "mcp__.*"

// Specific plugin's MCP tools
"matcher": "mcp__plugin_asana_.*"

// All tools from specific MCP server
"matcher": "mcp__.*_database__.*"
```

**Note:** Matchers are case-sensitive and use string matching or regex.

## Security Best Practices

### Input Validation

**Always validate in command hooks:**
```bash
#!/bin/bash
set -euo pipefail

input=$(cat)

# Extract and validate tool name
tool_name=$(echo "$input" | jq -r '.tool_name // empty')

if [ -z "$tool_name" ]; then
  echo '{"continue": true, "systemMessage": "No tool name found"}' >&2
  exit 0
fi

# Validate format (alphanumeric and underscores only)
if [[ ! "$tool_name" =~ ^[a-zA-Z0-9_]+$ ]]; then
  echo '{"continue": true, "systemMessage": "Invalid tool name format"}' >&2
  exit 1
fi
```

### Path Safety

```bash
#!/bin/bash
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Deny path traversal
if [[ "$file_path" == *".."* ]]; then
  echo '{"continue": true, "systemMessage": "Path traversal detected"}' >&2
  exit 1
fi

# Check for system directories
if [[ "$file_path" == /etc/* ]] || [[ "$file_path" == /sys/* ]]; then
  echo '{"continue": true, "systemMessage": "Cannot access system directories"}' >&2
  exit 1
fi

# Check for sensitive files
if [[ "$file_path" == *.env* ]] || [[ "$file_path" == *secret* ]]; then
  echo '{"continue": true, "systemMessage": "Sensitive file detected"}' >&2
  exit 1
fi
```

### Variable Quoting

```bash
# GOOD: Properly quoted
echo "$file_path"
cd "$CLAUDE_PROJECT_DIR"
cat "$input_file"

# BAD: Unquoted (injection risk)
echo $file_path
cd $CLAUDE_PROJECT_DIR
cat $input_file
```

### Timeout Configuration

```json
{
  "type": "command",
  "command": "bash script.sh",
  "timeout": 30
}
```

**Guidelines:**
- Command hooks: 60s default
- Prompt hooks: 30s default
- Quick checks: 5-10s
- Complex validation: 30-60s
- Maximum: 600s (10 minutes)

## Performance Optimization

### Parallel Execution

All matching hooks in the same event run **in parallel**:

```json
{
  "PreToolUse": [
    {
      "matcher": "Write",
      "hooks": [
        {"type": "command", "command": "check1.sh"},  // Runs in parallel
        {"type": "command", "command": "check2.sh"},  // Runs in parallel
        {"type": "prompt", "prompt": "Validate..."}    // Runs in parallel
      ]
    }
  ]
}
```

**Design implications:**
- Hooks execute simultaneously
- No guaranteed order
- Hooks don't see each other's output
- Design for independence

### Optimization Strategies

1. **Use command hooks for fast checks (< 100ms)**
   - Simple pattern matching
   - File existence checks
   - Size validations

2. **Use prompt hooks for complex logic**
   - Context-aware decisions
   - Multi-criteria validation
   - Natural language reasoning

3. **Cache expensive operations**
   ```bash
   # Cache validation results
   cache_key=$(echo "$file_path" | md5sum | cut -d' ' -f1)
   cache_file="/tmp/hook-cache-$cache_key"

   if [ -f "$cache_file" ] && [ $(($(date +%s) - $(stat -f%m "$cache_file"))) -lt 300 ]; then
     cat "$cache_file"
     exit 0
   fi
   ```

4. **Minimize I/O in hot paths**
   - Read files once
   - Batch validations
   - Avoid network calls in PreToolUse

## Hook Lifecycle

### Loading and Activation

**Important:** Hooks are loaded when Claude Code **starts**.

**Cannot hot-swap:**
- Editing `hooks/hooks.json` requires restart
- Adding new scripts requires restart
- Changing hook configuration requires restart

**Workflow:**
1. User starts Claude Code session
2. Claude Code loads all hooks from plugins and settings
3. Validates hook configuration
4. Registers hooks for events
5. Hooks active for entire session
6. Changes require Claude Code restart

### Testing Hooks

**Validate configuration:**
```bash
# Check JSON syntax
jq empty hooks/hooks.json

# Validate structure
./scripts/validate-hook-schema.sh hooks/hooks.json
```

**Test hook scripts:**
```bash
# Create sample input
./scripts/test-hook.sh --create-sample PreToolUse > test-input.json

# Test with sample data
./scripts/test-hook.sh -v scripts/validate-write.sh test-input.json
```

**Debug in Claude Code:**
```bash
claude --debug
```

Look for:
- Hook registration messages
- Hook execution logs
- Input/output JSON
- Timing information

### Viewing Loaded Hooks

Use `/hooks` command in Claude Code to see:
- All loaded hooks
- Hook configuration
- Matchers and events
- Hook sources (plugin vs user)

## Common Patterns

### Pattern 1: Security Validation

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Validate file write safety. Check: 1) Not system directories (/etc, /sys, /usr) 2) Not credential files (.env, secrets, keys) 3) No path traversal (../) 4) Content doesn't expose secrets or tokens. Return decision with explanation."
        }
      ]
    },
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Validate bash command safety. Check for: 1) Destructive operations (rm -rf, dd, mkfs) 2) Privilege escalation (sudo, su) 3) Network operations without user consent 4) System modifications. Return decision with explanation."
        }
      ]
    }
  ]
}
```

### Pattern 2: Quality Enforcement

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Verify task completion. Review transcript: 1) If code was modified (Write/Edit used), were tests executed? 2) Did builds succeed? 3) Were all user questions answered? 4) Is documentation updated? Return 'approve' or 'block' with specific reasons."
        }
      ]
    }
  ]
}
```

### Pattern 3: Context Loading

```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/detect-project.sh"
        }
      ]
    }
  ]
}
```

**Project detection script:**
```bash
#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" || exit 1

# Detect project type and set environment
if [ -f "package.json" ]; then
  echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"

  if [ -f "tsconfig.json" ]; then
    echo "export USES_TYPESCRIPT=true" >> "$CLAUDE_ENV_FILE"
  fi
elif [ -f "Cargo.toml" ]; then
  echo "export PROJECT_TYPE=rust" >> "$CLAUDE_ENV_FILE"
elif [ -f "pyproject.toml" ]; then
  echo "export PROJECT_TYPE=python" >> "$CLAUDE_ENV_FILE"
fi
```

### Pattern 4: MCP Tool Protection

```json
{
  "PreToolUse": [
    {
      "matcher": "mcp__.*__delete.*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Destructive operation detected via MCP. Verify: 1) Is deletion intentional and safe? 2) Can operation be undone? 3) Are there backups? 4) Does user have permission? Return 'allow' only if all checks pass."
        }
      ]
    }
  ]
}
```

### Pattern 5: Notification Logging

```json
{
  "Notification": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/log-notification.sh"
        }
      ]
    }
  ]
}
```

**Logging script:**
```bash
#!/bin/bash
input=$(cat)
timestamp=$(date -Iseconds)

# Append to audit log
echo "$timestamp | $USER | Notification | $input" >> ~/.claude/notification-audit.log

exit 0
```

## Troubleshooting

### Hook Not Executing

**Checklist:**
1. Is Claude Code restarted after configuration changes?
2. Is hook configuration valid JSON?
3. Does matcher match the event?
4. Is script executable (`chmod +x`)?
5. Is path correct (use `${CLAUDE_PLUGIN_ROOT}`)?
6. Check `/hooks` command output

### Hook Times Out

**Solutions:**
1. Reduce timeout in configuration
2. Optimize script performance
3. Move complex logic to prompt hooks
4. Add early returns for fast paths
5. Cache expensive operations

### Hook Fails Silently

**Checklist:**
1. Verify exit code (0 for success, 2 for blocking error)
2. Check stderr output (`>&2`)
3. Ensure JSON output is valid
4. Review debug logs (`claude --debug`)
5. Test script directly with sample input

### Unexpected Behavior

**Debugging steps:**
1. Enable verbose logging: `claude --debug`
2. Check transcript for hook execution
3. Verify input data matches expectations
4. Test with minimal hook first
5. Add logging to identify issue location

## Best Practices Summary

### DO

✅ **Use prompt hooks for complex validation**
- Natural language criteria
- Context-aware decisions
- Easy to modify and understand

✅ **Use ${CLAUDE_PLUGIN_ROOT} for all paths**
- Ensures portability
- Works across different environments
- No hardcoded absolute paths

✅ **Validate all inputs in command hooks**
- Check tool names
- Validate file paths
- Sanitize user data

✅ **Quote all bash variables**
- Prevents injection
- Handles spaces correctly
- `"$variable"` not `$variable`

✅ **Set appropriate timeouts**
- Quick checks: 5-10s
- Standard operations: 30s
- Complex validation: 60s

✅ **Test hooks before deployment**
- Use test scripts
- Validate JSON
- Check with sample data

### DON'T

❌ **Hardcode absolute paths**
- Use environment variables
- Makes hooks non-portable

❌ **Trust user input without validation**
- Always sanitize inputs
- Check for injection attempts
- Validate data types

❌ **Create long-running hooks**
- Keep under 60 seconds
- Use timeouts
- Optimize performance

❌ **Rely on hook execution order**
- Hooks run in parallel
- No guaranteed sequence
- Design for independence

❌ **Log sensitive information**
- Don't log credentials
- Sanitize error messages
- Protect user data

## Quick Reference

### Hook Events Summary

| Event | When | Purpose | Prompt Support |
|-------|------|---------|----------------|
| PreToolUse | Before tool | Validation/modification | ✅ Yes |
| PostToolUse | After tool | Feedback/logging | ✅ Yes |
| UserPromptSubmit | User input | Context/validation | ✅ Yes |
| Stop | Agent stops | Completion check | ✅ Yes |
| SubagentStop | Subagent done | Task validation | ✅ Yes |
| SessionStart | Session begins | Setup/context | ❌ Command only |
| SessionEnd | Session ends | Cleanup | ❌ Command only |
| PreCompact | Before compact | Preserve context | ❌ Command only |
| Notification | User notified | Reactions | ❌ Command only |

### Configuration Checklist

- [ ] Valid JSON syntax
- [ ] Correct hook event names
- [ ] Proper matcher patterns
- [] Valid hook types (command/prompt)
- [ ] Appropriate timeouts set
- [ ] Scripts executable
- [ ] Paths use ${CLAUDE_PLUGIN_ROOT}
- [ ] Input validation implemented
- [ ] Error handling added
- [ ] Tested with sample data

## Additional Resources

### Official Documentation

- **Hook System**: https://code.claude.com/docs/en/hooks
- **Hook Guide**: https://code.claude.com/docs/en/hooks-guide
- **Plugin Development**: https://code.claude.com/docs/en/plugins
- **Settings Reference**: https://code.claude.com/docs/en/settings

### Reference Files

- **`references/patterns.md`** - Common hook patterns and use cases
- **`references/migration.md`** - Migrating from command to prompt hooks
- **`references/advanced.md`** - Advanced techniques and workflows

### Example Scripts

- **`examples/validate-write.sh`** - File write validation
- **`examples/validate-bash.sh`** - Bash command validation
- **`examples/load-context.sh`** - SessionStart context loading

### Utility Scripts

- **`scripts/validate-hook-schema.sh`** - Validate hooks.json structure
- **`scripts/test-hook.sh`** - Test hooks with sample data
- **`scripts/hook-linter.sh`** - Check scripts for issues

## Implementation Workflow

To implement hooks in a plugin:

1. **Identify requirements**
   - What events to hook?
   - What validation needed?
   - Security or quality focus?

2. **Choose hook types**
   - Prompt hooks for complex logic
   - Command hooks for fast checks
   - Hybrid for multi-stage validation

3. **Write hook scripts** (if using command hooks)
   - Use `set -euo pipefail`
   - Read input from stdin
   - Validate all inputs
   - Output structured JSON

4. **Configure hooks**
   - Edit `hooks/hooks.json`
   - Use `${CLAUDE_PLUGIN_ROOT}` for paths
   - Set appropriate timeouts

5. **Validate configuration**
   ```bash
   ./scripts/validate-hook-schema.sh hooks/hooks.json
   ```

6. **Test hooks**
   ```bash
   ./scripts/test-hook.sh scripts/validate-write.sh test-input.json
   ./scripts/hook-linter.sh scripts/*.sh
   ```

7. **Test in Claude Code**
   ```bash
   claude --debug
   ```

8. **Document hooks**
   - Explain purpose in README
   - Document configuration options
   - Provide usage examples

**Focus areas:**
- **Security**: Use prompt hooks for intelligent validation
- **Performance**: Use command hooks for fast checks
- **Usability**: Provide clear configuration options
- **Maintainability**: Write clear, well-documented code

## Conclusion

Hooks are powerful tools for securing and automating Claude Code workflows. Use prompt-based hooks for complex, context-aware validation and command hooks for fast, deterministic checks. Always validate inputs, use proper timeouts, and test thoroughly before deployment.