# Common Hook Patterns

This reference provides proven patterns for implementing Claude Code hooks. Each pattern includes configuration, explanation, and use cases.

## Pattern 1: Security Validation (Prompt-Based)

### Overview
Use prompt-based hooks for intelligent, context-aware security validation that adapts to new scenarios without code changes.

### Configuration
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze file_path and content. Check: 1) Not in system directories (/etc, /sys, /boot, /usr) 2) Not credential files (.env, secrets, keys, passwords) 3) No path traversal (../) 4) Content doesn't expose secrets (API keys, private keys, database URLs with credentials). Return decision with explanation."
        }
      ]
    },
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze bash command. Check for: 1) Destructive operations (rm -rf, dd, mkfs, fdisk) 2) Privilege escalation (sudo, su) 3) Network operations without consent 4) System modifications 5) Package manager operations (install, remove). Return decision with explanation."
        }
      ]
    }
  ]
}
```

### Why Prompt-Based?
- **Adaptive**: Understands new security patterns without code changes
- **Context-aware**: Considers file content, not just file paths
- **Natural language**: Easy to modify criteria
- **Comprehensive**: Single hook catches many issue types

### Use Cases
- Security-focused plugins
- Team environments with varying security needs
- Projects with evolving security requirements
- When you want to add criteria without code changes

### Example Scenarios
### Prompt hook catches:**
- Writing database credentials in file content
- Bash commands with hidden destructive operations
- Path traversal attempts through content injection
- New security patterns you haven't coded yet

### Command hook would miss:**
- Content-based secret detection
- Context-aware path validation
- Novel attack patterns
- Intent-based security decisions

---

## Pattern 2: Quality Enforcement (Stop Hook)

### Overview
Ensure work meets quality standards before allowing agent to stop.

### Configuration
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Review transcript at $TRANSCRIPT_PATH. Verify: 1) If code was modified (Write/Edit tools used), were tests executed? 2) Did builds succeed (npm run build, cargo build, etc)? 3) Were all user questions answered? 4) Is documentation updated? 5) Are there any TODO comments or incomplete work? Return 'approve' only if all checks pass, or 'block' with specific reasons."
        }
      ]
    }
  ]
}
```

### How It Works
1. User or agent wants to stop
2. Hook reads full transcript
3. LLM analyzes if work is complete
4. Returns decision with detailed feedback
5. If incomplete, provides specific reasons

### Benefits
- Prevents incomplete work
- Enforces quality gates
- Provides actionable feedback
- Adapts to different project types

### Customization
Modify the prompt for your quality criteria:
```json
"prompt": "Review transcript. If code changed: 1) Run linting 2) Run tests 3) Update docs 4) Create PR. If docs changed: 1) Verify links work 2) Check spelling. Return 'approve' or 'block' with reasons."
```

---

## Pattern 3: Context Loading (SessionStart)

### Overview
Detect project type and load relevant context automatically at session start.

### Configuration
```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/load-context.sh"
        }
      ]
    }
  ]
}
```

### Implementation (load-context.sh)
```bash
#!/bin/bash
cd "$CLAUDE_PROJECT_DIR" || exit 1

# Detect Node.js
if [ -f "package.json" ]; then
  echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"

  if [ -f "tsconfig.json" ]; then
    echo "export USES_TYPESCRIPT=true" >> "$CLAUDE_ENV_FILE"
  fi

  # Detect framework
  if grep -q "react" package.json 2>/dev/null; then
    echo "export FRAMEWORK=react" >> "$CLAUDE_ENV_FILE"
  fi
fi

# Detect Python
if [ -f "pyproject.toml" ]; then
  echo "export PROJECT_TYPE=python" >> "$CLAUDE_ENV_FILE"
fi
```

### Environment Variables Set
- `PROJECT_TYPE` - nodejs, python, rust, go, java, etc.
- `FRAMEWORK` - react, vue, angular, django, etc.
- `TEST_FRAMEWORK` - jest, pytest, cargo test, etc.
- `BUILD_SYSTEM` - maven, gradle, webpack, etc.

### Use Cases
- Automatically configure language-specific tools
- Load testing commands
- Set up build processes
- Detect CI/CD systems

---

## Pattern 4: MCP Tool Protection

### Overview
Add safety checks for destructive MCP operations.

