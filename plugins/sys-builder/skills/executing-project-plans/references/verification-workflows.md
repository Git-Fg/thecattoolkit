# Verification Workflows

## Overview

Verification Workflows ensure that tasks, phases, and plans are completed correctly and meet success criteria.

## Verification Levels

### Level 1: Task Verification

**Purpose:** Verify individual tasks are completed correctly

**Scope:**
- Task execution output
- Files created/modified
- Tests passing
- Success criteria met

**Process:**
```markdown
1. Execute task (via Worker agent)
2. Collect execution output
3. Verify against success criteria
4. Check file changes
5. Run verification commands
6. Update task status
```

**Example: Task Verification**

```markdown
Task: Create user registration form
Action: Create React component with validation

Verification Steps:
1. Check component file created: ✓
2. Verify validation logic: ✓
3. Test form submission: ✓
4. Check styling: ✓
5. Validate against success criteria: ✓

Success Criteria:
- Component renders without errors
- Form validates email/password
- Submit button disabled until valid
- Error messages display correctly

Result: ✅ Task Complete
```

**Task Verification Template:**

```markdown
# Task Verification: {task-name}

## Execution Output
```
{raw output from worker agent}
```

## Verification Checks

### File Changes
- [ ] {expected file 1} created/modified
- [ ] {expected file 2} created/modified
- [ ] {expected file 3} created/modified

### Code Quality
- [ ] No syntax errors
- [ ] Linting passes
- [ ] Type checking passes (if applicable)

### Tests
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Test coverage maintained

### Success Criteria
- [ ] {criteria 1}
- [ ] {criteria 2}
- [ ] {criteria 3}

## Result
**Status:** ✅ Complete / ❌ Failed

**Notes:**
{Any observations or issues}
```

### Level 2: Phase Verification

**Purpose:** Verify phase completion and deliverables

**Scope:**
- All tasks complete
- Phase deliverables produced
- Success criteria met
- Documentation updated

**Process:**
```markdown
1. Verify all tasks [x] complete
2. Check phase deliverables
3. Validate against phase objectives
4. Run integration tests
5. Create phase summary
6. Update ROADMAP.md
```

**Phase Verification Checklist:**

```markdown
## Phase Completion Checklist

### Tasks
- [ ] All tasks marked [x]
- [ ] No pending tasks
- [ ] No blocked tasks

### Deliverables
- [ ] {deliverable 1} produced
- [ ] {deliverable 2} produced
- [ ] {deliverable 3} produced

### Quality
- [ ] All tests passing
- [ ] No critical bugs
- [ ] Code review complete (if applicable)
- [ ] Documentation updated

### Success Criteria
- [ ] {phase objective 1}
- [ ] {phase objective 2}
- [ ] {phase objective 3}

### Integration
- [ ] Integrates with previous phases
- [ ] No breaking changes
- [ ] Dependencies satisfied

## Result
**Status:** ✅ Phase Complete / ❌ Phase Incomplete

**Next:** {next phase or action}
```

**Phase Summary Template:**

```markdown
# Phase {XX} Summary: {phase-name}

**Date:** {YYYY-MM-DD}
**Duration:** {X hours}
**Status:** ✅ Complete

## Completed Tasks
- [x] {Task 1} - {description}
- [x] {Task 2} - {description}
- [x] {Task 3} - {description}

## Deliverables
1. **{Deliverable 1}**
   - Location: {path}
   - Description: {what it is}

2. **{Deliverable 2}**
   - Location: {path}
   - Description: {what it is}

## Key Decisions
- **Decision 1:** {what was decided} → {rationale}
- **Decision 2:** {what was decided} → {rationale}

## Challenges Overcome
- **Challenge 1:** {description} → {solution}
- **Challenge 2:** {description} → {solution}

## Quality Metrics
- **Tests:** {X}/{Y} passing ({Z}% coverage)
- **Linting:** ✅ Pass
- **Type Checking:** ✅ Pass
- **Build:** ✅ Success

## Integration Status
- **Previous Phase:** Compatible ✅
- **Next Phase:** Ready to start ✅

## Lessons Learned
- {learning 1}
- {learning 2}

## Next Steps
{What needs to happen next}
```

### Level 3: Plan Verification

**Purpose:** Verify complete plan success

**Scope:**
- All phases complete
- All deliverables produced
- Success criteria met
- System functional end-to-end

**Process:**
```markdown
1. Verify all phases [x] complete
2. Check all deliverables
3. Run end-to-end tests
4. Validate success criteria
5. Create final report
6. Mark plan complete
```

**Plan Verification Checklist:**

```markdown
# Plan Verification: {project-name}

## Phase Completion
- [x] Phase 1: {name} - Complete
- [x] Phase 2: {name} - Complete
- [x] Phase 3: {name} - Complete
- [x] Phase 4: {name} - Complete

## Deliverables
- [x] {deliverable 1}
- [x] {deliverable 2}
- [x] {deliverable 3}

## Success Criteria
### Functional
- [x] {functional criteria 1}
- [x] {functional criteria 2}
- [x] {functional criteria 3}

### Non-Functional
- [x] Performance: {meets requirements}
- [x] Security: {no vulnerabilities}
- [x] Usability: {user-friendly}
- [x] Maintainability: {documented}

## End-to-End Testing
- [x] User journey 1 works
- [x] User journey 2 works
- [x] User journey 3 works

## Quality Assurance
- [x] All tests passing
- [x] No critical bugs
- [x] Documentation complete
- [x] Code review complete

## Deployment
- [x] Build successful
- [x] Deployment ready
- [x] Rollback plan documented

## Final Status
**Overall Status:** ✅ SUCCESS

**Completion Date:** {YYYY-MM-DD}
**Total Duration:** {X days}

## Success Metrics
- **On Time:** ✅ / ❌
- **On Budget:** ✅ / ❌
- **All Requirements Met:** ✅ / ❌
- **Quality Standards Met:** ✅ / ❌
```

