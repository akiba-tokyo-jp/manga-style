"""2枚組の読取と互換性。保存済みの新形式を旧readerが落とす回帰。"""
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from fastapi.testclient import TestClient
from PIL import Image
from app import main
from app.store import Store, InputError

NID = 'shonen-battle-chibi-comic'
ORIGIN = 'https://manga.akiba.tokyo.jp'

def image_bytes(size=(1024, 768), value=210):
    out = io.BytesIO()
    Image.new('L', size, value).save(out, 'PNG')
    return out.getvalue()

class PairTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='manga-pairs-')
        self.root = Path(self.temp.name)
        self.s = Store(self.root / 'data', seed_dir=self.root/'no-seed', compare_dir=self.root/'no-compare')
        self.old = main._store
        main._store = self.s
        self.client = TestClient(main.app, base_url=ORIGIN)

    def tearDown(self):
        main._store = self.old
        self.temp.cleanup()

    def seed_pair_state(self):
        # A legacy primary plus the new second slot, as persisted on disk.
        first = self.s.put_sample(NID, image_bytes())
        second = copy.deepcopy(first)
        second.update(subject='application', file='application-test.jpg', thumb='application-test-thumb.jpg', width=1024, height=768)
        folder = self.s.files_dir / NID
        for key in ('file', 'thumb'):
            (folder/second[key]).write_bytes((folder/first[key]).read_bytes())
        self.s.state['nodes'][NID]['additional_samples'] = [second]
        self.s._save()
        return first, second

    def test_detail_page_shows_two_labeled_images_and_prompts(self):
        first, second = self.seed_pair_state()
        for lang, labels in [('ja', ('代表の絵', '別の場面')), ('en', ('Representative', 'Another scene'))]:
            html = self.client.get('/n/'+NID+'?lang='+lang).text
            self.assertIn(second['file'], html)
            for label in labels:
                self.assertIn(label, html)
            self.assertIn('sample-pair', html)

    def pair_items(self):
        style = self.s.style_prompt(NID)
        return [{'subject': role, 'raw': image_bytes(value=v),
                 'prompt': {lang: style[lang] + ' ' + scene for lang, scene in [('ja', '人物が立つ。'), ('en', 'A person standing.')]},
                 'model_version': 'gpt-image-2.6-sunburst', 'created_at': '2026-11-07T04:00:00Z'}
                for role, v in [('representative', 100), ('application', 210)]]

    def test_atomic_pair_preserves_aspect_and_is_idempotent(self):
        from app.store import _digest
        items = self.pair_items()
        before = copy.deepcopy(self.s.state)
        self.s.put_sample_pair(NID, items, _digest(self.s.style_prompt(NID)))
        samples = self.s.samples(NID)
        self.assertEqual(len(samples), 2)
        self.assertEqual([x['subject'] for x in samples], ['representative', 'application'])
        for item in samples:
            with Image.open(self.s.files_dir/NID/item['file']) as im:
                self.assertEqual(im.size, (1024, 768))
            with Image.open(self.s.files_dir/NID/item['thumb']) as im:
                self.assertEqual(im.size, (384, 512))
        installed = copy.deepcopy(self.s.state)
        self.s.put_sample_pair(NID, items, _digest(self.s.style_prompt(NID)))
        self.assertEqual(self.s.state, installed)
        for nid in before['nodes']:
            if nid != NID:
                self.assertEqual(before['nodes'][nid], installed['nodes'][nid])
        reloaded = Store(self.root/'data', seed_dir=self.root/'none', compare_dir=self.root/'none')
        self.assertEqual(reloaded.samples(NID), samples)

    def test_invalid_second_picture_or_style_leaves_original_unchanged(self):
        from app.store import _digest
        self.s.put_sample(NID, image_bytes())
        before = copy.deepcopy(self.s.state)
        items = self.pair_items()
        items[1]['raw'] = b'broken'
        with self.assertRaises(InputError):
            self.s.put_sample_pair(NID, items, _digest(self.s.style_prompt(NID)))
        self.assertEqual(self.s.state, before)
        with self.assertRaises(InputError):
            self.s.put_sample_pair(NID, self.pair_items(), '0'*64)
        self.assertEqual(self.s.state, before)

    def test_complete_style_and_both_pictures_change_in_one_commit(self):
        from app.store import _digest
        old_style = self.s.style_prompt(NID)
        style = {'ja':'白い紙に丸い顔と小さい体を線だけで描く。',
                 'en':'Round faces and small bodies in lines on white paper.', 'tags':'monochrome, chibi, lines'}
        items = self.pair_items()
        for item in items:
            item['prompt'] = {lang:style[lang]+' '+('男性と女性。' if lang=='ja' else 'A man and a woman.') for lang in ('ja','en')}
        self.s.put_sample_pair(NID,items,_digest(style),complete_style=style)
        self.assertEqual(self.client.get('/v1/styles/'+NID).json()['prompt'],style)
        self.assertNotEqual(self.s.style_prompt(NID),old_style)
        published = self.client.get('/v1/styles/'+NID).json()
        self.s.edit(NID, {'words_en':'A different complete line style.'})
        after = self.client.get('/v1/styles/'+NID).json()
        self.assertEqual(after['prompt'], published['prompt'])
        self.assertEqual(after['samples'], published['samples'])
        self.assertEqual(after['version'], published['version'])
        self.assertIsNotNone(self.s.state['nodes'][NID]['regen'])
        self.assertTrue(self.s.generation_prompt(NID)['en'].startswith('A different complete line style.'))
        queued = next(q for q in self.s.queue() if q['id'] == NID)
        self.assertEqual([x['subject'] for x in queued['sample_prompts']], ['representative','application'])
        self.assertTrue(all(x['prompt']['en'].startswith('A different complete line style.') for x in queued['sample_prompts']))

    def test_complete_style_refuses_single_image_update(self):
        from app.store import _digest
        style = {'ja':'白黒の絵。', 'en':'Black ink.', 'tags':'monochrome'}
        items = self.pair_items()
        for item in items:
            item['prompt']={lang:style[lang]+' scene' for lang in ('ja','en')}
        self.s.put_sample_pair(NID,items,_digest(style),complete_style=style)
        with self.assertRaisesRegex(InputError,'2枚'):
            self.s.put_sample(NID,image_bytes(value=70))

    def test_changed_style_cannot_keep_either_old_picture(self):
        from app.store import _digest
        items = self.pair_items()
        self.s.put_sample_pair(NID, items, _digest(self.s.style_prompt(NID)))
        before = copy.deepcopy(self.s.state)
        newstyle = {'ja':'別の線画。', 'en':'Different lines.', 'tags':'lines'}
        changed = copy.deepcopy(items)
        for item in changed:
            item['prompt'] = {lang:newstyle[lang]+' scene' for lang in ('ja','en')}
        with self.assertRaisesRegex(InputError, '2枚とも'):
            self.s.put_sample_pair(NID, changed, _digest(newstyle), complete_style=newstyle)
        self.assertEqual(self.s.state, before)

    def test_old_pixels_cannot_be_relabelled_with_changed_scene_prompt(self):
        from app.store import _digest
        items = self.pair_items()
        sha = _digest(self.s.style_prompt(NID))
        self.s.put_sample_pair(NID, items, sha)
        before = copy.deepcopy(self.s.state)
        changed = copy.deepcopy(items)
        changed[1]['prompt']['en'] += ' A different scene.'
        with self.assertRaisesRegex(InputError, '作り直'):
            self.s.put_sample_pair(NID, changed, sha)
        self.assertEqual(self.s.state, before)

    def test_legacy_word_override_cannot_override_new_style_or_change_children(self):
        from app.store import _digest
        nid='shojo-penonly'
        self.s.edit(nid,{'words_en':'Old legacy words that must remain only in old child recipes.'})
        child=self.s.children(nid)[0]
        child_before=self.s.style_prompt(child)
        style={'ja':'細いペン線だけ。','en':'Fine pen lines only.','tags':'pen lines'}
        items=self.pair_items()
        for item in items:
            item['prompt']={lang:style[lang]+' scene' for lang in ('ja','en')}
        self.s.put_sample_pair(nid,items,_digest(style),complete_style=style)
        self.assertEqual(self.s.style_prompt(nid),style)
        self.assertEqual(self.s.style_prompt(child),child_before)

    def test_pair_import_without_complete_style_still_refuses_single_image(self):
        from app.store import _digest
        self.s.put_sample_pair(NID,self.pair_items(),_digest(self.s.style_prompt(NID)))
        before=copy.deepcopy(self.s.state)
        with self.assertRaisesRegex(InputError,'2枚'):
            self.s.put_sample(NID,image_bytes(value=80))
        self.assertEqual(self.s.state,before)

    def test_pending_edit_rejects_old_images_then_commits_new_pair(self):
        from app.store import _digest
        items=self.pair_items()
        self.s.put_sample_pair(NID,items,_digest(self.s.style_prompt(NID)))
        previous=self.client.get('/v1/styles/'+NID).json()
        self.s.edit(NID,{'words_en':'The requested new drawing method.'})
        pending=self.s.requested_style(NID)
        changed=copy.deepcopy(items)
        for item in changed:
            item['prompt']={lang:pending[lang]+' scene' for lang in ('ja','en')}
        with self.assertRaisesRegex(InputError,'作り直'):
            self.s.put_sample_pair(NID,changed,_digest(pending))
        self.assertEqual(self.client.get('/v1/styles/'+NID).json()['prompt'],previous['prompt'])
        for i,item in enumerate(changed):
            item['raw']=image_bytes(value=30+i*40)
        self.s.put_sample_pair(NID,changed,_digest(pending))
        after=self.client.get('/v1/styles/'+NID).json()
        self.assertEqual(after['prompt'],pending)
        self.assertEqual(after['version'],previous['version']+1)
        self.assertNotEqual(after['samples'],previous['samples'])
        self.assertNotIn('pending_style',self.s.state['nodes'][NID])
        self.assertIsNone(self.s.state['nodes'][NID]['regen'])

    def test_tags_only_edit_queues_pair_without_changing_publication(self):
        from app.store import _digest
        items = self.pair_items()
        self.s.put_sample_pair(NID, items, _digest(self.s.style_prompt(NID)))
        published = self.client.get('/v1/styles/'+NID).json()
        self.assertIsNone(self.s.state['nodes'][NID]['regen'])
        self.s.edit(NID, {'words_tags': 'new pending tags'})
        pending = self.s.requested_style(NID)
        self.assertEqual(pending['tags'], 'new pending tags')
        current = self.client.get('/v1/styles/'+NID).json()
        for key in ('prompt', 'samples', 'version'):
            self.assertEqual(current[key], published[key])
        self.assertIsNotNone(self.s.state['nodes'][NID]['regen'])
        self.assertIn(NID, [q['id'] for q in self.s.queue()])
        reloaded = Store(self.root/'data', seed_dir=self.root/'none', compare_dir=self.root/'none')
        self.assertEqual(reloaded.requested_style(NID), pending)
        self.assertIn(NID, [q['id'] for q in reloaded.queue()])
        self.assertEqual(reloaded.style_prompt(NID), published['prompt'])
        with self.assertRaisesRegex(InputError, '作り直'):
            self.s.put_sample_pair(NID, items, _digest(pending))
        for i, item in enumerate(items):
            item['raw'] = image_bytes(value=40+i*40)
        self.s.put_sample_pair(NID, items, _digest(pending))
        self.assertEqual(self.s.style_prompt(NID), pending)
        self.assertIsNone(self.s.state['nodes'][NID]['regen'])

    def test_pending_pair_reset_and_cancel_preserve_confirmed_style(self):
        from app.store import _digest
        self.s.put_sample_pair(NID, self.pair_items(), _digest(self.s.style_prompt(NID)))
        published = self.client.get('/v1/styles/'+NID).json()
        for operation in (self.s.reset, self.s.cancel_regen):
            self.s.edit(NID, {'words_tags': 'pending tags'})
            operation(NID)
            self.assertNotIn('pending_style', self.s.state['nodes'][NID])
            current = self.client.get('/v1/styles/'+NID).json()
            for key in ('prompt', 'samples', 'version'):
                self.assertEqual(current[key], published[key])

    def test_pending_pair_survives_failed_import_and_restart(self):
        from unittest.mock import patch
        from app.store import _digest
        items = self.pair_items()
        self.s.put_sample_pair(NID, items, _digest(self.s.style_prompt(NID)))
        self.s.edit(NID, {'words_tags': 'pending tags'})
        before = copy.deepcopy(self.s.state)
        for i, item in enumerate(items):
            item['raw'] = image_bytes(value=40+i*40)
        with patch.object(self.s, '_save', side_effect=OSError('synthetic disk failure')):
            with self.assertRaises(OSError):
                self.s.put_sample_pair(NID, items, _digest(self.s.requested_style(NID)))
        self.assertEqual(self.s.state, before)
        reloaded = Store(self.root/'data', seed_dir=self.root/'none', compare_dir=self.root/'none')
        self.assertEqual(reloaded.state['nodes'][NID], before['nodes'][NID])
        self.assertIn(NID, [q['id'] for q in reloaded.queue()])

    def test_pending_style_is_visible_in_admin_form_not_public_prompt(self):
        import re
        from unittest.mock import patch
        from app.store import _digest
        self.s.put_sample_pair(NID,self.pair_items(),_digest(self.s.style_prompt(NID)))
        self.s.edit(NID,{'words_en':'A pending drawing method.'})
        with patch.object(main,'require_admin',return_value=None):
            html=self.client.get('/admin/n/'+NID).text
        match=re.search(r'<textarea[^>]*name="words_en"[^>]*>(.*?)</textarea>',html,re.S)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1),'A pending drawing method.')

    def test_stale_complete_style_cannot_cancel_pending_edit(self):
        from app.store import _digest
        items=self.pair_items()
        style=self.s.style_prompt(NID)
        self.s.put_sample_pair(NID,items,_digest(style))
        self.s.edit(NID,{'words_en':'The newer pending method.'})
        before=copy.deepcopy(self.s.state)
        stale=copy.deepcopy(items)
        for item in stale:
            item['created_at']='2026-11-07T05:00:00Z'
        with self.assertRaisesRegex(InputError,'再生成待ち'):
            self.s.put_sample_pair(NID,stale,_digest(style),complete_style=style)
        self.assertEqual(self.s.state,before)

    def test_single_replacement_drops_old_application(self):
        self.seed_pair_state()
        self.s.put_sample(NID, image_bytes(value=80))
        self.assertEqual(len(self.s.samples(NID)), 1)

    def test_pair_state_save_failure_preserves_previous_state_and_files(self):
        from unittest.mock import patch
        from app.store import _digest
        first = self.s.put_sample(NID, image_bytes())
        before = copy.deepcopy(self.s.state)
        with patch.object(self.s, '_save', side_effect=OSError('synthetic disk failure')):
            with self.assertRaises(OSError):
                self.s.put_sample_pair(NID, self.pair_items(), _digest(self.s.style_prompt(NID)))
        self.assertEqual(self.s.state, before)
        self.assertTrue((self.s.files_dir/NID/first['file']).is_file())

    def test_loopback_pair_import_and_external_denial(self):
        import base64
        from app.store import _digest
        items = self.pair_items()
        payload = {'samples': [{**{k:v for k,v in i.items() if k != 'raw'},
                                'image_b64':base64.b64encode(i['raw']).decode()} for i in items],
                   'style_prompt_sha256':_digest(self.s.style_prompt(NID))}
        self.assertEqual(self.client.post('/internal/sample-pairs/'+NID,json=payload).status_code,404)
        with TestClient(main.app,base_url=ORIGIN,client=('127.0.0.1',55000)) as local:
            response = local.post('/internal/sample-pairs/'+NID,json=payload)
            self.assertEqual(response.status_code,200,response.text[:500])
        self.assertEqual(len(self.client.get('/v1/styles/'+NID).json()['samples']),2)

    def test_api_returns_both_saved_samples_and_primary_reference(self):
        first, second = self.seed_pair_state()
        body = self.client.get('/v1/styles/'+NID).json()
        self.assertEqual([s['subject'] for s in body['samples']], [first['subject'], 'application'])
        self.assertEqual(body['reference'], 0)
        self.assertEqual(body['samples'][1]['prompt'], second['prompt'])
        self.assertEqual(self.client.get(body['samples'][1]['url']).status_code, 200)



