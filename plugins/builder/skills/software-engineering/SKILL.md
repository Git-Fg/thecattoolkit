---
name: software-engineering
description: |
  Code manipulation patterns, engineering protocols, and development methodologies. Defines WHAT code patterns to apply (TDD, Debugging, Refactoring, Security). HOW to execute is defined by execution-core skill.
  <example>
  Context: Need to debug code
  user: "Debug this error"
  assistant: "I'll apply software-engineering debugging protocols to identify and fix the issue."
  </example>
  <example>
  Context: Code review needed
  user: "Review my changes"
  assistant: "I'll use software-engineering code review patterns to assess the changes."
  </example>
  <example>
  Context: TDD workflow
  user: "Implement with TDD"
  assistant: "I'll follow software-engineering TDD protocols (Red-Green-Refactor)."
  </example>
allowed-tools: Read Write Edit Bash Glob Grep
---

# Software Engineering Protocols

## Core Purpose

**This skill defines WHAT code patterns and engineering methodologies to apply.**

It answers: "What protocols should I use for debugging, testing, refactoring?" (not "How to execute them").

**HOW to execute** (Uninterrupted Flow, Self-Verification, Handoffs) is defined by `execution-core` skill.

## Skill Contents

**Engineering Protocols:**
- `references/debug.md` - Systematic debugging (6-phase protocol)
- `references/code-review.md` - Code review workflow
- `references/refactor.md` - Refactoring methodology
- `references/security-audit.md` - Security assessment workflow
- `references/security-checklist.md` - OWASP Top 10 and safety protocols
- `references/test-driven-development.md` - TDD Red-Green-Refactor workflow
- `references/tdd-protocol.md` - TDD methodology and iron law
- `references/testing.md` - Testing implementation workflow
- `references/prototype.md` - Draft-then-harden workflow
- `references/refactoring-patterns.md` - Code smells and SOLID principles

## Foundational Knowledge

### Critical: Security-First Protocol

**BEFORE executing ANY workflow in this skill that involves MODIFYING code, you MUST read:**

**`references/security-checklist.md`** - OWASP Top 10, security vulnerabilities, and safety protocols

**For READ-ONLY workflows (review, analyze), security checklist is recommended but not mandatory.**

**WHY:** Engineering workflows that modify code can introduce security vulnerabilities, data corruption, or system instability. The security checklist contains non-negotiable safety protocols.

**EXECUTION RULE:** Read foundational knowledge IMMEDIATELY upon workflow invocation. For modification workflows, this is non-negotiable.

## Core Principles

1. **Verify, Don't Assume**: Run code/tests to confirm hypotheses
2. **Atomic Changes**: One logical change per commit/step
3. **Safety First**: Security and data integrity checks before functionality
4. **Evidence-Based**: Collect proof before making changes

## Protocol Reference Index

### Debugging
- **Protocol**: `references/debug.md` - The 6-Phase Debug Protocol
- **When to Apply**: Errors, crashes, unexpected behavior, performance issues
- **Core Method**: Scientific Method (Hypothesis → Test → Fix)

### Code Review
- **Protocol**: `references/code-review.md` - PR Review Workflow
- **When to Apply**: Before merging PRs, peer review, quality assurance
- **Focus**: Security, correctness, maintainability

### Refactoring
- **Protocol**: `references/refactor.md` - Refactoring Workflow
- **Reference**: `references/refactoring-patterns.md` - Code smells and SOLID principles
- **When to Apply**: Code cleanup, modernization, technical debt reduction, pattern improvement
- **Rule**: Tests must pass before and after

### Security Audit
- **Protocol**: `references/security-audit.md` - Security Assessment Workflow
- **Reference**: `references/security-checklist.md` - OWASP Top 10 focus areas
- **When to Apply**: Vulnerability assessment, security review, compliance validation
- **Priority**: Security over functionality

### Test-Driven Development
- **Protocol**: `references/test-driven-development.md` - Red-Green-Refactor Workflow
- **Reference**: `references/tdd-protocol.md` - The Iron Law and methodology
- **When to Apply**: New features, bug fixes, refactoring, behavior changes
- **Cycle**: Write failing test → Write minimal code → Refactor

