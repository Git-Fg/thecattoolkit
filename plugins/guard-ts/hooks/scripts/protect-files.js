#!/usr/bin/env node
/**
 * Protect sensitive files from modification.
 * Warns about edits to production configs, lock files, and sensitive directories.
 * All edits are allowed but warnings are shown to Claude.
 */
const fs = require('fs');
const path = require('path');

// Files/patterns to warn about
const PROTECTED_PATTERNS = [
    // Lock files (usually shouldn't be manually edited)
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    'npm-shrinkwrap.json',
    'bun.lockb',

    // Sensitive files
    '.env',
    '.env.local',
    '.env.production',
    'secrets/*',
    '*/secrets/*',
    '*/*/secrets/*',
    'credentials/*',
    '*/credentials/*',
    '*/*/credentials/*',

    // Git internals
    '.git/*',
];

// Files that should warn but not block (semantics are same as blocked but different message in Python version, here we unify or separate as needed)
const WARN_PATTERNS = [
    '.github/workflows/*',
    'docker-compose.yml',
    'Dockerfile',
    'production/*',
    '*/production/*',
    '*/*/production/*',
];

function isSafePath(filePath) {
    try {
        const projectRoot = process.cwd();
        const targetPath = path.resolve(projectRoot, filePath);
        return !path.relative(projectRoot, targetPath).startsWith('..');
    } catch (e) {
        return false;
    }
}

function matchesPattern(filePath, patterns) {
    // Remove leading ./
    const cleanPath = filePath.startsWith('./') ? filePath.slice(2) : filePath;
    const basename = path.basename(cleanPath);

    for (const pattern of patterns) {
        // Simple manual implementation or use minimatch if available. 
        // For portability without installing node_modules in the plugin dir, we might want a simple matcher.
        // But the previous python script used fnmatch.
        // Let's implement a simple wildcard matcher to avoid dependencies if possible, OR assume minimatch is not there.
        // JS RegExp for globs is complex.
        // Actually, for "2025 best practices" in a plugin, we should probably avoid dependencies if not installed.
        // I will implement a basic glob-to-regex converter or simple checks.

        if (simpleGlobMatch(cleanPath, pattern) || simpleGlobMatch(basename, pattern)) {
            return pattern;
        }
    }
    return null;
}

function simpleGlobMatch(str, glob) {
    // Basic glob matcher for * handling
    const regexStr = glob
        .replace(/\./g, '\\.')
        .replace(/\*/g, '.*')
        .replace(/\?/g, '.');
    const regex = new RegExp(`^${regexStr}$`);
    return regex.test(str);
}

async function main() {
    try {
        const inputData = JSON.parse(fs.readFileSync(0, 'utf-8'));
        const toolInput = inputData.tool_input || {};
        const filePath = toolInput.file_path || '';

        if (!filePath) process.exit(0);

        if (!isSafePath(filePath)) {
            // Path traversal detected
            process.exit(0);
        }

        const blocked = matchesPattern(filePath, PROTECTED_PATTERNS);
        if (blocked) {
            const warning = `[protect-files] WARNING: Editing protected file ${filePath}\n` +
                `[protect-files]   Matches protected pattern: ${blocked}\n` +
                `[protect-files]   This file type should generally not be manually edited.`;

            console.log(JSON.stringify({
                continue: true,
                systemMessage: warning,
                hookSpecificOutput: {
                    hookEventName: "PreToolUse",
                    permissionDecision: "allow",
                    permissionDecisionReason: warning
                }
            }));
            process.exit(0);
        }

        const warned = matchesPattern(filePath, WARN_PATTERNS);
        if (warned) {
            const warning = `[protect-files] NOTE: Editing sensitive file ${filePath}\n` +
                `[protect-files]   Matches pattern: ${warned}`;
            console.log(JSON.stringify({
                continue: true,
                systemMessage: warning,
                hookSpecificOutput: {
                    hookEventName: "PreToolUse",
                    permissionDecision: "allow",
                    permissionDecisionReason: warning
                }
            }));
            process.exit(0);
        }

    } catch (e) {
        // concise error log if needed, or silent fail
        process.exit(0);
    }
}

main();
