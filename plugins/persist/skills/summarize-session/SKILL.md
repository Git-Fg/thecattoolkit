---
name: summarize-session
description: |
  USE when consolidating session state, tracking progress, or preparing for session rotation.
  Reads session logs and creates detailed session summary with health metrics.
context: fork
agent: scribe
allowed-tools: [Read, Write, Bash(ls:.cattoolkit/context/*), Bash(cat:.cattoolkit/context/*), Glob, Grep]
---

# Summarize Session Skill

## Purpose

Analyze the current session context and create a comprehensive summary documenting all key decisions, progress, and current state. This skill operates in isolated context to preserve the main thread's token budget while generating thorough documentation.

## What It Does

The summarize-session skill:

1. **Reads Context Files**:
   - `.cattoolkit/context/scratchpad.md` - Current thinking and decisions
   - `.cattoolkit/context/todos.md` - Persistent task tracking
   - `.cattoolkit/context/context.log` - Session action history
   - `.cattoolkit/context/checkpoints/*.md` - State snapshots

2. **Analyzes Session State**:
   - Counts context entries and estimates token usage
   - Assesses context health across four dimensions
   - Identifies key decisions and progress made
   - Evaluates session completeness and relevance

3. **Generates Summary**:
   - Creates comprehensive session summary
   - Calculates health score (0-100)
   - Documents key decisions and outcomes
   - Identifies next actions and priorities

4. **Writes Outputs**:
   - Session summary: `.cattoolkit/context/session-summary-{timestamp}.md`
   - Metrics data: `.cattoolkit/context/session-metrics.json`
   - Updates context log with summary completion

## When to Use

Invoke this skill when:

- **Session approaching rotation** - Consolidate before context overflow
- **Mid-session checkpoint** - Document progress for continuity
- **Complex task completion** - Preserve important decisions
- **Handoff preparation** - Create foundation for session handoff
- **Context health check** - Assess if context is being used effectively

## Output

The skill creates:

1. **Session Summary** (Markdown):
   - Session overview and duration
   - Key decisions made
   - Progress achieved
   - Current state documentation
   - Health score assessment
   - Recommendations for improvement

2. **Metrics File** (JSON):
   - Context health scores
   - Token usage estimates
   - File operation counts
   - Timeline data

## How It Works

This skill uses the **Forked Skill Pattern** with the scribe agent:

1. **Isolated Execution** - Runs in separate context window via `context: fork`
2. **Scribe Delegation** - Delegates to scribe agent for specialized context processing
3. **Background Processing** - Main thread continues with fresh context
4. **File-Based Results** - Outputs written to `.cattoolkit/context/` directory

## Invocation

```bash
@summarize-session
```

Or as part of a natural language request:

"I need to summarize this session before rotating to a new context window."
"Create a session summary documenting all the work we've done."
"Summarize the current session state and track progress."

## Integration

Works seamlessly with:

- **Context-Engineering** - Provides methodology and templates
- **Prepare-Handoff** - Session summary becomes input for handoff creation
- **Hook System** - Integrates with automatic context logging hooks
- **Checkpoints** - References checkpoint files for state snapshots

## Benefits

- **Preserves Context** - All decisions and progress documented
- **Token Efficient** - Uses isolated context, not main thread
- **Comprehensive** - Thorough analysis across all context dimensions
- **Actionable** - Provides next steps and recommendations
- **Automated** - No manual context compilation needed
