#!/usr/bin/env python3
"""
Detect Patterns

Detects architectural and design patterns in codebase.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set


def detect_naming_conventions(root: Path) -> Dict[str, str]:
    """Detect naming conventions from files."""
    conventions = {
        'files': Counter(),
        'directories': Counter(),
        'classes': Counter(),
        'functions': Counter(),
        'variables': Counter()
    }

    # File naming
    for path in root.rglob('*.py'):
        name = path.name
        if '_' in name:
            conventions['files']['snake_case'] += 1
        elif '-' in name:
            conventions['files']['kebab-case'] += 1
        elif name[0].isupper():
            conventions['files']['PascalCase'] += 1

    for path in root.rglob('*.js'):
        name = path.name
        if '_' in name:
            conventions['files']['snake_case'] += 1
        elif '-' in name:
            conventions['files']['kebab-case'] += 1
        elif name[0].isupper():
            conventions['files']['PascalCase'] += 1
        else:
            conventions['files']['camelCase'] += 1

    # Directory naming
    for path in root.rglob('*'):
        if path.is_dir() and not path.name.startswith('.'):
            name = path.name
            if '_' in name:
                conventions['directories']['snake_case'] += 1
            elif '-' in name:
                conventions['directories']['kebab-case'] += 1
            elif name[0].isupper():
                conventions['directories']['PascalCase'] += 1

    return {k: v.most_common(1)[0][0] if v else 'unknown'
            for k, v in conventions.items()}


def detect_architectural_patterns(root: Path) -> Dict[str, List[str]]:
    """Detect architectural patterns."""
    patterns = {
        'mvc': [],
        'mvvm': [],
        'flux': [],
        'microservices': [],
        'monolith': [],
        'layered': []
    }

    # Check directory structure
    dirs = [p.name.lower() for p in root.rglob('*') if p.is_dir()]

    # MVC detection
    mvc_indicators = ['controller', 'view', 'model']
    if any(indicator in ' '.join(dirs) for indicator in mvc_indicators):
        patterns['mvc'].append("Directory structure indicates MVC")

    # Check file content
    for py_file in root.rglob('*.py'):
        try:
            content = py_file.read_text().lower()

            # MVC
            if 'class.*controller' in content or 'def.*controller' in content:
                patterns['mvc'].append(f"Controllers found in {py_file.relative_to(root)}")

            # Layered architecture
            if 'service layer' in content or 'business logic layer' in content:
                patterns['layered'].append(f"Layered architecture in {py_file.relative_to(root)}")

            # Microservices
            if 'docker-compose' in content or 'service discovery' in content:
                patterns['microservices'].append(f"Service pattern in {py_file.relative_to(root)}")

        except Exception:
            pass

    for js_file in root.rglob('*.js'):
        try:
            content = js_file.read_text().lower()

            # Flux/Redux
            if 'flux' in content or 'redux' in content:
                patterns['flux'].append(f"Flux pattern in {js_file.relative_to(root)}")

            # MVC
            if 'model.*view.*controller' in content or 'mvc' in content:
                patterns['mvc'].append(f"MVC in {js_file.relative_to(root)}")

        except Exception:
            pass

    return {k: v for k, v in patterns.items() if v}


def detect_design_patterns(root: Path) -> Dict[str, List[str]]:
    """Detect design patterns."""
    patterns = {
        'singleton': [],
        'factory': [],
        'observer': [],
        'decorator': [],
        'adapter': [],
        'strategy': []
    }

    # Check file content for patterns
    for py_file in root.rglob('*.py'):
        try:
            content = py_file.read_text()

            # Singleton
            if 'class.*singleton' in content.lower() or '_instance' in content:
                patterns['singleton'].append(f"{py_file.relative_to(root)}")

            # Factory
            if 'factory' in content.lower() or 'create_' in content:
                patterns['factory'].append(f"{py_file.relative_to(root)}")

            # Observer
            if 'observer' in content.lower() or 'subscribe' in content:
                patterns['observer'].append(f"{py_file.relative_to(root)}")

            # Decorator
            if '@' in content and 'decorator' in content.lower():
                patterns['decorator'].append(f"{py_file.relative_to(root)}")

        except Exception:
            pass

    for js_file in root.rglob('*.js'):
        try:
            content = js_file.read_text()

            # Observer
            if 'observer' in content.lower() or 'subscribe' in content:
                patterns['observer'].append(f"{js_file.relative_to(root)}")

            # Strategy
            if 'strategy' in content.lower() or 'strategy pattern' in content.lower():
                patterns['strategy'].append(f"{js_file.relative_to(root)}")

        except Exception:
            pass

    return {k: v for k, v in patterns.items() if v}


def detect_code_patterns(root: Path) -> Dict[str, any]:
    """Detect common code patterns."""
    patterns = {
        'testing': {},
        'error_handling': {},
        'async_patterns': {},
        'dependency_injection': {}
    }

    # Testing patterns
    test_indicators = Counter()
    for path in root.rglob('*'):
        if 'test' in path.name.lower() or 'spec' in path.name.lower():
            test_indicators['test_files'] += 1

        if path.suffix == '.py':
            try:
                content = path.read_text()
                if 'pytest' in content or 'unittest' in content:
                    test_indicators['pytest'] += 1
                elif 'testcase' in content.lower():
                    test_indicators['unittest'] += 1
            except Exception:
                pass

    patterns['testing'] = dict(test_indicators.most_common())

    # Error handling patterns
    error_patterns = Counter()
    for path in root.rglob('*.py'):
        try:
            content = path.read_text()
            if 'try:' in content and 'except' in content:
                error_patterns['try_except'] += 1
            if 'raise' in content:
                error_patterns['raise'] += 1
            if 'logging' in content:
                error_patterns['logging'] += 1
        except Exception:
            pass

    patterns['error_handling'] = dict(error_patterns.most_common())

    # Async patterns
    async_patterns = Counter()
    for path in root.rglob('*.py'):
        try:
            content = path.read_text()
            if 'async def' in content:
                async_patterns['async_def'] += 1
            if 'await' in content:
                async_patterns['await'] += 1
        except Exception:
            pass

    patterns['async_patterns'] = dict(async_patterns.most_common())

    return patterns


def generate_pattern_report(root: Path) -> Dict:
    """Generate a complete pattern detection report."""
    print(f"\n{'='*60}")
    print(f"Detecting Patterns: {root}")
    print(f"{'='*60}\n")

    report = {
        'naming_conventions': {},
        'architectural_patterns': {},
        'design_patterns': {},
        'code_patterns': {}
    }

    # Detect naming conventions
    print("1. Detecting naming conventions...")
    report['naming_conventions'] = detect_naming_conventions(root)
    for category, convention in report['naming_conventions'].items():
        print(f"   {category}: {convention}")

    # Detect architectural patterns
    print("\n2. Detecting architectural patterns...")
    report['architectural_patterns'] = detect_architectural_patterns(root)
    for pattern, instances in report['architectural_patterns'].items():
        print(f"   {pattern}: {len(instances)} instance(s)")

    # Detect design patterns
    print("\n3. Detecting design patterns...")
    report['design_patterns'] = detect_design_patterns(root)
    for pattern, instances in report['design_patterns'].items():
        print(f"   {pattern}: {len(instances)} instance(s)")

    # Detect code patterns
    print("\n4. Detecting code patterns...")
    report['code_patterns'] = detect_code_patterns(root)
    for category, patterns in report['code_patterns'].items():
        if patterns:
            print(f"   {category}:")
            for pattern, count in patterns.items():
                print(f"     {pattern}: {count}")

    print(f"\n{'='*60}")
    print("Pattern detection complete")
    print(f"{'='*60}\n")

    return report


def save_report(report: Dict, output_path: Path) -> None:
    """Save pattern report to file."""
    output_path.write_text(json.dumps(report, indent=2))
    print(f"\nGOOD Report saved to: {output_path}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: detect-patterns.py <project-root> [output-file]")
        print("\nExample:")
        print("  python detect-patterns.py . pattern-report.json")
        sys.exit(1)

    project_root = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "pattern-report.json"

    root = Path(project_root)
    report = generate_pattern_report(root)
    save_report(report, Path(output_file))

    print(f"\nPattern summary:")
    print(f"  Naming conventions: {len(report['naming_conventions'])} categories")
    print(f"  Architectural patterns: {len(report['architectural_patterns'])} types")
    print(f"  Design patterns: {len(report['design_patterns'])} types")
    print(f"  Code patterns: {len(report['code_patterns'])} categories")


if __name__ == "__main__":
    # Need to add json import
    import json

    main()
