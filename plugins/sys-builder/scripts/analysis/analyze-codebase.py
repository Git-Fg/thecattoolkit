#!/usr/bin/env python3
"""
Analyze Codebase

Auto-discovers project structure and technology stack.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set


def count_files(root: Path) -> int:
    """Count total files in directory."""
    count = 0
    for path in root.rglob('*'):
        if path.is_file() and not path.name.startswith('.'):
            count += 1
    return count


def find_config_files(root: Path) -> Dict[str, List[Path]]:
    """Find configuration files."""
    configs = {
        'package.json': [],
        'requirements.txt': [],
        'pyproject.toml': [],
        'Cargo.toml': [],
        'go.mod': [],
        'pom.xml': [],
        'build.gradle': [],
        'composer.json': [],
        'Dockerfile': [],
        'docker-compose.yml': [],
        '.env': [],
        '.env.example': [],
        'Makefile': [],
    }

    for config in configs.keys():
        configs[config] = list(root.glob(f'**/{config}'))
        configs[config] += list(root.glob(config))

    return configs


def detect_languages(root: Path) -> Dict[str, int]:
    """Detect programming languages by file extension."""
    lang_counts = Counter()
    extensions = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React',
        '.tsx': 'React',
        '.java': 'Java',
        '.go': 'Go',
        '.rs': 'Rust',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.cpp': 'C++',
        '.c': 'C',
        '.h': 'C',
        '.cs': 'C#',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
    }

    for ext, lang in extensions.items():
        count = len(list(root.glob(f'**/*{ext}')))
        if count > 0:
            lang_counts[lang] = count

    return dict(lang_counts)


def detect_frameworks(configs: Dict[str, List[Path]]) -> Dict[str, str]:
    """Detect frameworks from configuration files."""
    frameworks = {}

    # Check package.json
    for pkg_file in configs['package.json']:
        try:
            with open(pkg_file) as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

                # Frontend frameworks
                if 'react' in deps:
                    frameworks['frontend'] = 'React'
                elif 'vue' in deps:
                    frameworks['frontend'] = 'Vue.js'
                elif '@angular/core' in deps:
                    frameworks['frontend'] = 'Angular'

                # Backend frameworks
                if 'express' in deps:
                    frameworks['backend'] = 'Express.js'
                elif 'next' in deps:
                    frameworks['framework'] = 'Next.js'
                elif 'nest' in deps:
                    frameworks['backend'] = 'NestJS'

                # Build tools
                if 'vite' in deps:
                    frameworks['build'] = 'Vite'
                elif 'webpack' in deps:
                    frameworks['build'] = 'Webpack'

        except Exception:
            pass

    # Check Python files
    if configs['requirements.txt'] or configs['pyproject.toml']:
        frameworks['backend'] = 'Python'

        try:
            # Check for Django
            req_file = configs['requirements.txt'][0] if configs['requirements.txt'] else None
            if req_file:
                content = req_file.read_text().lower()
                if 'django' in content:
                    frameworks['backend'] = 'Django'
                elif 'flask' in content:
                    frameworks['backend'] = 'Flask'
                elif 'fastapi' in content:
                    frameworks['backend'] = 'FastAPI'
        except Exception:
            pass

    # Check Go
    if configs['go.mod']:
        frameworks['backend'] = 'Go'

    # Check Rust
    if configs['Cargo.toml']:
        frameworks['backend'] = 'Rust'

    # Check Java
    if configs['pom.xml'] or configs['build.gradle']:
        frameworks['backend'] = 'Java'

    return frameworks


def detect_databases(configs: Dict[str, List[Path]]) -> List[str]:
    """Detect databases from configuration files."""
    databases = []

    # Check package.json
    for pkg_file in configs['package.json']:
        try:
            with open(pkg_file) as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

                if 'mongoose' in deps:
                    databases.append('MongoDB')
                if 'sequelize' in deps or 'prisma' in deps:
                    databases.append('PostgreSQL')
                if 'redis' in deps:
                    databases.append('Redis')

        except Exception:
            pass

    # Check Python requirements
    req_file = configs['requirements.txt'][0] if configs['requirements.txt'] else None
    if req_file:
        try:
            content = req_file.read_text().lower()
            if 'django' in content or 'postgresql' in content:
                databases.append('PostgreSQL')
            if 'redis' in content:
                databases.append('Redis')
            if 'pymongo' in content or 'motor' in content:
                databases.append('MongoDB')
        except Exception:
            pass

    return list(set(databases))


def detect_testing(configs: Dict[str, List[Path]]) -> Dict[str, str]:
    """Detect testing frameworks."""
    tests = {}

    # Check package.json
    for pkg_file in configs['package.json']:
        try:
            with open(pkg_file) as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

                if 'jest' in deps:
                    tests['javascript'] = 'Jest'
                elif 'mocha' in deps:
                    tests['javascript'] = 'Mocha'

        except Exception:
            pass

    # Check for test files
    root = configs['package.json'][0].parent if configs['package.json'] else Path.cwd()

    test_patterns = ['test', 'tests', '__tests__', 'spec', 'specs']
    test_files = []
    for pattern in test_patterns:
        test_files.extend(list(root.glob(f'**/{pattern}/**/*.js')))
        test_files.extend(list(root.glob(f'**/*.{pattern}.js')))

    if test_files:
        tests['test_files'] = f"{len(test_files)} test files found"

    return tests


def analyze_directory_structure(root: Path) -> Dict:
    """Analyze directory structure."""
    structure = {
        'total_files': 0,
        'total_dirs': 0,
        'max_depth': 0,
        'top_dirs': [],
    }

    dirs = []
    for path in root.rglob('*'):
        if path.is_dir() and not path.name.startswith('.'):
            dirs.append(path)

    structure['total_dirs'] = len(dirs)

    # Calculate depth
    max_depth = 0
    for path in dirs:
        depth = len(path.relative_to(root).parts)
        max_depth = max(max_depth, depth)

    structure['max_depth'] = max_depth

    # Top level directories
    top_level = [d for d in root.iterdir() if d.is_dir() and not d.name.startswith('.')]
    structure['top_dirs'] = [d.name for d in sorted(top_level)]

    # Count files
    structure['total_files'] = count_files(root)

    return structure


def generate_discovery_report(project_root: str) -> Dict:
    """Generate a complete discovery report."""
    root = Path(project_root)

    print(f"\n{'='*60}")
    print(f"Analyzing Codebase: {root}")
    print(f"{'='*60}\n")

    report = {
        'project_root': str(root),
        'analysis_date': str(Path(__file__).stat().st_mtime),
        'languages': {},
        'frameworks': {},
        'databases': [],
        'testing': {},
        'structure': {},
        'config_files': {},
    }

    # Analyze structure
    print("1. Analyzing directory structure...")
    report['structure'] = analyze_directory_structure(root)
    print(f"   Found {report['structure']['total_files']} files")
    print(f"   Found {report['structure']['total_dirs']} directories")
    print(f"   Max depth: {report['structure']['max_depth']}")

    # Find config files
    print("\n2. Finding configuration files...")
    configs = find_config_files(root)
    report['config_files'] = {k: len(v) for k, v in configs.items()}
    for config, files in configs.items():
        if files:
            print(f"   {config}: {len(files)} file(s)")

    # Detect languages
    print("\n3. Detecting languages...")
    report['languages'] = detect_languages(root)
    for lang, count in report['languages'].items():
        print(f"   {lang}: {count} files")

    # Detect frameworks
    print("\n4. Detecting frameworks...")
    report['frameworks'] = detect_frameworks(configs)
    for category, framework in report['frameworks'].items():
        print(f"   {category}: {framework}")

    # Detect databases
    print("\n5. Detecting databases...")
    report['databases'] = detect_databases(configs)
    for db in report['databases']:
        print(f"   {db}")

    # Detect testing
    print("\n6. Detecting testing frameworks...")
    report['testing'] = detect_testing(configs)
    for category, framework in report['testing'].items():
        print(f"   {category}: {framework}")

    print(f"\n{'='*60}")
    print("Analysis complete")
    print(f"{'='*60}\n")

    return report


def save_report(report: Dict, output_path: Path) -> None:
    """Save discovery report to file."""
    output_path.write_text(json.dumps(report, indent=2))
    print(f"\nGOOD Report saved to: {output_path}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: analyze-codebase.py <project-root> [output-file]")
        print("\nExample:")
        print("  python analyze-codebase.py . discovery-report.json")
        sys.exit(1)

    project_root = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "discovery-report.json"

    report = generate_discovery_report(project_root)
    save_report(report, Path(output_file))

    print(f"\nReport summary:")
    print(f"  Languages: {', '.join(report['languages'].keys())}")
    print(f"  Frameworks: {', '.join(report['frameworks'].values())}")
    print(f"  Databases: {', '.join(report['databases']) if report['databases'] else 'None detected'}")


if __name__ == "__main__":
    main()
