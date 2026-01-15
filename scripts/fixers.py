"""
Auto-fix and marketplace synchronization logic for the Cat Toolkit analyzer.
All write/modification operations are contained in this module.
"""

import io
import json
import re
import shutil
import yaml
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ruamel.yaml.scalarstring import DoubleQuotedScalarString

# Local imports (same directory)
from common import (
    FixResult,
    NAME_PATTERN,
    MAX_DESCRIPTION_LENGTH,
    normalize_name,
    clean_description_text,
    normalize_tool_syntax,
    ALLOWED_FIELDS_SKILL,
    filter_excluded_paths,
    _ruamel_yaml,
)


class ComponentFixer:
    """Handles auto-fixing of component files."""

    def __init__(self, plugins_dir: Path, dry_run: bool = False):
        self.plugins_dir = plugins_dir
        self.dry_run = dry_run
        self.results: List[FixResult] = []

    def fix_all(self) -> List[FixResult]:
        """Fix all component files."""
        print("=" * 70)
        print("🛠️  Cat Toolkit Auto-Fixer")
        print(f"Mode: {'DRY RUN (no changes)' if self.dry_run else 'LIVE'}")
        print(f"Scanning: {self.plugins_dir}")
        print("=" * 70)
        print()

        # Fix skills
        skill_files = list(self.plugins_dir.rglob("SKILL.md")) + list(
            self.plugins_dir.rglob("skill.md")
        )
        skill_files = filter_excluded_paths(list(set(skill_files)))
        print(f"Phase 1: Fixing {len(skill_files)} skills...")
        for skill_file in skill_files:
            result = self.fix_component_file(skill_file, "skill")
            self.results.append(result)

        # Fix agents
        agent_files = filter_excluded_paths(list(self.plugins_dir.rglob("agents/*.md")))
        print(f"Phase 2: Fixing {len(agent_files)} agents...")
        for agent_file in agent_files:
            result = self.fix_component_file(agent_file, "agent")
            self.results.append(result)

        # Fix commands
        command_files = filter_excluded_paths(
            list(self.plugins_dir.rglob("commands/*.md"))
        )
        print(f"Phase 3: Fixing {len(command_files)} commands...")
        for cmd_file in command_files:
            result = self.fix_component_file(cmd_file, "command")
            self.results.append(result)

        # Directory-name synchronization for skills
        print("Phase 4: Checking directory-name synchronization...")
        self.fix_directory_name_sync()

        self.print_summary()
        return self.results

    def fix_component_file(self, file_path: Path, comp_type: str) -> FixResult:
        """Fix a single component file."""
        result = FixResult(file_path=str(file_path), fixed=False)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                full_content = f.read()

            # Split into frontmatter and body
            if not full_content.startswith("---"):
                return result

            parts = full_content.split("---", 2)
            if len(parts) < 3:
                return result

            fm_raw = parts[1]
            body = parts[2]

            # Parse YAML with ruamel for round-trip
            try:
                data = _ruamel_yaml.load(fm_raw)
                if not isinstance(data, dict):
                    return result
            except Exception as e:
                result.errors.append(f"YAML parse error: {e}")
                return result

            changes_made = []

            # --- Fix 1: Sanitize Description ---
            if "description" in data:
                original_desc = str(data["description"])
                cleaned = clean_description_text(original_desc)

                if cleaned != original_desc:
                    data["description"] = DoubleQuotedScalarString(cleaned)
                    changes_made.append(
                        "Sanitized description (removed newlines/special chars)"
                    )

            # --- Fix 2: Normalize Name ---
            if "name" in data:
                original_name = str(data["name"])
                normalized = normalize_name(original_name)
                if normalized != original_name:
                    data["name"] = normalized
                    changes_made.append(
                        f"Normalized name: {original_name} -> {normalized}"
                    )

            # --- Fix 3: Tool Syntax Normalization ---
            tools_field = (
                "allowed-tools" if comp_type in ["skill", "command"] else "tools"
            )
            if tools_field in data:
                tools = data[tools_field]
                if isinstance(tools, list):
                    normalized_tools = normalize_tool_syntax(tools)
                    if normalized_tools != tools:
                        data[tools_field] = normalized_tools
                        changes_made.append(f"Normalized tool syntax in {tools_field}")

            # --- Fix 4: Ensure description is double-quoted ---
            if "description" in data and not isinstance(
                data["description"], DoubleQuotedScalarString
            ):
                data["description"] = DoubleQuotedScalarString(str(data["description"]))
                changes_made.append("Enforced double-quoted description")

            if changes_made:
                result.changes = changes_made
                result.fixed = True

                if not self.dry_run:
                    # Write back
                    stream = io.StringIO()
                    _ruamel_yaml.dump(data, stream)
                    new_fm = stream.getvalue()

                    # Reconstruct file
                    new_content = f"---\n{new_fm}---{body}"
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)

        except Exception as e:
            result.errors.append(f"Error: {e}")

        return result

    def fix_directory_name_sync(self) -> None:
        """Check and optionally fix directory-name mismatches for skills."""
        skills_dirs = filter_excluded_paths(list(self.plugins_dir.rglob("skills/*")))

        for skill_dir in skills_dirs:
            if not skill_dir.is_dir():
                continue

            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                skill_file = skill_dir / "skill.md"
            if not skill_file.exists():
                continue

            try:
                content = skill_file.read_text()
                if not content.startswith("---"):
                    continue

                end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                if not end_match:
                    continue

                fm_text = content[3 : 3 + end_match.start()]
                frontmatter = yaml.safe_load(fm_text)

                if not isinstance(frontmatter, dict):
                    continue

                yaml_name = frontmatter.get("name", "")
                dir_name = skill_dir.name

                if yaml_name and yaml_name != dir_name:
                    result = FixResult(
                        file_path=str(skill_dir),
                        fixed=False,
                        changes=[
                            f"Name mismatch: YAML='{yaml_name}' vs Dir='{dir_name}'"
                        ],
                    )

                    # Determine which to use (prefer dir name as it's the canonical reference)
                    if NAME_PATTERN.match(dir_name):
                        # Directory name is valid, update YAML
                        if not self.dry_run:
                            new_content = (
                                content.replace(
                                    f"name: {yaml_name}", f"name: {dir_name}"
                                )
                                .replace(f'name: "{yaml_name}"', f'name: "{dir_name}"')
                                .replace(f"name: '{yaml_name}'", f"name: '{dir_name}'")
                            )
                            skill_file.write_text(new_content)
                        result.changes.append(
                            f"Updated YAML name to match directory: {dir_name}"
                        )
                        result.fixed = True
                    elif NAME_PATTERN.match(yaml_name):
                        # YAML name is valid, rename directory
                        if not self.dry_run:
                            new_dir = skill_dir.parent / yaml_name
                            shutil.move(str(skill_dir), str(new_dir))
                        result.changes.append(
                            f"Renamed directory to match YAML: {yaml_name}"
                        )
                        result.fixed = True

                    self.results.append(result)

            except Exception:
                pass

    def print_summary(self) -> None:
        """Print fix summary."""
        print()
        print("=" * 70)
        print("FIX SUMMARY")
        print("=" * 70)

        fixed_count = sum(1 for r in self.results if r.fixed)
        error_count = sum(1 for r in self.results if r.errors)

        print(f"Files Processed: {len(self.results)}")
        print(f"Files Fixed: {fixed_count}")
        print(f"Files with Errors: {error_count}")
        print()

        if fixed_count > 0:
            print(
                "CHANGES MADE:"
                if not self.dry_run
                else "CHANGES (DRY RUN - NOT APPLIED):"
            )
            for result in self.results:
                if result.fixed:
                    print(f"\n  {result.file_path}:")
                    for change in result.changes:
                        print(f"    ✓ {change}")

        if error_count > 0:
            print("\nERRORS:")
            for result in self.results:
                if result.errors:
                    print(f"\n  {result.file_path}:")
                    for error in result.errors:
                        print(f"    ✗ {error}")

        if fixed_count == 0 and error_count == 0:
            print("✅ No fixes needed - all files are clean!")

        # Show next steps
        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("Run validation to verify fixes:")
        print()
        print("  uv run scripts/toolkit.py")
        print()
        print("=" * 70)

        print()


