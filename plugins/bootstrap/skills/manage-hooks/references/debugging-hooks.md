# Hook Debugging Guide

## Overview

This guide provides comprehensive debugging workflows for Claude Code hooks. Hooks can fail silently, making diagnosis difficult. This guide provides systematic approaches to identify and fix common hook issues.

## Quick Diagnostic Commands

```bash
# 1. Check hook configuration validity
jq . .claude/hooks/hooks.json
python3 manage-hooks/assets/scripts/hook-tester.py validate .claude/hooks/hooks.json

# 2. Check script permissions
find .claude/hooks/scripts -type f -name "*.py" -exec ls -la {} \;

# 3. Test all hooks in the suite
python3 manage-hooks/assets/scripts/hook-tester.py test .claude/hooks/hooks.json

# 4. Security check all hooks
python3 manage-hooks/assets/scripts/hook-tester.py security-check .claude/hooks/hooks.json
```

## Debugging Workflow

### Phase 1: Configuration Validation

**Goal:** Ensure hooks.json is syntactically correct and structurally valid.

**Steps:**
1. **JSON Syntax Check:**
   ```bash
   jq . .claude/hooks/hooks.json
   ```
   If this fails, fix JSON syntax errors.

2. **Schema Validation:**
   ```bash
   python3 manage-hooks/assets/scripts/hook-tester.py validate .claude/hooks/hooks.json
   ```
   This checks for:
   - Missing required fields (description, hooks)
   - Invalid event types
   - Missing matchers where required
   - Invalid hook types (must be 'command' or 'prompt')
   - Missing command/prompt fields
   - Invalid timeout values

**Common Configuration Errors:**
- Missing 'matcher' field for PreToolUse/PostToolUse events
- Using 'matcher' field for events that don't require it (SessionStart, etc.)
- Invalid event type (typo in event name)
- Hook type 'command' without 'command' field
- Hook type 'prompt' without 'prompt' field

### Phase 2: Permission Verification

**Goal:** Ensure all hook scripts are executable.

**Steps:**
1. **List all hook scripts with permissions:**
   ```bash
   find .claude/hooks/scripts -type f -name "*.py" | while read file; do
     ls -la "$file"
   done
   ```

2. **Fix permissions if needed:**
   ```bash
   find .claude/hooks/scripts -type f -name "*.py" -exec chmod +x {} \;
   ```

**Symptoms of Permission Issues:**
- "Permission denied" errors
- Scripts appear in hooks.json but never execute
- Hook seems to hang or fail immediately

### Phase 3: Individual Hook Testing

**Goal:** Test each hook script independently with controlled input.

**For PreToolUse/PostToolUse Hooks:**

Test with realistic tool event data:
```bash
# Test Edit tool hook
echo '{
  "tool": "Edit",
  "arguments": {
    "file_path": "test.txt",
    "old_string": "old",
    "new_string": "new"
  }
}' | python3 .claude/hooks/scripts/{hook-name}.py

# Test Read tool hook
echo '{
  "tool": "Read",
  "arguments": {
    "file_path": "test.txt"
  }
}' | python3 .claude/hooks/scripts/{hook-name}.py
```

**For Stop Hooks:**

Test with stop_hook_active flag:
```bash
echo '{
  "stop_hook_active": false
}' | python3 .claude/hooks/scripts/stop-hook.py
```

**For Session Hooks:**

Test with session data:
```bash
echo '{
  "session_id": "test-session",
  "timestamp": "2026-01-09T00:00:00Z"
}' | python3 .claude/hooks/scripts/session-start-hook.py
```

**What to Look For:**
- Script runs without crashing (exit code 0)
- Script outputs valid JSON to stdout
- Script outputs to stderr for logging (acceptable)
- Script handles edge cases gracefully

### Phase 4: JSON Output Validation

**Goal:** Ensure hooks produce valid JSON output that Claude Code can parse.

**Blocking Hook Output (PreToolUse, Stop, etc.):**

