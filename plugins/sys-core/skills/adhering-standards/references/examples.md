# Working Examples

## Skill Router Pattern

A canonical example of a skill that:
- Analyzes code to determine workflow
- Delegates to appropriate sub-skills
- Uses progressive disclosure

### Key Features
```yaml
name: code-analyzer
description: "Analyzes code and routes to appropriate analysis workflow. USE when analyzing code for security, performance, or architectural issues."
context: fork
allowed-tools: [Read, Grep, Glob, Skill(code-security-audit), Skill(performance-analysis)]
```

### Pattern Benefits
- Single entry point for multiple workflows
- Automatic routing based on context
- Reusable sub-skills
- Clean separation of concerns

## Command Orchestration

A command that:
- Executes git operations
- Runs deployment gates
- Uses dynamic context

### Key Features
```yaml
description: "Executes git operations and runs deployment gates. USE when committing and deploying changes."
allowed-tools: [Skill(git-operations), Skill(deployment-gates)]
disable-model-invocation: true
```

### Pattern Benefits
- Multi-skill orchestration
- User-centric interface
- Autonomous execution
- Argument integration with `$ARGUMENTS`

## Background-Safe Agent

A read-only code explorer suitable for background execution.

### Key Features
```yaml
name: code-explorer
description: "Read-only code analysis agent for background execution. MUST Use when analyzing code without modifications."
tools: [Read, Grep, Glob]
```

### Pattern Benefits
- Background execution safety
- Least privilege security
- Read-only operations
- No interactive prompts

## Anti-Pattern Examples

### BAD: Vague Description
```yaml
description: "Analyzes code"
```
**Problem:** Won't be discovered by users

**Fix:**
```yaml
description: "Analyzes code for security vulnerabilities. USE when performing security audits."
```

### BAD: Logic Duplication
```yaml
description: "Analyzes code... [embedded analysis logic]"
allowed-tools: [Skill(code-analyzer)]
```
**Problem:** Code duplication, maintenance nightmare

**Fix:**
```yaml
description: "Shortcut for code analysis workflow."
allowed-tools: [Skill(code-analyzer)]
```

### BAD: Missing Tool Restrictions
```yaml
tools: [Read, Write, Edit, Bash]
```
**Problem:** Security risk

**Fix:**
```yaml
tools: [Read, Grep, Glob]
```
