# Structural Patterns

## Hybrid Semantic Structure

The **Hybrid Semantic Structure** combines XML and Markdown to maximize clarity while minimizing token overhead. The core principle: **XML for Logic Containers, Markdown for Content**.

## The Container Principle

Use XML tags to create semantic containers that help the model understand structure. Limit to **3-5 tags maximum** - never nest XML tags inside each other (avoids "XML soup").

### When to Use Each Container

#### `<context>`
Use when injecting large data dumps to prevent the model from confusing data with instructions.

**Example:**
```xml
<context>
{
  "user_id": "12345",
  "session": "morning",
  "preferences": ["python", "fastapi"]
}
</context>

Your task: Build a REST API based on these user preferences.
```

#### `<workflow>`
Use when step order is non-negotiable and must be followed exactly.

**Example:**
```xml
<workflow>
1. Read the database schema
2. Create migration files
3. Run migrations
4. Verify schema
</workflow>
```

#### `<constraints>`
Use for negative constraints (NEVER/MUST NOT) to separate them from general instructions.

**Example:**
```xml
<constraints>
- NEVER use global variables
- MUST validate input
- MUST NOT hardcode credentials
</constraints>

Follow these security guidelines when writing the API.
```

#### `<output_format>`
Use when the response must be parsed by a machine/script.

**Example:**
```xml
<output_format>
{
  "status": "success|error",
  "data": {...},
  "errors": [...]
}
</output_format>

Return the results in this exact JSON structure.
```

### Everything Else: Markdown

Standard instructions, descriptions, explanations, and most content should use Markdown:

```markdown
# API Development Guide

## Overview
This guide covers building REST APIs with FastAPI.

## Key Steps
1. Define your data models
2. Create endpoint handlers
3. Add validation
4. Test thoroughly

## Best Practices
- Use type hints
- Document with docstrings
- Follow REST conventions
```

## Tag Limit: 3-5 Maximum

**Critical Rule:** Never use more than 5 XML tags in a single prompt, and never nest XML tags.

**Bad (XML Soup):**
```xml
<context>
  <data>
    {"users": [...]}
  </data>
</context>
```

**Good (Flat Structure):**
```xml
<context>
{"users": [...]}
</context>
```

## Why This Works

XML containers create **explicit boundaries** that help the model:
- Distinguish instructions from data
- Understand non-negotiable sequences
- Parse machine-readable output
- Separate constraints from guidance

Markdown handles everything else more efficiently with less token overhead.

## Anti-Patterns

### XML Soup
Nesting XML tags creates confusion and wastes tokens.

### Over-Containerization
Using XML for simple instructions that should be Markdown.

### Inconsistent Structure
Mixing patterns without clear reasoning.

## Quick Reference

| Content Type | Use XML? | Tag |
|--------------|----------|-----|
| Large data dumps | Yes | `<context>` |
| Strict sequences | Yes | `<workflow>` |
| Negative constraints | Yes | `<constraints>` |
| Machine parsing | Yes | `<output_format>` |
| Instructions | No | Markdown |
| Explanations | No | Markdown |
| Descriptions | No | Markdown |
