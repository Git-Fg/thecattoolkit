# Cat Toolkit: Technical Reference Index

> **📘 Context:** This document contains **Technical Specifications, Tables, and Configuration References**.
> For narrative guides and "How-to", see:
> *   [🏛 Architecture](guides/architecture.md)
> *   [⚡️ Commands](guides/commands.md)
> *   [🧠 Skills](guides/skills.md)
> *   [🤖 Agents](guides/agents.md)
> *   [🔌 Infrastructure](guides/infrastructure.md)

---

# 1. Configuration Specifications

## 1.1 Marketplace Configuration (`marketplace.json`)

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

### Source Types

| Source Type | Format | Use When |
|:------------|:-------|:---------|
| Relative Path | `"./plugins/sys-core"` | Same repository |
| GitHub | `{"source": "github", "repo": "user/repo"}` | Separate repositories |
| Git URL | `{"source": "url", "url": "https://..."}` | GitLab, Bitbucket |

## 1.2 Frontmatter Specs

| Primitive | Required Fields | Whitelisted Optional |
|:----------|:----------------|:---------------------|
| **Skill** | `name`, `description` | `allowed-tools`, `context`, `user-invocable`, `disable-model-invocation` |
| **Agent** | `name` | `tools`, `skills`, `disallowedTools`, `hooks` |
| **Command** | `description` | `allowed-tools`, `disable-model-invocation`, `argument-hint`, `hooks` |

### Validation Rules
- **Skill Name Regex**: `^[a-z][a-z0-9-]{2,49}$`
- **Directory Match**: `name` field MUST match directory name.
- **Description**: 1-1024 chars, 3rd person only.

## 1.3 Directory Structure

```
plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/             # Global Skills
├── commands/           # Global Commands
└── agents/             # Global Agents
```

## 1.4 Syntax Rules

| Rule | Correct Syntax | Incorrect |
|:-----|:---------------|:----------|
| **Tool Specifier** | `Bash(git:*)`, `Skill(name)` | `Bash[git]`, `Bash:git` |
| **Paths** | `scripts/helper.py` (Forward slash) | `scripts\helper.py` |

---

# 2. Standards & Constraints

## 2.1 Forbidden Patterns

| Field | Constraint | Rationale |
|:------|:-----------|:----------|
| `permissionMode` | **NEVER** in frontmatter | Runtime-controlled Security Sovereignty |
| `model` | **NEVER** in frontmatter | User Model Choice |

## 2.2 Description Patterns

| Pattern | Format | Use Case |
|:--------|:-------|:---------|
| **Standard** | `{CAPABILITY}. Use when {TRIGGERS}.` | Public/Portable skills |
| **Enhanced** | `{CAPABILITY}. {MODAL} Use when {TRIGGERS}.` | Internal metrics, orchestration |

### Enhanced Modals

| Modal | Meaning | Example |
|:------|:--------|:---------|
| **MUST** | Critical Standard | `"MUST Use when committing code."` |
| **PROACTIVELY** | Primary Orchestration | `"PROACTIVELY Use when handling queries."` |
| **SHOULD** | Recommendation | `"SHOULD Use when processing user data."` |

---

# 3. Component & Resource Metrics

## 3.1 Component Selection

| Component | best For | Token Retention | Auto-Invokable? |
|:----------|:---------|:----------------|:----------------|
| **Skill** | Knowledge, Protocols | High (Text loaded) | GOOD Yes |
| **Command** | Orchestration | Zero (Indexing only) | BAD No |
| **Agent** | High Volume | Isolated Context | BAD No |

## 3.2 Token Economy

| Primitive | Prominence | RAM Cost | Implementation |
|:----------|:----------|:---------|:---------------|
| **Skill (Inline)** | ⭐⭐⭐ | 1× | `skills/*/SKILL.md` |
| **Skill (Fork)** | ⭐⭐ | 3× | `context: fork` |
| **Agent** | ⭐ | 2×N | `agents/*.md` |
| **Command** | WARNING DEPRECATED | 0* | `commands/*.md` |

*\*0 = Not indexed for model invocation usage (use only for bash/env injection)*

