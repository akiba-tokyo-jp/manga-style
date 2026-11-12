#!/usr/bin/env python3
"""Export only the existing application's public read projections for Cloudflare."""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'costlab-auth/manga'))
from starlette.requests import Request
from app import main

# Replaced with the receiving origin by the compatibility Worker, never a secret.
ASSET_ORIGIN = 'https://static.manga.invalid'


def request(path, **query):
    return Request({'type': 'http', 'method': 'GET', 'scheme': 'https',
                    'server': ('static.manga.invalid', 443), 'path': path,
                    'query_string': urlencode(query).encode(), 'headers': []})


def public_api(store, nid):
    previous = main._store
    try:
        main._store = store
        return {lang: json.loads(main.api_style(request('/v1/styles/' + nid, lang=lang), nid).body)
                for lang in ('ja', 'en')}
    finally:
        main._store = previous


def snapshot_store(snapshot, scratch, *, compare_dir=None):
    """Clone a quiescent snapshot and attach exact persisted state after metadata init.

    Store.__init__ normally refreshes/imports/saves. It must never see the source
    volume, nor refresh a snapshot's versions with newer seed images.
    """
    from app.store import COMPARE_DIR, ISO_Z, Store
    source, target = Path(snapshot).resolve(), Path(scratch).resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Snapshot and scratch must not overlap')
    def no_links(path):
        for candidate in (path, *path.parents):
            if candidate.is_symlink() or candidate.is_junction():
                raise ValueError('Linked snapshot paths are not supported')
    no_links(Path(snapshot).absolute())
    state_file = source / 'state.json'
    no_links(state_file)
    raw = state_file.read_bytes()
    state = json.loads(raw)
    if state.get('format') != 1 or state.get('api', {}).get('mode') != 'public':
        raise ValueError('Only a valid public-mode snapshot can be exported')
    for folder, dirs, files in os.walk(source / 'files', followlinks=False):
        for name in dirs + files:
            no_links(Path(folder) / name)
    if target.exists():
        raise ValueError('Snapshot scratch must be new')
    clone = Store(target, seed_dir=target / 'no-seed', compare_dir=compare_dir or COMPARE_DIR)
    if not isinstance(state.get('nodes'), dict) or set(state['nodes']) != set(clone.base):
        raise ValueError('Snapshot and source catalogue node identities differ')
    for node in state['nodes'].values():
        if (not isinstance(node, dict) or type(node.get('published')) is not bool
                or type(node.get('version')) is not int or node['version'] < 1
                or not isinstance(node.get('updated_at'), str) or not ISO_Z.fullmatch(node['updated_at'])):
            raise ValueError('Invalid persisted public state')
    if (source / 'files').exists():
        shutil.copytree(source / 'files', clone.files_dir, dirs_exist_ok=True)
    if state_file.read_bytes() != raw:
        raise ValueError('Snapshot changed while being copied')
    clone.state = state
    return clone


