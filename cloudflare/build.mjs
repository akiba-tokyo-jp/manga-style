import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, realpathSync } from 'node:fs';
import { basename, dirname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';

const args = process.argv.slice(2);
const root = fileURLToPath(new URL('../', import.meta.url));
const values = new Map();
const accepted = new Set(['--snapshot-dir', '--archive-dir', '--output']);
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--help' || args[i] === '-h') continue;
  const equal = args[i].indexOf('=');
  const name = equal < 0 ? args[i] : args[i].slice(0, equal);
  if (!accepted.has(name)) throw new Error('Unknown build option: ' + name);
  const value = equal < 0 ? args[++i] : args[i].slice(equal + 1);
  if (value === undefined || (equal < 0 && value.startsWith('-'))) throw new Error('Missing value for ' + name);
  if (name === '--snapshot-dir' && value === '') throw new Error('snapshot directory must not be empty');
  values.set(name, value);
}
function option(name, fallback) { return values.has(name) ? values.get(name) : fallback; }
function canonical(path) {
  let cursor = resolve(path);
  const tail = [];
  while (!existsSync(cursor)) {
    const parent = dirname(cursor);
    if (parent === cursor) throw new Error('Cannot resolve snapshot/build path: ' + path);
    tail.unshift(basename(cursor)); cursor = parent;
  }
  return resolve(realpathSync(cursor), ...tail);
}
function contains(parent, child) {
  const value = relative(parent, child);
  return !value || (value !== '..' && !value.startsWith('..' + sep) && !isAbsolute(value));
}
const snapshot = option('--snapshot-dir', process.env.MANGA_SNAPSHOT_DIR);
if (snapshot !== undefined && snapshot !== null) {
  if (snapshot === '') throw new Error('snapshot directory must not be empty');
  const source = canonical(snapshot), checkout = canonical(root);
  if (contains(source, checkout) || contains(checkout, source)) throw new Error('snapshot must be outside the checkout');
  const output = option('--output', join(root, 'dist/assets'));
  const targets = [output, join(dirname(output), 'build-report.json'),
    option('--archive-dir', process.env.MANGA_ARCHIVE_DIR || join(root, '.build/archives')),
    join(root, '.build/bootstrap'), join(root, 'costlab-auth/manga/app/seed/additions'),
    join(root, 'costlab-auth/manga/app/seed/pairs'), join(root, 'costlab-auth/manga/compare/files')];
  for (const path of targets) {
    const target = canonical(path);
    if (contains(source, target) || contains(target, source)) throw new Error('snapshot overlaps a build write target');
  }
  if (contains(source, canonical(tmpdir()))) throw new Error('snapshot contains the temporary directory');
}

function run(command, args) {
  const result = spawnSync(command, args, { stdio: 'inherit', env: process.env });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}

// Cloudflare Builds need only Node + Python; bootstrap a pinned uv in a local
// venv when it is not installed. Never install packages into the system Python.
let uv = 'uv';
if (spawnSync(uv, ['--version'], { stdio: 'ignore' }).status !== 0) {
  const directory = join('.build', 'bootstrap');
  const windows = process.platform === 'win32';
  const python = join(directory, windows ? 'Scripts/python.exe' : 'bin/python');
  uv = join(directory, windows ? 'Scripts/uv.exe' : 'bin/uv');
  if (!existsSync(python)) {
    mkdirSync('.build', { recursive: true });
    run(process.env.PYTHON || 'python3', ['-m', 'venv', directory]);
  }
  if (!existsSync(uv)) run(python, ['-m', 'pip', 'install', 'uv==0.12.18']);
}
run(uv, ['run', '--no-project', '--python', '3.12', '--with-requirements',
  'costlab-auth/manga/requirements.txt', 'python', 'tools/manga_catalog/export_cloudflare.py', ...process.argv.slice(2)]);
