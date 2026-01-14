# State Management

## Overview

State Management in executing-project-plans handles the lifecycle of plan execution, from initiation to completion.

## State Model

### Hierarchical State Structure

```
Plan State (ROADMAP.md)
├── Phase 01 State
│   ├── Task 1 State
│   ├── Task 2 State
│   └── Task N State
├── Phase 02 State
└── Phase N State
```

### State Codes

**Global State (Phases):**
- `[ ]` = Pending - Not started, waiting for dependencies
- `[~]` = In Progress - Currently executing
- `[x]` = Complete - Finished successfully
- `[!]` = Blocked - Needs intervention

**Task State:**
- `[ ]` = Pending - Not started
- `[~]` = In Progress - Currently executing
- `[x]` = Complete - Finished successfully
- `[!]` = Blocked - Needs intervention

## State Transitions

### Valid Transitions

#### Phase Transitions

```mermaid
graph TD
    A[Pending [ ]] --> B[In Progress [~]]
    B --> C[Complete [x]]
    B --> D[Blocked [!]]
    D --> B
```

**Rules:**
- `[ ]` → `[~]`: Start phase when dependencies complete
- `[~]` → `[x]`: Complete phase when all tasks finish
- `[~]` → `[!]`: Block when handoff required
- `[!]` → `[~]`: Resume after handoff resolved

#### Task Transitions

```mermaid
graph TD
    A[Pending [ ]] --> B[In Progress [~]]
    B --> C[Complete [x]]
    B --> D[Blocked [!]]
    D --> B
```

**Rules:**
- `[ ]` → `[~]`: Start task
- `[~]` → `[x]`: Complete task successfully
- `[~]` → `[!]`: Block when handoff required
- `[!]` → `[~]`: Resume after handoff resolved

### Invalid Transitions

**Cannot:**
- `[ ]` → `[x]` (skip without execution)
- `[x]` → `[~]` (reopen completed phase)
- `[~]` → `[~]` (already in progress)
- `[!]` → `[x]` (complete without resolving block)

## State Management Operations

### Operation 1: Start Phase

**Preconditions:**
- Phase status is `[ ]`
- All dependencies are `[x]`
- Phase plan file exists

**Steps:**
```markdown
1. Read ROADMAP.md
2. Verify dependencies
3. Update phase status [ ] → [~]
4. Read phase plan file
5. Prepare execution context
6. Begin task execution
```

**Implementation:**
```python
def start_phase(phase_id):
    """Start executing a phase"""

    # Load ROADMAP
    roadmap = read_roadmap()

    # Verify phase exists and pending
    phase = roadmap.get_phase(phase_id)
    assert phase.status == '[ ]', f"Phase {phase_id} not pending"

    # Verify dependencies
    for dep in phase.dependencies:
        dep_phase = roadmap.get_phase(dep)
        assert dep_phase.status == '[x]', f"Dependency {dep} not complete"

    # Update status
    phase.status = '[~]'
    write_roadmap(roadmap)

    # Prepare context
    context = prepare_phase_context(phase_id)

    return context
```

### Operation 2: Complete Task

**Preconditions:**
- Task status is `[~]`
- Task execution completed
- Verification passed

**Steps:**
```markdown
1. Read execution report
2. Verify task completion
3. Update task status [~] → [x]
4. Check if phase complete
5. If complete: Mark phase [x] and create summary
6. If incomplete: Continue to next task
```

**Implementation:**
```python
def complete_task(phase_id, task_id, execution_report):
    """Mark task as complete"""

    # Verify completion
    verify_task_completion(task_id, execution_report)

    # Update task status
    phase_plan = read_phase_plan(phase_id)
    task = phase_plan.get_task(task_id)
    task.status = '[x]'
    write_phase_plan(phase_plan, phase_id)

    # Check if phase complete
    if phase_plan.all_tasks_complete():
        complete_phase(phase_id)

    return True
```

### Operation 3: Block Phase

**Preconditions:**
- Phase status is `[~]`
- Blocker identified
- Handoff document created

**Steps:**
```markdown
1. Identify blocker
2. Create HANDOFF.md (using managing-project-plans template)
3. Update phase status [~] → [!]
4. Save execution state
5. Pause execution
```

**Implementation:**
```python
def block_phase(phase_id, blocker_type, description):
    """Create handoff and block phase"""

    # Create handoff document
    handoff = create_handoff(
        phase_id=phase_id,
        blocker_type=blocker_type,
        description=description
    )

    # Update phase status
    roadmap = read_roadmap()
    phase = roadmap.get_phase(phase_id)
    phase.status = '[!]'
    write_roadmap(roadmap)

    # Save state for resume
    save_execution_state(phase_id)

    return handoff
```

### Operation 4: Resume Phase

**Preconditions:**
- Phase status is `[!]`
- Handoff resolved
- User confirms resume

**Steps:**
```markdown
1. Verify handoff resolved
2. Read saved execution state
3. Update phase status [!] → [~]
4. Continue execution
```

