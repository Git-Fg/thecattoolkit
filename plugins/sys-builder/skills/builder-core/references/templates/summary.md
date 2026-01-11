# Summary Template

**MANDATORY:** Create `{phase}-{plan}-SUMMARY.md` after completing each plan.

```markdown
# Phase [X]: [Name] Summary

**[Substantive one-liner - what shipped, NOT "phase complete"]**

## Accomplishments
- [Most important outcome]
- [Second key accomplishment]
- [Third if applicable]

## Verification Evidence

**Build/Test Results:**
```
[Output from build and test commands]
```

**Manual Verification:**
- [Endpoint/feature tested]: [result]
- [File verified]: [method]

## Files Created/Modified
- `path/to/file` - Description
- `path/to/file` - Description

## Decisions Made
[Key decisions with rationale, or "None - followed plan"]

## Deviations from Plan
[Changes from original plan, or "None"]

## Issues Encountered
[Problems and resolutions, or "None"]

## Next Steps
[Ready for next phase / blockers]

---
*Phase: XX-name*
*Completed: [date]*
```

## One-Liner Rules

**MUST be substantive:**

✅ Good:
- "Token auth with refresh rotation"
- "User model with email validation"
- "Dashboard with real-time updates"

❌ Bad:
- "Phase complete"
- "Authentication implemented"
- "All tasks done"

## Example

```markdown
# Phase 1: Foundation Summary

**Token auth with refresh rotation and protected API middleware**

## Accomplishments
- User model with email/password auth
- Login/logout endpoints with secure cookies
- Protected route middleware

## Verification Evidence

**Build/Test Results:**
```
Build completed successfully
All 12 tests passed
No type errors
```

**Manual Verification:**
- POST /api/auth/login: Returns 200 + token
- GET /api/protected: Returns 401 without token, 200 with valid token

## Files Created/Modified
- `src/models/user` - User schema
- `src/api/auth/login` - Login endpoint
- `src/middleware/auth` - Token validation

## Decisions Made
- 15-min access tokens, 7-day refresh tokens
- Storing refresh tokens in database for revocation

## Deviations from Plan
None

## Issues Encountered
None

## Next Steps
Ready for Phase 2: Features

---
*Phase: 01-foundation*
*Completed: 2026-01-08*
```
