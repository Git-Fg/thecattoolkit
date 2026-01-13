# Test: manage-plan - Haiku Tier

## Test Case 1: View Current Status
**Input**: `/sys-builder:manage-plan "show current status"`
**Expected Output**: Current plan status displayed
**Success Criteria**:
- [ ] ROADMAP.md contents displayed
- [ ] Phase status table shown
- [ ] Progress metrics displayed
- [ ] Active phase identified
- [ ] No modifications to files

## Test Case 2: Mark Task Complete
**Input**: `/sys-builder:manage-plan "mark task 1 in phase 2 as complete"`
**Expected Output**: Task marked complete in phase plan
**Success Criteria**:
- [ ] Task 1 status changes to [x]
- [ ] Phase 2 plan file updated
- [ ] No changes to ROADMAP.md
- [ ] Task description preserved
- [ ] File formatting maintained

## Test Case 3: Mark Phase Complete
**Input**: `/sys-builder:manage-plan "mark phase 1 complete"`
**Expected Output**: Phase marked complete
**Success Criteria**:
- [ ] Phase 1 status in ROADMAP.md: [ ] → [x]
- [ ] Phase summary created
- [ ] All tasks in phase marked [x]
- [ ] Dependencies verified
- [ ] Next phase ready to execute

## Test Case 4: Add New Task
**Input**: `/sys-builder:manage-plan "add task to phase 2"`
**Expected Output**: New task added to phase plan
**Success Criteria**:
- [ ] New task appears in phase plan
- [ ] Task follows naming convention
- [ ] Status set to [ ]
- [ ] Task numbered correctly
- [ ] File formatting preserved

## Test Case 5: Resume from Handoff
**Input**: `/sys-builder:manage-plan "resume from phase 3"`
**Expected Output**: Phase resumed from blocked state
**Success Criteria**:
- [ ] Phase 3 status: [!] → [~]
- [ ] HANDOFF.md reviewed
- [ ] Resolution verified
- [ ] Phase ready to execute
- [ ] State consistency maintained
