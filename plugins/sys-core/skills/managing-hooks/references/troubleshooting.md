# Troubleshooting Guide

## Common Issues

### Issue: Hook Not Firing

**Symptoms:**
- Hook configuration exists but doesn't trigger
- No error messages

**Diagnosis:**
```bash
# Check JSON syntax
jq . hooks/hooks.json

# Verify matcher pattern
jq '.hooks.PreToolUse[0].matcher' hooks/hooks.json
```

**Solutions:**
1. Verify matcher pattern matches tool name
2. Check JSON syntax
3. Restart Claude session
4. Enable debug logging

### Issue: Hook Timeout

**Symptoms:**
- Hook execution takes too long
- "Timeout" error message

**Diagnosis:**
```bash
# Test hook manually
bash ${CLAUDE_PLUGIN_ROOT}/scripts/hook.sh test_input
```

**Solutions:**
1. Increase timeout in configuration
2. Optimize hook script performance
3. Break complex operations into smaller checks
4. Use background processes for long operations

### Issue: Permission Denied

**Symptoms:**
- "Permission denied" error
- Script not executable

**Diagnosis:**
```bash
# Check file permissions
ls -la scripts/

# Test execution
bash scripts/hook.sh
```

**Solutions:**
1. Make scripts executable: `chmod +x scripts/*.sh`
2. Check file ownership
3. Verify SELinux/AppArmor policies
4. Run with appropriate user permissions

### Issue: Invalid JSON Output

**Symptoms:**
- "Invalid JSON" error
- Hook output not processed

**Diagnosis:**
```bash
# Test output format
bash scripts/hook.sh | jq .

# Check for debug output
bash -x scripts/hook.sh
```

**Solutions:**
1. Ensure output is valid JSON
2. Add error handling to script
3. Suppress debug output with `suppressOutput: true`
4. Use `set -euo pipefail` for safety

### Issue: Unexpected Exit Code

**Symptoms:**
- Hook fails with non-zero exit code
- Operation blocked or allowed incorrectly

**Diagnosis:**
```bash
# Test with sample input
echo '{"test": "data"}' | bash scripts/hook.sh
echo "Exit code: $?"
```

**Solutions:**
1. Use proper exit codes (0, 1, 2, 124)
2. Add error messages to stderr
3. Test with various inputs
4. Validate exit code behavior

## Debug Mode

Enable verbose logging:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash -x ${CLAUDE_PLUGIN_ROOT}/scripts/debug.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Testing Hooks

### Unit Test Script

```bash
#!/usr/bin/env bash
set -euo pipefail

# Test input
test_input='{
  "session_id": "test",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write"
}'

# Run hook
output=$(echo "$test_input" | bash scripts/hook.sh)
echo "Output: $output"

# Validate JSON
echo "$output" | jq .

# Check exit code
if [ $? -eq 0 ]; then
  echo "✓ Test passed"
else
  echo "✗ Test failed"
  exit 1
fi
```

### Test Cases

1. **Valid input** - Normal operation
2. **Invalid input** - Error handling
3. **Missing fields** - Validation
4. **Large input** - Performance
5. **Timeout scenario** - Long operation

## Logging and Monitoring

### Add Logging

```bash
exec 3>&1 4>&2
exec 1> >(tee -a /tmp/hook.log)
exec 2>&1

# Hook logic
echo "Hook executed at $(date)"

# Restore
exec 1>&3 2>&4
```

### Monitor Performance

```bash
start=$(date +%s%3N)
# ... operation ...
end=$(date +%s%3N)
duration=$((end - start))

{
  "continue": true,
  "systemMessage": "Execution time: ${duration}ms"
}
```

## Getting Help

1. Check logs: `/tmp/hook.log`
2. Test manually: `bash scripts/hook.sh`
3. Validate JSON: `jq . hooks/hooks.json`
4. Review timeout settings
5. Check file permissions
6. Test with sample data
7. Review security policies
8. Check environment variables

## Prevention Checklist

- [ ] All scripts use `set -euo pipefail`
- [ ] JSON validation in place
- [ ] Appropriate timeouts set
- [ ] File permissions correct
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Performance tested
- [ ] Security reviewed
