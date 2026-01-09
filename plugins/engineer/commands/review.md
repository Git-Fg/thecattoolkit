---
description: |
  Execute systematic code review protocol using autonomous agent for comprehensive analysis and quality assessment.
  <example>
  Context: User wants code review
  user: "Review my changes before I commit"
  assistant: "I'll delegate to the review agent for comprehensive code analysis."
  </example>
  <example>
  Context: Pull request review
  user: "Review this PR for issues"
  assistant: "I'll use the review command to analyze the pull request."
  </example>
  <example>
  Context: Security-focused review
  user: "Review our authentication code for vulnerabilities"
  assistant: "I'll delegate for security-focused review of the authentication system."
  </example>
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
argument-hint: [files, PR, or changes to review]
disable-model-invocation: true
---

## Objective
Execute code review workflow for: $ARGUMENTS

## Deep Discovery Phase

Before delegating to the agent, gather comprehensive context to ensure thorough code analysis.

### Step 1: Analyze Review Request

Determine the nature of the code review:

**Analyze $ARGUMENTS to classify:**
- **Staged Changes**: Review `git diff --staged` before commit
- **Working Directory**: Review uncommitted changes
- **Specific Files**: Review particular files or directories
- **Pull Request**: Review entire PR or branch
- **Focused Review**: Security, performance, or correctness focus

### Step 2: Map Project Context

Gather essential project information:

**Technology Stack Identification:**
- Identify language and framework
- Identify test framework and runner
- Identify code quality tools (linters, formatters, type checkers)

**Project Structure Mapping:**
- Locate affected source files
- Identify related files and dependencies
- Check test coverage for reviewed code
- Locate configuration files

**Version Control State:**
```bash
git status
git diff --staged  # For staged reviews
git diff HEAD      # For PR reviews
git log --oneline -5
```

### Step 3: Determine Review Focus

Clarify the primary review concerns:

**Review Categories:**
- **Correctness**: Bugs, edge cases, error handling, logic errors
- **Security**: Vulnerabilities, input validation, authentication/authorization
- **Performance**: Inefficiencies, bottlenecks, resource management
- **Code Quality**: Maintainability, readability, naming, structure
- **Testing**: Test coverage, test quality, edge case coverage
- **Documentation**: Comments, docstrings, README accuracy

### Step 4: Delegation Package

Compile all gathered context into a comprehensive assignment for the code-implementer agent.

## Delegation Phase

<assignment>
Execute the code review workflow from the engineering skill to review: $ARGUMENTS

**Context Provided:**
- Review Type: [staged changes / working directory / specific files / PR / focused]
- Technology Stack: [language, framework, test framework, quality tools]
- Project Structure: [affected files, related files, tests, configuration]
- Review Focus: [correctness / security / performance / code quality / testing / documentation]
- Git State: [current branch, recent commits, diff summary]

**Follow the systematic code review protocol:**
1. **Context Gathering**: Read affected files and understand changes
2. **Analysis**: Apply review checklist based on focus area
3. **Categorization**: Group findings by severity (CRITICAL/WARNING/NIT)
4. **Documentation**: Provide specific file:line references for all findings

**Work autonomously using Uninterrupted Flow:**
- Read and analyze all affected files
- Use grep/search to find related code patterns
- Run tests if available to verify behavior
- Log all findings with precise references
- Create HANDOFF.md only for critical access blockers
- DO NOT use AskUserQuestion during execution

**Review Checklist:**
- Read the code review protocol from the engineering skill
- Check for security vulnerabilities (OWASP patterns)
- Verify error handling and edge cases
- Assess code complexity and readability
- Check for proper testing coverage
- Verify documentation accuracy
- Look for performance issues
- Check for proper resource cleanup

**Output Format:**
Create a structured review report with:
- **[CRITICAL]**: Must fix immediately (Bug/Security)
- **[WARNING]**: Strong recommendation (Tech debt)
- **[NIT]**: Style/Preference

Each finding must include:
- File:line reference
- Category (security/performance/correctness/style)
- Description of the issue
- Concrete fix suggestion (for CRITICAL/WARNING)
</assignment>

<context>
You are executing in isolated context to perform comprehensive code review. The engineering skill provides systematic review protocols and quality checklists.
All relevant project context has been gathered for you.
</context>

Execute via code-implementer agent.

## Success Criteria

- [ ] Review type properly classified
- [ ] Project context fully mapped (stack, structure, tests)
- [ ] Review focus clarified
- [ ] Agent receives comprehensive context package
- [ ] All affected files analyzed
- [ ] Findings categorized by severity
- [ ] Each finding includes file:line reference
- [ ] Critical findings include concrete fix suggestions
