# Implementation Patterns: Agent Development

## Pattern 1: Plan Mode Workflow

### Description
A structured approach to agent development emphasizing planning before implementation.

### When to Use
- Complex, multi-step tasks
- New feature development
- Refactoring projects
- Bug fixing with unclear root causes

### Structure
```
1. Research Phase
   - Analyze codebase
   - Identify patterns
   - Understand context

2. Clarification Phase
   - Ask targeted questions
   - Confirm assumptions
   - Fill knowledge gaps

3. Planning Phase
   - Create detailed plan (Markdown)
   - Define success criteria
   - Identify risks

4. Approval Phase
   - Present plan for review
   - Wait for approval
   - Refine based on feedback

5. Implementation Phase
   - Execute systematically
   - Validate at milestones
   - Iterate based on results
```

### Example Plan Template
```markdown
# Project Plan: User Authentication Refactor

## Objective
Refactor authentication system to support OAuth2 and improve security

## Current State Analysis
- Existing system: JWT-based authentication
- Pain points: No refresh tokens, security vulnerabilities
- Dependencies: express, jsonwebtoken, bcrypt

## Proposed Solution
1. Add OAuth2 provider support
2. Implement refresh token mechanism
3. Add rate limiting
4. Update security headers

## Implementation Steps
1. Audit current authentication flows
2. Research OAuth2 libraries
3. Design new architecture
4. Implement OAuth2 provider
5. Add refresh token logic
6. Implement security measures
7. Write comprehensive tests
8. Update documentation

## Success Criteria
- [ ] OAuth2 providers working (Google, GitHub)
- [ ] Refresh tokens implemented
- [ ] All tests passing
- [ ] Security audit passed
- [ ] Documentation updated

## Risks & Mitigation
- **Risk**: Breaking existing JWT flows
  - **Mitigation**: Backward compatibility layer
- **Risk**: OAuth2 complexity
  - **Mitigation**: Use established library (passport.js)

## Timeline
- Research: 1 day
- Design: 1 day
- Implementation: 3 days
- Testing: 1 day
- Documentation: 0.5 days
```

## Pattern 2: Context Discovery

### Description
Let agents find context through powerful search tools rather than manual file tagging.

### When to Use
- Exploring unfamiliar codebases
- Understanding project structure
- Finding related code
- Identifying patterns

### Implementation
```
Agent Instructions:
"Analyze the codebase structure and identify files related to user authentication.
Use search tools to find:
- Authentication middleware
- Login/logout handlers
- JWT token handling
- Security policies
Return a summary of findings with file paths."
```

### Benefits
- Reduces manual context preparation
- Leverages agent's search capabilities
- Discovers unexpected connections
- Adapts to project conventions

## Pattern 3: Rule & Skill Separation

### Description
Distinguish between static guidelines (Rules) and dynamic capabilities (Skills).

### Rules Implementation
**Location**: `.cursor/rules/`

**Example**: `RULE.md`
```markdown
# Code Style Guidelines

## TypeScript Standards
- Use strict mode
- Prefer interfaces over types for objects
- Use enums for constants
- Always specify return types

## React Patterns
- Functional components with hooks
- Props interfaces prefixed with component name
- Use forwardRef for reusable components
- Keep components under 200 lines

## Error Handling
- Always handle async errors
- Use try/catch with specific error types
- Log errors with context
- Never swallow errors silently
```

### Skills Implementation
**Location**: `SKILL.md` (in appropriate plugin)

**Example**: Authentication Skill
```markdown
# Authentication Skill

## Capabilities
- JWT token generation and validation
- OAuth2 provider integration
- Password hashing and verification
- Session management

## Usage Patterns
"Implement authentication for the new user dashboard"
-> Invokes authentication skill with dashboard context
```

## Pattern 4: Parallel Agent Execution

### Description
Run multiple agents simultaneously to explore different solutions, then compare results.

### When to Use
- Complex design decisions
- Multiple implementation approaches
- Research and exploration
- Code generation with different styles

### Implementation
```bash
# Create isolated worktrees
git worktree add solution-a feature-branch
git worktree add solution-b feature-branch

# Run agents in parallel
Agent A: Implement using strategy pattern
Agent B: Implement using factory pattern
Agent C: Implement using class-based approach

# Compare results
- Code quality
- Performance characteristics
- Maintainability
- Team preferences
```

### Git Worktrees Example
```bash
# Set up parallel environments
git worktree add ../agent-solution-1 feature/auth-v1
git worktree add ../agent-solution-2 feature/auth-v2

# In each environment, run different agent approaches
# Compare outputs and select best solution
```

