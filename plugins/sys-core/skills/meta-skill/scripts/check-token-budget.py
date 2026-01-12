#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""
Check token budget for all skills in a plugin or directory.

Usage:
    uv run scripts/check-token-budget.py <root-directory>
"""

import sys
import os
import re
import yaml

TOKEN_BUDGET_LIMIT = 15000  # characters

def extract_descriptions(root_dir):
    """Extract all descriptions from skill files"""
    descriptions = []
    total_chars = 0

    # Find all SKILL.md files
    for root, dirs, files in os.walk(root_dir):
        if 'SKILL.md' in files:
            skill_dir = root
            skill_name = os.path.basename(skill_dir)

            try:
                with open(f'{skill_dir}/SKILL.md', 'r') as f:
                    content = f.read()

                # Extract frontmatter
                frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
                if frontmatter_match:
                    try:
                        frontmatter = yaml.safe_load(frontmatter_match.group(1))
                        if 'description' in frontmatter:
                            description = frontmatter['description']
                            desc_length = len(description)
                            total_chars += desc_length

                            descriptions.append({
                                'skill': skill_name,
                                'description': description,
                                'length': desc_length
                            })
                    except yaml.YAMLError:
                        print(f"Warning: Invalid YAML in {skill_dir}/SKILL.md")

            except FileNotFoundError:
                continue

    return descriptions, total_chars

def check_token_budget(root_dir):
    """Check token budget for all skills"""
    descriptions, total_chars = extract_descriptions(root_dir)

    print(f"\n{'='*70}")
    print(f"Token Budget Analysis")
    print(f"{'='*70}\n")

    if not descriptions:
        print("No skills found with descriptions")
        return

    print(f"Total Skills: {len(descriptions)}")
    print(f"Total Characters: {total_chars:,}")
    print(f"Budget Limit: {TOKEN_BUDGET_LIMIT:,}")
    print(f"Remaining: {TOKEN_BUDGET_LIMIT - total_chars:,}")
    print(f"Usage: {(total_chars / TOKEN_BUDGET_LIMIT * 100):.1f}%\n")

    # Check if over budget
    if total_chars > TOKEN_BUDGET_LIMIT:
        print(f"❌ OVER BUDGET by {total_chars - TOKEN_BUDGET_LIMIT:,} characters!")
    elif total_chars > TOKEN_BUDGET_LIMIT * 0.9:
        print(f"⚠️  WARNING: Over 90% of budget used")
    else:
        print(f"✅ Within budget\n")

    # Individual skill breakdown
    print(f"{'='*70}")
    print(f"Individual Skill Breakdown")
    print(f"{'='*70}\n")

    descriptions.sort(key=lambda x: x['length'], reverse=True)

    for item in descriptions:
        status = "⚠️" if item['length'] > 500 else "✓"
        print(f"{status} {item['skill']:30s} {item['length']:6d} chars")

    # Suggestions for optimization
    print(f"\n{'='*70}")
    print(f"Optimization Suggestions")
    print(f"{'='*70}\n")

    if total_chars > TOKEN_BUDGET_LIMIT:
        print("To reduce token usage:")
        print("1. Shorten descriptions (aim for <200 chars each)")
        print("2. Consolidate similar skills")
        print("3. Use progressive disclosure for detailed content")
        print("4. Remove redundant words and phrases\n")

    if descriptions:
        avg_length = total_chars / len(descriptions)
        print(f"Average description length: {avg_length:.0f} chars")

        long_descriptions = [d for d in descriptions if d['length'] > 500]
        if long_descriptions:
            print(f"\nSkills with long descriptions (>500 chars):")
            for item in long_descriptions:
                print(f"  - {item['skill']}: {item['length']} chars")

        short_descriptions = [d for d in descriptions if d['length'] < 50]
        if short_descriptions:
            print(f"\nSkills with short descriptions (<50 chars):")
            for item in short_descriptions:
                print(f"  - {item['skill']}: {item['length']} chars")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check-token-budget.py <root-directory>")
        print("\nExample:")
        print("  python check-token-budget.py ./plugins/my-plugin/")
        print("  python check-token-budget.py ./plugins/")
        sys.exit(1)

    root_dir = sys.argv[1]
    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' not found")
        sys.exit(1)

    check_token_budget(root_dir)
