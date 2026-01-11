# GitIngest Integration Examples

## CLI Integration Examples

**Basic usage - stream to AI processor:**
```bash
gitingest https://github.com/user/repo -o - | your_ai_processor
```

**Selective file analysis:**
```bash
gitingest https://github.com/user/repo \
  -i "*.py" -i "*.js" -i "*.md" \
  -s 102400 \
  -o - | python your_analyzer.py
```

**Exclude unwanted files:**
```bash
gitingest https://github.com/user/repo \
  -e "node_modules/*" -e "*.log" -e "dist/*" \
  -o - | your_analyzer
```

**Private repositories with token:**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
gitingest https://github.com/user/private-repo -t $GITHUB_TOKEN -o -
```

**Specific branch analysis:**
```bash
gitingest https://github.com/user/repo -b main -o -
```

## Python Package Integration

**Synchronous processing:**
```python
from gitingest import ingest, ingest_async
import asyncio

def analyze_repository(repo_url: str):
    summary, tree, content = ingest(repo_url)

    # Process metadata
    repo_info = parse_summary(summary)

    # Analyze structure
    file_structure = parse_tree(tree)

    # Process code content
    return analyze_code(content)
```

**Asynchronous processing for batch analysis:**
```python
async def batch_analyze_repos(repo_urls: list):
    tasks = [ingest_async(url) for url in repo_urls]
    results = await asyncio.gather(*tasks)
    return [process_repo_data(*result) for result in results]
```

**Memory-efficient processing for large repos:**
```python
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

## Installation

**CLI Installation:**
```bash
# Best practice: Use pipx for isolated environment
pipx install gitingest

# Alternative: Use pip
pip install gitingest

# Verify installation
gitingest --help
gitingest --version
```

**Python Package Installation:**
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

## Error Handling

**Robust ingestion with retry logic:**
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

## Common Use Cases

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

## Best Practices

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

**Memory Management:**
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

**Batch Processing:**
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
