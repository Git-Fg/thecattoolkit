---
name: create-prompt
description: Create optimized prompts with XML structure for AI agents. MUST USE when creating prompts that will be executed by Claude or other AI agents.
argument-hint: [task description]
allowed-tools: [Task]
---

Invoke @prompt-architect with input: $ARGUMENTS

The subagent will:
1. Use Intake Gate protocol if the request is vague
2. Analyze complexity to determine template type
3. If simple: Generate standard prompt using simple-task-patterns
4. If complex: Generate meta-prompt structure using do/research/plan patterns
5. Save to ./prompts/ directory and present execution options
