# Advanced Hook Use Cases and Techniques

This reference covers sophisticated hook patterns for complex automation workflows, multi-stage validation, and integration with external systems.

## Multi-Stage Validation

### Overview
Combine command hooks (fast) with prompt hooks (intelligent) for optimal performance and security.

### Implementation

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
          "prompt": "Deep analysis of bash command: $TOOL_INPUT.command. Check for: 1) Sophisticated command injection 2) Obfuscated destructive operations 3) Context-dependent dangers 4) Intent vs literal meaning 5) Hidden side effects. Return decision with detailed explanation.",
          "timeout": 20
        }
      ]
    }
  ]
}
```

### quick-check.sh (Ultra-Fast Path)
```bash
#!/bin/bash
set -euo pipefail

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Ultra-fast approval: obviously safe commands
if [[ "$command" =~ ^(ls|pwd|echo|date|whoami|id|hostname|uname|cat|less|more|tail|head|grep|find|which|whereis)$ ]]; then
  exit 0
fi

# Ultra-fast denial: extremely dangerous
if [[ "$command" == *"rm -rf /"* ]] || \
   [[ "$command" == *":(){ :|:& };:"* ]] || \
   [[ "$command" == *"mkfs"* ]] || \
   [[ "$command" == *"dd if=/dev/zero"* ]]; then
  echo '{"continue": true, "systemMessage": "Extremely dangerous operation detected"}' >&2
  exit 2
fi

# Let prompt hook handle everything else
exit 0
```

### Benefits

1. **Instant approval** for safe commands (< 5ms)
2. **Instant denial** for obviously dangerous commands (< 5ms)
3. **Intelligent analysis** for everything else (500-2000ms)
4. **Best of both worlds**: Speed + Intelligence

### Performance Comparison

| Command Type | Command Hook Only | Prompt Hook Only | Hybrid Approach |
|--------------|------------------|------------------|-----------------|
| Safe (ls) | 5ms | 800ms | 5ms ✅ |
| Dangerous (rm -rf) | 5ms | 900ms | 5ms ✅ |
| Unknown | 5ms | 1200ms | 1200ms ✅ |
| Complex | N/A | 2000ms | 2000ms ✅ |

---

## Cross-Event Workflows

### Overview
Coordinate hooks across different events to track state and enforce complex workflows.

### Implementation: Testing Enforcement

**SessionStart - Initialize tracking:**
```bash
#!/bin/bash
# Initialize test tracking
echo "0" > /tmp/test-runs-$$
echo "0" > /tmp/build-runs-$$
echo "[]" > /tmp modified-files-$$
```

**PostToolUse - Track events:**
```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
tool_result=$(echo "$input" | jq -r '.tool_result // empty')

# Track test executions
if [ "$tool_name" = "Bash" ] && [[ "$tool_result" == *"test"* ]]; then
  count=$(cat /tmp/test-runs-$$ 2>/dev/null || echo "0")
  echo $((count + 1)) > /tmp/test-runs-$$
fi

# Track builds
if [ "$tool_name" = "Bash" ] && [[ "$tool_result" == *"build"* ]]; then
  count=$(cat /tmp/build-runs-$$ 2>/dev/null || echo "0")
  echo $((count + 1)) > /tmp/build-runs-$$
fi

# Track file modifications
if [ "$tool_name" = "Write" ] || [ "$tool_name" = "Edit" ]; then
  file_path=$(echo "$input" | jq -r '.tool_input.file_path')
  files=$(cat /tmp/modified-files-$$ 2>/dev/null || echo "[]")
  echo "$files" | jq --arg fp "$file_path" '. + [$fp]' > /tmp/modified-files-$$
fi

exit 0
```

**Stop - Enforce based on tracking:**
```bash
#!/bin/bash
test_count=$(cat /tmp/test-runs-$$ 2>/dev/null || echo "0")
build_count=$(cat /tmp/build-runs-$$ 2>/dev/null || echo "0")
modified_files=$(cat /tmp/modified-files-$$ 2>/dev/null || echo "[]")

# Check if code was modified
code_modified=$(echo "$modified_files" | jq 'length > 0')

if [ "$code_modified" = "true" ]; then
  # Code was modified, enforce testing and building
  if [ "$test_count" -eq "0" ]; then
    echo '{"decision": "block", "reason": "Code was modified but no tests were run. Please run tests before stopping."}' >&2
    exit 2
  fi

  if [ "$build_count" -eq "0" ]; then
    echo '{"decision": "block", "reason": "Code was modified but project was not built. Please run build before stopping."}' >&2
    exit 2
  fi
