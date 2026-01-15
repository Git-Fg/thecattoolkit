#!/usr/bin/env node
/**
 * Production-ready AST deobfuscation script
 * Performs constant folding, string array resolution, and variable inlining
 *
 * Usage: node deobf.mjs <input.js> <output.js>
 */

import fs from 'node:fs';
import { parse } from '@babel/parser';
import traverse from '@babel/traverse';
import generate from '@babel/generator';
import * as t from '@babel/types';

// ============================================================================
// CONSTANT FOLDING
// ============================================================================

function evaluatePureLiteral(node) {
  if (t.isStringLiteral(node)) return node.value;
  if (t.isNumericLiteral(node)) return node.value;
  if (t.isBooleanLiteral(node)) return node.value;
  if (t.isNullLiteral(node)) return null;

  // Unary operations
  if (t.isUnaryExpression(node) && node.prefix) {
    const v = evaluatePureLiteral(node.argument);
    if (v === undefined) return undefined;
    switch (node.operator) {
      case '!': return !v;
      case '+': return +v;
      case '-': return -v;
      case '~': return ~v;
      case 'void': return undefined;
      default: return undefined;
    }
  }

  // Binary operations
  if (t.isBinaryExpression(node)) {
    const l = evaluatePureLiteral(node.left);
    const r = evaluatePureLiteral(node.right);
    if (l === undefined || r === undefined) return undefined;

    switch (node.operator) {
      case '+': return l + r;
      case '-': return l - r;
      case '*': return l * r;
      case '/': return l / r;
      case '%': return l % r;
      case '**': return l ** r;
      case '<<': return l << r;
      case '>>': return l >> r;
      case '>>>': return l >>> r;
      case '|': return l | r;
      case '&': return l & r;
      case '^': return l ^ r;
      case '==': return l == r;
      case '!=': return l != r;
      case '===': return l === r;
      case '!==': return l !== r;
      case '<': return l < r;
      case '<=': return l <= r;
      case '>': return l > r;
      case '>=': return l >= r;
      default: return undefined;
    }
  }

  // Logical operations
  if (t.isLogicalExpression(node)) {
    const l = evaluatePureLiteral(node.left);
    if (l === undefined) return undefined;
    if (node.operator === '&&') {
      return l ? evaluatePureLiteral(node.right) : l;
    }
    if (node.operator === '||') {
      return l ? l : evaluatePureLiteral(node.right);
    }
    if (node.operator === '??') {
      return l ?? evaluatePureLiteral(node.right);
    }
  }

  // Ternary operator
  if (t.isConditionalExpression(node)) {
    const test = evaluatePureLiteral(node.test);
    if (test === undefined) return undefined;
    return test
      ? evaluatePureLiteral(node.consequent)
      : evaluatePureLiteral(node.alternate);
  }

  return undefined;
}

function literalToNode(v) {
  if (v === undefined) return t.identifier('undefined');
  if (v === null) return t.nullLiteral();
  if (typeof v === 'string') return t.stringLiteral(v);
  if (typeof v === 'number') return t.numericLiteral(v);
  if (typeof v === 'boolean') return t.booleanLiteral(v);
  return null;
}

// ============================================================================
// STRING ARRAY RESOLUTION
// ============================================================================

const constStringArrays = new Map();

function findStringArrays(ast) {
  traverse(ast, {
    VariableDeclarator(path) {
      const id = path.node.id;
      const init = path.node.init;
      if (!t.isIdentifier(id)) return;
      if (!t.isArrayExpression(init)) return;

      const elems = init.elements;
      if (!elems.every((e) => e && t.isStringLiteral(e))) return;

      const binding = path.scope.getBinding(id.name);
      if (!binding) return;

      const isConst =
        binding.kind === 'const' ||
        (t.isVariableDeclaration(path.parentPath.node) &&
         path.parentPath.node.kind === 'const');

      if (!isConst) return;

      constStringArrays.set(id.name, elems.map((e) => e.value));
    }
  });
}

function resolveStringArrays(ast) {
  traverse(ast, {
    MemberExpression(path) {
      const { object, property, computed } = path.node;
      if (!computed) return;
      if (!t.isIdentifier(object)) return;

      const arr = constStringArrays.get(object.name);
      if (!arr) return;

      const idx = evaluatePureLiteral(property);
      if (typeof idx !== 'number') return;

      const v = arr[idx];
      if (typeof v !== 'string') return;

      path.replaceWith(t.stringLiteral(v));
      path.skip();
    }
  });
}

// ============================================================================
// VARIABLE INLINING
// ============================================================================

const constVariables = new Map();

