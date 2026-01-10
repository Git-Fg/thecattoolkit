---
name: thinking-frameworks
description: |
  USE when a reasoning engine needs structured methodologies for analysis.
  Contains 12 passive frameworks (Strategic, Prioritization, Problem Analysis).
  Keywords: reasoning, frameworks, first principles, analysis, strategy, thinking models
context: fork
agent: strategist
allowed-tools: [Read]
---

# Thinking Frameworks Methodology Library

## AI Selection Rationale (Internal)
- **Use First-Principles + Inversion**: For greenfield projects or "impossible" bugs.
- **Use Pareto + Eisenhower**: For task overwhelm or roadmap prioritization.
- **Use 5-Whys + Occam's Razor**: For recurring system failures or root cause analysis.
- **Use Second-Order + 10-10-10**: For high-stakes architectural or business pivots.

## Framework Methodologies

### 1. First-Principles Thinking
*Method*: Break down complex problems into basic elements and reassemble them from the ground up.
*Application*:
- Identify every assumption you are making.
- Break down the problem into fundamental truths (physics, math, logic).
- Creates new solutions rather than iterating on existing ones.

### 2. Inversion
*Method*: Solve problems backwards; instead of "how do I succeed?", ask "how do I avoid failure?".
*Application*:
- Define the "Worst Case Scenario" in detail.
- Identify the specific actions that would lead to that failure.
- Avoid those actions at all costs.

### 3. Second-Order Thinking
*Method*: Think through the consequences of the consequences.
*Application*:
- Ask "And then what?" for immediate results.
- Look for non-obvious long-term effects (1-3 years out).
- Evaluate if short-term gain leads to long-term pain.

### 4. SWOT Analysis
*Method*: Map Strengths, Weaknesses, Opportunities, and Threats.
*Application*:
- **Internal**: Strengths & Weaknesses (Team, Codebase, Resources).
- **External**: Opportunities & Threats (Market, Competitors, Technology changes).

### 5. 10-10-10 Framework
*Method*: Evaluate decisions across three time horizons.
*Application*:
- How will I feel about this in 10 minutes? (Immediate emotional reaction)
- How will I feel about this in 10 months? (Medium-term consequences)
- How will I feel about this in 10 years? (Long-term legacy/impact)

### 6. Pareto Principle (80/20)
*Method*: Identify the vital few factors that drive the majority of results.
*Application*:
- List all inputs/activities.
- Identify which top 20% generate 80% of the value/bugs/load.
- ruthlessly cut or deprioritize the bottom 80%.

### 7. One-Thing Method
*Method*: Identify the single domino that makes everything else easier or unnecessary.
*Application*:
- Ask: "What is the ONE thing I can do such that by doing it, everything else will be easier or unnecessary?"
- Focus execution solely on that lead domino.

### 8. Eisenhower Matrix
*Method*: Categorize tasks by Urgency vs. Importance.
*Application*:
- Important & Urgent: Do it now.
- Important & Not Urgent: Schedule it (Deep Work).
- Not Important & Urgent: Delegate it.
- Not Important & Not Urgent: Delete it.

### 9. 5-Whys
*Method*: Ask "Why?" five times to drill down to the root cause.
*Application*:
- State the problem.
- Ask "Why did this happen?" -> [Reason 1]
- Ask "Why did [Reason 1] happen?" -> [Reason 2]
- Continue until you reach the system-level root cause (process failing).

### 10. Opportunity-Cost Analysis
*Method*: Evaluate what you are giving up to choose an option.
*Application*:
- Clearly define the "Next Best Alternative".
- Quantify the value of that alternative.
- Ensure the chosen path exceeds the value of what is sacrificed.

### 11. Occam's Razor
*Method*: The simplest explanation is usually the correct one.
*Application*:
- When facing competing hypotheses, choose the one with fewest assumptions.
- Cut unnecessary complexity in code and architecture.

### 12. Via Negativa
*Method*: Improvement by subtraction.
*Application*:
- Instead of adding features to solve a problem, remove the friction/bloat causing it.
- Simplify systems to increase reliability.

## Reference Resources

### Deep Dives
- `references/prioritization.md`: Advanced prioritization techniques
- `references/strategic.md`: Strategic thinking patterns
- `references/problem-analysis.md`: Root cause analysis methods
- `references/framework-applications.md`: Application examples

### Templates
- `assets/templates/analysis-summary.md`: Standard format for analysis outputs
