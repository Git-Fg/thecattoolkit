# Project Orchestrator Plugin

**License:** MIT

End-to-end project planning and execution suite using the Orchestrator-Executor pattern for autonomous AI development.

## Overview

The Project Orchestrator plugin implements the **Sovereign Triangle** architecture to provide comprehensive project management capabilities. It handles hierarchical planning, autonomous execution, and quality assurance through a coordinated system of commands, agents, and skills.

## Target Users

- **Project Lead/Architect** - High-level project planning and strategy
- **Development Team** - Task execution and progress tracking
- **Product Managers** - Feature prioritization and roadmap management

## Architecture Pattern

This plugin implements the **Sovereign Triangle** pattern:
- **Commands** orchestrate workflows
- **Agents** execute specialized tasks in isolated contexts
- **Skills** provide standards and templates

## Features

### Hierarchical Planning
- **BRIEF.md** - Project vision and scope definition
- **ROADMAP.md** - High-level milestones and timeline
- **PLAN.md** - Detailed phase-by-phase execution plan

### Autonomous Execution
- Fresh context for each task execution
- Self-verification of outputs
- Automated quality assurance checks

### State-in-Files
- All decisions tracked in disk-based files
- Persistent progress tracking
- Complete audit trail

## Commands

### `/create-plan` [project description]

Creates a hierarchical project plan from a high-level description.

**Pattern:** Sovereign Triangle (delegates to plan-author agent)

**Usage:**
```bash
/create-plan "Build a web application for task management with user authentication"
```

**Output:**
- `BRIEF.md` - Project vision and scope
- `ROADMAP.md` - Milestone roadmap
- `PLAN.md` - Detailed execution plan

**Example:**
```
You: /create-plan "Build an e-commerce platform"

AI: I'll create a comprehensive project plan. Let me gather context about your requirements.

[... AI collects requirements ...]

[... Delegates to plan-author agent ...]

AI: Project plan created!
- BRIEF.md - Vision and scope
- ROADMAP.md - 6-month milestone roadmap
- PLAN.md - Detailed phase-by-phase plan
```

### `/run-plan` [path to PLAN.md]

Orchestrates the execution of a detailed project plan with quality assurance.

**Pattern:** Sovereign Triangle (delegates to task-executor agent)

**Usage:**
```bash
/run-plan ./my-project/PLAN.md
```

**Process:**
1. Reads and parses the PLAN.md
2. Executes each phase sequentially
3. Verifies task completion
4. Tracks progress
5. Reports completion status

**Example:**
```
You: /run-plan ./ecommerce-platform/PLAN.md

AI: Starting plan execution...

Phase 1: Foundation Setup
├─ Task 1.1: Set up repository structure ✓
├─ Task 1.2: Configure CI/CD pipeline ✓
└─ Task 1.3: Initialize database schema ✓

Phase 2: Authentication System
├─ Task 2.1: Implement user registration ✓
├─ Task 2.2: Build login functionality ✓
└─ Task 2.3: Add password reset flow ✓

Plan execution complete! All tasks verified.
```

## Agents

### plan-author

Specialized in creating hierarchical project plans.

**Responsibilities:**
- Analyzes project requirements
- Creates BRIEF.md with vision and scope
- Develops ROADMAP.md with milestones
- Structures PLAN.md with detailed phases

**Skills:**
- `project-lifecycle` - Document templates, planning methodology, and best practices

**Output:**
- Comprehensive project documentation
- Structured execution plan
- Task breakdowns with dependencies

### task-executor

Executes individual tasks within a plan phase.

**Responsibilities:**
- Performs specific development tasks
- Verifies task completion
- Generates progress reports
- Handles task dependencies

**Skills:**
- `project-lifecycle` - Output format compliance and task structure understanding

**Output:**
- Completed deliverables
- Verification reports
- Progress tracking

## Skills

### project-lifecycle

Provides document templates, format standards, and planning methodology.

**Resources:**
- `assets/templates/brief.md` - Project brief template
- `assets/templates/roadmap.md` - Roadmap template
- `assets/templates/phase-plan.md` - Plan template
- `assets/templates/summary.md` - Progress summary template
- `assets/templates/handoff.md` - Task handoff template
- `references/` - All planning and execution protocol standards

