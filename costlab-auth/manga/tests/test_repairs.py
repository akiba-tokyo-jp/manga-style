"""再確認で指定された29枝だけを改修し、他の枝を変えない回帰試験。"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/manga_catalog'))
import build_tree as B

TARGETS = {
    'shonen-sports-muscle-mass', 'shonen-carved-engraving',
    'josei-office-doodle-casual', 'josei-office-natural-quiet', 'josei-office-pencil-soft',
    'josei-family-doodle-casual', 'josei-love', 'josei-love-modern-flat', 'josei-love-rough-light',
    'josei-drama', 'josei-drama-ink-bleed', 'josei-period-ukiyoe-flat', 'josei-period-kirie',
    'josei-period-inkwash-quiet', 'josei-comedy-doodle-casual', 'kodomo-animal-kirie',
    'gag', 'gag-surreal-dot-contours', 'gag-deadpan-modern-town', 'horror-kaidan',
    'horror-folk-kirie', 'horror-school', 'horror-urban-kagee', 'horror-panic-crack-debris',
    'essay', 'essay-diary-gentle-soft', 'essay-travel-kirie',
    'gekiga-historical-hikime-yamato', 'gekiga-adventure-ligne-claire',
}

class RepairTests(unittest.TestCase):
    def test_repairs_are_scoped_to_the_29_requested_nodes(self):
        tree = B.build()
        scoped = {n['id'] for n in tree['nodes'] if n.get('medium', '').startswith('repair-')}
        self.assertEqual(scoped, TARGETS)
        self.assertEqual(len(tree['nodes']), 2756)

    def test_generation_uses_the_repaired_medium_at_every_level(self):
        import tempfile
        sys.path.insert(0, str(ROOT / 'costlab-auth/manga'))
        from app.store import Store
        with tempfile.TemporaryDirectory() as d:
            catalog = Path(d) / 'fixture-catalog.json'
            tree = B.build()
            # 実画像を承認した記録とは別の、画材組立て専用の空Store fixture。
            fixture = {k: tree[k] for k in ('common', 'media', 'subjects', 'character',
                'scenes', 'l2_edit', 'l3_scenes', 'l3_lead', 'avoid')}
            fixture.update(format=1, approved_samples={}, avoid_words=B.AVOID_WORDS,
                deny=B.DENY, step_labels=B.STEP_LABELS, nodes=[], styles={})
            for n in tree['nodes']:
                src = dict(n, title={'ja': n['title'], 'en': n['title']},
                    summary={'ja': n['summary'], 'en': n['summary']})
                if n['level'] == 3:
                    fixture['styles'][n['id']] = src
                    src = dict(id=n['id'], parent=n['parent'], level=3, style=n['id'])
                fixture['nodes'].append(src)
            catalog.write_text(json.dumps(fixture, ensure_ascii=False))
            s = Store(Path(d) / 'state', catalog_file=catalog, seed_dir=Path(d) / 'empty-seeds')
            for nid in s.order:
                self.assertEqual(s.style_prompt(nid), B.style_prompt(tree, nid), nid)
                self.assertEqual(s.generation_steps(nid), B.sample_steps(tree, nid), nid)
            for nid in TARGETS:
                with self.subTest(nid=nid):
                    medium = s.media[s.base[nid]['medium']]
                    steps = s.generation_steps(nid)
                    if s.base[nid]['level'] == 1:
                        self.assertIn(medium['common']['en'], steps[-1]['en'])
                    else:
                        self.assertEqual(steps[-1]['en'], medium['edit']['en'].replace('{look}',
                            s.words(nid)['en'] if s.base[nid]['level'] == 2 else
                            s.words(s.base[nid]['parent'])['en'] + '. ' + s.l3_lead['en'] + s.words(nid)['en']))
