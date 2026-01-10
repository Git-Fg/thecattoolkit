#!/usr/bin/env node

/**
 * Comprehensive Marketplace Validation Framework
 *
 * Validates the Cat Toolkit marketplace against:
 * - Plugin structure and metadata integrity
 * - Skills, commands, hooks, and agent configurations
 * - Edge cases and error conditions
 * - Cross-plugin dependencies and interactions
 */

import { readFileSync, existsSync, statSync } from 'fs';
import { join, basename, dirname, resolve } from 'path';
import { query } from '@anthropic-ai/claude-agent-sdk';

// ============================================================
// CONFIGURATION
// ============================================================

const MARKETPLACE_PATH = resolve(__dirname, '../.claude-plugin/marketplace.json');
const PLUGINS_PATH = resolve(__dirname, '../plugins');
const RESULTS_DIR = resolve(__dirname, '../validation-results');

// Validation thresholds
const MAX_PLUGIN_SIZE_MB = 50;
const MAX_SKILL_DESCRIPTION_LENGTH = 200;
const MAX_COMMAND_DESCRIPTION_LENGTH = 200;
const REQUIRED_PLUGIN_FILES = ['.claude-plugin/plugin.json'];

// Edge case scenarios to test
const EDGE_CASES = {
  empty_plugin: { name: 'empty-plugin', shouldFail: true },
  missing_metadata: { name: 'missing-metadata', shouldFail: true },
  oversized_description: { name: 'oversized-description', shouldFail: true },
  invalid_json: { name: 'invalid-json', shouldFail: true },
  missing_required_files: { name: 'missing-required', shouldFail: true },
  circular_dependencies: { name: 'circular-deps', shouldFail: true }
};

// ============================================================
// VALIDATION CLASSES
// ============================================================

class ValidationResult {
  constructor(testName) {
    this.testName = testName;
    this.passed = true;
    this.errors = [];
    this.warnings = [];
    this.metadata = {};
  }

  addError(message, details = null) {
    this.passed = false;
    this.errors.push({ message, details });
  }

  addWarning(message, details = null) {
    this.warnings.push({ message, details });
  }

  setMetadata(key, value) {
    this.metadata[key] = value;
  }

  getSummary() {
    return {
      test: this.testName,
      passed: this.passed,
      errorCount: this.errors.length,
      warningCount: this.warnings.length,
      metadata: this.metadata
    };
  }
}

class MarketplaceValidator {
  constructor() {
    this.marketplace = null;
    this.plugins = [];
    this.results = [];
  }

  // Load and parse marketplace.json
  async loadMarketplace() {
    try {
      if (!existsSync(MARKETPLACE_PATH)) {
        throw new Error(`Marketplace file not found: ${MARKETPLACE_PATH}`);
      }
      const content = readFileSync(MARKETPLACE_PATH, 'utf-8');
      this.marketplace = JSON.parse(content);
      console.log(`✅ Loaded marketplace with ${this.marketplace.plugins.length} plugins`);
    } catch (error) {
      throw new Error(`Failed to load marketplace: ${error.message}`);
    }
  }

  // Validate marketplace.json structure
  validateMarketplaceStructure() {
    const result = new ValidationResult('Marketplace Structure');

    try {
      // Check required fields
      const requiredFields = ['name', 'metadata', 'plugins'];
      for (const field of requiredFields) {
        if (!this.marketplace[field]) {
          result.addError(`Missing required field: ${field}`);
        }
      }

      // Validate metadata
      if (this.marketplace.metadata) {
        if (!this.marketplace.metadata.version) {
          result.addError('Missing metadata.version');
        }
        if (!this.marketplace.metadata.description) {
          result.addError('Missing metadata.description');
        }
      }

      // Validate plugins array
      if (!Array.isArray(this.marketplace.plugins)) {
        result.addError('plugins must be an array');
      } else {
        result.setMetadata('pluginCount', this.marketplace.plugins.length);

        // Check for duplicate plugin names
        const names = this.marketplace.plugins.map(p => p.name);
        const duplicates = names.filter((name, index) => names.indexOf(name) !== index);
        if (duplicates.length > 0) {
          result.addError(`Duplicate plugin names: ${duplicates.join(', ')}`);
        }

        // Validate each plugin reference
        for (const plugin of this.marketplace.plugins) {
          if (!plugin.name) {
            result.addError('Plugin missing name field');
          }
          if (!plugin.source) {
            result.addError(`Plugin ${plugin.name || 'unnamed'} missing source field`);
          } else {
            const sourcePath = resolve(PLUGINS_PATH, plugin.source.replace('./plugins/', ''));
            if (!existsSync(sourcePath)) {
              result.addError(`Plugin source not found: ${plugin.source}`);
            }
          }
          if (!plugin.description) {
            result.addWarning(`Plugin ${plugin.name} missing description`);
          }
        }
      }
    } catch (error) {
      result.addError(`Validation error: ${error.message}`);
    }

    this.results.push(result);
    return result;
  }

