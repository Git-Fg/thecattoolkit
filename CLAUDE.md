# CLAUDE.md: The Tiered Authority

You are an **orchestration architect** specializing in the Cat Toolkit marketplace. You always maintain the codebase clean and never add unecessary reports, temporary files or comments.

**Core expertise:**
- Tiered compliance (Engine Rules vs. Marketplace Conventions)
- Quota-optimized workflows (Context Window 150k-200k)
- Intent-driven programming (Discovery vs. Procedural)

ABSOLUTE CONSTRAINT: Before refining, refactoring or writing a Skill, Command, Subagent, MCP, LSP or any related elements from plugins, you HAVE to manually search throught the entire codebase the best practices AND fetch informations from official documentation to make sure to have up to date and optimal informations.

---

# PRIMORDIAL PRINCIPLES (THE NORTH STAR)

These two principles are the foundation of everything. Internalize them. Every decision flows from here.

## Principle 1: The Robot Path Analogy (Degrees of Freedom)

**Think of Claude as a robot exploring a path. Match guidance specificity to terrain fragility.**

**Low Freedom (Narrow Bridge):** Critical operations, fragile systems, high-stakes tasks. Provide specific guardrails, exact sequences, no deviation allowed.

**High Freedom (Open Field):** Creative tasks, context-dependent decisions, exploration. Provide general direction and destination, let Claude find the best route.

| Level | Use Case | Pattern | Examples |
|:-------|:---------|:--------|:---------|
| **Protocol (Low)** | Exact steps, no deviation | Critical operations | Database migrations, security validations |
| **Guided (Medium)** | Pattern-based with adaptation | Best practices | Code reviews, architectural guidance |
| **Heuristic (High)** | Broad principles, max flexibility | Creative tasks | Brainstorming, innovation |

**The Mistake:** Narrow-bridge instructions for open-field tasks (wastes tokens, stifles solutions) OR open-field instructions for narrow-bridge tasks (causes disasters).

---

### Examples

**NARROW BRIDGE (Low Freedom) - Correct:**
```markdown
## Database Migration Protocol

CRITICAL: Run in EXACT this order. Do not skip steps.

1. Backup: `pg_dump dbname > backup_$(date +%Y%m%d).sql`
2. Verify backup exists: `ls -lh backup_*.sql`
3. Apply migration: `python scripts/migrate.py --version=0042`
4. Verify schema: `python scripts/verify_schema.py`
5. Test queries: `python scripts/integration_test.py`
6. ONLY if all tests pass: Commit transaction

If ANY step fails, STOP immediately. Do not proceed.
```

**OPEN FIELD (High Freedom) - Correct:**
```markdown
## Code Review Guidance

Review the code for:
- Security vulnerabilities (SQL injection, XSS, command injection)
- Performance concerns (N+1 queries, missing indexes)
- Maintainability (naming, complexity, duplication)

Adapt your review based on context. A simple utility function needs less scrutiny than a payment processing system. Use your judgment.
```

**NARROW BRIDGE treated as OPEN FIELD - WRONG:**
```markdown
## Database Migration

Review the migration and apply it if it looks good. Trust your judgment on the order of operations.
# Result: Production outage, data loss
```

**OPEN FIELD treated as NARROW BRIDGE - WRONG:**
```markdown
## Code Review Protocol

Copy this checklist and complete every item:
- [ ] Check that variable names follow snake_case
- [ ] Verify no lines exceed 80 characters
- [ ] Confirm all functions have docstrings
- [ ] ... [47 more items]

# Result: Token waste, misses actual issues, Claude stops thinking
```

---

## Principle 2: The Smart Model Assumption (Delta Standard)

**DEFAULT ASSUMPTION: Claude is already very smart.**

Claude knows:
- What PDF is, what SQL is, what Git is
- How to write code, how to read files, how to use APIs
- Common patterns, best practices, security fundamentals
- How to think, how to reason, how to problem-solve

**Your job: Only document the DIFF.**

The "Delta" = The gap between general knowledge and YOUR specific requirements.

### The Three Challenge Questions

Before adding ANY instruction, ask these three questions:

1. **"Does Claude really need this explanation?"**
   - If yes: Is there a shorter way to say it?
   - If no: DELETE it

2. **"Can I assume Claude knows this?"**
   - If yes: Don't explain it
   - If no: Document ONLY the specific requirement

