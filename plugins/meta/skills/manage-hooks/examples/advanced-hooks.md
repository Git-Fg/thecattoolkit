# Example: Advanced Hook Patterns

Complex patterns including intelligent stop logic, hook chaining, and conditional execution.

## Intelligent Stop Logic

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review the conversation: $ARGUMENTS\n\nCheck if:\n1. All user-requested tasks are complete\n2. Tests are passing (if code changes made)\n3. No errors that need fixing\n4. Documentation updated (if applicable)\n\nIf incomplete: {\"decision\": \"block\", \"reason\": \"specific issue\", \"systemMessage\": \"what needs to be done\"}\n\nIf complete: {\"decision\": \"approve\", \"reason\": \"all tasks done\"}\n\nIMPORTANT: If stop_hook_active is true, return {\"decision\": undefined} to avoid infinite loop",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

## Hook Chaining

Execute multiple hooks for the same event in order.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'First hook' >> /tmp/hook-chain.log"
          },
          {
            "type": "command",
            "command": "echo 'Second hook' >> /tmp/hook-chain.log"
          },
          {
            "type": "prompt",
            "prompt": "Final validation: $ARGUMENTS"
          }
        ]
      }
    ]
  }
}
```

## Conditional Execution (File Type)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/format-by-type.sh"
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
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

case "$file_path" in
  *.js|*.jsx|*.ts|*.tsx)
    prettier --write "$file_path"
    ;;
  *.py)
    black "$file_path"
    ;;
  *.go)
    gofmt -w "$file_path"
    ;;
esac
```
