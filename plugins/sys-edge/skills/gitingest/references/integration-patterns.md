# GitIngest Integration Patterns

## Pattern 1: Code Review Automation

### Use Case
Automated code review for pull requests by analyzing repository changes.

### Implementation

**Python Script:**
```python
from gitingest import ingest_async
import asyncio
import json

async def analyze_pr_changes(repo_url: str, pr_number: int):
    """
    Analyze PR changes for code review insights
    """
    # Get repository content
    summary, tree, content = await ingest_async(repo_url)

    # Parse changes
    files = parse_file_contents(content)

    # Analyze each file
    review_insights = {
        'total_files': len(files),
        'languages': detect_languages(files),
        'complex_files': identify_complex_files(files),
        'security_issues': scan_security(files),
        'test_coverage': check_test_coverage(files)
    }

    # Generate review report
    report = generate_review_report(review_insights)

    return report

def parse_file_contents(content: str) -> list:
    """Split content into individual files"""
    files = []
    current_file = None

    for line in content.split('\n'):
        if line.startswith('FILE: '):
            if current_file:
                files.append(current_file)
            current_file = {
                'path': line.replace('FILE: ', ''),
                'content': []
            }
        elif current_file and line.strip():
            current_file['content'].append(line)

    if current_file:
        files.append(current_file)

    return files

def detect_languages(files: list) -> dict:
    """Detect programming languages used"""
    extensions = {}
    for file in files:
        ext = file['path'].split('.')[-1] if '.' in file['path'] else 'unknown'
        extensions[ext] = extensions.get(ext, 0) + 1
    return extensions

def identify_complex_files(files: list) -> list:
    """Identify potentially complex files"""
    complex_files = []
    for file in files:
        lines = len(file['content'])
        # Consider files with >200 lines as complex
        if lines > 200:
            complex_files.append({
                'path': file['path'],
                'lines': lines,
                'reason': 'High line count'
            })
    return complex_files

def scan_security(files: list) -> list:
    """Basic security scanning"""
    security_issues = []
    security_keywords = ['eval(', 'exec(', 'os.system', 'subprocess.call']

    for file in files:
        file_content = '\n'.join(file['content'])
        for keyword in security_keywords:
            if keyword in file_content:
                security_issues.append({
                    'file': file['path'],
                    'keyword': keyword,
                    'severity': 'high'
                })

    return security_issues

def check_test_coverage(files: list) -> dict:
    """Check for test files"""
    test_files = [f for f in files if 'test' in f['path'].lower()]
    source_files = [f for f in files if not 'test' in f['path'].lower()]

    return {
        'test_files': len(test_files),
        'source_files': len(source_files),
        'ratio': len(test_files) / max(len(source_files), 1)
    }

def generate_review_insights(insights: dict) -> str:
    """Generate human-readable review report"""
    report = f"""
# Code Review Analysis

## Overview
- **Total Files**: {insights['total_files']}
- **Languages**: {', '.join(insights['languages'].keys())}

## Complex Files
"""

    for file in insights['complex_files']:
        report += f"- {file['path']} ({file['lines']} lines) - {file['reason']}\n"

    report += "\n## Security Scan\n"
    for issue in insights['security_issues']:
        report += f"- {issue['severity'].upper()}: {issue['file']} contains '{issue['keyword']}'\n"

    report += "\n## Test Coverage\n"
    ratio = insights['test_coverage']['ratio']
    report += f"- Test files: {insights['test_coverage']['test_files']}\n"
    report += f"- Source files: {insights['test_coverage']['source_files']}\n"
    report += f"- Coverage ratio: {ratio:.2f}\n"

    return report

# Usage
async def main():
    insights = await analyze_pr_changes(
        "https://github.com/user/repo/pull/123",
        123
    )
    print(generate_review_insights(insights))

asyncio.run(main())
```

