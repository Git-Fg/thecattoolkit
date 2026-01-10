#!/usr/bin/env node

/**
 * Full Marketplace Validation Pipeline
 *
 * Orchestrates all validation phases:
 * 1. Structural validation
 * 2. Integration testing
 * 3. Edge case testing
 * 4. Performance benchmarking
 * 5. Security analysis
 * 6. Compliance checking
 */

import { spawn } from 'child_process';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

// ============================================================
// CONFIGURATION
// ============================================================

const VALIDATION_PHASES = [
  { name: 'structural', script: './marketplace-validator.js', required: true },
  { name: 'integration', script: './integration-tester.js', required: true },
  { name: 'edge-cases', script: './edge-case-tester.js', required: false },
  { name: 'performance', script: './performance-benchmark.js', required: false },
  { name: 'security', script: './security-scanner.js', required: false }
];

const RESULTS_DIR = join(process.cwd(), 'validation-results');
const FINAL_REPORT_PATH = join(RESULTS_DIR, 'final-validation-report.json');

// ============================================================
// PIPELINE ORCHESTRATOR
// ============================================================

class ValidationPipeline {
  constructor() {
    this.phaseResults = [];
    this.startTime = Date.now();
  }

  async run() {
    console.log('🚀 Starting Full Marketplace Validation Pipeline\n');
    console.log(`Timestamp: ${new Date().toISOString()}`);
    console.log(`Results Directory: ${RESULTS_DIR}\n`);

    // Ensure results directory exists
    require('fs').mkdirSync(RESULTS_DIR, { recursive: true });

    // Run each validation phase
    for (const phase of VALIDATION_PHASES) {
      await this.runPhase(phase);
    }

    // Generate final report
    await this.generateFinalReport();

    // Display summary
    this.displaySummary();

    // Exit with appropriate code
    const allPassed = this.phaseResults.every(r => r.success);
    process.exit(allPassed ? 0 : 1);
  }

