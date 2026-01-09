# Handoff Template

**MANDATORY:** Use this template when execution must pause. Enables "State-in-Files" architecture.

## MANDATORY Triggers

- Unrecoverable blocker (auth gate, critical error)
- Agent cannot proceed without human intervention

## Location

**MUST** create in phase directory: `.cattoolkit/planning/{project-slug}/phases/XX-name/HANDOFF.md`

## Template

```markdown
# Phase [X]: [Name] Handoff

**Session paused:** [YYYY-MM-DD HH:MM]
**Reason:** [AUTH_GATE | AMBIGUOUS | CONFLICT | User requested]
**Progress:** [N]/[M] tasks complete

## Current State

**Phase:** XX-name
**Plan File:** `XX-YY-PLAN.md`
**Status:** [In Progress / Partially Complete]

### Completed Tasks

- [x] **Task [N]: [Task name]**
  - **Result:** [Brief outcome]
  - **Files modified:** [List]
  - **Verification:** [Status]

### In-Progress Task

- [ ] **Task [N]: [Current task name]**
  - **Where I left off:** [Specific point of interruption]
  - **What was done:** [Steps completed]
  - **What remains:** [Next steps to continue]

### Remaining Tasks

- [ ] **Task [N]: [Next task name]** - Not started
- [ ] **Task [N]: [Following task]** - Not started

## Blockers

**[If no blockers: None]**

**[If blockers exist:]**

### Blocker 1: [Description]

- **Type:** [AUTH_GATE | AMBIGUOUS | CONFLICT]
- **Impact:** [What this prevents]
- **Attempted resolutions:** [What was tried]
- **Next action needed:** [Specific step to resolve]

## Context Snapshot

**Files currently open/modified:**
- `path/to/file.ts` - [Brief state description]
- `path/to/another.ts` - [Brief state description]

**Decisions made this session:**
- [Decision 1 with rationale]
- [Decision 2 with rationale]

** deviations from plan:**
- [Any unplanned changes or issues encountered]

## Next Actions (Ordered)

When resuming, execute in this order:

1. **[First action]** - [Brief description]
2. **[Second action]** - [Brief description]
3. **[Third action]** - [Brief description]

## Resume Instructions

**To resume this session:**

1. Read this HANDOFF.md file completely
2. Read the phase PLAN.md to see full context
3. Read BRIEF.md and ROADMAP.md for project context
4. Continue from "In-Progress Task" section above
5. Delete this HANDOFF.md file when phase is complete

**DO NOT:** Restart the phase or redo completed tasks.

**Verification before resuming:**
- [ ] All completed tasks in this handoff match PLAN.md status
- [ ] In-progress task is clear on where to continue
- [ ] All file modifications are saved
- [ ] No merge conflicts or unresolved states

---

*Handoff created: [YYYY-MM-DD HH:MM]*
*Resume with: Continue from Task [N] - [Task name]*
```

## MANDATORY Principles

1. **MUST Be Specific**: "Left off at line 42 of auth.ts" not "Was working on auth"
2. **MUST List Everything**: All files modified, all decisions made
3. **MUST Order Actions**: Next steps must be executable in order
4. **MUST Delete on Complete**: Handoff is temporary state, not permanent documentation

## Example

```markdown
# Phase 1: Foundation Handoff

**Session paused:** 2026-01-08 14:32
**Reason:** Session checkpoint for extended planning
**Progress:** 2/3 tasks complete

## Current State

**Phase:** 01-foundation
**Plan File:** `01-01-PLAN.md`
**Status:** Partially Complete

### Completed Tasks

- [x] **Task 1: Initialize project**
  - **Result:** Project scaffolded with dependencies
  - **Files modified:** project config files
  - **Verification:** Build passes

- [x] **Task 2: Create server**
  - **Result:** Server running on port 3000 with health check
  - **Files modified:** src/server
  - **Verification:** Health check returns 200

### In-Progress Task

- [ ] **Task 3: Configure database**
  - **Where I left off:** About to initialize ORM after installing packages
  - **What was done:** Installed database packages
  - **What remains:** Initialize ORM, configure connection, create schema

### Remaining Tasks

None - Task 3 is last task in this phase

## Blockers

None

## Context Snapshot

**Files currently open/modified:**
- `src/server` - Server with health check endpoint
- `.env` - Created but empty, needs DATABASE_URL

**Decisions made this session:**
- Using ORM for database access

**Deviations from plan:**
- None

## Next Actions (Ordered)

1. **Initialize ORM** - Run initialization command
2. **Add DATABASE_URL to .env** - Configure connection string
3. **Create User model** - Define database structure
4. **Run migration** - Create initial database migration
5. **Verify schema** - Run validation

## Resume Instructions

**To resume this session:**

1. Read this HANDOFF.md file completely
2. Read `01-01-PLAN.md` to see full task details
3. Read project BRIEF.md and ROADMAP.md for context
4. Continue from Task 3: Configure database
5. Delete this HANDOFF.md file when phase is complete

**DO NOT:** Restart Tasks 1 or 2 - they are complete.

---

*Handoff created: 2026-01-08 14:32*
*Resume with: Continue from Task 3*
```

## MANDATORY Verification Checklist

After creating a handoff:
- [ ] All completed tasks listed with outcomes
- [ ] In-progress task has specific "where I left off"
- [ ] All modified files listed
- [ ] Next actions are ordered and executable
- [ ] Blockers section is accurate (or "None")
- [ ] Resume instructions are clear
- [ ] Handoff file is in phase directory (not root)
