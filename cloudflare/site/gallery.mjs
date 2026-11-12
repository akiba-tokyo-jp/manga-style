import { selectPage } from './catalogue.mjs';

// Reuse the original HTML/CSS. User strings are always textContent or URLSearchParams.
function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = String(text);
  return node;
}
const format = (text, values) => text.replace(/\{(\w+)\}/g, (_, key) => String(values[key] ?? ''));

async function render() {
  const response = await fetch('/_public/catalogue.json', { cache: 'no-cache' });
  if (!response.ok) throw new Error('catalogue unavailable');
  const index = await response.json();
  const lang = document.documentElement.lang;
  const text = index.text[lang], ui = index.ui[lang];
  const current = new URL(location.href);
  const genko = current.searchParams.get('client') === 'genko' || Boolean(document.querySelector('input[name=client][value=genko]'));
  const model = document.body.dataset.activeModel;
  const rootFromPath = current.pathname.startsWith('/n/') ? current.pathname.slice(3) : '';
  const filterParams = new URLSearchParams(current.searchParams);
  filterParams.set('model', model);
  const selected = selectPage(index, filterParams, lang, rootFromPath);
  const byId = new Map(index.records.map(record => [record.id, record]));
  function link(path, extra = {}) {
    const params = new URLSearchParams({ lang, model, ...extra });
    if (genko) params.set('client', 'genko');
    for (const [key, value] of [...params]) if (!value) params.delete(key);
    return path + '?' + params;
  }
  const conditions = { root: selected.root, topic: selected.topic, q: selected.q, ...selected.facets };
  document.querySelector('.gallery-intro h1').textContent = selected.root ? byId.get(selected.root).labels[lang].title : text.heading;
  document.querySelector('#gallery-query').value = selected.q;
  for (const form of document.querySelectorAll('form')) {
    for (const [key, value] of Object.entries({ ...conditions, lang, model })) {
      const field = form.elements.namedItem(key);
      if (field) field.value = value;
      else if (form.classList.contains('gallery-search') && key === 'root' && value) {
        const input = element('input'); input.type = 'hidden'; input.name = key; input.value = value; form.append(input);
      }
    }
  }
  const topics = document.querySelector('.gallery-filters select[name=topic]');
  if (topics) {
    topics.replaceChildren(new Option(text.all, ''));
    for (const record of index.records) {
      if (record.level !== 2 || record.look_group || (selected.root && record.chain[0] !== selected.root)) continue;
      topics.add(new Option(record.chain.map(id => byId.get(id).labels[lang].title).join(ui.path_sep), record.id));
    }
    topics.value = selected.topic;
  }
  for (const anchor of document.querySelectorAll('.category-strip a')) {
    const target = new URL(anchor.href);
    const id = target.pathname.startsWith('/n/') ? target.pathname.slice(3) : '';
    if (selected.root === id) anchor.setAttribute('aria-current', 'true');
    else anchor.removeAttribute('aria-current');
  }
  for (const anchor of document.querySelectorAll('.lang-switch, .model-tab')) {
    const target = new URL(anchor.href);
    target.pathname = '/search';
    for (const [key, value] of Object.entries(conditions)) value ? target.searchParams.set(key, value) : target.searchParams.delete(key);
    for (const key of ['page', 'plang', 'view']) {
      if (current.searchParams.has(key)) target.searchParams.set(key, current.searchParams.get(key));
    }
    if (genko) target.searchParams.set('client', 'genko');
    anchor.href = target.pathname + target.search;
  }
  const clear = document.querySelector('.filter-clear');
  if (clear) clear.href = link('/search', { root: selected.root });
  // A preparing model has no records; populated models render only their own cards.
  if (model !== 'gpt-image' && !index.records.some(record => record.model === model)) { document.body.dataset.galleryReady = 'true'; return; }
  const container = document.querySelector('.gallery-results');
  container.setAttribute('aria-label', format(text.results, { n: selected.total }));
  const bar = element('div', 'results-bar');
  bar.append(element('h2', '', format(text.results, { n: selected.total })), element('span', '', format(text.page, selected)));
  container.replaceChildren(bar);
  if (selected.topic) {
    const p = element('p'), a = element('a', 'text-link', text.topic_basic);
    a.href = link('/n/' + selected.topic); p.append(a); container.append(p);
  }
  if (genko && selected.root && model === 'gpt-image') {
    const p = element('p'), a = element('a', 'text-link', ui.use_style + ' — ' + byId.get(selected.root).labels[lang].title);
    a.href = 'genko://use-style?id=' + selected.root; p.append(a); container.append(p);
  }
  if (!selected.ids.length) container.append(element('p', 'gallery-no-results', text.none));
  else {
    const list = element('ul', 'gallery-grid');
    for (const id of selected.ids) {
      const record = byId.get(id), label = record.labels[lang];
      const li = element('li'), anchor = element('a', 'gallery-card');
      anchor.dataset.styleId = id; anchor.dataset.level = String(record.level);
      anchor.href = link((record.level === 1 ? '/styles/' : '/n/') + id);
      const picture = element('span', 'gallery-image');
      if (label.thumb_url) {
        const image = element('img'); image.src = label.thumb_url; image.alt = label.title;
        image.loading = 'lazy'; image.width = 384; image.height = 512; picture.append(image);
      } else picture.append(element('span', 'gallery-no-image', ui.no_sample));
      const body = element('span', 'gallery-card-body'), bottom = element('span', 'gallery-card-bottom');
      bottom.append(element('span', '', label.model_name), element('code', '', id));
      body.append(element('span', 'card-path', label.path || text.basic), element('strong', '', label.title), bottom);
      anchor.append(picture, body); li.append(anchor); list.append(li);
    }
    container.append(list);
  }
  const pagination = element('nav', 'pagination');
  pagination.setAttribute('aria-label', lang === 'ja' ? 'ページ' : 'Pages');
  if (selected.page > 1) {
    const a = element('a', 'page-link', '← ' + text.previous); a.href = link('/search', { ...conditions, page: selected.page - 1 }); pagination.append(a);
  }
  pagination.append(element('span', '', format(text.page, selected)));
  if (selected.page < selected.pages) {
    const a = element('a', 'page-link', text.next + ' →'); a.href = link('/search', { ...conditions, page: selected.page + 1 }); pagination.append(a);
  }
  container.append(pagination);
  document.body.dataset.galleryReady = 'true';
}

render().catch(() => {
  document.body.dataset.galleryReady = 'error';
  const message = element('p', 'gallery-no-results', document.documentElement.lang === 'ja'
    ? '絵柄一覧を読み込めませんでした。再読み込みしてください。' : 'Could not load the catalogue. Please reload.');
  message.setAttribute('role', 'alert');
  document.querySelector('.gallery-results')?.replaceChildren(message);
});
