# GitIngest Quick Start Guide

## Installation (30 seconds)

### Option 1: CLI Installation
```bash
pipx install gitingest
# or
pip install gitingest

# Verify
gitingest --version
```

### Option 2: Python Package
```python
pip install gitingest

# Test
python -c "from gitingest import ingest; print('Success!')"
```

## First Use Cases

### 1. Quick Repository Digest (1 minute)

**CLI Method:**
```bash
# Download any repository
gitingest https://github.com/octocat/Hello-World

# View result
cat digest.txt
```

**Python Method:**
```python
from gitingest import ingest

summary, tree, content = ingest("https://github.com/octocat/Hello-World")

print("Summary:", summary)
print("\nStructure:", tree[:200])
print("\nContent preview:", content[:500])
```

### 2. AI Analysis Pipeline (2 minutes)

**One-liner:**
```bash
# Stream directly to analysis
gitingest https://github.com/user/repo -o - | python analyze.py
```

**Analyze Script:**
```python
# analyze.py
import sys

content = sys.stdin.read()

# Simple analysis
files = content.count("FILE:")
lines = content.count('\n')

print(f"Analyzed {files} files with {lines} lines")
print("\nFirst 500 chars:")
print(content[:500])
```

### 3. Code Review Bot (5 minutes)

```python
from gitingest import ingest

def quick_code_review(repo_url: str):
    """Basic code review in 5 lines"""
    summary, tree, content = ingest(repo_url)

    # Count languages
    py_count = content.count('FILE:')  # Simplistic

    # Basic checks
    has_tests = 'test' in tree.lower()
    has_docs = 'readme' in tree.lower()

    return f"""
# Code Review for {repo_url}

## Quick Stats
- Files: {py_count}
- Has tests: {'✓' if has_tests else '✗'}
- Has docs: {'✓' if has_docs else '✗'}

## Summary
{summary}
"""
```

**Usage:**
```bash
python quick_review.py https://github.com/user/repo
```

### 4. Filtered Analysis (3 minutes)

**CLI:**
```bash
# Python files only
gitingest https://github.com/user/repo -i "*.py" -o -

# Exclude dependencies
gitingest https://github.com/user/repo -e "node_modules/*" -e "*.log" -o -

# Combine filters
gitingest repo-url -i "*.py" -i "*.js" -e "node_modules/*" -e "dist/*" -o -
```

**Python:**
```python
summary, tree, content = ingest(
    "https://github.com/user/repo",
    include_patterns=["*.py", "*.js"],
    exclude_patterns=["node_modules/*", "*.log"],
    max_file_size=51200  # Skip files > 50KB
)

print(f"Analyzed Python and JS files only")
print(f"Skipped large files, node_modules, and logs")
```

### 5. Private Repository (2 minutes)

**Setup:**
```bash
# Create token at https://github.com/settings/tokens
export GITHUB_TOKEN="ghp_your_token_here"

# Use it
gitingest https://github.com/user/private-repo -t $GITHUB_TOKEN -o -
```

**Python:**
```python
import os
from gitingest import ingest

token = os.getenv('GITHUB_TOKEN')
if not token:
    print("Set GITHUB_TOKEN environment variable")
    exit(1)

summary, tree, content = ingest(
    "https://github.com/user/private-repo",
    token=token
)

print("Successfully accessed private repository!")
```

### 6. Batch Processing (5 minutes)

```python
import asyncio
from gitingest import ingest_async

async def analyze_multiple():
    repos = [
        "https://github.com/user/repo1",
        "https://github.com/user/repo2",
        "https://github.com/user/repo3"
    ]

    # Process all at once
    tasks = [ingest_async(url) for url in repos]
    results = await asyncio.gather(*tasks)

    # Display summary
    for i, (summary, tree, content) in enumerate(results):
        print(f"\n=== Repository {i+1} ===")
        print(summary.split('\n')[0])  # First line only

asyncio.run(analyze_multiple())
```

**Usage:**
```bash
python batch_analyze.py
```

## Common Patterns (Copy-Paste)

### Pattern 1: Extract All Python Files
```python
from gitingest import ingest

summary, tree, content = ingest(
    "https://github.com/user/repo",
    include_patterns=["*.py"]
)

# Split into individual files
files = []
current_file = None

for line in content.split('\n'):
    if line.startswith('FILE: '):
        if current_file:
            files.append(current_file)
        current_file = {'path': line.replace('FILE: ', ''), 'content': []}
    elif current_file:
        current_file['content'].append(line)

if current_file:
    files.append(current_file)

print(f"Found {len(files)} Python files")
for file in files:
    print(f"- {file['path']} ({len(file['content'])} lines)")
```

### Pattern 2: Count Lines of Code
```python
from gitingest import ingest

summary, tree, content = ingest("https://github.com/user/repo")

files = content.split('================================================')
files = [f for f in files if 'FILE:' in f]

total_lines = 0
for file in files:
    lines = file.split('\n')
    total_lines += len(lines)

print(f"Total lines of code: {total_lines}")
print(f"Files: {len(files)}")
```

