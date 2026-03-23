import { readFileSync } from 'fs';
import { resolve } from 'path';
import { createHash } from 'crypto';

export interface PackageMeta {
  name: string;
  version: string;
}

export interface DependencyEntry {
  name: string;
  version: string;
}

export interface CanonicalLineage {
  primary_package: PackageMeta;
  runtime: PackageMeta;
  lockfile_digest: string;
  resolved_dependencies: DependencyEntry[];
}

/**
 * Build the canonical lineage payload from the current project.
 * Extracts resolved dependency state from lockfile, normalizes
 * (sorted alphabetically), and produces deterministic payload.
 */
export function buildLineagePayload(projectRoot?: string): CanonicalLineage {
  const root = projectRoot || process.cwd();

  const pkgPath = resolve(root, 'package.json');
  const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));

  const lockfilePath = resolve(root, 'package-lock.json');
  const lockfileRaw = readFileSync(lockfilePath, 'utf-8');
  const lockfile_digest = 'sha256:' + createHash('sha256').update(lockfileRaw).digest('hex');
  const lockfile = JSON.parse(lockfileRaw);

  let rawDeps: Record<string, any> = {};

  if (lockfile.packages && lockfile.packages['']) {
    const rootPkg = lockfile.packages[''];
    rawDeps = rootPkg.dependencies || {};
  } else if (lockfile.dependencies) {
    rawDeps = lockfile.dependencies;
  }

  // CRITICAL: Alphabetical sort guarantees identical arrays across machines
  const resolved_dependencies: DependencyEntry[] = Object.keys(rawDeps)
    .sort()
    .map((name) => ({
      name,
      version: typeof rawDeps[name] === 'string'
        ? rawDeps[name]
        : rawDeps[name].version || 'unknown',
    }));

  return {
    primary_package: {
      name: pkg.name || 'unknown',
      version: pkg.version || '0.0.0',
    },
    runtime: {
      name: 'node',
      version: process.versions.node,
    },
    lockfile_digest,
    resolved_dependencies,
  };
}

/**
 * Generate SHA-256 hash of canonical lineage payload.
 * Mirrors Rust core hashing: serialize to minified JSON then SHA-256.
 */
export function generateTreeHash(lineage: CanonicalLineage): string {
  const canonical = JSON.stringify(lineage);
  return createHash('sha256').update(canonical).digest('hex');
}