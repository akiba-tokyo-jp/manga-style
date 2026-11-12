"""固定SHA配布から通常起動までの2枚組取込み。全入力は使い捨て。"""
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
from app.store import Store, _digest
from PIL import Image

NID = 'shojo-penonly'


def fixture():
    style = {'ja': '細い線だけ。', 'en': 'Fine lines only.', 'tags': 'fine lines'}
    files = {}
    samples = []
    for role, gray in [('representative', 90), ('application', 200)]:
        out = io.BytesIO()
        Image.new('L', (512, 768), gray).save(out, 'JPEG')
        name = NID+'-'+role+'.jpg'
        files[name] = out.getvalue()
        samples.append({'subject': role, 'file': name, 'sha256': hashlib.sha256(files[name]).hexdigest(),
                        'bytes': len(files[name]), 'prompt': {'ja': style['ja']+' 成人。', 'en': style['en']+' An adult.'},
                        'model_version': 'gpt-image-2.6-sunburst', 'created_at': '2026-11-07T04:00:00Z'})
    return [{'id': NID, 'complete_style': style, 'style_prompt_sha256': _digest(style), 'samples': samples}], files


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='manga-pair-release-')
        self.root = Path(self.tmp.name)
        self.seed = self.root/'seed'
        self.pairs = self.seed/'pairs'
        self.pairs.mkdir(parents=True)
        self.doc, self.files = fixture()

    def tearDown(self):
        self.tmp.cleanup()

    def stage(self):
        (self.pairs/'manifest.json').write_text(json.dumps(self.doc, ensure_ascii=False))
        for name, raw in self.files.items():
            (self.pairs/name).write_bytes(raw)

    def store(self):
        return Store(self.root/'data', seed_dir=self.seed, compare_dir=self.root/'no-compare')

    def test_normal_startup_imports_pair_once_and_preserves_later_pending_edit(self):
        s = self.store()
        old = s.put_sample(NID, next(iter(self.files.values())))
        old_node = copy.deepcopy(s.state['nodes'][NID])
        self.stage()
        s = self.store()
        backups = list((s.data_dir/'pair-history').glob(NID+'-*.json'))
        self.assertTrue(any(json.loads(p.read_text()) == old_node for p in backups))
        self.assertEqual(len(s.samples(NID)), 2)
        self.assertEqual(s.style_prompt(NID), self.doc[0]['complete_style'])
        self.assertTrue((s.files_dir/NID/old['file']).exists())
        version = s.state['nodes'][NID]['version']
        s.edit(NID, {'words_tags': 'pending later change'})
        restarted = self.store()
        self.assertEqual(restarted.requested_style(NID)['tags'], 'pending later change')
        self.assertIsNotNone(restarted.state['nodes'][NID]['regen'])
        self.assertEqual(restarted.state['nodes'][NID]['version'], version)

    def test_invalid_second_image_keeps_old_state_on_disk(self):
        s = self.store()
        s.put_sample(NID, next(iter(self.files.values())))
        before = s.state_file.read_bytes()
        name = self.doc[0]['samples'][1]['file']
        self.files[name] = b'broken'
        self.stage()
        with self.assertRaises(ValueError):
            self.store()
        self.assertEqual(s.state_file.read_bytes(), before)

    def test_prepare_shards_then_normal_store_imports_both_branches(self):
        spec = importlib.util.spec_from_file_location('pair_prepare_shards', ROOT/'tools/manga_catalog/prepare_explanatory.py')
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        records = []
        for i, nid in enumerate((NID, 'shonen-battle-chibi-comic')):
            doc, files = fixture()
            doc[0]['id'] = nid
            renamed = {}
            for sample in doc[0]['samples']:
                old = sample['file']
                sample['file'] = nid+'-'+sample['subject']+'.jpg'
                renamed[sample['file']] = files[old]
            archive = self.root/f'part-{i}.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('manifest.json', json.dumps(doc))
                for name, raw in renamed.items():
                    z.writestr(name, raw)
            records.append({'asset':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'nodes':[nid],'release_bodies':[]})
        registry = self.root/'registry.json'
        registry.write_text(json.dumps({'repository':'akiba-tokyo-jp/manga-style','bundles':records}))
        module.prepare(self.root, registry_path=registry, dest=self.pairs)
        self.assertEqual(len(list(self.pairs.glob('*/manifest.json'))), 2)
        s = self.store()
        for nid in (NID, 'shonen-battle-chibi-comic'):
            self.assertEqual(len(s.samples(nid)), 2)
        before = {str(p.relative_to(self.pairs)):p.read_bytes() for p in self.pairs.rglob('*') if p.is_file()}
        records[1]['sha256'] = '0'*64
        registry.write_text(json.dumps({'repository':'akiba-tokyo-jp/manga-style','bundles':records}))
        with self.assertRaises(ValueError):
            module.prepare(self.root, registry_path=registry, dest=self.pairs)
        self.assertEqual(before, {str(p.relative_to(self.pairs)):p.read_bytes() for p in self.pairs.rglob('*') if p.is_file()})

    def test_release_asset_download_is_verified_before_staging(self):
        import shutil
        import subprocess
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('pair_prepare_assets', ROOT/'tools/manga_catalog/prepare_explanatory.py')
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        archive = self.root/'asset.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('manifest.json', json.dumps(self.doc))
            for name, raw in self.files.items():
                z.writestr(name, raw)
        record = {'asset':archive.name,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
                  'nodes':[NID],'release_tag':'manga-assets-test'}
        registry = self.root/'asset-registry.json'
        def save_registry():
            registry.write_text(json.dumps({'repository':'akiba-tokyo-jp/manga-style','bundles':[record]}))
        save_registry()
        calls = []
        def download(command, **kwargs):
            calls.append(command)
            self.assertEqual(command[:4], ['gh','release','download','manga-assets-test'])
            self.assertEqual(command[command.index('--pattern')+1], 'asset.zip')
            self.assertEqual(command[command.index('--repo')+1], 'akiba-tokyo-jp/manga-style')
            dest = Path(command[command.index('--dir')+1])
            shutil.copyfile(archive, dest/'asset.zip')
            return subprocess.CompletedProcess(command, 0, '', '')
        with patch.object(module.subprocess, 'run', side_effect=download):
            module.prepare(registry_path=registry, dest=self.pairs)
        self.assertEqual(len(calls), 1)
        self.assertEqual(len(self.store().samples(NID)), 2)
        record['release_tag'] = '../outside'
        save_registry()
        with patch.object(module.subprocess, 'run') as network:
            with self.assertRaises(ValueError):
                module.prepare(registry_path=registry, dest=self.pairs)
            network.assert_not_called()
        record['release_tag'] = 'manga-assets-test'
        record['sha256'] = '0'*64
        save_registry()
        before = {str(p):p.read_bytes() for p in self.pairs.rglob('*') if p.is_file()}
        with patch.object(module.subprocess, 'run', side_effect=download):
            with self.assertRaises(ValueError):
                module.prepare(registry_path=registry, dest=self.pairs)
        self.assertEqual(before, {str(p):p.read_bytes() for p in self.pairs.rglob('*') if p.is_file()})

    def test_release_checks_are_registered_in_routine_entrypoints(self):
        import ast
        driver = ast.parse((ROOT/'tools/manga_catalog/validate_explanatory.py').read_text())
        commands = next(ast.literal_eval(n.value) for n in driver.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=='COMMANDS' for t in n.targets))
        self.assertEqual(sum('test_pair_release.py' in cmd for cmd in commands), 1)
        prepare = ast.parse((ROOT/'tools/manga_catalog/prepare_samples.py').read_text())
        self.assertTrue(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='prepare_explanatory' and n.func.attr=='prepare' for n in ast.walk(prepare)))

    def test_archive_validation_rejects_tampering_duplicates_and_traversal(self):
        spec = importlib.util.spec_from_file_location('pair_prepare_test', ROOT/'tools/manga_catalog/prepare_explanatory.py')
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        path = self.root/'pairs.zip'
        def archive(doc, files):
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('manifest.json', json.dumps(doc, ensure_ascii=False))
                for name, raw in files.items():
                    z.writestr(name, raw)
            return {'asset': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'nodes': [NID], 'release_bodies': []}
        record = archive(self.doc, self.files)
        self.assertEqual(module.read_bundle(path, record, {NID})[0], self.doc)
        record['sha256'] = '0'*64
        with self.assertRaises(ValueError):
            module.read_bundle(path, record, {NID})
        cases = []
        bad = copy.deepcopy(self.doc); bad[0]['samples'][1]['sha256'] = '0'*64; cases.append(bad)
        bad = copy.deepcopy(self.doc); bad[0]['samples'][1]['file'] = '../outside.jpg'; cases.append(bad)
        bad = copy.deepcopy(self.doc); bad[0]['samples'][1]['subject'] = 'representative'; cases.append(bad)
        bad = copy.deepcopy(self.doc); bad[0]['style_prompt_sha256'] = '0'*64; cases.append(bad)
        bad = copy.deepcopy(self.doc); bad[0]['samples'][1]['prompt']['en'] = 'Unrelated scene'; cases.append(bad)
        for bad in cases:
            with self.subTest(doc=bad):
                record = archive(bad, self.files)
                with self.assertRaises(ValueError):
                    module.read_bundle(path, record, {NID})


if __name__ == '__main__':
    unittest.main()