class SeedStartupPersistenceTests(unittest.TestCase):
    """Synthetic seed fixtures; never production state or generated sample artwork."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='manga-seed-startup-')
        self.root = Path(self.temp.name)
        self.data = self.root/'data'
        self.seed = self.root/'seed'
        self.ids = ['shonen-battle', 'shonen-battle-chibi-comic']
        self.initial = Store(self.data, seed_dir=self.root/'none', compare_dir=self.root/'none')
        # Larger retained metadata makes repeated full-state writes explicit, not a timing assertion.
        self.initial.state['nodes'][self.ids[0]]['synthetic_retained_metadata'] = 'fixture-' * 32000
        self.initial._save()
        self.before = copy.deepcopy(self.initial.state)
        self.add_seed('a'*64, self.ids)

    def tearDown(self):
        self.temp.cleanup()

    def add_seed(self, shard, ids):
        import hashlib
        from app.store import _digest
        folder = self.seed/'pairs'/shard
        folder.mkdir(parents=True)
        style = {'ja':'白黒の線画。', 'en':'Monochrome line drawing.', 'tags':'monochrome, lines'}
        manifest = []
        for nid in ids:
            samples = []
            for role, value in [('representative', 80), ('application', 180)]:
                output = io.BytesIO()
                Image.new('L', (256, 256), value).save(output, 'JPEG')
                raw = output.getvalue()
                name = nid+'-'+role+'.jpg'
                (folder/name).write_bytes(raw)
                samples.append({'subject':role, 'file':name, 'sha256':hashlib.sha256(raw).hexdigest(),
                                'bytes':len(raw), 'prompt':{lang:style[lang]+' scene' for lang in ('ja','en')},
                                'model_version':'gpt-image-2.6-sunburst', 'created_at':'2026-11-07T04:00:00Z'})
            manifest.append({'id':nid, 'complete_style':style, 'style_prompt_sha256':_digest(style), 'samples':samples})
        (folder/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False))
        return folder

    def test_startup_commits_all_seed_pairs_once(self):
        from unittest.mock import patch
        from app import store as module
        with patch.object(module, '_write_atomic', wraps=module._write_atomic) as writer:
            loaded = Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        state_writes = [call for call in writer.call_args_list if Path(call.args[0]) == loaded.state_file]
        self.assertEqual(len(state_writes), 1, 'startup must not serialize all retained data twice for every pair')
        self.assertEqual(json.loads(loaded.state_file.read_text()), loaded.state)
        for nid in self.ids:
            self.assertEqual([sample['subject'] for sample in loaded.samples(nid)], ['representative','application'])
            self.assertIn('pair_seed_sha256', loaded.state['nodes'][nid])
            self.assertEqual(loaded.state['nodes'][nid]['version'], self.before['nodes'][nid]['version']+1)
        for nid in set(self.before['nodes'])-set(self.ids):
            self.assertEqual(loaded.state['nodes'][nid], self.before['nodes'][nid])
        restarted = Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        self.assertEqual(restarted.state, loaded.state)
        self.assertEqual(len(list((self.data/'pair-history').glob('*.json'))), 2)

    def test_later_bad_shard_preserves_earlier_valid_pairs(self):
        broken = self.seed/'pairs'/('f'*64)
        broken.mkdir()
        (broken/'manifest.json').write_text('[{}]')
        with self.assertRaises(ValueError):
            Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        loaded = Store(self.data, seed_dir=self.root/'none', compare_dir=self.root/'none')
        for nid in self.ids:
            self.assertEqual(len(loaded.samples(nid)), 2)
            self.assertIn('pair_seed_sha256', loaded.state['nodes'][nid])

    def test_later_bad_shard_keeps_original_error_when_flushing_also_fails(self):
        from unittest.mock import patch
        from app import store as module
        broken = self.seed/'pairs'/('f'*64)
        broken.mkdir()
        (broken/'manifest.json').write_text('[{}]')
        previous = self.initial.state_file.read_bytes()
        original = module._write_atomic
        def fail_state(path, raw):
            if Path(path) == self.initial.state_file:
                raise OSError('synthetic flush failure')
            return original(path, raw)
        with patch.object(module, '_write_atomic', side_effect=fail_state):
            with self.assertRaisesRegex(ValueError, '2枚組の項目が不正') as caught:
                Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        self.assertIsInstance(caught.exception.__cause__, OSError)
        self.assertEqual(str(caught.exception.__cause__), 'synthetic flush failure')
        self.assertEqual(self.initial.state_file.read_bytes(), previous)

    def test_state_commit_failure_leaves_previous_disk_bytes(self):
        from unittest.mock import patch
        from app import store as module
        previous = self.initial.state_file.read_bytes()
        original = module._write_atomic
        def fail_state(path, raw):
            if Path(path) == self.initial.state_file:
                raise OSError('synthetic state disk failure')
            return original(path, raw)
        with patch.object(module, '_write_atomic', side_effect=fail_state):
            with self.assertRaisesRegex(OSError, 'synthetic state disk failure'):
                Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        self.assertEqual(self.initial.state_file.read_bytes(), previous)
        recovered = Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        self.assertTrue(all(len(recovered.samples(nid)) == 2 for nid in self.ids))

    def test_resume_after_pair_commit_before_seed_marker_does_not_bump_twice(self):
        loaded = Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        nid = self.ids[0]
        expected = copy.deepcopy(loaded.state['nodes'][nid])
        loaded.state['nodes'][nid].pop('pair_seed_sha256')
        loaded._save()
        resumed = Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        self.assertEqual(resumed.state['nodes'][nid], expected)
        self.assertTrue(list((self.data/'pair-history').glob(nid+'-*.json')))

    def test_manual_save_remains_immediate_after_startup(self):
        loaded = Store(self.data, seed_dir=self.seed, compare_dir=self.root/'none')
        loaded.state['nodes'][self.ids[0]]['synthetic_manual_marker'] = 'updated'
        loaded._save()
        self.assertEqual(json.loads(loaded.state_file.read_text()), loaded.state)

if __name__ == '__main__':
    unittest.main()
