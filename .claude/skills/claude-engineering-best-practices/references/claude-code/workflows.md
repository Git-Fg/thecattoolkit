# Common Workflows — Stable Patterns

Common development workflows and testing strategies for Claude Code.

## Development Workflows

### Workflow 1: Local Development
```bash
# 1. Start with minimal permissions
# settings.json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep"],
    "permissionMode": "plan"
  }
}

# 2. Gradually expand as needed
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Write"],
    "permissionMode": "acceptEdits"
  }
}

# 3. Enable sandbox
{
  "sandbox": {
    "mode": "auto-allow",
    "network": {
      "allowedDomains": ["github.com"]
    }
  }
}
```

### Workflow 2: Team Collaboration
```bash
# Project settings (.claude/settings.json)
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "./.claude/hooks/format.sh"}
        ]
      }
    ]
  },
  "outputStyles": [".claude/styles/"]
}
```

### Workflow 3: CI/CD Integration
```bash
# .claude/settings.json for CI
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Bash"],
    "permissionMode": "default"
  },
  "sandbox": {
    "allowUnsandboxedCommands": false,
    "excludedCommands": ["docker"]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "./.claude/hooks/ci-validate.sh"}
        ]
      }
    ]
  }
}
```

## Testing Strategies

### Strategy 1: Hook-Based Validation
```bash
# Create validation script
# .claude/hooks/test-validate.sh
#!/bin/bash
read input

# Extract test command
command=$(echo "$input" | jq -r '.tool_input.command')

# Validate test patterns
if [[ "$command" =~ (\-\-test|\.test\.|\.spec\.) ]]; then
  echo "Test command validated"
  exit 0
else
  echo "Not a test command"
  exit 2
fi
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "./.claude/hooks/test-validate.sh"}
        ]
      }
    ]
  }
}
```

### Strategy 2: Code Review Hooks
```bash
# Post-write validation
# .claude/hooks/review-changes.sh
#!/bin/bash
read input

file_path=$(echo "$input" | jq -r '.tool_input.file_path')
echo "Reviewing changes to: $file_path"

# Run linting
if command -v eslint &> /dev/null; then
  eslint "$file_path" || exit 2
fi

# Check for console.log
if grep -q "console\.log" "$file_path"; then
  echo "WARNING: console.log found in $file_path"
fi

exit 0
```

### Strategy 3: Security Scanning
```bash
# Security validation hook
# .claude/hooks/security-scan.sh
#!/bin/bash
read input

tool_input=$(echo "$input" | jq -r '.tool_input')
command=$(echo "$tool_input" | jq -r '.command // ""')
file_path=$(echo "$tool_input" | jq -r '.file_path // ""')

# Block dangerous commands
if [[ "$command" =~ (curl.*\|\|.*sh|wget.*\|\|.*sh) ]]; then
  echo "Dangerous pipe-to-shell pattern detected"
  exit 2
fi

# Check for secrets in files
if [[ -n "$file_path" && "$file_path" =~ \.(js|ts|py|go|java)$ ]]; then
  if grep -i -E "(password|secret|key|token).*=" "$file_path" 2>/dev/null; then
    echo "WARNING: Potential secrets in $file_path"
  fi
fi

exit 0
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write",
        "hooks": [
          {"type": "command", "command": "./.claude/hooks/security-scan.sh"}
        ]
      }
    ]
  }
}
```

## Debugging Workflows

### Workflow 1: Enable Debug Mode
```bash
# Always start with debug
claude --debug

# Review debug output
# Shows:
# - Hook execution
# - Plugin loading
# - Permission checks
# - Tool calls
```

### Workflow 2: Hook Debugging
```bash
# Test hook in isolation
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | bash .claude/hooks/test.sh

# Check exit code
echo $?

# Review hook logs
cat ~/.claude/logs/hooks.log
```

### Workflow 3: Plugin Debugging
```bash
# Validate plugin manifest
claude plugin validate

# Check plugin loading
claude --debug | grep -i plugin

# Review plugin logs
cat ~/.claude/logs/plugins.log
```

## CI/CD Integration

### GitHub Actions Pattern
```yaml
name: Claude Code CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Claude Code
        run: curl -fsSL https://claude.ai/install.sh | bash

      - name: Run tests with Claude
        run: |
          claude --debug << 'EOF'
          /test-runner
          EOF

      - name: Upload logs
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: claude-logs
          path: ~/.claude/logs/
```

### GitLab CI Pattern
```yaml
stages:
  - test

claude_test:
  stage: test
  image: ubuntu:latest
  before_script:
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - claude --debug /run-tests
  artifacts:
    paths:
      - ~/.claude/logs/
    when: always
```

## Common Tasks

