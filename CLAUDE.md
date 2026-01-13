# CLAUDE.md: The Tiered Authority

You are an **orchestration architect** specializing in the Cat Toolkit marketplace.

**Core expertise:**
- Tiered compliance (Engine Rules vs. Marketplace Conventions)
- Quota-optimized workflows (Context Window 150k-200k)
- Intent-driven programming (Discovery vs. Procedural)

---

# TERMINOLOGY (TOKEN, INDEXING, INVOCATION)

This document uses a few overloaded terms. These definitions are the canonical meaning.

## Token / Context Concepts
- **Indexing cost**: Tokens included at startup to *describe what exists* (e.g., metadata such as `name` + `description`). This affects discovery/selection.
- **Execution cost**: Tokens consumed when a component actually runs (a command prompt is injected; a Skill's `SKILL.md` is read/loaded; scripts produce output).
- **Retention**: Whether something remains present/visible for later selection without re-reading (practically: whether metadata stays in the "available tool catalog").

## Invocation Concepts
- **Manual invocation**: User explicitly runs something via the `/` menu.
- **Model invocation**: Claude triggers a command/skill programmatically via the `Skill(...)` tool.
- **Auto-discovery**: Claude selects a Skill/Command based on metadata keywords in `description` (when allowed and visible).

## Frontmatter Controls (high-impact)
- `disable-model-invocation: true`: Prevents model invocation *and removes the item's metadata from the model’s catalog*, which also reduces unintended auto-selection.
- `user-invocable: false` (Skills only): Hides the Skill from the `/` menu while keeping it usable by the model (unless model invocation is disabled).

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
- ✓ **Run `uv run scripts/toolkit-analyzer.py` after EVERY edit**
- ✓ **If fixable issues detected:** run `uv run scripts/toolkit-analyzer.py --fix`
- ✓ **Pollution Control:** ANY external/temp file (PLAN.md, PROMPTS.md) MUST be in `.cattoolkit/`. NEVER pollute root.
- ✓ **Attic:** Move deprecated code to `.attic/` instead of deleting.
- ✓ **Relative Paths:** Use relative paths from skill root within skills.
- ✓ **Hooks:** Use `$CLAUDE_PROJECT_DIR`/`${CLAUDE_PLUGIN_ROOT}` for hooks.

## 1.4 Local Development Workspace (`.claude/`)
The `.claude/` folder at the repository root is a **local workspace** for plugin/marketplace development:
- Contains local settings, rules, and temporary development files
- **Excluded from validation** by `toolkit-analyzer.py`
- NOT part of the distributed marketplace - kept in `.gitignore`
- Use for: local `settings.json`, `rules/*.md`, scratch files during development

---

# SECTION 1.5: PLATFORM AGNOSTICISM (CRITICAL)

*Claude Code is provider-agnostic. Use this section to understand alternatives to direct Anthropic API access.*

## 1.5.1 Provider Options

Claude Code can operate with different API providers through environment variable configuration:

| Provider | Endpoint | Model Access | Cost Model | Quotas |
|:---------|:---------|:-------------|:----------|:-------|
| **Anthropic Direct** | `api.anthropic.com` | Claude 3.5 Sonnet, Haiku, Opus | Standard API pricing | Per-token billing |
| **Z.AI Routing** | `api.z.ai/api/anthropic` | GLM-4.7, 4.6, 4.5, 4.5-Air | Subscription-based | Prompt-based cycles |

**Alternative Endpoint for Non-Claude Tools:**
```yaml
# For tools like Cline, OpenCode, etc.
BASE_URL: "https://api.z.ai/api/paas/v4"
MODEL: "glm-4.7"
```

### Key Configuration Variables

```yaml
ANTHROPIC_BASE_URL: "https://api.z.ai/api/anthropic"  # or https://api.anthropic.com
ANTHROPIC_AUTH_TOKEN: "your_api_key_here"
API_TIMEOUT_MS: "3000000"  # 50 minutes (Z.AI recommended)
```

## 1.5.2 Z.AI GLM Coding Plan Alternative

**Overview:** Z.AI offers a cost-effective subscription plan providing access to GLM models through Claude Code's interface, effectively routing requests through their platform.

### Pricing & Quotas

| Plan | Price/Month | Prompts per 5hrs | Model Calls per Prompt | MCP Quota (Search/Reader) | Vision Pool |
|:-----|:------------|:-----------------|:----------------------|:-------------------------|:------------|
| **Lite** | ~$3 | ~120 | 15-20 | 100/month | 5-hour cycle |
| **Pro** | ~$15 | ~600 | 15-20 | 1,000/month | 5-hour cycle |
| **Max** | ~$60 | ~2,400 | 15-20 | 4,000/month | 5-hour cycle |

**Cost Efficiency:** Approximately **1% of standard API pricing** with 3× more usage than comparable Anthropic plans. Each prompt allows 15-20 model calls, providing tens of billions of tokens monthly.

**Speed:** Generate **>55 tokens per second** for real-time interaction.

### Model Mapping (Z.AI → Claude Interface)

```yaml
# Default mappings (configurable)
ANTHROPIC_DEFAULT_OPUS_MODEL: "glm-4.7"     # Top-tier reasoning
ANTHROPIC_DEFAULT_SONNET_MODEL: "glm-4.7"  # Balanced performance
ANTHROPIC_DEFAULT_HAIKU_MODEL: "glm-4.5-air" # Fast, efficient
```

### Setup Process (Z.AI)

**Step 1: Subscribe**
- Register at [z.ai](https://z.ai)
- Choose plan (Lite/Pro/Max)
- Generate API key

**Step 2: Configure Claude Code**

```bash
# Method 1: Coding Tool Helper (Recommended)
# Automated setup for all supported tools
npx @z_ai/coding-helper

# Method 2: Automated Script (macOS/Linux only)
curl -O "https://cdn.bigmodel.cn/install/claude_code_zai_env.sh" && \
  bash ./claude_code_zai_env.sh

# Method 3: Manual Configuration
# Edit ~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your_zai_api_key",
    "ANTHROPIC_BASE_URL": "https://api.z.ai/api/anthropic",
    "API_TIMEOUT_MS": "3000000"
  }
}

# Method 4: Environment Variables
export ANTHROPIC_AUTH_TOKEN="your_zai_api_key"
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
```

**Step 2.5: Configure MCP Servers (Optional)**

Add Z.AI's exclusive MCP servers for enhanced capabilities:

```bash
# Vision MCP (Local Installation)
claude mcp add -s user zai-mcp-server \
  --env Z_AI_API_KEY=your_api_key Z_AI_MODE=ZAI \
  -- npx -y "@z_ai/mcp-server"

# Web Search MCP (Remote)
claude mcp add -s user -t http web-search-prime \
  https://api.z.ai/api/mcp/web_search_prime/mcp \
  --header "Authorization: Bearer your_api_key"

# Web Reader MCP (Remote)
claude mcp add -s user -t http web-reader \
  https://api.z.ai/api/mcp/web_reader/mcp \
  --header "Authorization: Bearer your_api_key"

# ZRead MCP for GitHub Q&A (Remote)
claude mcp add -s user -t http zread \
  https://api.z.ai/api/mcp/zread/mcp \
  --header "Authorization: Bearer your_api_key"
```

**Step 3: Verify**
```bash
claude  # Start Claude Code
/status  # Check model status
```

### Exclusive MCP Servers (Z.AI Only)

Z.AI provides **4 exclusive MCP servers** for coding plan subscribers:

#### 1. Vision MCP Server (`@z_ai/mcp-server`)
**Model:** GLM-4.6V | **Installation:** Local npm | **Prerequisites:** Node.js >= v22

**Capabilities:**
- `ui_to_artifact` - Turn UI screenshots into code, prompts, specs, or descriptions
- `extract_text_from_screenshot` - OCR screenshots for code, terminals, docs
- `diagnose_error_screenshot` - Analyze error snapshots and propose fixes
- `understand_technical_diagram` - Interpret architecture, flow, UML, ER diagrams
- `analyze_data_visualization` - Read charts and dashboards for insights
- `ui_diff_check` - Compare UI shots to flag visual or implementation drift
- `image_analysis` - General-purpose image understanding
- `video_analysis` - Inspect videos (local/remote ≤8 MB; MP4/MOV/M4V)

#### 2. Web Search MCP Server (`web-search-prime`)
**Installation:** Remote HTTP service

**Capabilities:**
- `webSearchPrime` - Comprehensive web search with titles, URLs, summaries, site metadata

#### 3. Web Reader MCP Server (`web-reader`)
**Installation:** Remote HTTP service

**Capabilities:**
- `webReader` - Fetch complete webpage content including text, links, and structured data (title, body, metadata)

#### 4. ZRead MCP Server (`zread`)
**Installation:** Remote HTTP service | **Powered by:** zread.ai

**Capabilities:**
- `search_doc` - Search documentation, code, and comments in GitHub repositories
- `get_repo_structure` - Get directory structure and file lists of repositories
- `read_file` - Read complete code content of specified files for deep analysis

**Use Cases:**
- Quick start with open source libraries
- Issue troubleshooting and history research
- Deep source code analysis
- Dependency library research

### Comparison: Direct Anthropic vs Z.AI Routing

| Aspect | Anthropic Direct | Z.AI Routing |
|:-------|:-----------------|:-------------|
| **Models** | Claude 3.5 Sonnet/Haiku/Opus | GLM-4.7/4.6/4.5/4.5-Air |
| **Pricing** | ~$15-75/M (Pro/Max) | ~$3-60/M (Lite/Max) |
| **Quota Model** | Token-based | Prompt-based cycles |
| **Speed** | Standard | >55 tokens/sec |
| **MCP Access** | Standard MCP | +4 Exclusive MCP servers |
| **Reliability** | Standard network | No account bans |
| **Geographic** | US-based | Singapore-based |
| **Data Policy** | Standard | No content storage |
| **Cancellation** | Standard | Must cancel 24hrs before renewal |
| **Supported Tools** | Claude Code only | Claude Code, Cline, OpenCode, Roo Code, Kilo Code, Crush, Goose, Cursor, others |

### Decision Matrix

**Choose Z.AI when:**
- ✓ Cost efficiency is critical
- ✓ High-volume usage expected
- ✓ Need exclusive MCP tools
- ✓ Require guaranteed reliability
- ✓ Prefer subscription model

**Choose Direct Anthropic when:**
- ✓ Need latest Claude models exclusively
- ✓ Existing Anthropic infrastructure
- ✓ Per-token billing preferred
- ✓ US-based data residency required
- ✓ Complex enterprise compliance needs

### Platform Switching

To switch between providers:

```bash
# 1. Update configuration
export ANTHROPIC_BASE_URL="https://api.anthropic.com"  # or Z.AI URL
export ANTHROPIC_AUTH_TOKEN="new_api_key"

# 2. Restart Claude Code
claude

# 3. Verify
/status
```

### Troubleshooting

**Common Issues:**

1. **Configuration Not Taking Effect**
   ```bash
   # Solution: Restart terminal completely
   # Delete ~/.claude/settings.json and regenerate
   ```

2. **Model Mapping Confusion**
   ```bash
   # Remove hardcoded model mappings to use defaults
   # Delete model-specific env vars from settings.json
   # Claude Code will automatically use latest default models
   ```

3. **Quota Exhaustion**
   - **Z.AI:** Wait for 5-hour cycle reset. The system will NOT consume account balance
   - **Anthropic:** Check billing dashboard

4. **Manual Configuration Not Working**
   - Close all Claude Code windows, open new command-line window
   - Verify JSON format in settings.json (use online validator)
   - Check variable names and ensure no missing/extra commas

5. **MCP Server Connection Issues**
   ```bash
   # Vision MCP requires Node.js >= v22
   node -v  # Verify version

   # Clear npx cache for latest version
   npx -y @z_ai/mcp-server@latest

   # Check API key is activated and has sufficient balance
   # Verify Z_AI_MODE=ZAI for Vision MCP
   ```

6. **Invalid API Key Errors**
   - Confirm API key is correctly copied
   - Check if API key is activated
   - Ensure API key has sufficient balance
   - Verify Authorization header format (Bearer token)

7. **Network/Timeout Issues**
   - Check network connection and firewall settings
   - Verify server URL is correct
   - Increase timeout settings if needed
   - Z.AI is Singapore-based (check geographic access)

### Subscription Management

**Cancellation:**
- Must cancel at least 24 hours before renewal to avoid auto-renewal
- Current plan remains valid until expiration after cancellation
- No refunds - payments are non-refundable

**Billing:**
- Auto-renews at end of each billing cycle
- Fees deducted in order: Credits → Cash balance → Payment method
- Small minimum applies when charging credit card (rounded up if needed)

**Upgrade/Downgrade:**
- Changes take effect after current billing cycle ends
- Can also cancel and re-subscribe to desired plan

**Credits Program:**
- Credits earned via "Invite Friends, Get Credits" program
- Credits cannot be withdrawn, transferred, or refunded
- Used to offset purchases on Z.AI platform
- Issued within 24-48 hours after friend's payment confirmed

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

## 3.1 Plugin Architecture

The Cat Toolkit organizes capabilities into domain-specific plugins:

| Plugin | Domain | Focus |
|:-------|:-------|:------|
| **sys-core** | Infrastructure | Validation, scaffolding, hooks, MCP, security |
| **sys-builder** | Engineering | Architecture, planning, execution, testing, TDD |
| **sys-cognition** | Reasoning | Thinking frameworks, prompt engineering, analysis (directly actionable) |
| **sys-agents** | Agent Development | Context engineering, memory systems, orchestration (requires implementation) |
| **sys-research** | Knowledge | Research tools, documentation, codebase analysis |
| **sys-multimodal** | Media | Vision, audio, video processing |
| **sys-edge** | Edge/Mobile | Optimization, offline-first, resource-constrained environments |

### sys-cognition vs sys-agents (Key Distinction)
- **sys-cognition**: Skills that are **directly actionable** for any project (prompt patterns, reasoning frameworks, meta-prompts)
- **sys-agents**: Skills that **require external frameworks or code implementation** (Vector DBs, GraphRAG, multi-agent architectures)

## 3.2 Core Architecture Summary

| Component | Role | Reference Guide |
|:----------|:-----|:----------------|
| **Commands** | Orchestration, User Interaction | [⚡️ Commands](docs/guides/commands.md) |
| **Skills** | Domain Knowledge, Procedures | [🧠 Skills](docs/guides/skills.md) |
| **Agents** | Background Tasks, High Volume | [🤖 Agents](docs/guides/agents.md) |
| **Hooks/MCP** | Infrastructure, Integration | [🔌 Infrastructure](docs/guides/infrastructure.md) |

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

## 3.4 The "Min Core" Pattern (Brain + Button)
Structure capabilities using the **Brain (Skill)** + **Button (Command)** approach.
1.  **Skill**: Contains the methodology (auto-discovered).
2.  **Command**: Invocable trigger. Two modes:
    *   `/plugin:run`: Batch mode (Assumptions).
    *   `/plugin:run-interactive`: Interactive mode (AskUserQuestion).

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

## 3.8 Decision Matrix
| Need | Use |
|:---|:---|
| Single capability | **SKILL** |
| Multi-skill orchestration | **COMMAND** |
| User interaction | **COMMAND** |
| Isolation (>10 files) | **AGENT** |

## 3.9 State Anchoring & Validation-First Architecture

### State Anchoring
**Problem:** Context windows are temporary.

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

**Example:**
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

## 3.12 The Validator Pattern (Self-Healing)
1. **EXECUTE** → Perform task.
2. **VALIDATE** → Run `toolkit-analyzer` or lint/test.
3. **CORRECT** → If error, analyze and fix.
4. **RE-VALIDATE** → Repeat (max 3 iterations).
5. **RETURN** → Only when clean.

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

## 3.14 Skill Archetypes (Legacy - Use Universal Archetypes Above)
### 1. Task-Oriented (Workflows)
- **Purpose:** Execute sequential processes.
- **Trigger:** Gerund verbs (`deploying-app`, `reviewing-code`).
- **Pattern:** Execute → Validate → Report.

### 2. Knowledge-Oriented (Expertise)
- **Purpose:** Provide domain knowledge.
- **Trigger:** Domain nouns (`prompt-engineering`, `security-audit`).
- **Pattern:** Query → Load → Synthesize.

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

---

# SECTION 4: ANTI-PATTERNS & CONSTRAINTS

## Quota Optimization (The "Why")
| ✗ Expensive | ✓ Efficient | Why |
|:------------|:------------|:-----|
| Fork skill for <10 files | Use inline skill | Forking costs 3; inline costs 1 |
| Agent for task in context | Use inline Skill | Agents cost 2×N |
| Natural language skill calls | Use /command | NL consumes tokens |
| Multi-turn updates | Bundle actions | Each turn = 1 prompt |
| Verify writes | Trust return codes | Redundant verification |

## 🚨 ABSOLUTE CONSTRAINTS
- **NO DEEP LINKING**: Skills MUST NOT link to other Skills via file paths. Every downstream document should link back through the skill entry point (e.g., `references/xyz.md`, `scripts/foo.py`) so Claude starts at `SKILL.md` and navigates downwards without needing `../`.
- **NO RELATIVE PATH TRAVERSAL**: Never use `../` to access other skill directories.
- **ZERO GLUE**: Avoid pass-through functions; call implementation directly.

### Clarifying examples (prevents common mistakes)
✅ Allowed: orchestration via Command/Agent using tool calls
```yaml
---
description: "Orchestrate analysis + build + tests"
allowed-tools: [Skill(analyzer), Skill(builder), Skill(tester), Bash]
---
```

❌ Forbidden: Skill A referencing Skill B's files by path
```markdown
See ../other-skill/references/rules.md
```

✅ Allowed: Skill A references only its own resources
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
