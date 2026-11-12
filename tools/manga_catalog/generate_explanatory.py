#!/usr/bin/env python3
"""説明用見本の独立生成。1画像1process・新turn ID。既存契約以外へ切替しない。

検査だけ: python generate_explanatory.py jobs.json --output <作業先>
実生成: 同じコマンドに --run --limit 4 --workers 2 を付ける。
生成データはgit外へ。途中失敗・未確定の要求は自動再送しない。
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

MODEL = 'gpt-image-2.6-sunburst'
JOB_KEYS = {'id', 'subject', 'prompt', 'aspect_ratio', 'style_prompt_sha256', 'expression'}
ID = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path = Path(path)
    tmp = path.with_name('.'+path.name+'.'+uuid.uuid4().hex+'.tmp')
    with tmp.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def validate_jobs(jobs):
    if not isinstance(jobs, list) or not jobs:
        raise ValueError('画像ごとの生成依頼が必要です')
    seen = set()
    for job in jobs:
        if not isinstance(job, dict) or set(job) != JOB_KEYS:
            raise ValueError('依頼に履歴・参照画像・未知の項目は入れられません')
        key = (job['id'], job['subject'])
        if not isinstance(key[0], str) or not ID.fullmatch(key[0]) or key in seen:
            raise ValueError('枝IDが不正または重複しています')
        seen.add(key)
        if key[1] not in ('representative', 'application') or job['expression'] not in ('mono','color'):
            raise ValueError('見本の種類が不正です')
        if job['aspect_ratio'] not in ('portrait','square','landscape'):
            raise ValueError('構図の指定が不正です')
        if not isinstance(job['style_prompt_sha256'],str) or not re.fullmatch('[a-f0-9]{64}',job['style_prompt_sha256']):
            raise ValueError('絵柄プロンプトの記録が必要です')
        if not isinstance(job['prompt'],dict) or set(job['prompt']) != {'ja','en'}:
            raise ValueError('日英のプロンプトが必要です')
        if any(not isinstance(v,str) or not v.strip() or len(v)>8000 for v in job['prompt'].values()):
            raise ValueError('プロンプトが空または長すぎます')
    return jobs


def validate_request(job, endpoint, body):
    expected = {'prompt','model','n','quality','size','background'}
    if (endpoint != 'images/generations' or set(body) != expected or body['model'] != MODEL
            or body['prompt'] != job['prompt']['en'] or type(body['n']) is not int or body['n'] != 1
            or body['quality'] != 'high' or body['background'] != 'opaque'):
        raise ValueError('履歴なし・参照なし・指定モデルの独立要求ではありません')


def completed(job, folder):
    path = folder/'complete.json'
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    if record.get('success') is not True or record.get('job_sha256') != digest(job):
        raise ValueError('完了記録と現在の依頼が一致しません')
    image = folder/record['image']
    if image.parent != folder or not image.is_file() or file_sha(image) != record['image_sha256']:
        raise ValueError('保存画像が完了記録と一致しません')
    return True


def worker(job_path, attempt):
    """Fresh process only. Resolve credentials inside the existing provider, never print them."""
    from datetime import datetime, timezone
    from types import SimpleNamespace
    from PIL import Image
    job = json.loads(job_path.read_text())
    validate_jobs([job])
    home = Path(os.environ.get('HERMES_HOME', Path.home()/'.hermes'))
    plugin = home/'plugins/image_gen/sunburst-codex/__init__.py'
    # A local request override only; no config/plugin/auth changes.
    spec = importlib.util.spec_from_file_location('explanatory_image_provider', plugin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    session_id = str(uuid.uuid4())
    module.API_MODEL = MODEL
    module._resolve_model = lambda: (MODEL, {'quality':'high'})
    module.uuid = SimpleNamespace(uuid4=lambda: uuid.UUID(session_id))
    original = module._build_image_request
    request_seen = []
    def build(**kwargs):
        endpoint, body = original(**kwargs)
        validate_request(job, endpoint, body)
        request = {'endpoint':endpoint,'body':body,'session_id':session_id,
                   'provider_source_sha256':file_sha(plugin)}
        save(attempt/'request.json', request)
        request_seen.append(request)
        return endpoint, body
    module._build_image_request = build
    started = time.monotonic()
    result = module.OpenAICodexImageGenProvider().generate(job['prompt']['en'], aspect_ratio=job['aspect_ratio'])
    save(attempt/'result.json', result)  # Preserve the real response before assertions.
    if result.get('success') is not True:
        save(attempt/'failed.json', {'status':'failed','result':result,'elapsed_seconds':time.monotonic()-started})
        return 2
    if len(request_seen) != 1 or result.get('image_source') != 'final' or result.get('input_image_count') != 0:
        raise ValueError('最終画像または独立リクエストの確認ができません')
    source = Path(result['image'])
    with Image.open(source) as image:
        image.load()
        size, mode = list(image.size), image.mode
    shutil.copyfile(source, attempt/'original.png')
    record = {'success':True, 'job_sha256':digest(job), 'session_id':session_id,
              'image':'original.png','image_sha256':file_sha(attempt/'original.png'),
              'pixel_size':size,'mode':mode, 'requested_model':MODEL,
              'reported_model':result.get('reported_model'),'reported_quality':result.get('reported_quality'),
              'created_at':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'elapsed_seconds':time.monotonic()-started}
    save(attempt/'complete.json',record)
    print(json.dumps({'id':job['id'],'subject':job['subject'],'success':True,'size':size},ensure_ascii=False),flush=True)
    return 0


def launch(job, output, runtime_root):
    folder = output/job['id']/job['subject']
    folder.mkdir(parents=True,exist_ok=True)
    # Retain every attempt; never infer that an interrupted request was not sent.
    if (folder/'complete.json').exists():
        completed(job,folder)
        return {'id':job['id'],'subject':job['subject'],'status':'reused'}
    if (folder/'attempt.json').exists():
        raise ValueError('未完了の要求があります。記録を確認するまで再送しません: '+str(folder))
    save(folder/'job.json', job)
    save(folder/'attempt.json', {'job_sha256':digest(job),'started_at':time.time()})
    sys.path.insert(0,str(runtime_root))
    from hermes_cli._launchers import runtime_command
    command = runtime_command(runtime_root, code="import runpy,sys; path=sys.argv.pop(1); runpy.run_path(path,run_name='__main__')",
                              args=[str(Path(__file__).resolve()),'--worker',str(folder/'job.json'),str(folder)])
    with (folder/'worker.log').open('w') as log:
        proc = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=390)
    if proc.returncode != 0 or not completed(job,folder):
        raise RuntimeError('画像生成が停止しました。再送・別経路への切替はしません: '+str(folder))
    return {'id':job['id'],'subject':job['subject'],'status':'generated'}


def main():
    if len(sys.argv)>1 and sys.argv[1]=='--worker':
        return worker(Path(sys.argv[2]),Path(sys.argv[3]))
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('jobs',type=Path)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--run',action='store_true')
    p.add_argument('--limit',type=int,default=4)
    p.add_argument('--workers',type=int,choices=range(1,5),default=2)
    p.add_argument('--runtime-root',type=Path,default=Path.home()/'.hermes/hermes-agent')
    a = p.parse_args()
    jobs = validate_jobs(json.loads(a.jobs.read_text()))
    if a.limit < 1:
        p.error('--limit は1以上です')
    print(json.dumps({'jobs':len(jobs),'requested_model':MODEL,'run':a.run,'limit':a.limit,'workers':a.workers}),flush=True)
    if not a.run:
        return 0
    a.output.mkdir(parents=True,exist_ok=True)
    # An exclusive whole-run lock also guards the per-job exactly-once claim.
    import fcntl
    with (a.output/'.run.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        pending = [j for j in jobs if not completed(j,a.output/j['id']/j['subject'])]
        rows, failed = [], None
        with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
            # Submit only a bounded wave. No new wave after an access/quota/other failure.
            selected = pending[:a.limit]
            for start in range(0,len(selected),a.workers):
                futures = [pool.submit(launch,j,a.output,a.runtime_root) for j in selected[start:start+a.workers]]
                for f in futures:
                    try:
                        rows.append(f.result())
                    except Exception as exc:
                        failed = str(exc)
                if failed:
                    break
        summary = {'expected':len(jobs),'completed':sum(completed(j,a.output/j['id']/j['subject']) for j in jobs),
                   'this_run':rows,'error':failed}
        save(a.output/'summary.json',summary)
        print(json.dumps(summary,ensure_ascii=False),flush=True)
        return 2 if failed else 0

if __name__ == '__main__':
    raise SystemExit(main())
