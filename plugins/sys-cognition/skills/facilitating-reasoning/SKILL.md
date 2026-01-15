---
name: facilitating-reasoning
description: "Clarifies goals and applies structured thinking frameworks (Pareto, Inversion, First-Principles) to complex problems. Use when exploring constraints, analyzing decisions, or applying structured reasoning to uncover hidden assumptions."
allowed-tools: [Read, Skill(applying-reasoning), AskUserQuestion]
---

# Reasoning Facilitation Protocol



## Process

### Phase 1: Context Check
Read `.cattoolkit/context/scratchpad.md` if exists to understand current session context.

### Phase 2: Analyze Input
Parse user's problem statement to identify:
- Ambiguities in requirements
- Hidden assumptions
- Missing constraints
- Decision points

### Phase 3: Select Frameworks
Choose the most relevant frameworks from `applying-reasoning` skill:
- **Pareto Principle**
- **Inversion**
- **First-Principles**
- **Systems Thinking**

### Phase 4: Targeted Questions
Ask actionable questions based on selected frameworks to help users uncover:
- Specific constraints not initially mentioned
- Dependencies and relationships
- Risk factors and edge cases
- Success criteria and metrics

## Success Criteria

- User provides specific constraints they hadn't mentioned before
- Problem narrowed down to actionable scope
- Session context preserved in scratchpad
- Clear path forward identified

## References

- `applying-reasoning` - Framework selection and application

