---
name: managing-npm
description: "Manages npm, pnpm, and bun dependencies following strict protocols. Use when installing, updating, or auditing packages. Do not use for TypeScript configuration or build tooling."
allowed-tools: [Read, Edit, Bash(npm:*), Bash(pnpm:*), Bash(bun:*), Bash(npx:*)]
---

# Dependency Management Protocol

## Core Principle

**NEVER manually edit `package.json`** for dependency changes. Always use package manager commands.

## Dependency Operations

### Adding Dependencies

```bash
# Production dependency
bun add <package>
pnpm add <package>
npm install <package>

# Dev dependency
bun add -d <package>
pnpm add -D <package>
npm install --save-dev <package>
```

### Removing Dependencies

```bash
bun remove <package>
pnpm remove <package>
npm uninstall <package>
```

### Updating Dependencies

```bash
# Check outdated
bun outdated
pnpm outdated
npm outdated

# Update specific package
bun update <package>
pnpm update <package>
npm update <package>

# Update all (interactive)
pnpm update --interactive
npx npm-check-updates -i
```

## Security Audit

```bash
# Run audit
bun audit
pnpm audit
npm audit

# Auto-fix vulnerabilities
pnpm audit --fix
npm audit fix

# Force fix (breaking changes allowed)
npm audit fix --force
```

## Lockfile Hygiene

1. **Commit lockfiles** (`bun.lockb`, `pnpm-lock.yaml`, `package-lock.json`)
2. **Never delete lockfiles** to resolve conflicts - regenerate properly
3. **Use `--frozen-lockfile`** in CI environments

```bash
# CI install (no lockfile changes)
bun install --frozen-lockfile
pnpm install --frozen-lockfile
npm ci
```

## Quality Gates

- [ ] Dependencies added via CLI, not manual edits
- [ ] Lockfile committed with changes
- [ ] No high/critical vulnerabilities in audit
- [ ] Unused dependencies removed