Valid patterns:
```json
{"status": "approve"}
{"status": "block", "reason": "security_policy", "message": "Access denied"}
{"status": "approve", "updatedInput": {"file_path": "safe.txt"}}
```

**Observer Hook Output (PostToolUse, SessionStart, etc.):**

Valid patterns:
```json
{"status": "success"}
{"status": "success", "systemMessage": "Operation completed"}
```

**Invalid Output Examples:**
```json
# Missing quotes around keys
{status: "approve"}

# Trailing commas
{"status": "approve",}

# Non-JSON text
Success!
{"status": "approve"}

# Wrong field name
{"decision": "approve"}
```

**Testing JSON Validity:**
```bash
# Test a hook and validate its output
output=$(echo '{"tool": "Edit", "arguments": {}}' | python3 .claude/hooks/scripts/hook.py)
echo "$output" | jq .
```

If `jq .` fails, the JSON is invalid.

### Phase 5: Runtime Analysis

**Goal:** Identify runtime issues (timeouts, infinite loops, dependency problems).

**Enable Verbose Logging:**
```bash
# Run hook with Python traceback on error
echo '{"tool": "Edit", "arguments": {}}' | python3 -u .claude/hooks/scripts/hook.py 2>&1

# Test with timeout to catch hangs
timeout 10s bash -c 'echo '{"tool": "Edit", "arguments": {}}' | python3 .claude/hooks/scripts/hook.py'
```

**Common Runtime Issues:**

1. **Import Errors:**
   ```
   ModuleNotFoundError: No module named 'requests'
   ```
   **Fix:** Use stdlib alternatives or document required dependencies

2. **Path Errors:**
   ```
   FileNotFoundError: script-config.json
   ```
   **Fix:** Use absolute paths with environment variables

3. **Infinite Loops:**
   Hook never returns
   **Fix:** Add timeout handling, break conditions

4. **Exception Handling:**
   ```
   Unhandled exception in hook
   ```
   **Fix:** Wrap logic in try/except blocks

### Phase 6: Integration Testing

**Goal:** Test hooks in realistic Claude Code scenarios.

**Test with Debug Mode:**
```bash
claude --debug
```
This enables verbose logging that shows hook execution.

**Test Individual Events:**

Force specific events:
```bash
# Test PreToolUse by editing a file
claude edit test.txt

# Test PostToolUse by running a tool
claude read test.txt

# Test Stop by ending session
claude # then Ctrl+C or /exit
```

## Common Failure Modes

### 1. Silent Failures

**Symptom:** Hook configured but never seems to run.

**Possible Causes:**
- Script not executable (chmod +x missing)
- Wrong script path in hooks.json
- Event never triggered (check matcher pattern)

**Debugging:**
```bash
# Verify script exists and is executable
ls -la .claude/hooks/scripts/hook.py

# Test script directly
python3 .claude/hooks/scripts/hook.py

# Check matcher pattern is correct
jq '.hooks.PreToolUse[0].matcher' .claude/hooks/hooks.json
```

### 2. Hook Blocks Everything

**Symptom:** Claude becomes unresponsive, all operations blocked.

**Possible Causes:**
- Hook always returns `{"status": "block"}`
- Logic error in blocking condition
- Missing `stop_hook_active` check in Stop hooks

**Debugging:**
```bash
# Test hook with various inputs
echo '{"tool": "Read", "arguments": {"file_path": "safe.txt"}}' | python3 .claude/hooks/scripts/hook.py

# Check for stop_hook_active in Stop hooks
grep -n "stop_hook_active" .claude/hooks/scripts/stop-hook.py
```

**Fix:** Review blocking logic, add more specific conditions.

### 3. Hook Timeout

**Symptom:** Operations hang, hooks exceed timeout.

**Possible Causes:**
- Network calls without timeout
- Infinite loops
- Blocking I/O operations
- Slow external commands

