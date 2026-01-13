# Anti-Patterns

Common mistakes to avoid when creating skills.

## 1. Over-Spending Context Tokens

### ❌ Expensive: Long SKILL.md

Creating a 1000-line `SKILL.md` with detailed explanations:

```markdown
## Background (100 lines)

PDF files were created by Adobe in 1993. They are designed to be...
[100 lines of PDF history and theory]

## Installation (50 lines)

To install Python, go to python.org...
[50 lines of Python installation instructions]

## Library Comparison (100 lines)

There are many PDF libraries. pdfplumber is good because...
[100 lines of library comparisons]
```

**Problems**:
- Every skill activation loads 1000+ tokens
- Most content is not needed for most tasks
- Pollutes context window

### ✓ Efficient: Progressive Disclosure

```markdown
## Quick Start (10 lines)

Use pdfplumber for PDF text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Background**: `references/background.md`
**Library comparison**: `references/libraries.md`
```

**Benefits**:
- 50 tokens for activation
- Background info only loaded when needed
- Clean context window

## 2. First-Person Descriptions

### ❌ Wrong: "I can help you"

```yaml
---
description: "I can help you process CSV files with validation and export"
---
```

### ✓ Correct: 3rd Person

```yaml
---
description: "Processes CSV files with validation and export. Use when working with tabular data or when the user mentions CSV imports."
---
```

**Why**: Claude doesn't speak in first person. It's weird and unprofessional.

## 3. Nested References

### ❌ Wrong: Multi-Level Hierarchy

```
skill-name/
├── SKILL.md
├── overview.md
├── details.md
└── deep-details.md
```

```markdown
# SKILL.md
See overview.md...

# overview.md
See details.md...

# details.md
See deep-details.md...

# deep-details.md
Here's the actual information...
```

**Problems**:
- Claude must traverse multiple files
- Can't predict where information lives
- Wastes tokens on intermediate files

### ✓ Correct: Flat Hierarchy

```
skill-name/
├── SKILL.md
└── references/
    ├── api.md
    ├── workflows.md
    └── examples.md
```

```markdown
# SKILL.md

**API reference**: `references/api.md`
**Workflows**: `references/workflows.md`
**Examples**: `references/examples.md`

# references/api.md
Direct content here (one level deep)
```

## 4. Path Traversal

### ❌ Wrong: Accessing Other Skills

```markdown
See ../../other-skill/references/shared.md
```

**Problems**:
- Breaks portability
- Validation failure
- Creates implicit dependencies

### ✓ Correct: Self-Contained

Each skill contains its own references:

```markdown
# my-skill/SKILL.md
See references/shared.md

# my-skill/references/shared.md
Content here (copied or synthesized)
```

**Note**: If content is truly shared, it should be in a common location (docs/) and skills reference it via absolute paths from project root.

## 5. Over-Explaining Basics

### ❌ Wrong: Teaching Claude

```markdown
## What is a CSV?

CSV stands for Comma-Separated Values. It is a file format that stores
tabular data in plain text. Each line represents a row, and columns
are separated by commas. CSV files are widely used because they are
simple and human-readable...

## What is Python?

Python is a high-level programming language created by Guido van Rossum...
```

**Problems**:
- Claude already knows what CSV and Python are
- Wastes 100+ tokens on基础知识
- Insults Claude's intelligence

### ✓ Correct: Assume Knowledge

```markdown
## CSV Processing

Use pandas for CSV operations:

```python
import pandas as pd
df = pd.read_csv("file.csv")
```

For complex parsing, see `references/parsing.md`
```

## 6. No "Use When" Pattern

### ❌ Wrong: Vague Description

```yaml
---
description: "Processes PDF files"
---
```

**Problems**:
- Claude doesn't know when to select it
- User doesn't understand the trigger
- Poor discovery

### ✓ Correct: Clear Triggers

```yaml
---
description: "Extracts text and tables from PDF files. Use when working with PDF documents or when the user mentions PDF parsing, text extraction, or document analysis."
---
```

## 7. Windows-Style Paths

### ❌ Wrong: Backslashes

```markdown
Use the script at `scripts\helper.py` to process data.
```

### ✓ Correct: Forward Slashes

```markdown
Use the script at `scripts/helper.py` to process data.
```

