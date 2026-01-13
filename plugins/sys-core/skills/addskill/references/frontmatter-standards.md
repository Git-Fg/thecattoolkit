# YAML Frontmatter Standards

Complete reference for skill frontmatter validation and best practices.

## Required Fields

### name

**Format**: `^[a-z][a-z0-9-]{2,49}$`

**Rules**:
- Lowercase letters, numbers, hyphens only
- Must start with a letter
- 3-64 characters
- No consecutive hyphens
- Cannot start or end with hyphen
- No reserved words: "anthropic", "claude"

**Examples**:
- ✓ `pdf-processor`
- ✓ `serving-llms`
- ✓ `context-engineering`
- ✗ `PDF-processor` (uppercase)
- ✗ `my--skill` (consecutive hyphens)
- ✗ `-skill` (starts with hyphen)
- ✗ `claude-helper` (reserved word)

### description

**Format**: 3rd person, 1-1024 characters

**Pattern**: `{CAPABILITY}. Use when {TRIGGERS}.`

**Requirements**:
- MUST be 3rd person
- MUST include "Use when" pattern
- MUST describe what it does
- MUST indicate when to use it
- No XML tags
- No quotes around text

**Examples**:

✓ **Standard pattern**:
```yaml
description: Processes CSV files with validation and export. Use when working with tabular data or when the user mentions CSV imports.
```

✓ **Enhanced pattern** (internal tools):
```yaml
description: Enforces coding standards. MUST Use when committing code or reviewing pull requests.
```

✗ **First person** (forbidden):
```yaml
description: I can help you process CSV files
```

✗ **Missing "Use when"** (weak):
```yaml
description: Processes CSV files
```

## Optional Fields

### allowed-tools

**Purpose**: Security whitelist - restricts skill to specific tools

**Default**: If omitted, NO RESTRICTION (all tools available)

**Format**: Array of tool names with optional specifiers

**Examples**:
```yaml
allowed-tools: [Read, Write, Edit, Bash]
allowed-tools: [Skill(planner), Skill(executor), Bash(git:*)]
```

**Best Practice**: Always specify for security unless full access is required.

### user-invocable

**Purpose**: Controls visibility in `/` menu

**Values**:
- `false` - Hidden from menu, model can still invoke (unless `disable-model-invocation: true`)
- Omitted or `true` - Visible in menu

**Use cases**:
- `false`: Internal orchestration skills
- Omitted: User-facing tools

### disable-model-invocation

**Purpose**: Prevents model from auto-selecting the skill

**Values**:
- `true` - Model cannot invoke, removes from catalog
- Omitted or `false` - Model can invoke

**Use cases**:
- `true`: Manual-only commands, expensive operations
- Omitted: Discovery-capable skills

### context

**Purpose**: Execution isolation

**Values**:
- `fork` - Execute in isolated sub-agent (cognitive sandbox)

**Use cases**:
- Noisy research (reading 100+ files)
- Massive logs that would pollute context
- Isolation requirements

## Forbidden Fields

### permissionMode

**NEVER specify** in frontmatter.

**Rationale**: Runtime-controlled for security. Users must retain sovereignty.

### model

**NEVER specify** in frontmatter.

**Rationale**: Runtime-controlled. Prevents breakage on model deprecation.

## Complete Example

```yaml
---
name: hybrid-search-implementation
description: Implements hybrid keyword and vector search with reranking. Use when building search applications, implementing RAG systems, or optimizing retrieval relevance.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Search, RAG, Vector Database, Information Retrieval]
dependencies: [numpy>=1.24.0, scipy>=1.10.0]
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
user-invocable: false
---
```

## Validation Commands

```bash
# Validate name
uv run scripts/validate-skill-name.py <skill-name>

# Validate description
uv run scripts/validate-description.py ./my-skill/

# Validate full frontmatter
uv run scripts/validate-frontmatter.py ./my-skill/

# Full validation
uv run scripts/toolkit-analyzer.py
```
