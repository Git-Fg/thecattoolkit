# Subagent Crisis & Token Cost Evidence

**January 2026**

## The Core Problem

Subagents are almost always a mistake within standard plan constraints due to their high token cost and quota consumption.

## The 5-Hour Rule

- A Pro session provides ~200k tokens (5 hours of typical usage)
- Subagent spawn costs: 20K-25K tokens to "say hello"
- Full system prompt reinstantiated (not cached)
- CLAUDE.md re-read in each subagent
- MCP/project context duplicated

**Real-World Impact:** Task to refactor >1000 LOC script created >40 parallel agents, each re-reading entire script. Result: Session exhaustion in 30-90 minutes instead of 5 hours.

## Quota Impact (Z.AI/Subscription Models)

- Subagents consume **1 prompt quota** per spawn (not a free tool call)
- A prompt allows 15-20 tool calls for free
- Spawning 10 subagents = 10 prompts consumed = 150-200 potential tool calls wasted
- **Use `context: fork` instead:** Runs as isolated skill context, counts as tool call (free within prompt), not as new prompt

## Examples

**BAD (Subagent for simple task):**
```yaml
# Wastes 25k tokens + 1 prompt quota
Task(subagent_type="general-purpose", prompt="Extract data from this CSV")
```

**GOOD (Inline skill):**
```yaml
# Costs ~1x, free within prompt
# Just do the work directly in context
Read the CSV and extract the required data.
```

**GOOD (Fork for isolation when needed):**
```yaml
---
name: processing-batch
description: Processes multiple files in isolated context
context: fork
---
# Costs 3x inline, but FREE as tool call within prompt
# Avoids the 1 prompt quota penalty of subagents
```

## Official Recommendation

Use main conversation when frequent back-and-forth needed. Use subagents ONLY when parallelization benefit clearly exceeds 20K token startup cost AND the subscription "prompt cost" overhead (subagents consume prompts, not free tool calls). Prefer `context: fork` for isolation needs.

## Cost Comparison

| Approach | Token Cost | Quota Cost | When to Use |
|:---------|:-----------|:-----------|:------------|
| **Inline** | ~1x | Free (tool call) | Most tasks |
| **Fork** | ~3x | Free (tool call) | Isolation needed, heavy I/O |
| **Subagent** | ~25k+ | 1 prompt per spawn | Parallelization only |
