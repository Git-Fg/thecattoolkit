# Example: UUID Generator (Minimal Skill)

A minimal skill for generating UUIDs, demonstrating the fundamental structure.

```markdown
---
name: uuid-generator
description: Generate + UUIDs + for testing or database keys - MUST USE when user needs unique identifiers
---

# OBJECTIVE

Generate standard UUIDs (v4) for use as unique identifiers in testing or database operations.

## Quick Start

```python
# Generate a single UUID
import uuid
print(uuid.uuid4())
```

## Foundational Knowledge

**Before executing this workflow, review:**
- **Standard**: Use UUID v4 for random generation unless specified otherwise.
- **Format**: Standard hex string representation (e.g., `f47ac10b-58cc-4372-a567-0e02b2c3d479`).

## Operational Protocol

**Strong Core:**
1. **Identify Quantity**: Determine how many UUIDs are needed (default to 1).
2. **Generate**: Use Python's `uuid` library to generate the identifiers.
3. **Output**: Present the UUIDs in a code block for easy copying.

## Common Options

- **Bulk Generation**: "Generate 10 UUIDs"
- **Format Specific**: "Upper case UUIDs" or "UUIDs without hyphens"

## Success Criteria

- [ ] UUIDs are valid v4 format
- [ ] Correct quantity generated
- [ ] Output is clean and copy-pastable
```
