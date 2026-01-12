# Arguments Reference

How to handle arguments in slash commands.

## $ARGUMENTS - All Arguments

Captures all arguments as a single concatenated string.

### Basic Example

**Command:**
```markdown
---
description: "Fix issue following standards"
---

Fix issue #$ARGUMENTS following our coding standards.
```

**Usage:** `/fix-issue 123 high-priority`

**Result:** "Fix issue #123 high-priority following our coding standards."

### Multi-Word Arguments

**Command:**
```markdown
---
description: "Optimize performance"
argument-hint: [file-path]
---

Analyze performance of @ $ARGUMENTS and suggest optimizations.
```

**Usage:** `/optimize src/utils/helper.js`

**Result:** "Analyze performance of @ src/utils/helper.js and suggest optimizations."

## Positional Arguments - $1, $2, $3

Access specific arguments individually.

### Example

**Command:**
```markdown
---
description: "Review PR"
argument-hint: <pr-number> <priority> <assignee>
---

Review PR #$1 with priority $2 and assign to $3.
```

**Usage:** `/review-pr 456 high alice`

**Result:** "Review PR #456 with priority high and assign to alice."

- `$1` becomes `456`
- `$2` becomes `high`
- `$3` becomes `alice`

## Argument Patterns

### File Reference with Argument

```markdown
---
description: "Optimize file"
argument-hint: [file-path]
---

Analyze @ $ARGUMENTS and suggest three specific optimizations.
```

**Usage:** `/optimize src/app.js`

### Issue Tracking

```markdown
---
description: "Find and fix issue"
argument-hint: [issue-number]
---

Find and fix issue #$ARGUMENTS.

Steps:
1. Understand the issue
2. Locate relevant code
3. Implement solution
4. Add tests
```

**Usage:** `/fix-issue 789`

### Code Review with Context

```markdown
---
description: "Review with parameters"
argument-hint: <pr-number> <priority> <assignee>
---

Review PR #$1 with priority $2 and assign to $3.

Context: ! gh pr diff $1
```

**Usage:** `/review-pr 123 critical bob`

## When to Use Each

### Use $ARGUMENTS for Simple Commands

When you just need to pass a value through:
```markdown
Fix issue #$ARGUMENTS
Optimize @ $ARGUMENTS
Summarize $ARGUMENTS
```

### Use Positional Arguments for Structure

When different arguments have different meanings:
```markdown
Review PR #$1 with priority $2 and assign to $3
Deploy $1 to $2 with tag $3
```

### No Arguments for Self-Contained

When command operates on implicit context:
```markdown
---
description: "Review recent changes"
---

Review recent git changes.
```

## Empty Arguments

Commands work with or without arguments:

```markdown
---
description: "Analyze code"
---

Analyze this code: $ARGUMENTS

If no file provided, analyze current context.
```

**Usage 1:** `/analyze src/app.js` (analyzes file)
**Usage 2:** `/analyze` (analyzes conversation)

## Combining Features

### Arguments + Dynamic Context

```markdown
---
description: "Review changes for issue"
argument-hint: [issue-number]
---

Issue #$ARGUMENTS

Recent changes:
! git status
! git diff

Review changes related to this issue.
```

### Arguments + File References

```markdown
---
description: "Compare files"
argument-hint: <file1> <file2>
---

Compare @ $1 with @ $2 and highlight differences.
```

**Usage:** `/compare src/old.js src/new.js`

### Arguments + Tool Restrictions

```markdown
---
description: "Commit for issue"
allowed-tools: Bash(git add:*), Bash(git commit:*)
argument-hint: [issue-number]
---

Create commit for issue #$ARGUMENTS.

Status: ! git status
```

## Notes

- Arguments are whitespace-separated
- Quote arguments with spaces: `/command "argument with spaces"`
- Arguments passed as-is (no special parsing)
- Empty arguments replaced with empty string
- Use `argument-hint` to document expected input
