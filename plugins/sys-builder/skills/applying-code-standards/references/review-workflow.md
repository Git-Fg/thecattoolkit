# Code Review Protocol

## Core Purpose

Act as a Senior Engineer reviewing a Junior Engineer's PR. Focus on Logic, Security, and Maintainability.

## Review Checklist

### 1. Correctness
- [ ] Does the logic handle edge cases (null, 0, empty array)?
- [ ] Are error states handled (try/catch, promises)?
- [ ] Does the change actually solve the stated problem?
- [ ] Are there unintended side effects?

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
- [ ] No unnecessary re-renders (frontend)?
- [ ] Efficient algorithms used (appropriate time complexity)?

### 4. Maintainability
- [ ] Variables named for intent (`userList` vs `data`)?
- [ ] Functions do one thing?
- [ ] No magic numbers?
- [ ] Code follows DRY principle?
- [ ] Appropriate abstractions?

### 5. Testing
- [ ] Test coverage for new functionality?
- [ ] Edge cases tested?
- [ ] Test quality and assertions correct?
- [ ] Tests are deterministic (no flakes)?

### 6. Documentation
- [ ] Complex logic commented?
- [ ] Function signatures documented?
- [ ] README updated if needed?
- [ ] CHANGELOG entry for user-facing changes?

### 7. Static Analysis (NEW)
- [ ] Linter passes without new warnings?
- [ ] Type checking passes (TypeScript, mypy, etc.)?
- [ ] Security scan clean (no new vulnerabilities)?
- [ ] Dependency audit passed?

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

### Step 3: Run Automated Checks
```bash
# Run linter
npm run lint  # or ruff check ., golangci-lint run, etc.

# Run type checker
npm run type-check  # or tsc --noEmit, mypy .

# Run security scan
npm audit  # or pip-audit, go list -json, cargo audit
```

### Step 4: Analysis
Review the changes against the checklist:

1. **Correctness**: Does it actually solve the problem?
2. **Security**: Are inputs sanitized? Auth checks present?
3. **Performance**: Any N+1 queries? Loop inefficiencies?
4. **Style**: Variable naming, folder structure
5. **Testing**: Adequate test coverage?
6. **Static Analysis**: Any tool warnings or errors?

### Step 5: Report Findings
Group findings by severity and provide specific file:line references:

- **[CRITICAL]**: Must fix immediately (Bug/Security)
- **[WARNING]**: Strong recommendation (Tech debt)
- **[NIT]**: Style/Preference

## Output Format

Each finding must include:
- File:line reference
- Category (security/performance/correctness/style/analysis)
- Description of the issue
- Concrete fix suggestion (for CRITICAL/WARNING)

## Example Review Output

```markdown
## Review Summary
**Files Changed**: 5
**Lines Added**: 127
**Lines Removed**: 43

## Critical Issues

### [CRITICAL] SQL Injection Risk
- **File**: `src/api/users.ts:45`
- **Category**: security
- **Description**: User input is directly interpolated into SQL query
- **Fix**: Use parameterized query:
```typescript
// Before
const query = `SELECT * FROM users WHERE id = ${userId}`;

// After
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```

### [CRITICAL] Missing Authorization Check
- **File**: `src/api/admin/delete.ts:12`
- **Category**: security
- **Description**: Admin endpoint lacks role verification
- **Fix**: Add admin role check before processing

## Warning Issues

### [WARNING] Unhandled Promise Rejection
- **File**: `src/services/auth.ts:78`
- **Category**: correctness
- **Description**: Async function lacks error handling
- **Fix**: Wrap in try/catch or add .catch()

### [WARNING] N+1 Query Pattern
- **File**: `src/api/posts.ts:56`
- **Category**: performance
- **Description**: DB query inside loop will cause performance issues
- **Fix**: Use JOIN or batch loading

## Nit Picks

### [NIT] Inconsistent Naming
- **File**: `src/utils/helpers.ts`
- **Category**: style
- **Description**: Function uses camelCase but exports as snake_case
- **Fix**: Align naming conventions

## Static Analysis Results
- ESLint: 2 new warnings (see above)
- TypeScript: No type errors
- npm audit: 1 high vulnerability (lodash@4.17.15)

## Approval Status
**Changes Requested** - Please address critical and warning issues
```

## Success Criteria
- [ ] Report is categorized by severity
- [ ] Every finding includes a specific file:line reference
- [ ] Every critical finding suggests a concrete fix
- [ ] Security checklist verified
- [ ] All affected files reviewed
- [ ] Static analysis results included