**CLI Pipeline:**
```bash
# Quick code review
gitingest https://github.com/user/repo/pull/123 \
  -i "*.py" -i "*.js" \
  -e "node_modules/*" -e "*.test.*" \
  -o - | python code_review_analyzer.py
```

## Pattern 2: Documentation Generation

### Use Case
Automatically generate documentation from repository structure and code.

### Implementation

```python
from gitingest import ingest
import re

def generate_docs_from_repo(repo_url: str):
    """Generate comprehensive documentation"""
    summary, tree, content = ingest(repo_url)

    # Parse repository info
    repo_info = parse_summary(summary)

    # Extract documentation
    docs = {
        'readme': extract_readme(content),
        'api_endpoints': extract_api_endpoints(content),
        'data_models': extract_data_models(content),
        'functions': extract_functions(content),
        'classes': extract_classes(content)
    }

    # Generate documentation
    doc_content = format_documentation(repo_info, docs)

    return doc_content

def extract_readme(content: str) -> str:
    """Extract README content"""
    files = split_content_by_file(content)
    for file in files:
        if 'readme' in file['path'].lower():
            return '\n'.join(file['content'])
    return ""

def extract_api_endpoints(content: str) -> list:
    """Extract API endpoints from code"""
    endpoints = []
    files = split_content_by_file(content)

    for file in files:
        if file['path'].endswith(('.py', '.js', '.ts')):
            content_text = '\n'.join(file['content'])

            # Flask/Python patterns
            patterns = [
                r"@app\.route\(['\"]([^'\"]+)['\"]",
                r"def \w+\([^)]*\):\s*#\s*([^:]+)",
            ]

            for pattern in patterns:
                matches = re.findall(pattern, content_text)
                for match in matches:
                    endpoints.append({
                        'file': file['path'],
                        'endpoint': match
                    })

    return endpoints

def extract_data_models(content: str) -> list:
    """Extract data models/classes"""
    models = []
    files = split_content_by_file(content)

    for file in files:
        content_text = '\n'.join(file['content'])

        # Class definitions
        class_pattern = r"class\s+(\w+).*?:"
        for match in re.finditer(class_pattern, content_text):
            models.append({
                'file': file['path'],
                'class': match.group(1)
            })

    return models

def format_documentation(repo_info: dict, docs: dict) -> str:
    """Format documentation as markdown"""
    output = f"""
# {repo_info['repo']} Documentation

## Overview

This repository contains {repo_info['files']} files.

## Table of Contents

1. [README](#readme)
2. [API Endpoints](#api-endpoints)
3. [Data Models](#data-models)
4. [Functions](#functions)

## README

{docs['readme']}

## API Endpoints

"""

    for endpoint in docs['api_endpoints']:
        output += f"- **{endpoint['endpoint']}** ({endpoint['file']})\n"

    output += "\n## Data Models\n\n"
    for model in docs['data_models']:
        output += f"- {model['class']} ({model['file']})\n"

    return output

def split_content_by_file(content: str) -> list:
    """Split content into individual files"""
    files = []
    current_file = None

    for line in content.split('\n'):
        if line.startswith('FILE: '):
            if current_file:
                files.append(current_file)
            current_file = {
                'path': line.replace('FILE: ', ''),
                'content': []
            }
        elif current_file:
            current_file['content'].append(line)

    if current_file:
        files.append(current_file)

    return files

# Usage
docs = generate_docs_from_repo("https://github.com/user/repo")
with open('documentation.md', 'w') as f:
    f.write(docs)
```

## Pattern 3: Vulnerability Scanner

### Use Case
Scan repositories for security vulnerabilities and suspicious patterns.

### Implementation

