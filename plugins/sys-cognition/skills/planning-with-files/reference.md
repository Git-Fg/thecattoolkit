# Reference: Context Engineering and Planning with Files

This reference documents the theoretical foundations and advanced techniques of the Planning with Files workflow, based on Manus's $2 billion context engineering research.

## Theoretical Foundation: Manus Context Engineering

### Background: The $2 Billion Context Problem

In December 2025, Meta acquired Manus for $2 billion, recognizing that **context management** is the critical bottleneck in AI agent effectiveness. Their research identified fundamental limitations in how AI systems manage long-running workflows.

### The 6 Manus Principles

Manus's research distilled context engineering into six core principles:

#### 1. Filesystem as External Memory

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

#### 2. Attention Manipulation Through Repetition

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

#### 3. Keep Failure Traces

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

#### 4. Avoid Few-Shot Overfitting

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

#### 5. Stable Prefixes for Cache Optimization

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

#### 6. Append-Only Context

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
│    Choose appropriate tool                    │
│    Read necessary files                      │
│    Prepare arguments                         │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ 4. EXECUTE                                  │
│    Run tool                                 │
│    Observe results                           │
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
│    Loop back to step 1                       │
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

## Advanced Context Engineering Techniques

### Technique 1: Structured State Persistence

Store state in a structured format:

```markdown
## State Tracking
- Current Phase: 3 of 5
- Files Modified: 3
- Tests Run: 12 (all passing)
- Coverage: 78%
- Build Status: ✓ Success
```

Benefits:
- Quick state assessment
- Easy to compare across sessions
- Structured data can be parsed

### Technique 2: Decision Checkpointing

Before major decisions, update plan:

```markdown
## Decisions Made
- [2026-01-11 14:32] Technology: React over Vue
  Rationale: Team experience, ecosystem maturity
  Vote: 3-1, unanimous agreement

- [2026-01-11 14:45] Database: PostgreSQL over MySQL
  Rationale: Better JSON support, scaling characteristics
  Vote: 4-0, unanimous
```

Benefits:
- Rationale preserved for future reference
- Team alignment visible
- Rollback possible if needed

### Technique 3: Error Learning Loop

Transform errors into learning:

```markdown
## Errors Encountered
- [2026-01-11 14:00] TypeError: Cannot read property 'id' of undefined
  → Cause: User object not awaited properly
  → Fix: Added await before accessing user
  → Prevention: Add type guards in similar contexts

- [2026-01-11 14:20] API timeout after 30s
  → Cause: No retry logic implemented
  → Fix: Added exponential backoff (3 retries)
  → Prevention: Implement retry helper for all API calls
```

Benefits:
- Pattern recognition develops
- Prevention strategies emerge
- Knowledge compounds across tasks

### Technique 4: Context Sandwich Pattern

For very long tasks (>100 calls):

```
[Start]
Read task_plan.md ← Fresh context
Read notes.md ← Additional context
[Execute work]
[Every 30 calls]
Read task_plan.md ← Context refresh
[Continue]
[End]
Read task_plan.md ← Verify completion
```

Benefits:
- Maintains alignment
- Prevents context drift
- Ensures goal achievement

### Technique 5: Parallel Stream Tracking

For multi-faceted research:

```markdown
## Parallel Research Streams

### Stream A: Technical Architecture
- Progress: 60%
- Next: Evaluate service mesh options
- Files: architecture_research.md

### Stream B: Cost Analysis
- Progress: 80%
- Next: Cloud provider comparison
- Files: cost_analysis.md

### Stream C: Team Capabilities
- Progress: 40%
- Next: Skills assessment
- Files: team_assessment.md

## Integration Plan
Will synthesize streams in Phase 4
```

Benefits:
- Multiple threads tracked simultaneously
- Progress visible per stream
- Clear integration point

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

## Integration with Cat Toolkit

### How It Works with Skills

Planning with Files enhances other skills:

- **Deep Analysis Skill**: Store findings in notes.md
- **Prompt Engineering Skill**: Track iterations
- **Context Engineering Skill**: Manage working memory
- **Thinking Frameworks Skill**: Structure reasoning

### File Structure in Projects

```
project/
├── .cattoolkit/          # Cat Toolkit config
├── task_plan.md          # Main plan file
├── notes.md              # Research/findings
├── deliverable.md        # Final output
└── supporting/          # Additional files
    ├── api_research.md
    ├── architecture.md
    └── cost_analysis.md
```

### Best Practices for Cat Toolkit Integration

