/// ⚠️ DEPRECATED: COMMANDS ARE RARELY NEEDED (2026 PHILOSOPHY) ///

**Commands are ONLY for:**
- ✅ Dynamic bash injection (Skills cannot parse `!bash`)
- ✅ Environment variable resolution (Skills cannot access `$VAR`)
- ✅ Auto-resolution logic that requires shell execution

**Commands are NOT for:**
- Simple skill wrappers (use Skills directly)
- User interaction (use `AskUserQuestion` in Skills)
- Workflow orchestration (use Orchestrator Skills)

**Before creating a command, ask:**
1. Can this be a Skill? (95% of the time: YES)
2. Does this require bash/env parsing? (If no: Use Skill)
3. Does this add unique value beyond a Skill? (If no: Delete it)

# Commands (Slash Commands - Deprecated)

Commands are the **explicit interface** of the plugin. These are **Instructions for Claude**, not messages for the user.

**2026 Status:** Commands are deprecated. Use Skills instead, except for bash/env injection.

## Quick Reference (Cat Toolkit Specific - 2026)

This section provides quick, practical patterns for commands in the Cat Toolkit.

### 1. Anatomy (`commands/*.md`)

A command is a Markdown file with strict frontmatter.

```yaml
---
description: "Review security flaws"   # Mandatory.
argument-hint: "[file] [level]"        # UX: Guides autocompletion.
allowed-tools: ["Read", "Grep"]        # Security: Whitelist.
disable-model-invocation: true         # Control: Prevents model from calling it alone.
hide-from-slash-command-tool: "true"   # Visibility: Hide from menu.
---

# Prompt Body

Direct instruction to the AI.
```

### 2. Dynamic Syntax (Commands' Unique Value)

**Why Commands Still Exist:**
Skills cannot execute bash or resolve environment variables at load time. Commands can.

#### Bash Injection (`!command`)
**Executed by shell before prompt reaches model.**

**Use when:**
- Environment validation (`!test -f .env && echo "OK"`)
- Dynamic path resolution (`!find . -name "*.json" | head -1`)
- Version checking (`!node -v`)

**Example:**
```markdown
Environment Check: !`test -f .env || echo "MISSING"`

If MISSING, stop and notify the user.
```

**NOT a use case:** Simple skill invocation
```markdown
❌ BAD: Use the pdf-parser skill!
✅ GOOD: Just use the skill directly (model will discover it)
```

#### File Injection (`@file`)
**Injects file content at command invocation.**

**Use when:**
- Template files (`@templates/config.json`)
- User project context (`@package.json`)
- Dynamic configuration

**NOT a use case:** Static skill content
```markdown
❌ BAD: Include skill's reference file
✅ GOOD: Skill references its own files (hub-and-spoke)
```

### 3. Interaction Patterns

#### The "Hybrid" Pattern (args vs questions)
Should you use arguments (`$1`) or ask questions?
*   **Rule:** Use arguments for power users (fast), use `AskUserQuestion` for exploration.
*   **Best Practice:** Check if `$1` is empty. If yes, trigger the Wizard.

```markdown
Project Type: !`[ -z "$1" ] && echo "ASK" || echo "$1"`

If Project Type is "ASK", call AskUserQuestion to get the user's preference.
```

### 4. The 3 Command Patterns (2026 Aligned)

Based on official plugins (`commit-commands`, `hookify`, `pr-review-toolkit`), here are the standard patterns that remain valid.

#### 1. The Wizard ("Interactive Configuration")
**Example:** `sys-core:doctor`

**Function:** Guides user through complex setup using `AskUserQuestion`.

**Why Command, Not Skill:**
- Requires interactive question flow
- Dynamic configuration generation
- Environment-specific setup

**Pattern:**
```markdown
1. Analyze environment: !`test -f .env && echo "OK" || echo "MISSING"`

2. If MISSING, use `AskUserQuestion`:
   - "Which database?" (MySQL, PostgreSQL, SQLite)
   - "What port?" (3306, 5432, custom)

3. Generate config.json based on responses
```

#### 2. The Context Loader ("Debug/Diagnose")
**Example:** `/doctor` commands

**Function:** Massively retrieves system info for debugging.

**Why Command, Not Skill:**
- Bash execution for environment detection
- Multiple shell invocations
- Dynamic system introspection

**Pattern:**
```markdown
Context Analysis:
- Node Version: !`node -v`
- Git Status: !`git status`
- Env Vars: !`printenv | grep MY_PLUGIN`
- Dependencies: !`npm list --depth=0`

Diagnose configuration issues based on this data.
```

