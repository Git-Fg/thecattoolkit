---
description: |
  Generate and execute conventional commit messages from staged changes (agent-accessible).
  <example>
  Context: User or agent needs to commit changes
  user: "Commit these changes"
  assistant: "I'll analyze staged changes and generate a conventional commit message."
  </example>
  <example>
  Context: Agent needs autonomous git operations
  user: "Auto-commit the feature implementation"
  assistant: "I'll use the auto-commit command for autonomous git operations."
  </example>
allowed-tools: Bash(git diff:*), Bash(git commit:*), Skill(git-workflow)
argument-hint: [optional: additional context for commit message]
---

## Objective
Generate and execute a conventional commit for staged changes. This command is designed to be callable by other agents for autonomous git operations.

## Process

**Capture staged changes:**
Run git diff --staged to load context.

**Generate commit message:**
Use the git-workflow skill to analyze the diff and generate a conventional commit message.

**Execute commit autonomously:**
Display the message for transparency and execute immediately without requiring user input. This is the Type B (Agent-Ready) variant of the /commit command.

**Additional context:** $ARGUMENTS

**Success criteria:**
- Staged changes analyzed correctly
- Appropriate commit type determined
- Message displayed and commit executed
- Commit completed successfully
