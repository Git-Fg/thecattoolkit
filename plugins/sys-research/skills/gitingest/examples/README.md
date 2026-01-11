# GitIngest Examples

This directory contains practical, runnable examples demonstrating how to use the GitIngest skill in various scenarios.

## Prerequisites

Install GitIngest:
```bash
pip install gitingest
```

## Examples

### 1. repo_summary.py - Quick Repository Overview

**Purpose**: Generate a concise markdown summary of any repository.

**Usage**:
```bash
python repo_summary.py https://github.com/octocat/Hello-World
python repo_summary.py https://github.com/user/private-repo -t $GITHUB_TOKEN
```

**Features**:
- Repository metadata (files, tokens, structure)
- Language distribution
- Top files by size
- Key functions and classes
- README content
- Configuration and test files

**Output**: `repository-summary.md`

---

### 2. code_analyzer.py - Comprehensive Code Analysis

**Purpose**: Perform detailed code quality analysis including metrics, security scan, and recommendations.

**Usage**:
```bash
# Asynchronous mode (full analysis)
python code_analyzer.py https://github.com/user/repo

# Synchronous mode (basic analysis)
python code_analyzer.py https://github.com/user/repo --sync

# Private repository
GITHUB_TOKEN=your_token python code_analyzer.py https://github.com/user/private-repo
```

**Features**:
- Line counts (code, comments, blank)
- Function and class detection
- Language distribution
- Security vulnerability scanning
- Complexity scoring
- Maintainability recommendations

**Output**: Terminal report with metrics, issues, and recommendations

**Example Output**:
```
======================================================================
  CODE ANALYSIS REPORT
======================================================================

 Repository: user/my-project
 Files Analyzed: 42

----------------------------------------------------------------------
  METRICS
----------------------------------------------------------------------
  Total Files:        42
  Total Lines:        3,450
  Code Lines:         2,100
  Comment Lines:      450
  Blank Lines:        900
  Functions:          156
  Classes:            23
  Complexity Score:   45.2/100

  Language Distribution:
    Python           35 files (83.3%)
    JavaScript        5 files (11.9%)
    Markdown          2 files (4.8%)

----------------------------------------------------------------------
  SECURITY ISSUES
----------------------------------------------------------------------

  🔴 CRITICAL (1):
    src/auth.py:42 - Use of eval()

  🟠 HIGH (2):
    src/db.py:15 - SQL injection risk
    config.py:8 - Hardcoded password

  🟡 MEDIUM (3):
    src/utils.py:23 - Unvalidated input
    ...

----------------------------------------------------------------------
  RECOMMENDATIONS
----------------------------------------------------------------------

  1. CRITICAL: 1 security issues found. Review immediately.
  2. Large codebase detected. Consider modular organization.
  3. Primary language: Python (35 files)

======================================================================
```

---

### 3. batch_processor.py - Multiple Repository Analysis

**Purpose**: Analyze multiple repositories concurrently and generate a comparative report.

**Usage**:
```bash
# Multiple repositories from command line
python batch_processor.py \
  https://github.com/user/repo1 \
  https://github.com/user/repo2 \
  https://github.com/user/repo3

# Repositories from file
echo "https://github.com/user/repo1" > repos.txt
echo "https://github.com/user/repo2" >> repos.txt
python batch_processor.py repos.txt

# Control concurrency and export JSON
python batch_processor.py repos.txt --concurrency 10 --json
```

**Features**:
- Concurrent processing (configurable)
- Comparative statistics
- Success/failure tracking
- Aggregate language distribution
- Feature comparison (tests, docs, config)
- JSON export option

**Output**:
- `batch-analysis-report.md` - Comparative markdown report
- `batch-analysis.json` - Raw data (with `--json` flag)

**Example Report Structure**:
```markdown
# Batch Repository Analysis Report

## Summary
- **Total Repositories**: 5
- **Successful**: 4
- **Failed**: 1
- **Total Files**: 156
- **Total Lines**: 12,340

## Repository Details

### https://github.com/user/repo1

**Repository**: user/repo1
**Files**: 45 | **Lines**: 3,450 | **Code**: 2,100

- **Languages**: Python, JavaScript
- **Functions**: 156
- **Classes**: 23
- **Largest File**: src/main.py (450 lines)
- **Features**:
  - Tests: ✓
  - Docs: ✓
  - Config: ✓

...
```

---

## File Format for Batch Processing

Create a `.txt` file with repository URLs (one per line):

```text
# My repositories
https://github.com/user/project1
https://github.com/user/project2
https://github.com/user/project3

# Private repositories (will need token)
https://github.com/company/private-repo
```

Lines starting with `#` are treated as comments and ignored.

---

## Authentication for Private Repositories

### Method 1: Environment Variable (Recommended)
```bash
export GITHUB_TOKEN="ghp_your_token_here"
python code_analyzer.py https://github.com/user/private-repo
```

