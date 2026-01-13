# The Universal Engineering Standard for Agent Skills

## Division 1: Architectural Foundations (The Hierarchy)

The fundamental design of an Agent Skill is based on the **Filesystem-as-Context** model. A Skill is not a static text prompt; it is a directory structure that the Agent navigates dynamically. This architecture enables **Progressive Disclosure**, ensuring that the context window is only populated with information strictly necessary for the current step of a task.

### 1.1 The 3-Tier Loading Model
Every Skill must be structured to respect three distinct levels of data loading to prevent token bloat and performance degradation:

*   **Level 1: Metadata (The Discovery Layer)**
    *   **Components:** YAML frontmatter (`name`, `description`).
    *   **Behavior:** Always loaded into the System Prompt at startup.
    *   **Constraint:** Must be ultra-lightweight (~100 tokens). It serves as "SEO" for the model to decide if the Skill is relevant.
*   **Level 2: Instructions (The Logic Layer)**
    *   **Components:** The main body of `SKILL.md`.
    *   **Behavior:** Loaded into context only when the Skill is "activated" (matched by description).
    *   **Constraint:** Recommended < 500 lines. It should act as a high-level router or "onboarding guide" pointing to specific resources.
*   **Level 3: Resources (The Payload Layer)**
    *   **Components:** Files in `references/`, `scripts/`, `assets/`.
    *   **Behavior:** Remains on the filesystem. Consumes **zero context tokens** until the Agent explicitly reads them (via `Read`) or executes them (via `Bash`). This allows for unlimited potential knowledge (e.g., a 50MB API schema) with zero startup penalty.

### 1.2 The Hub-and-Spoke Topology
To maintain structural integrity, Skills must adhere to a flat navigational structure:
*   **The Rule:** Keep file references **one level deep** from `SKILL.md`.
*   **Negative Pattern (Daisy-Chaining):** `SKILL.md` links to `A.md`, which links to `B.md`. If the Agent performs a partial read on `A.md`, it may never discover the link to `B.md`.
*   **Positive Pattern (Hub-and-Spoke):** `SKILL.md` acts as the central hub, linking directly to every reference file.

### 1.3 The Atomic Unit Principle (Single Responsibility)
Each Skill should focus on **exactly one area of expertise**.
*   **Engineering Standard:** Avoid "Mega-Skills" that handle unrelated tasks (e.g., "PDF-and-Excel-Helper"). If a workflow is multifaceted, create separate Skills and use the "Pipeline Pattern" (see Division 6) to coordinate them.

---

## Division 2: Metadata & Discovery (The Interface)

The YAML frontmatter is the only interface the Agent uses to discover and understand the Skill's purpose.

### 2.1 The Description Field (The Trigger)
The `description` field is injected into the System Prompt and is used for semantic matching.
*   **Formula:** Capability + Trigger + Negative Constraint.
*   **Voice:** Always write in the third person ("Extracts data...") never the first or second ("I can help..." or "Use me...").
*   **Example:**
    ```yaml
    description: >
      Extracts raw text and tabular data from .pdf files.
      Use when the user mentions parsing, scraping, or converting PDF invoices.
      Do not use for PDF generation, editing, or image-to-PDF conversion.
    ```

### 2.2 Naming Constraints & Compatibility
*   **Reserved Words:** The `name` field strictly **forbids** the words `"anthropic"` and `"claude"`.
*   **Naming Format:** Use `kebab-case` (lowercase, alphanumeric, hyphens). Gerund form is preferred (e.g., `analyzing-logs`).
*   **The Compatibility Field:** Use the optional `compatibility` field (max 500 chars) to indicate environment requirements.
    ```yaml
    compatibility: "Requires Python 3.10+, 'pdfplumber' package, and access to local /tmp directory."
    ```

### 2.3 Visibility Control (`user-invocable`)
If a Skill is a "utility" (e.g., a complex JSON validator used only by other scripts), hide it from the user's slash-command menu to reduce UI clutter.
```yaml
user-invocable: false
```

---

## Division 3: Instruction Engineering (The Grammar)

Instructions are the code that directs the Agent's reasoning.

