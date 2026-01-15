# Troubleshooting Guide

## Common Issues & Solutions

### Babel Errors

#### "Cannot read properties of undefined"

**Error**:
```javascript
TypeError: Cannot read properties of undefined (reading 'value')
```

**Cause**: Trying to access property on undefined node

**Solution**:
```javascript
// WRONG
const value = path.node.init.value;

// RIGHT - Check for existence
if (path.node.init && path.node.init.value !== undefined) {
  const value = path.node.init.value;
}

// BETTER - Use optional chaining
const value = path.node.init?.value;
```

#### "Invalid left-hand side in assignment"

**Error**:
```javascript
SyntaxError: Invalid left-hand side in assignment
```

**Cause**: Trying to replace node incorrectly

**Solution**:
```javascript
// WRONG
path.node = newNode;

// RIGHT
path.replaceWith(newNode);
path.skip();
```

#### "Module not found: @babel/parser"

**Error**:
```bash
Error: Cannot find module '@babel/parser'
```

**Solution**:
```bash
# Install all required Babel modules
npm i @babel/parser @babel/traverse @babel/generator @babel/types

# Verify installation
node -e "console.log(require('@babel/parser').version)"
```

---

### Parsing Errors

#### "Unexpected token"

**Error**:
```javascript
SyntaxError: Unexpected token (1:1)
```

**Cause**: JavaScript syntax not supported

**Solution**:
```javascript
// Add more plugins
parse(code, {
  sourceType: 'unambiguous',
  allowReturnOutsideFunction: true,
  plugins: [
    'jsx',
    'typescript',
    'classProperties',
    'dynamicImport',
    'optionalChaining',
    'nullishCoalescingOperator',
    'objectRestSpread',
    'numericSeparator',
    'topLevelAwait'
  ]
});
```

#### "This experimental syntax requires a parser plugin"

**Error**:
```javascript
SyntaxError: This experimental syntax requires a parser plugin
```

**Solution**:
```bash
# Identify the syntax (e.g., optional chaining)
npm i @babel/plugin-proposal-optional-chaining

# Add to plugins
parse(code, {
  plugins: ['optionalChaining']
});
```

---

### Traversal Issues

#### "Maximum call stack size exceeded"

**Error**:
```javascript
RangeError: Maximum call stack size exceeded
```

**Cause**: Infinite recursion in traversal

**Solution**:
```javascript
// Add skip() to prevent revisiting
traverse(ast, {
  FunctionDeclaration(path) {
    // Process node
    path.skip(); // Prevent visiting children
  }
});
```

#### "path.replaceWith is not a function"

**Error**:
```javascript
TypeError: path.replaceWith is not a function
```

**Cause**: Wrong path type

**Solution**:
```javascript
// Check path type before replacing
if (path.isIdentifier()) {
  path.replaceWith(t.stringLiteral('new value'));
}
```

---

### isolated-vm Issues

#### "Cannot read properties of undefined (reading 'eval')"

**Error**:
```javascript
TypeError: Cannot read properties of undefined (reading 'eval')
```

**Cause**: Wrong context setup

**Solution**:
```javascript
// Set up context properly
const context = await isolate.createContext();

// Define hooks BEFORE eval
const evalRef = new IsolatedVM.Reference(function(code) {
  console.log('Hooked:', code);
});

await context.global.set('evalCapture', evalRef);
await context.eval(wrapper);
```

#### "Execution timed out"

**Error**:
```javascript
Error: Execution timed out
```

**Cause**: Code took too long

**Solution**:
```javascript
// Increase timeout
await context.eval(code, { timeout: 10000 }); // 10 seconds

// Or fix the code to be faster
```

---

### IOC Extraction Issues

#### "No IOCs found" but code is suspicious

**Cause**: IOCs are obfuscated

**Solution**:
```bash
# 1. First deobfuscate
node deobf.mjs sample.js deobf.js

# 2. Then extract IOCs
node extract_iocs.mjs deobf.js

# Or use regex fallback
grep -oE 'https?://[^"'\''<>]+' sample.js
```

#### "Parse error" in IOC extraction

**Error**:
```javascript
SyntaxError: Unexpected token (1:1)
```

**Cause**: JavaScript too complex for parser

**Solution**:
```javascript
// Try/catch around parse
try {
  analyzeAST(code);
} catch (err) {
  console.log('AST parse failed, using regex fallback');
  analyzeRegex(code);
}
```

---

### Pattern Detection Issues

#### "obfuscation-detector returns empty array"

**Cause**: Custom/obscure obfuscation

**Solution**:
```javascript
// Manual inspection
if (code.includes('eval(') || code.includes('Function(')) {
  console.log('Dynamic code detected');
}

if (code.match(/_0x[a-f0-9]{2,}/g)) {
  console.log('Hex variable naming detected');
}
```

#### False positives in pattern detection

**Cause**: Legitimate code triggering patterns

**Solution**:
```javascript
// Add confidence scoring
const patterns = detect(code, false);
const confidence = calculateConfidence(patterns, code);

if (confidence > 0.7) {
  console.log('High confidence obfuscation');
} else {
  console.log('Likely benign code');
}
```

---

### General Debugging

#### Enable Debug Logging

```javascript
// Verbose traversal
traverse(ast, {
  enter(path) {
    console.log(`Visiting: ${path.node.type} at line ${path.node.loc?.start.line}`);
  }
});
```

#### Print AST Structure

```javascript
const util = require('util');
console.log(util.inspect(ast, { depth: null }));
```

#### Check File Size

```bash
# Check if file is too large
ls -lh sample.js

# Large files may need chunking
# > 5MB consider dynamic approach
```

---

## Getting Help

### Resources

1. **Babel Handbook**: https://github.com/jamiebuilds/babel-handbook
2. **AST Explorer**: https://astexplorer.net/ - Visual AST inspection
3. **isolated-vm Docs**: https://github.com/laverdet/isolated-vm
4. **obfuscation-detector**: https://github.com/HumanSecurity/obfuscation-detector

### Community Support

- **Stack Overflow**: Tag with `babel`, `javascript`, `obfuscation`
- **GitHub Issues**: Report bugs in tool repositories
- **Discord**: JavaScript/Node.js communities
- **Reddit**: r/javascript, r/security

### Reporting Issues

When reporting a bug:

1. **Input sample**: Provide the JavaScript causing the issue
2. **Error message**: Include full stack trace
3. **Expected behavior**: What should happen
4. **Environment**: Node version, OS, tool version

```markdown
## Bug Report

**Input**: [Attach or paste sample.js]
**Error**:
```
[Full error message]
```

**Expected**: Should deobfuscate without errors
**Actual**: Throws error

**Environment**:
- Node.js: v18.x
- OS: Ubuntu 22.04
- Tool: deobf.mjs v1.0

**Steps to reproduce**:
1. Run: `node deobf.mjs sample.js output.js`
2. See error
```
