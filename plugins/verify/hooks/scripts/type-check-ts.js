#!/usr/bin/env node
/**
 * Run TypeScript type checker on files after Claude edits them.
 * Auto-detects tsconfig.json and runs tsc.
 */
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

function findTsConfig(startPath) {
    let current = path.resolve(startPath);
    const root = path.parse(current).root;

    while (current !== root) {
        const tsconfig = path.join(current, 'tsconfig.json');
        if (fs.existsSync(tsconfig)) return tsconfig;
        current = path.dirname(current);
    }
    return null;
}

function runTsc(projectRoot, callback) {
    // Try to use local tsc first, then npx, then global
    // But npx tsc --noEmit is the safest standard.
    // We run it in the project root.
    exec('npx tsc --noEmit', { cwd: projectRoot, timeout: 10000 }, (error, stdout, stderr) => {
        callback(error, stdout, stderr);
    });
}

async function main() {
    try {
        const inputData = JSON.parse(fs.readFileSync(0, 'utf-8'));
        const toolInput = inputData.tool_input || {};
        const filePath = toolInput.file_path || '';

        if (!filePath) process.exit(0);

        // Only check .ts, .tsx, .mts, .cts files
        if (!/\.(ts|tsx|mts|cts)$/.test(filePath)) {
            process.exit(0);
        }

        // Find tsconfig
        const tsconfigPath = findTsConfig(filePath.startsWith('/') ? filePath : path.join(process.cwd(), filePath));
        if (!tsconfigPath) {
            // No tsconfig (maybe assume not a TS project or simple JS), skip silently or log
            process.exit(0);
        }

        const projectRoot = path.dirname(tsconfigPath);

        // To avoid excessive checking, we might want to only check the file edited, but tsc checks the project.
        // tsc --noEmit is project-wide. 
        // NOTE: Running full tsc on every edit might be slow for large repos.
        // Optimization: checking only the file is hard because of dependencies.
        // We will run project-wide check, assuming incremental is set in tsconfig or it's fast enough.
        // 10 second timeout in runTsc.

        runTsc(projectRoot, (error, stdout, stderr) => {
            const basename = path.basename(filePath);

            if (error) {
                // tsc failed (errors found)
                // Parse output to find errors relevant to the file (optional, but helpful)
                // Or just report top errors.

                const output = stdout.toString();
                const lines = output.split('\n');
                let relevantErrors = [];

                // Basic filter for relevant errors (containing file path)
                // tsc output example: src/App.tsx(10,5): error TS2322: ...
                for (const line of lines) {
                    if (line.includes(basename)) {
                        relevantErrors.push(line.trim());
                        if (relevantErrors.length >= 3) break; // Limit errors
                    }
                }

                if (relevantErrors.length === 0) {
                    // If no errors in this file, maybe report general "TSC failed"
                    // But we don't want to noise up if the user is editing a valid file and elsewhere is broken.
                    // IMPORTANT: Only report if THIS file caused issues or has issues?
                    // A safe bet is: if tsc fails, check if the edited file is in the output.
                    // If not, maybe silence? 
                    // Let's report "TSC errors detected" generically if we can't map, but preferably match.
                    if (lines.length > 0 && lines[0].trim() !== '') {
                        // Report first line distinct
                        relevantErrors.push(lines.find(l => l.includes("error TS")) || lines[0].trim());
                    }
                }

                const errorMsg = relevantErrors.join('\n');
                if (errorMsg) {
                    console.log(JSON.stringify({
                        continue: true,
                        hookSpecificOutput: {
                            hookEventName: "PostToolUse",
                            additionalContext: `[type-check] TS Errors in ${basename}:\n${errorMsg}`
                        }
                    }));
                }
            } else {
                console.log(JSON.stringify({
                    continue: true,
                    hookSpecificOutput: {
                        hookEventName: "PostToolUse",
                        additionalContext: `[type-check] ${basename} passed type check`
                    }
                }));
            }
        });

    } catch (e) {
        process.exit(0);
    }
}

main();
