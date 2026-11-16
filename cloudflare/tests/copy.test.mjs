import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../../costlab-auth/manga/app/static/site.js', import.meta.url), 'utf8');
async function clickCopy({ raw, displayed = '', prefix = '', clipboardAvailable = true }) {
  let listener, written, fallbackCalls = 0;
  class Element { closest() { return this; } }
  class Input extends Element {}
  class Textarea extends Input {}
  const field = new Textarea();
  field.value = displayed;
  field.focus = () => {};
  field.select = () => {};
  field.setSelectionRange = () => {};
  field.dataset = raw === undefined ? {} : { copyValue: raw };
  const button = new Element();
  button.dataset = { copyTarget: 'negative', copyPrefix: prefix, copied: 'copied', failed: 'failed' };
  const status = { classList: { contains: () => true }, textContent: '' };
  button.nextElementSibling = status;
  const document = {
    querySelector: () => null, querySelectorAll: () => [],
    addEventListener: (_, handler) => { listener = handler; },
    getElementById: () => field,
    createElement: () => ({ setAttribute() {}, remove() {}, focus() {}, select() {}, setSelectionRange() {} }),
    body: { appendChild() {} },
    execCommand: () => { fallbackCalls++; return true; },
  };
  vm.runInNewContext(source, {
    document, window: {}, Element, HTMLElement: Element, HTMLInputElement: Input, HTMLTextAreaElement: Textarea,
    navigator: clipboardAvailable ? { clipboard: { writeText: async text => { written = text; } } } : {},
    setTimeout: () => 1, clearTimeout() {}, WeakMap,
  });
  await listener({ target: button });
  return { written, fallbackCalls };
}

test('Anima copy hands the raw mixed line endings to the clipboard API, not textarea normalization', async () => {
  const raw = '\r\n exact negative\rsecond\n';
  const result = await clickCopy({ raw: JSON.stringify(raw), displayed: '\n exact negative\nsecond\n' });
  assert.equal(result.written, raw);
});

test('legacy prompt copying still uses its original text and prefix', async () => {
  const result = await clickCopy({ displayed: 'legacy prompt', prefix: 'style path' });
  assert.equal(result.written, 'style path\nlegacy prompt');
});

test('raw negatives with CR fail closed when the clipboard API is unavailable', async () => {
  const result = await clickCopy({ raw: JSON.stringify('first\rsecond'), displayed: 'first\nsecond', clipboardAvailable: false });
  assert.equal(result.written, undefined);
  assert.equal(result.fallbackCalls, 0);
});

test('invalid or nonstring raw copy data is not copied', async () => {
  for (const raw of ['broken JSON', 'null', '7']) {
    const result = await clickCopy({ raw, displayed: 'must not silently copy this' });
    assert.equal(result.written, undefined);
    assert.equal(result.fallbackCalls, 0);
  }
});
