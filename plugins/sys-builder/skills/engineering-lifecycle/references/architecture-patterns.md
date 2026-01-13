# Architecture Patterns

## Breaking Down Work
**Principle:** Tasks should be atomic, verifiable, and independent.

### Granularity Guide
- **Too Big:** "Build the backend" (Takes > 3 hours)
- **Too Small:** "Fix typo in comment" (Combine with others)
- **Just Right:** "Implement User Auth API endpoints" (30-90 mins)

## Phase Structure Pattern
1.  **Foundation:** Scaffolding, deps, env setup.
2.  **Core:** Primary logic and "Happy Path".
3.  **Enhancement:** Error handling, edge cases, logging.
4.  **Polish:** UI tweaks, cleanup, documentation.

## Dependency Rules
- No circular dependencies.
- Foundation must precede Core.
- Updates to `ROADMAP.md` must reflect these dependencies.
