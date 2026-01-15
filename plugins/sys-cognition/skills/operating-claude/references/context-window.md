# Context Window Management

## Understanding Context Windows

### The 200K Token Promise

Claude Code provides a **consistent 200K token context window**. This is not theoretical—Claude Code delivers it reliably.

**Contrast with other tools**:
- **Cursor**: Practical usage often falls short of 200K due to internal truncation
- **Claude Code**: Consistent 200K with explicit handling

**Why this matters**: For large, interconnected codebases where you need Claude to understand how systems connect (auth → API routes → database schema), context matters.

### The 40% Degradation Threshold

**Critical insight**: Quality degrades at ~40% context utilization, not at 100%.

**Quality curve**:
- **0-20%**: Optimal performance
- **20-40%**: Quality starts chipping away (may not be noticeable)
- **40-80%**: Significant degradation
- **80-100%**: Major issues, compaction likely

**Warning sign**: If you run `/compact` and output is still terrible, degradation happened *before* compaction.

### What Consumes Context

Every interaction adds to context:
- Messages you send
- Files Claude reads
- Code Claude generates
- Tool results
- Error messages
- **Everything accumulates**

**Once quality drops**, more context makes it worse, not better.

## Context Management Strategies

### 1. Scope Your Conversations

#### The One-Task Rule

**Rule**: One conversation per feature or task.

**Why**: Contexts bleed together and Claude gets confused.

**Examples**:
- GOOD Conversation 1: Build authentication system
- GOOD Conversation 2: Refactor database layer
- BAD Don't do both in the same conversation

**Practical application**:
```
Starting auth system implementation
  ↓
Complete auth system (all features)
  ↓
Start new conversation for database refactor
```

**Benefits**:
- Cleaner context
- Focused Claude
- Better results
- Easier to track progress

#### When to Start New Conversation

**Signals it's time for a new conversation**:
- Moving to different logical task
- Context >60% utilized
- Claude seems confused
- You've completed one major feature
- Context has unrelated discussions

### 2. External Memory Pattern

#### The Concept

Store plans and progress in **actual files** that persist across sessions.

```
.my-project/
├── plan-auth-system.md          # Auth system plan
├── plan-api-refactor.md         # API refactor plan
└── .cattoolkit/
    └── context/
        ├── current-plan.md      # What's being worked on
        └── progress.md          # What's been done
```

#### How It Works

**When you start a new conversation**:
```markdown
# Current Context

Working on: Authentication system (Phase 2)
Previous work: [Link to plan-auth-system.md]
Current status: User login implemented, working on password reset

Next steps:
1. Implement password reset flow
2. Add email verification
3. Write integration tests

Relevant files:
- src/auth/login.ts
- src/auth/password-reset.ts
- src/auth/email-verification.ts
```

**Claude can read this file** and pick up exactly where you left off.

#### External Memory Best Practices

1. **Keep files at top level** - Easier to find and reference
2. **Use consistent naming** - Easy to identify purpose
3. **Update regularly** - Keep status current
4. **Link related files** - Show relationships
5. **Version important plans** - Keep history of changes

#### Plan File Template

```markdown
# Project Plan: [Feature Name]

## Overview
Brief description of what this feature does and why it matters.

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Architecture
### Components
- Component A: Does X
- Component B: Does Y

### Data Flow
1. User action
2. System processes
3. Result returned

## Implementation Phases
### Phase 1: Core Functionality
- [ ] Task 1
- [ ] Task 2

### Phase 2: Edge Cases
- [ ] Task 3
- [ ] Task 4

### Phase 3: Polish
- [ ] Task 5
- [ ] Task 6

## Notes
- Important decisions made
- Trade-offs considered
- Open questions

## Related Files
- Existing code: `src/path/file.ts`
- New code: `src/path/new-file.ts`
- Tests: `tests/path/test-file.ts`
```

### 3. The Copy-Paste Reset

#### When Context Bloats

**Symptoms**:
- Output quality dropped
- Claude keeps misunderstanding
- Context is >70% utilized
- Conversation went off track

#### The Reset Process

1. **Copy** important terminal output
   ```bash
   # Terminal shows important results
   Test results: 12 passed, 3 failed
   Build output: Success with warnings
   ```

