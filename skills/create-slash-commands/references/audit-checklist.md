# Slash Command Best Practices

Reference for auditing slash commands. Contains evaluation criteria, anti-patterns, and output format templates.

## Required Reading for Auditing

When auditing a slash command, read these reference files:
1. SKILL.md - Overview of slash command structure
2. references/arguments.md - Argument usage patterns
3. references/patterns.md - Command patterns
4. references/tool-restrictions.md - Security patterns

## Evaluation Areas

### YAML Configuration

**description**:
- Clear, specific description of what the command does
- Uses strong language patterns (MUST BE USED/PROACTIVELY USE/CONSULT)
- No vague terms like "helps with" or "processes data"
- Max 1024 characters

**allowed-tools**:
- Present when appropriate for security (git commands, thinking-only, read-only analysis)
- Properly formatted (array or bash patterns)
- Examples: `[Read, Write]`, `Bash(git add:*)`, `Bash(git:*)`

**argument-hint**:
- Present when command uses arguments
- Clear indication of expected arguments format
- Examples: `<file-path>`, `[issue-description]`, `[optional-hint]`

### Arguments

**Appropriate argument type**:
- Uses `$ARGUMENTS` for simple pass-through
- Uses positional `$1`, `$2`, `$3` for structured input
- Arguments properly integrated into prompt

**Argument integration**:
- Examples: "Fix issue #$ARGUMENTS", "@$ARGUMENTS", "Check $1 for $2"
- Arguments are used in the prompt, not ignored

**Handling empty arguments**:
- Command works with or without arguments when appropriate
- Or clearly requires arguments (e.g., `<file-path>` not `[file-path]`)

### Dynamic Context

**Context loading**:
- Uses exclamation mark + backtick syntax for state-dependent tasks
- Example: `Git status: ! git status --short`

**Context relevance**:
- Loaded context is directly relevant to command purpose
- Git commands load git status
- Project commands load project structure

**Examples**:
```markdown
Git context:
- Current branch: ! git branch --show-current
- Status: ! git status --short

Environment context:
- Python version: ! python3 --version
- Node version: ! node --version
```

### Tool Restrictions

**Security appropriateness**:
- Restricts tools for security-sensitive operations
- Git-only commands use `allowed-tools: [Bash(git:*)]`
- Read-only analysis uses `allowed-tools: [Read, Grep, Glob]`

**Restriction specificity**:
- Uses specific patterns: `Bash(git add:*)` rather than overly broad access
- Prevents destructive operations without explicit permission

**Common patterns**:
- Git commands: `allowed-tools: [Bash(git:*)]`
- Read-only: `allowed-tools: [Read, Grep, Glob]`
- Thinking-only: `allowed-tools: []` (no tools, pure reasoning)

### Content Quality

**Clarity**:
- Prompt is clear, direct, specific
- Instructions are unambiguous

**Structure**:
- Multi-step workflows properly structured with numbered steps or sections
- Single-step commands are concise

**File references**:
- Uses @ prefix for file references when appropriate
- Example: "Analyze @$ARGUMENTS for issues"

## Anti-Patterns

Flag these issues during audits:

1. **vague_descriptions**: "helps with", "processes data", "does stuff"
2. **missing_tool_restrictions**: Git or deployment commands without tool restrictions
3. **no_dynamic_context**: State-dependent commands (git, env) without context loading
4. **poor_argument_integration**: Arguments not used or used incorrectly
5. **overly_complex**: Commands that should be broken into multiple commands
6. **missing_description**: No description field in YAML frontmatter
7. **unclear_instructions**: Commands without structure or clear steps
8. **inconsistent_naming**: Command name doesn't match purpose

## Contextual Judgment

Apply judgment based on command purpose and complexity:

**Simple commands** (single action, no state):
- Dynamic context may not be needed - don't flag its absence
- Minimal tool restrictions may be appropriate
- Brief prompts are fine

**State-dependent commands** (git, environment-aware):
- Missing dynamic context is a real issue
- Tool restrictions become important

**Security-sensitive commands** (git push, deployment, file modification):
- Missing tool restrictions is critical
- Should have specific patterns, not broad access

**Delegation commands** (invoke subagents):
- `allowed-tools: [Task]` is appropriate
- Success criteria can focus on invocation
- Pre-validation may be redundant if subagent validates

Always explain WHY something matters for this specific command, not just that it violates a rule.

## Output Format

Audit reports use severity-based findings, not scores:

```markdown
## Audit Results: [command-name]

### Assessment
[1-2 sentence overall assessment: Is this command fit for purpose? What's the main takeaway?]

### Critical Issues
Issues that hurt effectiveness or security:

1. [Issue category] (file:line)
   - Current: [What exists now]
   - Should be: [What it should be]
   - Why it matters: [Specific impact on this command's effectiveness/security]
   - Fix: [Specific action to take]

2. ...

(If none: "No critical issues found.")

### Recommendations
Improvements that would make this command better:

1. [Issue category] (file:line)
   - Current: [What exists now]
   - Recommendation: [What to change]
   - Benefit: [How this improves the command]

2. ...

(If none: "No recommendations - command follows best practices well.")

### Strengths
What's working well (keep these):
- [Specific strength with location]
- ...

### Quick Fixes
Minor issues easily resolved:
1. [Issue] at file:line → [One-line fix]
2. ...

### Context
- Command type: [simple/state-dependent/security-sensitive/delegation]
- Line count: [number]
- Security profile: [none/low/medium/high - based on what the command does]
- Estimated effort to address issues: [low/medium/high]
```
