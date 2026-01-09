# @cattoolkit/context

**Session state management and scratchpad pattern for avoiding context overflow and enabling session handoffs.**

**License:** MIT

## Purpose

Provides persistent session state management independent of the LLM context window using the **Scratchpad Pattern**. Preserve decisions, track progress, and enable seamless session handoffs for solo developers working with AI agents.

## Usage

### Automatic (Hooks)
- **Initialization**: Auto-loads on session start
- **Logging**: Auto-tracks changes to `context.log`
- **Compaction**: Auto-compacts working memory when full

### Manual (Skill)

Invoke the skill directly to manage context:

```bash
/context-engineering
```

**Capabilities:**
- Create comprehensive handoffs
- Summarize current session
- Archive completed work

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
