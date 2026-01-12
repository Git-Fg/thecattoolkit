# Naming Conventions for Skills

## Critical Importance

**Naming conventions are CRITICAL for Claude Code runtime stability.** Violations cause immediate crashes.

## Name Field Requirements

### Format Rules

`regex
Pattern: ^[a-z][a-z0-9]*(-[a-z0-9]+)*$
Length: 3-50 characters
Characters: lowercase letters (a-z), numbers (0-9), hyphens (-)
`

### Breakdown

| Rule | Description | Example |
|------|-------------|---------|
| **Start with letter** | First character must be a-z | ✅ pdf-processor ❌ 1-processor |
| **Lowercase only** | All characters lowercase | ✅ code-analyzer ❌ CodeAnalyzer |
| **Numbers allowed** | Numbers in middle/end | ✅ v2-processor ✅ api-v1 |
| **Hyphens allowed** | Separate words | ✅ code-analyzer ❌ code_analyzer |
| **No consecutive hyphens** | -- forbidden | ✅ pdf-processor ❌ pdf--processor |
| **No start/end hyphens** | Can't start or end with - | ✅ pdf-processor ❌ -processor |

## Valid Examples

### Simple Names
`yaml
✅ data-validator      # 15 chars
✅ pdf-processor       # 14 chars
✅ code-analyzer       # 13 chars
✅ image-resizer       # 13 chars
✅ csv-parser          # 10 chars
`

### Versioned Names
`yaml
✅ api-v1              # 7 chars
✅ analyzer-v2         # 11 chars
✅ processor-v3        # 13 chars
✅ data-v2-validator   # 16 chars
`

### Multi-Word Names
`yaml
✅ web-scraper         # 12 chars
✅ file-converter      # 14 chars
✅ image-generator     # 15 chars
✅ code-quality-check  # 17 chars
✅ database-migrator   # 17 chars
`

### Domain-Specific Names
`yaml
✅ postgres-connector  # 17 chars
✅ react-component    # 16 chars
✅ python-type-check  # 17 chars
✅ csv-data-cleaner   # 16 chars
✅ pdf-text-extractor # 18 chars
`

## Invalid Examples

### Character Violations
`yaml
❌ CodeAnalyzer        # Contains uppercase
❌ code_analyzer       # Contains underscore
❌ code.analyzer       # Contains period
❌ code@analyzer       # Contains special character
❌ code+analyzer       # Contains plus sign
❌ 1-processor         # Starts with number
`

### Length Violations
`yaml
❌ ab                  # Too short (2 chars)
❌ a                   # Too short (1 char)
❌ this-name-is-way-too-long-and-will-cause-validation-failure # Too long (68 chars)
`

### Hyphen Violations
`yaml
❌ -processor         # Starts with hyphen
❌ processor-          # Ends with hyphen
❌ pdf--processor     # Double hyphen
❌ code--analyzer     # Double hyphen
`

### Empty or Whitespace
`yaml
❌ ""                 # Empty string
❌ " "                # Whitespace only
❌ "  "               # Multiple whitespace
`

## Naming Strategy

### Descriptive but Concise

**Good:**
`yaml
✅ pdf-processor       # Clear purpose
✅ data-validator      # Clear function
✅ image-resizer       # Clear action
`

**Too Vague:**
`yaml
❌ tool               # Too generic
❌ processor          # Unclear what it processes
❌ handler            # Unclear what it handles
`

**Too Long:**
`yaml
❌ pdf-document-text-extraction-and-manipulation-tool # 53 chars
`

### Semantic Clarity

**Domain + Action:**
`yaml
✅ pdf-processor       # Domain: PDF, Action: Process
✅ csv-validator      # Domain: CSV, Action: Validate
✅ image-resizer      # Domain: Image, Action: Resize
`

**Action + Target:**
`yaml
✅ validate-csv       # Action: Validate, Target: CSV
✅ resize-image       # Action: Resize, Target: Image
✅ extract-pdf-text  # Action: Extract, Target: PDF Text
`

### Consistency Patterns

**Use consistent patterns within a skill family:**

`yaml
# Data processing family
✅ csv-parser
✅ json-validator
✅ xml-converter

# Image processing family
✅ image-resizer
✅ image-cropper
✅ image-filter

# Web scraping family
✅ web-scraper
✅ page-parser
✅ link-extractor
`

## Cat Toolkit Examples

### From Current Ecosystem

