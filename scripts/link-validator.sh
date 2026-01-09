#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
QUIET=false
EXIT_CODE=0

usage() {
  echo "Usage: $0 [--quiet]"
  echo "  --quiet  Only output critical errors"
  exit 0
}

[[ "${1:-}" == "--help" ]] && usage
[[ "${1:-}" == "--quiet" ]] && QUIET=true

log_info() { [[ "$QUIET" == "false" ]] && echo "[INFO] $1"; }
log_warn() { echo "[WARNING] $1"; }
log_error() { echo "[CRITICAL] $1"; EXIT_CODE=1; }

echo "=== Link Validator ==="
echo

cd "$ROOT_DIR"

validate_markdown_links() {
  local file="$1"
  local dir
  dir=$(dirname "$file")
  
  local matches
  matches=$(grep -oE '\[[^\]]+\]\([^)]+\)' "$file" 2>/dev/null || true)
  if [[ -n "$matches" ]]; then
    while IFS= read -r match; do
      local link
      link=$(echo "$match" | sed -E 's/.*\]\(([^)]+)\).*/\1/')
      
      [[ "$link" =~ ^https?:// ]] && continue
      [[ "$link" =~ ^# ]] && continue
      [[ "$link" =~ ^file:// ]] && continue
      [[ "$link" =~ ^\$ ]] && continue
      
      local target_path="$dir/$link"
      target_path=$(echo "$target_path" | sed 's/#.*//')
      
      if [[ ! -e "$target_path" ]]; then
        log_error "$file: Broken link -> $link"
      fi
    done <<< "$matches"
  fi
}

validate_backtick_paths() {
  local file="$1"
  # Find the Skill Root (directory containing SKILL.md)
  local skill_root="$file"
  while [[ "$skill_root" != "/" && "$skill_root" != "." ]]; do
    if [[ -f "$skill_root/SKILL.md" ]]; then
      break
    fi
    skill_root=$(dirname "$skill_root")
  done
  
  # If no SKILL.md found, default to file dir (fallback)
  if [[ ! -f "$skill_root/SKILL.md" ]]; then
    skill_root=$(dirname "$file")
  fi
  
  local matches
  matches=$(grep -oE '`(references|assets|scripts)/[^`]+`' "$file" 2>/dev/null || true)
  if [[ -n "$matches" ]]; then
    while IFS= read -r match; do
      local path
      path=$(echo "$match" | tr -d '`')
      
      # Check relative to Skill Root
      if [[ ! -e "$skill_root/$path" ]]; then
        # Also check relative to file (just in case)
        local dir
        dir=$(dirname "$file")
        if [[ ! -e "$dir/$path" ]]; then
             log_error "$file: Broken backtick path -> $path (checked relative to skill root '$skill_root')"
        fi
      fi
    done <<< "$matches"
  fi
}

validate_all_skill_files() {
  log_info "Checking all markdown files within skills..."
  
  while IFS= read -r -d '' skill_dir; do
    while IFS= read -r -d '' file; do
      validate_markdown_links "$file"
      validate_backtick_paths "$file"
    done < <(find "$skill_dir" -name "*.md" -type f -print0 2>/dev/null)
  done < <(find plugins -type d -path "*/skills/*" ! -name "skills" -print0 2>/dev/null)
}

validate_plugin_files() {
  log_info "Checking plugin-level markdown files..."
  
  while IFS= read -r -d '' file; do
    validate_markdown_links "$file"
  done < <(find plugins -maxdepth 3 -name "*.md" -type f -not -path "*/skills/*" -print0 2>/dev/null)
}

check_cross_component_refs() {
  log_info "Checking for forbidden cross-component references..."
  
  while IFS= read -r -d '' skill_dir; do
    while IFS= read -r -d '' file; do
      local matches
      matches=$(grep -oE '\.\./[^/]+/skill' "$file" 2>/dev/null || true)
      if [[ -n "$matches" ]]; then
        log_warn "$file: Cross-skill reference found (violates Law 1: Zero-Shared-State)"
      fi
    done < <(find "$skill_dir" -name "*.md" -type f -print0 2>/dev/null)
  done < <(find plugins -type d -name "skills" -print0 2>/dev/null)
}

check_at_syntax_misuse() {
  log_info "Checking for @[file] syntax misuse in static files..."
  
  while IFS= read -r -d '' file; do
    if grep -qE '@\[[^\]]+\]' "$file" 2>/dev/null; then
      local base
      base=$(basename "$file")
      if [[ "$base" == "SKILL.md" ]]; then
        log_warn "$file: @[file] syntax found (only valid in Commands/User Input)"
      fi
    fi
  done < <(find plugins/*/skills -name "SKILL.md" -type f -print0 2>/dev/null)
  
  while IFS= read -r -d '' file; do
    if grep -qE '@\[[^\]]+\]' "$file" 2>/dev/null; then
      log_warn "$file: @[file] syntax in agent (only valid in Commands/User Input)"
    fi
  done < <(find plugins/*/agents -name "*.md" -type f -print0 2>/dev/null)
}

check_orphan_references() {
  log_info "Checking for orphan reference files..."
  
  while IFS= read -r -d '' skill_dir; do
    local skill_md="$skill_dir/SKILL.md"
    [[ ! -f "$skill_md" ]] && continue
    
    local skill_content
    skill_content=$(cat "$skill_md")
    
    for ref_type in "references" "assets" "scripts"; do
      local ref_dir="$skill_dir/$ref_type"
      [[ ! -d "$ref_dir" ]] && continue
      
      while IFS= read -r -d '' ref_file; do
        # Skip .attic and .DS_Store
        [[ "$ref_file" =~ /\.attic/ ]] && continue
        [[ "$ref_file" =~ /\.DS_Store/ ]] && continue
        
        local rel_path="${ref_file#$skill_dir/}"
        local basename
        basename=$(basename "$ref_file")
        
        if ! echo "$skill_content" | grep -qE "(${rel_path}|${basename})" 2>/dev/null; then
          log_warn "$ref_file: Orphan file not referenced in SKILL.md"
        fi
      done < <(find "$ref_dir" -type f -print0 2>/dev/null)
    done
  done < <(find plugins -type d -path "*/skills/*" ! -name "skills" -print0 2>/dev/null)
}

validate_all_skill_files
validate_plugin_files
check_cross_component_refs
check_at_syntax_misuse
check_orphan_references

echo
if [[ "$EXIT_CODE" -eq 0 ]]; then
  log_info "No critical link issues found."
else
  echo "[SUMMARY] Critical issues found. Exit code: $EXIT_CODE"
fi

exit "$EXIT_CODE"