### Configuration
```json
{
  "PreToolUse": [
    {
      "matcher": "mcp__.*__delete.*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Destructive MCP operation detected. Analyze: 1) Is deletion intentional and reversible? 2) Are there backups? 3) Does user have permission? 4) Is operation scope appropriate? Return 'allow' only if safe, or 'deny' with specific concerns."
        }
      ]
    },
    {
      "matcher": "mcp__.*__execute.*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "SQL execution detected. Check: 1) Operation type (SELECT/INSERT/UPDATE/DELETE) 2) Is it safe (no DROP, TRUNCATE)? 3) Are there WHERE clauses to limit scope? 4) Is user authorized? Return decision with explanation."
        }
      ]
    }
  ]
}
```

### Matcher Patterns
- `mcp__.*__delete.*` - All delete operations
- `mcp__.*__drop.*` - Drop table/database operations
- `mcp__.*__execute.*` - SQL execution
- `mcp__plugin_name_.*` - Specific plugin's tools

### Use Cases
- Database safety (prevent accidental drops)
- File system protection
- API operations that modify data
- Cost control (expensive operations)

---

## Pattern 5: Notification Logging

### Overview
Log all notifications for audit trail and analysis.

### Configuration
```json
{
  "Notification": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/log-notification.sh"
        }
      ]
    }
  ]
}
```

### Implementation (log-notification.sh)
```bash
#!/bin/bash
input=$(cat)
timestamp=$(date -Iseconds)

# Parse notification type
notification_type=$(echo "$input" | jq -r '.notification_type // "unknown"')

# Append to audit log
{
  echo "$timestamp | $notification_type | $USER | Session: $SESSION_ID"
  echo "$input" | jq .
  echo "---"
} >> ~/.claude/notification-audit.log

# Optionally send to external system
if [ -n "${SLACK_WEBHOOK:-}" ]; then
  curl -X POST "$SLACK_WEBHOOK" \
    -H 'Content-Type: application/json' \
    -d "{\"text\": \"Claude notification: $notification_type\"}" \
    2>/dev/null || true
fi

exit 0
```

### Use Cases
- Audit compliance
- Security monitoring
- Performance analysis
- User behavior tracking
- Integration with external monitoring (Slack, email, etc.)

---

## Pattern 6: Build Verification

### Overview
Ensure projects build successfully after code changes.

### Configuration
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Check if code was modified (Write/Edit tools used). If yes: 1) Was the project built (npm run build, cargo build, mvn compile, etc)? 2) Did build succeed? 3) Are there build errors? If no build was run, block and request build. Return 'approve' only if build succeeded or no code was changed."
        }
      ]
    }
  ]
}
```

### Detection Logic
The prompt-based hook can:
- Parse transcript for build commands
- Check for build success indicators
- Detect error messages
- Identify build tools used

### Benefits
- Prevents broken code commits
- Enforces build discipline
- Catches compilation errors early
- Works across different build systems

---

## Pattern 7: Permission Confirmation

### Overview
Ask user to confirm potentially dangerous operations.

### Configuration
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze command. If it contains destructive keywords (rm, delete, drop, truncate, alter) OR system operations (chmod, chown, install, remove) OR privilege escalation (sudo, su), return 'ask' to request user confirmation. Otherwise return 'allow'."
        }
      ]
    }
  ]
}
```

### How It Works
1. Hook detects potentially dangerous operation
2. Returns `permissionDecision: "ask"`
3. Claude Code prompts user for confirmation
4. User can approve or deny
5. Operation proceeds or blocks

### User Experience
```
Claude: I'm about to run: rm -rf node_modules/
This will delete the node_modules directory. Should I proceed?
[Yes] [No]
```

### Use Cases
- Destructive file operations
- System modifications
- Package installations
- Database changes
- Production deployments

---

## Pattern 8: Code Quality Checks

### Overview
Run linters and formatters on code edits automatically.

### Configuration
```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-quality.sh"
        }
      ]
    }
  ]
}
```

### Implementation (check-quality.sh)
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# Determine file type and run appropriate linter
case "$file_path" in
  *.js|*.ts|*.jsx|*.tsx)
    if command -v eslint &>/dev/null; then
      echo "Running ESLint on $file_path"
      npx eslint "$file_path" 2>&1 || true
    fi
    if command -v prettier &>/dev/null; then
      echo "Checking Prettier format"
      npx prettier --check "$file_path" 2>&1 || true
    fi
    ;;
  *.py)
    if command -v flake8 &>/dev/null; then
      echo "Running flake8 on $file_path"
      flake8 "$file_path" 2>&1 || true
    fi
    if command -v black &>/dev/null; then
      echo "Checking black format"
      black --check "$file_path" 2>&1 || true
    fi
    ;;
  *.rs)
    if command -v rustfmt &>/dev/null; then
      echo "Running rustfmt on $file_path"
      rustfmt --check "$file_path" 2>&1 || true
    fi
    ;;
