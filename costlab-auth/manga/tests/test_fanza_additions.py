"""FANZA本文調査から既存平面彩色を成人3土台へ拡張する。"""
from pathlib import Path
import hashlib,json
import sys,unittest
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/manga_catalog'))
import build_tree as bt
from commercial_additions import NEW_IDS as COMMERCIAL_IDS
NEW={'josei-office-flat-color','josei-comedy-flat-color','seinen-profession-flat-color'}

class FanzaAdditionsTests(unittest.TestCase):
    def test_three_adult_rendering_placements_without_new_figure_bases(self):
        t=bt.build();by={n['id']:n for n in t['nodes']}
        self.assertTrue(NEW <= set(by),'成人土台の平面カラー3枝が不足')
        self.assertEqual(len(by),2754+len(COMMERCIAL_IDS))
        self.assertEqual(sum(n['level']==2 for n in by.values()),117)
        for nid in NEW:
            self.assertEqual(by[nid]['level'],3)
            self.assertEqual(by[nid]['medium'],'x100-flat-color')
            self.assertEqual(by[by[nid]['parent']]['level'],2)

    def test_existing_2751_prompt_pairs_are_unchanged(self):
        t=bt.build()
        old={n['id']:{'style':bt.style_prompt(t,n['id']),'sample':bt.sample_prompt(t,n['id'])}
             for n in t['nodes'] if n['id'] not in (NEW|COMMERCIAL_IDS)}
        self.assertEqual(len(old),2751)
        self.assertEqual(hashlib.sha256(json.dumps(old,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
                         '18dc585d21777163d8487291fc86ad80da418652e34400d2a8663354eaced9f3')

    def test_adult_background_retains_clear_objects_without_sparse_white_rule(self):
        t=bt.build()
        old='background in white space and a few unblurred colored shapes'
        for nid in NEW:
            prompt=bt.style_prompt(t,nid)['en']
            self.assertNotIn(old,prompt)
            self.assertIn('background in clear colored shapes without blur',prompt)
        self.assertIn(old,bt.style_prompt(t,'essay-parenting-flat-color')['en'])

    def test_export_scopes_new_background_words_away_from_old_flat_styles(self):
        import export_site_tree as ex
        t=ex.bundle()
        by={n['id']:n for n in t['nodes']}
        old_key=by['essay-parenting-flat-color']['style']
        for nid in NEW:
            key=by[nid]['style']
            self.assertNotEqual(key,old_key)
            self.assertIn('background in clear colored shapes without blur',t['styles'][key]['words']['en'])
        self.assertIn('background in white space and a few unblurred colored shapes',t['styles'][old_key]['words']['en'])

    def test_routine_ci_discovers_fanza_regression_once(self):
        workflow=(ROOT/'.github/workflows/manga-style-validate.yml').read_text()
        self.assertEqual(workflow.count("-p 'test_fanza_additions.py'"),1)

if __name__=='__main__':unittest.main()
