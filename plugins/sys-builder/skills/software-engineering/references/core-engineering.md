# Core Engineering Standards

## Universal Standards

### Security (OWASP Top 10)
- **Injection Prevention**: All user inputs validated/sanitized
- **Authentication**: Auth checks on sensitive endpoints
- **Access Control**: Authorization on every protected resource
- **Cryptography**: No hardcoded passwords or keys
- **Input Validation**: All entry points validated
- **Error Handling**: Errors don't expose sensitive information
- **Dependencies**: No vulnerable/outdated components

### Testing Standards
- No code without tests
- Edge cases covered
- Test quality and assertions correct

### State Persistence
- Persist decisions to `.cattoolkit/context/scratchpad.md`

## Test-Driven Development (TDD)

### Three Laws of TDD
1. **First Law**: You may not write production code until you have written a failing test.
2. **Second Law**: You may not write more of a test than is sufficient to fail, and not compiling is failing.
3. **Third Law**: You may not write more production code than is sufficient to pass the currently failing test.

### Red-Green-Refactor Cycle

#### Red (Fail) - Write failing test first
- Write a test that describes the desired functionality
- Run the test to confirm it fails
- Failures should be compilation errors or assertion failures

#### Green (Pass) - Minimal implementation
- Write the minimal production code to make the test pass
- Focus on making the test green, not on code quality
- Resist the urge to optimize or refactor yet

#### Refactor - Clean up while tests pass
- Improve the code design while maintaining functionality
- Remove duplication
- Improve naming and structure
- All tests must continue to pass

### Test Structure (AAA Pattern)
- **Arrange**: Set up test data and conditions
- **Act**: Execute the code under test
- **Assert**: Verify the results

### Testing Strategy
- **Unit Tests (70%)**: Focus on pure functions and business logic
- **Integration Tests (20%)**: Test interaction between modules
- **E2E Tests (10%)**: Critical user journeys only

## Debugging Workflow

### Phase 1: Capture Trace
1. **Gather Error Information**
   - Full stack trace
   - Error message and context
   - Input that caused the error
   - Expected vs actual behavior

2. **Reproduce the Issue**
   - Create minimal reproduction case
   - Document steps to trigger the bug
   - Verify issue is consistent

### Phase 2: Hypothesize
1. **Root Cause Analysis**
   - Identify the failure point
   - Trace the execution flow backwards
   - Consider multiple hypotheses

2. **Prioritize Hypotheses**
   - Most likely cause first
   - Easiest to test first
   - Eliminate impossible causes

### Phase 3: Test (Repro)
1. **Validate Hypothesis**
   - Run targeted tests
   - Add logging/breakpoints
   - Use scientific method

2. **Iterate**
   - Refine hypothesis based on results
   - Test next most likely cause
   - Continue until root cause found

### Phase 4: Fix & Verify
1. **Implement Fix**
   - Make minimal change to address root cause
   - Document the fix and reasoning

2. **Verify Solution**
   - Test with original reproduction case
   - Run full test suite
   - Check for regressions
   - Add regression test

## Security Checklist (OWASP Top 10)

### A01:2021 - Broken Access Control
- [ ] Authentication required for all sensitive endpoints
- [ ] Authorization checks on every protected resource
- [ ] No direct object references without validation
- [ ] Session management properly implemented
- [ ] Role-based access control (RBAC) enforced

### A02:2021 - Cryptographic Failures
- [ ] Data encrypted in transit (TLS/SSL)
- [ ] Data encrypted at rest
- [ ] Strong encryption algorithms used (AES-256, RSA-2048+)
- [ ] Cryptographic keys properly secured
- [ ] No hardcoded passwords or keys

### A03:2021 - Injection
- [ ] All user inputs parameterized/prepared statements
- [ ] No dynamic SQL queries
- [ ] Input validation on all entry points
- [ ] Output encoding/escaping implemented
- [ ] Command injection prevention (no eval(), exec())

### A04:2021 - Insecure Design
- [ ] Threat modeling completed
- [ ] Security requirements defined
- [ ] Secure architecture patterns followed
- [ ] Defense in depth implemented
- [ ] Security controls fail securely

### A05:2021 - Security Misconfiguration
- [ ] Default accounts/passwords changed
- [ ] Unnecessary features disabled
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Error messages don't expose sensitive info
- [ ] Security updates applied

### A06:2021 - Vulnerable and Outdated Components
- [ ] Dependencies regularly updated
- [ ] Vulnerability scanning implemented
- [ ] No deprecated libraries in use
- [ ] Component versions tracked
- [ ] Security advisories monitored

### A07:2021 - Identification and Authentication Failures
- [ ] Multi-factor authentication (MFA) where appropriate
- [ ] Strong password policies enforced
- [ ] Account lockout after failed attempts
- [ ] Session timeouts implemented
- [ ] No session fixation vulnerabilities

### A08:2021 - Software and Data Integrity Failures
- [ ] Code signed and verified
- [ ] Integrity checks on updates
- [ ] No unsigned/unaltered plugins
- [ ] Secure CI/CD pipeline
- [ ] Dependencies pinned and verified

### A09:2021 - Security Logging and Monitoring Failures
- [ ] Security events logged (auth failures, access attempts)
- [ ] Logs protected from tampering
- [ ] Monitoring/alerting configured
- [ ] Log retention policy defined
- [ ] Regular log review process

### A10:2021 - Server-Side Request Forgery (SSRF)
- [ ] URL validation on external requests
- [ ] Network segmentation implemented
- [ ] Allowlist of approved URLs/domains
- [ ] Response validation implemented
- [ ] Metadata protection enabled

### Input Validation
- [ ] Length limits enforced
- [ ] Type checking implemented
- [ ] Range/format validation
- [ ] Canonicalization performed
- [ ] Reject unexpected input

### Output Security
- [ ] HTML encoding for web output
- [ ] SQL escaping for database
- [ ] Command escaping for shell
- [ ] URL encoding for links
- [ ] JSON/XML encoding
