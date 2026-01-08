---
name: git-workflow
description: |
  PROACTIVELY load this skill when creating PRs, resolving merge conflicts, or asked about version control best practices. Independent knowledge base for Git workflows, branching strategies, commit conventions, and collaboration patterns. Can be invoked directly by main AI anytime for Git guidance.
<example>
Context: User needs to create a commit
user: "Help me commit these changes"
assistant: "I'll load the git-workflow skill to generate a proper conventional commit message."
</example>
<example>
Context: User asks about Git best practices
user: "What's the best way to organize branches for our team?"
assistant: "I'll load the git-workflow skill to explain branching strategies."
</example>
allowed-tools: [Bash, Read, Write, Edit]
---

# Git Workflow Standards

## Commit Message Standards

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type | Description |
|------|-------------|
| **feat** | New feature |
| **fix** | Bug fix |
| **docs** | Documentation only |
| **style** | Formatting, no logic change |
| **refactor** | Code change that neither fixes bug nor adds feature |
| **perf** | Performance improvement |
| **test** | Adding/updating tests |
| **chore** | Build process, dependencies |
| **ci** | CI configuration |

### Commit Message Examples

**Feature:**
```bash
feat(auth): add OAuth2 login support

Implements Google and GitHub OAuth providers.
Closes #123

BREAKING CHANGE: Session tokens now expire after 24h
```

**Bug Fix:**
```bash
fix(api): handle null response from payment gateway

Previously caused 500 error when gateway returned null.
Now returns appropriate error message to user.
```

**Documentation:**
```bash
docs(api): update authentication endpoint documentation

Adds request/response examples for OAuth flow.
```

## Branch Naming Conventions

Format: `<type>/<ticket-id>-<short-description>`

**Examples:**
- `feature/AUTH-123-oauth-login`
- `fix/BUG-456-null-pointer`
- `chore/TECH-789-upgrade-deps`
- `docs/README-001-update-installation`

## Pull Request Quality Guidelines

### PR Size Standards

| Size | Lines Changed | Expected Review Time |
|------|---------------|---------------------|
| XS | < 50 | < 15 minutes |
| S | 50-200 | 15-30 minutes |
| M | 200-500 | 30-60 minutes |
| L | 500+ | Should be split if possible |

### Required PR Content

**Every PR must include:**
- [ ] Clear, concise summary of changes
- [ ] Link to related ticket/issue
- [ ] Testing documentation
- [ ] Updated documentation if applicable
- [ ] Screenshots for UI changes

**PR Template:**
```markdown
## Summary
[Brief description of changes]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing performed
- [ ] E2E tests pass

## Checklist
- [ ] Code follows project conventions
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
```

## Branching Strategy

### GitHub Flow (Recommended)
```
main ──●────●────●────●────●── (always deployable)
        \          /
feature  └──●──●──┘
```
- main branch is always deployable
- Feature branches created from main
- PR + review + merge workflow
- Deploy after merge to main

### Git Flow (For Release-Based Projects)
```
main     ──●─────────────●────── (releases only)
            \           /
release      └────●────┘
                 /
develop  ──●──●────●──●──●──
            \     /
feature      └──●┘
```

### PR Review Checklist

**Before Submitting:**
- [ ] Code compiles and tests pass
- [ ] Commit messages follow standards
- [ ] No merge conflicts
- [ ] Code follows project style guidelines
- [ ] Self-review completed

**Reviewer Evaluation Criteria:**
- [ ] Code correctness and logic
- [ ] Security implications
- [ ] Performance considerations
- [ ] Test coverage adequacy
- [ ] Documentation completeness

---

## Protocol Reference Index

### Commit Message Generation
- **Protocol**: `references/generate-commit.md` - Analyze staged changes and generate conventional commit
- **When to Apply**: Creating commits, ensuring commit message quality
