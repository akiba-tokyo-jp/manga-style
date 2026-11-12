#!/usr/bin/env python3
"""Verify the comparison pictures (the same prompt drawn by another image model) and stage them for deployment.

    python3 tools/manga_catalog/prepare_compare.py [--archive-dir DIR]

The pictures stay outside git: each bundle is a zip on a GitHub Release of this repository.
costlab-auth/manga/compare/records.json pins every bundle (SHA-256 and size) and every picture
(SHA-256, size, the SHA-256 of the English prompt it was drawn from, and the SHA-256 of the approved
catalogue sample it is compared with). Before anything enters the build context:

  * the archive and every picture must match the records;
  * the prompt must still be the English sample prompt of the branch's current approved sample, and the
    approved sample must still be the picture it was compared with. A branch whose words or sample changed
    since is NOT staged (printed as stale; make its comparison again or drop its record). It never blocks the
    catalogue: the comparison is not part of the style, and the site never shows a comparison drawn from
    words that no longer made the sample next to it.

Staging replaces costlab-auth/manga/compare/files/ (git-ignored) with <id>.jpg for every record.
prepare_samples.py runs this after the catalogue samples, so CI and every deployment path do the same.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_tree as bt  # noqa: E402

ROOT = HERE.parents[1]
COMPARE = ROOT / "costlab-auth/manga/compare"
RECORDS = COMPARE / "records.json"
DEST = COMPARE / "files"
MAX_ARCHIVE = 512 * 1024 * 1024
MAX_IMAGE = 4 * 1024 * 1024
SAMPLE_KEYS = {"sha256", "bytes", "prompt_sha256", "reference_sha256", "png_sha256", "native_job_id", "created_at"}


def text_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_records(records: dict, tree: dict, approved: dict) -> list[str]:
    """The records agree with themselves (no network). Returns the stale ids: records whose words or sample
    picture are no longer the branch's current ones."""
    if records.get("format") != 1:
        raise ValueError("unknown comparison records format")
    model, settings = records.get("model") or {}, records.get("settings") or {}
    if not model.get("id") or not model.get("version") or not model.get("name"):
        raise ValueError("comparison model is not named")
    if set(settings) != {"seed", "steps", "cfg_scale", "sampler", "size", "negative_prompt"}:
        raise ValueError("comparison settings are incomplete")
    in_bundles: dict[str, str] = {}
    for spec in records["bundles"]:
        if not spec["asset"].endswith(".zip") or "/" in spec["asset"] or not spec["tag"]:
            raise ValueError("invalid comparison bundle name")
        for nid in spec["nodes"]:
            if nid in in_bundles:
                raise ValueError(f"comparison picture in two bundles: {nid}")
            in_bundles[nid] = spec["asset"]
    nodes = {n["id"] for n in tree["nodes"]}
    stale = []
    for nid, rec in records["samples"].items():
        if not bt.ID_RE.fullmatch(nid) or nid not in nodes or nid not in approved:
            raise ValueError(f"comparison record for an unknown branch: {nid}")
        if set(rec) != SAMPLE_KEYS:
            raise ValueError(f"comparison record fields differ: {nid}")
        if nid not in in_bundles:
            raise ValueError(f"comparison record without a bundle: {nid}")
        if (rec["prompt_sha256"] != text_digest(bt.sample_prompt(tree, nid)["en"])
                or rec["reference_sha256"] != approved[nid]["sha256"]):
            stale.append(nid)
    return stale


def unpack(path: Path, spec: dict, records: dict, out: Path, skip: set[str] = frozenset()) -> list[str]:
    """Check one archive against the records and write the recorded pictures (except skip) into out/.
    Returns their ids."""
    if path.stat().st_size != spec["bytes"] or spec["bytes"] > MAX_ARCHIVE or file_digest(path) != spec["sha256"]:
        raise ValueError("comparison archive hash or size mismatch")
    expected = {nid + ".jpg" for nid in spec["nodes"]}
    staged = []
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        if len(entries) != len(expected) or {e.filename for e in entries} != expected:
            raise ValueError("unexpected or duplicate comparison archive paths")
        if any(stat.S_ISLNK(e.external_attr >> 16) or e.file_size > MAX_IMAGE for e in entries):
            raise ValueError("unsafe comparison archive entry")
        for nid in spec["nodes"]:
            rec = records["samples"].get(nid)
            if rec is None or nid in skip:  # dropped or stale: the archive keeps it, the site does not show it
                continue
            image = archive.read(nid + ".jpg")
            if (not image.startswith(b"\xff\xd8") or len(image) != rec["bytes"]
                    or hashlib.sha256(image).hexdigest() != rec["sha256"]):
                raise ValueError(f"comparison picture does not match its record: {nid}")
            target = out / (nid + ".jpg")
            target.write_bytes(image)
            target.chmod(0o644)
            staged.append(nid)
    return staged


def prepare(archive_dir: Path | None = None, records_file: Path = RECORDS, dest: Path = DEST) -> int:
    records = json.loads(records_file.read_text(encoding="utf-8"))
    stale = set(check_records(records, bt.build(), bt.approved_samples()))
    wanted = sorted(set(records["samples"]) - stale)
    work = dest.with_name(dest.name + ".new")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    work.chmod(0o755)  # Docker serves the pictures as uid 10002.
    staged: list[str] = []
    try:
        with tempfile.TemporaryDirectory(prefix="manga-compare-") as tmp:
            for spec in records["bundles"]:
                if not any(nid in records["samples"] and nid not in stale for nid in spec["nodes"]):
                    continue
                source = archive_dir or Path(tmp)
                if archive_dir is None:
                    subprocess.run(["gh", "release", "download", spec["tag"], "--repo", records["repository"],
                                    "--pattern", spec["asset"], "--dir", str(source), "--clobber"], check=True)
                staged += unpack(source / spec["asset"], spec, records, work, stale)
                if archive_dir is None:
                    (source / spec["asset"]).unlink()
        if sorted(staged) != wanted:
            raise ValueError("comparison pictures missing from their bundles")
        # Every bundle verified: replace the disposable staging directory.
        if dest.exists():
            shutil.rmtree(dest)
        work.rename(dest)
    finally:
        if work.exists():
            shutil.rmtree(work)
    print(f"verified and staged {len(staged)} comparison pictures")
    if stale:
        print(f"not staged, words or sample changed since (make again or drop): {len(stale)} "
              + " ".join(sorted(stale)[:20]))
    return len(staged)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--archive-dir", type=Path, help="use locally downloaded archives")
    args = parser.parse_args()
    prepare(args.archive_dir)
