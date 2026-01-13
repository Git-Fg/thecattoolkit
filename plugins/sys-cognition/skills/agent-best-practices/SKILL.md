---
name: agent-best-practices
description: "Provides comprehensive best practices for building effective AI agents based on Cursor's Universal Agentic Runtime principles. Use when developing agent systems, designing agent workflows, or optimizing agent performance. Do not use for skill development, command creation, or plugin configuration."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Agent Best Practices: Universal Agentic Runtime

## Quick Reference

**Agent Harness Components:**
1. **Instructions**: System prompts, rules, and operational guidelines
2. **Tools**: File editing, search, terminal execution, and external APIs
3. **User Messages**: Directives and context from human operators

**Core Principle**: Plan-First Approach - Research shows experienced developers who plan before coding achieve significantly better results.

## The Plan Mode Workflow

### Step 1: Research
- Analyze the codebase structure
- Identify existing patterns and conventions
- Understand the problem domain thoroughly
- Gather relevant context through powerful search

### Step 2: Clarify
- Ask targeted questions to fill knowledge gaps
- Confirm assumptions about requirements
- Validate understanding of edge cases
- Document unclear requirements

### Step 3: Plan Creation
- Create detailed implementation plans in Markdown
- Break down complex tasks into manageable steps
- Define success criteria and verification methods
- Identify potential risks and mitigation strategies

### Step 4: Approval
- Present the plan for review
- Wait for explicit approval before proceeding
- Refine based on feedback
- Document decisions for future reference

### Step 5: Implementation
- Execute the plan systematically
- Follow established patterns and conventions
- Validate at each milestone
- Iterate based on feedback

## Context Management Strategy

### Effective Context Discovery
- Let agents find context through search tools rather than manual tagging
- Use powerful search capabilities to identify relevant files
- Keep prompts simple and focused
- Include exact file paths when known, otherwise let agents discover

### Prompt Specificity Guidelines
- Write specific prompts with concrete goals
- Compare: "add tests for auth.ts" vs "Write a test case for auth.ts covering the logout edge case, using patterns in `__tests__/` and avoiding mocks"
- Provide verifiable goals through tests, typed languages, and linters
- Set clear targets for iteration

## Component Architecture: Rules vs Skills

### Rules (Static Context)
- Location: `.cursor/rules/` folders
- Format: `RULE.md` files
- Purpose: Always-on instructions and guidelines
- Use when: Consistent patterns that apply across all interactions

### Skills (Dynamic Capabilities)
- Location: `SKILL.md` files
- Purpose: Specialized workflows and domain expertise
- Use when: Specific capabilities for particular tasks
- Advantage: Can be discovered and invoked contextually

## Best Practices for Interaction

### Conversation Management
Start new conversations when:
- Moving to different logical tasks
- Agent appears confused or stuck
- After completing one logical unit of work
- Context becomes too large (>50 messages)

### Rule Optimization
- Avoid copying entire style guides into rules
- Don't document every single command
- Keep rules focused on essentials
- Reference files rather than copying contents
- Treat rules as living documents that evolve

### Code Review Integration
Multiple review strategies:
1. **Watch During Generation**: Real-time observation and course correction
2. **Dedicated Review Passes**: Post-completion comprehensive review
3. **Automated Review Tools**: PR-level automated checks
4. **Parallel Execution**: Run multiple agents and compare results

## Advanced Context Management Techniques

### TodoWrite Attention Manipulation (Recitation Pattern)

The **recitation technique** prevents "lost-in-the-middle" issues by constantly rewriting todos to push objectives into recent attention:

**Implementation:**
1. Create `todo.md` at task start with clear objectives
2. Update after every major tool call (check off completed, add new)
3. Rewrite to keep global plan visible in model's recent attention

**Why It Works:**
- Typical complex task requires ~50 tool calls (long context loops)
- LLMs drift off-topic or forget goals in extended conversations
- **Constant todo rewriting recites objectives into context end**
- Pushes global plan into recent attention span without architectural changes

**Example Pattern:**
```markdown
# Continuous todo updates maintain objective visibility
## Phase 1: Research
- [x] Analyze codebase structure
- [ ] Identify authentication patterns
- [ ] Review existing tests

## Phase 2: Implementation
- [ ] Add edge case handling
- [ ] Update documentation
```

### System Reminders for Context Anchoring

System reminders combat context degradation through **recurring objective injection**:

**Effective Patterns:**
1. **Objective recitation** - Reiterate main goal at critical checkpoints
2. **Constraint reinforcement** - Re-emphasize critical requirements
3. **Context anchoring** - Reference key context elements

**Usage:**
- Add reminders in user messages
- Inject at runtime via tool results
- Include in code execution scripts

### Context Window Thresholds & Actions

| Utilization | Action | Technique |
|:------------|:-------|:----------|
| **<60%** | Monitor | No action needed |
| **60-80%** | Light compression | Observation masking |
| **80-95%** | Aggressive compression | Summarization + compaction |
| **>95%** | Emergency | Force session handoff |

### Plan Mode Integration

**When to Use:**
- Complex tasks requiring 10+ tool calls
- Multi-phase implementations
- When agent appears confused or drifting
- Long-running workflows

**Best Practices:**
- Create plan at task start
- Update as understanding evolves
- Reference plan in reminders
- Use as context anchor during compaction
- Store in `.cattoolkit/context/plan.md`

## Advanced Techniques

### Parallel Agent Execution
- Use git worktrees for isolation
- Run multiple agents simultaneously on the same problem
- Compare and select the best results
- Leverage diversity of approaches

### Hypothesis-Driven Debugging
For complex bugs:
1. Formulate hypotheses about root causes
2. Add instrumentation for data collection
3. Gather runtime evidence
4. Make evidence-based fixes
5. Verify through testing

### Workflow Development Principles
- Start simple and add complexity incrementally
- Add rules only when patterns emerge
- Iterate on setup based on actual usage
- Treat agents as capable collaborators, not simple tools

## Detailed Reference

**For comprehensive guidelines, see:**
- [Core Principles](references/core-principles.md) - Fundamental concepts
- [Implementation Patterns](references/implementation-patterns.md) - Detailed patterns
- [Anti-Patterns](references/anti-patterns.md) - What to avoid
- [Workflow Templates](references/workflow-templates.md) - Ready-to-use workflows

**For reusable assets, see:**
- [Agent Planning Template](assets/templates/agent-plan-template.md)
- [Rule Template](assets/templates/rule-template.md)
- [Review Checklist](assets/templates/review-checklist.md)

## Success Criteria

Well-designed agent systems demonstrate:
- Clear planning before implementation
- Specific, goal-oriented prompts
- Effective context management
- Regular conversation management
- Robust review processes
- Continuous iteration and improvement
