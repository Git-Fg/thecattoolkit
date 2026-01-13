# Handoff Protocols

## Overview

Handoff Protocols define how to pause, document, and resume execution when blocked by issues requiring human intervention.

## Handoff Triggers

### When to Create Handoff

**1. Authentication Gate**
```markdown
Type: AUTH_GATE
Trigger: API keys, credentials, or service access required
Action: Create handoff, pause execution
Example: AWS credentials needed for deployment
```

**2. Dependency Missing**
```markdown
Type: DEPENDENCY
Trigger: External service down, library unavailable, environment not configured
Action: Create handoff, pause execution
Example: PostgreSQL service not running
```

**3. Conflict**
```markdown
Type: CONFLICT
Trigger: Merge conflicts, dependency conflicts, version conflicts
Action: Create handoff, pause execution
Example: Git merge conflict in critical file
```

**4. Ambiguity**
```markdown
Type: AMBIGUOUS
Trigger: Unclear requirements, missing information, decision needed
Action: Create handoff, pause execution
Example: Unclear API specification
```

**5. Critical Error**
```markdown
Type: ERROR
Trigger: Build failure, test failure, system error
Action: Create handoff, pause execution
Example: Production build repeatedly failing
```

**6. External Decision**
```markdown
Type: DECISION
Trigger: Business decision required, stakeholder input needed
Action: Create handoff, pause execution
Example: Feature scope change needed
```

## Handoff Document Structure

### Standard Handoff Format

**Using Managing-Project-Plans Template:**

```markdown
# HANDOFF Required

**Reason:** {AUTH_GATE | CONFLICT | AMBIGUOUS | DEPENDENCY | ERROR | DECISION}

**Date:** {YYYY-MM-DD}
**Phase:** {XX - phase-name}
**Task:** {task-name}

## What Happened
{Detailed description of the blocker or issue}

## Current State
- **Completed Tasks:**
  - [x] {Task 1} - {completion details}
  - [x] {Task 2} - {completion details}

- **In Progress:**
  - [~] {Task N} - {current status}

- **Blocked On:**
  - {Specific blocker or issue}

## What You Need to Do
1. {Action 1 - specific and actionable}
2. {Action 2 - specific and actionable}
3. {Action 3 - specific and actionable}

## Verification
{How to confirm the fix has been applied}
- Command to run: `{command}`
- Expected result: {result}
- Alternative check: {alternative verification}

## Next Steps
After resolving the issue:
1. Restart execution
2. Verify the blocker is resolved
3. Continue with remaining tasks

## Context
{Additional context that might be helpful}
- Previous attempts: {what was tried}
- Error messages: {relevant error output}
- Related issues: {links or references}

## Attachments
- Log files: {path}
- Screenshots: {path}
- Error reports: {path}
```

## Handoff Examples

### Example 1: Authentication Gate

```markdown
# HANDOFF Required

**Reason:** AUTH_GATE

**Date:** 2026-01-12
**Phase:** 02 - Core Features
**Task:** Deploy to staging environment

## What Happened
Deployment failed due to missing AWS credentials. The deployment script requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to push Docker images to ECR.

## Current State
- **Completed Tasks:**
  - [x] Task 1: Setup Docker configuration
  - [x] Task 2: Create deployment scripts

- **In Progress:**
  - [~] Task 3: Deploy to staging (BLOCKED)

- **Blocked On:**
  - AWS credentials not configured

## What You Need to Do
1. Provide AWS_ACCESS_KEY_ID
2. Provide AWS_SECRET_ACCESS_KEY
3. Confirm ECR repository exists: `thecattoolkit-staging`

## Verification
Run: `aws sts get-caller-identity`
Expected: Should return your AWS account info without errors

## Next Steps
After resolving the issue:
1. Restart execution
2. Verify AWS credentials work
3. Continue with deployment task

## Context
- Deployment target: AWS ECR + ECS
- Region: us-east-1
- Repository: thecattoolkit-staging
- No sensitive data in logs
```

### Example 2: Merge Conflict