### Method 2: Command Line
```bash
python code_analyzer.py https://github.com/user/private-repo -t $GITHUB_TOKEN
```

**Create Token**:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (for private repos)
4. Copy the token

---

## Error Handling

All examples include error handling for common issues:

### Rate Limiting
If you hit GitHub's rate limit:
```bash
# Wait 1 hour, or use authentication
export GITHUB_TOKEN="your_token"
```

### Network Errors
```bash
# Retry automatically by running again
python repo_summary.py https://github.com/user/repo
```

### Private Repository Access
```bash
# Check token is set
echo $GITHUB_TOKEN

# Verify token has correct permissions
# Must have 'repo' scope for private repositories
```

---

## Customization Examples

### Modify for Your Needs

**1. Custom Code Analyzer**
```python
# In code_analyzer.py, modify _generate_recommendations():
def _generate_recommendations(self) -> List[str]:
    recommendations = []

    # Add your custom checks
    if self.metrics['complexity_score'] > 30:
        recommendations.append("Consider refactoring for lower complexity")

    # Check for specific patterns
    if 'TODO' in content:
        recommendations.append("Review TODO comments")

    return recommendations
```

**2. Custom Summary Format**
```python
# In repo_summary.py, modify generate_overview():
def generate_overview(stats: Dict) -> str:
    # Add your custom overview
    overview = f"This is a {stats['total_files']} file project..."

    # Add custom sections
    if stats['languages']:
        primary = stats['languages'][0]
        overview += f"\n\nMain language: {primary}"

    return overview
```

**3. Custom Batch Report**
```python
# In batch_processor.py, modify generate_comparative_report():
def generate_comparative_report(self, results: List[Dict]) -> str:
    # Add your custom sections
    report = "# Custom Report\n\n"

    # Add project health scores
    for result in successful:
        score = calculate_health_score(result['metrics'])
        report += f"{result['url']}: Health Score {score}/100\n"

    return report
```

---

## Integration with Other Tools

### With GitHub Actions
```yaml
name: Analyze Repository

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install gitingest
      - run: python code_analyzer.py ${{ github.repository }}
```

### With CI/CD Pipeline
```bash
# In your CI script
python code_analyzer.py https://github.com/$REPO

# Fail build if critical issues found
if grep -q "CRITICAL" analysis-report.txt; then
  echo "Critical security issues found!"
  exit 1
fi
```

### With Jupyter Notebooks
```python
# In a Jupyter notebook
from gitingest import ingest
import pandas as pd

# Analyze multiple repos
repos = ['https://github.com/user/repo1', 'https://github.com/user/repo2']
data = []

for repo in repos:
    summary, tree, content = ingest(repo)
    # Process and add to data
    data.append(process_repo(summary))

df = pd.DataFrame(data)
df.to_csv('repo-analysis.csv')
```

---

## Performance Tips

### 1. Use Concurrency Wisely
```python
# Good: Control concurrency to avoid rate limits
processor = BatchProcessor(max_concurrent=3)

# Too high may trigger rate limiting
processor = BatchProcessor(max_concurrent=50)  # 
```

### 2. Filter Large Repositories
```python
# Use filters to reduce data
summary, tree, content = ingest(
    repo_url,
    include_patterns=["*.py"],  # Only Python files
    exclude_patterns=["test/*"],  # Skip tests
    max_file_size=51200  # Skip files > 50KB
)
```

### 3. Cache Results
```python
# Cache expensive operations
import hashlib
import pickle

def cached_ingest(repo_url):
    cache_key = hashlib.md5(repo_url.encode()).hexdigest()
    cache_file = f"cache/{cache_key}.pkl"

    try:
        return pickle.load(open(cache_file, 'rb'))
    except FileNotFoundError:
        result = ingest(repo_url)
        pickle.dump(result, open(cache_file, 'wb'))
        return result
```

---

## Troubleshooting

### Issue: "Command not found"
```bash
# Solution: Use python -m
python -m gitingest repo-url -o -

# Or install with pipx
pipx install gitingest
```

### Issue: "Permission denied"
```bash
# Solution: Check token permissions
# Token needs 'repo' scope for private repositories
```

### Issue: "Repository not found"
```bash
# Check URL format
gitingest https://github.com/username/repository-name

# Verify repository exists and is accessible
```

### Issue: Memory Error
```bash
# Solution: Filter files
gitingest repo-url -i "*.py" -s 51200 -o -
```

---

## Next Steps

1. **Read the API Reference** - `../references/api-reference.md`
2. **Explore Integration Patterns** - `../references/integration-patterns.md`
3. **Check Quick Start Guide** - `../references/quick-start.md`

## Support

- **Website**: https://gitingest.com
- **GitHub**: https://github.com/coderamp-labs/gitingest
- **Discord**: https://discord.gg/zerRaGK9EC

---

**Happy analyzing!** 