**Implementation:**
```python
def resume_phase(phase_id):
    """Resume blocked phase"""

    # Verify handoff resolved
    assert verify_handoff_resolved(phase_id), "Handoff not resolved"

    # Load saved state
    state = load_execution_state(phase_id)

    # Update status
    roadmap = read_roadmap()
    phase = roadmap.get_phase(phase_id)
    phase.status = '[~]'
    write_roadmap(roadmap)

    # Continue execution
    return state
```

## State Persistence

### Persistence Strategy

**File-Based State:**

```
.cattoolkit/plan/{project-slug}/
├── BRIEF.md          # Project definition (static)
├── ROADMAP.md        # Phase states (changes frequently)
├── DISCOVERY.md      # Discovery findings (static)
├── phases/
│   ├── 01-setup/
│   │   ├── 01-01-PLAN.md  # Task states (changes frequently)
│   │   ├── HANDOFF.md     # Created when blocked (temporary)
│   │   └── SUMMARY.md     # Created when complete (static)
```

**State Snapshot:**

```python
def save_execution_state(phase_id):
    """Save current execution state"""

    state = {
        'phase_id': phase_id,
        'timestamp': datetime.now().isoformat(),
        'completed_tasks': get_completed_tasks(phase_id),
        'in_progress_task': get_in_progress_task(phase_id),
        'execution_context': get_execution_context(phase_id)
    }

    state_file = f"phases/{phase_id}/STATE.json"
    write_json(state_file, state)

    return state
```

### Recovery Protocol

**After Interruption:**

```markdown
1. Check for incomplete phases
2. Load saved state
3. Verify handoff status
4. Resume or recreate context
5. Continue execution
```

**Implementation:**
```python
def recover_execution(plan_dir):
    """Recover from interruption"""

    # Check ROADMAP.md
    roadmap = read_roadmap(plan_dir)

    # Find in-progress phases
    in_progress = roadmap.get_in_progress_phases()

    for phase in in_progress:
        # Load state
        state = load_execution_state(phase.id)

        # Check handoff
        if phase.status == '[!]':
            # Wait for handoff resolution
            continue

        # Resume phase
        resume_phase(phase.id)

    return in_progress
```

## State Validation

### Validation Rules

**1. Consistency Check**
```markdown
Rule: Task completion implies phase completion
Check: If all tasks [x], phase must be [x]
```

**2. Dependency Check**
```markdown
Rule: Phase N depends on N-1 being [x]
Check: Cannot start phase if dependencies not [x]
```

**3. Handoff Check**
```markdown
Rule: Handoff file exists iff phase is [!]
Check: [status] implies existence of HANDOFF.md
```

### Validation Implementation

```python
def validate_plan_state(plan_dir):
    """Validate plan state consistency"""

    roadmap = read_roadmap(plan_dir)

    # Check 1: Task-Phase consistency
    for phase in roadmap.phases:
        phase_plan = read_phase_plan(phase.id)
        if phase_plan.all_tasks_complete():
            assert phase.status == '[x]', \
                f"Phase {phase.id} complete but status is {phase.status}"

    # Check 2: Dependency consistency
    for phase in roadmap.phases:
        for dep in phase.dependencies:
            dep_phase = roadmap.get_phase(dep)
            assert dep_phase.status == '[x]', \
                f"Phase {phase.id} depends on incomplete {dep}"

    # Check 3: Handoff consistency
    for phase in roadmap.phases:
        handoff_path = f"phases/{phase.id}/HANDOFF.md"
        if phase.status == '[!]':
            assert os.path.exists(handoff_path), \
                f"Phase {phase.id} blocked but no HANDOFF.md"

    return True
```

## State Visualization

### Progress Dashboard

**ROADMAP.md as Dashboard:**

```markdown
# Roadmap: {project-name}

## Phases

| Phase | Name | Status | Progress | ETA |
|-------|------|--------|----------|-----|
| 01 | Foundation | [x] | 100% | ✓ |
| 02 | Core Features | [~] | 66% | 2h |
| 03 | Enhancement | [ ] | 0% | 4h |
| 04 | Polish | [ ] | 0% | 1h |

## Progress
**Overall:** 2/4 phases complete (50%)
**Current:** Phase 02 in progress
**Next:** Phase 03 (waiting for 02)
```

### Visual Indicators

```markdown
Status Icons:
[ ] Pending (not started)
[~] In Progress (executing)
[x] Complete (finished successfully)
[!] Blocked (needs intervention)
```

## State Management Checklist

### Phase Lifecycle

- [ ] Phase started (status [ ] → [~])
- [ ] Tasks executing (status updates)
- [ ] Tasks completed (status [~] → [x])
- [ ] Phase completed (status [~] → [x])
- [ ] Summary created
- [ ] Next phase ready

### Handoff Lifecycle

- [ ] Blocker identified
- [ ] Handoff created (status [~] → [!])
- [ ] State saved
- [ ] Resolution applied
- [ ] Handoff verified resolved
- [ ] Phase resumed (status [!] → [~])

### Recovery Lifecycle

- [ ] Interruption detected
- [ ] State recovered
- [ ] Handoff status checked
- [ ] Execution resumed or paused
- [ ] Progress continued
