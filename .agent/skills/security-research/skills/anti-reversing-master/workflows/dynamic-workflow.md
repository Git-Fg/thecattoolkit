# Dynamic Sandbox Workflow

**Controlled unpacking for multi-stage and runtime-generated code.**

## ⚠️ Safety Critical

Dynamic analysis executes potentially malicious code. **Follow safety protocols:**

- [ ] Run in isolated VM (isolated-vm, not Node vm)
- [ ] Set 1-5 second timeout on all execution
- [ ] No network access or credentials
- [ ] Log all artifacts with timestamps
- [ ] Containerize if possible

## When to Use Dynamic Analysis

**Use when static analysis fails:**
- Multi-stage unpacking (eval staging)
- Runtime code generation
- Control flow flattening
- Environment checks (anti-debug, anti-VM)
- Compressed/encoded payloads

**Don't use if:**
- Static analysis works (prefer safer approach)
- You lack authorization
- Sample is extremely large (>5MB)

## Prerequisites

```bash
npm i isolated-vm @babel/parser @babel/traverse @babel/generator @babel/types
```

## Workflow Steps

### Step 1: Pre-Analysis Assessment (30 seconds)

```bash
# Check for eval/Function patterns
grep -E "eval\(|Function\(" sample.js | head -5

# Check file size
ls -lh sample.js

# Pattern detection
node -e "
const detect = require('obfuscation-detector');
const fs = require('fs');
const code = fs.readFileSync('sample.js', 'utf8');
const patterns = detect(code, false);
console.log('Patterns:', patterns);
"
```

**Go to dynamic if:**
- `eval-staging` detected
- `Function()` constructor calls found
- Multiple compressed/encoded strings
- State machine patterns (control flow flattening)

### Step 2: Environment Setup (1 minute)

```bash
# Create analysis directory
mkdir -p dynamic/{stages,logs,artifacts}

# Set up logging
cat > dynamic/logs/analysis.log << 'EOF'
=== Dynamic Unpacking Analysis ===
Date: $(date)
Sample: sample.js
Operator: [Your name]
Authorization: [Confirm you have permission]
EOF
```

### Step 3: Instrumented Execution (5-10 minutes)

#### Option A: Using provided harness (Recommended)

```bash
# Use production script
node examples/tools/unpack_dynamic.mjs sample.js

# Produces:
# stage_0.js (first unpacked stage)
# stage_1.js (second stage if multi-layer)
# stages_metadata.json (timestamps, sizes)
# execution_log.txt (console output)
```

#### Option B: Custom instrumentation

```javascript
// Create: dynamic/instrument.js
const IsolatedVM = require('isolated-vm');
const fs = require('fs');

async function unpack(sourceCode, timeout = 3000) {
  const isolate = new IsolatedVM.Isolate({ memoryLimit: 128 });
  const context = await isolate.createContext();

  const stages = [];

  // Hook eval
  const evalRef = new IsolatedVM.Reference(function(code) {
    console.log(`[EVAL] Captured: ${code.length} bytes`);
    stages.push({ type: 'eval', code, timestamp: Date.now() });
    return undefined;
  });

  await context.global.set('evalCapture', evalRef);

  // Inject hooks
  const wrapper = `
    globalThis.eval = function(code) { evalCapture(code); };
    globalThis.Function = function(...args) {
      const code = args[args.length - 1];
      evalCapture(code);
      return function(){};
    };
  `;

  try {
    await context.eval(wrapper, { timeout: 1000 });
    await context.eval(sourceCode, { timeout });
  } catch (e) {
    console.log(`Execution error: ${e.message}`);
  }

  isolate.dispose();
  return stages;
}

// Run
const code = fs.readFileSync('sample.js', 'utf8');
const results = await unpack(code);

results.forEach((stage, i) => {
  fs.writeFileSync(`dynamic/stages/stage_${i}.js`, stage.code);
});
```

**Run:**
```bash
node dynamic/instrument.js
```

### Step 4: Analyze Extracted Stages (5-15 minutes)

For each stage:

```bash
# Stage 0
node examples/tools/extract_iocs.mjs dynamic/stages/stage_0.js
mv iocs.json dynamic/stages/stage_0_iocs.json

# Stage 1
node examples/tools/extract_iocs.mjs dynamic/stages/stage_1.js
mv iocs.json dynamic/stages/stage_1_iocs.json

# Compare IOCs
diff dynamic/stages/*_iocs.json
```

### Step 5: Apply Static Analysis to Each Stage (10-30 minutes)

```bash
# Deobfuscate stage 0
node examples/scripts/static-deobfuscation-complete.mjs \
  dynamic/stages/stage_0.js \
  dynamic/stages/stage_0_deobf/

# Deobfuscate stage 1
node examples/scripts/static-deobfuscation-complete.mjs \
  dynamic/stages/stage_1.js \
  dynamic/stages/stage_1_deobf/
```

