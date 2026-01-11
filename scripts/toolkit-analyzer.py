# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
# ]
# ///

#!/usr/bin/env python3
"""
Cat Toolkit Plugin Analyzer & Validator
Unified Python script for analyzing and validating Cat Toolkit plugins
Merges strict validation with architectural analysis.
"""

import sys
import re
import json
import yaml
import argparse
import unicodedata
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Set
from dataclasses import dataclass, field
from collections import defaultdict


# --- Validation Constants ---
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500

# Hardcore naming regex - violation causes CLI crash
# Pattern: lowercase alphanumeric, hyphens allowed, no start/end hyphen, no consecutive hyphens
NAME_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

# Allowed frontmatter fields per Agent Skills Spec
ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
    "context",
    "agent",
    "model",
    "user-invocable",
    "hooks",
    "tools",  # Added for agents
    "permissionMode",  # Added for agents
}

# Built-in core tools
VALID_TOOLS = [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash",
    "Task",
    "AskUserQuestion",
    "Skill",
]

# Known external/custom tools that are valid (not errors)
KNOWN_CUSTOM_TOOLS = {
    "WebFetch",
    "WebSearch",
    "TodoWrite",
    "ExitPlanMode",
    "EnterPlanMode",
}

# MCP tools pattern (mcp__plugin_namespace-toolname__)
# Supports hyphens in namespace and tool names
MCP_TOOL_PATTERN = re.compile(r"^mcp__plugin_[a-zA-Z0-9_-]+__[a-zA-Z0-9_-]+$")


@dataclass
class ValidationResult:
    """Stores validation result for a single check"""

    name: str
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)


@dataclass
class ValidatorReport:
    """Comprehensive validation report"""

    timestamp: str
    validators_run: int
    total_errors: int
    total_warnings: int
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        return self.total_errors == 0 and all(r.passed for r in self.results)


@dataclass
class PluginComponent:
    """Represents a plugin component (skill, agent, command, hook)."""

    name: str
    type: str  # skill, agent, command, hook
    plugin: str
    path: str
    frontmatter: dict = field(default_factory=dict)
    references: Set[str] = field(default_factory=set)
    referenced_by: Set[str] = field(default_factory=set)


@dataclass
class CrossPluginLink:
    """Represents a cross-plugin dependency or reference."""

    source: str  # plugin:name:type
    target: str  # plugin:name:type
    link_type: str  # requires, invokes, delegates, references
    source_file: str
    target_file: str
    description: str = ""


# --- Validation Logic (Ported from skills-ref) ---


def _validate_name(name: str, skill_dir: Optional[Path] = None) -> List[str]:
    """Validate skill name format and directory match.
    Violation causes CLI crash - errors are CRITICAL."""
    errors = []

    if not name or not isinstance(name, str) or not name.strip():
        errors.append("CRITICAL: Field 'name' is missing. Code will crash.")
        return errors

    name_normalized = unicodedata.normalize("NFKC", name.strip())

    # 1. Length check
    if len(name_normalized) > MAX_NAME_LENGTH:
        errors.append(
            f"CRITICAL: Name length ({len(name_normalized)}) exceeds limit ({MAX_NAME_LENGTH}). "
            "Code will crash."
        )

    # 2. Pattern check (comprehensive)
    if not NAME_PATTERN.match(name_normalized):
        errors.append(
            f"CRITICAL: Name '{name_normalized}' contains invalid characters. "
            "Must be lowercase alphanumeric (a-z, 0-9), hyphens allowed, "
            "no start/end hyphens, no consecutive hyphens (--). Code will crash."
        )

    # 3. Explicit checks for clearer error messages
    if name_normalized != name_normalized.lower():
        errors.append(f"CRITICAL: Name '{name_normalized}' must be lowercase only.")

    if name_normalized.startswith("-"):
        errors.append(f"CRITICAL: Name '{name_normalized}' cannot start with a hyphen.")

    if name_normalized.endswith("-"):
        errors.append(f"CRITICAL: Name '{name_normalized}' cannot end with a hyphen.")

    if "--" in name_normalized:
        errors.append(f"CRITICAL: Name '{name_normalized}' contains consecutive hyphens (--).")

    if "_" in name_normalized:
        errors.append(
            f"CRITICAL: Name '{name_normalized}' contains underscore (_). "
            "Use hyphens (-) only."
        )

    # 4. Directory match (skills only)
    if skill_dir:
        dir_name = unicodedata.normalize("NFKC", skill_dir.name)
        if dir_name != name_normalized:
            errors.append(
                f"CRITICAL: Skill name '{name_normalized}' MUST match directory name '{dir_name}'. "
                "Code will crash."
            )

    return errors


