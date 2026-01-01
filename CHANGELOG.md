# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-01-01

### Major Refactor - XML to Markdown Migration

This release refactors the entire plugin from XML-heavy structure to Markdown-first organization. The goal is to prioritize readability and maintenance while preserving XML only for highly structured elements (complex routing logic in router pattern skills).

### Changed

#### Format Migration (58 files refactored)

**Phase 1: Audit Instructions** (2 files)
- Updated skill-auditor.md - Changed format requirements from "pure XML" to "Markdown-first"
- Updated subagent-auditor.md - Removed XML-only requirement for agent files

**Phase 2: Router Pattern Skills** (4 files)
- Preserved `<intake>` and `<routing>` XML sections (complex routing logic)
- Converted content sections to Markdown headings
- Files: create-plans, create-agent-skills, create-subagents, create-hooks

**Phase 3: Simple Skills** (15 files)
- Full XML to Markdown conversion
- expertise: api-design, architecture-patterns, iphone-apps, macos-apps
- frameworks: problem-analysis, prioritization, strategic-thinking
- patterns: create-meta-prompts, create-slash-commands, debug-like-expert, git-workflow, performance-optimization, project-analysis, prompt-engineering-patterns, testing-strategy

**Phase 4: Commands** (20 files)
- Reduced XML usage, converted structure to Markdown headings
- Files: architect, audit-skill, audit-slash-command, audit-subagent, brainstorm, create-agent-skill, create-hook, create-meta-prompt, create-plan, create-prompt, create-slash-command, create-subagent, debug, heal-skill, mentor, rapid, review, run-plan, run-prompt, whats-next

**Phase 5: Agents** (11 files)
- Minimal changes (already using Markdown headings well)
- Files: brainstormer, code-reviewer, debugger, docs-writer, orchestrator, refactorer, security-auditor, skill-auditor, slash-command-auditor, subagent-auditor, test-architect

### Key Principles

1. **Markdown headings for structure** - Use `#`, `##`, `###` instead of bold text or XML tags
2. **XML reserved for routing logic** - Keep `<intake>` and `<routing>` sections only in router pattern skills
3. **Content-level bold** - Bold for emphasis is appropriate (e.g., `**CRITICAL**`, `**If X:**`)
4. **Progressive disclosure** - SKILL.md as overview (<500 lines), details in references/

### Migration Guide

**Before (XML structure):**
```xml
<objective>
Text here
</objective>

<process>
Step 1
Step 2
</process>
```

**After (Markdown structure):**
```markdown
# Objective

Text here

# Process

Step 1
Step 2
```

### Technical Notes
- Total files modified: 58
- Files deleted: 15 (old consider/ commands moved to .attic)
- Router skills retain XML for `<intake>` and `<routing>` sections
- All audit instructions updated to reflect Markdown-first standards

## [2.2.0] - 2025-01-01

### Major Refactor - Thinking Frameworks

This release consolidates 12 fragmented `consider:*` commands into 3 cohesive skills with a unified brainstormer agent and command, significantly reducing namespace pollution while improving discoverability and integration.

### Added

#### Strategic Thinking Skills (3 new)
- **strategic-thinking** - Long-term perspective and big-picture analysis
  - Frameworks: first-principles, inversion, second-order, swot, 10-10-10
  - Use when making strategic decisions, business planning, or major life choices
- **prioritization** - Focus resources on high-impact activities
  - Frameworks: pareto, one-thing, eisenhower-matrix
  - Use when overwhelmed with tasks, need clarity on what to do first
- **problem-analysis** - Deep understanding and root causes
  - Frameworks: 5-whys, opportunity-cost, occams-razor, via-negativa
  - Use when analyzing problems, making constrained choices, or simplifying complexity

#### Unified Brainstormer (1 new)
- **brainstormer agent** - Strategic thinking and decision specialist (opus model)
  - Auto-selects appropriate frameworks based on context
  - Combines multiple frameworks when beneficial
  - Provides structured, actionable output
- **/brainstorm command** - Unified entry point for all thinking frameworks
  - Auto-detect mode: Agent analyzes context and suggests frameworks
  - Specific framework mode: Apply named framework directly
  - Skill mode: Apply frameworks from strategic-thinking, prioritization, or problem-analysis

### Changed
- **README** - Updated with new strategic thinking section
  - Replaced "Thinking Models" (12 commands) with "Strategic Thinking" (3 skills + 1 command)
  - Added documentation for all 3 skills with frameworks
  - Updated command counts (31 → 20)
  - Updated agent counts (10 → 11, added brainstormer)
  - Updated skill counts (13 → 16, added 3 strategic thinking skills)

### Removed
- **12 consider:* commands - Moved to `.attic/consider/` (preserved but not active)
  - pareto, first-principles, inversion, second-order, 5-whys, occams-razor
  - one-thing, swot, eisenhower-matrix, 10-10-10, opportunity-cost, via-negativa

