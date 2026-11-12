"""The extracted catalogue must restore its assets from its own private repo."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'costlab-auth/manga/tests'))
from test_pair_release import fixture

class RepositorySplitTests(unittest.TestCase):
    def test_verified_bundle_accepts_own_private_repository(self):
        spec=importlib.util.spec_from_file_location('split_prepare',ROOT/'tools/manga_catalog/prepare_explanatory.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); doc,files=fixture(); archive=root/'split-pair.zip'
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('manifest.json',json.dumps(doc))
                for name,raw in files.items():z.writestr(name,raw)
            digest=hashlib.sha256(archive.read_bytes()).hexdigest()
            registry=root/'registry.json'
            registry.write_text(json.dumps({'repository':'akiba-tokyo-jp/manga-style','bundles':[{'asset':archive.name,'sha256':digest,'nodes':[doc[0]['id']],'release_tag':'split-fixture'}]}))
            dest=root/'seed'
            module.prepare(root,registry_path=registry,dest=dest)
            self.assertEqual(json.loads((dest/digest/'manifest.json').read_text()),doc)
            invalid=json.loads(registry.read_text())
            invalid['repository']='untrusted/repository'
            registry.write_text(json.dumps(invalid))
            with self.assertRaises(ValueError):
                module.prepare(root,registry_path=registry,dest=dest)

    def test_split_regression_is_registered_in_routine_entrypoint(self):
        import ast
        tree=ast.parse((ROOT/'tools/manga_catalog/validate_explanatory.py').read_text())
        commands=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='COMMANDS' for t in n.targets))
        self.assertEqual(sum('test_split_repository.py' in cmd for cmd in commands),1)

if __name__=='__main__':unittest.main()
