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

{2-3 sentences: what this skill does and why it's valuable}

## Quick Start

```{language}
# Minimal working example
{quick_implementation}
```

## Core Concepts

{2-3 key concepts explained briefly}

**For detailed information:**
- {Concept 1} → See `references/{file1}.md`
- {Concept 2} → See `references/{file2}.md`
- {Advanced topic} → See `references/{file3}.md`

## Basic Workflow

### Step 1: {Action}
{Brief description}

### Step 2: {Action}
{Brief description}

### Step 3: {Action}
{Brief description}

**Detailed procedures:** See `references/workflows.md`

## Common Use Cases

### {Use Case 1}
```{language}
{example_code}
```
**Complete example:** See `examples/{example1}.md`

### {Use Case 2}
```{language}
{example_code}
```
**Complete example:** See `examples/{example2}.md`

## Decision Points

- **If {condition}** → {action} (See `references/{ref}.md`)
- **If {condition}** → {action} (See `references/{ref}.md`)
- **Otherwise** → {default action}

## Reference Materials

### Documentation
- `references/concepts.md` - Core concepts and theory
- `references/workflows.md` - Detailed procedures
- `references/api-reference.md` - Complete API documentation
- `references/troubleshooting.md` - Common issues

### Examples
- `examples/basic.md` - Simple use case
- `examples/intermediate.md` - Moderate complexity
- `examples/advanced.md` - Expert scenarios

### Scripts (if applicable)
```bash
# Validation script with PEP 723 inline metadata
uv run scripts/validate.py {args}
```

**Note:** Reference files >100 lines should include table of contents for navigation.

## Success Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Common Issues

**{Issue 1}** → See `references/troubleshooting.md`
**{Issue 2}** → See `references/troubleshooting.md`

---

**Directory Structure:**
```
{skill-name}/
├── SKILL.md              # This file (<500 lines)
├── references/           # Detailed documentation
│   ├── concepts.md       # Include TOC for files >100 lines
│   ├── workflows.md
│   ├── api-reference.md
│   └── troubleshooting.md
├── examples/
│   ├── basic.md
│   └── advanced.md
├── scripts/              # With PEP 723 metadata
│   └── validate.py
└── assets/               # Static resources
```

**Remember:** Load reference files only when needed. SKILL.md provides quick access to core functionality.
