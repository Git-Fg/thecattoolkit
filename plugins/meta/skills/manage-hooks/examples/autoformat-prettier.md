# Example: Auto-format with Prettier

Automatically run Prettier on files after they are edited by Claude.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$(echo {} | jq -r '.tool_input.file_path')\" 2>/dev/null || true",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```
