# Framework Selection Guide

This document provides the standardized framework selection process for both Sovereign Direct (foreground) and Sovereign Delegated (delegation) patterns.

## Selection Workflow

### Step 1: Category Selection

Present to user:

```
Framework Category Selection

Which category best fits your analysis needs?

A) Strategic Thinking
   → Long-term perspective, big-picture analysis, foundational decisions
   → Use for: evaluating directions, understanding impacts, challenging assumptions
   → Best when: Making foundational choices with long-term consequences

B) Prioritization & Focus
   → Identifying high-impact activities and resource allocation
   → Use for: overwhelming tasks, priority clarification, focus struggles
   → Best when: Too many options, need to identify what matters most

C) Problem Analysis
   → Root cause analysis, simplification, optimal decision-making
   → Use for: troubleshooting, debugging, understanding why things happen
   → Best when: Something isn't working, need to understand why

Enter your choice (A/B/C):
```

**Implementation:** Use `AskUserQuestion` to get category selection.

### Step 2: Framework-Specific Selection

#### If A) Strategic Thinking Selected:

```
Strategic Framework Selection

Which specific framework?

1) First-Principles
   → Break down to fundamentals and rebuild from base truths
   → Use when: challenging assumptions, avoiding reasoning by analogy
   → Best for: Complex problems needing fundamental rethinking

2) Inversion
   → Solve problems backwards - identify what would guarantee failure
   → Use when: identifying failure points, building robust systems
   → Best for: Risk assessment, avoiding known pitfalls

3) Second-Order Thinking
   → Think through consequences of consequences
   → Use when: understanding ripple effects, evaluating long-term impacts
   → Best for: Decisions with cascading effects

4) SWOT Analysis
   → Map strengths, weaknesses, opportunities, threats
   → Use when: strategic positioning, comprehensive situation analysis
   → Best for: Strategic planning, competitive analysis

5) 10-10-10 Framework
   → Evaluate across three time horizons (10 min, 10 months, 10 years)
   → Use when: overcoming present bias, clarifying long-term impact
   → Best for: Important decisions with time implications

Enter choice (1-5):
```

#### If B) Prioritization Selected:

```
Prioritization Framework Selection

Which specific framework?

1) Pareto Principle (80/20)
   → Identify vital few factors that drive majority of results
   → Use when: overwhelmed, need to cut through noise
   → Best for: Finding the highest-impact activities

2) One-Thing Method
   → Find single highest-leverage action
   → Use when: identifying domino actions, finding leverage points
   → Best for: Complex problems with one key solution

3) Eisenhower Matrix
   → Categorize by urgency vs importance
   → Use when: task triage, managing overwhelm, sprint planning
   → Best for: Organizing many competing priorities

Enter choice (1-3):
```

#### If C) Problem Analysis Selected:

```
Problem Analysis Framework Selection

Which specific framework?

1) 5-Whys
   → Drill to root cause by asking "why" repeatedly
   → Use when: troubleshooting recurring problems, root cause analysis
   → Best for: Debugging, solving persistent issues

2) Opportunity-Cost Analysis
   → Analyze trade-offs and what you give up by choosing an option
   → Use when: making constrained choices, evaluating alternatives
   → Best for: Resource allocation, trade-off decisions

3) Occam's Razor
   → Find simplest explanation that fits all facts
   → Use when: evaluating competing explanations, simplifying complexity
   → Best for: Cutting through complexity to find truth

4) Via Negativa
   → Improve by removing rather than adding
   → Use when: simplifying complexity, reducing bloat, improving systems
   → Best for: Optimization, simplification, decluttering

Enter choice (1-4):
```

**Implementation:** Use `AskUserQuestion` to get specific framework selection.

## Selection Mapping

### Category A: Strategic Thinking
- Choice 1 → `first-principles`
- Choice 2 → `inversion`
- Choice 3 → `second-order`
- Choice 4 → `swot`
- Choice 5 → `10-10-10`

### Category B: Prioritization & Focus
- Choice 1 → `pareto`
- Choice 2 → `one-thing`
- Choice 3 → `eisenhower-matrix`

### Category C: Problem Analysis
- Choice 1 → `5-whys`
- Choice 2 → `opportunity-cost`
- Choice 3 → `occams-razor`
- Choice 4 → `via-negativa`

## Usage in Commands

### For Sovereign Direct (think.md):
1. Present category options
2. Get category selection via AskUserQuestion
3. Present framework-specific options
4. Get framework selection via AskUserQuestion
5. Reference the framework from skill resources
6. Apply using Direct pattern (direct execution with user)

### For Sovereign Delegated (brainstorm.md):
1. Present category options
2. Get category selection via AskUserQuestion
3. Present framework-specific options
4. Get framework selection via AskUserQuestion
5. Gather comprehensive context
6. Delegate to strategist agent with framework selection
7. Reference the framework from skill resources in delegation

## Error Handling

**No Framework Selected:**
- Re-present options with clearer descriptions
- Ask user to explain their goal
- Provide concrete examples

**Unknown Category:**
- Default to Problem Analysis (most common use case)
- Note assumption in output

**Framework Not Found:**
- Read all reference files from thinking-frameworks skill
- Select closest matching framework
- Apply with best interpretation
- Note selection rationale in analysis
