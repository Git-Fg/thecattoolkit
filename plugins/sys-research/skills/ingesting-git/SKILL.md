---
name: ingesting-git
description: "Transforms repositories into structured plain-text digests optimized for LLM consumption. Use when analyzing GitHub repositories, digesting codebases, or ingesting git repos for AI analysis."
allowed-tools: [Read, Write, Edit, Bash, Grep]
---

# GitIngest Protocol

## Purpose

GitIngest is an AI agent integration tool that turns any Git repository into a prompt-ready text digest. It fetches, cleans, and formats source code so AI agents and Large Language Models can reason over complete projects programmatically.

## Quick Start

**Execute via Script:**
```bash
uv run --with gitingest scripts/ingest.py <url_or_path> [options]
```

**Examples:**
```bash
# Ingest remote repo
uv run --with gitingest scripts/ingest.py https://github.com/user/repo

# Ingest with filtering
uv run --with gitingest scripts/ingest.py . -i "*.py" -e "tests/*"
```

## Output Format

GitIngest returns **structured plain-text** optimized for LLM consumption with three distinct sections:

**Section 1: Repository Summary**
```
Repository: owner/repo-name
Files analyzed: 42
Estimated tokens: 15.2k
```

**Section 2: Directory Structure**
```
Directory structure:
└── project-name/
    ├── src/
    │   ├── main.py
    │   └── utils.py
    ├── tests/
    │   └── test_main.py
    └── README.md
```

**Section 3: File Contents**
```
================================================
FILE: src/main.py
================================================
def hello_world():
    print("Hello, World!")
```

## Configuration Options

| Option | Purpose | Example |
|:-------|:--------|:--------|
| `-i` / `--include-pattern` | Include files matching patterns | `-i "*.py" -i "*.js"` |
| `-e` / `--exclude-pattern` | Exclude files matching patterns | `-e "node_modules/*"` |
| `-s` / `--max-size` | Maximum file size in bytes | `-s 102400` |
| `-b` / `--branch` | Specify branch | `-b main` |
| `-t` / `--token` | GitHub access token | `-t $GITHUB_TOKEN` |
| `-o` | Output file (or `-` for stdout) | `-o digest.txt` |

## Common Exclude Patterns

```
node_modules/*          # Dependencies
*.log                   # Log files
dist/*                  # Build outputs
build/*                 # Build directories
*.min.js                # Minified files
*.lock                  # Lock files
```

## Implementation Protocol

When executing the gitingest skill:

1. **Assess Requirements**
   - Determine if CLI or Python integration is needed
   - Identify repository size and scope
   - Plan filtering strategy (include/exclude patterns)

2. **Setup Environment**
   - Verify gitingest installation
   - Check authentication for private repositories
   - Configure output destination

3. **Execute Ingestion**
   - Run gitingest with appropriate parameters
   - Monitor for errors and timeouts
   - Apply filtering and size limits

4. **Process Results**
   - Parse the three-section output format
   - Analyze summary, tree, and content
   - Generate insights and reports

## Extended Documentation

For detailed integration examples, error handling patterns, and best practices:
- **Integration Examples:** `references/integration-examples.md`

## Support Resources

- **Web UI:** https://gitingest.com (for human use, not AI agents)
- **GitHub:** https://github.com/coderamp-labs/gitingest
- **PyPI:** https://pypi.org/project/gitingest/
- **Discord:** https://discord.gg/zerRaGK9EC

## Integration with CatToolkit

**Usage Examples:**
```bash
# "Ingest this repository for AI analysis"
# → Uses gitingest to create structured digest

# "Analyze the codebase without dependencies"
# → Uses gitingest with exclude-patterns for node_modules, dist, etc.

# "Generate documentation from this repo"
# → Uses gitingest + filtering to extract docs and code structure
```

The gitingest skill integrates seamlessly with other CatToolkit skills:
- **deep-analysis**: Process gitingest output for comprehensive insights
- **software-engineering**: Analyze ingested code for quality and security
- **prompt-engineering**: Use repository context to generate better prompts