```markdown
# HANDOFF Required

**Reason:** CONFLICT

**Date:** 2026-01-12
**Phase:** 03 - Enhancement
**Task:** Add user dashboard

## What Happened
Git merge conflict detected in `src/components/Dashboard.js`. Two branches modified the same file with conflicting changes.

## Current State
- **Completed Tasks:**
  - [x] Task 1: Create dashboard layout
  - [x] Task 2: Add data fetching logic

- **In Progress:**
  - [~] Task 3: Merge dashboard changes (BLOCKED)

- **Blocked On:**
  - Merge conflict in src/components/Dashboard.js

## What You Need to Do
1. Resolve merge conflict in src/components/Dashboard.js
2. Choose which version to keep or merge both
3. Test the merged version
4. Commit the resolved changes

## Verification
Run: `git status`
Expected: No unmerged paths, clean working tree

Run: `npm test -- Dashboard.test.js`
Expected: All tests pass

## Next Steps
After resolving the issue:
1. Restart execution
2. Verify tests pass
3. Continue with remaining dashboard tasks

## Context
- Conflict file: src/components/Dashboard.js
- Both branches added different features:
  - Branch A: Added filtering
  - Branch B: Added pagination
- Need to preserve both features if possible
- Tests already written for both features
```

### Example 3: Dependency Issue

```markdown
# HANDOFF Required

**Reason:** DEPENDENCY

**Date:** 2026-01-12
**Phase:** 01 - Foundation
**Task:** Install dependencies

## What Happened
Package installation failed due to version conflict between dependencies. `package-lock.json` has conflicting requirements for `react-router-dom`.

## Current State
- **Completed Tasks:**
  - [x] Task 1: Setup project structure

- **In Progress:**
  - [~] Task 2: Install dependencies (BLOCKED)

- **Blocked On:**
  - npm install failing with dependency conflict

## What You Need to Do
1. Review dependency conflicts in package.json
2. Choose versions that are compatible
3. Update package.json if necessary
4. Run `npm install` again

## Verification
Run: `npm install`
Expected: Installation completes without errors

Run: `npm ls react-router-dom`
Expected: Shows single version installed

## Next Steps
After resolving the issue:
1. Restart execution
2. Verify all dependencies installed
3. Continue with project setup

## Context
- Conflicting packages: react-router-dom v6.10.0 vs v6.8.0
- Root cause: One dependency requires older version
- Recommended: Upgrade older dependency or pin react-router-dom
```

### Example 4: Ambiguous Requirements

```markdown
# HANDOFF Required

**Reason:** AMBIGUOUS

**Date:** 2026-01-12
**Phase:** 02 - Core Features
**Task:** Implement user authentication

## What Happened
Unclear requirements for authentication flow. Multiple authentication methods mentioned but no clear specification of which to implement first or what the complete flow should look like.

## Current State
- **Completed Tasks:**
  - [x] Task 1: Setup user database schema

- **In Progress:**
  - [~] Task 2: Implement authentication (BLOCKED)

- **Blocked On:**
  - Unclear authentication requirements

## What You Need to Do
1. Clarify authentication methods to implement (email/password, OAuth, SSO, etc.)
2. Define complete authentication flow (login, register, logout, password reset)
3. Specify which features are in-scope for this phase
4. Approve authentication approach

## Verification
Review requirements document and confirm:
- Authentication methods specified ✅
- Complete flow documented ✅
- In-scope features defined ✅
- Design approved ✅

## Next Steps
After clarification:
1. Restart execution
2. Implement authentication as specified
3. Continue with authorization tasks

## Context
- User mentioned: "Need authentication" and "Should support OAuth"
- Questions: Which OAuth providers? Email/password also? Multi-factor?
- Related: User management system being built
- Timeline: Authentication needed for Phase 3 features
```

## Handoff Lifecycle

### Phase 1: Detection

**Identify Blocker:**
```markdown
1. Task execution fails
2. Error detected
3. Automatic recovery attempted
4. Recovery fails
5. Blocker classified
```

### Phase 2: Documentation

**Create Handoff:**
```markdown
1. Use managing-project-plans handoff template
2. Fill all required sections
3. Include relevant context
4. Provide clear action items
5. Add verification steps
```

