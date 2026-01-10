# Workflow: Safe Refactoring

## Purpose
Improve code structure without altering external behavior.

## Required Reading
- `references/security-checklist.md` - **MANDATORY** for all refactoring operations
- `references/refactoring-patterns.md` - Code improvement patterns

## Process

### Step 1: Establish Safety Net
Run tests **before** touching anything.
```bash
npm test
```
*If tests fail, stop. Fix tests first.*

### Step 2: Identify Smells
- **Long Method**: >20 lines?
- **Cognitive Complexity**: Too many `if/else`?
- **Duplication**: Copy-pasted logic?

### Step 3: Apply Pattern
Choose one transformation:
- Extract Method
- Rename Variable
- Inline Temp
- Extract Class

### Step 4: Verify
Run tests again.
```bash
npm test
```

## Success Criteria
- [ ] Tests pass before AND after.
- [ ] Code is demonstrably cleaner (lower complexity score/LOC).
- [ ] No behavioral changes occurred.