def export_store(store, output, *, max_files=20000, max_asset_bytes=25 * 1024 * 1024):
    """Read the approved public projection; replace a previous export only after success.

    The supplied Store must be an isolated copy, never the production volume.
    No raw state, archive, pending prompt, history or unreferenced file is copied.
    """
    from app.catalogue import FACETS, GPT, LOOK_GROUPS, MODELS, PAGE_SIZE, TEXT, features_match
    from app.ui import UI

    if store.api_mode() != 'public':
        raise ValueError('Token-mode snapshots cannot be published as a public static API')
    output = Path(output).resolve()
    data = store.data_dir.resolve()
    if output == ROOT or output in ROOT.parents or output == data or data in output.parents or output in data.parents:
        raise ValueError('Unsafe output directory')
    if output.exists() and not (output / '.manga-static-output').is_file():
        raise ValueError('Refusing to replace a directory that is not a manga static export')
    visible = [nid for nid in store.order if store.visible(nid)]
    if not visible:
        raise ValueError('Refusing to publish an empty catalogue')
    if any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', nid) for nid in visible):
        raise ValueError('Invalid public style identifier')
    output.parent.mkdir(parents=True, exist_ok=True)
    old_store, old_origin = main._store, main.SITE_ORIGIN
    old_same_title = store.same_title
    # Avoid re-scanning the whole catalogue for every translated detail page.
    names = {lang: defaultdict(list) for lang in UI}
    for lang in UI:
        for nid in visible:
            names[lang][store.title(nid, lang)].append(nid)
    def same_title(nid, lang):
        root = store.chain(nid)[0]
        return sorted((other for other in names[lang][store.title(nid, lang)] if other != nid),
                      key=lambda other: store.chain(other)[0] != root)
    store.same_title = same_title
    image_records = {}
    try:
        main._store, main.SITE_ORIGIN = store, ASSET_ORIGIN
        with tempfile.TemporaryDirectory(prefix='manga-static-', dir=output.parent) as temp:
            stage = Path(temp) / 'assets'
            stage.mkdir()
            def write(name, body):
                path = stage / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body if isinstance(body, str) else json.dumps(body, ensure_ascii=False, separators=(',', ':')),
                                encoding='utf-8', newline='\n')
            def copy_image(nid, name, expected=None):
                if not isinstance(name, str) or not re.fullmatch(r'[a-zA-Z0-9_.-]+\.jpg', name):
                    raise ValueError('Unsafe image name')
                path = store.sample_path(nid, name)
                if path is None or path.is_symlink():
                    raise ValueError(f'Missing or linked public image: {nid}/{name}')
                raw = path.read_bytes()
                digest = hashlib.sha256(raw).hexdigest()
                if expected is not None and digest != expected:
                    raise ValueError(f'Public image SHA mismatch: {nid}/{name}')
                target = stage / 'files' / nid / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
                image_records[f'/files/{nid}/{name}'] = {'sha256': digest, 'bytes': len(raw)}
            records = []
            for nid in visible:
                chain = store.chain(nid)
                prompt = store.style_prompt(nid)
                features = {key: [value for value, _, _ in choices
                                  if features_match(prompt, {key: value}, store.expression(nid))]
                            for key, choices in FACETS.items()}
                records.append({'id': nid, 'level': store.base[nid]['level'], 'chain': chain,
                                'look_group': nid in LOOK_GROUPS, 'features': features,
                                'labels': {lang: {**main.card(store, nid, lang, False),
                                    'hay': ' '.join([nid, *store.path_titles(nid, 'ja'), *store.path_titles(nid, 'en'),
                                                    store.shown(nid, 'summary', lang), prompt.get('tags', '')]).casefold()}
                                           for lang in UI}})
                write(f'_data/styles/{nid}.json', public_api(store, nid))
                pages = {}
                for lang in UI:
                    pages[lang] = {GPT: {plang: main.direct_style(request('/styles/' + nid, lang=lang, plang=plang,
                                                                           model=GPT), nid).body.decode()
                                        for plang in UI},
                                   'anima-turbo': {'ja': main.direct_style(request('/styles/' + nid, lang=lang,
                                                                                  model='anima-turbo'), nid).body.decode()}}
                write(f'_data/pages/{nid}.json', pages)
                for sample in store.samples(nid):
                    copy_image(nid, sample['file'], sample['sha256'])
                    copy_image(nid, sample['thumb'])
                comparison = store.comparison(nid)
                if comparison:
                    copy_image(nid, comparison['file'], comparison['sha256'])
            roots = [r['id'] for r in records if r['level'] == 1]
            topics = {r['id']: r['chain'][0] for r in records if r['level'] == 2}
            routes = {'roots': roots, 'topics': topics, 'visible': visible,
                      'facets': {k: [v[0] for v in values] for k, values in FACETS.items()},
                      'health': {'ok': True, 'nodes': len(visible),
                                 'comparisons': sum(bool(store.comparison(n)) for n in visible)},
                      'empty': {lang: str(main.env.get_template('_model_empty.html').module.empty(TEXT[lang])) for lang in UI},
                      'compare_note': {lang: TEXT[lang]['compare_note'] for lang in UI}}
            write('_data/routes.json', routes)
            fold = {chr(i): chr(i).casefold() for i in range(sys.maxunicode + 1)
                    if chr(i).casefold() != chr(i).lower()}
            write('_public/catalogue.json', {'records': records, 'facets': FACETS, 'text': TEXT,
                                            'ui': UI, 'page_size': PAGE_SIZE, 'casefold': fold})
            write('_data/models.json', json.loads(main.api_models(request('/v1/models')).body))
            for lang in UI:
                for model in MODELS:
                    write(f'_data/tree/{lang}-{model}.json', json.loads(main.api_tree(request('/v1/tree', lang=lang, model=model)).body))
                    gallery = main.index(request('/', lang=lang, model=model)).body.decode()
                    gallery = gallery.replace('</head>', '<script type="module" src="/static/gallery.mjs"></script></head>')
                    note = ('絞り込みには JavaScript が必要です。' if lang == 'ja' else 'Filtering requires JavaScript.')
                    gallery = gallery.replace('<main ', f'<noscript><p>{html.escape(note)}</p></noscript><main ', 1)
                    write(f'_data/gallery/{lang}-{model}.html', gallery)
                    write(f'_data/guide/{lang}-{model}.html', main.api_guide(request('/api', lang=lang, model=model)).body.decode())
                    write(f'_data/error/{lang}-{model}.html', main.not_found_page(request('/missing', lang=lang, model=model)).body.decode())
            for name in ('site.css', 'gallery.css', 'site.js'):
                write('static/' + name, (main.APP_DIR / 'static' / name).read_text(encoding='utf-8'))
            for name in ('gallery.mjs', 'catalogue.mjs'):
                source = ROOT / 'cloudflare/site' / name
                write('static/' + name, source.read_text(encoding='utf-8'))
            write('robots.txt', main.robots())
            write('.manga-static-output', '1\n')
            assets = [p for p in stage.rglob('*') if p.is_file()]
            if len(assets) > max_files:
                raise ValueError(f'Static asset count {len(assets)} exceeds limit {max_files}')
            oversized = [p.relative_to(stage).as_posix() for p in assets if p.stat().st_size > max_asset_bytes]
            if oversized:
                raise ValueError(f'Static assets exceed per-file limit: {oversized}')
            receipt = {'visible_nodes': len(visible), 'file_count': len(assets),
                       'total_bytes': sum(p.stat().st_size for p in assets),
                       'max_asset_bytes': max(p.stat().st_size for p in assets), 'images': image_records}
            backup = Path(temp) / 'previous'
            if output.exists():
                output.rename(backup)
            try:
                stage.rename(output)
            except BaseException:
                if backup.exists():
                    backup.rename(output)
                raise
            return receipt
    finally:
        store.same_title = old_same_title
        main._store, main.SITE_ORIGIN = old_store, old_origin


