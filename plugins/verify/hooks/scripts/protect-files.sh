#!/bin/bash

# Protect sensitive files from modification
# Warns about edits to production configs, lock files, and sensitive directories.

# Read JSON input
input=$(jq -c '.')
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Exit if no file path
if [ -z "$file_path" ] || [ "$file_path" = "null" ]; then
    exit 0
fi

# Define patterns
PROTECTED_PATTERNS="package-lock.json|yarn.lock|pnpm-lock.yaml|Gemfile.lock|poetry.lock|Cargo.lock|.env|.env.local|.env.production|secrets/|credentials/|.git/"
WARN_PATTERNS=".github/workflows/|docker-compose.yml|Dockerfile|production/"

# Check for protected patterns
if echo "$file_path" | grep -E -q "$PROTECTED_PATTERNS"; then
    MSG="[protect-files] WARNING: Editing protected file $file_path. This file type should generally not be manually edited."
    # Output JSON warning
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

# Check for warning patterns
if echo "$file_path" | grep -E -q "$WARN_PATTERNS"; then
    MSG="[protect-files] NOTE: Editing sensitive file $file_path."
    # Output JSON warning
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
