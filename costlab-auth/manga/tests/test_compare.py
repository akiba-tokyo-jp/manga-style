"""Comparison pictures (the same sample prompt drawn by another image model, 2026-10-18).

What can go wrong without anyone noticing:
  * a comparison shown next to a sample it was not made against (the sample was replaced or reworded);
  * a comparison changing the style: version / samples / reference / model must stay as they were;
  * a picture served under a name the records do not give, or for a hidden branch;
  * prepare_compare.py staging a picture that differs from its record, or one made from other words.

    python -m unittest discover -s costlab-auth/manga/tests -p 'test_compare.py' -v
"""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(ROOT / "tools/manga_catalog"))

from fastapi.testclient import TestClient  # noqa: E402
from PIL import Image  # noqa: E402

import build_tree as bt  # noqa: E402
import prepare_compare as pc  # noqa: E402
from app import main  # noqa: E402
from app.store import Store  # noqa: E402

ORIGIN = "https://manga.akiba.tokyo.jp"
NID = "shonen-battle-bold-black"
SETTINGS = {"seed": 20261018, "steps": 20, "cfg_scale": 5, "sampler": "euler_a", "size": "768x1024",
            "negative_prompt": None}
MODEL = {"id": "wai-illustrious-sdxl-v17.0", "version": "v17.0", "name": "WAI-Illustrious-SDXL"}


