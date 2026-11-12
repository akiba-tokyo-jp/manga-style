import { test, expect } from '@playwright/test';

const NID = 'shonen-battle-chibi-comic';

test('gallery search and filters agree with exported catalogue, keeping paths and model selection', async ({ page }) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/?lang=ja&model=gpt-image');
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-card')).toHaveCount(48);
  await page.screenshot({ path: `dist/verification/${test.info().project.name}-gallery.png` });
  await page.locator('#gallery-query').fill(NID);
  await page.locator('.gallery-search button[type=submit]').click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-card')).toHaveCount(1);
  await expect(page.locator('.gallery-card')).toHaveAttribute('data-style-id', NID);
  await expect(page.locator('.results-bar h2')).toHaveText('1件の絵柄');
  await page.locator('.lang-switch').click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-card')).toHaveCount(1);
  await expect(page.locator('.results-bar h2')).toHaveText('1 styles');
  expect(errors).toEqual([]);
});

test('detail preserves two images, language-specific prompts, clipboard, comparison, and Anima separation', async ({ page, context, request }) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const api = await (await request.get('/v1/styles/' + NID + '?lang=ja')).json();
  await page.goto('/n/' + NID + '?lang=ja&plang=en&model=gpt-image');
  await expect(page.locator('#prompt-text')).toHaveValue(api.prompt.en);
  await page.screenshot({ path: `dist/verification/${test.info().project.name}-detail.png` });
  await expect(page.locator('.sample-pair img')).toHaveCount(2);
  for (const image of await page.locator('.sample-pair img').all()) {
    await expect(image).toBeVisible();
    await expect.poll(() => image.evaluate(img => img.complete && img.naturalWidth > 0)).toBe(true);
  }
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  await page.locator('button[data-copy-target=prompt-text]').click();
  await expect.poll(() => page.evaluate(() => navigator.clipboard.readText())).toContain(api.prompt.en);
  await page.locator('.compare-link').click();
  await expect(page.locator('.model-comparison')).toHaveCount(1);
  await expect(page.locator('.model-comparison .model-empty')).toHaveCount(1);
  await page.locator('.model-tab', { hasText: 'Anima Turbo' }).click();
  await expect(page.locator('.model-empty')).toHaveCount(1);
  await expect(page.locator('#prompt-text')).toHaveCount(0);
  await expect(page.locator('.sample-image')).toHaveCount(0);
  await page.locator('.lang-switch').click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  await expect(page.locator('.model-empty')).toHaveCount(1);
  await page.locator('.lang-switch').click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'ja');
  await page.locator('.model-tab', { hasText: 'GPT Image' }).click();
  await expect(page.locator('#prompt-text')).toHaveValue(api.prompt.en);
  expect(errors).toEqual([]);
});

test('Anima gallery keeps category and search filters through language and model round trips', async ({ page }) => {
  await page.goto('/search?lang=ja&model=gpt-image&root=shonen&q=chibi&expression=mono');
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  const ids = await page.locator('.gallery-card').evaluateAll(nodes => nodes.map(node => node.dataset.styleId));
  expect(ids.length).toBeGreaterThan(0);
  await page.locator('.model-tab', { hasText: 'Anima Turbo' }).click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('#gallery-query')).toHaveValue('chibi');
  await expect(page.locator('.gallery-intro h1')).toHaveText('少年漫画');
  await expect(page.locator('.gallery-card, .sample-image, #prompt-text')).toHaveCount(0);
  await page.locator('.lang-switch').click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  expect(new URL(page.url()).searchParams.get('root')).toBe('shonen');
  expect(new URL(page.url()).searchParams.get('expression')).toBe('mono');
  await page.locator('.lang-switch').click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await page.locator('.model-tab', { hasText: 'GPT Image' }).click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  expect(await page.locator('.gallery-card').evaluateAll(nodes => nodes.map(node => node.dataset.styleId))).toEqual(ids);
  await page.goto('/n/shonen?lang=ja&model=anima-turbo&q=chibi&expression=mono');
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-intro h1')).toHaveText('少年漫画');
  const back = new URL(await page.locator('.model-tab', { hasText: 'GPT Image' }).getAttribute('href'), page.url());
  expect(back.searchParams.get('root')).toBe('shonen');
  expect(back.searchParams.get('q')).toBe('chibi');
  expect(back.searchParams.get('expression')).toBe('mono');
  await expect(page.locator('.gallery-card, .sample-image, #prompt-text')).toHaveCount(0);
});