#### 3. The Scaffolder ("Template Generator")
**Example:** `plugin-dev:create`

**Function:** Copies templates from plugin cache to user project.

**Why Command, Not Skill:**
- Requires `${CLAUDE_PLUGIN_ROOT}` resolution
- File copying via bash
- Template instantiation

**Pattern:**
```markdown
Execute: !`bash ${CLAUDE_PLUGIN_ROOT}/scripts/scaffold.sh`

This script:
1. Copies templates from plugin cache
2. Renames placeholders
3. Creates project structure

Then ask user for customization preferences.
```

### Deprecated Patterns (DO NOT USE)

#### ❌ The Wrapper ("Skill Runner")
**Deprecated:** Simple skill invocation

```markdown
❌ BAD:
---
description: "Run the pdf-parser skill"
---

Use the pdf-parser skill now!

✅ GOOD:
Delete this command. The skill is auto-discoverable.
```

#### ❌ The Delegator ("Agent Launcher")
**Deprecated:** Simple agent delegation

```markdown
❌ BAD:
---
description: "Launch the code-reviewer agent"
---

Initiate review using code-reviewer agent.

✅ GOOD:
Use Skill with `context: fork` for isolation, or Skill directly.
```

**Migration Path:**
1. Delete wrapper command files
2. Ensure underlying Skill has good description for discovery
3. Test model invocation works

---

## Deep Dive: Universal Command Engineering

> **Note:** This section contains comprehensive, framework-agnostic principles for command design. It extends beyond the Cat Toolkit-specific patterns above.

### Division I: Command Fundamentals

#### What is a Command?

A **command** is a discrete, invocable unit of functionality that:
- Accepts input (arguments, context, or both)
- Executes a defined operation or workflow
- Returns output or produces side effects
- Can be composed with other commands

Commands serve as the **interface layer** between human intent and agent execution.

#### The Command Spectrum

Commands exist on a spectrum from simple to complex:

| Type | Complexity | Invocation | Context |
|------|------------|------------|---------|
| **Shortcuts** | Single operation | Explicit (user-typed) | Minimal |
| **Workflows** | Multi-step operations | Explicit | Moderate |
| **Agents/Skills** | Autonomous operations | Implicit (model-decided) | Rich |

**Key Insight**: The best command systems support the full spectrum, allowing simple shortcuts to compose into complex workflows.

#### Core Design Principles

1. **Single Responsibility**: Each command does one thing well
2. **Composability**: Commands can chain and combine
3. **Discoverability**: Commands are easy to find and understand
4. **Predictability**: Same input produces same output
5. **Graceful Degradation**: Commands fail informatively

### Division II: Command Architecture

#### Metadata Design

##### Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| **Verb-first** | `deploy-staging` | Actions |
| **Noun-first** | `test-results` | Queries |
| **Domain-scoped** | `git-commit`, `db-query` | Namespaced operations |

**Anti-patterns to avoid**:
- Cryptic abbreviations (`dpl` instead of `deploy`)
- Overlapping names across scopes
- Names that don't indicate action or purpose

##### Description Engineering

The description serves two audiences:
1. **Humans**: Understand what the command does
2. **Models**: Decide when to invoke the command automatically

**Effective description formula**:
```
[Action verb] + [Target/Domain] + [Key constraint or outcome]

Examples:
✓ "Review code for security vulnerabilities and provide remediation steps"
✓ "Deploy application to staging environment with health check verification"
✗ "Deploy" (too vague)
✗ "This command deploys things" (passive, unclear)
```

##### Argument Specification

Three patterns for handling arguments:

1. **Positional** (`$1`, `$2`, `$3`): For structured, ordered inputs
2. **Aggregated** (`$ARGUMENTS`): For flexible, free-form inputs
3. **Named**: For complex commands with many optional parameters

**Best practice**: Provide hints showing expected format:
```
argument-hint: [environment] [--dry-run]
```

#### Capability Scoping

Commands should request **minimum necessary capabilities**:

| Command Type | Typical Capabilities |
|--------------|---------------------|
| Read-only analysis | Read, Search, Query |
| Code modification | Read, Write, Edit |
| System operations | Read, Write, Execute |
| Full autonomy | All capabilities |

**Principle of Least Privilege**: A code review command doesn't need write access. A deployment command doesn't to read unrelated files.

#### Frontmatter Configuration

