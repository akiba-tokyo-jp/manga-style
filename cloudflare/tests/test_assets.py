import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENTRY = ROOT / 'tools/manga_catalog/cloudflare_assets.py'


class AssetTests(unittest.TestCase):
    def test_verified_local_cache_does_not_require_credentials_or_network(self):
        self.assertTrue(ENTRY.is_file(), 'portable private Release downloader is missing')
        spec = importlib.util.spec_from_file_location('cloudflare_assets', ENTRY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            raw = b'explicit unit-test fixture, not a release archive'
            (path / 'fixture.zip').write_bytes(raw)
            record = {'asset': 'fixture.zip', 'sha256': hashlib.sha256(raw).hexdigest(), 'release_tag': 'fixture'}
            module.fetch_archives(path, specs=[record], token='')
            self.assertEqual((path / 'fixture.zip').read_bytes(), raw)
            record['sha256'] = '0' * 64
            with self.assertRaises(ValueError):
                module.fetch_archives(path, specs=[record], token='')
            self.assertEqual((path / 'fixture.zip').read_bytes(), raw)
            with self.assertRaises(ValueError):
                module.fetch_archives(path, specs=[{**record, 'asset': '../escape.zip'}], token='')


if __name__ == '__main__':
    unittest.main()
