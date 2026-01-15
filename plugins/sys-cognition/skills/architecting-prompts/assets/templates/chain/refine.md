# Refine Step Template

Use this template for the **refinement phase** of a prompt chain workflow.

## Step Purpose

Review execution results and improve the output quality.

---

## Template

```markdown
---
chain-position: 4
chain-name: {{CHAIN_NAME}}
step-type: refine
depends-on: [step-3-execute]
outputs-to: final-output
---

# Refine: {{TOPIC}}

# Context
## Execution Results
{{EXECUTE_OUTPUT}}

## Original Success Criteria
{{SUCCESS_CRITERIA}}

<workflow>
## Phase 1: Review
1. Compare output against success criteria
2. Identify quality issues or gaps
3. Gather improvement suggestions

## Phase 2: Improve
1. Address identified issues
2. Enhance clarity and completeness
3. Optimize for target audience

## Phase 3: Finalize
1. Perform final quality check
2. Format for delivery
3. Document lessons learned
</workflow>

<output_format>
## Refined Output

### Final Deliverable
{{REFINED_CONTENT}}

### Improvements Made
- {{IMPROVEMENT_1}}
- {{IMPROVEMENT_2}}

### Quality Assessment
| Criterion | Status | Notes |
|:----------|:-------|:------|
| {{CRITERION_1}} |  Met | {{NOTES}} |
| {{CRITERION_2}} |  Met | {{NOTES}} |

### Lessons Learned
{{LESSONS_FOR_FUTURE}}
</output_format>
```

---

## Usage Notes

- This step reviews and improves the execution output
- Focus on quality improvement, not starting over
- Document improvements for transparency
- Capture lessons for future chain executions