### Phase 3: State Update

**Update Status:**
```markdown
1. Update phase status [~] → [!]
2. Save execution state
3. Mark blocked task
4. Document handoff location
```

### Phase 4: Resolution

**User Action:**
```markdown
1. Review handoff document
2. Perform required actions
3. Verify resolution
4. Confirm ready to resume
```

### Phase 5: Resume

**Restart Execution:**
```markdown
1. Verify handoff resolved
2. Update phase status [!] → [~]
3. Load saved state
4. Continue task execution
5. Monitor for progress
```

## Handoff Management

### Tracking Handoffs

**Handoff Registry:**

```markdown
# Handoff Registry

## Active Handoffs

| ID | Phase | Task | Reason | Date | Status |
|----|-------|------|--------|------|--------|
| H001 | 02-Core | 03-Deploy | AUTH_GATE | 2026-01-12 | Open |
| H002 | 03-Enh | 01-Dashboard | CONFLICT | 2026-01-12 | Open |

## Resolved Handoffs

| ID | Phase | Task | Reason | Date | Resolved |
|----|-------|------|--------|------|----------|
| H000 | 01-Found | 02-Deps | DEPENDENCY | 2026-01-11 | 2026-01-11 |
```

### Handoff Quality Checklist

**Before Creating Handoff:**
- [ ] Blocker clearly identified
- [ ] Classification correct (AUTH_GATE, CONFLICT, etc.)
- [ ] All context included
- [ ] Actions specific and actionable
- [ ] Verification steps clear
- [ ] Template fully filled

**Before Resuming:**
- [ ] All actions completed
- [ ] Verification commands run
- [ ] Expected results confirmed
- [ ] Ready to continue
- [ ] State restored

## Best Practices

### Writing Effective Handoffs

**DO:**
- ✅ Be specific about the issue
- ✅ Provide clear action items
- ✅ Include relevant context
- ✅ Add verification steps
- ✅ Use template consistently
- ✅ Keep it professional

**DON'T:**
- ❌ Blame or criticize
- ❌ Include sensitive data
- ❌ Be vague or ambiguous
- ❌ Forget to include context
- ❌ Skip verification steps
- ❌ Leave actions unclear

### Common Mistakes

**Mistake 1: Vague Actions**
```markdown
❌ "Fix the issue"
✅ "Update package.json to use react-router-dom v6.10.0"
```

**Mistake 2: Missing Context**
```markdown
❌ "Build failed"
✅ "Production build failed with error: 'Module not found: Error: Cannot resolve './utils'"
✅ "File: src/utils/auth.js was deleted in commit abc123"
✅ "Context: Refactoring authentication module"
```

**Mistake 3: No Verification**
```markdown
❌ "AWS credentials configured"
✅ "Run 'aws sts get-caller-identity' and verify no errors"
```

## Quick Reference

### Handoff Checklist

**Creating Handoff:**
- [ ] Identify blocker type
- [ ] Use handoff template
- [ ] Fill all sections
- [ ] Include relevant logs
- [ ] Provide specific actions
- [ ] Add verification steps
- [ ] Update phase status
- [ ] Save execution state

**Resolving Handoff:**
- [ ] Review handoff document
- [ ] Perform required actions
- [ ] Run verification commands
- [ ] Confirm expected results
- [ ] Update handoff registry
- [ ] Notify execution to resume

### Handoff Types

```markdown
AUTH_GATE    - Credentials/API keys needed
CONFLICT     - Merge or dependency conflicts
AMBIGUOUS    - Unclear requirements
DEPENDENCY   - Missing external service
ERROR        - Critical errors
DECISION     - Business decision needed
```

### Handoff Status Codes

```markdown
[~] - In Progress (executing)
[!] - Blocked (handoff created)
[x] - Complete (finished successfully)
```

### Recovery Commands

```bash
# Verify Git state
git status
git log --oneline -5

# Verify dependencies
npm install
npm ls

# Verify AWS credentials
aws sts get-caller-identity

# Verify service status
curl http://localhost:5432
```
