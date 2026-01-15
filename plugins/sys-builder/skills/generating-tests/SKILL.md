---
name: generating-tests
description: "Follows project conventions, extracts examples from documentation, converts them to tests, and ensures documentation accuracy through automated testing. PROACTIVELY Use when generating comprehensive Vitest tests for code examples in JavaScript concept documentation pages. Do not use for end-to-end browser automation, user flow testing, or browser-server integration → see testing-e2e skill."
user-invocable: true
allowed-tools: [Read, Write, Bash, Grep, Glob]
---

# Test Writer for Documentation Code Examples

Extracts, converts, and verifies documentation examples.



## When to Use This Skill

Use this skill when you need to:
- Generate tests for new concept documentation pages
- Add tests when updating existing documentation examples
- Verify documentation accuracy through automated testing
- Ensure all code examples in documentation work as documented
- Create comprehensive test coverage for educational content

## Test Writing Methodology

Follow a four-phase approach to create comprehensive tests:

1. **Extract & Categorize** - Scan documentation for code examples and categorize by type
2. **Determine Structure** - Organize tests by project conventions
3. **Convert to Tests** - Transform examples into proper Vitest tests
4. **Handle Special Cases** - Address DOM, async, error, and edge cases

**See:** `references/methodology.md` for complete four-phase methodology

## Quick Start Pattern

### Basic Transformation

```javascript
// Documentation
console.log('Hello, World!') // Hello, World!

// Test
it('should produce expected output - Line 1', () => {
  const result = /* code from documentation */
  expect(result).toBe('Hello, World!')
})
```

### Error Testing

```javascript
// Test error cases
it('should throw error - Line X', () => {
  expect(() => problematicFunction()).toThrow('Expected error')
})
```

### Async Testing

```javascript
// Test async operations
it('should handle async - Line X', async () => {
  const result = await asyncFunction()
  expect(result).toEqual(/* expected */)
})
```

**See:** `references/examples.md` for complete worked examples

## Test Conventions

### Import Pattern
```javascript
import { describe, it, expect } from 'vitest'
```

### File Naming
- Standard tests: `{concept-name}.test.js`
- DOM tests: `{concept-name}.dom.test.js`

### Test Structure
```javascript
describe('{Concept Name}', () => {
  it('should {expected behavior} - Line {line}', () => {
    // Implementation
  })
})
```

**See:** `references/conventions.md` for complete conventions and validation checklist

## Common Patterns

- **Output Verification**: Assert expected results
- **Side Effect Testing**: Test mutations and state changes
- **Error Handling**: Test error conditions
- **Async Operations**: Handle promises and async/await
- **DOM Testing**: Use jsdom environment for browser APIs

**See:** `references/patterns.md` for detailed pattern examples

## DOM Testing

For DOM-related tests:

```javascript
/**
 * @vitest-environment jsdom
 */
import { vi } from 'vitest'

beforeEach(() => {
  document.body.innerHTML = '<div id="app"></div>'
})
```

**See:** `references/dom-testing.md` for complete DOM testing guide

## Running Tests

```bash
# Run all tests
vitest

# Run specific file
vitest run {concept-name}.test.js

# Run with coverage
vitest run --coverage
```

## Reference Materials

**Core Implementation:**
- `references/methodology.md` - Four-phase test writing methodology
- `references/conventions.md` - Project conventions and validation checklist
- `references/examples.md` - Complete worked examples
- `references/patterns.md` - Common test patterns and examples
- `references/dom-testing.md` - DOM testing setup and patterns

**Quality Standards:**
Each test must be traceable, use appropriate assertions, follow naming conventions, include clear descriptions, handle edge cases, and pass when executed.
