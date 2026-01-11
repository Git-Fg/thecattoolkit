# Environment Variables in Hooks

## Overview

Hooks have access to specific environment variables depending on their scope and trigger event. Understanding these variables is critical for writing effective hook scripts.

## Global Variables

Available in ALL hook contexts:

| Variable | Description | Syntax Variants |
|:----------|:-------------|:----------------|
| `CLAUDE_PROJECT_DIR` | Project root directory | `$CLAUDE_PROJECT_DIR`, `${CLAUDE_PROJECT_DIR}` |

**Example:**
```bash
#!/bin/bash
# Hook script
PROJECT_ROOT="${CLAUDE_PROJECT_DIR}"
echo "Project: $PROJECT_ROOT"
```

## Plugin-Specific Variables

Available ONLY in plugin hooks (hooks configured in `plugins/*/hooks/hooks.json`):

| Variable | Description | Example |
|:----------|:-------------|:--------|
| `CLAUDE_PLUGIN_ROOT` | Plugin root directory | `/path/to/plugin` |

**Critical:** `${CLAUDE_PLUGIN_ROOT}` is NOT available in project-level hooks (`.claude/settings.json`).

**Example:**
```bash
#!/bin/bash
# Plugin hook script
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
SCRIPT="${PLUGIN_ROOT}/scripts/validate.sh"
```

## SessionStart-Specific Variables

Available ONLY during SessionStart hooks:

| Variable | Description | Usage |
|:----------|:-------------|:------|
| `CLAUDE_ENV_FILE` | Environment file path | Write-only, persist env vars |

**Usage Pattern:**
```bash
#!/bin/bash
# SessionStart hook

# Persist environment variable for session duration
echo 'export MY_VAR=value' >> "$CLAUDE_ENV_FILE"

# This variable will be available in all subsequent tool calls
```

**Important Notes:**
- File is write-only (append)
- Variables persist for session duration
- Use for setup configuration

## Tool Argument Variables

Available in PreToolUse and PostToolUse hooks:

| Variable | Description | Example |
|:----------|:-------------|:--------|
| `ARGUMENTS` | Tool arguments as JSON | `{"file_path": "/path/to/file"}` |
| `TOOL_NAME` | Name of tool being invoked | `Write`, `Bash`, `Read` |

**Access Pattern:**
```bash
#!/bin/bash
# PreToolUse hook

# Arguments come via stdin
ARGUMENTS=$(cat)

# Parse with jq
FILE_PATH=$(echo "$ARGUMENTS" | jq -r '.file_path')

# Validate
if [ "$FILE_PATH" = "/etc/passwd" ]; then
  echo "Error: Cannot modify system files" >&2
  exit 2
fi
```

## Variable Expansion

### In JSON Configuration

Variables are expanded in hook configuration:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/init.sh",
        "timeout": 30
      }]
    }]
  }
}
```

### In Bash Scripts

Standard bash variable expansion:

```bash
#!/bin/bash
# Use quotes for safety
SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/script.sh"

# Use default values if not set
TIMEOUT=${HOOK_TIMEOUT:-30}

# Conditional usage
if [ -n "${CLAUDE_PLUGIN_ROOT}" ]; then
  # Running in plugin context
  PLUGIN_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/check.sh"
else
  # Running in project context
  PROJECT_SCRIPT="${CLAUDE_PROJECT_DIR}/.claude/scripts/check.sh"
fi
```

## Path Best Practices

### Plugin Hooks

Always use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths:

```json
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/guard.sh"
      }]
    }]
  }
}
```

### Project Hooks

Use `$CLAUDE_PROJECT_DIR` for project-relative paths:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PROJECT_DIR}/.claude/scripts/init.sh"
      }]
    }]
  }
}
```

### Absolute Paths (Fallback)

When environment variables are uncertain:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "/usr/local/bin/validate.sh"
      }]
    }]
  }
}
```

## Security Considerations

### Path Traversal Prevention

**Bad:** User-controlled paths
```bash
#!/bin/bash
# DANGEROUS
USER_PATH="$1"
cat "$USER_PATH"  # Could be ../../etc/passwd
```

**Good:** Validate and sanitize
```bash
#!/bin/bash
USER_PATH="$1"
# Resolve to absolute path and check it's within project
REAL_PATH=$(realpath "$USER_PATH")
if [[ "$REAL_PATH" != "${CLAUDE_PROJECT_DIR}"* ]]; then
  echo "Error: Path outside project" >&2
  exit 2
fi
cat "$REAL_PATH"
```

### Command Injection Prevention

**Bad:** Unsanitized input in command
```bash
#!/bin/bash
# DANGEROUS
USER_FILE="$1"
cat "$USER_FILE"  # Could be 'file; rm -rf /'
```

**Good:** Use proper quoting
```bash
#!/bin/bash
USER_FILE="$1"
cat "$USER_FILE"  # Properly quoted
```

### Plugin Root Validation

**Best Practice:** Validate plugin root before using

```bash
#!/bin/bash
# Validate CLAUDE_PLUGIN_ROOT
if [ -z "${CLAUDE_PLUGIN_ROOT}" ]; then
  echo "Error: CLAUDE_PLUGIN_ROOT not set" >&2
  exit 2
fi

if [ ! -d "${CLAUDE_PLUGIN_ROOT}" ]; then
  echo "Error: CLAUDE_PLUGIN_ROOT not a directory" >&2
  exit 2
fi

PLUGIN_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/script.sh"
```

## Debugging Environment Variables

### Test Script

```bash
#!/bin/bash
# debug-env.sh

echo "=== Environment Variables ==="
echo "CLAUDE_PROJECT_DIR: ${CLAUDE_PROJECT_DIR}"
echo "CLAUDE_PLUGIN_ROOT: ${CLAUDE_PLUGIN_ROOT}"
echo "CLAUDE_ENV_FILE: ${CLAUDE_ENV_FILE}"

echo "=== Tool Arguments (if applicable) ==="
if [ -n "$ARGUMENTS" ]; then
  echo "ARGUMENTS: $ARGUMENTS"
fi

if [ -n "$TOOL_NAME" ]; then
  echo "TOOL_NAME: $TOOL_NAME"
fi
```

### Usage in Hook

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/debug-env.sh > /tmp/hook-env-debug.txt"
      }]
    }]
  }
}
```

## Quick Reference

| Variable | Available In | Scope |
|:----------|:-------------|:------|
| `$CLAUDE_PROJECT_DIR` | All hooks | Global |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin hooks only | Plugin |
| `$CLAUDE_ENV_FILE` | SessionStart only | Session |
| `$ARGUMENTS` | PreToolUse, PostToolUse | Tool event |
| `$TOOL_NAME` | PreToolUse, PostToolUse | Tool event |

## Validation Checklist

- [ ] Correct environment variable for hook scope
- [ ] `${CLAUDE_PLUGIN_ROOT}` only in plugin hooks
- [ ] `$CLAUDE_PROJECT_DIR` used in project hooks
- [ ] Paths properly quoted
- [ ] Path traversal protection implemented
- [ ] Command injection prevention implemented
- [ ] Variables validated before use
- [ ] Fallback paths for uncertain contexts
