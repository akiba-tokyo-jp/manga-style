import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';

const entry = new URL('../worker.mjs', import.meta.url);

test('image reads ignore UI cookies and private paths never become SPA fallbacks', async () => {
  const { default: worker } = await import(entry);
  const env = { ASSETS: { async fetch(request) {
    return new URL(request.url).pathname === '/files/test-style/a.jpg' ? new Response(new Uint8Array([255, 216, 255, 217])) : new Response('', { status: 404 });
  } } };
  const get = (path, init) => worker.fetch(new Request('https://preview.example' + path, init), env);
  const image = await get('/files/test-style/a.jpg', { headers: { Cookie: 'manga_model=anima-turbo' } });
  assert.equal(image.status, 200);
  assert.equal(image.headers.get('Content-Type'), 'image/jpeg');
  assert.equal((await get('/files/test-style/a.jpg', { method: 'HEAD' })).body, null);
  for (const path of ['/admin', '/internal/queue', '/state.json', '/_data/routes.json', '/.git/config', '/static/admin.js']) {
    assert.equal((await get(path)).status, 404);
  }
  assert.equal((await get('/admin')).headers.get('Cache-Control'), 'private, no-store');
  assert.equal((await get('/v1/tree', { method: 'POST' })).status, 405);
  assert.equal((await get('/v1/tree/')).status, 307);
});

test('API models are explicit; Anima is empty and never borrows GPT styles or images', async () => {
  const { default: worker } = await import(entry);
  const env = { ASSETS: { async fetch(request) {
    const path = new URL(request.url ?? request).pathname;
    const values = {
      '/_data/tree/ja-anima-turbo.json': { version: 1, nodes: [], model: { id: 'anima-turbo' } },
      '/_data/models.json': { models: [{ id: 'gpt-image', style_count: 3 }, { id: 'anima-turbo', style_count: 0 }] },
      '/_data/styles/test-style.json': { ja: { id: 'test-style' } },
    };
    return Object.hasOwn(values, path) ? Response.json(values[path]) : new Response('', { status: 404 });
  } } };
  const fetch = (path, init) => worker.fetch(new Request('https://preview.example' + path, init), env);
  assert.equal((await fetch('/v1/styles/test-style?model=unknown')).status, 400);
  assert.equal((await fetch('/v1/styles/test-style?model=')).status, 400);
  assert.deepEqual((await (await fetch('/v1/tree?model=anima-turbo')).json()).nodes, []);
  assert.equal((await fetch('/v1/styles/test-style?model=anima-turbo')).status, 404);
  assert.equal((await fetch('/files/test-style/a.jpg?model=anima-turbo')).status, 404);
  assert.equal((await (await fetch('/v1/models')).json()).models[1].style_count, 0);
  assert.equal((await fetch('/v1/styles/test-style', { headers: { Cookie: 'manga_model=anima-turbo' } })).status, 200);
  const preflight = await fetch('/v1/unknown', { method: 'OPTIONS' });
  assert.equal(preflight.status, 204);
  assert.equal(preflight.headers.get('Access-Control-Allow-Headers'), 'Authorization');
});

test('legacy bilingual style API keeps its payload and resolves URLs against preview origin', async () => {
  assert.ok(existsSync(entry), 'compatibility Worker is not implemented');
  const { default: worker } = await import(entry);
  const payload = { id: 'test-style', prompt: { ja: '線', en: 'Lines', tags: 'line art' },
    samples: [{ url: 'https://static.manga.invalid/files/test-style/a.jpg' }] };
  const paths = [];
  const env = { ASSETS: { async fetch(request) {
    const path = new URL(request.url ?? request).pathname;
    paths.push(path);
    if (path === '/_data/styles/test-style.json') return Response.json({ ja: { ...payload, title: '絵' }, en: { ...payload, title: 'Style' } });
    return new Response('missing', { status: 404 });
  } } };
  const response = await worker.fetch(new Request('https://preview.example/v1/styles/test-style?lang=en'), env);
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('Access-Control-Allow-Origin'), '*');
  assert.deepEqual(await response.json(), { ...payload, title: 'Style', samples: [{ url: 'https://preview.example/files/test-style/a.jpg' }] });
  assert.deepEqual(paths, ['/_data/styles/test-style.json']);
});