def jpeg(color=(40, 120, 200)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (768, 1024), color).save(buf, "JPEG", quality=85)
    return buf.getvalue()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="manga-compare-"))
        seeds = self.tmp / "seeds"
        seeds.mkdir()
        for item in (HERE.parent / "app/seed").iterdir():
            if item.is_file():
                shutil.copy2(item, seeds / item.name)
        self.compare = self.tmp / "compare"
        (self.compare / "files").mkdir(parents=True)
        self.store = Store(self.tmp / "data", seed_dir=seeds, compare_dir=self.tmp / "none")
        self.before = self.store.effective(NID)
        sample = self.store.state["nodes"][NID]["sample"]
        self.picture = jpeg()
        (self.compare / "files" / f"{NID}.jpg").write_bytes(self.picture)
        records = {"format": 1, "repository": "x/y", "model": MODEL, "settings": SETTINGS, "bundles": [],
                   "samples": {NID: {"sha256": digest(self.picture), "bytes": len(self.picture),
                                     "prompt_sha256": digest(sample["prompt"]["en"].encode("utf-8")),
                                     "reference_sha256": sample["sha256"], "png_sha256": "0" * 64,
                                     "native_job_id": "job", "created_at": "2026-10-18T03:34:52Z"}}}
        (self.compare / "records.json").write_text(json.dumps(records), encoding="utf-8")
        main.DATA_DIR = str(self.tmp / "data")
        main._store = Store(self.tmp / "data", seed_dir=seeds, compare_dir=self.compare)
        self.client = TestClient(main.app, base_url=ORIGIN)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        main._store = None
        shutil.rmtree(self.tmp, ignore_errors=True)

    def comparison_url(self) -> str:
        items = self.client.get(f"/v1/styles/{NID}").json()["comparisons"]
        self.assertEqual(len(items), 1)
        return items[0]["url"]

    def test_api_page_and_picture(self):
        body = self.client.get(f"/v1/styles/{NID}").json()
        cmp = body["comparisons"][0]
        self.assertEqual(cmp["model"], MODEL)
        self.assertEqual(cmp["settings"], SETTINGS)
        self.assertEqual(cmp["prompt_from"], "samples[0].prompt.en")
        self.assertEqual(cmp["created_at"], "2026-10-18T03:34:52Z")
        self.assertRegex(cmp["url"], rf"^{ORIGIN}/files/{NID}/compare-wai-illustrious-sdxl-v17-0-[0-9a-f]{{12}}\.jpg$")
        img = self.client.get(cmp["url"].replace(ORIGIN, ""))
        self.assertEqual((img.status_code, img.headers["content-type"]), (200, "image/jpeg"))
        self.assertEqual(img.content, self.picture)
        for lang, words in (("ja", "WAI-Illustrious-SDXL（同じプロンプト・v17.0）"), ("en", "WAI-Illustrious-SDXL (same prompt, v17.0)")):
            html = self.client.get(f"/n/{NID}?lang={lang}").text
            self.assertIn('class="legacy-comparison"', html)
            self.assertIn('class="node has-sample"', html)
            self.assertIn(words, html)
            self.assertIn(cmp["url"].replace(ORIGIN, ""), html)
            self.assertIn("seed 20261018", html)
        self.assertEqual(self.client.get("/healthz").json()["comparisons"], 1)

    def test_the_style_itself_does_not_change(self):
        body = self.client.get(f"/v1/styles/{NID}").json()
        self.assertEqual(main.store().effective(NID), self.before)
        self.assertEqual(body["version"], self.before["version"])
        self.assertEqual(len(body["samples"]), 1)
        self.assertEqual(body["reference"], 0)
        self.assertNotIn("wai", json.dumps(body["samples"]))
        self.assertNotIn("wai", json.dumps(body["model"]))

    def test_branch_without_comparison(self):
        self.assertEqual(self.client.get("/v1/styles/shonen").json()["comparisons"], [])
        self.assertNotIn('class="legacy-comparison"', self.client.get("/n/shojo-magical-shojo-classic?lang=ja").text)

    def test_replaced_sample_hides_the_old_comparison(self):
        url = self.comparison_url().replace(ORIGIN, "")
        sample = main.store().state["nodes"][NID]["sample"]
        main.store().put_sample(NID, jpeg((200, 200, 200)), prompt=sample["prompt"])  # same words, new picture
        self.assertEqual(self.client.get(f"/v1/styles/{NID}").json()["comparisons"], [])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertNotIn('class="legacy-comparison"', self.client.get(f"/n/{NID}?lang=ja").text)

    def test_reworded_sample_hides_the_old_comparison(self):
        s = main.store()
        sample = s.state["nodes"][NID]["sample"]
        s.put_sample(NID, jpeg(), prompt={"ja": sample["prompt"]["ja"], "en": sample["prompt"]["en"] + " changed"})
        s.compare[NID]["reference_sha256"] = s.state["nodes"][NID]["sample"]["sha256"]
        self.assertEqual(self.client.get(f"/v1/styles/{NID}").json()["comparisons"], [])

    def test_hidden_branch_and_other_names(self):
        url = self.comparison_url().replace(ORIGIN, "")
        self.assertEqual(self.client.get(url.replace("compare-wai", "compare-gpt")).status_code, 404)
        self.assertEqual(self.client.get(f"/files/shonen/{url.rsplit('/', 1)[1]}").status_code, 404)
        self.assertEqual(self.client.get(f"/files/{NID}/{NID}.jpg").status_code, 404)
        main.store().set_published(NID, False)
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_missing_or_short_file_is_not_shown(self):
        path = self.compare / "files" / f"{NID}.jpg"
        path.write_bytes(self.picture[:-10])
        main._store = Store(self.tmp / "data", compare_dir=self.compare)
        self.assertEqual(self.client.get(f"/v1/styles/{NID}").json()["comparisons"], [])
        path.unlink()
        main._store = Store(self.tmp / "data", compare_dir=self.compare)
        self.assertEqual(self.client.get(f"/v1/styles/{NID}").json()["comparisons"], [])

    def test_no_records_file(self):
        main._store = Store(self.tmp / "data", compare_dir=self.tmp / "nothing")
        self.assertEqual(self.client.get(f"/v1/styles/{NID}").json()["comparisons"], [])


