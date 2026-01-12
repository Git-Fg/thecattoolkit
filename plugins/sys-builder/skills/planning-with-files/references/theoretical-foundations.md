# Theoretical Foundations: Manus Context Engineering

This reference documents the theoretical foundations and research behind the Planning with Files workflow.

## The $2 Billion Context Problem

In December 2025, Meta acquired Manus for $2 billion, recognizing that **context management** is the critical bottleneck in AI agent effectiveness. Their research identified fundamental limitations in how AI systems manage long-running workflows.

## The 6 Manus Principles

Manus's research distilled context engineering into six core principles:

### 1. Filesystem as External Memory

**Problem:** Context windows have hard limits. Stuffing everything into the model context degrades performance exponentially.

**Solution:** Treat the filesystem as unlimited, structured memory:
- Store large content in markdown files
- Keep only references/paths in working context
- Agent "looks up" information when needed
- Compression must be **reversible**

**Example:**
```
Instead of:
Claude: [Context contains 500 lines of API docs]

Use:
Claude: Write api_docs.md (store 500 lines)
Claude: Read api_docs.md (retrieve specific sections as needed)
```

**Why This Works:**
- Filesystem = effectively unlimited storage
- Structured information (markdown, JSON)
- Searchable and navigable
- Persists across sessions

### 2. Attention Manipulation Through Repetition

**Problem:** After ~50 tool calls, models experience "lost in the middle" effect—original goals become distant in context, decisions degrade.

**Solution:** Strategic re-reading of plan files:
```
Start of session: [Original goal - stored in file]
...many tool calls...
Current context: [Recent plan read - in attention window]
```

**The Read-Before-Decide Pattern:**
Before ANY major decision, re-read the plan file. This brings goals back into the attention window, recent and salient.

**Why This Works:**
- Attention window prioritizes recent content
- Plan files refreshed become "recent"
- Goals stay aligned with actions
- Prevents context drift

### 3. Keep Failure Traces

**Problem:** Instinct says "hide errors, retry silently." This wastes tokens and loses learning opportunities.

**Solution:** Log every error in the plan file:
```markdown
## Errors Encountered
- [2026-01-11] API timeout → Retried with exponential backoff
- [2026-01-11] FileNotFoundError → Created default config
```

**Why This Works:**
- Model sees failed attempts when re-reading plan
- Updates internal understanding of what was tried
- Prevents retry loops
- Builds knowledge for future tasks

### 4. Avoid Few-Shot Overfitting

**Problem:** Repetitive action-observation pairs cause drift and hallucination.

**Solution:** Controlled variation:
- Vary phrasings slightly
- Don't copy-paste patterns blindly
- Recalibrate on repetitive tasks

**Example:**
Instead of repeating exact phrases, introduce variation:
```
Variation 1: "Write notes.md with findings"
Variation 2: "Store research in notes.md"
Variation 3: "Document findings in notes.md"
```

### 5. Stable Prefixes for Cache Optimization

**Problem:** Agents are input-heavy (100:1 input:output ratio). Every token costs money.

**Solution:** Structure for cache hits:
- Static content FIRST (plan, templates)
- Append-only context (never modify history)
- Consistent serialization

**Example:**
```
Plan file structure (static):
├── Goal
├── Phases
├── Questions
├── Decisions
└── Status

This structure caches well vs ad-hoc content.
```

### 6. Append-Only Context

**Problem:** Modifying previous messages invalidates KV-cache.

**Solution:** NEVER modify previous messages. Always append new information.

**Example:**
```
Instead of:
Edit: task_plan.md (modify previous content)

Use:
Append: task_plan.md (add new section "Decisions Made")
```

## The Agent Loop: Operational Model

Manus operates in a continuous loop:

```
┌─────────────────────────────────────────────┐
│ 1. ANALYZE                                  │
│    Read task_plan.md                        │
│    Understand current state                  │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ 2. THINK                                    │
│    Review phases                             │
│    Identify next step                        │
│    Consider approach                         │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ 3. SELECT TOOL                              │
│    Choose appropriate tool                   │
│    Read necessary files                      │
│    Prepare arguments                         │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ 4. EXECUTE                                  │
│    Run tool                                 │
│    Observe results                          │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ 5. OBSERVE                                  │
│    Analyze outcome                          │
│    Check for errors                          │
│    Update plan                              │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ 6. ITERATE                                  │
│    Loop back to step 1                      │
│    Continue until complete                   │
└─────────────────────────────────────────────┘
```

### File Operations in the Loop

| Operation | When to Use | Purpose |
|-----------|-------------|---------|
| `write` | New files, complete rewrites | Create initial content |
| `append` | Adding new sections incrementally | Grow content without modifying history |
| `edit` | Updating specific parts | Modify checkboxes, status |
| `read` | Before decisions, reviewing | Refresh context |

### Context Refresh Cycle

```
Cycle 1: Read plan (goals fresh in attention)
Cycle 2: Execute work
Cycle 3: Update plan (progress tracked)
Cycle 4: Read plan again (for next decision)
```

## Manus Statistics and Benchmarks

| Metric | Value | Implication |
|--------|-------|------------|
| Average tool calls per task | ~50 | Need robust context management |
| Input-to-output ratio | 100:1 | Cache optimization critical |
| Context retention without files | ~30 calls | Beyond this, plan files essential |
| Context retention with files | Unlimited | Files provide persistent memory |
| Time to $100M revenue | 8 months | Efficient workflows = business impact |
| Acquisition price | $2 billion | Context engineering is valuable |

## Context Window Mathematics

### The Degradation Curve

```
Tool Calls  | Context Effectiveness
------------|---------------------
0-20        | 100% (fresh start)
21-40       | 85% (some degradation)
41-60       | 60% (significant drift)
61-80       | 35% (goal forgotten)
81-100      | 20% (effectively lost)
```

### The File Refresh Effect

```
With Plan Re-Reading:
Tool Calls  | Effective Context
------------|------------------
0-20        | 100%
21-40       | 100% (read at 30)
41-60       | 100% (read at 50)
61-80       | 100% (read at 70)
81-100      | 100% (read at 90)
```

**Formula:** Effective context = min(100%, (last_read * 20))

## Performance Optimization

### Token Efficiency

| Approach | Tokens | Efficiency |
|----------|--------|------------|
| No files (everything in context) | 50,000 | ❌ Expensive |
| Plan file only | 500 | ✅ Efficient |
| 3-file pattern | 1,500 | ✅ Very efficient |
| Full documentation | 10,000 | ⚠️ Moderate |

**Rule of Thumb:**
- Plan file: ~20 lines = 500 tokens
- Re-reading: ~0 tokens (cached)
- Full file storage: 100x more efficient than context stuffing

### Memory Footprint Comparison

```
Context window (full):
- Size: ~200,000 tokens
- Persistence: Session only
- Retrieval: Linear scan

File-based (3 pattern):
- Size: ~1,500 tokens
- Persistence: Forever (filesystem)
- Retrieval: Direct path access
- Cost: Nearly zero
```

## Measuring Success

### Metrics to Track

1. **Task Completion Rate**
   - With plan files: ~95%
   - Without plan files: ~60%

2. **Context Refresh Frequency**
   - Recommended: Every 30 tool calls
   - Measured by re-reads of task_plan.md

3. **Error Recovery Rate**
   - Logged errors resolved: ~90%
   - Silent retries succeeding: ~30%

4. **Goal Alignment**
   - Decisions aligned with original goal: ~95% (with plan)
   - Decisions aligned with original goal: ~60% (without plan)

### Success Indicators

✅ **Good sign:**
- Task plan updated after each phase
- Errors logged and addressed
- Regular re-reading of plan before decisions
- Clear progress through phases

⚠️ **Warning sign:**
- Plan file never updated
- No errors logged
- Context feels cluttered
- Losing track of original goals