2. **Run** `/compact` to get summary
   ```
   Conversation Summary:
   - Implemented user authentication
   - Added password reset flow
   - Found 3 failing tests
   - Build successful with warnings
   ```

3. **Run** `/clear` to reset context
   ```
   Context cleared. Ready for fresh conversation.
   ```

4. **Paste back** only essential information
   ```markdown
   # Current Status

   Working on: Authentication system

   Completed:
   - User login ✓
   - Password reset flow ✓

   Next: Fix 3 failing tests

   Key files:
   - src/auth/test.ts (3 failing tests)
   - src/auth/password-reset.ts (recent changes)
   ```

#### Benefits

- **Fresh context** - Claude starts clear
- **Preserved information** - Critical details retained
- **Better output** - No degradation
- **Continued progress** - No restart from zero

### 4. TodoWrite Attention Manipulation

#### The Problem

In long conversations (~50 tool calls), LLMs drift off-topic or forget goals.

#### The Recitation Pattern

Constantly rewrite todos to push objectives into recent attention:

**Implementation**:
1. Create `todo.md` at task start
2. Update after every major tool call
3. Rewrite to keep global plan visible

**Example**:
```markdown
# Continuous Todo Updates

## Phase 1: Research
- [x] Analyze codebase structure
- [x] Identify auth patterns
- [ ] Review existing tests
- [ ] Document current state

## Phase 2: Implementation
- [ ] Fix failing tests (3 tests)
- [ ] Add email verification
- [ ] Update password reset flow

## Phase 3: Validation
- [ ] Run full test suite
- [ ] Verify edge cases
- [ ] Update documentation

**Current focus**: Phase 1, Task 3
**Next**: Review existing tests
```

#### Why It Works

- **Recites objectives** into context end
- **Prevents drift** in long sessions
- **Maintains focus** on global goals
- **No architectural changes** needed

### 5. Context Window Thresholds & Actions

| Utilization | Action | Technique |
|------------|--------|-----------|
| **<20%** | Monitor | No action needed |
| **20-40%** | Light compression | Observation masking |
| **40-60%** | Aggressive compression | Summarization + compaction |
| **60-80%** | Emergency | Copy-paste reset |
| **>80%** | Critical | Start new conversation |

### 6. Plan Mode Integration

#### When to Use Plan Mode

**Always use** for:
- Complex tasks (10+ tool calls)
- Multi-phase implementations
- When agent appears confused
- Long-running workflows
- Architecture decisions

#### Plan Mode + Context Management

1. **Create plan** at task start
2. **Update** as understanding evolves
3. **Reference** in reminders
4. **Use as** context anchor during compaction
5. **Store** in `.cattoolkit/context/plan.md`

**Example**:
```markdown
# Plan: Authentication System Refactor

## Current Understanding
- User login works ✓
- Password reset implemented ✓
- 3 failing tests need fixing

## Next Steps
1. Debug failing tests (Est: 30 min)
2. Add email verification (Est: 45 min)
3. Run full test suite (Est: 15 min)

## Decisions Made
- Use JWT for email verification tokens
- Store tokens in Redis (expire in 24h)
- Send verification emails via SendGrid

**Context anchor**: This plan defines scope and prevents scope creep
```

### 7. Conversation Start Templates

#### Template 1: New Feature
```markdown
# New Conversation: [Feature Name]

## Context
Starting new feature development after previous work on [X].

## Goal
[What you're building]

## Constraints
- Must work with existing [system]
- Cannot break [current functionality]
- Timeline: [deadline if any]

## Known Files
- [List relevant files]

## First Step
[What you want to do first]
```

#### Template 2: Debug Session
```markdown
# New Conversation: Debug [Issue]

## Problem
[Brief description of bug]

## Symptoms
- [Symptom 1]
- [Symptom 2]

## Environment
- Branch: [current branch]
- Node version: [version]
- Previous changes: [what changed recently]

## Reproduce Steps
1. [Step 1]
2. [Step 2]
3. [Error occurs]

## Files to Check
- [Suspected files]

## Hypothesis
[What you think might be wrong]
```