fi

# Cleanup
rm -f /tmp/test-runs-$$ /tmp/build-runs-$$ /tmp/modified-files-$$

echo '{"decision": "approve"}'
exit 0
```

**Configuration:**
```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/init-tracking.sh"
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/track-events.sh"
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/enforce-quality.sh"
        }
      ]
    }
  ]
}
```

### Use Cases

1. **Testing enforcement**: Track file changes → require tests
2. **Build verification**: Track builds → verify success
3. **Code review**: Track modifications → require review
4. **Deployment gates**: Track changes → require approvals

---

## Context-Aware Prompt Hooks

### Overview
Use transcript and session context for intelligent, informed decisions.

### Implementation

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Review the complete transcript at $TRANSCRIPT_PATH. Analyze: 1) What was the user's original request? 2) What work has been completed? 3) Are there any open questions or TODOs? 4) Were all requirements addressed? 5) Is there evidence of testing and quality checks? 6) Has the user indicated satisfaction? Return 'approve' if task is complete, or 'block' with specific missing items and next steps."
        }
      ]
    }
  ]
}
```

### Advanced Context Patterns

**Pattern 1: Requirement Tracking**
```json
"prompt": "Review transcript. Extract all user requirements from initial prompt. Check each requirement: 1) Was it addressed? 2) Was it completed successfully? 3) Are there any partial implementations? 4) Did user confirm completion? Return 'approve' if all requirements met, or list incomplete requirements."
```

**Pattern 2: Decision Documentation**
```json
"prompt": "Analyze transcript for key decisions made during the session: 1) Technical decisions (architecture, tools, approaches) 2) User preferences expressed 3) Constraints identified 4) Trade-offs discussed. Summarize decisions and verify they were implemented correctly."
```

**Pattern 3: Quality Gate Validation**
```json
"prompt": "Quality gate checklist: 1) Code changes → tests run? 2) Tests → all passing? 3) Build → successful? 4) Documentation → updated? 5) Security → reviewed? 6) Performance → acceptable? Return 'approve' only if all gates passed, or list failed gates."
```

---

## Dynamic Configuration

### Overview
Modify hook behavior based on project configuration, environment, or user preferences.

### Implementation: Config-File Driven Hooks

**Script (configurable-validate.sh):**
```bash
#!/bin/bash
set -euo pipefail

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Load configuration
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/hook-config.json"

if [ ! -f "$CONFIG_FILE" ]; then
  # Use defaults
  STRICT_MODE=false
  MAX_FILE_SIZE=1000000
  ALLOWED_EXTENSIONS="[]"
else
  STRICT_MODE=$(jq -r '.strictMode // false' "$CONFIG_FILE")
  MAX_FILE_SIZE=$(jq -r '.maxFileSize // 1000000' "$CONFIG_FILE")
  ALLOWED_EXTENSIONS=$(jq -r '.allowedExtensions // "[]"' "$CONFIG_FILE")
  FORBIDDEN_PATHS=$(jq -r '.forbiddenPaths // "[]"' "$CONFIG_FILE")
fi

# Apply strict mode checks
if [ "$STRICT_MODE" = "true" ]; then
  # Additional validations in strict mode
  if [[ "$file_path" == *".log"* ]] || [[ "$file_path" == *".tmp"* ]]; then
    echo '{"continue": true, "systemMessage": "Log/temp files not allowed in strict mode"}' >&2
    exit 2
  fi
fi

# Check file size
file_content=$(echo "$input" | jq -r '.tool_input.content // empty')
if [ -n "$file_content" ]; then
  content_size=${#file_content}
  if [ "$content_size" -gt "$MAX_FILE_SIZE" ]; then
    echo "{\"continue\": true, \"systemMessage\": \"File size ($((content_size / 1024))KB) exceeds limit ($((MAX_FILE_SIZE / 1024))KB)\"}" >&2
    exit 2
  fi
fi

# Check allowed extensions
if [ "$ALLOWED_EXTENSIONS" != "[]" ]; then
  extension="${file_path##*.}"
  allowed=$(echo "$ALLOWED_EXTENSIONS" | jq -e ". | index(\"$extension\")" 2>/dev/null)
  if [ $? -ne 0 ]; then
    echo "{\"continue\": true, \"systemMessage\": \"File extension .$extension not allowed\"}" >&2
    exit 2
  fi
fi

# Check forbidden paths
if [ "$FORBIDDEN_PATHS" != "[]" ]; then
  for path in $(echo "$FORBIDDEN_PATHS" | jq -r '.[]'); do
    if [[ "$file_path" == "$path"* ]]; then
      echo "{\"continue\": true, \"systemMessage\": \"Path in forbidden list: $path\"}" >&2
      exit 2
    fi
  done
fi

exit 0
```

