# Multi-Model Testing Suite

## Testing Methodology

This test suite validates the sys-builder plugin across three model tiers to ensure compatibility and optimal performance.

### Model Tiers

#### 1. Haiku Tests (Fast Operations)
- **Purpose**: Validate basic operations and simple workflows
- **Complexity**: Low - single-step operations
- **Focus**: Core functionality, simple plan creation, basic execution
- **Expected**: Fast responses, minimal context usage

#### 2. Sonnet Tests (Medium Complexity)
- **Purpose**: Validate standard workflows and multi-step operations
- **Complexity**: Medium - 2-5 step workflows
- **Focus**: Plan creation with discovery, phase execution, state management
- **Expected**: Balanced performance, standard workflows

#### 3. Opus Tests (High Complexity)
- **Purpose**: Validate complex workflows and edge cases
- **Complexity**: High - multi-phase, multi-file operations
- **Focus**: Complex plan architecture, handoff handling, error recovery
- **Expected**: Deep reasoning, comprehensive validation

### Test Categories

Each tier tests three core commands:

1. **create-plan** - Plan architecture and generation
2. **run-plan** - Plan execution and state management
3. **manage-plan** - Plan modification and tracking

### Test Structure

```
tests/multi-model/
├── README.md (this file)
├── run-all-tests.sh
├── haiku/
│   ├── create-plan.test.md
│   ├── run-plan.test.md
│   └── manage-plan.test.md
├── sonnet/
│   ├── create-plan.test.md
│   ├── run-plan.test.md
│   └── manage-plan.test.md
└── opus/
    ├── create-plan.test.md
    ├── run-plan.test.md
│   └── manage-plan.test.md
```

### Test Content Template

Each test file follows this structure:

```markdown
# Test: {Command Name} - {Model Tier}

## Test Case 1: {Scenario}
**Input**: `/sys-builder:command-name "{input}"`
**Expected Output**: {expected result}
**Success Criteria**:
- [ ] Output format matches expected
- [ ] Files created in correct location
- [ ] State transitions correctly
- [ ] No errors

## Test Case 2: {Scenario}
...
```

### Running Tests

#### Run All Tests
```bash
./tests/multi-model/run-all-tests.sh
```

#### Run Specific Tier
```bash
# Haiku tests (fast)
./tests/multi-model/run-all-tests.sh haiku

# Sonnet tests (medium)
./tests/multi-model/run-all-tests.sh sonnet

# Opus tests (complex)
./tests/multi-model/run-all-tests.sh opus
```

#### Run Specific Command
```bash
./tests/multi-model/run-all-tests.sh haiku create-plan
```

### Success Criteria

A test passes when:
- All success criteria are met
- No errors in execution
- Files created in expected locations
- State transitions are correct
- Output format matches specification

### Failure Handling

If a test fails:
1. Check error messages in output
2. Verify expected vs actual results
3. Review state transitions
4. Check file system for created files
5. Document issue and remediation

### Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clean State**: Start each test with clean state
3. **Clear Criteria**: Success criteria must be measurable
4. **Documentation**: Document expected vs actual behavior
5. **Iteration**: Fix and re-run until all tests pass

### Model-Specific Considerations

#### Haiku
- Keep tests simple and focused
- Minimal context requirements
- Fast execution expected
- Single operation per test

#### Sonnet
- Standard workflows
- Moderate complexity
- Balanced performance
- 2-3 operations per test

#### Opus
- Complex workflows
- Edge cases and error handling
- Deep reasoning required
- Multi-step validation

## References

- **Test Execution**: Use `./run-all-tests.sh` script
- **Expected Results**: See individual test files
- **Success Criteria**: Defined per test case
