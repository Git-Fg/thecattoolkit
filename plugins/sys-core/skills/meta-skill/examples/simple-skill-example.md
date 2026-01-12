# Example: Creating a Simple CSV Validator Skill

## Overview

This example shows how to create a simple skill using the **Standard Template**. The skill validates CSV files and checks for common issues.

## Step-by-Step Creation

### Step 1: Choose Template

**Template:** Standard Skill Template
**Reason:** Simple utility, single workflow, straightforward purpose

### Step 2: Create Directory

```bash
mkdir -p csv-validator
cd csv-validator
```

### Step 3: Use Template

Copy from `meta-skill/assets/skill-standard.md`:

```markdown
---
name: csv-validator
description: "USE when validating CSV data files. Triggers: 'clean CSV data', 'validate CSV columns', 'check CSV format', 'verify CSV schema'."
allowed-tools: [Read, Write, Bash]
---

# CSV Validator
```

### Step 4: Fill Core Knowledge

```markdown
## Core Knowledge

### CSV Format Specifications
- RFC 4180 standard compliance
- Common delimiters: comma, semicolon, tab
- Encoding support: UTF-8, UTF-16, ISO-8859-1
- Line endings: LF, CRLF

### Validation Rules
- Required columns check
- Data type validation (string, number, date)
- Pattern matching (email, phone, etc.)
- Range validation (min/max values)
- Null/empty value handling

### Common CSV Issues
- Inconsistent column counts
- Unexpected delimiters
- Special characters in data
- Missing headers
- Duplicate column names
```

### Step 5: Define Workflow

```markdown
## Workflow

### Step-by-Step Process
1. **Read CSV File** - Load and parse CSV
2. **Validate Structure** - Check headers, delimiters, encoding
3. **Schema Validation** - Verify against defined schema
4. **Data Validation** - Check data types, patterns, ranges
5. **Generate Report** - Create validation summary
6. **Handle Errors** - Provide helpful error messages

### Decision Points
- **If schema provided** → Validate against schema
- **If no schema** → Basic structure validation only
- **If errors found** → Generate detailed error report
- **If valid** → Confirm validation success
```

### Step 6: Add Examples

```markdown
## Usage Examples

### Example 1: Basic Validation
```python
# Validate basic CSV structure
validator = CSVValidator()
result = validator.validate('data.csv')
print(result.is_valid)  # True/False
print(result.errors)    # List of errors
```

### Example 2: Schema Validation
```python
# Validate against schema
schema = {
    'columns': ['name', 'email', 'age'],
    'types': ['string', 'email', 'number']
}
validator = CSVValidator(schema=schema)
result = validator.validate('users.csv')
```

### Example 3: Error Handling
```python
# Check validation result
result = validator.validate('data.csv')

if not result.is_valid:
    print(f"Found {len(result.errors)} errors:")
    for error in result.errors:
        print(f"  - {error.message} at row {error.row}")
else:
    print("CSV validation passed!")
```
```

### Step 7: Define Success Criteria

```markdown
## Success Criteria

### Quality Gates
- [ ] All CSV files validated successfully
- [ ] Schema compliance verified
- [ ] Clear error messages generated
- [ ] Validation report created

### Verification
- Validate output exists
- Check error messages are helpful
- Confirm schema rules enforced
- Verify performance acceptable (<1s for typical files)
```

### Step 8: Add Troubleshooting

```markdown
## Common Issues

### Issue 1: Encoding Error
**Problem:** UnicodeDecodeError when reading CSV
**Solution:** Specify encoding explicitly
```python
validator = CSVValidator(encoding='utf-8')
```

### Issue 2: Delimiter Detection
**Problem:** Wrong delimiter detected
**Solution:** Specify delimiter manually
```python
validator = CSVValidator(delimiter=';')
```

### Issue 3: Large File Handling
**Problem:** Memory issues with large CSV files
**Solution:** Use chunked processing
```python
validator = CSVValidator(chunk_size=10000)
```
```

### Step 9: Complete Skill

Full `SKILL.md`:

```markdown
---
name: csv-validator
description: "USE when validating CSV data files. Triggers: 'clean CSV data', 'validate CSV columns', 'check CSV format', 'verify CSV schema'."
allowed-tools: [Read, Write, Bash]
---

# CSV Validator

## Overview

Validates CSV files for structure compliance, data integrity, and schema adherence. Detects common issues and provides clear error messages.

## Quick Start

```python
validator = CSVValidator()
result = validator.validate('data.csv')
```

## Core Knowledge

### CSV Format Specifications
- RFC 4180 standard compliance
- Common delimiters: comma, semicolon, tab
- Encoding support: UTF-8, UTF-16, ISO-8859-1

### Validation Rules
- Required columns check
- Data type validation (string, number, date)
- Pattern matching (email, phone, etc.)
- Range validation (min/max values)

### Common CSV Issues
- Inconsistent column counts
- Unexpected delimiters
- Special characters in data
- Missing headers

## Workflow

### Step-by-Step Process
1. **Read CSV File** - Load and parse CSV
2. **Validate Structure** - Check headers, delimiters
3. **Schema Validation** - Verify against schema
4. **Data Validation** - Check types and patterns
5. **Generate Report** - Create summary
6. **Handle Errors** - Provide helpful messages

## Usage Examples

### Basic Validation
```python
validator = CSVValidator()
result = validator.validate('data.csv')
print(result.is_valid)
```

### Schema Validation
```python
schema = {'columns': ['name', 'email']}
validator = CSVValidator(schema=schema)
result = validator.validate('users.csv')
```

## Success Criteria

- [ ] All CSV files validated
- [ ] Schema compliance verified
- [ ] Clear error messages
- [ ] Validation report created

## Common Issues

### Encoding Error
**Solution:** Specify encoding
```python
validator = CSVValidator(encoding='utf-8')
```

### Wrong Delimiter
**Solution:** Set delimiter
```python
validator = CSVValidator(delimiter=';')
```

## Anti-Patterns

### ❌ Don't
- Modify data during validation
- Skip error reporting
- Assume UTF-8 encoding

### ✅ Do
- Report all errors found
- Provide helpful messages
- Support multiple encodings
```

## Result

The skill is complete and ready for testing!

### Validation Checklist

- [x] Name: `csv-validator` (14 chars, kebab-case)
- [x] Description: Modal pattern, includes triggers
- [x] Structure: Single workflow, straightforward
- [x] Examples: Concrete and actionable
- [x] Success Criteria: Clear and measurable
- [x] Anti-Patterns: Listed do's and don'ts

### Testing

```bash
# Validate skill
python scripts/validate-skill.py ./csv-validator/

# Check token budget
python scripts/check-token-budget.py ./csv-validator/

# Test discovery
claude --plugin-dir ./plugins -p "I need to validate a CSV file"
```

## Key Takeaways

1. **Simple skills** work well with Standard Template
2. **Clear workflow** helps users understand the process
3. **Concrete examples** make skills immediately useful
4. **Success criteria** define clear expectations
5. **Validation** ensures quality before publishing

## Next Steps

After creating this skill:

1. **Add scripts/** directory with validation utilities
2. **Create examples/** with real CSV test files
3. **Consider progressive disclosure** if complexity grows
4. **Test with real users** and iterate based on feedback
5. **Publish** after validation passes

## Summary

Creating a simple skill involves:
- Choosing appropriate template
- Defining clear workflow
- Providing concrete examples
- Setting success criteria
- Following validation rules

This example demonstrates the Standard Template in action for a straightforward utility skill.
