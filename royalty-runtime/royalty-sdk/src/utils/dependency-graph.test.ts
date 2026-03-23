import { describe, it, expect } from 'vitest';
import { generateTreeHash, type CanonicalLineage } from './dependency-graph.js';

function mockLineage(overrides?: Partial<CanonicalLineage>): CanonicalLineage {
  return {
    primary_package: { name: 'test-app', version: '1.0.0' },
    runtime: { name: 'node', version: '20.11.0' },
    lockfile_digest: 'sha256:abcdef1234567890',
    resolved_dependencies: [
      { name: 'express', version: '4.18.2' },
      { name: 'pg', version: '8.11.3' },
      { name: 'zod', version: '3.22.4' },
    ],
    ...overrides,
  };
}

describe('Lineage Hash Generation', () => {
  it('same_input_same_hash', () => {
    const hash1 = generateTreeHash(mockLineage());
    const hash2 = generateTreeHash(mockLineage());
    expect(hash1).toBe(hash2);
  });

  it('version_change_changes_hash', () => {
    const hash1 = generateTreeHash(mockLineage());
    const hash2 = generateTreeHash(
      mockLineage({
        resolved_dependencies: [
          { name: 'express', version: '4.18.3' },
          { name: 'pg', version: '8.11.3' },
          { name: 'zod', version: '3.22.4' },
        ],
      }),
    );
    expect(hash1).not.toBe(hash2);
  });

  it('dependency_order_matters_for_hash', () => {
    const sorted = mockLineage();
    const unsorted = mockLineage({
      resolved_dependencies: [
        { name: 'zod', version: '3.22.4' },
        { name: 'express', version: '4.18.2' },
        { name: 'pg', version: '8.11.3' },
      ],
    });
    expect(generateTreeHash(sorted)).not.toBe(generateTreeHash(unsorted));
  });

  it('hash_is_64_hex_chars', () => {
    const hash = generateTreeHash(mockLineage());
    expect(hash).toMatch(/^[0-9a-f]{64}$/);
  });

  it('different_primary_package_changes_hash', () => {
    const hash1 = generateTreeHash(mockLineage());
    const hash2 = generateTreeHash(
      mockLineage({ primary_package: { name: 'other-app', version: '1.0.0' } }),
    );
    expect(hash1).not.toBe(hash2);
  });

  it('adding_dependency_changes_hash', () => {
    const base = mockLineage();
    const extended = mockLineage({
      resolved_dependencies: [
        ...base.resolved_dependencies,
        { name: 'lodash', version: '4.17.21' },
      ],
    });
    expect(generateTreeHash(base)).not.toBe(generateTreeHash(extended));
  });
});