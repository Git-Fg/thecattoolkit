#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
#     "ruamel.yaml",
# ]
# ///

"""
Cat Toolkit Plugin Analyzer & Validator
CLI entry point for the Flat Module refactored toolkit.
"""

import sys
import json
import argparse
from pathlib import Path

# Local imports (same directory)
from validators import ToolkitAnalyzer
from fixers import ComponentFixer, MarketplaceSyncer


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Cat Toolkit Plugin Analyzer & Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--root-dir",
        help="Root directory of the project (default: current directory or parent of scripts/)",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Automatically fix linting errors"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )

    args = parser.parse_args()

    # Logic to determine root dir
    if args.root_dir:
        root_dir = args.root_dir
    else:
        # Default behavior:
        # 1. If cwd has 'plugins' dir, use cwd
        # 2. If cwd IS 'plugins' dir, use cwd
        # 3. Else fallback to script location parent
        cwd = Path.cwd()
        if (cwd / "plugins").is_dir() or cwd.name == "plugins":
            root_dir = str(cwd)
        else:
            # Fallback to parent of script dir (assuming script is in scripts/)
            root_dir = str(Path(__file__).parent.parent)

    root_path = Path(root_dir)

    if args.fix:
        # Run the fixer
        analyzer = ToolkitAnalyzer(root_dir)
        analyzer._discover_and_parse()

        print("\n" + "=" * 70)
        print("STEP 1: Component Fixes (Markdown & YAML)")
        print("=" * 70 + "\n")

        fixer = ComponentFixer(analyzer.plugins_dir, dry_run=args.dry_run)
        component_results = fixer.fix_all()

        # Check if marketplace.json exists
        marketplace_path = root_path / ".claude-plugin" / "marketplace.json"
        sync_results = {"errors": []}  # Initialize to avoid undefined variable

        if marketplace_path.exists():
            print("\n" + "=" * 70)
            print("STEP 2: Marketplace Synchronization (JSON)")
            print("=" * 70 + "\n")

            syncer = MarketplaceSyncer(
                analyzer.plugins_dir, marketplace_path, dry_run=args.dry_run
            )
            sync_results = syncer.sync_all()

        # Run full validation including claude plugin validate
        print("\n" + "=" * 70)
        print("STEP 3: Full Validation (Including Claude Plugin Validate)")
        print("=" * 70 + "\n")

        report = analyzer.validate_all()

        # Exit with appropriate code
        if args.json:
            # Output JSON
            output = {
                "timestamp": report.timestamp,
                "validators_run": report.validators_run,
                "total_errors": report.total_errors,
                "total_warnings": report.total_warnings,
                "all_passed": report.all_passed,
                "results": [],
            }

            for result in report.results:
                output["results"].append(
                    {
                        "name": result.name,
                        "passed": result.passed,
                        "errors": result.errors,
                        "warnings": result.warnings,
                        "info": result.info,
                    }
                )

            print(json.dumps(output, indent=2))

        # Exit with appropriate code
        has_errors = (
            any(r.errors for r in component_results)
            or sync_results.get("errors", [])
            or not report.all_passed
        )
        sys.exit(1 if has_errors else 0)
    else:
        # Run validation
        analyzer = ToolkitAnalyzer(root_dir)
        report = analyzer.validate_all()

    if args.json:
        # Output JSON
        output = {
            "timestamp": report.timestamp,
            "validators_run": report.validators_run,
            "total_errors": report.total_errors,
            "total_warnings": report.total_warnings,
            "all_passed": report.all_passed,
            "results": [],
        }

        for result in report.results:
            output["results"].append(
                {
                    "name": result.name,
                    "passed": result.passed,
                    "errors": result.errors,
                    "warnings": result.warnings,
                    "info": result.info,
                }
            )

        print(json.dumps(output, indent=2))

    # Exit with appropriate code
    sys.exit(0 if report.all_passed else 1)


if __name__ == "__main__":
    main()
