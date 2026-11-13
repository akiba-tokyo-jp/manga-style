# Anima 絵柄の作成・公開

## 正本と分離

- `content/anima-turbo/catalog.json` が Anima 専用の公開定義。GPT Image の既存定義・画像・プロンプトは変更しない。
- 名称と観察説明は日本語・英語。`prompt.en` は再利用する絵柄部分、`sample.prompt.en` は実際に送信した全文。日本語訳を実生成プロンプトとして登録しない。
- `requested_settings` と `reported_settings` を分ける。seed と negative が未指定なら null のまま残す。モデル名・実 job ID・画像SHAを保存する。
- 現行サーバーは Anima Turbo v1.1。初回は近年の漫画6作品の公式無料試し読みを実見し、一般化した線・顔・体型・陰影から7絵柄を収録する。作品名・作家名を生成指示に入れず、出版社の画像は公開ZIPや生成参照へ含めない。
- 微妙な色味、ハッチング量、画角、指定と異なる頭身などは観察説明に残す。原PNGを白黒化・修正して適合したように扱わない。別人物・別場面の再現性は未確立と明示する。

## 必須の2枚組

Animaの各絵柄は別々に生成した原画を2枚持つ。1枚目 `mixed-gender` は男女が同じ漫画場面に登場するもの、2枚目 `showcase` は絵柄の魅力を表す構図とキャラクター。棒立ち・無地背景の比較試験やサムネイル/切り抜きを代用にしない。既存項目も改訂対象で、1枚の旧形式を2枚完了と数えない。

新版manifestは `schema: 2`、各定義の `samples` は上記順の2件。各原画に別のnative job/画像SHA、実送信 `prompt.en`、requested/reported settings、SHAに結び付けた `visual_review`（self-reviewed、日英の実見説明）を保存する。両方の全文に同じ再利用絵柄部分を含める。コードのroleやレビュー印だけで実際の男女や魅力を証明したことにはならないため、原画で点検する。欠陥・文字様印・意図しない人物・片方の性別しかいない等は保留/再生成。意図の通る複数コマは、誤って増えた人物や人物の併記とは区別し、指定からの残差として実見説明に残す。

API `samples[]` と詳細ページは2枚それぞれの原画、全文コピー、設定・job ID、観察説明を返す。旧 `schema: 1` は過去データの読み込み互換のため維持するだけで、新しい2枚要件への適合を意味しない。旧原画/プロンプトは履歴と不変Releaseに保持し、意図的改訂でversionを上げる。GPT Imageの定義/2枚組は変更しない。

### 自作原画を参照した見本

参照を使う場合も、2枚は別native jobの未加工原PNGとする。同一項目のもう一方を入力にした場合は、`requested_settings.references_used` にその `source_role` と原PNGの `sha256` を保存し、実際にダウンロードできる原画と一致させる。条件付き生成を「条件なしの独立抽選2回」と説明しない。出版社画像を入力へ流用しない。

SnapRef CSの見本は詳細の観察・制約欄に入力関係を明記する。再投入する人は、参照元の原画、該当画像の実英語全文、`reference_adapter: snapref_cs` 等の実設定を使う。英語文のコピーだけで同じ参照条件を再現したことにはならない。APIではこれらの設定を `samples[].settings` に返す。

PS5 Image Front経由の実出力は `transport_client: ps5-image-front` と証拠の出所を残す。共通の `provider: ps5-anima` はPS5のAnimaバックエンドを指し、Hermes pluginを呼んだとの意味ではない。このクライアントが実送信した `seed: -1` と空文字negativeを、未指定のnullへ置き換えない。返っていない確定seedは不明のままにする。nativeの完了・実step・参照GPU評価・正規化入力SHA、およびnative画像と保存PNGの一致を確認し、参照GPU動作と視覚的な絵柄一致は別に点検する。

## 次の追加

