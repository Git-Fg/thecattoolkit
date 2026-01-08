# Example: Workflow Automation

Automate routine tasks like commits, documentation updates, and pre-commit checks.

## Auto-commit After Changes

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/auto-commit.sh"
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
cd "$cwd" || exit 1

# Check if there are changes
if ! git diff --quiet; then
  git add -A
  git commit -m "chore: auto-commit from claude session" --no-verify
  echo '{"systemMessage": "Changes auto-committed"}'
fi
```

## Update Documentation

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/update-docs.sh",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

## Run Pre-commit Hooks

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-pre-commit.sh"
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
command=$(echo "$input" | jq -r '.tool_input.command')

# If git commit, run pre-commit hooks first
if [[ "$command" == *"git commit"* ]]; then
  pre-commit run --all-files > /dev/null 2>&1

  if [ $? -ne 0 ]; then
    echo '{"decision": "block", "reason": "Pre-commit hooks failed", "systemMessage": "Fix formatting/linting issues first"}'
    exit 0
  fi
fi

echo '{"decision": "approve", "reason": "ok"}'
```
