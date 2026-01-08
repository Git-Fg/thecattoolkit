# Example: Block Writes to Protected Files

Prevent modifications to critical project files like lockfiles or configuration.

## Hook Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-protected-files.sh"
          }
        ]
      }
    ]
  }
}
```

## Check Script (`check-protected-files.sh`)

```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# Protected files
protected_files=(
  "package-lock.json"
  ".env.production"
  "credentials.json"
)

for protected in "${protected_files[@]}"; do
  if [[ "$file_path" == *"$protected"* ]]; then
    echo "{\"decision\": \"block\", \"reason\": \"Cannot modify $protected\", \"systemMessage\": \"This file is protected from automated changes\"}"
    exit 0
  fi
done

echo '{"decision": "approve", "reason": "File is not protected"}'
```
