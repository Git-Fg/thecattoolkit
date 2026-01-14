---
description: "Update or modify existing plans."
argument-hint: "<status update or change request>"
allowed-tools: [Read, Write, Edit, Skill(project-lifecycle)]
disable-model-invocation: true
---

# Manage Plan

## Quick Reference
- **Usage**: `/sys-builder:manage-plan "<action>"`
- **Purpose**: Update plan files, modify structure, view status
- **Returns**: Modified plan files
- **Constraint**: Does NOT execute code—only modifies plan files

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start) (Common operations)
3. [Detailed Protocol](#detailed-protocol) (Complete workflow)
4. [Common Operations](#common-operations) (Reference guide)
5. [Examples](#examples) (Common scenarios)
6. [Reference](#reference) (Technical details)

## Overview (Expandable)

This command updates or modifies existing plans in `.cattoolkit/plan/`.

**Capabilities:**
- View plan status and progress
- Update task/phase status
- Modify plan structure
- Resume from handoffs
- Manage dependencies

**Key Features:**
- No code execution
- Only plan file modifications
- Status tracking
- Structure updates

**Uses Skills:**
- `project-lifecycle` - Templates, schemas, validation rules

## Quick Start

```bash
# View current status
/sys-builder:manage-plan "show current status"

# Mark phase complete
/sys-builder:manage-plan "mark phase 1 as complete"

# Add new task
/sys-builder:manage-plan "add task to phase 2"

# Resume from handoff
/sys-builder:manage-plan "resume from phase 2 task 3"
```

**Common Actions:**
1. **View** → Show plan status
2. **Update** → Modify task/phase status
3. **Modify** → Change structure
4. **Resume** → Continue from handoff

## Detailed Protocol

### Phase 1: Parse Request
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
   ```bash
   Read: ROADMAP.md
   Read: BRIEF.md
   Read: phase plan files
   ```

**Output:** Request parsed and validated

### Phase 2: Modify Plan
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

### Phase 3: Report Changes
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
**Commands:**
```bash
/sys-builder:manage-plan "show current status"
/sys-builder:manage-plan "display roadmap"
/sys-builder:manage-plan "view progress"
```

**Displays:**
- ROADMAP.md contents
- Phase status table
- Progress metrics
- Active phase
- Blocked phases (if any)

### Update Progress
**Mark Tasks Complete:**
```bash
/sys-builder:manage-plan "mark task 1 in phase 2 as complete"
/sys-builder:manage-plan "complete phase 1"
/sys-builder:manage-plan "mark all tasks in phase 3 as done"
```

**Mark Phases Complete:**
```bash
/sys-builder:manage-plan "mark phase 1 complete"
/sys-builder:manage-plan "complete phase 2"
```

**Update Status:**
```bash
/sys-builder:manage-plan "mark phase 2 as in progress"
/sys-builder:manage-plan "set phase 3 to blocked"
```

### Modify Structure
**Add Phases:**
```bash
/sys-builder:manage-plan "add new phase after phase 2"
/sys-builder:manage-plan "insert phase 3 before phase 4"
```

**Split Tasks:**
```bash
/sys-builder:manage-plan "split task 2 in phase 1 into 2 tasks"
/sys-builder:manage-plan "break down task 3 into subtasks"
```

**Update Dependencies:**
```bash
/sys-builder:manage-plan "add dependency phase 3 on phase 2"
/sys-builder:manage-plan "remove dependency phase 2 on phase 1"
```

### Resume Work
**From Handoff:**
```bash
/sys-builder:manage-plan "resume from phase 2"
/sys-builder:manage-plan "continue after handoff"
/sys-builder:manage-plan "restart phase 3"
```

**From Interruption:**
```bash
/sys-builder:manage-plan "resume from task 2 phase 3"
/sys-builder:manage-plan "continue execution"
```

### Modify Content
**Update BRIEF:**
```bash
/sys-builder:manage-plan "update project objective"
/sys-builder:manage-plan "add new constraint to brief"
/sys-builder:manage-plan "modify success criteria"
```

**Edit Tasks:**
```bash
/sys-builder:manage-plan "edit task 1 in phase 2"
/sys-builder:manage-plan "update task description"
/sys-builder:manage-plan "change task scope"
```

## Examples

### Example 1: View Status
```bash
/sys-builder:manage-plan "show current status"
```
**Output:**
```
Current Plan Status:

Phases:
[ x ] Phase 1: Foundation - Complete
[ ~ ] Phase 2: Core Features - In Progress
[ ] Phase 3: Enhancement - Pending
[ ] Phase 4: Polish - Pending

Progress: 1/4 phases complete (25%)
Active: Phase 2 (tasks 1-2 of 3)
```

### Example 2: Complete Task
```bash
/sys-builder:manage-plan "mark task 2 phase 2 as complete"
```
**Output:**
```
Task marked complete:
- Task 2 in Phase 2: "Implement user authentication"

Updated: phases/02-core/02-01-PLAN.md

Current Status:
Phase 2: 2/3 tasks complete
Next: Task 3 - "Add authorization"
```

### Example 3: Add Phase
```bash
/sys-builder:manage-plan "add phase 5 for deployment"
```
**Output:**
```
New phase added:
Phase 5: Deployment

Updated: ROADMAP.md

Dependencies: Phase 4 (Polish)

New structure:
[ ] Phase 5: Deployment - depends on Phase 4
```

### Example 4: Resume from Handoff
```bash
/sys-builder:manage-plan "resume from phase 3"
```
**Output:**
```
Resuming Phase 3...

Handoff Status:
✓ AWS credentials configured
✓ Merge conflicts resolved
✓ Dependency conflicts fixed

Phase 3 marked as [~] (In Progress)

Current: Task 1 - "Implement payment processing"
```

## Reference

### File Modifications
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

### Status Codes
**Valid Transitions:**
- `[ ]` → `[~]` (start phase)
- `[~]` → `[x]` (complete phase)
- `[~]` → `[!]` (block phase)
- `[!]` → `[~]` (resume phase)

**Task Status:**
- Same as phase status
- Tasks inherit phase status

### Modification Types

#### Status Updates
```bash
# Mark complete
"mark phase 1 as complete"
"complete task 2"
"set task 3 to done"

# Mark in progress
"start phase 2"
"mark task 1 as in progress"

# Mark blocked
"block phase 3"
"pause task 2"
```

#### Structural Changes
```bash
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

#### Navigation
```bash
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

### Validation Rules
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

### Error Handling
**If target not found:**
- Show available options
- Suggest similar targets
- Provide usage examples

**If invalid transition:**
- Show valid transitions
- Explain why invalid
- Suggest valid alternative

**If dependency violation:**
- Show blocking dependencies
- Explain what must complete first
- Suggest execution order

### File Structure After Modification
```
.cattoolkit/plan/{project-slug}/
├── ROADMAP.md         # Updated status/structure
├── BRIEF.md           # Updated if modified
├── phases/
│   ├── 01-setup/
│   │   ├── 01-01-PLAN.md  # Updated tasks
│   │   ├── HANDOFF.md      # Created if blocked
│   │   └── SUMMARY.md      # Created if complete
│   ├── 02-core/
│   │   └── 02-01-PLAN.md
│   └── 03-enhancement/
│       └── 03-01-PLAN.md
```

### Skills Used
| Skill | Purpose | When |
|-------|---------|------|
| managing-project-plans | Templates, schemas, validation | All operations |

### Commands Comparison
| Command | Purpose | Modifies |
|---------|---------|----------|
| create-plan | Create new plan | New files |
| run-plan | Execute plan | Execution state |
| manage-plan | Modify plan | Plan structure |
| create-plan-interactive | Create with questions | New files |

### Common Patterns
**View Status:**
- Use before execution
- Check progress
- Identify blockers

**Update Progress:**
- Mark completion
- Track status
- Maintain state

**Modify Structure:**
- Adjust plan
- Update dependencies
- Rescope work

### Limitations
- Cannot execute code
- Cannot modify outside `.cattoolkit/plan/`
- Cannot violate dependencies
- Cannot create invalid transitions

### Next Steps After Modification
**Execute Modified Plan:**
```bash
/sys-builder:run-plan
```

**View Changes:**
```bash
/sys-builder:manage-plan "show current status"
```

**Create New Plan:**
```bash
/sys-builder:create-plan "new project"
```

### Best Practices
✓ Check status before modifying
✓ Validate dependencies
✓ Maintain file structure
✓ Document significant changes
✓ Test status transitions

✗ Don't modify during execution
✗ Don't break dependencies
✗ Don't use invalid status codes
✗ Don't modify source files