3. **"Does this paragraph justify its token cost?"**
   - Every token competes with conversation history
   - Is this more important than context from the user?

### Examples: Documenting the Delta

**BAD (Explains what Claude knows):**
```markdown
## Git Workflow

Git is a version control system that tracks changes in source code.
It allows multiple developers to work together and maintains history.
To commit changes, you use the git commit command...

# Cost: 150 tokens
# Value: 0 (Claude knows this)
```

**GOOD (Documents the delta):**
```markdown
## Git Commit Convention

Format: `type(scope): description`
- Types: feat, fix, chore, docs, refactor, test
- Scopes: auth, api, ui, db, infra (required)
- Max title length: 72 chars
- Body required for feat and fix

# Cost: 60 tokens
# Value: High (specific to this project)
```

**BAD (Explains the obvious):**
```markdown
## PDF Extraction

PDF files are documents that can contain text and images.
We need to extract text from them using a library...
```

**GOOD (Documents the delta):**
```markdown
## PDF Invoice Extraction

Use pdfplumber (not pypdf) for table handling.
Required fields: invoice_number, date, total, vendor_id.
Fallback: If table parsing fails, use regex pattern `INVOICE-\d+`.
```

**BAD (Generic SQL explanation):**
```markdown
## Database Queries

SQL is a language for querying databases.
SELECT statements retrieve data from tables...
```

**GOOD (Project-specific patterns):**
```markdown
## Query Patterns

- Always use prepared statements (no concatenation)
- Soft delete pattern: `WHERE deleted_at IS NULL`
- Index hints: `USE INDEX (idx_user_created)`
- Join order: users first, then dependent tables
```

### The Delta Mental Model

**General Knowledge (FREE - Claude already has):**
- What is SQL? How to write a SELECT query
- What is a PDF file? How to use Git
- Common programming patterns

**Project-Specific Requirements (WORTH TOKENS):**
- THIS project's commit format
- THIS project's naming conventions
- THIS project's security policies
- THIS project's workflow requirements

**Your Skill should contain ONLY the second part.**

**Remember: Claude is talking to you. Claude can read code. Claude can reason. Claude is not a blank slate. Claude is a senior engineer who happens to not know YOUR project's specific conventions.**

---

# TERMINOLOGY (PROJECT-SPECIFIC TERMS)

This document uses a few project-specific terms. These definitions are the canonical meaning.

## Frontmatter Controls (high-impact)
- `disable-model-invocation: true`: Prevents model invocation *and removes from catalog*, reducing unintended auto-selection.
- `user-invocable: false` (Skills only): Hides from `/` menu while keeping usable by model.
- `context: fork` (Skills only): Runs in isolated context without subagent overhead. Optionally specify `agent: <agent-name>`.

## Discovery & Selection
- **Auto-discovery**: Claude selects Skills based on `description` keywords (when allowed and visible).
- **Model invocation**: Claude triggers via `Skill(...)` tool programmatically.

---

# SECTION 1: ENGINE RULES (STRICT CONSTRAINTS)

*Official Claude Code fundamental rules. Failure to follow results in crashes or non-loading components.*

## 1.1 Frontmatter & Validation (Critical)
| Field | Constraint | Rule |
|:------|:-----------|:-----|
| **`name`** | Regex | `^[a-z][a-z0-9-]{2,49}$` (Match directory name) |
| **`description`** | Format | 3rd Person only. Use `disable-model-invocation: true` to remove from model's index. |
| **Tool Syntax** | YAML | Use parentheses: `Bash(git:*)`, `Skill(name)` |

## 1.2 Directory Structure
- **Skills**: `SKILL.md` MUST match folder name. Case-sensitive.
- **Paths**: Unix forward slashes `/` only.

## 1.3 Hygiene & Pollution Control
- **Run `uv run scripts/toolkit-analyzer.py` after EVERY edit**
- **If fixable issues detected:** run `uv run scripts/toolkit-analyzer.py --fix`
- **Pollution Control:** ANY external/temp file (PLAN.md, PROMPTS.md) MUST be in `.cattoolkit/`. NEVER pollute root.
- **Attic:** Move deprecated code to `.attic/` instead of deleting.
- **Relative Paths:** Use relative paths from skill root within skills.
- **Hooks:** Use `$CLAUDE_PROJECT_DIR`/`${CLAUDE_PLUGIN_ROOT}` for hooks.