**Configuration File (.claude/hook-config.json):**
```json
{
  "strictMode": true,
  "maxFileSize": 500000,
  "allowedExtensions": ["js", "ts", "jsx", "tsx", "py", "md"],
  "forbiddenPaths": ["/tmp", "/var/log"],
  "requireTests": true,
  "enableSecurityScan": true,
  "rateLimit": {
    "maxOperations": 50,
    "timeWindow": 60
  }
}
```

### Environment-Based Configuration

```bash
#!/bin/bash
# Load config from environment or config file

# Priority: Environment variable > Config file > Default
CONFIG_SOURCE="${HOOK_CONFIG_SOURCE:-config-file}"

case "$CONFIG_SOURCE" in
  "environment")
    STRICT_MODE="${HOOK_STRICT_MODE:-false}"
    MAX_FILE_SIZE="${HOOK_MAX_FILE_SIZE:-1000000}"
    ;;
  "config-file")
    CONFIG_FILE="${HOOK_CONFIG_FILE:-$CLAUDE_PROJECT_DIR/.claude/hook-config.json}"
    if [ -f "$CONFIG_FILE" ]; then
      STRICT_MODE=$(jq -r '.strictMode // false' "$CONFIG_FILE")
      MAX_FILE_SIZE=$(jq -r '.maxFileSize // 1000000' "$CONFIG_FILE")
    else
      STRICT_MODE=false
      MAX_FILE_SIZE=1000000
    fi
    ;;
  "default")
    STRICT_MODE=false
    MAX_FILE_SIZE=1000000
    ;;
esac

# Export for use in hook
export STRICT_MODE
export MAX_FILE_SIZE
```

---

## State Sharing Between Hooks

### Overview
Share state across hook executions using temporary files, databases, or external storage.

### Implementation: Shared State File

**Initialization (SessionStart):**
```bash
#!/bin/bash
# Create shared state file
STATE_FILE="/tmp/hook-state-$$"

cat > "$STATE_FILE" <<'EOF'
{
  "session_start": "'$(date -Iseconds)'",
  "test_runs": 0,
  "builds": 0,
  "files_modified": [],
  "decisions": [],
  "warnings": []
}
EOF

chmod 600 "$STATE_FILE"
echo "$STATE_FILE" > /tmp/hook-state-location
```

**Update State (PostToolUse):**
```bash
#!/bin/bash
STATE_FILE=$(cat /tmp/hook-state-location 2>/dev/null || echo "")

if [ -z "$STATE_FILE" ] || [ ! -f "$STATE_FILE" ]; then
  exit 0
fi

input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

# Update based on tool used
case "$tool_name" in
  "Bash")
    command=$(echo "$input" | jq -r '.tool_input.command')
    if [[ "$command" == *"test"* ]]; then
      jq '.test_runs += 1' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    fi
    if [[ "$command" == *"build"* ]]; then
      jq '.builds += 1' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    fi
    ;;
  "Write"|"Edit")
    file_path=$(echo "$input" | jq -r '.tool_input.file_path')
    jq --arg fp "$file_path" '.files_modified += [$fp]' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
    ;;
esac
```

**Read State (Stop):**
```bash
#!/bin/bash
STATE_FILE=$(cat /tmp/hook-state-location 2>/dev/null || echo "")

if [ -z "$STATE_FILE" ] || [ ! -f "$STATE_FILE" ]; then
  exit 0
fi

# Read and analyze state
test_runs=$(jq -r '.test_runs' "$STATE_FILE")
builds=$(jq -r '.builds' "$STATE_FILE")
files_modified=$(jq -r '.files_modified | length' "$STATE_FILE")

if [ "$files_modified" -gt "0" ] && [ "$test_runs" -eq "0" ]; then
  echo '{"decision": "block", "reason": "Files modified but no tests run"}' >&2
  exit 2
fi

# Cleanup
rm -f "$STATE_FILE" /tmp/hook-state-location

echo '{"decision": "approve"}'
exit 0
```

### Redis-Based State Sharing

For distributed or multi-session state:

