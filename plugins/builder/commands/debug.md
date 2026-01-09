---
description: |
  Execute systematic debugging protocol using autonomous worker agent for comprehensive bug analysis and fixing.
  <example>
  Context: User encounters a bug
  user: "Debug this crash I'm getting"
  assistant: "I'll delegate to the debugging agent for systematic bug analysis."
  </example>
  <example>
  Context: Test failures need investigation
  user: "Debug these failing tests"
  assistant: "I'll use the debug command to analyze and fix the test failures."
  </example>
  <example>
  Context: Performance issue
  user: "Debug why the API is slow"
  assistant: "I'll delegate to the debugging agent for performance analysis."
  </example>
allowed-tools: [Task, Read, Write, Edit, Glob, Grep, Bash]
argument-hint: [error description or bug report]
disable-model-invocation: true
---

## Objective
Execute debugging protocol for: $ARGUMENTS

## Deep Discovery Phase

Before delegating to the agent, gather comprehensive context to ensure efficient autonomous execution.

### Step 1: Analyze Error Type

Determine the nature of the debugging task:

**Analyze $ARGUMENTS to classify:**
- **Runtime Error**: Application crashes, exceptions, unhandled errors
- **Logic Error**: Wrong behavior, incorrect output, edge cases
- **Performance Issue**: Slow execution, memory leaks, bottlenecks
- **Test Failure**: Failing tests, broken builds, CI failures
- **Security Vulnerability**: OWASP issues, injection, auth bypass

### Step 2: Map Project Context

Gather essential project information:

**Technology Stack Identification:**
- Identify language (package.json, requirements.txt, Cargo.toml, go.mod, etc.)
- Identify framework (Express, Django, React, Rails, etc.)
- Identify test runner (pytest, jest, cargo test, go test, etc.)

**Project Structure Mapping:**
- Locate entry points (main, index, app)
- Identify source directories (src/, lib/, app/)
- Locate test directories (tests/, __tests__, spec/)
- Check for configuration files (.env.*, config/)

**Version Control State:**
- Check current branch and recent commits
- Verify git status for uncommitted changes
- Identify repository state for debugging context

### Step 3: Capture Error Evidence

Gather concrete error information:

**For Runtime Errors:**
- Capture full stack trace
- Identify error file and line number
- Note error type and message
- Check if error is reproducible

**For Logic Errors:**
- Identify expected vs actual behavior
- Locate relevant code sections
- Check input data and assumptions
- Review edge cases

**For Test Failures:**
- Run tests to capture full output
- Identify which tests fail
- Check error messages and assertions
- Review test setup and fixtures

**For Performance Issues:**
- Identify slow operations
- Check for N+1 queries or nested loops
- Review algorithmic complexity
- Look for missing caching or pagination

**For Security Issues:**
- Identify vulnerability type
- Check OWASP Top 10 categories
- Locate affected code paths
- Review data handling and sanitization

### Step 4: Environment Verification

Check development environment state:
- Verify dependencies are installed
- Check environment variables configuration
- Verify database/connection status
- Check for running services/daemons

### Step 5: Delegation Package

Compile all gathered context into a comprehensive assignment for the worker agent.

## Delegation Phase

# Assignment

Execute the debugging workflow from the software-engineering skill to investigate and fix: $ARGUMENTS

**Context Provided:**
- Error Type: [classification from Step 1]
- Technology Stack: [language, framework, test runner]
- Project Structure: [entry points, source dirs, test dirs]
- Error Evidence: [stack traces, test output, behavior description]
- Environment State: [git status, dependencies, configuration]

**Follow systematic debugging protocol:**
1. Analyze the error and gather context using provided information
2. Identify root cause using systematic hypothesis testing
3. Implement targeted fix following security best practices
4. Verify the fix resolves the issue (run tests, check behavior)

**Work autonomously using Uninterrupted Flow:**
- Collect evidence via CLI tools autonomously
- Implement fixes based on your analysis
- Verify by running tests and checking behavior
- Create HANDOFF.md only for unrecoverable blockers
- DO NOT use ask_user during execution

**Security Reminders:**
- Read the security checklist from the software-engineering skill before modifying code
- Sanitize inputs and validate data
- Check for authentication/authorization issues
- Ensure no sensitive data exposure in fixes

# Context

You are executing in isolated context to perform thorough debugging. The software-engineering skill provides comprehensive debugging methodology with systematic analysis protocols.
All relevant project context has been gathered for you.

Execute via worker agent.

## Success Criteria

- [ ] Error type and nature properly classified
- [ ] Project context fully mapped (stack, structure, state)
- [ ] Error evidence captured (stack traces, output, behavior)
- [ ] Environment verified and documented
- [ ] Agent receives comprehensive context package
- [ ] Bug resolved and verified
- [ ] No regressions introduced
