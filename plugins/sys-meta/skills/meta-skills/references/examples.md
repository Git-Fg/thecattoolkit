# Representative Skill Patterns

## Pattern 1: Simple Capability (Single Purpose)

**Use Case:** Single, well-defined capability

```markdown
---
name: pdf-processing
description: "USE when processing PDF files, extracting text, or filling forms."
allowed-tools: [Read, Write, Bash]
---

# PDF Processing Skill

## Core Purpose
Process PDF documents for text extraction and form filling.

## Operational Protocol

1. **Extraction:** Run `scripts/extract.py` on input PDF
2. **Form Filling:** Use template from `assets/form-template.json`
3. **Output:** Write results to specified output path

## Quick Reference

| Task | Command | Output |
|:-----|:--------|:-------|
| Extract text | `scripts/extract.py file.pdf` | `file.txt` |
| Fill form | `scripts/fill.py template.json data.json` | `filled.pdf` |

## When to Load References
- Load `references/advanced.md` for OCR options
- Load `references/troubleshooting.md` for error handling
```

## Pattern 2: Domain Expert (Progressive Disclosure)

**Use Case:** Complex domain requiring detailed theory

**SKILL.md (Router, <400 lines):**
```markdown
---
name: software-architecture
description: "SHOULD USE when designing system architecture or evaluating structural decisions."
---

# Software Architecture Authority

## Core Purpose
Guide system design decisions using established architectural patterns.

## Quick Reference

| Pattern | Use Case | Complexity |
|:--------|:---------|:----------|
| Monolith | Simple apps, fast iteration | Low |
| Layered | Enterprise apps | Medium |
| Microservices | Distributed systems | High |

## Operational Protocol

1. **Assess Requirements:** Load `references/assessment.md`
2. **Select Pattern:** Load `references/patterns.md`
3. **Define Boundaries:** Load `references/boundaries.md`
4. **Validate:** Load `references/validation.md`

## When to Load References
- `references/assessment.md` - When evaluating requirements
- `references/patterns.md` - When comparing architectural patterns
- `references/boundaries.md` - When defining module boundaries
- `references/validation.md` - When validating design decisions
```

**references/patterns.md (Heavy theory):**
```markdown
# Architectural Patterns

## Monolithic Architecture
[200 lines detailed theory]

## Layered Architecture
[200 lines detailed theory]

## Microservices
[200 lines detailed theory]
```

## Pattern 3: Workflow Orchestrator

**Use Case:** Multi-step process with clear phases

```markdown
---
name: release-management
description: "SHOULD USE when orchestrating software releases, version bumps, or deployment workflows."
---

# Release Management Authority

## Core Purpose
Orchestrate complete release workflows with validation and rollback.

## Operational Protocol

### Phase 1: Preparation
1. Version bump (load `references/versioning.md`)
2. Changelog update (load `references/changelog.md`)

### Phase 2: Validation
1. Run tests (load `references/testing.md`)
2. Build artifacts (load `references/build.md`)

### Phase 3: Deployment
1. Deploy to staging
2. Smoke tests (load `references/smoke-tests.md`)
3. Production deployment

### Phase 4: Rollback (if needed)
1. Load `references/rollback.md`
2. Execute rollback procedure

## Quick Reference

| Phase | Key Files | Validation |
|:------|:----------|:-----------|
| Preparation | package.json, CHANGELOG.md | Version format valid |
| Validation | test results, build logs | All tests pass |
| Deployment | deployment logs | Smoke tests pass |
| Rollback | rollback procedure | Previous version restored |

## When to Load References
- `references/versioning.md` - Semantic versioning rules
- `references/changelog.md` - Changelog format standards
- `references/testing.md` - Test requirements and coverage
- `references/build.md` - Build procedures
- `references/smoke-tests.md` - Smoke test definitions
- `references/rollback.md` - Rollback procedures
```

## Pattern 4: Internal Standard (Critical)

**Use Case:** Non-optional internal standards

```markdown
---
name: execution-core
description: "MUST USE when defining behavioral standards for autonomous agents. Universal reference for Uninterrupted Flow, Self-Verification, and Auth-Gates."
allowed-tools: [Read, Write, Edit, Bash, Grep]
---

# Execution Core - Universal Behavioral Standards

## Core Purpose
Define the behavioral contract for all autonomous agents in the system.

## Critical Standards

All agents MUST follow these standards without exception:

1. **Uninterrupted Flow:** No mid-task user questions
2. **Self-Verification:** Verify own work before reporting completion
3. **Auth-Gates:** Handle authentication challenges independently
4. **Handoff Protocol:** Create HANDOFF.md when blocked

## Quick Reference

| Standard | Reference | Criticality |
|:---------|:----------|:-----------|
| Uninterrupted Flow | `references/uninterrupted-flow.md` | MANDATORY |
| Self-Verification | `references/observation-points.md` | MANDATORY |
| Auth-Gates | `references/auth-gates.md` | MANDATORY |
| Handoff Protocol | `references/handoff-protocol.md` | MANDATORY |

## Operational Mandate

When creating or modifying agents:
1. Load all four critical references
2. Apply standards to agent behavior
3. Validate compliance before deployment

## Agent Type Matrix

| Agent Type | Uninterrupted Flow | Self-Verification | Auth-Gates |
|:-----------|:------------------:|:-----------------:|:----------:|
| Worker | ✓ | ✓ | ✓ |
| Background | ✓ | ✓ | ✓ |
| Interactive | ✗ | ✓ | ✓ |

## References (Load All)
- `references/uninterrupted-flow.md` - No-stops execution protocol
- `references/observation-points.md` - Self-verification checklist
- `references/auth-gates.md` - Authentication handling
- `references/handoff-protocol.md` - Blockage and resumption
```
