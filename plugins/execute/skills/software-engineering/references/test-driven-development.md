# Workflow: Test-Driven Development

## Purpose
Implement features and bug fixes using the Red-Green-Refactor cycle. Write tests first, watch them fail, write minimal code to pass, then refactor while tests remain green.

## Required Reading
- `references/tdd-protocol.md` - The Iron Law and Red-Green-Refactor methodology

## When to Use TDD

**Always use TDD for:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions:**
- Throwaway prototypes
- Generated code
- Configuration files

## Process

### Step 1: Define the Feature
Be specific about what you're implementing:
- Write a clear description of the feature/bug
- Break down into smallest testable unit

### Step 2: RED - Write a Failing Test

1. **Write the test**
   ```python
   def test_specific_behavior():
       # Arrange
       setup_test_data()

       # Act
       result = function_under_test()

       # Assert
       assert result == expected_value
   ```

2. **Run the test to verify it fails**
   ```bash
   pytest test_file.py::test_specific_behavior
   ```

3. **Confirm failure is expected**
   - Should fail because feature doesn't exist yet
   - If it passes, fix the test
   - If it fails for wrong reason, fix the test

**CRITICAL:** You must see the test fail for the right reason before proceeding.

### Step 3: GREEN - Write Minimal Code

1. **Write ONLY what's needed to pass the test**
   ```python
   def function_under_test():
       return expected_value  # Hard-coded is okay!
   ```

2. **Run the test**
   ```bash
   pytest test_file.py::test_specific_behavior
   ```

3. **Verify it passes**
   - Don't add extra features
   - Don't optimize
   - Just make the test pass

### Step 4: REFACTOR - Clean Up

1. **Improve the code while tests pass**
   - Fix naming
   - Remove duplication
   - Improve structure
   - Add better algorithms

2. **Run tests frequently**
   ```bash
   pytest test_file.py
   ```

3. **If tests break, undo changes**
   - Tests are your safety net
   - Revert and try different approach

### Step 5: Repeat for Next Feature

1. **Write next failing test**
2. **Make it pass with minimal code**
3. **Refactor while green**
4. **Continue until feature complete**

## TDD for Bug Fixes

### Pattern: Write Reproduction Test

1. **Write test that reproduces the bug**
   ```python
   def test_bug_description():
       # Set up conditions that trigger bug
       buggy_input = create_buggy_input()

       # Execute
       result = function_under_test(buggy_input)

       # Assert on expected (correct) behavior
       assert result != buggy_behavior  # Bug produces wrong result
       assert result == correct_behavior  # Should produce this instead
   ```

2. **Run test → fails (RED)** - Confirms bug exists

3. **Fix with minimal change**
   ```python
   def function_under_test(input):
       # Add minimal fix
       if input == buggy_condition:
           return correct_behavior
       # ... rest of code
   ```

4. **Run test → passes (GREEN)** - Bug is fixed

5. **Run full test suite** - Verify no regressions

## Example: Building a Calculator

### Test 1: Addition
```python
def test_calculator_adds_two_numbers():
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5
```

**Run test → Fails** (Calculator doesn't exist)

**Minimal implementation:**
```python
class Calculator:
    def add(self, a, b):
        return 5
```

**Run test → Passes**

### Test 2: Subtraction
```python
def test_calculator_subtracts_two_numbers():
    calc = Calculator()
    result = calc.subtract(5, 3)
    assert result == 2
```

**Run test → Fails** (no subtract method)

**Minimal implementation:**
```python
class Calculator:
    def add(self, a, b):
        return a + b  # Refactored from hard-coded

    def subtract(self, a, b):
        return 2  # Hard-coded
```

**Run test → Passes**

### Continue for multiply, divide...

### Refactoring Phase
After all basic operations work:
```python
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        return a / b
```

## Success Criteria

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Code is refactored while tests remain green
- [ ] Output pristine (no errors, warnings)

Can't check all boxes? You skipped TDD. Start over.

## Common Mistakes

### Writing Code First
**Mistake:** Implementing function before writing test
**Solution:** DELETE THE CODE. Write test first.

### Test Passes Immediately
**Mistake:** Test passes without implementation
**Reason:** Feature already exists or test is wrong
**Solution:** Fix test to actually test missing functionality

### Too Much Implementation
**Mistake:** Adding extra features in GREEN phase
**Solution:** Only write code needed to pass the test

### Skipping Refactor
**Mistake:** Leaving ugly hard-coded solutions
**Solution:** Refactor while tests are green

## Integration with Engineering Workflows

### With Debugging
Bug found? Write failing test first, then fix using debug protocol.

### With Code Review
Submit PRs with:
- All tests pass
- TDD approach documented
- Refactoring completed

### With Security
Write tests for security requirements:
```python
def test_sql_injection_prevented():
    malicious_input = "'; DROP TABLE users; --"
    result = query_database(malicious_input)
    assert "DROP TABLE" not in result
    assert result is sanitized
```

### With Refactoring
Before refactoring:
1. Write tests for current behavior
2. Ensure all tests pass (GREEN)
3. Refactor code
4. Verify tests still pass (REFACTOR)

## Tools and Commands

### Quick Test Run
```bash
pytest test_file.py -v
```

### Watch Tests
```bash
pytest-watch test_file.py  # Reruns on file change
```

### Test Coverage
```bash
pytest --cov=module test_file.py
```

## Remember

**The Iron Law is non-negotiable:**
- Write test first
- Watch it fail
- Write minimal code
- Refactor while green
- Repeat

Violate the rules, and you violate the spirit of TDD.
