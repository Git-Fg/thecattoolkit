# Quality & Validation Standards

## 1. The "State-in-Files" Law
Because Agents are ephemeral and async, **state must be persisted to disk immediately**.
*   **Anti-Pattern:** Keeping the plan in the chat context.
*   **Standard:** Update `PLAN.md` or `STATUS.md` after every atomic step.

## 2. Self-Correction Protocol
When an Agent generates an output (e.g., a new Skill), it must perform a **Verification Loop** before finishing:
1.  **Read:** Does the file exist?
2.  **Lint:** Does the YAML frontmatter parse?
3.  **Check:** Does it reference non-existent files?

## 3. Error Handling
*   **Vector (Interactive):** Report error to user, ask for guidance.
*   **Triangle (Async):** Log error to `ERROR_LOG.md`, attempt one retry with different strategy, then exit. Do not hang waiting for input.

## Audit Standards

### Overview

Audits serve multiple purposes:
- Quality assurance validation
- Issue identification and remediation
- Learning and pattern recognition
- Pre-modification baseline assessment

### Pre-Audit Requirements

**Criteria Hydration (MANDATORY):**

Before listing skills, audit criteria must be hydrated:

**Step 1: Read System Standards**
Read `references/standards-architecture.md` completely to absorb:
- Skills Audit Checklist (Frontmatter, Structure, Content, Resources)
- Component-Specific Checklists (Agents, Hooks, Commands)
- Slash Commands Integration Audit

**Step 2: Understand Audit Purpose**
- Quality assurance validation
- Issue identification and remediation
- Learning and pattern recognition
- Pre-modification baseline assessment

**Step 3: Identify Skill Context**
- Skill type (simple, router, domain expertise)
- Application scenario and usage context
- Dependencies (tools, permissions, MCP servers, slash commands)

### Systematic Review Process

**For each skill component, apply the corresponding checklist:**

#### 1. YAML Frontmatter Audit

Check `references/standards-architecture.md` for frontmatter requirements:
- [ ] `name` field present and valid (lowercase-with-hyphens, max 64 chars)
- [ ] `description` field present and valid (max 1024 chars, third person)
- [ ] `allowed-tools` field (if present) properly formatted
- [ ] No extraneous fields

#### 2. Structure Audit

