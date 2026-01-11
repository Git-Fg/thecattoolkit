# Multi-Skill Orchestration

## Purpose

Commands excel at orchestrating multiple skills, agents, or tools in a coordinated workflow.

## Orchestration Patterns

### Sequential Execution

Execute skills one after another, with each step building on the previous:

```yaml
---
description: "Complete release workflow"
allowed-tools: [Skill(version-bump), Skill(testing), Skill(deploy), Bash]
---

# Release Orchestrator

Execute complete release workflow:

## 1. Version Bump
Invoke `version-bump` to increment version in package.json

## 2. Testing
Invoke `testing` to run full test suite
**Abort if:** Tests fail

## 3. Build
Build production artifacts

## 4. Deploy
Invoke `deploy` to push to production

## 5. Verify
Run smoke tests against production
```

### Conditional Execution

Branch workflow based on conditions:

```yaml
---
description: "Smart deploy with conditional logic"
allowed-tools: [Skill(test), Skill(deploy-staging), Skill(deploy-prod), Bash]
---

# Smart Deploy

Conditional deployment workflow:

## Check Test Results
```bash
npm test 2>&1 | grep -q "passing"
```

## Branch
- **If tests pass:** Deploy to production
- **If tests fail:** Deploy to staging and notify
```

### Parallel Execution

Launch multiple agents in parallel:

```yaml
---
description: "Parallel security audit"
allowed-tools: [Task, Skill(audit-security)]
---

# Parallel Security Audit

Launch parallel security audits:

1. **Agent 1:** Audit `src/` directory
2. **Agent 2:** Audit `tests/` directory
3. **Agent 3:** Audit `scripts/` directory

**Merge** results into unified report
```

## Specifying Skill Order

List skills in `allowed-tools` in execution order:

```yaml
# Correct - explicit order
allowed-tools: [Skill(plan), Skill(build), Skill(test), Skill(deploy)]

# Also correct - grouped by phase
allowed-tools: [
  Skill(plan), Skill(analyze),
  Skill(build), Skill(test),
  Skill(deploy), Skill(verify)
]
```

## Error Handling

### Abort on Failure

```yaml
---
description: "Release with validation"
---

## Workflow
1. **Test:** Run full suite
   **Abort if:** Any test fails

2. **Lint:** Check code quality
   **Abort if:** Lint errors found

3. **Deploy:** Push to production
   **Rollback if:** Deployment fails
```

### Continue on Warning

```yaml
---
description: "Best-effort cleanup"
---

## Workflow
1. **Remove temp files:** `rm -rf tmp/`
   **Continue even if:** Directory doesn't exist

2. **Clear cache:** `npm cache clean`
   **Continue even if:** Cache is empty

3. **Report:** Summary of actions taken
```

## State Management

### Pass State Between Steps

```yaml
---
description: "Multi-phase build"
---

## Phase 1: Setup
Create build directory
**Output:** `./build/`

## Phase 2: Compile
Source: `src/` → Output: `./build/compiled/`

## Phase 3: Optimize
Input: `./build/compiled/` → Output: `./build/optimized/`

## Phase 4: Package
Input: `./build/optimized/` → Output: `./dist/package.tar.gz`
```

### Check State Before Execution

```yaml
---
description: "Resumable workflow"
---

## Check Previous State
```bash
if [ -f .workflow-state ]; then
  cat .workflow-state
fi
```

## Resume from Last State
- **If "phase-1-complete":** Start at Phase 2
- **If "phase-2-complete":** Start at Phase 3
- **Otherwise:** Start from beginning
```

## Complex Example: Multi-Environment Deployment

```yaml
---
description: "Multi-environment deployment pipeline"
allowed-tools: [Skill(test), Skill(deploy), Skill(verify), Task, Bash]
---

# Deployment Pipeline

Deploy to multiple environments with validation.

## Phase 1: Pre-Deployment

1. **Run Tests:** Full test suite
   **Abort if:** Tests fail

2. **Security Scan:** Check for vulnerabilities
   **Abort if:** Critical issues found

3. **Build:** Create deployment artifacts

## Phase 2: Staging Deployment

1. **Deploy to Staging:** Push artifacts to staging environment
2. **Smoke Tests:** Run basic functionality tests
   **Abort if:** Smoke tests fail

3. **Integration Tests:** Run full integration suite
   **Abort if:** Integration tests fail

## Phase 3: Production Deployment

1. **Create Backup:** Backup current production
2. **Deploy to Production:** Push artifacts to production
3. **Production Verification:** Run critical path tests
   **Rollback if:** Verification fails

## Phase 4: Post-Deployment

1. **Health Check:** Verify system health
2. **Monitor:** Watch for errors for 5 minutes
3. **Cleanup:** Remove old backups

## Rollback Procedure
If any phase fails:
1. Stop deployment
2. Restore from backup
3. Notify team
4. Log incident
```

## Best Practices

1. **Document dependencies:** Clearly state which steps depend on others
2. **Handle errors:** Specify abort/continue behavior
3. **Verify outputs:** Check results before proceeding
4. **Enable rollback:** Provide recovery path for failures
5. **Log state:** Track workflow progress for resumption

## Integration with Skills

- **meta-skills:** For skill standards invoked in orchestration
- **meta-agents:** For agent patterns spawned in workflows
- **toolkit-registry:** For discovering available skills
