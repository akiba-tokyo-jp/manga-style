#!/usr/bin/env python3
"""2枚組のローカル回帰。CI自動起動を再有効化せず、結果と入力SHAを保存する。"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
COMMANDS = [
    ['tools/manga_catalog/export_site_tree.py','--check'],
    ['tools/manga_catalog/check_pairs.py','--self-test'],
    ['-m','unittest','discover','-s','tools/manga_catalog','-p','test_explanatory_generation.py','-v'],
    ['-m','unittest','discover','-s','costlab-auth/manga/tests','-p','test_explanatory_pairs.py','-v'],
    ['-W','ignore','-m','unittest','discover','-s','costlab-auth/manga/tests','-p','checks.py','-v'],
    ['-m','unittest','discover','-s','costlab-auth/manga/tests','-p','test_compare.py','-k','SiteTests','-v'],
    ['ops/tools/check_secrets_scope.py'],
    ['-m','unittest','discover','-s','costlab-auth/manga/tests','-p','test_pair_release.py','-v'],
    ['-m','unittest','discover','-s','costlab-auth/manga/tests','-p','test_model_gallery.py','-v'],
    ['-m','unittest','discover','-s','costlab-auth/manga/tests','-p','test_split_repository.py','-v'],
]

def sources():
    paths = set()
    for base in ['tools/manga_catalog','costlab-auth/manga/app','costlab-auth/manga/tests']:
        for p in (ROOT/base).rglob('*'):
            if p.is_file() and p.suffix in {'.py','.json','.html','.css','.js','.jpg'} and '__pycache__' not in p.parts:
                paths.add(p)
    paths.add(ROOT/'ops/tools/check_secrets_scope.py')
    for p in [ROOT/'costlab-auth/docker-compose.yml',ROOT/'caddy/Caddyfile',ROOT/'costlab-auth/manga/requirements.txt']:
        paths.add(p)
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    before=sources()
    (args.output/'pre-sources.json').write_text(json.dumps(before,indent=2))
    rows=[]
    for i,argsv in enumerate(COMMANDS):
        log=args.output/f'command-{i}.log'
        start=time.monotonic()
        with log.open('w') as f:
            done=subprocess.run([sys.executable,*argsv],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=180)
        row={'command':[sys.executable,*argsv],'exit_code':done.returncode,'seconds':time.monotonic()-start,
             'log':str(log),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
        rows.append(row)
        print(json.dumps({'index':i,'exit_code':done.returncode,'seconds':round(row['seconds'],2)}),flush=True)
        if done.returncode:
            break
    after=sources()
    receipt={'expected_commands':len(COMMANDS),'commands':rows,'pre_sources':before,'post_sources':after,
             'sources_unchanged':before==after,'dependencies':{name:importlib.metadata.version(name) for name in ['fastapi','starlette','pillow','httpx2','jinja2']},
             'passed':len(rows)==len(COMMANDS) and all(r['exit_code']==0 for r in rows) and before==after,
             'scope_note':'旧checksの追加画像試験2件は未ステージならskip。本番取込・配布bundle・全件生成・配備の成功は含まない。'}
    (args.output/'result.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2))
    return 0 if receipt['passed'] else 1

if __name__=='__main__':
    raise SystemExit(main())
