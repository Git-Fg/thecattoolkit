# THE CAT TOOLKIT

**Version:** 2.0.1 | **License:** MIT | **Author:** Git-Fg

A comprehensive collection of AI agent resources (primarily for Claude Code,
adaptable to other AI assistants) built for real workflows.

/// A PERSONAL MERGE & REFINEMENT FROM <https://github.com/glittercowboy/taches-cc-resources>
and <https://github.com/CloudAI-X/claude-workflow> ///

## Quick Start

### Installation

```bash
# Add the marketplace
claude plugin marketplace add Git-Fg/thecattoolkit

# Install the plugin
claude plugin install thecattoolkit
```

### First Steps

Try these commands to get started:

```bash
# Main toolkit router - build, audit, or heal any resource
/thecattoolkit:toolkit Create a new skill for database validation

# Strategic decision making
/thecattoolkit:brainstorm Should I refactor this module now?

# Code review
> Use the code-reviewer agent to check my recent changes

# System architecture
> Use the architect agent to design a user authentication system

# Run a plan
/thecattoolkit:run-plan path/to/PLAN.md
```

## Table of Contents

- [Philosophy](#philosophy)
- [What's Inside](#whats-inside)
- [Installation](#installation)
- [Quick Examples](#quick-examples)
- [Commands](#commands)
- [Agents](#agents)
- [Skills](#skills)
- [Hooks](#hooks)
- [Troubleshooting](#troubleshooting)

## Philosophy

When you use an AI agent, it's your responsibility to assume everything is possible.

I built these tools using that mindset.

Dream big. Happy building.

— TÂCHES

## What's Inside

**[Commands](#commands)** (7 total) - Essential slash commands with central router

- **Central Router**: Single entry point for building, auditing, and healing resources
- **Strategic Thinking**: Unified thinking frameworks with 12 thinking patterns
- **Deep Analysis**: Systematic debugging methodology with evidence and hypothesis testing
- **Planning & Execution**: Hierarchical project planning and execution

**[Skills](#skills)** (16 total) - Autonomous workflows that research, generate, and self-heal

- **Workflow Creation**: Create plans, meta-prompts, slash commands, subagents, hooks
- **Unified Thinking**: Single thinking-frameworks skill with Router Pattern
- **Knowledge Domains**: Project analysis, architecture patterns, testing, performance, git workflow, API design
- **Specialized**: Debug like expert, prompt engineering patterns

**[Agents](#agents)** (16 total) - Specialized subagents for various workflows

- **Operational**: Orchestrator, code-reviewer, debugger, docs-writer, security-auditor, refactorer, test-architect, brainstormer
- **Output Modes**: Architect, Mentor, Rapid Developer, QA Reviewer
- **Quality Assurance**: skill-auditor, slash-command-auditor, subagent-auditor

**[Hooks](#hooks)** (4 total) - Automation triggers (Claude Code-specific)

- **File Protection**: Warn about edits to sensitive files (lock files, .env, .git)
- **Security Check**: Warn about potential secrets before writes

- **Type-Check**: Type-check Python files when pyproject.toml is configured (pyrefly/mypy)

## Installation Options

### Option 1: Plugin Install (Recommended for Claude Code)

```bash
# Add the marketplace
claude plugin marketplace add Git-Fg/thecattoolkit

# Install the plugin
claude plugin install thecattoolkit
```

Start a new Claude Code session to use the commands and skills.

### Option 2: Manual Install

```bash
# Clone the repo
git clone https://github.com/Git-Fg/thecattoolkit.git
cd thecattoolkit

# Install commands
cp -r commands/* ~/.claude/commands/

# Install skills
cp -r skills/* ~/.claude/skills/
```

Commands install globally to `~/.claude/commands/`. Skills install to `~/.claude/skills/`. Project-specific data (prompts, todos) lives in each project's working directory.

## Quick Examples

### Code Review Workflow

```
> Use the code-reviewer agent to review my changes
```

The code-reviewer will:

1. Run `git diff` to see changes
2. Analyze modified files for quality, security, performance
3. Provide findings with severity ratings (Critical, Warning, Suggestion, Positive)
4. Include specific fixes with file:line references

### Strategic Decision Making

```
/thecattoolkit:brainstorm Should we migrate to microservices?
```

The brainstorm command applies strategic thinking frameworks:

- **Auto-detect**: Chooses appropriate frameworks automatically
- **Specific framework**: `/thecattoolkit:brainstorm pareto`
- **Skill-level**: `/thecattoolkit:brainstorm strategic`

### Creating a New Skill

```
/thecattoolkit:toolkit Create a skill for React component testing
```

This will:

1. Route to the create-agent-skills skill via central toolkit
2. Guide through skill structure (simple vs router pattern)
3. Help with YAML frontmatter and progressive disclosure
4. Offer to create directory structure and files

### Auditing Components

```
# Use the central toolkit router for all audits
/thecattoolkit:toolkit Audit my skill
```

The toolkit router guides you through:

- Selecting the appropriate auditor (skill, command, or subagent)
- Providing overall assessment
- Identifying critical issues (must-fix)
- Making recommendations (should-fix)
- Highlighting strengths (what works well)
- Giving context-specific guidance

### Platform-Specific Development

```
> Build a native macOS menu bar app for monitoring system resources
```

The macos-apps skill provides:

- CLI-only development (no Xcode required)
- "Prove, don't promise" methodology
- Verification with xcodebuild
- Focus on outcomes, not code changes

## Commands

### Central Toolkit Router

The main entry point for building, auditing, and healing resources. Use this instead of individual wrapper commands.

- [`/toolkit`](./commands/toolkit.md) - Main router for create, audit, and heal operations

**Examples:**

- `/toolkit Create a skill for database validation` → Routes to create-agent-skills
- `/toolkit Audit my command` → Routes to appropriate auditor
- `/toolkit Heal broken skill references` → Routes to heal-skill
- `/toolkit Create a slash command for deployments` → Routes to create-slash-commands

### Strategic Thinking

Unified mental models framework for decision-making, prioritization, and problem analysis.

- [`/brainstorm`](./commands/brainstorm.md) - Apply strategic thinking frameworks (auto-detect or specify)

**12 Frameworks in Unified Skill:**

**Strategic Thinking** (5 frameworks) - Long-term perspective and big-picture analysis:

- first-principles - Break down to fundamentals and rebuild
- inversion - Solve backwards (what guarantees failure?)
- second-order - Think through consequences of consequences
- swot - Map strengths, weaknesses, opportunities, threats
- 10-10-10 - Evaluate across time horizons

**Prioritization** (3 frameworks) - Focus resources on high-impact activities:

- pareto - Apply 80/20 rule to focus on what matters
- one-thing - Identify highest-leverage action
- eisenhower-matrix - Prioritize by urgent/important

**Problem Analysis** (4 frameworks) - Deep understanding and root causes:

- 5-whys - Drill to root cause
- opportunity-cost - Analyze what you give up
- occams-razor - Find simplest explanation
- via-negativa - Improve by removing

**Usage:**

- `/brainstorm` - Auto-detect best framework for your situation
- `/brainstorm pareto` - Apply specific framework
- `/brainstorm strategic` - Use strategic-thinking frameworks

### Deep Analysis

Systematic debugging with methodical investigation.

- [`/debug`](./commands/debug.md) - Apply expert debugging methodology to investigate issues

### Planning & Execution

Hierarchical project planning and execution workflows.

- [`/run-plan`](./commands/run-plan.md) - Execute generated plans (PLAN.md) with intelligent segmentation
- [`/run-prompt`](./commands/run-prompt.md) - Execute saved prompts in sub-agent contexts

### Self-Improvement

- [`/uprules`](./commands/uprules.md) - Audit and update AI rule files to synchronize with code changes

## Agents

Specialized subagents for various workflows.

### Operational Agents

Active agents that perform specific tasks during development.

- [`orchestrator`](./agents/orchestrator.md) - Master coordinator for complex multi-step tasks with planning capabilities
- [`code-reviewer`](./agents/code-reviewer.md) - Expert code review specialist for quality, security, and performance
- [`debugger`](./agents/debugger.md) - Systematic bug investigation and fixing with 6-phase protocol
- [`docs-writer`](./agents/docs-writer.md) - Technical documentation specialist
- [`security-auditor`](./agents/security-auditor.md) - Security vulnerability detection specialist
- [`refactorer`](./agents/refactorer.md) - Code structure improvements and technical debt reduction
- [`test-architect`](./agents/test-architect.md) - Comprehensive test strategy design
- [`brainstormer`](./agents/brainstormer.md) - Creative ideation and thinking frameworks specialist

### Output Mode Agents

Behavior modes for different workflows.

- [`architect`](./agents/architect.md) - System design mode - focuses on architecture before code (read-only tools)
- [`mentor`](./agents/mentor.md) - Learning mode - explains the "why" with educational approach (read-only tools)
- [`rapid-developer`](./agents/rapid-developer.md) - Fast development mode - ship quickly, iterate (full tools)
- [`qa-reviewer`](./agents/qa-reviewer.md) - Code review mode - strict quality standards with testing (read + test execution)

### Quality Assurance Agents

Specialized auditors for validation and quality.

- [`skill-auditor`](./agents/skill-auditor.md) - Expert skill auditor for best practices compliance
- [`slash-command-auditor`](./agents/slash-command-auditor.md) - Expert slash command auditor
- [`subagent-auditor`](./agents/subagent-auditor.md) - Expert subagent configuration auditor

## Skills

### [Create Plans](./skills/create-plans/)

Hierarchical project planning optimized for solo developer + Claude. Create executable plans that Claude runs, not enterprise documentation that sits unused.

**PLAN.md IS the prompt** - not documentation that gets transformed later. Brief → Roadmap → Research (if needed) → PLAN.md → Execute → SUMMARY.md.

**Two planning modes:** Lite Mode for simple tasks (single PLAN.md), Standard Mode for complex projects (hierarchical structure with phases).

**Quality controls:** Research includes verification checklists, blind spots review, critical claims audits, and streaming writes to prevent gaps and token limit failures.

**Context management:** Auto-handoff at 10% tokens remaining. Git versioning commits outcomes, not process.

**Commands:** `/run-plan <path>` (execute PLAN.md with intelligent segmentation via orchestrator agent)

See [create-plans README](./skills/create-plans/README.md) for full documentation.

### [Create Agent Skills](./skills/create-agent-skills/)

Build skills by describing what you want. Asks clarifying questions, researches APIs if needed, and generates properly structured skill files.

**Two types of skills:**

1. **Task-execution skills** - Regular skills that perform specific operations
2. **Domain expertise skills** - Exhaustive knowledge bases (5k-10k+ lines) that live in `~/.claude/skills/expertise/` and provide framework-specific context to other skills like [create-plans](#create-plans)

**Context-aware:** Detects if you're in a skill directory and presents relevant options. Progressive disclosure guides you through complex choices.

When things don't work perfectly, `/heal-skill` analyzes what went wrong and updates the skill based on what actually worked.

Commands: `/create-agent-skill`, `/heal-skill`, `/audit-skill`

### [Create Meta-Prompts](./skills/create-meta-prompts/)

The skill-based evolution of the meta-prompting system. Builds prompts with structured outputs (research.md, plan.md) that subsequent prompts can parse. Adds automatic dependency detection to chain research → plan → implement workflows.

**Note:** For end-to-end project building, consider [create-plans](#create-plans) - it's the more structured evolution of this approach with full lifecycle management (brief → roadmap → execution → handoffs). Use create-meta-prompts for abstract workflows and Claude→Claude pipelines. Use create-plans for actually building projects.

Commands: `/create-meta-prompt`

### [Create Slash Commands](./skills/create-slash-commands/)

Build commands that expand into full prompts when invoked. Describe the command you want, get proper YAML configuration with arguments, tool restrictions, and dynamic context loading.

Commands: `/create-slash-command`, `/audit-slash-command`

### [Create Subagents](./skills/create-subagents/)

Build specialized Claude instances that run in isolated contexts. Describe the agent's purpose, get optimized system prompts with the right tool access and orchestration patterns.

Commands: `/create-subagent`, `/audit-subagent`

### [Create Hooks](./skills/create-hooks/)

Build event-driven automation that triggers on tool calls, session events, or prompt submissions. Describe what you want to automate, get working hook configurations.

Commands: `/create-hook`

---

## Strategic Thinking Skills

Mental models and frameworks for decision-making, prioritization, and problem analysis.

### [Thinking Frameworks](./skills/thinking-frameworks/)

Unified mental models framework with Router Pattern for decision-making, prioritization, and problem analysis.

**12 Frameworks across 3 categories:**

**Strategic Thinking** (5 frameworks) - Long-term perspective and big-picture analysis:

- first-principles - Break down to fundamentals and rebuild
- inversion - Solve backwards (what guarantees failure?)
- second-order - Think through consequences of consequences
- swot - Map strengths, weaknesses, opportunities, threats
- 10-10-10 - Evaluate across time horizons

**Prioritization** (3 frameworks) - Focus resources on high-impact activities:

- pareto - Apply 80/20 rule to identify vital few
- one-thing - Find highest-leverage domino action
- eisenhower-matrix - Categorize by urgent/important

**Problem Analysis** (4 frameworks) - Deep understanding and root causes:

- 5-whys - Drill to root cause by asking why repeatedly
- opportunity-cost - Analyze what you give up by choosing
- occams-razor - Find simplest explanation that fits all facts
- via-negativa - Improve by removing rather than adding

**Router Pattern:** Auto-detects best framework or routes to specific categories based on context.

Agent integration: Brainstormer agent (unified access to all frameworks)

---

## Specialized Skills

### [Debug Like Expert](./skills/debug-like-expert/)

Deep analysis debugging mode for complex issues. Activates methodical investigation protocol with evidence gathering, hypothesis testing, and rigorous verification. Use when standard troubleshooting fails or when issues require systematic root cause analysis.

Commands: `/debug`

### [Prompt Engineering Patterns](./skills/prompt-engineering-patterns/)

Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability in production. Covers few-shot learning, chain-of-thought prompting, prompt optimization, template systems, and system prompt design.

---

## Knowledge Domain Skills

Specialized skills for specific technical domains and best practices.

### [Project Analysis](./skills/project-analysis/)

Understand any codebase structure and patterns. Essential for onboarding to new projects or analyzing unfamiliar codebases.

### [Architecture Patterns](./skills/architecture-patterns/)

System design guidance with patterns like Layered Architecture, Clean Architecture, Hexagonal Architecture, Event-Driven Architecture, and CQRS. Includes trade-off analysis templates.

### [Testing Strategy](./skills/testing-strategy/)

Design comprehensive test approaches covering unit tests, integration tests, and E2E testing.

### [Performance Optimization](./skills/performance-optimization/)

Speed up applications and identify bottlenecks with systematic performance analysis techniques.

### [Git Workflow](./skills/git-workflow/)

Version control best practices and conventional commits for professional development workflows.

### [API Design](./skills/api-design/)

REST and GraphQL API patterns, best practices, and design principles.

---

## Hooks

### [Automation Hooks](./hooks/)

Event-driven automation that triggers during Claude Code operations. All hooks use **permissive mode** - they warn but never block edits.

**Security Features:**

- Path traversal protection (detects `..`, `%2e%2e` encoded attempts)
- Input validation on all file paths
- Proper error logging for debugging

- **PreToolUse (Edit/Write)**: File protection and security checks (warn only, never block)
  - `protect-files.py` - Warns about edits to lock files, .env, .git, credentials
  - `security-check.py` - Warns about potential secrets (API keys, passwords, tokens)
- **PostToolUse (Edit/Write)**: Auto-formatting and type-checking

  - `type-check-on-edit.py` - Type-checks Python files when pyproject.toml is configured (uv run pyrefly/mypy)

**Hooks use uv with python3 fallback** - Automatically prefers `uv run` for formatters/type-checkers if available.

**Code Quality:**

- Modern type annotations (`list[str]` vs `List[str]`)
- Comprehensive error handling with `logging` module
- All scripts follow official Claude Code hooks documentation best practices

**See [docs/hooks-best-practices.md](./docs/hooks-best-practices.md) for detailed documentation.**

---

## Recommended Workflow

**For building projects:** Use the central `/toolkit` router to create plans, or invoke the [create-plans](#create-plans) skill directly. After planning, use `/run-plan <path-to-PLAN.md>` to execute phases with intelligent segmentation via the orchestrator agent. This provides hierarchical planning (BRIEF.md → ROADMAP.md → phases/PLAN.md), two planning modes (Lite and Standard), context management with handoffs, and git versioning.

**For creating resources:** Use `/toolkit` as the main entry point for all create, audit, and heal operations. The router guides you to the appropriate skill based on your needs.

**Other tools:** The [create-meta-prompts](#create-meta-prompts-1) skill and `/run-prompt` command are available for custom Claude→Claude pipelines that don't fit the project planning structure.

---

## Troubleshooting

### Plugin Not Loading

**Symptom:** Commands don't appear after installation

**Solutions:**

1. Verify plugin.json exists and is valid:

   ```bash
   cat .claude-plugin/plugin.json | python3 -m json.tool
   ```

2. Try loading with full path:

   ```bash
   claude --plugin-dir /full/path/to/thecattoolkit
   ```

3. Check Claude Code version (requires 1.0.33+):

   ```bash
   claude --version
   ```

### Commands Not Appearing

**Symptom:** `/help` doesn't show thecattoolkit commands

**Solutions:**

1. Verify command files exist:

   ```bash
   ls commands/*.md
   ```

2. Check YAML frontmatter in commands:

   ```bash
   head -5 commands/your-command.md
   ```

3. Restart Claude Code after adding commands

### Skills Not Triggering

**Symptom:** Skills don't activate automatically

**Solutions:**

1. Check SKILL.md exists:

   ```bash
   ls skills/your-skill/SKILL.md
   ```

2. Verify description includes trigger keywords:

   ```bash
   head -10 skills/your-skill/SKILL.md
   ```

3. Use explicit invocation:

   ```
   > Use the your-skill skill to...
   ```

### Hook Scripts Failing

**Symptom:** Errors on file edits or hooks not running

**Solutions:**

1. Verify Python is available:

   ```bash
   which python3
   ```

2. Test script manually:

   ```bash
   python3 hooks/scripts/protect-files.py < /dev/null
   ```

3. Check CLAUDE_PLUGIN_ROOT variable:

   ```bash
   echo $CLAUDE_PLUGIN_ROOT
   ```

4. Review hook configuration:

   ```bash
   cat hooks/hooks.json | python3 -m json.tool
   ```

### Agent Not Found

**Symptom:** "Agent not found" error when invoking

**Solutions:**

1. Check agent file exists:

   ```bash
   ls agents/your-agent.md
   ```

2. Verify agent name in YAML frontmatter:

   ```bash
   head -5 agents/your-agent.md
   ```

3. Use exact name from frontmatter (not filename)

### Mental Model Frameworks

**Symptom:** Not sure which framework to use in `/brainstorm`

**Guidance:**

| Situation | Use Framework |
|----------|--------------|
| Challenging assumptions | first-principles |
| Identifying risks | inversion |
| Understanding ripple effects | second-order |
| Strategic positioning | swot |
| Short-term vs long-term | 10-10-10 |
| Too many tasks | pareto, one-thing |
| Prioritizing by urgency | eisenhower-matrix |
| Finding root cause | 5-whys |
| Trade-off analysis | opportunity-cost |
| Simplifying complexity | occams-razor |
| Removing bloat | via-negativa |

---

## Complete Component Reference

### All Skills (16)

| Skill | Purpose | Type | Location |
|-------|---------|------|----------|
| create-agent-skills | Guide for creating AI agent skills | Creation | skills/create-agent-skills/ |
| create-hooks | Guide for creating automation hooks | Creation | skills/create-hooks/ |
| create-meta-prompts | AI-to-AI pipeline prompts | Creation | skills/create-meta-prompts/ |
| create-plans | Hierarchical project planning | Creation | skills/create-plans/ |
| create-slash-commands | Command creation guide | Creation | skills/create-slash-commands/ |
| create-subagents | Agent creation guide | Creation | skills/create-subagents/ |
| prompt-engineering-patterns | Effective prompts for AI-to-AI | Creation | skills/prompt-engineering-patterns/ |
| debug-like-expert | Deep debugging methodology | Specialized | skills/debug-like-expert/ |
| thinking-frameworks | 12 frameworks unified via Router Pattern | Strategic | skills/thinking-frameworks/ |
| api-design | REST/GraphQL patterns | Domain | skills/api-design/ |
| architecture-patterns | Software architecture | Domain | skills/architecture-patterns/ |
| git-workflow | Git optimization | Domain | skills/git-workflow/ |
| performance-optimization | Code performance | Domain | skills/performance-optimization/ |
| project-analysis | Project structure | Domain | skills/project-analysis/ |
| testing-strategy | Testing methodologies | Domain | skills/testing-strategy/ |

### All Agents (16)

| Agent | Purpose | Tools | Skills |
|-------|---------|-------|--------|
| architect | System design and architecture planning | Read, Grep, Glob | - |
| brainstormer | Creative ideation and thinking frameworks | - | thinking-frameworks |
| code-reviewer | Code quality and security review | Read, Grep, Glob, Bash, SlashCommand | git-workflow, testing-strategy |
| debugger | Root cause analysis | Read, Edit, Bash, Grep, Glob, Write, SlashCommand | debug-like-expert, performance-optimization, prompt-engineering-patterns |
| docs-writer | Technical documentation | - | - |
| mentor | Educational guidance and explanations | Read, Grep, Glob | - |
| orchestrator | Multi-agent coordination and planning | Task, SlashCommand, TodoWrite, etc. | project-analysis, architecture-patterns, prompt-engineering-patterns, thinking-frameworks, create-plans |
| qa-reviewer | Quality assurance and testing | Read, Grep, Glob, Bash | - |
| rapid-developer | Fast-paced development | Read, Write, Edit, Bash, Grep, Glob | - |
| refactorer | Code refactoring | - | - |
| security-auditor | Security assessment | - | - |
| skill-auditor | Skill compliance audit | Read, Grep, Glob, SlashCommand | create-agent-skills |
| slash-command-auditor | Command configuration audit | Read, Grep, Glob, SlashCommand | create-slash-commands |
| subagent-auditor | Agent prompt quality audit | Read, Grep, Glob, SlashCommand | create-subagents |
| test-architect | Testing strategy specialist | - | - |

### All Commands (7)

| Command | Purpose | Type |
|---------|---------|------|
| /thecattoolkit:brainstorm | Strategic thinking frameworks | Strategic |
| /thecattoolkit:debug | Deep debugging methodology | Deep Analysis |
| /thecattoolkit:run-plan | Execute generated plans | Planning |
| /thecattoolkit:run-prompt | Execute saved prompts | Meta-Prompting |
| /thecattoolkit:toolkit | Central router for create, audit, heal | Router |
| /thecattoolkit:uprules | Audit and update AI rule files | Self-Improvement |

### All Hooks (4)

| Hook | Trigger | Script | Purpose |
|------|---------|--------|---------|
| PreToolUse | Edit, Write | protect-files.py | Warn about edits to sensitive files |
| PreToolUse | Edit, Write | security-check.py | Warn about potential secrets |

| PostToolUse | Edit, Write | type-check-on-edit.py | Type-check Python (config-aware) |

---

More resources coming soon.

---

**Community Ports:** [OpenCode](https://github.com/stephenschoettler/taches-oc-prompts)

**Support:**

- Issues: <https://github.com/Git-Fg/thecattoolkit/issues>
- Email: <felix@gitfg.dev>

—TÂCHES
