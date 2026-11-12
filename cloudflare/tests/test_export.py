"""Cloudflare public export uses the existing application's public reader."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'costlab-auth/manga'))
from app import main
from app.store import Store

EXPORT = ROOT / 'tools/manga_catalog/export_cloudflare.py'
NID = 'shonen-battle-chibi-comic'


class ExportTests(unittest.TestCase):
    def test_exports_exact_bilingual_public_api_without_private_state(self):
        self.assertTrue(EXPORT.is_file(), 'Cloudflare exporter is not implemented')
        spec = importlib.util.spec_from_file_location('export_cloudflare', EXPORT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = Store(root / 'data', seed_dir=root / 'none', compare_dir=root / 'none')
            store.state['api']['tokens'] = [{'hash': 'PRIVATE_TOKEN_CANARY'}]
            store.state['nodes'][NID]['pending_style'] = {'en': 'PRIVATE_PENDING_CANARY'}
            old = main._store
            try:
                main._store = store
                payload = module.public_api(store, NID)
                for lang in ('ja', 'en'):
                    request = module.request('/v1/styles/' + NID, lang=lang)
                    expected = json.loads(main.api_style(request, NID).body)
                    self.assertEqual(payload[lang], expected)
                serialized = json.dumps(payload)
                self.assertNotIn('PRIVATE_TOKEN_CANARY', serialized)
                self.assertNotIn('PRIVATE_PENDING_CANARY', serialized)
            finally:
                main._store = old

    def test_export_keeps_only_visible_reader_assets_byte_for_byte(self):
        self.assertTrue(EXPORT.is_file())
        spec = importlib.util.spec_from_file_location('export_cloudflare', EXPORT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(hasattr(module, 'export_store'), 'disk export is not implemented')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = Store(root / 'data', seed_dir=root / 'none', compare_dir=root / 'none')
            keep = store.chain(NID)
            for nid in store.order:
                store.state['nodes'][nid]['published'] = nid in keep
            import io
            from PIL import Image
            image = io.BytesIO()
            Image.new('L', (768, 1024), 100).save(image, 'JPEG')
            sample = store.put_sample(NID, image.getvalue())
            store.state['nodes'][NID]['pending_style'] = {'en': 'PRIVATE_PENDING_CANARY'}
            store.state['api']['tokens'] = [{'hash': 'PRIVATE_TOKEN_CANARY'}]
            (store.files_dir / 'unreferenced.txt').write_text('PRIVATE_BACKUP_CANARY')
            store._save()
            before = store.state_file.read_bytes()
            output = root / 'assets'
            receipt = module.export_store(store, output)
            self.assertEqual(receipt['visible_nodes'], len(keep))
            self.assertEqual(store.state_file.read_bytes(), before)
            data = json.loads((output / '_data/styles' / (NID + '.json')).read_text())
            self.assertEqual(data['ja']['version'], store.effective(NID)['version'])
            self.assertEqual(data['ja']['updated_at'], store.effective(NID)['updated_at'])
            for key in ('file', 'thumb'):
                self.assertEqual((output / 'files' / NID / sample[key]).read_bytes(),
                                 (store.files_dir / NID / sample[key]).read_bytes())
            self.assertEqual(len(list((output / '_data/styles').glob('*.json'))), len(keep))
            self.assertFalse((output / 'state.json').exists())
            before_output = (output / '_data/styles' / (NID + '.json')).read_bytes()
            with self.assertRaises(ValueError):
                module.export_store(store, output, max_files=1)
            self.assertEqual((output / '_data/styles' / (NID + '.json')).read_bytes(), before_output)
            store.state['api']['mode'] = 'token'
            with self.assertRaises(ValueError):
                module.export_store(store, output)
            store.state['api']['mode'] = 'public'
            with self.assertRaises(ValueError):
                module.export_store(store, store.data_dir / 'new-export')
            text = ''.join(p.read_text() for p in output.rglob('*') if p.suffix in ('.json', '.html', '.js', '.mjs'))
            for canary in ('PRIVATE_PENDING_CANARY', 'PRIVATE_TOKEN_CANARY', 'PRIVATE_BACKUP_CANARY'):
                self.assertNotIn(canary, text)
            html = json.loads((output / '_data/pages' / (NID + '.json')).read_text())
            self.assertIn('prompt-text', html['ja']['gpt-image']['en'])
            self.assertNotIn('prompt-text', html['ja']['anima-turbo']['ja'])
            self.assertIn('src="/static/gallery.mjs"', (output / '_data/gallery/ja-anima-turbo.html').read_text())


    def test_snapshot_loader_never_refreshes_or_rewrites_source_state(self):
        spec = importlib.util.spec_from_file_location('export_cloudflare', EXPORT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(hasattr(module, 'snapshot_store'), 'read-only snapshot import is not implemented')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = Store(root / 'snapshot', seed_dir=root / 'none', compare_dir=root / 'none')
            original.state['nodes'][NID]['version'] = 123
            original.state['nodes'][NID]['updated_at'] = '2026-11-01T12:00:00Z'
            original.state['nodes']['shonen']['published'] = False
            original._save()
            before = original.state_file.read_bytes()
            clone = module.snapshot_store(root / 'snapshot', root / 'scratch', compare_dir=root / 'none')
            self.assertEqual(clone.state, original.state)
            self.assertEqual(clone.effective(NID)['version'], 123)
            self.assertFalse(clone.visible(NID))
            self.assertEqual(original.state_file.read_bytes(), before)
            with self.assertRaises(ValueError):
                module.snapshot_store(root / 'snapshot', root / 'snapshot' / 'nested')
            original.state['api']['mode'] = 'token'
            original._save()
            with self.assertRaises(ValueError):
                module.snapshot_store(root / 'snapshot', root / 'private')

    def test_cli_refuses_original_snapshot_write_overlap_before_downloading(self):
        from unittest.mock import patch
        sys.path.insert(0, str(ROOT / 'tools/manga_catalog'))
        spec = importlib.util.spec_from_file_location('export_cloudflare', EXPORT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            snapshot = root / 'snapshot'
            snapshot.mkdir()
            (snapshot / 'sentinel').write_bytes(b'original snapshot must not change')
            report_snapshot = root / 'build-report.json'
            report_snapshot.mkdir()
            cases = [(snapshot, snapshot / 'export', root / 'archives'),
                     (snapshot, root / 'public/assets', snapshot / 'archives'),
                     (report_snapshot, root / 'assets', root / 'archives')]
            for source, output, archives in cases:
                argv = ['export_cloudflare.py', '--snapshot-dir', str(source), '--output', str(output), '--archive-dir', str(archives)]
                with self.subTest(source=source, output=output, archives=archives):
                    with patch.object(sys, 'argv', argv), patch('cloudflare_assets.fetch_archives', side_effect=AssertionError('download reached before snapshot guard')) as fetch:
                        with self.assertRaisesRegex(ValueError, 'snapshot'):
                            module.cli()
                        fetch.assert_not_called()
            self.assertEqual((snapshot / 'sentinel').read_bytes(), b'original snapshot must not change')
            self.assertEqual([p.name for p in snapshot.iterdir()], ['sentinel'])

    def test_cli_rejects_snapshot_abbreviations_and_empty_values_before_download(self):
        import io
        from contextlib import redirect_stderr
        from unittest.mock import patch
        sys.path.insert(0, str(ROOT / 'tools/manga_catalog'))
        spec = importlib.util.spec_from_file_location('export_cloudflare', EXPORT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            for args, env in [(['--snapshot-d', tmp], {}), (['--snapshot-dir', ''], {}), ([], {'MANGA_SNAPSHOT_DIR': ''})]:
                with self.subTest(args=args, env=env):
                    with patch.object(sys, 'argv', ['export_cloudflare.py', *args]), patch.dict(module.os.environ, env), patch('cloudflare_assets.fetch_archives', side_effect=AssertionError('download reached for invalid arguments')) as fetch, redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit) as error:
                            module.cli()
                        self.assertEqual(error.exception.code, 2)
                        fetch.assert_not_called()

if __name__ == '__main__':
    unittest.main()
