# Quick Reference Guide

## Decision Matrix

### Template Selection

| Scenario | Template | Pattern | Example |
|----------|----------|---------|---------|
| Simple type checker | standard | Knowledge Base | check-types skill |
| PDF processor | progressive | Progressive | prompt-engineering skill |
| Component router | router | Router | toolkit-registry skill |
| Security audit hook | minimal | Passive | audit-security skill |

### Description Pattern Selection

**Choose between Standard and Enhanced patterns:**

| Use Case | Pattern | Format | Example |
|----------|---------|--------|---------|
| **Public/Portable skills** | Standard | `{CAPABILITY}. Use when {TRIGGERS}.` | `"Processes CSV files. Use when working with tabular data."` |
| **Internal infrastructure** | Enhanced | `{CAPABILITY}. {MODAL} Use when {TRIGGERS}.` | `"Validates toolkit standards. MUST Use when building skills."` |
| **User-facing tools** | Standard | `{CAPABILITY}. Use when {TRIGGERS}.` | `"Extracts text from PDFs. Use when processing documents."` |
| **Critical standards** | Enhanced | `{CAPABILITY}. MUST Use when {TRIGGERS}.` | `"Enforces security rules. MUST Use before deployments."` |

**Enhanced Pattern Modal Types:**

| Modal | Use When | Audience | Example |
|-------|----------|----------|---------|
| **MUST** | Critical internal standards | Developers | `"Enforces coding standards. MUST Use when committing code."` |
| **PROACTIVELY** | Primary orchestration | AI Agents | `"Routes requests intelligently. PROACTIVELY Use when handling queries."` |
| **SHOULD** | Recommended practices | Users | `"Validates inputs. SHOULD Use when processing user data."` |

**Decision Guide:**

```
┌─────────────────────────────────────┐
│  Is this skill...                   │
├─────────────────────────────────────┤
│  1. For external users?             │
│     → Use Standard Pattern          │
│                                     │
│  2. Internal infrastructure only?  │
│     → Use Enhanced Pattern          │
│                                     │
│  3. Critical compliance tool?      │
│     → MUST Use when (Enhanced)     │
│                                     │
│  4. General capability?             │
│     → Use when (Standard)          │
└─────────────────────────────────────┘
```

### Template Pattern Selection

| Need | Pattern | Use When |
|------|---------|----------|
| Single capability | Knowledge Base | One clear purpose |
| Multiple capabilities | Router | Intelligent routing |
| Complex domain | Progressive | Detailed documentation |
| Internal tool | Passive | Hooks, monitoring |

## Validation Checklist

### Name Validation

`bash
# Check format
echo "skill-name" | grep -E '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'

# Check length (3-50 chars)
[ ${#skill_name} -ge 3 ] && [ ${#skill_name} -le 50 ]

# Examples
✅ pdf-processor (13 chars)
✅ code-analyzer-v2 (16 chars)
❌ PDFProcessor (uppercase)
❌ code_analyzer (underscore)
❌ ag (too short)
`

### Description Validation

`yaml
# Required format
description: "(MODAL) USE when [condition with triggers]"

# Modal options
MUST USE when     # Critical internal standards
SHOULD USE when   # Recommended but situational
PROACTIVELY USE when  # Auto-invocation for orchestration
USE when          # Direct entry point

# Examples
✅ "SHOULD USE when processing CSV files. Provides validation, transformation, and analysis capabilities."
❌ "A skill for data processing"
`

### Content Validation

`bash
# Check SKILL.md length (should be < 500 lines)
wc -l SKILL.md

# Check references exist
ls references/  # Should have relevant files

# Check examples exist
ls examples/    # Should have 2-3 examples

# Check workflows exist (if needed)
ls workflows/   # Should have process documentation
`

### Token Budget

`bash
# Calculate total description characters
grep -r "description:" . | awk '{ sum += length($0) } END { print sum }'
# Should be < 15,000

# If over limit:
# 1. Shorten descriptions
# 2. Consolidate similar skills
# 3. Use progressive disclosure
`

