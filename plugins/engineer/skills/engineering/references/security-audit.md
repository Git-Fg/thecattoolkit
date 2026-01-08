# Workflow: Security Audit

## Purpose
Systematic scan for vulnerabilities using OWASP patterns.

## Required Reading
- `references/security-checklist.md`

## Process

### Step 1: Reconnaissance
Find sensitive surface areas.
```bash
grep -r "password" .
grep -r "api_key" .
grep -r "eval(" .
```

### Step 2: Data Flow Analysis
Trace user input from Entry Point (API Controller) to Sink (Database/HTML).
- Is it validated at entry?
- Is it escaped at exit?

### Step 3: Report
Create a confidential vulnerability report.
- **Severity**: CVSS Score estimation.
- **Exploit**: How it could be abused.
- **Fix**: Code patch.

## Success Criteria
- [ ] All "Critical" inputs traced.
- [ ] Report assumes "Attacker Mindset".