test('Anima gallery, exact English prompts, images and clipboard are live model-specific content', async ({ page, context, request }) => {
  const models = await (await request.get('/v1/models')).json();
  const count = models.models.find(model => model.id === 'anima-turbo').style_count;
  expect(count).toBeGreaterThan(0);
  const catalogue = await (await request.get('/_public/catalogue.json')).json();
  const visibleCount = Math.min(count, catalogue.page_size);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/search?lang=ja&model=anima-turbo');
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-card')).toHaveCount(visibleCount);
  expect(await page.locator('.gallery-card').evaluateAll(cards => cards.every(card => card.dataset.styleId.startsWith('anima-')))).toBe(true);
  await expect(page.locator('.gallery-card img')).toHaveCount(visibleCount);
  for (const image of await page.locator('.gallery-card img').all()) {
    await image.scrollIntoViewIfNeeded();
    await expect.poll(() => image.evaluate(img => img.complete && img.naturalWidth > 0)).toBe(true);
    expect(await image.evaluate(img => new URL(img.src).origin === location.origin)).toBe(true);
  }
  await page.screenshot({ path: `dist/verification/${test.info().project.name}-anima-gallery.png` });
  const id = await page.locator('.gallery-card').first().getAttribute('data-style-id');
  const api = await (await request.get('/v1/styles/' + id + '?model=anima-turbo&lang=ja')).json();
  expect(api.prompt.ja).toBeUndefined();
  expect(api.samples).toHaveLength(2);
  expect(api.samples.map(sample => sample.subject)).toEqual(['mixed-gender', 'showcase']);
  expect(new Set(api.samples.map(sample => sample.sha256)).size).toBe(2);
  expect(new Set(api.samples.map(sample => sample.native_job_id)).size).toBe(2);
  await page.locator('.gallery-card').first().click();
  await expect(page.locator('#prompt-text')).toHaveAttribute('lang', 'en');
  await expect(page.locator('#prompt-text')).toHaveValue(api.prompt.en);
  await expect(page.locator('.sample-image')).toHaveCount(2);
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  for (let i = 0; i < api.samples.length; i++) {
    const sample = api.samples[i];
    expect(sample.prompt.ja).toBeUndefined();
    await expect(page.locator('#sample-prompt-' + i)).toHaveText(sample.prompt.en);
    const image = page.locator('.sample-image').nth(i);
    await image.scrollIntoViewIfNeeded();
    await expect.poll(() => image.evaluate(img => img.complete && img.naturalWidth > 0)).toBe(true);
    await page.locator('.sample-prompt > summary').nth(i).click();
    await page.locator('button[data-copy-target=sample-prompt-' + i + ']').click();
    await expect.poll(() => page.evaluate(() => navigator.clipboard.readText())).toContain(sample.prompt.en);
  }
  await page.screenshot({ path: `dist/verification/${test.info().project.name}-anima-detail.png` });
  await page.locator('.lang-switch').click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  await expect(page.locator('#prompt-text')).toHaveValue(api.prompt.en);
  expect((await request.get('/v1/styles/' + id + '?model=gpt-image')).status()).toBe(404);
  await page.goto('/');
  await expect(page.locator('body')).toHaveAttribute('data-active-model', 'anima-turbo');
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-card')).toHaveCount(visibleCount);
  expect(errors).toEqual([]);
});

test('Anima-only other category keeps its labels and drops unsupported GPT filters', async ({ page, request }) => {
  const tree = await (await request.get('/v1/tree?model=anima-turbo&lang=ja')).json();
  const others = tree.nodes.filter(node => node.category === 'other');
  expect(others.length).toBeGreaterThan(0);
  const response = await page.goto('/n/other?lang=ja&model=anima-turbo');
  expect(response.status()).toBe(200);
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-intro h1')).toHaveText('その他・成人向け参考');
  await expect(page.locator('.gallery-card')).toHaveCount(others.length);
  await page.locator('.gallery-card').first().click();
  await expect(page.locator('.category-notice')).toContainText('着衣・非露骨');
  await page.goto('/n/other?lang=ja&model=anima-turbo');
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await page.locator('.lang-switch').click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-intro h1')).toHaveText('Other / adult-manga references');
  await page.screenshot({ path: `dist/verification/${test.info().project.name}-anima-other.png` });
  await page.locator('.model-tab', { hasText: 'GPT Image' }).click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  expect(new URL(page.url()).searchParams.has('root')).toBe(false);
  expect((await request.get('/n/other?model=gpt-image')).status()).toBe(404);
});

test('category routes, facet filters, pagination, Genko mode and denied routes', async ({ page, request }) => {
  await page.goto('/n/shonen?lang=ja&model=gpt-image');
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-intro h1')).toHaveText('少年漫画');
  const filters = page.locator('.filter-panel');
  await filters.evaluate(el => { el.open = true; });
  await page.locator('.gallery-filters select[name=expression]').selectOption('mono');
  await page.locator('.gallery-filters button[type=submit]').click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  await expect(page.locator('.gallery-filters select[name=root]')).toHaveValue('shonen');
  const next = page.locator('.pagination a').last();
  await next.click();
  await expect(page.locator('body')).toHaveAttribute('data-gallery-ready', 'true');
  expect(new URL(page.url()).searchParams.get('page')).toBe('2');
  await page.goto('/n/' + NID + '?lang=en&model=gpt-image&client=genko');
  await expect(page.locator('.url-field')).toHaveCount(0);
  const genkoSwitch = new URL(await page.locator('.lang-switch').getAttribute('href'), page.url());
  expect(genkoSwitch.searchParams.get('model')).toBe('gpt-image');
  expect(genkoSwitch.searchParams.get('client')).toBe('genko');
  await expect(page.locator('a[href="genko://use-style?id=' + NID + '"]')).toHaveCount(1);
  for (const path of ['/admin', '/internal/queue', '/state.json', '/_data/routes.json', '/files/missing.jpg']) {
    expect((await request.get(path)).status()).toBe(404);
  }
  expect((await request.get('/search?expression=invalid')).status()).toBe(400);
});
