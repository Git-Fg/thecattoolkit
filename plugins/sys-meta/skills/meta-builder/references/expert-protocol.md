# Expert Protocol for Agent Skills (v2026.1)

## 1. Ground Truth Verification (MANDATORY)

Before proposing or applying any changes to Agent Skills:

1. **Identify Scope:** Determine which component is being modified (Skill, Agent, or integration)
2. **Fetch Official Spec:** Use `WebFetch` or `Bash(curl)` to retrieve current specification from:
   - https://agentskills.io/specification
   - https://agentskills.io/integrate-skills
3. **Check for Drift:** Compare against the official specification from agentskills.io
4. **Validate Resources:** Check skills-ref library at https://github.com/agentskills/agentskills/tree/main/skills-ref

## 2. Agent Skills Standards

**For all Agent Skills operations, follow these standards:**

1. **Parse Intent:** Identify component type (Skill) and action (Create/Validate/Audit/Modify)
2. **Load Knowledge:** Use meta-builder skill to get current Agent Skills specification
3. **Apply Standards:** Follow official specification from agentskills.io
4. **Autonomous Execution:** Propose and apply changes without asking user for clarification
5. **Verify Compliance:** Ensure skills follow the open standard format
6. **Log Completion:** Report updates in structured format

## 3. Skill Creation & Modification Workflow

1. **Parse Requirements:** Identify skill purpose and use cases
2. **Select Framework:** Use Agent Skills open standard (agentskills.io)
3. **Generate Structure:**
   - Create directory matching skill name
   - Generate SKILL.md with proper YAML frontmatter
   - Add optional directories (scripts/, references/, assets/)
4. **Apply Frontmatter:**
   - Valid name field (lowercase, hyphens, 1-64 chars)
   - Descriptive "when to use" text (1-1024 chars)
   - Optional fields as needed
5. **Implement Progressive Disclosure:**
   - Main SKILL.md < 500 lines
   - Reference files in references/
   - Executable scripts in scripts/
   - Templates/resources in assets/
6. **Validate:** Use skills-ref library to verify compliance
7. **Document:** Update any necessary documentation

## 4. Validation Checklist

For every skill created or modified:

- [ ] Directory name matches `name` field in frontmatter
- [ ] Name field: 1-64 chars, lowercase alphanumeric and hyphens only
- [ ] Description: 1-1024 chars, includes "when to use" guidance
- [ ] Progressive disclosure: SKILL.md < 500 lines
- [ ] Optional directories properly structured
- [ ] File references use relative paths (one level deep)
- [ ] Scripts self-contained or clearly documented
- [ ] Validated against official specification

## 5. Audit & Healing Workflow

1. **Scan Existing Skills:** Execute audit of skill directories
2. **Detect Discrepancies:** Compare against agentskills.io specification
3. **Recommend Fixes:** Follow systematic protocol from official docs
4. **Apply Corrections:** Update skills to comply with open standard
5. **Validate Results:** Use skills-ref library for verification
6. **Log Changes:** Document all infrastructure updates

## 6. Open Standard Compliance

Agent Skills is an **open standard** developed by Anthropic and adopted by leading AI development tools.

**Key Principles:**
- Open development (contributions welcome)
- Cross-platform compatibility
- Progressive disclosure for context efficiency
- Self-documenting format
- Portable and version-controllable

**Official Repository:** https://github.com/agentskills/agentskills
