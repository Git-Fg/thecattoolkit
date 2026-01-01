# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