function findConstVariables(ast) {
  traverse(ast, {
    VariableDeclarator(path) {
      const { id, init } = path.node;
      if (!t.isIdentifier(id) || !init) return;

      const folded = evaluatePureLiteral(init);
      if (folded === undefined) return;

      const binding = path.scope.getBinding(id.name);
      if (!binding || binding.kind !== 'const') return;

      constVariables.set(id.name, init);
    }
  });
}

function inlineConstVariables(ast) {
  traverse(ast, {
    Identifier(path) {
      if (path.isReferencedIdentifier()) {
        const init = constVariables.get(path.node.name);
        if (init) {
          const binding = path.scope.getBinding(path.node.name);
          if (binding && binding.kind === 'const') {
            path.replaceWith(JSON.parse(JSON.stringify(init)));
            path.skip();
          }
        }
      }
    }
  });
}

// ============================================================================
// UNICODE ESCAPE DECODING
// ============================================================================

function decodeEscapes(str) {
  return str
    .replace(/\\x([0-9A-Fa-f]{2})/g, (match, hex) =>
      String.fromCharCode(parseInt(hex, 16))
    )
    .replace(/\\u([0-9A-Fa-f]{4})/g, (match, hex) =>
      String.fromCharCode(parseInt(hex, 16))
    )
    .replace(/\\u\{([0-9A-Fa-f]+)\}/g, (match, hex) =>
      String.fromCodePoint(parseInt(hex, 16))
    );
}

function decodeStringLiterals(ast) {
  traverse(ast, {
    StringLiteral(path) {
      if (path.node.value.includes('\\')) {
        const decoded = decodeEscapes(path.node.value);
        if (decoded !== path.node.value) {
          path.node.value = decoded;
        }
      }
    }
  });
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

function usage() {
  const cmd = process.argv[1].split('/').pop();
  console.error(`Usage: node ${cmd} <input.js> <output.js>`);
  console.error('\nDeobfuscates JavaScript using AST transforms:\n');
  console.error('  - Constant folding (e.g., "a"+"b" → "ab")');
  console.error('  - String array resolution (e.g., arr[0] → "string")');
  console.error('  - Variable inlining (const variables only)');
  console.error('  - Unicode/hex escape decoding\n');
  process.exit(2);
}

const inputPath = process.argv[2];
const outputPath = process.argv[3];

if (!inputPath || !outputPath) {
  usage();
}

try {
  const src = fs.readFileSync(inputPath, 'utf8');

  console.log(`[>] Reading: ${inputPath}`);
  console.log(`[>] Parsing JavaScript...\n`);

  const ast = parse(src, {
    sourceType: 'unambiguous',
    allowReturnOutsideFunction: true,
    plugins: [
      'jsx',
      'typescript',
      'classProperties',
      'classPrivateProperties',
      'classPrivateMethods',
      'dynamicImport',
      'optionalChaining',
      'nullishCoalescingOperator',
      'objectRestSpread',
      'numericSeparator',
      'topLevelAwait',
    ],
  });

  console.log('[1/4] Finding string arrays...');
  findStringArrays(ast);

  console.log('[2/4] Constant folding...');
  traverse(ast, {
    enter(path) {
      const folded = evaluatePureLiteral(path.node);
      if (folded !== undefined && !t.isIdentifier(path.node)) {
        const repl = literalToNode(folded);
        if (repl) {
          path.replaceWith(repl);
          path.skip();
        }
      }
    },
  });

  console.log('[3/4] Resolving string arrays...');
  resolveStringArrays(ast);

  console.log('[4/4] Decoding escapes...');
  decodeStringLiterals(ast);

  const output = generate(
    ast,
    {
      comments: false,
      retainLines: false,
      compact: false,
      jsescOption: { minimal: true },
    },
    src
  ).code;

  fs.writeFileSync(outputPath, output, 'utf8');

  const originalSize = fs.statSync(inputPath).size;
  const newSize = fs.statSync(outputPath).size;
  const reduction = ((1 - newSize / originalSize) * 100).toFixed(2);

  console.log(`\n[✓] Deobfuscation complete\n`);
  console.log(`    Input:  ${inputPath} (${originalSize.toLocaleString()} bytes)`);
  console.log(`    Output: ${outputPath} (${newSize.toLocaleString()} bytes)`);
  console.log(`    Reduction: ${reduction}%`);
  console.log(`\n[>] Next steps:`);
  console.log(`    - Review output: less ${outputPath}`);
  console.log(`    - Extract IOCs: node extract_iocs.mjs ${outputPath}`);
  console.log(`    - If still obfuscated: use dynamic analysis\n`);

} catch (error) {
  console.error(`\n[!] Error: ${error.message}\n`);
  console.error(error.stack);
  process.exit(1);
}
