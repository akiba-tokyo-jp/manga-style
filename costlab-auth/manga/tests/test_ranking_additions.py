"""ランキング本文の不足候補を足し、既存の語と見本の対を保つ回帰試験。"""
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/manga_catalog'))
sys.path.insert(0, str(ROOT / 'costlab-auth/manga'))
import build_tree as bt
from picturebook_additions import NEW_IDS as PICTUREBOOK_IDS
from x100_additions import NEW_IDS as X100_IDS
from fanza_additions import NEW_IDS as FANZA_IDS
from commercial_additions import NEW_IDS as COMMERCIAL_IDS
from PIL import Image
from app.store import process_image

L2 = {'seinen-round-adult', 'seinen-dash-round', 'josei-compact-adult', 'josei-solid-adult'}
COLOR = {'josei-love-color-gradation', 'josei-romance-color-gradation',
         'shonen-romcom-color-gradation', 'seinen-action-color-gradation',
         'josei-yuri-spot-accent'}


class RankingAdditionTests(unittest.TestCase):
    def test_unselected_l2_trials_are_not_exported(self):
        tree = bt.build()
        ids = {n['id'] for n in tree['nodes']}
        self.assertFalse(ids & L2, '既存との差が未確定の土台を公開している')
        for nid in L2:
            self.assertFalse(any(i.startswith(nid + '-') for i in ids), nid)
            self.assertNotIn(nid, tree['l3_scenes'])
        existing = set(json.loads(bt.APPROVED.read_text())['samples']) - COLOR - PICTUREBOOK_IDS - X100_IDS - FANZA_IDS - COMMERCIAL_IDS
        self.assertEqual(ids - existing, COLOR | PICTUREBOOK_IDS | X100_IDS | FANZA_IDS | COMMERCIAL_IDS)

    def test_color_medium_is_scoped_to_the_verified_leaf(self):
        tree = bt.build()
        by = {n['id']: n for n in tree['nodes']}
        self.assertTrue(COLOR <= set(by), '彩色の追加枝がない')
        for nid in COLOR:
            n = by[nid]
            self.assertEqual(n['level'], 3)
            medium = tree['media'][n['medium']]
            self.assertEqual(medium['expression'], 'color')
            self.assertTrue(medium['retain_parent_look'])
            self.assertNotIn('No color at all', bt.sample_steps(tree, nid)[1]['en'])
            self.assertIn('color', bt.style_prompt(tree, nid)['en'].lower())

    def test_every_existing_prompt_digest_is_unchanged(self):
        tree = bt.build()
        records = json.loads(bt.APPROVED.read_text())['samples']
        for nid, record in records.items():
            self.assertEqual(bt.prompt_digest(bt.style_prompt(tree, nid)), record['style_prompt_sha256'], nid)
            self.assertEqual(bt.prompt_digest(bt.sample_prompt(tree, nid)), record['prompt_sha256'], nid)

    def test_expression_and_avoid_are_per_branch(self):
        from app.store import Store
        tree = bt.build()
        s = Store.__new__(Store)
        s.base = {n['id']: n for n in tree['nodes']}
        s.media = tree['media']
        s.avoid = list(tree['avoid'])
        self.assertEqual(s.expression('josei-romance-color-gradation'), 'color')
        self.assertEqual(s.expression('josei-love-pen-classic'), 'mono')
        self.assertNotIn('色', s.avoid_for('josei-romance-color-gradation'))
        self.assertEqual(s.avoid_for('josei-love-pen-classic'), s.avoid)

    def test_store_and_public_api_preserve_color_per_leaf(self):
        import tempfile
        from fastapi.testclient import TestClient
        from app import main
        from app.store import Store
        tree = bt.build()
        fixture = {k: tree[k] for k in ('common', 'media', 'subjects', 'character',
                   'scenes', 'l2_edit', 'l3_scenes', 'l3_lead', 'avoid')}
        # 実画像の採用とは別の、Store/API組立て専用の合成fixture。
        fixture.update(format=1, approved_samples={}, avoid_words=bt.AVOID_WORDS,
                       deny=bt.DENY, step_labels=bt.STEP_LABELS, nodes=[], styles={})
        for n in tree['nodes']:
            src = dict(n, title={'ja': n['title'], 'en': n['title']},
                       summary={'ja': n['summary'], 'en': n['summary']})
            if n['level'] == 3:
                fixture['styles'][n['id']] = src
                src = dict(id=n['id'], parent=n['parent'], level=3, style=n['id'])
            fixture['nodes'].append(src)
        with tempfile.TemporaryDirectory() as d:
            catalog = Path(d) / 'fixture.json'
            catalog.write_text(json.dumps(fixture, ensure_ascii=False))
            s = Store(Path(d) / 'state', catalog_file=catalog, seed_dir=Path(d) / 'no-seeds')
            buf = io.BytesIO()
            Image.new('RGB', (768, 1024), (152, 224, 65)).save(buf, 'JPEG', quality=85)
            raw = buf.getvalue()
            saved = main._store
            main._store = s
            try:
                with TestClient(main.app, base_url='https://manga.akiba.tokyo.jp') as client:
                    for nid in sorted(COLOR | PICTUREBOOK_IDS | X100_IDS | FANZA_IDS | COMMERCIAL_IDS):
                        s.put_sample(nid, raw)
                        before = json.dumps(s.state, sort_keys=True)
                        s.put_sample(nid, raw)
                        self.assertEqual(json.dumps(s.state, sort_keys=True), before)
                        r = client.get('/v1/styles/' + nid)
                        self.assertEqual(r.status_code, 200)
                        api = r.json()
                        expected = 'color'
                        self.assertEqual(api['expression'], expected)
                        self.assertNotIn('色', api['avoid'])
                        self.assertEqual(api['prompt'], s.style_prompt(nid))
                        image = client.get(api['samples'][0]['url'])
                        self.assertEqual(image.status_code, 200)
                        self.assertEqual(image.content, raw)
                        self.assertEqual(Image.open(io.BytesIO(image.content)).mode, 'RGB')
                    mono = client.get('/v1/styles/josei-love-pen-classic').json()
                    self.assertEqual(mono['expression'], 'mono')
                    self.assertIn('色', mono['avoid'])
                    from app.store import _digest
                    for old_id in set(s.order) - COLOR - PICTUREBOOK_IDS - X100_IDS - FANZA_IDS - COMMERCIAL_IDS:
                        legacy = _digest({
                            'path': [s.effective(c)['title'] for c in s.chain(old_id)],
                            'summary': s.effective(old_id)['summary'],
                            'prompt': s.style_prompt(old_id), 'avoid': s.avoid,
                        })
                        self.assertEqual(s.fingerprint(old_id), legacy, old_id)
                    # APIのexpressionだけが変わっても版のfingerprintは変わる。
                    nid = 'josei-romance-color-gradation'
                    before = s.fingerprint(nid)
                    medium = s.media[s.base[nid]['medium']]
                    medium['expression'] = 'mono'
                    try:
                        self.assertNotEqual(s.fingerprint(nid), before)
                    finally:
                        medium['expression'] = 'color'
            finally:
                main._store = saved

    def test_rgb_processing_is_opt_in_and_keeps_encoded_pair(self):
        im = Image.new('RGB', (768, 1024), (60, 180, 240))
        buf = io.BytesIO()
        im.save(buf, format='JPEG', quality=85)
        raw = buf.getvalue()
        sample, thumb = process_image(raw, color=True)
        self.assertEqual(sample, raw)
        self.assertEqual(Image.open(io.BytesIO(sample)).mode, 'RGB')
        self.assertEqual(Image.open(io.BytesIO(thumb)).mode, 'RGB')
        mono, _ = process_image(raw)
        self.assertEqual(Image.open(io.BytesIO(mono)).mode, 'L')


if __name__ == '__main__':
    unittest.main()
