# Common Test Patterns

## Pattern 1: Output Verification

```javascript
it('should produce expected output - Line X', () => {
  // Execute code
  const result = /* code from documentation */

  // Assert
  expect(result).toBe(/* expected value */)
})
```

## Pattern 2: Side Effect Testing

```javascript
it('should mutate object - Line X', () => {
  const obj = { count: 0 }

  // Execute code that mutates
  increment(obj)

  expect(obj.count).toBe(1)
})
```

## Pattern 3: Error Handling

```javascript
it('should throw error - Line X', () => {
  expect(() => {
    problematicFunction()
  }).toThrow(/* expected error */)
})
```

## Pattern 4: Async Operations

```javascript
it('should handle async operation - Line X', async () => {
  const result = await asyncFunction()
  expect(result).toEqual(/* expected */)
})
```

## Special Case Patterns

| Case | Pattern |
|------|---------|
| Browser-only APIs | Mock or skip with note |
| Timing-dependent code | Use `vi.useFakeTimers()` |
| Async code | Use `async/await` with proper assertions |
| Intentional errors | Use `expect(() => {...}).toThrow()` |
