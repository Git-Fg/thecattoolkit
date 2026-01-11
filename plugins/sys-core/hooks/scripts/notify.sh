#!/bin/bash

# Notification script for Claude Code
# Adapts to the operating system to send a desktop notification

TITLE="Claude Code"
MESSAGE="Awaiting your input"

# Check if a custom message was provided as an argument
if [ -n "$1" ]; then
    MESSAGE="$1"
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\""
elif command -v notify-send >/dev/null 2>&1; then
    # Linux / capable systems
    notify-send "$TITLE" "$MESSAGE"
else
    # Fallback
    echo "[$TITLE] $MESSAGE" >&2
fi
