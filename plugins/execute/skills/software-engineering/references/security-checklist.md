# Security Checklist (OWASP Top 10)

## A01:2021 - Broken Access Control
- [ ] Authentication required for all sensitive endpoints
- [ ] Authorization checks on every protected resource
- [ ] No direct object references without validation
- [ ] Session management properly implemented
- [ ] Role-based access control (RBAC) enforced

## A02:2021 - Cryptographic Failures
- [ ] Data encrypted in transit (TLS/SSL)
- [ ] Data encrypted at rest
- [ ] Strong encryption algorithms used (AES-256, RSA-2048+)
- [ ] Cryptographic keys properly secured
- [ ] No hardcoded passwords or keys

## A03:2021 - Injection
- [ ] All user inputs parameterized/prepared statements
- [ ] No dynamic SQL queries
- [ ] Input validation on all entry points
- [ ] Output encoding/escaping implemented
- [ ] Command injection prevention (no eval(), exec())

## A04:2021 - Insecure Design
- [ ] Threat modeling completed
- [ ] Security requirements defined
- [ ] Secure architecture patterns followed
- [ ] Defense in depth implemented
- [ ] Security controls fail securely

## A05:2021 - Security Misconfiguration
- [ ] Default accounts/passwords changed
- [ ] Unnecessary features disabled
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Error messages don't expose sensitive info
- [ ] Security updates applied

## A06:2021 - Vulnerable and Outdated Components
- [ ] Dependencies regularly updated
- [ ] Vulnerability scanning implemented
- [ ] No deprecated libraries in use
- [ ] Component versions tracked
- [ ] Security advisories monitored

## A07:2021 - Identification and Authentication Failures
- [ ] Multi-factor authentication (MFA) where appropriate
- [ ] Strong password policies enforced
- [ ] Account lockout after failed attempts
- [ ] Session timeouts implemented
- [ ] No session fixation vulnerabilities

## A08:2021 - Software and Data Integrity Failures
- [ ] Code signed and verified
- [ ] Integrity checks on updates
- [ ] No unsigned/unaltered plugins
- [ ] Secure CI/CD pipeline
- [ ] Dependencies pinned and verified

## A09:2021 - Security Logging and Monitoring Failures
- [ ] Security events logged (auth failures, access attempts)
- [ ] Logs protected from tampering
- [ ] Monitoring/alerting configured
- [ ] Log retention policy defined
- [ ] Regular log review process

## A10:2021 - Server-Side Request Forgery (SSRF)
- [ ] URL validation on external requests
- [ ] Network segmentation implemented
- [ ] Allowlist of approved URLs/domains
- [ ] Response validation implemented
- [ ] Metadata protection enabled

## Additional Security Checks

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

### Authentication & Authorization
- [ ] Password hashing (bcrypt, Argon2)
- [ ] Secure session tokens
- [ ] OAuth/OpenID properly configured
- [ ] JWT tokens properly secured
- [ ] API keys rotated regularly

### Data Protection
- [ ] PII encrypted
- [ ] Data minimization applied
- [ ] Secure data disposal
- [ ] Backup encryption
- [ ] Privacy controls implemented

## Severity Levels

**Critical (Must Fix)**
- Authentication/authorization bypasses
- SQL injection vulnerabilities
- Remote code execution
- Direct object reference flaws

**High (Fix Soon)**
- XSS vulnerabilities
- CSRF protection missing
- Cryptographic weaknesses
- Insecure deserialization

**Medium (Plan to Fix)**
- Information disclosure
- Missing security headers
- Weak session management
- Insecure configurations

**Low (Monitor)**
- Verbose error messages
- Missing rate limiting
- Weak password policies
- Outdated dependencies
