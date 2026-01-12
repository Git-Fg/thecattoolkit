---
name: {SKILL_NAME}
# Standard Pattern (default - for public task-oriented skills):
description: "Executes {PROCESS} with autonomous validation. Use when {TASK}."
# OR Enhanced Pattern (for toolkit infrastructure):
# description: "Executes {PROCESS} with autonomous validation. MUST Use when {TASK}."
allowed-tools: [{ALLOWED_TOOLS}]
---

# {HUMAN_READABLE_NAME}

## Overview

{What this task accomplishes}

## Process Checklist

**Copy and track progress:**

- [ ] Step 1: {Action}
- [ ] Step 2: {Action}
- [ ] Step 3: {Action}
- [ ] Step 4: Validation
- [ ] Step 5: {Final action}

## Execution Rules

1. Execute steps sequentially
2. Do NOT proceed if current step fails
3. Run validation after each critical step
4. Apply Self-Correction Pattern (max 3 retries)
5. Mark items complete: `- [x]`

## Step Details

### Step 1: {Action}
```bash
{command}
```
**Expected:** {outcome}
**Verify:** {how to check success}

### Step 2: {Action}
```bash
{command}
```
**Expected:** {outcome}
**Verify:** {how to check success}

### Step 3: {Action}
```bash
{command}
```
**Expected:** {outcome}
**Verify:** {how to check success}

### Step 4: Validation
```bash
uv run scripts/validate.sh
```

**If validation fails:**
1. Read error output
2. Identify issue
3. Apply correction
4. Re-run validation (max 3 attempts)

### Step 5: {Final action}
```bash
{command}
```
**Expected:** {final outcome}

## Self-Correction Pattern

```
┌─────────────────────────────────────────────────┐
│  attempt = 0, max = 3                           │
│  WHILE attempt < max:                           │
│    Execute step → Validate result               │
│    IF pass: Mark complete → CONTINUE            │
│    ELSE: Analyze error → Apply fix → Retry      │
│    attempt++                                    │
│  IF max reached: Report failure with details    │
└─────────────────────────────────────────────────┘
```

**Implementation:**
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Self-correcting execution pattern."""

def execute_with_retry(step_fn, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = step_fn()
            if validate(result):
                return result
            # Auto-correct based on validation failure
            apply_correction(result)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            diagnose_and_fix(e)
    raise MaxRetriesExceeded()
```

## Success Criteria

**All must be true:**
- [ ] All checklist items complete
- [ ] Validation passes
- [ ] Output generated
- [ ] No errors in log

## Common Failures & Auto-Corrections

### Failure 1: {Description}
**Detection:** {How to detect}
**Auto-fix:** {Correction approach}
```bash
{fix_command}
```

### Failure 2: {Description}
**Detection:** {How to detect}
**Auto-fix:** {Correction approach}
```bash
{fix_command}
```

## Validation Script

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Validation script for {SKILL_NAME}."""

import sys

def validate():
    errors = []

    # Check 1: {Validation}
    if not {condition}:
        errors.append("{Error message}")

    # Check 2: {Validation}
    if not {condition}:
        errors.append("{Error message}")

    if errors:
        print("✗ Validation failed:")
        for e in errors:
            print(f"  - {e}")
        return False

    print("✓ Validation passed")
    return True

if __name__ == "__main__":
    sys.exit(0 if validate() else 1)
```

**Usage:**
```bash
uv run scripts/validate.py
```

## Final Report Template

```markdown
## {Task} Complete

### Summary
- Steps completed: {n}/{total}
- Validation: {PASSED/FAILED}
- Retries required: {count}

### Output
{Description of output}

### Issues Encountered
{List of issues and how they were resolved, or "None"}
```

---

**Critical Rules:**
1. Never ask user to verify mid-execution
2. Run validation autonomously
3. Apply self-correction before asking for help
4. Report only final result
5. Include diagnostic info if failed after max retries
