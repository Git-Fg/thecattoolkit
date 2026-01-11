#!/bin/bash
# PreToolUse Hook Example - Bash Command Validation
# Validates bash commands for safety before execution
# Returns structured JSON decision

set -euo pipefail

# Read hook input from stdin
input=$(cat)

# Extract command from input
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# If no command, approve
if [ -z "$command" ]; then
  echo '{"continue": true}'
  exit 0
fi

# Log for debugging (only in verbose mode)
if [ "${HOOK_DEBUG:-false}" = "true" ]; then
  echo "Validating command: $command" >&2
fi

# Pattern 1: Obviously safe commands (immediate approval)
# These commands are safe and don't need further analysis
if [[ "$command" =~ ^(ls|pwd|echo|date|whoami|hostname|id|uname|cat|less|more|tail|head|grep|find|which|whereis|history)(\s|$) ]]; then
  if [ "${HOOK_DEBUG:-false}" = "true" ]; then
    echo "Approved: Safe read-only command" >&2
  fi
  exit 0
fi

# Pattern 2: Dangerous operations (immediate denial)
# Check for highly destructive operations

# rm operations (especially recursive force)
if [[ "$command" == *"rm -rf"* ]] || [[ "$command" == *"rm -fr"* ]] || [[ "$command" == *"rm --"* ]] || [[ "$command" == *"rm -r -f"* ]]; then
  echo '{"continue": true, "systemMessage": "Dangerous deletion operation detected (rm -rf). This command cannot be undone. Consider using safer alternatives like rm -i for interactive deletion."}' >&2
  exit 2
fi

# Disk operations
if [[ "$command" == *"dd if="* ]] || [[ "$command" == *"fdisk"* ]] || [[ "$command" == *"mkfs"* ]]; then
  echo '{"continue": true, "systemMessage": "Dangerous disk operation detected (dd, fdisk, mkfs). These commands can destroy data or make systems unbootable."}' >&2
  exit 2
fi

# System modification
if [[ "$command" == *"chmod -R 777"* ]] || [[ "$command" == *"chown -R"* ]] || [[ "$command" == *"killall"* ]]; then
  echo '{"continue": true, "systemMessage": "Potentially dangerous system operation detected. These commands can break system functionality."}' >&2
  exit 2
fi

# Pattern 3: Privilege escalation (ask for confirmation)
# Commands that require elevated privileges
if [[ "$command" == sudo* ]] || [[ "$command" =~ ^su(\s|$) ]] || [[ "$command" == doas* ]]; then
  echo '{"continue": true, "systemMessage": "Command requires elevated privileges. Review carefully before proceeding."}' >&2
  exit 2
fi

# Pattern 4: File operations in sensitive locations
# Check for operations on system directories
if [[ "$command" =~ (/etc/|/sys/|/boot/|/var/log|/usr/bin|/usr/sbin) ]]; then
  echo '{"continue": true, "systemMessage": "Operation on system directory detected. Ensure you have proper permissions and backups."}' >&2
  exit 2
fi

# Pattern 5: Network operations
# Check for network transfers, downloads
if [[ "$command" =~ (curl|wget|scp|rsync|ssh).*(http|https|ftp|ssh) ]]; then
  echo '{"continue": true, "systemMessage": "Network operation detected. Verify the destination is trusted before proceeding."}' >&2
  exit 2
fi

# Pattern 6: Process manipulation
# Kill commands
if [[ "$command" =~ ^kill(\s|$) ]] || [[ "$command" =~ ^pkill(\s|$) ]] || [[ "$command" =~ ^killall(\s|$) ]]; then
  echo '{"continue": true, "systemMessage": "Process termination command detected. Ensure you are targeting the correct process."}' >&2
  exit 2
fi

# Pattern 7: Package manager operations
# Check for install/remove operations
if [[ "$command" =~ (apt|yum|dnf|pacman|brew|choco).*(install|remove|purge|uninstall) ]]; then
  echo '{"continue": true, "systemMessage": "Package management operation detected. This will modify system packages."}' >&2
  exit 2
fi

# Pattern 8: File descriptor operations
# Operations that can consume resources
if [[ "$command" == *"> /dev/null"* ]] || [[ "$command" == *"> /dev/zero"* ]]; then
  echo '{"continue": true, "systemMessage": "Operation writing to special device detected. Can consume resources or fill disk space."}' >&2
  exit 2
fi

# Pattern 9: Fork bombs and resource exhaustion
# Commands that can overwhelm system
if [[ "$command" == *":(){ :|:& };:"* ]] || [[ "$command" == *"forkbomb"* ]] || [[ "$command" == *"yes > /dev/null &"* ]]; then
  echo '{"continue": true, "systemMessage": "Potential resource exhaustion attack detected. These commands can crash the system."}' >&2
  exit 2
fi

# If we get here, the command passed all checks
# For unknown or complex commands, we'll do additional checks

# Check for command substitution with user input
# This is a common injection vector
if [[ "$command" =~ \$\(.*\.\.\. ]] || [[ "$command" == *'`'*'`'* ]]; then
  echo '{"continue": true, "systemMessage": "Command substitution detected. Ensure user input is properly sanitized."}' >&2
  exit 2
fi

# Final approval
if [ "${HOOK_DEBUG:-false}" = "true" ]; then
  echo "Command approved: $command" >&2
fi

exit 0