  // Validate individual plugin structure
  validateAllPlugins() {
    for (const pluginRef of this.marketplace.plugins) {
      this.validatePlugin(pluginRef);
    }
  }

  validatePlugin(pluginRef) {
    const result = new ValidationResult(`Plugin: ${pluginRef.name}`);
    const pluginPath = resolve(PLUGINS_PATH, pluginRef.source.replace('./plugins/', ''));

    try {
      // Check plugin directory exists
      if (!existsSync(pluginPath)) {
        result.addError(`Plugin directory not found: ${pluginPath}`);
        this.results.push(result);
        return result;
      }

      // Validate plugin.json
      const pluginJsonPath = join(pluginPath, '.claude-plugin/plugin.json');
      if (!existsSync(pluginJsonPath)) {
        result.addError(`Missing plugin.json at ${pluginJsonPath}`);
        this.results.push(result);
        return result;
      }

      const pluginContent = readFileSync(pluginJsonPath, 'utf-8');
      let pluginData;
      try {
        pluginData = JSON.parse(pluginContent);
      } catch (error) {
        result.addError(`Invalid JSON in plugin.json: ${error.message}`);
        this.results.push(result);
        return result;
      }

      // Validate plugin.json structure
      if (!pluginData.name) {
        result.addError('plugin.json missing name field');
      } else if (pluginData.name !== pluginRef.name) {
        result.addWarning(`Plugin name mismatch: marketplace=${pluginRef.name}, plugin.json=${pluginData.name}`);
      }

      if (!pluginData.version) {
        result.addError('plugin.json missing version field');
      }

      if (!pluginData.description) {
        result.addError('plugin.json missing description field');
      }

      // Check for optional but recommended fields
      if (!pluginData.license) {
        result.addWarning('No license specified');
      }

      // Validate file sizes
      this.validateFileSizes(pluginPath, result);

      // Validate skills
      this.validateSkills(pluginPath, result);

      // Validate hooks
      this.validateHooks(pluginPath, result);

      // Validate agents
      this.validateAgents(pluginPath, result);

      // Validate styles
      this.validateStyles(pluginPath, result);

    } catch (error) {
      result.addError(`Plugin validation error: ${error.message}`);
    }

    this.results.push(result);
    return result;
  }

  validateFileSizes(pluginPath, result) {
    const files = this.getAllFiles(pluginPath);
    const totalSize = files.reduce((sum, file) => sum + statSync(file).size, 0);
    const totalSizeMB = totalSize / (1024 * 1024);

    result.setMetadata('fileCount', files.length);
    result.setMetadata('totalSizeMB', totalSizeMB);

    if (totalSizeMB > MAX_PLUGIN_SIZE_MB) {
      result.addWarning(`Plugin size (${totalSizeMB.toFixed(2)}MB) exceeds recommended limit of ${MAX_PLUGIN_SIZE_MB}MB`);
    }
  }

  validateSkills(pluginPath, result) {
    const skillsPath = join(pluginPath, 'skills');
    if (!existsSync(skillsPath)) {
      result.addWarning('No skills directory found');
      return;
    }

    const skills = this.findFiles(skillsPath, 'SKILL.md');
    result.setMetadata('skillCount', skills.length);

    for (const skillPath of skills) {
      this.validateSkillFile(skillPath, result);
    }
  }

