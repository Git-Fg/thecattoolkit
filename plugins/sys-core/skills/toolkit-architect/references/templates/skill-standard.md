---
name: {SKILL_NAME}
# Standard Pattern (default - recommended for most skills):
description: "{CAPABILITY}. Use when {TRIGGERS}."
# OR Enhanced Pattern (for toolkit infrastructure):
# description: "{CAPABILITY}. {MUST|PROACTIVELY|SHOULD} Use when {TRIGGERS}."
allowed-tools: [{ALLOWED_TOOLS}]
---

# {HUMAN_READABLE_NAME}

## Overview

{Brief description of what this skill accomplishes}

## Quick Start

```language
# Quick example
quick_implementation()
```

## Core Knowledge

### Domain Expertise
- {Key concept 1}
- {Key concept 2}
- {Key concept 3}

### Best Practices
- {Practice 1}
- {Practice 2}
- {Practice 3}

## Workflow

### Step-by-Step Process
1. **First Step** - {Description}
2. **Second Step** - {Description}
3. **Third Step** - {Description}

### Decision Points
- **If X** → Follow path A
- **If Y** → Follow path B
- **Otherwise** → Follow default path

## Usage Examples

### Example 1: {Use Case}
```language
# Context: {Describe scenario}
# Action: {What to do}
result = implement()
```

### Example 2: {Use Case}
```language
# Context: {Describe scenario}
# Action: {What to do}
result = implement()
```

## Success Criteria

### Quality Gates
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

### Verification
- {How to verify success}
- {Expected outcomes}
- {Error handling}

## Common Issues

### Issue 1: {Problem}
**Solution:** {How to fix}

### Issue 2: {Problem}
**Solution:** {How to fix}

## Anti-Patterns

### ❌ Don't
- {Common mistake 1}
- {Common mistake 2}
- {Common mistake 3}

### ✅ Do
- {Correct approach 1}
- {Correct approach 2}
- {Correct approach 3}

## Integration

### With Other Tools
- {Tool 1}: {How it integrates}
- {Tool 2}: {How it integrates}

### Environment Requirements
- {Requirement 1}
- {Requirement 2}

## Configuration

### Options
- **Option 1:** {Description}
- **Option 2:** {Description}
- **Option 3:** {Description}

### Customization
{Customization options}

## References

- [Related Skill 1] - {Description}
- [Related Skill 2] - {Description}

## Scripts (if applicable)

```bash
# Validation script with PEP 723 inline metadata
uv run scripts/validate.py {args}
```

**Script template:**
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Script description."""
```

## Summary

This skill provides {core value} for {target users} by {key benefit}.
