# Test: manage-plan - Opus Tier

## Test Case 1: Complex Dependency Graph Modification
**Input**: `/sys-builder:manage-plan "reorganize phase dependencies for 10-phase plan"`
**Expected Output**: Dependency graph restructured
**Success Criteria**:
- [ ] All 10 phases analyzed
- [ ] Dependency relationships mapped
- [ ] Circular dependencies detected and removed
- [ ] New dependency order optimized
- [ ] ROADMAP.md updated with new structure
- [ ] Execution sequence validated
- [ ] No orphaned phases
- [ ] Critical path identified

## Test Case 2: Emergency Phase Injection
**Input**: `/sys-builder:manage-plan "insert security audit phase before deployment"`
**Expected Output**: Security phase inserted with proper dependencies
**Success Criteria**:
- [ ] New security phase created
- [ ] Positioned before deployment phase
- [ ] Dependencies adjusted correctly
- [ ] Deployment phase now depends on security
- [ ] No circular dependencies
- [ ] Critical path updated
- [ ] Timeline impact assessed
- [ ] Blocking relationships maintained

## Test Case 3: Bulk Handoff Creation
**Input**: `/sys-builder:manage-plan "create handoff for all blocked phases"`
**Expected Output**: HANDOFF.md for each blocked phase
**Success Criteria**:
- [ ] Identifies all [!] phases
- [ ] HANDOFF.md created for each
- [ ] Unique handoff per phase
- [ ] Each handoff properly formatted
- [ ] Dependencies between handoffs documented
- [ ] Resolution order specified
- [ ] Context preserved per phase
- [ ] Recovery strategy defined

## Test Case 4: State Reconstruction
**Input**: `/sys-builder:manage-plan "recover corrupted plan state"`
**Expected Output**: Plan state restored and consistent
**Success Criteria**:
- [ ] Corrupted state detected
- [ ] Backup state located
- [ ] Integrity checks performed
- [ ] Missing files recreated
- [ ] Inconsistent status codes fixed
- [ ] Dependencies re-validated
- [ ] Execution history preserved
- [ ] Clean state achieved

## Test Case 5: Multi-Plan Management
**Input**: `/sys-builder:manage-plan "show status for all active plans"`
**Expected Output**: Aggregate status across multiple plans
**Success Criteria**:
- [ ] All plans in .cattoolkit/plan/ scanned
- [ ] Status aggregated per plan
- [ ] Cross-plan dependencies identified
- [ ] Resource conflicts detected
- [ ] Execution priorities set
- [ ] Parallel execution opportunities noted
- [ ] Summary report generated
- [ ] Action items per plan
