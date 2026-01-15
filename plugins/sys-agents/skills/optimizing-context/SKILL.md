---
name: optimizing-context
description: "Provides unified interface for all context engineering patterns. Use when optimizing AI agent context: compression, degradation detection, KV-cache optimization, or session management."
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(rm:*), Glob, Grep]
---

# Context Engineering

Unified skill for all context engineering patterns in AI agent systems. This skill consolidates context management, compression, degradation detection, and KV-cache optimization into a single entry point with progressive disclosure.

## Quick Decision Matrix

| Problem | Solution | Reference |
|:--------|:---------|:----------|
| Context window filling up | **Compression** | [compression.md](references/compression.md) |
| Agent ignoring mid-context info | **Degradation Detection** | [degradation.md](references/degradation.md) |
| High API costs | **KV-Cache Optimization** | [kv-cache.md](references/kv-cache.md) |
| Session state persistence | **Session Management** | [session-management.md](references/session-management.md) |

## Core Concepts

### Context Window Thresholds

| Utilization | Action | Technique |
|:------------|:-------|:----------|
| **<60%** | Monitor | No action needed |
| **60-80%** | Light compression | Observation masking |
| **80-95%** | Aggressive compression | Summarization + compaction |
| **>95%** | Emergency | Force session handoff |

### The Four-Bucket Framework

1. **Write**: Save non-critical info outside context (scratchpads, files)
2. **Select**: Pull only relevant context (high-precision retrieval)
3. **Compress**: Reduce while preserving information
4. **Isolate**: Separate contexts across sub-agents

## Compression Techniques Summary

| Technique | Token Overhead | Reduction | Best For |
|:----------|:--------------|:----------|:---------|
| **Observation Masking** | 0% | 90-98% | Tool outputs >200 tokens |
| **Summarization** | 5-7% | 60-90% | Mixed content |
| **Compaction** | 0% | 50-80% | Older messages |

**Quick Pattern - Observation Masking:**
```
Before: 500 lines of tool output (500 tokens)
After:  "See /results/search_20260101.txt" (12 tokens)
```

## Degradation Patterns Summary

| Pattern | Symptom | Mitigation |
|:--------|:--------|:-----------|
| **Lost-in-Middle** | Info at 40-60% position ignored | Place critical info at start/end |
| **Context Poisoning** | Errors compound through references | Require source citations |
| **Context Distraction** | Model ignores training knowledge | Quality over quantity |
| **Context Confusion** | Incorrect associations | Rigorous context selection |
| **Context Clash** | Contradictory information | Establish information hierarchy |

## KV-Cache Optimization Summary

**The Four Principles:**

1. **Stable Prefix**: Never change system prompts across requests
2. **Append-Only**: Never modify previous messages
3. **Deterministic Serialization**: Same data = same tokens (sort JSON keys)
4. **Explicit Breakpoints**: Mark cache boundaries



## Session Management Summary

**Directory Structure:**
```
.cattoolkit/
├── context/
│   ├── scratchpad.md    # Current thinking/decisions
│   ├── todos.md         # Persistent task tracking
│   ├── context.log      # Session history
│   └── checkpoints/     # State snapshots
```

**Scratchpad Hygiene Rule:**
Only update scratchpad for:
- Critical decisions made
- Errors encountered
- Phase changes
- Progress milestones

## Attention Manipulation via TodoWrite (Proactive Tracking)

The **recitation technique** from Manus/Claude Code pushes objectives into recent attention span to prevent "lost-in-the-middle" issues:

### The Pattern:
1. **Create todo.md** at task start
2. **Update continuously** - Check off completed items, add new ones
3. **Recite objectives** - Rewrite todo to push global plan into model's recent attention

### Why It Works:
- **Constant todo rewriting recites objectives into context end**
- Avoids "lost-in-the-middle" issues without architectural changes

### Implementation:
```markdown
# Before task
- [ ] Research codebase structure
- [ ] Identify patterns
- [ ] Plan implementation

# After research
- [x] Research codebase structure
- [ ] Identify patterns ← Still visible in recent attention
- [ ] Plan implementation
```

**Best Practice:** Update todos after every major tool call to maintain objective visibility.

## System Reminders Integration

System reminders combat context degradation through **recurring objective injection**:

### Locations:
1. **User messages** - System reminders in prompt
2. **Tool results** - Runtime injections
3. **Code execution** - Added via scripts

### Usage Pattern:
```bash
# Add reminder at critical points
echo "Reminder: Focus on authentication edge cases" >> .claude/reminders.txt
```

### Effective Reminders:
- **Objective recitation** - Reiterate main goal
- **Constraint reinforcement** - Re-emphasize critical requirements
- **Context anchoring** - Reference key context elements

## Plan Mode Best Practices

Plan mode uses **recurring prompts to remind the agent**:

### Implementation:
- Creates markdown files (PLAN.md) persisted during compaction
- Stored in `.cattoolkit/context/`
- Accessible via `/plan` command
- Multiple plan prompts and tool schemas for lifecycle

### When to Use:
- Complex tasks requiring 10+ tool calls
- Multi-phase implementations
- When agent appears confused or drifting
- Long-running workflows

### Best Practices:
- Create plan at task start
- Update as understanding evolves
- Reference plan in reminders
- Use as context anchor during compaction

## Integration Points

| Skill | Integration |
|:------|:------------|
| **memory-systems** | Long-term memory complements context |
| **agent-orchestration** | Each agent manages own context |
| **planning-with-files** | Plans stored outside context |

## Usage

When invoked, this skill will:
1. Assess current context state
2. Identify appropriate technique
3. Apply optimization
4. Generate metrics report

**For detailed implementation, see `references/` subdirectory.**