# --- Marketplace Synchronization (2026 Bi-Directional Source of Truth) ---


def clean_json_value(value):
    """Clean JSON field values - apply same rules as descriptions."""
    if not isinstance(value, str):
        return value
    return " ".join(value.split()).strip()


def sanitize_json_fields(data: dict) -> Tuple[bool, List[str]]:
    """Clean all string values in a JSON object."""
    changes = []
    for key, value in data.items():
        if isinstance(value, str):
            cleaned = clean_json_value(value)
            if cleaned != value:
                data[key] = cleaned
                changes.append(f"Cleaned '{key}' field")
        elif isinstance(value, dict):
            sub_changed, sub_changes = sanitize_json_fields(value)
            if sub_changed:
                changes.extend([f"  - {c}" for c in sub_changes])
    return bool(changes), changes


def sync_marketplace(
    plugins_dir: Path, marketplace_path: Path, dry_run: bool = False
) -> Tuple[List[str], List[str]]:
    """
    Synchronize marketplace.json with local plugin.json files.
    plugin.json acts as local authority, marketplace.json as compiled index.
    """
    warnings = []
    errors = []

    if not marketplace_path.exists():
        warnings.append(f"⚠️ No marketplace.json found at {marketplace_path}")
        return warnings, errors

    try:
        with open(marketplace_path, "r", encoding="utf-8") as f:
            mkt_data = json.load(f)

        mkt_plugins = mkt_data.get("plugins", [])
        updated = False

        # 1. Identify all actual plugin folders on disk
        local_plugin_folders = [
            f
            for f in plugins_dir.iterdir()
            if f.is_dir() and not f.name.startswith(".")
        ]
        local_plugin_names = []

        for plugin_folder in local_plugin_folders:
            plugin_json_path = plugin_folder / ".claude-plugin" / "plugin.json"
            if not plugin_json_path.exists():
                continue

            local_plugin_names.append(plugin_folder.name)

            try:
                with open(plugin_json_path, "r", encoding="utf-8") as f:
                    local_metadata = json.load(f)

                plugin_name = local_metadata.get("name", plugin_folder.name)

                # Find the corresponding entry in marketplace
                mkt_entry = next(
                    (p for p in mkt_plugins if p.get("name") == plugin_name), None
                )

                if mkt_entry:
                    # Check for drift between local plugin.json and marketplace.json
                    fields_to_sync = [
                        "description",
                        "version",
                        "author",
                        "license",
                        "tags",
                        "category",
                    ]
                    for field in fields_to_sync:
                        local_val = local_metadata.get(field)
                        mkt_val = mkt_entry.get(field)

                        # Skip if local has no value (None/empty) - don't overwrite marketplace
                        if local_val is None or local_val == "":
                            continue

                        # Normalize for comparison
                        if isinstance(local_val, str):
                            local_val = clean_json_value(local_val)
                        if isinstance(mkt_val, str):
                            mkt_val = clean_json_value(mkt_val)

                        if local_val != mkt_val:
                            msg = f"📊 Drift detected in '{plugin_name}' [{field}]: Local='{local_val}' vs Mkt='{mkt_val}'"
                            warnings.append(msg)
                            if not dry_run:
                                # Propagate local changes to marketplace
                                if field == "tags" and isinstance(local_val, list):
                                    # Merge and deduplicate tags
                                    existing_tags = mkt_entry.get("tags", [])
                                    merged_tags = list(set(existing_tags + local_val))
                                    mkt_entry["tags"] = merged_tags
                                else:
                                    mkt_entry[field] = local_val
                                updated = True
                else:
                    # plugin exists on disk but not in marketplace
                    msg = f"➕ Missing Plugin: '{plugin_name}' exists on disk but not in marketplace.json"
                    warnings.append(msg)
                    if not dry_run:
                        new_entry = {
                            "name": plugin_name,
                            "source": f"./plugins/{plugin_folder.name}",
                            "description": clean_json_value(
                                local_metadata.get("description", "")
                            ),
                            "version": local_metadata.get("version", "1.0.0"),
                            "strict": True,
                        }
                        # Copy additional fields if present
                        for field in ["author", "license", "tags", "category"]:
                            if field in local_metadata:
                                new_entry[field] = local_metadata[field]

                        mkt_plugins.append(new_entry)
                        updated = True

            except Exception as e:
                errors.append(f"✗ Error processing {plugin_folder.name}: {e}")

        # 2. Cleanup: Find entries in marketplace that no longer exist on disk
        original_count = len(mkt_plugins)

        # Keep entries that:
        # - Exist locally, OR
        # - Are remote (http/https/git sources)
        mkt_plugins = [
            p
            for p in mkt_plugins
            if any(p.get("name", "") == local_name for local_name in local_plugin_names)
            or any(
                p.get("source", "").startswith(prefix)
                for prefix in ["http", "git", "github:"]
            )
        ]

        if len(mkt_plugins) != original_count:
            removed = original_count - len(mkt_plugins)
            msg = f"🗑️ Removed {removed} dead plugin references from marketplace.json"
            warnings.append(msg)
            mkt_data["plugins"] = mkt_plugins
            updated = True

        # Save if updated
        if updated and not dry_run:
            with open(marketplace_path, "w", encoding="utf-8") as f:
                json.dump(mkt_data, f, indent=2, ensure_ascii=False)
            print("🚀 Marketplace synchronized and saved.")
        elif updated and dry_run:
            print("💾 Marketplace changes ready (DRY RUN - not saved)")

    except Exception as e:
        errors.append(f"✗ Error synchronizing marketplace: {e}")

    return warnings, errors


