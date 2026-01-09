---
name: thinking-frameworks
description: |
  USE when user asks to 'apply a framework', 'think strategically', 'analyze a decision', 'brainstorm', or 'prioritize options'.
  Structured thinking patterns for analysis, decision-making, and prioritization (first-principles, SWOT, Pareto, 5-whys, Eisenhower).
context: fork
agent: brainstormer
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Thinking Frameworks Standard

Provide the theoretical basis and methodology for structured analysis. This skill contains no active execution logic - only passive reference documentation.

## Framework Index

### Strategic Thinking (5 frameworks)
**For long-term perspective, big-picture analysis, and foundational decisions**

- **first-principles**: Challenge assumptions, rebuild from fundamentals (references/strategic.md)
- **inversion**: Identify failure modes to avoid them (references/strategic.md)
- **second-order**: Understand cascading consequences and long-term impacts (references/strategic.md)
- **swot**: Analyze strengths, weaknesses, opportunities, threats (references/strategic.md)
- **10-10-10**: Evaluate across three time horizons (references/strategic.md)

### Prioritization & Focus (3 frameworks)
**For identifying high-impact activities and resource allocation**

- **pareto**: Apply 80/20 rule to identify vital few factors (references/prioritization.md)
- **one-thing**: Find single highest-leverage action (references/prioritization.md)
- **eisenhower-matrix**: Categorize by urgency vs importance (references/prioritization.md)

### Problem Analysis (4 frameworks)
**For root cause analysis, simplification, and optimal decision-making**

- **5-whys**: Drill to root cause by asking "why" repeatedly (references/problem-analysis.md)
- **opportunity-cost**: Analyze trade-offs and what you give up (references/problem-analysis.md)
- **occams-razor**: Find simplest explanation that fits all facts (references/problem-analysis.md)
- **via-negativa**: Improve by removing rather than adding (references/problem-analysis.md)

## Skill Resources

### Selection Process
- **references/framework-selection.md**: Standardized framework selection prompts and workflow for both Vector and Triangle patterns

### Application Methodology
- **references/framework-applications.md**: Detailed step-by-step instructions for applying each framework, with examples and templates

### Individual Framework Details
- **references/strategic.md**: In-depth coverage of strategic thinking frameworks
- **references/prioritization.md**: In-depth coverage of prioritization frameworks
- **references/problem-analysis.md**: In-depth coverage of problem analysis frameworks

### Templates
- **assets/templates/analysis-summary.md**: Standard output template for all framework analyses

## Compliance Rule

**Any agent or command using this skill MUST produce a final output file:**
- Use `assets/templates/analysis-summary.md` as the template
- Write complete analysis to `ANALYSIS.md` (or specified output file)
- Include framework name, category, context, analysis, insights, and recommendations
- Follow the template structure exactly

## Framework Combinations

For complex problems, these combinations are effective:
- first-principles + inversion: Rebuilding while avoiding failure modes
- second-order + 10-10-10: Understanding cascading impacts across time
- pareto + one-thing: Identifying leverage points
- 5-whys + occams-razor: Root cause analysis with simple solutions
- eisenhower-matrix + pareto: Task triage with impact focus

## Usage Patterns

### For Sovereign Vector Commands (Foreground)
1. Reference `references/framework-selection.md` for user interaction prompts
2. Read `references/framework-applications.md` for methodology
3. Apply framework interactively with user guidance
4. Write output following `assets/templates/analysis-summary.md`

### For Sovereign Triangle Commands (Delegation)
1. Reference `references/framework-selection.md` for user interaction prompts
2. Gather comprehensive context
3. Delegate to agent with framework selection
4. Agent reads `references/framework-applications.md` for autonomous execution
5. Agent writes output following `assets/templates/analysis-summary.md`

### For Agents
1. Load skill via `skills: [thinking-frameworks]`
2. Read `references/framework-applications.md` for methodology
3. Apply framework autonomously to provided context
4. Write output following `assets/templates/analysis-summary.md`