  async runPhase(phase) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`🔍 Phase: ${phase.name.toUpperCase()}`);
    console.log(`${'='.repeat(60)}\n`);

    const phaseStart = Date.now();

    try {
      // Check if script exists
      const scriptPath = join(__dirname, phase.script);
      if (!existsSync(scriptPath)) {
        if (phase.required) {
          throw new Error(`Required phase script not found: ${scriptPath}`);
        } else {
          console.log(`⚠️  Optional phase script not found, skipping: ${phase.name}`);
          this.phaseResults.push({
            name: phase.name,
            success: false,
            skipped: true,
            duration: 0,
            error: 'Script not found'
          });
          return;
        }
      }

      // Run the validation script
      const result = await this.runScript(scriptPath);

      this.phaseResults.push({
        name: phase.name,
        success: result.success,
        duration: Date.now() - phaseStart,
        output: result.output,
        error: result.error
      });

      if (result.success) {
        console.log(`\n✅ Phase completed: ${phase.name}`);
      } else {
        console.log(`\n❌ Phase failed: ${phase.name}`);
        if (result.error) {
          console.error(`Error: ${result.error}`);
        }
      }

    } catch (error) {
      console.error(`\n❌ Phase error: ${phase.name}`);
      console.error(error.message);

      this.phaseResults.push({
        name: phase.name,
        success: false,
        duration: Date.now() - phaseStart,
        error: error.message
      });
    }
  }

  runScript(scriptPath) {
    return new Promise((resolve) => {
      const child = spawn('node', [scriptPath], {
        stdio: ['inherit', 'pipe', 'pipe']
      });

      let output = '';
      let error = '';

      child.stdout.on('data', (data) => {
        const str = data.toString();
        process.stdout.write(str);
        output += str;
      });

      child.stderr.on('data', (data) => {
        const str = data.toString();
        process.stderr.write(str);
        error += str;
      });

      child.on('close', (code) => {
        resolve({
          success: code === 0,
          output,
          error: code !== 0 ? error : null
        });
      });
    });
  }

  async generateFinalReport() {
    const totalDuration = Date.now() - this.startTime;
    const phases = this.phaseResults.length;
    const passedPhases = this.phaseResults.filter(r => r.success).length;
    const failedPhases = phases - passedPhases;
    const allPassed = failedPhases === 0;

    const report = {
      metadata: {
        timestamp: new Date().toISOString(),
        totalDuration: `${(totalDuration / 1000).toFixed(2)}s`,
        phases,
        passedPhases,
        failedPhases
      },
      summary: {
        overallStatus: allPassed ? 'PASSED' : 'FAILED',
        passRate: `${((passedPhases / phases) * 100).toFixed(1)}%`
      },
      phases: this.phaseResults,
      recommendations: this.generateRecommendations(),
      nextSteps: this.generateNextSteps()
    };

    writeFileSync(FINAL_REPORT_PATH, JSON.stringify(report, null, 2));
    console.log(`\n📊 Final report saved to: ${FINAL_REPORT_PATH}`);

    return report;
  }

  generateRecommendations() {
    const recommendations = [];

    for (const result of this.phaseResults) {
      if (!result.success) {
        if (result.name === 'structural') {
          recommendations.push({
            priority: 'HIGH',
            message: 'Fix structural issues in plugin definitions before proceeding',
            phase: 'structural'
          });
        } else if (result.name === 'integration') {
          recommendations.push({
            priority: 'HIGH',
            message: 'Resolve plugin interaction failures',
            phase: 'integration'
          });
        } else if (result.name === 'edge-cases') {
          recommendations.push({
            priority: 'MEDIUM',
            message: 'Improve error handling for edge cases',
            phase: 'edge-cases'
          });
        } else if (result.name === 'security') {
          recommendations.push({
            priority: 'CRITICAL',
            message: 'Address security vulnerabilities immediately',
            phase: 'security'
          });
        }
      }
    }

    // General recommendations
    if (recommendations.length === 0) {
      recommendations.push({
        priority: 'LOW',
        message: 'All validation phases passed. Consider implementing automated validation in CI/CD',
        phase: 'all'
      });
    }

    return recommendations;
  }

  generateNextSteps() {
    const steps = [];

    if (this.phaseResults.some(r => !r.success && r.name === 'structural')) {
      steps.push('Review structural validation errors and fix plugin definitions');
    }

    if (this.phaseResults.some(r => !r.success && r.name === 'integration')) {
      steps.push('Review integration test failures and fix plugin interactions');
    }

    steps.push('Re-run validation pipeline after fixes');
    steps.push('Consider adding validation to pre-commit hooks');
    steps.push('Set up automated validation in CI/CD pipeline');

    return steps;
  }

  displaySummary() {
    console.log(`\n${'='.repeat(60)}`);
    console.log('📊 FINAL VALIDATION SUMMARY');
    console.log(`${'='.repeat(60)}\n`);

    console.log(`Overall Status: ${this.phaseResults.every(r => r.success) ? '✅ PASSED' : '❌ FAILED'}`);
    console.log(`Total Duration: ${((Date.now() - this.startTime) / 1000).toFixed(2)}s`);
    console.log(`Phases: ${this.phaseResults.length}\n`);

    console.log('Phase Breakdown:');
    for (const result of this.phaseResults) {
      const status = result.success ? '✅' : (result.skipped ? '⏭️' : '❌');
      const duration = `${(result.duration / 1000).toFixed(2)}s`;
      console.log(`  ${status} ${result.name.padEnd(15)} ${duration}`);
    }

    console.log('\nRecommendations:');
    const recommendations = this.generateRecommendations();
    for (const rec of recommendations) {
      console.log(`  [${rec.priority}] ${rec.message}`);
    }

    console.log('\nNext Steps:');
    const nextSteps = this.generateNextSteps();
    for (const step of nextSteps) {
      console.log(`  • ${step}`);
    }

    console.log(`\n${'='.repeat(60)}\n`);
  }
}

// ============================================================
// MAIN EXECUTION
// ============================================================

async function main() {
  const pipeline = new ValidationPipeline();
  await pipeline.run();
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { main, ValidationPipeline };
