#!/usr/bin/env node

/**
 * Agent SDK-Based Integration Test Suite
 *
 * Tests plugin interactions, capabilities, and edge cases using the Claude Agent SDK
 * Inspired by adk_e2e framework but enhanced for marketplace validation
 */

import { config } from 'dotenv';
config({ path: resolve(__dirname, '../.env.local'), override: true });

import { query, type SDKMessage, type Options } from '@anthropic-ai/claude-agent-sdk';
import { readFileSync, writeFileSync, mkdirSync, existsSync, appendFileSync } from 'fs';
import { join, resolve, dirname } from 'path';

// ============================================================
// CONFIGURATION
// ============================================================

const RESULTS_DIR = join(process.cwd(), 'validation-results', 'integration');
const MARKETPLACE_PATH = resolve(__dirname, '../.claude-plugin/marketplace.json');
const PLUGINS_PATH = resolve(__dirname, '../plugins');

// Test configuration
const MAX_TURNS_PER_TEST = 50;
const TIMEOUT_MS = 180000; // 3 minutes

// ============================================================
// INTERFACES
// ============================================================

interface TestResult {
  testName: string;
  pluginName: string;
  success: boolean;
  duration: number;
  messageCount: number;
  turns: number;
  cost: number;
  errors: string[];
  warnings: string[];
  metadata: any;
}

interface IntegrationTest {
  name: string;
  description: string;
  plugins: string[];
  prompt: string;
  allowedTools: string[];
  expectedOutcomes: string[];
  edgeCases?: string[];
}

// ============================================================
// INTEGRATION TEST SUITE
// ============================================================

class IntegrationTestSuite {
  constructor() {
    this.results = [];
    this.testPlugins = this.loadTestPlugins();
  }

  loadTestPlugins() {
    try {
      const marketplace = JSON.parse(readFileSync(MARKETPLACE_PATH, 'utf-8'));
      return marketplace.plugins.map(p => p.name);
    } catch (error) {
      console.error('Failed to load marketplace:', error.message);
      return [];
    }
  }

  // Test 1: Individual Plugin Loading
  async testPluginLoading() {
    console.log('\n🧪 Test 1: Individual Plugin Loading\n');

    for (const pluginName of this.testPlugins) {
      const result = await this.runTest({
        name: `Plugin Loading: ${pluginName}`,
        pluginName,
        plugins: [pluginName],
        prompt: `Load and initialize the ${pluginName} plugin. Verify it loads successfully and report what capabilities are available.`,
        allowedTools: ['Read', 'Glob', 'Bash'],
        expectedOutcomes: ['Plugin loads successfully', 'Capabilities reported']
      });

      this.results.push(result);
    }
  }

  // Test 2: Cross-Plugin Interaction
  async testCrossPluginInteraction() {
    console.log('\n🧪 Test 2: Cross-Plugin Interaction\n');

    // Test bootstrap + execute
    const test1 = await this.runTest({
      name: 'Bootstrap + Execute Interaction',
      pluginName: 'bootstrap+execute',
      plugins: ['bootstrap', 'execute'],
      prompt: `Use the bootstrap plugin to understand system initialization, then use execute plugin to perform a file operation. Demonstrate how they work together.`,
      allowedTools: ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep', 'Task', 'Skill'],
      expectedOutcomes: ['Bootstrap provides context', 'Execute performs operations']
    });
    this.results.push(test1);

    // Test guide + reason
    const test2 = await this.runTest({
      name: 'Guide + Reason Interaction',
      pluginName: 'guide+reason',
      plugins: ['guide', 'reason'],
      prompt: `Use the reason plugin for strategic thinking about a task, then use guide plugin to structure a response. Show how reasoning informs guidance.`,
      allowedTools: ['Read', 'Glob', 'Grep', 'Task'],
      expectedOutcomes: ['Reasoning completed', 'Guidance structured']
    });
    this.results.push(test2);

    // Test persist + verify
    const test3 = await this.runTest({
      name: 'Persist + Verify Interaction',
      pluginName: 'persist+verify',
      plugins: ['persist', 'verify'],
      prompt: `Create some state with persist plugin, then verify the state is correct using verify plugin. Show state management and validation working together.`,
      allowedTools: ['Read', 'Write', 'Edit', 'Bash'],
      expectedOutcomes: ['State persisted', 'State verified']
    });
    this.results.push(test3);
  }

