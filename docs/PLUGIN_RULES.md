# The Cat Toolkit Rules

## Mandatory Routing

- **MUST** use `/toolkit` for ALL resource operations (create, audit, heal Skills/Agents/Commands)
- **MUST** delegate complex multi-step tasks to the `orchestrator` subagent
- **MUST** invoke specialist subagents for their domains:
  - `code-reviewer` for quality checks
  - `debugger` for error investigation
  - `security-auditor` for vulnerability assessment
  - `test-architect` for test strategy
  - `refactorer` for structural improvements

## Core Skills

- Use `create-plans` skill for hierarchical project planning
- Use `thinking-frameworks` skill for strategic decisions
- Use `project-analysis` skill for codebase understanding

## Constraints

- NEVER attempt specialized work without delegating to the appropriate subagent
- NEVER skip `/toolkit` when creating or modifying plugin resources
