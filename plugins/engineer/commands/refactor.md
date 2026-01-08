---
description: |
  Execute systematic refactoring protocol to improve code structure without altering external behavior.
  <example>
  Context: Code needs improvement
  user: "Refactor this file to use better patterns"
  assistant: "I'll delegate to the refactoring agent for systematic code improvement."
  </example>
  <example>
  Context: Technical debt reduction
  user: "Refactor the authentication module"
  assistant: "I'll use the refactor command to improve the code structure."
  </example>
  <example>
  Context: Performance optimization through refactoring
  user: "Refactor this loop for better performance"
  assistant: "I'll delegate to the refactoring agent for optimization."
  </example>
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
argument-hint: [file path or code description to refactor]
---

## Objective
Execute refactoring workflow for: $ARGUMENTS

## Deep Discovery Phase

Before delegating to the agent, gather comprehensive context to ensure safe and effective refactoring.

### Step 1: Analyze Refactoring Request

Determine the nature of the refactoring task:

**Analyze $ARGUMENTS to classify:**
- **Code Quality**: Improve maintainability, readability, or structure
- **Performance**: Optimize algorithms or reduce complexity
- **Technical Debt**: Address anti-patterns or legacy code
- **Design Patterns**: Apply established patterns for better architecture
- **Module Extraction**: Extract reusable components or utilities

### Step 2: Map Project Context

Gather essential project information:

**Technology Stack Identification:**
- Identify language and framework
- Identify test framework and runner
- Identify code quality tools (linters, formatters, type checkers)

**Project Structure Mapping:**
- Locate source files to be refactored
- Identify related files and dependencies
- Check test coverage for affected code
- Locate test files for the target code

**Current State Analysis:**
- Run existing tests to establish baseline
- Check for linter/formatter warnings
- Identify code complexity metrics if available
- Review git history for recent changes

### Step 3: Safety Verification

Ensure refactoring can be performed safely:

**Test Coverage Check:**
- Verify tests exist for code to be refactored
- If no tests exist, recommend TDD approach first
- Identify test utilities and helpers available

**Risk Assessment:**
- Identify high-risk areas (authentication, payment, data processing)
- Check for critical paths that require extra caution
- Verify rollback capability (git status clean)

### Step 4: Delegation Package

Compile all gathered context into a comprehensive assignment for the task-executor agent.

## Delegation Phase

<assignment>
Execute the refactoring workflow from the engineering skill to improve: $ARGUMENTS

**Context Provided:**
- Refactoring Type: [code quality / performance / technical debt / design patterns / module extraction]
- Technology Stack: [language, framework, test framework, quality tools]
- Project Structure: [source files, related files, tests]
- Current State: [test status, linter warnings, complexity metrics]
- Risk Assessment: [high-risk areas, critical paths, rollback capability]

**Follow the safe refactoring protocol:**
1. **Establish Safety Net**: Run tests BEFORE any changes to verify baseline
2. **Identify Smells**: Long methods, cognitive complexity, duplication
3. **Apply Pattern**: Choose appropriate refactoring pattern
4. **Verify**: Run tests AFTER each change to ensure no behavioral changes

**Work autonomously using Uninterrupted Flow:**
- Self-verify via test commands after each refactoring step
- Log all test results and code changes
- Create HANDOFF.md only for critical failures
- DO NOT use AskUserQuestion during execution

**Safety Reminders:**
- Read the security checklist from the engineering skill before modifying code
- Read the refactoring patterns from the engineering skill for improvement patterns
- Ensure tests pass before AND after refactoring
- No behavioral changes should occur
- Code must be demonstrably cleaner (lower complexity, better naming)
</assignment>

<context>
You are executing in isolated context to perform safe refactoring. The engineering skill provides comprehensive refactoring methodology with safety protocols and best practices.
All relevant project context has been gathered for you.
</context>

Execute via task-executor agent.

## Success Criteria

- [ ] Refactoring type properly classified
- [ ] Project context fully mapped (stack, structure, tests)
- [ ] Safety net established (tests pass before changes)
- [ ] Risk assessment completed
- [ ] Agent receives comprehensive context package
- [ ] Tests pass before AND after refactoring
- [ ] Code is demonstrably cleaner
- [ ] No behavioral changes occurred
- [ ] No linter/type checker warnings
