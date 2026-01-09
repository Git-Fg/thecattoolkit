# ISSUES.md Format (Deferred Enhancements)

## Purpose

Log non-critical improvements for future phases. Keeps plans focused while capturing good ideas.

## Template

Use `assets/templates/issue-entry.md` for issue structure.

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
