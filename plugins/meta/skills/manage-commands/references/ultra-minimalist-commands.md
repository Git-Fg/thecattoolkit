# Ultra-Minimalist Commands Reference

## Important Note

This structure applies specifically to **commands that invoke skills with workflows**. These commands provide comprehensive guidance by including Objective, Process, and Success Criteria sections that delegate to skills.

**For commands that do NOT invoke workflows** (e.g., direct command implementations, agent invocations without workflows, or simple delegation commands), use a simpler structure with just the instruction text and minimal frontmatter.

## Cat Toolkit Examples

All Cat Toolkit commands that invoke skills with workflows follow this structured pattern:

### Verbs (Invoke Skills)

**`/debug`**
```markdown
---
description: Debug issues and fix bugs with systematic investigation.
allowed-tools: Skill(engineering)
argument-hint: [error description]
---

## Objective
Debug and fix the issue described: $ARGUMENTS

This systematically investigates problems, identifies root causes, and implements effective solutions.

## Process
1. Invoke the `engineering` skill with debugging workflow
2. Gather error details and context
3. Analyze symptoms and failure patterns
4. Investigate root causes systematically
5. Develop and test solutions
6. Implement fixes with verification
7. Add tests to prevent regression

## Success Criteria
- Root cause identified with certainty
- Solution implemented and verified
- No regressions introduced
- Tests added to prevent future occurrences
- Clear explanation of fix provided
```

**`/review`**
```markdown
---
description: Perform comprehensive code review with quality assurance.
allowed-tools: Skill(engineering)
argument-hint: [focus areas or changes to review]
---

## Objective
Perform comprehensive code review and analyze: $ARGUMENTS

This ensures code quality, identifies potential issues, and provides actionable feedback for improvements.

## Process
1. Invoke the `engineering` skill with code-review workflow
2. Analyze code structure and architecture
3. Review implementation quality and patterns
4. Check for potential bugs and edge cases
5. Assess security and performance implications
6. Provide specific, actionable feedback
7. Suggest improvements with rationale

## Success Criteria
- Code thoroughly reviewed with depth
- Specific issues identified with locations
- Actionable feedback provided
- Best practices recommendations delivered
- Quality assessment with improvement suggestions
```

**`/system-design`**
```markdown
---
description: Design systems and plan architectural solutions.
allowed-tools: Skill(engineering)
argument-hint: [system requirements or design task]
---

## Objective
Design system architecture and plan solutions for: $ARGUMENTS

This creates comprehensive architectural plans with clear patterns, trade-offs, and implementation guidance.

## Process
1. Invoke the `engineering` skill with architecture workflow
2. Analyze requirements and constraints
3. Identify architectural patterns and trade-offs
4. Design system components and interactions
5. Document decisions and alternatives
6. Provide implementation roadmap
7. Suggest verification strategies

## Success Criteria
- Clear architectural design documented
- Components and interactions defined
- Trade-offs and decisions explained
- Implementation roadmap provided
- Verification strategies suggested
```

### Personas (Use Agents)

**`/brainstorm`**
```markdown
---
description: [Personas] Delegate to brainstormer for strategic thinking and framework-based analysis
allowed-tools: Task, Read, Glob, Grep
argument-hint: [problem or task to analyze]
disable-model-invocation: true
---

Task the brainstormer agent with: $ARGUMENTS

This leverages strategic thinking expertise to break down complex problems and explore multiple solution pathways.

Important: The context provided to the Agent must be exhaustive and cover all relevant information. It starts with a fully-clean slate, like a child - it's better to give it too much context than not enough.
```

**`/prompt-engineer`**
```markdown
---
description: [Personas] Delegate to prompt-engineer for prompt optimization and design
allowed-tools: Task, Read, Glob, Grep
argument-hint: [prompt or task requiring prompt engineering]
disable-model-invocation: true
---

Task the prompt-engineer agent with: $ARGUMENTS

This applies advanced prompt engineering techniques to create high-quality, optimized prompts.

Important: The context provided to the Agent must be exhaustive and cover all relevant information. It starts with a fully-clean slate, like a child - it's better to give it too much context than not enough.
```

