/*
 * Copy buttons, e.g.
 *   <button type="button" data-copy-target="api-url" data-copy-prefix="..." data-copied="..." data-failed="...">
 * copy the value (or text) of the element with that id, then show the copied /
 * failed message for about 2 seconds in the live region right after the button.
 * With data-copy-prefix, that line (the category path and the id of the style) comes first,
 * so that a copied prompt or URL never travels with the style name alone.
 */
(() => {
  'use strict';


  // Model-scoped links are server rendered; JS never swaps a prompt without its picture.
  const filterPanel = document.querySelector('.filter-panel');
  if (filterPanel && window.matchMedia('(max-width: 760px)').matches) {
    filterPanel.removeAttribute('open');
  }
  document.querySelectorAll('.gallery-filters select[name="root"]').forEach((field) => {
    field.addEventListener('change', () => {
      const topic = field.form.querySelector('select[name="topic"]');
      if (topic) topic.value = '';
    });
  });

  const MESSAGE_MS = 2000;
  const timers = new WeakMap();

  const isField = (el) => el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement;

  const textOf = (el) => (isField(el) ? el.value : el.textContent);

  // Older way: select the text and copy the selection. If that fails too,
  // the text is left selected so it can be copied by hand.
  const copyBySelection = (el) => {
    const previous = document.activeElement;
    let copied = false;
    try {
      if (isField(el)) {
        el.focus({ preventScroll: true });
        el.select();
        el.setSelectionRange(0, el.value.length);
      } else {
        const range = document.createRange();
        range.selectNodeContents(el);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
      }
      copied = document.execCommand('copy');
    } catch (err) {
      copied = false;
    }
    if (copied && previous instanceof HTMLElement && previous !== el) {
      previous.focus({ preventScroll: true });
    }
    return copied;
  };

  // The older way for a text that is not on the page as it is (prefix + value):
  // put it in a hidden field for a moment, copy, and remove the field again.
  const copyText = (text) => {
    const field = document.createElement('textarea');
    field.value = text;
    field.setAttribute('readonly', '');
    field.className = 'copy-scratch';
    document.body.appendChild(field);
    const copied = copyBySelection(field);
    field.remove();
    return copied;
  };

  const copy = async (el, prefix) => {
    const text = prefix ? `${prefix}\n${textOf(el)}` : textOf(el);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch (err) {
        // Not allowed here (permission, insecure page, old WebView): try the older way.
      }
    }
    if (prefix && copyText(text)) {
      return true;
    }
    return copyBySelection(el);
  };

  // The live region next to the button; added if the page has none.
  const statusFor = (button) => {
    const next = button.nextElementSibling;
    if (next && next.classList.contains('copy-status')) {
      return next;
    }
    const status = document.createElement('span');
    status.className = 'copy-status';
    status.setAttribute('aria-live', 'polite');
    button.insertAdjacentElement('afterend', status);
    return status;
  };

  const show = (status, message) => {
    clearTimeout(timers.get(status));
    // Empty it first so that the same message is announced again on a second click.
    status.textContent = '';
    timers.set(status, setTimeout(() => {
      status.textContent = message;
      timers.set(status, setTimeout(() => {
        status.textContent = '';
      }, MESSAGE_MS));
    }, 50));
  };

  document.addEventListener('click', async (event) => {
    const button = event.target instanceof Element
      ? event.target.closest('button[data-copy-target]')
      : null;
    if (!button) {
      return;
    }
    const status = statusFor(button);
    const target = document.getElementById(button.dataset.copyTarget || '');
    const copied = target ? await copy(target, button.dataset.copyPrefix || '') : false;
    show(status, (copied ? button.dataset.copied : button.dataset.failed) || '');
  });
})();
