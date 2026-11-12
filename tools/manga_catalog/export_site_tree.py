#!/usr/bin/env python3
"""Export the approved style tree as the catalogue site's bundle (costlab-auth/manga/app/catalog.json).

    python3 tools/manga_catalog/export_site_tree.py          # write the bundle
    python3 tools/manga_catalog/export_site_tree.py --check  # fail if the committed bundle is stale

The tree itself is defined by genres.py / styles.py and checked by build_tree.check() (ids, counts,
distinct leaves, deny-list of real names). English display strings come from i18n_en.py.
Level-3 nodes reference a shared finished style ("style": key) so its words are stored once.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_tree as bt  # noqa: E402
import i18n_en  # noqa: E402
from styles import ARCH  # noqa: E402
from ranking_additions import ARCH_EN as RANKING_ARCH_EN
from picturebook_additions import ARCH_EN as PICTUREBOOK_ARCH_EN  # noqa: E402
from x100_additions import ARCH_EN as X100_ARCH_EN  # noqa: E402
from fanza_additions import NEW_IDS as FANZA_IDS  # noqa: E402
from commercial_additions import ARCH_EN as COMMERCIAL_ARCH_EN  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "costlab-auth" / "manga" / "app" / "catalog.json"


def deny_check(where: str, text: str) -> None:
    for d in bt.DENY:
        if d in text:
            raise SystemExit(f"{where}: contains {d!r}")
    if any(q in text for q in "「」『』《》"):
        raise SystemExit(f"{where}: contains title brackets")


def bundle() -> dict:
    tree = bt.build()
    problems = bt.check(tree)
    if problems:
        raise SystemExit("tree check failed:\n  " + "\n  ".join(problems[:40]))
    styles: dict[str, dict] = {}
    nodes = []
    for n in tree["nodes"]:
        if n["level"] == 3:
            key = n["id"][len(n["parent"]) + 1:]
            if key not in ARCH:
                raise SystemExit(f"{n['id']}: unknown style {key!r}")
            title_en, summary_en = (i18n_en.ARCH_EN if key in i18n_en.ARCH_EN else
                                    RANKING_ARCH_EN if key in RANKING_ARCH_EN else
                                    PICTUREBOOK_ARCH_EN if key in PICTUREBOOK_ARCH_EN else
                                    X100_ARCH_EN if key in X100_ARCH_EN else COMMERCIAL_ARCH_EN)[key]
            # 修正した枝の画材・語を、同名の別親の枝へ漏らさない。
            if n.get('medium', '').startswith('repair-'):
                key = key + '--' + n['id']
            elif n['id'] in FANZA_IDS:
                # 成人3枝の背景語を既存4枝の共有定義へ漏らさない。
                key = key + '--fanza-adult'
            if key not in styles:
                deny_check(key, title_en + " " + summary_en)
                styles[key] = {
                    "title": {"ja": n["title"], "en": title_en},
                    "summary": {"ja": n["summary"], "en": summary_en},
                    "words": n["words"],
                }
                if "medium" in n:
                    styles[key]["medium"] = n["medium"]
            elif styles[key]["words"] != n["words"] or styles[key]["title"]["ja"] != n["title"]:
                raise SystemExit(f"{n['id']}: style {key!r} differs between parents")
            nodes.append({"id": n["id"], "parent": n["parent"], "level": 3, "style": key})
            continue
        title_en, summary_en = (i18n_en.L1_EN if n["level"] == 1 else i18n_en.L2_EN)[n["id"]]
        deny_check(n["id"], title_en + " " + summary_en)
        nodes.append({
            "id": n["id"], "parent": n["parent"], "level": n["level"],
            "title": {"ja": n["title"], "en": title_en},
            "summary": {"ja": n["summary"], "en": summary_en},
            "words": n["words"],
            **({"medium": n["medium"]} if "medium" in n else {}),
        })
    return {
        "format": 1,
        "common": tree["common"],
        "media": tree["media"],
        "subjects": tree["subjects"],
        "character": tree["character"],
        "scenes": tree["scenes"],
        "l2_edit": tree["l2_edit"],
        "step_labels": bt.STEP_LABELS,
        "l3_scenes": tree["l3_scenes"],
        "l3_lead": tree["l3_lead"],
        "approved_samples": bt.approved_samples(),
        "avoid": tree["avoid"],
        "avoid_words": bt.AVOID_WORDS,
        "deny": bt.DENY,
        "styles": styles,
        "nodes": nodes,
    }


def render() -> str:
    return json.dumps(bundle(), ensure_ascii=False, indent=0, sort_keys=True) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    text = render()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"{OUT.relative_to(ROOT)} is stale: run tools/manga_catalog/export_site_tree.py", file=sys.stderr)
            return 1
        print("catalog.json is up to date")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(text.encode())} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