**`/expert`**
```markdown
---
description: [Personas] Delegate to expert for system maintenance and infrastructure
allowed-tools: Task, Read, Glob, Grep
argument-hint: [maintenance or audit task]
disable-model-invocation: true
---

Task the plugin-expert agent with: $ARGUMENTS

This provides system maintenance expertise for auditing, creating, or fixing AI components (agents, skills, commands).

Important: The context provided to the Agent must be exhaustive and cover all relevant information. It starts with a fully-clean slate, like a child - it's better to give it too much context than not enough.
```

### Objects (Lifecycle Management)

**`/build`**
```markdown
---
description: Lifecycle manager for toolkit components. Shortcut to create or audit agents, skills, commands, and hooks.
argument-hint: [agent|skill|command|hook] [create|audit] [name/path]
---

## Objective
Perform $2 operation on $1 component: $3

This consolidates all toolkit component lifecycle management into a single command for efficiency and clarity.

## Process
Task the `plugin-expert` agent with the maintenance task: $1 $2 $3

The plugin-expert will:
1. Route to the appropriate management skill based on component type
2. Execute the requested create or audit operation
3. Ensure best practices and Cat Toolkit standards
```

**`/create-plan`**
```markdown
---
description: Create a hierarchical project plan with phases, milestones, and tasks.
allowed-tools: Skill(manage-planning)
argument-hint: [project description]
---

## Objective
Create a hierarchical project plan for: $ARGUMENTS

This establishes a structured plan with clear phases, milestones, and actionable tasks.

## Process
1. Invoke the `manage-planning` skill to create the project plan
2. Follow the plan creation workflow

## Success Criteria
- Project plan created with proper hierarchy in the proper path
- Clear phases and milestones defined
- Tasks actionable and specific
- Follows manage-planning structure
```

### Execution (Run Artifacts)

**`/run-plan`**
```markdown
---
description: Execute hierarchical project plans with intelligent segmentation.
allowed-tools: Skill(manage-planning)
argument-hint: [plan-path]
---

## Objective
Execute the project plan at: $ARGUMENTS

This runs the plan with intelligent segmentation, context management, and progress tracking.

## Process
1. Invoke the `manage-planning` skill with run-plan workflow
2. Load and parse the plan
3. Segment into manageable chunks
4. Execute with context management
5. Track progress and handle handoffs

## Success Criteria
- Plan executed completely
- Progress tracked accurately
- Context managed effectively
- Handoffs handled properly
- Results documented clearly
```

**`/run-plan`**
```markdown
---
description: Execute saved plans in sub-agent contexts.
allowed-tools: Skill(manage-planning)
argument-hint: [plan-name or path]
---

## Objective
Execute the plan at: $ARGUMENTS

This runs saved plans with proper context and structured output handling.

## Process
1. Invoke the `manage-planning` skill
2. Load the plan file
3. Execute in appropriate context
4. Handle structured output
5. Document results

## Success Criteria
- Plan executed successfully
- Context properly managed
- Output structured and clear
- Results documented
- No context pollution
```

## Pattern Analysis

### Structure
1. **YAML Frontmatter** (description, allowed-tools, argument-hint)
2. **## Objective** - Clear purpose with $ARGUMENTS substitution
3. **## Process** - Numbered steps (typically 5-7 steps)
4. **## Success Criteria** - Bullet points of expected outcomes

### YAML Frontmatter

**Required Fields:**
- `description` - Clear, actionable description of what the command does
- `allowed-tools` - Skill or agent to invoke (e.g., `Skill(engineering)`)
- `argument-hint` - Format for arguments (e.g., `[error description]`)

**Optional Fields:**
- None currently used

### Language Patterns

**Objective Section:**
- "This [action verb] [outcome/purpose] for: $ARGUMENTS"
- "This provides [benefit] and [additional value]"
- Keep to 1-2 sentences maximum

