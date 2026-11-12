#!/usr/bin/env python3
"""Detection power of costlab-auth/manga/tests/checks.py: break one guard at a time, the checks must FAIL.

    python costlab-auth/manga/tests/power.py

Each case copies the app into a fresh temporary directory, applies one deliberate break and runs the
checks there. A case passes only when the checks exit non-zero (the break was caught). The
temporary directories are made by tempfile and removed by it.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("admin without a session", "app/main.py",
     "def admin_allowed(request: Request) -> bool:\n",
     "def admin_allowed(request: Request) -> bool:\n    return True\n"),
    ("hidden branches shown", "app/store.py",
     "    def visible(self, nid) -> bool:\n",
     "    def visible(self, nid) -> bool:\n        return nid in self.base\n"),
    ("cross-site admin POST", "app/main.py",
     "    if post:\n",
     "    if False:\n"),
    ("artist_names true", "app/main.py",
     '"license": {"generated": True, "artist_names": False, "terms": LICENSE_TERMS},',
     '"license": {"generated": True, "artist_names": True, "terms": LICENSE_TERMS},'),
    ("prompt language ignored", "app/main.py",
     'prompt={"text": prompt[plang], "tags": prompt["tags"], "lang": plang},',
     'prompt={"text": prompt[lang], "tags": prompt["tags"], "lang": lang},'),
    ("no version bump on a new sample", "app/store.py",
     "            if bump:\n                self._bump(nid, ts)\n",
     ""),
    ("bearer token not checked", "app/main.py",
     "    if s.api_mode() != \"token\":\n        return\n",
     "    return\n"),
    ("level-1 words added below level 1", "app/store.py",
     "        return ch if len(ch) == 1 else ch[1:]\n",
     "        return ch\n"),
    ("API prompt changed without a new picture", "app/store.py",
     "            \"tags\": \", \".join([common[\"tags\"]] + [w[\"tags\"] for w in words]),\n",
     "            \"tags\": \"; \".join([common[\"tags\"]] + [w[\"tags\"] for w in words]),\n"),
    ("word edit does not queue the pictures", "app/store.py",
     "                st[\"regen\"] = {\"requested_at\": ts, \"note\": STALE_NOTE}\n",
     "                pass\n"),
    ("re-import bumps the version", "app/store.py",
     "                    and old[\"model\"][\"version\"] == version):\n                return old\n",
     "                    and old[\"model\"][\"version\"] == version):\n                pass\n"),
    ("level-3 sample drawn from the level-2 sample scene", "app/store.py",
     "            scene = self.l3_scenes[ch[1]]\n",
     "            scene = self.scene(nid)[\"l2_scene\"]\n"),
    ("level-3 API prompt without the override lead", "app/store.py",
     "        if self.base[nid][\"level\"] == 3:\n            lead = self.l3_lead\n",
     ""),
    ("hidden child listed in children", "app/main.py",
     "    for k in s.children(nid):\n",
     "    for k in s.children(nid, visible_only=False):\n"),
    ("API guide link removed from the footer", "app/templates/base.html",
     "    <p class=\"footer-api\"><a href=\"/api?lang={{ lang }}{% if genko %}&amp;client=genko{% endif %}\">{{ ui.api_guide_link }}</a></p>\n",
     ""),
    # 2026-09-28（Genko の試験で見つかった 3 つの問題）
    ("Genko button only with client=genko again", "app/templates/node.html",
     "    <div class=\"use-style\">\n      <a class=\"button button-primary button-large\" href=\"{{ node.genko_url }}\">{{ ui.use_style }}</a>\n",
     "    <div class=\"use-style\">\n"),
    ("category path missing above the title", "app/templates/node.html",
     "  {%- if node.path_upper %}\n",
     "  {%- if false %}\n"),
    ("same-name styles not linked", "app/main.py",
     "            for k in s.same_title(nid, lang)]\n",
     "            for k in s.same_title(nid, lang)][:0]\n"),
    ("same-name notice back under the title", "app/templates/node.html",
     '  <p class="node-id">{{ ui.id_label }}: <code>{{ node.id }}</code></p>\n',
     '  <p class="node-id">{{ ui.id_label }}: <code>{{ node.id }}</code></p>\n'
     '  {%- if same_title %}<p class="same-title-notice">{{ ui.same_title_notice.format(n=same_title | length) }}</p>{%- endif %}\n'),
    ("copied text without the path and id", "app/templates/node.html",
     " data-copy-target=\"prompt-text\" data-copy-prefix=\"{{ copy_head.prompt }}\"",
     " data-copy-target=\"prompt-text\""),
    ("cards without their category", "app/main.py",
     "            \"path\": path_text(s, nid, lang, include_self=False),\n",
     "            \"path\": \"\",\n"),
    ("level-3 path in the style API includes itself again", "app/main.py",
     "for c in s.chain(nid)[:-1]],\n",
     "for c in s.chain(nid)],\n"),
    ("tree nodes without path", "app/main.py",
     "                      \"path\": s.path_titles(nid, lang)})\n",
     "                      })\n"),
    ("search ignores the category words", "app/store.py",
     "            hay = \" \".join(self.path_titles(nid, \"ja\") + self.path_titles(nid, \"en\")\n",
     "            hay = \" \".join([self.title(nid, \"ja\"), self.title(nid, \"en\")]\n"),
]


def skip_copies(folder: str, names: list[str]) -> set[str]:
    # 比較の絵（compare/files、最大 約 500 MB）は checks が使わない。変異ごとに複写しない。
    skip = {n for n in names if n == "__pycache__"}
    if Path(folder).name == "compare":
        skip |= {n for n in names if n in ("files", "files.new")}
    return skip


def run_checks(tree: Path) -> int:
    # 検出力は壊したガードで1件でも落ちれば判定できる。失敗後の全件再実行を避ける。
    cmd = [sys.executable, "-W", "ignore", "-m", "unittest", "discover", "-s", "tests", "-p", "checks.py", "-f"]
    return subprocess.run(cmd, cwd=tree, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def main() -> int:
    # 元から壊れた試験を「全変異を検出した」と誤認しない。
    if run_checks(ROOT) != 0:
        print("NG   unmodified baseline: checks must pass before mutation tests")
        return 1
    failures = 0
    for name, rel, old, new in CASES:
        with tempfile.TemporaryDirectory(prefix="manga-power-") as tmp:
            tree = Path(tmp) / "manga"
            shutil.copytree(ROOT, tree, ignore=skip_copies)
            target = tree / rel
            text = target.read_text(encoding="utf-8")
            if text.count(old) != 1:
                print(f"NG   {name}: the code to break was not found exactly once (the checks cannot be proven)")
                failures += 1
                continue
            target.write_text(text.replace(old, new, 1), encoding="utf-8")
            code = run_checks(tree)
            if code == 0:
                print(f"NG   {name}: the checks still PASSED with this break")
                failures += 1
            else:
                print(f"ok   {name}: caught (exit {code})")
    if failures:
        print(f"{failures} case(s) without detection power")
        return 1
    print(f"all {len(CASES)} breaks were caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())
