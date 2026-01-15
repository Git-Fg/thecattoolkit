#!/usr/bin/env node
/**
 * Dynamic Unpacking Tool
 * Safely extracts staged JavaScript code using isolated-vm
 *
 * Usage: node unpack_dynamic.mjs <input.js>
 * Output: stage_*.js files + metadata
 */

import fs from 'node:fs';
import IsolatedVM from 'isolated-vm';

// ============================================================================
// INSTRUMENTATION
// ============================================================================

const capturedStages = [];

async function unpackDynamicIsolated(sourceCode, timeoutMs = 3000) {
  const isolate = new IsolatedVM.Isolate({ memoryLimit: 128 });
  const context = await isolate.createContext();

  const evalCallback = new IsolatedVM.Reference(function(code) {
    console.log(`[EVAL] Intercepted, length: ${code.length}`);
    capturedStages.push({ stage: 'eval', code, timestamp: Date.now() });
    return undefined;
  });

  await context.global.set('evalCapture', evalCallback);

  const wrapper = `
    const originalEval = eval;
    globalThis.eval = function(code) {
      evalCapture(code);
      return undefined;
    };
    globalThis.Function = function(...args) {
      const code = args[args.length - 1];
      evalCapture(code);
      return function() {};
    };
  `;

  try {
    await context.eval(wrapper, { timeout: 1000 });
    await context.eval(sourceCode, { timeout: timeoutMs });
  } catch (err) {
    console.log(`[>] Execution ended: ${err.message}`);
  }

  isolate.dispose();
  return { stages: capturedStages };
}

// ============================================================================
// USAGE
// ============================================================================

function usage() {
  const cmd = process.argv[1].split('/').pop();
  console.error(`Usage: node ${cmd} <input.js> [timeout_ms]\n`);
  console.error('Safely unpacks JavaScript code using isolated-vm\n');
  console.error('Options:');
  console.error('  timeout_ms  Maximum execution time (default: 3000ms)\n');
  console.error('Output:');
  console.error('  stage_0.js, stage_1.js, ...');
  console.error('  stages_metadata.json\n');
  process.exit(2);
}

// ============================================================================
// MAIN
// ============================================================================

const inputPath = process.argv[2];
const timeoutMs = parseInt(process.argv[3] || '3000', 10);

if (!inputPath) {
  usage();
}

async function main() {
  try {
    const obfuscatedCode = fs.readFileSync(inputPath, 'utf8');

    console.log(`[>] Unpacking: ${inputPath}`);
    console.log(`[>] Timeout: ${timeoutMs}ms`);
    console.log(`[>] Using isolated-vm for security...\n`);

    const result = await unpackDynamicIsolated(obfuscatedCode, timeoutMs);

    console.log(`\n[✓] Extracted ${result.stages.length} stage(s)\n`);

    if (result.stages.length === 0) {
      console.log('[!] WARNING: No eval() calls captured');
      console.log('    This may indicate:');
      console.log('    - Code never reaches eval (conditional unpacking)');
      console.log('    - Instrumentation was detected');
      console.log('    - Execution timed out before eval');
      console.log('\n    Try:');
      console.log('    1. Increase timeout: node unpack_dynamic.mjs file.js 10000');
      console.log('    2. Use browser-based extraction (Playwright)');
      console.log('    3. Analyze with static techniques first\n');
    }

    result.stages.forEach((stage, idx) => {
      const filename = `stage_${idx}.js`;
      fs.writeFileSync(filename, stage.code, 'utf8');
      console.log(`  → ${filename} (${stage.code.length.toLocaleString()} bytes)`);
    });

    const metadata = {
      original_file: inputPath,
      timeout_ms: timeoutMs,
      timestamp: new Date().toISOString(),
      stages: result.stages.map((s, i) => ({
        index: i,
        type: s.stage,
        length: s.code.length,
        timestamp: s.timestamp
      }))
    };

    fs.writeFileSync('stages_metadata.json', JSON.stringify(metadata, null, 2));

    console.log('\n[✓] Metadata saved to: stages_metadata.json\n');
    console.log('[>] Next steps:');
    console.log('    1. Analyze each stage: node deobf.mjs stage_0.js stage_0_deobf.js');
    console.log('    2. Extract IOCs: node extract_iocs.mjs stage_0.js');
    console.log('    3. If still obfuscated, try static deobfuscation\n');

  } catch (error) {
    console.error(`\n[!] Fatal error: ${error.message}\n`);
    process.exit(1);
  }
}

main();
