---
name: applying-code-standards
description: "Provides Universal Standard for TDD, Security, and Code Quality. PROACTIVELY Use when writing code, debugging errors, or reviewing PRs. Modes: debug, review, refactor, implement."
context: fork
agent: worker
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Applying Code Standards Protocol



## Workflow Selection

### Mode: Debugging
**Trigger**: "Fix this error", "Why is this failing?", "Debug...", crashes, test failures
**Protocol**: Load and apply the Debugging Workflow section from [core-engineering.md](references/core-engineering.md)

### Mode: Code Review
**Trigger**: "Review this", "Check for bugs", "PR review", assessing code quality
**Protocol**: Load and apply [review-workflow.md](references/review-workflow.md)

### Mode: Static Analysis
**Trigger**: "Static analysis", "Security scan", "Code quality check", "SAST", "Analyze code"
**Protocol**: Load and apply [static-analysis-workflow.md](references/static-analysis-workflow.md)

### Mode: Implementation (TDD)
**Trigger**: "Implement feature", "Write code", "Build..."
**Protocol**: Load and apply [tdd-protocol.md](references/tdd-protocol.md)

### Mode: Refactoring
**Trigger**: "Refactor", "Clean up", "Improve structure"
**Protocol**: Load and apply [refactoring-patterns.md](references/refactoring-patterns.md)

## Engineering Standards
Consult [core-engineering.md](references/core-engineering.md) for Universal Standards including TDD Protocol, Security (OWASP), Testing, and Debugging workflows.