```python
from gitingest import ingest, ingest_async
import asyncio
import re
from typing import List, Dict

class VulnerabilityScanner:
    def __init__(self):
        # OWASP Top 10 and common vulnerabilities
        self.vulnerability_patterns = {
            'sql_injection': [
                r"execute\s*\(\s*['\"].*?%.*?['\"]",
                r"cursor\.execute\s*\(\s*f['\"].*\{.*\}.*['\"]",
            ],
            'command_injection': [
                r"os\.system\s*\(",
                r"subprocess\.call\s*\(",
                r"subprocess\.run\s*\(",
                r"eval\s*\(",
                r"exec\s*\(",
            ],
            'path_traversal': [
                r"\.\./",
                r"os\.path\.join\s*\(.*\.\./",
            ],
            'hardcoded_secrets': [
                r"password\s*=\s*['\"][^'\"]{8,}['\"]",
                r"api_key\s*=\s*['\"][^'\"]{20,}['\"]",
                r"secret\s*=\s*['\"][^'\"]{20,}['\"]",
            ],
            'weak_crypto': [
                r"md5\s*\(",
                r"sha1\s*\(",
            ],
            'xss': [
                r"innerHTML\s*=",
                r"document\.write\s*\(",
            ]
        }

        self.compliance_issues = {
            'missing_validation': [
                r"input\(\)",
                r"raw_input\(\)",
            ],
            'error_disclosure': [
                r"traceback\.print_exc",
                r"console\.log\(",
            ]
        }

    async def scan_repository(self, repo_url: str) -> Dict:
        """Scan entire repository for vulnerabilities"""
        summary, tree, content = await ingest_async(repo_url)

        files = self.split_content(content)
        scan_results = {
            'vulnerabilities': [],
            'compliance_issues': [],
            'summary': {
                'total_files': len(files),
                'files_scanned': 0,
                'vulnerabilities_found': 0,
                'severity_levels': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
            }
        }

        for file in files:
            file_vulns = self.scan_file(file)
            scan_results['vulnerabilities'].extend(file_vulns['vulnerabilities'])
            scan_results['compliance_issues'].extend(file_vulns['compliance'])
            scan_results['summary']['files_scanned'] += 1

        # Update severity counts
        for vuln in scan_results['vulnerabilities']:
            scan_results['summary']['vulnerabilities_found'] += 1
            scan_results['summary']['severity_levels'][vuln['severity']] += 1

        return scan_results

    def scan_file(self, file: Dict) -> Dict:
        """Scan individual file for vulnerabilities"""
        content = '\n'.join(file['content'])
        vulnerabilities = []
        compliance_issues = []

        # Check each vulnerability pattern
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1

                    vulnerabilities.append({
                        'type': vuln_type,
                        'file': file['path'],
                        'line': line_num,
                        'severity': self.get_severity(vuln_type),
                        'match': match.group(),
                        'description': self.get_description(vuln_type)
                    })

        # Check compliance patterns
        for comp_type, patterns in self.compliance_issues.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1

                    compliance_issues.append({
                        'type': comp_type,
                        'file': file['path'],
                        'line': line_num,
                        'match': match.group(),
                        'recommendation': self.get_recommendation(comp_type)
                    })

        return {
            'vulnerabilities': vulnerabilities,
            'compliance': compliance_issues
        }

    def get_severity(self, vuln_type: str) -> str:
        """Map vulnerability type to severity"""
        severity_map = {
            'sql_injection': 'critical',
            'command_injection': 'critical',
            'hardcoded_secrets': 'high',
            'path_traversal': 'high',
            'weak_crypto': 'medium',
            'xss': 'medium'
        }
        return severity_map.get(vuln_type, 'low')

    def get_description(self, vuln_type: str) -> str:
        """Get description for vulnerability type"""
        descriptions = {
            'sql_injection': 'Potential SQL injection vulnerability',
            'command_injection': 'Potential command injection vulnerability',
            'hardcoded_secrets': 'Hardcoded secret or credential detected',
            'path_traversal': 'Potential path traversal vulnerability',
            'weak_crypto': 'Use of weak cryptographic hash',
            'xss': 'Potential XSS vulnerability'
        }
        return descriptions.get(vuln_type, 'Security issue detected')

    def get_recommendation(self, issue_type: str) -> str:
        """Get recommendation for compliance issue"""
        recommendations = {
            'missing_validation': 'Add input validation',
            'error_disclosure': 'Remove or properly handle error output'
        }
        return recommendations.get(issue_type, 'Review this code')

    def split_content(self, content: str) -> List[Dict]:
        """Split content into individual files"""
        files = []
        current_file = None

        for line in content.split('\n'):
            if line.startswith('FILE: '):
                if current_file:
                    files.append(current_file)
                current_file = {
                    'path': line.replace('FILE: ', ''),
                    'content': []
                }
            elif current_file:
                current_file['content'].append(line)

        if current_file:
            files.append(current_file)

        return files

    def generate_report(self, scan_results: Dict) -> str:
        """Generate vulnerability scan report"""
        report = f"""
# Security Scan Report

## Summary
- Files scanned: {scan_results['summary']['files_scanned']}
- Total vulnerabilities: {scan_results['summary']['vulnerabilities_found']}
- Critical: {scan_results['summary']['severity_levels']['critical']}
- High: {scan_results['summary']['severity_levels']['high']}
- Medium: {scan_results['summary']['severity_levels']['medium']}
- Low: {scan_results['summary']['severity_levels']['low']}

## Vulnerabilities

"""

        for vuln in scan_results['vulnerabilities']:
            report += f"""
### {vuln['type'].upper()} - {vuln['severity'].upper()}
- **File**: {vuln['file']}
- **Line**: {vuln['line']}
- **Match**: `{vuln['match']}`
- **Description**: {vuln['description']}
"""

        report += "\n## Compliance Issues\n\n"
        for issue in scan_results['compliance_issues']:
            report += f"""
### {issue['type'].upper()}
- **File**: {issue['file']}
- **Line**: {issue['line']}
- **Recommendation**: {issue['recommendation']}
"""

        return report

# Usage
async def main():
    scanner = VulnerabilityScanner()
    results = await scanner.scan_repository("https://github.com/user/repo")
    report = scanner.generate_report(results)

    with open('security-report.md', 'w') as f:
        f.write(report)

asyncio.run(main())
```

