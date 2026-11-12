"""Bundle verification: corruption and stale prompts must stop deployment."""
import copy
import hashlib
import json
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from pathlib import Path

import build_tree as bt
from prepare_samples import read_bundle
import prepare_samples as bundles


class BundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = bt.build()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "samples.zip"
        self.nid = "gag-surreal-dot-contours"
        self.image = b"\xff\xd8test-image"
        prompt = bt.sample_prompt(self.tree, self.nid)
        self.manifest = [{"id": self.nid, "file": self.nid + ".jpg", "prompt": prompt,
                          "model": {"id": "chatgpt-image", "version": "test"}, "created_at": "2026-09-30T00:00:00Z"}]
        self.approved = {self.nid: {"sha256": hashlib.sha256(self.image).hexdigest(), "bytes": len(self.image),
                                  "prompt_sha256": bt.prompt_digest(prompt),
                                  "style_prompt_sha256": bt.prompt_digest(bt.style_prompt(self.tree, self.nid)),
                                  "model_version": "test", "created_at": self.manifest[0]["created_at"]}}

    def tearDown(self):
        self.tmp.cleanup()

    def archive(self, extra=None, image=None, manifest=None):
        with zipfile.ZipFile(self.path, "w") as archive:
            archive.writestr("manifest.json", json.dumps(manifest or self.manifest))
            archive.writestr(self.nid + ".jpg", self.image if image is None else image)
            if extra:
                archive.writestr(extra, b"unexpected")
        return {"sha256": hashlib.sha256(self.path.read_bytes()).hexdigest(), "nodes": [self.nid]}

    def test_valid_bundle(self):
        manifest, files = read_bundle(self.path, self.archive(), self.tree, self.approved)
        self.assertEqual(manifest, self.manifest)
        self.assertEqual(files[self.nid + ".jpg"], self.image)

    def test_prepare_combines_two_bundle_manifests(self):
        first = self.archive()
        second_id = "josei-drama-tone-shapes"
        second_path = Path(self.tmp.name) / "second.zip"
        item = copy.deepcopy(self.manifest[0])
        item.update(id=second_id, file=second_id + ".jpg", prompt=bt.sample_prompt(self.tree, second_id))
        record = {**self.approved[self.nid], "prompt_sha256": bt.prompt_digest(item["prompt"]),
                  "style_prompt_sha256": bt.prompt_digest(bt.style_prompt(self.tree, second_id))}
        with zipfile.ZipFile(second_path, "w") as archive:
            archive.writestr("manifest.json", json.dumps([item]))
            archive.writestr(item["file"], self.image)
        second = {"asset": second_path.name, "nodes": [second_id],
                  "sha256": hashlib.sha256(second_path.read_bytes()).hexdigest()}
        registry = Path(self.tmp.name) / "registry.json"
        registry.write_text(json.dumps({"bundles": [{**first, "asset": self.path.name}, second]}))
        dest = Path(self.tmp.name) / "staged"
        with patch.object(bundles, "REGISTRY", registry), patch.object(bundles, "DEST", dest), \
                patch.object(bt, "approved_samples", return_value={**self.approved, second_id: record}):
            bundles.prepare(Path(self.tmp.name))
        self.assertEqual(json.loads((dest / "manifest.json").read_text()), self.manifest + [item])
        self.assertEqual((dest / (self.nid + ".jpg")).read_bytes(), self.image)
        self.assertEqual((dest / item["file"]).read_bytes(), self.image)

    def test_archive_corruption_stops_import(self):
        spec = self.archive()
        self.path.write_bytes(self.path.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "archive hash"):
            read_bundle(self.path, spec, self.tree, self.approved)

    def test_traversal_stops_import_even_with_matching_archive_hash(self):
        spec = self.archive(extra="../outside.jpg")
        with self.assertRaisesRegex(ValueError, "archive paths"):
            read_bundle(self.path, spec, self.tree, self.approved)

    def test_image_change_without_approval_stops_import(self):
        spec = self.archive(image=self.image + b"changed")
        with self.assertRaisesRegex(ValueError, "image does not match"):
            read_bundle(self.path, spec, self.tree, self.approved)

    def test_stale_prompt_stops_import(self):
        manifest = copy.deepcopy(self.manifest)
        manifest[0]["prompt"]["en"] += " extra lines"
        spec = self.archive(manifest=manifest)
        with self.assertRaisesRegex(ValueError, "prompt does not match"):
            read_bundle(self.path, spec, self.tree, self.approved)


if __name__ == "__main__":
    unittest.main()
