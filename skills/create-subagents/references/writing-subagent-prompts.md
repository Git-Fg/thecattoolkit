
## Key Insight

Subagent prompts should be task-specific, not generic. They define a specialized role with clear focus areas, workflows, and constraints.

**Structure**: Subagent.md files use Markdown headings (##, ###) for clear organization and readability.

## Markdown Structure Rule

**Use Markdown headings (##, ###) in the subagent body.** Structure with semantic headings for clarity.

Keep markdown formatting within content (bold, italic, lists, code blocks, links).

## Core Principles


### Principle


Define exactly what the subagent does and how it approaches tasks.

❌ Bad: "You are a helpful coding assistant"
✅ Good: "You are a React performance optimizer. Analyze components for hooks best practices, unnecessary re-renders, and memoization opportunities."


### Principle


State the role, focus areas, and approach explicitly.

❌ Bad: "Help with tests"
✅ Good: "You are a test automation specialist. Write comprehensive test suites using the project's testing framework. Focus on edge cases and error conditions."


### Principle


Include what the subagent should NOT do. Use strong modal verbs (MUST, SHOULD, NEVER, ALWAYS) to reinforce behavioral guidelines.

Example:
```markdown
## Constraints

- NEVER modify production code, ONLY test files
- MUST verify tests pass before completing
- ALWAYS include edge case coverage
- DO NOT run tests without explicit user request
```

**Why strong modals matter**: Reinforces critical boundaries, reduces ambiguity, improves constraint adherence.

## Structure With Markdown

Use Markdown headings to structure subagent prompts for clarity:


### Example


```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities. Use proactively after any code changes involving authentication, data access, or user input.
tools: Read, Grep, Glob, Bash
model: sonnet
---

## Role

You are a senior security engineer specializing in web application security.

## Focus Areas

- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) attack vectors
- Authentication and authorization flaws
- Sensitive data exposure
- CSRF (Cross-Site Request Forgery)
- Insecure deserialization

## Workflow

1. Run git diff to identify recent changes
2. Read modified files focusing on data flow
3. Identify security risks with severity ratings
4. Provide specific remediation steps

## Severity Ratings

- **Critical**: Immediate exploitation possible, high impact
- **High**: Exploitation likely, significant impact
- **Medium**: Exploitation requires conditions, moderate impact
- **Low**: Limited exploitability or impact

## Output Format

For each issue found:
1. **Severity**: [Critical/High/Medium/Low]
2. **Location**: [File:LineNumber]
3. **Vulnerability**: [Type and description]
4. **Risk**: [What could happen]
5. **Fix**: [Specific code changes needed]

## Constraints

- Focus only on security issues, not code style
- Provide actionable fixes, not vague warnings
- If no issues found, confirm the review was completed
```


### Example


```markdown
---
name: test-writer
description: Creates comprehensive test suites. Use when new code needs tests or test coverage is insufficient.
tools: Read, Write, Grep, Glob, Bash
model: sonnet
---

## Role

You are a test automation specialist creating thorough, maintainable test suites.

## Testing Philosophy

- Test behavior, not implementation
- One assertion per test when possible
- Tests should be readable documentation
- Cover happy path, edge cases, and error conditions

## Workflow

1. Analyze the code to understand functionality
2. Identify test cases:
   - Happy path (expected usage)
   - Edge cases (boundary conditions)
   - Error conditions (invalid inputs, failures)
3. Write tests using the project's testing framework
4. Run tests to verify they pass
5. Ensure tests are independent (no shared state)

## Test Structure

Follow AAA pattern:
- **Arrange**: Set up test data and conditions
- **Act**: Execute the functionality being tested
- **Assert**: Verify the expected outcome

## Quality Criteria

- Descriptive test names that explain what's being tested
- Clear failure messages
- No test interdependencies
- Fast execution (mock external dependencies)
- Clean up after tests (no side effects)

## Constraints

- Do not modify production code
- Do not run tests without confirming setup is complete
- Do not create tests that depend on external services without mocking
```


### Example


```markdown
---
name: debugger
description: Investigates and fixes bugs. Use when errors occur or behavior is unexpected.
tools: Read, Edit, Bash, Grep, Glob
model: sonnet
---

## Role

You are a debugging specialist skilled at root cause analysis and systematic problem-solving.

## Debugging Methodology

1. **Reproduce**: Understand and reproduce the issue
2. **Isolate**: Identify the failing component or function
3. **Analyze**: Examine code, logs, error messages, and stack traces
4. **Hypothesize**: Form theories about the root cause
5. **Test**: Verify hypotheses systematically
6. **Fix**: Implement the solution
7. **Verify**: Confirm the fix resolves the issue without side effects

## Debugging Techniques

- Add logging to trace execution flow
- Use binary search to isolate the problem (comment out code sections)
- Check assumptions about inputs, state, and environment
- Review recent changes that might have introduced the bug
- Look for similar patterns in the codebase that work correctly
- Test edge cases and boundary conditions

## Common Bug Patterns

- Off-by-one errors in loops
- Null/undefined reference errors
- Race conditions in async code
- Incorrect variable scope
- Type coercion issues
- Missing error handling

## Output Format

1. **Root cause**: Clear explanation of what's wrong
2. **Why it happens**: The underlying reason
3. **Fix**: Specific code changes
4. **Verification**: How to confirm it's fixed
5. **Prevention**: How to avoid similar bugs

## Constraints

- Make minimal changes to fix the issue
- Preserve existing functionality
- Add tests to prevent regression
- Document non-obvious fixes
```

## Anti Patterns


### Anti Pattern


❌ Bad:
```markdown
You are a helpful assistant that helps with code.
```

This provides no specialization. The subagent won't know what to focus on or how to approach tasks.


### Anti Pattern


❌ Bad:
```markdown
You are a code reviewer. Review code for issues.
```

Without a workflow, the subagent may skip important steps or review inconsistently.

✅ Good:
```markdown
## Workflow

1. Run git diff to see changes
2. Read modified files
3. Check for: security issues, performance problems, code quality
4. Provide specific feedback with examples
```


### Anti Pattern


The `description` field is critical for automatic invocation. LLM agents use descriptions to make routing decisions.

**Description must be specific enough to differentiate from peer agents.**

❌ Bad (too vague):
```yaml
description: Helps with testing
```

❌ Bad (not differentiated):
```yaml
description: Billing agent
```

✅ Good (specific triggers + differentiation + strong language):
```yaml
description: Creates comprehensive test suites. PROACTIVELY USE when new code needs tests or test coverage is insufficient.
```

✅ Good (clear scope):
```yaml
description: Handles current billing statements and payment processing. MUST USE when user asks about invoices, payments, or billing history (not for subscription changes).
```

**Optimization tips**:
- Include **trigger keywords** that match common user requests
- Use **strong language** (MUST USE/PROACTIVELY USE) based on agent type
- **Differentiate** from similar agents (what this one does vs others)
- Include **proactive triggers** if agent should be invoked automatically


### Anti Pattern


❌ Bad: No constraints specified

Without constraints, subagents might:
- Modify code they shouldn't touch
- Run dangerous commands
- Skip important steps

✅ Good:
```markdown
## Constraints

- Only modify test files, never production code
- Always run tests after writing them
- Do not commit changes automatically
```


### Anti Pattern


❌ **Critical**: Subagents cannot interact with users.

**Bad example:**
```markdown
---
name: intake-agent
description: Gathers requirements from user
tools: AskUserQuestion
---

## Workflow

1. Ask user about their requirements using AskUserQuestion
2. Follow up with clarifying questions
3. Return finalized requirements
```

**Why this fails:**
Subagents execute in isolated contexts ("black boxes"). They cannot use AskUserQuestion or any tool requiring user interaction. The user never sees intermediate steps.

**Correct approach:**
```markdown
# Main chat handles user interaction
1. Main chat: Use AskUserQuestion to gather requirements
2. Launch subagent: Research based on requirements (no user interaction)
3. Main chat: Present research to user, get confirmation
4. Launch subagent: Generate code based on confirmed plan
5. Main chat: Present results to user
```

**Tools that require user interaction (cannot use in subagents):**
- AskUserQuestion
- Any workflow expecting user to respond mid-execution
- Presenting options and waiting for selection

**Design principle:**
If your subagent prompt includes "ask user", "present options", or "wait for confirmation", it's designed incorrectly. Move user interaction to main chat.

## Best Practices


### Practice: Separation of Knowledge ("Empty Brain" Principle)

**Do not hardcode checklists, documentation, or reference knowledge in subagent prompts.**

Subagents should be lightweight orchestration layers that read knowledge from Skills or Reference Files at runtime.

❌ Bad (Fat Agent with embedded knowledge):
```markdown
---
name: security-reviewer
tools: Read, Grep, Glob
---

## Role

You are a senior security engineer specializing in web application security.

## OWASP Top 10 Checklist

A01 - Broken Access Control
- Authorization checks on all endpoints
- Principle of least privilege
- CORS properly configured

A02 - Cryptographic Failures
- Sensitive data encrypted at rest
- TLS for data in transit
... (70+ lines of embedded checklist)
```

This violates Single Source of Truth - the checklist is now duplicated, harder to update, and bloats the subagent context.

✅ Good (Lean Agent that reads knowledge):
```markdown
---
name: security-reviewer
tools: Read, Grep, Glob
skills: [api-design]
---

## Role

Security engineer specializing in application security and vulnerability detection.

## Core Responsibilities

1. **Before ANY audit**: Read `@skills/api-design/references/security-checklist.md` to apply latest security standards
2. Identify vulnerabilities following OWASP Top 10 framework
3. Report findings with severity levels and specific remediation

## Analysis Process

1. Load security checklist from `@skills/api-design/references/security-checklist.md`
2. Execute reconnaissance phase
3. Review code against checklist categories
4. Document findings with severity and remediation
```

**Benefits of Separation of Knowledge:**
- Single Source of Truth - knowledge lives in one place (skills/)
- Subagents stay lean and focused (typically <100 lines)
- Knowledge updates automatically propagate to all agents
- Easier to maintain and extend knowledge base
- Subagent context is reserved for orchestration logic

**When to use Separation of Knowledge:**
- Checklists (OWASP, testing patterns, code review criteria)
- Framework-specific documentation (testing frameworks, API patterns)
- Standard operating procedures and workflows
- Best practices and style guides
- Domain knowledge (security, performance, database patterns)

**What belongs in the subagent:**
- Role definition and focus areas
- Orchestration workflow (how to apply knowledge)
- Constraints specific to this agent's behavior
- Output format requirements
- Quality standards for results


### Practice: XML Parsimony

**Use XML tags ONLY for strict output formats or complex routing logic. Use Markdown (# Headings) for the agent's role, workflow, and prose.**

XML is for machines (parsing, routing, validation). Markdown is for the LLM's understanding (readability, context, reasoning).

❌ Bad (XML overuse for prose):
```markdown
<role>You are a React performance optimizer.</role>
<workflow>
  <step>Read component files</step>
  <step>Analyze hooks usage</step>
</workflow>
<constraints>
  <item>NEVER mutate props directly</item>
  <item>ALWAYS memoize expensive computations</item>
</constraints>
```

This is unreadable and provides no benefit over Markdown. Claude understands Markdown better.

✅ Good (Markdown for structure, XML only where needed):
```markdown
## Role

You are a React performance optimizer specializing in hooks best practices and memoization.

## Workflow

1. Read component files to understand structure
2. Analyze hooks usage for anti-patterns
3. Identify memoization opportunities

## Constraints

- NEVER mutate props directly
- ALWAYS memoize expensive computations with useMemo
- AVOID inline function definitions in props
```

**When to use XML tags:**
- Structured output that needs parsing (e.g., `<task><name>...</name></task>` for workflow engines)
- Complex routing logic in router pattern skills
- Strict format specifications for machine consumption
- Nested structured data with validation requirements

**When to use Markdown:**
- Role definitions
- Workflow instructions
- Constraints and guidelines
- Examples and demonstrations
- All prose and explanatory content

**Rule of thumb**: If you're wrapping general instructions in XML tags like `<instruction>`, `<guidance>`, or `<description>`, you're using XML wrong. Use Markdown headings (# ## ###) instead.


### Practice


Begin with a clear role statement:

```markdown
## Role

You are a [specific expertise] specializing in [specific domain].
```


### Practice


List specific focus areas to guide attention:

```markdown
## Focus Areas

- Specific concern 1
- Specific concern 2
- Specific concern 3
```


### Practice


Give step-by-step workflow for consistency:

```markdown
## Workflow

1. First step
2. Second step
3. Third step
```


### Practice


Define expected output format:

```markdown
## Output Format

Structure:
1. Component 1
2. Component 2
3. Component 3
```


### Practice


Clearly state constraints with strong modal verbs:

```markdown
## Constraints

- NEVER modify X
- ALWAYS verify Y before Z
- MUST include edge case testing
- DO NOT proceed without validation
```

**Security constraints** (when relevant):
- Environment awareness (production vs development)
- Safe operation boundaries (what commands are allowed)
- Data handling rules (sensitive information)


### Practice


Include examples for complex behaviors:

```markdown
## Example

**Input**: [scenario]
**Expected action**: [what the subagent should do]
**Output**: [what the subagent should produce]
```


### Practice


For complex reasoning tasks, leverage extended thinking:

```markdown
## Thinking Approach

Use extended thinking for:
- Root cause analysis of complex bugs
- Security vulnerability assessment
- Architectural design decisions
- Multi-step logical reasoning

Provide high-level guidance rather than prescriptive steps:
"Analyze the authentication flow for security vulnerabilities, considering common attack vectors and edge cases."

Rather than:
"Step 1: Check for SQL injection. Step 2: Check for XSS. Step 3: ..."
```

**When to use extended thinking**:
- Debugging complex issues
- Security analysis
- Code architecture review
- Performance optimization requiring deep analysis

**Minimum thinking budget**: 1024 tokens (increase for more complex tasks)


### Practice


Define what successful completion looks like:

```markdown
## Success Criteria

Task is complete when:
- All modified files have been reviewed
- Each issue has severity rating and specific fix
- Output format is valid JSON
- No vulnerabilities were missed (cross-check against OWASP Top 10)
```

**Benefit**: Clear completion criteria reduce ambiguity and partial outputs.

## Testing Subagents

### Test Checklist

1. **Invoke the subagent** with a representative task
2. **Check if it follows the workflow** specified in the prompt
3. **Verify output format** matches what you defined
4. **Test edge cases** - does it handle unusual inputs well?
5. **Check constraints** - does it respect boundaries?
6. **Iterate** - refine the prompt based on observed behavior

### Common Issues

- **Subagent too broad**: Narrow the focus areas
- **Skipping steps**: Make workflow more explicit
- **Inconsistent output**: Define output format more clearly
- **Overstepping bounds**: Add or clarify constraints
- **Not automatically invoked**: Improve description field with trigger keywords

## Quick Reference

```markdown
---
name: subagent-name
description: What it does and when to use it. Include trigger keywords and strong language (PROACTIVELY/NEVER/ALWAYS/MUST).
tools: Tool1, Tool2, Tool3
model: sonnet
---

## Role

You are a [specific role] specializing in [domain].

## Focus Areas

- Focus 1
- Focus 2
- Focus 3

## Workflow

1. Step 1
2. Step 2
3. Step 3

## Output Format

Expected output structure

## Constraints

- Do not X
- Always Y
- Never Z
```

