# GitIngest API Reference

## Python Package API

### Core Functions

#### `ingest(repo_url: str, **kwargs) -> Tuple[str, str, str]`

**Synchronous repository ingestion**

**Parameters:**
- `repo_url` (str): Git repository URL (GitHub, GitLab, etc.)
- `token` (str, optional): Authentication token for private repositories
- `max_file_size` (int, optional): Maximum file size in bytes (default: unlimited)
- `include_patterns` (List[str], optional): Files to include (Unix shell patterns)
- `exclude_patterns` (List[str], optional): Files to exclude (Unix shell patterns)
- `branch` (str, optional): Specific branch to analyze (default: repository default)

**Returns:**
- `Tuple[str, str, str]`: (summary, tree, content)
  - `summary`: Repository metadata (name, file count, token estimate)
  - `tree`: Directory structure in text format
  - `content`: All file contents with clear delimiters

**Raises:**
- `GitIngestError`: General ingestion errors
- `AuthenticationError`: Invalid or missing token
- `RateLimitError`: API rate limit exceeded
- `NetworkError`: Connection or timeout issues

**Example:**
```python
from gitingest import ingest

# Basic usage
summary, tree, content = ingest("https://github.com/user/repo")

# With options
summary, tree, content = ingest(
    "https://github.com/user/private-repo",
    token="ghp_xxxxxxxxxxxx",
    max_file_size=51200,
    include_patterns=["*.py", "*.js"],
    exclude_patterns=["node_modules/*", "*.log"],
    branch="develop"
)
```

#### `ingest_async(repo_url: str, **kwargs) -> asyncio.Future`

**Asynchronous repository ingestion**

**Parameters:** Same as `ingest()`

**Returns:**
- `asyncio.Future`: Future object containing (summary, tree, content) tuple

**Example:**
```python
import asyncio
from gitingest import ingest_async

async def main():
    future = ingest_async("https://github.com/user/repo")
    summary, tree, content = await future

asyncio.run(main())
```

### Utility Functions

#### `parse_summary(summary: str) -> Dict[str, Any]`

Parse repository summary into structured data.

**Example:**
```python
from gitingest import parse_summary

summary_text = "Repository: octocat/hello-world\nFiles analyzed: 1\nEstimated tokens: 29"
parsed = parse_summary(summary_text)
# Returns: {'repo': 'octocat/hello-world', 'files': 1, 'tokens': 29}
```

#### `parse_tree(tree: str) -> Dict[str, Any]`

Parse directory tree into nested dictionary structure.

**Example:**
```python
from gitingest import parse_tree

tree_text = "Directory structure:\n└── project-name/\n    ├── src/\n    └── README.md"
parsed = parse_tree(tree_text)
# Returns: {'project-name': {'src': {}, 'README.md': None}}
```

#### `split_content(content: str) -> Iterator[str]`

Split file contents into individual files for processing.

**Example:**
```python
from gitingest import split_content

all_content = "================================================\nFILE: src/main.py\n================================================\n..."
for file_content in split_content(all_content):
    process_file(file_content)
```

### Exception Classes

#### `GitIngestError(Exception)`

Base exception for all gitingest errors.

**Subclasses:**
- `AuthenticationError`: Token authentication failed
- `RateLimitError`: API rate limit exceeded
- `NetworkError`: Network connectivity issues
- `RepositoryError`: Repository access errors (private, deleted, etc.)
- `ParsingError`: Content parsing errors

**Example:**
```python
from gitingest import ingest
from gitingest.utils.exceptions import GitIngestError, AuthenticationError

try:
    summary, tree, content = ingest(repo_url, token=token)
except AuthenticationError:
    print("Invalid authentication token")
except RateLimitError:
    print("Rate limit exceeded, please wait")
except GitIngestError as e:
    print(f"GitIngest error: {e}")
```

## CLI Reference

### Command Syntax

```bash
gitingest [OPTIONS] REPOSITORY_URL
```

### Options

#### `-o, --output FILE`
Output destination (default: `digest.txt`)
- Use `-` for stdout
- Use filename to save to file

**Examples:**
```bash
gitingest repo-url -o digest.txt     # Save to file
gitingest repo-url -o -              # Stream to stdout
```

#### `-s, --max-size BYTES`
Maximum file size in bytes
- Default: No limit
- Common: 51200 (50KB), 102400 (100KB)

**Examples:**
```bash
gitingest repo-url -s 51200           # 50KB limit
gitingest repo-url -s 102400         # 100KB limit
```

#### `-i, --include-pattern PATTERN`
Include files matching pattern (can be used multiple times)
- Supports Unix shell wildcards: `*`, `?`, `[chars]`
- Example: `*.py`, `*.js`, `src/*.ts`

**Examples:**
```bash
gitingest repo-url -i "*.py" -i "*.js"
gitingest repo-url -i "src/*" -i "tests/*"
```

#### `-e, --exclude-pattern PATTERN`
Exclude files matching pattern (can be used multiple times)
- Common patterns: `node_modules/*`, `*.log`, `dist/*`

**Examples:**
```bash
gitingest repo-url -e "node_modules/*" -e "*.log"
gitingest repo-url -e "dist/*" -e "build/*"
```

#### `-b, --branch BRANCH`
Specific branch to analyze
- Default: Repository's default branch

**Examples:**
```bash
gitingest repo-url -b main
gitingest repo-url -b develop
gitingest repo-url -b feature/new-auth
```

