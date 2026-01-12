# Example: Creating a Code Analyzer Router

## Overview

This example shows how to create a router skill that intelligently routes code analysis requests to specialized analyzer skills.

## Step-by-Step Creation

### Step 1: Identify Routes

**Analysis Types:**
- Security analysis → security-analyzer skill
- Performance analysis → performance-analyzer skill
- Code quality → quality-analyzer skill
- Architecture review → architecture-analyzer skill

### Step 2: Create Directory

```bash
mkdir -p code-analyzer-router
cd code-analyzer-router
```

### Step 3: Use Router Template

```markdown
---
name: code-analyzer-router
description: "USE when analyzing code quality, security, or performance. Routes analysis requests to specialized analyzers based on user intent."
allowed-tools: [Read, Grep, Skill]
---

# Code Analysis Router

## Activation Triggers

Router activates when users ask to:
- "analyze code security"
- "check performance"
- "review code quality"
- "assess architecture"

## Routing Logic

### Route 1: Security Analysis
**Triggers:** security, vulnerabilities, XSS, injection, CVE
**Routes to:** security-analyzer
**Pattern:** "Analyze code for security vulnerabilities"

**Example:**
```
User: "Check this code for security issues"
Router: Detects "security" → Routes to security-analyzer
```

### Route 2: Performance Analysis
**Triggers:** performance, slow, optimize, bottleneck, memory
**Routes to:** performance-analyzer
**Pattern:** "Analyze code for performance issues"

**Example:**
```
User: "Why is this function slow?"
Router: Detects "slow" → Routes to performance-analyzer
```

### Route 3: Code Quality
**Triggers:** clean code, best practices, maintainability, refactor
**Routes to:** quality-analyzer
**Pattern:** "Review code quality and maintainability"

**Example:**
```
User: "How can I improve this code?"
Router: Detects "improve" → Routes to quality-analyzer
```

### Default Route
**Routes to:** quality-analyzer (general analysis)
**Pattern:** When no specific route matches
```

## Testing

### Test Cases

```bash
# Test 1: Security
User: "Check for SQL injection vulnerabilities"
Expected: Routes to security-analyzer
Result: ✓ Pass

# Test 2: Performance
User: "Why is this loop so slow?"
Expected: Routes to performance-analyzer
Result: ✓ Pass

# Test 3: Quality
User: "How can I make this more maintainable?"
Expected: Routes to quality-analyzer
Result: ✓ Pass

# Test 4: Ambiguous
User: "Review this code"
Expected: Routes to quality-analyzer (default)
Result: ✓ Pass
```

## Success Criteria

- [x] Routes match user intent >90% of time
- [x] Default route handles unknown requests
- [x] Confidence levels appropriate
- [x] Delegation format consistent
- [x] Response time <100ms

## Key Principles

### 1. Clear Trigger Keywords
Each route should have distinct, non-overlapping keywords.

### 2. Always Include Default Route
Handle unknown requests gracefully.

### 3. Proper Delegation
Router analyzes and routes - it doesn't implement the analysis itself.

### 4. Confidence Levels
Include confidence indicators when routing is ambiguous.

## Summary

Creating a router skill involves:
1. Identifying distinct routes
2. Defining keyword triggers
3. Implementing routing logic
4. Testing with real queries
5. Providing clear delegation

This example demonstrates the Router Template for intelligent request routing to specialized skills.
