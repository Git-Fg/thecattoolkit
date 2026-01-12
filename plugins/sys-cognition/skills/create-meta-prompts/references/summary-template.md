# Summary Template

Standard SUMMARY.md structure for all prompt outputs.

## Template

```markdown
# {Topic} {Purpose} Summary

**{Substantive one-liner describing outcome}**

## Key Findings
- {Most important finding}
- {Second key item}
- {Third key item}

## Files Created
{Only for Do prompts}
- `path/file.ext` - Description

## Decisions Needed
{Specific actionable decisions or "None"}

## Next Step
{Concrete forward action}
```

## Examples

### Research Summary

```markdown
# Auth Research Summary

**JWT with jose library and httpOnly cookies recommended**

## Key Findings
- jose outperforms jsonwebtoken in security and TypeScript support
- httpOnly cookies required (localStorage XSS vulnerable)
- Refresh rotation is OWASP standard

## Decisions Needed
None - ready for planning

## Next Step
Create auth-plan.md
```

### Plan Summary

```markdown
# Auth Plan Summary

**4-phase implementation: setup → JWT core → refresh → tests**

## Key Findings
- Phased approach allows testing at each stage
- Rate limiting critical for production
- Phase 4 depends on successful Phase 3

## Decisions Needed
Approve 15-minute token expiry

## Next Step
Execute Phase 1 (setup infrastructure)
```

### Implementation Summary

```markdown
# Auth Implementation Summary

**JWT middleware complete with 6 files created**

## Files Created
- `src/auth/middleware.ts` - JWT validation middleware
- `src/auth/routes.ts` - Auth endpoints
- `src/auth/types.ts` - Type definitions
- `src/auth/utils.ts` - Helper functions
- `src/auth/__tests__/auth.test.ts` - Unit tests

## Verification
- Tests: All passing
- Type check: Clean
- Manual test: Login flow working

## Next Step
Run full test suite and deploy
```

## Field Requirements

### One-Liner
Must be substantive - describes outcome, not status.

**Good:** "JWT with jose library recommended"
**Bad:** "Research completed"

**Good:** "4-phase implementation created"
**Bad:** "Plan created"

### Key Findings
Purpose-specific:
- Research: Key recommendations
- Plan: Phase breakdown
- Do: What was implemented

### Decisions Needed
Actionable items requiring user judgment:
- Architectural choices
- Trade-off confirmations
- Assumption validation

Must be specific: "Approve 15-min expiry" not "review"

### Next Step
Concrete action:
- "Create auth-plan.md"
- "Execute Phase 1"
- "Run tests"

Not vague: "proceed to next phase"
