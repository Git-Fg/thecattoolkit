#!/bin/bash
# Standalone Bootstrap Script for The Cat Toolkit
# Broken AI recovery mechanism using pure git.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../../" && pwd)"
cd "$REPO_ROOT"

usage() {
    echo "Usage: $0 [mode] [target]"
    echo ""
    echo "Modes:"
    echo "  list              Show changed files that can be restored"
    echo "  soft [path]       Restore specific path from HEAD (Default: plugins/meta)"
    echo "  hard [N]          Hard reset to HEAD~N (N defaults to 0)"
    echo "  remote [path]     Restore path from origin/main"
    echo ""
    echo "Examples:"
    echo "  $0 soft"
    echo "  $0 soft plugins/meta/skills/manage-hooks"
    echo "  $0 hard 1"
    exit 1
}

MODE=${1:-"soft"}
TARGET=${2}

case $MODE in
    list)
        echo "Changes in toolkit:"
        git status --short plugins/ agents/ skills/
        ;;
    soft)
        TARGET=${TARGET:-"plugins/meta"}
        echo "Restoring $TARGET from HEAD..."
        git checkout HEAD -- "$TARGET"
        echo "✓ Restored $TARGET"
        ;;
    hard)
        N=${TARGET:-"0"}
        echo "!!! WARNING: Performing hard reset to HEAD~$N !!!"
        echo "This will discard all uncommitted changes."
        read -p "Are you sure? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git reset --hard "HEAD~$N"
            echo "✓ Reset to HEAD~$N"
        else
            echo "Abort."
        fi
        ;;
    remote)
        TARGET=${TARGET:-"plugins/meta"}
        echo "Fetching from origin and restoring $TARGET..."
        git fetch origin
        git checkout origin/main -- "$TARGET"
        echo "✓ Restored $TARGET from origin/main"
        ;;
    *)
        usage
        ;;
esac
