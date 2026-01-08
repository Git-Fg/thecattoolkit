# Subagent Management Guide

## Overview

This guide covers the complete lifecycle of subagent management: creation, modification, evaluation, testing, and maintenance.

## Skill vs Agent Decision Matrix

### Core Distinction

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

### Decision Framework

#### Use a SKILL when you need:

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

#### Use an AGENT when you need:

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

## Subagent Creation

### When to Create a Subagent

Use subagents for **isolated context** and **specialized expertise**:

1. **Separate Context Required**: Deep thinking and analysis
2. **System Maintenance**: Maintaining AI infrastructure
3. **Specialized Expertise**: Domain-specific knowledge

### Quick Reference

**Subagent Creation Pattern:**
1. **Default**: Project-level (`.claude/agents/`) for portability
2. Define the subagent:
   - **name**: lowercase-with-hyphens
   - **description**: "[Role]. MUST/PROACTIVELY USE when [trigger condition]"
   - **tools**: Optional comma-separated list
   - **skills**: List relevant skills
3. Write system prompt using normal conversational language
4. Test with real delegation

## Subagent Types

### Simple Agent (Default)

**Structure:**
```yaml
---
name: simple-agent
description: Brief description with trigger
tools: [optional list]
---

## Role
[Who/what the agent is]

## Constraints
[MUST/NEVER rules]

## Workflow
[Step-by-step process]
```

**Use for:** Straightforward tasks, single-purpose agents

### Specialized Agent

**Structure:**
```yaml
---
name: specialized-agent
description: Domain expertise with trigger
tools: [appropriate tools]
skills: [related skills]
---

## Role
[Specialized identity]

## Focus Areas
[What to prioritize]

## Constraints
[Boundaries]

## Workflow
[Approach]

## Success Criteria
[Completion markers]
```

**Use for:** Domain expertise, focused knowledge areas

### Coordinator Agent

**Structure:**
```yaml
---
name: coordinator-agent
description: Orchestration role
tools: Task, [others]
skills: [skills to delegate to]
---

## Role
[Orchestrator identity]

## Capabilities
[What it can coordinate]

## Workflow
[How to orchestrate]

## Delegation Patterns
[How to use Task tool]
```

**Use for:** Multi-step orchestration, coordinates multiple subagents/subtasks

### Research Agent

**Structure:**
```yaml
---
name: research-agent
description: Research and analysis
tools: Read, Grep, WebSearch, WebFetch
---

## Role
[Researcher identity]

## Methodology
[Systematic approach]

## Focus Areas
[What to research]

## Validation
[How to verify findings]
```

**Use for:** Research, analysis, and verification with systematic methodology

### Explorer Agent

**Structure:**
```yaml
---
name: explorer-agent
description: Safe code exploration
tools: Read, Grep, Glob
model: haiku
---

## Role
[Explorer identity]

## Capabilities
[Safe exploration only]

## Constraints
[Read-only safety]

## Workflow
[How to explore]
```

**Use for:** Read-only code exploration, safe for background execution

## Management Operations

### Creating New Subagents

**Process:**
1. Identify valid use case for isolated context
2. Define clear subagent persona
3. Use conversational language
4. List relevant skills in YAML
5. Use appropriate template
6. Test with real delegation

### Modifying Existing Subagents

**Process:**
1. Update subagent personas or descriptions
2. Modify tool access or skill references
3. Refine workflow steps or constraints
4. Add new capabilities or refine existing ones
5. Edit subagent file directly
6. Validate against standards

### Auditing Subagents

**Evaluate:**
- YAML frontmatter quality (name, description, tools, skills)
- Role definition clarity and specialization
- Workflow specification presence and clarity
- Constraints definition with strong boundaries
- Contextual judgment based on complexity

## Context Management

### Memory Architecture

**Short-Term Memory (STM):**
- Current task context
- Recent tool invocations
- Immediate results

**Long-Term Memory (LTM):**
- Persistent knowledge
- Agent role and identity
- General expertise

**Working Memory:**
- Active task state
- Current decision point
- Temporary calculations

### Context Strategies

**Summarization:**
- Compress long contexts
- Keep essential information
- Discard temporary data

**Sliding Window:**
- Maintain recent context
- Drop older information
- Focus on current task

