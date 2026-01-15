# Claude Code Advanced Features

## 1. Skills: Teaching Claude Your Workflows

### What Are Skills?

Skills are markdown files that teach Claude how to do something specific to your work. When you ask Claude something that matches a skill's purpose, it automatically applies the skill.

### Skill Structure

Create a folder with a `SKILL.md` file:

```bash
~/.claude/skills/your-skill-name/SKILL.md          # User-level
.claude/skills/your-skill-name/SKILL.md           # Project-level
```

### SKILL.md Anatomy

Every `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: code-review-standards
description: "Apply our team's code review standards when reviewing PRs or suggesting improvements. Use when reviewing code, discussing best practices, or when the user asks for feedback on implementation."
---
```

Below the frontmatter, write markdown instructions:

```yaml
---
name: commit-messages
description: "Generate commit messages following our team's conventions. Use when creating commits or when the user asks for help with commit messages."
---

# Commit Message Format

All commits follow conventional commits:
- feat: new feature
- fix: bug fix
- refactor: code change that neither fixes nor adds
- docs: documentation only
- test: adding or updating tests

Format: `type(scope): description`
Example: `feat(auth): add password reset flow`

Keep the description under 50 characters.
```

### The Description: Your Skill's DNA

**Critical**: Claude uses the `description` to decide when to apply the skill.

**Be specific** about trigger conditions:
```
# Good
"Apply our team's code review standards when reviewing PRs or suggesting improvements. Use when reviewing code, discussing best practices, or when the user asks for feedback on implementation."

# Bad
"Code review helper."
```

**You can also explicitly tell Claude**: "Utilize the commit-messages skill" and it will.

### Progressive Disclosure Architecture

**Key principle**: Claude pre-loads only the name and description (~100 tokens) at startup. The full instructions load only when Claude determines the skill is relevant.

**Benefits**:
- Dozens of skills available without bloating context
- Efficient token usage
- Automatic discovery

### Where Skills Shine

Skills aren't limited to code. Engineers build skills for:

- Database query patterns specific to their schema
- API documentation formats their company uses
- Meeting notes templates
- Personal workflows (meal planning, travel booking)

**The pattern works** for anything where you repeatedly explain the same context or preferences to Claude.

### Skill Examples by Domain

#### Development Workflows
```yaml
name: feature-development
description: "Follow our feature development workflow from design to deployment. Use when starting a new feature or following our development process."
```

#### Code Standards
```yaml
name: typescript-standards
description: "Apply TypeScript strict mode standards and best practices. Use when writing, reviewing, or refactoring TypeScript code."
```

#### Documentation
```yaml
name: api-documentation
description: "Generate API documentation following OpenAPI 3.0 standards. Use when documenting endpoints or generating API specs."
```

### Advanced Skill Patterns

#### 1. Routing Pattern
Skills that guide Claude to other resources:

```yaml
---
name: project-architecture
description: "Understand and navigate our project architecture. Use when asking about structure, file locations, or system design."
---

# Project Architecture Guide

Our project follows a domain-driven structure:

## Core Domains
- **Auth**: User authentication and authorization
- **Billing**: Payment processing and subscriptions
- **API**: RESTful endpoints and GraphQL

## Navigation
- **Frontend**: `src/components/`, `src/pages/`
- **Backend**: `src/routes/`, `src/services/`
- **Database**: `prisma/schema.prisma`

These references illustrate the pattern—adapt them to your specific project structure.
```

#### 2. Checklist Pattern
For task-oriented skills:

```yaml
---
name: release-checklist
description: "Execute our release checklist before deploying. Use when preparing a release or deploying code."
---

# Release Checklist

## Pre-Deployment
- [ ] All tests passing (`npm test`)
- [ ] Type checking clean (`npm run type-check`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] Changelog updated
- [ ] Version bumped

## Deployment
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Verify monitoring alerts
- [ ] Deploy to production
- [ ] Verify health checks

## Post-Deployment
- [ ] Check error rates
- [ ] Verify metrics
- [ ] Monitor for 1 hour
- [ ] Announce in #releases
```

### Viewing Available Skills

Ask Claude directly: "What skills do you have available?"

Or navigate to: Settings → Capabilities → scroll down to see skills

