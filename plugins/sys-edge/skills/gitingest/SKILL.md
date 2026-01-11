---
name: gitingest
description: "USE when you need to ingest Git repositories into AI-readable format. Transforms repositories into structured plain-text digests optimized for LLM consumption with CLI and Python package support."
allowed-tools: [Read, Write, Edit, Bash, Grep]
---

# GitIngest Protocol

## Purpose

GitIngest is an AI agent integration tool that turns any Git repository into a prompt-ready text digest. It fetches, cleans, and formats source code so AI agents and Large Language Models can reason over complete projects programmatically.

## Core Capabilities

### 1. Repository Ingestion Methods

**CLI Integration (Recommended for Automation)**
```bash
# Basic usage - stream to AI processor
gitingest https://github.com/user/repo -o - | your_ai_processor

# Selective file analysis
gitingest https://github.com/user/repo \
  -i "*.py" -i "*.js" -i "*.md" \
  -s 102400 \
  -o - | python your_analyzer.py

# Exclude unwanted files
gitingest https://github.com/user/repo \
  -e "node_modules/*" -e "*.log" -e "dist/*" \
  -o - | your_analyzer

# Private repositories with token
export GITHUB_TOKEN="ghp_your_token_here"
gitingest https://github.com/user/private-repo -t $GITHUB_TOKEN -o -

# Specific branch analysis
gitingest https://github.com/user/repo -b main -o -
```

**Python Package Integration (Best for Code Integration)**
```python
from gitingest import ingest, ingest_async
import asyncio

# Synchronous processing
def analyze_repository(repo_url: str):
    summary, tree, content = ingest(repo_url)

    # Process metadata
    repo_info = parse_summary(summary)

    # Analyze structure
    file_structure = parse_tree(tree)

    # Process code content
    return analyze_code(content)

# Asynchronous processing for batch analysis
async def batch_analyze_repos(repo_urls: list):
    tasks = [ingest_async(url) for url in repo_urls]
    results = await asyncio.gather(*tasks)
    return [process_repo_data(*result) for result in results]

# Memory-efficient processing for large repos
def stream_process_repo(repo_url: str):
    summary, tree, content = ingest(
        repo_url,
        max_file_size=51200,  # 50KB max per file
        include_patterns=["*.py", "*.js"],  # Focus on code files
    )

    # Process in chunks to manage memory
    for file_content in split_content(content):
        yield analyze_file(file_content)
```

### 2. Output Format Structure

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

if __name__ == "__main__":
    hello_world()


================================================
FILE: README.md
================================================
# Project Title