**Debugging:**
```bash
# Add timeout to test
timeout 5s bash -c 'echo '{"tool": "Edit", "arguments": {}}' | python3 .claude/hooks/scripts/slow-hook.py'
```

**Fix:** Add timeouts to network calls, optimize logic, increase hook timeout in config.

### 4. Invalid JSON Output

**Symptom:** "Failed to parse hook output" errors.

**Possible Causes:**
- Print statements mixed with JSON output
- Python exceptions not caught
- json.dumps() not used
- Unicode encoding issues

**Debugging:**
```bash
# Capture exact output
output=$(echo '{"tool": "Edit", "arguments": {}}' | python3 .claude/hooks/scripts/hook.py)
echo "OUTPUT: $output"
echo "$output" | jq .

# Check for print statements in hook
grep -n "print(" .claude/hooks/scripts/hook.py
```

**Fix:** Ensure only JSON to stdout, use print(json.dumps(data)), wrap in try/except.

### 5. Hook Crashes

**Symptom:** Python tracebacks in logs.

**Possible Causes:**
- Syntax errors
- Import errors
- Type errors
- Index/key errors

**Debugging:**
```bash
# Run with full traceback
echo '{"tool": "Edit", "arguments": {}}' | python3 -u .claude/hooks/scripts/hook.py 2>&1

# Check Python syntax
python3 -m py_compile .claude/hooks/scripts/hook.py
```

**Fix:** Add error handling, validate inputs, fix syntax errors.

## Debugging Tools

### Hook Tester Script

The `hook-tester.py` script provides three diagnostic modes:

1. **validate:** Check hooks.json structure
2. **test:** Run all hooks with test data
3. **security-check:** Audit for security issues

Example:
```bash
python3 manage-hooks/assets/scripts/hook-tester.py validate .claude/hooks/hooks.json
python3 manage-hooks/assets/scripts/hook-tester.py test .claude/hooks/hooks.json
python3 manage-hooks/assets/scripts/hook-tester.py security-check .claude/hooks/hooks.json
```

### Quick Test Script

Create a comprehensive test script:

```bash
#!/bin/bash
# test-hooks.sh - Comprehensive hook testing

echo "=== Hook Configuration Validation ==="
jq . .claude/hooks/hooks.json && echo "✓ JSON valid" || echo "✗ JSON invalid"
python3 manage-hooks/assets/scripts/hook-tester.py validate .claude/hooks/hooks.json

echo -e "\n=== Permission Check ==="
find .claude/hooks/scripts -name "*.py" -exec ls -la {} \;

echo -e "\n=== Individual Hook Tests ==="
for script in .claude/hooks/scripts/*.py; do
  echo "Testing $(basename $script)..."
  echo '{"tool": "Edit", "arguments": {"file_path": "test.txt"}}' | python3 "$script" > /tmp/hook-output.json 2>&1
  if [ $? -eq 0 ]; then
    echo "✓ $(basename $script) executed"
    if jq . /tmp/hook-output.json > /dev/null 2>&1; then
      echo "  ✓ Valid JSON output"
    else
      echo "  ✗ Invalid JSON output"
      cat /tmp/hook-output.json
    fi
  else
    echo "✗ $(basename $script) failed"
    cat /tmp/hook-output.json
  fi
done

echo -e "\n=== Full Test Suite ==="
python3 manage-hooks/assets/scripts/hook-tester.py test .claude/hooks/hooks.json
python3 manage-hooks/assets/scripts/hook-tester.py security-check .claude/hooks/hooks.json
```

## Security Considerations

When debugging hooks, be aware of security implications:

1. **Path Traversal:** Test with paths like `../../../etc/passwd`
2. **Code Injection:** Avoid eval(), exec() with user input
3. **Privilege Escalation:** Don't run hooks as root
4. **Information Disclosure:** Don't log sensitive data
5. **Resource Exhaustion:** Implement timeouts and limits

Use the security-check mode:
```bash
python3 manage-hooks/assets/scripts/hook-tester.py security-check .claude/hooks/hooks.json
```

