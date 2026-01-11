# Prompt Quality & Audit Criteria

The standards used to evaluate prompt artifacts for production readiness.

## Core Quality Pillars

### 1. Structure Compliance
- **Single Prompts**: Must be Pure Markdown (0 XML tags).
- **Chains/Meta-Prompts**: Hybrid XML (1-15 tags maximum).
- **Flat Tags**: No nested XML tags allowed.
- **Hierarchy**: Uses clear Markdown headings and lists.

### 2. Instructability
- **Actionable**: Steps are concrete and unambiguous.
- **Specific**: No vague commands like "be helpful" or "analyze".
- **Complete**: All necessary context for the task is included or requested.
- **Sequential**: Logical flow for multi-step instructions.

### 3. Output Control
- **Format**: Output format (JSON, Markdown, etc.) is explicitly defined.
- **Structure**: Clear schemas or templates for complex outputs.
- **Constraints**: Critical negative constraints (NEVER/MUST NOT) are highlighted.

### 4. Safety & Security
- **Isolation**: Few-shot examples are wrapped in `<example>` tags.
- **Data Protection**: No hardcoded credentials or sensitive data instructions.
- **Boundaries**: Clear scope on what the AI should and should NOT do.

## Audit Scoring Matrix

| Quality | Description | Ready? |
|:---|:---|:---:|
| **Production** | Meets all criteria, tested on edge cases, concise. | ✅ |
| **Needs Work** | Good content but minor structural or clarity issues. | ⚠️ |
| **Failing** | Nested XML, vague tasks, or missing output format. | ❌ |

## The "AI Soup" Anti-Checklist
- [ ] Is there any nested XML? (If yes, fix to flat).
- [ ] Is there a tag soup (>5 tags)? (If yes, consolidate).
- [ ] Is there instruction leakage? (Check if examples are isolated).
- [ ] Is it too verbose? (Prune low-value tokens).
- [ ] Is the role duplicated from a parent agent? (Keep it lean).

## Verification Strategy
1. **Manual Review**: Check against the pillars above.
2. **Execution Test**: Run with `run-prompt` on 3-5 diverse inputs.
3. **Audit Prompt**: Use the Prompt Auditor meta-prompt for an AI-driven critique.

---

## Approval Gate Workflows

For complex prompts and workflows, implement structured approval gates to ensure quality and user alignment.

### Gate 1: Requirements Validation (Pre-Design)

**When to Apply:** Complex prompts with multiple phases or architectural decisions

**Approval Required From:** User or Stakeholder

**Checklist:**
- [ ] User has explicitly stated the goal/objective
- [ ] Success criteria are defined and measurable
- [ ] Edge cases and constraints are documented
- [ ] Risk level has been assessed (Low/Medium/High/Critical)
- [ ] Scope boundaries are clear (what's in/out)

**Output:** Requirements document with explicit user sign-off

---

### Gate 2: Architecture Selection (Pre-Implementation)

**When to Apply:** Prompts requiring design decisions or multiple approaches

**Approval Required From:** User

**Checklist:**
- [ ] Multiple approaches have been presented
- [ ] Trade-offs are clearly explained
- [ ] User has selected preferred approach
- [ ] Implementation plan is aligned with selected architecture
- [ ] All questions from requirements phase are answered

**Output:** Architecture decision document with user signature

**Presentation Format:**
```markdown
### Architecture Options

| Approach | Pros | Cons | Estimated Complexity |
|----------|------|------|---------------------|
| A: Minimal | Fast to implement | Limited flexibility | Low |
| B: Clean | Maintainable, scalable | More complex | Medium-High |
| C: Pragmatic | Balanced trade-offs | Compromise on purity | Medium |

**Recommendation:** [Approach] because [reasoning]

Which approach do you prefer?
```

---

### Gate 3: Quality Review (Pre-Deployment)

**When to Apply:** Production-ready prompts and workflows

**Approval Required From:** User (with automated checks)

**Automated Checks:**
- [ ] All quality pillars are satisfied
- [ ] No nested XML tags present
- [ ] XML tag count ≤ 15
- [ ] Examples are properly isolated
- [ ] Output format is clearly specified

**Human Review:**
- [ ] **Critical Issues:** Must be fixed before deployment
- [ ] **Recommended Issues:** Should be addressed for optimal quality
- [ ] **Optional Issues:** Nice-to-have improvements

**Output:**
```markdown
### Review Findings

**Critical (must fix):**
- [Issue]: [Location] — [Reason]

**Recommended (should fix):**
- [Issue]: [Location] — [Reason]

**Optional (nice to have):**
- [Issue]: [Location] — [Reason]

How would you like to proceed?
- A) Fix all issues
- B) Fix critical + recommended only
- C) Fix critical only
- D) Deploy as-is
```

---

### Gate 4: Final Sign-Off (Pre-Production)

**When to Apply:** Critical production systems

**Approval Required From:** User and Technical Reviewer

**Checklist:**
- [ ] All critical issues are resolved
- [ ] Testing has been completed
- [ ] Documentation is up-to-date
- [ ] Rollback plan is defined (if applicable)
- [ ] User explicitly approves production deployment

**Output:** Deployment approval document

---

## Approval Gate Templates

### Template 1: Requirements Validation
```markdown
## Requirements Review

**Objective:** {Clear statement of prompt goal}

**Success Criteria:**
1. {Measurable criterion 1}
2. {Measurable criterion 2}
3. {Measurable criterion 3}

**Constraints:**
- {Constraint 1}
- {Constraint 2}

**Risk Assessment:** {Low/Medium/High/Critical}

**Approved by:** _________________ **Date:** _________
```

### Template 2: Architecture Selection
```markdown
## Architecture Decision

**Selected Approach:** {A/B/C}

**Rationale:**
{User's reasoning for selection}

**Implementation Plan:**
{Brief description of how the selected approach will be implemented}

**Approved by:** _________________ **Date:** _________
```

### Template 3: Quality Review
```markdown
## Quality Review Report

**Prompt:** {Name}

**Automated Checks:** ✅ All passed

**Critical Issues:** {Count}
**Recommended Issues:** {Count}
**Optional Issues:** {Count}

**Decision:** {A/B/C/D from review options}

**Approved by:** _________________ **Date:** _________
```

---

## Escalation Path

| Severity | Action Required | Who |
|:---------|:----------------|:----|
| **Critical** | Immediate fix before proceeding | User + Technical Review |
| **Recommended** | Address within current session | User |
| **Optional** | Future enhancement | Deferred |
| **Structural** | Architecture redesign | User + Technical Review |

---

## Quality Gate Decision Matrix

| Prompt Type | Gate 1 | Gate 2 | Gate 3 | Gate 4 |
|:------------|:------:|:------:|:------:|:------:|
| **Single Prompt** | Optional | Never | Always | Never |
| **Chain Prompt** | Required | Sometimes | Always | High-Risk Only |
| **Complex Command** | Always | Always | Always | High-Risk Only |
| **Meta-Prompt** | Always | Sometimes | Always | Always |

**Legend:**
- **Always:** Mandatory approval gate
- **Sometimes:** Apply based on complexity/requirements
- **Never:** Not applicable
- **High-Risk Only:** Apply when risk level is Critical
