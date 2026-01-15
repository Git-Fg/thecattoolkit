---
name: testing-e2e
description: "Orchestrates end-to-end testing workflows coordinating browser automation with server verification. Use when validating complete user flows, testing multi-step scenarios, or verifying browser-server integration. Do not use for unit testing, API testing, isolated component testing, or documentation code examples → see generating-tests skill."
context: fork  # Required: Coordinates browser automation with server-side verification, orchestrates complete test workflows
user-invocable: false
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
---

# End-to-End Testing Orchestration



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



## Orchestration Pattern

1. **Coordinate**: Start server, launch browser
2. **Execute**: Run test steps in sequence
3. **Verify**: Check server state, browser output
4. **Report**: Consolidate results and findings

## Reference Materials

Test patterns and verification strategies are documented inline above.

**Note**: For isolated browser automation, use `driving-browser` skill. For server-only testing, use appropriate backend testing tools.
