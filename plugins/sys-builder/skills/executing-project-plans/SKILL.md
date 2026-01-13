---
name: executing-project-plans
description: "Orchestrates plan execution, manages state transitions, and handles verification workflows. PROACTIVELY Use when executing project phases and managing state transitions."
context: fork
allowed-tools: [Task]
---

# Executing Project Plans: Orchestration Layer

## Core Purpose

**Execution Orchestration:** This skill manages the execution of project plans, handles state transitions, and coordinates verification workflows.

It answers: "HOW do we execute the plan?" and "HOW do we manage execution state?"

## Integration Pattern

This skill **orchestrates**:
- Worker agent execution
- State management
- Verification workflows
- Handoff protocols

This skill **uses**:
- `managing-project-plans` for standards and handoff format
- `executing-project-plans` references for methodology
- Worker agent for actual code execution

## State Management

### State Model

**Plan State:**
```markdown
Global State (ROADMAP.md):
- [ ] = Pending
- [~] = In Progress
- [x] = Complete
- [!] = Blocked

Phase State (Phase Plan):
- Task Status: [ ] → [~] → [x]
- Handoff: Created when blocked
- Summary: Created when complete
```

**State Transitions:**
```
[ ] (Pending) → [~] (In Progress)
    ↓
[x] (Complete) OR [!] (Blocked)
    ↓
Next Phase OR Intervention Required
```

### State Management Protocol

**Starting a Phase:**
1. Check ROADMAP.md for phase status
2. Verify dependencies are [x] complete
3. Update phase status [ ] → [~]
4. Read phase plan file
5. Start executing tasks

**Completing a Task:**
1. Execute task (via Worker agent)
2. Verify task completion
3. Update task status [~] → [x]
4. Check if phase complete
5. If complete: Update ROADMAP.md [~] → [x]
6. Create phase summary

**Handling Blockers:**
1. Identify blocker
2. Create HANDOFF.md (using managing-project-plans template)
3. Update phase status [~] → [!]
4. Pause execution
5. Resume after intervention

## Execution Orchestration

### Worker Agent Orchestration

**Protocol:**

1. **Prepare Context**
   ```markdown
   Phase plan content
   + BRIEF.md context
   + Current state
   = Full execution context
   ```

2. **Dispatch to Worker**
   ```markdown
   Task: {Full context}
   Agent: Worker
   Constraint: Non-interactive execution
   Tools: [Read, Write, Edit, Bash, Glob, Grep]
   Skills: [managing-project-plans, software-engineering, execution-core]
   ```

3. **Monitor Execution**
   - Check for completion
   - Monitor for errors
   - Detect handoff creation
   - Verify state updates

4. **Handle Completion**
   - Read execution report
   - Verify task completion
   - Update state
   - Continue or pause

### Task Execution Loop

**For Each Task:**

```markdown
Step 1: Execute
- Dispatch to worker
- Pass full context
- Monitor execution

Step 2: Verify
- Check execution report
- Run verification commands
- Confirm success criteria

Step 3: Update State
- Mark task [x] complete
- Update progress metrics
- Check phase completion

Step 4: Continue
- Next task OR
- Phase complete OR
- Handoff required
```

## Verification Workflows

### Verification Levels

**Level 1: Task Verification**
```markdown
Task: {description}
Verification: {how to verify}

Verification Method:
- Read execution output
- Check files created/modified
- Run tests
- Validate against success criteria
```

**Level 2: Phase Verification**
```markdown
Phase: {name}
Verification: Comprehensive check

Verification Method:
- All tasks [x] complete
- Success criteria met
- Tests passing
- Documentation updated
```

**Level 3: Plan Verification**
```markdown
Plan: {project-name}
Verification: End-to-end validation

Verification Method:
- All phases [x] complete
- Deliverables produced
- Success criteria met
- System functional
```

### Self-Verification Pattern

**Automated Verification:**

```python
def verify_task_completion(task, execution_report):
    """Verify task was completed successfully"""

    # Check 1: Expected files created
    expected_files = task.get('expected_files', [])
    for file in expected_files:
        assert os.path.exists(file), f"Expected file {file} not found"

    # Check 2: Tests passing
    if task.get('run_tests'):
        result = run_command('npm test')
        assert result.returncode == 0, "Tests failed"

    # Check 3: Success criteria
    success_criteria = task.get('success_criteria', [])
    for criteria in success_criteria:
        assert verify_criteria(criteria), f"Criteria not met: {criteria}"

    return True
```

**Verification Checklist:**

```markdown
For Each Task:
- [ ] Files created as expected
- [ ] Code changes applied correctly
- [ ] Tests passing
- [ ] Success criteria met
- [ ] No errors in execution
- [ ] State updated correctly

For Each Phase:
- [ ] All tasks complete
- [ ] Phase summary created
- [ ] ROADMAP.md updated
- [ ] Next phase ready

For Plan:
- [ ] All phases complete
- [ ] Deliverables produced
- [ ] Final verification passed
- [ ] Success criteria met
```

