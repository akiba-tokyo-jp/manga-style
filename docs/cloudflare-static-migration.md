# Cloudflareへの静的配信移行（未実施・次段階）

## 現在の位置

このrepoはakiba-infraから分離したprivateなソース管理先です。公開サイトのDNS・本番コンテナ・管理volumeは変更していません。以下は移行の設計と受入条件であり、静的exportやCloudflare配備の完了報告ではありません。

## 推奨構成

- private repo：カタログ定義、採用manifest、画像／実生成promptの結合、試験、公開用export。
- ビルド：公開対象だけをHTML・検索用データ・Genko互換JSON・採用済み画像へ書き出す。
- 配信：Cloudflareの静的asset配信。検索・特徴フィルタ・ページ送り・日英／モデル選択はブラウザ側。
- 互換ルーティング：必要最小限のWorkerで既存のsuffixless APIとqueryによる応答選択を維持する。
- 画像：まず静的assetの実測件数・最大サイズを確認し、必要な場合だけR2へ分離する。
- 管理：公開配信から分離。初期はローカルまたは既存の保護環境で編集・承認し、検証した公開snapshotを配備する。

管理画面の廃止、Web管理APIの追加、API token modeの廃止／移植、Cloudflareプランは別途決定する。純粋な静的ファイル配信だけでは認証付き編集やtoken管理は行えない。

## exportの入力と保護

1. 本番volumeを読取snapshotとして取得し、元state・画像・復旧履歴を保全する。今回のGit分離では本番データを取得していない。
2. Store初期化はrefresh・seed取込・保存を行うので、本番volumeへ直接接続しない。必ずsnapshotのコピーを使う。
3. `effective`／`visible`／比較の失効判定を適用し、公開中の枝・子孫・現在採用された画像だけを抽出する。
4. raw `state.json`、token hash、待機語、再生成queue、pair-history、退避画像を配信物へ混ぜない。
5. JPEG bytes・SHA、branch ID、完全な絵柄promptと各sampleの実生成prompt、版・updated_at・白黒／カラー区分・縦横比を保持する。移行のための再生成・再encodeをしない。
6. exportは一時出力で全件検証し、成功した公開snapshotだけを原子的に採用する。途中出力を公開しない。

## 互換契約

- `/`、`/n/<id>`、`/styles/<id>`、`/search`、`/api`。
- `/v1/models`、`/v1/tree`、`/v1/styles/<id>`、`/files/<id>/<name>`。
- APIの既定は日本語／GPT Imageで、model選択はCookieに依存しない。未知modelの400、Anima未登録の空tree・style/fileの404を維持する。
- `?lang`、`?plang`、`?model`、モデル選択保持、検索／特徴filter／pagination、Genko用の表示と`genko://use-style?id=...`を確認する。
- 同名styleをID・分類経路で区別し、コピー文や共有URLの内容を保つ。
- APIのfield、children、reference、CORS、OPTIONS、HTTP status、Content-Type、cache policyを比較する。
- 通常閲覧とモデル比較を混同せず、元画像／元promptが変わった古い比較を公開しない。
- 非公開化した枝・古いURLを、検索・API・画像・キャッシュの各入口でどう失効させるかを決める。

HTMLのquery組合せをすべてSSGする必要はない。日英・モデル別JSONを作り、小さなWorkerで既存API URLを維持すると、Genko側の変更を抑えられる。Workerを一切使わない方式を選ぶ場合は、query互換と下流クライアント変更を先に評価する。

## 容量・配備

Cloudflareの公式上限は移行時にも再確認する。

- [Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/)
- [Workers limits](https://developers.cloudflare.com/workers/platform/limits/#static-assets)
- [Pages limits](https://developers.cloudflare.com/pages/platform/limits/)

調査時の静的asset上限はFree 20,000 files、該当有料プラン100,000 files、単一25MiB。exportの実ファイル数・最大サイズを機械集計し、HTML shell共用・代表thumbのみ配信・R2分離などを選ぶ。登録枝数だけで収まると決めない。

private repoと公開Webサイトは別の公開範囲。ソースをprivateのまま、従来の公開カタログだけを配信する。previewにも未公開データを含めず、必要なら閲覧保護を設ける。

## 受入と切替

1. 同一snapshotの現行アプリと静的exportで、全ID集合・API値・画像SHA・非公開判定を比較。
2. 日英／モデル／検索／コピー／Genko連携、スマホ幅・PC幅、404／CORS／headersをプレビューで確認。
3. Cloudflare上の実配信bytesとassetの到達性・容量を確認。
4. DNSを独立に再確認し、完全一致のmanga hostを切り替える。今回の調査では当環境から既存hostのDNSが解決できなかったため、現在の到達性を受入済みとしない。
5. 切替後の公開URL・Genko API・画像・キャッシュをreadback。
6. 旧コンテナ・volume・Release・DNSの復旧手順を保全し、問題があれば戻す。
7. 安定した受入後だけ旧配信経路・古いwriterを整理する。他サービスの認証・Caddy・メール制限を巻き込まない。

Docker build・本番snapshot取得・Cloudflareアカウント設定・DNS切替は、今回のソース分離とは別の未実施項目です。
