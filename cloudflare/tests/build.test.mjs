import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { existsSync, mkdtempSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const root = fileURLToPath(new URL('../../', import.meta.url));
const build = fileURLToPath(new URL('../build.mjs', import.meta.url));

test('an unavailable Windows volume fails instead of looping during snapshot path resolution', { skip: process.platform !== 'win32' }, () => {
  const drive = ['Z', 'Y', 'X', 'W'].find(letter => !existsSync(letter + ':/'));
  assert.ok(drive, 'fixture requires one unavailable test volume');
  const result = spawnSync(process.execPath, [build, '--snapshot-dir', drive + ':/missing-snapshot'], {
    cwd: root, encoding: 'utf8', timeout: 2000,
    env: { ...process.env, PATH: '', PYTHON: 'intentionally-missing-test-python' },
  });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /cannot resolve/i);
});

test('snapshot output, report and archive overlaps are rejected before tool bootstrap', () => {
  const directory = mkdtempSync(join(process.env.TMPDIR || tmpdir(), 'manga-build-guard-'));
  try {
    const snapshot = join(directory, 'snapshot'), reportSnapshot = join(directory, 'build-report.json');
    mkdirSync(snapshot); mkdirSync(reportSnapshot);
    for (const args of [
      ['--snapshot-dir', snapshot, '--output', join(snapshot, 'export')],
      ['--snapshot-dir=' + snapshot, '--archive-dir=' + join(snapshot, 'archives')],
      ['--snapshot-dir', reportSnapshot, '--output', join(directory, 'assets')],
    ]) {
      const result = spawnSync(process.execPath, [build, ...args], {
        cwd: root, encoding: 'utf8',
        env: { ...process.env, PATH: '', PYTHON: 'intentionally-missing-test-python' },
      });
      assert.equal(result.status, 1);
      assert.match(result.stderr, /snapshot overlaps a build write target/);
    }
    assert.deepEqual(readdirSync(snapshot), []);
    assert.deepEqual(readdirSync(reportSnapshot), []);
  } finally { rmSync(directory, { recursive: true, force: true }); }
});

test('abbreviated, unknown, missing and empty snapshot options fail before bootstrap', () => {
  for (const [args, envExtra, message] of [
    [['--snapshot-d', root], {}, /unknown build option/i],
    [['--snapshot-dir='], {}, /snapshot.*empty/i],
    [['--snapshot-dir', ''], {}, /snapshot.*empty/i],
    [[], { MANGA_SNAPSHOT_DIR: '' }, /snapshot.*empty/i],
    [['--snapshot-dir'], {}, /missing value/i],
  ]) {
    const result = spawnSync(process.execPath, [build, ...args], {
      cwd: root, encoding: 'utf8', timeout: 10000,
      env: { ...process.env, PATH: '', PYTHON: 'intentionally-missing-test-python', ...envExtra },
    });
    assert.equal(result.status, 1);
    assert.match(result.stderr, message);
  }
});

test('snapshot checkout overlap is rejected before bootstrapping build tools', () => {
  const result = spawnSync(process.execPath, [build, '--snapshot-dir', root], {
    cwd: root, encoding: 'utf8',
    env: { ...process.env, PATH: '', PYTHON: 'intentionally-missing-test-python' },
  });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /snapshot.*outside.*checkout/i);
});