class MarketplaceSyncer:
    """Handles marketplace.json synchronization with local plugin.json files."""

    def __init__(
        self, plugins_dir: Path, marketplace_path: Path, dry_run: bool = False
    ):
        self.plugins_dir = plugins_dir
        self.marketplace_path = marketplace_path
        self.dry_run = dry_run
        self.results: Dict[str, Any] = {
            "warnings": [],
            "errors": [],
            "plugins_checked": 0,
            "plugins_synced": 0,
        }

    def sync_all(self) -> Dict[str, Any]:
        """Run complete marketplace synchronization."""
        print("=" * 70)
        print("🔄 Marketplace Synchronization")
        print(f"Source of Truth: plugin.json (local authority)")
        print(f"Index: marketplace.json (compiled registry)")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print("=" * 70)
        print()

        # Phase 1: Sync marketplace with plugin.json
        print("Phase 1: Synchronizing marketplace.json with plugin.json...")
        sync_warnings, sync_errors = sync_marketplace(
            self.plugins_dir, self.marketplace_path, dry_run=self.dry_run
        )
        self.results["warnings"].extend(sync_warnings)
        self.results["errors"].extend(sync_errors)

        # Phase 2: Lint and sanitize all plugin.json files
        print("Phase 2: Linting and sanitizing plugin.json files...")
        plugin_json_files = list(self.plugins_dir.rglob(".claude-plugin/plugin.json"))
        self.results["plugins_checked"] = len(plugin_json_files)

        for plugin_json_path in plugin_json_files:
            try:
                with open(plugin_json_path, "r", encoding="utf-8") as f:
                    plugin_data = json.load(f)

                # Sanitize fields
                changed, changes = sanitize_json_fields(plugin_data)

                if changed:
                    self.results["plugins_synced"] += 1
                    if not self.dry_run:
                        with open(plugin_json_path, "w", encoding="utf-8") as f:
                            json.dump(plugin_data, f, indent=2, ensure_ascii=False)
                        print(f"  ✓ Sanitized: {plugin_json_path.parent.parent.name}")
                    else:
                        print(
                            f"  • Would sanitize: {plugin_json_path.parent.parent.name}"
                        )
                        for change in changes:
                            print(f"    - {change}")

            except Exception as e:
                error_msg = f"✗ Error processing {plugin_json_path}: {e}"
                self.results["errors"].append(error_msg)

        self.print_summary()
        return self.results

    def print_summary(self) -> None:
        """Print synchronization summary."""
        print()
        print("=" * 70)
        print("MARKETPLACE SYNC SUMMARY")
        print("=" * 70)

        print(f"Plugin .json files checked: {self.results['plugins_checked']}")
        print(f"Plugin .json files updated: {self.results['plugins_synced']}")
        print(f"Warnings: {len(self.results['warnings'])}")
        print(f"Errors: {len(self.results['errors'])}")
        print()

        if self.results["warnings"]:
            print("WARNINGS:")
            for warning in self.results["warnings"]:
                print(f"  ⚠️ {warning}")
            print()

        if self.results["errors"]:
            print("ERRORS:")
            for error in self.results["errors"]:
                print(f"  ✗ {error}")
            print()

        # Show next steps
        print("=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print("Run validation to verify sync:")
        print()
        print("  uv run scripts/toolkit.py")
        print()
        print("=" * 70)

        print()


__all__ = [
    "ComponentFixer",
    "MarketplaceSyncer",
    "sync_marketplace",
    "clean_json_value",
    "sanitize_json_fields",
]
