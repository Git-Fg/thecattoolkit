# Execution Observation Points

## Core Principle

**Agents execute autonomously, self-verify via CLI, log results in SUMMARY.md, and continue without interruption.**

Plans execute in UNINTERRUPTED FLOW mode. There are no "Blocking Checkpoints" where agents wait for human input. Instead, agents:
1. Execute the task (implement, configure, build)
2. Run automated verification (CLI commands, tests)
3. Log the result in SUMMARY.md
4. Proceed to the next task

## Standard Pattern

### Self-Verification Point (Automated)

**When:** After completing a task, agent verifies success programmatically

**Pattern:**
```markdown
### Task 1: Create utility file

**Scope**: Utility functions module

**Action**: Create a utility file that will contain common helper functions for the application. The file should export functions for email validation, date formatting, and input sanitization.

**Verify**: `ls -la src/utils.ts` returns file exists
**Verify**: `head -5 src/utils.ts` contains function exports

**Done**: utils.ts created with exported functions

---

**Self-Verification Results:**
✓ File exists: src/utils.ts
✓ Contains exports: isValidEmail, formatDate, sanitizeInput
✓ No syntax errors detected
```

### Evidence Collection Point (Automated)

**When:** Agent collects verification evidence for phase review

**Pattern:**
```markdown
### Task 2: Configure Vercel deployment

**Scope**: Deployment configuration

**Action**: Deploy the application to Vercel using the CLI tool. This will make the application accessible via a public URL for testing and production use.

**Verify**: `vercel ls` shows deployment
**Verify**: `curl {url}` returns 200

**Done**: App deployed successfully

---

**Verification Evidence:**
```bash
# Deployment verification
vercel ls
✓ Production: https://myapp-abc123.vercel.app [1m ago]

# Health check
curl -s https://myapp-abc123.vercel.app/api/health
{"status":"ok"} ✓
```
```

### Phase Boundary Point (Automated Review)

**When:** End of phase, before SUMMARY.md creation

**Pattern:**
```markdown
## Phase Complete: Foundation

All tasks executed in UNINTERRUPTED FLOW mode.

**Verification Summary:**
- [x] User model created and validated
- [x] Login endpoint tested (200 response)
- [x] Build succeeds without errors
- [x] Deployed to production

**Evidence Logged:**
See: 01-foundation-SUMMARY.md for detailed verification results
```

## Key Differences: Old vs New

###  OLD: Blocking Checkpoint
```markdown
### Task 1: Build dashboard

**Action**: Create responsive dashboard

**Verify**: Build succeeds

**Done**: Dashboard builds successfully

### Checkpoint: Human Verification (Blocking)

**What Built**: Dashboard at /dashboard

**How to Verify**:
1. Run development server
2. Visit dashboard route
3. Test responsive breakpoints

**Resume Signal**: Type "approved" to continue
```

**Problem:** Agent waits for human input → Stop-and-Wait anti-pattern

###  NEW: Self-Verification Point
```markdown
### Task 1: Build dashboard

**Scope**: Dashboard module

**Action**: Create a responsive dashboard component that includes a sidebar for navigation, a header section, and a main content area. The dashboard should adapt to different screen sizes and include responsive design patterns.

**Verify**: Build succeeds
**Verify**: Dashboard component file exists
**Verify**: No compilation errors

**Done**: Dashboard component created and builds successfully

---

**Self-Verification Results:**
✓ Build completed: 0 errors, 0 warnings
✓ Component exists: src/components/Dashboard
✓ Route configured: /dashboard
✓ Responsive classes detected

**Evidence Collected:**
- Build log: dashboard build completed
- Component created
- Responsive breakpoints: 4 detected

Next: Continue to Task 2
```

**Benefit:** Agent verifies automatically → Uninterrupted Flow

## Observation Point Types

### 1. Self-Verification Point

**Purpose:** Agent confirms task completion programmatically