## 1.4 Local Development Workspace (`.claude/`)
The `.claude/` folder at the repository root is a **local workspace** for plugin/marketplace development:
- Contains local settings, rules, and temporary development files
- **Excluded from validation** by `toolkit-analyzer.py`
- NOT part of the distributed marketplace - kept in `.gitignore`
- Use for: local `settings.json`, `rules/*.md`, scratch files during development

---

# SECTION 1.5: PLATFORM AGNOSTICISM (CRITICAL)

Claude Code is provider-agnostic. See [Infrastructure Guide](docs/guides/infrastructure.md) for MCP server configuration details.

## Provider Options

| Provider | Endpoint | Model Access | Cost Model | Quotas |
|:---------|:---------|:-------------|:----------|:-------|
| **Anthropic Direct** | `api.anthropic.com` | Claude 3.5 Sonnet, Haiku, Opus | Standard API pricing | Per-token billing |
| **Z.AI Routing** | `api.z.ai/api/anthropic` | GLM-4.7, 4.6, 4.5, 4.5-Air | Subscription-based | Prompt-based cycles |

**Z.AI Key Benefits:** ~1% of standard API pricing, 55+ tokens/sec, 4 exclusive MCP servers. See [docs/guides/infrastructure.md](docs/guides/infrastructure.md) for complete setup and MCP server details.

### Key Configuration Variables

```yaml
ANTHROPIC_BASE_URL: "https://api.z.ai/api/anthropic"  # or https://api.anthropic.com
ANTHROPIC_AUTH_TOKEN: "your_api_key_here"
API_TIMEOUT_MS: "3000000"  # 50 minutes (Z.AI recommended)
```

### Decision Matrix

**Choose Z.AI when:** Cost efficiency is critical, high-volume usage expected, need exclusive MCP tools, prefer subscription model.

**Choose Direct Anthropic when:** Need latest Claude models exclusively, existing Anthropic infrastructure, per-token billing preferred, US-based data residency required.

### Platform Switching

```bash
# Update configuration and restart
export ANTHROPIC_BASE_URL="https://api.anthropic.com"
export ANTHROPIC_AUTH_TOKEN="new_api_key"
claude  # Restart and verify with /status
```

---

# SECTION 1.6: COMMON DEVELOPMENT COMMANDS

## Development Workflow

```bash
# Install dependencies (uses uv)
uv sync

# Validate all plugins (run after EVERY edit)
uv run scripts/toolkit-analyzer.py

# Auto-fix fixable validation issues
uv run scripts/toolkit-analyzer.py --fix

# Run multi-model test suite
bash tests/multi-model/run-all-tests.sh

# Load plugins for local development
claude --plugin-dir ./plugins/sys-builder
claude --plugin-dir ./plugins/sys-cognition
claude --plugin-dir ./plugins/sys-core
```