**sys-core skills:**
`yaml
✅ audit-security      # 15 chars
✅ check-types        # 12 chars
✅ manage-healing     # 15 chars
✅ meta-hooks         # 10 chars
✅ meta-mcp           # 8 chars
✅ scaffold-component # 18 chars
✅ toolkit-registry   # 16 chars
✅ validate-toolkit   # 17 chars
`

**All follow:**
- Lowercase only
- Hyphen-separated words
- 3-50 character limit
- Descriptive purpose

## Validation Commands

### Regex Validation
`bash
# Test if name matches pattern
skill_name="pdf-processor"
if [[ $skill_name =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]]; then
    echo "✓ Valid name"
else
    echo "✗ Invalid name"
fi
`

### Length Check
`bash
# Check name length
skill_name="pdf-processor"
length=${#skill_name}

if [ $length -ge 3 ] && [ $length -le 50 ]; then
    echo "✓ Length valid ($length chars)"
else
    echo "✗ Length invalid ($length chars)"
fi
`

### Comprehensive Validation Script
`bash
#!/bin/bash
# validate-skill-name.sh

skill_name="$1"

if [ -z "$skill_name" ]; then
    echo "Usage: $0 <skill-name>"
    exit 1
fi

# Check length
if [ ${#skill_name} -lt 3 ]; then
    echo "✗ Too short (${#skill_name} chars, minimum 3)"
    exit 1
fi

if [ ${#skill_name} -gt 50 ]; then
    echo "✗ Too long (${#skill_name} chars, maximum 50)"
    exit 1
fi

# Check pattern
if [[ ! $skill_name =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]]; then
    echo "✗ Invalid format"
    echo "  Must: lowercase letters, numbers, hyphens"
    echo "  Must: start with letter"
    echo "  Must: no consecutive hyphens"
    echo "  Must: no hyphens at start/end"
    exit 1
fi

echo "✓ Valid skill name: $skill_name"
`

## Directory Name Matching

### Critical Rule

**The name field MUST match the directory name exactly.**

`
# CORRECT
skill-name/
└── SKILL.md
    name: skill-name  # Matches directory

# INCORRECT
skill-name/
└── SKILL.md
    name: skill_name  # Doesn't match (underscore)
`

### Automated Checking
`bash
#!/bin/bash
# check-skill-directory.sh

skill_dir="$1"
skill_name="$2"

if [ -z "$skill_dir" ] || [ -z "$skill_name" ]; then
    echo "Usage: $0 <skill-directory> <skill-name>"
    exit 1
fi

dir_name=$(basename "$skill_dir")

if [ "$dir_name" == "$skill_name" ]; then
    echo "✓ Directory name matches skill name"
else
    echo "✗ Mismatch:"
    echo "  Directory: $dir_name"
    echo "  Name field: $skill_name"
    exit 1
fi
`

## Good Naming Patterns

### Pattern 1: Domain-Action
`
{domain}-{action}
`
**Examples:**
- pdf-processor (process PDFs)
- csv-validator (validate CSVs)
- image-resizer (resize images)

### Pattern 2: Action-Domain
`
{action}-{domain}
`
**Examples:**
- validate-csv (validate CSV)
- convert-json (convert JSON)
- scrape-web (scrape web)

### Pattern 3: Compound Domain
`
{compound-domain}-{action}
`
**Examples:**
- web-scraper (scrape web)
- database-migrator (migrate database)
- api-client (client for API)

### Pattern 4: Versioned
`
{base-name}-v{number}
`
**Examples:**
- analyzer-v2 (version 2 of analyzer)
- processor-v3 (version 3 of processor)

## Bad Naming Patterns

### Too Generic
`yaml
❌ helper           # What does it help with?
❌ tool             # Too vague
❌ utils            # Which utilities?
❌ core             # Core what?
❌ main             # Main what?
`

### Unclear Purpose
`yaml
❌ processor        # Process what?
❌ handler          # Handle what?
❌ manager          # Manage what?
❌ system           # What system?
❌ engine           # What engine?
`

### Overly Complex
`yaml
❌ pdf-document-processing-and-manipulation-tool # Too long, unclear
❌ web-scraping-and-data-extraction-utility     # Too long
❌ advanced-image-filtering-and-resize-module    # Too long
`

### Inconsistent
`yaml
# Don't mix patterns
❌ csv-parser
❌ JSON-validator     # Inconsistent capitalization
❌ XMLConverter       # Inconsistent capitalization
❌ pdf_processor      # Underscore instead of hyphen
`

## Refactoring Existing Skills

### From Bad to Good