#### `-t, --token TOKEN`
GitHub personal access token for private repositories
- Alternative: Set `GITHUB_TOKEN` environment variable

**Examples:**
```bash
gitingest repo-url -t ghp_xxxxxxxxxxxx
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
gitingest repo-url  # Uses environment variable
```

#### `--version`
Show version information and exit

#### `--help`
Show help message and exit

### CLI Examples

**Basic Usage:**
```bash
# Download and save to digest.txt
gitingest https://github.com/octocat/Hello-World

# Stream to stdout
gitingest https://github.com/octocat/Hello-World -o -

# Save to custom file
gitingest https://github.com/octocat/Hello-World -o my-repo.txt
```

**Filtered Analysis:**
```bash
# Python files only
gitingest repo-url -i "*.py" -o -

# Multiple file types
gitingest repo-url -i "*.py" -i "*.js" -i "*.md" -o -

# Exclude dependencies
gitingest repo-url -e "node_modules/*" -e "*.log" -o -

# Combine filters
gitingest repo-url \
  -i "*.py" -i "*.js" \
  -e "test/*" -e "node_modules/*" \
  -o -
```

**Advanced Options:**
```bash
# Large repo with size limit
gitingest repo-url -s 51200 -o -

# Specific branch
gitingest repo-url -b develop -o -

# Private repository
gitingest repo-url -t $GITHUB_TOKEN -o -

# All options combined
gitingest repo-url \
  -i "*.py" -i "*.js" \
  -e "node_modules/*" -e "*.log" \
  -s 102400 \
  -b main \
  -t $GITHUB_TOKEN \
  -o my-analysis.txt
```

## Output Format Specification

### Section 1: Summary

**Format:**
```
Repository: {owner}/{repo-name}
Files analyzed: {count}
Estimated tokens: {number}k
```

**Example:**
```
Repository: octocat/hello-world
Files analyzed: 1
Estimated tokens: 29
```

**Token Estimation:**
- Used for LLM planning and context budgeting
- Based on average 4 characters per token
- Helps determine if content fits in context window

### Section 2: Directory Structure

**Format:**
```
Directory structure:
└── {root-dir}/
    ├── {subdir1}/
    │   ├── {file1}
    │   └── {file2}
    └── {file}
```

**Example:**
```
Directory structure:
└── octocat-hello-world/
    └── README
```

**Notes:**
- Tree structure uses Unicode box-drawing characters
- Indentation shows directory hierarchy
- Maximum depth preserved for readability

### Section 3: File Contents

**Format:**
```
================================================
FILE: {path/to/file}
================================================
{file contents}
================================================

================================================
FILE: {next-file}
================================================
{contents}
================================================

```

**Example:**
```
================================================
FILE: README
================================================
Hello World!

================================================

================================================
FILE: src/main.py
================================================
def hello():
    print("Hello, World!")

================================================

```

**Notes:**
- Clear delimiters between files
- Relative paths from repository root
- Preserves exact file contents (including whitespace)
- Empty line added after each file for separation

## Configuration

### Environment Variables

#### `GITHUB_TOKEN`
GitHub personal access token for private repositories.

**Usage:**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
gitingest https://github.com/user/private-repo
```

**Token Requirements:**
- Must have `repo` scope for private repositories
- Can be set in `.bashrc`, `.zshrc`, or shell session
- Never hardcode in scripts or version control

### Python Configuration

```python
# Custom configuration
import gitingest

# Set default options
gitingest.set_config({
    'max_file_size': 51200,
    'default_branch': 'main',
    'timeout': 30
})

# Use custom configuration
summary, tree, content = ingest(repo_url)
```

### Configuration File Support

**`.gitingest.yaml` (optional):**
```yaml
defaults:
  max_file_size: 51200
  include_patterns:
    - "*.py"
    - "*.js"
    - "*.md"
  exclude_patterns:
    - "node_modules/*"
    - "*.log"
  branch: main
```

## Rate Limiting and Performance

### Rate Limits
- GitHub API: 60 requests/hour for unauthenticated
- GitHub API: 5000 requests/hour with authentication
- Built-in delays to respect rate limits

### Performance Tips
1. **Use authentication** for private repos and higher rate limits
2. **Filter aggressively** with include/exclude patterns
3. **Set size limits** for large repositories
4. **Batch processing** with async for multiple repos
5. **Cache results** to avoid repeated API calls

### Memory Management
- Large repositories automatically chunked
- Stream processing available for very large repos
- Configurable memory limits per file
- Garbage collection between batches

## Error Codes and Troubleshooting

### Common Errors

#### Error: "Repository not found"
**Cause:** Repository is private, deleted, or URL is incorrect
**Solution:**
- Check repository URL
- Add authentication token for private repos
- Verify token has correct permissions

#### Error: "Rate limit exceeded"
**Cause:** Too many requests in short time period
**Solution:**
- Add authentication token
- Implement delays between requests
- Use exponential backoff retry logic

#### Error: "Network timeout"
**Cause:** Slow network or large repository
**Solution:**
- Increase timeout value
- Try again during off-peak hours
- Use selective filtering to reduce data

#### Error: "File too large"
**Cause:** File exceeds max_file_size limit
**Solution:**
- Increase max_file_size parameter
- Use exclude_patterns to skip large files
- Split repository into smaller chunks

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now all gitingest operations will log debug info
summary, tree, content = ingest(repo_url)
```

### Verbose CLI Output

```bash
gitingest --verbose repo-url -o -
# Shows detailed progress and API calls
```
