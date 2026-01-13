# Validation Criteria

Complete validation rules and success criteria for skill creation.

## Name Validation

**Regex**: `^[a-z][a-z0-9-]{2,49}$`

**Requirements**:
- Lowercase letters only
- Must start with letter
- 3-64 characters
- Hyphens allowed (but not consecutive)
- Cannot end with hyphen

**Examples**:
- ✓ `pdf-processor`
- ✓ `serving-llms`
- ✓ `context-engineering`
- ✗ `PDF-processor` (uppercase)
- ✗ `my--skill` (consecutive hyphens)
- ✗ `-skill` (starts with hyphen)
- ✗ `skill-` (ends with hyphen)
- ✗ `ab` (too short)
- ✗ `a-very-long-skill-name-that-exceeds-the-maximum-allowed-length` (too long)

**Validation command**:
```bash
uv run scripts/validate-skill-name.py <skill-name>
```

## Description Validation

**Requirements**:
- 1-1024 characters
- Single line (no newlines)
- Third person only
- Includes "Use when" pattern
- No XML tags
- No quotes around text

**Pattern**: `{CAPABILITY}. Use when {TRIGGERS}.`

**Examples**:

✓ **Valid**:
```yaml
description: Processes CSV files with validation and export. Use when working with tabular data or when the user mentions CSV imports.
```

✓ **Enhanced** (internal):
```yaml
description: Enforces coding standards. MUST Use when committing code or reviewing pull requests.
```

✗ **First person**:
```yaml
description: I can help you process CSV files
```

✗ **Missing Use when**:
```yaml
description: Processes CSV files
```

✗ **Too long** (> 1024 chars):
```yaml
description: [1000+ character description that exceeds limits...]
```

## Frontmatter Validation

**Required fields**:
- `name`
- `description`

**Optional fields**:
- `allowed-tools` - Security whitelist
- `user-invocable` - Menu visibility (default: true)
- `disable-model-invocation` - Catalog inclusion (default: false)
- `context` - Isolation mode (e.g., "fork")

**Forbidden fields**:
- `permissionMode` - Runtime-controlled
- `model` - Runtime-controlled

**Validation command**:
```bash
uv run scripts/validate-frontmatter.py ./my-skill/
```

## Structure Validation

**Directory structure**:
```
skill-name/
├── SKILL.md              # Required
├── references/           # Optional
│   └── *.md
├── assets/               # Optional
│   └── templates/
└── scripts/              # Optional
    └── *.py
```

**Requirements**:
- Directory name MUST match `name` field
- SKILL.md MUST exist
- Forward slashes only (Unix paths)
- NO `../` traversal paths
- NO Windows backslashes

## Content Validation

**SKILL.md Requirements**:
- < 500 lines (aim for 200-300)
- 3rd person throughout
- Progressive disclosure used
- References point to own files only
- Clear when-to-use guidance

**Reference files**:
- One level deep from SKILL.md
- No nested references (A → B → C)
- Links use relative paths: `references/file.md`
- Table of contents if > 100 lines

## Path Validation

**Valid patterns**:
- `references/guide.md`
- `scripts/helper.py`
- `assets/templates/template.md`

**Invalid patterns**:
- `../other-skill/references/file.md` (traversal)
- `scripts\helper.py` (Windows path)
- `/absolute/path/to/file` (absolute path)

## Link Validation

**Internal links**:
```bash
# Validate all links work
uv run scripts/toolkit-analyzer.py --check-links
```

**Requirements**:
- All referenced files exist
- No broken relative paths
- No external dependency links

## Token Budget Validation

**Check token usage**:
```bash
uv run scripts/check-token-budget.py ./my-plugin/
```

**Targets**:
- SKILL.md: < 500 lines (200-300 optimal)
- References: Load on-demand
- Scripts: Only stdout taxed

## Success Criteria Checklist

### Frontmatter
- [ ] Name matches directory (kebab-case)
- [ ] Name passes regex validation
- [ ] Description is 3rd person
- [ ] Description includes "Use when"
- [ ] Description < 1024 characters
- [ ] No forbidden fields
- [ ] `allowed-tools` specified (security)

### Structure
- [ ] SKILL.md < 500 lines
- [ ] No nested references
- [ ] No `../` paths
- [ ] Unix-style forward slashes
- [ ] Directory name matches `name` field

### Content
- [ ] Assumes Claude is smart
- [ ] Consistent terminology
- [ ] Concrete examples
- [ ] Progressive disclosure used
- [ ] 3rd person throughout

### Validation
- [ ] `toolkit-analyzer.py` passes
- [ ] No broken links
- [ ] Name regex passes
- [ ] Description format valid
- [ ] Frontmatter valid

### Architecture
- [ ] Appropriate archetype chosen
- [ ] Inline-first (cost optimization)
- [ ] Intent-driven design
- [ ] No anti-patterns
- [ ] Clear value proposition

## Full Validation Command

```bash
# Run all validations
uv run scripts/toolkit-analyzer.py

# Fix issues automatically
uv run scripts/toolkit-analyzer.py --fix

# Detailed output
uv run scripts/toolkit-analyzer.py --verbose
```

## Common Validation Failures

**Name Issues**:
- `my_skill` - underscores not allowed
- `MySkill` - uppercase not allowed
- `skill` - too short (< 3 chars)
- `my-skill-` - ends with hyphen

**Description Issues**:
- "I help you..." - first person
- "Processes files." - missing "Use when"
- Multi-line descriptions - newlines break parsing

**Structure Issues**:
- SKILL.md > 500 lines - token inefficient
- Nested references (A → B → C) - breaks progressive disclosure
- `../other-skill/file.md` - breaks portability

**Path Issues**:
- `scripts\helper.py` - Windows path
- `/abs/path/file` - absolute path
- `../../file` - traversal path

## Validation Workflow

1. **CREATE** → Write skill files
2. **VALIDATE** → Run `toolkit-analyzer.py`
3. **FIX** → Address reported issues
4. **RE-VALIDATE** → Run again (max 3 iterations)
5. **CONFIRM** → Only when all checks pass

Never skip validation. It catches naming conflicts, broken links, and architecture violations.
