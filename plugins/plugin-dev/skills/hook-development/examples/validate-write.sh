#!/bin/bash
# PreToolUse Hook Example - File Write/Edit Validation
# Validates file write operations for safety
# Checks for path traversal, system files, and sensitive content

set -euo pipefail

# Read hook input from stdin
input=$(cat)

# Extract file path and content from input
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# If no file path, approve
if [ -z "$file_path" ]; then
  echo '{"continue": true}'
  exit 0
fi

# Extract content (for secret detection)
file_content=$(echo "$input" | jq -r '.tool_input.content // empty')

# Log for debugging (only if debug mode enabled)
if [ "${HOOK_DEBUG:-false}" = "true" ]; then
  echo "Validating file path: $file_path" >&2
fi

# Check 1: Path traversal
# Detect attempts to access files outside the intended directory
if [[ "$file_path" == *".."* ]] || [[ "$file_path" == *"/.."* ]] || [[ "$file_path" == *"../"* ]]; then
  echo '{"continue": true, "systemMessage": "Path traversal detected. Cannot write to files outside project directory."}' >&2
  exit 2
fi

# Check 2: Absolute path to system directories
# Prevent writes to critical system locations
system_patterns=(
  "/etc/"
  "/sys/"
  "/boot/"
  "/var/log/"
  "/var/run/"
  "/usr/bin/"
  "/usr/sbin/"
  "/bin/"
  "/sbin/"
  "/dev/"
  "/proc/"
)

for pattern in "${system_patterns[@]}"; do
  if [[ "$file_path" == "$pattern"* ]]; then
    echo "{\"continue\": true, \"systemMessage\": \"Cannot write to system directory: $pattern\"}" >&2
    exit 2
  fi
done

# Check 3: Sensitive files
# Prevent writing to configuration files that might contain secrets
sensitive_patterns=(
  ".env"
  ".env."
  "*.env"
  "*secret*"
  "*credential*"
  "*password*"
  "*key*"
  "id_rsa"
  "id_dsa"
  "id_ecdsa"
  "id_ed25519"
  ".aws/credentials"
  ".aws/config"
  "config.json"
  "secrets.json"
  "*.key"
  "*.pem"
  "*.p12"
  "*.pfx"
)

for pattern in "${sensitive_patterns[@]}"; do
  # Support glob patterns
  if [[ "$pattern" == *"*"* ]]; then
    # Convert glob to regex
    glob_pattern="${pattern//\*/.*}"
    glob_pattern="${glob_pattern//\./\.}"
    if [[ "$file_path" =~ $glob_pattern ]]; then
      echo "{\"continue\": true, \"systemMessage\": \"Writing to potentially sensitive file: $file_path\"}" >&2
      exit 2
    fi
  else
    # Exact match
    if [[ "$file_path" == *"$pattern"* ]]; then
      echo "{\"continue\": true, \"systemMessage\": \"Writing to potentially sensitive file: $file_path\"}" >&2
      exit 2
    fi
  fi
done

# Check 4: Project root restrictions
# Prevent writing to certain project root files
project_root_restrictions=(
  ".git/config"
  ".git/HEAD"
  "package-lock.json"
  "yarn.lock"
  "Cargo.lock"
  "Pipfile.lock"
)

for restriction in "${project_root_restrictions[@]}"; do
  if [[ "$file_path" == "$restriction" ]]; then
    echo "{\"continue\": true, \"systemMessage\": \"Direct modification of $restriction is not recommended. Use appropriate tools instead.\"}" >&2
    exit 2
  fi
done

# Check 5: File size limits
# Warn about very large file writes
max_size=$((100 * 1024 * 1024))  # 100MB default

if [ -n "$file_content" ]; then
  content_size=${#file_content}
  if [ $content_size -gt $max_size ]; then
    echo "{\"continue\": true, \"systemMessage\": \"Large file write detected ($((content_size / 1024 / 1024))MB). Consider using streaming or chunking for large files.\"}" >&2
    # This is a warning, not a block - continue
  fi
fi

# Check 6: Content-based checks
# Scan for potential secrets in file content
if [ -n "$file_content" ]; then
  # Check for common API key patterns
  if echo "$file_content" | grep -qiE "(api[_-]?key|apikey).{0,20}['\"]?[A-Za-z0-9]{20,}"; then
    echo "{\"continue\": true, \"systemMessage\": \"Potential API key detected in file content. Ensure this is intentional and consider using environment variables instead.\"}" >&2
    # Warning, not a block
  fi

  # Check for private key patterns
  if echo "$file_content" | grep -qE "-----BEGIN [A-Z ]*PRIVATE KEY-----"; then
    echo "{\"continue\": true, \"systemMessage\": \"Private key detected in file content. Never commit private keys to version control.\"}" >&2
    # Warning, not a block
  fi

  # Check for database URLs with credentials
  if echo "$file_content" | grep -qiE "(postgres|mysql|mongodb)://[^:@]+:[^@]+@"; then
    echo "{\"continue\": true, \"systemMessage\": \"Database URL with embedded credentials detected. Consider using environment variables or connection strings without passwords.\"}" >&2
    # Warning, not a block
  fi

  # Check for AWS credentials
  if echo "$file_content" | grep -qiE "aws_(access_key_id|secret_access_key).{0,20}['\"]?[A-Za-z0-9/+]{16,}"; then
    echo "{\"continue\": true, \"systemMessage\": \"AWS credentials detected in file content. Use AWS credentials file or environment variables instead.\"}" >&2
    # Warning, not a block
  fi
fi

# Check 7: Special file extensions
# Warn about binary or sensitive file types
binary_extensions=(
  ".exe"
  ".dll"
  ".so"
  ".dylib"
  ".bin"
  ".img"
  ".iso"
  ".zip"
  ".tar"
  ".gz"
  ".7z"
  ".pkg"
  ".deb"
  ".rpm"
  ".dmg"
)

for ext in "${binary_extensions[@]}"; do
  if [[ "$file_path" == *"$ext" ]]; then
    echo "{\"continue\": true, \"systemMessage\": \"Binary file detected ($file_path). Ensure this is intentional.\"}" >&2
    # Warning, not a block
    break
  fi
done

# Check 8: Lock files
# Warn about concurrent write operations
lock_files=(
  ".lock"
  ".flock"
  "*.lock"
)

for pattern in "${lock_files[@]}"; do
  if [[ "$pattern" == *"*"* ]]; then
    glob_pattern="${pattern//\*/.*}"
    if [[ "$file_path" =~ $glob_pattern ]]; then
      echo "{\"continue\": true, \"systemMessage\": \"Lock file detected. Ensure no concurrent writes to avoid conflicts.\"}" >&2
      break
    fi
  elif [[ "$file_path" == *"$pattern"* ]]; then
    echo "{\"continue\": true, \"systemMessage\": \"Lock file detected. Ensure no concurrent writes to avoid conflicts.\"}" >&2
    break
  fi
done

# Final approval
if [ "${HOOK_DEBUG:-false}" = "true" ]; then
  echo "File write approved: $file_path" >&2
fi

exit 0
