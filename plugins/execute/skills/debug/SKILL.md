---
name: debug
description: |
  Systematic debugging and bug fixing. USE when fixing errors, crashes, test failures, or performance issues.
  Keywords: fix bug, debug error, investigate crash, solve issue
context: fork
agent: worker
user-invocable: true
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Debugging Protocol

## Core Purpose

Fix bugs using the Scientific Method (Hypothesis → Test → Fix), not guesswork.

## 6-Phase Debugging Protocol

### Phase 0: Security Check
**CRITICAL:** Read security checklist below before modifying code.

Debugging often involves temporary fixes, logging sensitive data, or bypassing validation. Ensure you don't inadvertently create security issues.

### Phase 1: Capture & Reproduce
1. **Capture**: Run the code to see the EXACT error message
   ```bash
   npm run test
   ```
2. **Context**: Get the environment state
   ```bash
   node --version
   git status
   ```

### Phase 2: Analyze
Read the *full* stack trace and the relevant source file:
- **Trace**: Identify the file:line where it crashes
- **Code**: Read the surrounding logic

### Phase 3: Hypothesis Generation
Formulate 2 plausible theories:
- "Hypothesis A: The `user` object is null because fetch failed"
- "Hypothesis B: The API key env var is missing"

### Phase 4: Test Hypothesis
Add logs or create a reproduction script to prove one hypothesis TRUE.
*Do not fix yet. Prove it first.*

### Phase 5: Fix & Verify
1. Apply the fix
2. Run the reproduction case again to confirm it passes
3. Run related tests to ensure no regressions

### Phase 6: Complete
- Root cause identified (not just symptom patch)
- All tests pass
- No regressions introduced

## Security Checklist (OWASP Top 10)

**Before executing any code modifications:**

- [ ] **Injection Prevention**: All user inputs validated/sanitized, no dynamic SQL
- [ ] **Authentication**: Auth checks on sensitive endpoints, no hardcoded secrets
- [ ] **Access Control**: Authorization checks on every protected resource
- [ ] **Cryptography**: No hardcoded passwords or keys
- [ ] **Input Validation**: All entry points validated
- [ ] **Error Handling**: Errors don't expose sensitive information
- [ ] **Dependencies**: No vulnerable/outdated components

## Success Criteria
- [ ] Bug reproduced deterministically
- [ ] Root cause identified (not symptom patch)
- [ ] All tests pass
- [ ] Security checklist verified
