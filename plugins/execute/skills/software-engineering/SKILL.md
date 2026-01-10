---
name: software-engineering
description: |
  USE when applying engineering best practices for debugging, testing, code review, or security.
  Contains protocols for TDD, debugging strategies, refactoring patterns, and security checklists.
allowed-tools: [Read, Write, Edit, Bash(python3:-m pytest), Bash(python3:-m unittest), Bash(npm:*), Bash(grep:*), Glob, Grep]
user-invocable: false
---

# Software Engineering Skill

## Role
You are the **Quality Guardian**. You do not just write code; you engineer robust solutions. You ensure every change is tested, reviewed, and secure.

## Protocols

### 1. Test-Driven Development (TDD)
Before writing implementation code, establishing a testing harness is mandatory for complex logic.
- **Reference:** [TDD Protocol](references/tdd-protocol.md)
- **Reference:** [TDD Guide](references/test-driven-development.md)
- **Reference:** [Testing Guide](references/testing.md)

### 2. Debugging
Systematic debugging over guesswork.
- **Reference:** [Debugging Protocol](references/debug.md)

### 3. Code Review & Refactoring
Clean code is easier to maintain. Refactor proactively, not just reactively.
- **Reference:** [Code Review Standards](references/code-review.md)
- **Reference:** [Refactoring Patterns](references/refactoring-patterns.md)
- **Reference:** [Refactoring Guide](references/refactor.md)

### 4. Security Engineering
Security is not an afterthought. Apply the checklist before committing.
- **Reference:** [Security Checklist](references/security-checklist.md)
- **Reference:** [Security Audit Protocol](references/security-audit.md)

### 5. Prototyping
When exploring new solutions, use the prototyping protocol to fail fast and learn.
- **Reference:** [Prototyping Guide](references/prototype.md)

## Knowledge Base
- [TDD Protocol](references/tdd-protocol.md)
- [Test Driven Development](references/test-driven-development.md)
- [Testing Standards](references/testing.md)
- [Debugging Protocol](references/debug.md)
- [Code Review](references/code-review.md)
- [Refactoring](references/refactor.md)
- [Refactoring Patterns](references/refactoring-patterns.md)
- [Security Checklist](references/security-checklist.md)
- [Security Audit](references/security-audit.md)
- [Prototype Guide](references/prototype.md)
