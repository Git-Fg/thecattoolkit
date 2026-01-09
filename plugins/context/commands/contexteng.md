---
description: |
  Use when managing persistent session state,
  avoiding context overflow, or enabling session handoffs to ensure architectural
  compliance and state continuity. Now powered by **Hybrid Hook System** (Command + Prompt hooks with XML output) for automatic and intelligent context management.
allowed-tools: Skill(context-engineering), Agent(scribe)
argument-hint: [create-handoff|archive-session]
disable-model-invocation: true
---

# Context Engineering Command

**🆕 HYBRID HOOK-POWERED ARCHITECTURE**: Command hooks handle deterministic operations, prompt hooks provide intelligent decisions with robust XML output.

## Hook System Architecture

**Command Hooks** (deterministic, fast):
- ✅ **SessionStart**: Auto-loads plan and scratchpad from Planner
- ✅ **PostToolUse**: Auto-logs all Edit/Write/Bash operations
- ✅ **PreCompact**: Auto-compacts memory before context overflow

**Prompt Hooks** (intelligent, LLM-powered, XML output):
- ✅ **Stop**: Decides if handoff needed before stopping (XML-based response)
- ✅ **SubagentStop**: Verifies context operations completed successfully (XML-based response)

## Operations

**Manual Operations** (use when needed):
- `create-handoff` - Consolidate memory into portable handoff document
- `archive-session` - Create complete session archive (zip context.log + scratchpad)

## Hook System Benefits

- **Zero Friction**: No more "forgot to initialize" - it's automatic
- **Single Source of Truth**: Context reads Planner files directly
- **Perfect Memory**: Every action logged automatically
- **Token Efficiency**: File-based context vs. chat history

## When to Use

**Use this command for:**
- Creating portable handoffs for next session/agent
- Archiving completed work
- Manual context operations (rare)

**Don't use for:**
- Initialization (automatic via SessionStart hook)
- Logging (automatic via PostToolUse hook)
- Context tracking (automatic via hooks)
