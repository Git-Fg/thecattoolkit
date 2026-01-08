---
name: project-lifecycle
description: |
  Project planning standards, templates, execution protocols, verification standards, and handoff procedures for BRIEF.md, ROADMAP.md, PLAN.md, ADR, phase execution, verification points, and authentication gates.
  <example>
  Context: User wants to create a project plan
  user: "Create a project plan for our new feature"
  assistant: "I'll load the project-lifecycle skill to create BRIEF.md and ROADMAP.md."
  </example>
  <example>
  Context: User needs to execute a phase
  user: "Execute phase 1 of our plan"
  assistant: "I'll use the project-lifecycle skill to understand phase execution standards."
  </example>
  <example>
  Context: Handling authentication gates
  user: "The deployment failed with auth error"
  assistant: "I'll load the project-lifecycle skill to handle the authentication gate properly."
  </example>
allowed-tools: Bash Edit Read Write Glob Grep
---

# Project Lifecycle Standards

## Skill Contents

**Templates and Resources:**
- Document templates in `assets/templates/`
- Format standards in `references/`
- Protocol guidelines for planning and execution

**Reference Resources:**
- `assets/templates/` - Document templates for all project lifecycle phases
- `references/plan-format.md` - PLAN.md structure guidelines
- `references/phase-patterns.md` - Phase breakdown patterns
- `references/scope-estimation.md` - Task complexity estimation
- `references/context-management.md` - Context management practices
- `references/execution-observation-points.md` - Verification point standards
- `references/authentication-gates.md` - Authentication error handling
- `references/git-integration.md` - Git integration standards
- `references/` - All planning and execution protocol standards

## Document Templates

### Quick Reference

| Document Type | Template Location | Use Case |
|---------------|-------------------|----------|
| Project Brief | `assets/templates/brief.md` | Project starts |
| Roadmap | `assets/templates/roadmap.md` | Multi-phase projects |
| Phase Plan | `assets/templates/phase-plan.md` | Executable phases |
| ADR Entry | `assets/templates/adr-entry.md` | Architecture decisions |
| Issue Entry | `assets/templates/issue-entry.md` | Deferred enhancements |
| Issues File | `assets/templates/issues.md` | ISSUES.md creation |
| Phase Summary | `assets/templates/summary.md` | Phase completions |
| Session Handoff | `assets/templates/handoff.md` | Session pauses mid-phase |

### Location Standards

**Project Documents:** `.cattoolkit/planning/{project-slug}/`
- BRIEF.md - Template: `assets/templates/brief.md`
- ROADMAP.md - Template: `assets/templates/roadmap.md`
- ADR.md - Template: `assets/templates/adr-entry.md`
- ISSUES.md - Template: `assets/templates/issues.md`

**Phase Documents:** `.cattoolkit/planning/{project-slug}/phases/XX-name/`
- PLAN.md - Template: `assets/templates/phase-plan.md`
- SUMMARY.md - Template: `assets/templates/summary.md`
- HANDOFF.md - Template: `assets/templates/handoff.md`

## YAML Frontmatter Standards

**Standard Format for Documents:**

**BRIEF.md:**
```yaml
---
project: [Project Name]
version: 1.0
status: in_progress
---
```

**ROADMAP.md:**
```yaml
---
project: [Project Name]
version: 1.0
status: in_progress
---
```

**PLAN.md:**
```yaml
---
phase: XX-name
type: execute
domain: [optional]
status: in_progress
---
```

**Valid Status Values:** `in_progress`, `completed`

## PLAN.md Structure Standards

**Structure Reference:** See `references/plan-format.md` for detailed PLAN.md structure guidelines.

**Standard Sections:**
- Objective (purpose, output)
- Context (@references to required files)
- Tasks (specific, verifiable, with Done criteria)
- Checkpoints (human verification, decisions, actions)
- Success Criteria (measurable outcomes)

## Protocol Standards

### Planning Standards

**Git Integration Standards**

**Reference:** See `references/git-integration.md` for git integration guidelines.

**Standard Commit Points:**
- Project initialization (BRIEF + ROADMAP together)
- Phase completion (code shipped)
- Handoff (WIP state)

**Standard Commit Format:**
```
feat(domain): [one-liner from SUMMARY.md]

- [Key accomplishment 1]
- [Key accomplishment 2]
- [Key accomplishment 3]
```

**Commit Pattern:** Separate commits for PLAN.md creation, RESEARCH.md, FINDINGS.md, or minor planning tweaks are not part of the standard workflow.

### Self-Verification Standards

**Reference:** See `references/execution-observation-points.md` for verification point guidelines.

**Self-Verification Points replace Blocking Checkpoints:**
- Agents verify their own work via CLI/automated checks
- Evidence logged in SUMMARY.md
- Human review at phase boundaries only
- HANDOFF.md for unrecoverable blockers

**Standard Practice:** Automated verification is preferred over manual intervention when possible.

### Authentication Gate Protocol

**Reference:** See `references/authentication-gates.md` for authentication error handling.

**Standard Response to Auth Errors:**
1. RECOGNIZE: CLI/API returns "Not authenticated", "401", "403"
2. CREATE: HANDOFF.md with auth requirements
3. PROVIDE: Exact authentication steps needed
4. EXIT: Terminate execution (do not wait)
5. RESUME: Continue from handoff after human provides credentials

## Validation Standards

**Planning Document Compliance:**

**BRIEF.md Compliance:**
- [ ] Contains project one-liner
- [ ] Success criteria are measurable
- [ ] Out of scope prevents creep
- [ ] Under 50 lines (v1.0) or includes current state (v1.1+)

**ROADMAP.md Compliance:**
- [ ] 3-6 phases total
- [ ] Each phase has goal and dependencies
- [ ] Progress table tracks completion
- [ ] Plan counts realistic

**PLAN.md Compliance:**
- [ ] YAML frontmatter complete
- [ ] Context lists @references
- [ ] Tasks have Files, Action, Verify, Done
- [ ] 2-3 tasks per plan

**Execution Document Compliance:**

**SUMMARY.md Compliance:**
- [ ] Substantive one-liner (not "phase complete")
- [ ] Files created/modified listed
- [ ] Verification evidence included
- [ ] Deviations documented
- [ ] Next steps clear

**HANDOFF.md Compliance:**
- [ ] Clear reason category
- [ ] What happened description
- [ ] Specific next actions
- [ ] Verification method
- [ ] Resume instructions

## Handoff Classification Examples

These examples demonstrate the correct Handoff Reason for various scenarios.

<input>
CLI returns "Error: Login required to deploy"
</input>
<reason>AUTH_GATE</reason>
<action>Create HANDOFF.md requesting credentials.</action>

<input>
Task requires "Create User Model" but no database technology is selected in BRIEF.md
</input>
<reason>AMBIGUOUS</reason>
<action>Create HANDOFF.md requesting architectural decision.</action>

<input>
Git push rejected with "Updates were rejected"
</input>
<reason>CONFLICT</reason>
<action>Create HANDOFF.md requesting merge resolution.</action>