## Pattern 4: Code Search Engine

### Use Case
Build a semantic code search engine from repository content.

### Implementation

```python
from gitingest import ingest
import ast
import re
from typing import List, Dict, Any

class CodeSearchEngine:
    def __init__(self):
        self.index = {}

    def build_index(self, repo_url: str):
        """Build search index from repository"""
        summary, tree, content = ingest(repo_url)
        files = self.split_content(content)

        for file in files:
            self.index_file(file)

    def index_file(self, file: Dict):
        """Index individual file"""
        content = '\n'.join(file['content'])
        file_path = file['path']

        # Index functions
        functions = self.extract_functions(content)
        for func in functions:
            key = f"{file_path}:{func['name']}"
            self.index[key] = {
                'type': 'function',
                'file': file_path,
                'name': func['name'],
                'signature': func['signature'],
                'docstring': func['docstring'],
                'lines': func['lines']
            }

        # Index classes
        classes = self.extract_classes(content)
        for cls in classes:
            key = f"{file_path}:{cls['name']}"
            self.index[key] = {
                'type': 'class',
                'file': file_path,
                'name': cls['name'],
                'methods': cls['methods'],
                'docstring': cls['docstring']
            }

    def extract_functions(self, content: str) -> List[Dict]:
        """Extract function definitions"""
        functions = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            # Python function pattern
            match = re.match(r'def\s+(\w+)\s*\(([^)]*)\):', line)
            if match:
                name = match.group(1)
                signature = match.group(2)

                # Extract docstring
                docstring = ""
                if i + 1 < len(lines) and '"""' in lines[i + 1]:
                    docstring_lines = []
                    j = i + 1
                    while j < len(lines):
                        if '"""' in lines[j]:
                            break
                        docstring_lines.append(lines[j])
                        j += 1
                    docstring = '\n'.join(docstring_lines)

                functions.append({
                    'name': name,
                    'signature': signature,
                    'docstring': docstring,
                    'lines': i + 1
                })

        return functions

    def extract_classes(self, content: str) -> List[Dict]:
        """Extract class definitions"""
        classes = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            # Python class pattern
            match = re.match(r'class\s+(\w+)', line)
            if match:
                name = match.group(1)

                # Extract methods
                methods = []
                indent_level = len(line) - len(line.lstrip())
                j = i + 1

                while j < len(lines):
                    method_line = lines[j]
                    if method_line.strip() and not method_line.startswith(' ' * (indent_level + 4)):
                        break

                    method_match = re.match(r'\s+def\s+(\w+)\s*\(', method_line)
                    if method_match:
                        methods.append(method_match.group(1))

                    j += 1

                # Extract docstring
                docstring = ""
                if i + 1 < len(lines) and '"""' in lines[i + 1]:
                    docstring_lines = []
                    j = i + 1
                    while j < len(lines):
                        if '"""' in lines[j]:
                            break
                        docstring_lines.append(lines[j])
                        j += 1
                    docstring = '\n'.join(docstring_lines)

                classes.append({
                    'name': name,
                    'methods': methods,
                    'docstring': docstring,
                    'lines': i + 1
                })

        return classes

    def search(self, query: str) -> List[Dict]:
        """Search index for query"""
        results = []
        query_lower = query.lower()

        for key, item in self.index.items():
            # Match in name
            if query_lower in item['name'].lower():
                results.append({
                    'match_type': 'name',
                    'score': 1.0,
                    'item': item
                })
            # Match in docstring
            elif 'docstring' in item and item['docstring']:
                if query_lower in item['docstring'].lower():
                    results.append({
                        'match_type': 'docstring',
                        'score': 0.7,
                        'item': item
                    })
            # Match in signature
            elif 'signature' in item and query_lower in item['signature'].lower():
                results.append({
                    'match_type': 'signature',
                    'score': 0.8,
                    'item': item
                })

        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def split_content(self, content: str) -> List[Dict]:
        """Split content into individual files"""
        files = []
        current_file = None

        for line in content.split('\n'):
            if line.startswith('FILE: '):
                if current_file:
                    files.append(current_file)
                current_file = {
                    'path': line.replace('FILE: ', ''),
                    'content': []
                }
            elif current_file:
                current_file['content'].append(line)

        if current_file:
            files.append(current_file)

        return files

# Usage
engine = CodeSearchEngine()
engine.build_index("https://github.com/user/repo")

# Search for functions
results = engine.search("authentication")
for result in results:
    print(f"{result['item']['file']}:{result['item']['name']}")
```

