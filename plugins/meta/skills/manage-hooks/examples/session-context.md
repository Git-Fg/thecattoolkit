# Example: Session Context Injection

Inject environment information or project context when a session starts.

## Load Environment Info

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": \"Environment: '$(hostname)'\\nNode version: '$(node --version 2>/dev/null || echo 'not installed')'\\nPython version: '$(python3 --version 2>/dev/null || echo 'not installed)'\"}}'"
          }
        ]
      }
    ]
  }
}
```

## Load Git Branch

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd \"$cwd\" && git branch --show-current | jq -Rs '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": (\"Current branch: \" + .)}}'"
          }
        ]
      }
    ]
  }
}
```