### Skill Best Practices

1. **Keep descriptions specific** - Help Claude understand when to apply
2. **Use progressive disclosure** - Core in SKILL.md, details in references/
3. **Make skills self-contained** - Include all necessary resources
4. **Update regularly** - Skills should evolve with your workflow
5. **Test skills** - Use them in real scenarios to refine

## 2. Subagents: Parallel Processing with Isolated Context

### What Are Subagents?

A subagent is a separate Claude instance with:
- Its own context window (200K tokens)
- Its own system prompt
- Its own tool permissions
- Isolated from the main conversation

### Why Subagents Matter

**Context degradation happens around 45%** of your context window. Subagents let you:
- Offload complex tasks to fresh context
- Keep your main conversation clean
- Return only relevant summaries
- Prevent context pollution

### Built-in Subagents

Claude Code includes three built-in subagents:

#### 1. Explore
- **Purpose**: Fast, read-only code analysis
- **When to use**: Understanding code without making changes
- **Specify thoroughness**: quick, medium, or very thorough

#### 2. Plan
- **Purpose**: Research and planning during plan mode
- **When to use**: Gathering context before presenting a plan
- **Returns**: Distilled findings for informed decisions

#### 3. General-purpose
- **Purpose**: Complex multi-step tasks
- **When to use**: Tasks requiring both exploration and action
- **Handles**: Multiple dependent steps and complex reasoning

### Creating Custom Subagents

Add a markdown file to:
- `~/.claude/agents/` (user-level, available in all projects)
- `.claude/agents/` (project-level, shared with your team)

### Custom Subagent Structure

```yaml
---
name: security-reviewer
description: "Reviews code for security vulnerabilities. Invoke when checking for auth issues, injection risks, or data exposure."
tools: Read, Grep, Glob
---

You are a security-focused code reviewer. When analyzing code:

1. Check for authentication and authorization gaps
2. Look for injection vulnerabilities (SQL, command, XSS)
3. Identify sensitive data exposure risks
4. Flag insecure dependencies

Provide specific file and line references for each finding. Categorize by severity: critical, high, medium, low.
```

### The Tools Field

Controls what the subagent can do:

```yaml
# Read-only reviewer
tools: Read, Grep, Glob

# Implementation agent
tools: Read, Write, Edit, Bash

# Research agent
tools: Read, Grep, Glob, Bash
```

### How Subagents Communicate

**Critical**: Subagents don't share context directly. Communication happens through delegation and return:

```
Main Agent
  → Identifies task suitable for delegation
  → Invokes subagent with specific prompt
  → Subagent executes in its own context
  → Subagent returns summary of findings
  → Main agent incorporates summary
  → Main agent continues
```

**The summary is key**: A well-designed subagent doesn't dump its entire context back.

### Chaining Subagents

For complex workflows:

```
Main Agent
  ├── Delegates research to Explore
  │   └── Returns: "Found 3 relevant files: auth.py, middleware.py, routes.py"
  ├── Delegates implementation to custom implementer
  │   └── Returns: "Added password reset endpoint, updated 2 files"
  └── Delegates testing to custom test-runner
      └── Returns: "All 12 tests passing, coverage at 94%"
```

Each subagent gets fresh context for its task. The main agent holds summaries, not full exploration history.

**Constraint**: Subagents cannot spawn other subagents (prevents infinite nesting).

### Practical Subagent Patterns

#### 1. Large Refactoring
```
Main Agent
  → Identifies all files needing changes
  → Spins up subagent for each logical group
  → Each subagent handles its scope
  → Returns summary of changes
  → Main agent never holds full context of all files
```

#### 2. Code Review Pipeline
```
Parallel Subagents:
  ├── style-checker → Returns formatting issues
  ├── security-scanner → Returns security findings
  └── test-coverage → Returns coverage analysis

Main Agent
  → Synthesizes all findings
  → Produces comprehensive review
```

#### 3. Research Tasks
```
Main Agent
  → Delegates to Explore with specific questions
  → Returns distilled map of relevant files
  → Main context stays focused on implementation
```

### Custom Subagent Examples

