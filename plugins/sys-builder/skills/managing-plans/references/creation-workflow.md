# Project Planning Workflow

## Core Purpose

Creates `.cattoolkit/plan/{project-slug}/` structure based on user requirements and existing codebase state. Routes to autonomous or interactive workflow based on complexity detection.

## Routing Logic

### Force Interactive Mode
**Trigger:** `--interactive` flag present
**Action:** Use interactive workflow

### Force Autonomous Mode
**Trigger:** `--force-autonomous` flag present
**Action:** Use autonomous workflow regardless of complexity

### Auto-Detect Complexity

**Triggers for Interactive Mode:**
- Ambiguous technology terms ("framework", "database" without specifics)
- Multiple stakeholders mentioned ("team", "client", "stakeholder")
- Decision keywords ("decide", "choose", "discuss", "clarify")
- Complex scope ("platform", "system", "architecture")

**Default to Autonomous When:**
- Specific technology stack mentioned
- Clear feature scope
- Single well-defined objective
- Time constraints indicated

## Autonomous Workflow Protocol

### Phase 1: Investigation
**Goal:** Understand existing codebase

**Process:**
1. **Scan Project Structure**
   - Use Glob to find: package.json, pyproject.toml, requirements.txt, Cargo.toml
   - Use Glob to find: README.md, *.md, docs/*
   - Use Glob to find: src/**/*, lib/**/*, app/**/*

2. **Analyze Dependencies**
   - Read dependency files (package.json, requirements.txt, etc.)

3. **Codebase Metrics**
   - Count files and analyze structure

4. **Documentation Review**
   - Read README.md, ARCHITECTURE.md (if exists), docs/*

**Output:** Discovery report with technology stack, codebase size, patterns, and documentation state.

### Phase 2: Synthesis
**Goal:** Combine user requirements with discovery

**Process:**
1. **Parse User Requirements** - Extract functional/non-functional needs, constraints
2. **Map to Existing Codebase** - What exists, what's missing, what conflicts
3. **Generate Success Criteria** - Measurable outcomes, testable conditions

**Output:** Synthesized requirements mapped to reality.

### Phase 3: Plan Creation
**Goal:** Create standards-compliant plan files

**Process:**
1. **Create BRIEF.md** with objective, success criteria, constraints, current state
2. **Create ROADMAP.md** with phases table (status, dependencies, summaries)
3. **Create Phase Plans** in phases/XX-name/XX-XX-PLAN.md format

**Uses:** `managing-plans` templates and schemas

### Phase 4: Present Menu
**Ask User:**
> Plan created successfully! What's next?
>
> **Option 1:** Execute full plan → `/sys-builder:run-plan`
> **Option 2:** Execute Phase 1 only → `/sys-builder:run-plan 1`
> **Option 3:** Refine plan first → `/sys-builder:manage-plan`

## Interactive Workflow Protocol

### Phase 1: Deep Discovery
**Goal:** Understand technical context completely

**Process:** Same as autonomous Phase 1, but more thorough investigation.

### Phase 2: The Question Burst
**Goal:** Eliminate all ambiguities

**Process:**
1. **Analyze Requirements** - Parse user requirements, identify ambiguities
2. **Present Clarification Menu** using `AskUserQuestion` tool:
   - Present 3 options per ambiguity
   - Mark recommendation as [RECOMMENDED]
   - Wait for selection

**Question Structure:**
```
Clarification Needed: {Category}
{description of ambiguity}

[RECOMMENDED] {Recommended Option}
  - {Reason 1}
  - {Reason 2}
  - {Reason 3}

  Option B: {Option B Name}
  - {Pros/cons}

  Option C: {Option C Name}
  - {Pros/cons}
```

**Wait** for user selection before proceeding.

### Phase 3: Architecture
**Goal:** Create plan with 100% clarity

**Process:**
1. **Synthesize Requirements** - User requirements + discovery findings + clarified answers
2. **Create Plan Files** - Use `managing-plans` templates, generate BRIEF.md, ROADMAP.md
3. **STOP for Validation** - Present complete plan, ask for approval, wait

### Phase 4: Task Generation
**Goal:** Create detailed, actionable tasks

**Process:**
1. **Generate Phase Plans** - Create phases/XX-name/XX-XX-PLAN.md files
2. **Validate Task Quality** - Each task has Scope, Action, Verify, Done

## Output Structure

Both workflows create:
```
.cattoolkit/plan/{project-slug}/
├── BRIEF.md           # Project definition
├── DISCOVERY.md       # Investigation findings
├── ROADMAP.md         # Phase overview
└── phases/
    ├── 01-foundation/
    │   └── 01-01-PLAN.md
    ├── 02-core/
    │   └── 02-01-PLAN.md
    └── 03-enhancement/
        └── 03-01-PLAN.md
```

**Interactive mode additionally creates:**
```
├── QUESTIONS.md        # Clarification Q&A log
```

## Detection Algorithm

```python
# Complexity scoring (simplified)
complexity_score = 0

# Ambiguous tech terms (+2 each)
if contains_any(["framework", "database", "backend", "frontend"]):
    complexity_score += 2

# Stakeholder terms (+2 each)
if contains_any(["team", "client", "stakeholder", "organization"]):
    complexity_score += 2

# Decision keywords (+3 each)
if contains_any(["decide", "choose", "discuss", "clarify", "explore"]):
    complexity_score += 3

# Complex scope (+2 each)
if contains_any(["platform", "system", "architecture", "infrastructure"]):
    complexity_score += 2

# Route decision
if "--interactive" in args or complexity_score >= 5:
    route_to("interactive_workflow")
else:
    route_to("autonomous_workflow")
```

## Advanced Options

### Bypass Detection
Force autonomous mode: Use `--force-autonomous` flag

### Skip Discovery
When you already know the codebase: Use `--skip-discovery` flag

### Specify Output Directory
Custom plan location: Use `--output-dir` flag
