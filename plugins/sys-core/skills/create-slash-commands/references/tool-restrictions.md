# Tool Restrictions

How to restrict tool access in slash commands for security and focus.

## Why Restrict Tools

Tool restrictions provide:
- **Security** - Prevent destructive operations
- **Focus** - Limit scope for specialized commands
- **Safety** - Ensure intended operations only

## Basic Syntax

### Array Format

```yaml
---
description: "My command"
allowed-tools: [Read, Edit, Write]
---
```

### Single Tool

```yaml
---
description: "Thinking command"
allowed-tools: SequentialThinking
---
```

### Bash Patterns

```yaml
---
description: "Git command"
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---
```

## Common Patterns

### Git-Only Commands

```yaml
---
description: "Create a git commit"
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

Current status: ! git status
Changes: ! git diff HEAD

Create a commit for these changes.
```

**Allows:**
- `git add <anything>`
- `git status <anything>`
- `git commit <anything>`

**Prevents:**
- `rm -rf`
- `curl`
- Non-git commands

### NPM Script Restrictions

```yaml
---
description: "Run checks"
allowed-tools: Bash(npm test:*), Bash(npm run lint:*)
---

Run quality checks:
! npm test
! npm run lint
```

**Allows:**
- `npm test`
- `npm run lint`

**Prevents:**
- `npm install`
- `npm run deploy`

### Multiple Bash Patterns

```yaml
---
description: "Development workflow"
allowed-tools: Bash(git status:*), Bash(npm test:*), Bash(npm run build:*)
---
```

## Security Patterns

### Read-Only Analysis

```yaml
---
description: "Analyze codebase safely"
allowed-tools: [Read, Grep, Glob]
argument-hint: [search pattern]
---

Search codebase for: $ARGUMENTS

Analyze findings without modifying files.
```

**Security benefit:** Cannot write or execute

### Thinking-Only Commands

```yaml
---
description: "Deep analysis"
allowed-tools: SequentialThinking
---

Analyze the problem from first principles:

1. Identify core issue
2. Question assumptions
3. Rebuild solution
4. Compare approaches
```

**Focus benefit:** Pure reasoning, no file operations

### Controlled Deployment

```yaml
---
description: "Deploy to staging"
allowed-tools: Bash(npm run deploy:staging), Bash(git push origin:staging)
---

Deploy to staging environment only.

Status: ! git status
```

**Safety benefit:** Cannot deploy to production

## When to Restrict

### ✅ Restrict when:

1. **Security-sensitive operations**
   - Git workflows
   - Deployment commands
   - File deletions

2. **Focused tasks**
   - Deep analysis
   - Code review
   - Planning

3. **Read-only operations**
   - Searching codebase
   - Reading files
   - Analysis

4. **Specific commands**
   - Only npm test/lint
   - Only git status/diff
   - Only specific scripts

### ❌ Don't restrict when:

1. **Complex workflows**
   - Multi-step processes
   - Unknown requirements
   - Debugging tasks

2. **Exploratory tasks**
   - Investigating issues
   - General problem-solving
   - Learning

3. **Flexible needs**
   - Tool needs unpredictable
   - Context-dependent

## Best Practices

### 1. Use Specific Patterns

```yaml
# Good - specific operations
allowed-tools: Bash(git add:*), Bash(git commit:*)

# Better - minimal permissions
allowed-tools: Bash(git status:*), Bash(git diff:*)
```

### 2. Combine Tool Types

```yaml
# Analysis with git context
allowed-tools: [Read, Grep, Bash(git status:*)]
```

### 3. Document Restrictions

```yaml
---
description: "Git commit (git commands only for security)"
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---
```

### 4. Test Restrictions

Verify allowed operations work and blocked operations fail.

## Tool Types Reference

### File Operations
- `Read` - Read files
- `Write` - Write new files
- `Edit` - Modify existing files
- `Grep` - Search content
- `Glob` - Find files by pattern

### Execution
- `Bash(pattern:*)` - Execute bash commands
- `SequentialThinking` - Reasoning tool

### Other
- `Task` - Invoke subagents
- `WebSearch` - Web search
- `WebFetch` - Fetch web pages

## Examples

### Git Commit (Full Example)

```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: "Create a git commit"
---

Current status: ! git status
Changes: ! git diff HEAD
Branch: ! git branch --show-current
Recent commits: ! git log --oneline -5

Create a single git commit following repository conventions.
```

**Allowed:**
- `git add .`
- `git status`
- `git commit -m "message"`

**Blocked:**
- `rm file.js`
- `curl url`
- `npm install`

### Code Review (No Restrictions)

```yaml
---
description: "Review code for vulnerabilities"
---

Review this code for security vulnerabilities:

1. Check for common issues (XSS, SQL injection, CSRF)
2. Identify specific problems with locations
3. Suggest remediation steps
```

**No restrictions** = All tools available

## Limitations

1. **Wildcard patterns** may vary by version
2. **Cannot blacklist** - only whitelist
3. **All or nothing** for tool types
4. **File-specific restrictions** may not be supported

## Testing

After creating command with restrictions:

1. Try allowed operations - should work
2. Try blocked operations - should fail
3. Verify error messages are clear
4. Test with actual use cases