## Handoff Protocols

### Handoff Triggers

**When to Create Handoff:**

1. **Authentication Gate**
   - API keys needed
   - Credentials required
   - Service access blocked

2. **Dependency Missing**
   - External service down
   - Library not available
   - Environment not configured

3. **Conflict**
   - Merge conflicts
   - Dependency conflicts
   - Version conflicts

4. **Ambiguity**
   - Unclear requirements
   - Missing information
   - Decision needed

5. **Critical Error**
   - Build failure
   - Test failure
   - System error

### Handoff Format

**Using Managing-Project-Plans Template:**

```markdown
# HANDOFF Required

**Reason:** {AUTH_GATE | CONFLICT | AMBIGUOUS | DEPENDENCY | ERROR}

**Date:** {YYYY-MM-DD}
**Phase:** {XX - phase-name}
**Task:** {task-name}

## What Happened
{Detailed description of the blocker}

## Current State
- **Completed Tasks:**
  - [x] {task 1}
  - [x] {task 2}

- **In Progress:**
  - [~] {task N}

- **Blocked On:**
  - {Specific blocker}

## What You Need to Do
1. {Action 1}
2. {Action 2}
3. {Action 3}

## Verification
{How to confirm the fix}

## Next Steps
After resolving the issue:
1. Restart execution
2. Verify blocker resolved
3. Continue with remaining tasks

## Context
{Additional context that might be helpful}
```

## Error Handling

### Error Categories

**1. Execution Errors**
```markdown
Type: Code errors, build failures, test failures
Handling:
- Log error details
- Attempt recovery
- If unrecoverable: Create handoff
```

**2. State Errors**
```markdown
Type: Inconsistent state, corrupted files
Handling:
- Validate state integrity
- Attempt repair
- If unrepairable: Create handoff
```

**3. Dependency Errors**
```markdown
Type: Missing dependencies, version conflicts
Handling:
- Check dependency status
- Attempt resolution
- If unresolvable: Create handoff
```

**4. Resource Errors**
```markdown
Type: Out of memory, disk full, timeout
Handling:
- Check resource status
- Attempt cleanup
- If persistent: Create handoff
```

### Error Recovery Strategy

**Level 1: Automatic Recovery**
```markdown
Action: Attempt fix automatically
Examples:
- Retry failed command
- Clear cache
- Restart service
- Update dependency
```

**Level 2: Partial Recovery**
```markdown
Action: Adjust execution, continue
Examples:
- Skip non-critical task
- Use alternative approach
- Reduce scope temporarily
```

**Level 3: Handoff Required**
```markdown
Action: Create handoff, pause
Examples:
- Authentication needed
- Critical error
- Unresolvable conflict
- Decision required
```

## Execution Monitoring

### Progress Tracking

**Phase Progress:**
```markdown
Phase: {name} [~]
Progress: {X}/{Y} tasks complete

Completed:
- [x] Task 1 (completed at {time})
- [x] Task 2 (completed at {time})

In Progress:
- [~] Task 3 (started at {time})

Remaining:
- [ ] Task 4
- [ ] Task 5
```

**Plan Progress:**
```markdown
Plan: {project-name}
Overall: {X}/{Y} phases complete

Phases:
[x] Phase 1: Foundation (completed)
[x] Phase 2: Core (completed)
[~] Phase 3: Enhancement (in progress)
[ ] Phase 4: Polish (pending)

ETA: {estimated completion time}
```

### Execution Metrics

**Key Metrics:**

1. **Time Metrics**
   - Task duration
   - Phase duration
   - Plan duration
   - Blocked time

2. **Quality Metrics**
   - Test pass rate
   - Success criteria met
   - Rework count
   - Error rate

3. **Efficiency Metrics**
   - Tasks per hour
   - Success without handoff
   - Automatic recovery rate

## Quick Reference

### 1. State Management
How to track progress and handle transitions.
- **State Management**: [references/state-management.md](references/state-management.md)

### 2. Execution & Orchestration
How to dispatch tasks to workers.
- **Handoff Protocols**: [references/handoff-protocols.md](references/handoff-protocols.md)

### 3. Verification
How to verify success at Task, Phase, and Plan levels.
- **Verification Workflows**: [references/verification-workflows.md](references/verification-workflows.md)

### 4. Handoffs
How to handle blockers and transfer context.
- **Template**: [assets/handoff-template.md](assets/handoff-template.md)
- **Protocols**: [references/handoff-protocols.md](references/handoff-protocols.md)

## Execution Checklist (Summary)

**Phase Start:**
- [ ] Check ROADMAP.md & Dependencies
- [ ] Update status [ ] → [~]

**Task Execution:**
- [ ] Dispatch to worker (Non-interactive)
- [ ] Monitor & Verify

**Phase Complete:**
- [ ] All tasks [x]
- [ ] Create summary & Update ROADMAP.md

**Handoff Required:**
- [ ] Identify blocker & Create HANDOFF.md
- [ ] Pause execution