esac

exit 0
```

### Benefits
- Immediate feedback on code quality
- Consistent code formatting
- Early error detection
- Works across different languages

---

## Pattern 9: Test Enforcement

### Overview
Ensure tests run after code changes.

### Configuration
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Review transcript. If code was modified (Write/Edit tools used), verify: 1) Were tests executed? 2) Did all tests pass? 3) Is test coverage adequate? If tests weren't run, block and request test execution. Return 'approve' only if tests passed or no code changed."
        }
      ]
    }
  ]
}
```

### Detection
The prompt analyzes transcript for:
- Test commands (npm test, cargo test, pytest, etc.)
- Test results (passed/failed)
- Coverage reports
- Test file modifications

### Benefits
- Prevents code without tests
- Enforces quality standards
- Reduces bugs in production
- Works with any testing framework

---

## Pattern 10: Configuration-Driven Hooks

### Overview
Make hook behavior configurable via JSON files.

### Configuration
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/configurable-validate.sh"
        }
      ]
    }
  ]
}
```

### Implementation (configurable-validate.sh)
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# Read configuration
CONFIG_FILE="$CLAUDE_PROJECT_DIR/.claude/security-policy.json"

if [ -f "$CONFIG_FILE" ]; then
  # Load configuration
  allowed_paths=$(jq -r '.allowedPaths[]?' "$CONFIG_FILE")
  forbidden_paths=$(jq -r '.forbiddenPaths[]?' "$CONFIG_FILE")
  max_file_size=$(jq -r '.maxFileSize // 1000000' "$CONFIG_FILE")
  strict_mode=$(jq -r '.strictMode // false' "$CONFIG_FILE")

  # Check allowed paths
  if [ -n "$allowed_paths" ]; then
    path_allowed=false
    while IFS= read -r path; do
      if [[ "$file_path" == "$path"* ]]; then
        path_allowed=true
        break
      fi
    done <<< "$allowed_paths"

    if [ "$path_allowed" = false ]; then
      echo "{\"continue\": true, \"systemMessage\": \"Path not in allowed list: $file_path\"}" >&2
      exit 2
    fi
  fi

  # Check forbidden paths
  if [ -n "$forbidden_paths" ]; then
    while IFS= read -r path; do
      if [[ "$file_path" == "$path"* ]]; then
        echo "{\"continue\": true, \"systemMessage\": \"Path in forbidden list: $file_path\"}" >&2
        exit 2
      fi
    done <<< "$forbidden_paths"
  fi
fi

exit 0
```

### Configuration File (.claude/security-policy.json)
```json
{
  "strictMode": true,
  "allowedPaths": ["/tmp", "/home/user/projects"],
  "forbiddenPaths": ["/etc", "/sys"],
  "maxFileSize": 500000,
  "requireTests": true,
  "blockDeleteOperations": true
}
```

### Use Cases
- Team-specific policies
- Project-specific settings
- Environment-based configuration
- Gradual security rollout

---

## Pattern 11: Temporary Hook Activation

### Overview
Enable hooks conditionally via flag files.

### Configuration
```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/conditional-validate.sh"
        }
      ]
    }
  ]
}
```

### Implementation (conditional-validate.sh)
```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path')

# Check for flag files
STRICT_MODE_FILE="$CLAUDE_PROJECT_DIR/.enable-strict-validation"
SECURITY_SCAN_FILE="$CLAUDE_PROJECT_DIR/.enable-security-scan"
DEBUG_MODE_FILE="$CLAUDE_PROJECT_DIR/.enable-debug-hooks"

# Skip if no flags set
if [ ! -f "$STRICT_MODE_FILE" ] && [ ! -f "$SECURITY_SCAN_FILE" ]; then
  exit 0
fi

# Run strict validation if enabled
if [ -f "$STRICT_MODE_FILE" ]; then
  # Strict mode: more checks
  if [[ "$file_path" == *".env"* ]]; then
    echo "{\"continue\": true, \"systemMessage\": \"Environment file in strict mode requires review\"}" >&2
    exit 2
  fi

  if [ -f "$DEBUG_MODE_FILE" ]; then
    echo "Debug: Validating $file_path in strict mode" >&2
  fi
fi

# Run security scan if enabled
if [ -f "$SECURITY_SCAN_FILE" ]; then
  # Security scan: check for secrets
  file_content=$(echo "$input" | jq -r '.tool_input.content // empty')

  if echo "$file_content" | grep -qiE "(password|secret|key).{0,20}['\"]?[A-Za-z0-9]{20,}"; then
    echo "{\"continue\": true, \"systemMessage\": \"Potential secret detected in file content\"}" >&2
    exit 2
  fi
fi

exit 0
```

