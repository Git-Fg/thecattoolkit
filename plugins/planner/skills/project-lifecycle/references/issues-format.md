# ISSUES.md Format (Deferred Enhancements)

## Purpose

Log non-critical improvements for future phases. Keeps plans focused while capturing good ideas.

## Template

```markdown
## Open Enhancements

### ISS-XXX: [Brief description]
- **Discovered:** Phase X Plan Y Task Z (YYYY-MM-DD)
- **Type:** [Performance / Refactoring / UX / Testing / Documentation / Accessibility]
- **Description:** [What could be improved and why it would help]
- **Impact:** Low (works correctly, this would enhance)
- **Effort:** [Quick / Medium / Substantial]
- **Suggested phase:** [Phase number or "Future"]

## Closed Enhancements

[Moved here when addressed]
```

## Creation Protocol

**When Rule 5 applies during execution:**

1. **Auto-increment**: Count existing ISS entries and add 1
2. **Append**: Add to Open Enhancements section
3. **Track**: Log in phase SUMMARY.md under "Deferred Enhancements"

## Numbering

Auto-increment from existing entries:

```bash
# Count existing ISS
grep -c "^### ISS-" .cattoolkit/planning/{project-slug}/ISSUES.md

# Next number = count + 1
```

## When to Use ISSUES.md

**Log to ISSUES.md when:**

- Performance optimization (works correctly, just slower than ideal)
- Code refactoring (works, but could be cleaner/DRY-er)
- Better naming (works, but variables could be clearer)
- Organizational improvements (works, but file structure could be better)
- Nice-to-have UX improvements (works, but could be smoother)
- Additional test coverage beyond basics (basics exist, could be more thorough)
- Documentation improvements (code works, docs could be better)
- Accessibility enhancements beyond minimum

**Do NOT log to ISSUES.md:**

- Bugs (fix immediately - Rule 1)
- Missing critical functionality (add immediately - Rule 2)
- Blocking issues (resolve immediately - Rule 3)
- Security vulnerabilities (fix immediately - Rule 1 or 2)

## Effort Estimation

| Effort | Description | Example |
|--------|-------------|---------|
| Quick | <1 hour, low risk | Rename variable, extract small function |
| Medium | 1-4 hours, moderate risk | Refactor module, improve algorithm |
| Substantial | >4 hours or high risk | Restructure architecture, major refactor |

## Example

```markdown
# Project Issues Log

Enhancements discovered during execution. Not critical - address in future phases.

## Open Enhancements

### ISS-001: Add input validation to login endpoint
- **Discovered:** Phase 02 Task 3 (2025-01-08)
- **Type:** Testing
- **Description:** Login endpoint works but lacks comprehensive input validation. Adding email format validation and password strength checks would improve security and user experience.
- **Impact:** Low (current implementation works correctly)
- **Effort:** Quick
- **Suggested phase:** Future

### ISS-002: Refactor UserService into smaller modules
- **Discovered:** Phase 02 Task 5 (2025-01-08)
- **Type:** Refactoring
- **Description:** UserService has grown to 800 lines. Splitting into separate modules (UserRepository, UserValidator, UserMapper) would improve maintainability.
- **Impact:** Low (current code works well)
- **Effort:** Medium
- **Suggested phase:** 04-polish

### ISS-003: Add rate limiting to public API endpoints
- **Discovered:** Phase 03 Task 2 (2025-01-08)
- **Type:** Performance
- **Description:** Public endpoints have no rate limiting. Adding rate limiting would prevent abuse and improve service stability.
- **Impact:** Low (no current abuse detected)
- **Effort:** Medium
- **Suggested phase:** Future

## Closed Enhancements

[Enhancements moved here when completed]
```

## Closing Issues

When addressing an enhancement:

1. **Move** from Open to Closed section
2. **Add resolution note**: "Resolved in Phase X - [what was done]"
3. **Update** SUMMARY.md to mention closure

## Anti-Patterns

**Don't use ISSUES.md for:**

❌ Tracking bugs (fix immediately)
❌ Remembering to add critical features (add immediately)
❌ Documenting known issues (fix or document in README)
❌ Future feature ideas (keep separate backlog)

**Do use ISSUES.md for:**

✅ Non-critical improvements discovered during execution
✅ Code quality enhancements that don't affect correctness
✅ Performance optimizations for working code
✅ UX improvements for functional features
