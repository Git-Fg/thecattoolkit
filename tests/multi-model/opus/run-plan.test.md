# Test: run-plan - Opus Tier

## Test Case 1: Cross-Phase Dependency Management
**Input**: Execute Phase 3 with dependencies on Phases 1 and 2
**Expected Output**: Complex dependency resolution
**Success Criteria**:
- [ ] Verifies both Phase 1 and 2 are [x]
- [ ] Detects if only one dependency complete
- [ ] Blocks execution until all dependencies [x]
- [ ] Provides clear dependency status
- [ ] Suggests execution order
- [ ] No premature execution
- [ ] State consistency across phases

## Test Case 2: Critical System Rollback
**Input**: Execute phase on production system, encounter critical error
**Expected Output**: Immediate rollback and handoff
**Success Criteria**:
- [ ] Critical error detected immediately
- [ ] Automatic rollback initiated
- [ ] System state restored
- [ ] HANDOFF.md created with CRITICAL priority
- [ ] All actions documented
- [ ] No data loss
- [ ] Service restoration verified
- [ ] Escalation procedures triggered

## Test Case 3: Parallel Multi-Service Deployment
**Input**: Deploy 5 microservices simultaneously
**Expected Output**: Coordinated parallel deployment
**Success Criteria**:
- [ ] Service dependencies mapped
- [ ] Independent services deploy in parallel
- [ ] Dependent services wait and deploy sequentially
- [ ] Health checks pass for each service
- [ ] Integration points verified
- [ ] Rollback strategy per service
- [ ] Monitoring validates all services
- [ ] Circuit breaker patterns tested

## Test Case 4: Data Migration with Integrity Validation
**Input**: Execute 10M record migration phase
**Expected Output**: Data migrated with verification
**Success Criteria**:
- [ ] Batch migration process
- [ ] Integrity checks at each batch
- [ ] Performance metrics tracked
- [ ] Error handling for bad records
- [ ] Rollback capability maintained
- [ ] Migration progress logged
- [ ] Validation queries pass
- [ ] Zero data loss verified
- [ ] Downtime minimized

## Test Case 5: Handoff Resolution and Recovery
**Input**: 3 phases blocked, resolve in correct order
**Expected Output**: All phases successfully unblocked and completed
**Success Criteria**:
- [ ] HANDOFF.md created for each blocked phase
- [ ] Dependency graph of handoffs analyzed
- [ ] Resolution order determined
- [ ] Each handoff resolved in sequence
- [ ] State consistency maintained
- [ ] No orphaned blocked states
- [ ] All phases complete successfully
- [ ] Recovery process documented
- [ ] Lessons learned captured
