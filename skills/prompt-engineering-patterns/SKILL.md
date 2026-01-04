---
name: prompt-engineering-patterns
description: Create effective prompts for AI-to-AI communication through Web UI. Covers meta-prompts, constraint structuring, example-based learning, chain-of-thought, and skill creation patterns.
---

# Objective

Create effective prompts for AI-to-AI communication through Web UI. Covers meta-prompts, constraint structuring, example-based learning, chain-of-thought, and skill creation patterns.

The key principle is to reduce XML usage in general prompts - use text-based heuristics and markdown structure, reserving XML only for highly structured workflows and configurations.

# Essential Principles

## Concise Is Key

Every token competes with conversation history. Challenge each piece:
- "Does Claude already know this?"
- "Is this explanation necessary?"
- "Does this justify its token cost?"

Default assumption: Claude is already smart. Only add what it doesn't have.

## Control Degrees of Freedom

Match specificity to task fragility:

| Freedom Level | When to Use | Pattern |
|--------------|-------------|---------|
| High | Multiple valid approaches, context-dependent | Text-based heuristics |
| Medium | Preferred pattern exists, some variation OK | Pseudocode with parameters |
| Low | Error-prone operations, consistency critical | Exact scripts with no parameters |

Example: Database migration = low freedom (one safe path). Code review = high freedom (context determines approach).

## XML Usage

Use XML sparingly and only for highly structured content that requires machine parsing.

**XML is appropriate for:**
- Workflow configurations with strict steps and validation
- Agent command definitions with required fields and schemas
- Structured output specifications (e.g., `<output><files>...</files></output>`)
- Router pattern skills with complex conditional logic
- Meta-prompt chains where output feeds into subsequent prompts

**XML is NOT appropriate for:**
- General instructions and guidance
- Role definitions and descriptions
- Workflow explanations and process descriptions
- Most prompt content and prose

**Examples:**

❌ Bad (XML overuse):
```xml
<objective>Implement JWT authentication</objective>
<instructions>
  <step>Create login endpoint</step>
  <step>Add JWT middleware</step>
</instructions>
```

✅ Good (Markdown structure):
```markdown
## Objective

Implement JWT authentication for API endpoints.

## Implementation Steps

1. Create login endpoint at `/api/auth/login`
2. Add JWT middleware to protected routes
3. Implement token verification logic
```

**Rule of thumb**: If you're wrapping text in `<instruction>`, `<guidance>`, `<description>`, or `<requirement>` tags, use Markdown headings instead. XML is for machine-readable structure, not for human-readable prose.

# Quick Start

For quick prompt patterns:

1. Simple task: Direct instruction
   "Summarize this article"

2. Add constraints: "Summarize in 3 bullet points"

3. Add reasoning: "Identify findings, then summarize in 3 bullets"

4. Add examples: Include 2-3 examples showing desired format

See references/ for detailed patterns and templates.

# Patterns Index

## Templates Library

All prompt templates are consolidated in `templates/`:

**Simple Task Patterns:**
- templates/simple-task-patterns.md - Coding, analysis, and research tasks for single prompts

**Meta-Prompt Patterns:**
- templates/do-patterns.md - Execution prompts that produce artifacts (code, docs, designs)
- templates/research-patterns.md - Information gathering with quality controls and verification
- templates/plan-patterns.md - Approaches, roadmaps, and strategies for implementation
- templates/refine-patterns.md - Iteration and improvement of existing outputs

**Usage Guide:**
- Use simple-task-patterns for single, focused prompts (quick execution)
- Use meta-prompt patterns for multi-stage workflows (research → plan → implement)
- Meta-prompt patterns require `.prompts/` directory infrastructure and produce SUMMARY.md

# Reference Index

All in `references/`:

Patterns: prompt-templates.md
Learning: few-shot-learning.md
Reasoning: chain-of-thought.md
Advanced: advanced-techniques.md
Interaction: agent-interaction.md
Optimization: prompt-optimization.md

# Core Capabilities

## Example-Based Learning

- Zero-shot: Direct requests without examples
- One-shot: Single demonstration
- Few-shot: 3-8 examples for complex patterns
- Best practices: Mix class order for classification, start with 6 examples
- Detailed guide: references/few-shot-learning.md

## Chain-of-Thought Reasoning

- Zero-shot CoT with triggers ("Let's think step by step")
- Step-back prompting (principles before specifics)
- Tree-of-Thought (multiple reasoning branches)
- Least-to-Most (break into subproblems)
- Verification and self-consistency
- Detailed guide: references/chain-of-thought.md

## Meta Prompting

- Creating prompts that generate prompts
- Structuring constraints, goals, objectives
- Skill creation patterns
- Pattern: "Generate a prompt that will {task}..."
- Detailed guide: references/advanced-techniques.md

## Agent Interaction

- Working with pre-configured agents (don't redefine roles)
- Task delegation: "As the {agent}, help me {task}"
- Multi-agent workflows (sequential, parallel, iterative)
- Context propagation across agent boundaries
- Detailed guide: references/agent-interaction.md

## Prompt Templates

- Reusable template patterns
- AI-to-AI specific templates
- Code prompting patterns
- JSON schema templates
- Complete library: references/prompt-templates.md

## Optimization

- Systematic refinement workflows
- A/B testing framework
- Documentation (table-based format)
- Failure analysis and fixes
- Detailed guide: references/prompt-optimization.md

# Best Practices

1. Be specific - Vague prompts produce inconsistent results
2. Show, don't tell - Examples beat lengthy descriptions
3. Test extensively - Evaluate on diverse inputs
4. Iterate rapidly - Small changes can have large impacts
5. Version control - Track what works
6. Document intent - Explain why prompts are structured this way

# Common Pitfalls

- Over-engineering: Starting complex before trying simple
- Example mismatch: Examples don't align with target task
- Information overload: Too many examples or instructions
- Ambiguous instructions: Room for multiple interpretations
- Ignoring edge cases: Not testing boundary conditions

# Success Criteria

Evaluate prompts on:
- Accuracy: Correctness and relevance
- Consistency: Reproducible across similar inputs
- Clarity: How well intent is conveyed
- Completeness: Addresses all task aspects
- Efficiency: Achieves goals without complexity
