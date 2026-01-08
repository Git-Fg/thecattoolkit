---
description: |
  Generate and execute conventional commit messages from staged changes.
  <example>
  Context: User wants to commit changes
  user: "Commit these changes"
  assistant: "I'll analyze the staged changes and generate a conventional commit message."
  </example>
  <example>
  Context: Git workflow management
  user: "Create a commit for our feature"
  assistant: "I'll use the commit command to generate and execute the commit."
  </example>
allowed-tools: Bash(git diff:*), Bash(git commit:*), Skill(git-workflow)
argument-hint: [optional: additional context]
disable-model-invocation: true
---

## Objective
Generate and execute a conventional commit for staged changes.

## Process

**Capture staged changes:**
Run git diff --staged to load context.

**Generate commit message:**
Use the git-workflow skill to analyze the diff and generate a conventional commit message.

**Execute commit automatically:**
Display the message for transparency and execute immediately. Only ask for input if critical issues are detected (unusual patterns, breaking changes).

**Additional context:** $ARGUMENTS

**Success criteria:**
- Staged changes analyzed correctly
- Appropriate commit type determined
- Message displayed and commit executed
- Commit completed successfully