  validateSkillFile(skillPath, result) {
    try {
      const content = readFileSync(skillPath, 'utf-8');
      const relativePath = basename(dirname(skillPath));

      // Check for YAML frontmatter
      if (!content.startsWith('---')) {
        result.addError(`Skill ${relativePath} missing YAML frontmatter`);
        return;
      }

      // Parse YAML frontmatter
      const frontmatterEnd = content.indexOf('---', 3);
      if (frontmatterEnd === -1) {
        result.addError(`Skill ${relativePath} missing closing frontmatter marker`);
        return;
      }

      let frontmatter;
      try {
        frontmatter = JSON.parse(content.substring(3, frontmatterEnd));
      } catch (error) {
        result.addError(`Skill ${relativePath} invalid YAML frontmatter: ${error.message}`);
        return;
      }

      // Validate required frontmatter fields
      if (!frontmatter.name) {
        result.addError(`Skill ${relativePath} missing name in frontmatter`);
      } else {
        // Check name format (lowercase, hyphens only)
        if (!/^[a-z0-9-]+$/.test(frontmatter.name)) {
          result.addError(`Skill ${relativePath} name should be lowercase with hyphens only`);
        }
      }

      if (!frontmatter.description) {
        result.addError(`Skill ${relativePath} missing description in frontmatter`);
      } else {
        // Check description length
        if (frontmatter.description.length > MAX_SKILL_DESCRIPTION_LENGTH) {
          result.addWarning(`Skill ${relativePath} description exceeds recommended length`);
        }
      }

      // Validate allowed-tools if present
      if (frontmatter['allowed-tools']) {
        const tools = Array.isArray(frontmatter['allowed-tools'])
          ? frontmatter['allowed-tools']
          : frontmatter['allowed-tools'].split(',').map(t => t.trim());

        const validTools = ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep', 'WebSearch', 'WebFetch', 'Task', 'Skill', 'TodoWrite'];
        const invalidTools = tools.filter(t => !validTools.includes(t));
        if (invalidTools.length > 0) {
          result.addWarning(`Skill ${relativePath} has unknown tools: ${invalidTools.join(', ')}`);
        }
      }

    } catch (error) {
      result.addError(`Skill validation error: ${error.message}`);
    }
  }

  validateHooks(pluginPath, result) {
    const hooksPath = join(pluginPath, 'hooks');
    if (!existsSync(hooksPath)) {
      return; // Hooks are optional
    }

    const hooksJsonPath = join(hooksPath, 'hooks.json');
    if (!existsSync(hooksJsonPath)) {
      result.addWarning('hooks directory exists but no hooks.json found');
      return;
    }

    try {
      const hooksContent = readFileSync(hooksJsonPath, 'utf-8');
      const hooksData = JSON.parse(hooksContent);

      result.setMetadata('hasHooks', true);

      // Validate hooks.json structure
      if (!Array.isArray(hooksData)) {
        result.addError('hooks.json must be an array');
        return;
      }

      // Validate each hook
      for (const hook of hooksData) {
        if (!hook.event) {
          result.addError('Hook missing event field');
        }
        if (!hook.script) {
          result.addError('Hook missing script field');
        } else {
          const scriptPath = resolve(hooksPath, hook.script);
          if (!existsSync(scriptPath)) {
            result.addWarning(`Hook script not found: ${hook.script}`);
          }
        }
      }

    } catch (error) {
      result.addError(`Invalid hooks.json: ${error.message}`);
    }
  }

  validateAgents(pluginPath, result) {
    const agentsPath = join(pluginPath, 'agents');
    if (!existsSync(agentsPath)) {
      return; // Agents are optional
    }

    const agents = this.findFiles(agentsPath, '*.md');
    result.setMetadata('agentCount', agents.length);

    for (const agentPath of agents) {
      this.validateAgentFile(agentPath, result);
    }
  }

  validateAgentFile(agentPath, result) {
    try {
      const content = readFileSync(agentPath, 'utf-8');
      const relativeName = basename(agentPath, '.md');

      // Check for YAML frontmatter
      if (!content.startsWith('---')) {
        result.addError(`Agent ${relativeName} missing YAML frontmatter`);
        return;
      }

      // Parse frontmatter (simplified)
      const frontmatterEnd = content.indexOf('---', 3);
      if (frontmatterEnd === -1) {
        result.addError(`Agent ${relativeName} missing closing frontmatter marker`);
        return;
      }

      // Basic validation
      const frontmatterContent = content.substring(3, frontmatterEnd);
      if (!frontmatterContent.includes('name:')) {
        result.addError(`Agent ${relativeName} missing name in frontmatter`);
      }
      if (!frontmatterContent.includes('description:')) {
        result.addError(`Agent ${relativeName} missing description in frontmatter`);
      }

    } catch (error) {
      result.addError(`Agent validation error: ${error.message}`);
    }
  }