### Migration Guide
**Before:** `/consider:pareto` or `/consider:first-principles`
**After:**
- `/brainstorm` - Auto-detect best framework
- `/brainstorm pareto` - Apply specific framework
- `/brainstorm strategic` - Use strategic-thinking skill frameworks

### Total Counts
- **Agents**: 10 → 11 (+1 brainstormer)
- **Skills**: 13 → 16 (+3 strategic thinking)
- **Commands**: 31 → 20 (-12 consider, +1 brainstorm)
- **Hooks**: 3 (unchanged)

## [2.1.0] - 2025-01-01

### Refinement Release - Diamond Polish

This release refines the plugin from "raw diamond" to "refined diamond" by improving consistency, ensuring proper agent activation patterns, and optimizing integration between components.

### Changed

#### Agent Descriptions (3 agents)
- **test-architect** - Added "Use PROACTIVELY when..." pattern for proper activation
- **docs-writer** - Added "Use PROACTIVELY when..." pattern and project-analysis skill
- **refactorer** - Added "Use PROACTIVELY when..." pattern (already had architecture-patterns skill)

#### Agent Integration (1 agent)
- **debugger** - Added debug-like-expert skill for systematic debugging methodology

#### Creation Commands (7 commands)
- Added guidance notes to all creation commands explaining when to use each:
  - `/create-plan` - For building projects (hierarchical planning)
  - `/create-meta-prompt` - For Claude→Claude pipelines (staged workflows)
  - `/create-prompt` - For single prompts (simple, one-off)
  - `/create-agent-skill` - For creating new skills
  - `/create-subagent` - For creating specialized agents
  - `/create-slash-command` - For creating commands
  - `/create-hook` - For automation

### Technical Notes
- Verified all agent tool access is appropriate for their roles
- Confirmed knowledge reference skills use markdown (standard pattern for readability)
- Verified all agents use "Use PROACTIVELY when..." pattern for optimal Claude activation

## [2.0.0] - 2025-01-01

### Major Release - claude-workflow Integration

This release integrates the complete claude-workflow plugin, adding operational agents, knowledge domain skills, output mode commands, and automation hooks.

### Added

#### Operational Agents (7 new)
- **orchestrator** - Master coordinator for complex multi-step tasks (uses Opus model)
- **code-reviewer** - Expert code review specialist for quality, security, and performance
- **debugger** - Systematic bug investigation and fixing with 6-phase protocol
- **docs-writer** - Technical documentation specialist
- **security-auditor** - Security vulnerability detection specialist
- **refactorer** - Code structure improvements and technical debt reduction
- **test-architect** - Comprehensive test strategy design

#### Knowledge Domain Skills (6 new)
- **project-analysis** - Understand codebase structure and patterns
- **architecture-patterns** - System design guidance (Clean Architecture, Hexagonal, Event-Driven, CQRS)
- **testing-strategy** - Test approaches (unit, integration, E2E)
- **performance-optimization** - Speed optimization and bottleneck identification
- **git-workflow** - Version control best practices and conventional commits
- **api-design** - REST/GraphQL API patterns and best practices

#### Output Mode Commands (4 new)
- **/architect** - System design mode focusing on architecture before code
- **/rapid** - Fast development mode for shipping quickly and iterating
- **/mentor** - Learning mode that explains the "why"
- **/review** - Code review mode with strict quality standards

#### Automation Hooks (3 new)
- **protect-files.py** - Blocks edits to sensitive files (lock files, .env, .git)
- **security-check.py** - Scans for potential secrets before writes
- **format-on-edit.py** - Auto-formats files on edit
  - Python files use `ruff` (instead of black)
  - JS/TS/JSON/CSS/MD use prettier
  - Go uses gofmt
  - Rust uses rustfmt

#### Specialized Skills (1 new)
- **prompt-engineering-patterns** - Advanced prompt engineering techniques (few-shot learning, chain-of-thought, prompt optimization)

### Changed
- Updated plugin.json description to reflect expanded capabilities
- Added keywords: orchestration, code-review, security, testing, architecture, debugging
- Bumped version from 1.1.0 to 2.0.0

### Total Counts
- **Agents**: 3 → 10 (7 operational + 3 quality assurance)
- **Skills**: 9 → 13 (4 added, including 6 new knowledge domains integrated)
- **Commands**: 27 → 31 (+4 output modes)
- **Hooks**: 0 → 3 (automation system added)

## [1.1.0] - 2025-01-01

### Added
- Enhanced skill-auditor with fallback path resolution
- Improved audit-skill with relative path handling
- Added prompt-engineering-patterns skill

### Changed
- Bumped plugin version to 1.1.0

## [1.0.0] - Initial Release

### Features
- Meta-prompting system with staged prompts
- Todo management with context preservation
- 12 thinking model commands (consider/)
- Creation commands for skills, commands, subagents, hooks, meta-prompts, plans
- Quality assurance auditors for skills, commands, and subagents
- Debug-like-expert skill for systematic debugging
- Prompt engineering patterns skill
- Platform expertise (iPhone apps, macOS apps)
