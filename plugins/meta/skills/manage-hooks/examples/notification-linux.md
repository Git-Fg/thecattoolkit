# Example: Linux Notification Hook

Display a native Linux notification (using notify-send) when Claude needs input.

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input' --urgency=normal"
          }
        ]
      }
    ]
  }
}
```
