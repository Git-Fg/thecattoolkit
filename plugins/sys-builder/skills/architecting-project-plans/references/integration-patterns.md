# Integration Patterns

## Overview

How `architecting-project-plans` integrates with `managing-project-plans` to create comprehensive, standards-compliant plans.

## Integration Model

```
architecting-project-plans (Active Intelligence)
           ↓
    Uses standards from
           ↓
managing-project-plans (Passive Library)
           ↓
    Applies templates from
           ↓
    Creates plan files in
           ↓
   .cattoolkit/plan/{project-slug}/
```

## Pattern 1: Standard Template Application

### Using Managing-Project-Plans Templates

**Process:**

1. **Select Template**
   ```python
   # From architecting-project-plans
   Template needed: BRIEF.md
   ↓
   Source: managing-project-plans/assets/templates/brief.md
   ```

2. **Fill Template**
   ```markdown
   # Project: {project-name}

   ## Objective
   {synthesized from user requirements}

   ## Success Criteria
   {derived from discovery + requirements}

   ## Constraints
   {identified from analysis}
   ```

3. **Validate Against Standards**
   ```markdown
   Validation checklist:
   - [ ] BRIEF.md exists
   - [ ] All sections present
   - [ ] Success criteria measurable
   - [ ] Constraints documented
   ```

### Example: Creating BRIEF.md

```markdown
# Step-by-Step Integration

1. Discovery Protocol Run
   ↓
2. Requirements Synthesized
   ↓
3. Template Loaded from managing-project-plans
   ↓
4. Content Filled
   ↓
5. Validated Against Schema
   ↓
6. BRIEF.md Created in .cattoolkit/plan/{project-slug}/

Result: Standards-compliant BRIEF.md
```

## Pattern 2: Schema-Compliant Plan Creation

### ROADMAP.md Generation

**Input to architecting-project-plans:**
- Synthesized requirements
- Phase structure
- Dependencies

**Output using managing-project-plans:**
```markdown
# Roadmap: {project-name}

## Phases

| Phase | Name | Status | Dependencies | Summary |
|-------|------|--------|--------------|---------|
| 01 | Foundation | [ ] | none | Setup and structure |
| 02 | Core Features | [ ] | 01 | Main functionality |
| 03 | Enhancement | [ ] | 02 | Advanced features |
```

**Schema Compliance:**
- ✓ Table format matches standard
- ✓ Status codes are valid: `[ ]`, `[~]`, `[x]`, `[!]`
- ✓ Dependencies explicit
- ✓ Phase summaries present

### Phase Plan Creation

**Using Phase Plan Template:**

```markdown
# Phase 01: Foundation

## Overview
**Objective:** Setup project structure and dependencies
**Deliverable:** Working development environment
**Success Criteria:** All tests pass, dev server runs

## Tasks

### Task 1: Setup project structure
**Scope:** Root directory, basic folders
**Action:** Create directory structure
**Verify:** Structure matches standards
**Done:** Project compiles without errors

### Task 2: Install dependencies
**Scope:** package.json, lock file
**Action:** Install all required packages
**Verify:** All packages installed
**Done:** No missing dependencies

## Handoff Protocol
{Standard handoff template from managing-project-plans}
```

## Pattern 3: Validation Rule Application

### File Structure Validation

**Rules from managing-project-plans:**

```markdown
Validation Rules:
1. File Naming
   - BRIEF.md: Must exist at project root ✓
   - ROADMAP.md: Must exist at project root ✓
   - Phase files: Must be in phases/ directory ✓
   - Phase directories: Must be XX-name format ✓

2. Status Codes
   - Only [ ], [~], [x], [!] are valid ✓
   - No other symbols ✓

3. Dependencies
   - Phase N depends on Phase N-1 ✓
   - No circular dependencies ✓
   - Explicit in ROADMAP.md ✓
```

**Implementation in architecting-project-plans:**

```python
def validate_plan_structure(plan_dir):
    """Apply managing-project-plans validation rules"""

    # Rule 1: File naming
    assert os.path.exists(f"{plan_dir}/BRIEF.md")
    assert os.path.exists(f"{plan_dir}/ROADMAP.md")

    # Rule 2: Status codes
    roadmap = read_file(f"{plan_dir}/ROADMAP.md")
    valid_codes = ['[ ]', '[~]', '[x]', '[!]']
    for line in roadmap:
        if line.startswith('|') and 'Phase' not in line:
            assert any(code in line for code in valid_codes)

    # Rule 3: Dependencies
    validate_dependencies(roadmap)

    return True
```

## Pattern 4: Template Composition

### Combining Multiple Templates

**Complex Plan Structure:**

```
Plan Creation Flow:

1. Create BRIEF.md
   ↓
2. Create ROADMAP.md
   ↓
3. For each phase:
   a. Create phase directory
   b. Create 01-01-PLAN.md (phase plan template)
   c. Add tasks
   ↓
4. Validate entire structure
```

**Example: Full Plan Creation**

