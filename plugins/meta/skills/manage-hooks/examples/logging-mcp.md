# Example: Audit Trail for MCP Operations

Log all MCP tool usage to a JSONL file.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "jq '. + {timestamp: now}' >> ~/.claude/mcp-audit.jsonl"
          }
        ]
      }
    ]
  }
}
```
