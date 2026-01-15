# DOM Testing Guide

## Environment Setup

For DOM-related tests:

```javascript
/**
 * @vitest-environment jsdom
 */

import { describe, it, expect } from 'vitest'
import { vi } from 'vitest'

beforeEach(() => {
  // Setup DOM environment
  document.body.innerHTML = '<div id="app"></div>'
})

afterEach(() => {
  // Cleanup
  vi.clearAllMocks()
})
```

## DOM-Specific Test Categories

### DOM Test Classification

| Category | Characteristics | Action |
|----------|-----------------|--------|
| **DOM-specific** | Uses `document`, `window`, DOM APIs, event handlers | Write DOM tests (separate file) |
| **Browser-only** | Uses browser APIs not available in jsdom | Skip or mock |

### DOM Test File Naming

- DOM tests: `{concept-name}.dom.test.js`
- Use `.dom.test.js` suffix to distinguish from standard tests

## DOM Test Patterns

### Event Handler Testing

```javascript
it('should call handler on click - Line X', () => {
  const handler = vi.fn()
  const button = document.createElement('button')
  button.addEventListener('click', handler)
  button.click()

  expect(handler).toHaveBeenCalledTimes(1)
})
```

### DOM Manipulation Testing

```javascript
it('should update DOM content - Line X', () => {
  const element = document.getElementById('app')
  element.textContent = 'New content'

  expect(element.textContent).toBe('New content')
})
```

## Running Tests

### Execute Tests

```bash
# Run all tests
vitest

# Run specific test file
vitest run {concept-name}.test.js

# Run DOM tests specifically
vitest run {concept-name}.dom.test.js

# Run in watch mode
vitest

# Run with coverage
vitest run --coverage
```
