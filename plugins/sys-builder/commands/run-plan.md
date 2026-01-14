---
description: "Execute the next pending phase in the roadmap."
argument-hint: "[optional: phase number]"
allowed-tools: [Read, Write, Edit, Task, Skill(project-lifecycle)]
disable-model-invocation: true
---

# Run Plan

## Quick Reference
- **Usage**: `/sys-builder:run-plan` or `/sys-builder:run-plan [phase-number]`
- **Purpose**: Execute phases, manage state, verify results
- **Returns**: Updated ROADMAP.md with completed phases
- **Agent**: Uses `@worker` for actual code execution

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start) (Execute in 4 steps)
3. [Detailed Protocol](#detailed-protocol) (Complete workflow)
4. [Execution Flow](#execution-flow) (State transitions)
5. [Examples](#examples) (Common scenarios)
6. [Reference](#reference) (Technical details)

## Overview (Expandable)

This command drives the execution of project phases using the `@worker` agent.

**Workflow:**
1. **Read State** → Identify current/requested phase
2. **Dispatch to Worker** → Execute tasks via worker agent
3. **Verify Results** → Check success, update state
4. **Continue Flow** → Proceed or pause

**Key Features:**
- Non-interactive execution (worker cannot ask questions)
- Automatic state management
- Handoff support for blocked phases
- Progress tracking

**Uses Skills:**
- `project-lifecycle` - Consolidated execution orchestration, state management, and standards

## Quick Start

```bash
# Execute current active phase
/sys-builder:run-plan

# Execute specific phase
/sys-builder:run-plan 2
```

**Four Steps:**
1. **Read** → Load ROADMAP.md and phase plan
2. **Dispatch** → Spawn worker agent with full context
3. **Verify** → Check execution results
4. **Update** → Mark phase complete or blocked

## Detailed Protocol

### Phase 1: Read State
**Goal:** Identify what to execute

**Process:**
1. **Read ROADMAP.md**
   ```bash
   Read: .cattoolkit/plan/{project-slug}/ROADMAP.md
   ```

2. **Identify Phase**
   - If argument provided: Use specified phase number
   - If no argument: Find first `[ ]` (pending) phase
   - Check dependencies are `[x]` complete

3. **Load Phase Plan**
   ```bash
   Read: .cattoolkit/plan/{project-slug}/phases/{XX-name}/XX-01-PLAN.md
   ```

4. **Check for Handoff**
   ```bash
   Check: .cattoolkit/plan/{project-slug}/phases/{XX-name}/HANDOFF.md
   ```

**Output:** Phase plan and execution context

### Phase 2: Dispatch to Worker
**Goal:** Execute tasks via worker agent

**Process:**
1. **Prepare Context**
   ```markdown
   BRIEF.md context
   + ROADMAP.md state
   + Phase plan content
   + Current task
   = Full execution context
   ```

2. **Spawn Worker**
   ```bash
   Task: @worker
   Tools: [Read, Write, Edit, Bash, Glob, Grep]
   Skills: [project-lifecycle, software-engineering, execution-core]
   Constraint: NON-INTERACTIVE (no AskUserQuestion)
   ```

3. **Pass Phase Plan**
   - Include ENTIRE phase file content
   - Include task details
   - Include success criteria
   - Include verification requirements

**Output:** Worker execution in progress

### Phase 3: Verify Results
**Goal:** Check completion and update state

**Process:**
1. **Check Worker Output**
   - Read execution report
   - Verify task completion
   - Check for errors

2. **If Success:**
   ```bash
   - Mark phase [x] in ROADMAP.md
   - Update task statuses
   - Create phase summary
   - Continue to next phase
   ```

3. **If Failed:**
   ```bash
   - Create HANDOFF.md (using project-lifecycle template)
   - Mark phase [!] in ROADMAP.md
   - Ask user for intervention
   - Pause execution
   ```

**Output:** Updated state and next action

### Phase 4: Continue Flow
**Goal:** Determine next steps

**Process:**
1. **Check Remaining Phases**
   - Read ROADMAP.md
   - Count pending phases

2. **Ask User**
   ```
   Phase complete! Proceed to next phase?

   Option 1: Yes, continue → I'll run /sys-builder:run-plan
   Option 2: No, pause here → I'll stop execution
   Option 3: Review first → I'll show phase summary
   ```

3. **If All Complete**
   ```
   Plan fully executed. All objectives achieved.

   All phases [x] complete
   Summary: {link to final summary}
   ```

**Output:** Next action or completion

## Execution Flow

### State Transitions

```mermaid
graph TD
    A[Pending [ ]] --> B[In Progress [~]]
    B --> C[Complete [x]]
    B --> D[Blocked [!]]
    D --> B
```

**Flow Diagram:**
```
Phase Status: [ ]
    ↓
Phase Status: [~] (executing)
    ↓
Phase Status: [x] or [!]
    ↓
Phase Status: [ ] (next phase) OR Plan Complete
```

### Handoff Flow

```
Execution → Error Detected
    ↓
Create HANDOFF.md
    ↓
Mark Phase [!]
    ↓
Ask User for Intervention
    ↓
User Fixes Issue
    ↓
Restart Execution
    ↓
Mark Phase [~]
    ↓
Continue Execution
```

## Examples

### Example 1: Execute Next Phase
```bash
/sys-builder:run-plan
```
**Flow:**
1. Reads ROADMAP.md
2. Finds first `[ ]` phase
3. Checks dependencies are `[x]`
4. Loads phase plan
5. Spawns worker
6. Verifies results
7. Marks phase `[x]`
8. Asks to continue

### Example 2: Execute Specific Phase
```bash
/sys-builder:run-plan 2
```
**Flow:**
1. Reads ROADMAP.md
2. Finds Phase 2
3. Checks dependencies
4. Loads phase plan
5. Executes tasks
6. Updates state

### Example 3: Resume from Handoff
```bash
/sys-builder:run-plan
```
**Flow:**
1. Reads ROADMAP.md
2. Finds phase with `[!]` status
3. Checks HANDOFF.md
4. Verifies resolution
5. Marks phase `[~]`
6. Resumes execution

## Reference

### File Structure
```
.cattoolkit/plan/{project-slug}/
├── ROADMAP.md         # Phase states
├── BRIEF.md           # Project context
└── phases/
    ├── 01-setup/
    │   ├── 01-01-PLAN.md  # Tasks
    │   ├── HANDOFF.md      # Created when blocked
    │   └── SUMMARY.md     # Created when complete
    └── 02-core/
        └── 02-01-PLAN.md
```

### Skills Used
| Skill | Purpose | When |
|-------|---------|------|
| project-lifecycle | Consolidated execution, state management, and standards | All phases |

### Worker Agent Configuration
```yaml
Agent: @worker
Tools: [Read, Write, Edit, Bash, Glob, Grep]
Skills: [project-lifecycle, software-engineering, execution-core]
Constraint: NON-INTERACTIVE
```

### State Management
**ROADMAP.md Updates:**
- `[ ]` → `[~]` (start phase)
- `[~]` → `[x]` (complete phase)
- `[~]` → `[!]` (block phase)
- `[!]` → `[~]` (resume after handoff)

### Handoff Protocol
**Triggered When:**
- Authentication required (API keys, credentials)
- Merge conflicts
- Dependency errors
- Critical failures
- Ambiguous requirements

**Hand off Format:**
- Use `project-lifecycle` handoff template (see skill assets/templates/handoff.md)
- Include: Reason, What Happened, Actions Required, Verification
- Save in phase directory as `HANDOFF.md`

### Verification Criteria
**Phase Complete When:**
- All tasks marked `[x]`
- Execution report shows success
- Tests passing
- Deliverables produced

**Phase Blocked When:**
- Error encountered
- Worker cannot proceed
- Human intervention required
- HANDOFF.md created

### Error Handling
**If worker fails:**
1. Read execution report
2. Identify error type
3. Create HANDOFF.md
4. Mark phase `[!]`
5. Ask user for help

**If handoff not resolved:**
1. Check resolution status
2. Ask user to resolve
3. Don't proceed until fixed

**If dependencies not met:**
1. Verify ROADMAP.md
2. Check phase dependencies
3. Show which phases must complete first
4. Suggest execution order

### Next Steps After Execution
**Continue Execution:**
```bash
/sys-builder:run-plan
```

**Manage Plan:**
```bash
/sys-builder:manage-plan "show current status"
```

**View Progress:**
```bash
cat .cattoolkit/plan/{project-slug}/ROADMAP.md
```

### Command Shortcuts
```bash
# Execute next phase
/sys-builder:run-plan

# Execute specific phase
/sys-builder:run-plan 2

# Execute all remaining phases
/sys-builder:run-plan all
```

### Limitations
- Cannot execute if dependencies not met
- Cannot proceed through blocked phases
- Requires human intervention for handoffs
- Worker is non-interactive

### Validation
**Before Execution:**
- [ ] ROADMAP.md exists
- [ ] Phase exists and is `[ ]` or `[!]`
- [ ] Dependencies are `[x]`
- [ ] Phase plan exists

**After Execution:**
- [ ] Phase status updated
- [ ] Tasks marked complete
- [ ] Summary created (if complete)
- [ ] Next phase ready (if applicable)
