# Progressive Disclosure Pattern

## Overview

**Progressive disclosure** is the principle of revealing information gradually based on user needs, keeping the main skill file concise while providing detailed documentation in reference files.

## Core Principle

**Keep SKILL.md under 500 lines** while providing comprehensive guidance through organized reference files.

## Benefits

1. **Token Efficiency** - Main context stays lean
2. **Faster Discovery** - Users find relevant info quickly
3. **Better Organization** - Related content grouped logically
4. **Easier Maintenance** - Update specific topics independently
5. **Improved UX** - Users see only what they need

## Structure Pattern

### Main SKILL.md (Router)

`markdown
# Skill Name

## Overview
Brief description of what this skill accomplishes.

## Quick Start
Immediate solution for common case:
`language
quick_solution()
`

## Core Capabilities
- Capability 1: Brief description
- Capability 2: Brief description
- Capability 3: Brief description

## For More Details
See:
- references/domain1.md - Detailed guide
- references/domain2.md - API reference
- examples/use-case1.md - Example workflow

## Advanced Topics
- Advanced Topic 1 → See references/advanced1.md
- Advanced Topic 2 → See references/advanced2.md
`

### Reference Files (Deep Dive)

Each reference file is 100+ lines of detailed information on a specific topic.

`
references/
├── domain1.md          # Comprehensive guide (200+ lines)
├── domain2.md         # API reference (150+ lines)
├── advanced-topics.md  # Edge cases (100+ lines)
└── troubleshooting.md  # Common issues (100+ lines)
`

## Implementation Patterns

### Pattern 1: Domain-Based Organization

**Use when:** Skill covers multiple distinct domains

**Structure:**
`
skill-name/
├── SKILL.md (overview + navigation)
└── references/
    ├── domain1.md    # Complete guide to domain 1
    ├── domain2.md    # Complete guide to domain 2
    ├── domain3.md    # Complete guide to domain 3
`

**Example: Data Analysis Skill**
`markdown
# Data Analysis Skill

## Quick Start
`python
analyze_data('data.csv')
`

## Core Capabilities
- **CSV Analysis:** Validate and process CSV files
- **JSON Processing:** Transform and validate JSON data
- **Statistical Analysis:** Calculate metrics and trends

## For More Details
- references/csv-processing.md - CSV workflows
- references/json-processing.md - JSON operations
- references/statistics.md - Statistical methods
`

**CSV Reference File:**
`markdown
# CSV Processing

## Overview
Comprehensive guide to CSV processing capabilities.

## Supported Formats
[Detailed specifications]

## Common Operations
[Step-by-step workflows]

## Error Handling
[Troubleshooting guide]

## Examples
[Code examples]
`

### Pattern 2: Workflow-Based Organization

**Use when:** Skill involves complex multi-step processes

**Structure:**
`
skill-name/
├── SKILL.md (overview)
└── references/
    ├── workflow1.md   # Complete workflow documentation
    ├── workflow2.md   # Complete workflow documentation
    └── workflows/
        ├── detailed-steps.md  # Step-by-step breakdown
        └── edge-cases.md     # Complex scenarios
`

**Example: Deployment Skill**
`markdown
# Deployment Skill

## Quick Start
`bash
deploy --environment=production
`

## Supported Workflows
- **Simple Deploy:** Single service deployment
- **Rolling Deploy:** Zero-downtime updates
- **Blue-Green Deploy:** Traffic switching

## For More Details
- references/simple-deployment.md
- references/rolling-deployment.md
- references/blue-green-deployment.md
`

### Pattern 3: Capability-Based Organization

**Use when:** Multiple related capabilities

**Structure:**
`
skill-name/
├── SKILL.md (capabilities overview)
└── references/
    ├── capability1.md  # Detailed capability docs
    ├── capability2.md  # Detailed capability docs
    └── capability3.md  # Detailed capability docs
`

**Example: PDF Processing Skill**
`markdown
# PDF Processing

## Quick Start
`python
extract_text('document.pdf')
`

## Core Capabilities
- **Text Extraction:** Pull text from PDF pages
- **Page Manipulation:** Merge, split, rotate pages
- **Form Filling:** Complete PDF forms programmatically

## For More Details
- references/text-extraction.md
- references/page-manipulation.md
- references/form-filling.md
`

