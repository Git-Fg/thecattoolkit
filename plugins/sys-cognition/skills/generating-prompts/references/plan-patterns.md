# Plan Patterns

Prompt patterns for creating approaches and strategies.

## Template

```markdown
# Plan: {Topic}

## Objective
Create implementation plan for {topic}

## Context
Research: @.prompts/{num}-{topic}-research/{topic}-research.md

## Planning Requirements
{What to address}
{Constraints}
{Success criteria}

## Output
Save to: .prompts/{num}-{topic}-plan/{topic}-plan.md

Structure plan:

### Summary
{One paragraph overview}

### Approach
{Selected strategy with rationale}

### Phases
1. **Phase {n}: {Name}**
   - Objective: {What accomplished}
   - Tasks:
     - [ ] {Task 1}
     - [ ] {Task 2}
   - Deliverables: {What's produced}
   - Dependencies: {Requirements}

2. **Phase {n}: {Name}**
   - Objective: {What accomplished}
   - Tasks:
     - [ ] {Task 1}
     - [ ] {Task 2}
   - Deliverables: {What's produced}
   - Dependencies: {Requirements}

### Success Criteria
- {Criterion 1}
- {Criterion 2}

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| {Risk} | {Response} |

### Metadata
- **Confidence:** {high/medium/low}
- **Dependencies:** {External requirements}
- **Assumptions:** {Context assumed}

### Summary Requirements
Create .prompts/{num}-{topic}-plan/SUMMARY.md:

```markdown
# {Topic} Plan Summary

**{Substantive one-liner describing approach}**

## Phases
1. **{Phase 1}** - {Objective}
2. **{Phase 2}** - {Objective}
3. **{Phase 3}** - {Objective}

## Key Decisions
- {Decision 1}
- {Decision 2}

## Next Step
{Execute Phase 1 / proceed to implementation}
```
```

## Plan Types

### Implementation Roadmap
Breaking down how to build something.

**Example:** Authentication system

```markdown
## Objective
Create roadmap for implementing JWT authentication

## Context
Research complete: @.prompts/001-auth-research/auth-research.md

## Planning Requirements
- Break into testable phases
- Each phase builds on previous
- Include testing at each step
- Consider rollback points

## Phases
1. **Setup Infrastructure**
   - Tasks: Create auth module, define types, set up tests
   - Deliverables: Base structure, test framework
   - Dependencies: None

2. **Implement Core JWT**
   - Tasks: Add token generation/validation, middleware
   - Deliverables: Working JWT flow
   - Dependencies: Phase 1

3. **Add Refresh Logic**
   - Tasks: Implement refresh tokens, rotation
   - Deliverables: Secure session handling
   - Dependencies: Phase 2
```

### Decision Framework
Choosing between options.

**Example:** Database selection

```markdown
## Objective
Create decision framework for database selection

## Context
Research complete: @.prompts/001-database-research/database-research.md

## Planning Requirements
Evaluate: PostgreSQL, MongoDB, DynamoDB
Criteria: Scalability, flexibility, cost, team expertise

## Phases
1. **Define Criteria**
   - Tasks: Weight criteria by importance
   - Deliverables: Scoring framework

2. **Evaluate Options**
   - Tasks: Score each database against criteria
   - Deliverables: Comparison matrix

3. **Make Recommendation**
   - Tasks: Select option, document rationale
   - Deliverables: Decision with justification
```

## Quality Checklist

Before completing plan:
- [ ] Phases are logical and sequential
- [ ] Tasks are specific and actionable
- [ ] Dependencies are clear
- [ ] Success criteria are measurable
- [ ] SUMMARY.md created
