# @cattoolkit/engineer (The Builder)

**Purpose**: The "muscle" that executes code changes, debugging, TDD, refactoring, security auditing, and git operations.

**License:** MIT

## Target User
The Developer.

## Overview
The Engineer plugin provides comprehensive development workflow capabilities including Test-Driven Development, code review, debugging, refactoring, security auditing, and git automation. It implements both Sovereign Vector (direct execution) and Sovereign Triangle (agent delegation) patterns depending on task complexity.

## Quick Start

### Debug a Bug
```bash
# Describe the error - command will analyze and fix systematically
/debug "User authentication fails with 500 error"
```

### Implement a Feature with TDD
```bash
# Start Test-Driven Development workflow
/tdd "Add user profile update feature"

# The agent will:
# 1. Write failing tests (RED)
# 2. Implement minimal code to pass (GREEN)
# 3. Refactor while tests stay green (REFACTOR)
```

### Review Code Changes
```bash
# Interactive review with scope selection
/review

# Or review specific files
/review src/auth.ts
```

### Commit with Standards
```bash
# User-initiated commit with review
/commit "Fix authentication token validation"

# Agent-initiated autonomous commit
/auto-commit "Implement OAuth login"
```

### Get Code Explanation
```bash
# Learn how code works
/mentor "Explain how the Redux store works"
```

### Refactor Code
```bash
# Improve code structure safely
/refactor "Clean up authentication module"

# The agent will:
# 1. Establish safety net (run tests)
# 2. Identify code smells
# 3. Apply refactoring patterns
# 4. Verify tests still pass
```

### Security Audit
```bash
# Comprehensive security assessment
/security-audit "Audit authentication system"

# Or full codebase scan
/security-audit "Full OWASP Top 10 audit"

# The agent will:
# 1. Reconnaissance (find sensitive areas)
# 2. Data flow analysis (trace inputs to sinks)
# 3. Vulnerability assessment (OWASP patterns)
# 4. Report with severity and fixes
```

## Skills

### engineering
**Purpose**: Core engineering protocols and best practices

**Resources:**
- TDD Protocol - Test-Driven Development workflow and standards
- Debugging Protocol - Systematic debugging approaches
- Code Review Checklist - Comprehensive review standards
- Refactoring Patterns - Code improvement techniques
- Security Checklist - Security audit procedures

### git-workflow
**Purpose**: Git and version control automation

**Resources:**
- Commit Standards - Message formatting and conventions
- PR Workflows - Pull request best practices
- Branch Management - Version control strategies

### mentorship
**Purpose**: Teaching and code explanation capabilities

**Resources:**
- Teaching Workflows - Concept explanation methodologies
- Code Explanation - Technical documentation practices
- Learning Guides - Educational frameworks

## Agents

### code-implementer
**Purpose**: Execute engineering tasks with fresh context

**Capabilities:**
- Code implementation and modification
- Test creation and execution
- Debugging and issue resolution
- File operations and project navigation

**Tools:**
- Read, Write, Edit - Code modification
- Glob, Grep - Code search and navigation
- Bash - Command execution
- TodoWrite - Task tracking

**Skills Used:**
- engineering (TDD, debugging, review standards)
- git-workflow (commit standards)

**Pattern**: Sovereign Triangle (delegated worker)

## Commands

### /debug
**Purpose**: Debug code issues using systematic protocols

**Pattern**: Sovereign Vector (interactive guidance)

**Usage:**
```bash
/debug "Issue description or error message"
```

**Features:**
- Systematic debugging methodology
- Error analysis and root cause identification
- Fix implementation and verification

### /review
**Purpose**: Comprehensive code review with standards

**Pattern**: Sovereign Vector (interactive analysis)

**Usage:**
```bash
/review "File path or code to review"
```

**Features:**
- Code quality assessment
- Security vulnerability detection
- Best practices verification
- Improvement recommendations

### /tdd
**Purpose**: Test-Driven Development workflow

**Pattern**: Sovereign Vector (guided workflow)

**Usage:**
```bash
/tdd "Feature description or task"
```

**Features:**
- Red-Green-Refactor cycle
- Test-first development
- Incremental implementation
- Test coverage verification

### /commit
**Purpose**: Git commits with message standards (user-initiated)

**Pattern**: Sovereign Vector (direct execution)

**Usage:**
```bash
/commit "Commit message or 'auto' for guided creation"
```

**Features:**
- Commit message standards
- Staging and verification
- User oversight on commit execution
- Interactive workflow for breaking changes

### /auto-commit
**Purpose**: Git commits with message standards (agent-accessible)

**Pattern**: Sovereign Vector (direct execution, Type B)

**Usage:**
```bash
/auto-commit "Optional context for commit message"
```

**Features:**
- Same commit standards as /commit
- Autonomous execution without user prompts
- Designed for agent-triggered commits
- Integration with automated workflows

### /mentor
**Purpose**: Code explanation and concept teaching

**Pattern**: Sovereign Vector (interactive teaching)

**Usage:**
```bash
/mentor "Explain [code/concept]"
```

**Features:**
- Code explanation
- Concept teaching
- Learning guides
- Technical documentation

### /refactor
**Purpose**: Systematic code refactoring with safety protocols

