# Skill Standards: The Protocol Layer

## 1. Philosophy: Skills are Lenses, Not Agents

Skills are **Passive Procedural Knowledge**. They are not "active" participants. They do not have "state". They are standards, templates, and methodologies that an Agent "puts on" like a lens to view a task.

> **The Law of Description:** The `description` field in the frontmatter is the **API Signature**. It matches the Agent's need to the Skill's capability.

---

## 2. Directory Structure

```
skills/
└── skill-name/
    ├── SKILL.md          # The "Lens" (Instructions)
    ├── scripts/          # Deterministic Tools (Python/Bash)
    ├── references/       # Deep Knowledge (Manuals)
    └── assets/           # Templates (Raw files)
```

**Auto-discovery:** All `SKILL.md` files in subdirectories are automatically indexed.```

---

## 3. The Frontmatter API

The `description` is the most important field. It determines **Automatic Loading**.

```yaml
---
name: strict-typescript
description: |
  USE when modifying .ts/.tsx files.
  Enforces strict type safety, no-any policy, and Zod validation standards.
matches: 
  - "*.ts"
  - "*.tsx"
---
```
**Semantic Matching:** Claude matches the `description` text to the current task. Include trigger phrases (e.g., "Use this when...") and examples in the description.

### The Triggering Matrix

| Tier | Use Case | Pattern |
|:-----|:---------|:--------|
| **1: High Fidelity** | Complex tasks, overriding default AI behavior | `[MODAL] when [CONDITION].` |
| **2: High Gravity** | Safety, Security, Governance | `[MODAL] USE when [CONDITION].` |
| **3: Utility** | Simple helper tools | `{Action} {Object}` |

### Proactive vs. Reactive Triggering
- **Proactive:** Claude notices the intent in conversation and suggests the skill.
- **Reactive:** The explicit use of a command forces a skill evaluation.
- **Key:** The `description` must match the *current* conversation state.

---

## 4. Writing Style: Imperative & Objective

Write for the **Agent**, not the User.

**✅ Correct (Declarative/Imperative):**
> "Verify all inputs using the Zod schema before processing."
> "Use the repository standard formatting."

**❌ Incorrect (Conversational):**
> "You should make sure to check the inputs."
> "I think it's robust to use Zod."

### Structural Organization (XML Headers)
For complex skills (e.g., a migration guide or aesthetic standard), use **Semantic XML Tags** to group instructions. This helps the model's attention mechanism distinguish between different rule sets.

**Example (Prompt Organization):**

```xml
<frontend_aesthetics>
  Focus on typography and whitespace. Avoid "AI Slop" gradients.
  ...
</frontend_aesthetics>

<coding_guidelines>
  Use React.memo() for all list items.
  ...
</coding_guidelines>
```

**Benefits:**
*   **Hierarchical:** Creates clear "sections" in the system prompt.
*   **Integration:** When mixing multiple skills, XML tags prevent rules from bleeding into each other.
*   **Maintainability:** Easier to grep/replace sections of a prompt programmatically.

---

## 5. Progressive Disclosure

Do not dump 10,000 tokens of documentation into the context.

### The 3-Level Loading Hierarchy
1.  **Level 1 (Metadata):** `name` + `description`.
    -   **When:** Startup / Context Construction.
    -   **Cost:** ~100 tokens. Always visible.
2.  **Level 2 (Instructions):** `SKILL.md` body.
    -   **When:** Triggered by description match (Claude decides).
    -   **Cost:** <2000 tokens. Injected dynamically.
3.  **Level 3 (Resources):** `references/*.md`, `scripts/`, `assets/`.
    -   **When:** Agent explicitly calls `Read("references/guide.md")` or `Bash("scripts/do_thing.sh")` when it determines it needs more detail or action. Loading is **NOT automatic** upon skill activation; the model must "reach out" for these resources.
    -   **Cost:** Unlimited (On-demand).
    -   **Zero-Context Capabilities:** Scripts in the `scripts/` directory can be executed via the `Bash` tool to perform complex logic without ever being read into the context window. This provides an "unlimited" token budget for procedural logic.

**Refactor Rule:** If your `SKILL.md` is >500 lines, move sections to `references/`.
