#!/bin/bash

# Stop Hook: Evaluates if the session should stop or continue.
# Checks for uncommitted git changes and active HANDOFF.md files.

# Read input (only if stop_hook checked)
input=$(cat) # consume stdin

# Check for uncommitted changes
BLOCKERS=""
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    BLOCKERS="$BLOCKERS, uncommitted git changes"
fi

# Check for active HANDOFF.md
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
if [ -f "$ROOT/.cattoolkit/planning/HANDOFF.md" ]; then
    BLOCKERS="$BLOCKERS, active HANDOFF.md"
fi

# Clean up comma
BLOCKERS=$(echo "$BLOCKERS" | sed 's/^, //')

if [ -n "$BLOCKERS" ]; then
    MSG="Blockers detected: $BLOCKERS. Commit changes or resolve handoff before stopping."
    jq -n --arg msg "$MSG" '{decision: "block", reason: $msg}'
else
    jq -n '{decision: null}'
fi