## Pattern 5: Hypothesis-Driven Debugging

### Description
Debug complex issues through systematic hypothesis formation and evidence gathering.

### Process
```
1. Observe: What is the problem?
2. Hypothesize: What could cause this?
3. Test: Gather evidence to validate/invalidate
4. Analyze: What does the evidence show?
5. Iterate: Refine hypothesis based on findings
6. Fix: Implement solution based on evidence
7. Verify: Confirm fix resolves the issue
```

### Example Debug Session
**Problem**: Intermittent authentication failures in production

**Hypothesis 1**: Race condition in token validation
**Evidence Needed**:
- Check token validation timing
- Review concurrent request logs
- Examine token expiration handling

**Test**: Add instrumentation to track token validation timing

**Finding**: Token validation takes 50-200ms under load, sometimes expiring during validation

**Refined Hypothesis**: Clock skew between services
**Evidence**: Check service time synchronization

**Solution**: Implement clock skew tolerance in JWT validation

## Pattern 6: Multi-Layer Code Review

### Description
Implement multiple verification layers for quality assurance.

### Review Layers

#### 1. Real-Time Generation Review
- Watch agent during code generation
- Intervene for course correction
- Provide immediate feedback
- Address issues as they arise

**When**: Complex features, critical paths

#### 2. Post-Generation Review Pass
- Dedicated review session after completion
- Comprehensive analysis of changes
- Review architecture and design
- Check against standards

**When**: Feature complete, before merging

#### 3. Automated Review Tools
- Linting and formatting
- Security scanning
- Dependency analysis
- Performance profiling

**When**: Every commit, CI/CD pipeline

#### 4. Pull Request Review
- Team review for knowledge sharing
- Alternative perspective on design
- Catch edge cases
- Ensure maintainability

**When**: All changes to main branch

### Review Checklist Template
```markdown
## Code Review Checklist

### Functionality
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] Performance acceptable

### Design
- [ ] Follows project patterns
- [ ] Architecture is sound
- [ ] Code organization clear
- [ ] Dependencies minimized

### Quality
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Type definitions correct

### Security
- [ ] Input validation present
- [ ] No security vulnerabilities
- [ ] Authentication/authorization correct
- [ ] Sensitive data protected

### Maintainability
- [ ] Code is readable
- [ ] Comments clarify intent
- [ ] No duplication
- [ ] Easy to extend
```

## Pattern 7: Conversation Management

### Description
Manage conversation context to prevent confusion and maintain effectiveness.

### When to Start New Conversations
1. **Different Logical Tasks**
   - Moving from feature A to feature B
   - Switching from development to testing
   - Changing from frontend to backend work

2. **Agent Confusion**
   - Agent seems stuck or looping
   - Responses become irrelevant
   - Agent loses track of context

3. **Context Overflow**
   - More than 50 messages in conversation
   - Context window becoming full
   - Token usage becomes excessive

4. **Natural Completion Points**
   - After completing a feature
   - When shipping to production
   - After finishing code review

### Conversation Handoff
```markdown
# Conversation Handoff Summary

## Completed
- User authentication system implemented
- OAuth2 providers added (Google, GitHub)
- Refresh token mechanism working
- All tests passing

## Current Status
- Ready for production deployment
- Documentation updated
- Security audit passed

## Next Steps (New Conversation)
- Deploy to staging environment
- Performance testing
- User acceptance testing
- Production deployment plan

## Context Files
- `docs/auth-system.md` - System documentation
- `AUTH_PLAN.md` - Implementation plan
- `AUTH_REVIEW.md` - Code review results
```

## Pattern 8: Token Budget Management

### Description
Optimize token usage through progressive disclosure and efficient context management.

### Strategies

#### Progressive Disclosure
- **SKILL.md**: Core instructions (< 500 lines)
- **references/**: Detailed documentation (loaded on demand)
- **examples/**: Code examples (specific to task)
- **templates/**: Reusable patterns

#### Context Minimization
- Reference rather than include
- Use search for context discovery
- Leverage file-specific prompts
- Avoid copying large documents

#### Efficient Prompting
```markdown
# Inefficient
"Analyze the entire authentication system including all middleware,
controllers, models, and services. Review the database schema,
API documentation, and test files. Then implement OAuth2..."

# Efficient
"Analyze auth middleware in middleware/auth.js and login handler
in routes/auth/login.js. Implement OAuth2 following the patterns
you find. Use the JWT strategy already in use."
```

#### Zero-Context Scripts
- Put complex logic in scripts
- Scripts output only stdout
- No source code loaded into context
- Faster execution, lower token cost
