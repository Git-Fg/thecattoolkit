# Security Best Practices

## Core Principles

1. **Never trust user input**
2. **Validate all paths**
3. **Use least privilege**
4. **Audit all operations**
5. **Never log secrets**

## Input Validation

### File Paths

```bash
# Validate file path
if [[ "$1" =~ ^[[:alnum:]/._-]+$ ]]; then
  echo "Invalid path" >&2
  exit 2
fi

# Sanitize path
file_path=$(realpath -m "$1")
```

### Command Arguments

```bash
# Validate arguments
if [ ${#} -ne 1 ]; then
  echo "Usage: $0 <file_path>" >&2
  exit 1
fi
```

## Secure Scripting

### Safe Bash Practices

```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Disable globbing
set -f

# Use variables
file_path="${1}"
content="${2:-}"

# Validate before use
[ -n "$file_path" ] || exit 1

# Quote variables
echo "Processing: $file_path"
```

## Common Vulnerabilities

### Path Traversal

### DON'T:**
```bash
cat "$1"  # Could be ../../../etc/passwd
```

### DO:**
```bash
# Resolve and validate path
file_path=$(realpath -m "$1")
if [[ ! "$file_path" =~ ^$(pwd)/ ]]; then
  echo "Path outside directory" >&2
  exit 2
fi
```

### Command Injection

### DON'T:**
```bash
eval "rm $1"  # Could be "file; rm -rf /"
```

### DO:**
```bash
rm -- "$1"  # Use proper argument handling
```

## Logging Security

- Never log passwords, tokens, or API keys
- Redact sensitive fields in JSON
- Use `logger` for system logs
- Sanitize error messages

## Best Practices Checklist

- [ ] Use `set -euo pipefail`
- [ ] Validate all inputs
- [ ] Quote all variables
- [ ] Check file paths are within allowed directories
- [ ] Use absolute paths with `${CLAUDE_PLUGIN_ROOT}`
- [ ] Set appropriate timeouts (max 60s)
- [ ] Never use `eval` or backticks for user input
- [ ] Sanitize all outputs
- [ ] Use least privilege for file permissions
- [ ] Audit all hook executions