### project-analysis

Analyzes project structure, tech stack, and adheres to AI rules.

**Resources:**
- `references/architecture-map.md` - System design analysis
- `references/quick-scan.md` - Fast project identification
- `references/sync-rules.md` - AI rule synchronization
- `references/tech-stack-signatures.md` - Technology stack identification
- `references/dependency-audit.md` - Dependency analysis

## Document Structure

### BRIEF.md
Project vision and scope definition.

**Sections:**
- Project Vision
- Scope & Boundaries
- Success Criteria
- Constraints & Assumptions
- Stakeholders

### ROADMAP.md
High-level milestone roadmap.

**Sections:**
- Milestone Timeline
- Phase Dependencies
- Resource Allocation
- Risk Assessment

### PLAN.md
Detailed phase-by-phase execution plan.

**Structure:**
```markdown
# Project Plan: [Name]

## Phase 1: [Name]
### Tasks:
1. **Task 1.1** - [Description]
   - Owner: [Role]
   - Dependencies: [List]
   - Deliverables: [List]
   - Verification: [Criteria]

2. **Task 1.2** - [Description]
   [...]

## Phase 2: [Name]
[...]
```

## Usage Examples

### Example 1: New Project Setup

```bash
# Step 1: Create the plan
/create-plan "Build a task management web app with React and Node.js"

# Step 2: Review the plan
cat BRIEF.md
cat ROADMAP.md
cat PLAN.md

# Step 3: Execute the plan
/run-plan ./task-app/PLAN.md
```

### Example 2: Continuing an Existing Project

```bash
# Continue from where you left off
/run-plan ./existing-project/PLAN.md
```

### Example 3: Modifying a Plan

```bash
# Edit the plan as needed
nano ./my-project/PLAN.md

# Re-run with updated plan
/run-plan ./my-project/PLAN.md
```

## Quality Assurance

The orchestrator includes automated QA checks:

### Task Verification
- Output file existence
- Code compilation/tests
- Documentation completeness
- Specification compliance

### Progress Tracking
- Task completion percentage
- Phase progress
- Timeline adherence
- Dependency resolution

### Error Handling
- Failed task detection
- Retry mechanisms
- Error reporting
- Handoff documentation

## Integration

### Version Control
- Git integration for all deliverables
- Commit message standards
- Branch strategy recommendations

### CI/CD
- Pipeline configuration templates
- Automated testing integration
- Deployment workflows

### Documentation
- Markdown-based documentation
- Consistent formatting
- Template compliance

## Best Practices

1. **Start with Clear Vision** - Use BRIEF.md to define project scope
2. **Break Down Thoroughly** - Decompose into executable tasks
3. **Track Progress** - Review PLAN.md status regularly
4. **Verify Completion** - Ensure each task meets verification criteria
5. **Update Documentation** - Keep all files synchronized

## Architecture Benefits

### Separation of Concerns
- Planning separate from execution
- Orchestration separate from implementation
- Standards separate from application

### Autonomy
- Agents work independently
- Minimal human intervention
- Self-verifying outputs

### Maintainability
- Standards-based approach
- Consistent documentation
- Clear separation of roles

## Troubleshooting

### Plan Execution Fails
1. Check PLAN.md syntax
2. Verify task dependencies
3. Review handoff logs
4. Re-run specific phase

### Quality Checks Fail
1. Review verification criteria
2. Check deliverable completeness
3. Validate against templates
4. Update standards if needed

### Context Issues
1. Verify all files exist
2. Check file permissions
3. Review agent logs
4. Clear and restart if needed

## References

### Documentation
- **[@VECTOR_vs_TRIANGLE.md](../../../docs/VECTOR_vs_TRIANGLE.md)** - Architectural patterns
- **[@CLAUDE.md](../../CLAUDE.md)** - Development standards
- **[project-lifecycle SKILL.md](skills/project-lifecycle/SKILL.md)** - Planning methodology

### Templates
- **[Brief Template](skills/project-lifecycle/assets/templates/brief.md)**
- **[Roadmap Template](skills/project-lifecycle/assets/templates/roadmap.md)**
- **[Plan Template](skills/project-lifecycle/assets/templates/phase-plan.md)**

## License

MIT License - see plugin directory for full license text.
