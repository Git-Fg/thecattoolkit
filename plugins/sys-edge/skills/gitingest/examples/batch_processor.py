#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "gitingest",
#     "asyncio",
# ]
# ///

"""
Batch Repository Processor

Analyzes multiple repositories concurrently and generates a comparative report.
Perfect for auditing multiple projects or comparing codebases.

Usage:
    python batch_processor.py repo1.txt repo2.txt repo3.txt
    # Where repo1.txt contains repository URLs (one per line)

Or:
    python batch_processor.py https://github.com/user/repo1 https://github.com/user/repo2
"""

import sys
import asyncio
import json
from typing import List, Dict
from collections import Counter
import argparse

try:
    from gitingest import ingest_async
except ImportError:
    print("Error: gitingest package not installed.")
    print("Install with: pip install gitingest")
    sys.exit(1)


class BatchProcessor:
    """Process multiple repositories and generate comparative report"""

    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.results = []

    async def process_repositories(self, repo_urls: List[str]) -> List[Dict]:
        """Process multiple repositories concurrently"""
        print(f"Processing {len(repo_urls)} repositories...")
        print(f"Max concurrent: {self.max_concurrent}")

        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def process_single(url: str):
            async with semaphore:
                try:
                    print(f"  → Fetching: {url}")
                    summary, tree, content = await ingest_async(url)

                    print(f"  ✓ Analyzed: {url}")
                    return self._analyze_repository(url, summary, tree, content)

                except Exception as e:
                    print(f"  ✗ Failed: {url} - {e}")
                    return {
                        'url': url,
                        'status': 'error',
                        'error': str(e),
                        'metrics': {}
                    }

        # Execute all tasks
        tasks = [process_single(url) for url in repo_urls]
        results = await asyncio.gather(*tasks)

        return results

    def _analyze_repository(self, url: str, summary: str, tree: str, content: str) -> Dict:
        """Analyze single repository"""
        # Parse summary
        repo_info = self._parse_summary(summary)

        # Analyze code
        files = self._split_content(content)
        metrics = self._calculate_metrics(files)

        return {
            'url': url,
            'status': 'success',
            'repository': repo_info,
            'metrics': metrics
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
                    'content': []
                }
            elif current_file:
                current_file['content'].append(line)

        if current_file:
            files.append(current_file)

        return files

    def _calculate_metrics(self, files: List[Dict]) -> Dict:
        """Calculate repository metrics"""
        metrics = {
            'total_files': len(files),
            'total_lines': 0,
            'code_lines': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'languages': Counter(),
            'functions': 0,
            'classes': 0,
            'has_tests': False,
            'has_docs': False,
            'has_config': False,
            'largest_file': {'path': '', 'lines': 0}
        }

        for file in files:
            path = file['path']
            content_lines = file['content']
            line_count = len(content_lines)

            metrics['total_lines'] += line_count

            # Track largest file
            if line_count > metrics['largest_file']['lines']:
                metrics['largest_file'] = {'path': path, 'lines': line_count}

            # Detect special directories
            if 'test' in path.lower():
                metrics['has_tests'] = True
            if any(doc in path.lower() for doc in ['readme', 'doc', 'docs']):
                metrics['has_docs'] = True
            if path.endswith(('.json', '.yaml', '.yml', '.toml', '.cfg', '.ini')):
                metrics['has_config'] = True

            # Count line types
            for line in content_lines:
                stripped = line.strip()
                if not stripped:
                    metrics['blank_lines'] += 1
                elif stripped.startswith(('#', '//', '/*', '*')):
                    metrics['comment_lines'] += 1
                else:
                    metrics['code_lines'] += 1

            # Detect language
            ext = path.split('.')[-1] if '.' in path else ''
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
                'kt': 'Kotlin'
            }
            if ext in lang_map:
                metrics['languages'][lang_map[ext]] += 1

            # Count functions and classes
            file_content = '\n'.join(content_lines)

            # Simple function detection
            if ext == 'py':
                metrics['functions'] += len([m for m in re.finditer(r'def\s+\w+', file_content)])
                metrics['classes'] += len([m for m in re.finditer(r'class\s+\w+', file_content)])
            elif ext in ['js', 'ts']:
                metrics['functions'] += len([m for m in re.finditer(r'function\s+\w+|const\s+\w+\s*=', file_content)])
                metrics['classes'] += len([m for m in re.finditer(r'class\s+\w+', file_content)])

        return metrics

    def generate_comparative_report(self, results: List[Dict]) -> str:
        """Generate comparative analysis report"""
        # Filter successful results
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'error']

        # Calculate aggregate statistics
        total_files = sum(r['metrics']['total_files'] for r in successful)
        total_lines = sum(r['metrics']['total_lines'] for r in successful)
        total_code_lines = sum(r['metrics']['code_lines'] for r in successful)

        # Aggregate languages
        all_languages = Counter()
        for result in successful:
            all_languages.update(result['metrics']['languages'])

        # Generate report
        report = f"""# Batch Repository Analysis Report

## Summary
- **Total Repositories**: {len(results)}
- **Successful**: {len(successful)}
- **Failed**: {len(failed)}
- **Total Files**: {total_files:,}
- **Total Lines**: {total_lines:,}
- **Total Code Lines**: {total_code_lines:,}

## Repository Details

"""

        # Add each repository
        for result in successful:
            metrics = result['metrics']
            repo_info = result['repository']

            report += f"""### {result['url']}

**Repository**: {repo_info.get('Repository', 'Unknown')}
**Files**: {metrics['total_files']} | **Lines**: {metrics['total_lines']:,} | **Code**: {metrics['code_lines']:,}

- **Languages**: {', '.join(metrics['languages'].keys())}
- **Functions**: {metrics['functions']}
- **Classes**: {metrics['classes']}
- **Largest File**: {metrics['largest_file']['path']} ({metrics['largest_file']['lines']} lines)
- **Features**:
  - Tests: {'✓' if metrics['has_tests'] else '✗'}
  - Docs: {'✓' if metrics['has_docs'] else '✗'}
  - Config: {'✓' if metrics['has_config'] else '✗'}

"""

        # Failed repositories
        if failed:
            report += "## Failed Repositories\n\n"
            for result in failed:
                report += f"- **{result['url']}**: {result.get('error', 'Unknown error')}\n"
            report += "\n"

        # Language distribution
        report += "## Language Distribution (All Repositories)\n\n"
        for lang, count in all_languages.most_common(10):
            report += f"- **{lang}**: {count} files\n"

        # Comparative statistics
        if len(successful) > 1:
            report += "\n## Comparative Statistics\n\n"

            avg_files = total_files / len(successful)
            avg_lines = total_lines / len(successful)
            avg_code = total_code_lines / len(successful)

            largest_repo = max(successful, key=lambda r: r['metrics']['total_lines'])
            smallest_repo = min(successful, key=lambda r: r['metrics']['total_lines'])

            report += f"""### Averages
- **Files per repository**: {avg_files:.1f}
- **Lines per repository**: {avg_lines:,.0f}
- **Code lines per repository**: {avg_code:,.0f}

### Extremes
- **Largest**: {largest_repo['url']} ({largest_repo['metrics']['total_lines']:,} lines)
- **Smallest**: {smallest_repo['url']} ({smallest_repo['metrics']['total_lines']:,} lines)

### Features Comparison
"""

            test_count = sum(1 for r in successful if r['metrics']['has_tests'])
            docs_count = sum(1 for r in successful if r['metrics']['has_docs'])
            config_count = sum(1 for r in successful if r['metrics']['has_config'])

            report += f"- **Repositories with tests**: {test_count}/{len(successful)} ({test_count/len(successful)*100:.1f}%)\n"
            report += f"- **Repositories with docs**: {docs_count}/{len(successful)} ({docs_count/len(successful)*100:.1f}%)\n"
            report += f"- **Repositories with config**: {config_count}/{len(successful)} ({config_count/len(successful)*100:.1f}%)\n"

        report += f"""
---
*Generated by GitIngest Batch Processor*
*Analysis Date: {asyncio.get_event_loop().time()}*
"""

        return report

    def export_json(self, results: List[Dict], filename: str = 'batch-analysis.json'):
        """Export results to JSON"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✅ JSON export saved to {filename}")


def load_repositories_from_file(filename: str) -> List[str]:
    """Load repository URLs from file (one per line)"""
    with open(filename, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return urls


async def main():
    parser = argparse.ArgumentParser(
        description='Batch process multiple Git repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process multiple repos from command line
  python batch_processor.py https://github.com/user/repo1 https://github.com/user/repo2

  # Process repos from file
  python batch_processor.py repos.txt

  # Control concurrency
  python batch_processor.py repos.txt --concurrency 10
        """
    )

    parser.add_argument(
        'repos',
        nargs='+',
        help='Repository URLs or file containing URLs (one per line)'
    )
    parser.add_argument(
        '--concurrency',
        type=int,
        default=5,
        help='Maximum concurrent repository processing (default: 5)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Also export results to JSON'
    )

    args = parser.parse_args()

    # Load repositories
    repo_urls = []
    for arg in args.repos:
        if arg.endswith('.txt'):
            print(f"Loading repositories from {arg}...")
            urls = load_repositories_from_file(arg)
            repo_urls.extend(urls)
        else:
            repo_urls.append(arg)

    if not repo_urls:
        print("Error: No repositories to process")
        sys.exit(1)

    # Process repositories
    processor = BatchProcessor(max_concurrent=args.concurrency)
    results = await processor.process_repositories(repo_urls)

    # Generate report
    report = processor.generate_comparative_report(results)

    # Save report
    report_file = 'batch-analysis-report.md'
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"\n✅ Report saved to {report_file}")

    # Export JSON if requested
    if args.json:
        processor.export_json(results)

    # Print summary
    successful = len([r for r in results if r['status'] == 'success'])
    failed = len(results) - successful

    print(f"\n{'='*70}")
    print(f"  BATCH PROCESSING COMPLETE")
    print(f"{'='*70}")
    print(f"  Total: {len(results)} repositories")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nBatch processing interrupted by user")
        sys.exit(1)
