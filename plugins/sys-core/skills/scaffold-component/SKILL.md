---
name: scaffold-component
description: "SHOULD USE when generating new plugin components (skills, agents, commands). Scaffolds with 2026 Universal Agentic Runtime standards, frontmatter, and templates."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash(mkdir:-p), Bash(ls:*), Bash(cat:*), Bash(find:*)]
---

# Component Scaffolding Protocol

## Core Principle

**Transform natural language specifications into production-ready plugin components.** Generate complete, standards-compliant file structures with proper YAML frontmatter, following the 2026 Universal Agentic Runtime architecture.

## Execution Framework

### 1. Parse Component Specification

**Extract from user input:**
- **Component Type**: skill, agent, or command
- **Component Name**: lowercase-with-hyphens (max 64 chars)
- **Language/Framework**: python, typescript, javascript, etc.
- **Complexity Level**: minimal, standard, or complex
- **Special Requirements**: hooks, allowed-tools, specific templates

**Default Values (when unspecified):**
- Location: project-level (`.claude/`)
- Language: based on project context
- Complexity: standard
- Permission Mode: inherited from environment

### 2. Apply Universal Agentic Runtime Standards

**Generate compliant components following:**

**For Skills:**
- SKILL.md with proper frontmatter (name, description, allowed-tools)
- Description following Discovery Tiering Matrix
- context: fork for isolated execution
- agent binding when appropriate
- Directory structure: skill-name/SKILL.md (+ scripts/, references/, assets/ if needed)

**For Agents:**
- Markdown file with YAML frontmatter
- name: lowercase-with-hyphens
- description: role definition with "MUST USE when" trigger
- tools: explicit whitelist (never omit)
- skills: auto-load relevant skills
- model: omit unless specified (defaults to configured subagent model)

**For Commands:**
- Markdown file with YAML frontmatter
- description: clear purpose with natural language triggers
- $ARGUMENTS placeholder for user input
- argument-hint: UI documentation
- allowed-tools: safety restrictions

### 3. Template Selection Logic

**Minimal Complexity:**
- Single component, straightforward purpose
- Standard frontmatter only
- No additional directories

**Standard Complexity:**
- Single component with standard features
- May include references/ for documentation
- Standard templates from existing bootstrap skills

**Complex Complexity:**
- Multi-component system
- references/, assets/, scripts/ directories as needed
- Router pattern or progressive disclosure patterns
- Multiple templates combined

### 4. Frontmatter Generation

**Generate valid YAML with:**
- All required fields populated
- Appropriate optional fields based on component type
- No redundant defaults (e.g., user-invocable: true)
- Proper tool permissions and restrictions

### 5. File Creation

**Create files in correct locations:**
- Skills: `.claude/skills/skill-name/SKILL.md` (or plugin-level)
- Agents: `.claude/agents/agent-name.md`
- Commands: `.claude/commands/command-name.md`

**Write complete, production-ready files with:**
- Proper YAML frontmatter
- Complete content following standards
- No TODO markers or placeholder text
- Ready to use immediately

## Quality Gates

**Generated components must:**
- Pass YAML validation
- Follow naming conventions
- Include proper descriptions for semantic discovery
- Have appropriate tool restrictions
- Be self-contained (no cross-component coupling)
- Match 2026 Universal Agentic Runtime standards

## Output Format

**Return structured summary:**
- Component Type and Name
- Location created
- Files generated
- Key features enabled
- Next steps (if any)

**Example Output:**
```
✓ Created skill: database-validator
  Location: .claude/skills/database-validator/SKILL.md
  Features: context: fork, agent: plugin-expert, allowed-tools: [Read, Grep]
  Status: Ready to use
```

## Error Handling

**If component exists:**
- Report "Component already exists at [location]"
- Offer to overwrite or create with different name
- Never proceed without explicit confirmation

**If invalid specification:**
- Use reasonable defaults
- Apply standards-based decisions
- Never block on missing optional details

**If directory creation fails:**
- Verify path permissions
- Use project-level as fallback
- Report specific failure reason

## Standards References

**Core Architecture:**
- CLAUDE.md Part IV (SKILL Protocol)
- CLAUDE.md Part III (AGENT Architecture)
- CLAUDE.md Part II (COMMAND Patterns)

**Bootstrap Patterns:**
- toolkit-registry skill for component creation standards
- meta-builder skill for component patterns
- scaffold-component skill for generation workflows

**Template Library:**
- Consult existing templates in sys-core/skills/*/assets/templates/
- Follow progressive disclosure patterns
- Apply router pattern for complex skills