**Scratchpads:**
- External memory store
- Persist important data
- Reference when needed

### Context Reset

**When to Reset:**
- Starting new task
- Switching domains
- Context becomes too large
- Performance degrades

**Reset Protocol:**
1. Save essential context to scratchpad
2. Clear working memory
3. Load new task context
4. Resume with fresh perspective

## Error Handling

### Common Failure Modes

**Hallucinations:**
- Making up information
- Incorrect assumptions
- False confidence

**Format Errors:**
- Not following instructions
- Incorrect output structure
- Missing sections

**Tool Misuse:**
- Using tools incorrectly
- Wrong tool for task
- Permission errors

### Recovery Strategies

**Graceful Degradation:**
- Continue with partial information
- Use alternative approaches
- Provide best-effort results

**Retry Patterns:**
- One retry with different strategy
- Exponential backoff
- Circuit breaker for repeated failures

**Circuit Breaker:**
- Detect repeated failures
- Temporarily disable agent
- Provide fallback behavior

### Structured Communication

**Error Reports:**
```markdown
## Error Encountered
[What went wrong]

## Root Cause
[Why it happened]

## Recovery Attempted
[What was tried]

## Result
[What happened]

## Recommendation
[What to do next]
```

## Debugging and Troubleshooting

### Logging and Tracing

**Correlation IDs:**
- Track requests across systems
- Link related operations
- Trace execution flow

**Structured Logs:**
- Timestamp all events
- Categorize log levels
- Include context

### Diagnostic Procedures

**1. Reproduction:**
- Document exact conditions
- Identify trigger
- Reproduce consistently

**2. Isolation:**
- Test individual components
- Check permissions
- Verify context

**3. Resolution:**
- Apply targeted fix
- Test resolution
- Document changes

### Continuous Monitoring

**Metrics to Track:**
- Success/failure rate
- Average execution time
- Error types and frequency
- User satisfaction

**Alerting:**
- High error rates
- Performance degradation
- Unusual patterns

## Evaluation and Testing

### Evaluation Metrics

**Task Completion:**
- Did agent complete the task?
- Quality of completion
- Adherence to instructions

**Tool Correctness:**
- Used right tools for task
- Tool usage efficiency
- Permission compliance

**Robustness:**
- Handles edge cases
- Recovers from errors
- Maintains performance

### Testing Strategies

**Offline Testing:**
- Test without external dependencies
- Simulate scenarios
- Validate logic

**Simulation:**
- Mock external services
- Create test fixtures
- Verify behavior

**Online Monitoring:**
- Real-world testing
- Production observation
- User feedback

### Evaluation-Driven Development

**Process:**
1. Define success metrics
2. Create evaluation tests
3. Implement agent
4. Run evaluations
5. Iterate and improve

**G-Eval for Custom Criteria:**
- Custom evaluation prompts
- Domain-specific metrics
- Specialized assessment

## Integration Patterns

### Agent Uses Skill

```
Agent: "I need to debug this issue"
  ↓
Agent uses: engineering skill (debugging patterns)
  ↓
Agent applies: patterns to current context
  ↓
Agent executes: actual debugging workflow
```

### Skill Triggers Agent

```
User: "I need brainstorming help"
  ↓
Skill: thinking-frameworks (provides methodology)
  ↓
User/Agent: Applies methodology in current context
```

### Agent Delegates to Agent

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

## Best Practices

### Design Principles

**Clear Boundaries:**
- Define scope explicitly
- Set constraints
- Prevent scope creep

**Focused Expertise:**
- Specialize in specific domain
- Avoid generic roles
- Build on strengths

**Autonomous Operation:**
- Minimize user interaction
- Make reasonable assumptions
- Provide complete results

### Maintenance

**Regular Reviews:**
- Check performance metrics
- Update based on usage
- Refine based on feedback

**Version Control:**
- Track changes
- Document decisions
- Enable rollback

**Documentation:**
- Keep prompts current
- Update examples
- Share learnings

## Success Criteria

A well-configured subagent has:

- Valid YAML frontmatter (name matches file, description includes triggers)
- Clear role definition in system prompt
- Appropriate tool restrictions (least privilege)
- Well-structured system prompt with role, approach, and constraints
- Description field optimized for automatic routing
- Successfully tested on representative tasks
- Model selection appropriate for task complexity
