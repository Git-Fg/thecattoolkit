---
name: manage-hooks
description: Event-driven automation hooks for Claude Code. Security-hardened templates for PreToolUse, PostToolUse, SessionStart, and other hook events.
allowed-tools: Read Write Edit Bash Grep
---

## Protocol Overview

Hooks are event-driven automation for Claude Code. They execute shell commands or LLM prompts in response to:

- **Tool Events**: Before (PreToolUse) or after (PostToolUse) tool execution
- **Session Events**: SessionStart, SessionEnd, PreCompact
- **User Events**: UserPromptSubmit, PermissionRequest
- **Agent Events**: Stop, SubagentStart, SubagentStop
- **System Events**: Notification

**Core Principle:** Hooks operate within an event hierarchy: events trigger matchers (tool patterns) which execute hooks (commands or prompts). Hooks can block actions, modify tool inputs, inject context, or observe and log operations.

## Quick Reference

**Hook Creation Pattern:**
1. **Identify Event Type:** Select from 11 supported event types
2. **Choose Hook Type:** Command hook (shell) or Prompt hook (LLM)
3. **Configure Matcher:** Tool pattern filter (optional for some events)
4. **Define Action:** Shell command or LLM prompt
5. **Test:** Use `claude --debug` for verification

## Available Resources

### Templates and Assets

#### Python Templates (`assets/templates/`)

- **`base-hook.py`** - Core template with path validation, error handling, and security patterns
- **`blocking-hook.py`** - Template for PreToolUse/Stop hooks that can approve/block actions
- **`observer-hook.py`** - Template for PostToolUse/SessionStart hooks that observe/report
- **`hooks-json.md`** - Complete guide to hooks.json configuration structure

#### Utilities (`assets/scripts/`)

- **`path-validator.py`** - Reusable utility for validating file paths and preventing traversal attacks
- **`hook-tester.py`** - Automated validation tool supporting all 11 hook event types

**Usage**: Import or copy these into `.claude/hooks/scripts/` for use in hook configurations.

### Example: File Protection Hook

```
.claude/hooks/
├── hooks.json              # Hook configuration
└── scripts/
    └── protect-files.py    # Hook script
```

**Configuration**:
```json
{
  "description": "File protection and security checks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/.claude/hooks/scripts/protect-files.py"
          }
        ]
      }
    ]
  }
}
```

## Hook Event Types

### Supported Events (11 total)

| Event | Fires | Can Block? | Matcher Required? |
|-------|-------|-------------|-------------------|
| **PreToolUse** | Before tool execution | Yes | Yes |
| **PostToolUse** | After tool execution | No | Yes |
| **UserPromptSubmit** | User submits a prompt | Yes | No |
| **PermissionRequest** | Permission dialog shown | Yes | No |
| **Stop** | Claude attempts to stop | Yes | No |
| **SubagentStart** | Subagent starts | No | No |
| **SubagentStop** | Subagent attempts to stop | Yes | No |
| **SessionStart** | Session begins | No | No |
| **SessionEnd** | Session ends | No | No |
| **PreCompact** | Before context compaction | Yes | No |
| **Notification** | Claude sends notifications | No | No |

See `references/hook-types.md` for complete event documentation including input/output schemas and use cases.

## Hook Types

### Command Hook

**Type**: Executes a shell command

**Configuration**:
```json
{
  "type": "command",
  "command": "/path/to/script.sh",
  "timeout": 30000
}
```

**Use cases**: Simple validation, logging, external tools, notifications

**Input**: JSON via stdin
**Output**: JSON via stdout (optional)

### Prompt Hook

**Type**: LLM evaluates a prompt

**Configuration**:
```json
{
  "type": "prompt",
  "prompt": "Evaluate if this command is safe: $ARGUMENTS\n\nReturn JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
}
```

**Use cases**: Complex decision logic, natural language validation, context-aware checks, reasoning

**Input**: Prompt with `$ARGUMENTS` placeholder
**Output**: JSON with `decision` and `reason`

## Matchers

Matchers filter which tools trigger the hook:

```json
{
  "matcher": "Bash",             // Exact match
  "matcher": "Write|Edit",      // Multiple tools (regex OR)
  "matcher": "mcp__.*",         // All MCP tools
  "matcher": "mcp__memory__.*"   // Specific MCP server
}
```

**Optional for**: UserPromptSubmit, PermissionRequest, Stop, SubagentStart, SubagentStop, SessionStart, SessionEnd, PreCompact, Notification

## Input/Output Protocol

**Input Format**: JSON via stdin
```json
{
  "session_id": "string",
  "transcript_path": "path",
  "cwd": "path",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions",
  "hook_event_name": "EventName",
  "event_specific_data": "varies"
}
```

**Output Format**: JSON via stdout (blocking hooks)
```json
{
  "decision": "approve" | "block",
  "reason": "explanation",
  "continue": true,
  "systemMessage": "warning"
}
```

See `references/input-output-schemas.md` for complete schemas per event type.

## Environment Variables

Available in hook commands:

- `$CLAUDE_PROJECT_DIR` - Project root directory
- `${CLAUDE_PLUGIN_ROOT}` - Plugin directory (plugin hooks only)
- `$ARGUMENTS` - Hook input JSON (prompt hooks only)

## Working Examples

Ready-to-use patterns can be found in the `examples/` directory:

| Example | Description |
|---------|-------------|
| **[notification-macos.md](examples/notification-macos.md)** | Desktop notifications for macOS |
| **[notification-linux.md](examples/notification-linux.md)** | Desktop notifications for Linux |
| **[block-destructive.md](examples/block-destructive.md)** | Prevent dangerous commands (rm -rf, git push --force) |
| **[autoformat-prettier.md](examples/autoformat-prettier.md)** | Auto-format code after edits |
| **[linter-check.md](examples/linter-check.md)** | Run linters and fix issues automatically |
| **[session-context.md](examples/session-context.md)** | Inject sprint, branch, or environment context |
| **[workflow-automation.md](examples/workflow-automation.md)** | Auto-commit, docs update, pre-commit hooks |
| **[logging-bash.md](examples/logging-bash.md)** | Log all shell commands |
| **[logging-file-ops.md](examples/logging-file-ops.md)** | Log file modifications |
| **[advanced-hooks.md](examples/advanced-hooks.md)** | Chaining, conditional execution, stop logic |

## Reference Documentation

**Hook Types**: `references/hook-types.md`
- Complete list of hook events
- When each event fires
- Input/output schemas for each event
- Blocking vs non-blocking behavior

**Command vs Prompt**: `references/command-vs-prompt.md`
- Decision tree: which type to use
- Command hook patterns and examples
- Prompt hook patterns and examples
- Performance considerations

**Matchers**: `references/matchers.md`
- Regex patterns for tool matching
- MCP tool matching patterns
- Multiple tool matching
- Debugging matcher issues

**Input/Output Schemas**: `references/input-output-schemas.md`
- Complete schema for each hook type
- Field descriptions and types
- Hook-specific output fields
- Example JSON for each event


**Troubleshooting**: `references/troubleshooting.md`
- Hooks not triggering
- Command execution failures
- Prompt hook issues
- Permission problems
- Timeout handling
- Debug workflow
