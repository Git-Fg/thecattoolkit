#!/bin/bash
# Hook Script Linter
# Checks hook scripts for common issues, security problems, and best practices violations

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0
TIPS=0

# Usage
show_usage() {
  cat <<EOF
Usage: $0 [options] <hook-script.sh> [hook-script2.sh ...]

Checks hook scripts for:
  - Shebang presence and correctness
  - set -euo pipefail usage
  - Input reading from stdin
  - Proper error handling
  - Variable quoting (injection prevention)
  - Exit code usage
  - Hardcoded paths
  - Timeout considerations
  - Input validation
  - Security best practices

Options:
  -h, --help       Show this help message
  -v, --verbose    Show detailed output
  --severity LEVEL  Set minimum severity (error|warning|info)
  --fix             Attempt to auto-fix some issues
  --json            Output results in JSON format

Examples:
  $0 scripts/validate-bash.sh
  $0 -v scripts/*.sh
  $0 --json scripts/validate-write.sh
  $0 --severity warning scripts/*.sh
EOF
  exit 0
}

# Parse arguments
VERBOSE=false
SEVERITY="info"
OUTPUT_JSON=false
AUTO_FIX=false

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)
      show_usage
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    --severity)
      SEVERITY="$2"
      shift 2
      ;;
    --json)
      OUTPUT_JSON=true
      shift
      ;;
    --fix)
      AUTO_FIX=true
      shift
      ;;
    -*)
      echo "Unknown option: $1" >&2
      show_usage
      ;;
    *)
      break
      ;;
  esac
done

if [ $# -eq 0 ]; then
  echo "Error: No scripts provided" >&2
  echo ""
  show_usage
fi

# Helper functions
log_error() {
  echo -e "${RED}❌ $1${NC}" >&2
  ((ERRORS++))
}

log_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}" >&2
  ((WARNINGS++))
}

log_info() {
  if [ "$VERBOSE" = true ]; then
    echo -e "${BLUE}ℹ️  $1${NC}" >&2
  fi
}

log_tip() {
  echo -e "${CYAN}💡 $1${NC}" >&2
  ((TIPS++))
}

log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Check individual script
check_script() {
  local script="$1"
  local file_errors=0
  local file_warnings=0
  local file_tips=0

  echo -e "${BLUE}🔍 Linting: $script${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [ ! -f "$script" ]; then
    log_error "File not found"
    return 1
  fi

  # Check 1: Executable
  if [ ! -x "$script" ]; then
    log_warning "Script is not executable (chmod +x $script)"
    ((file_warnings++))
  else
    log_success "Script is executable"
  fi

  # Check 2: Shebang
  local first_line=$(head -1 "$script")
  if [[ ! "$first_line" =~ ^#!/ ]]; then
    log_error "Missing shebang (#!/bin/bash or #!/usr/bin/env bash)"
    ((file_errors++))
  elif [[ "$first_line" != "#!/bin/bash" ]] && [[ "$first_line" != "#!/usr/bin/env bash" ]]; then
    log_warning "Non-standard shebang: $first_line (use #!/bin/bash or #!/usr/bin/env bash)"
    ((file_warnings++))
  else
    log_success "Valid shebang: $first_line"
  fi

  # Check 3: set -euo pipefail
  if ! grep -q "set -euo pipefail" "$script"; then
    log_warning "Missing 'set -euo pipefail' (recommended for safety)"
    ((file_warnings++))

    if [ "$AUTO_FIX" = true ]; then
      log_info "Attempting to add set -euo pipefail..."
      # Add after shebang if not present
      if ! grep -q "set -euo pipefail" "$script"; then
        sed -i.tmp '2i set -euo pipefail' "$script" && rm -f "${script}.tmp"
        log_success "Added set -euo pipefail"
      fi
    fi
  else
    log_success "Has 'set -euo pipefail'"
  fi

  # Check 4: Reads from stdin
  if ! grep -qE "cat\s*\$|read\s+\w+" "$script" && ! grep -q '\$input\s*=\s*\$(' "$script"; then
    log_warning "Doesn't appear to read input from stdin"
    ((file_warnings++))

    log_tip "Hook scripts should read input from stdin using: input=\$(cat)"
  else
    log_success "Reads input from stdin"
  fi

  # Check 5: Uses jq for JSON parsing
  if grep -qE "tool_input|tool_name|tool_result|session_id" "$script"; then
    if ! grep -q "jq" "$script"; then
      log_warning "Parses hook input but doesn't use jq for JSON"
      ((file_warnings++))

      log_tip "Use jq to parse JSON: tool_name=\$(echo \"\$input\" | jq -r '.tool_name')"
    else
      log_success "Uses jq for JSON parsing"
    fi
  fi

  # Check 6: Unquoted variables (injection risk)
  if grep -E '\$[A-Za-z_][A-Za-z0-9_]*[^"]' "$script" | grep -v '#' | grep -v 'echo' | grep -q .; then
    log_error "Potentially unquoted variables detected (injection risk)"
    ((file_errors++))

    log_tip "Always quote variables: \"\$variable\" not \$variable"
    log_tip "Use quotes: \"\$file_path\", \"\$command\", etc."

    if [ "$VERBOSE" = true ]; then
      echo "  Examples found:"
      grep -E '\$[A-Za-z_][A-Za-z0-9_]*[^"]' "$script" | grep -v '#' | head -3 | sed 's/^/    /' >&2
    fi
  else
    log_success "No unquoted variables found"
  fi

  # Check 7: Hardcoded absolute paths
  if grep -E '^[^#]*/[a-z]+/|^[^#]*/[a-z]+/[a-z]+' "$script" | grep -v 'CLAUDE_PROJECT_DIR\|CLAUDE_PLUGIN_ROOT\|\$CLAUDE' | grep -q .; then
    log_warning "Hardcoded absolute paths detected"
    ((file_warnings++))

    log_tip "Use \$CLAUDE_PROJECT_DIR or \$CLAUDE_PLUGIN_ROOT for portability"

    if [ "$VERBOSE" = true ]; then
      echo "  Examples found:"
      grep -E '^[^#]*/[a-z]+/|^[^#]*/[a-z]+/[a-z]+' "$script" | grep -v 'CLAUDE_PROJECT_DIR\|CLAUDE_PLUGIN_ROOT\|\$CLAUDE' | head -3 | sed 's/^/    /' >&2
    fi
  else
    log_success "No hardcoded paths found"
  fi

  # Check 8: Uses environment variables
  if ! grep -q "CLAUDE_PROJECT_DIR\|CLAUDE_PLUGIN_ROOT" "$script"; then
    log_warning "Doesn't use \$CLAUDE_PROJECT_DIR or \$CLAUDE_PLUGIN_ROOT"
    ((file_warnings++))

    log_tip "Use \$CLAUDE_PLUGIN_ROOT for plugin-relative paths"
  else
    log_success "Uses environment variables for paths"
  fi

  # Check 9: Exit codes
  if ! grep -q "exit 0\|exit 1\|exit 2" "$script"; then
    log_warning "No explicit exit codes found"
    ((file_warnings++))

    log_tip "Hook scripts should exit with: exit 0 (success), exit 1 (error), exit 2 (blocking error)"
  else
    log_success "Has exit code statements"
  fi

  # Check 10: JSON output for decision hooks
  if grep -q "PreToolUse\|Stop" "$script"; then
    if ! grep -q "permissionDecision\|decision" "$script"; then
      log_warning "PreToolUse/Stop hook should output decision JSON"
      ((file_warnings++))

      log_tip "Output format: {\"decision\": \"allow|deny|ask\", \"reason\": \"...\"}"
    else
      log_success "Outputs decision JSON"
    fi
  fi

  # Check 11: Long-running commands
  if grep -E 'sleep [3-9][0-9]|[1-9][0-9][0-9]|while true|for.*in.*\$\(' "$script" | grep -v '#' | grep -q .; then
    log_warning "Potentially long-running code detected"
    ((file_warnings++))

    log_tip "Hooks should complete quickly (< 60s). Consider optimizing or adding timeouts."

    if [ "$VERBOSE" = true ]; then
      echo "  Examples found:"
      grep -E 'sleep [3-9][0-9]|[1-9][0-9][0-9]|while true' "$script" | grep -v '#' | head -3 | sed 's/^/    /' >&2
    fi
  else
    log_success "No long-running operations detected"
  fi

  # Check 12: Error messages to stderr
  if grep -qiE "error|Error|denied|Denied|failed|Failed" "$script"; then
    if ! grep -q '>&2' "$script"; then
      log_warning "Error messages should be written to stderr"
      ((file_warnings++))

      log_tip "Use: echo \"Error message\" >&2"
    else
      log_success "Writes errors to stderr"
    fi
  fi

  # Check 13: Input validation
  if ! grep -qE "if.*empty|if.*null|if.*-z|if.*==.*null" "$script"; then
    log_warning "No input validation detected"
    ((file_warnings++))

    log_tip "Consider validating inputs: if [ -z \"\$var\" ]; then ... fi"
  else
    log_success "Has input validation"
  fi

  # Check 14: Command injection prevention
  if grep -qE '\$.*|.*\$\(' "$script" | grep -v '#' | grep -E '(bash|sh|eval)' | grep -q .; then
    log_warning "Potential command injection risk"
    ((file_warnings++))

    log_tip "Avoid using eval or untrusted input in commands"

    if [ "$VERBOSE" = true ]; then
      echo "  Review these lines:"
      grep -nE '\$.*|.*\$\(' "$script" | grep -E '(bash|sh|eval)' | head -3 | sed 's/^/    /' >&2
    fi
  else
    log_success "No command injection risks detected"
  fi

  # Check 15: Usesjq for JSON safely
  if grep -q "jq" "$script"; then
    # Check for safe jq usage
    if ! grep -q "jq -r\|jq -e" "$script"; then
      log_info "Consider using 'jq -r' for raw strings or 'jq -e' for exit codes"
    fi

    # Check for jq without error handling
    if ! grep -q "|| true\|2>/dev/null" "$script"; then
      log_tip "Consider adding error handling for jq commands (|| true or 2>/dev/null)"
    fi
  fi

  # Check 16: Proper function usage
  local function_count=$(grep -c "^[[:space:]]*[a-zA-Z_][a-zA-Z0-9_]*() {" "$script" 2>/dev/null || echo "0")
  if [ "$function_count" -gt 0 ]; then
    log_success "Uses functions ($function_count found)"
  fi

  # Check 17: Comments
  local comment_count=$(grep -c "^#" "$script" 2>/dev/null || echo "0")
  if [ "$comment_count" -eq 0 ]; then
    log_tip "Consider adding comments to explain hook logic"
  else
    log_success "Has comments ($comment_count lines)"
  fi

  # Check 18: File descriptor handling
  if grep -qE '[0-9]>&|[0-9]<|' "$script"; then
    log_success "Handles file descriptors properly"
  fi

  # Summary for this file
  echo ""
  echo "Summary for $script:"
  echo "  Errors: $file_errors"
  echo "  Warnings: $file_warnings"
  echo "  Tips: $file_tips"
  echo ""

  if [ $file_errors -eq 0 ] && [ $file_warnings -eq 0 ]; then
    log_success "No issues found"
    return 0
  elif [ $file_errors -eq 0 ]; then
    log_warning "Passed with $file_warnings warning(s)"
    return 0
  else
    log_error "Failed with $file_errors error(s) and $file_warnings warning(s)"
    return 1
  fi
}

# Main execution
echo -e "${BLUE}🔎 Hook Script Linter${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$OUTPUT_JSON" = true ]; then
  echo "JSON output mode not yet implemented" >&2
  exit 1
