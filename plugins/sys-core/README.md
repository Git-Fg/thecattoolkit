# sys-core

**Infrastructure & Safety** - The foundation layer for plugin management, security, and toolkit maintenance.

## Purpose

Provides the essential infrastructure for the Cat Toolkit: security auditing, subagent lifecycle management, component scaffolding, and toolkit self-healing.

## Agents

- **security-auditor** - Read-only security vulnerability scanner (secrets, OWASP violations)
- **plugin-expert** - Infrastructure guardian for component creation and standardization

## Skills

- **audit-security** - Secret detection and protected file blocking
- **manage-subagents** - Create/audit/configure subagents for isolated execution
- **scaffold-component** - Generate new plugin components from specifications
- **meta-builder** - Build/audit components with live Claude Code docs
- **manage-healing** - Forensic investigation of component failures
- **manage-skills** - Audit/create/modify plugin skills
- **manage-commands** - Create/audit slash commands
- **check-types** - Python type safety validation (pyright, mypy)
- **validate-toolkit** - Comprehensive plugin/marketplace validation

## Hooks

- **SessionStart** - Injects toolkit protocols into session context
- **PostToolUse** - Logs all tool executions for forensic analysis

## Styles

- **thecattoolkit-persona** - Core identity and behavioral standards
- **shared-standards** - Universal quality principles across all components

## Usage

All security operations run in `plan` mode (read-only). Component management uses the plugin-expert with full toolkit documentation access. Hooks provide automatic logging and protocol injection.
