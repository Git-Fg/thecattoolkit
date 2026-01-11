#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
REPORT_FILE=""
QUIET=false
FINAL_EXIT_CODE=0

usage() {
  cat << EOF
Usage: $0 [OPTIONS]

Master validation script for the toolkit. Runs all validators and reports unified results.

OPTIONS:
  --report FILE   Write report to FILE (in addition to stdout)
  --quiet         Minimal output (only errors)
  --help          Show this help message

VALIDATORS RUN:
  1. glue-detector.sh       - Glue code detection
  2. link-validator.sh      - Broken link detection
  3. frontmatter-validator.sh - Frontmatter compliance
  4. fork-bloat-validator.sh   - 2026 Inline-First fork usage
  5. askuser-leakage-validator.sh - 2026 Autonomous Agent AskUserQuestion checks

EXIT CODES:
  0 - All validators passed
  1 - One or more validators found critical issues
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --report)
      REPORT_FILE="$2"
      shift 2
      ;;
    --quiet)
      QUIET=true
      shift
      ;;
    --help)
      usage
      ;;
    *)
      echo "Unknown option: $1"
      usage
      ;;
  esac
done

cd "$ROOT_DIR"

log() {
  local msg="$1"
  echo "$msg"
  [[ -n "$REPORT_FILE" ]] && echo "$msg" >> "$REPORT_FILE"
}

run_validator() {
  local name="$1"
  local script="$2"
  local exit_code=0
  
  log ""
  log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  log "🔍 Running: $name"
  log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  log ""
  
  if [[ -x "$script" ]]; then
    local output
    if [[ "$QUIET" == "true" ]]; then
      output=$("$script" --quiet 2>&1) || exit_code=$?
    else
      output=$("$script" 2>&1) || exit_code=$?
    fi
    log "$output"
    
    if [[ $exit_code -ne 0 ]]; then
      FINAL_EXIT_CODE=1
    fi
  else
    log "[ERROR] Script not found or not executable: $script"
    FINAL_EXIT_CODE=1
  fi
}

if [[ -n "$REPORT_FILE" ]]; then
  > "$REPORT_FILE"
fi

log "╔══════════════════════════════════════════════════════════════════════════════╗"
log "║                        TOOLKIT VALIDATION REPORT                             ║"
log "║                        $(date '+%Y-%m-%d %H:%M:%S')                                  ║"
log "╚══════════════════════════════════════════════════════════════════════════════╝"

run_validator "Glue Code Detector" "$SCRIPT_DIR/glue-detector.sh"
run_validator "Link Validator" "$SCRIPT_DIR/link-validator.sh"
run_validator "Frontmatter Validator" "$SCRIPT_DIR/frontmatter-validator.sh"
run_validator "Fork-Bloat Validator" "$SCRIPT_DIR/fork-bloat-validator.sh"
run_validator "AskUser-Leakage Validator" "$SCRIPT_DIR/askuser-leakage-validator.sh"

log ""
log "╔══════════════════════════════════════════════════════════════════════════════╗"
if [[ $FINAL_EXIT_CODE -eq 0 ]]; then
  log "║                    ✅ ALL VALIDATORS PASSED                                  ║"
else
  log "║                    ❌ VALIDATION ISSUES FOUND                                ║"
fi
log "╚══════════════════════════════════════════════════════════════════════════════╝"

if [[ -n "$REPORT_FILE" ]]; then
  log ""
  log "Report saved to: $REPORT_FILE"
fi

exit $FINAL_EXIT_CODE