fi

if [ "$VERBOSE" = true ]; then
  echo "Settings:"
  echo "  Verbose: Yes"
  echo "  Auto-fix: $([ "$AUTO_FIX" = true ] && echo Yes || echo No)"
  echo "  Severity threshold: $SEVERITY"
  echo ""
fi

total_errors=0
total_warnings=0
total_tips=0

for script in "$@"; do
  if [ -d "$script" ]; then
    log_info "Skipping directory: $script"
    continue
  fi

  if ! check_script "$script"; then
    ((total_errors++))
  fi

  # Note: We can't easily count per-file warnings/tips here
  # They are counted within check_script function
  echo ""
done

# Final summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}Final Summary${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Count totals by re-running checks without verbose
ERRORS=0
WARNINGS=0
TIPS=0

for script in "$@"; do
  if [ -d "$script" ]; then
    continue
  fi

  # Re-check with minimal output
  if ! bash -n "$script" 2>/dev/null; then
    ((ERRORS++))
  fi

  # Count warnings by checking for common issues
  if grep -q "^\s*set -euo pipefail" "$script" 2>/dev/null; then
    : # Has safe defaults
  else
    ((WARNINGS++))
  fi

  if grep -q "^\s*#\!" "$script" 2>/dev/null; then
    : # Has shebang
  else
    ((WARNINGS++))
  fi
done

echo "Total scripts checked: $#"
echo "Total errors: $ERRORS"
echo "Total warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo -e "${GREEN}✅ All scripts passed linting${NC}"
  exit 0
elif [ $ERRORS -eq 0 ]; then
  echo -e "${YELLOW}⚠️  All scripts passed with $WARNINGS warning(s)${NC}"
  exit 0
else
  echo -e "${RED}❌ $ERRORS error(s) found${NC}"
  exit 1
fi
