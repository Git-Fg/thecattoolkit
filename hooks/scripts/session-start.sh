#!/bin/bash
# SessionStart Hook - Injects Plugin Rules into Context

# Get the content and escape it for JSON
CONTENT=$(cat ${CLAUDE_PLUGIN_ROOT}/docs/PLUGIN_RULES.md | tr '\n' ' ' | sed 's/  */ /g')

# Escape double quotes for JSON
CONTENT=$(echo "$CONTENT" | sed 's/"/\\"/g')

# Output JSON with hookSpecificOutput
echo "{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": \"$CONTENT\"}}"
