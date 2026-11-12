"""Portable build-only private GitHub Release retrieval; no gh binary required."""
import base64
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPOSITORY = 'akiba-tokyo-jp/manga-style'
ID = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
MAX_ARCHIVE = 64 * 1024 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def github_bytes(path, token, *, binary=False):
    """Only api.github.com receives credentials; signed storage redirects never do."""
    request = urllib.request.Request('https://api.github.com/' + path, headers={
        'Authorization': 'Bearer ' + token, 'User-Agent': 'manga-style-static-build',
        'Accept': 'application/octet-stream' if binary else 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    })
    limit = MAX_ARCHIVE if binary else 2 * 1024 * 1024
    opener = urllib.request.build_opener(NoRedirect)
    try:
        response = opener.open(request, timeout=120)
    except urllib.error.HTTPError as exc:
        if not binary or exc.code not in (301, 302, 303, 307, 308):
            raise RuntimeError(f'GitHub Release read failed (HTTP {exc.code})') from None
        target = urllib.parse.urlsplit(exc.headers.get('Location', ''))
        exc.close()
        if (target.scheme != 'https' or not target.hostname or not target.hostname.endswith('.githubusercontent.com')
                or target.username or target.password or target.port not in (None, 443)):
            raise ValueError('Unexpected Release storage redirect')
        # Use a fresh unauthenticated request, with redirects still disabled.
        response = opener.open(urllib.request.Request(target.geturl(), headers={'User-Agent': 'manga-style-static-build'}), timeout=120)
    with response:
        raw = response.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('Release response exceeds build limit')
    return raw


def bundle_specs():
    specs = []
    for name in ('tools/manga_catalog/sample_bundles.json', 'tools/manga_catalog/explanatory_bundles.json',
                 'costlab-auth/manga/compare/records.json'):
        registry = json.loads((ROOT / name).read_text(encoding='utf-8'))
        if registry.get('repository') != REPOSITORY:
            raise ValueError('Unexpected Release repository')
        specs.extend(registry['bundles'])
    return specs


def fetch_archives(directory, *, specs=None, token=None):
    directory = Path(directory)
    specs = bundle_specs() if specs is None else specs
    names = set()
    for spec in specs:
        if (not re.fullmatch(r'[a-z0-9][a-z0-9.-]*\.zip', spec.get('asset', ''))
                or not re.fullmatch(r'[0-9a-f]{64}', spec.get('sha256', '')) or spec['asset'] in names):
            raise ValueError('Invalid or duplicate pinned archive')
        names.add(spec['asset'])
        tags = spec.get('release_bodies') or [spec.get('release_tag') or spec.get('tag')]
        if not all(isinstance(tag, str) and ID.fullmatch(tag) for tag in tags):
            raise ValueError('Invalid pinned Release tag')
    missing = []
    for spec in specs:
        path = directory / spec['asset']
        if path.exists():
            if path.is_symlink() or path.stat().st_size > MAX_ARCHIVE or hashlib.sha256(path.read_bytes()).hexdigest() != spec['sha256']:
                raise ValueError('Cached archive SHA mismatch: ' + spec['asset'])
        else:
            missing.append(spec)
    if not missing:
        return
    if token is None:
        token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if not token and shutil.which('gh'):
            result = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True)
            token = result.stdout.strip()
    if not token:
        raise ValueError('Missing private Release access: set GH_TOKEN as a build secret (Contents: read)')
    directory.mkdir(parents=True, exist_ok=True)
    def download(spec):
        if spec.get('release_bodies'):
            marker = '<!-- manga-explanatory-base64\n' if spec['asset'].startswith('manga-explanatory-') else '<!-- manga-samples-base64\n'
            encoded = []
            for tag in spec['release_bodies']:
                body = json.loads(github_bytes(f'repos/{REPOSITORY}/releases/tags/{tag}', token))['body']
                if not isinstance(body, str) or body.count(marker) != 1 or not body.endswith('\n-->\n'):
                    raise ValueError('Invalid legacy Release body')
                encoded.append(body.partition(marker)[2].removesuffix('\n-->\n'))
                if sum(map(len, encoded)) > MAX_ARCHIVE * 2:
                    raise ValueError('Legacy Release exceeds build limit')
            raw = base64.b64decode(''.join(encoded), validate=True)
        else:
            tag = spec.get('release_tag') or spec['tag']
            release = json.loads(github_bytes(f'repos/{REPOSITORY}/releases/tags/{tag}', token))
            matches = [a for a in release['assets'] if a['name'] == spec['asset'] and a['state'] == 'uploaded']
            if len(matches) != 1 or type(matches[0]['id']) is not int:
                raise ValueError('Missing or ambiguous pinned Release asset')
            raw = github_bytes(f"repos/{REPOSITORY}/releases/assets/{matches[0]['id']}", token, binary=True)
        if len(raw) > MAX_ARCHIVE or hashlib.sha256(raw).hexdigest() != spec['sha256']:
            raise ValueError('Downloaded archive SHA mismatch: ' + spec['asset'])
        target = directory / spec['asset']
        temporary = target.with_suffix('.download')
        temporary.write_bytes(raw)
        temporary.replace(target)
        print('Verified Release archive:', spec['asset'], flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        list(executor.map(download, missing))
