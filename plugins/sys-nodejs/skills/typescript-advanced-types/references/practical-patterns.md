# Practical Patterns

Copy/paste-ready patterns optimized for strong typing, minimal complexity, good inference, and reasonable compile time.

---

## Pattern 1 — Strongly Typed Configuration Objects

### Baseline: `satisfies` + `as const` (literal preservation)
```ts
type FeatureFlags = {
  auth: boolean;
  analytics: boolean;
  betaUI: boolean;
};

export const features = {
  auth: true,
  analytics: false,
  betaUI: false,
} as const satisfies FeatureFlags;

// - satisfies checks shape
// - as const preserves boolean literals (true/false)
```

### Prevent extra keys (common config requirement)
Use `satisfies` against an exact object type rather than an index signature.

```ts
type ExactFeatures = {
  auth: boolean;
  analytics: boolean;
};

export const exact = {
  auth: true,
  analytics: false,
  // extra: true, // error
} satisfies ExactFeatures;
```

---

## Pattern 2 — Type-Safe Event Emitter (Map-first)

```ts
export type EventMap = {
  "user:created": { id: string; name: string };
  "user:deleted": { id: string };
};

export class TypedEventEmitter<T extends Record<string, any>> {
  private listeners: { [K in keyof T]?: Array<(data: T[K]) => void> } = {};

  on<K extends keyof T>(event: K, cb: (data: T[K]) => void): void {
    (this.listeners[event] ??= []).push(cb);
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    this.listeners[event]?.forEach((cb) => cb(data));
  }
}

// Map literal checked with satisfies (keeps keys precise)
export const events = {
  "user:created": null,
  "user:deleted": null,
} satisfies Record<keyof EventMap, null>;
```

---

## Pattern 3 — Type-Safe API Client (Config-driven)

```ts
export type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";

export type EndpointConfig = {
  "/users": {
    GET: { response: { id: string; name: string }[] };
    POST: { body: { name: string; email: string }; response: { id: string } };
  };
  "/users/:id": {
    GET: { params: { id: string }; response: { id: string; name: string } };
    PUT: { params: { id: string }; body: { name?: string }; response: { ok: true } };
    DELETE: { params: { id: string }; response: { ok: true } };
  };
};

type ExtractParams<T> = T extends { params: infer P } ? P : never;
type ExtractBody<T> = T extends { body: infer B } ? B : never;
type ExtractResponse<T> = T extends { response: infer R } ? R : never;

export class APIClient<Config extends Record<string, Record<string, any>>> {
  async request<Path extends keyof Config, Method extends keyof Config[Path]>(
    path: Path,
    method: Method,
    ...[options]:
      ExtractParams<Config[Path][Method]> extends never
        ? ExtractBody<Config[Path][Method]> extends never
          ? []
          : [{ body: ExtractBody<Config[Path][Method]> }]
        : [{
            params: ExtractParams<Config[Path][Method]>;
            body?: ExtractBody<Config[Path][Method]>;
          }]
  ): Promise<ExtractResponse<Config[Path][Method]>> {
    // Replace with real fetch logic
    return {} as any;
  }
}
```

**Guidance:**
- Keep endpoint config small and modular
- If EndpointConfig becomes huge, split by feature and merge with `satisfies` to preserve inference

---

## Pattern 4 — Builder Pattern with Compile-Time "Completeness"

Powerful but can get expensive; use at boundaries where it pays off.

```ts
type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K
}[keyof T];

type IsComplete<T, S> =
  Exclude<RequiredKeys<T>, keyof S> extends never ? true : false;

export class Builder<T, S extends Partial<T> = {}> {
  private state: S = {} as S;

  set<K extends keyof T>(key: K, value: T[K]): Builder<T, S & Pick<T, K>> {
    (this.state as any)[key] = value;
    return this as any;
  }

  build(this: IsComplete<T, S> extends true ? this : never): T {
    return this.state as T;
  }
}
```