```bash
#!/bin/bash
# Use Redis for state sharing
REDIS_KEY="claude:hooks:session:$$"

# Store state
redis-cli SET "$REDIS_KEY" "$(cat state.json)" EX 3600

# Retrieve state
STATE=$(redis-cli GET "$REDIS_KEY")
echo "$STATE" | jq .
```

---

## External System Integration

### Overview
Integrate hooks with external systems for logging, monitoring, and notifications.

### Slack Integration

**Notification Hook:**
```bash
#!/bin/bash
set -euo pipefail

input=$(cat)
notification_type=$(echo "$input" | jq -r '.notification_type // "unknown"')
severity=$(echo "$input" | jq -r '.severity // "info"')

# Only send for high-severity notifications
if [ "$severity" != "error" ] && [ "$severity" != "warning" ]; then
  exit 0
fi

# Send to Slack
if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
  message="Claude Notification: $notification_type (Severity: $severity)"

  curl -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d "{\"text\":\"$message\",\"attachments\":[{\"color\":\"$severity\",\"text\":\"$(echo "$input" | jq -c .)\"}]}" \
    2>/dev/null || true
fi

exit 0
```

### Database Logging

**Audit Hook:**
```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
session_id=$(echo "$input" | jq -r '.session_id')
timestamp=$(date -Iseconds)

# Log to database
if [ -n "${AUDIT_DB_URL:-}" ]; then
  psql "$AUDIT_DB_URL" <<EOF 2>/dev/null || true
INSERT INTO hook_audit_log (session_id, tool_name, event_data, timestamp)
VALUES ('$session_id', '$tool_name', '$(echo "$input" | jq -c .)', '$timestamp');
EOF
fi

exit 0
```

### Metrics Collection

**Metrics Hook:**
```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
hook_event=$(echo "$input" | jq -r '.hook_event_name')

# Send metrics to StatsD/Datadog
if [ -n "${STATSD_HOST:-}" ]; then
  echo "claude.hooks.$hook_event.$tool_name:1|c" | nc -u -w1 "${STATSD_HOST}" 8125 2>/dev/null || true
fi

exit 0
```

---

## Advanced Security Patterns

### Secret Detection

**Content Scanning Hook:**
```bash
#!/bin/bash
set -euo pipefail

input=$(cat)
content=$(echo "$input" | jq -r '.tool_input.content // empty')

if [ -z "$content" ]; then
  exit 0
fi

# Check for various secret patterns
patterns=(
  # AWS Access Key
  'AKIA[0-9A-Z]{16}'
  # AWS Secret Access Key
  '[A-Za-z0-9/+=]{40}'
  # GitHub Token
  'ghp_[A-Za-z0-9]{36}'
  # Private Key
  '-----BEGIN.*PRIVATE KEY-----'
  # API Key
  'api[_-]?key["\x20]*[:=]["\x20]*[A-Za-z0-9]{20,}'
  # Password assignment
  'password["\x20]*[:=]["\x20]*["\x27]?[^"'\x27\n]{8,}'
)

for pattern in "${patterns[@]}"; do
  if echo "$content" | grep -Pq "$pattern"; then
    echo '{"continue": true, "systemMessage": "Potential secret detected in content. Use environment variables instead."}' >&2
    exit 2
  fi
done

exit 0
```

### Anomaly Detection

**Behavioral Analysis Hook:**
```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
session_id=$(echo "$input" | jq -r '.session_id')

# Track tool usage patterns
HISTORY_FILE="/tmp/hook-history-$session_id"

# Read history
if [ -f "$HISTORY_FILE" ]; then
  history=$(cat "$HISTORY_FILE")
else
  history="[]"
fi

# Add current tool
echo "$history" | jq --arg tool "$tool_name" '. + [$tool]' > "$HISTORY_FILE.tmp" && \
  mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"

# Analyze patterns
tool_count=$(jq -r '. | group_by(.) | map({tool: .[0], count: length})' "$HISTORY_FILE")

# Detect anomalies (e.g., too many delete operations)
delete_count=$(echo "$tool_count" | jq 'map(select(.tool | contains("delete") or contains("remove"))) | map(.count) | add // 0')

if [ "$delete_count" -gt 5 ]; then
  echo '{"continue": true, "systemMessage": "High number of delete operations detected. Please review your actions."}' >&2
  exit 2
fi

exit 0
```

### Compliance Enforcement

