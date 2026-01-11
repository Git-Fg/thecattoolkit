---
name: meta-builder
description: "USE when building, validating, or auditing Agent Skills according to the official Agent Skills specification from agentskills.io. Creates compliant SKILL.md files with proper frontmatter, implements progressive disclosure, and validates against the open standard format."
context: fork
model: opus
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
---

# Meta Builder Skill - Agent Skills Framework

## Overview

This skill implements the official Agent Skills framework from [agentskills.io](https://agentskills.io/), an open standard developed by Anthropic for extending AI agent capabilities.

Agent Skills are folders containing a `SKILL.md` file with YAML frontmatter and Markdown instructions. This skill helps you create, validate, and maintain skills that comply with the official specification.

## Core Principles

### 1. Directory Structure

A valid skill must be a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md          # Required
```

Optional directories for enhanced skills:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: additional documentation
└── assets/           # Optional: templates, resources
```

### 2. SKILL.md Format

Every `SKILL.md` must contain:

**YAML Frontmatter (Required):**
```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

**Markdown Body:** Step-by-step instructions, examples, and guidance.

### 3. Progressive Disclosure

Skills use progressive disclosure to manage context efficiently:

1. **Discovery (~50-100 tokens):** Only `name` and `description` loaded at startup
2. **Activation (<500 lines):** Full `SKILL.md` loaded when skill is activated
3. **Resources (on-demand):** Files in scripts/, references/, assets/ loaded only when needed

## Frontmatter Specification

### Required Fields

#### `name`
- **Constraints:** 1-64 characters, lowercase alphanumeric and hyphens only
- **Rules:** Must match directory name, no consecutive hyphens, no leading/trailing hyphens
- **Examples:** `pdf-processing`, `data-analysis`, `code-review`

#### `description`
- **Constraints:** 1-1024 characters
- **Requirements:** Must describe both what the skill does AND when to use it
- **Best Practice:** Include specific keywords that help agents identify relevant tasks
- **Example:**
  ```yaml
  description: "Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction."
  ```

### Optional Fields

#### `license`
- Specifies the license applied to the skill
- Keep it short (license name or bundled file reference)

#### `compatibility`
- Indicates environment requirements (1-500 characters)
- Examples: "Designed for Claude Code", "Requires git, docker, jq, and internet access"

#### `metadata`
- Arbitrary key-value mapping for additional metadata
- Use unique key names to avoid conflicts
- Example:
  ```yaml
  metadata:
    author: example-org
    version: "1.0"
  ```

#### `allowed-tools` (Experimental)
- Space-delimited list of pre-approved tools
- **Note:** Experimental feature, support varies between agent implementations

## Workflows

### Creating a New Skill

1. **Parse Requirements:** Identify the skill's purpose and use cases
2. **Generate Name:** Create valid skill name (lowercase, hyphens, matches directory)
3. **Write Description:** Include specific keywords and "when to use" guidance
4. **Structure Content:** Use progressive disclosure (main SKILL.md <500 lines)
5. **Add Resources:** Create scripts/, references/, assets/ as needed
6. **Validate:** Check against official specification

### Validating Existing Skills

Use the official skills-ref validation library:

```bash
skills-ref validate <path>
```

Check:
- [ ] YAML frontmatter is valid
- [ ] Name matches directory name
- [ ] Description follows specification
- [ ] Progressive disclosure implemented
- [ ] Optional directories structured correctly

### Auditing Skills

For existing skills, verify:

1. **Frontmatter Compliance:**
   - Valid name field
   - Descriptive "when to use" text
   - Proper optional fields

2. **Structure Compliance:**
   - Minimum: SKILL.md file present
   - Optional: scripts/, references/, assets/ directories
   - Progressive disclosure: <500 lines in main SKILL.md

3. **Content Quality:**
   - Clear step-by-step instructions
   - Examples of inputs/outputs
   - Common edge cases covered
   - Self-documenting code and references

## Best Practices

### Writing Effective Descriptions

**Good Example:**
```yaml
description: "Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction."
```

**Poor Example:**
```yaml
description: "Helps with PDFs."
```

### Progressive Disclosure Pattern

**SKILL.md** (<400 lines - router):
- High-level overview
- Quick reference
- Triggers for loading reference files

**references/** (detailed theory):
- Technical reference material
- Domain-specific guides
- Extended examples

**scripts/** (executable code):
- Self-contained or clearly documented
- Helpful error messages
- Graceful edge case handling

### File References

Use relative paths from skill root:
```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

Keep references one level deep from SKILL.md.

## Integration with Agent Implementations

Agent Skills are supported by leading AI development tools. The format was developed by Anthropic and released as an open standard.

**Discovery Process:**
1. Agent scans configured directories for skill folders
2. Parses frontmatter metadata (name, description) at startup
3. Matches user tasks to relevant skills via description keywords
4. Loads full instructions when skill is activated
5. Executes scripts and accesses resources as needed

**Security Considerations:**
- Scripts run in isolated environments
- Allowlisting trusted skills only
- Confirmation before dangerous operations
- Logging for audit purposes

## Validation Tools

Use the official [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) library:

**Validate a skill directory:**
```bash
skills-ref validate <path>
```

**Generate `<available_skills>` XML:**
```bash
skills-ref to-prompt <path>...
```

## External Resources

- **Specification:** https://agentskills.io/specification
- **Integration Guide:** https://agentskills.io/integrate-skills
- **Example Skills:** https://github.com/anthropics/skills
- **Reference Library:** https://github.com/agentskills/agentskills/tree/main/skills-ref
- **Best Practices:** https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Examples

**Creating a PDF Processing Skill:**
```bash
# 1. Create directory
mkdir pdf-processing
cd pdf-processing

# 2. Create SKILL.md with proper frontmatter
cat > SKILL.md << 'EOF'
---
name: pdf-processing
description: "Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction."
---

# PDF Processing Skill

## When to use this skill
Use this skill when...
EOF

# 3. Add optional directories
mkdir scripts references assets

# 4. Validate
skills-ref validate pdf-processing
```