  // Test 3: Skill Discovery and Auto-loading
  async testSkillDiscovery() {
    console.log('\n🧪 Test 3: Skill Discovery and Auto-loading\n');

    const test = await this.runTest({
      name: 'Skill Auto-discovery',
      pluginName: 'all',
      plugins: this.testPlugins,
      prompt: `Test skill discovery by requesting various capabilities:
      1. Ask for plugin management skills
      2. Ask for hooks management
      3. Ask for subagent management
      4. Verify skills are auto-discovered based on descriptions`,
      allowedTools: ['Read', 'Glob', 'Grep', 'Bash', 'Task', 'Skill'],
      expectedOutcomes: ['Skills auto-discovered', 'Descriptions match requests']
    });
    this.results.push(test);
  }

  // Test 4: Hook System Validation
  async testHookSystem() {
    console.log('\n🧪 Test 4: Hook System Validation\n');

    const test = await this.runTest({
      name: 'Hook System',
      pluginName: 'bootstrap',
      plugins: ['bootstrap'],
      prompt: `Test the hook management system:
      1. Load hooks from the bootstrap plugin
      2. Verify hook scripts are executable
      3. Test hook validation logic
      4. Report on hook types available`,
      allowedTools: ['Read', 'Bash', 'Glob'],
      allowedTools: ['Read', 'Bash', 'Glob', 'Write'],
      expectedOutcomes: ['Hooks loaded', 'Scripts executable', 'Validation works']
    });
    this.results.push(test);
  }

  // Test 5: Permission System
  async testPermissionSystem() {
    console.log('\n🧪 Test 5: Permission System\n');

    // Test with bypassPermissions
    const test1 = await this.runTest({
      name: 'Permission: Bypass',
      pluginName: 'execute',
      plugins: ['execute'],
      prompt: `Test file operations with bypass permissions enabled. Create a test file, edit it, and verify operations succeed without prompts.`,
      allowedTools: ['Read', 'Write', 'Edit', 'Bash'],
      permissionMode: 'bypassPermissions',
      expectedOutcomes: ['Operations succeed', 'No permission prompts']
    });
    this.results.push(test1);

    // Test with default permissions
    const test2 = await this.runTest({
      name: 'Permission: Default',
      pluginName: 'execute',
      plugins: ['execute'],
      prompt: `Test file operations with default permission mode. Verify that permission checks are in place.`,
      allowedTools: ['Read', 'Write', 'Edit', 'Bash'],
      permissionMode: 'default',
      expectedOutcomes: ['Permission checks active']
    });
    this.results.push(test2);
  }

  // Test 6: Error Handling and Edge Cases
  async testErrorHandling() {
    console.log('\n🧪 Test 6: Error Handling and Edge Cases\n');

    // Test 6a: Invalid file operations
    const test1 = await this.runTest({
      name: 'Error: Invalid File Operation',
      pluginName: 'execute',
      plugins: ['execute'],
      prompt: `Attempt to read a non-existent file to test error handling. Verify appropriate error messages are returned.`,
      allowedTools: ['Read', 'Bash'],
      expectedOutcomes: ['Error handled gracefully', 'Clear error message']
    });
    this.results.push(test1);

    // Test 6b: Permission denial
    const test2 = await this.runTest({
      name: 'Error: Permission Denial',
      pluginName: 'execute',
      plugins: ['execute'],
      prompt: `Test permission system by attempting operations with restricted tools.`,
      allowedTools: ['Read'], // Restrict tools
      permissionMode: 'default',
      expectedOutcomes: ['Operations blocked', 'Clear denial message']
    });
    this.results.push(test2);

    // Test 6c: Malformed plugin structure
    const test3 = await this.runTest({
      name: 'Error: Malformed Plugin',
      pluginName: 'invalid',
      plugins: ['nonexistent'],
      prompt: `Attempt to load a non-existent plugin and verify error handling.`,
      allowedTools: ['Read', 'Glob'],
      expectedOutcomes: ['Error handled gracefully', 'Plugin not found message']
    });
    this.results.push(test3);
  }

  // Test 7: Agent Delegation
  async testAgentDelegation() {
    console.log('\n🧪 Test 7: Agent Delegation\n');

    const test = await this.runTest({
      name: 'Agent Delegation',
      pluginName: 'bootstrap',
      plugins: ['bootstrap'],
      prompt: `Test agent delegation features:
      1. Create a subagent using the plugin-expert agent
      2. Delegate a task to the subagent
      3. Verify subagent reports back with results
      4. Test multi-agent coordination`,
      allowedTools: ['Read', 'Glob', 'Grep', 'Task'],
      expectedOutcomes: ['Subagent created', 'Task delegated', 'Results returned']
    });
    this.results.push(test);
  }