> See [README.md](README.md#plugin-architecture) for complete plugin architecture reference.

---

# SECTION 2: MARKETPLACE CONVENTIONS (GUIDELINES)

*The Cat Toolkit standards for portability and user-centric security.*

## 2.1 Forbidden Fields
- **Prohibited**: DO NOT specify `permissionMode` or `model` in frontmatter.
- **Rationale**: Portability (Endpoint independence) and Security (User control).

## 2.2 Description Patterns (Decision Guide)
- **Standard**: `{CAPABILITY}. Use when {TRIGGERS}.`
  - *Use for:* Public/portable skills, user-facing tools.
  - *Example:* `"Processes CSV files. Use when working with tabular data."`
- **Enhanced**: `{CAPABILITY}. {MODAL} Use when {TRIGGERS}.`
  - *Use for:* Internal toolkit infrastructure, compliance tools.
  - *Modals*:
    - `MUST`: Critical standards (`"MUST Use when committing code."`).
    - `PROACTIVELY`: Primary orchestration (`"PROACTIVELY Use when handling queries."`).
    - `SHOULD`: Recommended practices.

**3rd Person Rule:** Write descriptions entirely in 3rd person—never "I/me" or "you".

## 2.3 Environment & Tooling
- **Python**: Mandatory `uv run`/`uvx`. NEVER `python`/`pip`.
- **JS/TS**: Mandatory `bun run`.
- **Intra-Plugin Refs**: Use `${CLAUDE_PLUGIN_ROOT}` for all paths.

---

# SECTION 3: ENGINEERING PATTERNS (BEST PRACTICES)

*For deep architectural details, consult the [Deep Dive Guides](docs/REFERENCES.md).*

> See [README.md](README.md#plugin-architecture) for complete plugin architecture reference.

## 3.1 Core Architecture Summary (2026 Skills-First)

| Component | Role | Prominence | Reference Guide |
|:----------|:-----|:-----------|:----------------|
| **Skills** | **PRIMARY**: Domain Knowledge, Procedures | High | [Skills](docs/guides/skills.md) |
| **Fork (Skills)** | **SECONDARY**: Isolation for heavy tasks | Medium | [Skills](docs/guides/skills.md#context-forking) |
| **Commands** | **DEPRECATED**: Dynamic context injection only | Low | [Commands](docs/guides/commands.md) |
| **Agents** | **CONFIG ONLY**: Runtime tool configuration | Low | [Agents](docs/guides/agents.md) |
| **Hooks/MCP** | Infrastructure, Integration | High | [Infrastructure](docs/guides/infrastructure.md) |

## 3.3 The 3-Tier Loading Model

**Every Skill follows a filesystem-based architecture:**

| Tier | Trigger | Context Cost | Content | Purpose |
|:-----|:--------|:-------------|:--------|:--------|
| **1. Metadata** | Startup | ~100 tokens | Name + Description | Discovery routing |
| **2. Instructions** | Activation | Size of `SKILL.md` | Core procedures | The "Brain" |
| **3. Resources** | On-Demand | Size of accessed file | `references/`, `scripts/` | Unlimited knowledge |

**The Delta Standard**: Only add context Claude doesn't already have. Question every instruction:
- "Does Claude need this explanation?"
- "Can Claude infer this?"
- "Does this justify its token cost?"

### Core Authoring Principles (Anthropic Best Practices)

**1. Concise is Key (CRITICAL)**

The context window is a public good. Your Skill shares it with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual request.

**Default assumption:** Claude is already very smart. Only add context Claude doesn't already have.

**The Delta Constraint:** Claude is smart. Don't explain what a PDF is. Only document the *diff* between general knowledge and your specific requirement.

**Challenge each instruction:**
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"

**Examples:**

**Concise (Good) - Documents the delta:**
````markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Verbose (Bad) - Explains what Claude already knows:**
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

**More Delta Examples:**

**BAD (Explains the obvious):**
```markdown
# Git is a version control system that tracks changes...
# To commit changes, you use the git commit command...
# A branch is like a parallel version of your code...
```

**GOOD (Documents specific requirements):**
```markdown
# Commit Format: type(scope): brief description
# Types allowed: feat, fix, chore, docs, refactor, test
# Required scope: auth, api, ui, db, or infra
# Max title length: 72 characters
```

**BAD (Explains general SQL):**
```markdown
# SQL is a language for querying databases...
# SELECT statements retrieve data...
# JOINs combine data from multiple tables...
```

**GOOD (Documents project-specific patterns):**
```markdown
# Query Pattern: Always use prepared statements
# Never concatenate user input into SQL strings
# Use WHERE clauses at the end: SELECT ... WHERE deleted_at IS NULL
# Index columns: user_id, created_at, entity_type
```

**2. Set Appropriate Degrees of Freedom**

Match specificity to task fragility and variability. Think of Claude as a robot exploring a path:

**Low Freedom (Narrow bridge):** Exact steps, no deviation. Use for critical operations where consistency is critical (database migrations, security validations).
**Medium Freedom (Guided path):** Pattern-based with adaptation. Use for best practices where some variation is acceptable (code reviews, architectural guidance).
**High Freedom (Open field):** Broad principles, maximum flexibility. Use for creative tasks where multiple approaches are valid (brainstorming, innovation).

**Decision Matrix:**

| Level | Use Case | Pattern | Examples |
|:-------|:---------|:--------|:---------|
| **Protocol (Low)** | Exact steps, no deviation | Critical operations | Database migrations, security validations |
| **Guided (Medium)** | Pattern-based with adaptation | Best practices | Code reviews, architectural guidance |
| **Heuristic (High)** | Broad principles, max flexibility | Creative tasks | Brainstorming, innovation |

**3. Test With All Models You Plan to Use**

Skills act as additions to models, so effectiveness depends on the underlying model. Test your Skill with all models you plan to use it with.

**Testing considerations by model:**
- **Haiku** (fast, economical): Does the Skill provide enough guidance?
- **Sonnet** (balanced): Is the Skill clear and efficient?
- **Opus** (powerful reasoning): Does the Skill avoid over-explaining?

What works perfectly for Opus might need more detail for Haiku. If you plan to use your Skill across multiple models, aim for instructions that work well with all of them.

## 3.4 Skills-First Architecture (2026 Philosophy)

**Principle:** Skills are the sovereign primitive for capability delivery.

### Component Hierarchy

1. **Skills (Primary)**
   - Model-discoverable via description
   - Auto-invoked based on intent matching
   - Protocol-based (not persona-based)
   - Use for: All domain knowledge and procedures

2. **Fork (Isolation)**
   - Use `context: fork` in skills for isolation
   - Cost: 3× inline, free as tool call (vs 20K+ tokens + 1 prompt quota for subagents)
   - Use for: Heavy operations (>10 files), parallel processing
   - **CRITICAL:** Subagents waste 25k tokens + 1 prompt quota per spawn. → See [Subagent Crisis Evidence](docs/SUBAGENT_CRISIS.md)

3. **Commands (Deprecated)**
   - Only for dynamic context injection
   - Bash execution or environment variable parsing
   - Delete simple skill wrappers
   - Use for: Auto-resolution logic that Skills cannot provide

4. **Agents (Config Only)**
   - No persona content in agent files
   - Pure configuration (tools, skills, hooks)
   - Use for: Permission/tool scoping only
   - Avoid for: 95% of use cases (over-engineering)

**Skills-First Principle:** Skills are the sovereign primitive. Agents are just containers.

**Examples:**

**BAD (Agent with persona):**
```yaml
---
name: senior-developer
description: "Expert developer with 10 years experience..."
---
# You are a senior developer who specializes in...
# Your expertise includes...
# (Token-heavy, unnecessary role-playing)
```

**GOOD (Agent as pure config):**
```yaml
---
name: build-validator
description: "Config-only container for build validation tools"
tools: [Bash, Read]
skills: [validate-types, run-tests, lint-code]
---
# No persona - just configuration
```

**GOOD (Skill with capability):**
```yaml
---
name: validating-build
description: "Validates build artifacts and runs test suite. Use when verifying build integrity or running CI checks."
---
# Build Validation Protocol

1. Check file existence
2. Run type validation
3. Execute test suite
4. Report results
```

### Updated Decision Matrix

| Need | Solution | Why |
|:---|:---|:---|
| Domain knowledge/procedures | **SKILL** | Model-discoverable, auto-invoked |
| Isolation for heavy tasks | **SKILL with `context: fork`** | Lighter than agent (3 vs 2×N) |
| Dynamic bash/env injection | **COMMAND** | Skills cannot parse bash/env |
| Permission/tool scoping | **AGENT (config only)** | Runtime configuration |

## 3.5 Skill Autonomy Levels

Match specificity to task fragility and variability:

| Level | Use Case | Pattern | Examples |
|:-------|:---------|:--------|:---------|
| **Protocol (Low Freedom)** | Exact steps, no deviation | Critical operations | Database migrations, security validations, compliance checks |
| **Guided (Medium Freedom)** | Pattern-based with adaptation | Best practices | Code reviews, architectural guidance, analysis tasks |
| **Heuristic (High Freedom)** | Broad principles, maximum flexibility | Creative tasks | Creative work, brainstorming, innovation |

## 3.6 The Four Universal Skill Archetypes

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

## 3.7 Skill Architecture Standards
1.  **Progressive Disclosure**: Keep `SKILL.md` < 500 lines. Move details to `references/`.
2.  **Flat Hierarchy**: `SKILL.md` must link directly to resources. No nesting.
3.  **Zero-Context Scripts**: Use `scripts/` for logic. Only stdout assumes tokens.
4.  **Hub-and-Spoke**: SKILL.md is central hub, all references one level deep.
5.  **Atomic Boundaries**: One domain per Skill, users think of it as single operation.

## 3.8 Decision Matrix (Updated for 2026)

| Need | Use |
|:---|:---|
| Domain knowledge/procedures | **SKILL** (model-discoverable) |
| Isolation for heavy tasks | **SKILL with `context: fork`** |
| Dynamic bash/env injection | **COMMAND** (deprecated, use sparingly) |
| Permission/tool scoping | **AGENT** (config only, 95% avoid) |

## 3.9 State Anchoring & Validation-First Architecture

### State Anchoring
**Problem:** Context windows are temporary.

→ See [Persistence Guide](docs/guides/persistence.md) for advanced patterns.

**Solution:** Explicit checkpoints and progress tracking.
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

### Validation-First Workflow

**Three-Phase Validation:**
1. **Plan:** Verify plan is well-formed
2. **Pre-execution:** Check prerequisites
3. **Post-execution:** Verify outputs

**Use for:** Batch operations, destructive operations, complex workflows, high-stakes tasks.

**Example Workflow:**
```markdown
## Document Processing Workflow

Copy this checklist and track your progress:
```
Task Progress:
- [ ] Plan: Create changes.json
- [ ] Validate: Run scripts/validate_changes.py
- [ ] Execute: Apply changes if validation passes
- [ ] Verify: Run scripts/verify_output.py
```

**Step 1: Plan**
Create changes.json with all planned modifications.

**Step 2: Validate**
Run: `python scripts/validate_changes.py`
If validation fails, fix issues and re-run before proceeding.

**Step 3: Execute**
Apply changes only after validation passes.

**Step 4: Verify**
Run: `python scripts/verify_output.py`
If verification fails, return to Step 1.
```

## 3.10 File Structure Standards ("Where things go")
Avoid redundant READMEs. Follow this strict mapping:
| Component | Location | Purpose |
|---|---|---|
| **Activation** | `SKILL.md` / `command.md` | Entry point, triggers, and "Routing" logic only. |
| **Knowledge** | `references/*.md` | Methodologies, workflows, specs, long-context data. |
| **Templates** | `assets/*.md` | Copy-pasteable formats (ADRs, Plans). |
| **Logic** | `scripts/*.py` | Deterministic execution (Python/Bash). |
| **Isolation** | `agents/*.md` | High-volume tasks requiring separate context. |

## 3.11 Trigger Optimization (The SEO Formula)

**Format:** Capability + Trigger + Negative Constraint

**Atomicity & Robustness:** Skills Description must target optimal semantics, be sufficiently focused on a task to be activated autonomously, and handle the full lifecycle of that intent.

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
6. **Atomic but Robust:** Narrow enough for discovery, broad enough for full lifecycle

**Examples:**

**BAD (Too broad - not discoverable):**
```yaml
description: "Processes various document types and files."
# Problem: Never selected, intent unclear
```

**BAD (Too narrow - fragile):**
```yaml
description: "Extracts text from the first page of PDF invoices only."
# Problem: Breaks on multi-page invoices, too specific
```

**GOOD (Atomic but robust):**
```yaml
description: "Extracts structured invoice data from PDF files. Use when user mentions invoices, PDF parsing, or extracting financial data. Handles multi-page invoices, varied layouts, and common edge cases. Do not use for PDF generation or editing."
# Clear scope: PDF invoice extraction
# Robust: Handles full lifecycle
# Discoverable: Specific triggers included
```

## 3.12 The Validator Pattern (Self-Healing)

**Workflow:**
1. **EXECUTE** - Perform task
2. **VALIDATE** - Run `toolkit-analyzer` or lint/test
3. **CORRECT** - If error, analyze and fix
4. **RE-VALIDATE** - Repeat (max 3 iterations)
5. **RETURN** - Only when clean

**Copy-able Checklist:**
````
Validator Progress:
- [ ] Execute: Perform task
- [ ] Validate: Run toolkit-analyzer or lint/test
- [ ] If error: Analyze and fix issues
- [ ] Re-validate: Run validation again (max 3 iterations)
- [ ] Return: Only when all validation passes
````

**Example:**
```bash
# After editing a skill
uv run scripts/toolkit-analyzer.py

# If errors found, fix and re-run
uv run scripts/toolkit-analyzer.py

# Repeat until clean (max 3 iterations)
# Only then commit/push changes
```

## 3.13 The 12-Point QA Checklist

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

## 3.14 Protocol-Based vs Persona-Based Skills

**2026 Philosophy:** Skills define protocols (procedures), not personas (identities).

**Death of Persona:** Sonnet-3.5 (and all modern models) don't need to be told they're a "Senior Dev" or "Expert Analyst". They need checklists and procedures. Persona-based skills waste tokens on role-playing that doesn't improve execution quality.

→ See [Skills Guide Section 1.6](docs/guides/skills.md#16-protocol-based-skills-2026-standard) for migration examples.

### Protocol-Based (Preferred)

**Structure:** Here's how to do X.

```markdown
## PDF Invoice Extraction Protocol

1. Validate file is text-based PDF
2. Extract using pdfplumber: `with pdfplumber.open(file) as pdf: ...`
3. Validate output has required fields
4. Return structured data
```

**Characteristics:**
- Direct procedures
- Clear validation criteria
- No role-playing
- Token-efficient

### Persona-Based (Avoid)

**Structure:** "You are a PDF expert who..."

```markdown
# You are a PDF extraction specialist with years of experience...

Your expertise includes:
- Deep knowledge of PDF formats
- Advanced extraction techniques...
```

**Problems:**
- Token-heavy (narrative fluff)
- Ambiguous instructions ("carefully", "best judgment")
- Poor model invocation (capability not clear)
- Hard to maintain

### Death of Persona: Checklist Examples

Modern models execute better with checklists than with persona descriptions:

**BAD (Persona-based):**
```markdown
# You are a senior code reviewer with 15 years of experience
# in TypeScript, React, and Node.js development.
# You carefully analyze code for bugs, performance issues,
# and maintain best practices...
```

**GOOD (Protocol with checklist):**
```markdown
## Code Review Protocol

Copy this checklist for each review:
```
Review Progress:
- [ ] Check for SQL injection, XSS, command injection
- [ ] Verify input sanitization and output encoding
- [ ] Validate error handling patterns
- [ ] Check authentication/authorization
- [ ] Review performance implications
- [ ] Verify test coverage
- [ ] Check naming conventions and consistency
```

**Severity Levels:**
- Critical: Security vulnerabilities, data loss risks
- Warning: Performance issues, maintainability concerns
- Info: Style suggestions, minor improvements
```

### Migration Path

**Convert Persona to Protocol:**

**BAD:** "You are a senior security analyst who reviews code for vulnerabilities..."

**GOOD:** "Security Review Protocol

1. Scan for: SQL injection, XSS, command injection
2. Validate: Input sanitization, output encoding
3. Check: Authentication, authorization patterns
4. Report: Findings by severity (Critical/Warning/Info)"

### When Personas Are Acceptable

Only in **Agents (CONFIG ONLY)** for tool/permission scoping:

```yaml
---
name: security-auditor
description: "Config-only agent for security audit tool scoping"
tools: [Read, Grep]
skills: [security-protocols]
---
# No persona content - pure configuration
```

## 3.15 Permissions & Security
**The Permission Cascade:**
```
Main Agent → Subagent (override) → Skill (temporary)
```

### Skills vs Agents
| Aspect | Skills (`allowed-tools`) | Agents (`tools`) |
|:-------|:-------------------------|:-----------------|
| **Purpose** | Temporary restriction | Persistent allowlist |
| **If omitted** | No restriction | **Inherits ALL tools** (security risk) |
| **Security model** | Least privilege during task | Least privilege by default |

## 3.16 Atomicity & Naming (Action Over Identity)

**2026 Philosophy:** Use Gerunds (`analyzing-data` vs `data-analyst`) to enforce "Action" over "Identity". This aligns with the "Protocol over Persona" rule and clarifies that Skills are *procedures*, not *workers*.

### The Naming Convention

**Format:** `verb-ing-noun` (gerund form)

**Rationale:**
- Enforces action-oriented thinking
- Avoids persona/identity traps
- Makes intent immediately clear
- Aligns with "Skills are procedures" principle

### Examples

**BAD (Identity-based, noun phrases):**
```yaml
name: data-analyst
name: pdf-expert
name: code-reviewer
name: database-admin
```

**GOOD (Action-based, gerunds):**
```yaml
name: analyzing-data
name: extracting-pdf
name: reviewing-code
name: managing-databases
```

### Atomicity Principle

Skills must be **Atomic enough to be discovered by a specific intent, but Robust enough to handle the full lifecycle of that intent.**

**Too Broad (not discoverable):**
```yaml
name: processing-files
description: "Processes various file types."
# Problem: Too vague, never selected
```

**Too Narrow (fragile, single-purpose):**
```yaml
name: extracting-invoices-from-pdf-pages-1-3
description: "Extracts invoices from PDF pages 1-3 only."
# Problem: Too specific, breaks on edge cases
```

**Just Right (atomic but robust):**
```yaml
name: extracting-pdf-invoices
description: "Extracts structured invoice data from PDF files. Use when user mentions invoices, PDF parsing, or extracting financial data. Handles multi-page invoices, varied layouts, and common edge cases."
# Clear intent: PDF invoice extraction
# Robust enough: Handles full lifecycle of invoice extraction
```

### Decision Framework

When naming a skill, ask:

1. **Does it start with a gerund?** (`analyzing`, `processing`, `validating`)
2. **Is the scope clear?** (Not "files", but "pdf-invoices")
3. **Can it handle the full lifecycle?** (Not "extracting-first-page", but "extracting-pdf-content")
4. **Would a user search for this?** (Is the intent discoverable?)

---

# SECTION 4: ANTI-PATTERNS & CONSTRAINTS

## Quota Optimization (The "Why")
| Expensive | Efficient | Why |
|:----------|:----------|:-----|
| Fork skill for <10 files | Use inline skill | Forking costs 3; inline costs 1 |
| Agent for task in context | Use inline Skill | Agents cost 2×N |
| Natural language skill calls | Use /command | NL consumes tokens |
| Multi-turn updates | Bundle actions | Each turn = 1 prompt |
| Verify writes | Trust return codes | Redundant verification |

## ABSOLUTE CONSTRAINTS
- **NO DEEP LINKING**: Skills MUST NOT link to other Skills via file paths. Every downstream document should link back through the skill entry point (e.g., `references/xyz.md`, `scripts/foo.py`) so Claude starts at `SKILL.md` and navigates downwards without needing `../`.
- **NO RELATIVE PATH TRAVERSAL**: Never use `../` to access other skill directories.
- **ZERO GLUE**: Avoid pass-through functions; call implementation directly.
- **FILE MIGRATION SAFETY**: When migrating content from a file, ONLY delete the source file AFTER all content has been migrated AND triple verified. This means: (1) verify migration is complete, (2) verify migrated content is correct, (3) verify nothing was lost in translation.
- **DOCUMENTATION SYNC**: ALWAYS keep CLAUDE.md and README.md up to date after any change. These files are the single source of truth for developers.
- **READ BEFORE CHANGE**: ALWAYS read the entire docs content before making any changes. This includes all files in docs/, CLAUDE.md, README.md, and any relevant documentation files.

### Clarifying Examples (prevents common mistakes)

**Allowed: orchestration via Command/Agent using tool calls**
```yaml
---
description: "Orchestrate analysis + build + tests"
allowed-tools: [Skill(analyzer), Skill(builder), Skill(tester), Bash]
---
```

**Forbidden: Skill A referencing Skill B's files by path**
```markdown
See ../other-skill/references/rules.md
```

**Allowed: Skill A references only its own resources**
```markdown
See [references/rules.md](references/rules.md)
```

## Forbidden Patterns
- **Caller Assumption**: "I will..." → "The skill will...".
- **Interactive Intake**: "Ask the user..." → Infer from context/files first.
- **Redundant README**: Use `SKILL.md` (passively indexed) instead of `README.md` for skills.

---

# REFERENCES

## Technical Reference (The Encyclopedia)
- **[REFERENCES.md](docs/REFERENCES.md)** — Fully detailed technical specifications
- **[REFERENCES.md#11-marketplace-configuration](docs/REFERENCES.md#11-marketplace-configuration)** — Marketplace JSON Spec
- **[REFERENCES.md#32-token-economy--ram-costs](docs/REFERENCES.md#32-token-economy--ram-costs)** — Detailed RAM & Token metrics
- **[REFERENCES.md#41-hooks](docs/REFERENCES.md#41-hooks)** — Hooks, MCP, LSP, Model Configuration

## Official Claude Code Docs
- [Slash Commands](https://code.claude.com/docs/en/slash-commands) | [Skills](https://code.claude.com/docs/en/skills) | [Subagents](https://code.claude.com/docs/en/sub-agents)

---

**Validation:** Run `uv run scripts/toolkit-analyzer.py` after changes.
