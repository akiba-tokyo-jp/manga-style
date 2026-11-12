# Cloudflare Workers + Static Assets への配備

このリポジトリのルートからビルド・配備できます。Python/FastAPI は**ビルド時だけ**使用し、配備後は静的なHTML・JSON・既存JPEGと、URL互換性を保つ小さなJavaScript Workerだけで動きます。Docker、常設Python、DB、R2は必須ではありません。

## 最初に区別すること

- **対応コードのmainマージ ≠ 本番切替**。この設定には独自ドメイン、DNS変更、本番volume操作、GitHub Actionsの有効化を含めていません。
- GitHubのソースはprivateのままです。`workers.dev`に配備すると、従来と同じ公開カタログ/APIがインターネットから読めます。
- 初回はseedから作ったpreviewを`workers.dev`で確認してください。本番に管理画面での変更・公開停止・版がある場合は、**本番から取得した静止snapshot**で最終ビルドし、差分を確認してからドメインを切り替えます。
- Cloudflare Pagesの「出力フォルダだけ配信」ではありません。`/v1/tree`などの既存URL・query・CORS・モデル切替を保持するため、**Workers**を選んでください。

## ローカルで確認

必要: Node.js 22.12以降、Python 3（uvがない場合のbootstrap用）、private Releaseの読取権限。uvが既にある場合はその実行ファイルを使い、ない場合は`.build/bootstrap`のvenvに固定版uvを導入し、Python 3.12とビルド依存を隔離します。

```sh
npm ci
npm run build
npm run dev
```

`http://127.0.0.1:8787`で確認します。Windowsで再ビルドする場合は、先に`npm run dev`を停止してください。ファイル監視が`dist/assets`をロックし、正常な出力の置き換えを妨げることがあります。`npm run build`は次を行います。

1. このprivate repoのReleaseを取得する。アーカイブ全体SHA、既存prepare処理のmanifest・画像・promptの検証に合格した資産だけを使う。
2. 一時Storeを初期化し、既存アプリの公開readerからHTMLとAPI JSONを生成する。
3. `visible`、採用中のsample、失効していないcomparisonだけを書き出す。画像は再生成・再エンコードせず元のbytesでコピーする。
4. ファイル数20,000以下、1ファイル25 MiB以下を確認し、成功した出力だけを`dist/assets`へ置き換える。
5. `dist/build-report.json`に入力区分・総ファイル数・総bytes・最大asset・画像SHA一覧を残す。この記録自体は配備対象外。

取得済みの127アーカイブを使う場合:

```sh
npm run build -- --archive-dir /absolute/path/to/verified-archives
```

同じ指定は環境変数`MANGA_ARCHIVE_DIR`でも可能です。既存cacheのSHAが違う場合は上書きせずエラーにします。

認証は`GH_TOKEN`または`GITHUB_TOKEN`を使用します。ローカルだけは、どちらもなければログイン済み`gh auth token`から取得します。値を表示・ファイル保存しません。Cloudflare Buildsにgh CLIは不要です。

## Cloudflare管理画面の設定

Workers & Pages → **Workers** → Gitリポジトリから作成し、次を設定します。

- リポジトリ: `akiba-tokyo-jp/manga-style`（privateのまま）
- Production branch: `main`
- Worker名: `manga-style`（`wrangler.jsonc`と一致させる）
- Root directory: リポジトリのルート
- Build command: `npm ci && npm run build`
- Deploy command: `npx wrangler deploy`
- ビルド環境変数: `NODE_VERSION=22`、`PYTHON_VERSION=3.12`（環境側で既に満たす場合は追加不要）
- ビルド用secret: `GH_TOKEN` — このrepoだけの **Contents: Read-only** を持つfine-grained GitHub token
- はじめは独自ドメインを追加しない。公開先は`manga-style.<account-subdomain>.workers.dev`

GitHub Appでprivate repoを接続できることと、ビルド中にprivate Releaseをダウンロードできることは別です。`GH_TOKEN`は**ビルド用secret**に置き、Worker runtimeのvars・ブラウザ用変数・ソース・distに入れないでください。Cloudflare配備権限はWorkers Builds側で管理します。

