# Hooks Configuration Template

## File Location

```bash
.claude/hooks/hooks.json
```

## Template Structure

```json
{
  "description": "{Hook description - what this hook set accomplishes}",
  "hooks": {
    "{EventType}": [
      {
        "matcher": "{ToolPattern}",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/.claude/hooks/scripts/{hook-name}.py",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

## Configuration Fields

### description
- **Type**: String
- **Purpose**: Human-readable description of what these hooks do
- **Example**: `"Security checks to detect secrets before file operations"`

### Event Types

#### PreToolUse
- **Trigger**: Before a tool executes
- **Use For**: Validation, security checks, blocking operations
- **Can Block**: Yes
- **Example**: `"PreToolUse"`

#### PostToolUse
- **Trigger**: After a tool completes
- **Use For**: Type checking, formatting, logging
- **Can Block**: No
- **Example**: `"PostToolUse"`

#### UserPromptSubmit
- **Trigger**: User submits a prompt
- **Use For**: Prompt validation, preprocessing
- **Can Block**: Yes
- **Example**: `"UserPromptSubmit"`

#### PermissionRequest
- **Trigger**: Permission dialog is shown
- **Use For**: Automated permission handling
- **Can Block**: Yes
- **Example**: `"PermissionRequest"`

#### Stop
- **Trigger**: Claude attempts to stop
- **Use For**: Task completion validation
- **Can Block**: Yes (with stop_hook_active check)
- **Example**: `"Stop"`

#### SubagentStart
- **Trigger**: A subagent starts
- **Use For**: Subagent initialization
- **Can Block**: No
- **Example**: `"SubagentStart"`

#### SubagentStop
- **Trigger**: A subagent stops
- **Use For**: Subagent completion validation
- **Can Block**: Yes
- **Example**: `"SubagentStop"`

#### SessionStart
- **Trigger**: When session begins
- **Use For**: Context injection, setup tasks
- **Can Block**: No
- **Example**: `"SessionStart"`

#### SessionEnd
- **Trigger**: When session ends
- **Use For**: Cleanup tasks, final reports
- **Can Block**: No
- **Example**: `"SessionEnd"`

#### PreCompact
- **Trigger**: Before context compaction
- **Use For**: State validation before compaction
- **Can Block**: Yes
- **Example**: `"PreCompact"`

#### Notification
- **Trigger**: When Claude sends notifications
- **Use For**: Desktop notifications, alerts
- **Can Block**: No
- **Example**: `"Notification"`

### Matcher Patterns

#### Tool-Specific
- `"Edit"` - Matches Edit tool
- `"Write"` - Matches Write tool
- `"Bash"` - Matches Bash tool
- `"Read"` - Matches Read tool

#### Multiple Tools
- `"Edit|Write"` - Matches Edit OR Write
- `"Bash|Shell"` - Matches Bash OR Shell

#### Regex Patterns
- `"mcp__.*"` - Matches all MCP tools
- `"git-.*"` - Matches git-related tools
- `".*\\.py$"` - Matches Python files (in file paths)

### Command Configuration

#### type
- **Values**: `"command"` or `"prompt"`
- **command**: Executes a shell command (use for deterministic checks)
- **prompt**: Uses LLM to evaluate (use for complex decisions)
- **Example**: `"command"` or `"prompt"`

#### command
- **Required when**: `type` is `"command"`
- **Format**: Executable with arguments
- **Required**: Use absolute paths with environment variables
- **Example**: `"python3 ${CLAUDE_PLUGIN_ROOT}/.claude/hooks/scripts/security-check.py"`
- **WHY**: Absolute paths prevent path injection vulnerabilities

#### prompt
- **Required when**: `type` is `"prompt"`
- **Format**: Text prompt with optional `$ARGUMENTS` placeholder
- **Use for**: Natural language evaluation, context-aware decisions
- **Example**: `"Check if safe: $ARGUMENTS\nReturn {\"decision\": \"approve\" or \"block\"}"`
- **WHY**: LLM can handle complex reasoning that would be difficult to code

#### timeout
- **Type**: Integer (milliseconds)
- **Default**: 30000 (30 seconds)
- **Recommended**:
  - Fast checks: 10000-30000ms
  - Type checking: 30000-60000ms
  - Complex operations: 60000-120000ms
- **WHY**: Prevents hanging hooks from blocking Claude indefinitely

#### Environment Variables
- **${CLAUDE_PLUGIN_ROOT}**: Root directory of the plugin
- **${CLAUDE_PROJECT_DIR}**: Current working directory
- **WHY**: Ensures hooks work regardless of where Claude is invoked

## Complete Example

```json
{
  "description": "Security checks to detect secrets before file operations",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/.claude/hooks/scripts/security-check.py",
            "timeout": 30000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/.claude/hooks/scripts/type-check.py",
            "timeout": 60000
          }
        ]
      }
    ]
  }
}
```

## Security Checklist

- [ ] Uses absolute paths with environment variables (${CLAUDE_PLUGIN_ROOT})
- [ ] Has timeout configured (default: 30000ms)
- [ ] JSON validated with `jq . .claude/hooks/hooks.json`
- [ ] Scripts have proper permissions if needed
- [ ] Stop hooks check `stop_hook_active` flag

## Validation Commands

```bash
# Validate JSON syntax
jq . .claude/hooks/hooks.json

# Test hook script independently
python3 .claude/hooks/scripts/{hook-name}.py < test-input.json

# Debug mode testing
claude --debug
```
