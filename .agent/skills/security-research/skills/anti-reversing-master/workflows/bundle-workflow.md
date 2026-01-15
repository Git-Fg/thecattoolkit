# Bundle Reversal Workflow

**Analysis workflow for Webpack, Rollup, and Vite bundles.**

## Overview

Modern web applications are often bundled into single files. This workflow helps you:
1. Identify the bundler
2. Extract module structure
3. Find security-critical code
4. Recover original sources (if source maps available)

## Prerequisites

```bash
npm i webpack-bundle-analyzer source-map-explorer
```

## Workflow Steps

### Step 1: Identify Bundler (30 seconds)

```bash
# Look for distinctive patterns
grep -o "__webpack" sample.bundle.js | head -1
# Webpack if found

grep -o "__export" sample.bundle.js | head -1
# Rollup/Vite if found

# Check for source map comment
tail -1 sample.bundle.js
# If ends with: //# sourceMappingURL=bundle.js.map
```

### Step 2: Visual Analysis (2-3 minutes)

**Using webpack-bundle-analyzer:**

```bash
# Generate stats
npx webpack --json > stats.json

# Upload to webpack-bundle-analyzer
# https://chrisbateman.github.io/webpack-visualizer/

# Or generate report (if you have config)
npm i -D webpack-bundle-analyzer
# Add to webpack.config.js
```

### Step 3: Extract Module Index (5-10 minutes)

```bash
# Find module registry
grep -n "__webpack_modules__" sample.bundle.js
# Note the line number

# Extract module array (requires manual editing or script)
node examples/tools/parse_webpack.mjs sample.bundle.js
# Produces: module_index.json
```

### Step 4: Find Critical Modules (10-15 minutes)

```bash
# Search for suspicious patterns
grep -iE "auth|token|login|password|crypto|api|fetch" sample.bundle.js

# Use AST analysis
node examples/tools/find_critical.mjs module_index.json
# Produces: critical_modules.json
```

### Step 5: Source Map Recovery (5-10 minutes)

```bash
# Check for .map file
ls -la *.map

# If found, extract
source-map-explorer bundle.js bundle.js.map

# Or manually extract
node examples/tools/extract_sourcemap.mjs bundle.js.map
```

## Success Criteria

✅ Bundler identified
✅ Module index extracted
✅ Critical modules located
✅ Original sources recovered (if available)

## Next Steps

- [IOC Extraction](ioc-workflow.md) - Extract network indicators
- Manual review - Understand the logic
- Report findings

## References

- [Source Map Documentation](https://sourcemaps.info/)
- [Pattern Catalog](../references/pattern-catalog.md)
