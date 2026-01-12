# Cat Toolkit: Complete Technical Reference

> **📘 Quick Start:** [CLAUDE.md](../CLAUDE.md) - Summary of the Tiered Authority.

---

# 📋 TABLE OF CONTENTS

1. [Tier 1: Engine Rules (Strict Constraints)](#1-tier-1-engine-rules-strict-constraints)
2. [Tier 2: Marketplace Conventions (Guidelines)](#2-tier-2-marketplace-conventions-guidelines)
3. [Tier 3: Engineering Patterns (Best Practices)](#3-tier-3-engineering-patterns-best-practices)
4. [Infrastructure Reference (Hooks, MCP, LSP)](#4-infrastructure-reference-hooks-mcp-lsp)
5. [Development & Troubleshooting](#5-development--troubleshooting)

---

# 1. TIER 1: ENGINE RULES (STRICT CONSTRAINTS)

*Fundamental rules from official Claude Code. Failure results in crashes or non-loading components.*

## 1.1 Marketplace Configuration

**Location:** `.claude-plugin/marketplace.json` at repository root

| Field | Required | Description |
|:------|:---------|:------------|
| `name` | ✓ | Marketplace identifier (kebab-case) |
| `owner` | ✓ | Maintainer |
| `plugins` | ✓ | Array of plugin entries |

### Plugin Entry Fields

| Field | Type | Description |
|:------|:-----|:------------|
| `name` | string | Plugin identifier |
| `source` | string/object | Relative path, GitHub repo, or git URL |
| `strict` | boolean | Require plugin.json (default: true) |
| `description` | string | Brief description |
| `version` | string | Semantic version |
| `author` | object | Author info |
| `category` | string | Organization category |
| `tags` | array | Searchable tags |

### Strict Mode & Source Types

| Mode | Behavior | Use Case |
|:-----|:---------|:---------|
| `strict: true` | Requires plugin.json | Complete plugin manifests |
| `strict: false` | No plugin.json needed | Simple marketplace-defined plugins |

| Source Type | Format | Use When |
|:------------|:-------|:---------|
| Relative Path | `"./plugins/sys-core"` | Same repository |
| GitHub | `{"source": "github", "repo": "user/repo"}` | Separate repositories |
| Git URL | `{"source": "url", "url": "https://..."}` | GitLab, Bitbucket |

## 1.2 Frontmatter Validation

| Primitive | Required Fields | Whitelisted Optional |
|:----------|:----------------|:---------------------|
| **Skill** | `name`, `description` | `allowed-tools`, `context`, `user-invocable`, `disable-model-invocation` |
| **Agent** | `name` | `tools`, `skills` |
| **Command** | `description` | `allowed-tools`, `disable-model-invocation`, `argument-hint` |

### Naming & Identity
- **Skill Name Regex**: `^[a-z][a-z0-9-]{2,49}$` (Lowercase, start with letter, hyphens/numbers allowed).
- **Directory Match**: The `name` field in `SKILL.md` MUST match its containing directory exactly.
- **Description**: 1-1024 chars, single line (newline breaks parsing).

## 1.3 Syntax & Directory Structure

### Directory Structure Reference
**Plugin Distribution:**
```
plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/             # Global Skills
├── commands/           # Global Commands
└── agents/             # Global Agents
```

### Tool Syntax Rules
**Use `Tool(specifier)` with parentheses:**
- ✓ `Bash(git add:*)`, `Bash(npm:*)`
- ✗ `Bash[python, npm]` (Bracket syntax causes tool selection errors)

### Path Standards
- ✓ Unix-style forward slashes (`scripts/helper.py`)
- ✗ Windows-style paths (`scripts\helper.py`)

---

# 2. TIER 2: MARKETPLACE CONVENTIONS (GUIDELINES)

*Conventions specific to The Cat Toolkit for portability and security.*

## 2.1 Forbidden Patterns

| Field | Constraint | Rationale |
|:------|:-----------|:----------|
| `permissionMode` | **NEVER** in frontmatter | Runtime-controlled. Users must retain security sovereignty. |
| `model` | **NEVER** in frontmatter | Runtime-controlled. Prevents breakage on model deprecation. |

## 2.2 Description Patterns

### Unified Strategy: Standard + Enhanced

| Pattern | Format | Use Case |
|:--------|:-------|:---------|
| **Standard** | `{CAPABILITY}. Use when {TRIGGERS}.` | Public/Portable skills, user-facing tools |
| **Enhanced** | `{CAPABILITY}. {MODAL} Use when {TRIGGERS}.` | Internal metrics, orchestration, compliance |

**Enhanced Modals Table:**
| Modal | Use When | Example |
|:------|:---------|:---------|
| **MUST** | Critical internal standards | `"Enforces coding standards. MUST Use when committing code."` |
| **PROACTIVELY** | Primary orchestration | `"Routes requests intelligently. PROACTIVELY Use when handling queries."` |
| **SHOULD** | Recommended practices | `"Validates inputs. SHOULD Use when processing user data."` |

## 2.3 Environment & Tooling

- **Python**: Always use `uv run`/`uvx`. NEVER `python`/`pip`.
- **JS/TS**: Always use `bun run`.
- **Plugin Root**: Use `${CLAUDE_PLUGIN_ROOT}` for all intra-plugin references.
- **Validation**: `uv run scripts/toolkit-analyzer.py` is mandatory after every edit.

---

# 3. TIER 3: ENGINEERING PATTERNS (BEST PRACTICES)

*Architectural principles for peak performance and context window efficiency.*

## 3.1 Component Selection Guide

| Component | Best For | Token Mechanics | Auto-Invokable? |
|:----------|:---------|:----------------|:----------------|
| **Skill** | Knowledge, Frameworks, Protocols | High Retention (loaded text) | ✅ Yes (unless disabled) |
| **Command** | Workflows, Orchestration triggers | **0 Indexing / High Execution** | ❌ No (if disabled) |
| **Agent** | High Volume, Isolation, specific Tools | Isolated Context (fork) | ❌ No (via orchestration only) |

### Token Economy & Resource Costs

| Primitive | Use Case | RAM Cost | Implementation |
|:----------|:---------|:---------|:----------------|
| **Skill (Inline)** | Single capability, domain expertise | 1 | `skills/*/SKILL.md` |
| **Command** | Multi-skill orchestration, user interaction | 0* | `commands/*.md` |
| **Agent (Task)** | Parallel/Background execution | 2×N | `agents/*.md` |
| **Skill (Fork)** | Massive files (>10) | 3 | `context: fork` |

*\*`0*` means "not indexed for model invocation" when `disable-model-invocation: true`. It does NOT mean "free at runtime".*

### 3.1.1 The Three Pillars of Context Cost

1. **Indexing (The Catalog)**:
   - Claude sees the `name` and `description` of all available tools.
   - **Optimization**: Use `disable-model-invocation: true` to shrink this catalog.

2. **Execution (The Injection)**:
   - When you type `/cmd` or Claude triggers a Skill, the **full text** of that file enters the context window.
   - **Optimization**: Keep entry-point files small. Use `scripts/` (only stdout is taxed).

3. **Retention (The Memory)**:
   - Skills stay in context until the task is done. Commands vanish immediately.
   - **Optimization**: Use Commands for one-off actions to keep the context window "clean".

## 3.2 Progressive Disclosure (The 100-Line Rule)

| Content Type | Location | Rationale |
|:-------------|:---------|:----------|
| **Core instructions** (< 100 lines) | `SKILL.md` | Always loaded |
| **Deep theory** (> 100 lines) | `references/` | Loaded on-demand |
| **Examples** (> 3) | `examples/` | Load specific example |
| **Templates** | `assets/` | Copy when instantiating |

## 3.3 Skill Architecture

### Resource Discovery Rules
**Critical:** Claude does NOT automatically open shared resources. Must be **explicitly referenced**.

**Valid Pattern:**
```markdown
## Quick start
Use pdfplumber for basic extraction.
**For form filling:** See [references/forms.md](references/forms.md)
```

**Invalid Pattern:**
```markdown
## Quick start
Use pdfplumber for extraction.
```

### Skill Portability (Shared-Nothing)
1. **Isolation**: A Skill should contain all its own `references/`, `scripts/`, and `assets/`.
2. **Referencing**: Orchestrators load multiple skills; Skills do not hard-link to each other.
3. **Path Traversal**: Any use of `../` is a validation failure.

## 3.4 Orchestration Rules

### ✅ Correct: Orchestration (Sequential)
A Command or Agent acts as the conductor, calling Skills sequentially.
- **Pattern**: `Command` → invokes `Skill(Planner)` → invokes `Skill(Executor)`.
- **Why**: Keeps Skills atomic and "shared-nothing".

**Example:**
```yaml
---
description: "End-to-end workflow"
allowed-tools: [Skill(planner), Skill(designer), Skill(worker), Bash]
---
```

### ❌ Incorrect: Deep Linking (Dependency)
A Skill directly referencing another Skill's file path.
- **Anti-Pattern**: `skills/A/SKILL.md` links to `../B/references/doc.md`.
- **Why**: Breaks portability and context isolation.

**Forbidden:**
```markdown
See ../skills/other-skill/references/spec.md
```

### ✅ Correct: Self-Contained References
A Skill references only its own packaged resources:
```markdown
See [references/spec.md](references/spec.md)
```

### Degrees of Freedom
| Freedom Level | When to Use | Example |
|:--------------|:------------|:--------|
| **High** | Multiple valid approaches | Code review, analysis |
| **Medium** | Preferred pattern exists | Report generation |
| **Low** | Fragile operations | Database migrations, deployments |

## 3.4 Design Patterns

### Pattern A: "Brain + Button" (The Sys-Builder Model)
Use this for complex workflows (Build, Audit, Refactor).
1.  **The Brain (Skill)**: Auto-activable. Contains the *methodology* and *decision tree*.
    *   *Role*: Analyzes the request, determines the plan, tells the user *which* button to push.
2.  **The Button (Command)**: Human-invocable (`disable-model-invocation: true`).
    *   *Role*: Executes the heavy workflow (Batch or Interactive) defined by the Brain.
    *   *Two Modes*:
        *   `run` (Batch): No questions, use defaults, log assumptions.
        *   `run-interactive` (HITL): Ask validation questions at critical gates.

### Pattern B: "Fork & Delegate"
Use this to protect Main Context from massive logs or file reads.
1.  **Command/Skill**: Initiates the task.
2.  **Sub-agent**: Defined in `agents/`.
    *   *Crucial*: Sub-agents do **not** inherit parent Skills automatically.
    *   *Config*: Must explicitly list `skills: ["parent-skill-core"]` in frontmatter.

## 3.5 Progressive Disclosure Mechanics

Understanding how Claude loads Skills is critical for token optimization. It is a filesystem-based architecture.

| Stage | Trigger | Context Cost | Best Use For |
|:------|:--------|:-------------|:-------------|
| **1. Metadata** | Startup | ~100 tokens (Name + Description) | Routing. Claude decides *if* the skill is relevant. |
| **2. Instructions** | Activation | Size of `SKILL.md` | "The Brain". Methodologies and links to resources. |
| **3. Resources** | On-Demand | Size of accessed file | `references/*.md`. Static knowledge loaded *only* if referenced. |
| **4. Execution** | Script Run | **Size of STDOUT only** | `scripts/*.py`. Deterministic tasks. The source code remains on disk (0 tokens). |

## 3.6 Scripting Best Practices

Use the `scripts/` folder to offload cognitive load from the model to deterministic code.

### 1. "Solve, Don't Punt"
- **Bad**: A script that fails silently or returns raw errors, forcing Claude to "guess" the fix.
- **Good**: Handle exceptions (`try/except`) in Python. Print clear, actionable error messages to stdout.
- **Why**: Reduces the "fix-it" loops in conversation.

### 2. Machine-Verifiable Outputs
- **Pattern**: `Plan -> Validate -> Execute`.
- **Implementation**:
    1. Agent generates a JSON plan.
    2. Agent runs `scripts/validate_plan.py` to check inputs/paths.
    3. Only if `stdout == "OK"`, Agent runs `scripts/execute.py`.

### 3. Utility Scripts vs Generated Code
- **Rule**: If a task is repeatable (e.g., "Find all unused variables"), write a `scripts/find_unused.py` utility.
- **Why**: Running a pre-written script is faster, cheaper, and safer than asking Claude to "write a bash command to find unused variables" every time.

## 3.7 Commands & Permissions

### Command Advanced Patterns

**Read-Only Command:**
```yaml
---
description: "Analyze codebase without modifications"
argument-hint: Optional analysis scope
allowed-tools: [Read, Grep, Glob]
---
```

**Interactive Wizard:**
```yaml
---
description: "Interactive project setup wizard"
argument-hint: Optional configuration preset
disable-model-invocation: true
---
```

**Multi-Skill Orchestration:**
```yaml
---
description: "Complete development workflow"
allowed-tools: [Skill(analyzer), Skill(builder), Skill(tester), Bash]
---
```

### 3.4.1 Execution Protocols (Batch vs Interactive)

| Feature | **Batch Mode** (`/run`) | **Interactive Mode** (`/run-interactive`) |
|:---|:---|:---|
| **AskUserQuestion** | ❌ Forbidden (Make assumptions) | ✅ Mandatory (Triage/Clarify) |
| **Routing** | Direct delegation to `Worker` | **Router Command** → Questions → `Skill` |
| **Output** | `ASSUMPTIONS.md` | Validated Plan |

### 3.4.2 Sub-agent Skill Injection
Sub-agents **do not** inherit the Main Agent's skills. You MUST explicitly bind them:
```yaml
---
name: specialized-worker
skills: [core-standards, git-workflow]
---
```

### Permission Modes (Runtime Configuration)

| Mode | Behavior | Security | Use Case |
|:-----|:---------|:---------|:---------|
| `default` | Prompts per tool | High | Uncertain operations |
| `acceptEdits` | Auto-approves file ops | Medium | Trusted refactoring |
| `dontAsk` | Auto-denies prompts | High | CI/CD, automation |
| `plan` | Read-only | High | Exploration |
| `bypassPermissions` | All approved | Very Low | ⚠️ Dangerous |

### Skills vs Agents Security

| Aspect | Skills (`allowed-tools`) | Agents (`tools`) |
|:-------|:-------------------------|:-----------------|
| **Purpose** | Temporary restriction | Persistent allowlist |
| **If omitted** | No restriction | **Inherits ALL tools** (security risk) |
| **Security model** | Least privilege during task | Least privilege by default |

### 3.4.2 Plugin-first packaging (no CLAUDE.md dependency)
If distributing via plugin, treat the plugin as the "container":
- Put global workflow entrypoints in `commands/`.
- Put reusable expertise + references + scripts in `skills/<skill>/`.
- Put specialized long-running contexts in `agents/` and explicitly list `skills:` for each agent.

This avoids reliance on repository-level `CLAUDE.md` while keeping the system fully portable.

---

# 4. INFRASTRUCTURE REFERENCE (HOOKS, MCP, LSP)

## 4.1 Hooks

### Hook Events
| Event | When Fired | Use Case |
|:------|:----------|:---------|
| `SessionStart` | Claude starts/resumes | Setup, validation |
| `SessionEnd` | Session ends | Cleanup, persistence |
| `UserPromptSubmit` | Before processing | Input validation |
| `PreToolUse` | Before tool call | Safety checks |
| `PostToolUse` | After tool completes | Logging, validation |
| `Stop` | Main agent finishes | Cleanup |

### Configuration Example
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety-check.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 4.2 MCP (Model Context Protocol)

### Transport Types & Env Vars
**HTTP (Recommended):**
```json
{
  "mcpServers": {
    "api": {
      "command": "http",
      "url": "https://${HOST}:${PORT}/mcp",
      "headers": { "Authorization": "Bearer ${TOKEN}" }
    }
  }
}
```

**Stdio (Local):**
```json
{
  "mcpServers": {
    "local": {
      "command": "node",
      "args": ["server.js"]
    }
  }
}
```

## 4.3 LSP (Language Server Protocol)

### Common configurations
**TypeScript:**
```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "extensionToLanguage": { ".ts": "typescript", ".tsx": "typescript" }
    }
  }
}
```

**Python:**
```json
{
  "lspServers": {
    "python": {
      "command": "pyright-langserver",
      "args": ["--stdio"]
    }
  }
}
```

## 4.4 Runtime Configuration

### Configuration Scopes
**Precedence:** Managed > Command line > Local > Project > User

| Scope | Location | Affects | Shared |
|:------|:---------|:--------|:-------|
| **Managed** | System directories | All users | Yes |
| **Command line** | CLI arguments | Current session | No |
| **Local** | `.claude/*.local.*` | You (project) | No |
| **Project** | `.claude/settings.json` | All collaborators | Yes |
| **User** | `~/.claude/settings.json` | You (all projects) | No |

### Model Aliases
| Alias | Purpose |
|:------|:--------|
| `sonnet` | Latest Sonnet (4.5) |
| `opus` | Latest Opus (4.5) |
| `haiku` | Fast, efficient |
| `opusplan` | Opus planning, Sonnet execution |

---

# 5. DEVELOPMENT & TROUBLESHOOTING

## 5.1 Development Methodology

### Evaluation-Driven Development (Claude A/B)
```
STEP 1: CLAUDE A (Pattern Extraction)
  • Complete task manually | Document what worked | Extract repeatable pattern

STEP 2: CREATE SKILL
  • Encode pattern in SKILL.md | Add validation scripts | Structure references/

STEP 3: CLAUDE B (Fresh Testing)
  • New session (no context) | Invoke skill | Verify quality matches Claude A
```

## 5.2 Validator Pattern (Self-Healing)
1. **EXECUTE** → Perform task.
2. **VALIDATE** → Run checks (lint, test).
3. **CORRECT** → If error, apply fix.
4. **RE-VALIDATE** → Verify (max 3 iterations).

## 5.3 Troubleshooting Guide

### Commands
| Problem | Fix |
|:--------|:----|
| Missing `argument-hint` | Always include for interactive |
| Scattered questions | Consolidate at beginning |
| Vague orchestration | List skills explicitly |
| Over-restricting tools | Balance security/functionality |
| Command runs unexpectedly | Add `disable-model-invocation: true` (prevents model invocation + removes metadata visibility) |

### Permissions
| Problem | Solution |
|:--------|:---------|
| Tool not available | Check `allowed-tools` or `tools` list |
| Permission mode issues | Verify Runtime config (NOT frontmatter) |
| Over-permissive | Review `tools` list for unnecessary |
| Hook blocking | Check hook exit codes (2 = Block) |

### Infrastructure
| Issue | Resolution |
|:------|:----------|
| Hook not firing | Check matcher, use `${CLAUDE_PLUGIN_ROOT}` |
| Hook timeout | Increase timeout, optimize script |
| MCP no connect | Verify URL, check transport type |
| No LSP diagnostics | Verify server installation |

## 5.4 Validation Scripts & Best Practices

| Script | Purpose |
|:-------|:--------|
| `uv run scripts/toolkit-analyzer.py` | Comprehensive lint suite |
| `claude plugin validate .` | Marketplace validation |

**Summary:**
1. Always use `${CLAUDE_PLUGIN_ROOT}`.
2. Validate before deployment.
3. Test hooks with minimal configs.
4. Explicit tool lists for security.
5. Zero-token retention for heavy workflows.
