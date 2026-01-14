# Static Analysis Workflow

## Core Purpose

Automated code quality and security analysis using static application security testing (SAST) tools and language-specific linters. Focus on detecting vulnerabilities, code smells, and maintainability issues before runtime.

## Analysis Protocol

### Phase 1: Tool Selection

**Language-specific tools:**
| Language | Recommended Tools | Command |
|----------|-------------------|---------|
| **TypeScript/JavaScript** | ESLint, TypeScript Compiler, SonarJS | `eslint .`, `tsc --noEmit` |
| **Python** | Ruff, Pylint, Bandit, MyPy | `ruff check .`, `bandit -r .` |
| **Go** | golangci-lint, go vet, staticcheck | `golangci-lint run` |
| **Rust** | Clippy, rustfmt | `cargo clippy` |
| **Java** | SpotBugs, Checkstyle, PMD | `mvn spotbugs:check` |

**Security-focused tools:**
- **Semgrep**: Rule-based static analysis for multiple languages
- **CodeQL**: Semantic code analysis engine (GitHub)
- **Trivy**: Security scanner for dependencies and code

### Phase 2: Run Analysis

#### Step 1: Dependency Security Scan
```bash
# npm (JavaScript)
npm audit
# or
pnpm audit

# pip (Python)
pip-audit
# or
safety check

# go (Go)
go list -json -m all | nancy sleuth

# cargo (Rust)
cargo audit
```

#### Step 2: Code Quality Linting
```bash
# TypeScript/JavaScript
eslint . --ext .ts,.tsx,.js,.jsx --format json --output-file eslint-report.json

# Python
ruff check . --output-format json > ruff-report.json

# Go
golangci-lint run --out-format json > golangci-report.json
```

#### Step 3: Type Safety Check
```bash
# TypeScript
tsc --noEmit

# Python (with mypy)
mypy . --json-report mypy-report/

# Go (built-in)
go vet ./...
```

#### Step 4: Security Scan
```bash
# Semgrep (multi-language)
semgrep --config=auto --json --output=semgrep-report.json

# Bandit (Python security)
bandit -r . -f json -o bandit-report.json

# Trivy (filesystem scan)
trivy fs --format json --output trivy-report.json .
```

### Phase 3: Analyze Results

#### Severity Classification

**Critical (Must Fix):**
- SQL Injection, Command Injection, XSS vulnerabilities
- Hardcoded credentials or API keys
- Insecure cryptographic algorithms
- Authentication/authorization bypasses
- Remote code execution (RCE) vectors

**High (Should Fix):**
- Dependency vulnerabilities with known exploits
- Unsanitized user input
- Sensitive data exposure in logs
- Race conditions
- Memory leaks (resource exhaustion)

**Medium (Consider Fixing):**
- Code complexity violations
- Code smells (duplicate code, long functions)
- Deprecated API usage
- Performance anti-patterns

**Low (Technical Debt):**
- Style inconsistencies
- Missing documentation
- Weak typing issues

### Phase 4: Report Findings

#### Report Template

```markdown
# Static Analysis Report

## Summary
- **Tool**: [Tool Name]
- **Files Scanned**: N
- **Issues Found**: N (Critical: N, High: N, Medium: N, Low: N)
- **Date**: [Timestamp]

## Critical Issues
### [CWE-XXX] Issue Title
- **File**: `path/to/file.ts:123`
- **Tool**: [Tool Name]
- **Description**: Clear explanation of the vulnerability
- **Remediation**: Specific code example showing the fix
- **References**: [CWE Link] | [Documentation]

## High Issues
[Same format as above]

## Dependency Vulnerabilities
| Package | Version | Vulnerability | Severity | Fix Version |
|---------|---------|---------------|----------|-------------|
| package-name | 1.2.3 | CVE-2024-XXXX | High | 1.2.4 |

## Code Quality Metrics
- **Cyclomatic Complexity**: Average X.X (Max: Y)
- **Code Duplication**: X%
- **Test Coverage**: X%
- **Technical Debt Ratio**: X hours

## Recommendations
1. Prioritized list of remediation steps
2. Suggested tool configurations
3. Process improvements (CI/CD integration)
```

### Phase 5: Remediation

#### Automated Fixes
```bash
# ESLint auto-fix
eslint . --fix

# Ruff auto-fix (Python)
ruff check . --fix

# Black formatter (Python)
black .

# gofmt (Go)
gofmt -w .
```

#### Manual Fixes

For each critical/high issue:
1. Understand the root cause
2. Reference CWE/Owasp documentation
3. Implement fix following secure coding practices
4. Add regression test
5. Re-scan to verify fix

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Static Analysis

on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: auto

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload SARIF files
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running static analysis..."

# Run linter
if ! ruff check .; then
    echo "Linting failed. Run 'ruff check . --fix' to auto-fix."
    exit 1
fi

# Run type checker
if ! mypy .; then
    echo "Type checking failed."
    exit 1
fi

# Run security scanner
if ! bandit -r . -ll; then
    echo "Security issues detected."
    exit 1
fi

echo "All checks passed!"
```

## Best Practices

1. **Shift Left**: Run analysis during development, not just in CI
2. **Fail Fast**: Configure CI to fail on critical/high issues
3. **False Positives**: Maintain suppression files with justification
4. **Baseline**: Establish initial baseline, then enforce zero new issues
5. **Fix Timeboxes**: Set SLAs for critical (24h), high (1 week), medium (1 month)

## Anti-Patterns to Avoid

- BAD Ignoring tool outputs without review
- BAD Over-suppressing warnings (reduces tool effectiveness)
- BAD Running analysis manually only (automate in CI)
- BAD Using tools without custom rules for your domain
- BAD Treating all findings equally (prioritize by risk)

## Success Criteria

- [ ] All critical vulnerabilities remediated or documented with risk acceptance
- [ ] Dependency vulnerabilities addressed or updated
- [ ] Code quality metrics maintained or improved
- [ ] Analysis integrated into CI/CD pipeline
- [ ] Team trained on interpreting and fixing findings
- [ ] False positive rate < 10%
