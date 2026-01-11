# Code Review Workflow

## Phase 1: Security Scan (OWASP)
1. **Input Validation**
   - All user inputs validated
   - No injection vulnerabilities (SQL, NoSQL, OS command)
   - Proper sanitization

2. **Authentication & Authorization**
   - Auth checks on sensitive endpoints
   - Proper access control
   - No broken authentication patterns

3. **Data Protection**
   - No hardcoded secrets
   - Proper encryption
   - Secure data transmission

## Phase 2: Logic Verification
1. **Correctness**
   - Logic handles edge cases
   - No obvious bugs or race conditions
   - Error handling is comprehensive

2. **Edge Cases**
   - Null/undefined handling
   - Boundary conditions
   - Error scenarios

## Phase 3: Performance Check
1. **Efficiency**
   - No obvious performance bottlenecks
   - Appropriate data structures
   - Efficient algorithms

2. **Resource Usage**
   - No memory leaks
   - Proper cleanup
   - Appropriate resource management

## Phase 4: Report Findings by Severity

### Critical
- Security vulnerabilities
- Data loss risks
- System crashes

### High
- Significant bugs
- Performance issues
- Maintainability concerns

### Medium
- Code quality issues
- Minor bugs
- Improvement suggestions

### Low
- Style preferences
- Documentation
- Minor optimizations

## Integration with Security Standards
Refer to `references/core-engineering.md` for the complete OWASP Top 10 security checklist to use during code review.