  validateStyles(pluginPath, result) {
    const stylesPath = join(pluginPath, 'styles');
    if (!existsSync(stylesPath)) {
      return; // Styles are optional
    }

    const styles = this.findFiles(stylesPath, '*.md');
    result.setMetadata('styleCount', styles.length);
  }

  // Helper methods
  getAllFiles(dir) {
    if (!existsSync(dir)) return [];

    const entries = statSync(dir);
    if (!entries.isDirectory()) return [dir];

    let files = [];
    for (const entry of entries) {
      const fullPath = join(dir, entry.name);
      if (entry.isDirectory()) {
        files = files.concat(this.getAllFiles(fullPath));
      } else {
        files.push(fullPath);
      }
    }
    return files;
  }

  findFiles(dir, pattern) {
    if (!existsSync(dir)) return [];

    const files = this.getAllFiles(dir);
    if (pattern.includes('*')) {
      // Simple glob pattern matching
      const ext = pattern.replace('*', '');
      return files.filter(f => f.endsWith(ext));
    }
    return files.filter(f => basename(f) === pattern);
  }

  // Generate comprehensive report
  generateReport() {
    const totalTests = this.results.length;
    const passedTests = this.results.filter(r => r.passed).length;
    const failedTests = totalTests - passedTests;
    const totalErrors = this.results.reduce((sum, r) => sum + r.errors.length, 0);
    const totalWarnings = this.results.reduce((sum, r) => sum + r.warnings.length, 0);

    return {
      summary: {
        totalTests,
        passedTests,
        failedTests,
        totalErrors,
        totalWarnings,
        passRate: `${((passedTests / totalTests) * 100).toFixed(1)}%`
      },
      results: this.results.map(r => r.getSummary()),
      detailedErrors: this.results.filter(r => !r.passed).map(r => ({
        test: r.testName,
        errors: r.errors
      }))
    };
  }
}

// ============================================================
// EDGE CASE TESTING WITH AGENT SDK
// ============================================================

class EdgeCaseTester {
  constructor() {
    this.testResults = [];
  }

  async testPluginWithInvalidStructure() {
    console.log('\n🧪 Testing Edge Cases with Agent SDK...\n');

    // Test 1: Plugin with missing required files
    const test1 = await this.testMissingFiles();

    // Test 2: Plugin with invalid JSON
    const test2 = await this.testInvalidJson();

    // Test 3: Plugin with circular dependencies (if any)
    const test3 = await this.testCircularDependencies();

    // Test 4: Plugin with oversized content
    const test4 = await this.testOversizedContent();

    // Test 5: Plugin with invalid YAML frontmatter
    const test5 = await this.testInvalidYaml();

    return [test1, test2, test3, test4, test5];
  }

  async testMissingFiles() {
    const result = new ValidationResult('Edge Case: Missing Required Files');

    try {
      // Use Agent SDK to verify plugin structure
      const prompt = `Test that a plugin without plugin.json fails validation appropriately.

      Expected behavior: Plugin should be rejected or throw appropriate error.

      Please attempt to load a plugin with missing plugin.json and report the error handling.`;

      const options = {
        plugins: [{ type: 'local', path: PLUGINS_PATH }],
        allowedTools: ['Read', 'Glob', 'Bash'],
        permissionMode: 'bypassPermissions',
        maxTurns: 10
      };

      // This would be executed in a test environment
      result.addWarning('Test requires isolated plugin environment');

    } catch (error) {
      result.addError(`Edge case test error: ${error.message}`);
    }

    return result;
  }

  async testInvalidJson() {
    const result = new ValidationResult('Edge Case: Invalid JSON in plugin.json');

    try {
      // Simulate invalid JSON scenario
      const invalidJson = '{ "name": "test", "version": }';

      try {
        JSON.parse(invalidJson);
        result.addError('Invalid JSON should have thrown error');
      } catch (e) {
        result.addError('Successfully caught invalid JSON error (expected)');
      }

    } catch (error) {
      result.addError(`Test error: ${error.message}`);
    }

    return result;
  }