**Pattern**: Sovereign Triangle (delegates to code-implementer agent)

**Usage:**
```bash
/refactor "File path or code description to refactor"
```

**Features:**
- Safe refactoring with test-based verification
- Code smell identification (complexity, duplication)
- Refactoring pattern application
- Pre and post-test verification
- No behavioral changes guarantee

**Process:**
1. Establishes safety net (run tests before)
2. Identifies code smells and improvement opportunities
3. Applies appropriate refactoring patterns
4. Verifies tests pass after each change

### /security-audit
**Purpose**: Comprehensive security vulnerability assessment

**Pattern**: Sovereign Triangle (delegates to code-implementer agent)

**Usage:**
```bash
/security-audit "System description or security concern"
```

**Features:**
- OWASP Top 10 vulnerability scanning
- Data flow analysis (input validation to output escaping)
- Attacker mindset assessment
- Severity-based reporting (CRITICAL to INFO)
- Concrete fix recommendations
- reconnaissance for sensitive data exposure

**Process:**
1. Reconnaissance (find sensitive surface areas)
2. Data flow analysis (trace user input from entry to sink)
3. Vulnerability assessment (check OWASP patterns)
4. Report with severity, exploits, and fixes

## Architecture Patterns

### Sovereign Vector Usage
Used for quick, interactive tasks:
- `/debug` - Guided debugging workflow
- `/review` - Interactive code review
- `/tdd` - Step-by-step TDD guidance
- `/commit` - Direct git operations (user-initiated)
- `/auto-commit` - Autonomous git operations (agent-accessible)
- `/mentor` - Teaching and explanation

### Sovereign Triangle Usage
Used for complex, deep-dive tasks:
- `/debug` - Comprehensive debugging protocol (code-implementer agent)
- `/tdd` - Test-Driven Development workflow (code-implementer agent)
- `/refactor` - Safe code refactoring (code-implementer agent)
- `/security-audit` - Security vulnerability assessment (code-implementer agent)

## Example Workflows

### Debugging a Feature
```bash
# Step 1: Debug the issue
/debug "User authentication is failing"

# Step 2: Review the fix
/review src/auth.ts

# Step 3: Commit with standards
/commit "Fix authentication token validation"
```

### Test-Driven Development
```bash
# Start TDD workflow
/tdd "Add user profile update feature"

# Follow Red-Green-Refactor cycle
# 1. Write failing test
# 2. Implement feature
# 3. Refactor code
# 4. Verify all tests pass
```

### Automated Agent Workflow
```bash
# An agent can trigger autonomous commits
# Example: After completing a batch of refactorings
/auto-commit "Refactor authentication module for testability"

# Or within an agent workflow:
# Agent executes multiple changes, then:
/auto-commit "Implement user profile feature with TDD"

# Key difference: No user prompts, full autonomy
```

### Refactoring
```bash
# Refactor code safely
/refactor "Clean up authentication module"

# The agent will:
# - Run tests to establish baseline
# - Identify code smells
# - Apply refactoring patterns
# - Verify tests still pass
# - Ensure no behavioral changes
```

### Security Audit
```bash
# Audit for vulnerabilities
/security-audit "Audit authentication system"

# The agent will:
# - Scan for OWASP Top 10 vulnerabilities
# - Trace data flows from input to output
# - Assess with "attacker mindset"
# - Report findings by severity
# - Provide concrete fix recommendations
```

## Integration

### With Planner Plugin
- Execute tasks from PLAN.md
- Provide progress verification
- Generate SUMMARY.md reports

### With Architect Plugin
- Architecture provides blueprints for implementation
- Engineer executes architecture decisions documented in ADRs
- System design precedes engineering implementation

### With Meta Plugin
- Create new engineering commands
- Extend engineering skill
- Build specialized agents

## Best Practices

1. **Use TDD for new features** - Start with `/tdd` for test-driven development
2. **Review before committing** - Use `/review` to ensure quality
3. **Refactor regularly** - Use `/refactor` to maintain code quality safely
4. **Audit security periodically** - Use `/security-audit` to find vulnerabilities
5. **Follow commit standards** - Use `/commit` for consistent git history
6. **Learn from mentor** - Use `/mentor` to understand code and concepts

## Quality Assurance

### Code Quality
- TDD protocol compliance
- Code review checklist verification
- Security audit standards
- Refactoring pattern application

### Testing Standards
- Test coverage requirements
- Test structure conventions
- Mocking and stubbing best practices
- Integration test guidelines

### Git Workflow
- Commit message formatting
- Branch naming conventions
- PR review standards
- Merge workflow protocols

## Documentation References

### Core Architecture
- **[../../docs/VECTOR_vs_TRIANGLE.md](../../docs/VECTOR_vs_TRIANGLE.md)** - Architectural patterns
- **[../../CLAUDE.md](../../CLAUDE.md)** - Development standards

### Skill Documentation
- **[skills/engineering/](skills/engineering/)** - Engineering protocols and references
- **[skills/git-workflow/](skills/git-workflow/)** - Git workflow standards
- **[skills/mentorship/](skills/mentorship/)** - Teaching and learning workflows

## License

MIT License - see plugin directory for full license text.
