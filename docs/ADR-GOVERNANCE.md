# ADR Governance

## Ownership Model

**Architect Plugin** is the **SOLE OWNER** of Architecture Decision Records (ADRs).

- **Responsibility**: Create, update, and maintain all ADRs
- **Authority**: Makes all architectural decisions
- **Ownership**: Owns the ADR.md file and ADR template

**Planner Plugin** is a **READER/REFERENCER** of ADRs.

- **Responsibility**: Read and respect existing architectural decisions
- **Authority**: Cannot create or modify ADRs
- **Role**: Incorporates ADR decisions into project plans

## Workflow

### Standard Project Flow

1. **Architect Phase** (BEFORE planning)
   - Run Architect agent to establish system architecture
   - Create ADR.md with initial architectural decisions
   - Document technology choices, patterns, and constraints

2. **Planning Phase** (AFTER architecture)
   - Run Planner agent to create project roadmap
   - Plan-author reads existing ADR.md
   - Incorporates architectural decisions into ROADMAP.md
   - Does NOT generate new ADRs

### When ADR Doesn't Exist

If plan-author detects no ADR.md exists:
- Note in context: "No architectural decisions documented yet - Architect plugin should be consulted first"
- Proceed with planning but flag architectural uncertainty
- Recommend running Architect before execution

## File Locations

- **ADR.md**: `.cattoolkit/planning/{project-slug}/ADR.md`
- **Templates**: `plugins/architect/skills/architecture/references/adr-template.md`
- **Standards**: `plugins/architect/skills/architecture/SKILL.md`

## ADR Template

See `plugins/architect/skills/architecture/references/adr-template.md` for the canonical ADR format.

## Violation Detection

**Never:**
- Planner generates ADR.md
- Multiple ADR templates exist
- ADR entries are deleted or reordered
- Planning proceeds without architectural context

**Always:**
- Architect owns ADR creation
- Sequential numbering (ADR-001, ADR-002, etc.)
- Append-only entries
- Planner references existing ADRs


