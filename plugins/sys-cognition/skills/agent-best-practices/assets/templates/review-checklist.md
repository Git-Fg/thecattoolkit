# Code Review Checklist

## Pre-Review Preparation

### Before You Start
- [ ] I understand the context and purpose of this change
- [ ] I've reviewed the related tickets/PRs
- [ ] I have the necessary context (codebase, domain knowledge)
- [ ] I'm mentally prepared to provide constructive feedback
- [ ] I have allocated sufficient time for a thorough review

---

## 1. Functionality Review

### Core Functionality
- [ ] The code implements the requested feature/fix
- [ ] Logic is correct and handles edge cases
- [ ] Error handling is appropriate
- [ ] No obvious bugs or logic errors
- [ ] Code handles the happy path correctly
- [ ] Code handles error scenarios gracefully

### User Impact
- [ ] User-facing functionality works as expected
- [ ] UI/UX changes improve or maintain usability
- [ ] No regressions in user workflows
- [ ] Accessibility requirements are met
- [ ] Performance is acceptable for users

### Data & State
- [ ] Data flow is correct
- [ ] State management is appropriate
- [ ] No data loss scenarios
- [ ] Race conditions are prevented
- [ ] Concurrent access is handled correctly

---

## 2. Code Quality Review

### Readability
- [ ] Code is self-documenting and easy to understand
- [ ] Variable names are clear and descriptive
- [ ] Function names accurately describe their purpose
- [ ] Class/module names are meaningful
- [ ] Comments clarify intent, not obvious code
- [ ] No commented-out code left behind
- [ ] Code is not overly clever or obscure

### Structure & Design
- [ ] Code follows project conventions and patterns
- [ ] Functions are focused and single-purpose
- [ ] Classes have clear responsibilities (SOLID principles)
- [ ] Code is not duplicated (DRY principle)
- [ ] Abstractions are appropriate and not over-engineered
- [ ] Code is maintainable and extendable

### Complexity
- [ ] Cyclomatic complexity is reasonable (< 10)
- [ ] Functions are not overly long
- [ ] Nesting depth is manageable (< 4 levels)
- [ ] No unnecessary complexity introduced
- [ ] Simple solutions preferred over complex ones

---

## 3. Testing Review

### Test Coverage
- [ ] Unit tests cover new functionality
- [ ] Unit tests cover edge cases
- [ ] Unit tests cover error scenarios
- [ ] Integration tests are present (if needed)
- [ ] E2E tests cover critical user flows (if applicable)
- [ ] Coverage meets project standards

### Test Quality
- [ ] Tests are readable and maintainable
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Tests are independent and can run in any order
- [ ] No test logic complexity (tests should be simple)
- [ ] Test data is appropriate
- [ ] Mocks/stubs are used correctly

### Test Results
- [ ] All tests pass locally
- [ ] Tests verify the right behavior
- [ ] No flaky tests introduced
- [ ] Performance tests pass (if applicable)

---

## 4. Security Review

### Input Validation
- [ ] All user inputs are validated
- [ ] Input validation is done on server side
- [ ] Input sanitization is appropriate
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] File uploads are validated

### Authentication & Authorization
- [ ] Authentication is required where needed
- [ ] Authorization checks are in place
- [ ] Permissions are enforced correctly
- [ ] No privilege escalation possible
- [ ] Sessions/tokens are handled securely

### Data Protection
- [ ] Sensitive data is not logged
- [ ] Sensitive data is encrypted at rest
- [ ] Sensitive data is encrypted in transit
- [ ] API keys, passwords, tokens not in code
- [ ] Environment variables used for secrets
- [ ] PII is handled according to policy

### Security Best Practices
- [ ] HTTPS used everywhere
- [ ] Security headers are set correctly
- [ ] Dependencies are up to date
- [ ] No known vulnerabilities in dependencies
- [ ] CSRF protection is in place
- [ ] Rate limiting is implemented (if needed)

---

## 5. Performance Review

### Runtime Performance
- [ ] No obvious performance bottlenecks
- [ ] Database queries are optimized
- [ ] N+1 query problems are avoided
- [ ] Caching is used appropriately
- [ ] Expensive operations are minimized
- [ ] Lazy loading is used where appropriate

### Resource Usage
- [ ] Memory usage is reasonable
- [ ] No memory leaks
- [ ] Large data structures are handled efficiently
- [ ] Streaming is used for large files
- [ ] Connections are properly managed

