# Workflow: Systematic Debugging

## Purpose
Fix bugs using the Scientific Method (Hypothesis → Test → Fix), not guesswork.

## 6-Phase Debugging Protocol

1. **Capture**: Get the raw error log. Never paraphrase errors.
2. **Analyze**: Trace the stack backwards from crash point.
3. **Hypothesize**: "I believe X is causing Y because Z."
4. **Test**: Prove the hypothesis with a minimal repro.
5. **Fix**: Apply the minimal change required.
6. **Verify**: Run the repro case and regression suite.

## Process

### Step 0: Security Check
**CRITICAL:** Read `references/security-checklist.md` to understand security vulnerabilities that could be introduced during debugging.

**WHY:** Debugging often involves temporary fixes, logging sensitive data, or bypassing validation. This step ensures you don't inadvertently create security issues while fixing bugs.

### Step 1: Capture & Reproduce
1. **Capture**: Run the code to see the EXACT error message.
   ```bash
   # Example
   npm run test
   ```
2. **Context**: Get the environment state.
   ```bash
   node --version
   git status
   ```

### Step 2: Analyze
Read the *full* stack trace and the relevant source file.
- **Trace**: Identify the file:line where it crashes.
- **Code**: Read the surrounding logic.

### Step 3: Hypothesis Generation
Formulate 2 plausible theories.
- "Hypothesis A: The `user` object is null because fetch failed."
- "Hypothesis B: The API key env var is missing."

### Step 4: Verify Hypothesis
Add logs or create a reproduction script to prove one hypothesis TRUE.
*Do not fix yet. Prove it first.*

### Step 5: Fix & Verify
1. Apply the fix.
2. Run the reproduction case again to confirm it passes.
3. Run related tests to ensure no regressions.

## Success Criteria
- [ ] The bug is reproduced deterministically.
- [ ] The root cause is identified (not just a symptom patch).
- [ ] Tests pass.