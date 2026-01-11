# Exit Code Protocol

## Overview

Command hooks communicate results through exit codes. The exit code determines whether the original action proceeds or is blocked.

## Exit Codes

### Exit Code 0: Success (Continue)

**Meaning:** Hook completed successfully, action should proceed.

**Behavior:**
- Action continues normally
- No warning logged
- No interruption

**Use Cases:**
- Validation passed
- Safety checks passed
- Setup completed successfully

**Example:**
```bash
#!/bin/bash
# Validation script - all checks passed
exit 0
```

### Exit Code 1: Non-Blocking Warning

**Meaning:** Hook detected a warning, but action should continue.

**Behavior:**
- Action continues
- Warning logged to stderr
- No interruption to user

**Use Cases:**
- Minor issues detected
- Configuration inconsistencies
- Deprecated usage warnings

**Example:**
```bash
#!/bin/bash
# Check for deprecated configuration
if [ -f old-config.conf ]; then
  echo "Warning: old-config.conf is deprecated" >&2
  exit 1  # Non-blocking warning
fi
exit 0
```

### Exit Code 2: Blocking Error

**Meaning:** Hook detected a critical issue, action should be blocked.

**Behavior:**
- **Action is BLOCKED**
- Only stderr is used as error message
- JSON in stdout is NOT processed
- User sees the error message

**Use Cases:**
- Security violations
- Missing dependencies
- Invalid configurations
- Safety check failures

**Example:**
```bash
#!/bin/bash
# Security check - block dangerous operations
DANGER_PATTERNS="rm -rf / \..*etc/passwd"

for pattern in $DANGER_PATTERNS; do
  if echo "$1" | grep -q "$pattern"; then
    echo "Error: Dangerous operation detected" >&2
    exit 2  # Blocking error
  fi
done

exit 0
```

## Exit Code Behavior Summary

| Exit Code | Action Continues | User Notified | Stderr Used | Stdout Processed |
|:---------:|:----------------:|:-------------:|:-----------:|:----------------:|
| 0 | ✓ | ✗ | ✗ | ✗ |
| 1 | ✓ | ✓ (warning) | ✓ | ✗ |
| 2 | ✗ | ✓ (error) | ✓ | ✗ |

## Command Hook Pattern

### Standard Validation Hook

```bash
#!/bin/bash
# hooks/validate.sh

# Read tool arguments from stdin
ARGUMENTS=$(cat)

# Run validation
if ! validate "$ARGUMENTS"; then
  echo "Validation failed: $REASON" >&2
  exit 2
fi

# Warning example
if has_minor_issue "$ARGUMENTS"; then
  echo "Warning: minor issue detected" >&2
  exit 1
fi

exit 0
```

### Safety Check Hook

```bash
#!/bin/bash
# hooks/safety-check.sh

ARGUMENTS=$(cat)

# Block dangerous operations
if is_dangerous "$ARGUMENTS"; then
  echo "Error: Operation not permitted" >&2
  exit 2
fi

exit 0
```

### Environment Check Hook

```bash
#!/bin/bash
# hooks/env-check.sh

# Check required dependencies
if ! command -v git &> /dev/null; then
  echo "Error: git is required but not installed" >&2
  exit 2
fi

# Warning for optional dependency
if ! command -v node &> /dev/null; then
  echo "Warning: node not found, some features unavailable" >&2
  exit 1
fi

exit 0
```

## Prompt Hook JSON Protocol

Prompt hooks use a different protocol - they return JSON instead of exit codes.

### Success Response

```json
{
  "ok": true
}
```

**Behavior:** Action continues

### Block Response

```json
{
  "ok": false,
  "reason": "Explanation for why the action was blocked"
}
```

**Behavior:** Action is blocked, reason shown to user

## Choosing: Command vs Prompt Hook

| Factor | Command Hook | Prompt Hook |
|:-------|:-------------|:------------|
| **Speed** | Fast (script execution) | Slower (LLM evaluation) |
| **Complexity** | Simple rules | Complex reasoning |
| **Cost** | No token cost | Consumes tokens |
| **Use Case** | Safety checks, validation | Semantic evaluation |

**Best Practice:** Use command hooks for fast, rule-based checks. Use prompt hooks only when complex semantic understanding is required.

## Examples

### Command Hook: Block Dangerous Bash Commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/bash-guard.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**bash-guard.sh:**
```bash
#!/bin/bash
ARGUMENTS=$(cat)

DANGER_PATTERNS=(
  "rm -rf /"
  "rm -rf \.\./.*\.\./.*"
  "> /etc/"
  ":(){ :|:& };:"  # Fork bomb
)

for pattern in "${DANGER_PATTERNS[@]}"; do
  if echo "$ARGUMENTS" | grep -q "$pattern"; then
    echo "Error: Dangerous command pattern detected" >&2
    exit 2
  fi
done

exit 0
```

### Prompt Hook: Semantic Safety Check

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if this action is safe: $ARGUMENTS\n\nReturn JSON with ok field. If unsafe, set ok to false and include reason field.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Testing Exit Codes

### Test Blocking Behavior

```bash
# Should block
echo "rm -rf /" | ./hooks/bash-guard.sh
echo "Exit code: $?"  # Should be 2

# Should pass
echo "ls -la" | ./hooks/bash-guard.sh
echo "Exit code: $?"  # Should be 0
```

### Test Warning Behavior

```bash
# Should warn but continue
./hooks/env-check.sh
echo "Exit code: $?"  # Should be 1
```

## Validation Checklist

- [ ] Exit code 0 for success (action continues)
- [ ] Exit code 1 for warnings (action continues, user notified)
- [ ] Exit code 2 for blocking errors (action blocked)
- [ ] Error messages written to stderr
- [ ] Dangerous operations blocked
- [ ] Timeout configured appropriately
- [ ] Script has execute permissions
- [ ] Shebang line present (#!/bin/bash)