  // Test 8: Performance and Resource Usage
  async testPerformance() {
    console.log('\n🧪 Test 8: Performance and Resource Usage\n');

    const test = await this.runTest({
      name: 'Performance Benchmark',
      pluginName: 'all',
      plugins: this.testPlugins,
      prompt: `Perform a comprehensive benchmark:
      1. Load all plugins
      2. Execute operations across multiple plugins
      3. Measure response times
      4. Check for memory leaks or resource issues
      5. Report on overall performance`,
      allowedTools: ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep', 'Task', 'Skill'],
      expectedOutcomes: ['All plugins load', 'Operations complete', 'Performance measured']
    });
    this.results.push(test);
  }

  // Test 9: Session and State Management
  async testSessionManagement() {
    console.log('\n🧪 Test 9: Session and State Management\n');

    const test = await this.runTest({
      name: 'Session and State',
      pluginName: 'persist',
      plugins: ['persist'],
      prompt: `Test session and state management:
      1. Create persistent state
      2. Verify state persists across operations
      3. Test state cleanup
      4. Verify memory management`,
      allowedTools: ['Read', 'Write', 'Edit', 'Bash'],
      expectedOutcomes: ['State created', 'State persists', 'Cleanup works']
    });
    this.results.push(test);
  }

  // Test 10: MCP Integration
  async testMCPIntegration() {
    console.log('\n🧪 Test 10: MCP Integration\n');

    const test = await this.runTest({
      name: 'MCP Server Integration',
      pluginName: 'all',
      plugins: this.testPlugins,
      prompt: `Test MCP integration capabilities:
      1. Check if any plugins define MCP servers
      2. Test MCP server connection
      3. Verify MCP protocol compliance
      4. Test external service integration`,
      allowedTools: ['Read', 'Glob', 'Bash', 'WebSearch', 'WebFetch'],
      expectedOutcomes: ['MCP servers identified', 'Connection tested', 'Protocol validated']
    });
    this.results.push(test);
  }

  // Core test execution method
  async runTest(testConfig) {
    const startTime = Date.now();
    const messages = [];
    let success = false;
    let errors = [];
    let warnings = [];
    let turns = 0;
    let cost = 0;

    try {
      console.log(`  Running: ${testConfig.name}`);

      // Prepare plugin paths
      const pluginPaths = testConfig.plugins.map(p => {
        if (p === 'nonexistent') return null;
        return { type: 'local', path: join(PLUGINS_PATH, p) };
      }).filter(p => p !== null);

      const options = {
        plugins: pluginPaths,
        maxTurns: MAX_TURNS_PER_TEST,
        permissionMode: testConfig.permissionMode || 'bypassPermissions',
        allowDangerouslySkipPermissions: true,
        settingSources: ['project'],
        cwd: join(RESULTS_DIR, 'sandbox', testConfig.pluginName),
        systemPrompt: { type: 'preset', preset: 'claude_code' },
        tools: { type: 'preset', preset: 'claude_code' },
        env: { ...process.env },
        hooks: {
          PreToolUse: [this.logToolUse.bind(this)],
          PostToolUse: [this.logToolResult.bind(this)],
          Stop: [this.captureSessionMetadata.bind(this)]
        }
      };

      const stream = query({ prompt: testConfig.prompt, options });

      for await (const message of stream) {
        messages.push(message);

        // Track turns
        if (message.type === 'assistant') {
          turns++;
        }

        // Track cost
        if (message.total_cost_usd !== undefined) {
          cost = message.total_cost_usd;
        }

        // Check for success
        if (message.type === 'result') {
          success = message.subtype === 'success';
          if (!success) {
            errors = message.errors || [];
          }
          break;
        }
      }

      // Validate expected outcomes
      const outcomeValidation = this.validateExpectedOutcomes(
        testConfig.expectedOutcomes,
        messages
      );
      warnings = outcomeValidation.warnings;
      if (!outcomeValidation.success) {
        success = false;
        errors.push(...outcomeValidation.errors);
      }

    } catch (error) {
      success = false;
      errors.push(error.message);
    }

    const duration = Date.now() - startTime;

    const result = {
      testName: testConfig.name,
      pluginName: testConfig.pluginName,
      success,
      duration,
      messageCount: messages.length,
      turns,
      cost,
      errors,
      warnings,
      metadata: {
        expectedOutcomes: testConfig.expectedOutcomes,
        allowedTools: testConfig.allowedTools,
        timestamp: new Date().toISOString()
      }
    };

    console.log(`  ${success ? '✅' : '❌'} ${testConfig.name} (${duration}ms, ${turns} turns, $${cost.toFixed(4)})`);

    return result;
  }

