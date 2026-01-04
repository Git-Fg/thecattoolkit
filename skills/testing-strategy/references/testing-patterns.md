# Testing Patterns Reference

Comprehensive testing patterns, templates, and best practices. Reference for `test-architect` subagent.

## Test Strategy Process

### PHASE 1 - Analyze

```bash
# Find existing tests
find . -name "*.test.*" -o -name "*.spec.*" -o -name "test_*"

# Check coverage if available
npm run coverage / pytest --cov

# Identify untested code
grep -rn "export\|public" --include="*.{js,ts,py}" | head -20
```

### PHASE 2 - Test Types

#### Unit Tests (70% of tests)
- Test individual functions/methods
- Mock external dependencies
- Fast execution (<100ms each)
- High coverage of business logic

```javascript
describe('calculateTotal', () => {
	it('should sum items correctly', () => {
		const items = [{ price: 10 }, { price: 20 }];
		expect(calculateTotal(items)).toBe(30);
	});

	it('should return 0 for empty array', () => {
		expect(calculateTotal([])).toBe(0);
	});

	it('should handle negative prices', () => {
		const items = [{ price: 10 }, { price: -5 }];
		expect(calculateTotal(items)).toBe(5);
	});
});
```

#### Integration Tests (20% of tests)
- Test component interactions
- Use real dependencies when practical
- Database, API, filesystem tests
- Medium speed (seconds)

```javascript
describe('UserService', () => {
	it('should create user and send welcome email', async () => {
		const user = await userService.create({ email: 'test@example.com' });

		expect(user.id).toBeDefined();
		expect(emailService.sent).toContainEqual({
			to: 'test@example.com',
			template: 'welcome',
		});
	});
});
```

#### E2E Tests (10% of tests)
- Test complete user flows
- Real browser/environment
- Slow but comprehensive
- Critical paths only

```javascript
describe('Checkout Flow', () => {
	it('should complete purchase', async () => {
		await page.goto('/products');
		await page.click('[data-testid="add-to-cart"]');
		await page.click('[data-testid="checkout"]');
		await page.fill('#email', 'test@example.com');
		await page.click('[data-testid="submit"]');

		await expect(page.locator('.confirmation')).toBeVisible();
	});
});
```

### PHASE 3 - Patterns

#### AAA Pattern

```javascript
it('should update user name', () => {
	// Arrange
	const user = new User({ name: 'Old Name' });

	// Act
	user.updateName('New Name');

	// Assert
	expect(user.name).toBe('New Name');
});
```

#### BDD Pattern

```javascript
describe('Shopping Cart', () => {
	describe('given an empty cart', () => {
		describe('when adding an item', () => {
			it('then cart should have one item', () => {
				// ...
			});
		});
	});
});
```

#### Data Builders

```javascript
const userBuilder = () => ({
	id: 1,
	name: 'Test User',
	email: 'test@example.com',
	withName: (name) => ({ ...userBuilder(), name }),
	withEmail: (email) => ({ ...userBuilder(), email }),
});

// Usage
const user = userBuilder().withName('Custom Name');
```

### PHASE 4 - Edge Cases

- Empty inputs (null, undefined, [], '')
- Boundary values (0, -1, MAX_INT)
- Invalid inputs (wrong types, malformed data)
- Error conditions (network failure, timeout)
- Concurrent operations (race conditions)
- Large inputs (performance, memory)

### PHASE 5 - Quality Metrics

```bash
# Coverage (aim for 80%+ on critical paths)
npm run coverage

# Check for flaky tests
npm test -- --repeat 10

# Test execution time
time npm test
```

## Output Format

```markdown
## Test Plan for [Feature/Component]

### Test Categories
1. Unit Tests (X tests)
   - [Function] - [scenarios to test]

2. Integration Tests (Y tests)
   - [Component interaction] - [scenarios]

3. E2E Tests (Z tests)
   - [User flow] - [critical path]

### Edge Cases Covered
- [List of edge cases]

### Mocking Strategy
- [What to mock and why]

### Test Files Created
- `path/to/test.spec.js` - [description]
```

## Anti-Patterns

- Testing implementation details
- Flaky tests (timing, order-dependent)
- Slow tests in unit test suite
- Testing framework code
- Over-mocking (testing mocks, not code)
- No assertions (tests that can't fail)
