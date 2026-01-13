# Template Examples

Reference templates and examples for different skill types.

> **NOTE**: These are example structures showing frontmatter and content patterns. Links shown are illustrative placeholders, not actual references.

## Standard Skill Template

**Use when**: Single capability, straightforward implementation

```yaml
---
name: processing-csvs
description: Processes CSV files with validation, transformation, and export. Use when working with tabular data or when the user mentions CSV imports.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [CSV Processing, Data Validation, File I/O]
dependencies: [pandas>=2.0.0]
allowed-tools: [Read, Write, Edit, Bash]
---

# Processing CSVs

Handles CSV file operations with validation and transformation.

## Quick Start

```python
import pandas as pd

df = pd.read_csv("input.csv")
df = df.dropna()
df.to_csv("output.csv", index=False)
```

**For advanced transformations**: See `references/transformations.md`

## Common Operations

**Validation**: Check for required columns
```python
required = ["id", "name", "email"]
assert all(col in df.columns for col in required)
```

**Export**: Multiple formats
- CSV: `df.to_csv()`
- JSON: `df.to_json()`
- Excel: `df.to_excel()`

**Error handling**: See `references/errors.md`
```

## Progressive Skill Template

**Use when**: Complex domain expertise requiring detailed references

```yaml
---
name: hybrid-search-implementation
description: Implements hybrid search combining keyword matching and vector similarity with reranking. Use when building search applications, implementing RAG systems, or optimizing retrieval relevance.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Search, RAG, Vector Database, Information Retrieval]
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# Hybrid Search Implementation

Combines keyword and vector search with intelligent reranking for optimal relevance.

## Architecture Overview

Three-stage pipeline:
1. **Keyword search** - BM25 for exact matches
2. **Vector search** - Semantic similarity
3. **Reranking** - Fusion of results

**Quick start**: See `references/quick-start.md`
**Deployment**: See `references/deployment.md`
**Optimization**: See `references/optimization.md`

## Component Selection

**Vector database**: Choose based on scale
- < 100K docs: ChromaDB (in-memory)
- 100K-1M docs: Qdrant (standalone)
- > 1M docs: Pinecone/Weaviate (cloud)

**Embedding model**: See `references/embeddings.md`

## Implementation Workflow

```
Progress:
- [ ] 1. Choose vector database
- [ ] 2. Select embedding model
- [ ] 3. Implement keyword search
- [ ] 4. Implement vector search
- [ ] 5. Add reranking layer
- [ ] 6. Benchmark performance
- [ ] 7. Deploy and monitor
```

**Detailed workflow**: `references/workflow.md`

## Common Patterns

**Reranking strategies**:
- Reciprocal rank fusion (RRF)
- Learned reranking (Cross-encoder)
- Hybrid score combination

**Performance tuning**: `references/tuning.md`
```

## Router Skill Template

**Use when**: Multiple workflows or decision trees

```yaml
---
name: document-automation
description: Automates document processing workflows including parsing, validation, transformation, and export. Use when handling document pipelines, batch processing, or format conversion.
version: 1.0.0
author: Orchestra Research
license: MIT
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# Document Automation

Orchestrates document processing workflows with intelligent routing.

## Workflow Selection

Determine the task type:

**Parsing?** → Follow [parsing workflow](#parsing-workflow)
**Validation?** → Follow [validation workflow](#validation-workflow)
**Transformation?** → Follow [transformation workflow](#transformation-workflow)
**Export?** → Follow [export workflow](#export-workflow)

## Parsing Workflow

1. Identify document format (PDF, DOCX, TXT)
2. Extract text and structure
3. Parse metadata

**Format-specific guides**:
- PDF: `references/pdf-parsing.md`
- DOCX: `references/docx-parsing.md`
- TXT: `references/txt-parsing.md`

## Validation Workflow

1. Define schema requirements
2. Validate data types
3. Check constraints

**Schemas**: `references/schemas.md`

## Transformation Workflow

1. Map source to target fields
2. Apply transformations
3. Handle edge cases

**Common transformations**: `references/transformations.md`

## Export Workflow

1. Choose output format
2. Serialize data
3. Write to destination

**Format guides**: `references/export.md`
```

