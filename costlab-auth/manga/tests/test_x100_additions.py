"""X本文100件調査による4描法追加と、既存2747組の保全。"""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/manga_catalog'))
import build_tree as bt
from fanza_additions import NEW_IDS as FANZA_IDS
from commercial_additions import NEW_IDS as COMMERCIAL_IDS

NEW = {'yonkoma-mochi-flat-color', 'essay-parenting-flat-color',
       'kodomo-geometric-flat-color', 'gag-retro-flat-color'}
BASE_PROMPTS = '82ee8646e038032899e54d6b7b19e4bc005d4ac121735f56567b952f0db7ca7a'


class X100Tests(unittest.TestCase):
    def test_only_four_rendering_leaves_added_and_original_pairs_preserved(self):
        t = bt.build()
        by = {n['id']: n for n in t['nodes']}
        self.assertTrue(NEW <= set(by), '実見した4描法が追加されていない')
        self.assertEqual(len(by), 2751 + len(FANZA_IDS) + len(COMMERCIAL_IDS))
        self.assertEqual(sum(n['level'] == 2 for n in by.values()), 117)
        old = {nid: {'style': bt.style_prompt(t, nid),
                     'sample': bt.sample_prompt(t, nid)}
               for nid in by if nid not in (NEW | FANZA_IDS | COMMERCIAL_IDS)}
        self.assertEqual(len(old), 2747)
        self.assertEqual(hashlib.sha256(json.dumps(old, ensure_ascii=False, sort_keys=True).encode()).hexdigest(), BASE_PROMPTS)
        for nid in NEW:
            self.assertEqual(by[nid]['level'], 3)
            self.assertEqual(by[by[nid]['parent']]['level'], 2)

    def test_bilingual_export_and_routine_registration(self):
        import export_site_tree as ex
        t = ex.bundle()
        for nid in NEW:
            n = next(n for n in t['nodes'] if n['id'] == nid)
            s = t['styles'][n['style']]
            self.assertTrue(s['title']['en'])
            self.assertNotEqual(s['title']['ja'], s['title']['en'])
        workflow = (ROOT / '.github/workflows/manga-style-validate.yml').read_text()
        self.assertEqual(workflow.count("-p 'test_x100_additions.py'"), 1)


if __name__ == '__main__':
    unittest.main()
