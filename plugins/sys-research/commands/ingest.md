---
description: "Ingest a Git repository into an AI-readable digest. Use this instead of reading raw git files."
argument-hint: "<url> [options]"
allowed-tools: [Skill(gitingest)]
disable-model-invocation: true
---

# Ingest Repository

Invoke the `gitingest` skill.

If arguments are provided (`$ARGUMENTS`), pass them as the target.
If no arguments are provided, default to the current repository context.

Examples:
- `/ingest https://github.com/user/repo`
- `/ingest .`
