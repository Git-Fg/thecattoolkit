# @cat-toolkit/think

**Mental models and thinking frameworks for structured problem analysis and decision-making.**

**License:** MIT

## Purpose

Provides 12 structured thinking frameworks across three categories: Strategic Thinking, Prioritization, and Problem Analysis. No code execution—pure reasoning and decision support.

## Commands

### /think
Interactive framework application with real-time guidance.

```bash
/think "Problem or decision to analyze"
```

**Use for:**
- Quick decision support
- Learning framework methodology
- Simple to medium complexity problems
- Interactive exploration

**Example:**
```bash
/think "Should I switch careers?"

# 1. Select category (Strategic/Prioritization/Problem Analysis)
# 2. Select framework (e.g., First Principles, SWOT)
# 3. Apply step-by-step
# 4. Generate ANALYSIS.md
```

### /brainstorm
Comprehensive delegated analysis with deep exploration.

```bash
/brainstorm "Complex problem or strategic decision"
```

**Use for:**
- Complex, multi-faceted problems
- Strategic planning
- Multiple stakeholders involved
- Production decisions requiring documentation

**Example:**
```bash
/brainstorm "Should our startup pivot to AI?"

# Delegates to brainstormer agent
# Generates thorough ANALYSIS.md with:
# - Multiple framework applications
# - Risk assessment
# - Strategic recommendations
```

## Frameworks

### Strategic Thinking
- **First Principles** - Build from fundamental truths
- **Second-Order Thinking** - Consider long-term consequences
- **SWOT Analysis** - Strengths, Weaknesses, Opportunities, Threats
- **10-10-10 Rule** - Evaluate across 10 min, 10 months, 10 years

### Prioritization
- **Pareto Principle (80/20)** - Identify vital few drivers
- **Eisenhower Matrix** - Categorize by urgency/importance
- **One-Thing Method** - Find the one thing that enables others
- **Opportunity Cost** - Consider trade-offs

### Problem Analysis
- **5 Whys** - Root cause analysis
- **Occam's Razor** - Start with simplest explanation
- **Inversion** - Approach backwards (avoid stupidity)
- **Root Cause Analysis** - Systematic problem solving

## Agent

### brainstormer
Deep thinking agent for comprehensive analysis in isolated context.

**Pattern:** Sovereign Triangle (delegated)

**Capabilities:**
- Applies thinking frameworks to complex problems
- Performs thorough research and analysis
- Generates comprehensive documentation
- Explores multiple perspectives

## Decision Guide: /think vs /brainstorm

| Use /think when... | Use /brainstorm when... |
|:-------------------|:------------------------|
| Need immediate guidance | Problem is multi-faceted |
| Simple/focused problem | Comprehensive context needed |
| Want to see thinking process | Deep research required |
| Quick insights valued | Multiple frameworks needed |
| Interactive selection beneficial | Strategic planning with docs |

## Integration

- **With @cat-toolkit/planner** - Apply strategic thinking to project planning
- **With @cat-toolkit/engineer** - Guide architectural decisions with frameworks
- **With @cat-toolkit/prompter** - Combine structured thinking with prompt engineering
