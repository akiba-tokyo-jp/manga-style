import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
const entry = new URL('../site/catalogue.mjs', import.meta.url);
test('static gallery preserves category, topic, AND-search, facets and pagination semantics', async () => {
  assert.ok(existsSync(entry), 'static gallery filtering is not implemented');
  const { selectPage } = await import(entry);
  const record = (id, level, chain, hay, features = {}) => ({ id, level, chain, features, labels: { ja: { hay }, en: { hay } } });
  const index = { casefold: { 'ß': 'ss' }, page_size: 2, facets: { expression: [['mono'], ['color']], line: [['thin']] }, records: [
    record('genre', 1, ['genre'], 'genre'), record('topic', 2, ['genre', 'topic'], 'topic'),
    record('style', 3, ['genre', 'topic', 'style'], 'strasse cute ink', { line: ['thin'], expression: ['mono'] }),
    record('other', 3, ['genre', 'topic', 'other'], 'cute color', { expression: ['color'] }),
  ] };
  assert.deepEqual(selectPage(index, new URLSearchParams(), 'ja').ids, ['genre', 'style']);
  assert.deepEqual(selectPage(index, new URLSearchParams('topic=topic'), 'en').ids, ['topic', 'style']);
  assert.deepEqual(selectPage(index, new URLSearchParams('q=STRAßE+ink&line=thin'), 'en').ids, ['style']);
  assert.deepEqual(selectPage(index, new URLSearchParams('expression=color'), 'ja').ids, ['other']);
  assert.equal(selectPage(index, new URLSearchParams('page=9999'), 'ja').page, 2);
  assert.throws(() => selectPage(index, new URLSearchParams('root=bad'), 'ja'));
  assert.throws(() => selectPage(index, new URLSearchParams('line=bad'), 'ja'));
  assert.throws(() => selectPage(index, new URLSearchParams('page=1e3'), 'ja'));
});
