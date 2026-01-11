# Cat Toolkit Analysis Scripts

Unified Python-based analysis and validation suite for Cat Toolkit plugins.

## 🚀 Usage

### Quick Start

```bash
# Using uv (recommended)
./scripts/analyze.sh

# Or directly with uv
uv run python scripts/toolkit-analyzer.py

# With python3 fallback
python3 scripts/toolkit-analyzer.py
```

### Options

```bash
# Output JSON format
./scripts/analyze.sh --json

# Specify root directory
python scripts/toolkit-analyzer.py --root-dir /path/to/cattoolkit

# Get help
python scripts/toolkit-analyzer.py --help
```

## 🔍 What It Does

The unified analyzer performs 5 comprehensive validation phases:

### Phase 1: Frontmatter Validation
- Validates YAML frontmatter in skills, commands, and agents
- Checks required fields (name, description)
- Validates description patterns (USE when, MUST USE when, etc.)
- Verifies allowed-tools and other frontmatter fields

### Phase 2: Link Validation
- Detects broken markdown links
- Validates backtick path references
- Checks for cross-skill references (anti-pattern)
- Identifies @[file] syntax misuse

### Phase 3: Glue Code Detection
- Finds large command files (>10 lines)
- Detects high delegation patterns in agents
- Identifies wrapper agents
- Checks for cross-plugin coupling
- Finds AskUserQuestion in skills (anti-pattern)

### Phase 4: Fork-Bloat Validation (2026 Inline-First)
- Identifies skills with unnecessary `context: fork`
- Validates against 2026 Inline-First principles
- Suggests inline execution for simple tasks

### Phase 5: AskUser-Leakage Validation (2026 Autonomous Agents)
- Detects AskUserQuestion in worker agents
- Validates permissionMode configurations
- Enforces 2026 autonomous execution standards

## 📊 Example Output

```
======================================================================
🔍 Cat Toolkit Plugin Analyzer & Validator
======================================================================

📋 Phase 1: Frontmatter Validation
----------------------------------------------------------------------
  Validating 12 skills...

🔗 Phase 2: Link Validation
----------------------------------------------------------------------
  Checking 45 markdown files...

🔗 Phase 3: Glue Code Detection
----------------------------------------------------------------------
  Checking 8 command files...

⚡ Phase 4: Fork-Bloat Validation (2026 Inline-First)
----------------------------------------------------------------------
  Checking 12 skills...

🤖 Phase 5: AskUser-Leakage Validation (2026 Autonomous Agents)
----------------------------------------------------------------------
  Checking 15 agents...

======================================================================
📊 VALIDATION SUMMARY
======================================================================
Validators Run: 5
Total Errors: 0
Total Warnings: 3

✅ All validators passed!
```

## 📦 Installation

### With uv (Recommended)

```bash
# Install uv if not already installed
# Then install dependencies
uv pip install pyyaml

# Run analyzer
uv run python scripts/toolkit-analyzer.py
```

### With pip

```bash
pip3 install --user pyyaml
python3 scripts/toolkit-analyzer.py
```

## 🔄 Continuous Integration

```bash
# Check for errors (exit code 1 if issues found)
./scripts/analyze.sh

# Or check specific output
if ./scripts/analyze.sh --json | jq -e '.all_passed' > /dev/null; then
  echo "✅ All checks passed"
else
  echo "❌ Issues found"
  exit 1
fi
```

## 🛠️ Requirements

- Python 3.7+
- PyYAML

Install with:
```bash
uv pip install pyyaml
```

## 📝 Exit Codes

- `0` - All validators passed
- `1` - One or more validators found issues

## 🎯 Migration from Old Scripts

This unified script replaces:
- `toolkit-lint.sh` (master orchestrator)
- `frontmatter-validator.sh`
- `link-validator.sh`
- `glue-detector.sh`
- `fork-bloat-validator.sh`
- `askuser-leakage-validator.sh`
- `marketplace-validator.js`
- `run-full-validation.js`
- `integration-tester.js`

All functionality is now in a single, maintainable Python script.

## 🤝 Contributing

To add new validation checks:

1. Add a new `validate_<check_name>()` method to the `ToolkitAnalyzer` class
2. Call it from `validate_all()`
3. Follow the pattern of returning a `ValidationResult` object

## 📄 License

Part of the Cat Toolkit project. See main project license.

---

**Built with ❤️ for the Cat Toolkit ecosystem**