Commands support YAML frontmatter metadata for enhanced configuration:

**Standard frontmatter fields**:

| Field | Purpose | Default |
|-------|---------|---------|
| `allowed-tools` | List of tools the command can use | Inherits from conversation |
| `argument-hint` | Expected arguments format for autocomplete | None |
| `context` | Execution context mode (inline/fork) | inline |
| `agent` | Agent type for forked contexts | general-purpose |
| `description` | Brief command description | First line of prompt |
| `model` | Specific model to use | Inherits from conversation |
| `disable-model-invocation` | Prevent programmatic invocation | false |
| `hooks` | Hooks scoped to command execution | None |

**Example with positional arguments**:
```yaml
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request
model: claude-3-5-haiku-20241022
allowed-tools: Bash(git:*), Read, Grep
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

**Best practices**:
- Use `argument-hint` to show expected format (e.g., `add [tagId] | remove [tagId] | list`)
- Set `context: fork` for commands that need isolated context
- Specify `allowed-tools` explicitly for safety
- Use `disable-model-invocation: true` for manual-only commands

### Division III: Instruction Engineering

#### The Instruction Structure

Effective command instructions follow this pattern:

```
1. CONTEXT GATHERING
   - What information does the command need?
   - What files/state should be examined?

2. EXECUTION LOGIC
   - What specific steps should be taken?
   - What decisions need to be made?

3. OUTPUT FORMAT
   - How should results be presented?
   - What should be included/excluded?

4. ERROR HANDLING
   - What could go wrong?
   - How should failures be communicated?
```

#### Dynamic Context Injection

Commands become powerful when they incorporate dynamic context:

| Syntax | Purpose | Example |
|--------|---------|---------|
| `@file` | Include file contents | `@src/config.json` |
| `!command` | Execute and include output | `!git status` |
| `$VAR` | Inject argument values | `Review PR #$1` |

**Sequencing matters**: Gather context before asking for analysis.

```
# Good: Context first, then instruction
Current git status: !`git status`
Recent commits: !`git log --oneline -10`

Based on the above, create an appropriate commit message.

# Bad: Instruction without context
Create a commit message for the current changes.
```

#### Instruction Clarity Patterns

##### Be Explicit About Constraints

```
# Vague
Review this code.

# Explicit
Review this code for:
- Security vulnerabilities (SQL injection, XSS, command injection)
- Performance issues (N+1 queries, unnecessary loops)
- Code style violations per our ESLint config
Do NOT suggest refactoring unless it fixes one of the above issues.
```

##### Specify Output Format

```
Provide feedback organized by priority:
1. **Critical** (must fix before merge)
2. **Warning** (should fix)
3. **Suggestion** (consider improving)

For each issue, include:
- File and line number
- Problem description
- Suggested fix with code example
```

##### Define Success Criteria

```
Continue until:
- All tests pass
- No linter errors remain
- Coverage exceeds 80%

If any criterion cannot be met, report what's blocking progress.
```

### Division IV: Command Scoping & Organization

#### Scope Hierarchy

Commands should be organized by scope:

| Scope | Location | Visibility | Use Case |
|-------|----------|------------|----------|
| **Session** | Runtime/CLI flag | Current session only | Testing, one-off operations |
| **Project** | Project directory | Anyone in project | Team workflows, project-specific |
| **User** | Home directory | All user's projects | Personal preferences, cross-project |
| **System** | Platform/Plugin | Platform-wide | Shared infrastructure |

**Priority rule**: Narrower scope overrides broader scope.

#### Command Precedence Rules

When commands exist at multiple scopes, precedence determines which executes:

| Scenario | Precedence | Behavior |
|----------|------------|----------|
| **Project vs User** | Project wins | User command is silently ignored |
| **Same name, different scopes** | Narrower scope | Session > Project > User > System |
| **Namespaced commands** | All visible | Subdirectory shown in description for disambiguation |

**Example**:
```
.claude/commands/deploy.md      → /deploy (project version wins)
~/.claude/commands/deploy.md     → /deploy (ignored when project exists)

.claude/commands/frontend/test.md   → /test (shows as "project:frontend")
.claude/commands/backend/test.md    → /test (shows as "project:backend")
```

### Division V: Composition Patterns

#### Command Chaining

Commands should support sequential execution:

```
Pattern: Output of A becomes input to B

Example workflow:
1. /analyze-code → produces issue list
2. /fix-issues $ISSUES → applies fixes
3. /run-tests → verifies fixes
4. /commit "Fixed issues" → commits changes
```

