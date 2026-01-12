---
name: thinking-frameworks
description: "Applies 12 structured frameworks including Pareto, Inversion, and First-Principles. Use when performing strategic analysis, root-cause identification, or complex trade-off evaluation."
context: fork
user-invocable: false
agent: reasoner
allowed-tools: [Read, Glob, Grep, Bash]
---

# Thinking Frameworks Library

## Core Purpose
This skill is a **Knowledge Bank** for structured reasoning. Load this skill to gain access to the application methodologies in `references/`.

## Framework Categories
1. **Strategic**: `references/strategic.md` (Inversion, 10-10-10, Second-Order)
2. **Prioritization**: `references/prioritization.md` (Pareto, Eisenhower, One-Thing)
3. **Diagnostic**: `references/problem-analysis.md` (5-Whys, Occam's Razor, Via Negativa)

## Operational Protocol
- **Interactive Mode**: Used by `/think` to ask clarifying questions.
- **Autonomous Mode**: Used by `reasoner` agent to scan codebase and synthesize insights.
