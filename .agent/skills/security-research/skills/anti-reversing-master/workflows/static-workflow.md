# Static Deobfuscation Workflow

**Safe, offline analysis using AST transforms. No code execution.**

## Overview

Static deobfuscation is the **safest and fastest** approach for most JavaScript obfuscation. It works by:
1. Parsing code into an Abstract Syntax Tree (AST)
2. Applying deterministic transformations
3. Regenerating readable code

**Best for**: String arrays, variable renaming, constant folding, escape sequences

**Not for**: Multi-stage unpacking, runtime-generated code, VM-protected code

## Prerequisites

```bash
# Install required tools
npm i @babel/parser @babel/traverse @babel/generator @babel/types
npm i obfuscation-detector prettier

# Verify installation
node -e "console.log('Babel version:', require('@babel/parser').version)"
```

## Workflow Steps

### Step 1: Initial Assessment (30 seconds)

```bash
# Check file size and basic info
ls -lh sample.js
file sample.js

# Quick pattern detection
node -e "
const detect = require('obfuscation-detector');
const fs = require('fs');
const code = fs.readFileSync('sample.js', 'utf8');
const patterns = detect(code, false);
console.log('Detected patterns:', patterns);
"
```

**Expected outputs:**
- `['string-array']` → Good candidate for static analysis
- `['eval-staging']` → Need dynamic analysis instead
- `['variable-rename']` → Perfect for static deobfuscation
- `[]` (empty) → May be clean or use advanced obfuscation

### Step 2: Format & Normalize (1 minute)

```bash
# Create working directory
mkdir -p work/01-pretty work/02-folded work/03-strings work/04-inline work/05-escapes

# Format with Prettier
npx prettier --parser babel sample.js > work/01-pretty/baseline.js

# Check if formatting reveals anything
wc -l sample.js work/01-pretty/baseline.js
```

### Step 3: Pattern-Specific Transforms

#### Transform A: Constant Folding (2-3 minutes)

**What it does**: Evaluates constant expressions like `"a"+"b"` → `"ab"`, `1<<2` → `4`

```javascript
// Create: work/02-folded/constant-fold.js
const fs = require('fs');
const { parse } = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const generate = require('@babel/generator').default;
const * = require('@babel/types');

function evaluatePureLiteral(node) {
  // Implementation from references/static-techniques.md
  // (See: references/static-techniques.md#constant-folding)
}

const src = fs.readFileSync('work/01-pretty/baseline.js', 'utf8');
const ast = parse(src, {
  sourceType: 'unambiguous',
  allowReturnOutsideFunction: true,
  plugins: ['jsx', 'typescript', 'dynamicImport']
});

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
  }
});

const output = generate(ast, { comments: false, compact: false }, src).code;
fs.writeFileSync('work/02-folded/constant-fold.js', output, 'utf8');
console.log('✓ Constant folding complete');
```

**Run:**
```bash
node work/02-folded/constant-fold.js
```

#### Transform B: String Array Resolution (2-3 minutes)

**What it does**: Replaces `arr[idx]` with actual strings like `_0x5a1b[0]` → `"https://api.com"`

```javascript
// Create: work/03-strings/resolve-arrays.js
// Implementation from references/static-techniques.md
// (See: references/static-techniques.md#string-array-resolution)
```

**Run:**
```bash
node work/03-strings/resolve-arrays.js
```

#### Transform C: Variable Inlining (1-2 minutes)

**What it does**: Replaces `const x = 5;` with literal `5` where safe

```javascript
// Create: work/04-inline/inline-vars.js
// Implementation from references/static-techniques.md
```

**Run:**
```bash
node work/04-inline/inline-vars.js
```

#### Transform D: Escape Decoding (30 seconds)

**What it does**: Converts `\x48\x65\x6c\x6c\x6f` → `"Hello"`

```javascript
// Create: work/05-escapes/decode.js
// Implementation from references/static-techniques.md
```

**Run:**
```bash
node work/05-escapes/decode.js
```

### Step 4: Assessment & Iteration (2 minutes)

```bash
# Compare file sizes (should shrink as code becomes more readable)
wc -c work/*/*.js

# Check if code is now readable
head -50 work/05-escapes/final.js

# If still obfuscated:
# → Pattern not handled by static analysis
# → Proceed to dynamic-workflow.md
```

### Step 5: IOC Extraction (2 minutes)

```bash
# Use IOC extraction tool
node examples/tools/extract_iocs.mjs work/05-escapes/final.js

# Review IOCs
cat iocs.json | jq '.'
```

## Complete Script

For convenience, run the complete workflow:

```bash
# Using provided script
node examples/scripts/static-deobfuscation-complete.mjs sample.js output/

# Produces:
# output/01-pretty/baseline.js
# output/02-folded/constant-fold.js
# output/03-strings/string-arrays.js
# output/04-inline/variables.js
# output/05-escapes/decoded.js
# output/final.js (clean, readable version)
# output/iocs.json (indicators of compromise)
```

## Quality Checks

After static deobfuscation, verify:

✅ **Code is more readable**
```bash
# Count meaningful variable names
grep -o '[a-z]{4,}' work/05-escapes/final.js | sort | uniq -c | sort -rn | head -20
```

✅ **Logic is preserved**
```bash
# Check for syntax errors
node --check work/05-escapes/final.js && echo "Syntax OK"
```

✅ **IOCs are visible**
```bash
# Domains should be readable now
jq '.indicators.domains' iocs.json
```

## Success Criteria

**Static analysis is successful if:**
- [ ] Code is syntactically valid
- [ ] Variable names are slightly more meaningful (or at least not hex)
- [ ] String literals are readable
- [ ] Control flow is clear (if/else, loops visible)
- [ ] IOCs can be extracted

**If static analysis fails:**
- [ ] Code still contains `eval()`, `Function()`
- [ ] Control flow is flattened (state machines)
- [ ] Patterns detected: `['eval-staging']`, `['control-flow-flattening']`
- [ ] **Next step**: [dynamic-workflow.md](dynamic-workflow.md)

## Time Estimates

| File Size | Time | Complexity |
|-----------|------|------------|
| < 10 KB | 5-10 min | Simple patterns |
| 10-100 KB | 10-20 min | Moderate patterns |
| 100 KB - 1 MB | 20-45 min | Complex patterns |
| > 1 MB | 45+ min | Consider dynamic approach |

## Troubleshooting

**"Cannot read properties of undefined"**
→ Check Babel plugin configuration
→ See: [references/troubleshooting.md](../references/troubleshooting.md)

**"No patterns detected but code is obfuscated"**
→ Advanced obfuscation (Jscrambler, custom)
→ See: [references/pattern-catalog.md](../references/pattern-catalog.md)

**"Code became less readable"**
→ Transform order may be wrong
→ Try reversing transform sequence

## Next Steps

**After successful static analysis:**
1. [IOC extraction](ioc-workflow.md) - Extract network indicators
2. [Bundle analysis](bundle-workflow.md) - If it's a bundle
3. Manual review - Understand the logic
4. Report findings - Use STIX 2.1 format

**If static analysis is insufficient:**
1. [Dynamic workflow](dynamic-workflow.md) - For unpacking
2. [Pattern catalog](../references/pattern-catalog.md) - Re-identify techniques
3. Manual analysis - Last resort

## References

- **Pattern catalog**: [references/pattern-catalog.md](../references/pattern-catalog.md)
- **Production tools**: [examples/tools/](../examples/tools/)
- **Troubleshooting**: [references/troubleshooting.md](../references/troubleshooting.md)
