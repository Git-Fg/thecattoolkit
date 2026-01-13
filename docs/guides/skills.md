# Skills (Procedural Memory)

Skills are libraries of know-how activated on demand. They allow Claude to become a domain expert through a **3-tier progressive disclosure architecture**.

## 1. The 3-Tier Loading Model

Skills use a filesystem-based architecture with three distinct loading levels:

### Level 1: Metadata (Discovery)
- **Location:** YAML frontmatter (`name`, `description`)
- **Cost:** Always loaded at startup (~100 tokens)
- **Purpose:** Agent's "SEO" for relevance detection
- **Optimization:** Use `disable-model-invocation: true` to shrink catalog

### Level 2: Instructions (Logic)
- **Location:** Main body of `SKILL.md`
- **Cost:** Loaded on activation
- **Limit:** <500 lines recommended
- **Purpose:** High-level router/onboarding guide

### Level 3: Resources (Payload)
- **Location:** Files in `references/`, `scripts/`, `assets/`
- **Cost:** Zero context cost until accessed
- **Purpose:** Unlimited knowledge without token penalty
- **Pattern:** On-demand loading via explicit references

## 2. The Delta Standard

Only add context Claude doesn't already have.

**Question every instruction:**
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Example - Good (50 tokens):**
```markdown
## Extract PDF text

Use pdfplumber:

```python
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

Don't explain what PDFs are or how libraries work.
```

**Example - Bad (150 tokens):**
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common format that contains text, images, and other content. To extract text from a PDF, you'll need to use a library. There are many libraries available, but we recommend pdfplumber because it's easy to use...
```

## 3. Autonomy Levels

Match specificity to task fragility and variability.

### Protocol (Low Freedom)
Exact steps, no deviation. Use for:
- Database migrations
- Security validations
- Compliance checks

**Example:**
```markdown
CRITICAL: Execute ONLY scripts/migrate.py
Do not modify flags
If fails with code 127, STOP
```

### Guided (Medium Freedom)
Pattern-based with adaptation. Use for:
- Code reviews
- Architectural guidance
- Analysis tasks

**Example:**
```
Prioritize maintainability over cleverness
Follow criteria: 1) Readability, 2) Performance, 3) Security
```

### Heuristic (High Freedom)
Broad principles, maximum flexibility. Use for:
- Creative tasks
- Brainstorming
- Innovation

**Example:**
```
Apply your expertise to identify important issues
Use judgment to prioritize findings
```

## 4. The Four Universal Archetypes

### 1. Procedural Skill
**Purpose:** Deterministic, repeatable processes
- **Pattern:** Exact steps, validation gates, idempotent operations
- **Examples:** Migrations, security scans, compliance checks

### 2. Advisory Skill
**Purpose:** Provide expertise and recommendations
- **Pattern:** Heuristic principles, contextual adaptation, domain knowledge
- **Examples:** Code reviews, architectural guidance, best practices

### 3. Generator Skill
**Purpose:** Create structured outputs from inputs
- **Pattern:** Template-driven, validation-enhanced, iterative refinement
- **Examples:** Document generation, test creation, report formatting

### 4. Orchestrator Skill
**Purpose:** Coordinate multiple capabilities and workflows
- **Pattern:** Explicit dependencies, pipeline sequencing, state management
- **Examples:** Multi-step analysis, compound workflows, cross-domain tasks

## 5. Configuration & Isolation

### Frontmatter Options
*   **`user-invocable: false`:** Hides the Skill from the user menu (internal usage)
*   **`allowed-tools: [Read]`:** Sandboxes the Skill (read-only)
*   **`disable-model-invocation: true`:** Removes from model catalog, prevents auto-selection

### Context Forking
- **Purpose:** Protect main context from massive logs or file reads
- **Usage:** Define in agents/ with explicit skill injection
- **Rule:** Sub-agents do not inherit skills automatically

## 6. Trigger Optimization (The SEO Formula)

**Format:** Capability + Trigger + Negative Constraint

**Example:**
```yaml
description: Extracts raw text and tabular data from .pdf files. Use when user mentions parsing, scraping, or converting PDF invoices. Do not use for PDF generation, editing, or image-to-PDF conversion.
```

**Optimization Rules:**
1. Use specific triggers: "parsing PDF invoices" > "working with PDFs"
2. Use gerunds: "parsing", "analyzing", "extracting"
3. Include context anchoring: specific file types, use cases
4. State clear exclusions: what NOT to use it for
5. Third-person voice only: "Extracts data..." never "I can help..."

## 7. State Anchoring & Validation

### State Management
```markdown
# State
- [x] Step 1: Backup
- [ ] Step 2: Transform
**Last Checkpoint:** SUCCESS
```

**Requirements:**
1. Atomic checkpoints
2. Idempotent operations
3. Progress visibility
4. Failure isolation

### Validation-First Architecture
```markdown
## Document Processing Workflow
1. **Plan**: Create changes.json
2. **Validate**: Run scripts/validate_changes.py
3. **Execute**: Apply changes if validation passes
4. **Verify**: Run scripts/verify_output.py
```

**Use for:**
- Batch operations
- Destructive operations
- Complex workflows
- High-stakes tasks

## 8. The 12-Point QA Checklist

Before deploying any skill, verify:
- [ ] Description contains 3rd person Capability + Trigger?
- [ ] Negative constraints defined?
- [ ] Name excludes "anthropic" and "claude"?
- [ ] References are 1-level deep (Hub-and-Spoke)?
- [ ] TOC present for long reference files?
- [ ] `user-invocable` set for utility skills?
- [ ] `_state.md` artifact mandated for persistence?
- [ ] Scripts return JSON-over-Stdout?
- [ ] All file outputs directed to CWD/Tmp (not Skill dir)?
- [ ] `allowed-tools` set to minimum required set?
- [ ] Checksums included for critical assets?
- [ ] Sub-agent forks specify an agent type?

## 9. Architecture: Hub-and-Spoke

**Filesystem-as-Context Model:**
- SKILL.md is the central hub
- All references one level deep
- No daisy-chaining (A.md → B.md)

**Atomic Unit Principle:**
- One domain per Skill
- Users think of it as single operation
- Example: "Analyze PDF invoices" (one Skill), not "Process PDFs and generate reports" (two Skills)