class PrepareTests(unittest.TestCase):
    """prepare_compare.py against the real catalogue (no network: --archive-dir)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="manga-compare-prep-"))
        self.tree, self.approved = bt.build(), bt.approved_samples()
        self.ids = ["shonen", "shojo"]
        self.pictures = {nid: jpeg((i * 50, 90, 140)) for i, nid in enumerate(self.ids)}

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def build(self, pictures=None, extra=None, prompt_of=None) -> tuple[Path, Path]:
        pictures = pictures or self.pictures
        archive = self.tmp / "b.zip"
        with zipfile.ZipFile(archive, "w") as z:
            for nid, data in pictures.items():
                z.writestr(nid + ".jpg", data)
            for name, data in (extra or {}).items():
                z.writestr(name, data)
        raw = archive.read_bytes()
        samples = {nid: {"sha256": digest(self.pictures[nid]), "bytes": len(self.pictures[nid]),
                         "prompt_sha256": digest(bt.sample_prompt(self.tree, (prompt_of or {}).get(nid, nid))["en"].encode()),
                         "reference_sha256": self.approved[nid]["sha256"], "png_sha256": "0" * 64,
                         "native_job_id": "j", "created_at": "2026-10-18T03:34:52Z"} for nid in self.ids}
        records = {"format": 1, "repository": "x/y", "model": MODEL, "settings": SETTINGS,
                   "bundles": [{"tag": "t", "asset": "b.zip", "sha256": digest(raw), "bytes": len(raw), "nodes": self.ids}],
                   "samples": samples}
        rec = self.tmp / "records.json"
        rec.write_text(json.dumps(records), encoding="utf-8")
        return rec, self.tmp / "files"

    def test_stages_verified_pictures(self):
        rec, dest = self.build()
        self.assertEqual(pc.prepare(self.tmp, rec, dest), 2)
        self.assertEqual({p.name for p in dest.iterdir()}, {"shonen.jpg", "shojo.jpg"})
        self.assertEqual((dest / "shojo.jpg").read_bytes(), self.pictures["shojo"])

    def test_refuses_a_changed_picture_and_keeps_the_old_staging(self):
        rec, dest = self.build()
        pc.prepare(self.tmp, rec, dest)
        flipped = bytearray(self.pictures["shojo"])
        flipped[len(flipped) // 2] ^= 0xFF  # same length, other bytes
        bad = dict(self.pictures, shojo=bytes(flipped))
        records = json.loads(rec.read_text(encoding="utf-8"))
        rec2, _ = self.build(pictures=bad)
        fixed = json.loads(rec2.read_text(encoding="utf-8"))
        fixed["samples"] = records["samples"]  # records still pin the original picture
        rec2.write_text(json.dumps(fixed), encoding="utf-8")
        with self.assertRaises(ValueError):
            pc.prepare(self.tmp, rec2, dest)
        self.assertEqual((dest / "shojo.jpg").read_bytes(), self.pictures["shojo"])

    def test_does_not_stage_other_words(self):
        # A reworded branch must not block the catalogue: its comparison is left out, the rest is staged.
        rec, dest = self.build(prompt_of={"shojo": "shonen"})
        self.assertEqual(pc.prepare(self.tmp, rec, dest), 1)
        self.assertEqual({p.name for p in dest.iterdir()}, {"shonen.jpg"})

    def test_does_not_stage_another_reference(self):
        rec, dest = self.build()
        records = json.loads(rec.read_text(encoding="utf-8"))
        records["samples"]["shojo"]["reference_sha256"] = self.approved["shonen"]["sha256"]
        rec.write_text(json.dumps(records), encoding="utf-8")
        self.assertEqual(pc.prepare(self.tmp, rec, dest), 1)
        self.assertFalse((dest / "shojo.jpg").exists())

    def test_refuses_an_unexpected_archive_entry_or_archive_hash(self):
        rec, dest = self.build(extra={"../evil.jpg": b"x"})
        with self.assertRaises(ValueError):
            pc.prepare(self.tmp, rec, dest)
        rec, dest = self.build()
        records = json.loads(rec.read_text(encoding="utf-8"))
        records["bundles"][0]["sha256"] = "0" * 64
        rec.write_text(json.dumps(records), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "archive hash"):
            pc.prepare(self.tmp, rec, dest)

    def test_real_records_agree_with_the_catalogue(self):
        records = json.loads(pc.RECORDS.read_text(encoding="utf-8"))
        stale = pc.check_records(records, self.tree, self.approved)
        if stale:
            print(f"stale comparisons (not shown until made again): {stale[:20]}")
        self.assertEqual(records["model"], MODEL)
        self.assertEqual(records["settings"], SETTINGS)


class WiringTests(unittest.TestCase):
    def test_every_deployment_path_stages_comparisons(self):
        src = (ROOT / "tools/manga_catalog/prepare_samples.py").read_text(encoding="utf-8")
        self.assertIn("prepare_compare.prepare(args.archive_dir)", src)
        docker = (HERE.parent / "Dockerfile").read_text(encoding="utf-8")
        self.assertLess(docker.index("COPY compare/ ./compare/"), docker.index("COPY app/ ./app/"))
        self.assertIn("!compare/", (HERE.parent / ".dockerignore").read_text(encoding="utf-8"))
        self.assertIn('health["comparisons"] == len(records["samples"])', (ROOT / ".github/workflows/manga-style-validate.yml").read_text(encoding="utf-8"))
        workflow = (ROOT / ".github/workflows/manga-style-validate.yml").read_text(encoding="utf-8")
        self.assertEqual(workflow.count("-p 'test_compare.py'"), 1)


if __name__ == "__main__":
    unittest.main()