### Scalability
- [ ] Code will scale with increased load
- [ ] Database queries are efficient at scale
- [ ] External API calls have timeouts
- [ ] Rate limiting prevents abuse
- [ ] Horizontal scaling is possible

---

## 6. Dependencies Review

### New Dependencies
- [ ] New dependencies are necessary
- [ ] Dependencies have good maintenance history
- [ ] Dependencies don't introduce bloat
- [ ] License is compatible with project
- [ ] Dependencies are up to date
- [ ] Alternative dependencies were considered

### Dependency Usage
- [ ] Dependencies are used correctly
- [ ] No unnecessary features from dependencies imported
- [ ] Version constraints are appropriate
- [ ] Security vulnerabilities checked
- [ ] Dependency tree is reasonable

---

## 7. Documentation Review

### Code Documentation
- [ ] Public APIs are documented
- [ ] Complex logic has inline comments
- [ ] TODO/FIXME comments are addressed
- [ ] JSDoc/docstrings are accurate
- [ ] Comments explain why, not what

### Project Documentation
- [ ] README is updated (if needed)
- [ ] API documentation is updated
- [ ] Architecture docs are updated
- [ ] Deployment docs are current
- [ ] Changelog is updated

### User Documentation
- [ ] User guides are updated
- [ ] Migration guide is provided (if breaking change)
- [ ] Examples are included
- [ ] Breaking changes are documented

---

## 8. Integration Review

### External Systems
- [ ] External APIs are called correctly
- [ ] API contracts are respected
- [ ] Error handling for external services
- [ ] Timeouts and retries are configured
- [ ] Circuit breakers are used (if needed)

### Internal Systems
- [ ] Integration with other modules/services
- [ ] Event publishing/subscribing is correct
- [ ] Database migrations are included
- [ ] Backward compatibility is maintained

---

## 9. Deployment & Operations Review

### Deployment
- [ ] Configuration is externalized
- [ ] Environment-specific configs are handled
- [ ] No hard-coded values
- [ ] Environment variables documented
- [ ] Docker files are updated (if applicable)

### Monitoring & Observability
- [ ] Logging is appropriate
- [ ] Metrics are collected
- [ ] Alerts are configured
- [ ] Tracing is in place (if applicable)
- [ ] Health checks are implemented

### Rollback
- [ ] Rollback plan is documented
- [ ] Database migrations are reversible
- [ ] Feature flags can be toggled
- [ ] Blue-green deployment is possible

---

## 10. Browser/Platform Compatibility (if applicable)

### Frontend Changes
- [ ] Tested in target browsers
- [ ] No browser-specific code
- [ ] Progressive enhancement used
- [ ] Mobile compatibility verified
- [ ] Responsive design works correctly

### Backend Changes
- [ ] Tested on target platforms
- [ ] Platform-specific issues addressed
- [ ] Environment differences handled

---

## Final Assessment

### Overall Quality
- [ ] Code meets quality standards
- [ ] Code is production-ready
- [ ] No critical issues remain
- [ ] Technical debt is acceptable

### Recommendation
- [ ] **Approve** - Ready to merge
- [ ] **Approve with comments** - Minor issues, can address later
- [ ] **Request changes** - Significant issues must be addressed

### Blocking Issues
- [ ] None
- [ ] List any blocking issues here

### Non-Blocking Issues
- [ ] List any non-blocking issues/suggestions here

### Follow-up Required
- [ ] No follow-up needed
- [ ] Follow-up items:
  - [ ] [ ] [ ]
  - [ ] [ ] [ ]

---

## Review Comments

### Summary
[Brief summary of the review]

### Critical Issues
[None or description of critical issues]

### Important Issues
[Description of important issues]

### Minor Issues
[Description of minor issues]

### Suggestions
[Optional suggestions for improvement]

### Praise
[What was done well]

---

## Reviewer Information
- **Name**: [Your Name]
- **Role**: [Your Role]
- **Date**: [YYYY-MM-DD]
- **Review Time**: [Time spent]
- **PR/Change ID**: [Reference]

---

## Post-Review Actions

### For Author
- [ ] Address all blocking issues
- [ ] Consider non-blocking suggestions
- [ ] Update tests if needed
- [ ] Update documentation if needed
- [ ] Respond to all comments

### For Reviewer
- [ ] Re-review after changes
- [ ] Verify fixes
- [ ] Approve when ready
- [ ] Monitor deployment (if critical change)
