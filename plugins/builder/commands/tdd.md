---
description: |
  Execute test-driven development workflow using autonomous worker agent with Red-Green-Refactor cycle.
  <example>
  Context: User wants to implement a feature with TDD
  user: "Use TDD to add user authentication"
  assistant: "I'll delegate to the TDD agent to implement with Test-Driven Development."
  </example>
  <example>
  Context: Bug fix with TDD
  user: "Fix this bug using TDD"
  assistant: "I'll use the tdd command to fix the bug with test-driven approach."
  </example>
  <example>
  Context: Test-first development
  user: "Implement the API endpoints with TDD"
  assistant: "I'll delegate for TDD implementation of the API endpoints."
  </example>
allowed-tools: [Task, Read, Write, Edit, Glob, Grep, Bash]
argument-hint: [feature or bug description]
disable-model-invocation: true
---

## Objective
Execute TDD workflow for: $ARGUMENTS

## Deep Discovery Phase

Before delegating to the agent, gather comprehensive context to ensure efficient autonomous TDD execution.

### Step 1: Analyze Implementation Request

Determine the nature of the TDD task:

**Analyze $ARGUMENTS to classify:**
- **New Feature**: Adding new functionality, behavior, or capability
- **Bug Fix**: Fixing existing behavior that doesn't match expectations
- **Refactoring**: Improving code structure without changing behavior
- **API Change**: Modifying interfaces, endpoints, or contracts

### Step 2: Map Project Context

Gather essential project information:

**Technology Stack Identification:**
- Identify language (package.json, requirements.txt, Cargo.toml, go.mod, etc.)
- Identify framework (Express, Django, React, Rails, etc.)
- Identify test framework and runner (pytest, jest, cargo test, go test, vitest, etc.)
- Identify test utilities and libraries (testing-library, factory_bot, fixtures, etc.)

**Project Structure Mapping:**
- Locate source directories (src/, lib/, app/, internal/)
- Locate test directories (tests/, __tests__, spec/, test/)
- Check test organization patterns (co-located vs separated)
- Identify test configuration files (jest.config.js, pytest.ini, etc.)

**Existing Test Coverage:**
- Check if tests already exist for related functionality
- Identify test patterns and conventions used
- Look for test helpers, fixtures, or factory utilities
- Check coverage reports or configuration

### Step 3: Analyze Feature Requirements

Gather detailed requirements for implementation:

**For New Features:**
- Identify what behavior should be implemented
- Determine edge cases and error conditions
- Check for related existing code to understand patterns
- Look for similar implementations for consistency

**For Bug Fixes:**
- Understand current (buggy) behavior
- Identify expected (correct) behavior
- Locate related code and existing tests
- Check if bug is covered by existing failing tests

**For Refactoring:**
- Identify code to be refactored
- Understand current behavior (write characterization tests first)
- Check test coverage for affected code
- Ensure refactoring doesn't change external behavior

**For API Changes:**
- Identify interface changes required
- Check for versioning considerations
- Look for API contracts or documentation
- Identify breaking changes vs additions

### Step 4: Environment Verification

Check development environment state:
- Verify test framework is installed and configured
- Check that tests can run successfully
- Verify code quality tools (linters, formatters, type checkers)
- Check for pre-commit hooks or CI requirements

### Step 5: Delegation Package

Compile all gathered context into a comprehensive assignment for the worker agent.

## Delegation Phase

# Assignment

Execute the TDD workflow from the software-engineering skill to implement: $ARGUMENTS

**Context Provided:**
- Task Type: [new feature / bug fix / refactoring / API change]
- Technology Stack: [language, framework, test framework, test utilities]
- Project Structure: [source dirs, test dirs, test patterns]
- Requirements: [feature description, edge cases, related code]
- Existing Tests: [test coverage, patterns, helpers available]

**Follow the Red-Green-Refactor cycle:**
1. **RED**: Write failing tests for the feature/fix
   - Test must fail for the RIGHT reason (feature missing, not typo)
   - Cover edge cases and error conditions
   - Use existing test patterns and helpers
2. **GREEN**: Write minimal code to pass tests
   - Implement ONLY what's needed to pass
   - Hard-coded return values acceptable initially
   - Don't add extra features or optimizations
3. **REFACTOR**: Improve code while tests stay green
   - Clean up naming and structure
   - Remove duplication
   - Improve algorithms and design
   - Run tests frequently during refactoring

**Work autonomously using Uninterrupted Flow:**
- Self-verify via test commands after each cycle
- Log all test results and code changes
- Create HANDOFF.md only for authentication gates or critical failures
- DO NOT use ask_user during execution

**Quality Standards:**
- Read references/tdd-protocol.md before starting
- Every new function/method must have a test
- Watch each test fail before implementing (Iron Law)
- All tests must pass before completing
- Code must be refactored while tests remain green
- Output must be pristine (no errors, warnings from linters/type checkers)

# Context

You are executing in isolated context to prevent main chat overflow. The software-engineering skill provides comprehensive TDD methodology with safety protocols and best practices.
All relevant project context has been gathered for you.

Execute via worker agent.

## Success Criteria

- [ ] Task type properly classified (feature/fix/refactor/API)
- [ ] Project context fully mapped (stack, structure, test patterns)
- [ ] Requirements analyzed (edge cases, related code, existing tests)
- [ ] Environment verified (test framework, tools, coverage)
- [ ] Agent receives comprehensive context package
- [ ] Red-Green-Refactor cycle followed correctly
- [ ] All tests pass
- [ ] Code refactored while tests remain green
- [ ] No linter/type checker warnings