### Cost-Optimized Patterns (2026)

**Fork (3×) vs Agent (2×N) Decision Matrix:**

| Scenario | Recommendation | Cost Comparison |
|:---------|:---------------|:----------------|
| **Simple isolation** | Fork Skill | 3× vs 2×N (N=1+: Fork wins) |
| **Heavy processing** (>10 files) | Fork Skill | 3× vs 2×N (N=2+: Fork wins) |
| **Permission scoping only** | Agent with explicit tools | 2×N (necessary evil) |
| **Complex orchestration** | Orchestrator Skill (fork) | 3× vs 2×N×M (fork wins) |

**Key Insight:**
- Fork costs **3×** regardless of task complexity
- Agent costs **2×N** where N = number of invocations
- For single-call agents: **Fork (3×) < Agent (2×)**
- For multi-call agents: **Fork wins even harder**

**2026 Rule of Thumb:**
> Use Fork for isolation. Use Agents ONLY for explicit tool/permission scoping that cannot be achieved with `allowed-tools` in Skills.

**Token Budget Impact (5-Hour Rule):**
- Session budget: ~200,000 tokens
- Spawning agent: ~20,000-25,000 tokens (10-12% overhead)
- Forking skill: ~15,000 tokens (7.5% overhead)
- Inline skill: ~5,000 tokens (2.5% overhead)

## 3.3 Progressive Disclosure Rules

| Content Type | Location | Limit/Rule |
|:-------------|:---------|:-----------|
| **Instructions** | `SKILL.md` | < 100 lines |
| **Details** | `references/*.md` | Loaded on-demand |
| **Examples** | `examples/` | Specific files |
| **Logic** | `scripts/*.py` | JSON-over-Stdout |

---

# 4. Infrastructure Specifications

## 4.1 Hooks

### Hook Events

| Event | Trigger |
|:------|:--------|
| `SessionStart` | Claude starts/resumes |
| `SessionEnd` | Session ends |
| `UserPromptSubmit` | Before processing |
| `PreToolUse` | Before tool call |
| `PostToolUse` | After tool completes |
| `PostToolUseFailure` | After failure |
| `PermissionRequest` | Dialog shown |
| `SubagentStart`/`Stop` | Subagent lifecycle |
| `Stop` | Main agent finishes |

### Hook Types

| Type | Description |
|:-----|:------------|
| **command** | Execute shell script |
| **prompt** | Evaluate LLM prompt |
| **agent** | Run verification agent |

## 4.2 MCP Configuration

**HTTP Transport (Recommended)**:
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

## 4.3 LSP Configuration

**TypeScript**:
```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "extensionToLanguage": { ".ts": "typescript" }
    }
  }
}
```

## 4.4 Runtime Configuration Scopes

| Scope | Location | Shared? |
|:------|:---------|:--------|
| **Managed** | System directories | Yes |
| **Line** | CLI arguments | No |
| **Local** | `.claude/*.local.*` | No |
| **Project** | `.claude/settings.json` | Yes |
| **User** | `~/.claude/settings.json` | No |
| **Plugin** | `plugins/*/Settings` | Yes |

## 4.5 Model Aliases

| Alias | Target |
|:------|:-------|
| `sonnet` | Latest Sonnet (4.5) |
| `opus` | Latest Opus (4.5) |
| `haiku` | Fast, efficient |
| `opusplan` | Opus planning, Sonnet execution |

---

# 5. Troubleshooting Reference

## 5.1 Common Issues

| Component | Issue | Fix |
|:----------|:------|:----|
| **Command** | Runs unexpectedly | Add `disable-model-invocation: true` |
| **Permissions** | Tool not available | Check `allowed-tools` |
| **Permissions** | Hook blocking | Check hook exit codes |
| **Infra** | Hook not firing | Check matcher, use `${CLAUDE_PLUGIN_ROOT}` |
| **Infra** | MCP no connect | Verify URL/Headers |

## 5.2 Validation Scripts

| Script | Usage |
|:-------|:------|
| `toolkit` | `uv run scripts/toolkit.py` |
| `marketplace-validate` | `claude plugin validate .` |