#### Parallel Execution

Independent commands can run concurrently:

```
Pattern: Multiple commands execute simultaneously

Example:
- /lint-frontend (runs in parallel with)
- /lint-backend (runs in parallel with)
- /run-type-check

All complete → aggregate results
```

#### Conditional Execution

Commands can branch based on results:

```
Pattern: Execute B only if A succeeds/fails

Example:
/run-tests
  ├── If PASS → /deploy-staging
  └── If FAIL → /notify-team "Tests failed"
```

### Division VI: State & Session Management

#### Stateless vs. Stateful Commands

| Type | Characteristics | Use Case |
|------|-----------------|----------|
| **Stateless** | No memory between invocations | Simple queries, utilities |
| **Stateful** | Maintains context across calls | Iterative workflows, debugging |

#### Session Continuity

Commands should support:
- **Resume**: Continue where left off
- **Fork**: Branch from a previous state
- **Replay**: Re-execute with modifications

### Division VII: Error Handling & Resilience

#### Failure Modes

Commands should handle:

| Failure Type | Response Pattern |
|--------------|------------------|
| **Invalid input** | Validate early, provide examples |
| **Missing dependencies** | Check prerequisites, suggest installation |
| **Permission denied** | Explain what's needed, request authorization |
| **Partial completion** | Save progress, enable resume |
| **Timeout** | Set reasonable limits, allow extension |

#### Graceful Degradation

```
Priority order:
1. Complete task fully
2. Complete task partially with clear status
3. Fail informatively with actionable guidance
4. Fail safely without side effects
```

### Division VIII: Security Considerations

#### Permission Models

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Default** | Prompt for each sensitive action | Interactive use |
| **Allowlist** | Auto-approve specific operations | Trusted workflows |
| **Denylist** | Block specific operations | Safety constraints |
| **Bypass** | Skip all permission checks | CI/CD, controlled environments |

#### Input Sanitization

Commands accepting user input must:
- Validate format and type
- Escape special characters
- Limit input size
- Reject suspicious patterns

#### Capability Isolation

Subagents and delegated commands should:
- Run with minimum necessary permissions
- Not inherit parent's full capabilities by default
- Have explicit capability grants

### Division IX: Testing & Validation

#### Command Testing Patterns

| Test Type | What to Verify |
|-----------|---------------|
| **Unit** | Individual command logic |
| **Integration** | Command + external systems |
| **Composition** | Chained command workflows |
| **Edge cases** | Missing args, invalid input, failures |

#### Dry Run Mode

Commands with side effects should support:
```
--dry-run: Show what would happen without executing
--verbose: Show detailed execution trace
--confirm: Require explicit approval before changes
```

### Division X: Performance Optimization

#### Context Efficiency

| Strategy | Benefit |
|----------|---------|
| **Lazy loading** | Only fetch context when needed |
| **Selective context** | Include only relevant files |
| **Summarization** | Compress large outputs |
| **Caching** | Reuse unchanged context |

#### Execution Optimization

| Pattern | When to Use |
|---------|-------------|
| **Parallel subagents** | Independent research tasks |
| **Streaming output** | Long-running operations |
| **Incremental updates** | Large batch operations |
| **Early termination** | When goal is achieved |

#### Character Budget Management

When commands are programmatically invoked (e.g., via Skill tool), they consume context budget:

**Budget limits**:
- Default character budget: 15,000 characters
- Budget applies to command name + arguments + description
- Excess commands are excluded when budget is exceeded

**Optimization strategies**:
- Keep descriptions concise but informative
- Use `argument-hint` to show usage patterns without verbose descriptions
- Monitor context usage with `/context` command
- Set custom budget via `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable if needed

**Best practices**:
- Prioritize most-used commands in documentation
- Group related commands efficiently
- Use descriptive but terse naming

---

## Quick Reference Checklist

### Command Design Checklist

Before finalizing a command, verify:

**Metadata**
- [ ] Name is clear and action-oriented
- [ ] Description explains when to use it
- [ ] Arguments are documented with hints
- [ ] Capabilities are scoped minimally

**Instructions**
- [ ] Context is gathered before analysis
- [ ] Steps are explicit and ordered
- [ ] Output format is specified
- [ ] Error handling is defined

**Integration**
- [ ] Works with related commands
- [ ] Supports composition patterns
- [ ] Handles edge cases gracefully
- [ ] Documentation is complete
