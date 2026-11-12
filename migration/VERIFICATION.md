# 分離時の検証

元commit: `ec37450c4ded797a0e1da85711d3d3acdcfb210d`

- 全manifestファイルのSHA-256と元blobを照合。マンガの配布元参照・回帰登録6ファイルだけの変更はsource-adjustments.jsonへ明記。
- ローカルの選択した検証入口は最終的に全exit 0。これは全試験・全運用の合格を意味しません。実ログと入口はverification/に保存。
- 元workflowはinactive保存、remote Actionsは無効化して読戻し。
- Docker build、VPS上のデータ照合、本番切替、外部DB・NEUTRINO・実Grok生成の統合試験は未実施。
- 初回の失敗・警告はログから削除していません。