Apply structure checklist from `references/standards-architecture.md`:
- [ ] Proper markdown heading hierarchy (# ## ###)
- [ ] Clear navigation with descriptive headings
- [ ] Progressive disclosure (SKILL.md < 500 lines recommended)
- [ ] Required sections present (objective, quick start, success criteria)

#### 3. Description Quality Audit

- [ ] Third person: "Use this skill when..." not "I will help..."
- [ ] Specific triggers: Concrete phrases that invoke the skill
- [ ] No vague terms: Avoid "helps with", "processes data"
- [ ] Strong language: MUST USE / PROACTIVELY / CONSULT

#### 4. Content Quality Audit

- [ ] Instructions are clear and actionable
- [ ] Success criteria are measurable
- [ ] No unnecessary complexity
- [ ] Appropriate level of detail

#### 5. Resource Audit

- [ ] All referenced files exist
- [ ] Relative paths used correctly (no `../` to exit skill directory)
- [ ] Templates are in `assets/templates/`
- [ ] References are in `references/`
- [ ] Scripts (if any) are in `scripts/`

### Contextual Judgment Standards

#### Simple Skills (<100 lines)

**Relaxed standards apply:**
- Minimal requirements OK
- Don't flag missing optional sections
- Focus on clarity and core functionality

#### Complex Skills

**Strict standards apply:**
- Missing conditional sections is critical
- Comprehensive coverage expected
- All validation checkpoints required

#### Delegation Skills

**Specialized standards:**
- Success criteria can focus on invocation success
- Clear delegation paths required
- Tool permissions properly configured

### Common Anti-Patterns

| Pattern | Why It Matters | Fix |
|---------|---------------|-----|
| Missing objective | Unclear purpose | Add objective section |
| Wrong POV | Inconsistent | Use third person |
| Vague triggers | Won't invoke | Add specific trigger keywords |
| Bloat (>500 lines) | Hard to scan | Move details to references/ |
| No success criteria | Can't verify completion | Add clear success criteria |
| Deep references | Hard to maintain | Flatten to one level |
| Generic role | No specialization | Specify domain and expertise |
| Missing constraints | Can go out of scope | Add MUST/NEVER boundaries |

### Remediation Standards

#### Issue Prioritization

**Priority 1 (Critical):**
- Broken YAML frontmatter
- Missing required fields
- Invalid file structure
- Security vulnerabilities

**Priority 2 (High):**
- Vague descriptions
- Missing success criteria
- Incorrect path references
- Poor progressive disclosure

**Priority 3 (Medium):**
- Style inconsistencies
- Minor structural issues
- Missing optional enhancements

**Priority 4 (Low):**
- Cosmetic improvements
- Nice-to-have features
- Documentation enhancements

#### Remediation Verification

After applying fixes, re-run the audit checklist to verify:
- [ ] All critical issues resolved
- [ ] No new issues introduced
- [ ] Skill functionality preserved
- [ ] Standards compliance improved

## Modification Standards

### Pre-Modification Analysis

#### Context Hydration Requirements

Before applying modifications, hydrate understanding of current state:

**1. Locate Target Skill**
```bash
# Find the skill
cat {path-to-skill}/SKILL.md

# Check directory structure
ls -la {path-to-skill}/
ls -la {path-to-skill}/workflows/ 2>/dev/null || true
ls -la {path-to-skill}/references/ 2>/dev/null || true
ls -la {path-to-skill}/templates/ 2>/dev/null || true
ls -la {path-to-skill}/scripts/ 2>/dev/null || true
```

**2. Analyze Skill Type**
Identify which template pattern the skill follows:
- Simple (single SKILL.md)
- Router pattern (SKILL.md + workflows/ + references/)
- Domain expertise (exhaustive lifecycle coverage)

**3. Understand Skill Context**
- Purpose and application scenario
- User context and usage patterns
- Dependencies (tools, permissions, MCP servers)
- Related components (slash commands, other skills)

**4. Identify Modification Scope**
- Structure changes (pattern conversion)
- Content updates (objective, process, criteria)
- Workflow enhancements (additions, modifications)
- Reference updates (additions, modifications)
- Template/script modifications
- YAML frontmatter updates

### Modification Categories

#### Structure Changes

**Pattern Conversion:**

| From | To | Complexity |
|------|-----|------------|
| Simple | Router | Medium - requires extraction and routing |
| Router | Simple | Low - requires consolidation |
| Any | Domain Expertise | High - requires lifecycle expansion |

#### Content Updates

**Objective Modifications:**
- Clarify purpose
- Update scope
- Refine language
- Fix inaccuracies

**Process Updates:**
- Add/remove steps
- Clarify instructions
- Fix errors
- Improve flow

**Success Criteria Updates:**
- Add measurable outcomes
- Remove unmeasurable criteria
- Clarify completion conditions
- Fix validation logic

### Modification Safety Standards

#### Backup Protocol

Before any modification:
```bash
# Create backup
cp -r {skill-name} {skill-name}.backup.$(date +%Y%m%d_%H%M%S)
```

#### Incremental Changes

**Apply changes incrementally:**
1. Make one type of change at a time
2. Verify each change before proceeding
3. Test after each modification
4. Commit working states

#### Validation Gates

**After each modification, verify:**
- [ ] YAML frontmatter valid
- [ ] All file references exist
- [ ] No broken links or paths
- [ ] Skill loads without errors
- [ ] Functionality preserved
- [ ] Standards compliance maintained

### Pattern Migration Standards

#### Converting Simple to Router

**When:** Skill grows beyond 200 lines or needs multiple distinct workflows

**Process:**

1. **Identify Components:**
   - Essential principles (apply to all use cases)
   - Distinct workflows (different user intents)
   - Reusable knowledge (patterns, examples)

2. **Create Structure:**
   ```bash
   mkdir -p {skill-name}/workflows
   mkdir -p {skill-name}/references
   ```

3. **Extract Content:**
   - Move universal principles to SKILL.md
   - Create workflow files for distinct use cases
   - Move detailed content to references/

4. **Add Routing:**
   - Define intent-based routing logic
   - Map user intents to workflows
   - Update skill description

### Verification Standards

#### Post-Modification Testing

**After any modification:**

1. **Load Test:**
   - Verify skill loads without errors
   - Check YAML frontmatter validity
   - Ensure all file references resolve

2. **Functionality Test:**
   - Test primary use cases
   - Verify workflows execute correctly
   - Check outputs match expectations

3. **Integration Test:**
   - Test with dependent agents
   - Test with invoking commands
   - Verify compatibility

4. **Standards Compliance:**
   - Run audit checklist
   - Verify architectural compliance
   - Check best practices adherence

#### Rollback Protocol

**If modification introduces issues:**

1. Identify the failure point
2. Assess rollback vs. fix
3. If critical: Restore from backup
4. If minor: Apply targeted fix
5. Re-test thoroughly
