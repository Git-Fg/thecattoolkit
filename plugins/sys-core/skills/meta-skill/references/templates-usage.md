# Template Usage Guide

## Overview

Templates accelerate skill creation by providing proven patterns and structures. Choose the right template based on complexity, workflow requirements, and documentation needs.

## Template Selection Decision Tree

`
Start: What type of skill are you creating?
│
├─ Single straightforward purpose?
│  ├─ Yes → Standard Template
│  └─ No → Continue
│
├─ Complex domain requiring detailed docs?
│  ├─ Yes → Progressive Disclosure Template
│  └─ No → Continue
│
├─ Multiple workflows requiring routing?
│  ├─ Yes → Router Pattern Template
│  └─ No → Continue
│
└─ Internal/passive skill?
   ├─ Yes → Minimal Template
   └─ No → Standard Template
`

## Template Catalog

### 1. Standard Skill Template

**Purpose:** Single workflow, straightforward purpose
**Location:** toolkit-registry/assets/standard-skill.md
**Best for:** Simple utilities, single-purpose skills

**Structure:**
`markdown
---
name: {SKILL_NAME}
description: "..."
allowed-tools: {RESTRICTED_TOOLS}
context: fork  # Optional: use when isolation needed
---

# {HUMAN_READABLE_NAME}

## 1. Core Knowledge
{Passive knowledge base, key concepts}

## 2. Decision Logic / Protocol
{Guidelines for the AI}

## 3. Success Criteria
{How to determine success}

## 4. Anti-Patterns
{What to avoid}
`

**When to Use:**
- ✅ Simple utility skill
- ✅ Single clear workflow
- ✅ Minimal documentation needed
- ✅ Direct execution

**Examples from Cat Toolkit:**
- check-types - Type checking for Python
- Simple data validators
- Basic file processors

**Filling the Template:**

**Example: CSV Validator Skill**
`markdown
---
name: csv-validator
description: "USE when validating CSV data files. Provides column validation, data type checking, and schema compliance verification."
allowed-tools: [Read, Write, Bash]
---

# CSV Validator

## 1. Core Knowledge
- CSV format specifications (RFC 4180)
- Common validation rules (required columns, data types)
- Schema definition syntax
- Error reporting standards

## 2. Decision Logic / Protocol
1. Read CSV file
2. Validate structure (headers, delimiter, encoding)
3. Check against schema rules
4. Report validation errors
5. Generate compliance report

## 3. Success Criteria
- [ ] All required columns present
- [ ] Data types match schema
- [ ] No validation errors
- [ ] Clear error messages generated

## 4. Anti-Patterns
- Don't modify data during validation
- Don't skip error reporting
- Don't assume file encoding
`

### 2. Progressive Disclosure Template

**Purpose:** Complex domain requiring detailed documentation
**Location:** toolkit-registry/assets/progressive-disclosure.md
**Best for:** Multi-domain skills, rich documentation

**Structure:**
`markdown
---
name: NAME_HERE
description: "MUST USE when WORKFLOW_TRIGGER_KEYWORDS to progressively disclose TASK_NAME_HERE knowledge..."
---

# TASK_NAME_HERE

## Overview
Brief description

## Quick Start
Immediate solution

## Foundational Knowledge
Key concepts

## Core Concepts
- Concept 1
- Concept 2

## Operational Protocol
Strong Core + Flexible Application

## Progressive Disclosure
Advanced topics → references/

## Scripts
Bundled utilities

## Common Options
Variations

## Common Issues
Problems and solutions

## Success Criteria
Quality gates
`

**When to Use:**
- ✅ Complex domain knowledge
- ✅ Multiple related capabilities
- ✅ Rich documentation needed
- ✅ 400+ lines of content

**Examples from Cat Toolkit:**
- prompt-engineering - References + assets/
- toolkit-registry - Comprehensive standards
- meta-hooks - Detailed hook patterns

**Implementation Example:**

**Structure:**
`
skill-name/
├── SKILL.md (uses template)
├── references/
│   ├── advanced-topic1.md
│   ├── advanced-topic2.md
│   └── api-reference.md
├── examples/
│   └── use-case1.md
└── scripts/
    └── utility-script.py
`

**In SKILL.md:**
`markdown
## Progressive Disclosure

**Advanced Topics:**
- references/advanced-topic1.md - Detailed guide
- references/advanced-topic2.md - Advanced patterns

**API Reference:**
- references/api-reference.md - Complete API

**Examples:**
- examples/use-case1.md - Real-world scenario
`

### 3. Router Pattern Template