## Reference File Structure

### Standard Reference File Template

`markdown
# Topic Name

## Overview
[What this topic covers - 2-3 sentences]

## Prerequisites
[What users need before starting]

## Core Concepts
[Essential knowledge]

### Concept 1
[Detailed explanation]

### Concept 2
[Detailed explanation]

## Step-by-Step Guide
[Detailed workflow]

### Step 1: [Action]
[Instructions]

### Step 2: [Action]
[Instructions]

## Advanced Topics

### Advanced Topic 1
[Complex scenario]

### Advanced Topic 2
[Complex scenario]

## Common Patterns
[Reusable patterns]

## Examples

### Example 1: [Use Case]
`language
// Code example
example_code()
`

### Example 2: [Use Case]
`language
// Code example
example_code()
`

## Error Handling

### Common Errors
[Troubleshooting table]

### Error Resolution
[How to fix each error]

## Best Practices
[Recommendations]

## See Also
- related-topic.md - Related information
- another-topic.md - Another topic
`

## Examples from Cat Toolkit

### Example 1: prompt-engineering

**Structure:**
`
skills/prompt-engineering/
├── SKILL.md (280 lines - overview + navigation)
├── references/
│   ├── core-standards.md     (250+ lines)
│   ├── optimization.md       (200+ lines)
│   ├── design-patterns.md    (180+ lines)
│   ├── anti-patterns.md       (150+ lines)
│   └── metadata.md           (120+ lines)
├── examples/
│   └── workflows/
│       ├── research-workflow.md
│       └── optimization-workflow.md
└── assets/
    ├── chain/
    ├── meta/
    └── single-prompt.md
`

**SKILL.md Navigation:**
`markdown
## Core Standards
- references/core-standards.md - Fundamental principles
- references/design-patterns.md - Proven patterns
- references/anti-patterns.md - Common mistakes

## Advanced Topics
- references/optimization.md - Performance optimization
- references/metadata.md - Metadata management

## Examples
- examples/workflows/research-workflow.md
- examples/workflows/optimization-workflow.md
`

### Example 2: toolkit-registry

**Structure:**
`
skills/toolkit-registry/
├── SKILL.md (300 lines - overview + navigation)
├── references/
│   ├── standards-communication.md
│   ├── command-standards.md
│   ├── agent-security.md
│   └── syntax-guide.md
├── assets/
│   ├── standard-skill.md
│   ├── progressive-disclosure.md
│   └── router-pattern.md
└── examples/
    ├── router-pattern.md
    └── bash-logic.md
`

## When to Use Progressive Disclosure

### ✅ Use When

**Complex Domains**
- Multiple related capabilities
- Rich feature sets
- Detailed workflows

**Token Efficiency Needed**
- SKILL.md approaching 500 lines
- Detailed examples taking space
- Comprehensive documentation required

**Organizational Benefits**
- Related content logically grouped
- Easier to find specific information
- Modular documentation

**Active Development**
- Frequent updates to specific areas
- Independent versioning of topics
- Parallel documentation work

### ❌ Don't Use When

**Simple Skills**
- Single straightforward purpose
- SKILL.md under 200 lines
- Minimal documentation needed

**Overhead Not Justified**
- Only 1-2 reference files needed
- Content doesn't naturally separate
- Adds complexity without benefit

**Quick Reference Skills**
- Users need immediate answers
- Minimal setup or configuration
- Self-contained workflows

## Advanced Patterns

### Pattern 1: Multi-Level Disclosure

`
SKILL.md (overview)
  ↓
references/category1.md (high-level)
  ↓
references/category1/ (sub-references)
    ├── detailed-topic1.md
    └── detailed-topic2.md
`

**Example:**
`markdown
# PDF Processing

## For More Details
- references/text-extraction.md - Overview

# Text Extraction
[In references/text-extraction.md]

## Advanced Topics
- text-extraction/pdf-text.md - PDF-specific
- text-extraction/ocr-text.md - OCR methods
`

### Pattern 2: Conditional Loading

**In SKILL.md:**
`markdown
## For [Specific Use Case]
- use-case-specific.md
  - Load this only if working with [specific technology]
`

