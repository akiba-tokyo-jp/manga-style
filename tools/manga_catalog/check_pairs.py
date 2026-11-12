#!/usr/bin/env python3
"""絵とプロンプトは組で変わる（2026-09-27 本人「プロンプトを更新する場合は、必ず絵も更新しなさい　これは絶対です」）。

approved_samples.json を、元の版（PR の向き先など）と比べる。枝ごとに、
  見本を作った言葉（prompt_sha256）か、API の prompt（style_prompt_sha256）が変わったのに、
  絵（sha256）が変わっていなければ落とす。
絵だけ変わった枝（同じ言葉で作り直した）はよい。元の版に style_prompt_sha256 が無い枝は、その欄を比べない。

  python tools/manga_catalog/check_pairs.py <元の approved_samples.json>
  python tools/manga_catalog/check_pairs.py --self-test   （わざと壊した記録で、落ちることを確かめる）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CURRENT = HERE / "approved_samples.json"


def problems(base: dict, current: dict) -> list[str]:
    out = []
    for nid, cur in current.items():
        old = base.get(nid)
        if old is None:
            continue
        changed = [k for k in ("prompt_sha256", "style_prompt_sha256") if k in old and old[k] != cur.get(k)]
        if changed and old["sha256"] == cur["sha256"]:
            out.append(f"{nid}: {'・'.join(changed)} が変わったのに、絵が同じ（プロンプトを変えたら絵も作り直す）")
    return out


def self_test() -> int:
    base = {"a": {"sha256": "1", "prompt_sha256": "p", "style_prompt_sha256": "s"},
            "b": {"sha256": "2", "prompt_sha256": "p", "style_prompt_sha256": "s"},
            "c": {"sha256": "3", "prompt_sha256": "p"}}
    cases = [
        ("API の prompt だけ変えた", {**base, "a": {**base["a"], "style_prompt_sha256": "s2"}}, 1),
        ("見本の言葉だけ変えた", {**base, "b": {**base["b"], "prompt_sha256": "p2"}}, 1),
        ("言葉と絵を一緒に変えた", {**base, "a": {"sha256": "9", "prompt_sha256": "p2", "style_prompt_sha256": "s2"}}, 0),
        ("絵だけ作り直した", {**base, "b": {**base["b"], "sha256": "8"}}, 0),
        ("元の版に無い欄を足した", {**base, "c": {**base["c"], "style_prompt_sha256": "s"}}, 0),
    ]
    bad = 0
    for name, cur, want in cases:
        got = len(problems(base, cur))
        print(("ok  " if got == want else "NG  ") + f"{name}: 指摘 {got}（期待 {want}）")
        bad += got != want
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    if argv[1:] == ["--self-test"]:
        return self_test()
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    base = json.loads(Path(argv[1]).read_text(encoding="utf-8"))["samples"]
    current = json.loads(CURRENT.read_text(encoding="utf-8"))["samples"]
    found = problems(base, current)
    for p in found[:50]:
        print(p)
    if found:
        print(f"絵とプロンプトの組が崩れた枝 {len(found)}", file=sys.stderr)
        return 1
    same = sum(1 for k in current if k in base and base[k]["sha256"] == current[k]["sha256"])
    print(f"ok: {len(current)} 枝（絵が変わった {len(current) - same}、同じ {same}）。言葉だけ変わった枝はない")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