**Compliance Hook:**
```bash
#!/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Check for PII (basic pattern)
if echo "$file_path" | grep -qiE "(pii|personal|ssn|social.*security)"; then
  echo '{"continue": true, "systemMessage": "PII-related file detected. Ensure compliance with data protection regulations."}' >&2
  exit 2
fi

# Check content for PII
content=$(echo "$input" | jq -r '.tool_input.content // empty')
if echo "$content" | grep -Pq '\b\d{3}-\d{2}-\d{4}\b'; then  # SSN pattern
  echo '{"continue": true, "systemMessage": "Potential SSN detected. Ensure data protection compliance."}' >&2
  exit 2
fi

exit 0
```

---

## Performance Optimization

### Caching Strategies

**Result Caching:**
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# Create cache key from file path and size
cache_key=$(echo "$file_path" | md5sum | cut -d' ' -f1)
cache_dir="/tmp/hook-cache"
mkdir -p "$cache_dir"
cache_file="$cache_dir/$cache_key"

# Check cache
if [ -f "$cache_file" ]; then
  cache_age=$(($(date +%s) - $(stat -f%m "$cache_file" 2>/dev/null || stat -c%Y "$cache_file" 2>/dev/null)))

  # Use cache if less than 5 minutes old
  if [ "$cache_age" -lt 300 ]; then
    cat "$cache_file"
    exit 0
  fi
fi

# Perform validation
# ... validation logic ...

# Cache result
echo "$validation_result" > "$cache_file"
echo "$validation_result"
```

**State Caching:**
```bash
#!/bin/bash
# Cache expensive operations

CACHE_TTL=300  # 5 minutes
CACHE_PREFIX="hook-validate"

cache_get() {
  local key="$1"
  local cache_file="/tmp/$CACHE_PREFIX-$key"

  if [ -f "$cache_file" ]; then
    local age=$(($(date +%s) - $(stat -f%m "$cache_file" 2>/dev/null || stat -c%Y "$cache_file" 2>/dev/null)))
    if [ "$age" -lt "$CACHE_TTL" ]; then
      cat "$cache_file"
      return 0
    fi
  fi
  return 1
}

cache_set() {
  local key="$1"
  local value="$2"
  local cache_file="/tmp/$CACHE_PREFIX-$key"

  echo "$value" > "$cache_file"
}
```

### Parallel Processing

**Batch Validation:**
```bash
#!/bin/bash
input=$(cat)

# Extract multiple items to validate
files=$(echo "$input" | jq -r '.tool_input.files[]')

# Validate in parallel (using background jobs)
pids=()
while IFS= read -r file; do
  (
    # Validate single file
    validate_file "$file"
  ) &
  pids+=($!)
done <<< "$files"

# Wait for all validations
for pid in "${pids[@]}"; do
  wait "$pid"
done
```

---

## Testing Advanced Hooks

### Unit Testing Framework

**Test Suite Structure:**
```bash
#!/bin/bash
# run-tests.sh

TESTS_DIR="tests"
PASSED=0
FAILED=0

