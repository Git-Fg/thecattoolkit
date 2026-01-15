# Type-Level Toolbox

Classical "advanced types" section, tuned for correctness and performance.

## A) Generics

### Use generics to express *relationships* between values and types
```ts
export function first<T>(items: readonly T[]): T | undefined {
  return items;
}
```

### Prefer constraints over `any`
```ts
type HasId = { id: string };

export function byId<T extends HasId>(items: readonly T[], id: string): T | undefined {
  return items.find((x) => x.id === id);
}
```

### Avoid "generic soup"
If you have more than 2–3 type parameters, it may be a smell:
- Can you derive one from another?
- Can you use an object type parameter instead?

---

## B) Conditional Types

### Control distributivity (very important for performance)

Conditional types distribute over unions by default:
```ts
type ToArray<T> = T extends any ? T[] : never;
type X = ToArray<string | number>; // string[] | number[]
```

To avoid distributive behavior, wrap in tuples:
```ts
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
type Y = ToArrayNonDist<string | number>; // (string | number)[]
```

**Use non-distributive forms when unions can get large.**

### `infer` for extraction
```ts
type ElementType<T> = T extends readonly (infer U)[] ? U : never;
type PType<T> = T extends Promise<infer U> ? U : never;
type FnReturn<T> = T extends (...args: any[]) => infer R ? R : never;
```

---

## C) Mapped Types

### Key remapping and filtering
```ts
type PickByValue<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K]
};

type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never
}[keyof T];
```

### Deep utilities (use carefully; can get expensive)
```ts
export type DeepReadonly<T> =
  T extends Function ? T :
  T extends readonly (infer U)[] ? readonly DeepReadonly<U>[] :
  T extends object ? { readonly [K in keyof T]: DeepReadonly<T[K]> } :
  T;

export type DeepPartial<T> =
  T extends Function ? T :
  T extends readonly (infer U)[] ? DeepPartial<U>[] :
  T extends object ? { [K in keyof T]?: DeepPartial<T[K]> } :
  T;
```

**Guidance:**
- Use deep types at **boundaries** (e.g., library API) not everywhere
- Deep recursive types can slow typechecking in large codebases

---

## D) Template Literal Types

Use for:
- Event names
- Route building
- Strongly typed "path selectors"
- Serialization keys

**Example: event handler names**
```ts
type EventName = "click" | "focus" | "blur";
type HandlerName = `on${Capitalize<EventName>}`;
```

**Be careful:** Template literal expansions can explode with large unions.

---

## E) Standard Library Utility Types (Know Them, Don't Re-invent Them)

Use built-ins:
- `ReturnType`, `Parameters`, `ConstructorParameters`, `InstanceType`
- `Partial`, `Required`, `Readonly`
- `Pick`, `Omit`
- `Exclude`, `Extract`, `NonNullable`
- `Record`
- `Awaited`

Re-inventing is sometimes pedagogical, but in real projects prefer the built-ins.
