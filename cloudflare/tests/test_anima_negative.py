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
                import html
                import re
                pages = json.loads((output / '_data/pages/anima-example.json').read_text(encoding='utf-8'))
                rendered = pages[lang]['anima-turbo']['en']
                field = re.search(r'<textarea[^>]*id="sample-negative-prompt-1"[^>]*>(.*?)</textarea>', rendered, re.S)
                self.assertIsNotNone(field, 'Each sample needs its actual negative field')
                display = html.unescape(field.group(1)).replace('\r\n', '\n').replace('\r', '\n').removeprefix('\n')
                self.assertEqual(display, negative.replace('\r\n', '\n').replace('\r', '\n'))
                copy_value = re.search(r'id="sample-negative-prompt-1"[^>]*data-copy-value="([^"]*)"', rendered)
                self.assertIsNotNone(copy_value, 'Raw copy text must survive HTML newline normalization')
                self.assertEqual(json.loads(html.unescape(copy_value.group(1))), negative)
                self.assertIn('data-copy-target="sample-negative-prompt-1"', rendered)
                self.assertIn('negative-not-specified-0', rendered)
                self.assertNotIn('<gloss>', rendered)


if __name__ == '__main__':
    unittest.main()
