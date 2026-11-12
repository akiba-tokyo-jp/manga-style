#!/usr/bin/env python3
"""説明用2枚組を固定SHAのReleaseから検査してDockerのseedへ置く。stdlibのみ。"""
import base64
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = Path(__file__).with_name('explanatory_bundles.json')
DEST = ROOT/'costlab-auth/manga/app/seed/pairs'
HELPER = ROOT/'costlab-auth/manga/app/pair_seed.py'
spec = importlib.util.spec_from_file_location('manga_pair_seed', HELPER)
assert spec and spec.loader
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def read_bundle(path, record, known_ids):
    if path.stat().st_size > 8*1024*1024:
        raise ValueError('2枚組のアーカイブが大きすぎます。')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != record['sha256']:
        raise ValueError('2枚組のアーカイブSHAが不一致です。')
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if (len(entries) > 65 or len({e.filename for e in entries}) != len(entries)
                or any(stat.S_ISLNK(e.external_attr >> 16) or e.file_size > 4*1024*1024 for e in entries)
                or sum(e.file_size for e in entries) > 64*1024*1024):
            raise ValueError('2枚組アーカイブの項目が不正です。')
        expected = {'manifest.json', *(nid+'-'+role+'.jpg' for nid in record['nodes'] for role in ('representative','application'))}
        if len(set(record['nodes'])) != len(record['nodes']) or {e.filename for e in entries} != expected:
            raise ValueError('2枚組の配布対象が不一致です。')
        files = {e.filename:archive.read(e) for e in entries}
    manifest = json.loads(files.pop('manifest.json'))
    helper.validate(manifest, files, known_ids)
    if {p['id'] for p in manifest} != set(record['nodes']):
        raise ValueError('枝の一覧が配布記録と不一致です。')
    return manifest, files


def prepare(archive_dir=None, *, registry_path=REGISTRY, dest=DEST):
    registry = json.loads(Path(registry_path).read_text())
    catalog = json.loads((ROOT/'costlab-auth/manga/app/catalog.json').read_text())
    known_ids = {n['id'] for n in catalog['nodes']}
    dest = Path(dest)
    dest.parent.mkdir(parents=True,exist_ok=True)
    seen = set()
    if registry['repository'] != 'akiba-tokyo-jp/manga-style' or len(registry['bundles']) > 128:
        raise ValueError('配布元または配布数が不正です。')
    with tempfile.TemporaryDirectory(prefix='manga-explanatory-',dir=dest.parent) as temp:
        temp = Path(temp)
        staged = temp/'staged'
        staged.mkdir(mode=0o755)
        for record in registry['bundles']:
            if (not isinstance(record['asset'], str) or Path(record['asset']).name != record['asset']
                    or not helper.SHA.fullmatch(record['sha256'])
                    or any(not isinstance(nid,str) or not helper.ID.fullmatch(nid) for nid in record['nodes'])):
                raise ValueError('2枚組の配布指定が不正です。')
            if seen & set(record['nodes']):
                raise ValueError('配布枝が重複しています。')
            asset_channel = 'release_tag' in record
            if asset_channel == ('release_bodies' in record):
                raise ValueError('Release assetか旧本文分割のどちらか一つを指定してください。')
            if (asset_channel and (not isinstance(record['release_tag'], str)
                                  or not helper.ID.fullmatch(record['release_tag']))):
                raise ValueError('Release名が不正です。')
            if not re.fullmatch(r'[a-z0-9][a-z0-9.-]*\.zip',record['asset']):
                raise ValueError('アーカイブ名が不正です。')
            source = Path(archive_dir) if archive_dir is not None else temp
            if archive_dir is None and asset_channel:
                subprocess.run(['gh','release','download',record['release_tag'],'--repo',registry['repository'],
                                '--pattern',record['asset'],'--dir',str(source)],
                               check=True,capture_output=True,text=True,timeout=120)
            elif archive_dir is None:
                encoded = []
                for tag in record['release_bodies']:
                    if not isinstance(tag,str) or not helper.ID.fullmatch(tag):
                        raise ValueError('Release名が不正です。')
                    response = subprocess.run(['gh','api',f"repos/{registry['repository']}/releases/tags/{tag}"], check=True,capture_output=True,text=True)
                    body = json.loads(response.stdout)['body']
                    marker = '<!-- manga-explanatory-base64\n'
                    if not isinstance(body,str) or body.count(marker) != 1 or not body.endswith('\n-->\n'):
                        raise ValueError('2枚組Release本文が不正です。')
                    encoded.append(body.partition(marker)[2].removesuffix('\n-->\n'))
                    if sum(map(len,encoded)) > 12*1024*1024:
                        raise ValueError('2枚組Release本文が大きすぎます。')
                (source/record['asset']).write_bytes(base64.b64decode(''.join(encoded),validate=True))
            pairs, files = read_bundle(source/record['asset'],record,known_ids)
            seen.update(record['nodes'])
            shard = staged/record['sha256']
            shard.mkdir(mode=0o755)
            for name, raw in files.items():
                target=shard/name; target.write_bytes(raw); target.chmod(0o644)
            target=shard/'manifest.json'
            target.write_text(json.dumps(pairs,ensure_ascii=False,indent=2)+'\n');target.chmod(0o644)
        # All shards verified before replacing disposable staging. Nothing touches the live volume.
        if dest.exists():
            shutil.rmtree(dest)
        staged.rename(dest)
    print(f'verified and staged {len(seen)} explanatory pairs')


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive-dir',type=Path)
    args=parser.parse_args()
    prepare(args.archive_dir)
