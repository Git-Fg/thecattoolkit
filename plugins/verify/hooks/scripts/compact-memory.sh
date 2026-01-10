#!/bin/bash

# PreCompact Hook: Creates memory checkpoints before context compaction.

ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
CONTEXT_DIR="$ROOT/.cattoolkit/context"
CHECKPOINT_DIR="$CONTEXT_DIR/checkpoints"
mkdir -p "$CHECKPOINT_DIR"

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
FILE_TIMESTAMP=$(date "+%Y-%m-%d-%H-%M-%S")

LOG_FILE="$CONTEXT_DIR/context.log"
SCRATCHPAD_FILE="$CONTEXT_DIR/scratchpad.md"

# Read recent actions
if [ -f "$LOG_FILE" ]; then
    ACTIONS=$(grep "\[20" "$LOG_FILE" | tail -n 20)
    if [ -z "$ACTIONS" ]; then ACTIONS="No recent actions."; fi
else
    ACTIONS="No recent actions."
fi

# Read scratchpad
if [ -f "$SCRATCHPAD_FILE" ]; then
    SCRATCHPAD=$(head -c 500 "$SCRATCHPAD_FILE")
else
    SCRATCHPAD="Empty scratchpad."
fi

# Create checkpoint
CHECKPOINT_FILE="$CHECKPOINT_DIR/checkpoint-$FILE_TIMESTAMP.md"
cat <<EOF > "$CHECKPOINT_FILE"
# Checkpoint - $TIMESTAMP

## Actions
$ACTIONS

## Scratchpad
$SCRATCHPAD
EOF

# Update scratchpad with summary (simple append for shell version)
if [ -f "$SCRATCHPAD_FILE" ]; then
    # Simple logic: Just append active summary to end for now
    # A full robust sed replacement for the sections is complex in pure shell without risking data loss
    echo -e "\n## Recent Actions ($TIMESTAMP)\n$ACTIONS" >> "$SCRATCHPAD_FILE"
fi

# Clear context log
if [ -f "$LOG_FILE" ]; then
    echo "[$TIMESTAMP] Memory compacted" > "$LOG_FILE"
fi

# Output JSON result
jq -n --arg file "$(basename "$CHECKPOINT_FILE")" '{
    continue: true,
    systemMessage: ("Memory compacted. Checkpoint: " + $file)
}'
