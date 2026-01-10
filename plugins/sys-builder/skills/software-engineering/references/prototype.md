# Workflow: Rapid Prototyping

## Purpose
Creative exploration through throwaway first drafts, followed by mandatory rigor.

## Philosophy

LLMs solve creative problems better through **drafting then editing**. This workflow explicitly separates:

1. **Draft Phase** - Vibe code freely, get something working
2. **Harden Phase** - Apply engineering rigor to the draft

**This is NOT an excuse for sloppy code.** It's recognition that creative problem-solving benefits from exploration before optimization.

## When to Use

- Complex features with unclear implementation paths
- Exploring multiple architectural approaches
- Greenfield code where patterns aren't established
- Creative problem-solving where the "right" answer isn't obvious

## When NOT to Use

- Bug fixes (use debug workflow)
- Security-sensitive code (use security-audit first)
- Simple, well-understood features
- Production hotfixes

## Process

### Phase 1: Draft (Checks Suspended)

**Goal:** Get something working. Explore the problem space.

**Suspended during draft:**
- Security checklist validation
- Architecture compliance
- Code style enforcement
- Performance optimization
- Complete error handling

**Still mandatory:**
- Basic functionality works
- No obvious data corruption risks
- No credentials in code

**Process:**

1. **State the goal clearly** - What are we trying to build?
2. **Code freely** - Focus on making it work, not making it perfect
3. **Test the happy path** - Verify basic functionality
4. **Checkpoint** - Working prototype exists

```
[DRAFT COMPLETE]
Prototype: {description}
Status: Working / Partially working / Concept only
Known shortcuts:
- {shortcut 1}
- {shortcut 2}
Ready for hardening: Yes/No
```

### Phase 2: Harden (Full Rigor)

**Goal:** Transform draft into production-quality code.

**Now mandatory:**
- `references/security-checklist.md` - Full security review
- `references/refactoring-patterns.md` - Code quality patterns

**Hardening Checklist:**

```markdown
## Security
- [ ] Input validation on all entry points
- [ ] No SQL injection vectors
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization checks
- [ ] Sensitive data handling

## Error Handling
- [ ] All error paths handled
- [ ] Meaningful error messages
- [ ] No swallowed exceptions
- [ ] Graceful degradation

## Code Quality
- [ ] Functions under 20 lines
- [ ] Clear naming
- [ ] No magic numbers/strings
- [ ] DRY - no duplicated logic

## Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] No blocking operations in hot paths

## Testing
- [ ] Happy path tested
- [ ] Edge cases covered
- [ ] Error paths tested
```

**Process:**

1. **Read security checklist** - `references/security-checklist.md`
2. **Review draft against checklist** - Identify all gaps
3. **Fix systematically** - One category at a time
4. **Run full test suite** - Verify nothing broke
5. **Final review** - Would you deploy this?

### Phase 3: Commit

Only after hardening is complete:

```bash
git add -A
git commit -m "feat: {feature description}

Draft-then-harden approach:
- Initial prototype explored {approach}
- Hardened with full security review
- {key decisions made}"
```

## Anti-Patterns

❌ **Skipping Phase 2** - Draft code shipping to production
❌ **Over-drafting** - Spending too long in draft phase
❌ **Draft in security-critical code** - Authentication, payments, data access
❌ **Using as excuse** - "It's just a prototype" for code that will ship

## Success Criteria

- [ ] Phase 1: Working prototype exists
- [ ] Phase 2: All hardening checklist items addressed
- [ ] Phase 3: Code passes full test suite
- [ ] Final: You would confidently deploy this
