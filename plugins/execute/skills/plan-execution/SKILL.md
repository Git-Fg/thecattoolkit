---
name: plan-execution
description: |
  Execute a project plan. USE when the user wants to run a phase or execute tasks from PLAN.md.
  Keywords: execute plan, run phase, implement features, build project
context: fork
agent: director
user-invocable: true
allowed-tools: [Task, Read, Write, Bash, Glob, Grep]
---

# Plan Execution

## Instructions

Execute a project plan by delegating to the director agent for autonomous orchestration.

1. **Locate Plan**: Identify the target PLAN.md file from the user's request
2. **Analyze Structure**: Review the plan to understand phases and dependencies
3. **Delegate Execution**: Use the director agent to orchestrate execution in Uninterrupted Flow mode
4. **Monitor Progress**: Track progress and verify task completion

The director agent will:
- Discover project context files (BRIEF.md, PLAN.md, ADR.md)
- Analyze task dependencies for optimal execution
- Coordinate parallel execution where possible
- Verify outputs through read-back protocols
- Update project state files (PLAN.md, ROADMAP.md, SUMMARY.md)

## Delegation

Delegate to the director agent with clear instructions:
- Specify which plan or phase to execute
- Provide context about the project if needed
- The director agent will handle all orchestration autonomously
