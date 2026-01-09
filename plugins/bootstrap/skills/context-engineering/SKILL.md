---
name: context-engineering
description: |
  Passive protocol for managing persistent session state. Use when working with context files, creating handoffs, or managing session persistence. Context hooks are auto-managed by the meta plugin.
  Trigger words: preserve work, archive session, handoff document, session summary.
  Use when user mentions: "preserve work across sessions", "archive this session", "create handoff".
allowed-tools: [Read, Write, Edit, Bash]
---

# Context Engineering Skill

## Core Purpose

Manage persistent session state independent of the LLM context window. Preserve decisions, track progress, and enable seamless session handoffs through file-based persistence.

**Note:** Context hooks are auto-managed by the meta plugin. Use this skill for manual context operations only.

## Available Resources

- **[Context Initialization](references/context-initialization.md)**: Standards for setting up context foundations.
- **[Scratchpad Maintenance](references/scratchpad-maintenance.md)**: Procedures for tracking decisions and progress.
- **[Session Summary](references/session-summary.md)**: Protocols for consolidating session state.
- **[Handoff Protocol](references/handoff-protocol.md)**: Standards for seamless session rotation.

## The Scratchpad Pattern

**Core Problem**: AI models have limited context windows, but complex tasks require extensive context preservation across interactions.

**Solution**: Engineer context to maximize relevant information while minimizing token consumption through persistent storage in `.cattoolkit/context/`.

## When to Use

**Manual operations:**
- Creating comprehensive handoff documents
- Archiving completed sessions
- Manual scratchpad edits for complex decisions
- Emergency context management

**Use context-engineering when:**
- Working on complex, multi-step tasks
- Need to create portable handoffs
- Session approaching completion (archive work)
- Managing multiple parallel workstreams
- Switching between different tools (Claude Code, Cursor, Codex)

**Don't use for:**
- Initialization (automatic via hooks)
- Routine logging (automatic via hooks)
- Context tracking (automatic via hooks)

## Standard Operating Procedures

### [Context Initialization](references/context-initialization.md)
**Use when**: Starting new project or task requiring persistent state

**Creates**:
- `.cattoolkit/context/` directory structure
- Initial `scratchpad.md` with project context
- `todos.md` for persistent task tracking
- `context.log` for session history
- `checkpoints/` directory for state snapshots

### [Scratchpad Maintenance](references/scratchpad-maintenance.md)
**Use when**: Recording decisions, errors, progress, or important context

**Updates**:
- Current thinking and decisions
- Technical choices and rationale
- Progress tracking
- Open questions and issues
- Recent changes and discoveries

### [Session Summary](references/session-summary.md)
**Use when**: Consolidating session state before rotation or handoff

**Produces**:
- Session summary with key decisions
- Current state documentation
- Progress assessment
- Context health check
- Next steps identification

### [Handoff Protocol](references/handoff-protocol.md)
**Use when**: Transferring work to new session or different tool

**Generates**:
- Comprehensive handoff document
- Critical context preservation
- Next actions clarity
- File state summary
- Decision history

## Directory Structure

```
.cattoolkit/context/
├── scratchpad.md          # Current thinking and decisions
├── todos.md              # Persistent task tracking
├── context.log           # Session context history
├── handoff.md            # Session handoff summary
└── checkpoints/          # Critical state snapshots
    ├── 2026-01-05-feature-start.md
    ├── 2026-01-05-implementation-complete.md
    └── 2026-01-05-testing-phase.md
```

## Key Concepts

### Context Window Thresholds
- **60% Warning** → Begin context tracking
- **70% Critical** → Create checkpoint + handoff
- **80% Overflow** → Force session rotation

### Progressive Disclosure
- **Level 1** (500 tokens): Immediate context - current task, active files, next action
- **Level 2** (2000 tokens): Task context - requirements, approach, related files
- **Level 3** (3000 tokens): Project context - overview, decisions, conventions
- **Level 4** (On-demand): Reference context - detailed docs, examples

### Context Health Monitoring
Track these metrics:
- **Token Efficiency**: Actionable context percentage
- **Information Density**: Relevant info per token
- **Context Relevance**: Context used in responses
- **Update Frequency**: How often context is refreshed

## Integration with Other Skills

**Works seamlessly with:**
- **Manage Planning** - Track plan execution progress
- **Engineering** - Preserve debugging and review context
- **Thinking Frameworks** - Track strategic thinking
- **Git Workflow** - Preserve version control context

## Templates Reference

- **[scratchpad.md](templates/scratchpad.md)** - Standard scratchpad structure with Current Session Context, Technical Decisions, Open Questions
- **[handoff.md](templates/handoff.md)** - Session handoff format with completed work, current state, next steps
- **[context.log](templates/context-log.md)** - Context tracking format (CREATED)
- **[checkpoint.md](templates/checkpoint.md)** - Critical state snapshot template (CREATED)

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

## Quick Start

1. **Initialize**: See `references/context-initialization.md`
2. **Track**: See `references/scratchpad-maintenance.md`
3. **Monitor**: Watch context usage and update accordingly
4. **Handoff**: See `references/handoff-protocol.md`

For detailed guidance, see [Context Structure Reference](references/context-structure.md).
