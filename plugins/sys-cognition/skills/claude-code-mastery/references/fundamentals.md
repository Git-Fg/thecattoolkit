# Claude Code Fundamentals

## 1. Think First: The Plan Mode Revolution

### Why Planning Matters

**The #1 mistake developers make**: Opening Claude Code and immediately starting to type.

**The reality**: 10 out of 10 times, using plan mode produces significantly better results than ad-hoc conversations.

### How Plan Mode Works

1. **Access**: Press `Shift+Tab` twice to enter plan mode
2. **Process**: Think through the architecture, requirements, and approach
3. **Output**: A structured plan that guides implementation
4. **Benefit**: Saves hours of debugging and rework

### When to Use Plan Mode

Always use plan mode for:
- Building features or systems
- Refactoring code
- Debugging complex issues
- Architecture decisions
- **Even small tasks** like summarizing emails

### Plan Mode Best Practices

1. **Think like an architect**: Consider the end state before starting
2. **Ask questions**: If you don't fully understand the requirements, ask
3. **Get explicit agreement**: Have Claude confirm the plan before implementation
4. **Document decisions**: Keep the plan visible throughout execution

**Example of good planning**:
> "I need to build email/password authentication. Requirements: Use existing User model, store sessions in Redis with 24-hour expiry, add middleware for /api/protected routes."

**Example of poor planning**:
> "Build me an auth system."

## 2. CLAUDE.md: Your Project's DNA

### What Is CLAUDE.md?

A markdown file Claude reads at the start of every conversation. It's your project's instruction manual.

### The 150-200 Instruction Limit

Claude can reliably follow ~150-200 instructions. The system prompt already uses ~50, leaving ~100-150 for your project.

**Implication**: Every instruction competes for attention. Keep it focused.

### What Makes a Good CLAUDE.md

#### ✅ Do This

**Keep it short**:
- Focus on the essential workflows
- Remove redundant information
- Update constantly (press `#` to auto-add)

**Make it specific**:
```
# Good
Use TypeScript strict mode because we've had production bugs
from implicit any types.

# Bad
We use TypeScript.
```

**Tell the why**:
- Explains the reasoning behind rules
- Helps Claude make better judgment calls
- Provides context for edge cases

**Update constantly**:
- Press `#` while working to add instructions
- Every time you correct Claude twice, add it to CLAUDE.md
- It becomes a living document of how your codebase works

#### ❌ Don't Do This

- **Don't make it a novel** (Claude will ignore things)
- **Don't include generic documentation** (Claude knows what components are)
- **Don't leave it outdated** (stale instructions cause errors)
- **Don't write for new hires** (write for yourself with amnesia)

### Example: Good vs Bad

**Bad CLAUDE.md** (documentation style):
```
# Our Codebase

We have a React frontend with TypeScript.

## Components
Components are in src/components/...

## API
We use REST APIs...

[500 more lines...]
```

**Good CLAUDE.md** (notes style):
```
# Build Commands
- Dev: `npm run dev`
- Build: `npm run build`
- Test: `npm test`

# Coding Standards
- TypeScript strict mode (production bugs from implicit any)
- Always use zod for runtime validation
- No `any` types without explicit opt-in

# Common Tasks
- Add feature: Create route + component + test
- Database changes: Use Prisma migrations
- Deploy: Push to main → Vercel auto-deploys

# Gotchas
- API base: https://api.ourapp.com (not localhost)
- Auth: Headers not cookies
- Env vars: All required in Vercel dashboard
```

## 3. Context Window Management

### The Claude Code Advantage

**Claude Code**: Consistent 200K token context window
**Other tools** (like Cursor): May truncate to 70-120K due to internal safeguards

This matters for large codebases where you need Claude to understand interconnected systems.

### The 40% Degradation Threshold

**Critical knowledge**: Context degrades at ~40%, not 100%.

**Pattern**:
- **<20%**: Optimal performance
- **20-40%**: Quality starts chipping away
- **>40%**: Significant degradation

**Warning sign**: If Claude Code compacts and output is still terrible, degradation happened *before* compaction.

### Context Management Strategies

#### 1. Scope Your Conversations

**Rule**: One conversation per feature or task.

**Why**: Contexts bleed together and Claude gets confused.

**Example**:
- Conversation 1: Build authentication system
- Conversation 2: Refactor database layer
- ❌ Don't do both in the same conversation

#### 2. External Memory

Write plans and progress to files that persist across sessions:

```
.my-project/
├── plan-auth.md          # Auth system plan
├── plan-database.md      # Database refactor plan
└── context/
    └── progress.md       # Current progress
```

**When you return**: Claude can read these files and continue where you left off.