### Activation Commands
```bash
# Enable strict mode
touch .enable-strict-validation

# Enable security scanning
touch .enable-security-scan

# Enable debug logging
touch .enable-debug-hooks

# Disable all
rm -f .enable-*
```

### Benefits
- Temporary validation for sensitive operations
- Development vs production settings
- Feature flags for hook behavior
- Performance optimization (disable heavy hooks)

### Note
Flag file changes require Claude Code restart to take effect.

---

## Pattern 12: Hybrid Validation (Command + Prompt)

### Overview
Combine fast command checks with intelligent prompt analysis.

### Configuration
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
          "prompt": "Analyze bash command: $TOOL_INPUT.command. Check for: 1) Hidden destructive operations 2) Command substitution with user input 3) Complex logic that needs review 4) Intent vs literal meaning. Return decision with explanation.",
          "timeout": 15
        }
      ]
    }
  ]
}
```

### Implementation (quick-check.sh)
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Fast path: immediately approve obviously safe commands
if [[ "$command" =~ ^(ls|pwd|echo|date|whoami|cat)$ ]]; then
  exit 0
fi

# Fast path: immediately block extremely dangerous commands
if [[ "$command" == *"rm -rf /"* ]] || [[ "$command" == *":(){ :|:& };:"* ]]; then
  echo '{"continue": true, "systemMessage": "Dangerous operation detected"}' >&2
  exit 2
fi

# Let prompt hook handle everything else
exit 0
```

### Benefits
- **Fast**: Command hook handles obvious cases instantly
- **Smart**: Prompt hook analyzes complex scenarios
- **Parallel**: Both hooks run simultaneously
- **Resilient**: Command hook provides basic safety net

### Performance
- Obvious safe commands: < 10ms
- Obvious dangerous commands: < 10ms
- Complex commands: Command + Prompt (parallel, ~15s total)

---

## Pattern 13: Rate Limiting

### Overview
Prevent abuse by limiting operations per time window.

### Configuration
```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/rate-limit.sh"
        }
      ]
    }
  ]
}
```

### Implementation (rate-limit.sh)
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')
session_id=$(echo "$input" | jq -r '.session_id // "default"')

# Rate limit configuration
RATE_LIMIT_DIR="/tmp/claude-rate-limits"
mkdir -p "$RATE_LIMIT_DIR"

rate_file="$RATE_LIMIT_DIR/$session_id"
current_minute=$(date +%Y%m%d%H%M)

# Read or initialize rate limit
if [ -f "$rate_file" ]; then
  last_minute=$(head -1 "$rate_file" 2>/dev/null || echo "")
  count=$(tail -1 "$rate_file" 2>/dev/null || echo "0")

  if [ "$current_minute" = "$last_minute" ]; then
    # Same minute, check limit
    limit=50  # 50 operations per minute

    if [ "$count" -gt "$limit" ]; then
      echo '{"continue": true, "systemMessage": "Rate limit exceeded. Please wait before continuing."}' >&2
      exit 2
    fi

    count=$((count + 1))
  else
    # New minute, reset counter
    count=1
  fi
else
  # New session
  count=1
fi

# Write updated count
{
  echo "$current_minute"
  echo "$count"
} > "$rate_file"

