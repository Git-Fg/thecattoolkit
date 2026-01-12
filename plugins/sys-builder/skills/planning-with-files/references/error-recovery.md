# Error Recovery Patterns

Comprehensive guide to documenting, learning from, and recovering from errors in task_plan.md.

## Why Log Errors

### Benefits of Error Logging
1. **Pattern Recognition** - Identify recurring issues
2. **Prevention Strategy** - Develop safeguards
3. **Knowledge Building** - Learn from mistakes
4. **Recovery Guidance** - Know what to do next time
5. **Team Learning** - Share insights

### Anti-Pattern: Silent Retry
```
❌ DON'T:
Try API call → Fail → Retry → Succeed (no logging)

✅ DO:
Try API call → Fail → Log error → Add retry logic → Retry → Succeed
```

## Error Documentation Format

### Basic Error Entry
```markdown
## Errors Encountered
- [Timestamp] [Error]: [Resolution]
```

### Detailed Error Entry
```markdown
## Errors Encountered

### [Timestamp] - [Error Type]
**Error:** [What happened]
**Impact:** [How it affected the task]
**Root Cause:** [Why it happened]
**Resolution:** [How it was fixed]
**Prevention:** [How to avoid in future]
**Status:** [✅ Resolved / 🔄 In Progress / ⏳ Pending]
```

## Common Error Types

### Type 1: Tool/Technology Errors

#### API Failures
```markdown
### Error 1: API Timeout
- **Timestamp:** 2026-01-12 11:00
- **Error:** Request timeout after 30 seconds
- **Impact:** Could not fetch user data for analysis
- **Root Cause:** No timeout handling or retry logic
- **Resolution:** Implemented exponential backoff (3 retries, 1s, 2s, 4s)
- **Prevention:** Create API helper with built-in timeout and retry
- **Code Added:**
  ```python
  def api_call_with_retry(url, max_retries=3):
      for attempt in range(max_retries):
          try:
              return requests.get(url, timeout=30)
          except TimeoutError:
              if attempt == max_retries - 1:
                  raise
              time.sleep(2 ** attempt)
  ```
- **Status:** ✅ Resolved
```

#### Library/Dependency Issues
```markdown
### Error 2: Version Conflict
- **Timestamp:** 2026-01-12 14:30
- **Error:** Library X v2.0 incompatible with Library Y v1.5
- **Impact:** Cannot integrate features from both libraries
- **Root Cause:** Upgraded X without checking compatibility
- **Resolution:** Downgraded X to v1.8 (last compatible version)
- **Prevention:** Check compatibility matrix before upgrading
- **Action Item:** Schedule compatibility review for all dependencies
- **Status:** ✅ Resolved
```

#### Configuration Errors
```markdown
### Error 3: Missing Environment Variable
- **Timestamp:** 2026-01-12 09:15
- **Error:** DATABASE_URL not set in production
- **Impact:** Application failed to start
- **Root Cause:** Missing env var in deployment script
- **Resolution:** Added env var to deployment configuration
- **Prevention:** Add env var validation to startup script
- **Code Added:**
  ```python
  required_vars = ['DATABASE_URL', 'API_KEY']
  for var in required_vars:
      if not os.getenv(var):
          raise MissingEnvironmentVariable(f"{var} is required")
  ```
- **Status:** ✅ Resolved
```

### Type 2: Process Errors

#### Scope Creep
```markdown
### Error 4: Uncontrolled Scope Expansion
- **Timestamp:** 2026-01-12 16:00
- **Error:** Added 5 new features during implementation
- **Impact:** Task now 3x larger than original scope
- **Root Cause:** No scope control mechanism
- **Resolution:** Created "parking lot" list for future features
- **Prevention:**
  - Add scope review checkpoint every 2 phases
  - Require approval for any scope changes
  - Track original scope separately
- **Status:** ✅ Resolved
```

