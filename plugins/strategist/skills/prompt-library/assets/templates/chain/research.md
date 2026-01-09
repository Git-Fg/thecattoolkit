# Research Step Template

Use this template for the **research phase** of a prompt chain workflow.

## Step Purpose

Gather information, analyze requirements, and identify key factors before planning.

---

## Template

```markdown
---
chain-position: 1
chain-name: {{CHAIN_NAME}}
step-type: research
depends-on: []
outputs-to: step-2-plan
---

# Research: {{TOPIC}}

<context>
{{BACKGROUND_CONTEXT}}
</context>

<workflow>
## Phase 1: Initial Discovery
1. Identify key concepts and terminology
2. Search for authoritative sources
3. Gather initial findings

## Phase 2: Deep Investigation
1. Investigate specific aspects in detail
2. Cross-reference sources
3. Verify claims and collect examples

## Phase 3: Synthesis
1. Analyze patterns and insights
2. Identify gaps or contradictions
3. Summarize key findings
</workflow>

<output_format>
## Research Findings

### Key Discoveries
- {{DISCOVERY_1}}
- {{DISCOVERY_2}}

### Knowledge Gaps
- {{GAP_1}}

### Sources
- {{SOURCE_1}}

### Recommendations for Planning
{{PLANNING_RECOMMENDATIONS}}
</output_format>
```

---

## Usage Notes

- This step produces findings that feed into the Plan step
- Focus on gathering facts, not making decisions
- Document sources for traceability
- Identify gaps that need addressing in later steps
