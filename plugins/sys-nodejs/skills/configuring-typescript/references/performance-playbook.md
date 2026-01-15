# Compile-Time Performance Playbook

When compile times degrade, do not guess. Follow this sequence.

---

## 1) Measure, Don't Speculate

Run diagnostics:
```bash
# Single package
tsc -p tsconfig.json --noEmit --extendedDiagnostics

# Monorepo
tsc -b --noEmit --extendedDiagnostics
```

Record:
- Total time
- Parse time
- Bind/check time
- Number of files
- Memory usage

Keep a history (CI artifact or local notes) to see regressions.

---

## 2) Stabilize the Typechecking Surface Area

- Use project references to stop TypeScript from re-checking the world on every change
- Emit `.d.ts` for internal packages (especially shared libs) to reduce cross-package typechecking work

---

## 3) Common Sources of Type Slowness (and Fixes)

### A) Deep recursive types used everywhere

**Symptoms:** Typechecking slows as the codebase grows.

**Fix:**
- Restrict deep types to boundaries
- Provide shallow types for internal usage
- Avoid deep recursion on broad object types

### B) Distributive conditional types over large unions

**Symptoms:** A type like `Foo<A|B|C|...>` becomes huge.

**Fix:**
- Use non-distributive forms `[T] extends [X] ? ... : ...`
- Reduce union size earlier

### C) Template literal explosion

**Symptoms:** Route/event key types become enormous.

**Fix:**
- Keep key unions small
- Avoid generating huge cross-products of strings

### D) Accidental `any` or `unknown` propagation causing more work

Sometimes weak typing increases work because everything becomes "maybe" and the checker tries harder.

**Fix:**
- Keep core types precise
- Use `satisfies` for maps/configs

---

## 4) Decide Tradeoffs Explicitly

### `skipLibCheck`

**On:** Improves speed by skipping `.d.ts` checks.
**Off:** Increases correctness across dependency types.

**Policy recommendation:**
- Dev: usually `true`
- CI (optional strict job): `false`

### Typed ESLint (`recommended-type-checked`)

Valuable but can be slow if misconfigured.

**Policy:**
- Use `tsconfig.eslint.json` so ESLint has a stable, intentionally scoped project
- Use overrides to avoid typed rules in config files or scripts if needed
