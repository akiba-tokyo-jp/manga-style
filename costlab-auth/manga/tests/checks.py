"""Checks for the manga style catalogue (costlab-auth/manga). No network, no Docker.

    cd costlab-auth/manga && python -m unittest discover -s tests -v

What they protect (the ways this site can go wrong without anyone noticing):
  * the Genko API shape and its fixed values (license, avoid, CORS GET only);
  * hidden branches leaking through the pages, the API or the image files;
  * the admin being reachable without a costlab-auth session, or by a cross-site POST;
  * the language switches (screen and prompt) silently showing the other language;
  * versions not going up when a sample or the words change;
  * the prompt composition the owner approved (2026-09-27): level 2 and below never carry the level-1
    words, level-3 samples start from a scene of their own level-2 branch (not the level-2 sample), and
    the tree still rebuilds the exact prompt of every approved sample (all 2,734 branches).
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from fastapi.testclient import TestClient  # noqa: E402
from PIL import Image  # noqa: E402

from app import main  # noqa: E402
from app.store import Store  # noqa: E402

ORIGIN = "https://manga.akiba.tokyo.jp"
SAMPLED = ("shonen-battle-bold-black", "shojo-magical-shojo-classic")
COLOR_ADDITIONS = {
    'josei-love-color-gradation', 'josei-romance-color-gradation',
    'shonen-romcom-color-gradation', 'seinen-action-color-gradation',
    'josei-yuri-spot-accent',
    'kodomo-geometric-paper-collage', 'gag-hetauma-color-crayon',
    'seinen-penscape-color-wash', 'kodomo-animal-textile-relief',
    'yonkoma-mochi-clay-relief',
    'yonkoma-mochi-flat-color', 'essay-parenting-flat-color',
    'kodomo-geometric-flat-color', 'gag-retro-flat-color',
    'josei-office-flat-color', 'josei-comedy-flat-color', 'seinen-profession-flat-color',
    'seinen-profession-volumetric-color', 'seinen-plainreal-volumetric-color',
}
SHAPE_ADDITIONS = ("josei-drama-tone-shapes", "gag-retro-flat-bands", "seinen-profession-ring-irises")
ADDITIONS = ("gag-surreal-dot-contours", "gekiga-samurai-graphite-dark", "seinen-daily-graphite-light") + SHAPE_ADDITIONS
REPAIRS = {
    'shonen-sports-muscle-mass', 'shonen-carved-engraving',
    'josei-office-doodle-casual', 'josei-office-natural-quiet', 'josei-office-pencil-soft',
    'josei-family-doodle-casual', 'josei-love', 'josei-love-modern-flat', 'josei-love-rough-light',
    'josei-drama', 'josei-drama-ink-bleed', 'josei-period-ukiyoe-flat', 'josei-period-kirie',
    'josei-period-inkwash-quiet', 'josei-comedy-doodle-casual', 'kodomo-animal-kirie',
    'gag', 'gag-surreal-dot-contours', 'gag-deadpan-modern-town', 'horror-kaidan',
    'horror-folk-kirie', 'horror-school', 'horror-urban-kagee', 'horror-panic-crack-debris',
    'essay', 'essay-diary-gentle-soft', 'essay-travel-kirie',
    'gekiga-historical-hikime-yamato', 'gekiga-adventure-ligne-claire',
}


def staged_pairs():
    folder = HERE.parent/'app/seed/pairs'
    manifests = list(folder.glob('*/manifest.json'))
    if (folder/'manifest.json').exists():
        manifests.append(folder/'manifest.json')
    return [pair for manifest in manifests for pair in json.loads(manifest.read_text())]


def staged_additions():
    manifest = HERE.parent / "app/seed/additions/manifest.json"
    return json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else []


class VerifyServer:
    """Stands in for costlab-auth /__auth/verify: answers with self.status and records the requests."""

    def __init__(self):
        self.status = 303
        self.seen = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802
                outer.seen.append({"path": self.path, "cookie": self.headers.get("Cookie", "")})
                self.send_response(outer.status)
                if outer.status == 303:
                    self.send_header("Location", "/__auth/login?next=/admin")
                self.send_header("Content-Length", "0")
                self.end_headers()

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}/__auth/verify"

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def png_bytes(size=(900, 1200), color=(200, 30, 30)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, "PNG")
    return buf.getvalue()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="manga-checks-")
        main.DATA_DIR = self.tmp
        main._store = None
        # 一般API・権限の試験は従来の2見本で隔離。全34追加画像の取り込みは
        # 専用のAPI試験とStoreTestsで実行し、43回の再取り込みを避ける。
        if self._testMethodName != 'test_addition_samples_match_images_and_recorded_prompts':
            seeds = Path(self.tmp) / 'fixture-seeds'
            seeds.mkdir()
            source = HERE.parent / 'app' / 'seed'
            for item in source.iterdir():
                if item.is_file():
                    shutil.copy2(item, seeds / item.name)
            main._store = Store(self.tmp, seed_dir=seeds)
        self.verify = VerifyServer()
        main.ADMIN_VERIFY_URL = self.verify.url
        self.client = TestClient(main.app, base_url=ORIGIN)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.verify.close()
        main._store = None
        shutil.rmtree(self.tmp, ignore_errors=True)

    def admin_post(self, path, data=None, files=None, origin=ORIGIN):
        headers = {"Origin": origin, "Cookie": "costlab_session=ok"} if origin else {"Cookie": "costlab_session=ok"}
        return self.client.post(path, data=data or {}, files=files, headers=headers, follow_redirects=False)

    def login(self):
        self.verify.status = 204


class ApiTests(Base):
    def test_tree_shape_and_cors(self):
        r = self.client.get("/v1/tree", headers={"Origin": "https://example.org"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers["access-control-allow-origin"], "*")
        self.assertEqual(r.headers["access-control-allow-methods"], "GET")
        body = r.json()
        self.assertEqual(body["version"], 1)
        self.assertEqual(len(body["nodes"]), 2756)
        first = body["nodes"][0]
        self.assertEqual(set(first), {"id", "parent", "level", "title", "summary", "thumbnail_url", "path"})
        self.assertEqual((first["id"], first["parent"], first["level"], first["title"]), ("shonen", None, 1, "少年漫画"))
        self.assertTrue(first["thumbnail_url"].startswith(ORIGIN + "/files/"))
        levels = {n["level"] for n in body["nodes"]}
        self.assertEqual(levels, {1, 2, 3})
        # 2026-09-28（Genko 側の依頼）: 各ノードに、1段目からその枝までの題名の並び。最後がその枝。
        by_id = {n["id"]: n for n in body["nodes"]}
        self.assertEqual(by_id["shonen"]["path"], ["少年漫画"])
        self.assertEqual(by_id["gag-surreal-doodle-casual"]["path"], ["ギャグ漫画", "シュール", "ゆるい手描きの落書き風"])
        for n in body["nodes"]:
            self.assertEqual(len(n["path"]), n["level"], n["id"])
            self.assertEqual(n["path"][-1], n["title"], n["id"])
            if n["parent"]:
                self.assertEqual(n["path"][:-1], by_id[n["parent"]]["path"], n["id"])
        en = {n["id"]: n for n in self.client.get("/v1/tree?lang=en").json()["nodes"]}
        self.assertEqual(en["gag-surreal-doodle-casual"]["path"][:2], ["Gag manga", "Surreal"])

    def test_style_contract(self):
        r = self.client.get("/v1/styles/shonen-battle-bold-black")
        self.assertEqual(r.status_code, 200)
        b = r.json()
        self.assertEqual(list(b), ["id", "path", "level", "title", "summary", "expression", "model", "prompt", "avoid",
                                   "samples", "reference", "license", "version", "updated_at", "children",
                                   "comparisons"])
        self.assertEqual(b["children"], [], "a level-3 style has no children")
        # path: the levels above, from level 1 down to the parent (2026-09-28, Genko's request)
        self.assertEqual([p["id"] for p in b["path"]], ["shonen", "shonen-battle"])
        self.assertEqual(self.client.get("/v1/styles/shonen").json()["path"], [], "level 1 has an empty path")
        g = self.client.get("/v1/styles/gag-surreal-doodle-casual").json()
        self.assertEqual(g["path"], [{"id": "gag", "title": "ギャグ漫画"}, {"id": "gag-surreal", "title": "シュール"}])
        self.assertEqual(g["title"], "ゆるい手描きの落書き風")
        self.assertEqual(b["level"], 3)
        self.assertEqual(b["expression"], "mono")
        self.assertEqual(b["model"], {"id": "chatgpt-image", "version": "gpt-image-2.5-sunburst"})
        self.assertEqual(b["avoid"], ["文字", "フキダシ", "効果音の描き文字", "コマ枠", "署名", "透かし", "色"])
        self.assertIs(b["license"]["generated"], True)
        self.assertIs(b["license"]["artist_names"], False)
        self.assertEqual(set(b["prompt"]), {"ja", "en", "tags"})
        self.assertNotIn("題材", b["prompt"]["ja"], "the style prompt must not contain the subject")
        self.assertEqual(len(b["samples"]), 1)
        s = b["samples"][0]
        self.assertEqual(s["subject"], "upper_body")
        self.assertIn("題材", s["prompt"]["ja"])
        self.assertTrue(s["url"].startswith(ORIGIN + "/files/shonen-battle-bold-black/"))
        self.assertEqual(b["reference"], 0)
        self.assertEqual(b["version"], 1)
        self.assertRegex(b["updated_at"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        img = self.client.get(s["url"].replace(ORIGIN, ""))
        self.assertEqual(img.status_code, 200)
        self.assertEqual(img.headers["content-type"], "image/jpeg")
        self.assertLessEqual(len(img.content), 20 * 1024 * 1024)
        self.assertEqual(Image.open(io.BytesIO(img.content)).mode, "L")

    def test_seed_sample_keeps_the_prompt_that_made_it(self):
        # The two level-3 trial pictures were made before the approved level-1/2 words; the API must keep
        # reporting the prompt that really made them, not a prompt rebuilt from today's tree.
        seeds = json.loads((HERE.parent / "app" / "seed" / "manifest.json").read_text(encoding="utf-8"))
        for item in seeds:
            api = self.client.get(f"/v1/styles/{item['id']}").json()
            self.assertEqual(api["samples"][0]["prompt"], item["prompt"])

    def test_tree_rebuilds_every_approved_sample_prompt(self):
        # A prompt never changes without its picture: both the sample prompt and the API prompt of every
        # branch must be exactly the ones recorded with its picture.
        s = main.store()
        self.assertEqual(set(s.approved), set(s.order), "every branch has an approved sample")

        def digest(p):
            return hashlib.sha256(json.dumps(p, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()

        for nid, a in s.approved.items():
            self.assertEqual(digest(s.generation_prompt(nid)), a["prompt_sha256"],
                             f"{nid}: the words changed under an approved sample")
            self.assertEqual(digest(s.style_prompt(nid)), a["style_prompt_sha256"],
                             f"{nid}: the API prompt changed without a new picture")

    def test_new_media_are_scoped_and_redraws_discard_parent_detail(self):
        s = main.store()
        scoped = {nid for nid in s.order if "medium" in s.base[nid]}
        self.assertEqual(scoped, set(ADDITIONS) | REPAIRS | COLOR_ADDITIONS)
        self.assertEqual({nid for nid in scoped if s.base[nid]['medium'].startswith('repair-')}, REPAIRS)
        for nid in s.order:
            if nid not in scoped:
                self.assertTrue(s.style_prompt(nid)["en"].startswith(s.common["en"]), nid)
        for nid in set(ADDITIONS) - REPAIRS:
            parent = s.base[nid]["parent"]
            medium = s.media[s.base[nid]["medium"]]
            self.assertTrue(s.style_prompt(nid)["en"].startswith(medium["common"]["en"]))
            if nid in SHAPE_ADDITIONS:
                self.assertIn("blank white", s.style_prompt(nid)["en"])
            else:
                self.assertIn("extremely sparse", s.style_prompt(nid)["en"])
            steps = s.generation_steps(nid)
            self.assertTrue(steps[0]["en"].startswith(s.common["en"]))
            self.assertIn(s.words(parent)["en"], steps[0]["en"])
            self.assertNotIn(s.words(parent)["en"], steps[1]["en"])
            self.assertIn(s.words(nid)["en"], steps[1]["en"])

    def test_addition_samples_match_images_and_recorded_prompts(self):
        for item in staged_additions():
            nid = item["id"]
            api = self.client.get(f"/v1/styles/{nid}").json()
            self.assertEqual(len(api["samples"]), 1)
            sample = api["samples"][0]
            self.assertEqual(sample["prompt"], item["prompt"])
            self.assertEqual(api["model"], item["model"])
            raw = self.client.get(sample["url"].replace(ORIGIN, "")).content
            self.assertEqual(hashlib.sha256(raw).hexdigest(), main.store().approved[nid]["sha256"])
            im = Image.open(io.BytesIO(raw))
            expected_color = nid in COLOR_ADDITIONS
            self.assertEqual(api["expression"], "color" if expected_color else "mono")
            self.assertEqual((im.mode, im.size), ("RGB" if expected_color else "L", (768, 1024)))

    def test_prompt_composition_by_level(self):
        s = main.store()
        l1 = s.base["shonen"]["words"]
        l2 = s.base["shonen-battle"]["words"]
        l3 = s.base["shonen-battle-bold-black"]["words"]
        p1 = self.client.get("/v1/styles/shonen").json()["prompt"]
        self.assertTrue(p1["ja"].startswith(s.common["ja"]))
        self.assertIn(l1["ja"], p1["ja"])
        for nid, own in (("shonen-battle", (l2,)), ("shonen-battle-bold-black", (l2, l3))):
            p = self.client.get(f"/v1/styles/{nid}").json()["prompt"]
            self.assertNotIn(l1["ja"], p["ja"], f"{nid}: level-1 words must not be added below level 1")
            self.assertNotIn(l1["en"], p["en"], nid)
            for w in own:
                self.assertIn(w["ja"], p["ja"], nid)
                self.assertIn(w["en"], p["en"], nid)
        # level 3: the level-3 words come after the lead, so they override the level-2 words where they disagree
        p3 = self.client.get("/v1/styles/shonen-battle-bold-black").json()["prompt"]
        for lang in ("ja", "en"):
            self.assertTrue(p3[lang].endswith(s.l3_lead[lang] + l3[lang] + ("。" if lang == "ja" else ".")), lang)
            self.assertLess(p3[lang].index(l2[lang]), p3[lang].index(s.l3_lead[lang]), lang)
        p2 = self.client.get("/v1/styles/shonen-battle").json()["prompt"]
        self.assertNotIn(s.l3_lead["ja"], p2["ja"], "the lead belongs to level 3 only")
        # sample-only data (people, clothes, places) never reaches a style prompt
        for nid in ("shonen", "shonen-sports", "essay-food", "gekiga-hardboiled"):
            p = s.style_prompt(nid)
            for word in ("学生服", "マグ", "路地", "題材", "魔法少女", "uniform", "mug", "alley", "magical girl"):
                self.assertNotIn(word, p["ja"] + p["en"], f"{nid}: {word}")

    def test_children_let_an_agent_walk_the_tree(self):
        tree = self.client.get("/v1/tree").json()["nodes"]
        for nid in ("shonen", "shonen-battle"):
            b = self.client.get(f"/v1/styles/{nid}").json()
            self.assertEqual([c["id"] for c in b["children"]], [n["id"] for n in tree if n["parent"] == nid], nid)
            self.assertEqual(set(b["children"][0]), {"id", "title", "summary", "thumbnail_url"})
        en = self.client.get("/v1/styles/shonen?lang=en").json()["children"][0]
        self.assertEqual(en["title"], next(n for n in self.client.get("/v1/tree?lang=en").json()["nodes"]
                                           if n["id"] == en["id"])["title"])

    def test_level2_sample_prompt_has_two_steps(self):
        s = main.store()
        steps = s.generation_steps("shonen-battle")
        self.assertEqual(len(steps), 2)
        self.assertIn(s.base["shonen"]["words"]["ja"], steps[0]["ja"], "step 1 draws the genre scene in the level-1 look")
        self.assertIn(s.scenes["shonen"]["l2_scene"]["en"], steps[0]["en"])
        self.assertIn(s.base["shonen-battle"]["words"]["en"], steps[1]["en"], "step 2 redraws with the level-2 words")
        self.assertNotIn(s.base["shonen"]["words"]["en"], steps[1]["en"])
        joined = s.generation_prompt("shonen-battle")
        self.assertTrue(joined["ja"].startswith("1枚目（元の場面）: "))
        self.assertIn("\n\n2枚目（1枚目の絵を元に描き直す）: ", joined["ja"])
        self.assertEqual(len(s.generation_steps("shonen")), 1)

    def test_level3_sample_starts_from_its_own_level2_scene(self):
        s = main.store()
        nid, l2 = "shonen-battle-bold-black", "shonen-battle"
        steps = s.generation_steps(nid)
        self.assertEqual(len(steps), 2)
        self.assertIn(s.l3_scenes[l2]["ja"], steps[0]["ja"], "step 1 draws the level-2 branch's own scene")
        self.assertIn(s.base[l2]["words"]["en"], steps[0]["en"], "step 1 uses the level-2 look")
        self.assertNotIn(s.scenes["shonen"]["l2_scene"]["en"], steps[0]["en"], "not the level-2 sample scene")
        self.assertNotIn(s.base["shonen"]["words"]["en"], steps[0]["en"] + steps[1]["en"])
        for part in (s.base[l2]["words"]["en"], s.l3_lead["en"], s.base[nid]["words"]["en"]):
            self.assertIn(part, steps[1]["en"], "step 2 redraws with level-2 words + lead + level-3 words")
        self.assertEqual(set(s.l3_scenes), {n for n in s.order if s.base[n]["level"] == 2})

    def test_levels_without_sample_and_english_titles(self):
        b = self.client.get("/v1/styles/shonen-battle").json()
        self.assertEqual(b["level"], 2)
        self.assertEqual(b["samples"], [])
        self.assertIsNone(b["reference"])
        self.assertIs(b["license"]["generated"], True)
        self.assertIs(b["license"]["artist_names"], False)
        en = self.client.get("/v1/styles/shonen-battle?lang=en").json()
        self.assertEqual([p["title"] for p in en["path"]], ["Shonen manga"])
        self.assertEqual(en["prompt"], b["prompt"], "the prompt carries both languages regardless of ?lang")

    def test_only_get_is_allowed(self):
        r = self.client.options("/v1/tree", headers={"Origin": "https://example.org",
                                                     "Access-Control-Request-Method": "GET"})
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.headers["access-control-allow-methods"], "GET")
        for method in ("post", "put", "delete", "patch"):
            self.assertEqual(getattr(self.client, method)("/v1/tree").status_code, 405, method)

    def test_unknown_style_is_404_json(self):
        r = self.client.get("/v1/styles/nope")
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.headers["access-control-allow-origin"], "*")
        self.assertEqual(r.json(), {"error": "not found"})


class PageTests(Base):
    def test_top_page_languages(self):
        ja = self.client.get("/?lang=ja").text
        self.assertIn('<html lang="ja">', ja)
        self.assertIn("マンガ・アニメの絵柄見本帳", ja)
        self.assertIn("少年漫画", ja)
        en = self.client.get("/?lang=en").text
        self.assertIn('<html lang="en">', en)
        self.assertIn("Manga &amp; Anime Style Book", en)
        self.assertIn("Shonen manga", en)
        self.assertNotIn("少年漫画", en)
        self.assertIn('href="/search?lang=ja&amp;model=gpt-image"', en)
        auto = self.client.get("/", headers={"Accept-Language": "en-US,en;q=0.9"}).text
        self.assertIn('<html lang="en">', auto)

    def test_breadcrumb_and_children(self):
        # 分類の道筋は題名のすぐ上（node-path）。トップへはヘッダーのサイト名から戻る。
        html = self.client.get("/n/shonen-battle?lang=ja").text
        self.assertIn('class="site-name" href="/?lang=ja&amp;model=gpt-image"', html)
        self.assertIn('href="/n/shonen?lang=ja&amp;model=gpt-image">少年漫画</a>', html)
        self.assertIn('<span aria-current="page">バトル</span>', html)
        self.assertEqual(html.count('aria-current="page"'), 1, "the path is shown once, not twice")
        self.assertEqual(html.count('<li><a href="/n/shonen-battle-'), 25)

    def test_category_gallery_then_sample_prompt_and_api_url(self):
        # 新しい承認導線: 大分類→画像一覧→詳細。L2の通過は必須でない。
        html = self.client.get('/n/shonen?lang=ja').text
        self.assertIn('class="gallery-grid"', html)
        self.assertIn('data-level="3"', html)
        self.assertNotIn('id="prompt-text"', html)
        direct = self.client.get('/styles/shonen?lang=ja').text
        self.assertLess(direct.index('id="prompt-text"'), direct.index('id="api-url"'))
        genko = self.client.get('/n/shonen-battle?lang=en&client=genko').text
        self.assertLess(genko.index('id="prompt-text"'), genko.index('href="genko://use-style?id=shonen-battle"'))
        self.assertGreater(genko.index('class="related-styles"'), genko.index('id="prompt-text"'))
        leaf = self.client.get('/n/shonen-battle-bold-black?lang=ja').text
        self.assertNotIn('class="related-styles"', leaf)
        self.assertLess(leaf.index('class="sample-image"'), leaf.index('id="prompt-text"'))
        self.assertLess(leaf.index('id="prompt-text"'), leaf.index('id="api-url"'))
        empty_leaf = self.client.get('/n/shonen-battle-chibi-comic?lang=ja').text
        self.assertIn('見本の絵はまだありません', empty_leaf)

    def test_genko_button_on_every_style_page(self):
        # 2026-09-28（Genko の試験）: 共有された URL（client なし）でも「この絵柄を使う」を出す。
        # リンク先は genko://use-style?id=<id> のまま。近くに短い説明を添える。URL のコピーも残す。
        plain = self.client.get("/n/shonen-battle-bold-black?lang=ja").text
        self.assertIn('href="genko://use-style?id=shonen-battle-bold-black"', plain)
        self.assertIn("この絵柄を使う", plain)
        self.assertIn("Genko Studio で開きます（Genko が入っていないと何も起きません）", plain)
        self.assertIn('data-copy-target="api-url"', plain)
        self.assertIn(f'value="{ORIGIN}/v1/styles/shonen-battle-bold-black?model=gpt-image"', plain)
        en = self.client.get("/n/gag-surreal-doodle-casual?lang=en").text
        self.assertIn('href="genko://use-style?id=gag-surreal-doodle-casual"', en)
        self.assertIn("Opens in Genko Studio (nothing happens if Genko is not installed).", en)
        for nid in ("shonen", "shonen-battle"):  # every level
            self.assertIn(f'href="genko://use-style?id={nid}"', self.client.get(f"/styles/{nid}?lang=ja").text)
        # inside Genko: unchanged (only the button, no URL copy)
        for kw in ({"url": "/n/shonen-battle-bold-black?lang=ja&client=genko"},
                   {"url": "/n/shonen-battle-bold-black?lang=ja", "headers": {"User-Agent": "Mozilla/5.0 GenkoStudio/1.2"}}):
            html = self.client.get(kw["url"], headers=kw.get("headers")).text
            self.assertIn('href="genko://use-style?id=shonen-battle-bold-black"', html)
            self.assertNotIn('data-copy-target="api-url"', html)
            self.assertNotIn("Genko が入っていないと", html)
        # a level-1 branch can be chosen too (the levels below are left to the tool)
        self.assertIn('href="genko://use-style?id=shonen"', self.client.get("/n/shonen?client=genko").text)

    def test_path_id_and_same_name_styles_on_the_page(self):
        # 2026-09-28（Genko の試験）: 同じ題名の絵柄が別の分類にあり、名前だけで伝わって取り違えられた。
        html = self.client.get("/n/gag-surreal-doodle-casual?lang=ja").text
        head = html.split('<div class="node-head">', 1)[1].split("</div>", 1)[0]
        # the category path right above the title, and the id
        self.assertLess(head.index('class="node-path"'), head.index("<h1>"))
        self.assertIn('<a href="/n/gag?lang=ja&amp;model=gpt-image">ギャグ漫画</a>', head)
        self.assertIn('<a href="/n/gag-surreal?lang=ja&amp;model=gpt-image">シュール</a>', head)
        self.assertIn("<code>gag-surreal-doodle-casual</code>", head)
        self.assertIn("<title>ゆるい手描きの落書き風（ギャグ漫画 › シュール） | マンガ・アニメの絵柄見本帳</title>", html)
        # the other styles with the same name, with their paths; the same level-1 genre first.
        # The notice sits in that bottom section under the API URL, not under the title (the owner's request,
        # 2026-09-28: the page is used to take prompts, so nothing extra goes above them).
        self.assertNotIn("同じ名前の絵柄が、ほかの分類に", head)
        self.assertNotIn('href="#same-title"', html)
        self.assertLess(html.index('id="api-url"'), html.index('id="same-title"'))
        same = html.split('<section class="same-title" id="same-title">', 1)[1]
        self.assertRegex(same, r"同じ名前の絵柄が、ほかの分類に \d+ あります。")
        self.assertIn('<a href="/n/essay-food-doodle-casual?lang=ja&amp;model=gpt-image">エッセイ漫画 › 食べ歩き › ゆるい手描きの落書き風</a>', same)
        self.assertLess(same.index("gag-slapstick-doodle-casual"), same.index("essay-food-doodle-casual"))
        self.assertNotIn("/n/gag-surreal-doodle-casual?", same, "not itself")
        other = self.client.get("/n/essay-food-doodle-casual?lang=ja").text
        self.assertIn('<a href="/n/gag-surreal-doodle-casual?lang=ja&amp;model=gpt-image">ギャグ漫画 › シュール › ゆるい手描きの落書き風</a>', other)
        en = self.client.get("/n/gag-surreal-doodle-casual?lang=en").text
        self.assertIn("Styles with the same name", en)
        # a hidden branch is not listed
        main.store().set_published("essay-food-doodle-casual", False)
        self.assertNotIn("essay-food-doodle-casual", self.client.get("/n/gag-surreal-doodle-casual?lang=ja").text)
        # a unique title has no such notice
        self.assertNotIn('id="same-title"', self.client.get("/n/gag?lang=ja").text)

    def test_copy_starts_with_the_path_and_the_id(self):
        # 「プロンプトをコピー」「URL をコピー」の文の先頭に、分類の道筋と id を入れる（名前だけで伝わらない）。
        html = self.client.get("/n/gag-surreal-doodle-casual?lang=ja").text
        head = "モデル: GPT Image\n絵柄: ギャグ漫画 › シュール › ゆるい手描きの落書き風（id: gag-surreal-doodle-casual）"
        self.assertIn(f'data-copy-target="prompt-text" data-copy-prefix="{head}"', html)
        self.assertIn(f'data-copy-target="api-url" data-copy-prefix="{head}"', html)
        en_prompt = self.client.get("/n/gag-surreal-doodle-casual?lang=ja&plang=en").text
        self.assertIn('data-copy-target="prompt-text" data-copy-prefix="Model: GPT Image\nStyle: Gag manga › Surreal › ', en_prompt)
        self.assertIn(f'data-copy-target="api-url" data-copy-prefix="{head}"', en_prompt)
        js = (HERE.parent / "app" / "static" / "site.js").read_text(encoding="utf-8")
        self.assertIn("button.dataset.copyPrefix", js)
        self.assertIn("`${prefix}\\n${textOf(el)}`", js)

    def test_cards_show_the_category(self):
        html = self.client.get('/n/gag?lang=ja').text
        self.assertIn('<span class="card-path">ギャグ漫画 › シュール</span>', html)
        top = self.client.get('/?lang=ja').text
        self.assertIn('class="card-path"', top, 'flat list cards identify their original parent')
        self.assertIn('data-style-id="shonen"', top, 'base style stays available without becoming a required step')

    def test_search_tells_same_named_styles_apart(self):
        r = self.client.get("/search?lang=ja&q=ゆるい手描き")
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('href="/n/gag-surreal-doodle-casual?lang=ja&amp;model=gpt-image"', html)
        self.assertIn('href="/n/essay-food-doodle-casual?lang=ja&amp;model=gpt-image"', html)
        self.assertIn('<span class="card-path">ギャグ漫画 › シュール</span>', html)
        self.assertIn('<span class="card-path">エッセイ漫画 › 食べ歩き</span>', html)
        # narrowing with a category word; English words and ids work too
        narrow = self.client.get("/search?lang=ja&q=ゆるい手描き シュール").text
        self.assertIn("gag-surreal-doodle-casual", narrow)
        self.assertNotIn("essay-food-doodle-casual", narrow)
        self.assertIn("essay-food-doodle-casual", self.client.get("/search?lang=en&q=essay-food-doodle").text)
        self.assertIn('value="ゆるい手描き"', html)
        self.assertIn("見つかりませんでした", self.client.get("/search?lang=ja&q=存在しない言葉xyz").text)
        # the search form is on the top page and linked from every page
        self.assertIn('action="/search"', self.client.get("/?lang=ja").text)
        self.assertIn('href="/search?lang=ja&amp;model=gpt-image"', self.client.get("/n/shonen?lang=ja").text)
        self.assertIn('<input type="hidden" name="client" value="genko">', self.client.get("/search?client=genko&lang=ja").text)
        # a hidden branch is not found
        main.store().set_published("essay-food", False)
        self.assertNotIn("essay-food-doodle-casual", self.client.get("/search?lang=ja&q=ゆるい手描き").text)

    def test_prompt_language_switch_is_independent(self):
        s = main.store()
        prompt = s.style_prompt("shonen-battle-bold-black")
        ja = self.client.get("/n/shonen-battle-bold-black?lang=ja").text
        self.assertIn(f'lang="ja" aria-labelledby="prompt-heading">{prompt["ja"]}</textarea>', ja)
        en_prompt_ja_ui = self.client.get("/n/shonen-battle-bold-black?lang=ja&plang=en").text
        self.assertIn('<html lang="ja">', en_prompt_ja_ui)
        self.assertIn(f'lang="en" aria-labelledby="prompt-heading">{prompt["en"]}</textarea>', en_prompt_ja_ui)
        self.assertIn("見本を作ったプロンプト", en_prompt_ja_ui)
        en_ui = self.client.get("/n/shonen-battle-bold-black?lang=en").text
        self.assertIn(f'lang="en" aria-labelledby="prompt-heading">{prompt["en"]}</textarea>', en_ui)
        self.assertIn("Prompt used for the sample", en_ui)

    def test_api_guide_is_linked_from_the_bottom_of_the_top_page(self):
        # 本人の指示（2026-09-27）: トップページの一番下から、読めば API の使い方がわかるページへ。
        top = self.client.get("/?lang=ja").text
        footer = top.split('<footer class="site-footer">', 1)[1]
        self.assertIn('href="/api?lang=ja&amp;model=gpt-image"', footer)
        self.assertGreater(top.index('href="/api?lang=ja&amp;model=gpt-image"'), top.index('class="gallery-grid"'))
        self.assertIn('href="/api?lang=en&amp;model=gpt-image&amp;client=genko"', self.client.get("/?lang=en&client=genko").text)
        from app.api_doc import STYLE_FIELDS, TREE_FIELDS
        for lang in ("ja", "en"):
            page = self.client.get(f"/api?lang={lang}")
            self.assertEqual(page.status_code, 200)
            self.assertIn(f"{ORIGIN}/v1/tree", page.text)
            self.assertIn(f"{ORIGIN}/v1/styles/", page.text)
            for name, _ in TREE_FIELDS[lang] + STYLE_FIELDS[lang]:
                self.assertIn(f"<code>{name}</code>", page.text, f"{lang}: {name}")
        # every key the API really returns is explained on the page
        node = self.client.get("/v1/tree").json()["nodes"][0]
        self.assertEqual(set(node), {n for n, _ in TREE_FIELDS["ja"]})
        for nid in ("shonen", "shonen-battle-bold-black"):
            self.assertEqual(set(self.client.get(f"/v1/styles/{nid}").json()), {n for n, _ in STYLE_FIELDS["ja"]})
        self.assertEqual([n for n, _ in STYLE_FIELDS["ja"]], [n for n, _ in STYLE_FIELDS["en"]])
        self.assertIn('<html lang="en">', self.client.get("/api?lang=en").text)
        self.assertIn('href="/api?lang=en&amp;model=gpt-image"', self.client.get("/api?lang=ja").text, "language switch on the guide")

    def test_security_headers(self):
        r = self.client.get("/n/shonen?lang=ja")
        self.assertIn("script-src 'self'", r.headers["content-security-policy"])
        self.assertNotIn("unsafe-inline", r.headers["content-security-policy"])
        self.assertEqual(r.headers["x-content-type-options"], "nosniff")
        self.assertNotIn("<script>", r.text)
        self.assertNotIn(" style=", r.text)
        self.assertNotIn("onclick", r.text)

    def test_unknown_page_is_404_html(self):
        r = self.client.get("/n/nope?lang=en")
        self.assertEqual(r.status_code, 404)
        self.assertIn("Page not found", r.text)


class VisibilityTests(Base):
    def test_hidden_branch_disappears_everywhere(self):
        s = main.store()
        s.set_published("shonen-battle", False)
        tree = self.client.get("/v1/tree").json()["nodes"]
        ids = {n["id"] for n in tree}
        self.assertNotIn("shonen-battle", ids)
        self.assertNotIn("shonen-battle-bold-black", ids, "children of a hidden branch must be hidden too")
        self.assertIn("shonen-sports", ids)
        for path in ("/v1/styles/shonen-battle", "/v1/styles/shonen-battle-bold-black",
                     "/files/shonen-battle-bold-black/upper_body-v1.jpg",
                     "/files/shonen-battle-bold-black/upper_body-v1-thumb.jpg"):
            self.assertEqual(self.client.get(path).status_code, 404, path)
        self.assertEqual(self.client.get("/n/shonen-battle-bold-black").status_code, 404)
        top = self.client.get("/n/shonen?lang=ja").text
        self.assertNotIn("/n/shonen-battle?", top)
        self.assertNotIn("shonen-battle-bold-black", top, "the hidden sample must not be the thumbnail")
        rep = [n for n in tree if n["id"] == "shonen"][0]["thumbnail_url"]
        self.assertIsNone(rep)
        kids = [c["id"] for c in self.client.get("/v1/styles/shonen").json()["children"]]
        self.assertNotIn("shonen-battle", kids, "a hidden branch must not be listed as a child")
        self.assertIn("shonen-sports", kids)
        s.set_published("shonen-battle", True)
        self.assertEqual(self.client.get("/v1/styles/shonen-battle-bold-black").status_code, 200)

    def test_hiding_survives_restart(self):
        main.store().set_published("gekiga", False)
        main._store = None
        self.assertEqual(self.client.get("/v1/styles/gekiga").status_code, 404)


class AdminTests(Base):
    def test_admin_is_closed_without_session_or_config(self):
        r = self.client.get("/admin")
        self.assertEqual(r.status_code, 403)
        self.assertIn("ログインを確かめられませんでした", r.text)
        self.assertIn('href="/__auth/login?next=/admin"', r.text)
        self.assertNotIn("管理画面</a>\n    <nav", r.text.split("<main", 1)[1])
        self.assertTrue(self.verify.seen, "the session must be checked with costlab-auth")
        main.ADMIN_VERIFY_URL = ""
        self.verify.status = 204
        self.assertEqual(self.client.get("/admin").status_code, 403, "no verify URL = closed")
        main.ADMIN_VERIFY_URL = "http://127.0.0.1:9/__auth/verify"
        self.assertEqual(self.client.get("/admin").status_code, 403, "auth service down = closed")

    def test_admin_forwards_the_cookie(self):
        self.login()
        r = self.client.get("/admin", headers={"Cookie": "costlab_session=abc"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("管理画面", r.text)
        self.assertEqual(self.verify.seen[-1]["cookie"], "costlab_session=abc")
        self.assertEqual(r.headers["cache-control"], "private, no-store")
        self.assertIn("noindex", r.headers["x-robots-tag"])

    def test_post_needs_same_origin_and_session(self):
        self.login()
        self.assertEqual(self.admin_post("/admin/n/shonen/hide", origin="https://evil.example").status_code, 403)
        self.assertEqual(self.admin_post("/admin/n/shonen/hide", origin=None).status_code, 403)
        self.assertTrue(main.store().visible("shonen"))
        self.verify.status = 303
        self.assertEqual(self.admin_post("/admin/n/shonen/hide").status_code, 403)
        self.assertTrue(main.store().visible("shonen"))
        self.login()
        r = self.admin_post("/admin/n/shonen/hide")
        self.assertEqual(r.status_code, 303)
        self.assertFalse(main.store().visible("shonen"))
        self.assertEqual(self.admin_post("/admin/n/shonen/publish").status_code, 303)
        self.assertTrue(main.store().visible("shonen"))
        r = self.admin_post("/admin/n/shonen-battle/hide", data={"back": "shonen"})
        self.assertTrue(r.headers["location"].startswith("/admin/n/shonen?"), r.headers["location"])
        r = self.admin_post("/admin/n/shonen/hide", data={"back": "top"})
        self.assertTrue(r.headers["location"].startswith("/admin?"), r.headers["location"])
        page = self.client.get("/admin", headers={"Cookie": "costlab_session=ok"}).text
        self.assertIn("隠している", page)

    def test_edit_bumps_versions_and_rejects_real_names(self):
        self.login()
        before = self.client.get("/v1/styles/shonen-battle-bold-black").json()
        self.assertEqual(main.store().stats()["queue"], 0)
        form = {k: v for k, v in (("title_ja", "バトル（改）"), ("title_en", "Battle"), ("summary_ja", "説明"),
                                  ("summary_en", "Summary"), ("words_ja", "新しい言葉"), ("words_en", "new words"),
                                  ("words_tags", "tag"))}
        r = self.admin_post("/admin/n/shonen-battle/edit", data=form)
        self.assertEqual(r.status_code, 303)
        self.assertIn("msg=", r.headers["location"])
        after = self.client.get("/v1/styles/shonen-battle-bold-black").json()
        self.assertEqual(after["version"], before["version"] + 1, "a child's API content changed with its parent")
        self.assertEqual(after["path"][1]["title"], "バトル（改）")
        self.assertIn("新しい言葉", after["prompt"]["ja"])
        # new words need a new picture: the child whose sample was made with the old words is queued
        queued = {q["id"]: q for q in main.store().queue()}
        self.assertIn("shonen-battle-bold-black", queued, "a word change must queue the pictures made with other words")
        self.assertIn("新しい言葉", queued["shonen-battle-bold-black"]["prompt"]["ja"])
        self.assertNotIn("shonen-sports-bold-black", queued)
        # a title-only edit changes no prompt, so it queues nothing
        main.store().cancel_regen("shonen-battle-bold-black")
        s = main.store()
        s.put_sample("shonen-sports-bold-black", png_bytes(), prompt=s.generation_prompt("shonen-sports-bold-black"))
        base = s.base["shonen-sports"]
        title_only = {"title_ja": "スポーツ（改）", "title_en": base["title"]["en"], "summary_ja": base["summary"]["ja"],
                      "summary_en": base["summary"]["en"], "words_ja": base["words"]["ja"],
                      "words_en": base["words"]["en"], "words_tags": base["words"]["tags"]}
        self.admin_post("/admin/n/shonen-sports/edit", data=title_only)
        self.assertNotIn("shonen-sports-bold-black", {q["id"] for q in main.store().queue()},
                         "no prompt changed, so no picture is queued")
        bad = dict(form, words_ja="ドラゴンボールのような絵")
        r = self.admin_post("/admin/n/shonen-battle/edit", data=bad)
        self.assertIn("err=", r.headers["location"])
        self.assertNotIn("ドラゴンボール", self.client.get("/v1/styles/shonen-battle").json()["prompt"]["ja"])
        self.assertEqual(self.admin_post("/admin/n/shonen-battle/reset").status_code, 303)
        reset = self.client.get("/v1/styles/shonen-battle-bold-black").json()
        self.assertEqual(reset["prompt"], before["prompt"])
        self.assertEqual(reset["version"], before["version"] + 2)

    def test_sample_upload_replaces_and_bumps(self):
        self.login()
        self.admin_post("/admin/n/shonen-battle-bold-black/regen", data={"note": "もっと驚いた顔"})
        self.assertEqual(main.store().stats()["queue"], 1)
        before = self.client.get("/v1/styles/shonen-battle-bold-black").json()
        r = self.admin_post("/admin/n/shonen-battle-bold-black/sample",
                            data={"model_version": "gpt-image-2.5-sunburst", "prompt_ja": "", "prompt_en": ""},
                            files={"image": ("x.png", png_bytes(), "image/png")})
        self.assertEqual(r.status_code, 303)
        self.assertIn("msg=", r.headers["location"])
        after = self.client.get("/v1/styles/shonen-battle-bold-black").json()
        self.assertEqual(after["version"], before["version"] + 1)
        self.assertNotEqual(after["samples"][0]["url"], before["samples"][0]["url"])
        self.assertEqual(self.client.get(before["samples"][0]["url"].replace(ORIGIN, "")).status_code, 404)
        img = Image.open(io.BytesIO(self.client.get(after["samples"][0]["url"].replace(ORIGIN, "")).content))
        self.assertEqual((img.mode, img.size), ("L", (768, 1024)), "stored greyscale 3:4")
        self.assertEqual(main.store().stats()["queue"], 0, "a new sample clears the regeneration request")
        self.assertEqual(after["samples"][0]["prompt"], main.store().generation_prompt("shonen-battle-bold-black"))

    def test_level2_own_sample_and_optional_topic_gallery(self):
        s = main.store()
        s.put_sample("shonen-battle", png_bytes(), prompt=s.generation_prompt("shonen-battle"))
        html = self.client.get("/n/shonen-battle?lang=ja").text
        self.assertGreater(html.index('class="related-styles"'), html.index('id="prompt-text"'))
        self.assertLess(html.index('class="sample-image"'), html.index('id="prompt-text"'))
        self.assertIn("1枚目（元の場面）", html, "the two-step sample prompt is shown")
        top = self.client.get("/search?root=shonen&topic=shonen-battle&lang=ja").text
        self.assertIn('src="/files/shonen-battle/upper_body-v1-thumb.jpg"', top, "the level-2 card shows its own sample")

    def test_import_keeps_the_recorded_prompt_and_is_idempotent(self):
        s = main.store()
        prompt = {"ja": "記録したプロンプト", "en": "the recorded prompt"}
        v0 = s.effective("gag")["version"]
        a = s.put_sample("gag", png_bytes(), prompt=prompt, created_at="2026-09-26T15:00:00Z", origin="cli")
        self.assertEqual((a["prompt"], a["created_at"]), (prompt, "2026-09-26T15:00:00Z"))
        v1 = s.effective("gag")["version"]
        self.assertEqual(v1, v0 + 1)
        again = s.put_sample("gag", png_bytes(), prompt=prompt, created_at="2026-09-26T15:00:00Z", origin="cli")
        self.assertEqual(again["file"], a["file"])
        self.assertEqual(s.effective("gag")["version"], v1, "the same picture and prompt again changes nothing")
        with self.assertRaises(Exception):
            s.put_sample("gag", png_bytes(), prompt=prompt, created_at="yesterday")
        api = self.client.get("/v1/styles/gag").json()
        self.assertEqual(api["samples"][0]["prompt"], prompt)

    def test_bad_upload_is_rejected(self):
        self.login()
        for name, raw in (("a.gif", b"GIF89a" + b"\0" * 100), ("b.png", b"not an image")):
            r = self.admin_post("/admin/n/shonen/sample", files={"image": (name, raw, "image/png")})
            self.assertIn("err=", r.headers["location"], name)
        self.assertIsNone(main.store().effective("shonen")["sample"])

    def test_token_mode(self):
        self.login()
        self.assertIn("err=", self.admin_post("/admin/api-mode", data={"mode": "token"}).headers["location"])
        r = self.admin_post("/admin/tokens", data={"label": "Genko"})
        self.assertEqual(r.status_code, 200)
        token = r.text.split('id="new-token" type="text" value="', 1)[1].split('"', 1)[0]
        self.assertTrue(token.startswith("mst_"))
        self.assertNotIn(token, (Path(self.tmp) / "state.json").read_text(), "only the hash is stored")
        self.assertEqual(self.admin_post("/admin/api-mode", data={"mode": "token"}).status_code, 303)
        r = self.client.get("/v1/tree")
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.headers["access-control-allow-origin"], "*")
        self.assertEqual(self.client.get("/v1/tree", headers={"Authorization": "Bearer wrong"}).status_code, 401)
        ok = self.client.get("/v1/tree", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.headers["cache-control"], "private, no-store")
        self.assertEqual(self.client.get("/?lang=ja").status_code, 200, "pages stay public")
        tid = main.store().tokens()[0]["id"]
        self.assertIn("err=", self.admin_post(f"/admin/tokens/{tid}/revoke").headers["location"])
        self.admin_post("/admin/api-mode", data={"mode": "public"})
        self.assertEqual(self.client.get("/v1/tree").status_code, 200)

    def test_internal_routes_only_from_inside_the_container(self):
        for path in ("/internal/queue", "/internal/prompt/shonen"):
            self.assertEqual(self.client.get(path).status_code, 404, path)
        self.assertEqual(self.client.post("/internal/samples/shonen", content=png_bytes()).status_code, 404)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="manga-store-"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_empty_volume_boots_with_seeds_and_restart_keeps_state(self):
        s = Store(self.tmp / "data")
        pair_ids = {p['id'] for p in staged_pairs()}
        expected = len(set(SAMPLED) | {p['id'] for p in staged_additions()} | pair_ids)
        self.assertEqual(s.stats()["samples"], expected)
        for nid in SAMPLED:
            self.assertEqual(s.effective(nid)["version"], 2 if nid in pair_ids else 1)
        s.set_published("horror", False)
        s2 = Store(self.tmp / "data")
        self.assertFalse(s2.visible("horror"))
        self.assertEqual(s2.stats()["samples"], expected, "seeds are imported once")

    def test_additions_import_into_existing_volume_without_replacing_samples(self):
        items = staged_additions()
        if not items:
            self.skipTest("run prepare_samples.py to stage the release images")
        cat = json.loads((HERE.parent / "app/catalog.json").read_text(encoding="utf-8"))
        cat["nodes"] = [n for n in cat["nodes"] if n["id"] not in ADDITIONS]
        old = self.tmp / "old-catalog.json"
        old.write_text(json.dumps(cat, ensure_ascii=False), encoding="utf-8")
        first = Store(self.tmp / "data", catalog_file=old)
        original = {nid: first.effective(nid) for nid in SAMPLED}
        upgraded = Store(self.tmp / "data")
        self.assertEqual(upgraded.stats()["samples"], len(set(SAMPLED) | {p['id'] for p in items} | {p['id'] for p in staged_pairs()}))
        for nid, value in original.items():
            self.assertEqual(upgraded.effective(nid), value)
        snapshot = {nid: upgraded.effective(nid) for nid in ADDITIONS}
        restarted = Store(self.tmp / "data")
        for nid, value in snapshot.items():
            self.assertEqual(restarted.effective(nid), value)

    def test_addition_seed_does_not_overwrite_an_existing_image(self):
        if not staged_additions():
            self.skipTest("run prepare_samples.py to stage the release images")
        s = Store(self.tmp / "data", seed_dir=self.tmp / "no-seeds")
        nid = ADDITIONS[0]
        s.put_sample(nid, png_bytes())
        original = s.effective(nid)
        self.assertEqual(Store(self.tmp / "data").effective(nid), original)

    def test_parent_catalog_change_preserves_complete_pair_and_updates_legacy_child(self):
        from app.store import _digest
        seed = self.tmp / 'no-seeds'
        initial = Store(self.tmp / 'data', seed_dir=seed)
        nid = 'shonen-battle-bold-black'
        legacy = 'shonen-battle-comic-lively'
        style = {'ja': '白黒の太い線。', 'en': 'Bold monochrome lines.', 'tags': 'bold monochrome'}
        items = [
            {'subject': role, 'raw': png_bytes(size=(256, 256), color=(value,) * 3),
             'prompt': {lang: style[lang] + ' scene' for lang in ('ja', 'en')},
             'model_version': 'synthetic-test-fixture', 'created_at': '2026-11-07T00:00:00Z'}
            for role, value in [('representative', 80), ('application', 180)]
        ]
        initial.put_sample_pair(nid, items, _digest(style), complete_style=style)
        published = initial.effective(nid)
        legacy_version = initial.effective(legacy)['version']
        cat = json.loads((HERE.parent / 'app/catalog.json').read_text(encoding='utf-8'))
        for node in cat['nodes']:
            if node['id'] == 'shonen-battle':
                node['words']['ja'] += '。追加'
        changed = self.tmp / 'catalog.json'
        changed.write_text(json.dumps(cat, ensure_ascii=False), encoding='utf-8')
        upgraded = Store(self.tmp / 'data', catalog_file=changed, seed_dir=seed)
        self.assertEqual(upgraded.effective(nid), published)
        self.assertEqual(upgraded.style_prompt(nid), style)
        self.assertEqual(upgraded.effective(legacy)['version'], legacy_version + 1)
        restarted = Store(self.tmp / 'data', catalog_file=changed, seed_dir=seed)
        self.assertEqual(restarted.effective(nid), published)
        self.assertEqual(restarted.style_prompt(nid), style)

    def test_catalog_change_bumps_only_changed_nodes(self):
        # This test covers inherited legacy words, not branch-complete pair styles.
        # Keep ordinary seeds but exclude pair shards as the rollout grows.
        legacy_seed = self.tmp / 'legacy-seed'
        shutil.copytree(HERE.parent / 'app/seed', legacy_seed,
                        ignore=shutil.ignore_patterns('pairs'))
        initial = Store(self.tmp / "data", seed_dir=legacy_seed)
        self.assertFalse(initial.state['nodes']['shonen-battle-bold-black'].get('explanatory_style'))
        versions = {nid: initial.effective(nid)['version'] for nid in
                    ('shonen-battle', 'shonen-battle-bold-black', 'shonen-sports', 'shonen')}
        cat = json.loads((HERE.parent / "app" / "catalog.json").read_text(encoding="utf-8"))
        for n in cat["nodes"]:
            if n["id"] == "shonen-battle":
                n["words"]["ja"] += "。追加"
        changed = self.tmp / "catalog.json"
        changed.write_text(json.dumps(cat, ensure_ascii=False), encoding="utf-8")
        s = Store(self.tmp / "data", catalog_file=changed, seed_dir=legacy_seed)
        self.assertEqual(s.effective("shonen-battle")["version"], versions['shonen-battle'] + 1)
        self.assertEqual(s.effective("shonen-battle-bold-black")["version"], versions['shonen-battle-bold-black'] + 1)
        self.assertEqual(s.effective("shonen-sports")["version"], versions['shonen-sports'])
        self.assertEqual(s.effective("shonen")["version"], versions['shonen'])


class StaticTextTests(unittest.TestCase):
    def test_no_real_names_in_visible_text(self):
        cat = json.loads((HERE.parent / "app" / "catalog.json").read_text(encoding="utf-8"))
        deny = cat["deny"]
        texts = [p.read_text(encoding="utf-8") for p in (HERE.parent / "app" / "templates").glob("*.html")]
        texts.append((HERE.parent / "app" / "ui.py").read_text(encoding="utf-8"))
        texts.append(json.dumps(cat, ensure_ascii=False).replace(json.dumps(deny, ensure_ascii=False), ""))
        for text in texts:
            for word in deny:
                self.assertNotIn(word, text)

    def test_templates_have_no_inline_script_or_style(self):
        for p in (HERE.parent / "app" / "templates").glob("*.html"):
            text = p.read_text(encoding="utf-8")
            self.assertNotIn("<script>", text, p.name)
            self.assertNotIn("<style", text, p.name)
            self.assertNotIn(" style=", text, p.name)
            self.assertNotRegex(text, r"\son[a-z]+=", p.name)


if __name__ == "__main__":
    unittest.main()
