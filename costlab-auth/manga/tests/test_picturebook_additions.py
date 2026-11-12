"""絵本調査の素材L3追加だけを許し、既存2742組を固定する。"""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/manga_catalog'))
import build_tree as bt
from x100_additions import NEW_IDS as X100_IDS
from fanza_additions import NEW_IDS as FANZA_IDS
from commercial_additions import NEW_IDS as COMMERCIAL_IDS

NEW = {'kodomo-geometric-paper-collage', 'gag-hetauma-color-crayon',
       'seinen-penscape-color-wash', 'kodomo-animal-textile-relief',
       'yonkoma-mochi-clay-relief'}
BASE_PROMPTS = '2886a0c0e9a2d27ba7498a1db5ccb875d0add5d606bace7b2022e1f78a7c50d9'


class PicturebookTests(unittest.TestCase):
    def test_only_five_verified_l3_placements(self):
        t = bt.build()
        by = {n['id']: n for n in t['nodes']}
        self.assertTrue(NEW <= set(by), '素材L3の追加がない')
        self.assertEqual(len(by), 2751 + len(FANZA_IDS) + len(COMMERCIAL_IDS))
        for nid in NEW:
            self.assertEqual(by[nid]['level'], 3)
            self.assertEqual(by[by[nid]['parent']]['level'], 2)
        self.assertEqual(sum(n['level'] == 2 for n in by.values()), 117)

    def test_all_previous_sample_and_api_words_are_byte_preserved(self):
        t = bt.build()
        old = {n['id']: {'style': bt.style_prompt(t, n['id']),
                         'sample': bt.sample_prompt(t, n['id'])}
               for n in t['nodes'] if n['id'] not in (NEW | X100_IDS | FANZA_IDS | COMMERCIAL_IDS)}
        self.assertEqual(len(old), 2742)
        self.assertEqual(hashlib.sha256(json.dumps(old, ensure_ascii=False, sort_keys=True).encode()).hexdigest(), BASE_PROMPTS)

    def test_new_media_retain_figure_and_allow_color_only_on_new_leaves(self):
        t = bt.build()
        by = {n['id']: n for n in t['nodes']}
        scoped = {n['id'] for n in t['nodes'] if n.get('medium', '').startswith('picturebook-')}
        self.assertEqual(scoped, NEW)
        for nid in NEW:
            n = by[nid]
            medium = t['media'][n['medium']]
            self.assertEqual(medium['expression'], 'color')
            self.assertIs(medium['retain_parent_look'], True)
            for lang in ('ja', 'en'):
                p = bt.sample_steps(t, nid)[1][lang]
                self.assertIn(by[n['parent']]['words'][lang], p)
                self.assertIn(n['words'][lang], p)
            self.assertNotIn('No color at all', bt.sample_steps(t, nid)[1]['en'])
            self.assertIn('color', bt.style_prompt(t, nid)['en'].lower())
            self.assertLessEqual(len(n['words']['ja']), 164)
            self.assertLessEqual(len(n['words']['en']), 531)

    def test_bilingual_export_and_routine_registration(self):
        import export_site_tree as ex
        t = ex.bundle()
        for nid in NEW:
            n = next(n for n in t['nodes'] if n['id'] == nid)
            s = t['styles'][n['style']]
            self.assertTrue(s['title']['en'])
            self.assertNotEqual(s['title']['ja'], s['title']['en'])
        workflow = (ROOT / '.github/workflows/manga-style-validate.yml').read_text()
        self.assertEqual(workflow.count("-p 'test_picturebook_additions.py'"), 1)


if __name__ == '__main__':
    unittest.main()
