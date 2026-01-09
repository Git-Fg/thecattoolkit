---
name: deep-analysis
description: |
  USE when user requests 'deep analysis', 'strategic analysis', 'comprehensive problem analysis', or 'systematic exploration of complex issues'.
  Performs autonomous deep discovery using structured thinking frameworks to analyze complex problems comprehensively.
context: fork
agent: strategist
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Deep Analysis Protocol

## Purpose

This skill provides comprehensive strategic analysis capabilities for complex problems. It guides autonomous deep discovery using structured thinking frameworks to generate thorough, actionable insights.

## Execution Framework

### Phase 1: Context Gathering
Analyze the provided problem statement and gather relevant context:
- Identify all stakeholders and their perspectives
- Map the problem scope and boundaries
- Collect available data, constraints, and requirements
- Determine relevant frameworks based on problem type

### Phase 2: Multi-Framework Analysis
Apply multiple thinking frameworks to ensure comprehensive coverage:

**For Strategic Problems:**
- Use **first-principles** to rebuild from fundamentals
- Apply **second-order thinking** to understand cascading effects
- Employ **SWOT analysis** for comprehensive situational assessment
- Consider **inversion** to identify failure modes

**For Prioritization Problems:**
- Apply **Pareto analysis** (80/20 rule) to identify vital few factors
- Use **Eisenhower Matrix** to categorize by urgency and importance
- Employ **one-thing principle** to find highest-leverage action

**For Root Cause Analysis:**
- Apply **5-whys** to drill to root causes
- Use **Occam's Razor** to find simplest explanations
- Consider **opportunity cost** to analyze trade-offs

### Phase 3: Synthesis & Insights
Generate comprehensive analysis:
- Combine insights from multiple frameworks
- Identify patterns and contradictions
- Surface hidden assumptions and biases
- Evaluate confidence levels and uncertainty factors

### Phase 4: Recommendations & Action Planning
Develop actionable recommendations:
- Prioritize recommendations by impact and feasibility
- Consider implementation dependencies and sequencing
- Identify potential risks and mitigation strategies
- Define success metrics and validation criteria

## Output Requirements

### Generate ANALYSIS.md
Create a comprehensive output file following this structure:

```markdown
# Strategic Analysis Report

## Executive Summary
{{CONCISE_PROBLEM_STATEMENT_AND_KEY_FINDINGS}}

## Problem Framing
### Context
{{PROBLEM_CONTEXT_AND_CONSTRAINTS}}

### Stakeholders
{{STAKEHOLDER_ANALYSIS}}

### Success Criteria
{{WHAT_SUCCESS_LOOKS_LIKE}}

## Framework Analysis

### Primary Framework: {{FRAMEWORK_NAME}}
**Rationale:** {{WHY_THIS_FRAMEWORK}}

**Analysis:**
{{DETAILED_ANALYSIS}}

**Key Insights:**
- {{INSIGHT_1}}
- {{INSIGHT_2}}
- {{INSIGHT_3}}

### Secondary Framework: {{FRAMEWORK_NAME}}
**Rationale:** {{WHY_THIS_FRAMEWORK}}

**Analysis:**
{{DETAILED_ANALYSIS}}

**Key Insights:**
- {{INSIGHT_1}}
- {{INSIGHT_2}}
- {{INSIGHT_3}}

### Synthesis
{{COMBINED_INSIGHTS_FROM_ALL_FRAMEWORKS}}

## Recommendations

### Priority 1 (Critical)
1. {{HIGH_IMPACT_ACTION}}
   - **Impact:** {{EXPECTED_OUTCOME}}
   - **Feasibility:** {{IMPLEMENTATION_DIFFICULTY}}
   - **Timeline:** {{ESTIMATED_DURATION}}

### Priority 2 (Important)
2. {{SECONDARY_ACTION}}
   - **Impact:** {{EXPECTED_OUTCOME}}
   - **Feasibility:** {{IMPLEMENTATION_DIFFICULTY}}
   - **Timeline:** {{ESTIMATED_DURATION}}

### Priority 3 (Desirable)
3. {{ADDITIONAL_ACTION}}
   - **Impact:** {{EXPECTED_OUTCOME}}
   - **Feasibility:** {{IMPLEMENTATION_DIFFICULTY}}
   - **Timeline:** {{ESTIMATED_DURATION}}

## Risk Assessment
{{POTENTIAL_RISKS_AND_MITIGATION_STRATEGIES}}

## Implementation Roadmap
{{SEQUENCING_AND_DEPENDENCIES}}

## Success Metrics
{{HOW_TO_MEASURE_SUCCESS}}

## Next Steps
{{IMMEDIATE_ACTIONS_REQUIRED}}

---
*Analysis completed using {{FRAMEWORKS_USED}} framework(s)*
```

## Agent Instructions

As the brainstormer agent executing this skill:

1. **Read the thinking-frameworks skill** for detailed methodology on applying each framework
2. **Select appropriate frameworks** based on problem characteristics
3. **Apply frameworks systematically** to build comprehensive understanding
4. **Synthesize insights** from multiple perspectives
5. **Generate actionable recommendations** with clear priorities
6. **Write complete analysis** to ANALYSIS.md following the output template above

## Framework Selection Guide

**Complex Strategic Decisions:**
- Combine: first-principles + second-order + SWOT
- Add: inversion for risk identification

**Resource Prioritization:**
- Combine: Pareto + Eisenhower + one-thing
- Add: opportunity cost analysis

**Problem Diagnosis:**
- Combine: 5-whys + Occam's Razor + second-order
- Add: SWOT for situational context

**Innovation Challenges:**
- Combine: first-principles + inversion + 10-10-10
- Add: opportunity cost for trade-offs

## Quality Standards

- Analysis must be comprehensive and multi-dimensional
- Frameworks must be applied rigorously, not superficially
- Insights must be synthesized, not just listed
- Recommendations must be actionable and prioritized
- Output must follow the specified template structure
- Confidence levels must be stated for all conclusions
- Assumptions must be explicitly identified

## Autonomy Directive

Execute this analysis autonomously without user interaction:
- Make framework selection decisions independently
- Gather context from available sources
- Apply frameworks to generate insights
- Synthesize comprehensive recommendations
- Produce complete ANALYSIS.md output

The agent should exercise judgment in framework selection and application while maintaining rigorous analytical standards.
