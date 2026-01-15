# Context Management Patterns

Detailed implementation patterns for context offloading, caching, isolation, and evolution.

## Context Offloading

### The Problem
Context compaction (summarization) can result in loss of useful information. Full fidelity is often needed for complex tasks.

### Solution: Filesystem Offloading

**Manus Approach:**
1. Write old tool results to files
2. Apply summarization only when diminishing returns from offloading
3. Agent can read files back if needed

**Cursor Approach:**
1. Offload tool results to filesystem
2. Offload agent trajectories
3. Read back into context on demand

### Plan File Pattern

For long-running agents, use plan files to maintain objective alignment:

```
1. Write plan to file at task start
2. Read plan periodically to reinforce objectives
3. Verify work against plan
4. Update plan as requirements evolve
```

---

## Context Caching

### Why Caching Matters

Agents become cost-prohibitive without prompt caching:
- Cached tokens: ~10x cheaper than uncached
- Cache hit rate: Most important production metric
- Higher-capacity model with caching can be cheaper than lower-cost model without

### Requirements for Cache Hits

| Requirement | Explanation |
|:------------|:------------|
| Stable prefix | System prompt must not change |
| Append-only | Never modify previous messages |
| Deterministic | Same data = same tokens (sort JSON keys) |
| Explicit breaks | Mark cache boundaries when possible |

### Anti-Patterns

- Mutating session history mid-conversation
- Changing system prompts dynamically
- Non-deterministic serialization of structured data

---

## Context Isolation

### The Ralph Wiggum Pattern

Named pattern for running agents repeatedly until a plan is satisfied:

```
┌─────────────────────────────────────┐
│  Initializer Agent                  │
│  - Sets up plan file                │
│  - Creates tracking file            │
│  - Establishes environment          │
└─────────────────┬───────────────────┘
                  │
    ┌─────────────┴─────────────┐
    ▼                           ▼
┌─────────┐               ┌─────────┐
│ Sub-    │               │ Sub-    │
│ Agent 1 │               │ Agent N │
└────┬────┘               └────┬────┘
     │                         │
     └──────────┬──────────────┘
                ▼
        ┌───────────────┐
        │ Git History   │
        │ (Progress)    │
        └───────────────┘
                │
                ▼
        ┌───────────────┐
        │ Stop Hook     │
        │ (Verification)│
        └───────────────┘
```

### Use Cases for Isolation

| Scenario | Why Isolation Helps |
|:---------|:--------------------|
| Parallel reviews | Each reviewer has focused context |
| Migrations | Each file gets isolated context |
| Long tasks | Context doesn't saturate |
| Different expertise | Specialized prompts per sub-agent |

---

## Context Evolution

### Continual Learning in Token Space

Update agent context (not model weights) with learnings over time.

### Task-Specific Prompt Evolution (GEPA Pattern)

```
1. Collect agent trajectories
2. Score trajectory outcomes
3. Reflect on failures
4. Propose mix of task-specific prompt variants
5. Test variants
6. Select best performers
```

### Memory Evolution

```
1. Distill sessions into diary entries
2. Reflect across diary entries
3. Update CLAUDE.md or equivalent
4. Loop over time
```

### Skill Evolution

```
1. Reflect over trajectories
2. Identify reusable procedures
3. Save as new skills to filesystem
4. Skills available for future sessions
```

### Sleep-Time Compute

Agents can think offline about their own context:
- Reflect over past sessions
- Update memories or skills proactively
- Prepare for anticipated future tasks
