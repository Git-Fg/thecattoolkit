# Test: run-plan - Sonnet Tier

## Test Case 1: Multi-Phase Execution with Dependencies
**Input**: Execute Phase 2 of a 4-phase plan
**Expected Output**: Dependencies verified, phase executed
**Success Criteria**:
- [ ] Verifies Phase 1 is [x] complete
- [ ] Executes Phase 2 tasks in order
- [ ] Each task verified before next starts
- [ ] Phase 2 marked [x] on completion
- [ ] Phase 3 ready to execute
- [ ] No parallel execution of dependent tasks

## Test Case 2: Handoff Creation and Resolution
**Input**: Create blocker, execute, resolve handoff, resume
**Expected Output**: Full handoff workflow completed
**Success Criteria**:
- [ ] HANDOFF.md created with proper format
- [ ] Phase marked [!] blocked
- [ ] Reason and actions documented
- [ ] User intervention captured
- [ ] Resolution verified
- [ ] Phase resumed [~]
- [ ] Execution completed [x]

## Test Case 3: Error Recovery
**Input**: Execute phase with recoverable error
**Expected Output**: Automatic recovery attempted
**Success Criteria**:
- [ ] Error detected and logged
- [ ] Automatic recovery attempted
- [ ] Recovery strategy applied
- [ ] If successful: continue execution
- [ ] If failed: create HANDOFF.md
- [ ] Error context preserved
- [ ] State consistency maintained

## Test Case 4: Worker Agent Orchestration
**Input**: Execute complex phase requiring code changes
**Expected Output**: Worker executes with proper context
**Success Criteria**:
- [ ] Full phase plan passed to worker
- [ ] BRIEF.md context included
- [ ] Current state information available
- [ ] Worker has required tools
- [ ] Execution monitored
- [ ] Results verified
- [ ] State updated correctly

## Test Case 5: Parallel Task Execution
**Input**: Execute phase with independent tasks
**Expected Output**: Tasks execute in parallel when possible
**Success Criteria**:
- [ ] Independent tasks identified
- [ ] Parallel execution initiated
- [ ] All tasks complete successfully
- [ ] No race conditions
- [ ] Results merged correctly
- [ ] Phase marked complete
- [ ] Performance improved vs sequential
