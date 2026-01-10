---
name: code-review
description: |
  USE when reviewing changes, PRs, or assessing code quality through systematic code review and quality assessment.
  Keywords: code review, PR review, quality assessment, security review
context: fork
agent: worker
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Code Review Protocol

## Core Purpose

Act as a Senior Engineer reviewing a Junior Engineer's PR. Focus on Logic, Security, and Maintainability.

## Review Checklist

### 1. Correctness
- [ ] Does the logic handle edge cases (null, 0, empty array)?
- [ ] Are error states handled (try/catch, promises)?

### 2. Security (OWASP Top 10)
- [ ] **Injection Prevention**: All user inputs validated/sanitized, no dynamic SQL
- [ ] **Authentication**: Auth checks on sensitive endpoints, no hardcoded secrets
- [ ] **Access Control**: Authorization checks on every protected resource
- [ ] **Cryptography**: No hardcoded passwords or keys
- [ ] **Input Validation**: All entry points validated
- [ ] **Error Handling**: Errors don't expose sensitive information
- [ ] **Dependencies**: No vulnerable/outdated components

### 3. Performance
- [ ] No DB queries inside loops?
- [ ] Large datasets paginated?
- [ ] Heavy computations cached?

### 4. Maintainability
- [ ] Variables named for intent (`userList` vs `data`)?
- [ ] Functions do one thing?
- [ ] No magic numbers?

### 5. Testing
- [ ] Test coverage for new functionality?
- [ ] Edge cases tested?
- [ ] Test quality and assertions correct?

### 6. Documentation
- [ ] Complex logic commented?
- [ ] Function signatures documented?
- [ ] README updated if needed?

## Review Process

### Step 1: Gather Context
```bash
git diff --staged  # or git diff HEAD~1
```

### Step 2: The "Blast Radius" Check
Before reviewing lines, check imports and usages:
```bash
grep -r "ChangedFunctionName" .
```

### Step 3: Analysis
Review the changes against the checklist:

1. **Correctness**: Does it actually solve the problem?
2. **Security**: Are inputs sanitized? Auth checks present?
3. **Performance**: Any N+1 queries? Loop inefficiencies?
4. **Style**: Variable naming, folder structure
5. **Testing**: Adequate test coverage?

### Step 4: Report Findings
Group findings by severity and provide specific file:line references:

- **[CRITICAL]**: Must fix immediately (Bug/Security)
- **[WARNING]**: Strong recommendation (Tech debt)
- **[NIT]**: Style/Preference

## Output Format

Each finding must include:
- File:line reference
- Category (security/performance/correctness/style)
- Description of the issue
- Concrete fix suggestion (for CRITICAL/WARNING)

## Success Criteria
- [ ] Report is categorized by severity
- [ ] Every finding includes a specific file:line reference
- [ ] Every critical finding suggests a concrete fix
- [ ] Security checklist verified
- [ ] All affected files reviewed