### 3.1 The "Delta" Instruction Standard
Assume the model is already competent in general programming and language tasks.
*   **Standard:** Only provide the "Delta"—the specific nuances, API keys, or internal workflows that the model cannot know from its training data.
*   **Negative Example:** Explaining what a PDF is or how `import pandas` works.
*   **Positive Example:** Providing the specific column mapping for the company's proprietary CSV format.

### 3.2 Degrees of Freedom
Explicitly state how much autonomy the Agent has:
*   **Heuristic (High Freedom):** "Prioritize maintainability over cleverness during code review."
*   **Protocol (Low Freedom):** "CRITICAL: Execute ONLY `scripts/migrate.py`. Do not modify flags. If it fails with code 127, STOP."

### 3.3 Conditional Workflow Pattern
Use explicit logical branching to prevent the Agent from mixing instructions between different modes of operation.
```markdown
## Modification Workflow
1. Determine task:
   - **New File?** -> Follow [Creation Guide](references/creation.md)
   - **Update File?** -> Follow [Update Guide](references/update.md)
```

---

## Division 4: Resource Management (The Filesystem)

### 4.1 Reference Structuring
*   **Table of Contents (TOC):** Every reference file > 100 lines **must** have a TOC at the top. This ensures that if the Agent performs a partial read (`head -n 100`), it sees the full scope of available information.
*   **Segmentation:** Split documentation by domain (e.g., `references/api-v1.md`, `references/api-v2.md`) to allow the Agent to read only what is relevant.

### 4.2 Shared Libraries & Integrity
*   **The Shared Library Pattern (Symlinks):** If multiple Skills need the same large resource (e.g., a 100MB database schema), place it in a `common/` directory at the root and use an internal symlink within each Skill directory. Symlinks are honored during the copy-to-cache process.
*   **The Checksum Protocol:** For critical binaries or data assets, include a manifest and verify integrity before execution.
    ```markdown
    Before running bin/validator, verify integrity:
    `sha256sum -c references/checksums.txt`
    ```

---

## Division 5: Execution Patterns (The Determinism)

### 5.1 The "Zero-Context" Script Runner
**Code-over-Text:** Whenever a task can be solved by a static script, bundle the script in `scripts/`.
*   **The Logic:** Asking an Agent to write code consumes tokens and risks bugs. Running a bundled script consumes zero tokens for the logic—only the output is billed.
*   **Instruction:** "To calculate DCF, run `python scripts/dcf.py inputs.json`."

### 5.2 Hardened Wrapper Standard
Scripts should be "Agent-Aware."
*   **JSON-over-Stdout:** Scripts should return structured JSON, not raw text. This allows the Agent to parse results programmatically.
*   **Non-Zero Exits:** Always use `sys.exit(1)` on failure to trigger the Agent's error-handling protocols.
    ```python
    if error:
        print(json.dumps({"status": "error", "message": "File not found"}))
        sys.exit(1)
    ```

### 5.3 Self-Locating Path Pattern
Never use hardcoded paths. Use the self-locating script pattern to ensure portability across local, plugin, and container environments.
```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, '../assets')
```

---

## Division 6: Workflow & State Management (The Persistence)

### 6.1 State Anchoring
Since context windows are ephemeral and compactions occur, Skills must mandate "State Anchoring" via persistent artifacts.
*   **Standard:** The first step of a complex Skill must be to create a `_state.md` file in the project root.
```markdown
# State
- [x] Step 1: Backup
- [ ] Step 2: Transform
**Last Checkpoint:** SUCCESS
```
*   **Recovery:** If the context is lost, the Agent reads `_state.md` to re-hydrate its progress.

### 6.2 Pipeline Sequencing
Define clear dependency graphs for multi-Skill workflows.
```markdown
# Sequence
1. **Analyze:** Run `xlsx` tool. Verify file exists.
2. **Present:** Run `pptx` tool. Charts MUST match Step 1 data.
```

### 6.3 Garbage Collection
Implement the "Clean-As-You-Go" rule. scripts should use `finally` blocks to delete intermediate artifacts (temp files), preventing disk bloat in the code execution container.

---

## Division 7: Interaction & UX Patterns (The Interfacing)

