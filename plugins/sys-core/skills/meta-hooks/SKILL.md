---
name: meta-hooks
description: "Provides comprehensive hook development guidance for Claude Code plugins. MUST Use when creating hooks, implementing PreToolUse/PostToolUse/Stop hooks, or configuring event-driven automation. Do not use for general automation, workflow management, or task execution."
---

# Hook Development for Claude Code Plugins

Hooks are the **security and automation layer** of Claude Code. They intercept events throughout the session lifecycle to validate operations, enforce policies, add context, and integrate with external systems.

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

**Benefits:** Context-aware decisions, handles edge cases, natural language criteria, adapts to new scenarios, complex validation logic

**See:** `references/prompt-hooks.md`

### Command Hooks (Bash-Driven)
Execute deterministic bash scripts for fast, reliable checks:

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 60
}
```

**Use cases:** Fast validations (<100ms), file system operations, external tool integration, performance-critical checks

**See:** `references/command-hooks.md`

## Hook Configuration

Plugin hooks use `hooks/hooks.json` format:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate file write safety"
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
            "prompt": "Verify task completion"
          }
        ]
      }
    ]
  }
}
```

**See:** `references/configuration.md`

## Hook Events

| Event | When | Purpose | Decision |
|-------|------|---------|----------|
| **PreToolUse** | Before tool | Validation/modification | allow/deny/ask |
| **PostToolUse** | After tool | Feedback/logging | None |
| **Stop** | Agent stops | Completion check | approve/block |
| **SessionStart** | Session begins | Setup/context | None |
| **SessionEnd** | Session ends | Cleanup | None |
| **UserPromptSubmit** | User input | Validation | None |
| **SubagentStop** | Subagent done | Task validation | approve/block |

**See:** `references/events.md`

## Input/Output Formats

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

**See:** `references/io-formats.md`

### Output Format

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

### Exit Codes

- **0** - Success, continue, show stdout
- **1** - Non-blocking error, continue, log stderr
- **2** - Blocking error, halt operation
- **124** - Timeout

**See:** `references/exit-codes.md`

## Environment Variables

Available in command hooks:
- `$CLAUDE_PROJECT_DIR` - Project root directory
- `$CLAUDE_PLUGIN_ROOT` - Plugin directory (use for portability)
- `$CLAUDE_ENV_FILE` - SessionStart only
- `$CLAUDE_CODE_REMOTE` - Set if running remotely

**Always use `${CLAUDE_PLUGIN_ROOT}` for portability.**

## Matchers

**Exact:** `"Write"`
**Multiple:** `"Write|Edit|Read"`
**Wildcard:** `"*"`
**Regex:** `"mcp__.*__delete.*"` (all MCP delete tools)

## Security Best Practices

### DO ✅
- Use prompt hooks for complex validation
- Use `${CLAUDE_PLUGIN_ROOT}` for all paths
- Validate all inputs in command hooks
- Quote all bash variables
- Set appropriate timeouts (5-10s quick, 30s standard, 60s complex)

### DON'T ❌
- Hardcode absolute paths
- Trust user input without validation
- Create long-running hooks (>60s)
- Rely on hook execution order (hooks run in parallel)
- Log sensitive information

## Reference Materials

**Core Documentation:**
- `references/prompt-hooks.md` - Prompt-based implementation
- `references/command-hooks.md` - Command-based implementation
- `references/configuration.md` - Configuration guide
- `references/events.md` - All events with examples
- `references/io-formats.md` - Input/output formats
- `references/security.md` - Security practices
- `references/performance.md` - Performance optimization
- `references/troubleshooting.md` - Common issues

**Implementation Workflow:**
1. Identify requirements (what events? what validation?)
2. Choose hook types (prompt for complex, command for fast)
3. Write hook scripts (use set -euo pipefail)
4. Configure hooks (edit hooks/hooks.json)
5. Validate configuration
6. Test hooks with sample data
7. Document hooks

**Focus:** Security (prompt hooks), Performance (command hooks), Usability, Maintainability

## Conclusion

Use prompt-based hooks for complex, context-aware validation and command hooks for fast, deterministic checks. Always validate inputs, use proper timeouts, and test thoroughly.

**Next Steps:**
- Review `references/` for detailed documentation
- Examine `examples/` for working implementations
- Test with minimal configuration first
