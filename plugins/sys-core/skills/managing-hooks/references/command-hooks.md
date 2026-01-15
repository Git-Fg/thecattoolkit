# Command Hooks Reference

## Overview

Command hooks execute bash scripts to perform fast, deterministic validations and operations. They are ideal for file system checks, external tool integration, and performance-critical operations.

## Implementation

### Basic Command Hook

```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 30
}
```

### Script Structure

Use `set -euo pipefail` for safety:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Validate inputs
if [ -z "${1:-}" ]; then
  echo "Error: Missing input" >&2
  exit 1
fi

# Perform validation
if ! some-check "$1"; then
  echo "Validation failed" >&2
  exit 2
fi

exit 0
```

## Best Practices

1. **Always use `set -euo pipefail`**
2. **Validate all inputs**
3. **Use proper exit codes**
4. **Quote variables**
5. **Keep scripts under 60 seconds**

## Security Considerations

- Never trust user input
- Sanitize all file paths
- Avoid logging sensitive data
- Use absolute paths with `${CLAUDE_PLUGIN_ROOT}`