#### Template 3: Refactor
```markdown
# New Conversation: Refactor [Component]

## Current State
- [What exists now]
- Location: [path]
- Lines of code: [count]

## Target State
- [What you want it to look like]
- Improvements: [what gets better]

## Constraints
- Must maintain API compatibility
- Cannot change behavior
- Tests must continue passing

## Approach
[How you plan to do it]

## Files Involved
- [Primary files]
- [Related files]
- [Test files]
```

## Advanced Context Techniques

### 1. System Reminders

Combat degradation through **recurring objective injection**:

**Effective patterns**:
1. **Objective recitation** - Reiterate main goal
2. **Constraint reinforcement** - Re-emphasize critical requirements
3. **Context anchoring** - Reference key context elements

**Usage**:
- Add in user messages
- Inject via tool results
- Include in scripts

### 2. File-Based Context Anchoring

Store critical context in files:

```
.cattoolkit/context/
├── objectives.md          # Global goals
├── constraints.md        # Critical requirements
├── decisions.md          # Important decisions
└── current-focus.md      # Immediate next step
```

**Reference in conversation**:
```
User: "Continue working on the auth system"

Claude should:
1. Read .cattoolkit/context/current-focus.md
2. Understand immediate next step
3. Continue from there
```

### 3. Context Pre-Loading

Load context upfront rather than accumulating:

**Before** (accumulates):
```
Claude, here's my codebase...
[200 files loaded]
Now help me with X
```

**After** (pre-load):
```
Context: Working on auth system
Goal: Add email verification
Current status: Login ✓, Password reset ✓
Files: src/auth/login.ts, src/auth/password-reset.ts
Next: Implement email verification in src/auth/email-verification.ts

Help me: Implement the email verification flow
```

### 4. Conversation Checkpointing

Save conversation state to files:

```markdown
# Checkpoint: [Date/Time]

## Completed
- [Task 1] ✓
- [Task 2] ✓

## Current State
- Working on: [Current task]
- Files modified: [List]
- Tests: [Status]

## Next Actions
1. [Action 1]
2. [Action 2]

## Open Questions
- [Question 1]
- [Question 2]
```

**Use case**: When context gets full but work isn't complete.

## Measuring Context Utilization

### Claude Code Indicator

Check the context indicator (shows percentage):
- Green: <20% (optimal)
- Yellow: 20-40% (watch)
- Orange: 40-60% (compress)
- Red: >60% (reset)

### Manual Estimation

Count major context elements:
- Files read (× ~500 tokens each)
- Code generated (× length)
- Tool results (varies)
- Messages exchanged (× ~100 tokens each)

**Rough calculation**:
```
100 messages × 100 tokens = 10,000 tokens
50 files × 500 tokens = 25,000 tokens
Code generated: ~5,000 tokens
Total: ~40,000 tokens (20% of 200K)
```

## Context Anti-Patterns

### BAD Don't Do This

1. **Let it ride** - Ignore context until it breaks
2. **Copy-paste entire files** - Load only what's needed
3. **Never reset** - Better to reset than struggle
4. **All in one conversation** - Scope your tasks
5. **Ignore the indicator** - The percentage matters

### GOOD Do This Instead

1. **Monitor proactively** - Watch the percentage
2. **Use external memory** - Write plans to files
3. **Reset when needed** - Copy-paste reset is your friend
4. **Scope conversations** - One task per conversation
5. **Reference files, don't dump them** - Let Claude read what it needs

## Summary: Context Management

### Core Principles

1. **Scope conversations** - One task per conversation
2. **Use external memory** - Plans in files persist
3. **Copy-paste reset** - When context bloats
4. **Recite objectives** - Keep todos updated
5. **Plan mode first** - Start with a plan

### Thresholds & Actions

- **<20%**: Monitor
- **20-40%**: Light compression
- **40-60%**: Aggressive compression
- **>60%**: Reset or new conversation

### Tools & Techniques

- **External files** for persistence
- **TodoWrite** for attention management
- **Plan mode** for structure
- **Compaction** for recovery
- **Clear** for fresh start

### Mental Model

**Claude is stateless**. Every conversation starts from nothing except what you explicitly give it. Plan accordingly.

Next: See [patterns.md](patterns.md) for proven patterns and anti-patterns.
