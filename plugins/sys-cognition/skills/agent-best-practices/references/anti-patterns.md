# Anti-Patterns: What to Avoid

## Anti-Pattern 1: Over-Optimization of Rules

### Problem
Copying entire style guides, documentation, or command references into rules files.

### Example (Don't Do This)
```markdown
# .cursor/rules/CODING_STANDARDS.md

# Complete TypeScript Handbook (2000 lines)
[Entire TypeScript documentation copied here]

# Complete React Guide (3000 lines)
[Entire React documentation copied here]

# ESLint Rules (500 lines)
[All ESLint rules listed here]

# Every Git Command (1000 lines)
[Complete git command reference]
```

### Why It's Bad
- Rules become unmaintainable
- Context window pollution
- Slows down all agent interactions
- Information becomes stale
- Difficult to update

### Correct Approach
```markdown
# .cursor/rules/CODING_STANDARDS.md

# Key Standards
- Use TypeScript strict mode
- Prefer interfaces for object types
- Functional React components with hooks
- ESLint + Prettier for formatting

# References
- TypeScript: https://typescriptlang.org/docs
- React: https://react.dev
- Style Guide: See /docs/style-guide.md
- ESLint Config: See .eslintrc.js
```

## Anti-Pattern 2: Vague, Generic Prompts

### Problem
Using generic prompts without specific goals or context.

### Example (Don't Do This)
```
"Add authentication to the app"
"Fix the database issues"
"Improve performance"
"Add tests"
```

### Why It's Bad
- Agent must guess intent
- Results are unpredictable
- Wastes iteration cycles
- Produces suboptimal solutions
- Requires multiple corrections

### Correct Approach
```markdown
"Add OAuth2 authentication to the Express API at routes/auth/*.js,
following the JWT pattern in middleware/auth.js. Include Google
and GitHub providers. Add refresh tokens with 7-day expiry.
Write tests following the pattern in __tests__/auth.test.js"

"Fix database connection timeout issues in production. Add connection
pooling with 10 max connections. Implement exponential backoff
for retries (3 attempts, 1s, 2s, 4s delays). Add health check
endpoint at /health/database"

"Optimize API response times. Profile endpoints in routes/api/*.js.
Add caching for GET requests with 5-minute TTL. Implement database
query optimization for the user dashboard (see dashboard.js:45)"
```

## Anti-Pattern 3: No Conversation Management

### Problem
Running everything in one long conversation without boundaries.

### Example (Don't Do This)
- 200+ messages in a single conversation
- Mixing feature development, bug fixes, and refactoring
- Agent gets confused about current task
- Context window overflows
- Token costs skyrocket

### Why It's Bad
- Agent loses track of original goals
- Context becomes polluted with irrelevant information
- Performance degrades over time
- Difficult to review what was actually accomplished

### Correct Approach
```markdown
# Conversation 1: Feature Development
- Implement user authentication
- 50 messages total
- Ship to staging

# Conversation 2: Bug Fixes
- Fix authentication timeout issue
- 30 messages total
- Deploy hotfix

# Conversation 3: Refactoring
- Refactor authentication middleware
- 40 messages total
- Code review

# Handoff Documentation
See CONVERSATION_1_SUMMARY.md for what was accomplished
```

## Anti-Pattern 4: No Planning Before Implementation

### Problem
Jumping straight to coding without any planning or design phase.

### Example (Don't Do This)
```
User: "Add user profiles"
Agent: *immediately starts writing code*
[3 hours later]
User: "This isn't what I wanted"
```

### Why It's Bad
- Misaligned expectations
- Wasted development time
- Suboptimal architecture
- Difficult to maintain
- Technical debt accumulates

### Correct Approach
```markdown
1. User requests user profiles
2. Agent asks clarifying questions
3. Agent creates implementation plan
4. Plan is reviewed and approved
5. Agent implements according to plan
6. Results match expectations
```

## Anti-Pattern 5: Ignoring Agent Feedback

### Problem
Not heeding agent recommendations or concerns raised during development.

### Example (Don't Do This)
```
Agent: "Warning: This approach may cause memory leaks
in production. Consider using WeakMap instead."

User: "Just implement it as I asked"
[Later: Production outage due to memory leak]
```

### Why It's Bad
- Agent has valuable domain knowledge
- Warnings indicate real risks
- Learning opportunities missed
- Repeat mistakes

### Correct Approach
```markdown
Agent: "Warning: This approach may cause memory leaks
in production. Consider using WeakMap instead."

User: "Can you explain the memory leak risk
and show both approaches?"

Agent: [Provides explanation with examples]

User: "Use the WeakMap approach and add comments
explaining why it's needed"
```

## Anti-Pattern 6: Over-Engineering Simple Solutions

### Problem
Applying complex patterns to simple problems.

### Example (Don't Do This)
```typescript
// For a simple flag:
interface UserFlags {
  isAdmin: boolean;
  isVerified: boolean;
  isPremium: boolean;
}

class UserFlagManager {
  private flags: UserFlags;

  constructor(flags: UserFlags) {
    this.flags = flags;
  }

  getFlag(key: keyof UserFlags): boolean {
    return this.flags[key];
  }

  setFlag(key: keyof UserFlags, value: boolean): void {
    this.flags[key] = value;
  }

  toggleFlag(key: keyof UserFlags): void {
    this.flags[key] = !this.flags[key];
  }

  hasAllFlags(): boolean {
    return Object.values(this.flags).every(Boolean);
  }
}

// Usage:
const user = new UserFlagManager({ isAdmin: true, isVerified: false, isPremium: true });
```