def _validate_description(description: str) -> List[str]:
    """Validate description format.
    Violation causes CLI crash - errors are CRITICAL."""
    errors = []

    if not description or not isinstance(description, str) or not description.strip():
        errors.append("CRITICAL: Field 'description' is missing. Code will crash.")
        return errors

    # 1. Length check
    if len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"CRITICAL: Description length ({len(description)}) exceeds limit ({MAX_DESCRIPTION_LENGTH}). "
            "Code will crash."
        )

    # 2. Multi-line check (YAML parsing safety)
    if "\n" in description.strip():
        errors.append("CRITICAL: Description must be a single-line string only.")

    # 3. Pattern check (discovery tiering)
    first_line = description.split("\n")[0]
    normalized = re.sub(r'^["\']', "", first_line).upper()
    if not re.match(r"^(PROACTIVELY|MUST|SHOULD)?\s*USE\s+WHEN", normalized):
        errors.append(
            "CRITICAL: Description must start with 'USE when', 'MUST USE when', "
            "'SHOULD USE when', or 'PROACTIVELY USE when' pattern for semantic discovery."
        )

    return errors


def _validate_compatibility(compatibility: str) -> List[str]:
    """Validate compatibility format."""
    errors = []

    if not isinstance(compatibility, str):
        errors.append("Field 'compatibility' must be a string")
        return errors

    if len(compatibility) > MAX_COMPATIBILITY_LENGTH:
        errors.append(
            f"Compatibility exceeds {MAX_COMPATIBILITY_LENGTH} character limit "
            f"({len(compatibility)} chars)"
        )

    return errors


def _validate_metadata_fields(metadata: dict) -> List[str]:
    """Validate that only allowed fields are present."""
    errors = []
    extra_fields = set(metadata.keys()) - ALLOWED_FIELDS
    if extra_fields:
        errors.append(
            f"Unexpected fields in frontmatter: {', '.join(sorted(extra_fields))}. "
            f"Only {sorted(ALLOWED_FIELDS)} are allowed."
        )
    return errors