#### Incorrect Estimates
```markdown
### Error 5: Underestimated Complexity
- **Timestamp:** 2026-01-12 10:00
- **Error:** Estimated 2 hours, took 8 hours
- **Impact:** Delayed project by 6 hours
- **Root Cause:** Didn't account for edge cases
- **Resolution:** Adjusted remaining estimates based on actual data
- **Prevention:**
  - Add 50% buffer for complex tasks
  - Break down tasks more granularly
  - Track estimation accuracy
- **Lessons:** Data parsing always takes 3x longer than estimated
- **Status:** ✅ Resolved
```

### Type 3: Context/Communication Errors

#### Misunderstood Requirements
```markdown
### Error 6: Requirements Misinterpretation
- **Timestamp:** 2026-01-12 13:00
- **Error:** Built feature A instead of feature B
- **Impact:** 4 hours of work discarded
- **Root Cause:** Unclear requirements document
- **Resolution:** Rewrote requirements with examples
- **Prevention:**
  - Add "show me" examples to all requirements
  - Require stakeholder confirmation before building
  - Create quick prototype for validation
- **Status:** ✅ Resolved
```

#### Lost Context
```markdown
### Error 7: Forgot Original Goal
- **Timestamp:** 2026-01-12 15:30
- **Error:** Optimizing performance when goal was simplicity
- **Impact:** Made unnecessary architectural changes
- **Root Cause:** Didn't re-read task_plan.md before decision
- **Resolution:** Re-read plan, reverted changes
- **Prevention:**
  - Read task_plan.md before major decisions
  - Add decision checkpoint in workflow
  - Include goal reminder in status updates
- **Status:** ✅ Resolved
```

## Learning from Errors

### Pattern Analysis
```markdown
## Error Patterns Identified

### Pattern 1: External Dependencies
**Frequency:** 5 occurrences in 2 weeks
**Common Errors:**
- API timeouts (3x)
- Library conflicts (2x)
**Insight:** External dependencies are primary failure point
**Action:** Create reliability layer for all external calls
**Status:** [ ] In progress

### Pattern 2: Requirements Clarity
**Frequency:** 3 occurrences this month
**Common Errors:**
- Misinterpreted scope (2x)
- Missing details (1x)
**Insight:** Need better requirement validation
**Action:** Implement requirement review checklist
**Status:** [ ] Planned for next task

### Pattern 3: Estimation
**Frequency:** Underestimated 8 of 10 tasks
**Average Error:** 150% of estimate
**Insight:** Systematic over-optimism in estimates
**Action:** Use historical data for future estimates
**Status:** [ ] In progress
```

### Error Cost Tracking
```markdown
## Error Cost Analysis

### Time Wasted on Errors
- API failures: 4 hours
- Scope changes: 6 hours
- Misunderstood requirements: 8 hours
- Configuration issues: 2 hours
**Total:** 20 hours (25% of project time)

### Prevention Investment
- Created API helper: 2 hours
- Added validation: 1 hour
- Improved requirements template: 1 hour
**Total:** 4 hours

### ROI
- Prevented errors in future: Est. 16 hours saved
- Time to break-even: 1 project
**Verdict:** Worth the investment ✅
```

## Recovery Strategies

### Strategy 1: Immediate Recovery
When error occurs:
1. **Document** the error immediately
2. **Assess** impact on task
3. **Choose** recovery path
4. **Execute** fix
5. **Update** task_plan.md

```markdown
### Error Recovery Example
**Error:** Database migration failed
**Impact:** Cannot proceed with feature development
**Recovery Options:**
1. Rollback to previous version (5 min)
2. Fix migration script (2 hours)
3. Manual data fix (4 hours)

**Decision:** Option 2 - Fix migration script
**Reason:** Prevents future occurrence
**Time Cost:** 2 hours
**Outcome:** ✅ Successful, migration works
```

### Strategy 2: Learning Recovery
Transform error into learning:
1. Analyze root cause
2. Identify prevention
3. Create safeguards
4. Document for team
5. Update templates/processes

```markdown
### Learning Recovery Example
**Error:** Repeated API failures
**Root Cause:** No circuit breaker
**Prevention Strategy:**
- Implement circuit breaker pattern
- Add health checks
- Create fallback mechanisms
**Implementation Time:** 4 hours
**Future Savings:** Est. 20 hours
**Knowledge Transfer:** Shared pattern with team
```

