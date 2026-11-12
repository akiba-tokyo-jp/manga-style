#!/usr/bin/env python3
"""Verify release sample bundles and stage them for the ordinary Docker deployment.

Images stay outside git. A pinned archive hash, per-image approval records and the
current generation prompts must all agree before anything enters the build context.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path

import build_tree as bt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEST = ROOT / "costlab-auth/manga/app/seed/additions"
REGISTRY = HERE / "sample_bundles.json"


def read_bundle(path: Path, spec: dict, tree: dict, approved: dict) -> tuple[list, dict]:
    raw = path.read_bytes()
    if len(raw) > 8 * 1024 * 1024 or hashlib.sha256(raw).hexdigest() != spec["sha256"]:
        raise ValueError("sample archive hash or size mismatch")
    ids = spec["nodes"]
    if len(set(ids)) != len(ids) or not all(bt.ID_RE.fullmatch(nid) for nid in ids):
        raise ValueError("invalid sample node list")
    expected = {"manifest.json", *(nid + ".jpg" for nid in ids)}
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if len(entries) != len(expected) or {e.filename for e in entries} != expected:
            raise ValueError("unexpected or duplicate archive paths")
        if any(stat.S_ISLNK(e.external_attr >> 16) or e.file_size > 4 * 1024 * 1024 for e in entries):
            raise ValueError("unsafe sample archive entry")
        files = {e.filename: archive.read(e) for e in entries}
    manifest = json.loads(files.pop("manifest.json"))
    if not isinstance(manifest, list) or len(manifest) != len(ids) or {i["id"] for i in manifest} != set(ids):
        raise ValueError("sample manifest nodes mismatch")
    for item in manifest:
        nid = item["id"]
        if item["file"] != nid + ".jpg":
            raise ValueError("sample filename mismatch")
        image = files[item["file"]]
        record = approved[nid]
        if (not image.startswith(b"\xff\xd8") or len(image) != record["bytes"]
                or hashlib.sha256(image).hexdigest() != record["sha256"]):
            raise ValueError("sample image does not match approval record")
        if (item["prompt"] != bt.sample_prompt(tree, nid)
                or bt.prompt_digest(item["prompt"]) != record["prompt_sha256"]
                or bt.prompt_digest(bt.style_prompt(tree, nid)) != record["style_prompt_sha256"]):
            raise ValueError("sample prompt does not match the current style")
        if (item["model"] != {"id": "chatgpt-image", "version": record["model_version"]}
                or item["created_at"] != record["created_at"]):
            raise ValueError("sample provenance does not match approval record")
    return manifest, files


def prepare(archive_dir: Path | None = None) -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    tree, approved = bt.build(), bt.approved_samples()
    manifest, images = [], {}
    with tempfile.TemporaryDirectory(prefix="manga-samples-") as tmp:
        download = Path(tmp)
        for spec in registry["bundles"]:
            source = archive_dir or download
            if archive_dir is None:
                encoded = []
                for tag in spec["release_bodies"]:
                    result = subprocess.run(
                        ["gh", "api", f"repos/{registry['repository']}/releases/tags/{tag}?bundle={spec['sha256']}"],
                        check=True, capture_output=True, text=True)
                    body = json.loads(result.stdout)["body"]
                    marker = "<!-- manga-samples-base64\n"
                    if body.count(marker) != 1 or not body.endswith("\n-->\n"):
                        raise ValueError("invalid encoded sample release")
                    encoded.append(body.partition(marker)[2].removesuffix("\n-->\n"))
                (source / spec["asset"]).write_bytes(base64.b64decode("".join(encoded), validate=True))
            items, files = read_bundle(source / spec["asset"], spec, tree, approved)
            # Each archive has its own manifest; combine verified records below.
            files = {name: raw for name, raw in files.items() if name != "manifest.json"}
            if images.keys() & files.keys():
                raise ValueError("duplicate samples across bundles")
            manifest.extend(items)
            images.update(files)
        # Verify every bundle before replacing the disposable staging directory.
        DEST.parent.mkdir(parents=True, exist_ok=True)
        if DEST.exists():
            shutil.rmtree(DEST)
        DEST.mkdir()
        DEST.chmod(0o755)  # Docker serves the public samples as uid 10002.
        for name, raw in images.items():
            file = DEST / name
            file.write_bytes(raw)
            file.chmod(0o644)
        manifest_file = DEST / "manifest.json"
        manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest_file.chmod(0o644)
    print(f"verified and staged {len(manifest)} manga samples")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-dir", type=Path, help="use locally downloaded archives")
    args = parser.parse_args()
    prepare(args.archive_dir)
    # 比較の絵（同じプロンプトを別のモデルで描いた絵）も、同じ道筋で検査して置く。
    import prepare_compare
    prepare_compare.prepare(args.archive_dir)
    import prepare_explanatory
    prepare_explanatory.prepare(args.archive_dir)
