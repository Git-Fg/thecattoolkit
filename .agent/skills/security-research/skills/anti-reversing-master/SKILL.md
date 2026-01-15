---
name: anti-reversing-master
description: "Comprehensive anti-reversing, obfuscation, and deobfuscation knowledge base with intelligent routing for JavaScript malware analysis. Use when you need to understand protection mechanisms, deobfuscate code, reverse engineer bundles, or analyze malicious JavaScript with a structured workflow."
---

> **CONSTRAINT (dual-use)**: This skill contains dual-use security techniques. Before proceeding, confirm authorization and legal compliance. For authorized security research, malware analysis, and educational purposes only.

# Master Anti-Reversing & JavaScript Deobfuscation

## Overview

This is the **master knowledge base** for anti-reversing techniques and JavaScript deobfuscation. It provides:
- **Comprehensive reference** for all protection/obfuscation techniques
- **Intelligent routing** to specialized tools based on analysis needs
- **Structured workflows** for different analysis scenarios
- **Production-ready tools** for automated deobfuscation

## Quick Decision Guide

| **Your Situation** | **Navigate To** |
|:-------------------|:----------------|
| Don't know where to start | [Workflow Guide](workflows/quick-start.md) |
| See obfuscated code, don't recognize patterns | [Pattern Catalog](references/pattern-catalog.md) |
| Need static analysis (safe, offline) | [Static Workflow](workflows/static-workflow.md) |
| Need dynamic analysis (unpacking) | [Dynamic Workflow](workflows/dynamic-workflow.md) |
| Analyzing Webpack/Rollup bundles | [Bundle Workflow](workflows/bundle-workflow.md) |
| Quick IOC extraction for malware triage | [IOC Workflow](workflows/ioc-workflow.md) |
| Binary reversing (anti-debug, packing) | [Binary Techniques](references/binary-techniques.md) |
| Need production-ready scripts | [Tools Library](examples/tools/) |

## Core Capabilities

### 1. Pattern Recognition
Identify obfuscation techniques and select appropriate analysis strategies.
- **8 major obfuscation families** documented
- **Confidence levels** and AST signatures
- **Decision trees** for automated routing

### 2. Static Analysis (Safe/Offline)
Safe deobfuscation using AST transforms without code execution.
- Constant folding and binary expression simplification
- String array resolution
- Variable inlining (const-only)
- Unicode/hex escape decoding

### 3. Dynamic Analysis (Sandboxed)
Controlled unpacking for multi-stage and eval-staged code.
- **isolated-vm** for secure execution
- Instrumented evaluation hooks
- Artifact extraction with timestamps
- Multiple environment support (Node.js, Browser)

### 4. Bundle Reversal
Modern JavaScript bundle analysis (Webpack/Rollup/Vite).
- Module boundary recovery
- Source map leveraging
- Developer intent reconstruction
- Security-critical module identification

### 5. IOC Extraction
Rapid malware triage without full deobfuscation.
- Network indicators (domains, URLs, IPs)
- Suspicious API detection
- Behavioral classification
- STIX 2.1 formatted output

### 6. Binary Techniques
Traditional reverse engineering approaches.
- Anti-debugging bypass strategies
- Anti-VM detection evasion
- Code obfuscation analysis
- Packing/unpacking methodologies

## Workflow Selection

### Primary Analysis Paths

**Path 1: Safe Static First (Recommended)**
```
1. Pattern Recognition → Identify obfuscation type
2. Static Deobfuscation → Apply AST transforms
3. IOC Extraction → Extract indicators
4. Complete
```

**Path 2: Dynamic Unpacking**
```
1. Pattern Recognition → Detect eval staging
2. Dynamic Sandbox → Extract stages
3. Static Deobfuscation → Analyze each stage
4. IOC Extraction → Final triage
5. Complete
```

**Path 3: Bundle Analysis**
```
1. Identify bundler → Webpack/Rollup/Vite
2. Extract module index → Parse structure
3. Source map recovery → Original sources
4. Security analysis → Critical modules
5. Complete
```

**Path 4: Quick Triage**
```
1. IOC Extraction → Network indicators
2. Behavioral assessment → Threat classification
3. Blocking rules → Immediate action
4. Complete
```

## Specialized Skills Available

