---
name: thinking-frameworks
description: "Applies structured mental models to solve complex problems. Use when solving architectural decisions, root cause analysis, or strategic planning."
allowed-tools: [Read, Write, Edit, Glob]
---

# Reasoning Engine Protocol

## Core Principle
Apply specific **Mental Models** to transform context into structured insights. This protocol provides systematic frameworks for solving complex problems through proven reasoning patterns.

## Library of Models
(See `references/` for detailed definitions)

| Model | Use Case |
|:---|:---|
| **First Principles** | Building from scratch; verifying assumptions. |
| **Inversion** | Debugging; identifying failure modes ("How to break this?"). |
| **Pareto (80/20)** | Prioritization; finding high-leverage tasks. |
| **Second Order** | Architectural changes; predicting side effects. |
| **5 Whys** | Root cause analysis. |

## Standard Combinations
- **The Hardening (First Principles + Inversion):** Use for critical security or reliability code.
- **The Efficiency (Pareto + Via Negativa):** Use for refactoring and cleanup.
- **The Diagnostic (5 Whys + Occam's Razor):** Use for debugging.

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
