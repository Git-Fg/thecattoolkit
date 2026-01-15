---
name: auditing-security
description: "Scans for secrets and performs comprehensive security audits. MUST Use when verifying security of code changes or auditing file safety."
context: fork
user-invocable: true
agent: security-auditor
allowed-tools: [Read, Grep, Glob]
---

# Security Audit Standards

## Active Hooks


### 1. Secret Detection
**Trigger:** `PreToolUse` (Edit/Write)
**Action:** Scans content for:
- API Keys (OpenAI, Anthropic, AWS)
- Bearer Tokens
- Private Keys
- GitHub Tokens

### 2. File Protection
**Trigger:** `PreToolUse` (Edit/Write)
**Action:** Warns on modification of:
- Lock files (`package-lock.json`, `poetry.lock`)
- Secrets directories (`.env`, `credentials/`)
- Git internals



## Configuration

Patterns are defined in:
- `plugins/verify/hooks/scripts/security-check.py`
- `plugins/verify/hooks/scripts/protect-files.py`

## Manual Audit Protocol

### Phase 1: Discovery
1. **Identify Project Context**: Programming languages, config files, dependencies
2. **Locate Targets**: Source files, configuration files, dependency manifests
3. **Check Frameworks**: Security libraries or frameworks in use

### Phase 2: Scanning
**Secret Detection:**
- API keys: `/api[_-]?key["\s]*[:=]["\s]*[a-zA-Z0-9]{20,}/`
- Tokens: `/token["\s]*[:=]["\s]*[a-zA-Z0-9]{20,}/`
- Passwords: `/(password|passwd|pwd)["\s]*[:=]["\s]*["'][^"']{6,}["']/`
- Private keys: `/-----BEGIN.*PRIVATE KEY-----/`

**OWASP Top 10 Detection:**
- Injection flaws (SQL, NoSQL, OS command injection)
- Broken authentication
- Sensitive data exposure
- XML external entities (XXE)
- Broken access control
- Security misconfiguration
- Cross-site scripting (XSS)
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging & monitoring

**Anti-Patterns:**
- Unsafe eval() or exec() usage
- Hardcoded cryptographic keys
- Weak random number generation
- Missing input validation
- Insecure file operations
- Path traversal vulnerabilities
- Command injection vectors

### Phase 3: Reporting
**Structured Security Report:**
```markdown
# Security Audit Report

## Executive Summary
- Total files scanned: [N]
- Critical issues: [N]
- High severity: [N]
- Medium severity: [N]
- Low severity: [N]

## Critical Findings
[Critical security issues requiring immediate attention]

## High Severity
[Significant vulnerabilities]

## Medium Severity
[Potential security concerns]

## Low Severity
[Best practice violations]

## Recommendations
[Priority-ordered remediation steps]
```
