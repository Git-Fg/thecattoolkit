# Example: Log File Operations

Log every file write or edit operation to a local file.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"[\" + (now | todate) + \"] \" + .tool_name + \": \" + .tool_input.file_path' >> ~/.claude/file-operations.log"
          }
        ]
      }
    ]
  }
}
```
