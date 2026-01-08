# Skill vs Agent Decision Matrix

## Core Distinction

**Skills = Knowledge Bases**
- Contain domain expertise, patterns, and methodologies
- Provide "what" and "how" knowledge
- REFERENCE GUIDES, not actors
- No execution logic or decision-making

**Agents = Logic & Actors**
- Have decision-making and execution logic
- USE skills to get knowledge and patterns
- Perform actions based on skill guidance
- Orchestrate workflows and make choices

## Decision Framework

### Use a SKILL when you need:

✅ **Domain Expertise**
- Best practices for a specific domain
- Proven patterns and methodologies
- Reference documentation
- How-to guides and examples

✅ **Knowledge Transfer**
- Teaching someone a methodology
- Providing structured guidance
- Sharing expertise across teams

✅ **Single-Purpose Focus**
- One specific type of task
- Straightforward workflows
- Clear, well-defined processes

**Example Skills:**
- `manage-skills`: How to create and structure skills
- `engineering`: Debugging, code review, testing patterns
- `thinking-frameworks`: Strategic thinking methodologies

### Use an AGENT when you need:

✅ **Isolated Context**
- Separate conversation context
- Persona-based interactions
- Avoiding context pollution

✅ **Decision Making**
- Choosing between multiple approaches
- Adapting workflows based on context
- Making judgment calls

✅ **Workflow Orchestration**
- Coordinating multiple steps
- Managing state across operations
- Delegating to other agents

✅ **Specialized Persona**
- Distinct personality or perspective
- Role-based interactions
- Context-specific behavior

**Example Agents:**
- `brainstormer`: Isolated thinking space with creative persona
- `plugin-expert`: System maintenance with infrastructure focus
- `prompt-engineer`: Specialized prompt crafting expertise

## Common Scenarios

### Scenario 1: "I need help with debugging"

**❌ Don't create:** `debugging-agent`
**✅ Do use:** `engineering` skill

**Reason:** Debugging is a methodology/pattern that provides knowledge. Use the skill to get the patterns, then apply them in your current context.

### Scenario 2: "I need a separate space to brainstorm ideas"

**✅ Create:** `brainstormer` agent

**Reason:** You need isolated context + persona-based interaction. The brainstorming approach is the skill knowledge, but you need a separate agent to maintain context isolation.

### Scenario 3: "I need to manage plugins"

**✅ Create:** `plugin-expert` agent + `manage-plugins` skill

**Reason:** Complex orchestration requiring:
- Agent: System maintenance decisions and workflow orchestration
- Skill: Plugin management patterns and best practices

### Scenario 4: "I need code review patterns"

**❌ Don't create:** `code-review-agent`
**✅ Do use:** `engineering` skill (code review section)

**Reason:** Code review patterns are knowledge/expertise. Use the skill to get the patterns.

## Integration Patterns

### Pattern 1: Agent Uses Skill

```
Agent: "I need to debug this issue"
  ↓
Agent uses: engineering skill (debugging patterns)
  ↓
Agent applies: patterns to current context
  ↓
Agent executes: actual debugging workflow
```

### Pattern 2: Skill Triggers Agent

```
User: "I need brainstorming help"
  ↓
Skill: thinking-frameworks (provides methodology)
  ↓
User/Agent: Applies methodology in current context
```

### Pattern 3: Agent Delegates to Agent

```
Main Agent: Complex task requiring specialization
  ↓
Delegates to: Specialized Agent (via Task tool)
  ↓
Specialized Agent: Executes with its expertise
  ↓
Returns results to: Main Agent
```

## Anti-Patterns to Avoid

### ❌ Agent Duplicating Skill

**Wrong:**
- Create `debugging-agent` that contains debugging patterns
- Agent has the same knowledge as a skill

**Right:**
- Use `engineering` skill for debugging patterns
- Create agent only if you need isolated context

### ❌ Skill with Execution Logic

**Wrong:**
- Skill says "use the Task tool to delegate"
- Skill makes decisions about workflow routing

**Right:**
- Skill provides patterns and methodologies
- Agent makes decisions and executes

### ❌ Over-Delegation

**Wrong:**
- Delegate every simple task to an agent
- Use agent for straightforward knowledge lookup

**Right:**
- Use skill directly for knowledge
- Create agent only for complex orchestration or context isolation

## Quick Reference

| Need | Use | Example |
|------|-----|---------|
| How to do X | Skill | "How to write conventional commits" → `commit-messages` skill |
| Someone to do X | Agent | "I need brainstorming" → `brainstormer` agent |
| Patterns for X | Skill | "Code review patterns" → `engineering` skill |
| Persona for X | Agent | "Strategic thinking persona" → `brainstormer` agent |
| Orchestrate X | Agent | "Manage entire plugin lifecycle" → `plugin-expert` agent |
| Learn X | Skill | "Learn debugging methodology" → `engineering` skill |

## Summary

**Remember:**
- **Skills = Knowledge** (what/how)
- **Agents = Action** (decision/execution)
- Use skills for expertise and patterns
- Use agents for context isolation and orchestration
- If in doubt, start with a skill
- Only create agent when you have a clear reason for isolated context
