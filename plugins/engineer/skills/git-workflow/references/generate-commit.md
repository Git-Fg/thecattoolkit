# Workflow: Generate Commit Message

## Purpose
Analyze staged changes and generate a conventional commit message that accurately describes the changes.

## Required Reading
- Parent `SKILL.md` for commit type definitions and format standards

## Process

### Step 1: Capture Staged Changes
1. **Get diff**: Retrieve the staged changes for analysis.
   ```bash
   git diff --staged
   ```
2. **Get status**: Understand the files being modified.
   ```bash
   git status --short
   ```

### Step 2: Analyze Changes
Examine the diff output to understand:
- **What changed**: New files, modifications, deletions
- **Scope**: Which component/module/feature is affected
- **Nature**: Is this a new feature, bug fix, refactor, etc.

**Classification Matrix:**
| Change Pattern | Likely Type |
|----------------|-------------|
| New file with functionality | `feat` |
| Modification fixing behavior | `fix` |
| *.md, comments, docstrings | `docs` |
| Whitespace, formatting only | `style` |
| Code restructure, no behavior change | `refactor` |
| Optimization, benchmarks | `perf` |
| Test files added/modified | `test` |
| Build config, dependencies | `chore` |
| CI/CD files (.github/, etc.) | `ci` |

### Step 3: Determine Scope
Identify the most specific scope:
1. **Check file paths** for component/module names
2. **Check function/class names** being modified
3. **If changes span multiple areas**, use broader scope or omit

**Scope Examples:**
- `auth` - authentication related
- `api` - API endpoints
- `ui` - user interface
- `db` - database layer
- `deps` - dependencies

### Step 4: Generate Message
Compose the commit message following the format:

```
<type>(<scope>): <description>

[optional body - what and why, not how]

[optional footer - BREAKING CHANGE, Closes #issue]
```

**Rules:**
- Description: imperative mood, lowercase, no period, max 50 chars
- Body: wrap at 72 characters
- Footer: reference issues if applicable

### Step 5: Present or Execute

**For interactive use:** Display the generated message and await user confirmation before committing.

**For automated use (e.g., /commit command):** The message will be displayed for transparency and the commit will execute immediately. Only ask for input if critical issues are detected (unusual patterns, breaking changes).

## Success Criteria
- [ ] Staged changes captured
- [ ] Correct commit type identified
- [ ] Appropriate scope determined
- [ ] Message follows conventional commit format
- [ ] User confirms or modifies before commit
