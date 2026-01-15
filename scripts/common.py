"""
Common constants, dataclasses, and utilities for the Cat Toolkit analyzer.
Shared by validators.py and fixers.py.
"""

import re
import unicodedata
from pathlib import Path
from typing import List, Set, Tuple
from dataclasses import dataclass, field

from ruamel.yaml import YAML

# --- Validation Constants ---
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500

# Hardcore naming regex - violation causes CLI crash
# Pattern: lowercase alphanumeric, hyphens allowed, no start/end hyphen, no consecutive hyphens
NAME_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")

# Allowed frontmatter fields per CLAUDE.md and component type
# Base fields that apply to all components
ALLOWED_FIELDS_BASE = {
    "name",
    "description",
    "license",
    "compatibility",
    "version",
    "author",
}

# Component-specific allowed fields
ALLOWED_FIELDS_SKILL = ALLOWED_FIELDS_BASE | {
    "allowed-tools",
    "context",
    "user-invocable",
    "disable-model-invocation",
    "agent",  # Valid when context: fork (per CLAUDE.md line 1358-1361)
}

ALLOWED_FIELDS_AGENT = ALLOWED_FIELDS_BASE | {
    "tools",
    "skills",
    "agent",  # For fork context skills
}

ALLOWED_FIELDS_COMMAND = ALLOWED_FIELDS_BASE | {
    "allowed-tools",
    "disable-model-invocation",
    "argument-hint",
}

# Legacy: Keep ALLOWED_FIELDS for backward compatibility (union of all)
ALLOWED_FIELDS = ALLOWED_FIELDS_SKILL | ALLOWED_FIELDS_AGENT | ALLOWED_FIELDS_COMMAND

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

# Directories to exclude from validation
# .claude/ is a local workspace folder for plugin development (not part of the marketplace)
EXCLUDED_DIRS = {".claude", ".attic", ".git", "__pycache__", "node_modules"}


def filter_excluded_paths(paths: List[Path]) -> List[Path]:
    """Filter out paths that are inside excluded directories."""
    return [p for p in paths if not any(excl in p.parts for excl in EXCLUDED_DIRS)]


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


@dataclass
class FixResult:
    """Result of a fix operation."""

    file_path: str
    fixed: bool
    changes: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# Initialize ruamel.yaml for round-trip preservation
_ruamel_yaml = YAML()
_ruamel_yaml.preserve_quotes = True
_ruamel_yaml.width = 4096  # Prevent unwanted line wrapping
_ruamel_yaml.indent(mapping=2, sequence=4, offset=2)


def clean_description_text(text: str) -> str:
    """
    Sanitizes string: removes newlines, double spaces, special chars,
    and ensures it's a tight single line.
    """
    if not text:
        return ""

    # 1. Replace newlines and tabs with spaces
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # 2. Remove illegal/invisible special characters (control characters)
    text = "".join(ch for ch in text if ch.isprintable())

    # 3. Collapse multiple spaces into one and strip edges
    text = " ".join(text.split())

    # 4. Ensure it ends with proper punctuation
    if text and not text.endswith((".", "!", "?")):
        text += "."

    return text


def normalize_name(name: str) -> str:
    """Normalize name to lowercase kebab-case."""
    if not name:
        return ""
    return name.lower().replace("_", "-").strip()


def normalize_tool_syntax(tools_list: list) -> list:
    """Convert deprecated square bracket syntax to parentheses."""
    normalized = []
    for tool in tools_list:
        if isinstance(tool, str):
            # Convert Bash[python] -> Bash(python:*)
            match = re.match(r"^(\w+)\[([^\]]+)\]$", tool)
            if match:
                tool_name = match.group(1)
                params = match.group(2)
                # Split multiple params and convert each
                param_parts = [p.strip() for p in params.split(",")]
                for param in param_parts:
                    if ":" not in param:
                        param = f"{param}:*"
                    normalized.append(f"{tool_name}({param})")
            else:
                normalized.append(tool)
        else:
            normalized.append(tool)
    return normalized


__all__ = [
    # Constants
    "MAX_NAME_LENGTH",
    "MAX_DESCRIPTION_LENGTH",
    "MAX_COMPATIBILITY_LENGTH",
    "NAME_PATTERN",
    "ALLOWED_FIELDS_BASE",
    "ALLOWED_FIELDS_SKILL",
    "ALLOWED_FIELDS_AGENT",
    "ALLOWED_FIELDS_COMMAND",
    "ALLOWED_FIELDS",
    "VALID_TOOLS",
    "KNOWN_CUSTOM_TOOLS",
    "MCP_TOOL_PATTERN",
    "EXCLUDED_DIRS",
    # Dataclasses
    "ValidationResult",
    "ValidatorReport",
    "PluginComponent",
    "CrossPluginLink",
    "FixResult",
    # Utilities
    "filter_excluded_paths",
    "clean_description_text",
    "normalize_name",
    "normalize_tool_syntax",
    # YAML instance
    "_ruamel_yaml",
]
