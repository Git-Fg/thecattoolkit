# Discovery Protocol

**Goal:** Understand the existing codebase structure before planning.

## 1. Scan Structure
Use `find` and `glob` to map the territory.
```bash
find . -type f -not -path '*/.*' -maxdepth 3
```

## 2. Analyze Capabilities
- **Dependencies:** Read `package.json`, `pyproject.toml`, etc.
- **Frameworks:** Identify primary frameworks (Next.js, Django, etc.).
- **Patterns:** Grep for `class`, `function` to see coding style.

## 3. Assess Health
- Check for tests.
- Look for existing documentation (`README.md`).
- Identify obviously broken or legacy code.
