# Metadata & Documentation Guidelines

Standardized metadata for prompt artifacts to ensure searchability and context preservation.

## YAML Frontmatter (Optional)
For standardized prompts, use a minimal YAML frontmatter for metadata:

```yaml
---
type: [single|chain|meta]
version: 1.0.0
objective: "Brief description of goal"
tags: [tag1, tag2]
---
```

## Prompt Chain: SUMMARY.md
Every chain MUST have a `SUMMARY.md` in its root folder.

### Required Sections:
- **Title**: `# Chain: {Topic Name}`
- **Objective**: Detailed goal of the entire workflow.
- **Workflow Map**:
    - Step 1: Research (complete/pending)
    - Step 2: Planning (complete/pending)
    - etc.
- **Final Output**: Description of the combined deliverable.
- **Success Criteria**: How to know the chain succeeded.

## Directory Numbering
Follow the 01-based numbering for chains and (optionally) for single prompts:
- `.cattoolkit/chains/01-competitive-analysis/`
- `.cattoolkit/prompts/01-code-review.md`

## Output Staging
All intermediate results in a chain must be saved to the `outputs/` subfolder using meaningful names:
- `outputs/01-research-findings.md`
- `outputs/02-implementation-plan.md`

## Reference Naming
When referencing other files in a chain, use the relative path or @ symbol if the tool supports it:
`@outputs/01-research-findings.md`
