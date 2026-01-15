# Plan Modification Protocol

## Core Purpose

Updates or modifies existing plans in `.cattoolkit/plan/`. Does NOT execute code—only modifies plan files.

## Phase 1: Parse Request

**Goal:** Understand what to modify

**Process:**
1. **Parse Arguments**
   - Extract action from user request
   - Identify target (phase, task, plan)
   - Determine modification type

2. **Validate Request**
   - Check if plan exists
   - Verify target is valid
   - Confirm permissions

3. **Load Plan Files**
   - Read ROADMAP.md
   - Read BRIEF.md
   - Read phase plan files

**Output:** Request parsed and validated

## Phase 2: Modify Plan

**Goal:** Apply requested changes

**Process:**
1. **Update Files**
   - Modify ROADMAP.md (if needed)
   - Update phase plans (if needed)
   - Adjust BRIEF.md (if needed)

2. **Validate Changes**
   - Check file structure
   - Verify status codes
   - Confirm dependencies

3. **Save Changes**
   - Write updated files
   - Maintain formatting
   - Update timestamps

**Output:** Plan files modified

## Phase 3: Report Changes

**Goal:** Show what was modified

**Process:**
1. **Summarize Changes**
   - List files modified
   - Show status updates
   - Highlight important changes

2. **Show Current State**
   - Display updated status
   - Show progress metrics
   - Note next steps

3. **Suggest Actions**
   - Recommend next commands
   - Note dependencies
   - Warn about issues

**Output:** Change report and suggestions

## Common Operations

### View Status
**Commands:** "show current status", "display roadmap", "view progress"

**Displays:**
- ROADMAP.md contents
- Phase status table
- Progress metrics
- Active phase
- Blocked phases (if any)

### Update Progress

**Mark Tasks Complete:** "mark task 1 in phase 2 as complete", "complete phase 1"

**Mark Phases Complete:** "mark phase 1 complete", "complete phase 2"

**Update Status:** "mark phase 2 as in progress", "set phase 3 to blocked"

### Modify Structure

**Add Phases:** "add new phase after phase 2", "insert phase 3 before phase 4"

**Split Tasks:** "split task 2 in phase 1 into 2 tasks", "break down task 3 into subtasks"

**Update Dependencies:** "add dependency phase 3 on phase 2", "remove dependency"

### Resume Work

**From Handoff:** "resume from phase 2", "continue after handoff", "restart phase 3"

**From Interruption:** "resume from task 2 phase 3", "continue execution"

### Modify Content

**Update BRIEF:** "update project objective", "add new constraint to brief", "modify success criteria"

**Edit Tasks:** "edit task 1 in phase 2", "update task description", "change task scope"

## File Modifications

**Only modifies these files:**
- `ROADMAP.md` - Phase status and dependencies
- `BRIEF.md` - Project goals and requirements
- `phases/*/*.md` - Task lists and status
- `phases/*/SUMMARY.md` - Phase summaries
- `phases/*/HANDOFF.md` - Interruption state

**Never modifies:**
- Source code files
- Configuration files
- Build scripts
- Documentation outside `.cattoolkit/plan/`

## Status Codes

**Valid Transitions:**
- `[ ]` → `[~]` (start phase)
- `[~]` → `[x]` (complete phase)
- `[~]` → `[!]` (block phase)
- `[!]` → `[~]` (resume phase)

**Task Status:** Same as phase status. Tasks inherit phase status.

## Modification Types

### Status Updates
```
"mark phase 1 as complete"
"complete task 2"
"set task 3 to done"

"start phase 2"
"mark task 1 as in progress"

"block phase 3"
"pause task 2"
```

### Structural Changes
```
# Add
"add phase after 2"
"insert new task in phase 1"
"add dependency phase 3 on phase 2"

# Remove
"remove phase 4"
"delete task 2 from phase 1"
"remove dependency phase 3"

# Modify
"edit task 1 description"
"update phase 2 name"
"change task scope"
```

### Navigation
```
# View
"show status"
"display roadmap"
"view progress"
"list phases"

# Resume
"resume from phase 2"
"continue after handoff"
"restart phase 3"
```

## Validation Rules

**Before Modification:**
- Plan directory must exist
- Target phase/task must exist
- Status transitions must be valid
- Dependencies must be maintained

**After Modification:**
- ROADMAP.md structure valid
- Status codes correct
- Dependencies consistent
- Files properly formatted
