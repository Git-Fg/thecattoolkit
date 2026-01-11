# Official Agent Skills Documentation

This skill implements the official Agent Skills open standard from [agentskills.io](https://agentskills.io/).

## Core Resources

| Resource | URL | Purpose |
| :--- | :--- | :--- |
| **Homepage** | https://agentskills.io/home | Overview of Agent Skills framework |
| **Specification** | https://agentskills.io/specification | Complete format specification for SKILL.md files |
| **Integration Guide** | https://agentskills.io/integrate-skills | How to add skills support to agents/tools |
| **What are Skills?** | https://agentskills.io/what-are-skills | Understanding skills and progressive disclosure |

## Development Resources

| Resource | URL | Purpose |
| :--- | :--- | :--- |
| **Example Skills** | https://github.com/anthropics/skills | Browse example skills on GitHub |
| **Reference Library** | https://github.com/agentskills/agentskills/tree/main/skills-ref | Validate skills and generate prompt XML |
| **GitHub Repository** | https://github.com/agentskills/agentskills | Open development repository |

## Key Concepts

### Progressive Disclosure
Skills use progressive disclosure to manage context efficiently:

1. **Discovery (~50-100 tokens):** Only name and description loaded at startup
2. **Activation (<500 lines):** Full SKILL.md loaded when skill is activated
3. **Resources (on-demand):** Files in scripts/, references/, assets/ loaded only when needed

### Frontmatter Specification

**Required fields:**
- `name`: 1-64 characters, lowercase alphanumeric and hyphens only
- `description`: 1-1024 characters, describes what and when to use

**Optional fields:**
- `license`: License name or reference
- `compatibility`: Environment requirements (1-500 chars)
- `metadata`: Arbitrary key-value mapping
- `allowed-tools`: Pre-approved tools (experimental)

### Directory Structure

```
skill-name/
├── SKILL.md          # Required
├── scripts/          # Optional: executable code
├── references/       # Optional: additional documentation
└── assets/           # Optional: templates, resources
```

## Validation

Use the official skills-ref library to validate skills:

```bash
# Validate a skill directory
skills-ref validate <path>

# Generate available_skills XML
skills-ref to-prompt <path>...
```

## Security Considerations

When implementing Agent Skills support:

- **Sandboxing**: Run scripts in isolated environments
- **Allowlisting**: Only execute scripts from trusted skills
- **Confirmation**: Ask users before running potentially dangerous operations
- **Logging**: Record all script executions for auditing