class ToolkitAnalyzer:
    """Main analyzer class that orchestrates all validation tasks"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()

        # Smart detection of plugins dir
        if (self.root_dir / "plugins").is_dir():
            self.plugins_dir = self.root_dir / "plugins"
        elif self.root_dir.name == "plugins":
            self.plugins_dir = self.root_dir
        else:
            # Fallback for running inside a specific plugin or root without plugins dir
            self.plugins_dir = self.root_dir

        self.report = ValidatorReport(
            timestamp=datetime.now().isoformat(),
            validators_run=0,
            total_errors=0,
            total_warnings=0,
        )

        # Graph/Architecture Data
        self.components: Dict[str, PluginComponent] = {}
        self.cross_links: List[CrossPluginLink] = []
        self.plugin_stats: Dict[str, dict] = {}
        self.graphs_dir = self.root_dir / "graphs"

    def log_result(self, result: ValidationResult) -> None:
        """Add result to report and update counters"""
        if result.errors:
            result.passed = False

        self.report.results.append(result)
        if not result.passed:
            self.report.total_errors += len(result.errors)
        self.report.total_warnings += len(result.warnings)
        self.report.validators_run += 1

    def validate_all(self) -> ValidatorReport:
        """Run all validators"""
        print("=" * 70)
        print("Cat Toolkit Plugin Analyzer & Validator")
        print(f"Scanning: {self.plugins_dir}")
        print("=" * 70)
        print()

        # Phase 0: Discovery & Parsing (Architecture)
        self._discover_and_parse()
        self._extract_relationships()

        # Phase 1-6: Existing Validators
        self.validate_frontmatter()
        self.validate_links()
        self.validate_glue_code()
        self.validate_fork_bloat()
        self.validate_askuser_leakage()
        self.validate_token_budget()

        # Phase 7: Architecture Validation
        self.validate_architecture()

        # Display summary
        self.print_summary()

        return self.report

    def _discover_and_parse(self):
        """Discover plugins and parse components logic merged from plugin-analyzer.py"""
        if not self.plugins_dir.exists():
            return

        for plugin_dir in self.plugins_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
                self._parse_plugin(plugin_dir.name)

    def _parse_plugin(self, plugin_name: str):
        """Parse all components in a plugin."""
        plugin_path = self.plugins_dir / plugin_name
        stats = {"skills": 0, "agents": 0, "commands": 0, "hooks": 0}

        # Parse skills
        skills_dir = plugin_path / "skills"
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    # Check for both SKILL.md and skill.md
                    skill_file = skill_dir / "SKILL.md"
                    if not skill_file.exists():
                        skill_file = skill_dir / "skill.md"

                    if skill_file.exists():
                        component = self._parse_yaml_frontmatter(
                            skill_file, plugin_name, "skill"
                        )
                        if component:
                            self.components[f"{plugin_name}:{component.name}:skill"] = (
                                component
                            )
                            stats["skills"] += 1

        # Parse agents
        agents_dir = plugin_path / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                component = self._parse_yaml_frontmatter(
                    agent_file, plugin_name, "agent"
                )
                if component:
                    self.components[f"{plugin_name}:{component.name}:agent"] = component
                    stats["agents"] += 1

        # Parse commands
        commands_dir = plugin_path / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.md"):
                component = self._parse_yaml_frontmatter(
                    cmd_file, plugin_name, "command"
                )
                if component:
                    self.components[f"{plugin_name}:{component.name}:command"] = (
                        component
                    )
                    stats["commands"] += 1

        # Parse hooks
        hooks_file = plugin_path / "hooks" / "hooks.json"
        if hooks_file.exists():
            try:
                with open(hooks_file) as f:
                    hooks_data = json.load(f)
                    stats["hooks"] = len(hooks_data.get("hooks", {}))
                    # Add hook component placeholder for linking
                    self.components[f"{plugin_name}:hooks:{plugin_name}"] = (
                        PluginComponent(
                            name="hooks",
                            type="hook",
                            plugin=plugin_name,
                            path=str(hooks_file),
                        )
                    )
            except Exception:
                pass

        self.plugin_stats[plugin_name] = stats

    def _parse_yaml_frontmatter(
        self, file_path: Path, plugin_name: str, comp_type: str
    ) -> Optional[PluginComponent]:
        """Parse YAML frontmatter from markdown file."""
        try:
            content = file_path.read_text()

            if content.startswith("---"):
                end_yaml = content.find("---", 3)
                if end_yaml != -1:
                    yaml_content = content[3:end_yaml].strip()
                    frontmatter = yaml.safe_load(yaml_content)
                    if not isinstance(frontmatter, dict):
                        frontmatter = {}

                    name = frontmatter.get("name", file_path.stem)
                    if comp_type == "skill":
                        name = file_path.parent.name

                    component = PluginComponent(
                        name=name,
                        type=comp_type,
                        plugin=plugin_name,
                        path=str(file_path),
                        frontmatter=frontmatter,
                    )

                    self._extract_references(content, component)
                    return component
        except Exception:
            pass
        return None

    def _extract_references(self, content: str, component: PluginComponent):
        """Extract skill/agent references from component content."""
        # Pattern 1: skills: [skill1, skill2] (in YAML frontmatter)
        skills_match = re.search(
            r"skills:\s*\[(.*?)\]", content, re.MULTILINE | re.DOTALL
        )
        if skills_match:
            skills_str = skills_match.group(1)
            skills = [s.strip().strip("\"'") for s in skills_str.split(",")]
            for skill in skills:
                if skill:
                    component.references.add(f"skill:{skill}")

        # Pattern 2: allowed-tools: [Skill(tool-name)]
        tools_match = re.search(
            r"allowed-tools:\s*\[(.*?)\]", content, re.MULTILINE | re.DOTALL
        )
        if tools_match:
            tools_str = tools_match.group(1)
            tools = re.findall(r"Skill\(([^)]+)\)", tools_str)
            for tool in tools:
                component.references.add(f"skill:{tool}")

        # Pattern 3: references/other-plugin/skill-name
        ref_pattern = r"references/([\w-]+)/([\w-]+)"
        for match in re.finditer(ref_pattern, content):
            plugin = match.group(1)
            skill = match.group(2)
            if plugin != component.plugin:
                component.references.add(f"external:{plugin}:{skill}")

    def _extract_relationships(self):
        """Extract cross-plugin relationships."""
        # Build index of all components by type and name
        component_index = defaultdict(list)
        for comp_id, component in self.components.items():
            plugin, name, comp_type = comp_id.split(":", 2)
            component_index[f"{comp_type}:{name}"].append((plugin, comp_id))
            component_index[name].append((plugin, comp_id))

        unique_relationships = set()

        for comp_id, component in self.components.items():
            plugin, name, comp_type = comp_id.split(":", 2)

            for ref in component.references:
                if ref.startswith("external:"):
                    # External reference (external:plugin:name or external:plugin:component)
                    ref_parts = ref.split(":", 2)
                    if len(ref_parts) >= 3:
                        _, ref_plugin, ref_name = ref_parts

                        # Try to match by skill first, then agent, then any
                        matched = False
                        for comp_type_to_try in ["skill", "agent", "command"]:
                            target_key = f"{comp_type_to_try}:{ref_name}"
                            if target_key in component_index:
                                for target_plugin, target_id in component_index[
                                    target_key
                                ]:
                                    if target_plugin == ref_plugin:
                                        link_type = "delegates"
                                        if comp_type == "agent":
                                            link_type = "references"
                                        elif comp_type == "command":
                                            link_type = "invokes"

                                        rel_key = (comp_id, target_id, link_type)
                                        if rel_key not in unique_relationships:
                                            unique_relationships.add(rel_key)
                                            link = CrossPluginLink(
                                                source=comp_id,
                                                target=target_id,
                                                link_type=link_type,
                                                source_file=component.path,
                                                target_file=self.components[
                                                    target_id
                                                ].path,
                                                description=f"{comp_type} '{name}' {link_type} '{ref_name}' from {ref_plugin}",
                                            )
                                            self.cross_links.append(link)
                                        matched = True
                                        break
                                if matched:
                                    break

                elif ref.startswith("skill:"):
                    skill_name = ref.split(":", 1)[1]
                    # Check locally loop logic omitted for brevity as it's less critical for cross-plugin check
                    # But checking externals via skill name:
                    if skill_name in component_index:
                        for target_plugin, target_id in component_index[skill_name]:
                            if target_plugin != plugin:
                                link_type = "invokes"
                                rel_key = (comp_id, target_id, link_type)
                                if rel_key not in unique_relationships:
                                    unique_relationships.add(rel_key)
                                    link = CrossPluginLink(
                                        source=comp_id,
                                        target=target_id,
                                        link_type=link_type,
                                        source_file=component.path,
                                        target_file=self.components[target_id].path,
                                        description=f"{comp_type} '{name}' {link_type} '{skill_name}' from {target_plugin}",
                                    )
                                    self.cross_links.append(link)

    def validate_architecture(self) -> None:
        """Validate component graph architecture"""
        result = ValidationResult("Architecture Check", True)
        print("Phase 6: Architecture & Circular Dependency Check")
        print("-" * 70)

        # Check for circular dependencies
        visited = set()
        rec_stack = set()
        has_cycle = False
        cycle_path = []

        def has_cycle_dfs(node):
            nonlocal has_cycle
            visited.add(node)
            rec_stack.add(node)

            comp = self.components.get(node)
            if comp:
                # Naive reference checking for graph traversal
                # Simplify: just look at cross_links to find outgoing edges
                outgoing = [
                    link.target for link in self.cross_links if link.source == node
                ]
                for target_id in outgoing:
                    if target_id not in visited:
                        if has_cycle_dfs(target_id):
                            cycle_path.append(node)
                            return True
                    elif target_id in rec_stack:
                        comp_target = self.components.get(target_id)
                        if comp_target:
                            cycle_path.append(node)
                            result.errors.append(
                                f"Circular dependency detected involving {comp.plugin}:{comp.name} -> {comp_target.plugin}:{comp_target.name}"
                            )
                            has_cycle = True
                            return True

            rec_stack.remove(node)
            return False

        for comp_id in self.components:
            if comp_id not in visited:
                has_cycle_dfs(comp_id)

        # Check for broken cross-references
        # (This is already partially covered by validate_links, but this checks logical references)
        # We can implement specific checks if needed, but validate_links is robust enough for headers.

        print(
            f"  Checked {len(self.components)} components and {len(self.cross_links)} relationships."
        )

        print()
        self.log_result(result)

    def validate_frontmatter(self) -> None:
        """Validate YAML frontmatter in skills, commands, and agents"""
        result = ValidationResult("Frontmatter Validation", True)

        print("Phase 1: Frontmatter Validation")
        print("-" * 70)

        # Validate skills
        # Look for SKILL.md or skill.md files recursively
        skill_files = list(self.plugins_dir.rglob("SKILL.md")) + list(
            self.plugins_dir.rglob("skill.md")
        )

        # Deduplicate results if both patterns match same files
        skill_files = list(set(skill_files))

        if not skill_files:
            result.warnings.append("No SKILL.md files found")
        else:
            print(f"  Validating {len(skill_files)} skills...")

            for skill_file in skill_files:
                skill_dir = skill_file.parent
                try:
                    content = skill_file.read_text()
                    if not content.startswith("---"):
                        result.errors.append(f"{skill_file}: Missing YAML frontmatter")
                        continue

                    end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                    if not end_match:
                        result.errors.append(
                            f"{skill_file}: Missing closing frontmatter marker"
                        )
                        continue

                    fm_text = content[3 : 3 + end_match.start()]
                    try:
                        frontmatter = yaml.safe_load(fm_text)
                        if not isinstance(frontmatter, dict):
                            raise ValueError("Frontmatter is not a dict")
                    except Exception as e:
                        result.errors.append(
                            f"{skill_file}: Invalid YAML frontmatter: {e}"
                        )
                        continue

                    # 1. Field Validation
                    field_errors = _validate_metadata_fields(frontmatter)
                    result.errors.extend([f"{skill_file}: {e}" for e in field_errors])

                    # 2. Name Validation
                    if "name" not in frontmatter:
                        result.errors.append(
                            f"{skill_file}: Missing required field 'name'"
                        )
                    else:
                        name_errors = _validate_name(frontmatter["name"], skill_dir)
                        result.errors.extend(
                            [f"{skill_file}: {e}" for e in name_errors]
                        )

                    # 3. Description Validation
                    if "description" not in frontmatter:
                        result.errors.append(
                            f"{skill_file}: Missing required field 'description'"
                        )
                    else:
                        desc_errors = _validate_description(frontmatter["description"])
                        result.errors.extend(
                            [f"{skill_file}: {e}" for e in desc_errors]
                        )

                    # 4. Compatibility Validation
                    if "compatibility" in frontmatter:
                        comp_errors = _validate_compatibility(
                            frontmatter["compatibility"]
                        )
                        result.errors.extend(
                            [f"{skill_file}: {e}" for e in comp_errors]
                        )

                    # 5. Context/Agent Validation (Toolkit specific)
                    if "context" in frontmatter and frontmatter["context"] != "fork":
                        result.errors.append(
                            f"{skill_file}: context must be 'fork' if specified"
                        )

                    if "agent" in frontmatter and "context" not in frontmatter:
                        result.warnings.append(
                            f"{skill_file}: 'agent' field only valid with 'context: fork'"
                        )

                    # 6. Allowed Tools Validation
                    if "allowed-tools" in frontmatter:
                        tools = frontmatter["allowed-tools"]
                        if isinstance(tools, str):
                            tools = [t.strip() for t in tools.split(",")]
                        for tool in tools:
                            tool_clean = re.sub(r"Skill\(([^)]+)\)", r"\1", tool)
                            # Handle parameterized tools like Bash[python] or Bash(cat)
                            tool_base = re.split(r"[\[\(]", tool_clean)[0]

                            # Skip validation for:
                            # - Skill references (Skill(tool-name))
                            # - Known custom tools
                            # - MCP tools
                            if (
                                "Skill(" not in tool
                                and tool_base not in VALID_TOOLS
                                and tool_base not in KNOWN_CUSTOM_TOOLS
                                and not MCP_TOOL_PATTERN.match(tool_base)
                            ):
                                result.warnings.append(
                                    f"{skill_file}: Unknown tool '{tool_clean}' (base: {tool_base})"
                                )

                except Exception as e:
                    result.errors.append(f"{skill_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_links(self) -> None:
        """Validate markdown links and references"""
        result = ValidationResult("Link Validation", True)

        print("Phase 2: Link Validation")
        print("-" * 70)

        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        backtick_pattern = re.compile(r"`(references|assets|scripts)/[^`]+`")
        cross_ref_pattern = re.compile(r"\.\./[^/]+/skill")

        md_files = list(self.plugins_dir.rglob("*.md"))
        print(f"  Checking {len(md_files)} markdown files...")

        for md_file in md_files:
            try:
                content = md_file.read_text()
                file_dir = md_file.parent

                # Find skill root for backtick paths
                skill_root = file_dir
                while (
                    skill_root != self.root_dir
                    and skill_root != self.plugins_dir
                    and skill_root.parent != skill_root
                ):
                    if (skill_root / "SKILL.md").exists():
                        break
                    skill_root = skill_root.parent

                if not (skill_root / "SKILL.md").exists():
                    skill_root = file_dir

                # Validate markdown links
                for match in link_pattern.finditer(content):
                    link = match.group(2)

                    if link.startswith(
                        ("http://", "https://", "#", "file://", "$", "mailto:")
                    ):
                        continue

                    if not link.strip():
                        continue

                    target_path = file_dir / link
                    target_path = target_path.resolve()
                    if "#" in str(target_path):
                        target_path = Path(str(target_path).split("#")[0])

                    if not target_path.exists():
                        target_path_root = skill_root / link
                        if not target_path_root.exists():
                            result.errors.append(f"{md_file}: Broken link -> {link}")

                # Validate backtick paths
                # Template/documentation files may reference optional files
                is_template = "templates" in str(md_file) or "assets" in str(md_file)
                for match in backtick_pattern.finditer(content):
                    path = match.group(0).strip("`")
                    target = skill_root / path
                    if not target.exists():
                        # Only warn for non-template files
                        # Template files are documentation and may reference optional files
                        if not is_template:
                            result.warnings.append(
                                f"{md_file}: Backtick path not found -> {path}"
                            )
                        else:
                            result.info.append(
                                f"{md_file}: Optional reference -> {path}"
                            )

                # Check for cross-skill references (only flag in non-README files)
                # README files are expected to have cross-skill references for documentation
                is_readme = md_file.name.lower() in ["readme.md", "readme"]
                if not is_readme:
                    for match in cross_ref_pattern.finditer(content):
                        result.warnings.append(
                            f"{md_file}: Cross-skill reference found"
                        )

                # Check @[file] syntax misuse
                if "@[" in content and "commands" not in str(md_file):
                    result.warnings.append(
                        f"{md_file}: @[file] syntax found (only valid in commands)"
                    )

            except Exception as e:
                result.errors.append(f"{md_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_glue_code(self) -> None:
        """Detect glue code patterns and validate 2026 Standards"""
        result = ValidationResult("Glue Code & Standard Detection", True)

        print("Phase 3: Glue Code & AI Macro Standards")
        print("-" * 70)

        command_files = list(self.plugins_dir.rglob("commands/*.md"))
        print(f"  Checking {len(command_files)} command files...")

        for cmd_file in command_files:
            try:
                content = cmd_file.read_text()
                lines = content.split("\n")

                # AI Macro: Commands can wrap Skills for high-fidelity execution
                # Logic Duplication Check
                if len(lines) > 50 and "Skill(" not in content:
                    result.warnings.append(
                        f"{cmd_file}: Large command detected (>50 lines). "
                        "Commands should primarily orchestrate Skills/Agents, not contain heavy logic."
                    )

                # Description Check (AI needs terse descriptions for semantic routing)
                if "description" in content:
                    desc_match = re.search(r'description:\s*["\'](.*?)["\']', content, re.DOTALL)
                    if desc_match and len(desc_match.group(1)) > 200:
                        result.warnings.append(
                            f"{cmd_file}: Description is too long (>200 chars). "
                            "Keep descriptions semantic and terse for optimal AI routing."
                        )

            except Exception as e:
                result.errors.append(f"{cmd_file}: Error processing: {e}")

        agent_files = list(self.plugins_dir.rglob("agents/*.md"))
        for agent_file in agent_files:
            try:
                content = agent_file.read_text()
                task_count = content.count("Task(")
                if task_count > 5:
                    result.warnings.append(
                        f"{agent_file}: High delegation pattern ({task_count} Task calls)"
                    )
                lines = content.split("\n")
                if task_count > 5 and len(lines) < 50:
                    result.warnings.append(
                        f"{agent_file}: Potential wrapper agent (high delegation, minimal content)"
                    )
            except Exception as e:
                result.errors.append(f"{agent_file}: Error processing: {e}")

        for py_file in self.plugins_dir.rglob("*.py"):
            try:
                content = py_file.read_text()
                if "../../" in content:
                    result.warnings.append(f"{py_file}: Cross-plugin coupling detected")
            except Exception:
                pass

        print()
        self.log_result(result)

    def validate_fork_bloat(self) -> None:
        """Check for unnecessary fork usage"""
        result = ValidationResult("Fork-Bloat Validation", True)

        print("Phase 4: Fork-Bloat Validation (2026 Inline-First)")
        print("-" * 70)

        skill_files = list(self.plugins_dir.rglob("SKILL.md")) + list(
            self.plugins_dir.rglob("skill.md")
        )
        print(f"  Checking {len(skill_files)} skills...")

        for skill_file in skill_files:
            try:
                content = skill_file.read_text()
                if not content.startswith("---"):
                    continue

                end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                if not end_match:
                    continue

                fm_text = content[3 : 3 + end_match.start()]
                frontmatter = yaml.safe_load(fm_text)

                if frontmatter.get("context") == "fork":
                    skill_name = frontmatter.get("name", "unknown")
                    allowed_tools = frontmatter.get("allowed-tools", "")

                    if isinstance(allowed_tools, str):
                        has_task = "Task(" in allowed_tools or "Task" in allowed_tools
                    elif isinstance(allowed_tools, list):
                        has_task = "Task" in allowed_tools
                    else:
                        has_task = False

                    has_agent = "agent" in frontmatter

                    # Skills that legitimately need fork context for computational complexity
                    # (not just agent delegation)
                    computational_fork_skills = {
                        "intent-translation",
                        "multimodal-understanding",
                    }

                    if (
                        not has_task
                        and not has_agent
                        and skill_name not in computational_fork_skills
                        and "Read" not in allowed_tools
                        and "Grep" not in allowed_tools
                    ):
                        result.warnings.append(
                            f"{skill_file}: Skill '{skill_name}' has 'context: fork' but no 'Task', 'Read', or 'Grep' tools. "
                            f"Forked skills should either be for isolation (Task) or volume processing (Read/Grep)."
                        )
            except Exception as e:
                result.errors.append(f"{skill_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_askuser_leakage(self) -> None:
        """Check for AskUserQuestion in worker agents"""
        result = ValidationResult("AskUser-Leakage Validation", True)

        print("Phase 5: AskUser-Leakage Validation (2026 Autonomous Agents)")
        print("-" * 70)

        agent_files = list(self.plugins_dir.rglob("agents/*.md"))
        print(f"  Checking {len(agent_files)} agents...")

        for agent_file in agent_files:
            try:
                content = agent_file.read_text()
                if not content.startswith("---"):
                    continue

                end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                if not end_match:
                    continue

                fm_text = content[3 : 3 + end_match.start()]
                frontmatter = yaml.safe_load(fm_text)

                agent_name = agent_file.stem
                perm_mode = frontmatter.get("permissionMode")
                tools = frontmatter.get("tools", [])
                description = frontmatter.get("description", "")

                if perm_mode in ["acceptEdits", "bypassPermissions"]:
                    has_ask = "AskUserQuestion" in tools
                    if has_ask:
                        result.errors.append(
                            f"{agent_file}: Agent '{agent_name}' has 'permissionMode: {perm_mode}' with 'AskUserQuestion' in tools. "
                            f"2026 Autonomous Agent Rule: Execution-phase workers MUST NOT have AskUserQuestion."
                        )
                    if not tools and perm_mode == "acceptEdits":
                        result.warnings.append(
                            f"{agent_file}: Agent '{agent_name}' has 'permissionMode: acceptEdits' but no 'tools' whitelist. "
                            f"Agent inherits ALL tools including 'AskUserQuestion'."
                        )

                is_worker = (
                    "worker" in agent_name.lower() or "worker" in description.lower()
                )
                is_coordinator = any(
                    x in agent_name.lower() or x in description.lower()
                    for x in ["director", "coordinator", "planner"]
                )

                if is_worker:
                    tools = frontmatter.get("tools", [])
                    if "AskUserQuestion" in tools:
                        result.errors.append(
                            f"{agent_file}: Agent '{agent_name}' is a worker but has 'AskUserQuestion' in tools. "
                            f"Workers execute autonomously without user interaction."
                        )

                if is_coordinator:
                    result.info.append(
                        f"{agent_file}: Coordinator-type agent found. AskUserQuestion is acceptable here."
                    )
            except Exception as e:
                result.errors.append(f"{agent_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_token_budget(self) -> None:
        """Validate total metadata size against Token Budget"""
        result = ValidationResult("Token Budget Validation", True)

        print("Phase 6: Token Budget Validation")
        print("-" * 70)

        total_chars = 0
        limit = 15000

        # Calculate total description and argument-hint length
        for comp in self.components.values():
            if comp.frontmatter:
                desc = comp.frontmatter.get("description", "")
                total_chars += len(str(desc))

                # Check argument-hint if present (commands)
                hint = comp.frontmatter.get("argument-hint", "")
                total_chars += len(str(hint))

        print(f"  Total Metadata Size: {total_chars:,} / {limit:,} chars")

        if total_chars > limit:
            result.errors.append(
                f"Token Budget Exceeded: {total_chars:,} chars > {limit:,} limit. "
                "This risks context truncation. Consolidate skills or shorten descriptions."
            )
        else:
            usage_pct = (total_chars / limit) * 100
            result.info.append(
                f"Token Budget Usage: {usage_pct:.1f}% ({total_chars:,} chars)"
            )

        print()
        self.log_result(result)

    def print_summary(self) -> None:
        """Print validation summary"""
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"Validators Run: {self.report.validators_run}")
        print(f"Total Errors: {self.report.total_errors}")
        print(f"Total Warnings: {self.report.total_warnings}")
        print()

        if self.report.all_passed:
            print("All validators passed!")
        else:
            print("Validation issues found")

        # Always show errors if any
        if self.report.total_errors > 0:
            print("\nERRORS:")
            for result in self.report.results:
                if result.errors:
                    print(f"\n  {result.name}:")
                    for error in result.errors:
                        print(f"    • {error}")

        # Always show warnings if any
        if self.report.total_warnings > 0:
            print("\nWARNINGS:")
            for result in self.report.results:
                if result.warnings:
                    print(f"\n  {result.name}:")
                    for warning in result.warnings:
                        print(f"    • {warning}")

        # Show info messages if any
        info_count = sum(len(r.info) for r in self.report.results)
        if info_count > 0:
            print("\nINFO:")
            for result in self.report.results:
                if result.info:
                    print(f"\n  {result.name}:")
                    for info in result.info:
                        print(f"    • {info}")

        print()
        print("=" * 70)


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
