# Execute Step Template

Use this template for the **execution phase** of a prompt chain workflow.

## Step Purpose

Perform the actual work based on the implementation plan.

---

## Template

```markdown
---
chain-position: 3
chain-name: {{CHAIN_NAME}}
step-type: execute
depends-on: [step-2-plan]
outputs-to: step-4-refine
---

# Execute: {{TOPIC}}

# Context
## Implementation Plan
{{PLAN_OUTPUT}}

<workflow>
## Phase 1: Setup
1. Verify prerequisites are met
2. Prepare necessary resources
3. Confirm execution approach

## Phase 2: Execute
1. Perform planned steps sequentially
2. Document progress and decisions
3. Handle issues as they arise

## Phase 3: Verify
1. Check deliverables against success criteria
2. Validate output quality
3. Document completion status
</workflow>

<output_format>
## Execution Results

### Completed Deliverables
- {{DELIVERABLE_1}}
- {{DELIVERABLE_2}}

### Execution Log
| Step | Status | Notes |
|:-----|:-------|:------|
| {{STEP_1}} |  Complete | {{NOTES}} |
| {{STEP_2}} |  Complete | {{NOTES}} |

### Issues Encountered
{{ISSUES_OR_NONE}}

### Output Artifacts
- {{ARTIFACT_PATH_1}}
- {{ARTIFACT_PATH_2}}
</output_format>
```

---

## Usage Notes

- This step receives the plan and produces actual work output
- Document all significant decisions made during execution
- Flag issues for the Refine step to address
- Be thorough in deliverable documentation