  // Hook handlers
  logToolUse(input) {
    appendFileSync(
      join(RESULTS_DIR, 'tool-usage.log'),
      `${new Date().toISOString()} - Tool: ${input.tool_name}\n`
    );
    return {};
  }

  logToolResult(input, toolUseId, context) {
    appendFileSync(
      join(RESULTS_DIR, 'tool-results.log'),
      `${new Date().toISOString()} - Tool Result: ${toolUseId}\n`
    );
    return {};
  }

  captureSessionMetadata(result, context) {
    appendFileSync(
      join(RESULTS_DIR, 'session-metadata.log'),
      `${new Date().toISOString()} - Session complete: ${JSON.stringify(result)}\n`
    );
    return {};
  }

  // Validate expected outcomes
  validateExpectedOutcomes(expectedOutcomes, messages) {
    const result = { success: true, errors: [], warnings: [] };

    for (const outcome of expectedOutcomes) {
      const found = messages.some(msg => {
        if (typeof msg.message === 'string') {
          return msg.message.toLowerCase().includes(outcome.toLowerCase());
        }
        return false;
      });

      if (!found) {
        result.warnings.push(`Expected outcome not found: ${outcome}`);
      }
    }

    if (result.errors.length > 0) {
      result.success = false;
    }

    return result;
  }

  // Generate comprehensive report
  generateReport() {
    const total = this.results.length;
    const passed = this.results.filter(r => r.success).length;
    const failed = total - passed;
    const totalCost = this.results.reduce((sum, r) => sum + r.cost, 0);
    const avgDuration = this.results.reduce((sum, r) => sum + r.duration, 0) / total;

    return {
      summary: {
        total,
        passed,
        failed,
        passRate: `${((passed / total) * 100).toFixed(1)}%`,
        totalCost: totalCost.toFixed(4),
        avgDuration: `${avgDuration.toFixed(0)}ms`
      },
      results: this.results,
      summaryByPlugin: this.groupResultsByPlugin()
    };
  }

  groupResultsByPlugin() {
    const grouped = {};
    for (const result of this.results) {
      const plugin = result.pluginName;
      if (!grouped[plugin]) {
        grouped[plugin] = [];
      }
      grouped[plugin].push(result);
    }
    return grouped;
  }
}

// ============================================================
// MAIN EXECUTION
// ============================================================

async function main() {
  console.log('========================================');
  console.log('🧪 Agent SDK Integration Test Suite');
  console.log('========================================\n');

  // Ensure results directory exists
  mkdirSync(RESULTS_DIR, { recursive: true });

  const suite = new IntegrationTestSuite();

  try {
    // Run all tests
    await suite.testPluginLoading();
    await suite.testCrossPluginInteraction();
    await suite.testSkillDiscovery();
    await suite.testHookSystem();
    await suite.testPermissionSystem();
    await suite.testErrorHandling();
    await suite.testAgentDelegation();
    await suite.testPerformance();
    await suite.testSessionManagement();
    await suite.testMCPIntegration();

    // Generate report
    console.log('\n📊 Generating Integration Test Report...\n');
    const report = suite.generateReport();

    // Display summary
    console.log('========================================');
    console.log('📊 INTEGRATION TEST SUMMARY');
    console.log('========================================');
    console.log(`Total Tests: ${report.summary.total}`);
    console.log(`Passed: ${report.summary.passed}`);
    console.log(`Failed: ${report.summary.failed}`);
    console.log(`Pass Rate: ${report.summary.passRate}`);
    console.log(`Total Cost: $${report.summary.totalCost}`);
    console.log(`Avg Duration: ${report.summary.avgDuration}`);

    // Save report
    const reportPath = join(RESULTS_DIR, `integration-report-${Date.now()}.json`);
    writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`\n💾 Report saved to: ${reportPath}`);

    // Exit with appropriate code
    process.exit(report.summary.failed > 0 ? 1 : 0);

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

export { main, IntegrationTestSuite };
