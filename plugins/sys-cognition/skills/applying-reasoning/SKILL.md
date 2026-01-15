---
name: applying-reasoning
description: "Applies structured mental models to solve complex problems. Use when solving architectural decisions, root cause analysis, or strategic planning."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Reasoning Engine Protocol



## Library of Models
(See `references/` for detailed definitions)

| Model | Use Case |
|:---|:---|
| **First Principles** | Building from scratch; verifying assumptions. |
| **Inversion** | Debugging; identifying failure modes. |
| **Pareto (80/20)** | Prioritization; finding high-leverage tasks. |
| **Second Order** | Architectural changes; predicting side effects. |
| **5 Whys** | Root cause analysis. |

## Standard Combinations
- **The Hardening (First Principles + Inversion):** Use for critical security or reliability code.
- **The Efficiency (Pareto + Via Negativa):** Use for refactoring and cleanup.
- **The Diagnostic (5 Whys + Occam's Razor):** Use for debugging.

## Research Protocol (Core Mandate)
1. **Research**: Use `Grep` and `Bash` to find architectural patterns, performance bottlenecks, or technical debt.
2. **Framework Application**: Apply the `thinking-frameworks` methodology to the evidence found.
3. **Synthesis**: Create an `ANALYSIS.md` report using the template below.

## Constraints
- **Evidence-First**: Never make a claim without a file reference or shell output to support it.
- **Truth-First**: Contradict the user if the codebase evidence suggests their proposed path is flawed.

## Artifact Schema: `ANALYSIS.md`
When a Deep Analysis is requested, produce this artifact:

```markdown
# Strategic Analysis: {Topic}

## Executive Summary
{Concise findings}

## Framework Application
### {Framework Name}
**Insight:** {What did this model reveal?}

## Synthesis & Recommendations
1. {Actionable Item 1}
2. {Actionable Item 2}
```
