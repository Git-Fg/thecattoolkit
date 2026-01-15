# Patterns & Best Practices

## The Big Ideas

### 1. Think First, Type Second

**The #1 productivity hack**: Press Shift+Tab twice (plan mode) before typing anything.

**Evidence**: 10 out of 10 times, plan mode produces better results than ad-hoc conversation.

**Why it works**:
- Forces you to think through architecture
- Prevents scope creep
- Reduces debugging time
- Improves output quality

### 2. Input Quality = Output Quality

**Fundamental truth**: Bad prompting = bad results.

If you're getting poor output with Claude Code, it's not the model—it's your prompting.

**Fix your input**:
- Be specific (not vague)
- Use constraints (not open-ended)
- Provide examples (not just descriptions)
- Explain why (not just what)

### 3. Context is Your Enemy

**Reality**: Context degrades at 40%, not 100%.

**Manage it proactively**:
- Scope conversations
- Use external memory
- Reset when needed
- Don't let it accumulate

### 4. Skills > Commands > Ad-hoc

**Hierarchy of automation**:

```
Skills (automatic, discovered)
  ↓
Commands (manual invocation)
  ↓
Ad-hoc prompts (one-off, no pattern)
```

Build skills for patterns you repeat.

## Proven Patterns

### Pattern 1: The Plan Mode Workflow

#### When to Use
- Any complex task (5+ steps)
- Architecture decisions
- Multi-phase implementations
- When you don't know where to start

#### How It Works
1. **Shift+Tab** twice → Plan mode
2. **Think** through the problem
3. **Ask** clarifying questions
4. **Create** a structured plan
5. **Get agreement** from Claude
6. **Execute** the plan

#### Example

**Before** (bad):
```
User: "Build me an auth system"
Claude: [makes assumptions, builds wrong thing]
User: "No, that's not right"
Claude: [tries again, still wrong]
[Loop continues]
```

**After** (good):
```
User: [Shift+Tab twice]
Claude: "I'm in plan mode. Let's think through this. What kind of auth system do you need? What features? What constraints?"
User: "Email/password auth. User model exists. Need sessions in Redis. Middleware for protected routes."
Claude: "Here's my plan:

## Auth System Implementation Plan

### Phase 1: Setup
- [ ] Review existing User model
- [ ] Set up Redis session store
- [ ] Install necessary dependencies

### Phase 2: Implementation
- [ ] Create login endpoint
- [ ] Create logout endpoint
- [ ] Create session middleware
- [ ] Create password validation

### Phase 3: Integration
- [ ] Add middleware to protected routes
- [ ] Create auth helper functions
- [ ] Update User model if needed

### Phase 4: Testing
- [ ] Test login flow
- [ ] Test logout flow
- [ ] Test protected routes

Does this plan look good? Any changes?"
User: "Looks perfect. Let's proceed."
Claude: [Executes plan successfully]
```

### Pattern 2: External Memory

#### When to Use
- Complex, multi-session projects
- When context >40%
- Long-running workflows
- Collaborative work

#### How It Works
1. **Create** a plan file
2. **Update** progress regularly
3. **Reference** file in new conversations
4. **Claude reads** and continues

#### Example Structure
```
my-project/
├── plan-feature.md
├── notes-architecture.md
└── .cattoolkit/
    └── context/
        ├── current-plan.md
        ├── decisions.md
        └── progress.md
```

#### Benefits
- Context doesn't bloat
- Progress persists
- Team can collaborate
- Easy to resume work

### Pattern 3: Skills for Patterns

#### When to Use
- Repeated workflows
- Team conventions
- Complex procedures you explain repeatedly

#### Example
- What: Code Review Skill

Create `~/.claude/skills/code-review/SKILL.md`:

```yaml
---
name: code-review
description: "Apply our team's code review standards. Use when reviewing PRs or code changes."
---

# Code Review Standards

## Security Checklist
- [ ] Input validation present
- [ ] No hardcoded secrets
- [ ] Proper authentication checks
- [ ] SQL injection prevention
- [ ] XSS protection

## Performance Checklist
- [ ] Database queries optimized
- [ ] No N+1 queries
- [ ] Proper indexing considered
- [ ] Efficient data structures

## Code Quality Checklist
- [ ] TypeScript strict mode
- [ ] No `any` types without reason
- [ ] Proper error handling
- [ ] Tests added/updated
- [ ] Documentation updated

## Review Process
1. Read the PR description
2. Check out the branch locally
3. Review each commit
4. Run tests
5. Apply checklist
6. Leave specific, actionable feedback
```