def check_snapshot_write_paths(snapshot, output, archives):
    if snapshot is None:
        return
    source = Path(snapshot).resolve()
    targets = {
        'output': Path(output), 'report': Path(output).parent / 'build-report.json',
        'archives': Path(archives), 'checkout': ROOT,
        'bootstrap': ROOT / '.build/bootstrap',
        'sample seeds': ROOT / 'costlab-auth/manga/app/seed/additions',
        'pair seeds': ROOT / 'costlab-auth/manga/app/seed/pairs',
        'comparison staging': ROOT / 'costlab-auth/manga/compare/files',
    }
    for label, path in targets.items():
        target = path.resolve()
        if source == target or source in target.parents or target in source.parents:
            raise ValueError(f'Write target overlaps original snapshot: {label}')
    temp = Path(tempfile.gettempdir()).resolve()
    if source == temp or source in temp.parents:
        raise ValueError('Temporary files would be written inside original snapshot')


def cli():
    import argparse
    from app.store import Store
    from cloudflare_assets import fetch_archives
    import prepare_samples
    import prepare_compare
    import prepare_explanatory

    def snapshot_path(value):
        if not value:
            raise argparse.ArgumentTypeError('snapshot directory must not be empty')
        return Path(value)

    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--archive-dir', type=Path, default=os.environ.get('MANGA_ARCHIVE_DIR') or ROOT / '.build/archives')
    parser.add_argument('--snapshot-dir', type=snapshot_path, default=os.environ.get('MANGA_SNAPSHOT_DIR'))
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/assets')
    args = parser.parse_args()
    check_snapshot_write_paths(args.snapshot_dir, args.output, args.archive_dir)
    fetch_archives(args.archive_dir)
    prepare_samples.prepare(args.archive_dir)
    prepare_compare.prepare(args.archive_dir)
    prepare_explanatory.prepare(args.archive_dir)
    with tempfile.TemporaryDirectory(prefix='manga-export-data-') as temp:
        scratch = Path(temp) / 'data'
        store = snapshot_store(args.snapshot_dir, scratch) if args.snapshot_dir else Store(scratch)
        receipt = export_store(store, args.output)
        receipt['input_mode'] = 'snapshot' if args.snapshot_dir else 'seed-preview'
        receipt['catalogue_sha256'] = hashlib.sha256((main.APP_DIR / 'catalog.json').read_bytes()).hexdigest()
        receipt_path = args.output.parent / 'build-report.json'
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({k: v for k, v in receipt.items() if k != 'images'}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    cli()
