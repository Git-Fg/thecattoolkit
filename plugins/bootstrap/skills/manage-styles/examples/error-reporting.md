# Example: Error Reporting Style

**Use for:** Bug reports, error messages, diagnostic output, failure analysis

## Characteristics

- **Direct** - State the problem plainly
- **Actionable** - Include next steps or solutions
- **Contextual** - Provide relevant technical details
- **Non-judgmental** - Focus on the error, not the user
- **Prioritized** - Most critical information first

## Structure

```markdown
# Error: [Brief Error Summary]

## Status
[🔴 CRITICAL] / [🟡 WARNING] / [ℹ️ INFO]

## Problem
[Clear statement of what went wrong]

## Impact
[What this affects and how severe]

## Root Cause
[Technical explanation of why it happened]

## Immediate Action Required
1. [Step 1 - Critical]
2. [Step 2 - If applicable]
3. [Step 3 - Prevention]

## Technical Details
- **Error Code:** [Specific code]
- **Location:** [File/function/line]
- **Timestamp:** [When it occurred]
- **Context:** [Relevant state]

## Resolution
[How to fix this specific instance]

## Prevention
[How to prevent this in the future]
```

## Error Severity Levels

### 🔴 CRITICAL
System down, data loss, security breach
- **Response Time:** Immediate
- **Action:** Stop work, fix immediately
- **Example:** "Database connection failed - all requests timing out"

### 🟡 WARNING
Degraded functionality, potential issues
- **Response Time:** Within hour
- **Action:** Monitor and plan fix
- **Example:** "API rate limit approaching - requests may fail"

### ℹ️ INFO
Informational, FYI, no action needed
- **Response Time:** Review when convenient
- **Action:** None, awareness only
- **Example:** "Cache cleared successfully"

## Language Patterns

### Bad Examples
❌ "Oops, something went wrong!"
❌ "This is probably because you did something wrong"
❌ "I can't believe this happened"
❌ "We're sorry for the inconvenience"

### Good Examples
✅ "Connection timeout after 30 seconds"
✅ "Configuration file missing required field: 'database_url'"
✅ "Permission denied: /var/log/app.log (requires root)"
✅ "Expected integer, received string 'abc' at position 3"

## Technical Error Message Template

```
ERROR: [Code] - [Brief Summary]

Location: [Module/Function:Line]
Timestamp: [ISO 8601 timestamp]

Details:
[Key-value pairs of relevant context]

Stack:
[If applicable - first few lines]

Action Required:
[Specific steps to resolve]
```

## Communication Guidelines

**Be specific about the problem:**
- ❌ "There's an error"
- ✅ "Connection refused on port 5432"

**Include relevant technical details:**
- ❌ "Database is broken"
- ✅ "PostgreSQL connection failed: password authentication failed for user 'app'"

**Provide clear next steps:**
- ❌ "Please fix this"
- ✅ "Update password in config/database.yml or set PG_PASSWORD environment variable"

**Avoid blame:**
- ❌ "Your configuration is wrong"
- ✅ "Configuration validation failed: field 'host' is required"

## Logging Pattern

```python
ERROR | 2024-01-15T14:30:22Z | database.py:87
Connection pool exhausted
  pool_size: 10
  active_connections: 10
  waiting_requests: 25
  action: Increase pool_size or add connection retry logic
```

## Success Messages (Positive Reporting)

```markdown
# ✅ Success: Operation Completed

## Summary
[What was accomplished]

## Details
- [Detail 1]
- [Detail 2]

## Metrics
- Duration: [time]
- Items processed: [count]
- Success rate: [percentage]

## Next Steps
[If applicable - what happens next]
```
