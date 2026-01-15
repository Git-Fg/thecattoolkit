# Plan Execution Workflow

## Core Purpose

Drives execution of project phases using state-based plan management and worker agent dispatch.

## State Model

```markdown
- [ ] = Pending
- [~] = In Progress
- [x] = Complete
- [!] = Blocked
```

## Phase 1: Read State

**Goal:** Identify what to execute

**Process:**
1. **Read ROADMAP.md**
2. **Identify Phase**
   - If argument provided: Use specified phase number
   - If no argument: Find first `[ ]` (pending) phase
   - Check dependencies are `[x]` complete
3. **Load Phase Plan**
4. **Check for Handoff** - Look for existing HANDOFF.md

**Output:** Phase plan and execution context

## Phase 2: Dispatch to Worker

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
   Task: @executor
   Tools: [Read, Write, Edit, Bash, Glob, Grep]
   Skills: [managing-plans, software-engineering, executing-tasks]
   Constraint: NON-INTERACTIVE (no AskUserQuestion)
   ```

3. **Pass Phase Plan**
   - Include ENTIRE phase file content
   - Include task details
   - Include success criteria
   - Include verification requirements

**Output:** Worker execution in progress

## Phase 3: Verify Results

**Goal:** Check completion and update state

**Process:**
1. **Check Worker Output**
   - Read execution report
   - Verify task completion
   - Check for errors

2. **If Success:**
   - Mark phase [x] in ROADMAP.md
   - Update task statuses
   - Create phase summary
   - Continue to next phase

3. **If Failed:**
   - Create HANDOFF.md using `managing-plans` template
   - Mark phase [!] in ROADMAP.md
   - Ask user for intervention
   - Pause execution

**Output:** Updated state and next action

## Phase 4: Continue Flow

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

## Execution Flow Diagram

```
Phase Status: [ ]
    ↓
Phase Status: [~] (executing)
    ↓
Phase Status: [x] or [!]
    ↓
Phase Status: [ ] (next phase) OR Plan Complete
```

## Handoff Flow

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

## Handoff Protocol

**Triggered When:**
- Authentication required (API keys, credentials)
- Merge conflicts
- Dependency errors
- Critical failures
- Ambiguous requirements

**Handoff Format:**
- Use `managing-plans` handoff template
- Include: Reason, What Happened, Actions Required, Verification
- Save in phase directory as `HANDOFF.md`

## Verification Criteria

**Phase Complete When:**
- All tasks marked [x]
- Execution report shows success
- Tests passing
- Deliverables produced

**Phase Blocked When:**
- Error encountered
- Worker cannot proceed
- Human intervention required
- HANDOFF.md created
