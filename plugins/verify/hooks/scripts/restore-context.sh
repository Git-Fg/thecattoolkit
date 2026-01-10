#!/bin/bash

# SessionStart Hook: Restores context from Planner and scratchpad.

# Get project root
ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
CONTEXT_DIR="$ROOT/.cattoolkit/context"
PLANNING_DIR="$ROOT/.cattoolkit/planning"

# 1. Find Active Plan
PLAN_FILE=$(find "$PLANNING_DIR" -name "PLAN.md" -type f -print0 | xargs -0 ls -t | head -n 1 2>/dev/null)
if [ -f "$PLAN_FILE" ]; then
    PLAN_CONTENT=$(head -c 800 "$PLAN_FILE")
    PLAN_STATUS="✅ Active plan loaded"
    PLAN_PATH="$PLAN_FILE"
    # Add ellipsis if truncated
    if [ $(wc -c < "$PLAN_FILE") -gt 800 ]; then PLAN_CONTENT="${PLAN_CONTENT}..."; fi
else
    PLAN_CONTENT="No active plan found."
    PLAN_STATUS="⚠️ No active plan"
    PLAN_PATH="N/A"
fi

# 2. Get Scratchpad
SCRATCHPAD_FILE="$CONTEXT_DIR/scratchpad.md"
if [ -f "$SCRATCHPAD_FILE" ]; then
    SCRATCHPAD_CONTENT=$(head -c 600 "$SCRATCHPAD_FILE")
    SCRATCHPAD_STATUS="✅ Loaded"
    SCRATCHPAD_SIZE=$(wc -c < "$SCRATCHPAD_FILE" | xargs)
    if [ $(wc -c < "$SCRATCHPAD_FILE") -gt 600 ]; then SCRATCHPAD_CONTENT="${SCRATCHPAD_CONTENT}..."; fi
else
    SCRATCHPAD_CONTENT="Scratchpad not yet initialized."
    SCRATCHPAD_STATUS="⚠️ Not initialized"
    SCRATCHPAD_SIZE="0"
fi

# 3. Get Todos
TODOS_FILE="$CONTEXT_DIR/todos.md"
if [ -f "$TODOS_FILE" ]; then
    TODOS_CONTENT=$(head -c 400 "$TODOS_FILE")
    TODOS_STATUS="✅ Loaded"
    TODOS_SIZE=$(wc -c < "$TODOS_FILE" | xargs)
    if [ $(wc -c < "$TODOS_FILE") -gt 400 ]; then TODOS_CONTENT="${TODOS_CONTENT}..."; fi
else
    TODOS_CONTENT="No todos tracked yet."
    TODOS_STATUS="ℹ️ Not tracking todos"
    TODOS_SIZE="0"
fi

# 4. Get Context Log
LOG_FILE="$CONTEXT_DIR/context.log"
if [ -f "$LOG_FILE" ]; then
    LOG_CONTENT=$(tail -n 10 "$LOG_FILE")
    LOG_COUNT=$(wc -l < "$LOG_FILE" | xargs)
    LOG_STATUS="✅ $LOG_COUNT entries"
else
    LOG_CONTENT="No context log yet."
    LOG_STATUS="ℹ️ No history yet"
fi

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Output formatted message
cat <<EOF
# 🧠 MEMORY RESTORED - $TIMESTAMP

## 📋 Current Plan (Source of Truth)
**Status**: $PLAN_STATUS
**Source**: \`$PLAN_PATH\`

$PLAN_CONTENT

---

## 📝 Scratchpad (Working Memory)
**Status**: $SCRATCHPAD_STATUS
**Size**: $SCRATCHPAD_SIZE characters

$SCRATCHPAD_CONTENT

---

## ✅ Active Tasks (Todos)
**Status**: $TODOS_STATUS
**Size**: $TODOS_SIZE characters

$TODOS_CONTENT

---

## 📊 Session History (Recent)
**Status**: $LOG_STATUS

$LOG_CONTENT

---

## 🔄 Auto-Memory System Active

This session is using **Passive Memory Hooks**:
- ✅ **SessionStart**: Plan and scratchpad auto-loaded
- ✅ **PostToolUse**: All edits/bash logged automatically
- ✅ **PreCompact**: Memory compaction before context overflow

> System ready. Context fully restored from persistent storage.
EOF
