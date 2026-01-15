"""
Validation logic for the Cat Toolkit analyzer.
All read-only validation checks are contained in this module.
"""

import json
import re
import unicodedata
import yaml
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Local imports (same directory)
from common import (
    ValidationResult,
    ValidatorReport,
    PluginComponent,
    CrossPluginLink,
    MAX_NAME_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MAX_COMPATIBILITY_LENGTH,
    NAME_PATTERN,
    ALLOWED_FIELDS_SKILL,
    ALLOWED_FIELDS_AGENT,
    ALLOWED_FIELDS_COMMAND,
    ALLOWED_FIELDS,
    VALID_TOOLS,
    KNOWN_CUSTOM_TOOLS,
    MCP_TOOL_PATTERN,
    EXCLUDED_DIRS,
    filter_excluded_paths,
)


def _validate_name(
    name: str, skill_dir: Optional[Path] = None
) -> tuple[List[str], List[str]]:
    """Validate skill name format and directory match.
    Violation causes CLI crash - errors are CRITICAL."""
    errors = []
    warnings = []

    if not name or not isinstance(name, str) or not name.strip():
        errors.append("CRITICAL: Field 'name' is missing. Code will crash.")
        return errors, warnings

    name_normalized = unicodedata.normalize("NFKC", name.strip())

    # 1. Length check
    if len(name_normalized) > MAX_NAME_LENGTH:
        errors.append(
            f"CRITICAL: Name length ({len(name_normalized)}) exceeds limit ({MAX_NAME_LENGTH}). "
            "Code will crash."
        )
    elif len(name_normalized) > 30:
        warnings.append(
            f"Name is quite long ({len(name_normalized)} chars). "
            f"Consider shorter names for better usability (current: '{name_normalized}')."
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
        errors.append(
            f"CRITICAL: Name '{name_normalized}' contains consecutive hyphens (--)."
        )

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
        elif len(name_normalized) > 50:
            warnings.append(
                f"Skill name '{name_normalized}' matches directory but is very long. "
                f"Consider a shorter name for better maintainability."
            )

    return errors, warnings


def _validate_description(
    description: str, comp_type: str = "skill"
) -> tuple[List[str], List[str]]:
    """Validate description format.
    Violation causes CLI crash - errors are CRITICAL.

    Args:
        description: The description string to validate
        comp_type: Component type ('skill', 'agent', 'command')
    """
    errors = []
    warnings = []

    if not description or not isinstance(description, str) or not description.strip():
        errors.append("CRITICAL: Field 'description' is missing. Code will crash.")
        return errors, warnings

    # 1. Length check
    if len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"CRITICAL: Description length ({len(description)}) exceeds limit ({MAX_DESCRIPTION_LENGTH}). "
            "Code will crash."
        )
    elif len(description) > 500:
        warnings.append(
            f"Description is quite long ({len(description)} chars). "
            f"Consider shortening for better readability (current: '{description[:100]}...')."
        )

    # 2. Multi-line check (YAML parsing safety)
    if "\n" in description.strip():
        errors.append("CRITICAL: Description must be a single-line string only.")

    # 3. Pattern check (2026 Standard Pattern from CLAUDE.md)
    # Only Skills require "Use when" pattern for semantic discovery
    # Commands and Agents have more flexible description formats
    if comp_type == "skill":
        # Standard Pattern: {CAPABILITY}. Use when {TRIGGERS}.
        # Enhanced Pattern: {CAPABILITY}. {MODAL} Use when {TRIGGERS}.
        # Both should START with capability, NOT with "USE when"
        first_line = description.split("\n")[0].strip()
        normalized = re.sub(r'^["\']', "", first_line)

        # Check for "Use when" pattern (required for semantic discovery in skills)
        use_when_pattern = r"\.?\s*Use when"
        has_use_when = bool(re.search(use_when_pattern, normalized, re.IGNORECASE))

        if not has_use_when:
            errors.append(
                "CRITICAL: Description must contain 'Use when' pattern for semantic discovery. "
                "Standard Pattern: '{CAPABILITY}. Use when {TRIGGERS}.' "
                "Enhanced Pattern: '{CAPABILITY}. {MODAL} Use when {TRIGGERS}.'"
            )

        # Check for Enhanced Pattern (MUST/PROACTIVELY/SHOULD)
        has_modal = bool(
            re.search(
                r"\.\s*(MUST|PROACTIVELY|SHOULD)\s+Use when", normalized, re.IGNORECASE
            )
        )

        # 4. Optional: Check if description starts with capability (good practice)
        # Should start with capital letter and NOT start with "Use when"
        if re.match(r"^Use when", normalized, re.IGNORECASE):
            errors.append(
                "CRITICAL: Description should start with CAPABILITY statement, not 'Use when'. "
                "Format: '{CAPABILITY}. Use when {TRIGGERS}.' "
                f"Current: '{normalized[:100]}...'"
            )

    return errors, warnings


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


