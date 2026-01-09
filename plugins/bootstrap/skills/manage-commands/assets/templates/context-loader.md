---
description: [VERBS] Load context from {CONTEXT_SOURCE} for {PURPOSE}.
argument-hint: [{ARG_HINT}]
---

Execute the context loader: $ARGUMENTS

## Dynamic Context Loading

This command loads dynamic context using the `!` prefix for bash commands:

**Example:**
```
!/commands/context-loader {ARG}
```

This will execute: `{COMMAND_EXAMPLE}`

*WHY: The `!` prefix executes bash commands and returns output for context injection.*
