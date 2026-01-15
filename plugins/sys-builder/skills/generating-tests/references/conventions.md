# Test Conventions

## Import Pattern

```javascript
import { describe, it, expect } from 'vitest'
```

For DOM tests or tests needing mocks:

```javascript
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
```

## Test Structure Template

```javascript
import { describe, it, expect } from 'vitest'

describe('{Concept Name}', () => {
  describe('{Section Name}', () => {
    it('should {expected behavior} - Line {line}', () => {
      // Test implementation
    })
  })
})
```

## File Organization

### Directory Structure

```
tests/
├── fundamentals/              # Concepts 1-6
├── functions-execution/       # Concepts 7-8
├── web-platform/             # Concepts 9-10
├── object-oriented/          # Concepts 11-15
├── functional-programming/   # Concepts 16-19
├── async-javascript/         # Concepts 20-22
├── advanced-topics/          # Concepts 23-31
└── beyond/                   # Extended concepts
    └── {subcategory}/
```

### Naming Conventions

- **Standard tests:** `{concept-name}.test.js`
- **DOM tests:** `{concept-name}.dom.test.js`
- **Test descriptions:** `should {expected behavior} - Line {line}`

## Validation Checklist

Before finalizing tests:

- [ ] All testable code examples have corresponding tests
- [ ] Tests include line references to source documentation
- [ ] Tests use appropriate assertions (toBe, toEqual, toThrow, etc.)
- [ ] Tests follow naming convention: `{concept-name}.test.js`
- [ ] Tests are organized by documentation section
- [ ] DOM tests use `.dom.test.js` suffix
- [ ] Import patterns follow project conventions
- [ ] Tests pass when run with `vitest`
