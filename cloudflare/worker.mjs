import { validateFilters } from './site/catalogue.mjs';

const PLACEHOLDER = 'https://static.manga.invalid';
const GPT = 'gpt-image', ANIMA = 'anima-turbo';
const CORS = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET',
  'Access-Control-Allow-Headers': 'Authorization', 'Access-Control-Max-Age': '600' };
const CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'";
const routeCache = new WeakMap();
const escapeHtml = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

async function asset(env, url, path, required = false) {
  const response = await env.ASSETS.fetch(new Request(new URL(path, url)));
  if (response.status !== 200 && (required || response.status !== 404)) throw new Error('build unavailable');
  return response;
}
function routes(env, url) {
  if (!routeCache.has(env.ASSETS)) {
    const promise = asset(env, url, '/_data/routes.json', true).then(response => response.json());
    routeCache.set(env.ASSETS, promise);
    promise.catch(() => routeCache.delete(env.ASSETS));
  }
  return routeCache.get(env.ASSETS);
}
function modelOf(request, url, api) {
  const explicit = url.searchParams.get('model');
  if (explicit !== null) {
    if (explicit !== GPT && explicit !== ANIMA) throw new Error('unknown model');
    return explicit;
  }
  const cookie = !api && request.headers.get('Cookie')?.split(';').map(v => v.trim()).find(v => v.startsWith('manga_model='))?.slice(12);
  return cookie === ANIMA ? ANIMA : GPT;
}
function result(body, request, { status = 200, type = 'application/json; charset=utf-8', cache = 'no-cache', model } = {}) {
  const url = new URL(request.url);
  const headers = new Headers({ 'Content-Type': type, 'Cache-Control': cache,
    'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'strict-origin-when-cross-origin' });
  if (url.pathname.startsWith('/v1/')) {
    Object.entries(CORS).forEach(([k, v]) => headers.set(k, v));
    headers.set('Vary', 'Origin, Authorization');
  }
  if (type.startsWith('text/html')) {
    headers.set('Content-Security-Policy', CSP);
    headers.set('Vary', 'Accept-Language, User-Agent, Cookie');
    if (model) headers.set('Set-Cookie', `manga_model=${model}; Max-Age=31536000; Path=/; HttpOnly; SameSite=Lax${url.protocol === 'https:' ? '; Secure' : ''}`);
  }
  if (/^\/(admin|internal)/.test(url.pathname)) {
    headers.set('Cache-Control', 'private, no-store');
    headers.set('X-Robots-Tag', 'noindex, nofollow, noarchive');
  }
  return new Response(request.method === 'HEAD' ? null : body, { status, headers });
}
const error = (r, status, text) => result(JSON.stringify({ error: text }), r, { status });
const json = (data, r) => result(JSON.stringify(data).replaceAll(PLACEHOLDER, new URL(r.url).origin), r);

function page(body, request, lang, model, meta) {
  const url = new URL(request.url);
  const genko = url.searchParams.get('client') === 'genko' || (request.headers.get('User-Agent') || '').includes('GenkoStudio');
  const compare = model === GPT && url.searchParams.get('view') === 'compare';
  const plang = url.searchParams.get('plang');
  const keepPromptLanguage = model === ANIMA && ['ja', 'en'].includes(plang);
  const response = result(body.replaceAll(PLACEHOLDER, url.origin), request, { type: 'text/html; charset=utf-8', model });
  if (request.method === 'HEAD' || (!genko && !compare && !keepPromptLanguage)) return response;
  let rewriter = new HTMLRewriter();
  if (keepPromptLanguage) rewriter = rewriter.on('.model-tab, .lang-switch', { element(el) {
    const target = new URL(el.getAttribute('href').replaceAll('&amp;', '&'), url);
    target.searchParams.set('plang', plang);
    el.setAttribute('href', target.pathname + target.search + target.hash);
  } });
  if (genko) {
    rewriter = rewriter.on('a[href]', { element(el) {
      const href = el.getAttribute('href');
      if (!href?.startsWith('/') || href.startsWith('//') || /^\/(files|static)\//.test(href)) return;
      const target = new URL(href.replaceAll('&amp;', '&'), url);
      target.searchParams.set('client', 'genko');
      el.setAttribute('href', target.pathname + target.search + target.hash);
    } }).on('.url-field, .use-style-note', { element(el) { el.remove(); } })
      .on('form', { element(el) { el.append('<input type="hidden" name="client" value="genko">', { html: true }); } });
  }
  if (compare) rewriter = rewriter.on('.node', { element(el) {
    el.before('<div class="model-comparison"><div><h2>GPT Image</h2>', { html: true });
    el.after(`</div><div>${meta.empty[lang]}</div></div><p class="quiet-note">${escapeHtml(meta.compare_note[lang])}</p>`, { html: true });
  } });
  return rewriter.transform(response);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url), path = url.pathname;
    const api = path.startsWith('/v1/');
    if (api && request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
    if (!['GET', 'HEAD'].includes(request.method)) return error(request, 405, 'method not allowed');
    try {
      if (/^\/(admin|internal|_data\/)/.test(path) || path.includes('%')) return error(request, 404, 'not found');
      if (path === '/healthz') return json((await routes(env, url)).health, request);
      if (path === '/v1/models') return json(await (await asset(env, url, '/_data/models.json', true)).json(), request);
      const lang = ['ja', 'en'].includes(url.searchParams.get('lang')) ? url.searchParams.get('lang') : (!api && (request.headers.get('Accept-Language') || '').trim().toLowerCase().startsWith('en') ? 'en' : 'ja');
      let model;
      try { model = modelOf(request, url, api || path.startsWith('/files/')); } catch { return error(request, 400, 'unknown model'); }
      const style = path.match(/^\/v1\/styles\/([a-z0-9]+(?:-[a-z0-9]+)*)$/);
      if (style) {
        const prefix = model === GPT ? '' : 'anima-turbo/';
        const response = await asset(env, url, `/_data/styles/${prefix}${style[1]}.json`);
        return response.status === 200 ? json((await response.json())[lang], request) : error(request, 404, 'not found');
      }
      if (path === '/v1/tree') return json(await (await asset(env, url, `/_data/tree/${lang}-${model}.json`, true)).json(), request);
      if (/^\/files\/anima-turbo\/[a-z0-9]+(?:-[a-z0-9]+)*\/[a-zA-Z0-9_.-]+\.(?:png|jpg)$/.test(path)) {
        if (url.searchParams.has('model') && model !== ANIMA) return error(request, 404, 'not found');
        const response = await asset(env, url, path);
        const type = path.endsWith('.png') ? 'image/png' : 'image/jpeg';
        return response.status === 200 ? result(response.body, request, { type, cache: 'public, max-age=31536000, immutable' }) : error(request, 404, 'not found');
      }
      if (/^\/files\/[a-z0-9]+(?:-[a-z0-9]+)*\/[a-zA-Z0-9_.-]+\.jpg$/.test(path)) {
        if (model !== GPT) return error(request, 404, 'not found');
        const response = await asset(env, url, path);
        return response.status === 200 ? result(response.body, request, { type: 'image/jpeg', cache: 'public, max-age=31536000, immutable' }) : error(request, 404, 'not found');
      }
      if (/^\/static\/(site\.css|gallery\.css|site\.js|gallery\.mjs|catalogue\.mjs)$/.test(path) || path === '/_public/catalogue.json' || path === '/robots.txt') {
        const response = await asset(env, url, path, true);
        const type = path.endsWith('.css') ? 'text/css; charset=utf-8' : /\.m?js$/.test(path) ? 'application/javascript; charset=utf-8' : path.endsWith('.json') ? 'application/json; charset=utf-8' : 'text/plain; charset=utf-8';
        return result(response.body, request, { type, cache: path.endsWith('.json') ? 'no-cache' : 'public, max-age=300' });
      }
      const node = path.match(/^\/(n|styles)\/([a-z0-9]+(?:-[a-z0-9]+)*)$/);
      if (node || ['/', '/search', '/api'].includes(path)) {
        const meta = await routes(env, url);
        const modelRoots = meta.model_roots?.[model] ?? meta.roots;
        const modelMeta = { ...meta, roots: modelRoots };
        const rootCategory = node?.[1] === 'n' && modelRoots.includes(node[2]);
        const visible = model === GPT ? (meta.model_visible?.[GPT] || meta.visible) : meta.visible;
        if (node && !rootCategory && !visible.includes(node[2])) {
          const body = await (await asset(env, url, `/_data/error/${lang}-${model}.html`, true)).text();
          return result(body.replaceAll(PLACEHOLDER, url.origin), request, { status: 404, type: 'text/html; charset=utf-8', model });
        }
        const root = node?.[1] === 'n' && modelRoots.includes(node[2]) ? node[2] : '';
        if (path === '/' || path === '/search' || root) {
          try { validateFilters(modelMeta, url.searchParams, root); } catch { return error(request, 400, 'invalid gallery filter'); }
          return page(await (await asset(env, url, `/_data/gallery/${lang}-${model}.html`, true)).text(), request, lang, model, meta);
        }
        if (path === '/api') return page(await (await asset(env, url, `/_data/guide/${lang}-${model}.html`, true)).text(), request, lang, model, meta);
        const bundle = await (await asset(env, url, `/_data/pages/${node[2]}.json`, true)).json();
        const plang = model !== GPT ? 'en' : ['ja', 'en'].includes(url.searchParams.get('plang')) ? url.searchParams.get('plang') : lang;
        const body = bundle[lang][model][plang] ?? bundle[lang][model].ja;
        return page(body, request, lang, model, meta);
      }
      if (/^\/(?:api|search|v1\/(?:models|tree|styles\/[a-z0-9-]+)|(?:n|styles)\/[a-z0-9-]+)\/$/.test(path)) {
        url.pathname = path.slice(0, -1);
        return new Response(null, { status: 307, headers: { Location: url.href, 'Cache-Control': 'no-cache' } });
      }
      return error(request, 404, 'not found');
    } catch {
      return error(request, 503, 'static catalogue unavailable');
    }
  },
};