## Pattern 5: Batch Repository Analysis

### Use Case
Analyze multiple repositories in batch for organization-wide insights.

### Implementation

```python
from gitingest import ingest_async
import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

class BatchAnalyzer:
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.results = []

    async def analyze_repositories(self, repo_urls: List[str]) -> List[Dict]:
        """Analyze multiple repositories concurrently"""
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def analyze_single(url):
            async with semaphore:
                try:
                    summary, tree, content = await ingest_async(url)
                    return self.process_repository(url, summary, tree, content)
                except Exception as e:
                    return {
                        'url': url,
                        'status': 'error',
                        'error': str(e)
                    }

        # Execute all analyses concurrently
        tasks = [analyze_single(url) for url in repo_urls]
        results = await asyncio.gather(*tasks)

        return results

    def process_repository(self, url: str, summary: str, tree: str, content: str) -> Dict:
        """Process single repository results"""
        repo_info = {
            'url': url,
            'status': 'success',
            'summary': self.parse_summary(summary),
            'structure': self.parse_tree(tree),
            'metrics': self.calculate_metrics(content),
            'languages': self.detect_languages(content)
        }

        return repo_info

    def parse_summary(self, summary: str) -> Dict:
        """Parse repository summary"""
        lines = summary.split('\n')
        info = {}

        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()

        return info

    def parse_tree(self, tree: str) -> Dict:
        """Parse directory structure"""
        # Simplified - extract file count per directory
        directories = {}
        for line in tree.split('\n'):
            if '├──' in line or '└──' in line:
                path = line.strip().split('├── ')[-1].split('└── ')[-1]
                if '.' in path:  # It's a file
                    dir_path = '/'.join(path.split('/')[:-1])
                    directories[dir_path] = directories.get(dir_path, 0) + 1

        return directories

    def calculate_metrics(self, content: str) -> Dict:
        """Calculate code metrics"""
        metrics = {
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0
        }

        files = self.split_content(content)

        for file in files:
            for line in file['content']:
                metrics['total_lines'] += 1

                if line.strip() == '':
                    metrics['blank_lines'] += 1
                elif line.strip().startswith('#') or line.strip().startswith('//'):
                    metrics['comment_lines'] += 1
                else:
                    metrics['code_lines'] += 1

        return metrics

    def detect_languages(self, content: str) -> Dict:
        """Detect programming languages"""
        languages = {}
        files = self.split_content(content)

        for file in files:
            ext = file['path'].split('.')[-1] if '.' in file['path'] else 'unknown'
            languages[ext] = languages.get(ext, 0) + 1

        return languages

    def split_content(self, content: str) -> List[Dict]:
        """Split content into individual files"""
        files = []
        current_file = None

        for line in content.split('\n'):
            if line.startswith('FILE: '):
                if current_file:
                    files.append(current_file)
                current_file = {
                    'path': line.replace('FILE: ', ''),
                    'content': []
                }
            elif current_file:
                current_file['content'].append(line)

        if current_file:
            files.append(current_file)

        return files

    def generate_batch_report(self, results: List[Dict]) -> str:
        """Generate comprehensive batch analysis report"""
        report = "# Batch Repository Analysis Report\n\n"

        # Summary statistics
        total_repos = len(results)
        successful = sum(1 for r in results if r['status'] == 'success')
        failed = total_repos - successful

        report += f"## Overview\n"
        report += f"- Total repositories: {total_repos}\n"
        report += f"- Successful: {successful}\n"
        report += f"- Failed: {failed}\n\n"

        # Language distribution
        all_languages = {}
        for result in results:
            if result['status'] == 'success':
                for lang, count in result['languages'].items():
                    all_languages[lang] = all_languages.get(lang, 0) + count

        report += "## Language Distribution\n\n"
        for lang, count in sorted(all_languages.items(), key=lambda x: x[1], reverse=True):
            report += f"- {lang}: {count} files\n"

        # Repository details
        report += "\n## Repository Details\n\n"
        for result in results:
            if result['status'] == 'success':
                report += f"### {result['url']}\n"
                report += f"- Files: {result['summary'].get('Files analyzed', 'N/A')}\n"
                report += f"- Total lines: {result['metrics']['total_lines']}\n"
                report += f"- Code lines: {result['metrics']['code_lines']}\n"
                report += f"- Comments: {result['metrics']['comment_lines']}\n\n"
            else:
                report += f"### {result['url']}\n"
                report += f"- Status: FAILED\n"
                report += f"- Error: {result.get('error', 'Unknown')}\n\n"

        return report

# Usage
async def main():
    repos = [
        "https://github.com/user/repo1",
        "https://github.com/user/repo2",
        "https://github.com/user/repo3"
    ]

    analyzer = BatchAnalyzer(max_concurrent=3)
    results = await analyzer.analyze_repositories(repos)

    # Generate and save report
    report = analyzer.generate_batch_report(results)
    with open('batch-analysis.md', 'w') as f:
        f.write(report)

    # Save raw data
    with open('batch-data.json', 'w') as f:
        json.dump(results, f, indent=2)

asyncio.run(main())
```