def _validate_metadata_fields(metadata: dict, comp_type: str = "skill") -> List[str]:
    """Validate that only allowed fields are present per component type."""
    errors = []

    # Select appropriate allowed fields based on component type
    if comp_type == "skill":
        allowed = ALLOWED_FIELDS_SKILL
    elif comp_type == "agent":
        allowed = ALLOWED_FIELDS_AGENT
    elif comp_type == "command":
        allowed = ALLOWED_FIELDS_COMMAND
    else:
        allowed = ALLOWED_FIELDS  # Fallback to union

    extra_fields = set(metadata.keys()) - allowed
    if extra_fields:
        errors.append(
            f"Unexpected fields in frontmatter: {', '.join(sorted(extra_fields))}. "
            f"For {comp_type}, only {sorted(allowed)} are allowed per CLAUDE.md."
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

        # Phase 7-10: 2026 Standards Validators
        self.validate_zero_token_retention()
        self.validate_description_modalities()
        self.validate_permission_leakage()
        self.validate_command_structure()

        # Phase 11: Architecture Validation
        self.validate_architecture()

        # Phase 13-15: 2026 Security & Quality Validators
        self.validate_agent_security()
        self.validate_thin_wrappers()
        self.validate_persona_language()

        # Phase 16: Emoji Usage Validation
        self.validate_emoji_usage()

        # Phase 12: Claude Plugin Validation
        self.validate_claude_plugin()

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
        print("Phase 11: Architecture & Circular Dependency Check")
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

        # Deduplicate and filter excluded directories
        skill_files = filter_excluded_paths(list(set(skill_files)))

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

                    # CRITICAL: Strict Description Check (Raw Text)
                    # We must ban YAML block scalars (| and >) for descriptions to ensure simple one-liners.
                    if re.search(r"^description:\s*[|>]", fm_text, re.MULTILINE):
                        result.errors.append(
                            f"{skill_file}: CRITICAL: Description must be a simple one-line string. "
                            "Usage of '|' (literal) or '>' (folded) block styles is forbidden."
                        )

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
                    field_errors = _validate_metadata_fields(frontmatter, "skill")
                    result.errors.extend([f"{skill_file}: {e}" for e in field_errors])

                    # 2. Name Validation
                    if "name" not in frontmatter:
                        result.errors.append(
                            f"{skill_file}: Missing required field 'name'"
                        )
                    else:
                        name_errors, name_warnings = _validate_name(
                            frontmatter["name"], skill_dir
                        )
                        result.errors.extend(
                            [f"{skill_file}: {e}" for e in name_errors]
                        )
                        result.warnings.extend(
                            [f"{skill_file}: {e}" for e in name_warnings]
                        )

                    # 3. Description Validation
                    if "description" not in frontmatter:
                        result.errors.append(
                            f"{skill_file}: Missing required field 'description'"
                        )
                    else:
                        desc_errors, desc_warnings = _validate_description(
                            frontmatter["description"], "skill"
                        )
                        result.errors.extend(
                            [f"{skill_file}: {e}" for e in desc_errors]
                        )
                        result.warnings.extend(
                            [f"{skill_file}: {e}" for e in desc_warnings]
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

        # Validate agents
        agent_files = filter_excluded_paths(list(self.plugins_dir.rglob("agents/*.md")))
        if agent_files:
            print(f"  Validating {len(agent_files)} agents...")
            for agent_file in agent_files:
                try:
                    content = agent_file.read_text()
                    if not content.startswith("---"):
                        result.errors.append(f"{agent_file}: Missing YAML frontmatter")
                        continue

                    end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                    if not end_match:
                        result.errors.append(
                            f"{agent_file}: Missing closing frontmatter marker"
                        )
                        continue

                    fm_text = content[3 : 3 + end_match.start()]
                    try:
                        frontmatter = yaml.safe_load(fm_text)
                        if not isinstance(frontmatter, dict):
                            raise ValueError("Frontmatter is not a dict")
                    except Exception as e:
                        result.errors.append(
                            f"{agent_file}: Invalid YAML frontmatter: {e}"
                        )
                        continue

                    # Field Validation
                    field_errors = _validate_metadata_fields(frontmatter, "agent")
                    result.errors.extend([f"{agent_file}: {e}" for e in field_errors])

                    # Name Validation (required for agents)
                    if "name" not in frontmatter:
                        result.errors.append(
                            f"{agent_file}: Missing required field 'name'"
                        )
                    else:
                        name_errors, name_warnings = _validate_name(frontmatter["name"])
                        result.errors.extend(
                            [f"{agent_file}: {e}" for e in name_errors]
                        )
                        result.warnings.extend(
                            [f"{agent_file}: {e}" for e in name_warnings]
                        )

                except Exception as e:
                    result.errors.append(f"{agent_file}: Error processing: {e}")

        # Validate commands
        command_files = filter_excluded_paths(
            list(self.plugins_dir.rglob("commands/*.md"))
        )
        if command_files:
            print(f"  Validating {len(command_files)} commands...")
            for cmd_file in command_files:
                try:
                    content = cmd_file.read_text()
                    if not content.startswith("---"):
                        result.errors.append(f"{cmd_file}: Missing YAML frontmatter")
                        continue

                    end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                    if not end_match:
                        result.errors.append(
                            f"{cmd_file}: Missing closing frontmatter marker"
                        )
                        continue

                    fm_text = content[3 : 3 + end_match.start()]
                    try:
                        frontmatter = yaml.safe_load(fm_text)
                        if not isinstance(frontmatter, dict):
                            raise ValueError("Frontmatter is not a dict")
                    except Exception as e:
                        result.errors.append(
                            f"{cmd_file}: Invalid YAML frontmatter: {e}"
                        )
                        continue

                    # Field Validation
                    field_errors = _validate_metadata_fields(frontmatter, "command")
                    result.errors.extend([f"{cmd_file}: {e}" for e in field_errors])

                    # Description Validation (required for commands)
                    if "description" not in frontmatter:
                        result.errors.append(
                            f"{cmd_file}: Missing required field 'description'"
                        )
                    else:
                        # Commands don't require "Use when" pattern (more flexible format)
                        desc_errors, desc_warnings = _validate_description(
                            frontmatter["description"], "command"
                        )
                        result.errors.extend([f"{cmd_file}: {e}" for e in desc_errors])
                        result.warnings.extend(
                            [f"{cmd_file}: {e}" for e in desc_warnings]
                        )

                except Exception as e:
                    result.errors.append(f"{cmd_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def _resolve_skill_path(self, path: str, skill_root: Path, file_dir: Path) -> Path:
        try:
            parsed = Path(path)
        except Exception:
            return (file_dir / path).resolve()

        if parsed.parts and parsed.parts[0] in {"scripts", "assets", "references"}:
            return (skill_root / path).resolve()

        return (file_dir / path).resolve()

    def _path_within_skill(self, path: Path, skill_root: Path) -> bool:
        try:
            path.relative_to(skill_root)
            return True
        except ValueError:
            return False

    def validate_links(self) -> None:
        """Validate markdown links and references"""
        result = ValidationResult("Link Validation", True)

        print("Phase 2: Link Validation")
        print("-" * 70)

        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        backtick_pattern = re.compile(r"`(references|assets|scripts)/[^`]+`")
        cross_ref_pattern = re.compile(r"\.\./[^/]+/skill")

        md_files = filter_excluded_paths(list(self.plugins_dir.rglob("*.md")))
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

                    target_path = self._resolve_skill_path(link, skill_root, file_dir)
                    if "#" in str(target_path):
                        target_path = Path(str(target_path).split("#")[0])

                    if not target_path.exists():
                        result.errors.append(f"{md_file}: Broken link -> {link}")
                    elif not self._path_within_skill(target_path, skill_root):
                        is_readme = md_file.name.lower() in ["readme.md", "readme"]
                        if not is_readme:
                            result.errors.append(
                                f"{md_file}: Cross-skill link detected -> {link}"
                            )

                # Validate backtick paths
                # Template/documentation files may reference optional files
                is_template = "templates" in str(md_file) or "assets" in str(md_file)
                for match in backtick_pattern.finditer(content):
                    path = match.group(0).strip("`")
                    target = self._resolve_skill_path(path, skill_root, file_dir)
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
                        result.errors.append(
                            f"{md_file}: Cross-skill reference found -> {match.group(0)}"
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

        command_files = filter_excluded_paths(
            list(self.plugins_dir.rglob("commands/*.md"))
        )
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
                    desc_match = re.search(
                        r'description:\s*["\'](.*?)["\']', content, re.DOTALL
                    )
                    if desc_match and len(desc_match.group(1)) > 200:
                        result.warnings.append(
                            f"{cmd_file}: Description is too long (>200 chars). "
                            "Keep descriptions semantic and terse for optimal AI routing."
                        )

            except Exception as e:
                result.errors.append(f"{cmd_file}: Error processing: {e}")

        agent_files = filter_excluded_paths(list(self.plugins_dir.rglob("agents/*.md")))
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

        agent_files = filter_excluded_paths(list(self.plugins_dir.rglob("agents/*.md")))
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

    def validate_zero_token_retention(self) -> None:
        """Phase 7: Check if wrapper commands utilize disable-model-invocation"""
        result = ValidationResult("Zero-Token Retention Check", True)

        print("Phase 7: Zero-Token Retention Validation (2026 Quota Optimization)")
        print("-" * 70)

        command_files = filter_excluded_paths(
            list(self.plugins_dir.rglob("commands/*.md"))
        )
        print(f"  Checking {len(command_files)} commands...")

        for cmd_file in command_files:
            try:
                content = cmd_file.read_text()
                if not content.startswith("---"):
                    continue

                end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                if not end_match:
                    continue

                fm_text = content[3 : 3 + end_match.start()]
                frontmatter = yaml.safe_load(fm_text)

                if not isinstance(frontmatter, dict):
                    continue

                cmd_name = cmd_file.stem
                allowed_tools = frontmatter.get("allowed-tools", [])
                has_skill_invocation = False
                has_disable_model = frontmatter.get("disable-model-invocation", False)

                # Check if command delegates to a Skill
                if isinstance(allowed_tools, list):
                    for tool in allowed_tools:
                        if "Skill(" in str(tool):
                            has_skill_invocation = True
                            break

                # If command wraps a skill but lacks zero-token retention
                if has_skill_invocation and not has_disable_model:
                    result.warnings.append(
                        f"{cmd_file}: Command '{cmd_name}' wraps a Skill but missing "
                        f"'disable-model-invocation: true'. Add this to save ~15k tokens of context."
                    )

            except Exception as e:
                result.errors.append(f"{cmd_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_description_modalities(self) -> None:
        """Phase 8: Validate description modalities follow 2026 Cat Toolkit convention"""
        result = ValidationResult("Description Modality Validation", True)

        print("Phase 8: Description Modality Validation (2026 Modal Pattern)")
        print("-" * 70)

        skill_files = list(self.plugins_dir.rglob("SKILL.md")) + list(
            self.plugins_dir.rglob("skill.md")
        )
        print(f"  Checking {len(skill_files)} skills...")

        # Expected modality patterns by plugin tier (2026 convention)
        # Standard Pattern: {CAPABILITY}. Use when {TRIGGERS}.
        # Enhanced Pattern: {CAPABILITY}. {MODAL} Use when {TRIGGERS}.
        tier_guidance = {
            "sys-core": "Enhanced Pattern (MUST/PROACTIVELY/SHOULD) recommended for internal standards",
            "sys-builder": "Enhanced Pattern (PROACTIVELY/MUST) recommended for orchestration",
            "sys-cognition": "Standard Pattern (USE when) or Enhanced (SHOULD)",
            "sys-research": "Standard Pattern (USE when) recommended",
            "sys-meta": "Enhanced Pattern (SHOULD) recommended for best practices",
            "sys-multimodal": "Standard Pattern (USE when) recommended",
            "sys-edge": "Standard Pattern (USE when) recommended",
            "llm-application-dev": "Standard Pattern (USE when) recommended",
        }

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

                if not isinstance(frontmatter, dict):
                    continue

                skill_name = frontmatter.get("name", "")
                description = frontmatter.get("description", "")

                if not description:
                    continue

                # Find which plugin this skill belongs to
                skill_plugin = None
                for plugin_name in tier_guidance.keys():
                    if f"/plugins/{plugin_name}/" in str(skill_file):
                        skill_plugin = plugin_name
                        break

                # Check for Enhanced Pattern
                has_enhanced = bool(
                    re.search(
                        r"\.\s*(MUST|PROACTIVELY|SHOULD)\s+Use when",
                        description,
                        re.IGNORECASE,
                    )
                )
                has_standard = (
                    bool(re.search(r"\.\s*Use when", description, re.IGNORECASE))
                    and not has_enhanced
                )

                # Provide tier-specific guidance
                if skill_plugin:
                    expected_type = tier_guidance.get(skill_plugin, "")

                    # Check if using Enhanced in non-infrastructure context (warning)
                    is_infrastructure = skill_plugin in [
                        "sys-core",
                        "sys-builder",
                        "sys-meta",
                    ]
                    if has_enhanced and not is_infrastructure:
                        result.warnings.append(
                            f"{skill_file}: Skill '{skill_name}' uses Enhanced Pattern but '{skill_plugin}' "
                            f"is not an infrastructure plugin. Consider Standard Pattern for portability. "
                            f"Guidance: {expected_type}"
                        )

                    # Check if using Standard in infrastructure context (info)
                    if has_standard and is_infrastructure:
                        result.info.append(
                            f"{skill_file}: Skill '{skill_name}' in '{skill_plugin}' uses Standard Pattern. "
                            f"Consider Enhanced Pattern (MUST/PROACTIVELY/SHOULD) for internal toolkit standards. "
                            f"Guidance: {expected_type}"
                        )

            except Exception as e:
                result.errors.append(f"{skill_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_permission_leakage(self) -> None:
        """Phase 9: Validate that permissionMode is only used in Agents, not Skills/Commands"""
        result = ValidationResult("Permission Leakage Validation", True)

        print("Phase 9: Permission Leakage Validation (2026 Security)")
        print("-" * 70)

        # Check Skills for permissionMode (CRITICAL: Agent-only field)
        skill_files = list(self.plugins_dir.rglob("SKILL.md")) + list(
            self.plugins_dir.rglob("skill.md")
        )
        print(f"  Checking {len(skill_files)} skills...")

        for skill_file in skill_files:
            try:
                content = skill_file.read_text()
                if "permissionMode" in content:
                    result.errors.append(
                        f"{skill_file}: CRITICAL - Skills cannot define 'permissionMode'. "
                        f"This is an Agent-exclusive field. Remove from frontmatter."
                    )
            except Exception as e:
                result.errors.append(f"{skill_file}: Error processing: {e}")

        # Check Commands for permissionMode (CRITICAL: Agent-only field)
        command_files = filter_excluded_paths(
            list(self.plugins_dir.rglob("commands/*.md"))
        )
        print(f"  Checking {len(command_files)} commands...")

        for cmd_file in command_files:
            try:
                content = cmd_file.read_text()
                if "permissionMode" in content:
                    result.errors.append(
                        f"{cmd_file}: CRITICAL - Commands cannot define 'permissionMode'. "
                        f"This is an Agent-exclusive field. Commands inherit permissions from calling context."
                    )
            except Exception as e:
                result.errors.append(f"{cmd_file}: Error processing: {e}")

        # Check Agent tools allowlists (WARN if missing - security risk)
        agent_files = filter_excluded_paths(list(self.plugins_dir.rglob("agents/*.md")))
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

                if isinstance(frontmatter, dict) and "tools" not in frontmatter:
                    agent_name = agent_file.stem
                    result.warnings.append(
                        f"{agent_file}: Agent '{agent_name}' missing 'tools' allowlist. "
                        f"Agent inherits ALL tools from parent (security risk). "
                        f"2026 Standard: Always specify explicit tools allowlist."
                    )
            except Exception as e:
                result.errors.append(f"{agent_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_command_structure(self) -> None:
        """Phase 10: Validate Commands follow 2026 structure standards"""
        result = ValidationResult("Command Structure Validation", True)

        print("Phase 10: Command Structure Validation (2026 Standards)")
        print("-" * 70)

        command_files = filter_excluded_paths(
            list(self.plugins_dir.rglob("commands/*.md"))
        )
        print(f"  Checking {len(command_files)} commands...")

        for cmd_file in command_files:
            try:
                content = cmd_file.read_text()
                if not content.startswith("---"):
                    continue

                end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                if not end_match:
                    continue

                fm_text = content[3 : 3 + end_match.start()]
                frontmatter = yaml.safe_load(fm_text)

                if not isinstance(frontmatter, dict):
                    continue

                cmd_name = cmd_file.stem
                description = frontmatter.get("description", "")
                allowed_tools = frontmatter.get("allowed-tools", [])
                argument_hint = frontmatter.get("argument-hint", "")

                # Check 1: Commands should have argument-hint for user guidance
                if not argument_hint:
                    result.warnings.append(
                        f"{cmd_file}: Command '{cmd_name}' missing 'argument-hint'. "
                        f"2026 Standard: Always include argument-hint for user guidance."
                    )

                # Check 2: Commands should explicitly orchestrate Skills (no "magic" routing)
                if isinstance(allowed_tools, list):
                    skill_invocations = [t for t in allowed_tools if "Skill(" in str(t)]
                    if not skill_invocations:
                        # Check if command body has explicit skill references
                        body_content = content[end_match.end() + 3 :]
                        if not re.search(r"Skill\(|@[\w-]+|/[\w-]+", body_content):
                            result.warnings.append(
                                f"{cmd_file}: Command '{cmd_name}' has no explicit skill orchestration. "
                                f"2026 Standard: Commands should explicitly list Skills in allowed-tools "
                                f"or reference them by name in the command body."
                            )

                # Check 3: Check for square bracket syntax (deprecated)
                content_str = str(allowed_tools) + str(frontmatter.get("tools", ""))
                if "[" in content_str and "]" in content_str:
                    # Check for tool restrictions using brackets (deprecated syntax)
                    if re.search(r"\w+\[[^\]]+\]", str(allowed_tools)):
                        result.errors.append(
                            f"{cmd_file}: CRITICAL - Command '{cmd_name}' uses square bracket "
                            f"tool restriction syntax (e.g., Bash[python]). 2026 Standard: "
                            f"Use parentheses syntax: Bash(python:*)"
                        )

            except Exception as e:
                result.errors.append(f"{cmd_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_agent_security(self) -> None:
        """Phase 13: Validate agents have explicit security boundaries"""
        result = ValidationResult("Agent Security Validation", True)

        print("Phase 13: Agent Security Validation (2026 Standard)")
        print("-" * 70)

        agent_files = filter_excluded_paths(list(self.plugins_dir.rglob("agents/*.md")))
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

                if not isinstance(frontmatter, dict):
                    continue

                agent_name = frontmatter.get("name", agent_file.stem)
                has_tools = "tools" in frontmatter
                has_disallowed = "disallowedTools" in frontmatter

                # Check for security boundaries
                if not has_tools and not has_disallowed:
                    result.errors.append(
                        f"{agent_file}: Agent '{agent_name}' lacks explicit security boundaries. "
                        f"Agent inherits ALL tools from parent (CRITICAL security risk). "
                        f"2026 Standard: Specify 'tools' allowlist or 'disallowedTools' blocklist."
                    )
                elif has_tools:
                    tools = frontmatter.get("tools", [])
                    if not tools or (isinstance(tools, list) and len(tools) == 0):
                        result.errors.append(
                            f"{agent_file}: Agent '{agent_name}' has empty 'tools' allowlist. "
                            f"Empty allowlist = no tools available. "
                            f"2026 Standard: Specify explicit tools or use disallowedTools."
                        )

                # Check for READ-ONLY claims without enforcement
                body_lower = content[end_match.end() + 6 :].lower()
                if "read-only" in body_lower or "read only" in body_lower:
                    dangerous_tools = ["Write", "Edit", "Bash"]
                    has_restriction = has_disallowed or (
                        has_tools
                        and any(
                            tool not in frontmatter["tools"]
                            for tool in dangerous_tools
                        )
                    )
                    if not has_restriction:
                        result.errors.append(
                            f"{agent_file}: Agent '{agent_name}' claims 'READ-ONLY' but lacks enforcement. "
                            f"Add 'disallowedTools: [Write, Edit, Bash]' to enforce read-only operation."
                        )

            except Exception as e:
                result.errors.append(f"{agent_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_thin_wrappers(self) -> None:
        """Phase 14: Validate commands add unique value beyond skill invocation"""
        result = ValidationResult("Thin Wrapper Detection", True)

        print("Phase 14: Thin Wrapper Detection (2026 Standard)")
        print("-" * 70)

        command_files = filter_excluded_paths(
            list(self.plugins_dir.rglob("commands/*.md"))
        )
        print(f"  Checking {len(command_files)} commands...")

        skill_pattern = re.compile(r"use the \w+ skill", re.IGNORECASE)
        invoke_pattern = re.compile(r"Skill\(['\"]", re.IGNORECASE)

        for cmd_file in command_files:
            try:
                content = cmd_file.read_text()
                if not content.startswith("---"):
                    continue

                end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                if not end_match:
                    continue

                body = content[end_match.end() + 6 :]

                # Check for simple skill wrapper patterns
                skill_matches = skill_pattern.findall(body)
                invoke_matches = invoke_pattern.findall(body)

                # Count lines in body (excluding frontmatter)
                body_lines = [line for line in body.split("\n") if line.strip() and not line.strip().startswith("#")]
                line_count = len(body_lines)

                # Thin wrapper indicators:
                # 1. Single "Use the X skill" pattern
                # 2. Single Skill() invocation
                # 3. Less than 5 lines of actual content
                # 4. No bash/env injection (!` or $)
                has_bash_injection = "!`" in body or "$" in body
                has_questions = "AskUserQuestion" in body

                is_thin_wrapper = (
                    (skill_matches or invoke_matches)
                    and line_count < 5
                    and not has_bash_injection
                    and not has_questions
                )

                if is_thin_wrapper:
                    cmd_name = cmd_file.stem
                    result.warnings.append(
                        f"{cmd_file}: Command '{cmd_name}' appears to be a thin skill wrapper. "
                        f"2026 Standard: Commands should add unique value (bash injection, interactivity, batch processing). "
                        f"Consider deleting this command - the skill is auto-discoverable."
                    )

            except Exception as e:
                result.errors.append(f"{cmd_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_persona_language(self) -> None:
        """Phase 15: Validate skills and agents use protocol format, not persona"""
        result = ValidationResult("Persona Language Detection", True)

        print("Phase 15: Persona Language Detection (2026 Standard)")
        print("-" * 70)

        # Persona language patterns to detect
        persona_patterns = [
            (r"You are an?\s+\w+", "You are a/an [role]"),
            (r"I am an?\s+\w+", "I am a/an [role]"),
            (r"Act as an?\s+\w+", "Act as a/an [role]"),
            (r"Your role is?", "Your role"),
            (r"You are an?\s+\*\*Elite\*\*", "You are an **Elite**"),
            (r"You are an?\s+\*\*Senior\*\*", "You are a **Senior**"),
            (r"You specialize in", "You specialize in"),
        ]

        # Check skills
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

                body = content[end_match.end() + 6 :]

                for pattern, description in persona_patterns:
                    if re.search(pattern, body, re.IGNORECASE):
                        result.warnings.append(
                            f"{skill_file}: Detected persona language ({description}). "
                            f"2026 Standard: Use protocol format ('Follow this X-step process') "
                            f"instead of persona format ('You are an expert...'). "
                            f"See docs/guides/skills.md Section 1.6 for migration guide."
                        )
                        break  # Only report first persona pattern per file

            except Exception as e:
                result.errors.append(f"{skill_file}: Error processing: {e}")

        # Check agents (persona language less critical in agents, but still worth flagging)
        agent_files = filter_excluded_paths(list(self.plugins_dir.rglob("agents/*.md")))
        print(f"  Checking {len(agent_files)} agents...")

        for agent_file in agent_files:
            try:
                content = agent_file.read_text()
                if not content.startswith("---"):
                    continue

                end_match = re.search(r"^---$", content[3:], re.MULTILINE)
                if not end_match:
                    continue

                body = content[end_match.end() + 6 :]

                # More strict for agents - they should be config-only
                # Flag "You are" patterns as warnings (acceptable for minimal setup, but avoid narrative)
                if re.search(r"You are an?\s+\*\*[A-Z]\w+\*\*", body):
                    result.info.append(
                        f"{agent_file}: Agent uses elaborate persona (**Elite**, **Senior**, etc.). "
                        f"2026 Standard: Agents should be config-only. "
                        f"Keep agent body minimal (Core Purpose, Tool Access, Preloaded Skills)."
                    )

            except Exception as e:
                result.errors.append(f"{agent_file}: Error processing: {e}")

        print()
        self.log_result(result)

    def validate_emoji_usage(self) -> None:
        """Phase 16: Validate no emojis in documentation and code files"""
        result = ValidationResult("Emoji Usage Validation", True)

        print("Phase 16: Emoji Usage Detection (2026 Standard)")
        print("-" * 70)

        # Decorative emojis to detect (excludes text-like symbols)
        # Exclude: ✓ ✗ ✷ (commonly used as text markers)
        decorative_emoji_ranges = [
            r'[\U0001F300-\U0001F9FF]',        # Emoticons and picture emojis
            r'[\U0001F600-\U0001F64F]',        # Emoticons (smileys, people)
            r'[\U0001F300-\U0001F5FF]',        # Symbols & pictographs
            r'[\U0001F680-\U0001F6FF]',        # Transport & map symbols
            r'[\U0001F1E0-\U0001F1FF]',        # Flags
            r'[\u2600-\u26FF\u2700-\u27BF]',   # Misc symbols (excluding some)
        ]

        # Combined emoji regex pattern
        emoji_regex = '|'.join(f'({pattern})' for pattern in decorative_emoji_ranges)

        # Text-like symbols to exclude from emoji detection
        exclude_pattern = r'[✓✗√−×+•▪▫◼◻]'

        # Files to check
        file_patterns = [
            "SKILL.md",
            "skill.md",
            "*.md",
        ]

        files_checked = 0
        files_with_emojis = 0

        for pattern in file_patterns:
            for md_file in self.plugins_dir.rglob(pattern):
                # Skip attic
                if ".attic" in str(md_file):
                    continue

                try:
                    content = md_file.read_text(encoding="utf-8")

                    # Check for decorative emojis
                    matches = re.findall(emoji_regex, content, re.UNICODE)

                    # Filter out text-like symbols
                    decorative_emojis = []
                    for match in matches:
                        if isinstance(match, tuple):
                            # Check each captured group
                            for m in match:
                                if m and not re.search(exclude_pattern, m):
                                    decorative_emojis.append(m)
                        elif match and not re.search(exclude_pattern, match):
                            decorative_emojis.append(match)

                    if decorative_emojis:
                        files_with_emojis += 1
                        # Find line numbers
                        lines = content.split("\n")
                        emoji_lines = []
                        for i, line in enumerate(lines, 1):
                            # Check for emojis in this line (excluding text-like symbols)
                            line_matches = re.findall(emoji_regex, line, re.UNICODE)
                            line_emojis = []
                            for match in line_matches:
                                if isinstance(match, tuple):
                                    for m in match:
                                        if m and not re.search(exclude_pattern, m):
                                            line_emojis.append(m)
                                elif match and not re.search(exclude_pattern, match):
                                    line_emojis.append(match)

                            if line_emojis:
                                # Truncate line for display
                                display_line = line[:80] + "..." if len(line) > 80 else line
                                emoji_lines.append(
                                    f"  Line {i}: {', '.join(set(line_emojis))} in '{display_line}'"
                                )

                        if emoji_lines:
                            result.errors.append(
                                f"{md_file}: Contains {len(set(decorative_emojis))} decorative emoji(s).\n"
                                f"2026 Standard: Use text labels instead (e.g., 'BAD:', 'GOOD:', 'WARNING:', 'PREFERRED').\n"
                                f"Found at:\n" + "\n".join(emoji_lines[:5])  # Show first 5 occurrences
                            )

                    files_checked += 1

                except Exception as e:
                    result.errors.append(f"{md_file}: Error processing: {e}")

        print(f"  Checked {files_checked} markdown files")
        if files_with_emojis > 0:
            print(f"  Found decorative emojis in {files_with_emojis} file(s)")
        else:
            print(f"  No decorative emojis found")

        print()
        self.log_result(result)

    def validate_claude_plugin(self) -> None:
        """Phase 12: Run claude plugin validate on marketplace and each plugin"""
        result = ValidationResult("Claude Plugin Validation", True)

        print("Phase 12: Running claude plugin validate")
        print("-" * 70)

        import subprocess

        # Validate marketplace
        marketplace_path = self.root_dir / ".claude-plugin" / "marketplace.json"
        if marketplace_path.exists():
            print(f"  Validating marketplace: {marketplace_path}")
            try:
                proc = subprocess.run(
                    ["claude", "plugin", "validate", str(marketplace_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if proc.returncode != 0:
                    result.errors.append(
                        f"Marketplace validation failed (exit code {proc.returncode}):\n"
                        f"{proc.stdout}\n{proc.stderr}"
                    )
                else:
                    result.info.append("Marketplace validation passed")
            except subprocess.TimeoutExpired:
                result.errors.append("Marketplace validation timed out (>30s)")
            except FileNotFoundError:
                result.warnings.append(
                    "'claude' command not found - skipping marketplace validation"
                )
            except Exception as e:
                result.errors.append(f"Marketplace validation error: {e}")
        else:
            result.warnings.append(f"Marketplace not found at {marketplace_path}")

        # Validate each plugin
        plugin_json_files = list(self.plugins_dir.rglob(".claude-plugin/plugin.json"))
        print(f"  Validating {len(plugin_json_files)} plugins...")

        for plugin_json_path in plugin_json_files:
            plugin_name = plugin_json_path.parent.parent.name
            print(f"    - {plugin_name}")
            try:
                proc = subprocess.run(
                    ["claude", "plugin", "validate", str(plugin_json_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if proc.returncode != 0:
                    result.errors.append(
                        f"Plugin '{plugin_name}' validation failed (exit code {proc.returncode}):\n"
                        f"{proc.stdout}\n{proc.stderr}"
                    )
                else:
                    result.info.append(f"Plugin '{plugin_name}' validation passed")
            except subprocess.TimeoutExpired:
                result.errors.append(
                    f"Plugin '{plugin_name}' validation timed out (>30s)"
                )
            except FileNotFoundError:
                result.warnings.append(
                    "'claude' command not found - skipping plugin validations"
                )
                break  # Don't repeat this warning for each plugin
            except Exception as e:
                result.errors.append(f"Plugin '{plugin_name}' validation error: {e}")

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
            print("✓ All validators passed!")
        else:
            print("⚠️  Validation issues found")

        # Always show errors if any
        if self.report.total_errors > 0:
            print("\nERRORS:")
            for result in self.report.results:
                if result.errors:
                    print(f"\n  {result.name}:")
                    for error in result.errors:
                        print(f"    ✗ {error}")

        # Always show warnings if any
        if self.report.total_warnings > 0:
            print("\nWARNINGS:")
            for result in self.report.results:
                if result.warnings:
                    print(f"\n  {result.name}:")
                    for warning in result.warnings:
                        print(f"    ⚠️  {warning}")

        # Show info messages if any
        info_count = sum(len(r.info) for r in self.report.results)
        if info_count > 0:
            print("\nINFO:")
            for result in self.report.results:
                if result.info:
                    print(f"\n  {result.name}:")
                    for info in result.info:
                        print(f"    ℹ️  {info}")

        # Show recommendation to use --fix if there are issues
        if not self.report.all_passed:
            print("\n" + "=" * 70)
            print("💡 RECOMMENDATION")
            print("=" * 70)
            print("Run with --fix to automatically resolve fixable issues:")
            print()
            print("  uv run scripts/toolkit.py --fix")
            print()
            print("Or preview fixes first:")
            print("  uv run scripts/toolkit.py --fix --dry-run")
            print()
            print("=" * 70)

        print()
        print("=" * 70)


__all__ = [
    "ToolkitAnalyzer",
    "_validate_name",
    "_validate_description",
    "_validate_compatibility",
    "_validate_metadata_fields",
]
