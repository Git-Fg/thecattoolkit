# Authentication Gates

## Handling Authentication Errors During Execution

**When you encounter authentication errors during auto task execution:**

This is NOT a failure. Authentication gates are expected and normal. Handle them using the **Exit and Handoff** pattern.

## Authentication Error Indicators

- CLI returns: "Error: Not authenticated", "Not logged in", "Unauthorized", "401", "403"
- API returns: "Authentication required", "Invalid API key", "Missing credentials"
- Command fails with: "Please run {tool} login" or "Set {ENV_VAR} environment variable"

## Exit and Handoff Protocol

**CRITICAL:** Do NOT wait in a loop for user authentication. Instead:

1. **Recognize it's an auth gate** - Not a bug, just needs credentials
2. **STOP current task execution** - Don't retry repeatedly
3. **Create HANDOFF.md** - Document exact command needed from human
4. **EXIT process** - Terminate, don't wait in loop
5. **Human provides credentials** - Separate interaction
6. **Agent resumes** - On restart, continues from handoff point

## Example: Vercel Deployment

```
Task 3: Deploy to Vercel
Running: vercel --yes

Error: Not authenticated. Please run 'vercel login'

[Create HANDOFF.md and exit]

# HANDOFF Required

**Reason**: AUTH_GATE

**What Happened**:
I attempted to deploy to Vercel but encountered an authentication error.

**What You Need to Do**:
Run: `vercel login`

This will open your browser - complete the authentication flow.

**Verification**:
After completing authentication, run: `vercel whoami`
This should return your account email.

**Next Step**:
Restart execution after running `vercel login`. I will verify authentication and continue deployment.
```

**Human runs:** `vercel login` (in separate terminal/session)

**Agent resumes:** On restart, agent checks `vercel whoami` and continues deployment

## Example: Stripe API

```
Task 5: Create Stripe webhook endpoint
Using Stripe API...

Error: 401 Unauthorized - No API key provided

[Create HANDOFF.md and exit]

# HANDOFF Required

**Reason**: AUTH_GATE

**What Happened**:
I attempted to create a Stripe webhook endpoint but need your Stripe API key.

**What You Need to Do**:
1. Visit dashboard.stripe.com/apikeys
2. Copy your "Secret key" (starts with sk_test_ or sk_live_)
3. Set environment variable: `export STRIPE_SECRET_KEY=sk_test_...`

**Verification**:
After setting the key, I will verify Stripe API access with a test call.

**Next Step**:
Restart execution after providing the API key. I will verify it works and create the webhook endpoint.
```

**Human sets:** `export STRIPE_SECRET_KEY=sk_test_...`

**Agent resumes:** On restart, agent verifies key and creates webhook

## HANDOFF.md Template

```markdown
# HANDOFF Required

**Reason**: [AUTH_GATE | CONFLICT | AMBIGUOUS]

**What Happened**:
[Description of what you were trying to do]

**What You Need to Do**:
[Specific steps to resolve the issue]

**Verification**:
[How to confirm the issue is resolved]

**Next Step**:
Restart execution after [providing credentials | installing dependency | clarifying requirements]. I will verify the fix and continue execution.
```

## Error Types and Handling

### AUTH_GATE

**Trigger:** Authentication/authorization required

**Action:** Create HANDOFF.md with credential requirements

**Example:**
```markdown
**Reason**: AUTH_GATE

**What You Need to Do**:
Set environment variable: `export GITHUB_TOKEN=ghp_...`

**Verification**:
I will verify with: `gh api user`
```

### AMBIGUOUS

**Trigger:** Task requirements unclear or contradictory

**Action:** Create HANDOFF.md requesting clarification

**Example:**
```markdown
**Reason**: AMBIGUOUS

**What Happened**:
Task requirements are unclear - conflicting specifications for API endpoint.

**What You Need to Do**:
Clarify which specification should be implemented:
- Option A: REST-style endpoints
- Option B: GraphQL endpoints

**Next Step**:
Restart execution after clarification. I will implement according to your choice.
```

### CONFLICT

**Trigger:** Version control conflicts (git) or resource conflicts

**Action:** Create HANDOFF.md with resolution instructions

**Example:**
```markdown
**Reason**: CONFLICT

**What Happened**:
Git push rejected due to remote changes

**What You Need to Do**:
Resolve merge conflicts:
1. Run `git pull` to get latest changes
2. Resolve conflicts in files
3. Run `git add` and `git commit`

**Next Step**:
Restart execution after resolving conflicts. I will verify and continue.
```

## Documentation in Summary

Document authentication gates as normal flow, not deviations:

```markdown
## Authentication Gates

During execution, I encountered authentication requirements:

1. Task 3: Vercel CLI required authentication
   - Created HANDOFF.md with login instructions
   - Resumed after user ran `vercel login`
   - Deployed successfully

2. Task 5: Stripe API required API key
   - Created HANDOFF.md with key setup instructions
   - Resumed after user exported STRIPE_SECRET_KEY
   - Created webhook successfully

These are normal gates, not errors.
```

## Key Principles

- Authentication gates are NOT failures or bugs
- They're expected interaction points during first-time setup
- Handle them with **Exit and Handoff** pattern
- Create HANDOFF.md with clear instructions
- **NEVER wait in a loop** for user input
- Document them as normal flow, separate from deviations
- On restart, agents verify the fix and continue execution

## Differences: Old vs New

### ❌ OLD: Wait and Loop
```markdown
[Error occurs]

CHECKPOINT: Authentication Required
Please run: vercel login
Type "done" when authenticated

[Agent waits in loop]
```

### ✅ NEW: Exit and Handoff
```markdown
[Error occurs]

HANDOFF.md Created:
- Reason: AUTH_GATE
- Action: Run `vercel login`
- Next: Restart after authentication

[Agent exits]
```

**Benefit:** No token waste on waiting. Human handles auth separately.

See references/execution-observation-points.md for more on Uninterrupted Flow architecture.