This master skill orchestrates access to:

### JavaScript Deobfuscation
- **js-deobfuscation-static-ast**: Safe offline AST transforms
- **js-deobfuscation-dynamic-sandbox**: Controlled unpacking
- **js-obfuscator-patterns-catalog**: Pattern recognition & routing
- **js-malware-triage-iocs**: Rapid IOC extraction

### Bundle Analysis
- **webpack-bundle-reversal**: Modern bundle reversal

### Binary Analysis
- **anti-reversing-techniques**: Traditional RE techniques

## Tool Ecosystem

### Production Scripts
Ready-to-use tools in [tools library](examples/tools/):
- `deobf.mjs` - AST deobfuscation script
- `extract_iocs.mjs` - IOC extraction tool
- `unpack_dynamic.mjs` - Dynamic unpacking harness

### Detection Tools
- **obfuscation-detector** - Pattern classification
- **Babel toolchain** - AST manipulation
- **webpack-bundle-analyzer** - Bundle visualization

## Security & Ethics

### Authorization Requirements
Before analysis, confirm:
1. **Ownership/permission** to analyze the code
2. **Legal jurisdiction** compliance (CFAA, DMCA)
3. **Scope definition** (what's in/out of bounds)
4. **Purpose clarity** (security research, malware analysis, authorized auditing)

### Dual-Use Awareness
This knowledge applies to:
- **Legitimate**: Malware analysis, security research, CTFs, authorized auditing
- **Prohibited**: Software piracy, unauthorized access, malicious use

### Safety Protocols
- Always use **isolated-vm** for dynamic analysis
- Set **timeouts** on all execution
- Use **containerization** when possible
- Log **all artifacts** for forensic value

## Progressive Disclosure Structure

### Immediate Access (This File)
- Quick decision guide
- Core capabilities overview
- Workflow selection paths

### Deep Knowledge
- **[Workflows](workflows/)**: Step-by-step analysis procedures
- **[References](references/)**: Comprehensive technique documentation
- **[Examples](examples/)**: Working code and tool implementations

## Usage Examples

### Example 1: Unknown Obfuscated JavaScript
```bash
# Step 1: Identify patterns
node detect_patterns.mjs sample.js
# Output: ['string-array', 'variable-rename']

# Step 2: Apply static deobfuscation
node deobf.mjs sample.js deobf.js
# Output: readable code

# Step 3: Extract IOCs
node extract_iocs.mjs deobf.js
# Output: iocs.json with domains/URLs
```

### Example 2: Multi-Stage Malware
```bash
# Step 1: Detect staging
grep -E "eval\(|Function\(" sample.js
# Found: eval() calls present

# Step 2: Dynamic extraction
node unpack_dynamic.mjs sample.js
# Output: stage_0.js, stage_1.js, ...

# Step 3: Deobfuscate each stage
for stage in stage_*.js; do
  node deobf.mjs $stage deobf_$stage
done
```

### Example 3: Webpack Bundle Analysis
```bash
# Step 1: Visualize bundle
webpack-bundle-analyzer bundle.js

# Step 2: Extract modules
node parse_webpack.mjs bundle.js
# Output: module_index.json

# Step 3: Find security-critical code
node find_critical.mjs module_index.json
# Output: SECURITY_FINDINGS.md
```

## Getting Started

1. **Identify your use case** using the Quick Decision Guide above
2. **Follow the appropriate workflow** in the workflows/ directory
3. **Reference technique details** in the references/ directory
4. **Use production tools** from the examples/ directory
5. **Report findings** using standard formats (STIX 2.1, YARA, etc.)

## Additional Resources

- [MITRE ATT&CK](https://attack.mitre.org/) - Tactics, techniques for malware analysis
- [Babel Plugin Guide](https://babeljs.io/docs/plugins) - AST manipulation reference
- [OWASP Code Injection](https://owasp.org/www-community/attacks/Code_Injection) - Security context
- [STIX 2.1](https://oasis-open.github.io/cti-documentation/stix/intro.html) - Threat intelligence sharing

---

**Next Steps**: Navigate to [workflows/quick-start.md](workflows/quick-start.md) to begin your analysis, or jump directly to [references/pattern-catalog.md](references/pattern-catalog.md) if you already know what you're looking at.
