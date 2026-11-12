"""Anima-specific public assets keep exact prompts and never reuse GPT records."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/manga_catalog'))
MODULE=ROOT/'tools/manga_catalog/anima_catalog.py'

class AnimaCatalogTests(unittest.TestCase):
    def module(self):
        self.assertTrue(MODULE.is_file(),'Anima catalog reader/exporter is missing')
        spec=importlib.util.spec_from_file_location('anima_catalog',MODULE)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def fixture(self,root):
        a=io.BytesIO();Image.new('RGB',(64,64),'white').save(a,'PNG');raw=a.getvalue()
        b=io.BytesIO();Image.new('RGB',(384,512),'white').save(b,'JPEG');thumb=b.getvalue()
        sha=lambda v:hashlib.sha256(v).hexdigest()
        sid='anima-example';name=sha(raw)+'.png';tn=sha(thumb)+'.jpg'
        archive=root/'test-anima.zip'
        with zipfile.ZipFile(archive,'w') as z:z.writestr(sid+'/'+name,raw);z.writestr(sid+'/'+tn,thumb)
        entry={'id':sid,'category':'shonen','title':{'ja':'太い線','en':'Bold ink'},'summary':{'ja':'実見の説明','en':'Observed ink lines'},'features':{'expression':['mono'],'line':['thick'],'proportion':['standard'],'finish':['solid']},'prompt':{'en':'bold ink contours'},'model_version':'anima-turbo-v1.1','sample':{'file':name,'sha256':sha(raw),'width':64,'height':64,'thumb':tn,'thumb_sha256':sha(thumb),'prompt':{'en':'One adult with bold ink contours.'},'native_job_id':'1'*32,'requested_settings':{'model':'anima-turbo-v1.1','steps':8,'cfg_scale':1.0,'sampler':'euler','seed':None,'negative_prompt':None,'references_used':[]},'reported_settings':{'model':'anima-turbo-v1.1','provider':'ps5-anima','steps':8,'sampler':'euler','mode':'text2img','native_job_id':'1'*32},'max_rgb_channel_delta':0},'references':[],'limitations':{'ja':'再現性未検証','en':'Repeatability not established'}}
        registry={'schema':1,'repository':'akiba-tokyo-jp/manga-style','bundles':[{'tag':'test-anima','asset':archive.name,'sha256':sha(archive.read_bytes())}],'entries':[entry]}
        path=root/'catalog.json';path.write_text(json.dumps(registry),encoding='utf-8')
        return path,registry,raw

    def test_reads_verified_model_assets_and_exact_english_only_prompts(self):
        module=self.module()
        with tempfile.TemporaryDirectory() as tmp:
            path,registry,raw=self.fixture(Path(tmp))
            rows=module.load_catalog(path,Path(tmp))
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]['prompt'],{'en':'bold ink contours'})
            self.assertEqual(rows[0]['image_bytes'],raw)
            self.assertNotIn('ja',rows[0]['sample']['prompt'])

    def test_export_connects_gallery_detail_api_images_and_model_count(self):
        import inspect
        sys.path.insert(0,str(ROOT/'costlab-auth/manga'))
        from app import main
        from app.store import Store
        spec=importlib.util.spec_from_file_location('export_cloudflare',ROOT/'tools/manga_catalog/export_cloudflare.py')
        exporter=importlib.util.module_from_spec(spec);spec.loader.exec_module(exporter)
        self.assertIn('anima_catalog',inspect.signature(exporter.export_store).parameters,'Anima is not wired into the atomic public exporter')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path,registry,raw=self.fixture(root)
            store=Store(root/'store',seed_dir=root/'none',compare_dir=root/'none')
            keep=store.chain('shonen-battle-chibi-comic')
            for nid in store.order:store.state['nodes'][nid]['published']=nid in keep
            output=root/'assets'
            receipt=exporter.export_store(store,output,anima_catalog=path,archive_dir=root)
            self.assertEqual(receipt['anima_styles'],1)
            api=json.loads((output/'_data/styles/anima-turbo/anima-example.json').read_text())
            self.assertEqual(api['ja']['prompt'],{'en':'bold ink contours'})
            self.assertEqual(api['en']['samples'][0]['prompt'],{'en':'One adult with bold ink contours.'})
            self.assertEqual(api['ja']['model']['id'],'anima-turbo')
            self.assertFalse((output/'_data/styles/anima-example.json').exists())
            sample=registry['entries'][0]['sample']
            self.assertEqual((output/'files/anima-turbo/anima-example'/sample['file']).read_bytes(),raw)
            models=json.loads((output/'_data/models.json').read_text())['models']
            self.assertEqual(next(m for m in models if m['id']=='anima-turbo')['style_count'],1)
            self.assertEqual(next(m for m in models if m['id']=='gpt-image')['style_count'],len(keep))
            self.assertIn('anima-example',(output/'_data/gallery/ja-anima-turbo.html').read_text())
            index=json.loads((output/'_public/catalogue.json').read_text())
            anima_record=next(row for row in index['records'] if row.get('model')=='anima-turbo')
            self.assertTrue(anima_record['labels']['ja']['thumb_url'].startswith('/files/anima-turbo/'))
            self.assertNotIn('static.manga.invalid',anima_record['labels']['ja']['thumb_url'])
            pages=json.loads((output/'_data/pages/anima-example.json').read_text())
            self.assertIn('lang="en"',pages['ja']['anima-turbo']['en'])
            self.assertIn('One adult with bold ink contours.',pages['ja']['anima-turbo']['en'])
            old=json.loads((output/'_data/styles/shonen-battle-chibi-comic.json').read_text())
            self.assertNotEqual(old['ja']['model']['id'],'anima-turbo')
            self.assertEqual(main.MODELS['anima-turbo']['status'],'preparing')

    def test_other_category_requires_explicit_nonsexual_adult_sample_classification(self):
        module=self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path,registry,_=self.fixture(root)
            entry=registry['entries'][0]
            entry.update(category='other',reference_context='adult-manga',sample_content='non-explicit-fully-clothed-adult')
            path.write_text(json.dumps(registry),encoding='utf-8')
            self.assertEqual(module.load_catalog(path,root)[0]['category'],'other')
            for field,bad in [('reference_context',None),('sample_content','unspecified')]:
                value=json.loads(json.dumps(registry));value['entries'][0][field]=bad;path.write_text(json.dumps(value),encoding='utf-8')
                with self.assertRaises(ValueError):module.load_catalog(path,root)

    def test_other_export_is_anima_only_and_retains_nonexplicit_notice(self):
        sys.path.insert(0,str(ROOT/'costlab-auth/manga'))
        from app.store import Store
        spec=importlib.util.spec_from_file_location('export_cloudflare',ROOT/'tools/manga_catalog/export_cloudflare.py')
        exporter=importlib.util.module_from_spec(spec);spec.loader.exec_module(exporter)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path,registry,_=self.fixture(root)
            registry['entries'][0].update(category='other',reference_context='adult-manga',sample_content='non-explicit-fully-clothed-adult')
            path.write_text(json.dumps(registry),encoding='utf-8')
            store=Store(root/'store',seed_dir=root/'none',compare_dir=root/'none')
            keep=store.chain('shonen-battle-chibi-comic')
            for nid in store.order:store.state['nodes'][nid]['published']=nid in keep
            output=root/'assets';receipt=exporter.export_store(store,output,anima_catalog=path,archive_dir=root)
            self.assertEqual(receipt['anima_styles'],1)
            routes=json.loads((output/'_data/routes.json').read_text())
            self.assertNotIn('other',routes['roots'])
            self.assertNotIn('other',routes['model_roots']['gpt-image'])
            self.assertIn('other',routes['model_roots']['anima-turbo'])
            index=json.loads((output/'_public/catalogue.json').read_text())
            self.assertFalse(any(r['id']=='other' for r in index['records']))
            self.assertEqual(index['category_labels']['anima-turbo']['other']['ja'],'その他・成人向け参考')
            gallery=(output/'_data/gallery/ja-anima-turbo.html').read_text()
            self.assertIn('その他・成人向け参考',gallery)
            payload=json.loads((output/'_data/styles/anima-turbo/anima-example.json').read_text())['ja']
            self.assertEqual(payload['reference_context'],'adult-manga')
            self.assertEqual(payload['sample_content'],'non-explicit-fully-clothed-adult')
            pages=json.loads((output/'_data/pages/anima-example.json').read_text())
            self.assertIn('着衣・非露骨',pages['ja']['anima-turbo']['en'])

    def test_http_verifier_keeps_the_legacy_filter_oracle_model_scoped(self):
        sys.path.insert(0,str(ROOT/'costlab-auth/manga'))
        spec=importlib.util.spec_from_file_location('verify_public',ROOT/'cloudflare/tests/verify_public.py')
        verifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(verifier)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'_data/styles').mkdir(parents=True)
            records=[{'id':'gpt-example','level':1,'chain':['gpt-example'],'labels':{}},
                     {'id':'anima-example','model':'anima-turbo','level':3,'chain':['gpt-example','anima-example'],'labels':{}}]
            for record in records:(root/'_data/styles'/(record['id']+'.json')).write_text(json.dumps({'ja':{'prompt':{},'expression':'mono'}}))
            reader=verifier.PublicReader({'records':records},root)
            self.assertEqual(reader.order,['gpt-example'])

    def test_rejects_changed_images_model_mismatch_duplicate_ids_and_unsafe_names(self):
        module=self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path,original,_=self.fixture(root)
            for mutate in [lambda r:r['entries'][0]['sample'].__setitem__('sha256','0'*64),lambda r:r['entries'][0].__setitem__('model_version','gpt-image'),lambda r:r['entries'].append(r['entries'][0]),lambda r:r['entries'][0]['sample'].__setitem__('file','../../private.png'),lambda r:r['entries'][0]['prompt'].__setitem__('ja','not actually submitted'),lambda r:r['entries'][0]['references'].append({'title':'bad','url':'javascript:alert(1)'})]:
                value=json.loads(json.dumps(original));mutate(value);path.write_text(json.dumps(value),encoding='utf-8')
                with self.assertRaises(ValueError):module.load_catalog(path,root)
            path.write_text(json.dumps(original),encoding='utf-8')
            archive=root/'test-anima.zip';archive.write_bytes(archive.read_bytes()+b'changed')
            with self.assertRaises(ValueError):module.load_catalog(path,root)

if __name__=='__main__':unittest.main()
