---
description: "Quick access to file-search functionality for finding files and searching code."
argument-hint: "[pattern] [path]"
allowed-tools: [Skill(file-search), Bash(fd:*), Bash(rg:*), Bash(fzf:*)]
disable-model-invocation: true
---

# File Search Command

Invoke Skill(file-search) to perform file and content search operations.

## Usage

This command provides quick access to modern file search tools (fd, ripgrep, fzf).

**If arguments provided:**
- Execute search directly using fd/rg

**If no arguments:**
- Load skill for interactive discovery

## Examples

```bash
/sys-core:file-search "TODO"              # Search for TODO
/sys-core:file-search "config" src/       # Find in directory
/sys-core:file-search                     # Load skill interactively
```

The skill will guide you through appropriate search patterns based on your needs.
