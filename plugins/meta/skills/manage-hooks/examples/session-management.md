# Example: Session Management

Automate session lifecycle tasks like archiving transcripts and tracking statistics.

## Archive Transcript

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/archive-session.sh"
          }
        ]
      }
    ]
  }
}
```

*Script:*
```bash
#!/bin/bash
input=$(cat)
transcript_path=$(echo "$input" | jq -r '.transcript_path')
session_id=$(echo "$input" | jq -r '.session_id')

# Create archive directory
archive_dir="$HOME/.claude/archives"
mkdir -p "$archive_dir"

# Copy transcript with timestamp
timestamp=$(date +%Y%m%d-%H%M%S)
cp "$transcript_path" "$archive_dir/${timestamp}-${session_id}.jsonl"

echo "Session archived to $archive_dir"
```

## Save Session Stats

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "jq '. + {ended_at: now}' >> ~/.claude/session-stats.jsonl"
          }
        ]
      }
    ]
  }
}
```