### Testing
- **Protocol**: `references/testing.md` - Testing Implementation Workflow
- **When to Apply**: Writing new tests, improving coverage, test maintenance
- **Types**: Unit, integration, end-to-end

### Prototyping
- **Protocol**: `references/prototype.md` - Draft-then-Harden Workflow
- **When to Apply**: Complex features, exploring approaches, creative problem-solving
- **Method**: Fast prototype → Validate → Harden for production

## Behavioral Integration

### Using execution-core for HOW

**This skill defines WHAT engineering patterns to apply. HOW to execute is in execution-core:**

- **Uninterrupted Flow** - Apply engineering protocols without pausing
- **Self-Verification** - Use CLI commands to verify fixes and changes
- **Authentication Gates** - Handle auth errors per execution-core protocols
- **Handoff Protocol** - Create HANDOFF.md for blockers per execution-core standards

**Example Integration:**

When debugging:
1. Apply `references/debug.md` 6-phase protocol (software-engineering)
2. Execute in Uninterrupted Flow (execution-core)
3. Use Self-Verification Points to confirm fixes (execution-core)
4. Create HANDOFF.md if blocked by auth/dependencies (execution-core)

When doing TDD:
1. Follow `references/test-driven-development.md` Red-Green-Refactor cycle (software-engineering)
2. Execute each phase in Uninterrupted Flow (execution-core)
3. Verify tests pass using Self-Verification Points (execution-core)

### Standards Hierarchy

```
execution-core (HOW to behave)
    ↓
software-engineering (WHAT patterns to apply)
    ↓
director/worker agents (Execute using these standards)
```

## Protocol Usage Patterns

### For Director Agent

**When orchestrating engineering work:**

```
Use software-engineering protocols to define:
- Debugging approach for complex errors
- TDD cycle for feature implementation
- Security audit checklist for sensitive changes
- Code review standards for quality

Execute using execution-core behavioral standards:
- Uninterrupted Flow during implementation
- Self-Verification after each change
- Handoff for blockers
```

### For Worker Agent

**When executing engineering tasks:**

```
Apply software-engineering protocols:
1. Read relevant reference file (debug.md, tdd-protocol.md, etc.)
2. Follow the methodology step-by-step
3. Execute in Uninterrupted Flow (execution-core)
4. Verify changes programmatically (execution-core)
5. Create HANDOFF.md if blocked (execution-core)
```

### For Commands

**When users request engineering work:**

```
Route to appropriate software-engineering protocol:
- /debug → references/debug.md
- /tdd → references/test-driven-development.md
- /review → references/code-review.md
- /refactor → references/refactor.md
- /security-audit → references/security-audit.md

Delegate to worker agent with:
- Engineering protocol to follow (software-engineering)
- Behavioral standards to use (execution-core)
```

## Protocol Selection Guide

### Choosing the Right Protocol

**New Feature Development:**
- Start with `references/test-driven-development.md` (TDD)
- Use `references/testing.md` for test implementation
- Apply `references/security-checklist.md` throughout

**Bug Fixes:**
- Start with `references/debug.md` (6-phase debugging)
- Use `references/testing.md` to prevent regressions
- Apply `references/security-checklist.md` if security-related

**Code Quality:**
- Use `references/code-review.md` for PRs
- Apply `references/refactor.md` for improvements
- Reference `references/refactoring-patterns.md` for specific patterns

**Security Work:**
- Start with `references/security-checklist.md` (mandatory read)
- Apply `references/security-audit.md` for assessments
- Use `references/testing.md` to verify fixes

**Exploration:**
- Use `references/prototype.md` for complex problems
- Transition to TDD after validation
- Document learnings for future reference

## Key Principles

1. **Pattern-Driven**: Apply established engineering patterns
2. **Security-First**: Always check security checklist before modifying code
3. **Evidence-Based**: Verify hypotheses with tests and CLI commands
4. **Atomic Changes**: One logical change per iteration
5. **Behavioral Separation**: WHAT (engineering) separate from HOW (execution-core)