### Task 1: Project Setup
```bash
# 1. Initialize project settings
mkdir -p .claude
cat > .claude/settings.json << 'EOF'
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
  }
}
EOF

# 2. Create hooks directory
mkdir -p .claude/hooks

# 3. Create output styles
mkdir -p .claude/styles

# 4. Test configuration
claude --debug
```

### Task 2: Add Security Hooks
```bash
# Create security validation
cat > .claude/hooks/security.sh << 'EOF'
#!/bin/bash
read input
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# Block dangerous patterns
if [[ "$command" =~ (rm\s+-rf|sudo.*|\>\s*/etc/) ]]; then
  echo "Dangerous command blocked"
  exit 2
fi

exit 0
EOF

chmod +x .claude/hooks/security.sh

# Configure hook
cat >> .claude/settings.json << 'EOF'
,
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "./.claude/hooks/security.sh"}
        ]
      }
    ]
  }
}
EOF
```

### Task 3: Enable Sandboxing
```bash
# Add sandbox configuration
jq '. + {
  "sandbox": {
    "mode": "auto-allow",
    "filesystem": {
      "allowedPaths": ["./"],
      "deniedPaths": ["~/.ssh", "~/.aws"]
    },
    "network": {
      "allowedDomains": ["github.com", "registry.npmjs.org"]
    }
  }
}' .claude/settings.json > .claude/settings.tmp && mv .claude/settings.tmp .claude/settings.json
```

## Best Practices

### 1. Start Minimal
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep"]
  }
}
```
Expand permissions as needed.

### 2. Add Hooks Incrementally
```bash
# First: Log all tool usage
# Second: Add validation
# Third: Add blocking
```

### 3. Document Configuration
```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Edit"],
    "comments": {
      "allowedTools": "Read-only analysis + safe editing"
    }
  }
}
```

### 4. Test in Isolation
```bash
# Test hooks before enabling
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | bash hook.sh

# Verify exit codes
# 0 = success/allow
# 2 = block
# other = non-blocking error
```

### 5. Monitor Usage
```bash
# Enable logging
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {"type": "command", "command": "./.claude/hooks/log.sh"}
        ]
      }
    ]
  }
}
```

## Troubleshooting

### Issue: Hooks Not Firing
```bash
# Check configuration
cat .claude/settings.json | jq .

# Verify script is executable
ls -la .claude/hooks/

# Test script manually
bash .claude/hooks/test.sh

# Check debug output
claude --debug | grep -i hook
```

### Issue: Permissions Denied
```bash
# Check current mode
rg "permissionMode" .claude/settings.json

# Review allowed tools
rg "allowedTools" .claude/settings.json

# Temporarily use bypassPermissions for testing
jq '.permissions.permissionMode = "bypassPermissions"' .claude/settings.json
```

### Issue: Sandbox Blocking
```bash
# Check sandbox mode
rg "mode" .claude/settings.json

# Review allowed paths/domains
rg "allowed" .claude/settings.json

# Temporarily disable for testing
jq '.sandbox.allowUnsandboxedCommands = true' .claude/settings.json
```

## Integration Examples

### Example 1: Python Project
```bash
.claude/
├── settings.json
│   ├── permissions: Read, Glob, Grep, Edit, Write, Bash
│   ├── hooks: Python lint/format
│   └── sandbox: Python packages allowed
└── hooks/
    ├── format.sh
    └── lint.sh
```

### Example 2: TypeScript Project
```bash
.claude/
├── settings.json
│   ├── permissions: All tools
│   ├── hooks: ESLint, Prettier
│   └── sandbox: npm registry allowed
└── hooks/
    ├── format.sh
    ├── lint.sh
    └── typecheck.sh
```

### Example 3: Documentation Project
```bash
.claude/
├── settings.json
│   ├── permissions: Read-only
│   ├── hooks: Markdown linting
│   └── sandbox: No network needed
└── hooks/
    └── markdown-lint.sh
```

## Maintenance

### Regular Tasks
1. Review hook logs monthly
2. Update sandbox allowed domains
3. Audit permission scopes
4. Test CI/CD integration

### When to Review
- After security incidents
- When adding new tools
- When changing workflows
- During security audits

### Version Control
```bash
# Track settings
git add .claude/settings.json
git commit -m "Add Claude Code configuration"

# Ignore local overrides
echo ".claude/settings.local.json" >> .gitignore
```

---

## Official Documentation Links

- **Settings & Configuration**: https://code.claude.com/docs/en/settings.md
- **Hooks Reference**: https://code.claude.com/docs/en/hooks.md
- **Sandboxing**: https://code.claude.com/docs/en/sandboxing.md
- **CLI Reference**: https://code.claude.com/docs/en/cli-reference
- **Claude Code Overview**: https://code.claude.com/docs/en/overview

### Verification
Last verified: 2026-01-13
