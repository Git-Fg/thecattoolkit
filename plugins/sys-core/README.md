# sys-core

**Infrastructure & Safety** - The foundation layer for plugin management, security, and toolkit maintenance.

## Purpose

Provides the essential infrastructure for the Cat Toolkit: security auditing, subagent lifecycle management, component scaffolding, and toolkit self-healing.

## Agents

- **security-auditor** - Read-only security vulnerability scanner (secrets, OWASP violations)
- **plugin-expert** - Infrastructure guardian for component creation and standardization

## Skills

- **audit-security** - Secret detection and protected file blocking
- **toolkit-registry** - Component registry and management for skills/commands/agents
- **scaffold-component** - Generate new plugin components from specifications
- **meta-builder** - Build/audit components with live Claude Code docs
- **manage-healing** - Forensic investigation of component failures
- **manage-skills** - Consolidated into toolkit-registry for unified management
- **manage-commands** - Consolidated into toolkit-registry for unified management
- **check-types** - Python type safety validation (pyright, mypy)
- **validate-toolkit** - Comprehensive plugin/marketplace validation

## Hooks

- **SessionStart** - Injects 2026 Universal Agentic Runtime Protocols:
  - Prompt Churn Decision Flow (Inline Skill: 1, Fork: 3+, Agent: 2×N)
  - Behavioral Constraints (Uninterrupted Flow, Trust Return Codes, No Permission Fishing)
  - Autonomous Partner Overlay (No questions mid-execution, Strategic Assumption)
  - Auto-loads persistent context (.cattoolkit/context/scratchpad.md)
  - Auto-loads project roadmap (.cattoolkit/planning/**/ROADMAP.md)
- **PostToolUse** - Logs all tool executions for forensic analysis

## Styles

- **thecattoolkit-persona** - Core identity and behavioral standards
- **shared-standards** - Universal quality principles across all components

## Usage

All security operations run in `plan` mode (read-only). Component management uses the plugin-expert with full toolkit documentation access. Hooks provide automatic logging and protocol injection.
