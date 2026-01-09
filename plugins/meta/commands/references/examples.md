# Command Examples

This file contains examples for meta plugin commands.

## /build Examples

### Creating a Component
```
Context: User wants to create a component
user: "Build a new skill for database validation"
assistant: "I'll orchestrate the creation of a database validation skill using the manage-skills standards."
```

### Auditing Components
```
Context: Component audit
user: "Build audit our agents for compliance"
assistant: "I'll use the build command to audit agent configurations against standards."
```

### Creating Commands
```
Context: Structured component creation
user: "Build command create new-review"
assistant: "I'll orchestrate creating a new review command using the manage-commands standards."
```

## /heal Examples

### Skill Failure
```
Context: A skill just failed or produced incorrect output
user: "/heal the skill seems to have hallucinated a tool"
assistant: "I'll analyze the recent error and diagnose the drift in the skill definition."
```

### Agent Failure
```
Context: An agent entered an infinite loop
user: "/heal the agent keeps looping"
assistant: "I'll diagnose the missing constraint in the agent definition and propose a fix."
```

## /bootstrap Examples

### Plugin Restoration
```
Context: Component corruption detected
user: "/bootstrap plugins/meta"
assistant: "I'll perform a soft reset of the meta plugin to restore it to the last known good state from HEAD."
```

### System-Wide Recovery
```
Context: System-wide failure
user: "/bootstrap --hard 1"
assistant: "I'll perform a hard reset to HEAD~1 to recover from catastrophic state drift."
```
