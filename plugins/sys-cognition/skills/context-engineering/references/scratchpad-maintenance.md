# Workflow: Update Scratchpad

## Purpose
Append decisions, errors, progress, and important context to scratchpad.md in real-time.

## When to Use
- Recording important decisions
- Documenting errors and resolutions
- Tracking progress updates
- Capturing open questions
- Updating context state
- Context window reaching 60%

## Required Reading
1. `references/context-structure.md` - Context management best practices
2. `templates/scratchpad.md` - Standard scratchpad structure

## Pre-requisites
- Context structure initialized (run `initialize` workflow first)
- Working on active task with context tracking enabled

## Step 1: Identify Update Type

**Common update scenarios:**

### Type A: Decision Made
Record important technical or architectural decisions

### Type B: Error Encountered
Document errors, investigations, and resolutions

### Type C: Progress Update
Track milestone completion and progress

### Type D: Question Raised
Note open questions that need answers

### Type E: Context Shift
Update current task, phase, or focus

## Step 2: Update Current Session Context

### If updating active task or phase:

First, backup the current scratchpad.md to `.cattoolkit/context/scratchpad.md.backup`.

Then, update the "Current Session Context" section in `.cattoolkit/context/scratchpad.md`:

```
## Current Session Context
- **Project:** {project-name}
- **Active Task:** {updated-task-description}
- **Current Phase:** {updated-phase-name}
- **Started:** {original-start-date}
- **Context Window:** {current-percentage}% used
- **Last Updated:** {YYYY-MM-DD HH:MM}
```

**Why update current context:**
- Keeps active state clear
- Helps with context handoffs
- Enables quick recovery
- Tracks phase transitions

## Step 3: Add Decision Record

### If decision made:

Append the following to the "Technical Decisions" section in `.cattoolkit/context/scratchpad.md`:

```
### {YYYY-MM-DD HH:MM} - Decision: {decision-title}
**Context:** {why-this-decision-was-needed}
**Decision:** {what-was-decided}
**Rationale:** {why-this-choice}
**Alternatives Considered:** {other-options}
**Impact:** {how-this-affects-project}
```

**Example:**
```
### 2026-01-07 14:30 - Decision: Choose PostgreSQL over MongoDB
**Context:** Need relational data for user accounts with complex joins
**Decision:** Use PostgreSQL with Prisma ORM
**Rationale:** Better ACID compliance, easier migrations, Prisma integration
**Alternatives Considered:** MongoDB (NoSQL), MySQL (lesser ORM support)
**Impact:** Database schema design, migration strategy, hosting requirements
```

## Step 4: Document Error Resolution

### If error encountered:

Append the following to the "Recent Changes" section in `.cattoolkit/context/scratchpad.md`:

```
### {YYYY-MM-DD HH:MM} - Error Resolution
**Error:** {error-description}
**Investigation:** {what-was-tried}
**Root Cause:** {underlying-issue}
**Resolution:** {how-it-was-fixed}
**Prevention:** {how-to-prevent-future-occurrence}
```

**Example:**
```
### 2026-01-07 14:45 - Error Resolution
**Error:** Authentication middleware not triggered on protected routes
**Investigation:** Checked route definitions, middleware order, module exports
**Root Cause:** middleware() called instead of middleware
**Resolution:** Changed to proper function reference
**Prevention:** Add TypeScript types for middleware signatures
```

## Step 5: Track Progress

### If milestone reached:

Append the following to the "Recent Changes" section in `.cattoolkit/context/scratchpad.md`:

```
### {YYYY-MM-DD HH:MM} - Progress Update
**Milestone:** {milestone-description}
**Completed:** {what-was-finished}
**Files Modified:** {list-files}
**Next Phase:** {upcoming-work}
```

**Update todos.md:**

Append to the "Completed" section in `.cattoolkit/context/todos.md`:

```
- [{YYYY-MM-DD}] {task-description} - {brief-details}
```

## Step 6: Add Open Questions

### If questions arise:

Append the following to the "Open Questions" section in `.cattoolkit/context/scratchpad.md`:

```
### {question-number}: {question-text}
**Context:** {why-this-matters}
**Impact:** {what-depends-on-this}
**Research Needed:** {what-to-investigate}
**Deadline:** {when-answer-needed}
**Status:** Open
```

## Step 7: Update Context Log

Append the following to `.cattoolkit/context/context.log`:

```
### {YYYY-MM-DD HH:MM} - Scratchpad Updated
**Type:** {decision/error/progress/question}
**Summary:** {brief-description}
**Context File:** .cattoolkit/context/scratchpad.md
**Files Modified:** {if-any}
```

## Step 8: Context Window Check

Estimate current context usage by counting words in `.cattoolkit/context/scratchpad.md` (approximately 1 word ≈ 1.3 tokens).

If context usage exceeds 60%, consider creating a checkpoint. If it exceeds 70%, create a checkpoint or handoff document immediately.

## Update Templates

### Decision Template
```markdown
### {YYYY-MM-DD HH:MM} - Decision: {title}
**Context:** {why-this-was-needed}
**Decision:** {what-was-chosen}
**Rationale:** {why-this-choice}
**Alternatives Considered:** {other-options}
**Impact:** {consequences}
```

