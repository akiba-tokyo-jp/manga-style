import hashlib
import importlib.util
import io
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

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


    def load_downloader(self):
        spec = importlib.util.spec_from_file_location('cloudflare_assets', ENTRY)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_public_assets_and_legacy_archives_download_without_token_or_api(self):
        raw = b'explicit public-download test fixture'
        records = [
            {'release_tag': 'fixture'},
            {'release_bodies': ['fixture', 'fixture-part-2']},
        ]
        for release in records:
            with self.subTest(release=release), tempfile.TemporaryDirectory() as tmp:
                module = self.load_downloader()
                record = {**release, 'asset': 'fixture.zip', 'sha256': hashlib.sha256(raw).hexdigest()}
                opener = mock.Mock()
                opener.open.return_value = io.BytesIO(raw)
                with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener), \
                        mock.patch.dict(module.os.environ, {'GH_TOKEN': '', 'GITHUB_TOKEN': ''}), \
                        mock.patch('subprocess.run', side_effect=AssertionError('must not require gh login')):
                    module.fetch_archives(tmp, specs=[record])
                self.assertEqual((Path(tmp) / 'fixture.zip').read_bytes(), raw)
                request = opener.open.call_args.args[0]
                self.assertEqual(request.full_url,
                                 'https://github.com/akiba-tokyo-jp/manga-style/releases/download/fixture/fixture.zip')
                self.assertIsNone(request.get_header('Authorization'))
                self.assertEqual(opener.open.call_count, 1)

    def test_public_redirect_is_unauthenticated_and_rejects_foreign_storage(self):
        raw = b'explicit public redirect test fixture'
        record = {'asset': 'fixture.zip', 'sha256': hashlib.sha256(raw).hexdigest(), 'release_tag': 'fixture'}
        for host, accepted in [('release-assets.githubusercontent.com', True), ('evil.example', False)]:
            with self.subTest(host=host), tempfile.TemporaryDirectory() as tmp:
                module = self.load_downloader()
                redirect = urllib.error.HTTPError('https://github.com/', 302, 'Found',
                                                  {'Location': 'https://' + host + '/fixture'}, None)
                opener = mock.Mock()
                opener.open.side_effect = [redirect, io.BytesIO(raw)]
                with mock.patch.object(module.urllib.request, 'build_opener', return_value=opener):
                    if accepted:
                        module.fetch_archives(tmp, specs=[record], token='')
                        self.assertEqual((Path(tmp) / 'fixture.zip').read_bytes(), raw)
                        for call in opener.open.call_args_list:
                            self.assertIsNone(call.args[0].get_header('Authorization'))
                    else:
                        with self.assertRaisesRegex(ValueError, 'Unexpected Release storage redirect'):
                            module.fetch_archives(tmp, specs=[record], token='')
                        self.assertEqual(opener.open.call_count, 1)
                        self.assertFalse((Path(tmp) / 'fixture.zip').exists())

    def test_public_download_still_checks_pinned_sha_before_writing(self):
        module = self.load_downloader()
        record = {'asset': 'fixture.zip', 'sha256': '0' * 64, 'release_tag': 'fixture'}
        opener = mock.Mock()
        opener.open.return_value = io.BytesIO(b'explicit wrong archive test fixture')
        with tempfile.TemporaryDirectory() as tmp, \
                mock.patch.object(module.urllib.request, 'build_opener', return_value=opener):
            with self.assertRaisesRegex(ValueError, 'Downloaded archive SHA mismatch'):
                module.fetch_archives(tmp, specs=[record], token='')
            self.assertEqual(list(Path(tmp).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
