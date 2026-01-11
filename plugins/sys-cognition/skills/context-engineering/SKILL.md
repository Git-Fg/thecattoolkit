---
name: context-engineering
description: "USE when optimizing AI agent context: compression, degradation detection, KV-cache optimization, or session management. Unified interface for all context engineering patterns."
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

**Cost Impact:**
```
Cached tokens:   $0.30 per 1M tokens
Uncached tokens: $3.00 per 1M tokens
Target hit rate: >80% = 70%+ cost savings
```

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
