# Example: Block Destructive Commands

Prevent the execution of dangerous shell commands like `rm -rf` or specific git operations.

## Hook Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-command-safety.sh"
          }
        ]
      }
    ]
  }
}
```

## Safety Script (`check-command-safety.sh`)

```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

# Check for dangerous patterns
if [[ "$command" == *"rm -rf /"* ]] || \
   [[ "$command" == *"mkfs"* ]] || \
   [[ "$command" == *"> /dev/sda"* ]]; then
  echo '{"decision": "block", "reason": "Destructive command detected", "systemMessage": "This command could cause data loss"}'
  exit 0
fi

# Check for force push to main
if [[ "$command" == *"git push"*"--force"* ]] && \
   [[ "$command" == *"main"* || "$command" == *"master"* ]]; then
  echo '{"decision": "block", "reason": "Force push to main branch blocked", "systemMessage": "Use a feature branch instead"}'
  exit 0
fi

echo '{"decision": "approve", "reason": "Command is safe"}'
```
