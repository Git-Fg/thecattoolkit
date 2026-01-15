# Test Writing Methodology

## Four-Phase Approach

Follow these four phases to create comprehensive tests:

### Phase 1: Code Example Extraction

Scan the concept page for all code examples and categorize them:

| Category | Characteristics | Action |
|----------|-----------------|--------|
| **Testable** | Has `console.log` with output comments, returns values | Write tests |
| **DOM-specific** | Uses `document`, `window`, DOM APIs, event handlers | Write DOM tests (separate file) |
| **Error examples** | Intentionally throws errors, demonstrates failures | Write tests with `toThrow` |
| **Conceptual** | ASCII diagrams, pseudo-code, incomplete snippets | Skip (document why) |
| **Browser-only** | Uses browser APIs not available in jsdom | Skip or mock |

### Phase 2: Determine Test File Structure

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

**File naming:**
- Standard tests: `{concept-name}.test.js`
- DOM tests: `{concept-name}.dom.test.js`

### Phase 3: Convert Examples to Tests

For each testable code example:

1. Identify the expected output (from `console.log` comments or documented behavior)
2. Convert to `expect` assertions
3. Add source line reference in comments
4. Group related tests in `describe` blocks matching documentation sections

### Phase 4: Handle Special Cases

| Case | Solution |
|------|----------|
| Browser-only APIs | Use jsdom environment or skip with note |
| Timing-dependent code | Use `vi.useFakeTimers()` or test the logic, not timing |
| Side effects | Capture output or test mutations |
| Intentional errors | Use `expect(() => {...}).toThrow()` |
| Async code | Use `async/await` with proper assertions |
