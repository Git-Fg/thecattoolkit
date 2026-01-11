# Background Agent Safety

## The Problem

Background agents run independently of the main conversation. If they prompt the user via `AskUserQuestion`, the process will hang indefinitely waiting for input that can never be provided.

## The Solution

Background agents must be designed for **complete autonomy**. They cannot rely on user interaction.

## Critical Constraints

### 1. No AskUserQuestion

**Never include `AskUserQuestion` in background agent tools:**

```yaml
# BAD - Will hang
---
name: background-worker
tools: [Read, Write, Bash, AskUserQuestion]
---

# GOOD - Autonomous
---
name: background-worker
tools: [Read, Write, Bash]
---
```

### 2. Autonomous Decision Making

Background agents must make decisions independently:

**Strategy:**
1. **Make assumptions:** When ambiguous, choose the most reasonable option
2. **Document choices:** Log assumptions in output or HANDOFF.md
3. **Provide alternatives:** If multiple valid approaches, note them
4. **Continue execution:** Never stop to ask

### 3. Error Handling

Background agents must handle errors without intervention:

**Pattern:**
```markdown
## Error Handling

If [error condition]:
1. Log error to output file
2. Attempt [recovery strategy]
3. If recovery fails, document in HANDOFF.md
4. Continue with next task (if possible)
```

## Background Agent Design

### Example: Long-Running Test

```yaml
---
name: test-runner
description: "MUST USE when running test suites in background."
tools: [Read, Write, Bash, Glob, Grep]
skills: [execution-core, software-engineering]
---

# Background Test Runner

Execute test suites autonomously in the background.

## Operational Protocol

1. **Discover Tests:** Find all test files
2. **Run Suite:** Execute tests with timeout
3. **Collect Results:** Gather output and results
4. **Report:** Write summary to `test-results.md`

## Error Handling

- **Test timeout:** Log and continue to next test
- **Missing dependencies:** Document in output
- **Test failures:** Report but don't stop
- **Framework errors:** Log and attempt recovery

## Output Format

Write results to `test-results.md`:
```markdown
# Test Results

## Summary
- Total: N tests
- Passed: X
- Failed: Y
- Skipped: Z

## Failures
[Details of failures]

## Next Actions
[Recommended fixes]
```

## Assumptions

If test configuration is ambiguous:
- Assume common test directory: `tests/`
- Assume test framework from package.json
- Use default timeout: 30 seconds per test
```

### Example: Parallel Analysis

```yaml
---
name: parallel-analyzer
description: "MUST USE when analyzing multiple codebases in parallel."
tools: [Read, Glob, Grep, Write]
---

# Parallel Codebase Analyzer

Analyze multiple directories in parallel background processes.

## Operational Protocol

For each target directory:
1. **Scan:** Identify file types and structure
2. **Analyze:** Apply analysis patterns
3. **Report:** Write summary to `results/{dir}-analysis.md`

## Autonomous Decisions

When facing ambiguity:
- **Language detected:** Use appropriate analysis patterns
- **Missing config:** Use default patterns
- **Large files:** Sample first 1000 lines
- **Binary files:** Skip and note

## Error Handling

- **Access denied:** Log and continue to next directory
- **Corrupted files:** Document and continue
- **Timeout:** Move to next target
```

## Handoff Protocol

When a background agent cannot proceed:

1. **Create HANDOFF.md:**
   ```markdown
   # Handoff - Background Task

   ## Completed
   - [List of completed work]

   ## Blocked
   - [Specific blocker]

   ## Assumptions Made
   - [Document all assumptions]

   ## Recommended Actions
   - [What should happen next]
   ```

2. **Terminate gracefully:** Report completion status

3. **Provide context:** Include all relevant state for resumption

## Timeout Management

Background agents should have timeout strategies:

### Short Tasks (< 5 minutes)
- No special handling
- Allow natural completion

### Medium Tasks (5-30 minutes)
- Periodic progress updates
- Checkpoint state to files

### Long Tasks (> 30 minutes)
- Explicit timeout configuration
- Progress reporting intervals
- Checkpoint/resume capability

**Pattern:**
```yaml
---
name: long-running-task
tools: [Read, Write, Bash]
---

# Long-Running Background Task

Execute multi-hour processing job.

## Timeout Strategy
- **Checkpoint interval:** Every 100 items
- **Progress file:** `progress.json` (updated every checkpoint)
- **Resume capability:** Can restart from last checkpoint

## Progress Reporting
Update `progress.json`:
```json
{
  "total": 1000,
  "completed": 450,
  "last_checkpoint": "2026-01-11T20:00:00Z"
}
```

## On Interruption
If interrupted, state is preserved in `progress.json`.
```

## Validation Checklist

- [ ] NO `AskUserQuestion` in tools
- [ ] Error handling defined for all scenarios
- [ ] Assumption documentation strategy
- [ ] Handoff protocol for blockers
- [ ] Timeout strategy appropriate for task length
- [ ] Progress reporting for long tasks
- [ ] Checkpoint/resume capability for critical work

## Common Pitfalls

| Pitfall | Consequence | Fix |
|:--------|:------------|:-----|
| `AskUserQuestion` in tools | Process hangs forever | Remove from tools |
| No error handling | Agent crashes on error | Add try/catch or fallback logic |
| Assumptions not documented | Unclear decisions | Log all assumptions |
| No timeout strategy | Agent never completes | Add timeouts and checkpoints |
| Progress not visible | Unclear if working | Add progress reporting |

## Integration Points

- **execution-core**: For behavioral standards (Uninterrupted Flow)
- **software-engineering**: For quality standards in autonomous execution
- **manage-healing**: For automatic error recovery