1. 原画と英語全文を生成ごとに保存し、実見して重複人物・文字様印・手足の破綻を点検する。不適合な試行も私有の制作記録には残すが、公開manifestには入れない。
2. 公開する原PNGと384×512の白余白付きJPEGサムネイルだけをZIPにする。各memberは `<anima-id>/<sha256>.png|jpg`。原画像のSHAとサムネイルSHA、ZIP全体SHAを固定する。
3. このpublic repoのReleaseへ新しい不変tag/assetとして登録し、匿名ダウンロード往復のSHAを検証する。秘密・ローカルパス・出版社画像を含めない。
4. `catalog.json` の `bundles` と `entries` に追加する。既存ID・画像・プロンプトは上書きしない。既存項目を意図的に改訂する場合はversion/updated_atを更新する。
5. ローカル検証 → 独立コードレビュー → PR → mainマージ。GitHub Actionsは新設・有効化しない。Cloudflare Workers Buildsによる通常の公開を確認し、公開API・画像SHA・日本語/英語の表示とコピー操作を実URLで読み戻す。マージだけで公開完了とはしない。

## ビルド

既存の `npm run build` が Anima の固定ZIPも取得する。`anima_catalog.py` がZIP全体SHA、member SHA、重複ID、パス、英語プロンプト、実モデル、実job、画像形式・画素数を検査する。検証後、既存の原子的stagingに Anima の一覧・詳細・API・画像を加える。失敗した出力は公開用の前回出力へ置き換えない。

```
npm test
npm run test:python
npm run build
npm run check:deploy
# 別terminalで npm run dev を起動してから:
npm run test:browser
```

## 公開API

- `/v1/models`: Anima の `status=available` と実登録件数。
- `/v1/tree?model=anima-turbo`: Anima 絵柄をフラットなlevel 1として返し、`category` に共通の大分類IDを持つ。UIの分類階層とは別の投影。
- `/v1/styles/<anima-id>?model=anima-turbo`: Anima 専用のプロンプトと見本。言語指定は名称・説明にだけ作用し、生成指示は英語。
- `/files/anima-turbo/<id>/<sha>.png|jpg`: モデル専用かつ内容ハッシュ付きの画像URL。既定モデルやUI cookieに依存しない。
- model省略APIは従来どおりGPT Image。既存GPT IDをAnima APIで要求しても借用しない。旧絵柄のモデル切替ページは、その絵柄にAnima見本が未登録であることを表示する。

## 分類ごとの拡張目標

既存10大分類と、Anima専用の「その他・成人向け参考」を各最低30絵柄に拡張する（合計330以上の目標であり、達成済み件数ではない）。計画・生成・視覚点検・採用・main統合・ユーザーによる配備を別々に数える。名前や色だけを変えた近似例は独立した絵柄として件数に加えない。

`other` はAnimaの `model_roots` と表示ラベルだけへ追加し、GPTの既存階層・カード・件数は変えない。該当定義には `reference_context: adult-manga` と `sample_content: non-explicit-fully-clothed-adult` を必須とする。これは分類上の契約であり、画像の安全性や絵柄差をコードだけで証明するものではない。原PNGの視覚確認も必要。見本は成人の着衣・非露骨な内容にし、出版社画像は配布や生成入力へ使わない。

## 今回のビルド担当

ユーザーの最新指示「ビルドはこちらでできるから、マージしててってください」に従い、この依頼ではソースと公開資産の検証・PR/main統合までをこちらが進め、ビルド/配備はユーザー側が担当する。Cloudflare Workers Buildsの失敗を成功扱いしたり、mainマージを本番公開済みと呼んだりしない。初回PR #5はこの未解決の外部ビルド状態を開示した上でマージした。

## 第2便の追加

`anima-contemporary-002` の固定ZIPから、潤む大きな瞳、黒い服と強い顔影の動作漫画、丸眼鏡と丸頬の人情コメディを追加する。最初の7定義は変更せず、合計10定義。新たに実見した4作品の公式無料プレビューは部分画像として観察し、ページ全体の構成や厳密な頭身をそこから推定していない。文字様印・空の吹き出し・人物重複が残る他の5試行は非公開。動作漫画の服や見た目の性別、輪郭の粗さなどの差も観察説明に残す。

## 初回の保留

`anima-awkward-indie-daily` は、表情が気まずさより薄笑いに寄り、機材などに小さな記号状描写があったため未収録。人物のアップと全身の併記、同一人物3ポーズの試行も採用画像へ混ぜず、単一人物に直した見本を使用する。