## Pattern 6: Context-Aware Prompt Generation

### Use Case
Generate better AI prompts by understanding repository context.

### Implementation

```python
from gitingest import ingest
import json

class PromptGenerator:
    def __init__(self):
        self.prompt_templates = {
            'code_review': self.get_code_review_template(),
            'feature_request': self.get_feature_template(),
            'bug_fix': self.get_bug_fix_template(),
            'documentation': self.get_documentation_template()
        }

    def generate_context_aware_prompt(self, repo_url: str, task_type: str, **kwargs) -> str:
        """Generate prompt with repository context"""
        summary, tree, content = ingest(repo_url)

        # Extract relevant information
        context = self.extract_context(summary, tree, content)

        # Get template
        template = self.prompt_templates.get(task_type, self.get_default_template())

        # Generate prompt
        prompt = template.format(
            context=json.dumps(context, indent=2),
            task_details=kwargs.get('details', ''),
            output_format=kwargs.get('output_format', 'markdown')
        )

        return prompt

    def extract_context(self, summary: str, tree: str, content: str) -> dict:
        """Extract relevant context from repository"""
        files = self.split_content(content)

        return {
            'summary': self.parse_summary(summary),
            'structure': self.analyze_structure(tree),
            'main_files': self.identify_main_files(files),
            'technologies': self.detect_technologies(files),
            'architecture': self.analyze_architecture(files)
        }

    def parse_summary(self, summary: str) -> dict:
        """Parse repository summary"""
        lines = summary.split('\n')
        info = {}

        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()

        return info

    def analyze_structure(self, tree: str) -> dict:
        """Analyze directory structure"""
        return {
            'has_src': 'src/' in tree,
            'has_tests': 'test' in tree.lower(),
            'has_docs': any(doc in tree.lower() for doc in ['docs/', 'doc/', 'documentation/']),
            'has_config': any(cfg in tree for cfg in ['package.json', 'requirements.txt', 'Pipfile']),
            'depth': tree.count('    ') // 4
        }

    def identify_main_files(self, files: list) -> list:
        """Identify main source files"""
        main_files = []
        for file in files:
            path = file['path']
            if any(main in path.lower() for main in ['main', 'index', 'app', '__init__']):
                main_files.append(path)

        return main_files[:10]  # Top 10

    def detect_technologies(self, files: list) -> dict:
        """Detect technologies used"""
        technologies = {
            'languages': set(),
            'frameworks': set(),
            'databases': set()
        }

        for file in files:
            path = file['path'].lower()
            content = '\n'.join(file['content']).lower()

            # Detect languages
            if path.endswith('.py'):
                technologies['languages'].add('Python')
            elif path.endswith('.js') or path.endswith('.ts'):
                technologies['languages'].add('JavaScript/TypeScript')
            elif path.endswith('.java'):
                technologies['languages'].add('Java')

            # Detect frameworks
            if 'flask' in content or 'django' in content:
                technologies['frameworks'].add('Flask/Django')
            if 'express' in content:
                technologies['frameworks'].add('Express')
            if 'react' in content:
                technologies['frameworks'].add('React')

            # Detect databases
            if 'mongodb' in content or 'mongo' in content:
                technologies['databases'].add('MongoDB')
            if 'postgres' in content or 'postgresql' in content:
                technologies['databases'].add('PostgreSQL')

        return {k: list(v) for k, v in technologies.items()}

    def analyze_architecture(self, files: list) -> dict:
        """Analyze code architecture"""
        patterns = {
            'mvc': 0,
            'microservices': 0,
            'layered': 0,
            'functional': 0
        }

        for file in files:
            content = '\n'.join(file['content']).lower()

            if 'controller' in content and 'model' in content and 'view' in content:
                patterns['mvc'] += 1
            if 'service' in content and 'api' in content:
                patterns['microservices'] += 1
            if 'layer' in content or 'tier' in content:
                patterns['layered'] += 1

        return patterns

    def get_code_review_template(self) -> str:
        return """
You are conducting a code review for the following repository:

## Repository Context
{context}

## Task Details
{task_details}

## Review Focus Areas
1. Code quality and maintainability
2. Security vulnerabilities
3. Performance issues
4. Test coverage
5. Documentation completeness

## Output Format
{output_format}

Please provide detailed feedback with specific examples from the code.
"""

    def get_feature_template(self) -> str:
        return """
You are implementing a new feature for the following repository:

## Repository Context
{context}

## Feature Requirements
{task_details}

## Implementation Guidelines
1. Follow existing code style and patterns
2. Write comprehensive tests
3. Update documentation
4. Consider edge cases
5. Ensure backward compatibility

## Output Format
{output_format}

Please provide implementation plan and code.
"""

    def get_bug_fix_template(self) -> str:
        return """
You are fixing a bug in the following repository:

## Repository Context
{context}

## Bug Description
{task_details}

## Investigation Steps
1. Identify root cause
2. Check for similar issues
3. Develop fix
4. Add regression test
5. Verify solution

## Output Format
{output_format}

Please provide detailed analysis and fix.
"""

    def get_documentation_template(self) -> str:
        return """
You are creating documentation for the following repository:

## Repository Context
{context}

## Documentation Requirements
{task_details}

## Documentation Structure
1. Overview and purpose
2. Installation and setup
3. API reference
4. Usage examples
5. Troubleshooting

## Output Format
{output_format}

Please generate comprehensive documentation.
"""

    def get_default_template(self) -> str:
        return """
Repository Context:
{context}

Task: {task_details}

Output Format: {output_format}
"""

    def split_content(self, content: str) -> list:
        """Split content into individual files"""
        files = []
        current_file = None

        for line in content.split('\n'):
            if line.startswith('FILE: '):
                if current_file:
                    files.append(current_file)
                current_file = {
                    'path': line.replace('FILE: ', ''),
                    'content': []
                }
            elif current_file:
                current_file['content'].append(line)

        if current_file:
            files.append(current_file)

        return files

# Usage
generator = PromptGenerator()

# Generate code review prompt
prompt = generator.generate_context_aware_prompt(
    "https://github.com/user/repo",
    "code_review",
    details="Review authentication and authorization code",
    output_format="markdown"
)

print(prompt)
```