**Structure:**
```markdown
**Scope**: [Optional - describe the scope]

**Action**: [Natural language description of what needs to be done]

**Verify**: [CLI command 1]
**Verify**: [CLI command 2]

**Done**: [Measurable completion criteria]

---

**Self-Verification Results:**
✓ [Verification 1 passed]
✓ [Verification 2 passed]

Next: Continue to next task
```

**When to use:** After every task

### 2. Evidence Collection Point

**Purpose:** Collect detailed evidence for phase review

**Structure:**
```markdown
**Action**: [Implementation]

**Verify**: [Automated checks]

**Done**: [Completion criteria]

---

**Verification Evidence:**
```bash
# Command 1
[output]

# Command 2
[output]
```

**Metrics:**
- [Performance metric]
- [Quality metric]

Next: Continue to next task
```

**When to use:** Complex tasks or critical milestones

### 3. Phase Boundary Point

**Purpose:** Mark end of phase with comprehensive verification

**Structure:**
```markdown
## Phase Complete: [Name]

**Verification Summary:**
- [x] Task 1: Verified
- [x] Task 2: Verified
- [x] Task 3: Verified

**Evidence Logged:**
See: [phase]-SUMMARY.md for detailed results

**Next Phase Ready:**
[Status and prerequisites]
```

**When to use:** End of each phase

## Execution Protocol

When an agent encounters observation points:

1. **Execute** the task as specified
2. **Run verification commands** to confirm success
3. **Log verification results** in structured format
4. **Collect evidence** (CLI output, metrics, file changes)
5. **Continue to next task** without waiting for human input

**No waiting. No pausing. No checkpoint gates.**

## Benefits of Observation Points

### For Agents
- **Autonomy:** Execute without interruption
- **Clarity:** Clear verification criteria
- **Evidence:** Rich logs for review
- **Flow:** Continuous execution

### For Humans
- **Strategic Focus:** Review at phase boundaries, not every task
- **Evidence-Rich:** Detailed logs in SUMMARY.md
- **Clear Handoffs:** HANDOFF.md for blockers
- **Time Efficiency:** No terminal-sitting

### For Projects
- **Velocity:** Faster completion
- **Reliability:** Automated verification
- **Traceability:** Evidence-based progress
- **Scalability:** Works for any project size

## When to Use HANDOFF.md

Observation Points handle normal execution. Use HANDOFF.md only for:

- **Authentication Gates:** Credentials required
- **Critical Failures:** Unrecoverable errors
- **Ambiguous Requirements:** Task unclear
- **Missing Dependencies:** Installation required

**Pattern:**
```markdown
# HANDOFF Required

**Reason**: [AUTH_GATE | CONFLICT | AMBIGUOUS]

**What Happened**: [Description]

**What You Need to Do**: [Specific action]

**Verification**: [How to confirm it's fixed]

**Next Step**: Restart execution after providing [credentials | clarification | dependency]
```

## Migration Guide

### From Blocking Checkpoints

**Old Pattern:**
```markdown
### Checkpoint: Human Verification (Blocking)
**Resume Signal**: Type "approved"
```

**New Pattern:**
```markdown
**Self-Verification Results:**
✓ Automated checks passed
✓ Evidence collected

Next: Continue to Task 2
```

### From Decision Points

**Old Pattern:**
```markdown
### Checkpoint: Decision (Blocking)
**Resume Signal**: Select: option-a or option-b
```

**New Pattern:**
```markdown
**Decision Required**: [Moved to Planning Phase]

**Evidence Collected**: [Current state]

**Next**: HANDOFF.md created for human decision
```

### From Human Action

**Old Pattern:**
```markdown
### Checkpoint: Human Action (Blocking)
**Resume Signal**: Type "done"
```

**New Pattern:**
```markdown
**Action Required**: [Credentials needed]

**HANDOFF.md Created**: See file for instructions

**Status**: Execution paused, waiting for credentials
```

## Summary

Observation Points replace Blocking Checkpoints with automated verification and evidence collection. Agents execute in UNINTERRUPTED FLOW, verifying their work programmatically and logging evidence for human review at phase boundaries.

**Core Rule:** If you can verify it with CLI, verify it automatically. If you can't, create a HANDOFF.md and exit.