#### Auto-Discovery
When you ask "Review this PR", Claude sees the skill and applies it automatically.

### Pattern 4: Subagent Delegation

#### When to Use
- Large codebases (analyze without polluting main context)
- Parallel work (multiple agents on different tasks)
- Complex tasks (break into sub-tasks)
- Specialized work (security review, testing, etc.)

#### How It Works
1. **Identify** subtask suitable for delegation
2. **Invoke** subagent with specific prompt
3. **Receive** summary of findings
4. **Incorporate** into main task

#### Example: Security Review

```yaml
# Main conversation
User: "I need to review this PR for security issues"

# Delegate to security subagent
Claude (main): "I'll delegate this to our security review subagent to analyze the code changes for vulnerabilities."

Subagent (security): [Analyzes code]
Returns:
```
Security Findings:
- File: src/auth/login.ts, Line 45: SQL injection risk
- File: src/api/users.ts, Line 23: Missing authentication check
- Severity: 2 Critical, 1 High

Recommendation: Fix login.ts line 45 first.
```

Claude (main): "I found 3 security issues in this PR. Let's fix them..."
```

### Pattern 5: MCP Integration

#### When to Use
- GitHub workflows (PRs, issues)
- Database queries
- Team communication (Slack)
- Issue tracking (Jira, Linear)

#### Example: GitHub Workflow

```
User: "Create a feature branch for adding password reset"

Claude: [Uses GitHub MCP]
→ Creates branch: feature/password-reset
→ Creates PR: draft
→ Returns: PR URL and branch name

User: "Link this PR to Linear ticket ENG-1234"

Claude: [Uses Linear MCP]
→ Updates ticket: ENG-1234
→ Adds PR link
→ Sets status: In Progress
```

#### Compound Effect
Transform 5 context switches into 1 continuous session.

### Pattern 6: Copy-Paste Reset

#### When to Use
- Context >60%
- Output quality dropped
- Conversation went off track
- Claude is looping

#### How It Works
1. **Copy** important output
2. **Run** `/compact` for summary
3. **Run** `/clear` to reset
4. **Paste** essential info back

#### Example
```
Context is 75% full, Claude is confused.

1. Copy: Terminal test results showing 3 failures
2. Compact: "3 tests failing in auth module"
3. Clear: Context reset
4. Paste: "Fix 3 failing tests in src/auth/test.ts"
Result: Fresh start, focused on the issue
```

## Anti-Patterns

### Anti-Pattern 1: Never Use Plan Mode

**Symptoms**:
- Claude frequently misunderstood requirements
- Lots of back-and-forth corrections
- Implementation doesn't match vision
- Wasted time debugging

**Fix**: Always use plan mode for complex tasks.

### Anti-Pattern 2: Ad-hoc Everything

**Symptoms**:
- Explain the same thing repeatedly
- Inconsistent approaches
- Reinventing the wheel each time
- No team conventions

**Fix**: Create skills for repeatable patterns.

### Anti-Pattern 3: Let Context Bloat

**Symptoms**:
- Ignore context percentage
- Never reset conversations
- One conversation for entire projects
- Quality degrades over time

**Fix**:
- Monitor context indicator
- Use external memory
- Copy-paste reset when needed
- Scope conversations

### Anti-Pattern 4: Vague Prompting

**Symptoms**:
- "Build me a feature"
- "Fix this bug"
- "Improve this code"
- Claude makes wrong assumptions

**Fix**:
```
Instead of: "Add authentication"
Use: "Add email/password authentication using existing User model,
     sessions in Redis, middleware for /api/protected routes"
```

### Anti-Pattern 5: No External Memory

**Symptoms**:
- Lost context between sessions
- Can't remember what was done
- Restarting from scratch
- No progress tracking

**Fix**: Write plans and progress to files.

### Anti-Pattern 6: Ignoring Context Degradation

**Symptoms**:
- Continue working with poor output
- Compaction doesn't help
- Claude seems confused
- More context makes it worse

**Fix**: Recognize degradation at 40% and take action.

### Anti-Pattern 7: Skills Without Purpose

**Symptoms**:
- Creating skills for one-time use
- Skills that are too generic
- Skills with no clear trigger
- Not using progressive disclosure

**Fix**:
- Create skills for genuine patterns
- Use specific descriptions
- Follow progressive disclosure
- Test and refine

## Troubleshooting Guide

### Problem: Claude Keeps Making Mistakes

