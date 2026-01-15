# Quick Start Workflow

**Start here if you're unsure where to begin.**

## Decision Tree

```
START: You have obfuscated or suspicious JavaScript
  |
  ├─→ Don't recognize the code? ───────────┐
  │                                        │
  │   → See: references/pattern-catalog.md │
  │                                        │
  ├─→ It's a Webpack/Rollup/Vite bundle? ─┼──→ references/bundle-workflow.md
  │                                        │
  ├─→ Need quick results (malware triage)?─┼──→ references/ioc-workflow.md
  │                                        │
  ├─→ Code has eval()/Function() calls? ──┼──→ references/dynamic-workflow.md
  │                                        │
  └─→ Standard obfuscation (strings, vars)?┘
      → references/static-workflow.md
```

## Five-Minute Analysis

For rapid assessment when time is critical:

### Step 1: Pattern Detection (30 seconds)
```bash
npm i obfuscation-detector
node -e "
const detect = require('obfuscation-detector');
const fs = require('fs');
const code = fs.readFileSync('sample.js', 'utf8');
console.log('Patterns:', detect(code, false));
"
```

### Step 2: IOC Sweep (2 minutes)
```bash
node examples/tools/extract_iocs.mjs sample.js
cat iocs.json
```

### Step 3: Quick Classification (1 minute)
```bash
# Count IOCs
jq '.indicators | keys | length' iocs.json

# If > 5 suspicious APIs or domains:
# → HIGH PRIORITY - Malware triage

# If clean IOCs but obfuscated:
# → MEDIUM PRIORITY - Deobfuscation needed

# If clean IOCs and readable:
# → LOW PRIORITY - Likely benign
```

### Step 4: Immediate Action (1.5 minutes)
**If HIGH PRIORITY (malware suspected):**
- Extract blocking rules: `jq -r '.indicators.domains[]' iocs.json`
- Alert incident response team
- Quarantine sample
- Proceed to dynamic analysis if authorized

**If MEDIUM PRIORITY (obfuscated but unclear):**
- Apply static deobfuscation
- Re-assess after AST transforms

**If LOW PRIORITY (likely benign):**
- Archive sample
- Document as clean

## Common Scenarios

### Scenario 1: "I found this on a compromised website"
**Path**: IOC Workflow → Dynamic Analysis → Static Analysis
**Time**: 30-60 minutes
**Priority**: HIGH

### Scenario 2: "CTF challenge with obfuscated JavaScript"
**Path**: Pattern Recognition → Static Analysis
**Time**: 15-30 minutes
**Priority**: MEDIUM

### Scenario 3: "Need to understand a webpack bundle"
**Path**: Bundle Workflow → Module Analysis
**Time**: 20-45 minutes
**Priority**: MEDIUM

### Scenario 4: "Suspicious email attachment (JS file)"
**Path**: IOC Workflow → Dynamic Analysis
**Time**: 15-45 minutes
**Priority**: HIGH

### Scenario 5: "Learning about obfuscation techniques"
**Path**: Pattern Catalog → Reference Reading → Practice
**Time**: Self-paced
**Priority**: LOW

## Before You Begin

✅ **Check Authorization**
- [ ] You own the code OR have written permission
- [ ] Purpose is legitimate (security research, malware analysis, education)
- [ ] Jurisdiction allows analysis (check CFAA, DMCA)
- [ ] Scope is defined

✅ **Safety Setup**
- [ ] Use isolated-vm for dynamic analysis
- [ ] Set execution timeouts (1-5 seconds)
- [ ] Run in container/VM if available
- [ ] No network access during analysis

## Next Steps

**After quick start, proceed to:**
- [references/static-workflow.md](static-workflow.md) - For safe static analysis
- [references/dynamic-workflow.md](dynamic-workflow.md) - For dynamic unpacking
- [references/bundle-workflow.md](bundle-workflow.md) - For bundle reversal
- [references/ioc-workflow.md](ioc-workflow.md) - For malware triage

## Getting Help

**Pattern not recognized?** → [references/pattern-catalog.md](../references/pattern-catalog.md)

**Tool not working?** → [references/troubleshooting.md](../references/troubleshooting.md)

**Need more depth?** → See all available references in [references/](../references/)
