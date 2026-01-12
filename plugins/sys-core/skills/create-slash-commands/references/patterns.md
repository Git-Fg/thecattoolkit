# Command Patterns

Common patterns for creating effective slash commands.

## Git Workflow Patterns

### Commit with Context

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: "Create a git commit"
---

Current status: ! git status
Changes: ! git diff HEAD
Branch: ! git branch --show-current

Create a commit for these changes following repository conventions.
```

### Git-Only Analysis

```markdown
---
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*)
description: "Review recent changes"
---

Review recent changes:
! git log --oneline -5
! git diff HEAD~1
```

## Code Analysis Patterns

### Performance Review

```markdown
---
description: "Analyze performance and suggest optimizations"
---

Analyze this code for performance issues and suggest three specific optimizations:

1. Review code structure
2. Identify bottlenecks
3. Suggest concrete improvements
```

### Security Audit

```markdown
---
description: "Review code for security vulnerabilities"
---

Review this code for security vulnerabilities:
- Check for XSS, SQL injection, CSRF
- Identify specific issues with locations
- Suggest remediation steps
```

### File-Specific Analysis

```markdown
---
description: "Analyze specific file"
argument-hint: [file-path]
---

Analyze performance of @ $ARGUMENTS and suggest optimizations.
```

## Issue Tracking Patterns

### Fix Issue

```markdown
---
description: "Fix issue following standards"
argument-hint: [issue-number]
---

Fix issue #$ARGUMENTS:

1. Understand the issue
2. Locate relevant code
3. Implement solution
4. Add tests
5. Verify fix
```

### PR Review

```markdown
---
description: "Review PR with context"
argument-hint: <pr-number> <priority> <assignee>
---

Review PR #$1 with priority $2 and assign to $3.

Fetch PR details and review code changes.
```

## File Operations

### File Reference

```markdown
---
description: "Review implementation"
---

Review the implementation in @ src/utils/helpers.js

Check:
- Code quality
- Best practices
- Potential improvements
```

### Compare Files

```markdown
---
description: "Compare two files"
argument-hint: <file1> <file2>
---

Compare @ $1 with @ $2 and highlight key differences.
```

## Tool Restriction Patterns

### Read-Only Analysis

```markdown
---
allowed-tools: [Read, Grep, Glob]
description: "Analyze codebase safely"
argument-hint: [search pattern]
---

Search codebase for: $ARGUMENTS

Analyze findings and provide summary.
```

### Thinking-Only

```markdown
---
allowed-tools: SequentialThinking
description: "Analyze from first principles"
---

Analyze the current problem from first principles:

1. Identify core problem
2. Strip assumptions
3. Rebuild from fundamentals
4. Compare approaches
```

### Specific Commands Only

```markdown
---
allowed-tools: Bash(npm test:*), Bash(npm run lint:*)
description: "Run quality checks"
---

Run project quality checks:

Tests: ! npm test
Linting: ! npm run lint

Report pass/fail status.
```

## Multi-Step Workflows

### Complete Feature

```markdown
---
description: "Complete feature development"
argument-hint: [feature description]
---

Complete feature: $ARGUMENTS

Planning:
- Review requirements
- Design approach

Implementation:
- Write code
- Add tests
- Update docs

Verification:
- Run tests: ! npm test
- Check lint: ! npm run lint
```

### Analysis to Fix

```markdown
---
description: "Analyze and fix performance"
argument-hint: [file-path]
---

Analyze and fix performance issues in @ $ARGUMENTS:

1. Analyze performance
2. Identify top 3 issues
3. Implement fixes
4. Verify improvements
```

## Best Practices Summary

1. **Use tool restrictions** for safety
2. **Load dynamic context** when needed with `!`
3. **Reference files explicitly** with `@`
4. **Structure complex workflows** clearly
5. **Use arguments** for flexibility
6. **Keep focused** - one purpose per command
7. **Document expectations** with argument-hint
8. **Test commands** after creating
