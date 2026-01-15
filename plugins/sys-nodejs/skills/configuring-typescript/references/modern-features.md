# Modern TypeScript Features

High-leverage features often missing from "advanced types" guides that solve 80% of daily typing problems.

## 1) `satisfies` (Use It Aggressively)

### What problem it solves
You want the compiler to check that your object matches an interface/shape, but you do **not** want to lose literal inference (widening to `string`, `number`, etc.), and you want errors to point at the exact mismatched property.

### Canonical config pattern
```ts
type AppConfig = {
  env: "dev" | "prod";
  apiBaseUrl: string;
  retries: number;
  features: Record<string, boolean>;
};

export const config = {
  env: "dev",
  apiBaseUrl: "https://api.example.com",
  retries: 3,
  features: {
    auth: true,
    analytics: false,
  },
} satisfies AppConfig;

// Still keeps precise inference:
// - config.env is "dev" (literal), not "dev" | "prod"
// - config.retries is 3 (literal) if "as const" is used
```

### Map-of-things pattern (routes/events/commands)
```ts
type CommandSpec = {
  input: unknown;
  output: unknown;
};

type CommandRegistry = Record<string, CommandSpec>;

export const commands = {
  "user.create": {
    input: { name: "string", email: "string" },
    output: { id: "string" },
  },
  "user.delete": {
    input: { id: "string" },
    output: { ok: "boolean" },
  },
} satisfies CommandRegistry;

export type CommandName = keyof typeof commands;
```

### When NOT to use `satisfies`
- When you need to *change* the type of an expression (that's annotation or a function wrapper)
- When you need runtime validation (external input)

### Anti-patterns vs `satisfies`

**Anti-pattern: `as SomeType` on object literals**
```ts
// Bad: hides extra/missing keys and widens inference unexpectedly
const cfg = {
  env: "dev",
  retries: 3,
} as AppConfig;
```

**Better: `satisfies`**
```ts
const cfg = {
  env: "dev",
  retries: 3,
  apiBaseUrl: "https://api.example.com",
  features: {},
} satisfies AppConfig;
```

---

## 2) Strictness Flags Beyond `"strict": true`

Many codebases set `"strict": true` and stop. That is not enough for maximum safety.

### `noUncheckedIndexedAccess`
Adds `undefined` to indexed access results. Prevents many "undefined at runtime" bugs.

```ts
// With noUncheckedIndexedAccess: true
const dict: Record<string, { id: string }> = {};
const x = dict["missing"];
// x: { id: string } | undefined

// You must handle undefined:
if (x) {
  x.id;
}
```

**Pragmatic guidance:**
- Keep enabled for application code
- In tests, use non-null assertions (`!`) when test setup guarantees existence

### `exactOptionalPropertyTypes`
Optional does not automatically mean "can assign undefined."

```ts
// With exactOptionalPropertyTypes: true
type UserPrefs = {
  theme?: "dark" | "light";
};

const prefs: UserPrefs = {};
prefs.theme = "dark";     // ok
// prefs.theme = undefined; // error unless theme?: "dark" | "light" | undefined
```

**Pragmatic guidance:**
- Enable when optional-vs-undefined semantics should match runtime checks
- Expect friction with some third-party types
- Have a strategy: keep `skipLibCheck` on for dev, pin/upgrade types, add explicit `| undefined` where truly allowed

---

## 3) `verbatimModuleSyntax` + `import type` (Module Hygiene)

**Why it matters:**
- Predictable emitted output
- Eliminates "import elision gotchas"
- Forces clarity: what's runtime vs type-only

```ts
// Good: type-only import
import type { User } from "./types";

// Good: runtime import (kept in output)
import { createUser } from "./runtime";
```

With `verbatimModuleSyntax: true`, any import/export without the `type` modifier is preserved as-is. Treat this as "what you see is what you get."

---

## 4) Variadic Tuple Types (Function Wrappers Done Right)

Preserve argument lists across higher-order utilities.

```ts
type AnyFunc = (...args: any[]) => any;

export function withTiming<F extends AnyFunc>(fn: F) {
  return (...args: Parameters<F>): ReturnType<F> => {
    const start = performance.now();
    try {
      return fn(...args);
    } finally {
      const end = performance.now();
      console.log(`took ${end - start}ms`);
    }
  };
}
```

**More advanced: append arguments**
```ts
export function withContext<Args extends any[], R>(
  fn: (...args: [...Args, { requestId: string }]) => R,
  ctx: { requestId: string }
) {
  return (...args: Args) => fn(...args, ctx);
}
```

---

## 5) `Awaited<T>` and Async Type Modeling

`Awaited<T>` models the type you get after `await` (including nested promises).

```ts
type T1 = Awaited<Promise<number>>;              // number
type T2 = Awaited<Promise<Promise<string>>>;     // string

async function fetchUser() {
  return { id: "1", name: "Ada" };
}

type User = Awaited<ReturnType<typeof fetchUser>>;
// { id: string; name: string }
```

Use this in:
- API clients
- loader functions
- job queues
- async adapters

---

## 6) TS 5.x: `const` Type Parameters (Better Literal Inference in APIs)

When designing generic APIs that accept objects/arrays and want to preserve literals without requiring `as const`:

```ts
// Requires TS 5.0+
export function defineRoutes<const T extends Record<string, { method: string; path: string }>>(routes: T) {
  return routes;
}

export const routes = defineRoutes({
  users: { method: "GET", path: "/users" },
  user: { method: "GET", path: "/users/:id" },
});

// routes.users.method is "GET" (literal), not string
// routes.user.path is "/users/:id" (literal), not string
```

Combine with `satisfies` when also wanting shape validation against a broader contract.

---

## 7) Instantiation Expressions (Generic Specialization Without Calling)

When you have a generic function and want to "pre-bind" the type parameter:

```ts
type Parser<T> = (input: string) => T;

function makeParser<T>(): Parser<T> {
  return (input) => JSON.parse(input) as T;
}

// You want: a Parser<User> factory without calling yet
const userParserFactory = makeParser<User>;
// Later you can call it:
const parseUser = userParserFactory();
```

Niche but useful for library code and factories.
