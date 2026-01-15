---
name: testing-e2e
description: "Orchestrates end-to-end testing workflows coordinating browser automation with server verification. Use when validating complete user flows, testing multi-step scenarios, or verifying browser-server integration. Do not use for unit testing, API testing, or isolated component testing."
context: fork
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
---

# End-to-End Testing Orchestration

## Core Purpose

Orchestrates complete E2E test workflows by coordinating browser automation with server-side verification. Validates user flows across the full stack.

## Test Workflow

### 1. Test Planning
- Identify user flows to validate
- Define success criteria
- Map test scenarios to requirements

### 2. Environment Setup
- Start server (if needed)
- Configure browser automation
- Prepare test data

### 3. Test Execution
- Run browser automation steps
- Verify server responses
- Capture screenshots/logs on failure

### 4. Results Analysis
- Compare actual vs expected outcomes
- Generate test reports
- Identify failures and root causes

## Test Types

### User Flow Testing
- Multi-step user journeys
- Critical paths (signup, checkout, etc.)
- Cross-feature workflows

### Integration Testing
- Browser-server communication
- Data flow validation
- State management verification

### Regression Testing
- Prevent feature breaks
- Validate existing functionality
- Compare with baseline behavior

## Orchestration Pattern

1. **Coordinate**: Start server, launch browser
2. **Execute**: Run test steps in sequence
3. **Verify**: Check server state, browser output
4. **Report**: Consolidate results and findings

## Reference Materials

Test patterns and verification strategies are documented inline above.

**Note**: For isolated browser automation, use `driving-browser` skill. For server-only testing, use appropriate backend testing tools.
