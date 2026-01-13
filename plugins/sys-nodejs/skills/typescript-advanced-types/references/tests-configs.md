# Tests & Configs

Strong typing without losing debug velocity. Strict in production, pragmatic in tests.

---

## Tests: Strong Typing, Fast Debugging

Tests are special—you often intentionally violate invariants (partial objects, mocks, fake timers). The goal is **targeted pragmatism**: strict in production, adjustable in tests, enforced by config not vibes.

### Recommended directory patterns

**Option 1 — Co-located tests**
- `src/foo.ts`
- `src/foo.test.ts`

**Option 2 — Dedicated tests folder**
- `src/**`
- `tests/**`

**Option 3 — Monorepo packages**
- `packages/*/src/**`
- `packages/*/tests/**` or `packages/*/src/**/*.test.ts`

### Separate tsconfig for tests (always)

Create `tsconfig.test.json` extending the base config. Add test runner globals/types here only. Keep production tsconfig clean.

**Vitest example:**
```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "noEmit": true,
    "types": ["node", "vitest/globals"]
  },
  "include": [
    "src/**/*.test.ts",
    "src/**/*.spec.ts",
    "tests/**/*.ts"
  ]
}
```

For Jest, replace `vitest/globals` with appropriate Jest types.

### Pragmatic typing patterns in tests

**Prefer typed factories/builders for fixtures**
```ts
type User = { id: string; name: string; email: string; age?: number };

export function makeUser(overrides: Partial<User> = {}): User {
  return {
    id: "u_1",
    name: "Test User",
    email: "test@example.com",
    ...overrides,
  };
}
```

**Prefer `unknown` + narrowing for untrusted mock payloads**
```ts
function isUser(x: unknown): x is { id: string; name: string } {
  return typeof x === "object" && x !== null && "id" in x && "name" in x;
}
```

**Use `@ts-expect-error` for negative compile-time tests**
```ts
type Color = "red" | "blue";
declare const color: Color;

// @ts-expect-error - "green" is not assignable
const bad: Color = "green";
```

---

## ESLint: Production Strict, Tests Pragmatic

Use ESLint overrides to relax only in tests.

### Option A — Classic `.eslintrc.cjs`
```js
/* eslint-env node */
module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  parserOptions: {
    tsconfigRootDir: __dirname,
    project: true
  },
  plugins: ["@typescript-eslint"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-type-checked"
  ],
  rules: {
    // Enforce type-only imports if using verbatimModuleSyntax
    "@typescript-eslint/consistent-type-imports": ["error", { prefer: "type-imports" }]
  },
  overrides: [
    {
      files: ["**/*.test.ts", "**/*.spec.ts", "tests/**/*.ts"],
      rules: {
        "@typescript-eslint/no-explicit-any": "off",
        "@typescript-eslint/no-non-null-assertion": "off",
        "@typescript-eslint/unbound-method": "off",
        "@typescript-eslint/no-unsafe-assignment": "off",
        "@typescript-eslint/no-unsafe-member-access": "off",
        "@typescript-eslint/no-unsafe-call": "off"
      }
    }
  ]
};
```

### Option B — Flat config `eslint.config.js` (modern ESLint)

Keep the same idea: strict typed rules for src, relaxed for tests. Exact package imports vary by ESLint + typescript-eslint versions.

---

## Compiler Configuration (tsconfig): Strict + Fast

### Single-package template (Bun repo)

**`tsconfig.base.json`**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,

    "verbatimModuleSyntax": true,

    "skipLibCheck": true,

    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true
  }
}
```

**`tsconfig.json`** (production/dev typecheck)
```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "noEmit": true,
    "types": ["node"]
  },
  "include": ["src/**/*.ts", "src/**/*.tsx"]
}
```

**`tsconfig.test.json`** (test-only)
```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "noEmit": true,
    "types": ["node", "vitest/globals"]
  },
  "include": ["src/**/*.test.ts", "src/**/*.spec.ts", "tests/**/*.ts"]
}
```

**`tsconfig.eslint.json`** (optional, for typed lint stability)
```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "noEmit": true
  },
  "include": [
    "src/**/*.ts",
    "src/**/*.tsx",
    "tests/**/*.ts",
    "*.ts",
    "*.js",
    "*.cjs",
    "*.mjs"
  ]
}
```

**`package.json` scripts** (example)
```json
{
  "scripts": {
    "typecheck": "bunx tsc -p tsconfig.json",
    "typecheck:tests": "bunx tsc -p tsconfig.test.json",
    "lint": "bunx eslint .",
    "test": "bunx vitest run"
  }
}
```

### pnpm monorepo template (Project References)

**Why project references:** Enable scalable incremental builds by splitting packages into composite projects and building with `tsc -b`.

**Root layout:**
- `tsconfig.base.json`
- `tsconfig.json` (references graph)
- `tsconfig.eslint.json` (optional)
- `packages/*/tsconfig.json`
- `packages/*/tsconfig.test.json`

**Root `tsconfig.base.json`**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",

    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,

    "verbatimModuleSyntax": true,
    "skipLibCheck": true,

    "forceConsistentCasingInFileNames": true
  }
}
```

**Root `tsconfig.json`** (references)
```json
{
  "files": [],
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/api" }
  ]
}
```

**Package `packages/core/tsconfig.json`**
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "composite": true,
    "incremental": true,

    "rootDir": "./src",
    "outDir": "./dist",

    "declaration": true,
    "declarationMap": true,
    "emitDeclarationOnly": true
  },
  "include": ["src/**/*.ts"]
}
```

**Package test `packages/core/tsconfig.test.json`**
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "noEmit": true,
    "types": ["node", "vitest/globals"]
  },
  "include": ["src/**/*.test.ts", "src/**/*.spec.ts", "tests/**/*.ts"]
}
```

**Root scripts**
```json
{
  "scripts": {
    "typecheck": "tsc -b --noEmit",
    "build": "tsc -b",
    "typecheck:watch": "tsc -b -w --noEmit"
  }
}
```
