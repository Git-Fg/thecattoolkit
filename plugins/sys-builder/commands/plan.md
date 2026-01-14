---
description: "Intelligently architect project plans. Auto-detects complexity to route between autonomous and interactive modes. Use when starting projects or planning features."
argument-hint: "<project description> [--interactive]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, Skill(managing-project-plans), AskUserQuestion]
disable-model-invocation: true
---

# Plan (Unified Entry Point)

## Quick Reference
- **Usage**: `/sys-builder:plan "Description"` or `/sys-builder:plan "Description" --interactive`
- **Purpose**: Intelligent routing to appropriate planning workflow
- **Detection**: Auto-analyzes requirements complexity
- **Returns**: Plan files in `.cattoolkit/plan/{project-slug}/`

## Routing Logic

### 1. Force Interactive Mode
**Trigger:** `--interactive` flag present
**Action:** Use create-plan-interactive workflow

### 2. Auto-Detect Complexity
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

### 3. Execute Chosen Workflow
**Autonomous:**
- Investigate codebase automatically
- Generate plan without questions
- Present results for review

**Interactive:**
- Deep discovery phase
- Present clarification menu
- Wait for user selections
- Generate plan with 100% clarity

## Usage Examples

### Autonomous Mode (Auto-detected)
```bash
# Specific technology stack
/sys-builder:plan "Build a React TODO app with TypeScript"

# Clear feature scope
/sys-builder:plan "Add password reset to existing auth system"

# Single well-defined objective
/sys-builder:plan "Convert ES5 to ES6 in src/utils"
```

### Interactive Mode (Auto-detected)
```bash
# Ambiguous technology
/sys-builder:plan "Build a web application"

# Multiple stakeholders
/sys-builder:plan "Create platform for team collaboration"

# Decision keywords present
/sys-builder:plan "Build system - we need to decide on architecture"
```

### Force Interactive Mode
```bash
# Override auto-detection
/sys-builder:plan --interactive "Build a React TODO app"
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
    route_to("create-plan-interactive")
else:
    route_to("create-plan")
```

## Workflow Delegation

### Autonomous Workflow
Follow the `create-plan.md` protocol:
1. Investigation (automated)
2. Synthesis (automated)
3. Plan creation (automated)
4. Present menu for next steps

### Interactive Workflow
Follow the `create-plan-interactive.md` protocol:
1. Deep discovery
2. Question burst (use AskUserQuestion)
3. Wait for selections
4. Architecture based on clarified requirements
5. Task generation

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

## Advanced Options

### Bypass Detection
Force autonomous mode even with complex description:
```bash
/sys-builder:plan --force-autonomous "Build complex platform"
```

### Skip Discovery
When you already know the codebase:
```bash
/sys-builder:plan "Add feature" --skip-discovery
```

### Specify Output Directory
Custom plan location:
```bash
/sys-builder:plan "Build app" --output-dir .cattoolkit/plans/custom-name
```

## Next Steps

After plan creation:

```bash
# Execute full plan
/sys-builder:run-plan

# Execute specific phase
/sys-builder:run-plan 1

# Modify plan
/sys-builder:manage-plan "add task to phase 2"

# View plan
cat .cattoolkit/plan/{project-slug}/BRIEF.md
```

## Differences from Direct Commands

| Command | When to Use |
|---------|-------------|
| `/sys-builder:plan` | **Default** - let Claude decide the best approach |
| `/sys-builder:create-plan` | You know requirements are clear |
| `/sys-builder:create-plan-interactive` | You know requirements are complex |

**Use `/plan` for:** Intelligent routing, reduced cognitive load
**Use direct commands for:** Explicit control, known workflows