### Error Template
```markdown
### {YYYY-MM-DD HH:MM} - Error: {error-name}
**Error:** {description}
**Investigation:** {steps-taken}
**Root Cause:** {underlying-issue}
**Resolution:** {how-fixed}
**Prevention:** {avoid-reurrence}
```

### Progress Template
```markdown
### {YYYY-MM-DD HH:MM} - Progress: {milestone}
**Completed:** {what-finished}
**Files:** {modified-files}
**Next:** {upcoming-work}
**Impact:** {how-this-helps}
```

### Question Template
```markdown
### {YYYY-MM-DD HH:MM} - Question: {question}
**Context:** {why-important}
**Impact:** {what-depends-on-this}
**Research:** {what-to-investigate}
**Status:** Open
```

## Pruning Rule (Critical for Context Window Management)

**When a task is marked `Done`, move its reasoning to a checkpoint and delete the raw logs from `scratchpad.md` to keep the 150k-200k context window focused on current problems.**

**Procedure:**
1. Create checkpoint: `.cattoolkit/context/checkpoints/{YYYY-MM-DD}-{task-name}.md`
2. Move completed task entries from scratchpad.md to checkpoint
3. Delete raw logs and completed task entries from scratchpad.md
4. Keep only active tasks and current decisions in scratchpad.md

**Why:** This prevents context bloat and ensures the context window focuses on *current* problems rather than historical logs.

## Best Practices

### What to Record
 **High Priority:**
- Architectural decisions
- Technology choices
- Critical errors and fixes
- Milestone completions
- Context window approaching 60%

 **Medium Priority:**
- Minor decisions
- Incremental progress
- Research findings
- Code patterns discovered

 **Don't Record:**
- Every keystroke
- Personal notes
- Irrelevant details
- Completed tasks (move to todos.md or checkpoints per Pruning Rule above)

### Update Frequency
- **Real-time**: Critical decisions, errors, phase changes
- **Hourly**: Progress updates, minor decisions
- **Session end**: Complete summary

### Quality Guidelines
1. **Be Specific**: Include technical details
2. **Add Context**: Explain why decisions matter
3. **Link to Files**: Reference modified files
4. **Include Rationale**: Document thinking process
5. **Timestamp Everything**: Track when things happened

## Example Workflow

### Scenario: Implementing User Authentication

**Step 1: Decision made - choose auth library**

Append to `.cattoolkit/context/scratchpad.md` Technical Decisions section:

```
### 2026-01-07 14:00 - Decision: Auth Library Choice
**Context:** Need JWT-based authentication for API
**Decision:** Use next-auth with Credentials provider
**Rationale:** Battle-tested, TypeScript support, easy migration
**Alternatives Considered:** Custom JWT, Passport.js, Clerk
**Impact:** API routes, middleware, user session management
```

**Step 2: Error encountered**

Append to `.cattoolkit/context/scratchpad.md` Recent Changes section:

```
### 2026-01-07 14:15 - Error Resolution
**Error:** next-auth Credentials provider not validating
**Investigation:** Checked provider config, compared to docs
**Root Cause:** Missing authorize() function in CredentialsProvider
**Resolution:** Implemented proper authorize function with password check
**Prevention:** Add integration tests for auth flow
```

**Step 3: Progress update**

Append to `.cattoolkit/context/scratchpad.md` Recent Changes section:

```
### 2026-01-07 14:30 - Progress Update
**Milestone:** User registration endpoint complete
**Completed:** Registration, login, protected route middleware
**Files Modified:** src/api/auth/register.ts, src/middleware/auth.ts
**Next Phase:** Password reset flow implementation
```

**Step 4: Update todos**

Update `.cattoolkit/context/todos.md`:

```
## Completed
- [2026-01-07] User registration endpoint - Complete with validation
- [2026-01-07] Login endpoint - JWT token generation working
- [2026-01-07] Protected routes - Middleware implemented

## Active Tasks
- [ ] Password reset flow
- [ ] Email verification
- [ ] Session management
```

## Integration

### With Other Skills
- **engineering**: Document debugging decisions and error resolutions
- **manage-planning**: Update current phase in builder's project phase plan files in `.cattoolkit/planning/`
- **thinking-frameworks**: Record strategic thinking outcomes
- **git-workflow**: Link commits to context updates

### File Cross-References (Examples)
- `scratchpad.md#technical-decisions` - See auth library decision
- `todos.md#completed` - See completed authentication tasks
- `checkpoints/YYYY-MM-DD-auth-start.md` - Pre-implementation state


## Troubleshooting

### Scratchpad Too Large
1. Archive old entries to checkpoint: Create `.cattoolkit/context/checkpoints/{YYYY-MM-DD}-scratchpad-archive.md`
2. Move older entries to the archive file
3. Clean scratchpad.md keeping only recent entries

### Duplicate Entries
1. Find duplicate entries in scratchpad.md
2. Manually review and remove duplicates
3. Verify content integrity after cleanup

### Missing Timestamps
1. Add timestamps to entries that lack them
2. Use the format: `### {YYYY-MM-DD HH:MM} -`
3. Ensure all entries are properly dated

## Next Steps

After updating scratchpad:
1. **Continue execution** - Work with updated context
2. **Monitor usage** - Watch for 70% threshold
3. **Create checkpoint** - If reaching critical levels
4. **Update todos** - Track task completion

The scratchpad now contains current decisions and context for continued work.