## Checklist Skill Template

**Use when**: Task-oriented procedures with validation gates

```yaml
---
name: deploying-applications
description: Manages application deployment workflows with validation gates and rollback procedures. Use when deploying to production, managing releases, or coordinating multi-stage deployments.
version: 1.0.0
author: Orchestra Research
license: MIT
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# Deploying Applications

Coordinates application deployments with safety checks and rollback capability.

## Pre-Deployment Checklist

```
Pre-Deployment:
- [ ] 1. Run test suite
- [ ] 2. Verify environment configuration
- [ ] 3. Check database migrations
- [ ] 4. Validate dependencies
- [ ] 5. Review changelog
- [ ] 6. Create backup
```

**Step 1**: Run test suite
```bash
uv run pytest
```
Only proceed if all tests pass.

**Step 2**: Verify environment
```bash
./scripts/check-env.sh
```
Fix any missing variables.

**Step 3**: Database migrations
```bash
./scripts/migrate-dry-run.sh
```
Review planned migrations before proceeding.

**Step 4**: Validate dependencies
```bash
uv pip check
```

**Step 5**: Review changelog
See `references/changelog.md` for breaking changes.

**Step 6**: Create backup
```bash
./scripts/backup.sh
```

## Deployment

```
Deployment:
- [ ] 1. Deploy to staging
- [ ] 2. Run smoke tests
- [ ] 3. Deploy to production
- [ ] 4. Verify health
- [ ] 5. Monitor metrics
```

**Rollback procedures**: `references/rollback.md`

## Post-Deployment

```
Post-Deployment:
- [ ] 1. Verify application health
- [ ] 2. Check error logs
- [ ] 3. Monitor key metrics
- [ ] 4. Test critical paths
- [ ] 5. Notify team
```
```

## Minimal Skill Template

**Use when**: Internal utilities, helper functions

```yaml
---
name: formatting-json
description: Formats and validates JSON files with consistent indentation and sorting. Use when cleaning up JSON, ensuring valid syntax, or standardizing JSON structure.
allowed-tools: [Read, Write, Edit]
user-invocable: false
---

# Formatting JSON

Standardizes JSON file formatting across the project.

## Usage

```bash
python scripts/format-json.py path/to/file.json
```

## Standards

- Indentation: 2 spaces
- Keys: sorted alphabetically
- Trailing newline: yes

**Implementation**: `scripts/format-json.py`
```

## Zero-Context Skill Template

**Use when**: Tool wrappers, script execution without explanation

```yaml
---
name: converting-pdfs
description: Converts PDF files to text without loading source code into context. Use when extracting text from PDFs or batch processing documents.
allowed-tools: [Bash]
---

# Converting PDFs

Extracts text from PDF files using zero-context script execution.

## Usage

Do NOT write code. Run:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/convert.py "$1"
```

## Arguments

- `$1`: Input PDF path
- `$2`: Output text path (optional)

## Output

Text extracted to stdout or specified file.
```

## Command Templates

### Wrapper Command

```yaml
---
description: "Batch process CSV files"
argument-hint: "<input.csv> <output.csv>"
allowed-tools: [Skill(processing-csvs), Bash]
disable-model-invocation: true
---

# Process CSV

Invoke Skill(processing-csvs) with:
- Input: `$1`
- Output: `$2`

Process the CSV file and report results.
```

### Interactive Wizard

```yaml
---
description: "Interactive skill creation wizard"
argument-hint: "[skill-name]"
allowed-tools: [Skill(addskill), AskUserQuestion, Write, Edit]
disable-model-invocation: true
---

# Create Skill

If `$1` is empty, use AskUserQuestion to gather:
1. Skill name
2. Plugin location
3. Skill type

Then invoke Skill(addskill) with gathered information.
```

### Delegator Command

```yaml
---
description: "Launch code review agent"
allowed-tools: [Task, Bash]
disable-model-invocation: true
---

# Code Review

Get changed files:
!`git diff --name-only`

Launch code-reviewer agent with file list.
```
