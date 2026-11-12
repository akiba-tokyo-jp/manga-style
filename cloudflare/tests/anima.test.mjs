import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker.mjs';

test('Anima API and namespaced images are independent from legacy GPT', async () => {
  const seen = [];
  const payload = { id: 'anima-example', model: { id: 'anima-turbo', version: 'anima-turbo-v1.1' }, prompt: { en: 'ink contours', ja: null } };
  const env = { ASSETS: { async fetch(request) {
    const path = new URL(request.url).pathname; seen.push(path);
    if (path === '/_data/styles/anima-turbo/anima-example.json') return Response.json({ ja: payload, en: payload });
    if (path === '/files/anima-turbo/anima-example/a.png') return new Response(new Uint8Array([137, 80, 78, 71]));
    return new Response('missing', { status: 404 });
  } } };
  const get = (path, init) => worker.fetch(new Request('https://preview.example' + path, init), env);
  const style = await get('/v1/styles/anima-example?model=anima-turbo&lang=en');
  assert.equal(style.status, 200);
  assert.deepEqual(await style.json(), payload);
  assert.equal((await get('/v1/styles/anima-example')).status, 404);
  assert.equal((await get('/v1/styles/gpt-example?model=anima-turbo')).status, 404);
  const image = await get('/files/anima-turbo/anima-example/a.png', { headers: { Cookie: 'manga_model=gpt-image' } });
  assert.equal(image.status, 200);
  assert.equal(image.headers.get('Content-Type'), 'image/png');
  assert.equal(image.headers.get('Cache-Control'), 'public, max-age=31536000, immutable');
  assert.equal((await get('/files/anima-turbo/anima-example/a.png', { method: 'HEAD' })).body, null);
  assert.equal((await get('/files/anima-turbo/anima-example/a.png?model=gpt-image')).status, 404);
  assert.equal((await get('/files/anima-turbo/anima-example/missing.png')).status, 404);
  assert.ok(seen.includes('/_data/styles/anima-turbo/anima-example.json'));
});

test('Anima-only category routes never admit the same category under GPT', async () => {
  const meta = { roots: ['shonen'], topics: {}, facets: {}, visible: ['anima-example'],
    model_visible: { 'gpt-image': [], 'anima-turbo': ['anima-example'] },
    model_roots: { 'gpt-image': ['shonen'], 'anima-turbo': ['shonen', 'other'] } };
  const env = { ASSETS: { async fetch(request) {
    const path = new URL(request.url).pathname;
    if (path === '/_data/routes.json') return Response.json(meta);
    if (path === '/_data/gallery/ja-anima-turbo.html') return new Response('ANIMA GALLERY');
    if (path === '/_data/gallery/ja-gpt-image.html') return new Response('GPT GALLERY');
    if (path === '/_data/error/ja-gpt-image.html') return new Response('GPT NOT FOUND');
    return new Response('missing', { status: 404 });
  } } };
  const get = path => worker.fetch(new Request('https://preview.example' + path), env);
  assert.equal((await get('/n/other?model=anima-turbo')).status, 200);
  assert.equal((await get('/search?root=other&model=anima-turbo')).status, 200);
  assert.equal((await get('/n/other?model=gpt-image')).status, 404);
  assert.equal((await get('/n/other')).status, 404);
  assert.equal((await get('/search?root=other&model=gpt-image')).status, 400);
  assert.deepEqual(meta.roots, ['shonen']);
});
