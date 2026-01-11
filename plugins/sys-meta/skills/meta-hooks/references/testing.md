# Hook Testing Procedures

## Overview

Hooks intercept critical operations. Proper testing is essential to ensure they work correctly without breaking workflows.

## Testing Strategy

### 1. Schema Validation

Test that `hooks.json` is valid JSON and follows the schema.

```bash
# Validate JSON syntax
jq empty hooks/hooks.json

# Check for required fields
jq '.hooks' hooks/hooks.json

# List configured events
jq '.hooks | keys' hooks/hooks.json
```

### 2. Hook Script Testing

Test hook scripts independently before integrating.

```bash
# Test with success case
echo '{"file_path": "test.txt"}' | hooks/scripts/validate.sh
echo "Exit code: $?"

# Test with failure case
echo '{"file_path": "/etc/passwd"}' | hooks/scripts/validate.sh
echo "Exit code: $?"
```

### 3. Exit Code Testing

Verify exit codes produce correct behavior.

**Test Exit Code 0 (Success):**
```bash
#!/bin/bash
# test-success.sh
exit 0
```

Expected: Action continues, no error shown.

**Test Exit Code 1 (Warning):**
```bash
#!/bin/bash
# test-warning.sh
echo "Warning: minor issue" >&2
exit 1
```

Expected: Action continues, warning shown.

**Test Exit Code 2 (Blocking):**
```bash
#!/bin/bash
# test-block.sh
echo "Error: action blocked" >&2
exit 2
```

Expected: Action blocked, error shown.

### 4. Integration Testing

Test hooks within the actual runtime environment.

#### SessionStart Hook Test

**Test Hook:**
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo 'Session started' > /tmp/session-start-test.txt"
      }]
    }]
  }
}
```

**Test Procedure:**
1. Start Claude Code
2. Check if file was created: `cat /tmp/session-start-test.txt`
3. Clear and restart to verify it runs again

#### PreToolUse Hook Test

**Test Hook:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "grep -o '\"file_path\":\"[^\"]*\"' | grep -o '/etc/' && exit 2 || exit 0"
      }]
    }]
  }
}
```

**Test Procedure:**
1. Try writing to safe file: Should succeed
2. Try writing to `/etc/`: Should be blocked

#### Prompt Hook Test

**Test Hook:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Return JSON: {\"ok\": true}"
      }]
    }]
  }
}
```

**Test Procedure:**
1. Invoke any tool
2. Verify action continues (ok: true response)

## Common Issues and Solutions

### Issue: Hook Not Running

**Symptoms:** Hook script never executes

**Diagnosis:**
```bash
# Check hook file exists
ls -la hooks/hooks.json

# Check JSON is valid
jq empty hooks/hooks.json

# Check event name spelling
jq '.hooks | keys' hooks/hooks.json
```

**Solutions:**
- Ensure `hooks.json` is in correct location
- Verify JSON syntax is valid
- Check event name is correct

### Issue: Exit Code Not Working

**Symptoms:** Exit code 2 doesn't block action

**Diagnosis:**
```bash
# Test script directly
./hooks/scripts/block.sh
echo "Exit code: $?"

# Check script has execute permission
ls -l hooks/scripts/block.sh

# Check shebang line
head -1 hooks/scripts/block.sh
```

**Solutions:**
- Add execute permission: `chmod +x hooks/scripts/block.sh`
- Add shebang: `#!/bin/bash` or `#!/usr/bin/env python3`
- Ensure exit code is actually 2, not 1

### Issue: Prompt Hook Timing Out

**Symptoms:** Hook hangs, then timeout error

**Diagnosis:**
```bash
# Check prompt complexity
jq '.hooks[].hooks[].prompt | length' hooks/hooks.json

# Check timeout value
jq '.hooks[].hooks[].timeout' hooks/hooks.json
```

**Solutions:**
- Simplify prompt
- Increase timeout if needed
- Consider command hook instead

### Issue: Environment Variables Not Available

**Symptoms:** Script can't access `${CLAUDE_PLUGIN_ROOT}`

**Diagnosis:**
```bash
# Test env var in script
echo "Plugin root: ${CLAUDE_PLUGIN_ROOT}" > /tmp/env-test.txt

# Check location (plugin vs project hooks)
# ${CLAUDE_PLUGIN_ROOT} only available in plugin hooks
```

**Solutions:**
- Use `$CLAUDE_PROJECT_DIR` for project hooks
- Use `${CLAUDE_PLUGIN_ROOT}` for plugin hooks
- Use absolute paths as fallback

## Automated Testing

### Test Script Template

```bash
#!/bin/bash
# test-hooks.sh

echo "Testing hooks..."

# Test 1: Schema validation
echo "Test 1: Schema validation"
jq empty hooks/hooks.json || exit 1

# Test 2: Success case
echo "Test 2: Success exit code"
echo '{}' | hooks/scripts/validate.sh
[ $? -eq 0 ] || exit 1

# Test 3: Blocking case
echo "Test 3: Blocking exit code"
echo '{"dangerous": true}' | hooks/scripts/validate.sh
[ $? -eq 2 ] || exit 1

# Test 4: Warning case
echo "Test 4: Warning exit code"
echo '{}' | hooks/scripts/warning.sh
[ $? -eq 1 ] || exit 1

echo "All tests passed!"
```

### Integration Test Template

```bash
#!/bin/bash
# integration-test.sh

echo "Integration testing hooks..."

# Setup
export TEST_DIR="/tmp/hook-test-$$"
mkdir -p "$TEST_DIR"

# Test SessionStart
echo "Test: SessionStart hook"
# Start Claude with test hook
# Check if test file was created

# Test PreToolUse
echo "Test: PreToolUse hook"
# Trigger tool use
# Check if hook blocked/allowed correctly

# Cleanup
rm -rf "$TEST_DIR"

echo "Integration tests passed!"
```

## Validation Checklist

### Schema Validation

- [ ] `hooks.json` is valid JSON
- [ ] Top-level `hooks` object exists
- [ ] Event names are correct
- [ ] Hook definitions have required fields

### Script Validation

- [ ] Scripts have execute permissions
- [ ] Scripts have shebang line
- [ ] Scripts return correct exit codes
- [ ] Error messages written to stderr

### Integration Validation

- [ ] Hooks run on expected events
- [ ] Exit code 0 allows actions
- [ ] Exit code 1 warns but continues
- [ ] Exit code 2 blocks actions
- [ ] Prompt hooks return valid JSON
- [ ] Timeouts are appropriate

### Performance Validation

- [ ] Hooks complete quickly (<5 seconds for command hooks)
- [ ] Prompt hook timeouts configured
- [ ] No unnecessary LLM calls
- [ ] Minimal performance impact

## Best Practices

1. **Test scripts independently** before integrating
2. **Use exit code assertions** in tests
3. **Test both success and failure cases**
4. **Verify timeout behavior**
5. **Check performance impact**
6. **Log hook execution** for debugging
7. **Use gradual rollout** for production hooks