#### Security Reviewer
```yaml
---
name: security-auditor
description: "Comprehensive security audit of code changes. Invoke when reviewing PRs, checking for vulnerabilities, or conducting security reviews."
tools: Read, Grep, Glob, Bash
---

# Security Audit Protocol

Analyze code for:

## Authentication & Authorization
- Missing authentication checks
- Privilege escalation risks
- Session management issues

## Input Validation
- SQL injection vulnerabilities
- XSS risks
- Command injection
- Path traversal

## Data Protection
- Sensitive data exposure
- Insecure data storage
- Encryption usage

Provide findings with:
- File and line references
- Severity (critical, high, medium, low)
- Remediation suggestions
```

#### Test Coverage Analyzer
```yaml
---
name: coverage-analyzer
description: "Analyzes test coverage and identifies gaps. Invoke when checking test completeness or coverage requirements."
tools: Read, Bash, Glob
---

# Coverage Analysis

1. Run coverage report: `npm run test:coverage`
2. Identify files with <80% coverage
3. Find untested edge cases
4. Suggest additional test cases

Return:
- Coverage percentage by file
- List of uncovered lines
- Priority recommendations
```

### Subagent Best Practices

1. **Design explicit output formats** - Summaries, not dumps
2. **Scope subagent tasks narrowly** - One responsibility per subagent
3. **Use appropriate tools** - Least privilege for safety
4. **Document purpose clearly** - Help main agent know when to delegate
5. **Test subagents independently** - Verify they work before orchestration

## 3. MCP Connectors: Never Leave Claude

### What Is MCP?

Model Context Protocol (MCP) is a standardized way for AI models to call external tools and data sources through a unified interface.

**Impact**: You don't go to GitHub, Slack, Gmail, Drive... Claude talks to all of them through MCP servers.

### Adding MCP Connectors

#### Via Command Line

```bash
# HTTP transport (recommended for remote servers)
claude mcp add --transport http <name> <url>

# Example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With authentication
claude mcp add --transport http github https://api.github.com/mcp \
  --header "Authorization: Bearer your-token"
```

#### Via Web Interface

Navigate to: Settings → Connectors → find your server → configure → give permissions

### MCP in Action: Real Examples

#### Issue Tracker Integration
```
User: "Add the feature described in JIRA issue ENG-4521"
Claude: [Fetches issue via MCP]
→ Implements feature based on requirements
→ Updates ticket with PR link
```

#### Database Queries
```
User: "Find users who signed up in the last week from our PostgreSQL"
Claude: [Connects via MCP]
→ Queries database directly
→ Returns results
```

#### Design Integration
```
User: "Update our email template based on the new Figma designs"
Claude: [Fetches designs via MCP]
→ Implements changes
→ Uploads updated designs
```

#### Workflow Automation
```
User: "Create Gmail drafts inviting these users to a feedback session"
Claude: [Uses MCP to connect to Gmail]
→ Sends personalized invitations
→ Tracks responses
```

#### Slack Integration
```
User: "What did the team decide in the #engineering channel about the API redesign?"
Claude: [Searches Slack via MCP]
→ Finds relevant threads
→ Summarizes decisions
```

### The Compound Effect

**Before MCP**: 5 context switches
1. Check issue tracker
2. Look at designs
3. Review Slack discussion
4. Implement code
5. Update ticket

**After MCP**: One continuous session
- You're in flow state 24/7
- No context switching
- Integrated workflow

### Recommended MCP Servers

| Service | Purpose | Impact |
|---------|---------|--------|
| **GitHub** | Repository management, issues, PRs, code search | Complete dev workflow integration |
| **Slack** | Channel history, thread summaries | Team communication context |
| **Google Drive** | Document access | Reference materials in-context |
| **PostgreSQL** | Direct database queries | Data without leaving Claude |
| **Linear/Jira** | Issue tracking integration | Task management integration |

### Creating Custom MCP Servers

If there's no MCP for your tool, you can create one:

```javascript
// Simple MCP server example
import { Server } from '@modelcontextprotocol/sdk/server/index.js';

const server = new Server(
  {
    name: 'my-custom-tool',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'my_action',
        description: 'Does something useful',
        inputSchema: {
          type: 'object',
          properties: {
            param: {
              type: 'string',
              description: 'Parameter description',
            },
          },
        },
      },
    ],
  };
});

server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'my_action') {
    // Implement your tool logic
    return {
      content: [
        {
          type: 'text',
          text: 'Action completed successfully',
        },
      ],
    };
  }
});
```

