# Example: Log All Bash Commands

Log every bash command executed by Claude to a local file with timestamps.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"[\" + (.timestamp // now | todate) + \"] \" + .tool_input.command + \" - \" + (.tool_input.description // \"No description\")' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```