## Common Patterns

### Knowledge Base Pattern

`markdown
# Structure
skill-name/
└── SKILL.md (comprehensive guide)

# Content
- Overview
- Quick Start
- Core Knowledge
- Workflow
- Examples
- Success Criteria
`

### Progressive Disclosure Pattern

`markdown
# Structure
skill-name/
├── SKILL.md (navigation + overview)
├── references/ (detailed docs)
├── examples/ (concrete use cases)
├── workflows/ (complex processes)
└── assets/ (templates + tools)

# Content Distribution
SKILL.md (< 500 lines):
- Navigation
- Quick Start
- Core Concepts (summary)
- Advanced Topics (links)

references/ (> 100 lines each):
- Detailed explanations
- Advanced techniques
- API documentation
- Edge cases
`

### Router Pattern

`markdown
# Structure
skill-router/
├── SKILL.md (routing logic)
├── workflows/ (routing algorithm)
└── references/ (route definitions)

# Routing Logic
1. Analyze request
2. Match against routes
3. Calculate confidence
4. Delegate to target
5. Format response
`

### Minimal Pattern

`markdown
# Structure
minimal-skill/
└── SKILL.md (basic frontmatter)

# Content
---
name: minimal-skill
description: "MUST USE when [internal standard]. Provides [minimal capability]."
---
`

## Frontmatter Templates

### Standard Skill

`yaml
---
name: skill-name
description: "USE when [task description]. [Triggers and context]."
allowed-tools: [Read, Write, Edit, Bash]
---
`

### Cat Toolkit Extended

`yaml
---
name: skill-name
description: "SHOULD USE when [condition]. [Triggers and context]."
allowed-tools: [Read, Write, Edit, Bash]
user-invocable: false  # Hide from / menu (for commands)
context: fork           # Isolated execution
---
`

### Agent-Bound Skill

`yaml
---
name: skill-name
description: "SHOULD USE when [condition]. [Triggers and context]."
allowed-tools: [Read, Write, Edit, Bash]
context: fork  # Isolated execution when needed
---
`

### Command-Wrapped Skill

`yaml
---
name: skill-name
description: "USE when [condition]. [Triggers and context]."
user-invocable: false  # Hidden, used by command
allowed-tools: [Read, Write, Edit, Bash]
---
`

## File Organization

### Standard Structure

`
skill-name/
├── SKILL.md                    # Main guide (< 500 lines)
├── references/                 # Detailed documentation
│   ├── domain1.md
│   ├── domain2.md
│   └── api-reference.md
├── examples/                   # Concrete examples
│   ├── example1.md
│   └── example2.md
├── scripts/                    # Executable utilities
│   ├── script1.py
│   └── script2.sh
├── assets/                     # Output files
│   ├── templates/
│   └── images/
└── workflows/                  # Process documentation
    ├── workflow1.md
    └── workflow2.md
`

### Minimal Structure

`
minimal-skill/
└── SKILL.md
`

### Progressive Structure

`
complex-skill/
├── SKILL.md                    # Navigation + overview
├── references/                 # Domain expertise
│   ├── theory.md
│   ├── advanced-techniques.md
│   └── api-reference.md
├── examples/                   # Comprehensive examples
│   ├── basic-usage.md
│   ├── advanced-usage.md
│   └── edge-cases.md
├── workflows/                  # Complex processes
│   ├── setup-workflow.md
│   ├── processing-workflow.md
│   └── troubleshooting.md
├── scripts/                    # Automation
│   ├── validate.sh
│   ├── test.sh
│   └── deploy.sh
└── assets/                    # Resources
    ├── templates/
    ├── configs/
    └── examples/
`

## Quick Start Templates

### 5-Minute Skill

`markdown
# 1. Create directory
mkdir my-skill
cd my-skill

# 2. Create SKILL.md
---
name: my-skill
description: "USE when [task]. [Triggers]."
---

# My Skill

## Overview
[Brief description]

## Quick Start
[Basic usage]

## Workflow
1. Step 1
2. Step 2
3. Step 3

## Examples
[Concrete example]
`

