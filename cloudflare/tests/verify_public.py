#!/usr/bin/env python3
"""Read back every exported API/image through a running local Wrangler Worker.

This verifier never deploys, authenticates, edits the catalogue, or invents data.
"""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'costlab-auth/manga'))
from app.catalogue import FACETS, GPT, catalogue_page


class PublicReader:
    """Feed the original Python filter actual exported public API projections."""
    def __init__(self, index, assets):
        self.records = {row['id']: row for row in index['records']}
        self.order = list(self.records)
        self.base = {nid: {'level': row['level']} for nid, row in self.records.items()}
        self.styles = {nid: json.loads((assets / '_data/styles' / (nid + '.json')).read_text(encoding='utf-8'))['ja'] for nid in self.order}

    def visible(self, nid):
        return nid in self.records

    def chain(self, nid):
        return self.records[nid]['chain']

    def path_titles(self, nid, lang):
        return [self.records[key]['labels'][lang]['title'] for key in self.chain(nid)]

    def shown(self, nid, field, lang):
        return self.records[nid]['labels'][lang][field]

    def style_prompt(self, nid):
        return self.styles[nid]['prompt']

    def expression(self, nid):
        return self.styles[nid]['expression']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8787')
    parser.add_argument('--workers', type=int, default=8)
    args = parser.parse_args()
    base = args.base_url.rstrip('/')
    assets = ROOT / 'dist/assets'
    receipt = json.loads((ROOT / 'dist/build-report.json').read_text(encoding='utf-8'))
    meta = json.loads((assets / '_data/routes.json').read_text(encoding='utf-8'))
    index = json.loads((assets / '_public/catalogue.json').read_text(encoding='utf-8'))
    if set(meta['visible']) != {row['id'] for row in index['records']}:
        raise RuntimeError('Catalogue route/index identity mismatch')
    actual_images = {'/' + p.relative_to(assets).as_posix() for p in (assets / 'files').rglob('*.jpg')}
    if actual_images != set(receipt['images']):
        raise RuntimeError('Exported image inventory differs from receipt')
    tasks = [('json', '/v1/models', json.loads((assets / '_data/models.json').read_text(encoding='utf-8')))]
    for lang in ('ja', 'en'):
        for model in ('gpt-image', 'anima-turbo'):
            tasks.append(('json', f'/v1/tree?lang={lang}&model={model}', json.loads((assets / f'_data/tree/{lang}-{model}.json').read_text(encoding='utf-8'))))
    for nid in meta['visible']:
        values = json.loads((assets / '_data/styles' / (nid + '.json')).read_text(encoding='utf-8'))
        for lang in ('ja', 'en'):
            tasks.append(('json', f'/v1/styles/{nid}?lang={lang}', values[lang]))
    tasks.extend(('image', path, record) for path, record in receipt['images'].items())
    def check(task):
        kind, path, expected = task
        with urllib.request.urlopen(base + path, timeout=45) as response:
            raw = response.read()
            if response.status != 200:
                raise RuntimeError(f'Unexpected HTTP status: {path}')
            if kind == 'image':
                if len(raw) != expected['bytes'] or hashlib.sha256(raw).hexdigest() != expected['sha256']:
                    raise RuntimeError(f'Image bytes/SHA mismatch: {path}')
                if response.headers.get_content_type() != 'image/jpeg':
                    raise RuntimeError(f'Image Content-Type mismatch: {path}')
            else:
                expected = json.loads(json.dumps(expected, ensure_ascii=False).replace('https://static.manga.invalid', base))
                if json.loads(raw) != expected or response.headers.get('Access-Control-Allow-Origin') != '*':
                    raise RuntimeError(f'API payload/CORS mismatch: {path}')
        return kind
    start = time.monotonic()
    counts = {'json': 0, 'image': 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(check, task) for task in tasks]
        try:
            for number, future in enumerate(concurrent.futures.as_completed(futures), 1):
                counts[future.result()] += 1
                if number % 1000 == 0:
                    print(f'HTTP readback: {number}/{len(tasks)} verified', flush=True)
        except BaseException:
            for future in futures:
                future.cancel()
            raise
    reader = PublicReader(index, assets)
    cases = []
    queries = [{}, {'page': '2'}, {'page': '9999'}, {'q': 'chibi'}, {'q': '細い 線'}, {'q': 'INK'},
               {'q': 'shonen-battle-chibi-comic'}, {'q': '  cute   INK  '}, {'q': 'nothing_matches_43b0'}]
    queries += [{'root': root, 'page': page} for root in meta['roots'] for page in ('1', '9999')]
    queries += [{'topic': topic} for topic in meta['topics']]
    queries += [{key: value} for key, options in FACETS.items() for value, _, _ in options]
    queries += [{'expression': 'mono', 'line': 'thin'}, {'expression': 'color', 'finish': 'lineonly'}]
    for lang in ('ja', 'en'):
        for query in queries:
            expected = catalogue_page(reader, model=GPT, lang=lang, root=query.get('root', ''), topic=query.get('topic', ''),
                                      q=query.get('q', '').strip()[:100], page=int(query.get('page', 1)),
                                      facets={key: query.get(key, '') for key in FACETS})
            cases.append({'lang': lang, 'query': urllib.parse.urlencode(query),
                          'expected': {key: expected[key] for key in ('ids', 'total', 'page', 'pages')}})
    directory = ROOT / 'dist/verification'
    directory.mkdir(exist_ok=True)
    fixture = directory / 'catalogue-parity-input.json'
    fixture.write_text(json.dumps(cases, ensure_ascii=False), encoding='utf-8')
    js = """import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import { selectPage } from './cloudflare/site/catalogue.mjs';
const index = JSON.parse(readFileSync('dist/assets/_public/catalogue.json', 'utf8'));
const cases = JSON.parse(readFileSync('dist/verification/catalogue-parity-input.json', 'utf8'));
for (const item of cases) {
 const actual = selectPage(index, new URLSearchParams(item.query), item.lang);
 for (const key of ['ids', 'total', 'page', 'pages']) assert.deepEqual(actual[key], item.expected[key], item.lang + ' ' + item.query + ' ' + key);
}
console.log('Original Python catalogue_page / browser filter parity:', cases.length, 'cases passed');
"""
    subprocess.run(['node', '--input-type=module', '-e', js], cwd=ROOT, check=True)
    report = {'api_responses_verified': counts['json'], 'jpeg_responses_sha256_verified': counts['image'],
              'visible_nodes': len(meta['visible']), 'filter_parity_cases': len(cases),
              'seconds': round(time.monotonic() - start, 3), 'base_url': base, 'passed': True}
    (directory / 'http-readback.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
