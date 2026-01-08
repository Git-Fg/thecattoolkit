# Workflow: Code Review

## Purpose
Act as a Senior Engineer reviewing a Junior Engineer's PR. Focus on Logic, Security, and Maintainability.

## Required Reading
- `references/review-checklist.md`

## Process

### Step 1: Gather Context
```bash
git diff --staged  # or git diff HEAD~1
```

### Step 2: The "Blast Radius" Check
Before reviewing lines, check imports and usages.
```bash
grep -r "ChangedFunctionName" .
```

### Step 3: Analysis
Review the changes against the checklist:
1. **Correctness**: Does it actually solve the problem?
2. **Security**: Are inputs sanitized? Auth checks present?
3. **Performance**: Any N+1 queries? Loop inefficiencies?
4. **Style**: Variable naming, folder structure.

### Step 4: Report Findings
Group findings by severity:
- **[CRITICAL]**: Must fix immediately (Bug/Security).
- **[WARNING]**: Strong recommendation (Tech debt).
- **[NIT]**: Style/Preference.

## Success Criteria
- [ ] Report is categorized by severity.
- [ ] Every finding includes a specific file:line reference.
- [ ] Every critical finding suggests a concrete fix.