### 7.1 The Wizard Archetype (`AskUserQuestion`)
If a Skill requires missing data (e.g., an API Key), do not let the Agent "chat." Direct the Agent to use the `AskUserQuestion` tool to pause execution and gather specific input.
*   **Standard:** "If .env is missing, use `AskUserQuestion` to request the AWS_REGION."

### 7.2 The Search-Before-Read Protocol
To prevent context overflow when dealing with large files (>1MB):
*   **The Protocol:** Mandate a "Grep-then-Extract" flow.
    1.  Use `Grep` to find the relevant line numbers.
    2.  Use `wc -l` to verify the count.
    3.  Only `Read` the specific lines identified.

### 7.3 Approval Gates (Dry-Run)
For destructive actions (e.g., `rm -rf`), mandate a logic gate:
1.  Run `script --dry-run`.
2.  Display the list to the user.
3.  **Constraint:** Do not proceed unless the user provides a specific confirmation string (e.g., "CONFIRM DELETE").

---

## Division 8: Integration & Orchestration (The Ecosystem)

### 8.1 Skill-Agent Interface
Sub-agents (forked contexts) **do not inherit** Skills from the main session.
*   **Standard:** You must explicitly inject Skills into sub-agents via the `skills` parameter in the agent configuration.
    ```yaml
    # agents/reviewer.md
    skills: [linting-rules, security-guide]
    ```

### 8.2 Sub-Agent Context Forking
When using `context: fork`, specify the *Agent Type* to optimize for the task:
*   `Explore`: For fast, haiku-based searching.
*   `Plan`: For high-level reasoning.
*   `general-purpose`: For balanced execution.

### 8.3 MCP & LSP Whitelisting
*   **MCP Addressing:** Always use Fully Qualified Names: `ServerName:tool_name`.
*   **LSP Whitelist:** Whitelist specific atomic operations: `goToDefinition`, `findReferences`, `hover`, `documentSymbol`.

---

## Division 9: Security & Isolation (The Safety)

### 9.1 Tool Whitelisting (`allowed-tools`)
Apply the Principle of Least Privilege.
*   **Read-Only Skill:** `allowed-tools: [Read, Grep, Glob]`. This makes it physically impossible for the Agent to modify the filesystem, even if it hallucinates an instruction to do so.

### 9.2 Runtime Write Constraints
**The Read-Only Rule:** Skills are often cached in read-only directories (especially in Plugin environments).
*   **Rule:** Never instruct an Agent to write files inside the Skill directory.
*   **Standard:** Always output files to the **User's Project Root** or `/tmp/`.

### 9.3 The Vendor Strategy
For portability, "Vendor" small dependencies. Ship libraries inside the Skill's `scripts/libs/` folder rather than requiring the user to `pip install`. Use `sys.path.insert(0, ...)` to load them.

---

## Division  TEN: QA & Optimization (The Evaluation)

### 10.1 Evaluation-Driven Development Loop
Use two instances of Claude:
*   **Claude-A (The Author):** Writes the Skill.
*   **Claude-B (The Agent):** Attempts a task using the Skill.
*   **Loop:** Identify where Claude-B failed and update `SKILL.md` to address the gap.

### 10.2 Exponential Backoff
For Skills performing high-volume API calls, the bundled scripts **must** implement exponential backoff to handle rate limits (429 errors) gracefully without crashing the Agent's turn.

### 10.3 The 12-Point QA Checklist
1.  [ ] Description contains 3rd person Capability + Trigger?
2.  [ ] Negative constraints defined?
3.  [ ] Name excludes "anthropic" and "claude"?
4.  [ ] References are 1-level deep (Hub-and-Spoke)?
5.  [ ] TOC present for long reference files?
6.  [ ] `user-invocable` set for utility skills?
7.  [ ] `_state.md` artifact mandated for persistence?
8.  [ ] Scripts return JSON-over-Stdout?
9.  [ ] All file outputs directed to CWD/Tmp (not Skill dir)?
10. [ ] `allowed-tools` set to minimum required set?
11. [ ] Checksums included for critical assets?
12. [ ] Sub-agent forks specify an agent type?