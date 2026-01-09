# Hook Patterns Cookbook

This cookbook demonstrates common implementation patterns for Cat Toolkit hooks.

## 1. Automation Patterns

### Auto-format on Write/Edit
Automatically run Prettier on files after they are edited.
```json
{
  "matcher": "Write|Edit",
  "hooks": [
    {
      "type": "command",
      "command": "prettier --write \"$(echo {} | jq -r '.tool_input.file_path')\" 2>/dev/null || true"
    }
  ]
}
```

### Stop Guard (Test Coverage)
Prevent stopping if tests are failing.
```bash
#!/bin/bash
npm test > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo '{"decision": "approve", "reason": "Tests passing"}'
else
  echo '{"decision": "block", "reason": "Tests failing", "systemMessage": "Fix tests first"}'
fi
```

## 2. Security Patterns

### Block Destructive Operations
Prevent dangerous shell commands.
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command')

if [[ "$command" == *"rm -rf /"* ]] || [[ "$command" == *"mkfs"* ]]; then
  echo '{"decision": "block", "reason": "Destructive command detected"}'
  exit 0
fi
echo '{"decision": "approve"}'
```

### Protected Files
Prevent modifications to critical files.
```bash
#!/bin/bash
file_path=$(echo $(cat) | jq -r '.tool_input.file_path')
if [[ "$file_path" == *"package-lock.json"* ]] || [[ "$file_path" == *".env"* ]]; then
  echo '{"decision": "block", "reason": "File is protected"}'
  exit 0
fi
echo '{"decision": "approve"}'
```

## 3. Advanced Patterns

### Intelligent Stop Logic (Prompt)
```json
{
  "type": "prompt",
  "prompt": "Review conversation: $ARGUMENTS. Check if all tasks are done. If stop_hook_active is true, return {\"decision\": undefined}."
}
```

### Hook Chaining
Execute multiple hooks in order:
```json
{
  "matcher": "Bash",
  "hooks": [
    { "type": "command", "command": "echo 'Log' >> log.txt" },
    { "type": "prompt", "prompt": "Validate: $ARGUMENTS" }
  ]
}
```