### Step 6: Behavioral Analysis (10-20 minutes)

```bash
# Check for suspicious APIs in final stage
grep -E "fetch|XMLHttpRequest|WebSocket" dynamic/stages/stage_*_deobf/final.js

# Extract domains
jq -r '.indicators.domains[]' dynamic/stages/*_iocs.json | sort -u

# Check for persistence
grep -E "localStorage|sessionStorage|indexedDB" dynamic/stages/*_deobf/final.js
```

## Multi-Stage Analysis

### Understanding the Unpacking Chain

```
Original Sample → Stage 0 (unpacked) → Stage 1 (unpacked) → ... → Final Payload
     ↓                  ↓                    ↓                    ↓
  Compressed        Strings decrypted    Logic revealed      Malicious code
```

### Analyzing Each Stage

```bash
# Create analysis matrix
cat > dynamic/analysis_matrix.md << 'EOF'
| Stage | Size | IOCs | Suspicious APIs | Purpose |
|-------|------|-------|----------------|---------|
| 0     |      |       |                |         |
| 1     |      |       |                |         |
| 2     |      |       |                |         |
EOF

# Fill in based on analysis
```

## Security Considerations

### What Malware Might Try

1. **Detect instrumentation**
   - Check for hooked `eval`
   - Verify `Function` is native
   - Anti-debugging checks

   **Mitigation**: Use isolated-vm, not Node vm module

2. **Infinite loops**
   - `while(true) {}`
   - Recursive calls without base case

   **Mitigation**: Always set timeout (1-5 seconds)

3. **Resource exhaustion**
   - Large allocations
   - Deep recursion

   **Mitigation**: Memory limit in isolated-vm (128 MB default)

4. **Network beacons**
   - C2 communication
   - Data exfiltration

   **Mitigation**: No network access in sandbox

### Safety Checklist

Before running:
- [ ] Authorization confirmed
- [ ] Timeout set (1-5 seconds)
- [ ] Memory limit set (128 MB)
- [ ] No network access
- [ ] Artifacts being logged
- [ ] Running in VM/container

During execution:
- [ ] Monitor CPU usage
- [ ] Check for infinite loops
- [ ] Verify artifacts captured
- [ ] Log all errors

After execution:
- [ ] Verify timeout triggered
- [ ] Check artifacts completeness
- [ ] Clean up sandbox
- [ ] Report findings

## Common Issues

### "No stages captured"

**Possible causes:**
- Code never reaches eval (conditional unpacking)
- Instrumentation detected
- Execution timed out before eval

**Solutions:**
- Try longer timeout (10 seconds)
- Check for conditional unpacking
- Try browser-based extraction (Playwright)

### "Stages are still obfuscated"

**This is normal!** Dynamic extraction reveals the code, but you still need to deobfuscate it.

**Next steps:**
- Run static deobfuscation on each stage
- Look for patterns in the stage code
- May need multiple iteration cycles

### "Execution failed with error"

**Common errors:**
- Syntax error in sample (expected)
- Timeout reached
- Memory limit exceeded

**Solutions:**
- Increase timeout for complex unpacking
- Increase memory limit (256 MB)
- Try alternative extraction method

## Time Estimates

| Complexity | Time | Success Rate |
|------------|------|--------------|
| Simple eval staging | 5-15 min | 95% |
| Multi-stage (2-3 layers) | 15-30 min | 85% |
| Complex (4+ layers) | 30-60 min | 70% |
| Highly resilient | 60+ min | 50% |

## Deliverables

After dynamic analysis, produce:

1. **Stage files**: `stage_0.js`, `stage_1.js`, etc.
2. **Metadata**: `stages_metadata.json`
3. **Logs**: `execution_log.txt`
4. **Deobfuscated stages**: `stage_X_deobf/final.js`
5. **IOCs per stage**: `stage_X_iocs.json`
6. **Analysis report**: `FINDINGS.md`

## Next Steps

**After dynamic analysis:**

1. **Complete IOC extraction**
   - Aggregate IOCs from all stages
   - Create blocking rules
   - Map to MITRE ATT&CK

2. **Behavioral classification**
   - Keylogging
   - Data exfiltration
   - Persistence mechanisms
   - C2 communication

3. **Incident response**
   - If malicious: Alert SOC
   - Block domains/IPs
   - Quarantine samples
   - Document IOCs in threat intel platforms

## References

- **isolated-vm documentation**: https://www.npmjs.com/package/isolated-vm
- **Dynamic techniques**: [references/pattern-catalog.md](../references/pattern-catalog.md)
- **IOC standards**: [references/ioc-standards.md](../references/ioc-standards.md)
- **Playwright alternative**: https://playwright.dev
