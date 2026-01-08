# Example: Run Tests Before Stopping

Prevent the agent from stopping if tests are failing.

## Hook Configuration

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/check-tests.sh"
          }
        ]
      }
    ]
  }
}
```

## Check Script (`check-tests.sh`)

```bash
#!/bin/bash
cd "$cwd" || exit 1

# Run tests
npm test > /dev/null 2>&1

if [ $? -eq 0 ]; then
  echo '{"decision": "approve", "reason": "All tests passing"}'
else
  echo '{"decision": "block", "reason": "Tests are failing. Please fix before stopping.", "systemMessage": "Run npm test to see failures"}'
fi
```