### Correct Approach
```typescript
// Simple solution for simple problem:
interface User {
  isAdmin: boolean;
  isVerified: boolean;
  isPremium: boolean;
}

// Usage:
const user: User = { isAdmin: true, isVerified: false, isPremium: true };
```

## Anti-Pattern 7: No Verification or Testing

### Problem
Generating code without tests, validation, or verification.

### Example (Don't Do This)
```
Agent implements complex feature
No tests written
No manual testing
Deploys to production
Bugs discovered by users
```

### Why It's Bad
- Bugs reach production
- Difficult to debug
- No safety net for changes
- User experience suffers

### Correct Approach
```markdown
1. Implement feature with tests
2. Run all tests
3. Manual testing of critical paths
4. Code review
5. Deploy to staging
6. QA testing
7. Production deployment with monitoring
```

## Anti-Pattern 8: Premature Optimization

### Problem
Optimizing code before understanding performance requirements.

### Example (Don't Do This)
```typescript
// Before knowing if it's actually slow:
export class UltraOptimizedUserRepository {
  private cache = new Map<string, User>();
  private index = new Map<string, Set<string>>();

  async findByEmail(email: string): Promise<User | null> {
    // Complex caching logic
    // Memoization
    // Lazy loading
    // All before knowing if it's needed
  }
}
```

### Why It's Bad
- Wastes development time
- Adds complexity without benefit
- Harder to maintain
- Premature abstractions

### Correct Approach
```markdown
1. Implement simple solution first
2. Measure actual performance
3. Identify bottlenecks
4. Optimize only what matters
5. Verify improvements
```

## Anti-Pattern 9: Command-Centric Interaction

### Problem
Treating agents like command-line tools rather than collaborators.

### Example (Don't Do This)
```
"Execute: add auth middleware"
"Run: implement OAuth2"
"Perform: database migration"
"Execute task: fix bug #123"
```

### Why It's Bad
- Misses collaborative potential
- Agent becomes a simple executor
- Loses context and reasoning
- Inefficient use of capabilities

### Correct Approach
```markdown
"I'm working on adding OAuth2 authentication to our API.
Can you help me design the architecture? I'm considering
using passport.js but want to make sure it fits with our
existing JWT-based system."
[Agent engages as collaborator, provides design guidance]
```

## Anti-Pattern 10: No Context Handoff Between Conversations

### Problem
Starting new conversations without transferring context or learnings.

### Example (Don't Do This)
```
Conversation 1: Implement feature (50 messages)
Conversation 2: Fix bug in that feature (Agent doesn't know what was done)
Conversation 3: Add tests (Agent starts from scratch)
```

### Why It's Bad
- Duplicate work
- Lost knowledge
- Inconsistent decisions
- Wasted time

### Correct Approach
```markdown
# Conversation Handoff Document

## What Was Accomplished
- User authentication system implemented
- OAuth2 with Google and GitHub
- JWT with refresh tokens
- Rate limiting added

## Key Decisions
- Used passport.js for OAuth2
- JWT tokens expire in 1 hour
- Refresh tokens expire in 7 days
- Used Redis for token blacklisting

## Known Issues
- Token blacklisting needs testing under load
- Documentation link in welcome email is broken

## Next Steps
- Fix documentation link
- Add performance tests
- Implement token rotation

See: /docs/auth-implementation.md
```

## Anti-Pattern 11: Ignoring Code Review

### Problem
Skipping code review to save time, especially for agent-generated code.

### Example (Don't Do This)
```
Agent generates 1000 lines of code
"Looks good, ship it!"
[Production has critical bug]
```

### Why It's Bad
- Agent code needs review like any code
- Subtle bugs slip through
- Security issues missed
- Architecture problems undetected

### Correct Approach
```markdown
1. Agent generates code
2. Dedicated review session
3. Check architecture
4. Review edge cases
5. Verify tests
6. Security review
7. Performance analysis
8. Only then merge
```

## Anti-Pattern 12: Over-Reliance on Single Agent

### Problem
Using only one agent approach for all problems.

### Why It's Bad
- Agent has biases and limitations
- Single perspective
- Missed optimization opportunities
- No cross-validation

### Correct Approach
```markdown
# Parallel Approaches
Agent A: Implements using Strategy Pattern
Agent B: Implements using Factory Pattern
Agent C: Implements using Class-based Approach

# Compare Results
- Code quality
- Performance
- Maintainability
- Team preferences

# Select Best or Hybrid
```

## Summary: Key Takeaways

### DO
- Plan before implementing
- Use specific, contextual prompts
- Manage conversation boundaries
- Leverage agent as collaborator
- Implement multiple verification layers
- Start simple, add complexity as needed
- Document learnings and handoffs

### DON'T
- Over-optimize rules with copied content
- Use vague, generic prompts
- Run everything in one conversation
- Skip planning phase
- Ignore agent feedback
- Over-engineer simple solutions
- Skip testing and verification
- Treat agents as command executors
