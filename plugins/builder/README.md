# @cat-toolkit/builder

**The Execution Engine: Autonomous orchestration and engineering implementation.**

**License:** MIT

## Purpose

The Builder plugin provides the core **Engine** for the Cat Toolkit. It transforms plans into reality through two specialized agents:
1. **Director**: Orchestrates, creates fresh context, and manages state.
2. **Worker**: Executes tasks, writes code, and handles implementation details.

## Agents

### 1. Director (`director`)
The orchestrator. It does not write code. It coordinates `worker` subagents to execute tasks in parallel or sequence.
- **Specialty**: Context Management, State Tracking, Quality Assurance.
- **Mode**: Uninterrupted Flow.
- **Capabilities**: Parallel execution, Read-Back verification.

### 2. Worker (`worker`)
The implementer. It executes specific engineering tasks assigned by the Director.
- **Specialty**: TDD, Debugging, Implementation.
- **Mode**: Uninterrupted Flow (Strict).
- **Constraints**: No `ask_user` allowed. Must self-verify.

## Installation

```bash
claude plugin install @cat-toolkit/builder
```

## Usage

### Run a Plan
```bash
claude-code "Execute the current plan"
# Delegates to Director -> Spawns Workers
```

### Direct Implementation
```bash
claude-code "Implement the auth module using TDD"
# Delegates to Worker directly (for smaller tasks)
```

## Architecture

The Builder enforces the **Sovereign Triangle** pattern:
- **Command**: `/execute` (implied)
- **Agent**: `director` (Orchestrator) -> `worker` (Executor)
- **Skill**: `execution-core` (Behavior), `software-engineering` (Quality)

## Best Practices

- **Always have a plan**: The Director works best with a `PLAN.md`.
- **Trust the Flow**: The agents are designed to work autonomously. Do not interrupt them unless they hang.
- **Review Context**: The Director relies on injected context. Ensure `BRIEF.md` and `PLAN.md` are up to date.
