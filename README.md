# manga-style — マンガ絵柄カタログ

**private repository / source extraction stage**

`akiba-tokyo-jp/akiba-infra` の `ec37450c4ded797a0e1da85711d3d3acdcfb210d` からサービス関連ファイルを抽出しました。
初回は相対import・既存テストを保つため従来のディレクトリ構造を保持します。Git履歴の書換えではなく、元SHAと全ファイルのblob/SHA-256を `migration/source-manifest.json` に記録したsnapshotです。

## ソースと確認

- ビルドcontext：`costlab-auth/manga`
- 既存確認入口：`python -m unittest discover -s costlab-auth/manga/tests -p test_pair_release.py -v`（依存導入・外部条件は元ドキュメント参照）
- ファイルの分類：manifestの`owned`が本サービス、`reference`は共有infraの固定試験入力です。
- 本番Compose/Caddyの正本と配備権限は引き続きakiba-infraです。コピーした共有Composeを丸ごと本番実行しないでください。
- Docker未導入の調査環境ではDocker build/本番起動を確認できません。実行した検証は `migration/VERIFICATION.md` に記録します。

## 自動実行・本番変更を止めた移行

- 旧workflowは `migration/upstream-workflows/` に保全。`.github/workflows` には配置せず、このrepoのActionsも無効化します。
- secrets・.env・秘密鍵・実DB・学習済みモデル・本番volumeはコピーしていません。
- 本番の更新元・定期実行は切替えていません。新旧repoから二重に実行しないでください。
- 今後の切替ではimmutable image、既存volume名、ホストcron/排他/資源上限、rollbackを確認します。
- shared fixtureの変更はakiba-infra側の正本と併せて更新します。本repoだけで全サービスの設定を変更しません。

## 保持する外部依存

- 管理画面のcostlab-auth認証
- 本番volume costlab-auth_manga_style_data（今回移動しない）

## 配布資産の移管

182 Release・121画像ZIP・旧形式6アーカイブをこのprivate repoへ移管し、内容とSHAを再照合しました。[検証記録](migration/ASSET-TRANSFER.md)と[Cloudflare静的化の受入条件](docs/cloudflare-static-migration.md)を参照してください。本番の配備先・管理volumeは未変更です。

## Cloudflareへの配備

Workers + Static Assets向けのビルドと互換Workerを追加しました。詳細は[配備手順](docs/cloudflare-deploy.md)を参照してください。本番コンテナ・DNSはまだ切り替えません。

```sh
npm ci
npm run build
npm run dev
# 配備せずにWrangler設定を確認:
npm run check:deploy
```

Cloudflareではprivate repoの`main`、repo root、Build `npm ci && npm run build`、Deploy `npx wrangler deploy`を指定します。private Release読取用の`GH_TOKEN`がビルドsecretとして必要です。seedからのpreviewと、本番snapshotの引継ぎは別の工程です。

## 次の段階

このrepoでソースと配布物を検証 → 個別リリース経路を用意 → infra側の参照を切替 → 本番readback → 旧writer/ソースを整理、の順です。マンガのCloudflare本番切替も別段階です。
