# Do Patterns

Prompt patterns for execution tasks that produce artifacts.

## Template

```markdown
# {Topic} Implementation

## Objective
{What to build/create/fix}

## Context
Research: @.prompts/{num}-{topic}-research/{topic}-research.md
Plan: @.prompts/{num}-{topic}-plan/{topic}-plan.md

## Requirements
{Functional requirements}
{Quality requirements}
{Constraints}

## Implementation
{Approaches to follow}
{What to avoid}
{Integration points}

## Output
Create/modify files:
- `./path/file.ext` - {Description}

## Verification
Before declaring complete:
- [ ] {Specific test}
- [ ] {How to confirm}
- [ ] {Edge cases}

## Summary Requirements
Create .prompts/{num}-{topic}-{purpose}/SUMMARY.md:

```markdown
# {Topic} Implementation Summary

**{Substantive one-liner}**

## Files Created
- `path/file1.ext` - {Description}
- `path/file2.ext` - {Description}

## Verification
- Tests: {Status}
- Type check: {Status}
- Manual test: {Status}

## Next Step
{Run tests / proceed to next phase}
```
```

## Examples

### Simple Implementation
Single artifact:

```markdown
# Email Validator Implementation

## Objective
Create utility function to validate email addresses

## Context
Building validation utilities for user registration

## Requirements
- Support standard email format
- Return boolean result
- Handle edge cases (empty, null)

## Output
Create: `./src/utils/validate-email.ts`

## Verification
- Test with valid emails
- Test with invalid formats
- Test edge cases
```

### Complex Implementation
Multiple artifacts:

```markdown
# Authentication System Implementation

## Objective
Implement JWT authentication with refresh tokens

## Context
Research: @.prompts/001-auth-research/auth-research.md
Plan: @.prompts/002-auth-plan/auth-plan.md

## Requirements
- JWT access tokens (15min expiry)
- Refresh token rotation
- httpOnly cookies
- Rate limiting

## Implementation
Follow patterns from research:
- Use jose library
- Implement refresh rotation
- Store refresh tokens hashed

Avoid:
- localStorage (XSS vulnerable)
- Long-lived access tokens

## Output
Create in `./src/auth/`:
- `middleware.ts` - JWT validation
- `routes.ts` - Auth endpoints
- `types.ts` - Type definitions
- `utils.ts` - Helper functions

Create in `./src/auth/__tests__/`:
- `auth.test.ts` - Unit tests

## Verification
- Run: `npm test src/auth`
- Type check: `npx tsc --noEmit`
- Manual test: login flow
- Security check: cookies, expiry
```

### Document Creation

```markdown
# API Documentation Creation

## Objective
Create OpenAPI documentation for authentication endpoints

## Context
Implementation: @src/auth/routes.ts

## Requirements
- OpenAPI 3.0 spec
- Request/response examples
- Error codes
- Authentication flow

## Output
- `./docs/api/auth.yaml` - OpenAPI spec
- `./docs/guides/auth.md` - Integration guide

## Verification
- Validate OpenAPI: `npx @redocly/cli lint`
- Check completeness
- Verify examples
```

## Quality Checklist

Before completing:
- [ ] All files created as specified
- [ ] Tests pass
- [ ] Type check clean
- [ ] Follows research recommendations
- [ ] SUMMARY.md created
- [ ] Next step identified
