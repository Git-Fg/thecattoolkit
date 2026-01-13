# Skills (Procedural Memory)

Skills are libraries of know-how activated on demand. They allow Claude to become a domain expert.

## 1. "Progressive Disclosure" Architecture

To save tokens, a Skill is structured in 3 levels.

### Level 1: The Trigger (Frontmatter)
Permanently loaded. Must be surgical.
*   **Rule:** 3rd person. Describes user *intentions*.
*   **Example:** `description: Used when the user asks to "audit security" or mentions "OWASP".`

### Level 2: `SKILL.md` (The Router)
Loaded upon activation. < 1500 words.
*   **Content:** Imperative procedures, links to references.
*   **Example:** "Step 1: Read `references/api-spec.md`. Step 2: Validate input."

### Level 3: Resources (`references/`)
Loaded on demand ("Lazy Loading").
*   Heavy documentation, Diagrams, Specs.

## 2. Configuration & Isolation

*   **`user-invocable: false`:** Hides the Skill from the user menu (internal usage).
*   **`allowed-tools: [Read]`:** Sandboxes the Skill (read-only).
*   **`context: fork`:** Executes the Skill in an isolated process (Cognitive Sandbox). Ideal for noisy research (reading 100 files) to avoid polluting the main history.

## 3. The 4 Skill Archetypes

### 1. The Procedural Skill ("Workflow Guide")
A strict checklist.
*   *Example:* Release Process.
*   *Structure:* Step-by-step instructions.

### 2. The Qualitative Skill ("The Artist")
Design, Tone, Style.
*   *Example:* CSS Guidelines.
*   *Structure:* "Do" vs "Don't" examples. No scripts.

### 3. The Migration Skill ("The Mapper")
Massive translation (API v1 -> v2).
*   *Structure:* `SKILL.md` routes to `references/mapping-table.md`.

### 4. The "Zero-Context" Skill ("Tool Wrapper")
Calls a script without explaining the code.
*   *Prompt:* "To convert PDF, do not write code. Run: `python ${CLAUDE_PLUGIN_ROOT}/scripts/convert.py`".
*   *Gain:* Speed, Reliability, 0 Source Code Tokens loaded.
*   *Why:* Claude doesn't need to read the implementation of `convert.py` to use it. It just needs to know the CLI arguments. This saves cognitive load for the "reasoning" part of the task.
