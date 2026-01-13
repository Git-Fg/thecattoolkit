# Test: manage-plan - Sonnet Tier

## Test Case 1: Modify Dependencies
**Input**: `/sys-builder:manage-plan "add dependency phase 3 on phase 2"`
**Expected Output**: Dependency graph updated
**Success Criteria**:
- [ ] ROADMAP.md updated with new dependency
- [ ] No circular dependencies created
- [ ] Phase 3 blocked until Phase 2 [x]
- [ ] Dependency list validated
- [ ] Execution order adjusted

## Test Case 2: Split Complex Task
**Input**: `/sys-builder:manage-plan "split task 2 in phase 1 into 3 subtasks"`
**Expected Output**: Task broken down into smaller units
**Success Criteria**:
- [ ] Original task removed or marked as parent
- [ ] 3 new subtasks created
- [ ] Each subtask has clear scope
- [ ] Status codes consistent
- [ ] Dependencies maintained
- [ ] Verification criteria for each subtask

## Test Case 3: Bulk Status Update
**Input**: `/sys-builder:manage-plan "mark all tasks in phase 3 as complete"`
**Expected Output**: All tasks in phase marked [x]
**Success Criteria**:
- [ ] Every task in phase 3 updated
- [ ] No tasks missed
- [ ] Phase status auto-updates to [x] if all tasks [x]
- [ ] ROADMAP.md updated accordingly
- [ ] Summary created if needed
- [ ] Next phase unlocked

## Test Case 4: Handoff State Management
**Input**: `/sys-builder:manage-plan "create handoff for phase 2"`
**Expected Output**: HANDOFF.md created with proper format
**Success Criteria**:
- [ ] HANDOFF.md follows template
- [ ] Phase status set to [!]
- [ ] Reason clearly documented
- [ ] Actions required specified
- [ ] Current state recorded
- [ ] Next steps outlined
- [ ] Context preserved

## Test Case 5: Resume Workflow
**Input**: `/sys-builder:manage-plan "resume from phase 2 after resolving blocker"`
**Expected Output**: Phase resumed from blocked state
**Success Criteria**:
- [ ] HANDOFF.md reviewed
- [ ] Resolution verified
- [ ] Phase status: [!] → [~]
- [ ] Blocker removed from state
- [ ] Ready to execute
- [ ] Context restored
- [ ] Execution can continue
