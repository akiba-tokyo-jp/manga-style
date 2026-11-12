# マンガ配布資産のprivate repo移管記録

移管先：`akiba-tokyo-jp/manga-style`（private、Actions無効）
元ソース：`akiba-infra` @ `ec37450c4ded797a0e1da85711d3d3acdcfb210d`
分離先の初回ソース：`b41ce9a8d5e9618305f77f55eb12b11cce3989b2`

## 完了した検証

- 182 Releaseを移管。移管後の全Releaseを独立したGETで再取得し、必要タグ集合・本文・draft/prerelease flagを元データと完全照合。
- binary asset 121 ZIP、951631649 bytes。全件のGitHub側SHA-256 digest・サイズ・uploaded状態をmanifestと照合。
- 旧形式の6アーカイブは、新repoのRelease本文だけから再構成し、全6件のSHAを照合。7639132 bytes。
- 合計127アーカイブ、959270781 bytes。画像の再生成・再encode・promptの付替えは行っていない。
- 新repoの1 ZIPを実バイナリとして再ダウンロードし、SHA一致を確認。最初の大きいZIPの再downloadは180秒でtimeoutし、部分ファイルを合格扱いにせず保存。別の小さいassetを認証付きAPIで取得して確認した。
- fixtureでは新repo指定・不許可repo拒否・downloadの`--repo`指定・通常の回帰入口への登録を確認。
- 全seedによる隔離起動で2756枝／2756組／5512画像の実SHA、HTML/API/画像、Anima空契約、匿名管理・内部操作拒否を確認。これは本番ではない。

全Release/asset ID、URL、本文SHA、画像ZIP SHA、旧形式再構成の証拠は [asset-transfer-receipt.json](asset-transfer-receipt.json)。

## 現在の配布元

`tools/manga_catalog/sample_bundles.json`、`explanatory_bundles.json`、`costlab-auth/manga/compare/records.json`は、このprivate repoを参照する。通常の`prepare_samples.py`の順で旧追加見本・比較画像・説明用2枚組を検査・stagingする。

画像はGitへ直接追加していない。アカウントの認可された`gh`または、このrepoに対する読み取り権限を持つGitHub tokenが必要。旧private repoへの自動アクセス権に依存しない。今回、Actionsの有効化・secret登録・workflow実行は行っていない。

## 今回変更していないもの

- 本番のDNS／Caddy／Compose／管理volume／公開・非公開の管理状態／認証／cron。
- 既存サービスの更新元や本番writer。旧repoのコード・Release・実データは削除していない。
- Cloudflare静的export／配備。次段階の設計は [Cloudflare移行の受入条件](../docs/cloudflare-static-migration.md)。

ソースと配布資産の分離完了と、本番サービスの移行完了を区別する。