## Prevention Strategies

### 1. Use the Universal Hook Template

The `universal-hook.py` template includes:
- Proper error handling
- Path validation
- JSON input/output validation
- Logging to stderr

### 2. Test Hooks Before Deployment

```bash
# Always test after creating/updating hooks
python3 manage-hooks/assets/scripts/hook-tester.py test .claude/hooks/hooks.json
```

### 3. Implement Gradual Rollout

Start with observer hooks (PostToolUse) before blocking hooks (PreToolUse).

### 4. Monitor Hook Execution

```bash
# Enable debug mode to see hook execution
claude --debug

# Check logs for hook output
# Hooks log to stderr, check Claude logs
```

### 5. Use Descriptive Error Messages

```python
# Good: Specific error with context
return {
    "status": "block",
    "reason": "security_policy",
    "message": "Blocked access to .env files"
}

# Bad: Generic error
return {"status": "block"}
```

## Troubleshooting Checklist

- [ ] hooks.json is valid JSON (jq validates successfully)
- [ ] All hook scripts exist and are executable
- [ ] Each hook script runs without errors when tested independently
- [ ] Each hook outputs valid JSON to stdout
- [ ] Blocking hooks return approve/block status
- [ ] Observer hooks return success status
- [ ] Stop hooks check stop_hook_active flag
- [ ] Hook timeouts are configured appropriately
- [ ] Matcher patterns match intended tools
- [ ] Event types are spelled correctly
- [ ] No print statements mixed with JSON output
- [ ] Error handling is implemented
- [ ] Path validation is implemented
- [ ] Security patterns are followed

## Getting Help

If you're still experiencing issues:

1. Review the hook types reference: `references/hook-types.md`
2. Check the hooks.json template: `assets/templates/hooks-json.md`
3. Use the universal hook template: `assets/templates/universal-hook.py`
4. Review security patterns: Run security-check mode
5. Enable debug logging: Use `claude --debug`

## Examples

### Example 1: Debugging a Silent Failure

**Problem:** Hook configured but never executes.

**Diagnosis:**
```bash
# Check if script exists and is executable
ls -la .claude/hooks/scripts/my-hook.py
# Result: -rw-r--r-- 1 felix staff 1234 my-hook.py
# Problem found: Not executable!

# Fix:
chmod +x .claude/hooks/scripts/my-hook.py
ls -la .claude/hooks/scripts/my-hook.py
# Result: -rwxr-xr-x 1 felix staff 1234 my-hook.py
```

### Example 2: Debugging JSON Output

**Problem:** "Failed to parse hook output"

**Diagnosis:**
```bash
# Test hook and capture output
echo '{"tool": "Edit", "arguments": {}}' | python3 .claude/hooks/scripts/my-hook.py
# Output:
# Starting hook processing
# {"status": "approve"}
# Problem: Print statement before JSON!

# Fix in hook.py:
# Remove print("Starting hook processing")
# Use logging.info() instead
```

### Example 3: Debugging Timeout

**Problem:** Hook times out on every execution.

**Diagnosis:**
```bash
# Test with timeout
timeout 5s bash -c 'echo '{"tool": "Read", "arguments": {}}' | python3 .claude/hooks/scripts/slow-hook.py'
# Result: timeout command timed out

# Check hook code:
grep -A 10 "requests" .claude/hooks/scripts/slow-hook.py
# Found: requests.get(url)  # No timeout!

# Fix:
requests.get(url, timeout=5)
```

## Best Practices Summary

1. **Always test hooks before deploying**
2. **Use the universal hook template**
3. **Validate inputs and handle errors**
4. **Log to stderr, output JSON to stdout**
5. **Set appropriate timeouts**
6. **Start with observer hooks before blocking hooks**
7. **Use descriptive error messages**
8. **Enable debug mode when troubleshooting**
9. **Keep hooks simple and focused**
10. **Review security patterns regularly**
