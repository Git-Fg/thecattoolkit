---
name: prompt-engineering-patterns
description: MUST USE when creating prompts for AI agents, structuring constraints, or designing prompt workflows. Secondary: implementing chain-of-thought, using example-based learning, or building meta-prompts.
---

# Path Resolution

This skill can be installed in multiple locations. Before reading any references, locate the skill directory:

```bash
# Search in priority order (project → plugin → user)
SKILL_PATH="$(
  find .claude/skills/prompt-engineering-patterns -maxdepth 0 2>/dev/null && echo "project" ||
  find ~/.claude/skills/prompt-engineering-patterns -maxdepth 0 2>/dev/null && echo "user" ||
  find {plugin_root}/skills/prompt-engineering-patterns -maxdepth 0 2>/dev/null && echo "plugin"
)"

# Use absolute path when reading internal reference files
```

All references to `references/` files must use the discovered absolute path.

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

## Hybrid XML/Markdown Structure

Use the **Hybrid Semantic Structure**: XML for logic containers, Markdown for content.

See: `references/structural-patterns.md` for the complete Container Principle guide.

**When to use XML:**
- `<context>` - Large data dumps
- `<workflow>` - Non-negotiable step sequences
- `<constraints>` - Negative constraints (NEVER/MUST NOT)
- `<output_format>` - Machine-parseable responses

**When to use Markdown:**
- General instructions and guidance
- Explanations and descriptions
- Most prompt content

**Critical:** Limit to 3-5 XML tags maximum. Never nest XML tags (avoids "XML soup").

# Meta-Prompting Structure

Structure meta-prompts (prompts that generate prompts) using XML semantic containers to separate concerns.

## Required Structure

```xml
<system_role>
Define the AI's identity and core purpose
</system_role>

<task_context>
Provide background, constraints, and domain knowledge
</task_context>

<examples>
<example>
Input: [demonstration input]
Output: [demonstration output]
</example>
</examples>

<user_input>
The actual task to perform
</user_input>
```

## Container Definitions

### `<system_role>`
Defines WHO the AI is for this task:
- Core identity and expertise
- Primary responsibilities
- Behavioral guidelines
- What the AI should and should not do

### `<task_context>`
Provides WHAT the AI needs to know:
- Domain background
- Constraints and requirements
- Success criteria
- Relevant patterns or frameworks
- Important considerations

### `<examples>`
Demonstrates HOW to perform the task:
- Use `<example>` tags inside (see few-shot learning guide)
- Show input-output patterns
- Demonstrate edge cases
- Always use XML isolation to prevent example leakage

### `<user_input>`
Contains the actual task:
- The specific request
- Real data to process
- Actual question to answer
- Clear demarcation from examples

## Structure Example

```xml
<system_role>
You are a senior code reviewer specializing in security vulnerabilities.
You identify security issues and provide actionable remediation steps.
</system_role>

<task_context>
Review code for OWASP Top 10 vulnerabilities. Focus on:
- SQL injection
- XSS vulnerabilities
- Authentication flaws
- Insecure direct object references

For each issue found:
1. Severity (Critical/High/Medium/Low)
2. Location (file:line)
3. Vulnerability type
4. Remediation steps
</task_context>

<examples>
<example>
Input: "function getUser(id) { return db.query('SELECT * FROM users WHERE id = ' + id) }"
Output: "CRITICAL: SQL injection vulnerability
Location: auth.js:42
Fix: Use parameterized queries with prepared statements"
</example>
</examples>

<user_input>
Review this code for security issues:
function login(username, password) {
  if (password === storedPassword) {
    return true;
  }
  return false;
}
</user_input>
```

## Benefits

- **Clear separation** between role, context, examples, and task
- **Prevents confusion** between demonstration and instruction
- **Enables modular** prompt construction
- **Improves consistency** across similar tasks
- **Reduces example leakage** through XML isolation

# Quick Start

For quick prompt patterns:

1. Simple task: Direct instruction
   "Summarize this article"

2. Add constraints: "Summarize in 3 bullet points"

3. Add reasoning: "Identify findings, then summarize in 3 bullets"

4. Add examples: Include 2-3 examples showing desired format

See references/ for detailed patterns and templates.

# Reference Index

- `references/structural-patterns.md` - Hybrid XML/Markdown structure and Container Principle
- `references/prompt-templates.md` - Reusable prompt patterns
- `references/few-shot-learning.md` - Example-based learning
- `references/chain-of-thought.md` - Reasoning patterns
- `references/advanced-techniques.md` - Advanced prompting
- `references/agent-interaction.md` - Agent communication
- `references/prompt-optimization.md` - Optimization techniques

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
