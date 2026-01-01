---
name: prompt-engineering-patterns
description: Create effective prompts for AI-to-AI communication through Web UI. Covers meta-prompts, constraint structuring, example-based learning, chain-of-thought, and skill creation patterns.
---

# Prompt Engineering Patterns

Create effective prompts for AI-to-AI communication through Web UI.

## Core Principles

### CONCISE IS KEY

Every token competes with conversation history. Challenge each piece:
- "Does Claude already know this?"
- "Is this explanation necessary?"
- "Does this justify its token cost?"

Default assumption: Claude is already smart. Only add what it doesn't have.

### CONTROL DEGREES OF FREEDOM

Match specificity to task fragility:

| Freedom Level | When to Use | Pattern |
|--------------|-------------|---------|
| **High** | Multiple valid approaches, context-dependent | Text-based heuristics |
| **Medium** | Preferred pattern exists, some variation OK | Pseudocode with parameters |
| **Low** | Error-prone operations, consistency critical | Exact scripts with no parameters |

Example: Database migration = low freedom (one safe path). Code review = high freedom (context determines approach).

## When to Use This Skill

- Creating prompts for other AI agents/assistants
- Designing meta-prompts that generate prompts
- Structuring constraints, goals, objectives
- Building skills for other agents
- Optimizing prompt performance across agent workflows

## Quick Patterns

### Prompt Structure Hierarchy

```
[Task Instruction] → [Examples (optional)] → [Input] → [Output Format]
```

### Role-Defining Prompt Template

Use when setting up assistants or defining recurring behavior:

```
You are a {role} assistant specializing in {domain}.

Task: {task_description}

{examples (optional)}

Input: {user_input}

Output format: {format_specification}
```

### Task-Based Prompt Template

Use when working with pre-configured agents or one-off tasks:

```
{task_instruction}

{examples (optional)}

Input: {user_input}

Output format: {format_specification}
```

### Progressive Disclosure Pattern

Start simple, add complexity only when needed:

**Level 1:** Direct instruction → `"Summarize this article"`

**Level 2:** Add constraints → `"Summarize in 3 bullet points"`

**Level 3:** Add reasoning → `"Identify findings, then summarize in 3 bullets"`

**Level 4:** Add examples → Include 2-3 examples showing desired format

## Core Capabilities

### Example-Based Learning
- **Zero-shot**: Direct requests without examples
- **One-shot**: Single demonstration
- **Few-shot**: 3-8 examples for complex patterns
- **Best practices**: Mix class order for classification, start with 6 examples
- Detailed guide: [references/few-shot-learning.md](references/few-shot-learning.md)

### Chain-of-Thought Reasoning
- Zero-shot CoT with triggers ("Let's think step by step")
- Step-back prompting (principles before specifics)
- Tree-of-Thought (multiple reasoning branches)
- Least-to-Most (break into subproblems)
- Verification and self-consistency
- Detailed guide: [references/chain-of-thought.md](references/chain-of-thought.md)

### Meta-Prompting
- Creating prompts that generate prompts
- Structuring constraints, goals, objectives
- Skill creation patterns
- Pattern: `"Generate a prompt that will {task}..."`
- Detailed guide: [references/advanced-techniques.md](references/advanced-techniques.md)

### Agent Interaction
- Working with pre-configured agents (don't redefine roles)
- Task delegation: `"As the {agent}, help me {task}"`
- Multi-agent workflows (sequential, parallel, iterative)
- Context propagation across agent boundaries
- Detailed guide: [references/agent-interaction.md](references/agent-interaction.md)

### Prompt Templates
- Reusable template patterns
- AI-to-AI specific templates
- Code prompting patterns
- JSON schema templates
- Complete library: [references/prompt-templates.md](references/prompt-templates.md)

### Optimization
- Systematic refinement workflows
- A/B testing framework
- Documentation (table-based format)
- Failure analysis and fixes
- Detailed guide: [references/prompt-optimization.md](references/prompt-optimization.md)

## Common Templates

### Constraint Structuring

```
Task: {task_description}

Constraints:
- Must NOT: {prohibited_actions}
- Must: {required_actions}
- Limit: {specific_limits}
- Format: {output_format}

{task_input}
```

### Goal and Objective Framework

```
You are a {role} assistant.

Primary Objective: {main_target}

Goals:
- {goal_1}
- {goal_2}

Constraints:
- Must: {required}
- Must not: {prohibited}

Output format: {format}

Task: {task}
```

### Meta-Prompt Template

```
Generate a prompt that will {task_description}.

The generated prompt should:
- {requirement_1}
- {requirement_2}
- {requirement_3}

Context: {context}

Generate the prompt:
```

### AI-to-AI Task Delegation

```
As the {receiving_agent_type}, please {task}.

Context:
- Delegating from: {sending_agent_type}
- Task purpose: {why_this_task}
- Dependencies: {what_this_depends_on}
- Output will be used by: {next_agent_or_purpose}

{task_details}
```

### Inter-Agent Workflow

```
This prompt initiates a multi-agent workflow.

Step {N} of {total}: {step_name}

Your role: {agent_role}
Your task: {specific_task}

When complete, provide output in this format:
{structured_output_format}

The next agent will use your output to: {next_step_description}
```

## Best Practices

1. **Be specific** - Vague prompts produce inconsistent results
2. **Show, don't tell** - Examples beat lengthy descriptions
3. **Test extensively** - Evaluate on diverse inputs
4. **Iterate rapidly** - Small changes can have large impacts
5. **Version control** - Track what works
6. **Document intent** - Explain why prompts are structured this way

## Common Pitfalls

- **Over-engineering**: Starting complex before trying simple
- **Example mismatch**: Examples don't align with target task
- **Information overload**: Too many examples or instructions
- **Ambiguous instructions**: Room for multiple interpretations
- **Ignoring edge cases**: Not testing boundary conditions

## Success Criteria

Evaluate prompts on:
- **Accuracy**: Correctness and relevance
- **Consistency**: Reproducible across similar inputs
- **Clarity**: How well intent is conveyed
- **Completeness**: Addresses all task aspects
- **Efficiency**: Achieves goals without complexity
