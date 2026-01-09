# @cattoolkit/persist

**Making Ephemeral Context Permanent** - Session state and memory management.

## Purpose

Takes ephemeral context and makes it permanent. Provides session state management using the Scratchpad Pattern.

## Skills

- **context-engineering** - Persistent session state management, handoffs, checkpoints

## Agents

- **scribe** - Context management and session documentation

## Hooks

- **SessionStart** - Restores context from `.cattoolkit/context/`
- **PostToolUse** - Auto-logs state-changing operations
- **PreCompact** - Compacts memory before context limit
- **Stop/SubagentStop** - Session evaluation on completion

## Directory Structure

```
.cattoolkit/context/
├── scratchpad.md     # Current thinking and decisions
├── todos.md          # Persistent task tracking
├── context.log       # Session context history
├── handoff.md        # Session handoff summary
└── checkpoints/      # Critical state snapshots
```