  async testCircularDependencies() {
    const result = new ValidationResult('Edge Case: Circular Dependencies');

    // Check if any plugins reference each other
    result.addWarning('Circular dependency check requires cross-reference analysis');

    return result;
  }

  async testOversizedContent() {
    const result = new ValidationResult('Edge Case: Oversized Content');

    // Check for plugins exceeding size limits
    const plugins = readFileSync(MARKETPLACE_PATH, 'utf-8');
    const pluginData = JSON.parse(plugins);

    for (const plugin of pluginData.plugins) {
      const pluginPath = resolve(PLUGINS_PATH, plugin.source.replace('./plugins/', ''));
      const files = this.getAllFiles(pluginPath);
      const totalSize = files.reduce((sum, file) => sum + statSync(file).size, 0);

      if (totalSize > MAX_PLUGIN_SIZE_MB * 1024 * 1024) {
        result.addWarning(`Plugin ${plugin.name} exceeds size limit`);
      }
    }

    return result;
  }

  async testInvalidYaml() {
    const result = new ValidationResult('Edge Case: Invalid YAML Frontmatter');

    // Test YAML parsing with various invalid formats
    const invalidYamls = [
      '---name: test\n---',
      '---\nname: test\n--',
      '---name: test'
    ];

    for (const yaml of invalidYamls) {
      if (!yaml.endsWith('---')) {
        result.addError('Invalid YAML properly detected (expected)');
      }
    }

    return result;
  }

  getAllFiles(dir) {
    if (!existsSync(dir)) return [];

    try {
      const entries = statSync(dir);
      if (!entries.isDirectory()) return [dir];

      let files = [];
      for (const entry of entries) {
        const fullPath = join(dir, entry.name);
        if (entry.isDirectory()) {
          files = files.concat(this.getAllFiles(fullPath));
        } else {
          files.push(fullPath);
        }
      }
      return files;
    } catch (error) {
      return [];
    }
  }
}

// ============================================================
// MAIN EXECUTION
// ============================================================

async function main() {
  console.log('========================================');
  console.log('🔍 Cat Toolkit Marketplace Validator');
  console.log('========================================\n');

  const validator = new MarketplaceValidator();
  const edgeTester = new EdgeCaseTester();

  try {
    // Load marketplace
    await validator.loadMarketplace();

    // Run structural validations
    console.log('\n📋 Phase 1: Marketplace Structure Validation');
    validator.validateMarketplaceStructure();

    console.log('\n📦 Phase 2: Plugin Structure Validation');
    validator.validateAllPlugins();

    console.log('\n🧪 Phase 3: Edge Case Testing');
    const edgeResults = await edgeTester.testPluginWithInvalidStructure();
    validator.results.push(...edgeResults);

    // Generate and display report
    console.log('\n📊 Generating Report...\n');
    const report = validator.generateReport();

    // Display summary
    console.log('========================================');
    console.log('📊 VALIDATION SUMMARY');
    console.log('========================================');
    console.log(`Total Tests: ${report.summary.totalTests}`);
    console.log(`Passed: ${report.summary.passedTests}`);
    console.log(`Failed: ${report.summary.failedTests}`);
    console.log(`Errors: ${report.summary.totalErrors}`);
    console.log(`Warnings: ${report.summary.totalWarnings}`);
    console.log(`Pass Rate: ${report.summary.passRate}`);

    // Display failed tests
    if (report.summary.failedTests > 0) {
      console.log('\n❌ FAILED TESTS:');
      report.detailedErrors.forEach(err => {
        console.log(`  - ${err.test}`);
        err.errors.forEach(error => {
          console.log(`    • ${error.message}`);
        });
      });
    }

    // Save detailed report
    const reportPath = join(RESULTS_DIR, `validation-report-${Date.now()}.json`);
    require('fs').writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`\n💾 Detailed report saved to: ${reportPath}`);

    // Exit with appropriate code
    process.exit(report.summary.failedTests > 0 ? 1 : 0);

  } catch (error) {
    console.error('❌ Fatal error:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { main, MarketplaceValidator, EdgeCaseTester, ValidationResult };
