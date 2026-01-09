---
name: tdd
description: |
  USE when implementing new features, fixing bugs, or refactoring with TDD methodology (Test-Driven Development workflow).
  Keywords: test-driven development, TDD, red-green-refactor, write tests first
context: fork
agent: worker
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Test-Driven Development Protocol

## Core Purpose

Implement features and bug fixes using the Red-Green-Refactor cycle. Write tests first, watch them fail, write minimal code to pass, then refactor while tests remain green.

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

## Red-Green-Refactor Process

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

## Security Checklist (OWASP Top 10)

**Before executing any code modifications:**

- [ ] **Injection Prevention**: All user inputs validated/sanitized, no dynamic SQL
- [ ] **Authentication**: Auth checks on sensitive endpoints, no hardcoded secrets
- [ ] **Access Control**: Authorization checks on every protected resource
- [ ] **Cryptography**: No hardcoded passwords or keys
- [ ] **Input Validation**: All entry points validated
- [ ] **Error Handling**: Errors don't expose sensitive information
- [ ] **Dependencies**: No vulnerable/outdated components

## Success Criteria

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Code is refactored while tests remain green
- [ ] Output pristine (no errors, warnings)
- [ ] Security checklist verified

**Can't check all boxes? You skipped TDD. Start over.**

## The Iron Law (Non-Negotiable)

- Write test first
- Watch it fail
- Write minimal code
- Refactor while green
- Repeat

Violate the rules, and you violate the spirit of TDD.
