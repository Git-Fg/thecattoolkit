# Plan Step Template

Use this template for the **planning phase** of a prompt chain workflow.

## Step Purpose

Create a structured plan or strategy based on research findings.

---

## Template

```markdown
---
chain-position: 2
chain-name: {{CHAIN_NAME}}
step-type: plan
depends-on: [step-1-research]
outputs-to: step-3-execute
---

# Plan: {{TOPIC}}

<context>
## Research Findings
{{RESEARCH_OUTPUT}}
</context>

<workflow>
## Phase 1: Analyze Requirements
1. Review research findings
2. Identify constraints and dependencies
3. Define success criteria

## Phase 2: Design Solution
1. Outline approach options
2. Evaluate trade-offs
3. Select optimal strategy

## Phase 3: Create Roadmap
1. Break into actionable steps
2. Estimate effort/complexity
3. Define deliverables
</workflow>

<output_format>
## Implementation Plan

### Objective
{{CLEAR_OBJECTIVE}}

### Approach
{{SELECTED_APPROACH}}

### Steps
1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

### Success Criteria
- {{CRITERION_1}}
- {{CRITERION_2}}

### Risks & Mitigations
| Risk | Mitigation |
|:-----|:-----------|
| {{RISK_1}} | {{MITIGATION_1}} |
</output_format>
```

---

## Usage Notes

- This step receives research output and produces execution plan
- Be specific about deliverables and success criteria
- Consider risks and dependencies
- Output should be actionable by the Execute step
