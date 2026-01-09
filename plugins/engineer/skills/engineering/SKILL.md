---
name: engineering
description: |
  PROACTIVELY load this skill when the user asks to "debug this", "review my code", "refactor this file", or "security audit". Independent knowledge base for debugging, code review, refactoring, and testing. Can be invoked directly by main AI anytime for engineering guidance.
  <example>
  Context: User needs to debug an error
  user: "Debug this crash I'm getting when users login"
  assistant: "I'll load the engineering skill and route to the debugging workflow."
  </example>
  <example>
  Context: User wants code review
  user: "Review my changes before I commit"
  assistant: "I'll load the engineering skill and use the code review workflow."
  </example>
  <example>
  Context: User wants to refactor code
  user: "Refactor this file to use better patterns"
  assistant: "I'll load the engineering skill and apply the refactoring workflow."
  </example>
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, TodoWrite]
---

# Engineering Protocol Library

## Core Principles
1. **Verify, Don't Assume**: Run code/tests to confirm hypotheses.
2. **Atomic Changes**: One logical change per commit/step.
3. **Safety First**: Security and data integrity checks before functionality.

<foundational_knowledge>
## Critical: Read-First Protocol

**BEFORE executing ANY workflow in this skill that involves MODIFYING code, you MUST read:**

1. **`references/security-checklist.md`** - OWASP Top 10, security vulnerabilities, and safety protocols

**For READ-ONLY workflows (review, analyze), security checklist is recommended but not mandatory.**

**WHY:** Engineering workflows that modify code can introduce security vulnerabilities, data corruption, or system instability. The security checklist contains non-negotiable safety protocols.

**EXECUTION RULE:** Read foundational knowledge IMMEDIATELY upon workflow invocation. For modification workflows, this is non-negotiable.
</foundational_knowledge>



## Protocol Reference Index

### Debugging
- **Protocol**: `references/debug.md` - The 6-Phase Debug Protocol
- **When to Apply**: Errors, crashes, unexpected behavior, performance issues

### Code Review
- **Protocol**: `references/code-review.md` - PR Review Workflow
- **When to Apply**: Before merging PRs, peer review, quality assurance

### Refactoring
- **Protocol**: `references/refactor.md` - Refactoring Workflow
- **Reference**: `references/refactoring-patterns.md` - Code smells and SOLID principles
- **When to Apply**: Code cleanup, modernization, technical debt reduction, pattern improvement

### Security Audit
- **Protocol**: `references/security-audit.md` - Security Assessment Workflow
- **Reference**: `references/security-checklist.md` - OWASP Top 10 focus areas
- **When to Apply**: Vulnerability assessment, security review, compliance validation

### Test-Driven Development
- **Protocol**: `references/test-driven-development.md` - Red-Green-Refactor Workflow
- **Reference**: `references/tdd-protocol.md` - The Iron Law and methodology
- **When to Apply**: New features, bug fixes, refactoring, behavior changes

### Testing
- **Protocol**: `references/testing.md` - Testing Implementation Workflow
- **When to Apply**: Writing new tests, improving coverage, test maintenance

### Prototyping
- **Protocol**: `references/prototype.md` - Draft-then-Harden Workflow
- **When to Apply**: Complex features, exploring approaches, creative problem-solving