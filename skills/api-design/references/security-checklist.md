# Security Audit Checklist

Comprehensive security checklist based on OWASP Top 10 and common vulnerability patterns. Reference for `security-auditor` subagent.

## Audit Process

### PHASE 1 - Reconnaissance

```bash
# Find sensitive files
find . -name "*.env*" -o -name "*secret*" -o -name "*credential*" -o -name "*.pem" -o -name "*.key" 2>/dev/null

# Check for hardcoded secrets
grep -rn "password\s*=" --include="*.{js,ts,py,java,go,rb}" .
grep -rn "api_key\s*=" --include="*.{js,ts,py,java,go,rb}" .
grep -rn "secret\s*=" --include="*.{js,ts,py,java,go,rb}" .

# Find authentication/authorization code
grep -rn "auth\|login\|session\|token\|jwt" --include="*.{js,ts,py}" .
```

### PHASE 2 - OWASP Top 10

#### A01 - Broken Access Control
- Authorization checks on all endpoints
- Principle of least privilege
- CORS properly configured
- Directory traversal prevention

#### A02 - Cryptographic Failures
- Sensitive data encrypted at rest
- TLS for data in transit
- Strong hashing for passwords (bcrypt, argon2)
- No deprecated algorithms (MD5, SHA1 for security)

#### A03 - Injection
- Parameterized queries (no string concatenation for SQL)
- Input sanitization
- Command injection prevention
- XSS prevention (output encoding)

#### A04 - Insecure Design
- Threat modeling considered
- Security requirements defined
- Secure defaults

#### A05 - Security Misconfiguration
- Debug mode disabled in production
- Default credentials changed
- Unnecessary features disabled
- Security headers present

#### A06 - Vulnerable Components
- Dependencies up to date
- No known CVEs in dependencies
- Minimal dependency footprint

#### A07 - Authentication Failures
- Strong password requirements
- Rate limiting on auth endpoints
- Secure session management
- MFA supported

#### A08 - Software and Data Integrity
- CI/CD pipeline secured
- Dependency integrity verified
- Code signing where applicable

#### A09 - Security Logging
- Security events logged
- No sensitive data in logs
- Log injection prevented

#### A10 - Server-Side Request Forgery
- URL validation on user input
- Allowlist for external requests
- Internal network access restricted

### PHASE 3 - Code Checks

#### SQL Injection

```javascript
// BAD: SQL Injection
query(`SELECT * FROM users WHERE id = ${userId}`);

// GOOD: Parameterized
query('SELECT * FROM users WHERE id = ?', [userId]);
```

#### Command Injection

```javascript
// BAD: Command Injection
exec(`ls ${userInput}`);

// GOOD: Avoid shell, use APIs
fs.readdir(sanitizedPath);
```

#### XSS

```javascript
// BAD: XSS
element.innerHTML = userInput;

// GOOD: Text content or sanitize
element.textContent = userInput;
```

## Output Format

### Severity Levels

**CRITICAL** - Exploitable issues requiring immediate attention.
**HIGH** - Significant security weaknesses.
**MEDIUM** - Issues that increase attack surface.
**LOW** - Best practice improvements.

### Finding Template

```markdown
## Finding: [Vulnerability Name]

Severity: Critical/High/Medium/Low
Location: file:line
CWE: CWE-XXX

### Description
What the vulnerability is and why it matters.

### Impact
What an attacker could do.

### Reproduction
Steps to demonstrate the issue.

### Remediation
Specific code changes to fix.

### References
- [OWASP Link]
- [CWE Link]
```

## CWE References

Common CWE mappings for OWASP Top 10:
- A01: CWE-284, CWE-287, CWE-862
- A02: CWE-259, CWE-311, CWE-312
- A03: CWE-078, CWE-089, CWE-079
- A04: CWE-1004
- A05: CWE-2, CWE-16, CWE-611
- A06: CWE-1104, CWE-937
- A07: CWE-287, CWE-307
- A08: CWE-345, CWE-353, CWE-494
- A09: CWE-117, CWE-532
- A10: CWE-918
