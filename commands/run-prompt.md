---
name: run-prompt
description: Use when executing prompts from .prompts/prompts/ as delegated sub-tasks with fresh context. Secondary: running multiple prompts in parallel/sequential, delegating to fresh contexts, or automating prompt execution.
argument-hint: <prompt-number(s)-or-name> [--parallel|--sequential]
allowed-tools: [Read, Task, Glob, Bash(ls:*), Bash(mv:*), Bash(git add:*), Bash(git status:*), Bash(git commit:*)]
---

## Objective

Execute the prompt(s) specified in '$ARGUMENTS' located in `.prompts/prompts/`. Handle single or multiple prompts intelligently with parallel or sequential execution.

## Process

Delegate to Task tool with subagent_type="general-purpose" to:

1. **Resolve prompt files:**
   - Use Glob to find files in `.prompts/prompts/` matching the arguments
   - Support numbers (e.g., "5" or "005"), partial names, or empty for most recent
   - Handle single or multiple prompt selection

2. **Execute prompts:**
   - Single prompt: Execute directly with fresh context
   - Multiple prompts: Execute with --parallel or --sequential as specified
   - Default to sequential for safety if no flag provided

3. **Context strategy:**
   - Subagents need ALL relevant context about the project
   - Include project structure, tech stack, and working directory
   - Pass full prompt file contents to each subagent

4. **Complete execution:**
   - Archive completed prompts to `.prompts/prompts/completed/`
   - Commit all changes with appropriate type/format
   - Provide clear summary of results

## Constraints

- Use fresh context for each prompt execution
- Stage files individually (never `git add .`)
- Archive prompts only after successful completion
- For parallel: spawn all Task tools in a single message
- For sequential: wait for completion before next prompt