# Run each test
for test_file in "$TESTS_DIR"/*.sh; do
  if [ -f "$test_file" ]; then
    echo "Running: $(basename "$test_file")"

    if bash "$test_file"; then
      ((PASSED++))
      echo "  ✅ PASSED"
    else
      ((FAILED++))
      echo "  ❌ FAILED"
    fi
  fi
done

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] || exit 1
```

**Test Example:**
```bash
#!/bin/bash
# tests/test-bash-validation-safe.sh

source "$(dirname "$0")/test-helpers.sh"

# Test safe command
input='{"tool_input": {"command": "ls -la"}}'
result=$(echo "$input" | bash "$(dirname "$0")/../examples/validate-bash.sh")

if [ $? -eq 0 ]; then
  pass "Safe command approved"
else
  fail "Safe command rejected"
fi
```

### Integration Testing

**Test Scenario:**
```bash
#!/bin/bash
# integration-tests/full-workflow.sh

# Setup test environment
export CLAUDE_PROJECT_DIR="/tmp/test-project"
export CLAUDE_PLUGIN_ROOT="$(dirname "$0")/.."
mkdir -p "$CLAUDE_PROJECT_DIR"

# Test SessionStart → PostToolUse → Stop workflow

# 1. Test SessionStart
echo '{}' | bash "${CLAUDE_PLUGIN_ROOT}/examples/load-context.sh"
assert_file_exists "/tmp/hook-state-$$" "State file created"

# 2. Test PostToolUse (modify file)
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.js", "content": "console.log(test);"}}' | \
  bash "${CLAUDE_PLUGIN_ROOT}/examples/track-events.sh"
assert_file_exists "/tmp/test-runs-$$" "Test tracking works"

# 3. Test Stop with enforcement
echo '{"reason": "Task complete"}' | bash "${CLAUDE_PLUGIN_ROOT}/examples/enforce-quality.sh"
assert_fail "Should block without tests"

# Cleanup
rm -rf "$CLAUDE_PROJECT_DIR" /tmp/hook-state-$$ /tmp/test-runs-$$

echo "Integration tests passed!"
```

---

## Debugging and Monitoring

### Debug Mode

**Debug Hook:**
```bash
#!/bin/bash
input=$(cat)

# Enable debug if flag is set
if [ "${HOOK_DEBUG:-false}" = "true" ]; then
  echo "=== Hook Debug Info ===" >&2
  echo "Session ID: $(echo "$input" | jq -r '.session_id')" >&2
  echo "Event: $(echo "$input" | jq -r '.hook_event_name')" >&2
  echo "Tool: $(echo "$input" | jq -r '.tool_name')" >&2
  echo "Input: $(echo "$input" | jq -c .)" >&2
  echo "========================" >&2
fi

# ... normal validation logic ...

if [ "${HOOK_DEBUG:-false}" = "true" ]; then
  echo "=== Hook Decision ===" >&2
  echo "Decision: $(jq -r '.decision // "allow"' <<< "$output")" >&2
  echo "Reason: $(jq -r '.reason // "N/A"' <<< "$output")" >&2
  echo "=====================" >&2
fi
```

### Logging Hook Decisions

**Decision Logger:**
```bash
#!/bin/bash
input=$(cat)
output=$(cat)  # Hook's output

# Parse decision
decision=$(echo "$output" | jq -r '.decision // .permissionDecision // "allow"')
tool_name=$(echo "$input" | jq -r '.tool_name // "unknown"')
session_id=$(echo "$input" | jq -r '.session_id // "unknown"')

# Log to file
log_entry=$(jq -n \
  --ts "$(date -Iseconds)" \
  --sid "$session_id" \
  --tool "$tool_name" \
  --decision "$decision" \
  '{
    timestamp: $ts,
    session_id: $sid,
    tool: $tool,
    decision: $decision
  }')

echo "$log_entry" >> ~/.claude/hook-decisions.log

exit 0
```

### Performance Monitoring

**Performance Hook:**
```bash
#!/bin/bash
input=$(cat)

start_time=$(date +%s%N)

# ... hook logic ...

end_time=$(date +%s%N)
duration=$(( (end_time - start_time) / 1000000 ))  # Convert to milliseconds

# Log performance
echo "$(date -Iseconds),hook,$duration,ms" >> ~/.claude/hook-performance.log

exit 0
```

---

## Best Practices

### Security

1. **Never log secrets**
   - Sanitize inputs
   - Remove sensitive data from logs
   - Use pattern matching carefully

2. **Validate all inputs**
   - Check data types
   - Sanitize strings
   - Handle edge cases

3. **Use least privilege**
   - Limit file system access
   - Restrict network access
   - Run with minimal permissions

### Performance

1. **Cache expensive operations**
   - File scanning results
   - External API calls
   - Complex validations

2. **Set appropriate timeouts**
   - Quick checks: 5-10s
   - Standard validation: 15-30s
   - Complex analysis: 30-60s
   - Never exceed 60s

3. **Minimize I/O**
   - Read files once
   - Batch operations
   - Use memory for small data

### Maintainability

1. **Document complex logic**
   - Explain validation criteria
   - Provide examples
   - Document configuration

2. **Version your hooks**
   - Track changes
   - Support rollback
   - Test upgrades

3. **Monitor hook behavior**
   - Track decisions
   - Identify false positives
   - Gather user feedback

### Reliability

1. **Handle errors gracefully**
   - Provide clear messages
   - Don't crash on unexpected input
   - Fail safely

2. **Test thoroughly**
   - Unit tests for scripts
   - Integration tests for workflows
   - User acceptance testing

3. **Provide escape hatches**
   - Allow bypassing hooks
   - Support emergency overrides
   - Document workarounds

---

## Conclusion

Advanced hook patterns enable sophisticated automation while maintaining security and performance. Use these techniques to:

- **Layer security**: Combine multiple validation approaches
- **Share state**: Track workflows across events
- **Integrate systems**: Connect with external tools
- **Optimize performance**: Cache and parallelize
- **Monitor behavior**: Track decisions and performance

Remember: With great power comes great responsibility. Always test thoroughly and prioritize user experience over strict enforcement.