**Why**: Cross-platform compatibility and validation requirements.

## 8. Forking When Inline Would Work

### ❌ Wrong: Unnecessary Fork

```yaml
---
name: simple-validator
description: Validates JSON files
context: fork  # Unnecessary isolation
---
```

**Problems**:
- Fork costs 3× (inline = 1)
- Overkill for simple tasks
- Slower execution

### ✓ Correct: Inline by Default

```yaml
---
name: simple-validator
description: Validates JSON files. Use when checking JSON syntax or structure.
# No context: fork needed
---
```

**When to fork**:
- Reading 100+ files
- Massive log output
- Noisy research tasks

## 9. Too Many Options

### ❌ Wrong: Option Paralysis

```markdown
## PDF Processing Libraries

You can use:
- pdfplumber
- PyPDF2
- PyMuPDF
- pdf2image
- camelot
- tabula-py
- textract

Choose the one that fits your needs...
```

**Problems**:
- Claude wastes tokens deciding
- No clear recommendation
- Poor user experience

### ✓ Correct: Default with Escape Hatch

```markdown
## PDF Processing

Use pdfplumber for text extraction:
```python
import pdfplumber
```

**For OCR** (scanned PDFs): Use pdf2image with pytesseract instead.
**For tables**: Use camelot.
```

## 10. Interactive Intake Instead of Context

### ❌ Wrong: Ask First

```markdown
## Step 1: Ask the user

Use AskUserQuestion to determine:
- What format?
- What fields?
- What validation?
```

**Problems**:
- Wastes a turn
- User already provided context in files
- Poor experience

### ✓ Correct: Infer from Context

```markdown
## Step 1: Analyze requirements

Read existing files to infer:
- Format: Check file extensions
- Fields: Read schema files
- Validation: Look for validation rules

Only ask if context is insufficient.
```

## 11. Redundant README

### ❌ Wrong: Both README.md and SKILL.md

```
skill-name/
├── README.md      # Duplicate information
└── SKILL.md       # Same content
```

### ✓ Correct: SKILL.md Only

```
skill-name/
└── SKILL.md       # Single source of truth
```

**Why**: SKILL.md is indexed and loaded. README.md is ignored by the skill system.

## 12. Missing Validation

### ❌ Wrong: Ship and Pray

Write skill, never validate, hope it works.

### ✓ Correct: Validate Always

```bash
# After every edit
uv run scripts/toolkit-analyzer.py

# Fix issues
uv run scripts/toolkit-analyzer.py --fix

# Re-validate
uv run scripts/toolkit-analyzer.py
```

## 13. Ignoring Token Costs

### ❌ Wrong: Token Blobs

Loading 5000-line reference files for simple queries.

### ✓ Correct: Lazy Loading

Only load references when explicitly needed:

```markdown
## Quick start
Use pdfplumber for basic extraction.

**For advanced features**: See `references/advanced.md`
```

## 14. Fragile Assumptions

### ❌ Wrong: Brittle Code

```python
# Assumes file exists, line has 5 fields
fields = line.split(",")
```

### ✓ Correct: Handle Errors

```python
try:
    fields = line.split(",")
    if len(fields) != 5:
        raise ValueError(f"Expected 5 fields, got {len(fields)}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
```

## 15. Time-Sensitive Information

### ❌ Wrong: Temporal References

```markdown
If you're using this before August 2025, use the old API.
After August 2025, use the new API.
```

**Problems**:
- Expires quickly
- Confusing after date
- Maintenance burden

### ✓ Correct: Current Pattern

```markdown
## Current method

Use the v2 API: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`
</details>
```

## Summary

| Anti-Pattern | Solution |
|-------------|----------|
| Long SKILL.md | Progressive disclosure (< 500 lines) |
| First-person | Third-person descriptions |
| Nested references | Flat hierarchy |
| Path traversal | Self-contained skills |
| Over-explaining | Assume Claude is smart |
| No "Use when" | Clear trigger patterns |
| Windows paths | Unix forward slashes |
| Unnecessary forks | Inline-first |
| Too many options | Default with escape hatch |
| Interactive intake | Infer from context |
| Redundant README | SKILL.md only |
| No validation | Validate after every edit |
| Token blobs | Lazy loading |
| Brittle code | Error handling |
| Time-sensitive | Current + legacy sections |
