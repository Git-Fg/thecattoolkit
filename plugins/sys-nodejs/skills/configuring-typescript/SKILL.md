---
name: configuring-typescript
description: "Configures modern TypeScript (4.9+ through 5.x) for maximum type safety with sustainable compile times. Use when designing type-safe configs/maps/APIs, enforcing strictness flags, improving TS build performance (incremental, project references), or setting up separate TS/ESLint configs for tests."
---

# TypeScript Advanced Types

Modern TypeScript playbook for writing code that is **correct**, **ergonomic**, and **fast enough**.

## Quick Reference

| Need | See |
|:-----|-----|
| Modern features (`satisfies`, `const` type params) | [Modern Features](references/modern-features.md) |
| Generics, conditional types, mapped types | [Type-Level Toolbox](references/type-level-toolbox.md) |
| Config objects, event emitters, API clients | [Practical Patterns](references/practical-patterns.md) |
| Test patterns, tsconfig templates | [Tests & Configs](references/tests-configs.md) |
| Compile-time optimization | [Performance Playbook](references/performance-playbook.md) |
| Type testing, PR checklist | [Type Testing](references/type-testing.md) |

## When to Use

Use this skill when:
- Building **type-safe configs/maps/APIs** (feature flags, route tables, event maps)
- Designing **type-safe APIs** (HTTP clients, RPC layers, CLI command maps)
- Enforcing strictness beyond `"strict": true`:
  - `noUncheckedIndexedAccess`
  - `exactOptionalPropertyTypes`
  - `verbatimModuleSyntax`
- Improving compile times (incremental builds, project references)
- Setting up separate TS/ESLint configs for tests

## Operating Principles

### A — Value-level correctness + light typing over deep magic
- Use runtime validation for untrusted inputs (HTTP, env, user input)
- Types model expected structure, not unsafe data pretending to be safe

### B — Prefer `satisfies` to assertions and widenings
- `satisfies` validates shape while keeping precise inference
- Avoid `as SomeType` when it hides bugs

### C — Consider the typechecker's workload
Deep recursive types, huge unions, distributive conditionals, and template literal explosions can all be expensive

### D — Make strictness explicit
tsconfig flags, module settings, project structure, and ESLint configuration drive safety and compile-time behavior

## Default Workflow

1. **Start with data shape and ownership** — Is value internally constructed (safe) or external input (unsafe)?
2. **Choose the lightest typing tool** — `satisfies` for configs, mapped types for transformations, `infer` for function inference
3. **Lock strictness and hygiene** — Enable `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, consider `verbatimModuleSyntax`
4. **Keep builds fast** — Enable `incremental`, use project references in monorepos, measure with `--extendedDiagnostics`
5. **Tests: strict where matters, pragmatic where not** — Separate `tsconfig.test.json`, ESLint overrides for test files only

## Key Highlights

### `satisfies` — Use Aggressively
Validates object shape without losing literal inference or widening to `string`/`number`.

```ts
type AppConfig = {
  env: "dev" | "prod";
  apiBaseUrl: string;
  retries: number;
};

export const config = {
  env: "dev",
  apiBaseUrl: "https://api.example.com",
  retries: 3,
} satisfies AppConfig;
// config.env is "dev" (literal), not "dev" | "prod"
```

### Strictness Beyond `"strict": true`

**`noUncheckedIndexedAccess`** — Adds `undefined` to indexed access:
```ts
const dict: Record<string, { id: string }> = {};
const x = dict["missing"]; // { id: string } | undefined
```

**`exactOptionalPropertyTypes`** — Optional ≠ undefined:
```ts
type UserPrefs = { theme?: "dark" | "light" };
const prefs: UserPrefs = {};
prefs.theme = "dark";     // ok
// prefs.theme = undefined; // error
```

**`verbatimModuleSyntax`** — Module hygiene:
```ts
import type { User } from "./types";     // type-only
import { createUser } from "./runtime"; // runtime (kept in output)
```

## Resources

See [references/](references/) for detailed guides on each topic.
