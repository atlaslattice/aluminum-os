#!/usr/bin/env node

import { Command } from 'commander';
import { buildLineagePayload } from './utils/dependency-graph.js';
import { generateTreeHash } from './utils/dependency-graph.js';
import { acquireExecutionLease, isLeaseStructurallyValid } from './lease.js';

const program = new Command();

program
  .name('royalty')
  .description('Royalty Runtime SDK — Execution is compensation')
  .version('0.1.0');

program
  .command('trace')
  .description('Build and display the canonical lineage payload')
  .option('-p, --path <path>', 'Project root path', process.cwd())
  .option('--json', 'Output raw JSON', false)
  .action((opts) => {
    try {
      const lineage = buildLineagePayload(opts.path);
      if (opts.json) {
        console.log(JSON.stringify(lineage, null, 2));
      } else {
        console.log('\n  ROYALTY RUNTIME — LINEAGE TRACE\n');
        console.log(`  Package:      ${lineage.primary_package.name}@${lineage.primary_package.version}`);
        console.log(`  Runtime:      ${lineage.runtime.name} ${lineage.runtime.version}`);
        console.log(`  Dependencies: ${lineage.resolved_dependencies.length} resolved`);
        lineage.resolved_dependencies.forEach((dep) => {
          console.log(`    -> ${dep.name}@${dep.version}`);
        });
        console.log(`\n  Tree Hash:    ${generateTreeHash(lineage)}\n`);
      }
    } catch (err: any) {
      console.error(`[ROYALTY] Trace failed: ${err.message}`);
      process.exit(1);
    }
  });

program
  .command('hash')
  .description('Generate SHA-256 tree hash for the current dependency state')
  .option('-p, --path <path>', 'Project root path', process.cwd())
  .action((opts) => {
    try {
      const lineage = buildLineagePayload(opts.path);
      console.log(generateTreeHash(lineage));
    } catch (err: any) {
      console.error(`[ROYALTY] Hash failed: ${err.message}`);
      process.exit(1);
    }
  });

program
  .command('emit')
  .description('Emit a test execution event to the collector')
  .option('-p, --path <path>', 'Project root path', process.cwd())
  .option('--collector <url>', 'Collector URL', 'http://localhost:3210')
  .option('--tenant <id>', 'Tenant ID', 'dev-local')
  .action(async (opts) => {
    try {
      const lineage = buildLineagePayload(opts.path);
      const hash = generateTreeHash(lineage);
      const event = {
        event_type: 'cli_test_emit',
        lineage_hash: hash,
        tenant_id: opts.tenant,
        primary_package_name: lineage.primary_package.name,
        primary_package_version: lineage.primary_package.version,
        dependency_count: lineage.resolved_dependencies.length,
        premium_path_enabled: false,
        payload_json: lineage,
      };
      const response = await fetch(`${opts.collector}/v1/executions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event),
      });
      if (!response.ok) throw new Error(`Collector returned ${response.status}`);
      console.log('[ROYALTY] Event emitted successfully');
      console.log(JSON.stringify(await response.json(), null, 2));
    } catch (err: any) {
      console.error(`[ROYALTY] Emit failed: ${err.message}`);
      process.exit(1);
    }
  });

program
  .command('weight')
  .description('Calculate attribution weights for the current dependency tree')
  .option('-p, --path <path>', 'Project root path', process.cwd())
  .option('--simulate <amount>', 'Simulate royalty distribution', '100')
  .action((opts) => {
    try {
      const lineage = buildLineagePayload(opts.path);
      const total = lineage.resolved_dependencies.length;
      const primaryWeight = 0.4;
      const depWeight = total > 0 ? 0.6 / total : 0;
      const amount = parseFloat(opts.simulate);

      console.log('\n  ROYALTY RUNTIME — ATTRIBUTION WEIGHTS');
      console.log(`  Strategy: primary_40_equal_split_60 (v0.1)\n`);
      console.log(`  ${lineage.primary_package.name}  ${(primaryWeight * 100).toFixed(1)}%  $${(amount * primaryWeight).toFixed(2)}`);
      lineage.resolved_dependencies.forEach((dep) => {
        console.log(`  ${dep.name}  ${(depWeight * 100).toFixed(1)}%  $${(amount * depWeight).toFixed(2)}`);
      });
      console.log(`\n  Total: $${amount.toFixed(2)}  Confidence: experimental\n`);
    } catch (err: any) {
      console.error(`[ROYALTY] Weight failed: ${err.message}`);
      process.exit(1);
    }
  });

program
  .command('verify')
  .description('Verify a lease token is structurally valid')
  .argument('<token>', 'JWT lease token')
  .action((token) => {
    if (isLeaseStructurallyValid(token)) {
      const parts = token.split('.');
      const payload = JSON.parse(Buffer.from(parts[1], 'base64url').toString('utf-8'));
      console.log('[ROYALTY] Lease token is structurally valid');
      console.log(`  Tenant: ${payload.sub}  Hash: ${payload.lineage_hash}  Exp: ${new Date(payload.exp * 1000).toISOString()}`);
    } else {
      console.error('[ROYALTY] Lease token is invalid or expired');
      process.exit(1);
    }
  });

program
  .command('lease')
  .description('Acquire an execution lease from the collector')
  .option('-p, --path <path>', 'Project root path', process.cwd())
  .option('--collector <url>', 'Collector URL', 'http://localhost:3210')
  .option('--tenant <id>', 'Tenant ID', 'dev-local')
  .action(async (opts) => {
    try {
      const lineage = buildLineagePayload(opts.path);
      const lease = await acquireExecutionLease(
        { collectorUrl: opts.collector, tenantId: opts.tenant }, lineage);
      console.log('[ROYALTY] Lease acquired');
      console.log(`  ID: ${lease.lease_id}  Expires: ${lease.expires_at}  Caps: ${lease.capabilities.join(', ')}`);
    } catch (err: any) {
      console.error(`[ROYALTY] Lease failed: ${err.message}`);
      process.exit(1);
    }
  });

program.parse();