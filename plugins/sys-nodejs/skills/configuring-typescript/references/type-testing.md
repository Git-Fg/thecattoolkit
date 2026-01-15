# Type Testing & Review Checklist

Use type tests to prevent regressions in public APIs and advanced utilities.

---

## Type Testing (Compile-Time Tests)

### A) Inline type equality helpers
```ts
export type AssertEqual<T, U> =
  (<G>() => G extends T ? 1 : 2) extends
  (<G>() => G extends U ? 1 : 2)
    ? true
    : false;

export type Expect<T extends true> = T;

// Example:
type A = Expect<AssertEqual<string, string>>;
```

### B) Error expectation using `@ts-expect-error`
```ts
type Color = "red" | "blue";

// @ts-expect-error
const bad: Color = "green";
```

### C) "Public surface" tests

For libraries:
- Write type tests that assert the shape of exported APIs
- Run `tsc -p tsconfig.types.json --noEmit`

---

## Review Checklist (Use in PRs)

### Strong typing
- Uses `satisfies` for config/map literals instead of `as Type`
- Avoids `any` in production code (tests may allow)
- Optional vs undefined is intentional (`exactOptionalPropertyTypes` ready)
- Indexed access is safe (`noUncheckedIndexedAccess` ready)

### Module hygiene
- `import type` is used for type-only imports (especially with `verbatimModuleSyntax`)
- Runtime imports are not accidentally elided or relied upon

### Performance
- No unbounded recursive types used widely
- Conditional types are non-distributive when union size can grow
- Huge template literal unions are avoided unless strictly necessary
- Monorepo uses project references when packages depend on each other

### Tests
- Test tsconfig is separate and includes test globals/types
- ESLint overrides relax only test files, not production