**Purpose:** Multiple workflows requiring intelligent routing
**Location:** toolkit-registry/assets/router-pattern.md
**Best for:** Multi-capability systems, analysis workflows

**Structure:**
`markdown
# Router Name

## Purpose
Route requests to appropriate specialized skills

## Activation Triggers
- Trigger 1
- Trigger 2

## Routing Logic

### Type A
**Triggers:** [keywords]
**Routes to:** [skill name]
**Pattern:** "..."

### Type B
**Triggers:** [keywords]
**Routes to:** [skill name]
**Pattern:** "..."

## Default Route
[Fallback behavior]
`

**When to Use:**
- ✅ Multiple specialized skills
- ✅ Request classification needed
- ✅ Workflow orchestration
- ✅ Pattern matching

**Example from Cat Toolkit:**
- toolkit-registry - Routes to specialized components

**Implementation Example:**

`markdown
# Code Analysis Router

## Purpose
Route code analysis requests to appropriate specialized skills

## Activation Triggers
- "Analyze code for..."
- "Review this code"
- "Find issues in..."

## Routing Logic

### Security Analysis
**Triggers:** "security", "vulnerabilities", "XSS", "injection"
**Routes to:** security-analysis-skill
**Pattern:** "Analyze code for security vulnerabilities"

### Performance Analysis
**Triggers:** "performance", "speed", "optimize", "bottleneck"
**Routes to:** performance-analysis-skill
**Pattern:** "Analyze code for performance issues"

### Style Analysis
**Triggers:** "style", "format", "lint", "convention"
**Routes to:** code-style-skill
**Pattern:** "Review code style and formatting"

## Default Route
**Routes to:** general-review-skill
**Pattern:** "Perform general code review"
`

### 4. Minimal Template

**Purpose:** Internal/passive skills
**Location:** toolkit-registry/assets/minimal.md
**Best for:** Hook-based skills, passive monitoring

**Structure:**
`markdown
# Skill Name

## Purpose
[What this skill does]

## Triggers
[When this skill activates]

## Implementation
[How it works]
`

**When to Use:**
- ✅ Internal utility skills
- ✅ Hook-based execution
- ✅ Passive monitoring
- ✅ Minimal documentation

**Examples from Cat Toolkit:**
- audit-security - Runs via hooks
- check-types - Passive type checking

**Implementation Example:**
`markdown
# Security Audit

## Purpose
Automatically scan for secrets and protect sensitive files

## Triggers
PreToolUse hook on Edit/Write operations

## Implementation
- Scans content for API keys
- Warns on lock file modification
- Blocks writes to .env files
- Runs passively via hooks
`

## Using Templates

### Step 1: Choose Template

**Decision Matrix:**

| Skill Type | Template | Reason |
|------------|----------|--------|
| Simple utility | Standard | Clear purpose, single workflow |
| Complex domain | Progressive | Rich documentation needed |
| Multi-workflow | Router | Requires routing logic |
| Internal tool | Minimal | Passive execution |

### Step 2: Copy Template

`bash
# Copy from toolkit-registry
cp toolkit-registry/assets/standard-skill.md ./my-skill/SKILL.md

# Or copy specific template
cp toolkit-registry/assets/progressive-disclosure.md ./my-skill/SKILL.md
`

### Step 3: Fill Template

**Search and Replace:**

`markdown
# Replace placeholders
{SKILL_NAME} → csv-validator
{HUMAN_READABLE_NAME} → CSV Validator
{TASK_NAME_HERE} → CSV Data Validation
{WORKFLOW_TRIGGER_KEYWORDS} → validating CSV data files
{OPTIONAL_PERSONA} → plugin-expert
{RESTRICTED_TOOLS} → [Read, Write, Bash]
`

### Step 4: Customize Content

**Add your specific knowledge:**

`markdown
## 1. Core Knowledge
# Add your domain expertise
- CSV format specifications
- Validation rules
- Error patterns
- Best practices

## 2. Decision Logic / Protocol
# Add your workflow
1. Step one
2. Step two
3. Step three

## 3. Success Criteria
# Define success
- [ ] Criterion 1
- [ ] Criterion 2
`

## Template Customization

### Standard Template Customization

**Add Sections:**
`markdown
## 5. Configuration
[Optional configuration]

## 6. Integration
[How it works with other tools]

## 7. Examples
[Code examples]
`

**Remove Sections:**
`markdown
# If not applicable, remove sections
# e.g., remove "4. Anti-Patterns" if none exist
`

### Progressive Disclosure Customization

