---
name: audit-security
description: "MUST USE when verifying security of code changes or auditing file safety. Scans for secrets and prevents modification of protected files (Internal-only passive hook)."
user-invocable: false
allowed-tools: [Read, Grep]
---

# Security Audit Standards

## Capabilities

This skill provides automatic security verification via hooks:

### 1. Secret Detection
**Trigger:** `PreToolUse` (Edit/Write)
**Action:** Scans content for:
- API Keys (OpenAI, Anthropic, AWS)
- Bearer Tokens
- Private Keys
- GitHub Tokens

### 2. File Protection
**Trigger:** `PreToolUse` (Edit/Write)
**Action:** Warns on modification of:
- Lock files (`package-lock.json`, `poetry.lock`)
- Secrets directories (`.env`, `credentials/`)
- Git internals

## Usage

This skill functions **passively** via the runtime hook system. You do not need to invoke it manually.

## Configuration

Patterns are defined in:
- `plugins/verify/hooks/scripts/security-check.py`
- `plugins/verify/hooks/scripts/protect-files.py`
