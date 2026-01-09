# Handoff Protocol

## Purpose

Standard format for pausing execution when encountering blockers. Ensures consistent handoffs across all builder operations.

## When to Use Handoff

Create HANDOFF.md when:

- **Authentication Gates:** Credentials required (401/403 errors)
- **Critical Failures:** Unrecoverable errors
- **Ambiguous Requirements:** Task unclear or contradictory
- **Missing Dependencies:** Installation or setup required

## Standard Handoff Format

```markdown
# HANDOFF Required

**Reason**: [AUTH_GATE | CONFLICT | AMBIGUOUS | DEPENDENCY]

**What Happened**:
[Clear description of the issue or requirement]

**What You Need to Do**:
[Specific steps to resolve - commands, clicks, configuration]

**Verification**:
[How to confirm the issue is resolved]

**Next Step**:
Restart execution after [providing credentials | clarifying | installing]. I will verify the fix and continue execution.

**Context**:
- Phase: [current phase name]
- Task: [task that was blocked]
- Attempted: [what you tried]
```

## Reason Categories

### AUTH_GATE

**Trigger:** Authentication/authorization required

**Example:**
```markdown
**Reason**: AUTH_GATE

**What Happened**:
Attempted to deploy to Vercel but need authentication

**What You Need to Do**:
Run: `vercel login`

**Verification**:
Run: `vercel whoami` - should return your email

**Next Step**:
Restart execution after authentication
```

### CONFLICT

**Trigger:** Version control conflicts or resource conflicts

**Example:**
```markdown
**Reason**: CONFLICT

**What Happened**:
Git push rejected - remote has changes

**What You Need to Do**:
1. Run `git pull`
2. Resolve merge conflicts in files
3. Run `git add` and `git commit`

**Next Step**:
Restart execution after resolving conflicts
```

### AMBIGUOUS

**Trigger:** Task requirements unclear or contradictory

**Example:**
```markdown
**Reason**: AMBIGUOUS

**What Happened**:
Task specifies both REST and GraphQL APIs - unclear which to implement

**What You Need to Do**:
Choose implementation approach:
- REST: Traditional RESTful endpoints
- GraphQL: Single endpoint with queries/mutations

**Next Step**:
Restart execution after clarification
```

### DEPENDENCY

**Trigger:** Missing tools, packages, or system dependencies

**Example:**
```markdown
**Reason**: DEPENDENCY

**What Happened**:
Cannot run tests - pytest not installed

**What You Need to Do**:
Install pytest: `pip install pytest`

**Verification**:
Run: `pytest --version` - should show version

**Next Step**:
Restart execution after installation
```

## File Location

Save HANDOFF.md in the current working directory (project root or phase directory).

## After Handoff

1. **Agent terminates** - Do not wait
2. **Human resolves** the issue separately
3. **Agent resumes** - On restart, agent verifies fix and continues
4. **Document in SUMMARY.md** - Note handoff as normal flow

## Resume Protocol

When restarting after HANDOFF.md:

1. **Verify the fix** - Run the verification command specified
2. **Continue execution** - Pick up where left off
3. **Document the resolution** - In SUMMARY.md or next task log

## Integration with Observation Points

Handoff protocol works with observation-points.md:

- Use Self-Verification Points for normal task completion
- Use Handoff only for blockers that cannot be auto-verified
- Both follow Uninterrupted Flow principle (no waiting loops)

## Examples in Context

### During Plan Execution

```markdown
## Task 2: Deploy application

**Action**: Deploy to production environment

**Verify**: `curl https://myapp.com/health` returns 200

**Done**: Application deployed

---

**HANDOFF Required**

**Reason**: AUTH_GATE

**What Happened**:
Vercel CLI requires authentication before deployment

**What You Need to Do**:
Run: `vercel login`

**Verification**:
Run: `vercel whoami` should show your account

**Next Step**:
Restart execution after authentication
```

### During TDD Cycle

```markdown
## Test: User can login

**Action**: Write failing test for login functionality

**Verify**: `pytest tests/test_auth.py::test_login` fails as expected

**Done**: Failing test written

---

**HANDOFF Required**

**Reason**: DEPENDENCY

**What Happened**:
pytest not found - need to install test framework

**What You Need to Do**:
Install pytest: `pip install pytest`

**Verification**:
Run: `pytest --version`

**Next Step**:
Restart execution after installation
```

## Key Principles

1. **Clear and Specific:** Precise steps for resolution
2. **Verifiable:** Include how to confirm fix
3. **No Ambiguity:** Exact commands or actions needed
4. **Resume Path:** Clear next steps after resolution
5. **Standard Format:** Consistent across all operations
6. **Non-Blocking:** Agent exits, doesn't wait

## Benefits

- **Consistency:** Same handoff format everywhere
- **Clarity:** Human knows exactly what to do
- **Efficiency:** No back-and-forth clarification
- **Resume Path:** Clear restart instructions
- **Documentation:** Handoffs logged in project state
