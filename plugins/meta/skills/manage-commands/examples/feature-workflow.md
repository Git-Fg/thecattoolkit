# Example: Feature Development Workflow

A multi-step structured workflow for feature development.

```markdown
---
description: Complete feature development workflow
argument-hint: [feature description]
---

## Objective
Complete full feature development workflow for: $ARGUMENTS

This ensures features are developed systematically with proper planning, implementation, testing, and documentation.

## Process
1. **Planning**
   - Review requirements
   - Design approach
   - Identify files to modify

2. **Implementation**
   - Write code
   - Add tests
   - Update documentation

3. **Review**
   - Run tests: ! `npm test`
   - Check lint: ! `npm run lint`
   - Verify changes: ! `git diff`

4. **Completion**
   - Create commit
   - Write PR description

## Testing
- Run tests: ! `npm test`
- Check lint: ! `npm run lint`

## Verification
Before completing:
- All tests passing
- No lint errors
- Documentation updated
- Changes verified with git diff

## Success Criteria
- Feature fully implemented
- Tests added and passing
- Code passes linting
- Documentation updated
- Commit created
- PR description written
```
