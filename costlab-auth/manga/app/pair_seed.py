"""説明用2枚組の配布記録。実行/認証を含まないstdlib検査。"""
import hashlib
import json
import re

ID = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
SHA = re.compile(r'^[a-f0-9]{64}$')
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
MODEL = 'gpt-image-2.6-sunburst'


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def validate(manifest, files, known_ids):
    if not isinstance(manifest, list) or len(manifest) > 32:
        raise ValueError('2枚組の配布記録が不正です。')
    seen, expected = set(), set()
    for pair in manifest:
        if not isinstance(pair, dict) or set(pair) != {'id', 'complete_style', 'style_prompt_sha256', 'samples'}:
            raise ValueError('2枚組の項目が不正です。')
        nid = pair['id']
        if not isinstance(nid, str) or not ID.fullmatch(nid) or nid not in known_ids or nid in seen:
            raise ValueError('枝IDが不明または重複しています。')
        seen.add(nid)
        style = pair['complete_style']
        if (not isinstance(style, dict) or set(style) != {'ja', 'en', 'tags'}
                or any(not isinstance(v, str) or not v.strip() or len(v) > 8000 for v in style.values())
                or digest(style) != pair['style_prompt_sha256']):
            raise ValueError('絵柄の配布記録が一致しません。')
        samples = pair['samples']
        if not isinstance(samples, list) or len(samples) != 2:
            raise ValueError('2枚の見本が必要です。')
        for sample, role in zip(samples, ('representative', 'application')):
            if not isinstance(sample, dict) or set(sample) != {'subject', 'file', 'sha256', 'bytes', 'prompt', 'model_version', 'created_at'}:
                raise ValueError('見本の配布項目が不正です。')
            name = nid+'-'+role+'.jpg'
            if sample['subject'] != role or sample['file'] != name:
                raise ValueError('見本の順またはファイル名が不正です。')
            expected.add(name)
            raw = files.get(name)
            if (not isinstance(raw, bytes) or not raw.startswith(b'\xff\xd8')
                    or type(sample['bytes']) is not int or not 0 < len(raw) == sample['bytes'] <= 4*1024*1024
                    or not isinstance(sample['sha256'], str) or not SHA.fullmatch(sample['sha256'])
                    or hashlib.sha256(raw).hexdigest() != sample['sha256']):
                raise ValueError('見本画像のSHAまたは大きさが一致しません。')
            prompt = sample['prompt']
            if (not isinstance(prompt, dict) or set(prompt) != {'ja', 'en'}
                    or any(not isinstance(prompt[k], str) or not prompt[k].startswith(style[k]) or len(prompt[k]) > 8000 for k in ('ja','en'))
                    or sample['model_version'] != MODEL or not isinstance(sample['created_at'], str)
                    or not DATE.fullmatch(sample['created_at'])):
                raise ValueError('生成文または生成記録が不正です。')
        if samples[0]['sha256'] == samples[1]['sha256']:
            raise ValueError('別の場面の画像が必要です。')
    if set(files) != expected:
        raise ValueError('余分な画像または不足があります。')
    return manifest