`wrangler.jsonc`がWorker入口、`ASSETS` binding、`dist/assets`を指定するため、Pages用の出力ディレクトリ欄は使いません。`run_worker_first: true`と`not_found_handling: none`は必要です。削除すると内部の配信用bundleが直接返ったり、欠落API/画像がHTMLの200になったりします。

> 料金: 静的ファイルの保存・直接配信は無料でも、**この構成は互換性・モデル制御のため全リクエストでWorkerを通します**。Workerのリクエスト数・CPU時間の制限は別に適用されます。Freeで無制限に動くという意味ではありません。アクセス数やCPU使用量をpreviewで確認し、必要ならWorkers Paidを選んでください。

## 本番snapshotを使う場合

管理データはGitHubにも公開assetsにも載せません。既存運用の手順で、停止または整合性を確保して取得した**volumeのコピー**（`state.json`と`files/`）を用意します。稼働中volumeを直接指定しないでください。

```sh
npm run build -- --snapshot-dir /private/read-only-snapshot
npm run check:deploy
# 配備・切替が承認された後だけ:
npx wrangler deploy
```

`MANGA_SNAPSHOT_DIR`でも指定できます。snapshotはチェックアウトの外に置いてください。ビルド開始時に元snapshotと出力先・レポート先・archive cache・ビルド書込先の重複を検査し、入力を変えてしまう配置はツールのbootstrapやダウンロードより前に拒否します。入力は読み取りのみです。scratchにファイルをコピーし、Storeのseed import/refreshをsnapshotに適用せず、保存済み公開停止、採用prompt、sample、version、updated_atを保持します。カタログとsnapshotのID集合の不一致、token-mode API、不正な状態、symlink/junction、画像SHA不一致、欠落画像は失敗にします。

Cloudflare Buildsのseedビルドはこの本番snapshotを自動取得しません。最終snapshotを取り込む経路が確立するまでは、自動再ビルドが管理編集を反映するとは考えないでください。`dist/build-report.json`の`input_mode`が`seed-preview`か`snapshot`かを必ず確認します。

## 維持する公開機能

- `/`、`/search`、`/n/<id>`、`/styles/<id>`、`/api`、`/files/<id>/<name>`
- `/v1/models`、`/v1/tree`、`/v1/styles/<id>`、CORS / OPTIONS
- 日本語/英語、`lang`と`plang`の独立指定、`model`、モデル選択cookie、Genko用リンクとUser-Agent、`view=compare`
- 既存CSS、詳細ページの2枚組と実生成prompt、コピー時のモデル・分類・id、同名絵柄の識別
- カテゴリ・題材・特徴・AND検索・48件ずつのページ送り（**一覧の絞り込みにはJavaScriptが必要**）
- Animaは準備中の空モデル。GPTのpromptや画像をAnimaの生成物として返さない。

公開APIのoriginはアクセス先から組み立てるため、previewでも独自ドメインでも画像URLが同じ配信先を指します。`/admin*`、`/internal*`、state、token hash、待機prompt、再生成queue、pair-history、未参照画像は配備しません。管理・生成処理は引き続き保護された旧環境またはローカル側で行い、新しい静的snapshotの承認・ビルドが必要です。token認証の公開APIが必要になった場合は別実装が必要で、token-mode snapshotを公開に変換して配信することはしません。

## 検証コマンド

```sh
npm test
npm run test:python
npm run check:deploy
# npm run devを別terminalで起動した状態で:
npx playwright install chromium
npm run test:browser
```

Windowsで既存Edgeを利用する場合は`PLAYWRIGHT_CHANNEL=msedge`を設定できます。`check:deploy`はWranglerの**dry-run**であり、CloudflareへのuploadやDNS切替はしません。

`npm run deploy`はビルドから実配備まで行うコマンドです。実配備を許可されるまでは使用しないでください。初回公開後はHTML、API、画像SHA、Genkoクライアント、公開/非公開状態を実URLで確認し、それから独自ドメインを設定します。旧コンテナとvolumeはrollbackが完了するまで残します。

## 参照

- [Static Assets bindings](https://developers.cloudflare.com/workers/static-assets/binding/)
- [Worker-first routing](https://developers.cloudflare.com/workers/static-assets/routing/worker-script/)
- [料金と制限](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/)
- [プラットフォーム制限](https://developers.cloudflare.com/workers/platform/limits/)
- [元の移行受入条件](cloudflare-static-migration.md)
