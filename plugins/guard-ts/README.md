# @cattoolkit/guard-ts

**The Immune System for TypeScript: File safety warnings, security checks, and type-checking hooks.**

**License:** MIT

## Purpose

Provides passive safety and quality hooks for TypeScript projects. These hooks run automatically to protect against common mistakes, security issues, and type errors.

## Features

### Type Check (`type-check.js`)
- **Auto-detection**: Automatically detects `tsconfig.json`.
- **Behavior**: Runs `tsc --noEmit` on your project after edits to `.ts`/`.tsx` files.
- **Feedback**: Reports TypeScript errors directly to Claude's context.

### File Protection (`protect-files.js`)
- Warns before editing sensitive files:
  - Lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`
  - Secrets: `.env`, `secrets/*`
  - Git: `.git/*`

### Security Check (`security-check.js`)
- Scans content for secrets (API keys, tokens, passwords) before tool use.

## Installation

```bash
claude plugin install @cat-toolkit/guard-ts
```

### How Hooks Work

Hooks run automatically via Claude Code's plugin system:

1. **Install the plugin** - hooks are registered automatically
2. **No setup required** - hooks execute from the plugin cache via `${CLAUDE_PLUGIN_ROOT}`
3. **Immediate protection** - guards activate on your first edit

> **Note:** Hooks are Claude Code specific. Other MCP clients can use the marketplace but won't have automatic hook protection.

## Requirements

- **Node.js**: Scripts run with `node`.
- **TypeScript**: The target project should have `typescript` installed (checked via `npx tsc`).
