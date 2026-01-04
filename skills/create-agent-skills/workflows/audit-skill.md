# Workflow: Audit a Skill

## Required Reading
**Read these reference files NOW:**
1. references/skill-structure.md
2. references/core-principles.md

## Process

## Evaluation Areas

### YAML Frontmatter
- **name**: Lowercase-with-hyphens, max 64 chars, matches directory name, follows verb-noun convention (create-*, manage-*, setup-*, generate-*)
- **description**: Max 1024 chars, third person, includes BOTH what it does AND when to use it, no XML tags, uses strong language (MUST USE/PROACTIVELY USE/CONSULT based on skill type)
- **Strong language patterns**:
  - "MUST USE" for creation/critical skills (create-*, debug-like-expert, prompt-engineering-patterns)
  - "PROACTIVELY USE" for proactive usage skills (project-analysis, testing-strategy, performance-optimization, prioritization, problem-analysis, strategic-thinking, git-workflow)
  - "CONSULT" for reference/expert guidance skills (api-design, architecture-patterns)

### Structure and Organization
- **Progressive disclosure**: SKILL.md is overview (<500 lines), detailed content in reference files, references one level deep
- **Structure quality**:
  - Required sections present (objective, quick_start, success_criteria)
  - Markdown headings for structure (#, ##, ###)
  - Proper heading hierarchy and organization
  - Conditional sections appropriate for complexity level
  - XML reserved only for highly structured elements (routing, complex workflows)
- **File naming**: Descriptive, forward slashes, organized by domain

### Content Quality
- **Conciseness**: Only context Claude doesn't have. Apply critical test: "Does removing this reduce effectiveness?"
- **Clarity**: Direct, specific instructions without analogies or motivational prose
- **Specificity**: Matches degrees of freedom to task fragility
- **Examples**: Concrete, minimal, directly applicable

### Anti-Patterns (flag these issues)
- **missing_required_sections**: Missing objective, quick_start, or success_criteria
- **improper_heading_hierarchy**: Skipped heading levels, unclear organization
- **mixed_formatting**: Inconsistent use of markdown and XML
- **vague_descriptions**: "helps with", "processes data"
- **wrong_pov**: First/second person instead of third person
- **too_many_options**: Multiple options without clear default
- **deeply_nested_references**: References more than one level deep from SKILL.md
- **windows_paths**: Backslash paths instead of forward slashes
- **bloat**: Obvious explanations, redundant content

### Contextual Judgment

Apply judgment based on skill complexity and purpose:

**Simple skills** (single task, <100 lines):
- Required tags only is appropriate - don't flag missing conditional tags
- Minimal examples acceptable
- Light validation sufficient

**Complex skills** (multi-step, external APIs, security concerns):
- Missing conditional tags (security_checklist, validation, error_handling) is a real issue
- Comprehensive examples expected
- Thorough validation required

**Delegation skills** (invoke subagents):
- Success criteria can focus on invocation success
- Pre-validation may be redundant if subagent validates

Always explain WHY something matters for this specific skill, not just that it violates a rule.

### Output Format

Audit reports use severity-based findings, not scores:

```markdown
## Audit Results: [skill-name]

### Assessment
[1-2 sentence overall assessment: Is this skill fit for purpose? What's the main takeaway?]

### Critical Issues
Issues that hurt effectiveness or violate required patterns:

1. [Issue category] (file:line)
   - Current: [What exists now]
   - Should be: [What it should be]
   - Why it matters: [Specific impact on this skill's effectiveness]
   - Fix: [Specific action to take]

2. ...

(If none: "No critical issues found.")

### Recommendations
Improvements that would make this skill better:

1. [Issue category] (file:line)
   - Current: [What exists now]
   - Recommendation: [What to change]
   - Benefit: [How this improves the skill]

2. ...

(If none: "No recommendations - skill follows best practices well.")

### Strengths
What's working well (keep these):
- [Specific strength with location]
- ...

### Quick Fixes
Minor issues easily resolved:
1. [Issue] at file:line → [One-line fix]
2. ...

### Context
- Skill type: [simple/complex/delegation/etc.]
- Line count: [number]
- Estimated effort to address issues: [low/medium/high]
```

## Process
## Step 1: List Available Skills

**DO NOT use AskUserQuestion** - there may be many skills.

Enumerate skills in chat as numbered list:
```bash
ls ~/.claude/skills/
```

Present as:
```
Available skills:
1. create-agent-skills
2. build-macos-apps
3. manage-stripe
...
```

Ask: "Which skill would you like to audit? (enter number or name)"

## Step 2: Read the Skill

After user selects, read the full skill structure:
```bash
# Read main file
cat ~/.claude/skills/{skill-name}/SKILL.md

# Check for workflows and references
ls ~/.claude/skills/{skill-name}/
ls ~/.claude/skills/{skill-name}/workflows/ 2>/dev/null
ls ~/.claude/skills/{skill-name}/references/ 2>/dev/null
```

## Step 3: Run Audit Checklist

Evaluate against each criterion:

### YAML Frontmatter
- [ ] Has `name:` field (lowercase-with-hyphens)
- [ ] Name matches directory name
- [ ] Has `description:` field
- [ ] Description says what it does AND when to use it
- [ ] Description is third person with strong language (MUST USE/PROACTIVELY USE/CONSULT)

### Structure
- [ ] SKILL.md under 500 lines
- [ ] Pure XML structure (no markdown headings # in body)
- [ ] All XML tags properly closed
- [ ] Has required tags: objective OR essential_principles
- [ ] Has success_criteria

### Router Pattern (if complex skill)
- [ ] Essential principles inline in SKILL.md (not in separate file)
- [ ] Has intake question
- [ ] Has routing table
- [ ] All referenced workflow files exist
- [ ] All referenced reference files exist

### Workflows (if present)
- [ ] Each has required_reading section
- [ ] Each has process section
- [ ] Each has success_criteria section
- [ ] Required reading references exist

### Content Quality
- [ ] Principles are actionable (not vague platitudes)
- [ ] Steps are specific (not "do the thing")
- [ ] Success criteria are verifiable
- [ ] No redundant content across files

## Step 4: Generate Report

Present findings as:

```
## Audit Report: {skill-name}

### ✅ Passing
- [list passing items]

### ⚠️ Issues Found
1. **[Issue name]**: [Description]
   → Fix: [Specific action]

2. **[Issue name]**: [Description]
   → Fix: [Specific action]

### 📊 Score: X/Y criteria passing
```

## Step 5: Offer Fixes

If issues found, ask:
"Would you like me to fix these issues?"

Options:
1. **Fix all** - Apply all recommended fixes
2. **Fix one by one** - Review each fix before applying
3. **Just the report** - No changes needed

If fixing:
- Make each change
- Verify file validity after each change
- Report what was fixed

## Audit Anti Patterns
## Common Anti-Patterns to Flag

**Skippable principles**: Essential principles in separate file instead of inline
**Monolithic skill**: Single file over 500 lines
**Mixed concerns**: Procedures and knowledge in same file
**Vague steps**: "Handle the error appropriately"
**Untestable criteria**: "User is satisfied"
**Markdown headings in body**: Using # instead of XML tags
**Missing routing**: Complex skill without intake/routing
**Broken references**: Files mentioned but don't exist
**Redundant content**: Same information in multiple places

## Success Criteria
Audit is complete when:
- [ ] Skill fully read and analyzed
- [ ] All checklist items evaluated
- [ ] Report presented to user
- [ ] Fixes applied (if requested)
- [ ] User has clear picture of skill health