### Pattern 3: Find TODO Comments
```python
from gitingest import ingest

summary, tree, content = ingest("https://github.com/user/repo")

todos = []
for line in content.split('\n'):
    if 'todo' in line.lower() or 'fixme' in line.lower():
        todos.append(line.strip())

print(f"Found {len(todos)} TODOs/FIXMEs:")
for todo in todos[:10]:  # First 10
    print(f"- {todo}")
```

### Pattern 4: Extract Functions
```python
from gitingest import ingest
import re

summary, tree, content = ingest("https://github.com/user/repo")

functions = []
for line in content.split('\n'):
    match = re.match(r'def\s+(\w+)\s*\(', line)
    if match:
        functions.append(match.group(1))

print(f"Found {len(functions)} functions:")
for func in functions[:20]:  # First 20
    print(f"- {func}")
```

### Pattern 5: Check Test Coverage
```python
from gitingest import ingest

summary, tree, content = ingest("https://github.com/user/repo")

# Count test files
test_files = []
source_files = []

for line in content.split('\n'):
    if line.startswith('FILE: '):
        path = line.replace('FILE: ', '')
        if 'test' in path.lower():
            test_files.append(path)
        elif '.' in path and not path.startswith('.'):
            source_files.append(path)

coverage = len(test_files) / max(len(source_files), 1) * 100

print(f"Test files: {len(test_files)}")
print(f"Source files: {len(source_files)}")
print(f"Estimated test coverage: {coverage:.1f}%")
```

## Integration Examples

### With OpenAI/Anthropic
```python
from gitingest import ingest
import openai  # or anthropic

# Get repository
summary, tree, content = ingest("https://github.com/user/repo")

# Send to LLM
prompt = f"""
Analyze this repository:

{summary}

{tree}

{content[:10000]}  # First 10k chars

Provide insights about:
1. Architecture
2. Code quality
3. Potential improvements
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)
```

### With Vector Database
```python
from gitingest import ingest
from sentence_transformers import SentenceTransformer
import numpy as np

# Get repository
summary, tree, content = ingest("https://github.com/user/repo")

# Split into chunks
chunks = content.split('================================================')
chunks = [c.strip() for c in chunks if c.strip()]

# Embed
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)

# Store in vector DB (example with FAISS)
import faiss
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings.astype('float32'))

# Save index
faiss.write_index(index, 'repo_index.faiss')

print(f"Indexed {len(chunks)} chunks")
```

### With GitHub Actions
```yaml
# .github/workflows/analyze.yml
name: Repository Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install gitingest
        run: pip install gitingest

      - name: Analyze repository
        run: |
          gitingest . -o current-repo.txt

          python -c "
          from gitingest import ingest
          summary, tree, content = ingest('.')
          print('Repository analyzed successfully')
          "

      - name: Upload analysis
        uses: actions/upload-artifact@v3
        with:
          name: analysis
          path: current-repo.txt
```

## CLI One-Liners (Copy-Paste)

```bash
# Count files
gitingest repo-url -o - | grep -c "FILE:"

# Extract file names
gitingest repo-url -o - | grep "^FILE:" | sed 's/FILE: //'

# Count lines
gitingest repo-url -o - | wc -l

# Find Python files only
gitingest repo-url -i "*.py" -o - | grep "^FILE:"

# Skip large files
gitingest repo-url -s 10240 -o - | head -100

# Extract README
gitingest repo-url -o - | awk '/FILE: README/,/FILE:/' | tail -n +2

# Count functions
gitingest repo-url -o - | grep -c "def "

# Find TODOs
gitingest repo-url -o - | grep -i "todo\|fixme"

# Show structure only
gitingest repo-url -o - | sed -n '/Directory structure/,/=====/p'
```

## Troubleshooting

### Issue: "Command not found"
**Solution:**
```bash
# Add to PATH or use full path
python -m gitingest repo-url -o -

# Or reinstall
pipx uninstall gitingest
pipx install gitingest
```

### Issue: "Repository not found"
**Solution:**
```bash
# Check URL format
gitingest https://github.com/username/repository-name

# For private repos
export GITHUB_TOKEN="your_token"
gitingest https://github.com/private/repo -t $GITHUB_TOKEN
```

### Issue: "Rate limit exceeded"
**Solution:**
```bash
# Authenticate
export GITHUB_TOKEN="your_token"

# Or wait and retry
sleep 60
gitingest repo-url
```

### Issue: "Memory error"
**Solution:**
```python
# Use filtering
summary, tree, content = ingest(
    repo_url,
    include_patterns=["*.py"],  # Limit to specific files
    max_file_size=51200  # Skip large files
)

# Or process in chunks
files = split_content(content)
for file in files:
    process_file(file)  # Process one at a time
```

## Next Steps

1. **Read the API Reference** - Full documentation at `references/api-reference.md`
2. **Explore Integration Patterns** - See `references/integration-patterns.md`
3. **Check Examples** - See `examples/` directory
4. **Join Community** - https://discord.gg/zerRaGK9EC

## Resources

- **Website**: https://gitingest.com
- **GitHub**: https://github.com/coderamp-labs/gitingest
- **PyPI**: https://pypi.org/project/gitingest/
- **Documentation**: This skill's references/ directory

---

**Happy coding!** 🚀
