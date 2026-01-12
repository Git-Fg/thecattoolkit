# Input/Output Formats Reference

## Input Format

All hooks receive JSON via stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/directory",
  "permission_mode": "ask|allow|bypass",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file",
    "content": "file content"
  }
}
```

### Event-Specific Fields

**PreToolUse:**
- `tool_name`: Name of the tool being used
- `tool_input`: Tool-specific input data

**PostToolUse:**
- `tool_name`: Name of the tool used
- `tool_input`: Tool input data
- `tool_output`: Tool output data
- `duration_ms`: Execution time

**Stop:**
- `reason`: Stop reason
- `completed`: Boolean completion status

## Output Format

All hooks must output JSON:

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

### Output Fields

- **continue:** Boolean - Whether to proceed
- **suppressOutput:** Boolean - Hide stdout from Claude
- **systemMessage:** String - Message to display

## Exit Codes

- **0** - Success, continue, show stdout
- **1** - Non-blocking error, continue, log stderr
- **2** - Blocking error, halt operation
- **124** - Timeout

## Environment Variables

Available in command hooks:

- `$CLAUDE_PROJECT_DIR` - Project root
- `$CLAUDE_PLUGIN_ROOT` - Plugin directory
- `$CLAUDE_ENV_FILE` - SessionStart only
- `$CLAUDE_CODE_REMOTE` - Remote execution flag
