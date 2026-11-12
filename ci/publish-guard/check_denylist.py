#!/usr/bin/env python3
"""
公開ガード: 禁止リスト検査（CI: publish guard）。

articles/**・drafts/** の変更ファイルに、denylist.txt の語が 1 つでもあれば赤。

★ 単純であることが価値。大文字小文字を無視した**部分一致**だけで、
  正規表現も文脈判断もしない（すり抜けの余地を作らない）。
  文脈が要る判断（矛盾・推奨・誇大）は審査エージェント（judge_prompt.md）の担当。

使い方:
    python3 ci/publish-guard/check_denylist.py <file> [<file> ...]
    python3 ci/publish-guard/check_denylist.py --selftest
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DENYLIST = HERE / "denylist.txt"


def load_terms(path: Path = DENYLIST) -> "list[str]":
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    if not terms:
        raise SystemExit(f"{path} から語を 1 つも読めませんでした（書式が壊れた？）")
    return terms


def scan_text(text: str, terms: "list[str]") -> "list[tuple[int, str]]":
    """(行番号, 語) の一覧。行単位で照合し、どこで踏んだかを指せるようにする。"""
    hits = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        low = line.lower()
        for term in terms:
            if term.lower() in low:
                hits.append((lineno, term))
    return hits


def selftest() -> int:
    """検出力の自己確認。何も見ていない網はここで露見する。"""
    terms = load_terms()
    planted = (
        "本文です。\n"
        "接続先は keiba.cost-lab.jp です。\n"
        "KEIBA_EXP_FLAG を設定します。\n"
        "特徴量 m_popularity が効きます。\n"
        "stock の話。\n"
    )
    hits = scan_text(planted, terms)
    found = {t for _, t in hits}
    expect = {"keiba.cost-lab.jp", "KEIBA_", "m_popularity", "stock"}
    assert expect <= found, f"検出できていません: {expect - found}"
    clean = "地方競馬の検証記録です。ROI と 95% 信頼区間の話をします。"
    assert not scan_text(clean, terms), "無害な文を誤検知しています"
    print(f"ok  検出力あり（語彙 {len(terms)} 語）")
    return 0


def main(argv: "list[str]") -> int:
    if argv and argv[0] == "--selftest":
        return selftest()
    if not argv:
        print("検査対象のファイルがありません（何も変更されていない）")
        return 0
    terms = load_terms()
    failed = False
    for name in argv:
        path = Path(name)
        if not path.exists():
            continue  # PR で削除されたファイルは検査しようがない
        hits = scan_text(path.read_text(encoding="utf-8", errors="replace"), terms)
        if hits:
            failed = True
            for lineno, term in hits:
                # ⚠ 該当行の本文は出さない（ログにも秘密を残さない）。語と場所だけ
                print(f"::error file={name},line={lineno}::禁止リストの語があります: {term!r}")
        else:
            print(f"ok  {name}")
    if failed:
        print("::error::公開できない記述が含まれています。該当箇所を書き換えてください"
              "（語彙は ci/publish-guard/denylist.txt）")
        return 1
    print("禁止リスト検査を通過")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