### Strategy 3: Pivot Recovery
When stuck:
1. Acknowledge blocker
2. Explore alternative approaches
3. Document pivot decision
4. Adjust plan
5. Continue execution

```markdown
### Pivot Recovery Example
**Blocker:** Third-party API discontinued
**Original Plan:** Integrate with API X
**Pivot Decision:** Switch to API Y
**Impact:**
  - Lost: 3 hours integration time
  - Gained: Better features, similar cost
**New Plan:**
  - Use API Y instead
  - Estimated: 2 hours additional (more features)
**Outcome:** ✅ Successful, actually better result
```

## Prevention Mechanisms

### Proactive Checks
```markdown
## Prevention Checklist

Before Starting Work:
- [ ] Requirements reviewed with stakeholder
- [ ] Dependencies checked for compatibility
- [ ] Environment variables documented
- [ ] Error handling planned

During Implementation:
- [ ] Read task_plan.md before decisions
- [ ] Test assumptions early
- [ ] Validate progress against plan
- [ ] Log all errors immediately

After Each Phase:
- [ ] Review what went wrong
- [ ] Update prevention mechanisms
- [ ] Share learnings with team
- [ ] Adjust estimates based on reality
```

### Safety Nets
```markdown
## Safety Nets Implemented

### Technical Safety Nets
1. **API Helper Library**
   - Built-in retry logic
   - Circuit breaker pattern
   - Timeout handling
   - Error logging

2. **Environment Validation**
   - Startup checks for required vars
   - Clear error messages
   - Validation documentation

3. **Code Quality Gates**
   - Pre-commit hooks
   - Automated testing
   - Code review requirements

### Process Safety Nets
1. **Requirements Review**
   - Stakeholder sign-off required
   - Examples must be provided
   - Success criteria defined

2. **Estimation Buffer**
   - 50% buffer for complex tasks
   - Historical data for accuracy
   - Regular estimation reviews

3. **Progress Checkpoints**
   - Read task_plan.md before decisions
   - Phase completion reviews
   - Scope change approvals
```

## Error Recovery Templates

### Quick Recovery Template
```markdown
### Error: [Brief Description]
**Impact:** [How it affects the task]
**Fix:** [Immediate solution]
**Prevention:** [How to avoid next time]
**Time Cost:** [Hours spent]
**Status:** [Resolved/Pending]
```

### Detailed Recovery Template
```markdown
### Error: [Title]
- **Timestamp:** [Date and time]
- **Error Type:** [Tool/Process/Context]
- **Error:** [What happened]
- **Impact:**
  - Task impact: [How it affected progress]
  - Time impact: [Hours lost]
  - Quality impact: [Any degradation]

- **Investigation:**
  - Step 1: [What was tried]
    Result: [What was found]
  - Step 2: [What was tried]
    Result: [What was found]
  - Root Cause: [Why it happened]

- **Resolution:**
  - Immediate Fix: [What was done]
  - Verification: [How it was tested]
  - Outcome: [Result]

- **Prevention:**
  - Code Changes: [What was added]
  - Process Changes: [What was updated]
  - Documentation: [What was created]

- **Lessons Learned:**
  - [Insight 1]
  - [Insight 2]

- **Status:** [Resolved/Pending/In Progress]
- **Follow-up:** [Any future actions]
```

## Best Practices

### Do's
✅ Log ALL errors, no matter how small
✅ Include timestamps for pattern analysis
✅ Document root cause, not just symptoms
✅ Create prevention strategies
✅ Share learnings with team
✅ Track time spent on errors
✅ Update templates/processes based on learnings
✅ Celebrate error prevention wins

### Don'ts
❌ Don't hide or ignore errors
❌ Don't just fix and forget
❌ Don't blame tools or people
❌ Don't skip error logging to save time
❌ Don't repeat the same error twice
❌ Don't assume errors are one-time events
❌ Don't forget to update prevention mechanisms

### Tips
- Errors are learning opportunities
- Prevention is cheaper than recovery
- Patterns emerge from good logging
- Share errors to help the team
- Update your templates after errors
- Measure the cost of errors
- Celebrate error prevention
- Make error logging a habit
