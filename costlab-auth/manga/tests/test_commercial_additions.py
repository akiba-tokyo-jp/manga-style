"""商業本文で確認した輪郭を抑える立体カラーの配置。"""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/manga_catalog'))
import build_tree as bt
NEW={p+'-volumetric-color' for p in ('seinen-profession','seinen-plainreal')}

class CommercialAdditionsTests(unittest.TestCase):
    def test_rendering_changes_only_at_two_existing_adult_bases(self):
        t=bt.build();by={n['id']:n for n in t['nodes']}
        self.assertTrue(NEW<=set(by),'輪郭を抑えた立体カラーの2候補が未接続')
        self.assertEqual(len(by),2756)
        self.assertEqual(sum(n['level']==2 for n in by.values()),117)
        for nid in NEW:
            self.assertEqual(by[nid]['level'],3)
            self.assertEqual(by[nid]['medium'],'commercial-volumetric-color')
            self.assertEqual(t['media'][by[nid]['medium']]['expression'],'color')
            self.assertTrue(t['media'][by[nid]['medium']]['retain_parent_look'])

    def test_existing_2754_prompt_pairs_are_unchanged(self):
        import hashlib,json
        t=bt.build()
        old={n['id']:{'style':bt.style_prompt(t,n['id']),'sample':bt.sample_prompt(t,n['id'])}
             for n in t['nodes'] if n['id'] not in NEW}
        self.assertEqual(len(old),2754)
        self.assertEqual(hashlib.sha256(json.dumps(old,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
                         '364423e335a11b25d202f6b5802de394e1ce1aec0aa61922589e7b5b51e58833')

    def test_export_has_bilingual_new_style_and_keeps_shared_old_styles(self):
        import export_site_tree as ex
        bundle=ex.bundle();by={n['id']:n for n in bundle['nodes']}
        for nid in NEW:
            style=bundle['styles'][by[nid]['style']]
            self.assertEqual(style['title']['en'],'Volumetric color with subdued outlines')
            self.assertEqual(style['medium'],'commercial-volumetric-color')
        self.assertNotEqual(by['seinen-profession-flat-color']['style'],by['seinen-profession-volumetric-color']['style'])

    def test_routine_ci_discovers_commercial_suite_once(self):
        workflow=(ROOT/'.github/workflows/manga-style-validate.yml').read_text()
        self.assertEqual(workflow.count("-p 'test_commercial_additions.py'"),1)

    def test_container_smoke_uses_current_count_and_rejects_other_counts(self):
        import json,shlex,subprocess
        workflow=(ROOT/'.github/workflows/manga-style-validate.yml').read_text()
        line=next(s for s in workflow.splitlines() if 'curl -fsS http://127.0.0.1:18080/v1/tree | python3 -c' in s)
        args=shlex.split(line.strip());code=args[args.index('-c')+1]
        count=len(bt.build()['nodes'])
        # 通常CIの実埋込みPythonを、明示した合成JSONで実行。Docker/ネットは使わない。
        def check(size):
            return subprocess.run([sys.executable,'-c',code],input=json.dumps({'version':1,'nodes':[None]*size}),text=True,capture_output=True,timeout=10)
        self.assertEqual(check(count).returncode,0,'正常な新カタログをcontainer smokeが拒否')
        for wrong in (count-1,count+1):self.assertNotEqual(check(wrong).returncode,0)

if __name__=='__main__':unittest.main()