**Add Reference Files:**
`markdown
# In SKILL.md
## Progressive Disclosure
- references/topic1.md
- references/topic2.md

# Create files
references/
├── topic1.md (100+ lines)
└── topic2.md (100+ lines)
`

**Add Examples:**
`markdown
# In SKILL.md
## Examples
- examples/use-case1.md
- examples/use-case2.md

# Create files
examples/
├── use-case1.md
└── use-case2.md
`

### Router Template Customization

**Add Routing Logic:**
`markdown
## Routing Logic

### Workflow Type A
**Triggers:** keyword1, keyword2
**Routes to:** skill-a
**Pattern:** "Execute workflow A"

### Workflow Type B
**Triggers:** keyword3, keyword4
**Routes to:** skill-b
**Pattern:** "Execute workflow B"
`

**Implement Routing:**
`python
# Add to SKILL.md
def route_request(request):
    request_lower = request.lower()

    if any(term in request_lower for term in ['keyword1', 'keyword2']):
        return 'skill-a'

    if any(term in request_lower for term in ['keyword3', 'keyword4']):
        return 'skill-b'

    return 'default-skill'
`

## Template Best Practices

### DO

✅ **Choose template based on complexity**
✅ **Fill all placeholders**
✅ **Customize content to your domain**
✅ **Keep progressive disclosure files 100+ lines**
✅ **Use consistent structure**
✅ **Test the template**
✅ **Validate YAML frontmatter**

### DON'T

❌ **Use wrong template for complexity**
❌ **Leave placeholders unfilled**
❌ **Skip sections without reason**
❌ **Create reference files under 50 lines**
❌ **Duplicate content across templates**
❌ **Ignore template structure**
❌ **Forget to update descriptions**

## Template Combinations

### Combo 1: Progressive + Router

**Use when:** Complex domain with multiple workflows

`markdown
# SKILL.md (Progressive structure)
# + Router logic in "Routing Logic" section
# + references/ for detailed docs

## Routing Logic
[Router pattern implementation]

## Progressive Disclosure
- references/workflow-a.md
- references/workflow-b.md
`

### Combo 2: Standard + Scripts

**Use when:** Simple skill with utilities

`markdown
# SKILL.md (Standard structure)
# + scripts/ directory with utilities

## Scripts
Use bundled utilities:
- scripts/validate.py
- scripts/transform.py
`

### Combo 3: Progressive + Examples + Scripts

**Use when:** Full-featured skill

`markdown
# SKILL.md (Progressive structure)
# + references/ for detailed docs
# + examples/ for use cases
# + scripts/ for utilities
`

## Validation

### Template Completeness Checklist

**Standard Template:**
- [ ] All placeholders replaced
- [ ] Core Knowledge filled
- [ ] Decision Logic defined
- [ ] Success Criteria listed
- [ ] Anti-Patterns identified
- [ ] YAML frontmatter valid

**Progressive Template:**
- [ ] Quick Start provided
- [ ] Foundational Knowledge documented
- [ ] Core Concepts listed
- [ ] Operational Protocol defined
- [ ] Progressive Disclosure links added
- [ ] References files created (100+ lines each)

**Router Template:**
- [ ] Routing logic implemented
- [ ] Triggers defined
- [ ] Routes specified
- [ ] Default route provided
- [ ] Examples given

### Testing Template

**Manual Test:**
`markdown
1. Create skill from template
2. Test with realistic user query
3. Verify discovery works
4. Check all links functional
5. Validate output quality
`

## Migration Between Templates

### From Standard to Progressive

**When to migrate:**
- SKILL.md exceeds 500 lines
- Multiple domains covered
- Rich documentation needed

**Migration steps:**
1. Extract sections to references/
2. Update SKILL.md with navigation
3. Create reference files (100+ lines each)
4. Test discovery and navigation

### From Progressive to Router

**When to migrate:**
- Multiple workflows identified
- Request classification needed
- Delegation required

**Migration steps:**
1. Add routing logic section
2. Define triggers for each workflow
3. Specify route destinations
4. Implement routing function

## Summary

**Template Selection:**

| Template | Use Case | Complexity |
|----------|----------|------------|
| **Standard** | Simple skills | Low |
| **Progressive** | Complex domains | High |
| **Router** | Multi-workflow | Medium |
| **Minimal** | Internal tools | Low |

**Key Principles:**
- Choose based on actual needs, not complexity preference
- Customize content to your domain
- Use progressive disclosure for rich documentation
- Test before publishing

**Remember:** Templates accelerate development but require customization. Don't just fill placeholders—add your specific knowledge and workflows.
