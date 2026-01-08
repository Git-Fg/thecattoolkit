# Roadmap Template

## MANDATORY USAGE

**YOU MUST USE THIS TEMPLATE** when creating `.cattoolkit/planning/{project-slug}/ROADMAP.md`.

**Scoped Folder:** ALWAYS use scoped project folder `{project-slug}` (e.g., `user-auth-system`)

**Related Files:**
- `@.cattoolkit/planning/{project-slug}/BRIEF.md` - Project brief
- `@.cattoolkit/planning/{project-slug}/ADR.md` - Architecture Decision Records
- `@.cattoolkit/planning/{project-slug}/ISSUES.md` - Deferred enhancements

## Initial Roadmap (v1.0 Greenfield)

```markdown
---
project: [Project Name]
version: 1.0
status: in_progress  # Tracks: in_progress | completed
---

# Roadmap: [Project Name]

## Overview

[One paragraph describing the journey from start to finish]

## Phases

- [ ] **Phase 1: [Name]** - [One-line description]
- [ ] **Phase 2: [Name]** - [One-line description]
- [ ] **Phase 3: [Name]** - [One-line description]
- [ ] **Phase 4: [Name]** - [One-line description]

## Phase Details

### Phase 1: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Nothing (first phase)
**Plans**: [Number of plans, e.g., "3 plans" or "TBD after research"]

Plans:
- [ ] 01-01: [Brief description of first plan]
- [ ] 01-02: [Brief description of second plan]
- [ ] 01-03: [Brief description of third plan]

### Phase 2: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Phase 1
**Plans**: [Number of plans]

Plans:
- [ ] 02-01: [Brief description]

### Phase 3: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Phase 2
**Plans**: [Number of plans]

Plans:
- [ ] 03-01: [Brief description]
- [ ] 03-02: [Brief description]

### Phase 4: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Phase 3
**Plans**: [Number of plans]

Plans:
- [ ] 04-01: [Brief description]

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. [Name] | 0/3 | Not started | - |
| 2. [Name] | 0/1 | Not started | - |
| 3. [Name] | 0/2 | Not started | - |
| 4. [Name] | 0/1 | Not started | - |
```

## MANDATORY Guidelines

**Initial planning (v1.0):**
- **MUST** have 3-6 phases total (more = scope creep)
- **MUST** deliver something coherent per phase
- **MUST** split phases with >7 tasks or multiple subsystems
- **MUST** use naming: `{phase}-{plan}-PLAN.md` (e.g., `01-02-PLAN.md`)
- **STRICTLY PROHIBITED:** Time estimates
- Plan count can be "TBD" initially, refined during planning

**After milestones ship:**
- **MUST** reorganize with milestone groupings (see below)
- **MUST** collapse completed milestones in `<details>` tags
- **MUST** add new milestone sections for upcoming work
- **MUST** keep continuous phase numbering (never restart at 01)

## Status Values

- `Not started` - Haven't begun
- `In progress` - Currently working
- `Complete` - Done (add completion date)
- `Deferred` - Pushed to later (with reason)

## Milestone-Grouped Roadmap (After v1.0 Ships)

After completing first milestone, reorganize roadmap with milestone groupings:

```markdown
---
project: [Project Name]
version: 2.0
status: in_progress  # Tracks: in_progress | completed
---

# Roadmap: [Project Name]

## Milestones

- ✅ **v1.0 MVP** - Phases 1-4 (shipped YYYY-MM-DD)
- 🚧 **v1.1 [Name]** - Phases 5-6 (in progress)
- 📋 **v2.0 [Name]** - Phases 7-10 (planned)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-4) - SHIPPED YYYY-MM-DD</summary>

### Phase 1: [Name]
**Goal**: [What this phase delivers]
**Plans**: 3 plans

Plans:
- [x] 01-01: [Brief description]
- [x] 01-02: [Brief description]
- [x] 01-03: [Brief description]

### Phase 2: [Name]
**Goal**: [What this phase delivers]
**Plans**: 2 plans

Plans:
- [x] 02-01: [Brief description]
- [x] 02-02: [Brief description]

### Phase 3: [Name]
**Goal**: [What this phase delivers]
**Plans**: 2 plans

Plans:
- [x] 03-01: [Brief description]
- [x] 03-02: [Brief description]

### Phase 4: [Name]
**Goal**: [What this phase delivers]
**Plans**: 1 plan

Plans:
- [x] 04-01: [Brief description]

</details>

### 🚧 v1.1 [Name] (In Progress)

**Milestone Goal:** [What v1.1 delivers]

#### Phase 5: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Phase 4
**Plans**: 1 plan

Plans:
- [ ] 05-01: [Brief description]

#### Phase 6: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Phase 5
**Plans**: 2 plans

Plans:
- [ ] 06-01: [Brief description]
- [ ] 06-02: [Brief description]

### 📋 v2.0 [Name] (Planned)

**Milestone Goal:** [What v2.0 delivers]

#### Phase 7: [Name]
**Goal**: [What this phase delivers]
**Depends on**: Phase 6
**Plans**: 3 plans

Plans:
- [ ] 07-01: [Brief description]
- [ ] 07-02: [Brief description]
- [ ] 07-03: [Brief description]

[... additional phases for v2.0 ...]

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Foundation | v1.0 | 3/3 | Complete | YYYY-MM-DD |
| 2. Features | v1.0 | 2/2 | Complete | YYYY-MM-DD |
| 3. Polish | v1.0 | 2/2 | Complete | YYYY-MM-DD |
| 4. Launch | v1.0 | 1/1 | Complete | YYYY-MM-DD |
| 5. Security | v1.1 | 0/1 | Not started | - |
| 6. Hardening | v1.1 | 0/2 | Not started | - |
| 7. Redesign Core | v2.0 | 0/3 | Not started | - |
```

**Notes:**

- Milestone emoji: ✅ shipped, 🚧 in progress, 📋 planned
- Completed milestones collapsed in `<details>` for readability
- Current/future milestones expanded
- Continuous phase numbering (01-99)
- Progress table includes milestone column