exit 0
```

### Configuration Options
- Per-user rate limits
- Per-operation-type limits
- Different limits for different tools
- Sliding window vs fixed window
- Whitelisted operations

### Use Cases
- Prevent resource abuse
- Cost control for paid APIs
- Security (prevent DoS)
- Team usage policies

---

## Pattern 14: Context Injection (PreCompact)

### Overview
Add critical context before compaction to preserve important information.

### Configuration
```json
{
  "PreCompact": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Summarize key context from transcript at $TRANSCRIPT_PATH. Preserve: 1) Current task status 2) Important decisions made 3) Open questions 4) Next steps 5) Relevant file paths. Return concise summary for preservation."
        }
      ]
    }
  ]
}
```

### What Gets Preserved
- Task progress
- User requirements
- Important context
- Decisions made
- Open issues

### Benefits
- Prevents context loss during compaction
- Maintains session continuity
- Preserves important decisions
- Keeps track of progress

---

## Pattern 15: User Prompt Validation

### Overview
Analyze user prompts for security issues or provide guidance.

### Configuration
```json
{
  "UserPromptSubmit": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Analyze user prompt: $USER_PROMPT. If discussing: 1) API keys or credentials - provide security guidance 2) Production deployments - suggest caution 3) Database operations - recommend backups 4) Deletions - recommend verification. Provide helpful guidance."
        }
      ]
    }
  ]
}
```

### How It Works
1. User types prompt
2. Hook analyzes content
3. Provides relevant guidance
4. Guidance shown before processing

### Example Output
```
Security Guidance: I notice you're working with API keys. Remember to:
- Use environment variables, not hardcoded values
- Rotate keys regularly
- Never commit keys to version control
- Use least-privilege access
```

### Use Cases
- Security education
- Best practice reminders
- Risk awareness
- Policy enforcement

---

## Choosing the Right Pattern

### Decision Matrix

| Use Case | Best Pattern | Why |
|----------|--------------|-----|
| Security validation | Pattern 1: Security Validation | Prompt hooks adapt to new threats |
| Quality gates | Pattern 2: Quality Enforcement | Stop hook prevents incomplete work |
| Project setup | Pattern 3: Context Loading | Automatic detection |
| Data protection | Pattern 4: MCP Protection | Prevents destructive operations |
| Audit trail | Pattern 5: Notification Logging | Compliance and monitoring |
| Build checking | Pattern 6: Build Verification | Prevents broken code |
| User confirmation | Pattern 7: Permission Confirmation | Interactive safety |
| Code quality | Pattern 8: Code Quality Checks | Automatic linting |
| Testing | Pattern 9: Test Enforcement | Ensures test coverage |
| Configurable | Pattern 10: Configuration-Driven | Flexible policies |
| Temporary checks | Pattern 11: Temporary Activation | On-demand validation |
| Speed + intelligence | Pattern 12: Hybrid Validation | Best of both worlds |
| Abuse prevention | Pattern 13: Rate Limiting | Resource protection |
| Context preservation | Pattern 14: Context Injection | Maintains continuity |
| User guidance | Pattern 15: User Prompt Validation | Proactive assistance |

### Pattern Combinations

Common combinations:

**Security-Focused Plugin:**
- Pattern 1: Security Validation
- Pattern 4: MCP Protection
- Pattern 7: Permission Confirmation
- Pattern 13: Rate Limiting

**Quality-Focused Plugin:**
- Pattern 2: Quality Enforcement
- Pattern 6: Build Verification
- Pattern 8: Code Quality Checks
- Pattern 9: Test Enforcement

**Developer Experience Plugin:**
- Pattern 3: Context Loading
- Pattern 5: Notification Logging
- Pattern 10: Configuration-Driven
- Pattern 15: User Prompt Validation

---

## Best Practices Summary

### For All Patterns

### DO:**
- Use prompt hooks for complex logic
- Use command hooks for fast checks
- Combine patterns for layered validation
- Test hooks before deployment
- Document hook behavior
- Provide clear error messages
- Use appropriate timeouts
- Validate all inputs

### DON'T:**
- Create hooks that block everything
- Skip error handling
- Log sensitive information
- Create slow hooks
- Ignore user feedback
- Rely on hook execution order
- Use hardcoded paths

### Testing Hooks

Always test hooks:

1. **Unit test scripts**
   ```bash
   ./scripts/test-hook.sh scripts/validate-write.sh test-input.json
   ```

2. **Validate configuration**
   ```bash
   ./scripts/validate-hook-schema.sh hooks/hooks.json
   ```

3. **Lint scripts**
   ```bash
   ./scripts/hook-linter.sh scripts/*.sh
   ```

4. **Test in Claude Code**
   ```bash
   claude --debug
   ```

### Documentation

Document your patterns:
- Explain what each hook does
- Provide configuration examples
- Document configuration options
- List dependencies
- Include troubleshooting guide

---

## Conclusion

These patterns provide a solid foundation for hook development. Choose patterns based on your needs, combine them for layered protection, and always test thoroughly. Remember: hooks are powerful tools that should enhance user experience, not obstruct it.