## Best Practices Summary

### 1. Always Use Context Managers
```python
# Good
with open('output.txt', 'w') as f:
    summary, tree, content = ingest(repo_url)
    f.write(summary)

# Bad - don't do this
summary, tree, content = ingest(repo_url)
open('output.txt', 'w').write(summary)
```

### 2. Implement Retry Logic
```python
import time
from gitingest.utils.exceptions import GitIngestError

def robust_ingest(repo_url: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return ingest(repo_url)
        except GitIngestError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 3. Use Filtering Strategically
```python
# Always filter for large repos
summary, tree, content = ingest(
    repo_url,
    include_patterns=["*.py", "*.js"],
    exclude_patterns=["node_modules/*", "*.log"],
    max_file_size=51200
)
```

### 4. Handle Memory for Large Repos
```python
# Process in chunks
def process_large_repo(repo_url: str):
    summary, tree, content = ingest(repo_url)

    # Stream process files
    for file_content in split_content(content):
        yield process_file(file_content)
```

### 5. Cache Results
```python
import hashlib
import pickle

def cache_ingest(repo_url: str):
    cache_key = hashlib.md5(repo_url.encode()).hexdigest()
    cache_file = f"cache/{cache_key}.pkl"

    try:
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        result = ingest(repo_url)
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
        return result
```