**Step 1: Identify Issues**
`bash
# Check current name
grep "name:" SKILL.md

# Validate format
./validate-skill-name.sh <current-name>
`

**Step 2: Choose New Name**
`
Current: PDFProcessor
Issues: Uppercase, unclear

Better: pdf-processor
`

**Step 3: Rename Directory**
`bash
# Move directory
mv PDFProcessor pdf-processor

# Update name field in SKILL.md
sed -i 's/name: PDFProcessor/name: pdf-processor/' SKILL.md
`

**Step 4: Validate**
`bash
# Re-check
./validate-skill-name.sh pdf-processor
`

## Naming for Different Skill Types

### Processing Skills
`
{format}-{operation}
`
**Examples:**
- pdf-extract (extract from PDF)
- csv-parse (parse CSV)
- json-transform (transform JSON)

### Analysis Skills
`
{domain}-analyzer
`
**Examples:**
- code-analyzer (analyze code)
- data-analyzer (analyze data)
- security-analyzer (analyze security)

### Validation Skills
`
{domain}-validator
`
**Examples:**
- csv-validator (validate CSV)
- json-validator (validate JSON)
- schema-validator (validate schema)

### Conversion Skills
`
{from}-to-{to}
`
**Examples:**
- csv-to-json (convert CSV to JSON)
- pdf-to-text (convert PDF to text)
- xml-to-json (convert XML to JSON)

## Special Considerations

### Abbreviations
`yaml
# Use full words when possible
✅ javascript-processor  # Clear
❌ js-processor          # Less clear

# Abbreviations okay if well-known
✅ api-client            # API is widely known
✅ http-client          # HTTP is standard
`

### Numbers in Names
`yaml
# Numbers in middle/end are okay
✅ api-v1                # Version 1
✅ analyzer-v2           # Version 2
✅ processor-2x          # 2x variant

# Numbers at start are NOT okay
❌ 1-processor           # Invalid
❌ 2-analyzer            # Invalid
`

### Acronyms
`yaml
# All caps in middle okay if established
✅ api-gateway
✅ http-proxy
✅ sql-connector

# But prefer lowercase
✅ api-gateway    # Good
✅ ApiGateway     # Bad (uppercase)
`

## Testing Naming Decisions

### Questions to Ask

1. **Is it descriptive?**
   - Can a user understand what it does from the name?

2. **Is it concise?**
   - Under 50 characters?
   - No unnecessary words?

3. **Does it follow patterns?**
   - Consistent with similar skills?
   - Follows established conventions?

4. **Is it searchable?**
   - Keywords users would search for?
   - Contains relevant terms?

### User Testing
`markdown
Ask: "What would you call a skill that processes PDF files?"

Expected answers:
- pdf-processor ✓
- pdf-handler  ✓
- pdf-tool     ✓

Unexpected:
- processor    ❌ (too generic)
- helper       ❌ (too vague)
`

## Common Mistakes

### Mistake 1: Copying Internal Names
`yaml
# Don't use internal project names
❌ internal-project-name
❌ company-product-code
❌ legacy-system-name

# Use user-facing names
✅ pdf-processor
✅ document-converter
`

### Mistake 2: Technical Jargon
`yaml
# Too technical
❌ asynchronous-processor
❌ multi-threaded-handler
❌ event-driven-listener

# User-friendly
✅ background-processor
✅ concurrent-handler
✅ event-listener
`

### Mistake 3: Implementation Details
`yaml
# Implementation detail
❌ react-component-builder
❌ python-script-runner
❌ nodejs-server-deployer

# User benefit
✅ component-generator
✅ script-automation
✅ server-deployer
`

## Summary Checklist

### Before Publishing

**Name Validation:**
- [ ] 3-50 characters
- [ ] Matches pattern: ^[a-z][a-z0-9]*(-[a-z0-9]+)*$
- [ ] All lowercase
- [ ] No consecutive hyphens
- [ ] No start/end hyphens
- [ ] Matches directory name

**Quality Check:**
- [ ] Descriptive and clear
- [ ] Concise but not vague
- [ ] Follows established patterns
- [ ] Consistent with similar skills
- [ ] User-friendly terminology

**Final Verification:**
`bash
# Run validation
./validate-skill-name.sh <skill-name>

# Check directory match
./check-skill-directory.sh <skill-dir> <skill-name>

# Verify no conflicts
grep -r "name: <skill-name>" ./
`

**Remember:** A good name is clear, consistent, and follows conventions. Take time to choose wisely—it can't be changed easily once published.