**Best practice**: Keep these at the top level so they're visible in file search.

#### 3. The Copy-Paste Reset

When context gets bloated:

1. Copy important terminal output
2. Run `/compact` to get a summary
3. Run `/clear` to reset context
4. Paste back only the essential information

**Result**: Fresh context with critical information preserved.

**When to use**: When output quality drops or conversation goes off rails.

#### 4. Know When to Clear

**Trigger**: When you see these signs:
- Conversation has gone off the rails
- Accumulated irrelevant context
- Claude is confused or looping
- Context is >60% utilized

**Action**: Just `/clear` and start fresh.

**Reassurance**: CLAUDE.md persists, so project context isn't lost.

#### 5. The Stateless Mental Model

**Claude is stateless**. Every conversation starts from nothing except what you explicitly give it.

**Plan accordingly**:
- Provide necessary context upfront
- Don't assume Claude remembers previous conversations
- Use external files for continuity

## 4. Prompting: Input Quality = Output Quality

### The Fundamental Truth

> **Bad Input = Bad Output**

If you're getting bad results with Claude Code, your prompting needs work. The model is only as good as your instructions.

### What Actually Helps

#### 1. Be Specific About What You Want

**Vague**:
> "Build an auth system"

**Specific**:
> "Build email/password authentication using the existing User model, store sessions in Redis with 24-hour expiry, add middleware that protects routes under /api/protected."

#### 2. Tell It What NOT to Do

Claude 4.5 tends to over-engineer:
- Extra files
- Unnecessary abstractions
- Flexibility you didn't ask for

**Solution**:
> "Keep this simple. Don't add abstractions I didn't ask for. One file if possible."

#### 3. Give Context About Why

**Changes how Claude approaches the problem**:
- "We need this to be fast because it runs on every request"
- "This is a prototype we'll throw away"
- "This needs to handle 1M users"

#### 4. Show Instead of Tell

If Claude keeps misunderstanding:

```
Here's what the output should look like:
[minimal example]

Now apply this pattern to the rest.
```

### Prompting Best Practices

| Principle | Why | Example |
|-----------|-----|---------|
| **Specific > Vague** | Clear target for Claude | "Add logout button to navbar" vs "Add auth UI" |
| **Constraints > Open-ended** | Guides decision-making | "Use existing User model" vs "Create user system" |
| **Examples > Descriptions** | Concrete pattern to follow | Show code sample vs explain |
| **Why concept > What** | Context for judgment calls | Explain business requirement vs just task |

## 5. Model Selection

### Sonnet vs Opus

**Sonnet**:
- Faster and cheaper
- Excellent for execution tasks
- Clear path implementation
- Good for: writing boilerplate, refactoring, implementing features

**Opus**:
- Slower and more expensive
- Better for complex reasoning
- Good for: planning, architectural decisions, deep analysis

### The Workflow That Works

1. **Use Opus** (Shift+Tab) to plan and make architectural decisions
2. **Switch to Sonnet** for implementation
3. **Switch back to Opus** for review if needed

**Note**: Your CLAUDE.md ensures both models operate under the same constraints.

## 6. When Claude Gets Stuck

### Recognition Signs

- Tries the same thing repeatedly
- Fails, tries again, fails in loop
- Confidently implements wrong solution
- Can't be corrected after multiple attempts

### The Better Move: Change Approach

#### 1. Clear the Conversation

**Why**: Accumulated context might be confusing Claude.

**How**: `/clear` gives a fresh start.

#### 2. Simplify the Task

Break complex tasks into smaller pieces:
- Get each piece working before combining
- If Claude struggles with complex task → your plan mode was insufficient

#### 3. Show Instead of Tell

Write a minimal example yourself:
```
Here's what the output should look like.
Now apply this pattern to the rest.
```

#### 4. Be Creative

Try different framing:
- "Implement this as a state machine" vs "handle these transitions"
- Different angle might unlock progress

#### 5. Meta-Skill: Recognize Loops

**Rule**: If you've explained the same thing 3 times and Claude still doesn't get it, more explaining won't help.

**Action**: Change something about your approach.

## Summary: The Fundamentals

1. ✅ **Think first** → Use plan mode before typing
2. ✅ **Optimize CLAUDE.md** → Keep it short, specific, updated
3. ✅ **Manage context** → Proactive, not reactive
4. ✅ **Prompt well** → Specific, constrained, with examples
5. ✅ **Choose models wisely** → Opus for planning, Sonnet for execution
6. ✅ **Recognize when stuck** → Change approach, don't loop

Next: See [advanced-features.md](advanced-features.md) for skills, subagents, and MCP connectors.
