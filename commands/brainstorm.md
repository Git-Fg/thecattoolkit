---
name: brainstorm
description: Apply strategic thinking frameworks for decision-making, prioritization, and problem analysis
argument-hint: [framework name or skill name, optional]
allowed-tools: Skill(strategic-thinking), Skill(prioritization), Skill(problem-analysis), Task
---

## Objective

Apply strategic thinking frameworks to help with decision-making, prioritization, and problem analysis.

## Available Frameworks

Strategic Thinking (5 frameworks):
- first-principles, inversion, second-order, swot, 10-10-10

Prioritization (3 frameworks):
- pareto, one-thing, eisenhower-matrix

Problem Analysis (4 frameworks):
- 5-whys, opportunity-cost, occams-razor, via-negativa

## Process

Invoke the @brainstormer subagent with input: $ARGUMENTS

The subagent will:
1. Analyze the input for specific framework names or skill keywords
2. Route to the appropriate framework(s)
3. Apply the framework(s) and provide actionable recommendations

## Examples

`/brainstorm` - Auto-detect best framework
`/brainstorm pareto` - Apply specific framework
`/brainstorm strategic` - Apply all strategic-thinking frameworks
`/brainstorm Should I switch careers?` - Auto-detect and apply
