"""Submitted negative text is public; native generation metadata stays private."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

import test_anima as fixtures
ROOT = fixtures.ROOT


class AnimaNegativeTests(unittest.TestCase):
    def render_negative_page(self, values, lang='ja'):
        from jinja2 import Environment, FileSystemLoader, select_autoescape
        env = Environment(loader=FileSystemLoader(ROOT / 'costlab-auth/manga/app/templates'),
                          autoescape=select_autoescape(['html']))
        samples = [dict(role=role, width=64, height=64,
                        prompt={'en': 'Fixture positive prompt.'},
                        requested_settings={'negative_prompt': value})
                   for role, value in zip(('mixed-gender', 'showcase'), values)]
        return env.get_template('anima_style.html').render(
            lang=lang, ui={}, newui={}, title='Fixture', summary='Fixture summary',
            active_model='anima-turbo', entry=dict(id='anima-fixture',
                model_version='anima-turbo-v1.1', references=[]),
            sample_views=[dict(sample=sample, url='/fixture.png') for sample in samples],
            style_text='Fixture style.', copy_prefix='Fixture prefix')

    def test_shared_negative_is_shown_once_outside_sample_cards(self):
        import html
        import re
        negative = '\r\n hatching\r<gloss> & fabric\n '
        for lang in ('ja', 'en'):
            with self.subTest(lang=lang):
                rendered = self.render_negative_page([negative, negative], lang)
                fields = re.findall(r'<textarea[^>]*id="negative-prompt-text"[^>]*>(.*?)</textarea>', rendered, re.S)
                self.assertEqual(len(fields), 1, 'One shared negative field per style')
                self.assertEqual(rendered.count('data-copy-target="negative-prompt-text"'), 1)
                self.assertNotIn('sample-negative-prompt-', rendered)
                self.assertNotIn('negative-heading-', rendered)
                self.assertTrue(all('negative-prompt-text' not in card for card in
                    re.findall(r'<article class="anima-example".*?</article>', rendered, re.S)))
                raw = re.search(r'id="negative-prompt-text"[^>]*data-copy-value="([^"]*)"', rendered)
                self.assertEqual(json.loads(html.unescape(raw.group(1))), negative)
                self.assertNotIn('<gloss>', rendered)

    def test_different_sample_negatives_are_not_presented_as_a_shared_value(self):
        for values in ([None, 'hatching'], ['', None], ['hatching', 'gloss']):
            for lang in ('ja', 'en'):
                with self.subTest(values=values, lang=lang):
                    rendered = self.render_negative_page(values, lang)
                    self.assertIn('id="negative-not-shared"', rendered)
                    self.assertNotIn('id="negative-prompt-text"', rendered)
                    self.assertNotIn('data-copy-target="negative-prompt-text"', rendered)
                    self.assertNotIn('id="negative-not-specified"', rendered)
                    self.assertNotIn('sample-negative-prompt-', rendered)

    def test_shared_unspecified_and_empty_have_one_field_and_no_copy(self):
        for value, note_id in ((None, 'negative-not-specified'), ('', 'negative-empty')):
            for lang in ('ja', 'en'):
                with self.subTest(value=value, lang=lang):
                    rendered = self.render_negative_page([value, value], lang)
                    self.assertEqual(rendered.count('id="negative-prompt-text"'), 1)
                    self.assertEqual(rendered.count('id="' + note_id + '"'), 1)
                    self.assertNotIn('data-copy-target="negative-prompt-text"', rendered)

    def test_reader_preserves_omitted_null_empty_and_utf8_boundary(self):
        import copy
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, original, _ = fixtures.AnimaCatalogTests().paired_fixture(root)
            for value in (None, '', 'x' * 4096, 'あ' * 1365 + 'x'):
                registry = copy.deepcopy(original)
                registry['entries'][0]['samples'][0]['requested_settings']['negative_prompt'] = value
                path.write_text(json.dumps(registry), encoding='utf-8')
                row = fixtures.AnimaCatalogTests().module().load_catalog(path, root)[0]
                self.assertEqual(row['samples'][0]['requested_settings']['negative_prompt'], value)
            original['entries'][0]['samples'][0]['requested_settings'].pop('negative_prompt')
            path.write_text(json.dumps(original), encoding='utf-8')
            row = fixtures.AnimaCatalogTests().module().load_catalog(path, root)[0]
            self.assertNotIn('negative_prompt', row['samples'][0]['requested_settings'])

    def test_reader_rejects_non_text_or_oversized_negative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, registry, _ = fixtures.AnimaCatalogTests().paired_fixture(root)
            for invalid in (7, True, [], {'en': 'hatching'}, 'あ' * 1366):
                with self.subTest(negative_type=type(invalid).__name__):
                    registry['entries'][0]['samples'][0]['requested_settings']['negative_prompt'] = invalid
                    path.write_text(json.dumps(registry), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'negative prompt'):
                        fixtures.AnimaCatalogTests().module().load_catalog(path, root)

    def test_export_retains_exact_submitted_negative_per_sample(self):
        sys.path.insert(0, str(ROOT / 'costlab-auth/manga'))
        from app.store import Store
        spec = importlib.util.spec_from_file_location('export_cloudflare', ROOT / 'tools/manga_catalog/export_cloudflare.py')
        exporter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(exporter)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, registry, _ = fixtures.AnimaCatalogTests().paired_fixture(root)
            negative = '\r\n detailed irises, crosshatching\r<gloss> & textured cloth\n '
            registry['entries'][0]['samples'][1]['requested_settings']['negative_prompt'] = negative
            path.write_text(json.dumps(registry), encoding='utf-8')
            store = Store(root / 'store', seed_dir=root / 'none', compare_dir=root / 'none')
            keep = store.chain('shonen-battle-chibi-comic')
            for nid in store.order:
                store.state['nodes'][nid]['published'] = nid in keep
            output = root / 'assets'
            exporter.export_store(store, output, anima_catalog=path, archive_dir=root)
            payloads = json.loads((output / '_data/styles/anima-turbo/anima-example.json').read_text(encoding='utf-8'))
            for lang in ('ja', 'en'):
                samples = payloads[lang]['samples']
                self.assertIsNone(samples[0]['negative_prompt'])
                self.assertEqual(samples[1]['negative_prompt'], {'en': negative})
                self.assertEqual(set(samples[1]), {'subject', 'url', 'prompt', 'negative_prompt'})
                pages = json.loads((output / '_data/pages/anima-example.json').read_text(encoding='utf-8'))
                rendered = pages[lang]['anima-turbo']['en']
                self.assertEqual(rendered.count('id="negative-heading"'), 1)
                self.assertIn('id="negative-not-shared"', rendered)
                self.assertNotIn('id="negative-prompt-text"', rendered)
                self.assertNotIn('sample-negative-prompt-', rendered)
                self.assertNotIn('<gloss>', rendered)


if __name__ == '__main__':
    unittest.main()