1. **Co-locate with project**: Keep plan files in project root
2. **Version control**: Include in git (unless contains sensitive data)
3. **Naming consistency**: Use clear, descriptive filenames
4. **Cross-references**: Link between files
5. **Cleanup**: Archive completed plans after project end

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

### Cache Optimization

Structure plan files for cache hits:

```
✓ GOOD: Stable prefix structure
# Task Plan: [Title]
## Goal
## Phases
## Status

✗ BAD: Ad-hoc structure
[Various headings in different orders]
```

### Memory Footprint

Comparison:
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

## Common Anti-Patterns and Solutions

### Anti-Pattern 1: Plan Hoarding

**Problem:** Creating plans but never updating them.

**Solution:** Update after EVERY phase completion:
```bash
# After finishing work
Edit task_plan.md
  # Mark [x] completed phase
  # Update Status
```

### Anti-Pattern 2: Context Stuffing

**Problem:** Still putting everything in context despite having files.

**Solution:** "Store, Don't Stuff" rule:
```bash
✓ Write findings.md
✓ Read findings.md (specific sections)
✗ Stuff everything into response
```

### Anti-Pattern 3: Silent Error Recovery

**Problem:** Errors occur, retry silently, never log.

**Solution:** Log ALL errors:
```markdown
## Errors Encountered
- [Timestamp] [Error]: [Resolution]
```

### Anti-Pattern 4: Rewriting History

**Problem:** Modifying previous sections instead of appending.

**Solution:** Append-only updates:
```bash
✓ Edit task_plan.md (checkbox [x])
✓ Append "Decision Made" section
✗ Rewrite entire goal section
```

### Anti-Pattern 5: No Plan First

**Problem:** Starting work without creating plan.

**Solution:** Plan-first rule (non-negotiable):
```bash
Write task_plan.md  # ALWAYS first step
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

## Reference Implementation: Template Library

### Template 1: Research Task Plan

```markdown
# Task Plan: [Research Topic]

## Goal
[One sentence describing research objective]

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Gather sources
- [ ] Phase 3: Analyze findings
- [ ] Phase 4: Synthesize insights
- [ ] Phase 5: Create deliverable

## Key Questions
1. [Research question]
2. [Research question]
3. [Research question]

## Sources Found
- [Count] sources collected
- [Status] Research phase

## Status
**Currently in Phase X** - [What you're doing now]
```

### Template 2: Development Task Plan

```markdown
# Task Plan: [Feature/Bug Name]

## Goal
[One sentence describing desired end state]

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Understand requirements
- [ ] Phase 3: Design solution
- [ ] Phase 4: Implement code
- [ ] Phase 5: Test thoroughly
- [ ] Phase 6: Document and deliver

## Technical Details
- Files to modify: [List]
- Dependencies: [List]
- Testing approach: [Description]

## Decisions Made
- [Decision]: [Rationale]

## Errors Encountered
- [Timestamp] [Error]: [Resolution]

## Status
**Currently in Phase X** - [What you're doing now]
```

### Template 3: Multi-Stream Research Plan

```markdown
# Task Plan: [Multi-Topic Research]

## Goal
[One sentence describing overall objective]

## Phases
- [x] Phase 1: Create plan ✓
- [ ] Phase 2: Research streams
  - [ ] Stream A: [Topic] - [Status]
  - [ ] Stream B: [Topic] - [Status]
  - [ ] Stream C: [Topic] - [Status]
- [ ] Phase 3: Synthesize findings
- [ ] Phase 4: Create comprehensive deliverable

## Research Streams

### Stream A: [Topic]
- Focus: [What to investigate]
- Target sources: [Number]
- Status: [X% complete]
- File: stream_a.md

### Stream B: [Topic]
- Focus: [What to investigate]
- Target sources: [Number]
- Status: [X% complete]
- File: stream_b.md

### Stream C: [Topic]
- Focus: [What to investigate]
- Target sources: [Number]
- Status: [X% complete]
- File: stream_c.md

## Status
**Currently in Phase 2** - Researching streams
```

## Conclusion

Planning with Files implements proven context engineering principles to transform chaotic AI workflows into organized, trackable, recoverable processes. The filesystem becomes unlimited memory, plan files refresh attention, errors become learning, and the 3-file pattern provides structure for any complex task.

**Key Takeaway:** Context engineering isn't just about tools—it's about fundamentally rethinking how AI agents manage information over time. Files are the foundation for reliable, long-running workflows.