```markdown
# Phase 1: Setup
Using: managing-project-plans/templates/phase-plan.md

# Phase 2: Implementation
Using: managing-project-plans/templates/phase-plan.md

# Phase 3: Testing
Using: managing-project-plans/templates/phase-plan.md

All phases reference:
- BRIEF.md (from brief.md template)
- ROADMAP.md (from roadmap.md template)
- HANDOFF.md (from handoff.md template if needed)
```

## Pattern 5: Standards Inheritance

### Passive Library Pattern

**How managing-project-plans Works:**

```markdown
managing-project-plans is PASSIVE:
- Provides templates ✓
- Defines schemas ✓
- Sets validation rules ✓
- NO orchestration logic ✗

architecting-project-plans is ACTIVE:
- Loads templates ✓
- Fills schemas ✓
- Applies validation ✓
- Creates orchestration logic ✓
```

**Integration Contract:**

```markdown
managing-project-plans provides:
- Templates (in assets/templates/)
- Schemas (in SKILL.md)
- Validation rules (in SKILL.md)

architecting-project-plans consumes:
- Templates → Fills with content
- Schemas → Validates structure
- Rules → Ensures compliance

Result: Standards-compliant plans created by active intelligence
```

## Pattern 6: Progressive Refinement

### Iterative Plan Enhancement

**Iteration 1: Basic Structure**
```markdown
✓ BRIEF.md created (brief.md template)
✓ ROADMAP.md created (roadmap.md template)
✓ Phase 1 created (phase-plan.md template)

Status: Basic structure valid
```

**Iteration 2: Task Detail**
```markdown
↑ Previous structure
+ Task details filled
+ Verification criteria added
+ Success metrics defined

Status: Detailed tasks present
```

**Iteration 3: Dependencies**
```markdown
↑ Previous structure
+ Dependencies mapped
+ Critical path identified
+ Risk mitigation added

Status: Fully analyzed
```

**Iteration 4: Validation**
```markdown
↑ Previous structure
+ All validation rules applied
+ Schema compliance verified
+ Structure validated

Status: Production-ready plan
```

## Pattern 7: Multi-Algorithm Synthesis

### Applying Different Algorithms

**Greenfield Path:**
```markdown
Algorithm: Greenfield Planning
↓
Templates: brief.md, roadmap.md, phase-plan.md
↓
Output: New project structure
```

**Brownfield Path:**
```markdown
Algorithm: Brownfield Integration
↓
Templates: brief.md (with current state), roadmap.md, phase-plan.md
↓
Output: Migration + enhancement plan
```

**Feature Addition Path:**
```markdown
Algorithm: Feature Addition
↓
Templates: brief.md (focused scope), roadmap.md (incremental), phase-plan.md
↓
Output: Feature-specific plan
```

**Refactoring Path:**
```markdown
Algorithm: Refactoring
↓
Templates: brief.md (problem statement), roadmap.md (migration phases), phase-plan.md
↓
Output: Refactoring plan
```

## Quick Reference

### Integration Checklist

**Before Creating Plan:**
- [ ] Load templates from managing-project-plans
- [ ] Review schema definitions
- [ ] Understand validation rules

**During Creation:**
- [ ] Apply correct template
- [ ] Fill required sections
- [ ] Use valid status codes
- [ ] Define explicit dependencies

**After Creation:**
- [ ] Validate structure
- [ ] Check schema compliance
- [ ] Verify all sections present
- [ ] Ensure dependencies clear

### Template Selection Guide

```markdown
Need BRIEF.md?
→ Use managing-project-plans/assets/templates/brief.md

Need ROADMAP.md?
→ Use managing-project-plans/assets/templates/roadmap.md

Need phase plan?
→ Use managing-project-plans/assets/templates/phase-plan.md

Need to pause execution?
→ Use managing-project-plans/assets/templates/handoff.md

Need to summarize phase?
→ Use managing-project-plans/assets/templates/summary.md
```

### Common Patterns

```markdown
Pattern: Simple Project
Templates: brief.md + roadmap.md + phase-plan.md

Pattern: Complex Project
Templates: All templates + Manus 3-file pattern

Pattern: Feature Addition
Templates: brief.md (scoped) + roadmap.md (incremental) + phase-plan.md

Pattern: Refactoring
Templates: brief.md (problem) + roadmap.md (migration) + phase-plan.md
```

## Error Prevention

### Common Mistakes

❌ **Creating custom templates**
→ Use managing-project-plans templates

❌ **Inconsistent naming**
→ Follow XX-name format

❌ **Invalid status codes**
→ Use only [ ], [~], [x], [!]

❌ **Circular dependencies**
→ Validate with managing-project-plans rules

❌ **Missing validation**
→ Apply all validation rules

### Best Practices

✓ Always load templates from managing-project-plans
✓ Follow schema definitions exactly
✓ Apply validation rules systematically
✓ Use status codes consistently
✓ Make dependencies explicit
✓ Keep task atomic
✓ Document handoffs when blocked
