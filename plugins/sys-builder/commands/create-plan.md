---
description: "Architect a project plan based on autonomous codebase investigation."
argument-hint: "<project description>"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, Skill(managing-project-plans), Skill(architecting-project-plans)]
disable-model-invocation: true
---

# Create Plan (Autonomous)

## Quick Reference
- **Usage**: `/sys-builder:create-plan "Description of what to build"`
- **Purpose**: Investigate codebase, synthesize requirements, create comprehensive plan
- **Returns**: Plan files created in `.cattoolkit/plan/{project-slug}/`
- **Constraint**: Does NOT execute code—only creates plan files

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start) (Create a plan in 3 steps)
3. [Detailed Protocol](#detailed-protocol) (Complete workflow)
4. [Examples](#examples) (Common scenarios)
5. [Reference](#reference) (Technical details)

## Overview (Expandable)

This command creates a `.cattoolkit/plan/` structure based on:
- User requirements (from arguments)
- Existing codebase state (auto-discovered)
- Industry best practices (applied automatically)

**Workflow:**
1. **Investigation** → Scan codebase structure and dependencies
2. **Synthesis** → Combine requirements with discovery findings
3. **Plan Creation** → Generate BRIEF, ROADMAP, and phase plans
4. **Presentation** → Ask user how to proceed

**Uses Skills:**
- `managing-project-plans` - Templates and standards
- `architecting-project-plans` - Investigation and synthesis methodology

## Quick Start

```bash
# Basic usage
/sys-builder:create-plan "Build a React app with user authentication"

# Creates:
# .cattoolkit/plan/react-app-auth/BRIEF.md
# .cattoolkit/plan/react-app-auth/ROADMAP.md
# .cattoolkit/plan/react-app-auth/phases/01-foundation/01-01-PLAN.md
```

**Three Steps:**
1. **Invoke**: Run command with project description
2. **Wait**: Investigation and synthesis complete
3. **Choose**: Select next action (execute, refine, or review)

## Detailed Protocol

### Phase 1: Investigation
**Goal:** Understand existing codebase

**Process:**
1. **Scan Project Structure**
   ```bash
   # Use Glob to find key files
   Glob pattern: package.json, pyproject.toml, requirements.txt, Cargo.toml
   Glob pattern: README.md, *.md, docs/*
   Glob pattern: src/**/*, lib/**/*, app/**/*
   ```

2. **Analyze Dependencies**
   ```bash
   # Read dependency files
   Read: package.json
   Read: requirements.txt or pyproject.toml
   Read: Cargo.toml or go.mod
   ```

3. **Codebase Metrics**
   ```bash
   # Count files and analyze structure
   Bash: find . -type f -not -path '*/.*' | wc -l
   Bash: find . -type d -not -path '*/.*' | wc -l
   ```

4. **Documentation Review**
   ```bash
   # Read existing docs
   Read: README.md
   Read: ARCHITECTURE.md (if exists)
   Read: docs/* (if exists)
   ```

**Output:** Discovery report with:
- Technology stack identified
- Codebase size and structure
- Existing patterns and conventions
- Documentation state

### Phase 2: Synthesis
**Goal:** Combine user requirements with discovery

**Process:**
1. **Parse User Requirements**
   - Extract functional needs
   - Identify non-functional requirements
   - Note constraints and preferences

2. **Map to Existing Codebase**
   - What exists? (infrastructure, patterns, code)
   - What's missing? (gaps to fill)
   - What conflicts? (contradictions to resolve)

3. **Generate Success Criteria**
   - Measurable outcomes
   - Testable conditions
   - Acceptance criteria

**Output:** Synthesized requirements with:
- Requirements mapped to reality
- Constraints identified
- Success criteria defined

### Phase 3: Plan Creation
**Goal:** Create standards-compliant plan files

**Process:**
1. **Create BRIEF.md**
   ```markdown
   # Project: {name}

   ## Objective
   {Synthesized from requirements}

   ## Success Criteria
   - [ ] {Measurable criterion 1}
   - [ ] {Measurable criterion 2}

   ## Constraints
   - Technical: {Framework, versions, etc.}
   - Business: {Timeline, scope, etc.}

   ## Current State (Brownfield)
   - Existing: {What's already there}
   - Migration: {What needs to change}
   ```

2. **Create ROADMAP.md**
   ```markdown
   # Roadmap: {project-name}

   ## Phases

   | Phase | Name | Status | Dependencies | Summary |
   |-------|------|--------|--------------|---------|
   | 01 | Foundation | [ ] | none | Setup and structure |
   | 02 | Core Features | [ ] | 01 | Main functionality |
   | 03 | Enhancement | [ ] | 02 | Advanced features |
   ```

3. **Create Phase Plans**
   ```markdown
   # Phase 01: Foundation

   ## Tasks

   ### Task 1: Setup project structure
   **Scope:** {Files/directories}
   **Action:** {What to do}
   **Verify:** {How to verify}
   **Done:** {Acceptance criteria}
   ```

**Uses:** `managing-project-plans` templates and schemas

### Phase 4: Present Menu
**Goal:** Guide user to next action

**Ask User:**
> Plan created successfully! What's next?
>
> **Option 1:** Execute full plan → I'll run `/sys-builder:run-plan`
> **Option 2:** Execute Phase 1 only → I'll run `/sys-builder:run-plan 1`
> **Option 3:** Refine plan first → I'll run `/sys-builder:manage-plan`

**User Selection:** Based on user choice, invoke appropriate command

## Examples

### Example 1: New React App
```bash
/sys-builder:create-plan "Build a task management app with React"
```
**Creates:**
- BRIEF.md: Task app with React frontend
- ROADMAP.md: 4 phases (Foundation, Auth, Tasks, Polish)
- Phase plans with React-specific tasks

### Example 2: Adding Feature to Existing Project
```bash
/sys-builder:create-plan "Add payment processing to existing Django app"
```
**Creates:**
- BRIEF.md: Payment feature for Django
- ROADMAP.md: Integration + feature phases
- Phase plans respecting Django patterns

### Example 3: Python Package
```bash
/sys-builder:create-plan "Create a Python CLI tool for data processing"
```
**Creates:**
- BRIEF.md: CLI tool with data processing
- ROADMAP.md: Setup, core, tests, docs phases
- Phase plans with Python best practices

### Example 4: Microservice
```bash
/sys-builder:create-plan "Build a Go microservice with Docker"
```
**Creates:**
- BRIEF.md: Microservice architecture
- ROADMAP.md: Service + deployment phases
- Phase plans with Go and Docker patterns

## Reference

### File Structure Created
```
.cattoolkit/plan/{project-slug}/
├── BRIEF.md           # Project definition
├── DISCOVERY.md       # Auto-discovery findings
├── ROADMAP.md         # Phase overview
└── phases/
    ├── 01-foundation/
    │   └── 01-01-PLAN.md
    ├── 02-core/
    │   └── 02-01-PLAN.md
    └── 03-enhancement/
        └── 03-01-PLAN.md
```

### Skills Used
| Skill | Purpose | When |
|-------|---------|------|
| managing-project-plans | Templates, schemas, validation | During plan creation |
| architecting-project-plans | Investigation, synthesis methodology | During discovery and analysis |

### Validation Rules
**File Naming:**
- BRIEF.md: Must exist at project root
- ROADMAP.md: Must exist at project root
- Phase files: Must be in `phases/` directory
- Phase directories: Must be `XX-name` format

**Status Codes:**
- `[ ]` = Pending (not started)
- `[~]` = In Progress (currently executing)
- `[x]` = Complete (finished)
- `[!]` = Blocked (needs intervention)

**Dependencies:**
- Phase N must depend on Phase N-1 being `[x]`
- No circular dependencies allowed
- Dependencies must be explicit

### Templates Used
All templates sourced from `managing-project-plans/assets/templates/`:
- `brief.md` - Project definition template
- `roadmap.md` - Phase overview template
- `phase-plan.md` - Task list template

### Common Patterns
**Greenfield (New Project):**
- Foundation → Core → Enhancement → Polish
- Focus on setup first, features second

**Brownfield (Existing Project):**
- Discovery → Integration → Feature → Migration
- Respect existing patterns

**Feature Addition:**
- Analysis → Implementation → Testing → Documentation
- Follow existing conventions

**Refactoring:**
- Assessment → Migration → Validation → Cleanup
- Plan for rollback

### Error Handling
**If investigation fails:**
- Log discovery partial results
- Create plan with limited context
- Note assumptions made

**If synthesis unclear:**
- Ask user for clarification
- Create multiple plan options
- Mark assumptions in BRIEF.md

**If plan validation fails:**
- Check file structure
- Verify status codes
- Confirm dependencies
- Regenerate if necessary

### Limitations
- Does NOT execute code
- Does NOT modify existing files
- Does NOT install dependencies
- Does NOT create actual project structure

**Only Creates:**
- Plan files in `.cattoolkit/plan/`
- No side effects

### Next Steps After Creation
**Execute Plan:**
```bash
/sys-builder:run-plan
```

**Execute Specific Phase:**
```bash
/sys-builder:run-plan 1
```

**Refine Plan:**
```bash
/sys-builder:manage-plan "add task to phase 2"
```

**View Plan:**
```bash
cat .cattoolkit/plan/{project-slug}/BRIEF.md
cat .cattoolkit/plan/{project-slug}/ROADMAP.md
```