### 30-Minute Skill

`markdown
# 1. Create structure
mkdir -p my-skill/{references,examples,workflows,assets/{templates,scripts}}

# 2. Create SKILL.md
---
name: my-skill
description: "SHOULD USE when [condition]. [Triggers]."
allowed-tools: [Read, Write, Edit, Bash]
---

# My Skill

## Overview
[Description]

## Quick Start
[Basic usage]

## Core Knowledge
[Essential concepts]

## Workflow
[Step-by-step]

## Examples
[Concrete examples]

## Success Criteria
[Measurable outcomes]

## References
- references/domain.md - Detailed guide
- references/advanced.md - Advanced techniques
`

## Validation Commands

### Automated Validation

`bash
#!/bin/bash
# validate-skill.sh

echo "Validating skill structure..."

# Check name
if ! echo "$skill_name" | grep -qE '^[a-z][a-z0-9]*(-[a-z0-9]+)*$'; then
    echo "ERROR: Invalid name format"
    exit 1
fi

# Check SKILL.md
if [ $(wc -l < SKILL.md) -gt 400 ]; then
    echo "ERROR: SKILL.md exceeds 500 lines"
    exit 1
fi

# Check description
desc_length=$(grep -o "description:" SKILL.md | wc -c)
if [ $desc_length -gt 1024 ]; then
    echo "ERROR: Description too long"
    exit 1
fi

# Check references
if [ ! -d "references" ]; then
    echo "WARNING: No references/ directory"
fi

# Check examples
if [ ! -d "examples" ]; then
    echo "WARNING: No examples/ directory"
fi

echo "✓ Validation passed"
`

### Manual Validation

`markdown
# Validation Checklist

## Name
- [ ] 3-50 characters
- [ ] Kebab-case format
- [ ] Matches directory name
- [ ] No underscores or uppercase

## Description
- [ ] Starts with "(MODAL) USE when"
- [ ] 10-1024 characters
- [ ] Includes trigger phrases
- [ ] Describes actual capability

## Content
- [ ] SKILL.md under 500 lines
- [ ] Progressive disclosure implemented
- [ ] References organized properly
- [ ] Examples are concrete
- [ ] No TODO markers

## Standards
- [ ] Follows Universal Agentic Runtime
- [ ] Uses Cat Toolkit conventions
- [ ] Proper tool restrictions
- [ ] Token budget respected
`

## Anti-Patterns Quick Check

### ❌ Avoid These

**Description Issues:**
`yaml
# BAD
description: "A skill for data"
description: "Help with processing files"
description: "Tool for validation"

# GOOD
description: "USE when validating CSV files. Provides schema validation, data type checking, and format verification."
`

**Structure Issues:**
`markdown
# BAD
SKILL.md (1000+ lines with everything)

# GOOD
SKILL.md (300 lines) + references/ (detailed docs)
`

**Pattern Misuse:**
`markdown
# BAD
Router that does everything itself

# GOOD
Router that delegates to specialized skills
`

## Integration Quick Reference

### With toolkit-registry

`markdown
Use meta-skill for:
- Skill-specific guidance
- Implementation patterns
- Template selection

Reference toolkit-registry for:
- General standards
- Cross-component patterns
- Security requirements
`

### With scaffold-component

`markdown
Use meta-skill for:
- Learning patterns
- Manual creation
- Custom designs

Use scaffold-component for:
- Automated generation
- Quick prototypes
- Standard patterns
`

### With manage-healing

`markdown
Use meta-skill for:
- Prevention (standards)
- Best practices
- Pattern adherence

Reference manage-healing for:
- Failure diagnosis
- Repair workflows
- Drift detection
`

### With audit-security

`markdown
Use meta-skill for:
- Security-aware design
- Tool restriction planning
- Permission model design

Reference audit-security for:
- Security validation
- Vulnerability scanning
- Compliance checking
`

## Common Errors & Fixes

### Error: Name Too Long