**Possible causes**:
1. Vague prompting → Be more specific
2. Missing context → Provide more information
3. Context degradation → Reset conversation
4. Wrong approach → Try different framing

**Solutions**:
- Use plan mode
- Provide examples
- Reset context
- Show instead of tell

### Problem: Context Bloated But Work Isn't Done

**Solutions**:
1. Copy-paste reset (preserve essentials)
2. External memory (write progress to file)
3. Continue in new conversation (reference file)

### Problem: Can't Find Right Files

**Solutions**:
1. Use Explore subagent (codebase search)
2. Describe what you're looking for
3. Use glob patterns
4. Ask Claude to help search

### Problem: Conversation Went Off Track

**Solution**: `/clear` and start fresh with essentials.

### Problem: Claude Is Looping

**Symptoms**:
- Tries same thing repeatedly
- Doesn't learn from corrections
- Can't escape error loop

**Solutions**:
1. Simplify the task
2. Show example of correct output
3. Try different approach
4. Clear and restart

### Problem: Team Not Following Conventions

**Solutions**:
1. Create skills for conventions
2. Update CLAUDE.md with rules
3. Use subagents for enforcement
4. Document in shared location

### Problem: Claude Too Slow

**Possible causes**:
- Complex prompts
- Large context
- Too many tools

**Solutions**:
1. Simplify prompts
2. Use external memory
3. Scope conversations
4. Use Sonnet for execution

### Problem: Lost Work Between Sessions

**Solutions**:
1. Write plans to files
2. Commit code regularly
3. Update progress notes
4. Use external memory pattern

## Best Practices Checklist

### Planning
- [ ] Use plan mode for complex tasks
- [ ] Get explicit agreement before implementation
- [ ] Document decisions in plan
- [ ] Break tasks into phases

### Prompting
- [ ] Be specific about requirements
- [ ] Explain constraints and context
- [ ] Provide examples when possible
- [ ] Tell Claude what NOT to do

### Context Management
- [ ] Monitor context indicator
- [ ] Use external memory for long projects
- [ ] Reset when context >60%
- [ ] Scope conversations appropriately

### Skills & Automation
- [ ] Create skills for repeatable patterns
- [ ] Use specific descriptions for discovery
- [ ] Follow progressive disclosure
- [ ] Test skills in real scenarios

### Subagents
- [ ] Use for large/complex tasks
- [ ] Design explicit output formats
- [ ] Scope narrowly
- [ ] Don't nest subagents

### MCP Integration
- [ ] Connect to essential services
- [ ] Review security for third-party servers
- [ ] Use for workflow integration
- [ ] Monitor usage

### Team Collaboration
- [ ] Share skills via project-level
- [ ] Document conventions in CLAUDE.md
- [ ] Use consistent file structures
- [ ] Version important plans

## The Compound Effect

### How Skills + Subagents + MCP Compound

**Individually**:
- Skills: Encode patterns
- Subagents: Handle complexity
- MCP: Connect services

**Together**:
```
Skill (encodes team conventions)
  ↓
Subagent (handles complex subtasks)
  ↓
MCP (connects external services)
  ↓
System that multiplies productivity
```

### Building Systems

**Instead of**:
- Using Claude reactively
- One-off interactions
- No setup investment

**Build systems**:
- Headless mode for automation
- Feedback loops for improvement
- Compound gains over time
- Continuous refinement

**Example**:
1. Create skills for team conventions
2. Build subagents for complex tasks
3. Connect MCP for workflow integration
4. Use headless mode for automation
5. Improve based on usage patterns
6. Compound benefits over months

## Summary

### Core Principles

1. GOOD **Think first** - Plan mode before typing
2. GOOD **Specific prompts** - Clear, constrained instructions
3. GOOD **Manage context** - Proactive, not reactive
4. GOOD **Build skills** - For patterns you repeat
5. GOOD **Use subagents** - For complex tasks
6. GOOD **Connect MCP** - Eliminate context switching
7. GOOD **Build systems** - Beyond one-off tasks

### The Mindset

**People who get the most from Claude Code**:
- Invest time in setup
- Build for patterns
- Use advanced features
- Think systematically
- Compound improvements

**vs. people who**:
- Use it reactively
- Don't invest in setup
- Ignore advanced features
- Think transactionally
- See diminishing returns

The difference isn't the model—it's the approach.

Next: Review [fundamentals.md](fundamentals.md) or [advanced-features.md](advanced-features.md) based on your needs.
