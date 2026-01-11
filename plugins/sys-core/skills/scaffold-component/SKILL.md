---
name: scaffold-component
description: "MUST USE when creating new plugin components (skills, agents, commands) or scaffolding 2026 Universal Agentic Runtime components with proper frontmatter and templates."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash(mkdir:-p), Bash(ls:*), Bash(cat:*), Bash(find:*)]
---

# Component Scaffolding Protocol

## Core Principle

**Transform natural language specifications into production-ready plugin components.** Generate complete, standards-compliant file structures with proper YAML frontmatter, following the 2026 Universal Agentic Runtime architecture.

## Execution Framework

### 1. Parse Component Specification

**Extract from user input:**
- **Component Type**: skill (default 80%), agent, or command
- **Component Name**: lowercase-with-hyphens (max 64 chars)
- **Language/Framework**: python, typescript, javascript, etc.
- **Complexity Level**: minimal, standard, or complex
- **Special Requirements**: hooks, allowed-tools, specific templates

**Default Values (when unspecified):**
- Type: **Skill** (The 80% Rule)
- Location: project-level (`.claude/`)
- Language: based on project context
- Complexity: standard
- Permission Mode: inherited from environment

### 2. Apply Universal Agentic Runtime Standards

**Generate compliant components following:**

**For Skills (The Knowledge Base):**
- SKILL.md with proper frontmatter (name, description, allowed-tools)
- Description following Discovery Tiering Matrix ("USE when...")
- **Recommendation:** Suggest generating a companion **Command Shortcut** (`commands/name.md`) for easier invocation according to the 2026 Hybrid Standard.
- Directory structure: skill-name/SKILL.md (+ scripts/, references/, assets/ if needed)

**For Commands (The Shortcut):**
- Markdown file with YAML frontmatter
- **Shortcut Pattern:** If wrapping a skill, set `allowed-tools: [Skill(name)]` and `disable-model-invocation: true`.
- description: clear purpose with natural language triggers
- $ARGUMENTS placeholder for user input
- argument-hint: UI documentation
- allowed-tools: safety restrictions

**For Agents (The Specialist):**
- Markdown file with YAML frontmatter
- name: lowercase-with-hyphens
- description: role definition with "MUST USE when" trigger
- tools: explicit whitelist (never omit)
- skills: auto-load relevant skills
- model: do not specify (defaults to configured subagent model)

### 3. Hardcore Naming Constraints (Anti-Crash)

**You MUST follow these rules strictly. Violations cause the runtime to crash.**

**Name Field Rules:**
1. **Length:** 1-64 characters exactly.
2. **Charset:** Lowercase `a-z`, `0-9`, `-` ONLY. No underscores `_`. No uppercase.
3. **Format:** No consecutive hyphens (`--`). Cannot start/end with `-`.
4. **Consistency:** Skill filename `name` MUST match its parent directory name.

**Valid:** `pdf-processing`, `data-analysis-v2`, `code-review`
**Invalid:** `PDF_Processing` (caps/underscore), `-helper` (start hyphen), `tool--kit` (double hyphen)

**Description Field Rules:**
1. **Length:** 1-1024 characters max.
2. **Format:** Single line string only.
3. **Pattern:** Must start with "(MODAL) USE when..." where MODAL is optional (PROACTIVELY, MUST, SHOULD).

### 4. Template Selection Logic

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

### 5. Frontmatter Generation

**Generate valid YAML with:**
- All required fields populated
- **Description Enforcement:**
  - IF type == 'skill': Ensure string starts with "(MODAL) USE when".
  - IF user input was "Analyze code security":
    - Transform to: "USE when analyzing code security."
  - IF user input was "Help with git":
    - Transform to: "USE when helping with git operations."
- No redundant defaults (e.g., user-invocable: true)
- Proper tool permissions and restrictions

### 6. File Creation

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
