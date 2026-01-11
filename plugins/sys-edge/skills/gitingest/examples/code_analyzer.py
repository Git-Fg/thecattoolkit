#!/usr/bin/env python3
"""
GitIngest Code Analyzer Example

Analyzes a repository and generates a comprehensive code quality report.
Includes metrics, complexity analysis, and recommendations.

Usage:
    python code_analyzer.py <repository-url>
"""

import sys
import re
from typing import Dict, List, Tuple
from collections import Counter
import argparse

try:
    from gitingest import ingest, ingest_async
    import asyncio
except ImportError:
    print("Error: gitingest package not installed.")
    print("Install with: pip install gitingest")
    sys.exit(1)


class CodeAnalyzer:
    """Comprehensive code analysis tool"""

    def __init__(self):
        self.metrics = {
            'total_files': 0,
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'languages': Counter(),
            'functions': 0,
            'classes': 0,
            'complexity_score': 0
        }

        self.issues = {
            'security': [],
            'performance': [],
            'maintainability': [],
            'best_practices': []
        }

    async def analyze_repository(self, repo_url: str) -> Dict:
        """Analyze repository and return comprehensive report"""
        print(f"Analyzing repository: {repo_url}")

        try:
            summary, tree, content = await ingest_async(repo_url)
        except Exception as e:
            return {
                'error': f"Failed to analyze repository: {str(e)}",
                'metrics': self.metrics,
                'issues': self.issues
            }

        # Parse repository info
        repo_info = self._parse_summary(summary)

        # Analyze code
        files = self._split_content(content)

        print(f"Processing {len(files)} files...")

        for file in files:
            self._analyze_file(file)

        # Calculate derived metrics
        self._calculate_complexity()

        # Generate recommendations
        recommendations = self._generate_recommendations()

        return {
            'repository': repo_info,
            'metrics': self.metrics,
            'issues': self.issues,
            'recommendations': recommendations
        }

    def _parse_summary(self, summary: str) -> Dict:
        """Parse repository summary"""
        info = {}
        for line in summary.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()
        return info

    def _split_content(self, content: str) -> List[Dict]:
        """Split content into individual files"""
        files = []
        current_file = None

        for line in content.split('\n'):
            if line.startswith('FILE: '):
                if current_file:
                    files.append(current_file)
                current_file = {
                    'path': line.replace('FILE: ', ''),
                    'content': [],
                    'language': self._detect_language(line.replace('FILE: ', ''))
                }
            elif current_file:
                current_file['content'].append(line)

        if current_file:
            files.append(current_file)

        return files

    def _detect_language(self, filepath: str) -> str:
        """Detect programming language from file extension"""
        ext = filepath.split('.')[-1].lower() if '.' in filepath else ''
        lang_map = {
            'py': 'Python',
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'java': 'Java',
            'cpp': 'C++',
            'c': 'C',
            'cs': 'C#',
            'go': 'Go',
            'rs': 'Rust',
            'php': 'PHP',
            'rb': 'Ruby',
            'swift': 'Swift',
            'kt': 'Kotlin',
            'scala': 'Scala'
        }
        return lang_map.get(ext, 'Unknown')

    def _analyze_file(self, file: Dict):
        """Analyze individual file"""
        self.metrics['total_files'] += 1
        self.metrics['languages'][file['language']] += 1

        content_lines = file['content']
        self.metrics['total_lines'] += len(content_lines)

        # Count line types
        for line in content_lines:
            stripped = line.strip()
            if not stripped:
                self.metrics['blank_lines'] += 1
            elif self._is_comment(line, file['language']):
                self.metrics['comment_lines'] += 1
            else:
                self.metrics['code_lines'] += 1

        # Analyze structure
        file_content = '\n'.join(content_lines)
        self._analyze_structure(file, file_content)

        # Security scan
        self._scan_security(file, file_content)

    def _is_comment(self, line: str, language: str) -> bool:
        """Check if line is a comment"""
        stripped = line.strip()

        comment_patterns = {
            'Python': stripped.startswith('#'),
            'JavaScript': stripped.startswith('//'),
            'TypeScript': stripped.startswith('//'),
            'Java': stripped.startswith('//'),
            'C++': stripped.startswith('//'),
            'C': stripped.startswith('//'),
            'C#': stripped.startswith('//'),
            'Go': stripped.startswith('//'),
            'Rust': stripped.startswith('//'),
            'PHP': stripped.startswith('//'),
        }

        return comment_patterns.get(language, False)

    def _analyze_structure(self, file: Dict, content: str):
        """Analyze file structure (functions, classes, etc.)"""
        # Detect functions
        function_patterns = {
            'Python': r'def\s+(\w+)\s*\(',
            'JavaScript': r'function\s+(\w+)\s*\(',
            'TypeScript': r'function\s+(\w+)\s*\(',
            'Java': r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\(',
            'C++': r'(?:[\w:]+\s+)?(\w+)\s*\([^)]*\)\s*{',
            'Go': r'func\s+(\w+)\s*\(',
            'Rust': r'fn\s+(\w+)\s*\(',
        }

        for lang, pattern in function_patterns.items():
            if file['language'] == lang:
                matches = re.findall(pattern, content)
                self.metrics['functions'] += len(matches)
                break

        # Detect classes
        class_patterns = {
            'Python': r'class\s+(\w+)',
            'JavaScript': r'class\s+(\w+)',
            'TypeScript': r'class\s+(\w+)',
            'Java': r'class\s+(\w+)',
            'C++': r'class\s+(\w+)',
            'C#': r'class\s+(\w+)',
            'Go': r'type\s+(\w+)\s+struct',
            'Rust': r'struct\s+(\w+)',
        }

        for lang, pattern in class_patterns.items():
            if file['language'] == lang:
                matches = re.findall(pattern, content)
                self.metrics['classes'] += len(matches)
                break

    def _scan_security(self, file: Dict, content: str):
        """Scan for security vulnerabilities"""
        security_patterns = [
            (r'eval\s*\(', 'critical', 'Use of eval()'),
            (r'exec\s*\(', 'critical', 'Use of exec()'),
            (r'os\.system\s*\(', 'high', 'System command execution'),
            (r'subprocess\.call\s*\(', 'high', 'Subprocess call'),
            (r'password\s*=\s*["\'][^"\']{8,}["\']', 'high', 'Hardcoded password'),
            (r'api[_-]?key\s*=\s*["\'][^"\']{20,}["\']', 'high', 'Hardcoded API key'),
            (r'sql\s*=\s*["\'].*%.*["\']', 'critical', 'SQL injection risk'),
            (r'input\s*\(', 'medium', 'Unvalidated input'),
            (r'raw_input\s*\(', 'medium', 'Unvalidated input'),
        ]

        for pattern, severity, description in security_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1

                self.issues['security'].append({
                    'file': file['path'],
                    'line': line_num,
                    'severity': severity,
                    'issue': description,
                    'match': match.group()
                })

    def _calculate_complexity(self):
        """Calculate code complexity score"""
        if self.metrics['code_lines'] == 0:
            self.metrics['complexity_score'] = 0
            return

        # Simple complexity metric: functions per 100 lines
        functions_per_100_lines = (self.metrics['functions'] / self.metrics['code_lines']) * 100

        # Average file size
        avg_file_size = self.metrics['total_lines'] / max(self.metrics['total_files'], 1)

        # Complexity score (0-100)
        self.metrics['complexity_score'] = min(
            100,
            (functions_per_100_lines * 2) + (avg_file_size / 10)
        )

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []

        # Test coverage
        test_ratio = self.metrics['comment_lines'] / max(self.metrics['total_lines'], 1)
        if test_ratio < 0.1:
            recommendations.append(
                "Low test coverage detected. Consider adding unit tests."
            )

        # Language distribution
        if self.metrics['languages']:
            primary_lang = self.metrics['languages'].most_common(1)[0]
            recommendations.append(
                f"Primary language: {primary_lang[0]} ({primary_lang[1]} files)"
            )

        # Complexity
        if self.metrics['complexity_score'] > 50:
            recommendations.append(
                "High complexity detected. Consider refactoring large functions."
            )

        # Security issues
        critical_issues = [i for i in self.issues['security'] if i['severity'] == 'critical']
        if critical_issues:
            recommendations.append(
                f"CRITICAL: {len(critical_issues)} security issues found. Review immediately."
            )

        # File organization
        if self.metrics['total_files'] > 100:
            recommendations.append(
                "Large codebase detected. Consider modular organization."
            )

        return recommendations

    def print_report(self, report: Dict):
        """Print formatted analysis report"""
        if 'error' in report:
            print(f"\n❌ Error: {report['error']}")
            return

        repo = report['repository']
        metrics = report['metrics']
        issues = report['issues']
        recommendations = report['recommendations']

        print("\n" + "=" * 70)
        print(f"  CODE ANALYSIS REPORT")
        print("=" * 70)

        print(f"\n📦 Repository: {repo.get('Repository', 'Unknown')}")
        print(f"📊 Files Analyzed: {repo.get('Files analyzed', 'Unknown')}")

        print("\n" + "-" * 70)
        print("  METRICS")
        print("-" * 70)

        print(f"  Total Files:        {metrics['total_files']}")
        print(f"  Total Lines:        {metrics['total_lines']:,}")
        print(f"  Code Lines:         {metrics['code_lines']:,}")
        print(f"  Comment Lines:      {metrics['comment_lines']:,}")
        print(f"  Blank Lines:        {metrics['blank_lines']:,}")
        print(f"  Functions:          {metrics['functions']}")
        print(f"  Classes:            {metrics['classes']}")
        print(f"  Complexity Score:   {metrics['complexity_score']:.1f}/100")

        print("\n  Language Distribution:")
        for lang, count in metrics['languages'].most_common(5):
            percentage = (count / metrics['total_files']) * 100
            print(f"    {lang:15} {count:4} files ({percentage:.1f}%)")

        print("\n" + "-" * 70)
        print("  SECURITY ISSUES")
        print("-" * 70)

        if not issues['security']:
            print("  ✅ No security issues detected")
        else:
            critical = [i for i in issues['security'] if i['severity'] == 'critical']
            high = [i for i in issues['security'] if i['severity'] == 'high']
            medium = [i for i in issues['security'] if i['severity'] == 'medium']

            if critical:
                print(f"\n  🔴 CRITICAL ({len(critical)}):")
                for issue in critical[:5]:
                    print(f"    {issue['file']}:{issue['line']} - {issue['issue']}")

            if high:
                print(f"\n  🟠 HIGH ({len(high)}):")
                for issue in high[:5]:
                    print(f"    {issue['file']}:{issue['line']} - {issue['issue']}")

            if medium:
                print(f"\n  🟡 MEDIUM ({len(medium)}):")
                for issue in medium[:5]:
                    print(f"    {issue['file']}:{issue['line']} - {issue['issue']}")

        print("\n" + "-" * 70)
        print("  RECOMMENDATIONS")
        print("-" * 70)

        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print("  ✅ No recommendations - code looks good!")

        print("\n" + "=" * 70 + "\n")


async def main():
    parser = argparse.ArgumentParser(
        description='Analyze Git repository code quality',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python code_analyzer.py https://github.com/octocat/Hello-World
  python code_analyzer.py https://github.com/user/private-repo
        """
    )

    parser.add_argument('repo_url', help='Repository URL to analyze')
    parser.add_argument(
        '--sync', action='store_true',
        help='Use synchronous mode (default is async)'
    )

    args = parser.parse_args()

    analyzer = CodeAnalyzer()

    if args.sync:
        # Synchronous mode
        summary, tree, content = ingest(args.repo_url)
        # Simple synchronous analysis
        print("Synchronous mode - basic analysis only")
        print(f"Repository: {summary.split(chr(10))[0]}")
    else:
        # Asynchronous mode (full analysis)
        report = await analyzer.analyze_repository(args.repo_url)
        analyzer.print_report(report)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        sys.exit(1)
