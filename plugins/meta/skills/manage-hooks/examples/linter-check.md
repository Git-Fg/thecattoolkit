# Example: Run Linter After Edits

Run eslint on modified files and fix issues automatically where possible.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "eslint \"$(echo {} | jq -r '.tool_input.file_path')\" --fix 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```
