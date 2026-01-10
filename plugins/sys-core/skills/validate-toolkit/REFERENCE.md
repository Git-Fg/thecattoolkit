# Validate Toolkit - Quick Reference

## Usage

### Automatic Invocation
Simply describe your validation need:
```
"Validate my cattoolkit marketplace thoroughly"
"Test this plugin for any issues"
"Comprehensive validation of the plugins directory"
```

### Manual Invocation
```
/validate-toolkit
```

## What It Does

1. **Isolates** the test environment (temporary directory)
2. **Discovers** all components (agents, skills, commands, hooks)
3. **Calculates** complexity based on component count
4. **Executes** proportional test suites
5. **Reports** findings with actionable fixes

## Complexity Levels

| Components | Level | Tests | Duration |
|:----------|:------|:------|:---------|
| 1-10 | Simple | Basic validation | 2-3 min |
| 11-30 | Medium | Standard + interaction | 5-8 min |
| 31-50 | Large | Deep + stress tests | 10-15 min |
| 50+ | Complex | Exhaustive + edge cases | 15-20 min |

## Test Coverage

- ✅ JSON validation (marketplace.json, plugin.json)
- ✅ Component loading (plugins, agents, skills)
- ✅ Hook execution verification
- ✅ Interactive scenario testing
- ✅ Cross-component integration
- ✅ Performance benchmarks (for complex setups)

## Requirements

- Claude Code CLI installed
- `claude` command available in PATH
- Read access to plugin/marketplace files
- Temporary directory creation permissions

## Example Output

```
════════════════════════════════════════════════════════════
              VALIDATION REPORT - cattoolkit
════════════════════════════════════════════════════════════

📊 OVERVIEW
├─ Target: /path/to/cattoolkit
├─ Complexity: Medium
├─ Components: 23 total
└─ Test Duration: 6 minutes

✅ STRUCTURE VALIDATION
├─ marketplace.json: VALID
├─ plugin.json files: 3/3 valid
└─ File references: 5/5 present

⚙️  COMPONENT LOADING
├─ Plugins loaded: 3/3
├─ Agents discovered: 8/8
├─ Skills discovered: 19/20
├─ Commands discovered: 0/0
└─ Hooks functional: 2/2

🧪 INTERACTIVE TESTS
├─ Basic invocation: PASS
├─ Complex scenarios: PASS
├─ Edge cases: PASS
└─ Performance: ACCEPTABLE

📋 ISSUES FOUND
1. Skill 'check-types' not discoverable
   └─ Impact: Low
   └─ Suggested fix: Verify SKILL.md frontmatter description field

════════════════════════════════════════════════════════════
                    FINAL VERDICT: ✅ VALID
════════════════════════════════════════════════════════════
```

## Tips

- Run validation after any structural changes
- Use before releasing a plugin/marketplace
- Test in isolated environments first
- Review the "Issues Found" section carefully
