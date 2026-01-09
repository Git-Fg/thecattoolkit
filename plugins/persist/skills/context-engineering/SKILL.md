---
name: context-engineering
description: |
  USE when managing persistent session state, avoiding context overflow, or enabling session handoffs. 
  The Authority on Session Persistence with **Passive Hook System**. 
  Context is now auto-managed via hooks - no initialization needed!
  Keywords: context management, session handoff, scratchpad, context overflow, memory persistence
context: fork
allowed-tools: [Read, Write, Edit, Bash]
---

# Context Engineering Skill

## Available Resources

- **[Context Initialization](references/context-initialization.md)**: Standards for setting up context foundations.
- **[Scratchpad Maintenance](references/scratchpad-maintenance.md)**: Procedures for tracking decisions and progress.
- **[Session Summary](references/session-summary.md)**: Protocols for consolidating session state.
- **[Handoff Protocol](references/handoff-protocol.md)**: Standards for seamless session rotation.

## Core Purpose

Manage persistent session state independent of the LLM context window using the **Passive Hook System**. Preserve decisions, track progress, and enable seamless session handoffs with zero manual intervention.

## 🆕 Hybrid Hook-Powered Architecture

**NEW**: The Context plugin uses a **hybrid approach** combining command and prompt hooks for optimal performance and intelligence.

### The Hybrid Hook System

**Command Hooks** (Deterministic, Fast):
| Hook | Trigger | Action |
|:-----|:--------|:-------|
| **SessionStart** | Session begins | Auto-loads active plan from Planner + scratchpad state |
| **PostToolUse** | After Edit/Write/Bash | Auto-logs every state change to context.log |
| **PreCompact** | Context near overflow | Auto-creates memory checkpoint + compacts scratchpad |

**Command-Based Prompt Logic** (Deterministic Python Scripts):
| Hook | Trigger | Action |
|:-----|:--------|:-------|
| **Stop** | Session stopping | Runs `evaluate_stop.py` to check for safe exit |
| **SubagentStop** | Agent stops | Runs `evaluate_subagent.py` to verify completion |

### Why Hybrid Hooks?

**OLD WAY (Active Commands):**
- User/Agent must run `/contexteng initialize` → Often forgotten
- Manual context updates → Context rot
- Duplicate `plan.md` files → Conflicting sources of truth

**NEW WAY (Hybrid Hooks):**
- ✅ **Zero Friction**: Automatic operations via command hooks
- ✅ **Intelligent**: Smart decisions via deterministic scripts
- ✅ **Robust Parsing**: JSON output ensures reliable response parsing
- ✅ **Single Source**: Reads Planner files directly, no duplicates
- ✅ **Perfect Memory**: Every action logged, nothing lost
- ✅ **Token Efficient**: File-based memory vs. chat history bloat
- ✅ **Context-Aware**: Automated hooks evaluate when operations are safe

## When to Use

**The hooks auto-handle everything - use context-engineering for:**

**Automatic (via hooks):**
- ✅ Initializing session context (SessionStart hook)
- ✅ Logging state changes (PostToolUse hook)
- ✅ Context compaction (PreCompact hook)

**Manual operations (when needed):**
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

## The Scratchpad Pattern

**Core Problem**: AI models have limited context windows, but complex tasks require extensive context preservation across interactions.

**Solution**: Engineer context to maximize relevant information while minimizing token consumption through persistent storage in `.cattoolkit/context/`.

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
    ├── 2025-01-05-feature-start.md
    ├── 2025-01-05-implementation-complete.md
    └── 2025-01-05-testing-phase.md
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