**Process Section:**
- "Invoke the `{skill}` skill with [workflow type]"
- "Analyze [subject] and [action]"
- "Provide [output type] with [specifics]"
- 5-7 steps typically

**Success Criteria:**
- Start with action verbs (Identify, Implement, Provide, etc.)
- Be specific and measurable
- 3-6 bullet points typically

### Description Patterns

**Good:**
- "Debug issues and fix bugs with systematic investigation"
- "Perform comprehensive code review with quality assurance"
- "Create a hierarchical project plan with phases, milestones, and tasks"

**Action-Oriented:**
- Start with action verbs (Debug, Create, Perform, Design)
- Focus on what the user accomplishes
- Be specific about the outcome

**Bad:**
- "Shortcut to invoke the engineering skill for debugging"
- "Delegates to brainstormer agent for analysis"
- "Generates project planning using manage-planning"

### Argument Handling

**With Arguments:**
```markdown
argument-hint: [error description]
---

## Objective
Debug and fix the issue described: $ARGUMENTS
```

**Without Arguments:**
```markdown
argument-hint: (none)

## Objective
Perform comprehensive code review and analyze all changes
```

## Key Principles

1. **Structured format** - Use ## Objective, ## Process, ## Success Criteria
2. **Clear purpose** - What this command accomplishes
3. **Action-oriented descriptions** - Start with action verbs
4. **Semantic naming** - Category determines invocation pattern
5. **Comprehensive guidance** - Process steps provide clear direction
6. **Measurable outcomes** - Success criteria define expected results

## Anti-Patterns

❌ **Too Minimal:**
```markdown
---
description: Shortcut to invoke the engineering skill for debugging and bug fixing.
argument-hint: [error description]
---

Invoke the `engineering` skill (debugging workflow) and investigate: $ARGUMENTS
```

✅ **Well-Structured:**
```markdown
---
description: Debug issues and fix bugs with systematic investigation.
allowed-tools: Skill(engineering)
argument-hint: [error description]
---

## Objective
Debug and fix the issue described: $ARGUMENTS

This systematically investigates problems, identifies root causes, and implements effective solutions.

## Process
1. Invoke the `engineering` skill with debugging workflow
2. Gather error details and context
3. Analyze symptoms and failure patterns
4. Investigate root causes systematically
5. Develop and test solutions
6. Implement fixes with verification
7. Add tests to prevent regression

## Success Criteria
- Root cause identified with certainty
- Solution implemented and verified
- No regressions introduced
- Tests added to prevent future occurrences
- Clear explanation of fix provided
```

## Quality Checklist

- [ ] Description is action-oriented and clear
- [ ] allowed-tools specifies correct skill or agent
- [ ] argument-hint provides helpful format guidance
- [ ] Objective clearly states purpose and uses $ARGUMENTS
- [ ] Process has 5-7 clear, actionable steps
- [ ] Success Criteria are specific and measurable
- [ ] Follows semantic category pattern (Verbs/Personas/Objects/Execution)
- [ ] No technical jargon in description
- [ ] Purpose is immediately clear

## When NOT to Use This Structure

Use a simpler structure for:

**Direct Agent Delegation (No Workflow):**
```markdown
---
description: Delegate to specialized persona for isolated context.
argument-hint: [persona] [task description]
---

Task the appropriate agent based on the specified persona: $1 with: $2
```

**Simple Skill Invocation:**
```markdown
---
description: Apply strategic thinking frameworks to decision-making.
argument-hint: [situation or decision]
---

Invoke the `thinking-frameworks` skill to analyze: $ARGUMENTS
```

**Direct Implementations:**
```markdown
---
description: Create new project plans.
argument-hint: [project description]
---

Create a project plan for: $ARGUMENTS
```

**Choose the appropriate structure based on complexity:**
- **Workflow commands** → Full structure (Objective, Process, Success Criteria)
- **Simple invocations** → Just the instruction line(s)
- **Direct actions** → Minimal frontmatter + single instruction