**Reference File Header:**
`markdown
# Use Case Specific Guide

**Prerequisites:** This guide assumes:
- [Specific requirement 1]
- [Specific requirement 2]

**Load only if:** Working with [specific context]
`

### Pattern 3: Versioned References

`
references/
├── v1/
│   ├── topic1.md
│   └── topic2.md
├── v2/
│   ├── topic1.md
│   └── topic2.md
└── current.md -> v2/topic1.md
`

## Best Practices

### DO

✅ **Keep SKILL.md under 500 lines**
✅ **Link to references from main sections**
✅ **Use descriptive reference filenames**
✅ **Include context in reference introductions**
✅ **Cross-reference between related topics**
✅ **Group references logically**
✅ **Include examples in reference files**
✅ **Maintain consistent structure**

### DON'T

❌ **Create reference files under 50 lines**
❌ **Duplicate content between files**
❌ **Use generic reference names (e.g., "details.md")**
❌ **Embed references in main file**
❌ **Create too many shallow references**
❌ **Forget to link to references**
❌ **Mix unrelated topics in one file**
❌ **Ignore cross-references**

## Validation

### Checklist

**SKILL.md Structure:**
- [ ] Under 500 lines recommended
- [ ] Clear navigation to references
- [ ] Quick start section
- [ ] Core capabilities summary
- [ ] Link to all reference files

**Reference Files:**
- [ ] 100+ lines each
- [ ] Focused on single topic
- [ ] Consistent structure
- [ ] Cross-references included
- [ ] Examples provided

**Organization:**
- [ ] Logical grouping
- [ ] Descriptive filenames
- [ ] Clear hierarchy
- [ ] Easy navigation

## Token Budget Considerations

### Impact on Token Limit

**With Progressive Disclosure:**
- SKILL.md: ~10,000 characters
- Reference 1: ~15,000 characters (loaded only if needed)
- Reference 2: ~12,000 characters (loaded only if needed)
- Total metadata: ~37,000 characters

**Without Progressive Disclosure:**
- SKILL.md: ~37,000 characters (everything embedded)
- Total metadata: ~37,000 characters

**Key Difference:** References are loaded only when needed, not all at once.

### Optimization Strategy

1. **Minimize SKILL.md** - Keep essential info only
2. **Prioritize references** - Load heavy content on-demand
3. **Index strategically** - Link to references from multiple SKILL.md sections
4. **Cache references** - Don't reload frequently accessed references

## Migration Guide

### From Monolithic to Progressive

**Step 1: Audit Current SKILL.md**
`bash
wc -l SKILL.md
`

**Step 2: Identify Logical Groups**
`markdown
# Current SKILL.md content
- Topic A (100 lines)
- Topic B (150 lines)
- Topic C (200 lines)
`

**Step 3: Extract to References**
`bash
# Extract Topic A
sed -n '/^# Topic A/,/^# Topic B/p' SKILL.md > references/topic-a.md

# Extract Topic B
sed -n '/^# Topic B/,/^# Topic C/p' SKILL.md > references/topic-b.md

# Extract Topic C
sed -n '/^# Topic C/,$p' SKILL.md > references/topic-c.md
`

**Step 4: Update SKILL.md**
`markdown
# Skill Name

## Overview
[Keep short]

## Quick Start
[Keep essential]

## Core Capabilities
- Topic A: Brief description → See topic-a.md
- Topic B: Brief description → See topic-b.md
- Topic C: Brief description → See topic-c.md
`

## Success Metrics

### Measurable Improvements

**Before:**
- SKILL.md: 800 lines
- Discovery time: 30 seconds
- User confusion: High

**After:**
- SKILL.md: 250 lines
- Discovery time: 10 seconds
- User confusion: Low

### User Experience Indicators

- Users find information faster
- Fewer follow-up questions
- Better understanding of capabilities
- More effective skill usage

## Summary

Progressive disclosure enables:

✅ **Token efficiency** - Load details on-demand
✅ **Better organization** - Logical content grouping
✅ **Improved UX** - Faster information discovery
✅ **Easier maintenance** - Update specific topics independently
✅ **Scalable documentation** - Add references without bloating main file

**Remember:** The goal is helping users find exactly what they need, when they need it, without overwhelming them with information.
