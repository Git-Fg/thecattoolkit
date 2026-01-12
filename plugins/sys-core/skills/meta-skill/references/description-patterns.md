# Description Patterns Reference

## Overview

Two patterns supported: **Standard** (default) and **Enhanced** (optional for toolkit infrastructure).

---

## Standard Pattern (Official)

**Alignment:** Claude Code official best practices
**Portability:** ✓ Maximum (works everywhere)
**Complexity:** ✓ Simple (no toolkit-specific syntax)

### Format

```
{CAPABILITY}. Use when {TRIGGERS}.
```

### Anatomy

```
┌──────────────────────────────────────────────────────────────┐
│ "Extracts text from PDF files. Use when processing PDFs."   │
│  └──────┬──────────────────┘     └──────────┬──────────┘    │
│    CAPABILITY (what it does)          TRIGGERS (when)        │
└──────────────────────────────────────────────────────────────┘
```

### Guidelines

- **Capability**: 3rd person, describes functionality
- **Triggers**: Natural user phrases
- **Length**: 50-500 chars recommended
- **Style**: Clear, specific, actionable

### Examples

```yaml
# Utility skill
description: "Validates CSV structure and schema. Use when checking CSV files, validating data, or ensuring format compliance."

# Processing skill
description: "Transforms JSON data between formats. Use when converting JSON, restructuring data, or changing schemas."

# Analysis skill
description: "Analyzes code for security vulnerabilities. Use when reviewing code, checking security, or auditing applications."

# Deployment skill
description: "Deploys applications to production with validation and rollback. Use when deploying apps, managing releases, or updating production."

# API Integration
description: "Integrates with external APIs using REST and GraphQL. Use when connecting to APIs, fetching data, or managing authentication."
```

### When to Use

- ✓ Public-facing skills
- ✓ Marketplace plugins
- ✓ Skills needing maximum portability
- ✓ General-purpose utilities

---

## Enhanced Pattern (Cat Toolkit)

**Alignment:** Cat Toolkit internal conventions
**Portability:** ○ Toolkit-specific (not required elsewhere)
**Complexity:** ○ Moderate (adds modal syntax)

### Format

```
{CAPABILITY}. {MODAL} Use when {TRIGGERS}.
```

### Anatomy

```
┌──────────────────────────────────────────────────────────────────┐
│ "Routes requests. PROACTIVELY Use when orchestrating builds."   │
│  └─────┬──────┘  └────┬────┘      └──────────┬──────────┘      │
│   CAPABILITY    MODAL (priority)        TRIGGERS (when)         │
└──────────────────────────────────────────────────────────────────┘
```

### Modals

| Modal | Priority | Use Case | Example Skills |
|:------|:---------|:---------|:---------------|
| `MUST` | Critical | Non-negotiable standards | Validation, security gates |
| `PROACTIVELY` | High | Auto-orchestration | Routers, builders, coordinators |
| `SHOULD` | Medium | Recommended helpers | Optimizers, analyzers |

### Examples

```yaml
# Critical validation (MUST)
description: "Validates plugin configuration against schema. MUST Use when plugin installed, plugin modified, or validation requested."

# Auto-orchestration (PROACTIVELY)
description: "Routes component creation to specialized builders. PROACTIVELY Use when scaffolding components, creating structures, or orchestrating builds."

# Recommended helper (SHOULD)
description: "Analyzes token usage and suggests optimizations. SHOULD Use when reviewing skills, auditing efficiency, or optimizing context."

# Quality gate (MUST)
description: "Enforces security standards and prevents vulnerable patterns. MUST Use when code commits detected, deployment requested, or security audit triggered."

# Auto-coordinator (PROACTIVELY)
description: "Coordinates multi-skill workflows and manages dependencies. PROACTIVELY Use when complex tasks detected, workflow orchestration needed, or multi-step automation required."
```

### When to Use

- ✓ Internal toolkit infrastructure
- ✓ Orchestration layer
- ✓ Priority signaling needed
- ✓ Auto-invocation required

---

## Pattern Selection

### Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│ Q1: Is this skill part of INTERNAL TOOLKIT infrastructure? │
│                                                             │
│ NO  → USE STANDARD PATTERN                                  │
│ YES → Q2                                                    │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ Q2: Does this skill REQUIRE automatic invocation?          │
│                                                             │
│ NO  → USE STANDARD PATTERN                                  │
│ YES → Q3                                                    │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ Q3: What is the invocation priority?                       │
│                                                             │
│ - Non-negotiable standard → MUST Use when                  │
│ - Auto-orchestration      → PROACTIVELY Use when           │
│ - Recommended but optional → SHOULD Use when               │
└─────────────────────────────────────────────────────────────┘
```

### Decision Matrix

| Context | Audience | Pattern | Example |
|:--------|:---------|:--------|:--------|
| **Public skill** | External users | Standard | `Extracts text. Use when...` |
| **Plugin skill** | Plugin users | Standard | `Validates data. Use when...` |
| **Toolkit infrastructure** | Internal | Enhanced | `Validates plugins. MUST Use when...` |
| **Orchestration layer** | Internal | Enhanced | `Routes requests. PROACTIVELY Use when...` |
| **Optional helper** | Internal | Enhanced | `Analyzes usage. SHOULD Use when...` |

### Quick Reference

| Question | Yes → | No → |
|:---------|:------|:-----|
| Public-facing skill? | **Standard** | Continue |
| Marketplace plugin? | **Standard** | Continue |
| Internal toolkit? | Continue | **Standard** |
| Requires priority signal? | **Enhanced** | **Standard** |

**Default:** Start with **Standard**. Upgrade to Enhanced only if infrastructure requires it.

---

## Migration Guide

### Converting Old Cat Toolkit → Standard

```yaml
# Before (old Cat Toolkit style)
description: "USE when processing PDFs. Extracts text..."

# After (Standard)
description: "Extracts text, images, and metadata from PDFs. Use when processing PDF files, extracting content, or working with documents."
```

### Converting Standard → Enhanced

```yaml
# Before (Standard)
description: "Validates plugin structure. Use when checking plugins."

# After (Enhanced - for internal use)
description: "Validates plugin structure and configuration. MUST Use when plugin installation detected, plugin modified, or validation requested."
```

### Improving Vague → Standard

```yaml
# Before (vague)
description: "Data processing skill"

# After (Standard)
description: "Processes CSV and JSON with validation and transformation. Use when cleaning data, converting formats, or validating structure."
```

---

## Common Mistakes to Avoid

### ❌ Starting with "Use when"

```yaml
# Wrong
description: "Use when processing PDFs. Extracts text..."

# Correct
description: "Extracts text from PDFs. Use when processing documents..."
```

### ❌ Vague triggers

```yaml
# Wrong
description: "Processes data. Use when needed."

# Correct
description: "Processes CSV and JSON data. Use when cleaning data, converting formats, or validating structure."
```

### ❌ Unnecessary modal for public skill

```yaml
# Wrong (modal not needed for public skill)
description: "Validates CSV files. MUST Use when checking data."

# Correct (Standard for public)
description: "Validates CSV structure and schema. Use when checking files or ensuring quality."
```

### ❌ Missing modal for infrastructure

```yaml
# Wrong (infrastructure needs priority signal)
description: "Validates plugins. Use when checking configuration."

# Correct (Enhanced for infrastructure)
description: "Validates plugin configuration. MUST Use when plugin installed or modified."
```

---

## Validation

Descriptions are validated by `scripts/validate-description.py`:

```bash
uv run scripts/validate-description.py ./my-skill/
```

**Validation checks:**
- Length: 50-1024 characters
- Pattern: Must contain "Use when" trigger
- Capability: Must start with capability statement (not "Use when")
- Style: 3rd person, specific triggers

---

## Summary

**Standard Pattern (Default):**
```
{CAPABILITY}. Use when {TRIGGERS}.
```
- For public skills, marketplace plugins, general utilities
- Simple, portable, official standard

**Enhanced Pattern (Optional):**
```
{CAPABILITY}. {MODAL} Use when {TRIGGERS}.
```
- For internal toolkit infrastructure, orchestration
- Adds priority signaling (MUST/PROACTIVELY/SHOULD)
- Use only when infrastructure requires it
