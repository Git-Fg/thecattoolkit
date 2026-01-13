---
description: "Quick access to code review and static analysis capabilities. Runs automated checks including linting, type checking, and security scanning."
argument-hint: "[mode] [target]"
allowed-tools: [Skill(software-engineering), Bash(git:*,npm:*,pnpm:*,bun:*,yarn:*), Read, Grep]
disable-model-invocation: true
---

# Code Review & Static Analysis

Quick command for code review and static analysis workflows.

## Modes

**Interactive Mode** (default):
```
/sys-builder:code-review
```
Prompts for target files/directories and analysis preferences.

**Direct Mode**:
```
/sys-builder:code-review analyze <path>
```
Runs full static analysis on specified path without prompts.

## Usage Examples

```bash
# Interactive review of staged changes
/sys-builder:code-review

# Analyze specific file
/sys-builder:code-review analyze src/api/users.ts

# Full project scan
/sys-builder:code-review analyze .

# Security-focused scan
/sys-builder:code-review security .
```

## Workflow

This command invokes the `software-engineering` skill in **Static Analysis** or **Code Review** mode:

1. **Gathers context**: Runs `git diff` for staged changes or scans target path
2. **Runs automated checks**:
   - Linter (ESLint, Ruff, golangci-lint, etc.)
   - Type checker (TypeScript, mypy, etc.)
   - Security scanner (npm audit, pip-audit, etc.)
3. **Analyzes findings**: Categorizes by severity (Critical/Warning/Nit)
4. **Generates report**: Structured output with file:line references

## Output

Report includes:
- **Summary**: Files changed, lines added/removed
- **Critical Issues**: Security vulnerabilities, bugs
- **Warning Issues**: Tech debt, performance issues
- **Nit Picks**: Style inconsistencies
- **Static Analysis Results**: Tool output summary

## See Also

- `Skill(software-engineering)` - Full engineering standards reference
- `Skill(software-engineering)` - Full engineering standards reference
- See `software-engineering` references for:
  - `static-analysis-workflow.md`
  - `review-workflow.md`
