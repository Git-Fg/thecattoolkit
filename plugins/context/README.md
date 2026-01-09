# @cattoolkit/context

**Session state management and scratchpad pattern for avoiding context overflow and enabling session handoffs.**

**License:** MIT

## Purpose

Provides persistent session state management independent of the LLM context window using the **Scratchpad Pattern**. Preserve decisions, track progress, and enable seamless session handoffs for solo developers working with AI agents.

## Commands

### /contexteng

Initialize or manage session context state.

```bash
/contexteng [initialize|update-scratchpad|summarize-session|create-handoff]
```

**Modes:**
- **initialize** - Set up context tracking (scratchpad.md, todos.md, context.log)
- **update-scratchpad** - Record decisions, errors, progress, and important context
- **summarize-session** - Consolidate session state before rotation or handoff
- **create-handoff** - Generate comprehensive handoff document for session transfer

**Use for:**
- Working on complex, multi-step tasks
- Context window approaching 60% capacity
- Need to preserve state across sessions
- Managing multiple parallel workstreams
- Switching between different AI tools
- Tracking decisions and thinking over time

## Skill

### context-engineering

Persistent session state management using the scratchpad pattern.

**Resources:**
- Context initialization standards
- Scratchpad maintenance procedures
- Session summary protocols
- Handoff protocol standards
- Templates for scratchpad.md, handoff.md, context.log

## The Scratchpad Pattern

**Core Problem**: AI models have limited context windows, but complex tasks require extensive context preservation across interactions.

**Solution**: Engineer context to maximize relevant information while minimizing token consumption through persistent storage in `.cattoolkit/context/`.

## Directory Structure

```
.cattoolkit/context/
├── scratchpad.md          # Current thinking and decisions
├── todos.md              # Persistent task tracking
├── context.log           # Session context history
├── handoff.md            # Session handoff summary
└── checkpoints/          # Critical state snapshots
    ├── 2025-01-05-feature-start.md
    ├── 2025-01-05-implementation-complete.md
    └── 2025-01-05-testing-phase.md
```

## Context Window Thresholds

- **60% Warning** → Begin context tracking
- **70% Critical** → Create checkpoint + handoff
- **80% Overflow** → Force session rotation

## Workflow Example

```bash
# Step 1: Initialize context tracking
/contexteng initialize

# Step 2: Update scratchpad with decisions
/contexteng update-scratchpad

# Step 3: When context is full, create handoff
/contexteng create-handoff

# Step 4: Start new session with preserved context
# The handoff.md provides all critical context
```

## Integration

- **With @cat-toolkit/builder** - Track plan execution progress and preserve debugging/review context
- **With @cat-toolkit/think** - Track strategic thinking

## Benefits

**For Solo Developers:**
- Never lose critical context
- Quick recovery after interruptions
- Systematic approach to complexity
- Better decision tracking
- Improved workflow continuity

**Workflow Improvements:**
- Reduced context loss
- Faster handoffs
- Better progress tracking
- Improved quality
- Enhanced productivity
