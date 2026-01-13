# Test: run-plan - Haiku Tier

## Test Case 1: Execute First Phase
**Input**: `/sys-builder:run-plan 1`
**Expected Output**: Phase 1 executed and marked complete
**Success Criteria**:
- [ ] Phase 1 status changes from [ ] to [x]
- [ ] Tasks in phase 1 marked [x]
- [ ] Phase summary created
- [ ] ROADMAP.md updated correctly
- [ ] No errors during execution

## Test Case 2: Execute Without Arguments
**Input**: `/sys-builder:run-plan`
**Expected Output**: Next pending phase executed
**Success Criteria**:
- [ ] Finds first [ ] phase in ROADMAP.md
- [ ] Verifies dependencies are [x]
- [ ] Executes that phase
- [ ] Updates status correctly
- [ ] Reports next phase to execute

## Test Case 3: Execute Multiple Phases
**Input**: `/sys-builder:run-plan` (run 3 times)
**Expected Output**: Three phases executed sequentially
**Success Criteria**:
- [ ] Phase 1: [ ] → [x]
- [ ] Phase 2: [ ] → [x]
- [ ] Phase 3: [ ] → [x]
- [ ] Each phase dependencies verified
- [ ] Progress tracked correctly

## Test Case 4: Blocked Phase Handling
**Input**: Create phase with blocker, then `/sys-builder:run-plan`
**Expected Output**: Phase marked as blocked with HANDOFF.md
**Success Criteria**:
- [ ] HANDOFF.md created in phase directory
- [ ] Phase status changes to [!]
- [ ] Handoff reason documented
- [ ] Actions required clearly stated
- [ ] Execution pauses until resolution

## Test Case 5: Complete All Phases
**Input**: Execute all phases of a plan
**Expected Output**: Plan fully executed
**Success Criteria**:
- [ ] All phases marked [x]
- [ ] Final summary created
- [ ] ROADMAP.md shows 100% completion
- [ ] Deliverables produced
- [ ] Success criteria met