## Automated Verification

### Self-Verification Pattern

**Automated Task Verification:**

```python
def verify_task(task, execution_report):
    """Automatically verify task completion"""

    results = {
        'files_created': [],
        'tests_passed': [],
        'criteria_met': [],
        'errors': []
    }

    # Check 1: Expected files
    for expected_file in task.get('expected_files', []):
        if os.path.exists(expected_file):
            results['files_created'].append(expected_file)
        else:
            results['errors'].append(f"Missing file: {expected_file}")

    # Check 2: Tests
    if task.get('run_tests'):
        test_result = run_tests()
        if test_result.success:
            results['tests_passed'].append('All tests')
        else:
            results['errors'].append(f"Tests failed: {test_result.output}")

    # Check 3: Success criteria
    for criteria in task.get('success_criteria', []):
        if verify_criteria(criteria):
            results['criteria_met'].append(criteria)
        else:
            results['errors'].append(f"Criteria not met: {criteria}")

    # Determine result
    success = len(results['errors']) == 0

    return {
        'success': success,
        'results': results,
        'verification_report': format_verification_report(results)
    }
```

**Automated Phase Verification:**

```python
def verify_phase(phase_id):
    """Automatically verify phase completion"""

    phase_plan = read_phase_plan(phase_id)

    # Check all tasks complete
    all_complete = all(
        task.status == '[x]'
        for task in phase_plan.tasks
    )

    if not all_complete:
        return {
            'success': False,
            'reason': 'Not all tasks complete'
        }

    # Verify deliverables
    deliverables_verified = verify_deliverables(
        phase_plan.deliverables
    )

    # Run integration tests
    integration_tests_pass = run_integration_tests()

    # Check phase objectives
    objectives_met = verify_phase_objectives(phase_plan)

    success = (
        deliverables_verified and
        integration_tests_pass and
        objectives_met
    )

    return {
        'success': success,
        'all_tasks_complete': all_complete,
        'deliverables_verified': deliverables_verified,
        'integration_tests_pass': integration_tests_pass,
        'objectives_met': objectives_met
    }
```

### Verification Commands

**Common Verification Commands:**

```bash
# Code Quality
npm run lint          # ESLint
npm run type-check    # TypeScript
npm run format       # Prettier

# Testing
npm test             # Unit tests
npm run test:e2e     # End-to-end tests
npm run test:coverage # Coverage report

# Building
npm run build        # Production build
npm run build:test   # Test build

# Security
npm audit           # Dependency audit
npm run security-scan # Security scan

# Performance
npm run lighthouse   # Performance audit
npm run bundle-analyzer # Bundle size analysis
```

## Verification Reporting

### Verification Report Template

```markdown
# Verification Report: {component-name}

**Date:** {YYYY-MM-DD}
**Level:** {Task/Phase/Plan}
**Status:** ✅ Pass / ❌ Fail

## Summary
{Brief summary of verification results}

## Detailed Results

### Checks Performed
1. {check 1} - ✅ Pass / ❌ Fail
2. {check 2} - ✅ Pass / ❌ Fail
3. {check 3} - ✅ Pass / ❌ Fail

### Metrics
- **Files Created:** {X}/{Y}
- **Tests Passing:** {X}/{Y}
- **Coverage:** {X}%
- **Build Status:** ✅ Success / ❌ Failed

### Issues Found
- {issue 1} - {severity}
- {issue 2} - {severity}

### Recommendations
1. {recommendation 1}
2. {recommendation 2}

## Next Steps
- [ ] {action 1}
- [ ] {action 2}
- [ ] {action 3}
```

### Verification Metrics

**Task Metrics:**
```markdown
- Task completion time
- Verification time
- Number of retries
- Success rate
- Error rate
```

**Phase Metrics:**
```markdown
- Phase duration
- Task completion rate
- Deliverable quality score
- Test pass rate
- Integration success
```

**Plan Metrics:**
```markdown
- Plan completion rate
- Success criteria met
- Overall quality score
- Time to completion
- Budget adherence
```

## Quick Reference

### Verification Checklist

**Every Task:**
- [ ] Execution output captured
- [ ] Files created/modified verified
- [ ] Tests passing
- [ ] Success criteria met
- [ ] Status updated

**Every Phase:**
- [ ] All tasks complete
- [ ] Deliverables produced
- [ ] Integration tests pass
- [ ] Phase summary created
- [ ] ROADMAP.md updated

**Every Plan:**
- [ ] All phases complete
- [ ] All deliverables present
- [ ] End-to-end tests pass
- [ ] Success criteria met
- [ ] Final report created

### Verification Commands

```bash
# Quick verification
npm run lint && npm test && npm run build

# Full verification
npm run lint && npm test && npm run test:e2e && npm audit

# Performance verification
npm run lighthouse && npm run bundle-analyzer
```

### Verification Tools

- **Linting:** ESLint, flake8, black
- **Testing:** Jest, Pytest, Vitest
- **Type Checking:** TypeScript, mypy
- **Security:** npm audit, bandit, semgrep
- **Performance:** Lighthouse, web-vitals
- **Coverage:** Istanbul, coverage.py

## Self-Verification Pattern

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