**Problem:** Name exceeds 50 characters

**Fix:**
`markdown
# BAD
name: this-is-a-very-long-skill-name-that-exceeds-the-limit

# GOOD
name: long-skill-name
`

### Error: Description Too Vague

**Problem:** Description doesn't include triggers

**Fix:**
`markdown
# BAD
description: "SHOULD USE when processing data"

# GOOD
description: "SHOULD USE when processing CSV or JSON data files. Provides validation, transformation, and analysis capabilities."
`

### Error: SKILL.md Too Long

**Problem:** SKILL.md exceeds 500 lines

**Fix:**
`markdown
# Move to references/
- Advanced techniques → references/advanced.md
- Detailed API docs → references/api.md
- Complex workflows → workflows/process.md
- Edge cases → references/troubleshooting.md

# Keep in SKILL.md
- Overview
- Quick Start
- Core concepts (summary)
- Navigation to references
`

### Error: Missing Examples

**Problem:** No concrete examples

**Fix:**
`markdown
# Add examples/
examples/
├── basic-usage.md
│   - Simple use case
│   - Step-by-step
│   - Expected output
└── advanced-usage.md
    - Complex use case
    - Multiple steps
    - Edge cases
`

## Success Criteria Quick Check

### Quality Gates

`markdown
## Gate 1: Structure
- [ ] SKILL.md under 500 lines
- [ ] Progressive disclosure implemented
- [ ] Proper file organization

## Gate 2: Content
- [ ] Concrete examples provided
- [ ] Clear workflow defined
- [ ] Success criteria measurable

## Gate 3: Standards
- [ ] Naming conventions followed
- [ ] Description pattern correct
- [ ] Tool restrictions appropriate

## Gate 4: Usability
- [ ] Discovery works via natural language
- [ ] Examples are actionable
- [ ] Documentation is scannable

## Gate 5: Efficiency
- [ ] Token budget respected
- [ ] References properly used
- [ ] No redundant content
`

## Performance Tips

### Token Efficiency

`markdown
# Optimize token usage

## SKILL.md (< 500 lines)
- Use summaries
- Link to references
- Provide navigation

## references/ (loaded on-demand)
- Detailed explanations
- Advanced techniques
- Edge cases

## Avoid duplication
- Don't repeat content
- Use references for depth
- Keep SKILL.md concise
`

### Response Time

`markdown
# Optimize performance

## Lazy Loading
- Load references only when needed
- Use progressive disclosure
- Minimize context switching

## Smart Delegation
- Delegate efficiently
- Use concise prompts
- Cache results when possible
`

## Troubleshooting Quick Fixes

### Skill Not Discoverable

**Problem:** Users can't find skill

**Solution:**
1. Review description pattern
2. Add more trigger phrases
3. Test with natural language
4. Check naming conventions

### Poor User Experience

**Problem:** Users confused or frustrated

**Solution:**
1. Add concrete examples
2. Simplify workflow
3. Provide clear guidance
4. Test with real users

### Token Budget Exceeded

**Problem:** Description too long

**Solution:**
1. Shorten descriptions
2. Consolidate skills
3. Use progressive disclosure
4. Optimize references

### Validation Failures

**Problem:** Standards not met

**Solution:**
1. Run validation scripts
2. Check naming conventions
3. Verify description pattern
4. Review structure requirements

## Next Steps

After creating skill:

1. **Test Discovery**
   - Try triggering via natural language
   - Verify semantic matching
   - Adjust triggers if needed

2. **Validate Standards**
   - Run validation checklist
   - Check all requirements
   - Fix any issues

3. **Check Performance**
   - Verify token budget
   - Test response time
   - Optimize if needed

4. **Gather Feedback**
   - Test with users
   - Monitor usage
   - Iterate based on feedback

## Summary

**Remember:**
- Skills are knowledge bases
- Use progressive disclosure
- Follow naming conventions
- Provide concrete examples
- Validate thoroughly
- Optimize for users
- Respect token limits
- Test with real scenarios
