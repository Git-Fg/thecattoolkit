#!/usr/bin/env node
/**
 * Pre-commit security check hook.
 * Warns about edits that might contain secrets or security issues.
 */
const fs = require('fs');
const path = require('path');

const SECRET_PATTERNS = [
    { regex: /(api[_-]?key|apikey)\s*[:=]\s*["']?[a-zA-Z0-9_-]{20,}/i, type: "API key" },
    { regex: /(secret|password|passwd|pwd)\s*[:=]\s*["'][^"']+["']/i, type: "Password/Secret" },
    { regex: /bearer\s+[a-zA-Z0-9_-]{20,}/i, type: "Bearer token" },
    { regex: /ghp_[a-zA-Z0-9]{36}/, type: "GitHub Personal Access Token" },
    { regex: /github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}/, type: "GitHub PAT (fine-grained)" },
    { regex: /sk-[a-zA-Z0-9]{48}/, type: "OpenAI API Key" },
    { regex: /sk-ant-[a-zA-Z0-9-]{90,}/, type: "Anthropic API Key" },
    { regex: /-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----/, type: "Private key" },
    { regex: /aws[_-]?access[_-]?key[_-]?id\s*[:=]\s*[A-Z0-9]{20}/i, type: "AWS Access Key" },
    { regex: /aws[_-]?secret[_-]?access[_-]?key\s*[:=]\s*[a-zA-Z0-9/+=]{40}/i, type: "AWS Secret Key" }
];

const SKIP_FILES = new Set([
    ".env.example", ".env.template", ".env.sample",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml"
]);

function checkForSecrets(content, filePath) {
    const issues = [];
    const basename = path.basename(filePath);

    if (SKIP_FILES.has(basename)) return issues;
    // Skip test files
    if (filePath.toLowerCase().includes('test') || filePath.toLowerCase().includes('spec')) return issues;

    for (const { regex, type } of SECRET_PATTERNS) {
        if (regex.test(content)) {
            issues.push(`Potential ${type} detected`);
        }
    }
    return issues;
}

async function main() {
    try {
        const inputData = JSON.parse(fs.readFileSync(0, 'utf-8'));
        const toolInput = inputData.tool_input || {};

        const filePath = toolInput.file_path || '';
        const content = toolInput.content || toolInput.new_string || '';

        if (!filePath || !content) process.exit(0);

        const projectRoot = process.cwd();
        const targetPath = path.resolve(projectRoot, filePath);
        if (!path.relative(projectRoot, targetPath).startsWith('..')) {
            // Safe path
        } else {
            // Unsafe path
            process.exit(0);
        }

        const issues = checkForSecrets(content, filePath);

        if (issues.length > 0) {
            const issuesText = issues.map(i => `  - ${i}`).join('\n');
            const warning = `[security-check] WARNING: Potential security issue detected in ${filePath}:\n` +
                `${issuesText}\n` +
                `[security-check]   Please verify this is not a real secret before committing.\n` +
                `[security-check]   If this is a false positive, review security-check.js`;

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
        process.exit(0);
    }
}

main();