This is a sample project...
```

### 3. Filtering and Configuration Options

**Size Limits:**
- `-s` / `--max-size`: Maximum file size in bytes (default: no limit)
- Use for memory management with large repositories

**Pattern Filtering:**
- `-i` / `--include-pattern`: Include files matching Unix shell-style wildcards
- `-e` / `--exclude-pattern`: Exclude files matching Unix shell-style wildcards

**Common Exclude Patterns:**
```
node_modules/*          # Dependencies
*.log                   # Log files
dist/*                  # Build outputs
build/*                 # Build directories
*.min.js                # Minified files
*.lock                  # Lock files (package-lock.json, etc.)
```

**Branch and Authentication:**
- `-b` / `--branch`: Specify branch to analyze
- `-t` / `--token`: GitHub personal access token for private repos

### 4. Integration Patterns for AI Agents

**Pattern 1: Full Repository Analysis**
```python
def full_repo_analysis(repo_url: str):
    summary, tree, content = ingest(repo_url)
    return {
        'metadata': extract_metadata(summary),
        'structure': analyze_structure(tree),
        'code_analysis': analyze_all_files(content),
        'insights': generate_insights(summary, tree, content)
    }
```

**Pattern 2: Selective File Processing**
```python
def selective_analysis(repo_url: str, file_patterns: list):
    summary, tree, content = ingest(
        repo_url,
        include_patterns=file_patterns
    )
    return focused_analysis(content)
```

**Pattern 3: Streaming for Large Repositories**
```python
def stream_analysis(repo_url: str):
    # First pass: get structure and metadata only
    summary, tree, _ = ingest(
        repo_url,
        include_patterns=["*.md", "*.txt"],
        max_file_size=10240  # 10KB limit for docs
    )

    # Then process code files selectively by language
    for pattern in ["*.py", "*.js", "*.go", "*.rs"]:
        _, _, content = ingest(
            repo_url,
            include_patterns=[pattern],
            max_file_size=51200  # 50KB limit for code
        )
        yield process_language_specific(content, pattern)
```

### 5. Error Handling and Resilience

```python
from gitingest import ingest
from gitingest.utils.exceptions import GitIngestError
import time

def robust_ingest(repo_url: str, retries: int = 3):
    """Robust ingestion with retry logic"""
    for attempt in range(retries):
        try:
            return ingest(repo_url)
        except GitIngestError as e:
            if attempt == retries - 1:
                return None, None, f"Failed to ingest: {e}"
            time.sleep(2 ** attempt)  # Exponential backoff

def ingest_private_repo(repo_url: str):
    """Secure private repository access"""
    import os
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable required")
    return ingest(repo_url, token=token)
```

### 6. Common Use Cases

| Use Case | Method | Example |
|----------|--------|---------|
| **Code Review Bot** | Python async | `await ingest_async(pr_repo)` → analyze changes |
| **Documentation Generator** | CLI with filtering | `gitingest repo -i "*.py" -i "*.md" -o -` |
| **Vulnerability Scanner** | Python with error handling | Batch process multiple repos |
| **Code Search Engine** | CLI → Vector DB | `gitingest repo -o - \| embed \| store` |
| **AI Coding Assistant** | Python integration | Load repo context into conversation |
| **CI/CD Analysis** | CLI integration | `gitingest repo -o - \| analyze_pipeline` |
| **Repository Summarization** | Python with streaming | Process large repos in chunks |
| **Dependency Analysis** | CLI exclude patterns | `gitingest repo -e "node_modules/*" -e "*.lock" -o -` |
| **Security Audit** | CLI with size limits | `gitingest repo -i "*.py" -i "*.js" -s 204800 -o -` |

## Installation and Setup

### CLI Installation
```bash
# Best practice: Use pipx for isolated environment
pipx install gitingest

# Alternative: Use pip
pip install gitingest

# Verify installation
gitingest --help
gitingest --version
```

### Python Package Installation
```bash
# For projects: Use virtual environment
python -m venv gitingest-env
source gitingest-env/bin/activate  # On Windows: gitingest-env\Scripts\activate
pip install gitingest

# Add to requirements.txt
echo "gitingest" >> requirements.txt
pip install -r requirements.txt

# For development: Install with dev dependencies
pip install gitingest[dev,server]
```

### Verification
```bash
# Test CLI installation
gitingest --version

# Test Python package
python -c "from gitingest import ingest; print('GitIngest installed successfully')"

# Quick functionality test
gitingest https://github.com/octocat/Hello-World -o test_output.txt
```

## Best Practices

### 1. Repository Analysis Workflows

**For Complete Analysis:**
```python
def comprehensive_repo_scan(repo_url: str):
    # Get everything
    summary, tree, content = ingest(repo_url)

    # Parse and analyze
    repo_data = {
        'metrics': parse_summary_metrics(summary),
        'structure': parse_directory_tree(tree),
        'files': parse_file_contents(content)
    }

    return generate_analysis_report(repo_data)
```

**For Focused Analysis:**
```python
def code_only_analysis(repo_url: str):
    # Filter to source code only
    summary, tree, content = ingest(
        repo_url,
        include_patterns=["*.py", "*.js", "*.ts", "*.go", "*.rs"],
        exclude_patterns=["test/*", "*/test/*", "docs/*"],
        max_file_size=102400  # 100KB limit
    )

    return analyze_source_code(content)
```

### 2. Memory Management

```python
def memory_efficient_analysis(repo_url: str):
    # Process in stages to manage memory

    # Stage 1: Get overview
    summary, tree, _ = ingest(repo_url)
    file_count = extract_file_count(summary)

    # Stage 2: Process by language if large
    if file_count > 100:
        results = {}
        for lang in ["*.py", "*.js", "*.ts"]:
            _, _, content = ingest(
                repo_url,
                include_patterns=[lang],
                max_file_size=51200
            )
            results[lang] = analyze_language_specific(content)
        return results
    else:
        # Small repo, process all at once
        _, _, content = ingest(repo_url)
        return analyze_all_code(content)
```

### 3. Batch Processing

```python
async def batch_process_repositories(repo_urls: list):
    """Process multiple repositories concurrently"""
    semaphore = asyncio.Semaphore(5)  # Limit concurrent requests

    async def process_single_repo(url):
        async with semaphore:
            try:
                summary, tree, content = await ingest_async(url)
                return {
                    'url': url,
                    'status': 'success',
                    'data': (summary, tree, content)
                }
            except Exception as e:
                return {
                    'url': url,
                    'status': 'error',
                    'error': str(e)
                }

    # Process all repositories
    tasks = [process_single_repo(url) for url in repo_urls]
    results = await asyncio.gather(*tasks)

    return results
```

### 4. Quality Gates

- **Repository size**: Limit files to prevent memory overflow
- **File size**: Use `--max-size` for large file handling
- **Pattern filtering**: Always use include/exclude patterns for focused analysis
- **Error handling**: Implement retry logic with exponential backoff
- **Authentication**: Use environment variables for tokens, never hardcode
- **Rate limiting**: Add delays between batch requests to respect API limits

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

5. **Handle Edge Cases**
   - Implement retry logic for failures
   - Manage memory for large repositories
   - Secure token management for private repos

## Output Files Generated

- **digest.txt**: Complete repository digest (default output)
- **summary.json**: Parsed repository metadata
- **structure.json**: Directory tree as structured data
- **content_analysis.md**: AI-processed code insights
- **analysis_report.md**: Comprehensive analysis report

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

## Support Resources

- **Web UI**: https://gitingest.com (for human use, not AI agents)
- **GitHub**: https://github.com/coderamp-labs/gitingest
- **PyPI**: https://pypi.org/project/gitingest/
- **Discord**: https://discord.gg/zerRaGK9EC
