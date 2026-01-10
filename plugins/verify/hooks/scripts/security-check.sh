#!/bin/bash

# Pre-commit security check hook
# Warns about edits that might contain secrets or security issues.

# Read JSON input
input=$(jq -c '.')
tool_input=$(echo "$input" | jq -c '.tool_input // {}')
file_path=$(echo "$tool_input" | jq -r '.file_path // empty')
content=$(echo "$tool_input" | jq -r '.content // .new_string // empty')

# Exit if missing data
if [ -z "$file_path" ] || [ "$file_path" = "null" ] || [ -z "$content" ] || [ "$content" = "null" ]; then
    exit 0
fi

# Skip certain files
if [[ "$file_path" =~ \.env\.example$|\.env\.template$|\.env\.sample$|package-lock\.json$|yarn\.lock$|pnpm-lock\.yaml$|test|spec ]]; then
    exit 0
fi

# Define secret patterns (simplified for shell)
# Note: Complex regex in shell is tricky, using grep for basic detection
ISSUES=""

if echo "$content" | grep -i -q "api[_-]\?key.*="; then ISSUES="${ISSUES}  - Potential API key detected\n"; fi
if echo "$content" | grep -i -q "secret.*="; then ISSUES="${ISSUES}  - Potential Secret detected\n"; fi
if echo "$content" | grep -i -q "bearer [a-zA-Z0-9_-]\{20,\}"; then ISSUES="${ISSUES}  - Bearer token detected\n"; fi
if echo "$content" | grep -q "ghp_[a-zA-Z0-9]\{36\}"; then ISSUES="${ISSUES}  - GitHub Token detected\n"; fi
if echo "$content" | grep -q "sk-[a-zA-Z0-9]\{48\}"; then ISSUES="${ISSUES}  - OpenAI Key detected\n"; fi
if echo "$content" | grep -q "PRIVATE KEY-----"; then ISSUES="${ISSUES}  - Private Key detected\n"; fi

if [ -n "$ISSUES" ]; then
    MSG="[security-check] WARNING: Potential security issue detected in $file_path:\n$ISSUES[security-check] Please verify this is not a real secret before committing."
    
    jq -n --arg msg "$MSG" '{
        continue: true,
        systemMessage: $msg,
        hookSpecificOutput: {
            hookEventName: "PreToolUse",
            permissionDecision: "allow",
            permissionDecisionReason: $msg
        }
    }'
    exit 0
fi

exit 0
