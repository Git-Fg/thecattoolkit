# Sys-Builder Methodology Reference

## Decision Trees

### Task Classification

#### 1. Atomic Tasks (< 5 minutes, single file change)
**Examples:**
- Fix a typo
- Update a configuration value
- Add a simple validation
- Refactor a single function

**Action:** Execute directly using available tools

#### 2. Complex Tasks (> 5 minutes, multiple files, architectural decisions)
**Examples:**
- System refactoring
- Multi-step feature implementation
- Security audit
- Performance optimization

**Action:** Route to Director/Worker pattern

### Routing Logic

#### For Autonomous Execution (Batch Mode)
When user says:
- "implement", "build", "deploy"
- "refactor the entire system"
- "create a new feature from scratch"
- "run end-to-end tests"

**Response Template:**
```
I have analyzed the requirements. This is a complex task requiring systematic execution.

For autonomous execution, please run:
`/sys-builder:run`

This will:
1. Create a detailed PLAN.md
2. Execute all steps autonomously
3. Generate execution reports
```

#### For Interactive Planning (HITL Mode)
When user says:
- "plan the architecture"
- "review my approach"
- "what do you think about"
- "help me design"

**Response Template:**
```
This requires architectural decisions and validation.

For collaborative planning, please run:
`/sys-builder:run-interactive`

This will:
1. Create a detailed PLAN.md
2. Stop for your validation
3. Execute only after approval
```

### Director Responsibilities

The Director agent analyzes context and creates `PLAN.md`:

1. **Understand the goal**
   - Read requirements from user prompt
   - Scan codebase for relevant files
   - Identify dependencies

2. **Create detailed plan**
   - Break into sequential steps
   - Identify prerequisites
   - Define success criteria
   - Estimate complexity

3. **Handle execution mode**
   - **Batch mode**: Make standard assumptions, document in `ASSUMPTIONS.md`
   - **Interactive mode**: Use `AskUserQuestion` to validate plan before proceeding

### Worker Responsibilities

The Worker agent executes `PLAN.md`:

1. **Follow execution protocol**
   - Strict adherence to execution-core standards
   - Quality checks at each step
   - Security validation

2. **Handle blocking scenarios**
   - Create `HANDOFF.md` per protocol
   - Log errors to `ERRORS.md`
   - Continue with next task when possible

3. **Maintain flow**
   - NO questions during execution
   - Make strategic assumptions when blocked
   - Report completion in structured format

## Quality Gates

Before any execution:
- [ ] Requirements understood
- [ ] Success criteria defined
- [ ] Plan created (if complex task)
- [ ] Dependencies identified

During execution:
- [ ] Security checklist applied
- [ ] Tests pass
- [ ] Code review standards met
- [ ] Documentation updated

After execution:
- [ ] All tests passing
- [ ] No lint errors
- [ ] Success criteria met
- [ ] Reports generated