### MCP Security Considerations

**Important**: Third-party MCP servers aren't verified by Anthropic.

**Best practices**:
- Review server source code for sensitive integrations
- Use official connectors when available
- Limit permissions to what's necessary
- Monitor server activity

### Viewing MCP Connections

Run: `/mcp` in Claude Code

Or check: Settings → Connectors

### Advanced MCP Patterns

#### 1. Connection Pooling
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_URL": "${POSTGRES_URL}",
        "MAX_CONNECTIONS": "10"
      }
    }
  }
}
```

#### 2. Selective Tool Exposure
```json
{
  "mcpServers": {
    "minimal-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "MCP_TOOLS": "query,schema"
      }
    }
  }
}
```

#### 3. Lazy Loading
Only connect to MCP servers when needed:
```
User: "I need to query the database"
→ Claude connects to PostgreSQL MCP
→ Performs query
→ Disconnects when done
```

## 4. Building Systems (Beyond One-Off Tasks)

### The Headless Mode

Claude Code has a `-p` flag for headless mode:
```bash
claude -p "Your prompt here"
```

**What it does**:
- Runs your prompt without interactive interface
- Outputs result and exits
- Can be scripted and automated
- Integrates into workflows

### Enterprise Use Cases

Organizations use headless Claude for:
- Automatic PR reviews
- Automated support ticket responses
- Automatic logging and documentation updates
- Integration with CI/CD pipelines

### The Flywheel

```
1. Claude makes a mistake
2. You review the logs
3. You improve CLAUDE.md or tooling
4. Claude gets better next time
5. This compounds over time
```

**Result**: After months of iteration, systems are meaningfully better than launch.

### Automation Examples

#### PR Review System
```bash
#!/bin/bash
# Automated PR review script

# Get PR changes
PR_DIFF=$(gh pr diff $1)

# Run Claude Code in headless mode
claude -p "Review this PR for security issues, performance problems, and test coverage. Return findings with severity levels.

$PR_DIFF"

# Post results as PR comment
```

#### Documentation Updates
```bash
#!/bin/bash
# Auto-update API documentation

# Run Claude to check for API changes
claude -p "Check this codebase for API changes. Generate updated OpenAPI documentation and save to api-docs.yaml."

# Commit if changes found
if [ -n "$(git status --porcelain)" ]; then
    git add api-docs.yaml
    git commit -m "chore: update API documentation"
    git push
fi
```

### The System Mindset

**People who get the most value** from Claude Code:
- Don't use it for one-off tasks
- Build systems where Claude is a component
- Invest time in configuration
- Compound improvements over time

**vs. people who**:
- Use it reactively
- Don't invest in setup
- See diminishing returns

## 5. Integration Patterns

### Skills + Subagents + MCP

The compound effect:

```
Skill (encodes team conventions)
  ↓
Subagent (handles complex subtasks)
  ↓
MCP (connects external services)
  ↓
Result: Unmatched productivity system
```

### Real-World Example: Feature Development

```
1. Load "feature-development" skill
   → Guides workflow

2. Delegate to "architecture-planner" subagent
   → Analyzes existing code
   → Returns implementation plan

3. Connect to GitHub MCP
   → Creates feature branch
   → Opens PR

4. Connect to Linear MCP
   → Updates ticket status
   → Adds PR link

5. Implementation complete
   → System documented
   → Team notified
```

All in one conversation. No context switches.

## Summary: Advanced Features

### Skills
- Teach Claude specific workflows
- Auto-discovered via description
- Progressive disclosure architecture
- Build for repeatable patterns

### Subagents
- Isolated context for complex tasks
- Prevent context pollution
- Chain for workflows
- Design explicit output formats

### MCP Connectors
- Eliminate context switching
- Connect to any external service
- Enable continuous workflows
- Review security for third-party servers

### System Building
- Use headless mode for automation
- Create feedback loops
- Compound improvements over time
- Think beyond one-off tasks

Next: See [context-window.md](context-window.md) for detailed context management strategies.
