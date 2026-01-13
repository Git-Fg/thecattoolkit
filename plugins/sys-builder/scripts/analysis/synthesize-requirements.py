#!/usr/bin/env python3
"""
Synthesize Requirements

Combines user input with codebase analysis to create synthesized requirements.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def parse_user_requirements(requirements_text: str) -> Dict:
    """Parse user requirements into structured format."""
    requirements = {
        'original_text': requirements_text,
        'functional': [],
        'non_functional': [],
        'constraints': [],
        'goals': []
    }

    lines = requirements_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Categorize requirements
        line_lower = line.lower()

        if any(keyword in line_lower for keyword in
               ['should', 'must', 'need to', 'want to', 'create', 'build', 'add']):
            requirements['functional'].append(line)
        elif any(keyword in line_lower for keyword in
                 ['fast', 'secure', 'scalable', 'responsive', 'performant']):
            requirements['non_functional'].append(line)
        elif any(keyword in line_lower for keyword in
                 ['must use', 'must be', 'limited to', 'constrained']):
            requirements['constraints'].append(line)
        else:
            requirements['goals'].append(line)

    return requirements


def load_discovery_report(report_path: Path) -> Dict:
    """Load discovery report from file."""
    if not report_path.exists():
        return {}

    try:
        with open(report_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load discovery report: {e}")
        return {}


def map_to_existing_patterns(requirements: Dict, discovery: Dict) -> Dict:
    """Map requirements to existing codebase patterns."""
    mappings = {
        'aligned': [],  # Requirements that align with existing patterns
        'new': [],      # Requirements that need new implementation
        'conflicting': []  # Requirements that conflict with existing patterns
    }

    # Get existing frameworks
    existing_frameworks = discovery.get('frameworks', {})

    for req in requirements['functional']:
        req_lower = req.lower()

        # Check for alignment
        aligned = False

        if 'react' in req_lower and existing_frameworks.get('frontend') == 'React':
            mappings['aligned'].append(f"✓ {req} (aligns with existing React setup)")
            aligned = True
        elif 'express' in req_lower and existing_frameworks.get('backend') == 'Express.js':
            mappings['aligned'].append(f"✓ {req} (aligns with existing Express.js setup)")
            aligned = True
        elif 'django' in req_lower and existing_frameworks.get('backend') == 'Django':
            mappings['aligned'].append(f"✓ {req} (aligns with existing Django setup)")
            aligned = True

        if not aligned:
            mappings['new'].append(f"→ {req} (new implementation needed)")

    return mappings


def identify_gaps(requirements: Dict, discovery: Dict) -> List[str]:
    """Identify gaps between requirements and existing capabilities."""
    gaps = []

    # Get existing capabilities
    existing_langs = set(discovery.get('languages', {}).keys())
    existing_frameworks = set(discovery.get('frameworks', {}).values())
    existing_dbs = set(discovery.get('databases', []))

    # Check for gaps
    for req in requirements['functional']:
        req_lower = req.lower()

        # Authentication
        if 'auth' in req_lower or 'login' in req_lower:
            if 'authentication' not in str(existing_frameworks).lower():
                gaps.append("Authentication system needed")

        # API
        if 'api' in req_lower:
            if 'express' not in str(existing_frameworks).lower() and 'django' not in str(existing_frameworks).lower():
                gaps.append("API framework needed")

        # Database
        if 'database' in req_lower or 'data' in req_lower:
            if not existing_dbs:
                gaps.append("Database integration needed")

        # Frontend
        if 'ui' in req_lower or 'interface' in req_lower or 'component' in req_lower:
            if 'React' not in existing_frameworks and 'Vue' not in existing_frameworks:
                gaps.append("Frontend framework needed")

    return list(set(gaps))  # Remove duplicates


def synthesize_requirements(user_requirements: str, discovery_report: Path) -> Dict:
    """Synthesize user requirements with codebase discovery."""
    print(f"\n{'='*60}")
    print(f"Synthesizing Requirements")
    print(f"{'='*60}\n")

    # Parse user requirements
    print("1. Parsing user requirements...")
    requirements = parse_user_requirements(user_requirements)
    print(f"   Found {len(requirements['functional'])} functional requirements")
    print(f"   Found {len(requirements['non_functional'])} non-functional requirements")
    print(f"   Found {len(requirements['constraints'])} constraints")

    # Load discovery report
    print("\n2. Loading discovery report...")
    discovery = load_discovery_report(discovery_report)
    if discovery:
        print(f"   Loaded discovery for {discovery.get('project_root', 'unknown')}")
        print(f"   Detected: {', '.join(discovery.get('languages', {}).keys())}")
    else:
        print(f"   ⚠ No discovery report found")

    # Map to existing patterns
    print("\n3. Mapping to existing patterns...")
    mappings = map_to_existing_patterns(requirements, discovery)
    print(f"   Aligned: {len(mappings['aligned'])}")
    print(f"   New: {len(mappings['new'])}")

    # Identify gaps
    print("\n4. Identifying gaps...")
    gaps = identify_gaps(requirements, discovery)
    if gaps:
        for gap in gaps:
            print(f"   ⚠ {gap}")
    else:
        print(f"   ✓ No major gaps identified")

    # Synthesize
    synthesized = {
        'user_requirements': requirements,
        'discovery': discovery,
        'mappings': mappings,
        'gaps': gaps,
        'synthesis': {
            'aligned_count': len(mappings['aligned']),
            'new_count': len(mappings['new']),
            'gap_count': len(gaps),
            'recommendations': []
        }
    }

    # Generate recommendations
    print("\n5. Generating recommendations...")
    recommendations = []

    if mappings['aligned']:
        recommendations.append(
            "Leverage existing framework patterns for aligned requirements"
        )

    if mappings['new']:
        recommendations.append(
            "Plan new implementation for uncovered requirements"
        )

    if gaps:
        recommendations.append(
            "Address gaps through new dependencies or implementations"
        )

    # Add specific recommendations
    if discovery.get('frameworks'):
        recommendations.append(
            f"Continue using {', '.join(discovery['frameworks'].values())} "
            "for consistency"
        )

    synthesized['synthesis']['recommendations'] = recommendations

    for rec in recommendations:
        print(f"   → {rec}")

    print(f"\n{'='*60}")
    print("Synthesis complete")
    print(f"{'='*60}\n")

    return synthesized


def save_synthesis(synthesis: Dict, output_path: Path) -> None:
    """Save synthesis to file."""
    output_path.write_text(json.dumps(synthesis, indent=2))
    print(f"\n✅ Synthesis saved to: {output_path}")


def print_summary(synthesis: Dict) -> None:
    """Print a summary of the synthesis."""
    print(f"\n{'='*60}")
    print(f"Synthesis Summary")
    print(f"{'='*60}\n")

    print(f"Requirements:")
    print(f"  Functional: {len(synthesis['user_requirements']['functional'])}")
    print(f"  Non-Functional: {len(synthesis['user_requirements']['non_functional'])}")
    print(f"  Constraints: {len(synthesis['user_requirements']['constraints'])}")

    print(f"\nMappings:")
    print(f"  Aligned with existing: {synthesis['synthesis']['aligned_count']}")
    print(f"  Need new implementation: {synthesis['synthesis']['new_count']}")

    print(f"\nGaps: {synthesis['synthesis']['gap_count']}")

    print(f"\nRecommendations:")
    for rec in synthesis['synthesis']['recommendations']:
        print(f"  • {rec}")

    print(f"{'='*60}\n")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: synthesize-requirements.py <requirements-text> [discovery-report] [output-file]")
        print("\nExample:")
        print("  echo 'Create a React app with authentication' | python synthesize-requirements.py")
        sys.exit(1)

    requirements_text = sys.argv[1]
    discovery_report = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("discovery-report.json")
    output_file = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("requirements-synthesis.json")

    synthesis = synthesize_requirements(requirements_text, discovery_report)
    save_synthesis(synthesis, output_file)
    print_summary(synthesis)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Reading requirements from stdin...")
        requirements_text = sys.stdin.read()
        synthesis = synthesize_requirements(
            requirements_text,
            Path("discovery-report.json")
        )
        save_synthesis(synthesis, Path("requirements-synthesis.json"))
        print_summary(synthesis)
    else:
        main()
