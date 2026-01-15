#!/usr/bin/env node
/**
 * IOC Extraction Tool
 * Extracts indicators of compromise from JavaScript without deobfuscation
 *
 * Usage: node extract_iocs.mjs <input.js>
 * Output: iocs.json
 */

import fs from 'node:fs';
import { parse } from '@babel/parser';
import traverse from '@babel/traverse';

const iocs = {
  domains: new Set(),
  urls: new Set(),
  ips: new Set(),
  filePaths: new Set(),
  suspicious_apis: new Set(),
  keyloggers: new Set(),
  exfil_sinks: new Set()
};

// ============================================================================
// REGEX PATTERNS
// ============================================================================

const patterns = {
  url: /https?:\/\/[^\s"'<>;)}\]]+/gi,
  domain: /(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}/gi,
  ipv4: /\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/g,
  filePath: /(?:[a-zA-Z]:\\|\/)[^\s"'<>;)}\]]+/gi,
  registry: /HKLM|HKCU|HKEY_[A-Z_]+/gi
};

// ============================================================================
// AST-BASED DETECTION
// ============================================================================

const suspiciousApiPatterns = {
  network: ['fetch', 'XMLHttpRequest', 'WebSocket', 'navigator.sendBeacon', 'axios', 'request'],
  crypto: ['crypto.subtle', 'forge.aes', 'tweetnacl'],
  storage: ['localStorage', 'sessionStorage', 'indexedDB', 'document.cookie'],
  dom: ['document.write', 'innerHTML', 'insertAdjacentHTML'],
  worker: ['new Worker', 'importScripts'],
  process: ['child_process.spawn', 'require("child_process")'],
  keylog: ['addEventListener("keydown"', 'onkeypress', 'addEventListener("input"'],
  clipboard: ['navigator.clipboard.read', 'document.execCommand("paste")'],
  crypt: ['btoa(', 'Buffer.from(', 'atob(']
};

function analyzeAST(code) {
  try {
    const ast = parse(code, {
      sourceType: 'unambiguous',
      allowReturnOutsideFunction: true,
      plugins: ['jsx', 'typescript', 'dynamicImport']
    });

    traverse(ast, {
      // Detect function/method calls
      CallExpression(path) {
        const callee = path.node.callee;
        let callName = '';

        if (path.isCallExpression()) {
          if (callee.type === 'Identifier') {
            callName = callee.name;
          } else if (callee.type === 'MemberExpression') {
            const obj = callee.object?.name || '';
            const prop = callee.property?.name || '';
            callName = `${obj}.${prop}`;
          }
        }

        for (const [category, apis] of Object.entries(suspiciousApiPatterns)) {
          if (apis.some(api => callName.includes(api))) {
            iocs.suspicious_apis.add(`${category}: ${callName}`);

            const firstArg = path.node.arguments[0];
            if (firstArg?.type === 'StringLiteral') {
              const argValue = firstArg.value;
              if (patterns.url.test(argValue)) {
                iocs.urls.add(argValue);
              }
            }
          }
        }
      },

      // Detect string literals (potential IOCs)
      StringLiteral(path) {
        const value = path.node.value;

        const urlMatches = value.match(patterns.url);
        if (urlMatches) urlMatches.forEach(u => iocs.urls.add(u));

        const domainMatches = value.match(patterns.domain);
        if (domainMatches) domainMatches.forEach(d => {
          if (d.length > 4) iocs.domains.add(d.toLowerCase());
        });

        const ipMatches = value.match(patterns.ipv4);
        if (ipMatches) ipMatches.forEach(ip => iocs.ips.add(ip));

        const pathMatches = value.match(patterns.filePath);
        if (pathMatches) pathMatches.forEach(p => iocs.filePaths.add(p));
      }
    });
  } catch (err) {
    console.warn(`[!] Parse error: ${err.message}`);
  }
}

// ============================================================================
// REGEX FALLBACK
// ============================================================================

function analyzeRegex(code) {
  for (const [type, pattern] of Object.entries(patterns)) {
    const matches = code.match(pattern) || [];
    matches.forEach(match => {
      if (type === 'url') iocs.urls.add(match);
      if (type === 'domain') iocs.domains.add(match.toLowerCase());
      if (type === 'ipv4') iocs.ips.add(match);
      if (type === 'filePath') iocs.filePaths.add(match);
    });
  }
}

// ============================================================================
// THREAT ASSESSMENT
// ============================================================================

function assessThreat(iocs) {
  let threatLevel = 'LOW';
  let evidence = [];

  if (iocs.indicators.domains.length > 5) {
    threatLevel = 'MEDIUM';
    evidence.push('Multiple C2 domains detected');
  }

  if (iocs.indicators.suspicious_api_calls.some(api => api.includes('worker') || api.includes('spawn'))) {
    threatLevel = 'HIGH';
    evidence.push('Process/worker spawning detected (possible malware)');
  }

  if (iocs.indicators.suspicious_api_calls.some(api => api.includes('keylog'))) {
    threatLevel = 'HIGH';
    evidence.push('Keylogging patterns detected');
  }

  if (iocs.indicators.suspicious_api_calls.some(api => api.includes('clipboard'))) {
    threatLevel = 'MEDIUM';
    evidence.push('Clipboard exfiltration possible');
  }

  if (iocs.indicators.urls.some(url => url.includes('pastebin') || url.includes('discord.com/api/webhooks'))) {
    threatLevel = 'MEDIUM';
    evidence.push('Use of public paste/webhook services for exfil');
  }

  return { threatLevel, evidence };
}

// ============================================================================
// MAIN
// ============================================================================

function usage() {
  const cmd = process.argv[1].split('/').pop();
  console.error(`Usage: node ${cmd} <input.js>\n`);
  console.error('Extracts IOCs (domains, URLs, IPs, suspicious APIs) from JavaScript\n');
  console.error('Output: iocs.json\n');
  process.exit(2);
}

const inputPath = process.argv[2];

if (!inputPath) {
  usage();
}

try {
  const sourceCode = fs.readFileSync(inputPath, 'utf8');

  console.log(`[>] Analyzing: ${inputPath}`);
  console.log(`[>] Size: ${sourceCode.length.toLocaleString()} bytes\n`);

  analyzeAST(sourceCode);
  analyzeRegex(sourceCode);

  const report = {
    metadata: {
      file: inputPath,
      timestamp: new Date().toISOString(),
      size: sourceCode.length
    },
    indicators: {
      urls: Array.from(iocs.urls),
      domains: Array.from(iocs.domains),
      ipv4_addresses: Array.from(iocs.ips),
      file_paths: Array.from(iocs.filePaths),
      suspicious_api_calls: Array.from(iocs.suspicious_apis)
    }
  };

  fs.writeFileSync('iocs.json', JSON.stringify(report, null, 2));

  console.log('[IOC Summary]');
  console.log(`  URLs:             ${iocs.urls.size}`);
  console.log(`  Domains:          ${iocs.domains.size}`);
  console.log(`  IPv4 addresses:   ${iocs.ips.size}`);
  console.log(`  File paths:       ${iocs.filePaths.size}`);
  console.log(`  Suspicious APIs:  ${iocs.suspicious_apis.size}`);
  console.log();

  const assessment = assessThreat(report);

  console.log(`[Threat Assessment]`);
  console.log(`  Level: ${assessment.threatLevel}`);
  if (assessment.evidence.length > 0) {
    console.log(`  Evidence:`);
    assessment.evidence.forEach(e => console.log(`    - ${e}`));
  }
  console.log();

  if (iocs.urls.size > 0) {
    console.log('[URLS]');
    Array.from(iocs.urls).slice(0, 5).forEach(u => console.log(`  ${u}`));
    if (iocs.urls.size > 5) console.log(`  ... and ${iocs.urls.size - 5} more`);
    console.log();
  }

  if (iocs.domains.size > 0) {
    console.log('[DOMAINS]');
    Array.from(iocs.domains).slice(0, 5).forEach(d => console.log(`  ${d}`));
    if (iocs.domains.size > 5) console.log(`  ... and ${iocs.domains.size - 5} more`);
    console.log();
  }

  if (iocs.suspicious_apis.size > 0) {
    console.log('[SUSPICIOUS APIS]');
    Array.from(iocs.suspicious_apis).forEach(api => console.log(`  ${api}`));
    console.log();
  }

  console.log('[✓] Full report saved to: iocs.json\n');

} catch (error) {
  console.error(`\n[!] Error: ${error.message}\n`);
  process.exit(1);
}
