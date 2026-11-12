# マンガ・アニメの絵柄見本帳（manga.akiba.tokyo.jp）

## 複数モデル・画像一覧の構成

- 共通の大分類から画像一覧へ進み、絵柄を選ぶと詳細を表示する。旧L2は必須通過ではなく、題材・雰囲気の任意フィルタ／見た目そのものを表す絵柄として残す。同名でもID・親の描法・実生成文が異なる枝を統合しない。
- 常設の `GPT Image` / `Anima Turbo` 切替を置く。`?model=gpt-image` / `?model=anima-turbo` を共有URLに含め、明示URLを最優先、次に1年間の `manga_model` cookieを用いる。cookieを拒否しても明示リンクとフォームで選択を維持する。
- Anima Turbo は準備中の空枠のみ。画像・実生成文・設定・コピー・Genko操作は未登録。GPT Image の資料をAnima名義で表示・配信しない。データ収集・新規画像生成は今回行わない。
- GPT Imageの既存2756枝5512枚、ID・実生成プロンプト・版・来歴は保持する。特徴フィルタは既存プロンプトの指定を検索するもので、出力が指定どおりだと保証する採否gateではない。
- 大分類の従来URL `/n/<id>` は画像一覧へ。大分類自体のプロンプト詳細は `/styles/<id>`、旧L2/L3の `/n/<id>` は直接アクセス可能。詳細には絵柄プロンプトと各見本の実生成プロンプトを分け、コピーにモデル名・分類・IDを付ける。
- 既存 `/v1/tree`、`/v1/styles/<id>`、`/files/…` はcookieに依存せずGPT Image互換を保持する。明示Animaのtreeは空、style/fileは404。`/v1/models` でモデルの状態・登録数を取得できる。APIの既存認証/CORSは維持する。
- 通常閲覧とモデル比較は分ける。比較でもAnima側は空欄とし、異なる生成結果を同条件の性能比較と称しない。日英画面とプロンプト言語は独立して選べる。
- 回帰 `test_model_gallery.py` は `tools/manga_catalog/validate_explanatory.py` の既存8コマンドの後に1回だけ登録する。GitHub Actionsは起動・再有効化しない。既存画像seedは再生成・再encodeしない。


## 説明用2枚組：女性・コメディ（2026-11-10）

- 22枝44枚（42mono＋2color）を1画像1独立process/sessionで生成。初見44whole＋必要な限定9wholeを保存し、`chibi-comic`／`bold-comic`／`tall-cool`／`retro-shojo`の4組8monoを採用、18枝は旧公開を保持する。原full/partial/confirmed/notesと主担当の`adopt_with_differences`は別記録。
- 配置固有doodleの黒点2個・鼻なし・髪3形・服しわ2・背景1形を他枝へ足さず、この枝では免除しない。flat-colorの参照fieldだけ現親から解決し、親の顔/頭身/汗を全枝へ一律追加しない。両枝とも今回未採用。全枝の6field/key/tags、既訂正と日英length guardを保持。
- 採用の頭身は髪/顎/足の境界幅を伴う近似。bold appの元約3〜3.5と指定4〜5との差、tall repの約7.5〜8.3、retro repの約8〜8.5、衣服丈/背景距離/生成り色などを残差として保存し、厳密一致や全語完全再現とは呼ばない。別の小頭長胴脚構築は近似で肯定せず、natural/rough/hatching/realはhold。
- picture-book appはflat tone自体の肯定と人物の量過多を分離。背景の許可されたtoneを人物量へ加算せず、白余白だけでも少量を肯定しない。hair-detailの見える段階tone/白抜きの肯定も他の未確認を消さない。F事前依存でcompanion2件、続くI人物構築1件を取消し、肯定や公開必須欠落へ置換しない。
- 限定E/F/Hの8質問には出力JSON例のquote用backslash差があった。人物構築/描法の原文・程度・範囲はbyte同一と主担当が照合したが、元質問/実送信/rawと原integrity未確認を保全し、exactやfresh全体独立契約passへ改称しない。初見B/Cの出力手順差も保存。画像の追加実見・再生成でmetadataを修理しない。
- 旧60bundle554組prefixを保持し61bundle558組候補へ新ZIPだけ追加。新JPEGはL/元比率/長辺1024以下、thumbは白余白384×512。公開はローカル回帰・隔離Store・日英UI・独立review・PR/Release往復・merge後、GitHub Actionsを起動せず新seedだけ直接配置する。本番receipt全SHA/fullreadback前に558publishedとは呼ばない。認証/Caddy/workflow/UID/volume/network/CPU0.5/RAM384MiB/PID128・他service・rollbackは不変。

## 説明用2枚組：青年・日常（2026-11-09）

- 21枝42monoを1画像1独立process/新turnで生成、42完成/42固有session/拒否0未送信0。全42初見27partial15full/textnone42と限定8wholeを保存。14positive rolesから両役肯定の4pair8枚（deadpan-seinen/fine-tall/retro-seinen/sharp-stylish）だけ公開候補、17枝は旧公開保持。追加生成0、全語完全再現とはしない。requested gpt-image-2.6-sunburst/reported_model null/model_enforced falseを分離。
- source9/実API21＋親/6項目を照合。成人女性/たたんだ無地布/部屋の窓辺、成人男性/小布袋/家の玄関をsceneへ分離。親の人物構築・17歳キャンプscene・旧職業ラベルは継承しない。default20＋graphite1の全mono。monoをmediumNoneと同一視した初回plannerは要求前assert失敗/outputs0で保存、実graphiteのexport/media/6項目を確認しplanner/dryrun成功。既訂正fieldはsource6一致時だけ保持し、必要な背景整合は元以下の両言語で行う。
- 初見A18/B19はactualcall/session/raw/question/image/fullstyleSHAへ親結合し、各15API27tool/479.37秒21365bytes・542.13秒22937bytesで契約適合。native体型6件はgraphic-flat別役のみ標準構築を肯定、他5件は小頭/長い胴脚等で未確認として保持。約一頭の境界差だけの自動否定や寸法式なし。
- graphic-flat代表の硬鋭輪郭は別のwhole確認で未成立。曲線の存在自体を拒否せず、輪郭の張り/接続/折れを確認した。独立hold確定後は別役の線質を追加確認しない。graphite代表もwholeで明るいシャツ主面の粒調を影限定と確認できず、元fullを別保持。どちらも好ましいboolを得る反復実見なし。
- deadpanは白地/細い均一線/簡略目、fine-tallは細線/細いつり目尖顎/長身、retroは強弱線/粗網点/約7頭身、sharpは大黒面/強弱線/細いつり目尖顎/長身を当該pairで確認。広いトーン量、画角/靴/局所階調等の残差は元notesと採否理由へ保存。背景fieldの表面質感抑制をズボンへ拡張せず、瞳禁止/全直線/明部の構造線ゼロも足さない。主描法未確認の枝は他の美しさで救済しない。
- 旧46bundle497pairを先頭完全保持＋4で47bundle501候補。画像/ZIPはgit外の固定SHA配布、変更はdocs2＋registryだけ。同SHA17実装とfresh Gambling converterの肯定componentのみreuseし、新payload/採否/ZIP/実行は今回の独立公開review対象。
- 本人の「Github Actionsは動かさずに配置しなさい」に従いdispatchしない。回帰/隔離Store/UI/独立review/PR後に稼働アプリ同SHAの上へnewseedだけnetwork-free buildし、manga-styleだけ直接再作成。volume/network/security/CPU0.5/RAM384MiB/PID128と他サービス、Caddy/認証/権限/保護設定を保持。ローカル試験をCI成功と呼ばず、本番全受入receiptの正保存・全evidenceSHA/readback後だけ台帳publishedへ進める。旧image/composeを固定保持して復旧可能にする。

## 説明用2枚組：青年・アクション（2026-11-08）

- 25葉50枚を1画像1独立process/新turnで生成し50完成50固有session/拒否0未送信0。48mono2color、初見49none1uncertain/原寸23検査23role/肯定27role。両役positiveの6組12枚（bold-black/fine-tall/graphic-flat/muscle-hatch/muscle-mass/sharp-stylish）だけ候補、hold19は旧公開維持。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engine独立保証なし。
- 成人女性倉庫備品係の角箱/低い小結び髪と成人男性荷捌き場点検員の浅い角盆/刈上短髪、作業服/倉庫入口/通路をscene分離。hot代表は1時点の踏出し、体型枝は両役全身、標準静止代表は顔と手/別役全身。旧L3の約30歳殺し屋・拳銃・昼の立体駐車場、旧L2スーツ緩ネクタイ男性・夜の駅ホームscene不継承。mono24枝へ親の荒線/半顔ベタ/鋭目/眉間しわ/動線を自動追加せず実6項目だけ。
- 源5/25API＋親/実6項目/medium24None1ranking-color/adjustments全空/bg5keys(colorplain,dense,effect,normal,simple)を照合しunknown停止。color1枝だけreference型line/eyesを実L3＋親APIの少数で荒い強弱輪郭/細鋭目と深い眉間しわへ具体化、肌髪服の彩色を保持しmonoの半顔ベタ/網点義務を持込まず生成。原画は彩色されたが、両役とも速く荒い少数輪郭の主描法が弱いという元所見からholdし、美しさや彩色成功で救済しない。
- hatch/engraving5枝の顔・背景tone矛盾を生成前に元以下で整合。初回plannerは同sourceの既訂正fieldへ再amendしてlength guardで停止。実source/actualcall/error/jobs0attempt0request0/dryrun未実行を保存し、既訂正field保持・未訂正だけの整合で再planner/dryrun成功。guardは不変、画像要求前に全role/style/jobdigest/源SHAを確定した。
- 標準体の別役は全身nativeでgraphic-flatのみ約7.5頭身・標準胴脚構築を概ね肯定し近似採用、厳密6〜7保証なし。他15roleは当該原寸の推定幅と胴脚構築から6〜7未確認としてhold。代表hotのtone-layered/americanは約7〜7.5・踏出しと髪/顎/前後靴の境界幅を伴う標準構築を肯定したが、別役holdを救済しない。数字1頭差だけの自動合否/厳密寸法式なし。
- graphic-flat代表は原寸で人物自身の襟先/肩/袖/手の硬く明瞭な輪郭・平らな白黒面と、短い上瞼/小瞳の簡潔な目を肯定。曲線や黒瞳の完全禁止は加えない。fine-tall代表は襟/肩/袖/手/ズボンの主輪郭を髪ベタ/まつげ/陰影線と分離し細く概ね均一を原寸肯定。少量より広いトーンは元notesへ残す。
- brush-wild代表は原寸で人物の大きな線幅変化とカスレの併存を未確認、背景textureで救済せずhold。webtoon別役は細い鼻筋1本/小顔/切れ長目を肯定しても独立した長いまつげ未確認、男性免除や太いまつげの新義務なし。nineties別役は尖顎肯定でも眼裂横長で縦長大目未確認。代表の棚上小箱の文字様印はuncertain保持、別役独立holdのため文字だけを消す追加実見なし。
- inkwash代表のにじみとstipple代表の細均一線/点密度の組合せは元初見の未確証を保持し、別役独立体型holdがあるため余分な実見で合格flagを得ない。肌・顔の黒影、網点面/白抜き、骨太構築等の当該肯定は別predicateと分離。muscle-hatch採用は太輪郭/彫り顔太眉/骨太/ハッチングと白い明部を当該画像で肯定し、木箱/床/靴の細線量や代表の浅い肘曲げの残差も保持。全語完全再現、表面質感の完全無描写、実画材/工具/物理枚数/実年齢の保証なし。
- 同role複数原寸をlistで保持し、actual call/原画SHA/region/exact質問へ結合。原fit/defining_visible/nativefalseと主担当decision/correction_notesを分離、positive siblingでhold pair救済なし。採用12枚は全monoのためL/長辺1024以下/元比率保持、thumbだけ白余白384×512。builderは各job.expressionによりL/RGB分岐を保持し、holdのcolorをmono化して公開しない。
- 旧38bundle460pair全record保持＋6=39bundle466候補。固定SHAassetでJPEG/ZIPをgitへ置かず、変更registry+docs2のみ。同SHA17技術所見reuse、通常回帰/隔離Store/UI/独立review/PR/既存サービス別Actions/本番全受入は別gate。廃止CI/Caddy/認証/権限/workflow保護不変。receipt正保存fullreadback全evidenceSHA後だけpublished、復旧はrevert PR/通常Actionsとvolume pair-historyの旧node/旧画像復元確認まで。

## 説明用2枚組：少女・ペン線だけの端正な少女漫画（2026-11-08）

- 21葉42monoを1画像1独立process/新turnで生成、42完成/42固有session/拒否0/未送信0。literal初見41none1uncertain、原寸32検査25roleをactual call・exact質問・region・原画SHAへ結合。肯定22roleから両役positiveの5組10枚だけ候補、hold16は旧公開維持。採用bold-comic/elegant/gothic/round-eyes-bright/tall-cool、追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engine独立保証なし。
- 成人女性版画資料室案内係の薄い四角ケース/顎沿い短直毛と成人男性展示会館備品係の短い筒/襟足短い横分け髪、服・入口・広場をscene分離。旧17歳図書室の巻き毛/丸襟リボン/カーディガン/本抱えscene、L2古書店男女の本と川沿い振返りscene、親のアーモンド目/虹彩放射線と1小光/面長細首/ペンのみ・トーンぼかし不使用/短線密度陰影等をL3へ持込まず実6項目だけ。source5/21API＋親/mediumNone/adjustments空/bg5keysを照合しunknown停止。hatchingとpatternpenの背景tone衝突を生成前に元以下で整合、柄枝の無地服制約だけ除く。inspector/planner/dryrun全exit0、実call/result/実stdout/全digest/要求前attempt0request0を保存。
- white両役は全身native約6〜6.5/6.5〜7、長い胴脚で4〜5低頭身未確認。bold代表は髪込み約3.6〜3.7/髪除くと約4、別役は髪込み約3.3〜3.5/髪除くと4弱、髪/顎/靴境界の数え幅と低頭身構築を原寸肯定し、下限寄り近似で採用。厳密4〜5やstrict4以上の保証ではない。数字1頭差の自動合否や厳密寸法式は追加しない。
- standard別役の全身nativeはnatural約8〜8.5/modern約7.8〜8/dense約8.5〜9.5/hatching約7.8/pattern約9、境界差だけでない長い胴脚の構築から6〜7未確認でhold。一方rough約7.2/clean約7.3/pen-classic約7〜7.5は標準構築を肯定したが、独立した眼の大白光predicate未確認が残りhold。clean代表の輪郭は原寸で襟/肩/袖/手/上着へ照合し黒ベタ/太まつげと分離して細く概ね均一を肯定、初見所見は不変。
- hair代表約7.5〜8、classic代表髪込み約7.4/髪除けば8近く、nineties代表約7.7〜8前後は、各全身nativeのすらり構築を肯定し近似評価。hair両役とnineties代表のトーン濃淡面と白抜きも原寸肯定、全部位同時併存・物理トーン枚数・実工具の義務は追加しない。ただしhair別役は瞳の白光が小白点/細い抜きで大白光未確認、nineties別役は尖顎肯定でも眼裂横長で縦長大目未確認のためpairhold。clean/rough/pen別役の小白点も同様で、男性免除や極端な誇張/面積数値条件は加えない。
- pencil代表の原寸sampleで系統点径gradは未確認、別役は元grad/体型未確認のまま追加原寸なし。decor/classic代表左背景は規則的配列を保つ網点径変化を原寸肯定、別役左背景は粒/密度差と区別できず未確認でhold。cropは検査sampleで部位限定の義務ではなく、保存全景にも別部位の確証なし。全図不使用までは断定しない。別役の眼/体型未確認も保存し、不採用画像を救済するだけの追加実見は行わない。
- retro両役とstipple別役は原寸で独立した数本太まつげを未確認。retro代表白光個数も未確証、retro/stipple別役の白光2〜3は肯定。hatching代表の初見textuncertain（扉付近小札の文字様印）は、別役が独立体型holdのため追加原寸をせず保全。可読不能だけで無文字合格にしない。元fit/defining_visible/native旗と主担当採否を分け、同role複数原寸はlistで保存。全語完全再現/実年齢職務/物理画材工程の断定なし。
- 採用画像の元比率保持/長辺1024以下/L、thumbだけ白余白384×512。旧37bundle455pair全record保持＋5で38bundle460pair候補。画像はgit外の固定SHAasset、変更registry+docs2のみ。実caller build_publication.pyから同SHAStore.process_imageのL/RGB分岐と比率保持へ委譲するため、caller inline convertや別styles JSONファイル、ZIP内へ外部provenance metadataを重複させる義務はない。request英語strはjob.prompt.enへ、manifest内日英promptはdictとして比較し、原画/job/sessionを外部role provenanceからexact JPEGmemberSHAへ結合する。
- 通常回帰/隔離Store/UI/独立review/PR/既存サービス別Actions/本番全受入は別gate。廃止CI/Caddy/認証/権限/workflow保護は不変。receipt正保存fullreadback全evidenceSHA後だけpublished、復旧はrevert PR/通常Actionsに加えてvolume pair-history/旧nodeと旧画像の復元確認まで。preview/prod geometryが同一SHAでもactual origin/URL/呼出を別結合し、件数とbytesの単位を分ける。

## 説明用2枚組：少女・昭和の星の瞳（2026-11-08）

- 22葉44monoを1画像1独立process/新turnで生成し、44完成/44固有session/拒否0/未送信0。literal全44初見43none/1uncertain、原寸22件19roleをactual call・exact質問・region・原画SHAへ結合。肯定21roleから両役positive6組12枚だけ候補、16枝は旧公開維持。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engineの独立保証なし。
- 採用はart-nouveau/chibi-comic/elegant/gothic/pen-classic/round-eyes-bright。成人女性音楽資料室案内係の丸ケース（肩直毛/長袖ブラウス・腰丈上着・ふくらはぎスカート・平短靴）と成人男性演奏会館備品係の蓋角箱（短く刈った髪/長袖シャツ・袖なしベスト・長ズボン・平短靴）、入口と広場。旧温室の花受渡し/巻き毛とバラ髪飾り/花束庭椅子scene、親の巨大星瞳/光輪/放射まつげ/幼丸顔約5頭身などをL3へ加えず実6項目だけ。
- source5/22API＋親/mediumNone/adjustments空、実bg6keysを明示しunknown停止。ornamentは植物曲線と大円、decorとは別の実語で、両者とも疎scene。初回planner/dryrun44はexit0だったが要求前にpattern-penの無地服対刺繍/背景flat-tone対no-toneを検出し、初回実code/4JSON/callを保全、attempt0/request0。当該枝だけ服sceneから無地制約を除き、背景を元以下の両言語で白へ整合。hatching背景も元以下で整合。他21枝jobsは完全不変、訂正planner/dryrunもexit0。生成前の準備訂正であり追加画像要求ではない。
- bold代表は原寸約3.4頭身、大頭/短胴短脚で4〜5未確認。rough別役約7.5〜8、pattern別役約8〜9、hatching別役約8は長い胴脚の構築から6〜7標準未確認でhold。pen別役は約7頭身強/境界で7〜7.5、標準胴脚構築を肯定し近似採用。clean別役も約7.2を肯定したが、別predicateの大白光未確認でhold。数値1頭差の自動合否や厳密寸法式は追加しない。
- digital/pencil代表の衣服等、decor/classic代表の背景原寸で系統的点径gradは未確認。部位は検査sampleで限定義務ではなく、全景にも別部位の具体的確証なし。別役grad原寸未実施と目/体型の未確認を保持し、全図不使用とは断定しない。comic代表の肩袖/裾/スカートの主輪郭並走線は原寸肯定、別役は縫目/しわと異なるラフ重ね線が未確認でpairhold。
- hair両役の衣服トーン濃淡面と髪の鋭い白抜きは原寸肯定、代表約7.7/境界で8前後もすらり構築を肯定。しかし別役の瞳内白光は小白点/細い抜きで大白光を未確認、pairhold。全部位にトーン面と白抜きの同時併存義務は加えず、物理枚数/実工具は断定しない。
- retro/stipple/layered別役の独立した数本太まつげは原寸未確認。retro/stippleの白光2〜3個は肯定、layered個数は未確証。nineties別役は尖顎肯定だが眼裂横長で縦長大目未確認。男性免除なし。retro代表の8頭身/光個数とnineties代表の縦目未確証も追加実見せずholdへ。dense代表は背表紙の未解消文字様印を原寸確認、confirmedtrueはその存在で無文字合格ではない。可読文字/譜表音符/罫線/陰影の所見は分離し、別役の体型不確実さも保持する。
- 元fit/defining_visible/nativebooleanを主担当採否と分け、複数原寸は同roleでもlistで保持。初回件数診断のnative_roles44はdefaultdict空list挿入による表示誤りとして訂正し、実22検査/19roleの原所見は不変。トーン量/線量/背景設備・衣装細部/低踵/画角外等はrole別notesへ保持、全語完全再現・画材・物理工程・実年齢/職務の断定なし。
- 固定assetは12JPEGの元比率保持/長辺1024以下/L、thumbだけ白余白384×512。旧36bundle449pair全record＋新6組で37bundle455pair候補。実caller build_publication.py→同SHAStore.process_imageのL/RGB分岐を結合し、変換literalをcallerへ重複要求しない。変更はregistryとdocs2のみ、Caddy/認証/権限/workflow/保護設定は不変、廃止CI復活なし。回帰/隔離Store/UI/独立差分review/通常PR/既存サービス別Actions/本番全受入を別gateとし、receipt正保存fullreadback全SHA後だけpublished。復旧はrevert PR/通常Actionsに加えてvolume pair-history/旧nodeと旧画像の復元確認が必要。

## 説明用2枚組：少女・70年代の乙女ちっく（2026-11-08）

- 21葉42monoを1画像1独立process/新turnで生成、42完成/42固有session/拒否0/未送信0。literal全42初見41none/1uncertain、原寸20件をactual call・exact質問・region・原画SHAへ結合。肯定22roleを保存し、両役positive7組14枚だけ候補、14枝は旧公開維持。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engine独立保証なし。
- 成人女性植物資料室案内係の丸ケース（耳を出す短髪/長袖ブラウス・腰丈上着・ふくらはぎスカート・平短靴）と、成人男性園芸会館備品係の蓋角箱（横流し短髪/長袖シャツ・袖なしベスト・長ズボン・平短靴）、入口と広場。旧公園ベンチの封筒受渡し・短巻毛胸上sceneと親の丸顔/小楕円眼/約5頭身/輪巻髪/広白/隅小花小鳥は不継承。実L3の6項目だけ、21API＋親/source5/mediumNone/adjustments空、hatching背景衝突だけ両言語元以下で整合。
- 採用はchibi-comic/round-eyes-bright/picture-book/rough-light/pen-classic/elegant/hair-detail。rough別役の全身原寸約7.3は境界による数え幅、やや脚長でも標準構築を肯定して近似採用。厳密7以下の保証ではない。トーン量/線量/背景量/衣装・低踵/遮蔽・画角外の差はrole別notesへ保持、全語完全再現を主張しない。
- white両役の低頭身と簡単線目、natural/clean/modern/hatching別役の標準6〜7構築は未確認。bold代表は約3.5頭身で圧縮された胴脚、別役は約3.3〜4弱で髪と数え境界の不確実さが主だが4〜5を積極確認できずhold。数値1頭差の自動判定や厳密寸法式にしない。comic代表のラフ主輪郭は原寸肯定、別役は縫目/しわと区別できる重ね線未確認でpairhold。
- digital/pencil/decor代表は同一衣服原寸で系統点径grad未確認。衣服は検査sampleであって限定必須義務ではない。全景にも別部位の具体的確証なし、別役native未実施を保持し、全図不使用とは断定しない。classicは左背景の両役原寸で系統点径変化を肯定、代表全身約7.9もすらり構築を肯定したが、別役の独立数本太まつげ/白光個数未確認でpairhold。retro代表も約7.5〜7.7/髪除けば8前後を肯定するが、別役眼holdは救済しない。
- retro/classic/stipple別役は太い上瞼や目尻と独立した数本太まつげを未確認、男性免除なし。stipple白光2〜3個は肯定、retro/classic個数は未確証。dense代表は棚内背表紙/ラベルの未解消文字様印を原寸確認しhold。confirmedtrueはその存在であり無文字合格ではない。dense別役の体型未確証も保存し、既holdのため追加実見なし。
- 元fit/defining_visible/notes/nativebooleanと主担当採否を分離。複数原寸は同roleでもactual call＋質問＋regionのlist保持、別predicateの肯定でfalseを消さない。画材・物理トーン枚数・カッター実使用・実年齢/職務を画像だけで断定しない。
- 固定assetは元比率保持の14JPEG/長辺1024以下/L、thumbだけ白余白384×512。旧35bundle442pair全recordに新7組を追加し36bundle449pair候補。caller process_image(color=(job.expression!='mono'),preserve_aspect=True)→store.pyのL/RGB分岐を同SHAで再利用。変更はregistryとdocs2のみ、Caddy/認証/権限/workflow/保護設定は不変、廃止CIを再有効化しない。通常PRと既存サービス別Actions、本番全受入後だけpublished。復旧はrevert PR/通常Actionsに加えvolume pair-history/旧画像の復元確認が必要。

## 説明用2枚組：少女・SF（2026-11-08）

- 23葉46monoを1画像1独立process/新turnで生成し、46完成/46固有session/拒否0/未送信0。literal全46初見45none/1uncertain、原寸22件を同call・質問・region・原画SHAに結合。肯定26roleを保存し、両役positive8組16枚だけ候補、15枝は旧公開維持。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engineの独立保証なし。
- 成人女性天文資料室案内係の丸ケース（肩直毛/長袖ブラウス・腰丈上着・ふくらはぎスカート・平短靴）と成人男性観測館備品係の蓋角箱（短く刈った髪/長袖シャツ・袖なしベスト・長ズボン・平短靴）、入口と広場。旧宇宙船乗員男女の端末比較・親描法は不継承、実L3の6項目だけ。23API＋親/source5/全digest/mediumNone/adjustments空、bg5keys明示unknown停止/decor疎scene、hatching背景衝突だけ両言語元以下で整合。inspector/planner/dryrun46は初回成功。
- white両役は約6〜7/約7頭身で4〜5低頭身未確認。natural別役約9、clean約7.5〜8、modern約7.8〜8、hatching約8〜8.5、mecha約8.5〜9は、原寸で標準6〜7頭身の構築を未確認。数値1頭差だけでなく胴脚・特に脚の配分と境界の不確実さを保存しhold。rough別役は主輪郭に少しずれた重ね線を原寸確認、全身約7.4/数え幅7.3〜7.6で標準成人構築を肯定し差分採用、厳密7以下保証なし。
- hair代表約7.4/境界で7台後半〜8前後は細胴・長い下半身のすらり構築を肯定し採用。retro代表約8〜8.5、layered代表約7.7〜8前後、nineties代表約7.6〜7.8〜8前後も原寸肯定だが、別役の眼・まつげ争点によるpairholdを救済しない。元partialや比率・衣装丈・低ヒール所見を保持し、厳密8保証はしない。
- 4grad（shojo-digital/pencil-soft/decor-flowers/shojo-classic）は代表同一衣服の原寸で系統点径変化未確認、他部位全景の確証なし/別役原寸未実施を保持。衣服限定の追加義務ではない。nineties別役は横眼裂、stipple/retro/layered別役は上瞼・目尻とは独立した数本太まつげと2〜3白光の個数を未確認。黒い瞳と白光の存在は肯定、男性免除なし。
- dense代表は初見textuncertain、原寸confirmedtrueは背表紙の未解消文字様印の存在で、無文字合格ではなくhold。可読文字は未確認、罫線/陰影/装飾と区別。dense別役は原寸で均一粒面・明確黒影・壁扉段差の平面を確認、材質細線/斑点等の残差は保持。hatching別役の瞳内大白光は原寸肯定だが頭身holdは解消しない。
- 採用はchibi-comic/round-eyes-bright/rough-light/pen-classic/tall-cool/elegant/hair-detail/gothic。元fit/defining_visible/notes/nativebooleanを改変せず主担当の採否と分離。残差はrole別notesとcorrectionに結合し、量・程度・背景設備・衣装細部・低踵・頭身近似や画角外を全語完全再現と呼ばない。実画材/貼付枚数/カッター実使用/年齢・職務を画像から断定しない。複数nativeは同roleでも実call ID＋exact question＋regionのリストとして保持。
- 固定assetは新16JPEGの元比率を保持し長辺1024以下/L、thumbだけ白余白384×512。旧34bundle434pair全recordに新8組を追加し35bundle442pair候補。callerのprocess_image(color=(job.expression!="mono"), preserve_aspect=True)と同SHA store.pyのL/RGB変換を結合。実装17pathの同SHA所見を直接reuseし、今回差分はregistry＋本節2docsだけ。Caddy/認証/権限/workflow/保護は変更せず、廃止CIを復活させない。
- 本番受入は通常PR/許可済みmainの既存サービス別Actions、全API/原画から配布SHA/日英390・1280pxの2decode/操作/可視画面/actualhealthy、receipt正保存・fullreadback全SHA後のみ台帳published。viewport emulationは物理スマホ試験ではない。復旧はrevert PR＋通常Actionsとvolumeのpair-history/旧画像を併せて確認し、コードrevertだけで完了としない。

## 説明用2枚組：少女・ヒューマンドラマ（2026-11-08）

- 23葉46monoを1画像1独立process/新turnで生成し、46完成/46固有session/拒否0/未送信0。literal全46初見は43none/3uncertain、原寸16件。両役positive8組16枚だけ候補、15枝は旧公開維持。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engine保証なし。
- 成人女性生活資料館案内係の丸ケース（耳下短髪/長袖blouse腰丈jacketふくらはぎskirt平短靴）と成人男性地域会館備品係の蓋角箱（短いくせ毛/長袖shirt袖なしvestpants平短靴）、入口と広場。旧小食堂で二人が湯のみを前に話を聞く場面や親の写実顔/灰tone髪/斜帯光などは不継承。L3実6項目だけ、23API+親/source5/全digest/mediumNone/adjustments空を照合。実bg5keys明示unknown停止/decor等疎scene、hatching背景とrealistic-dense背景/顔のflat-tone衝突だけ両言語元以下で整合。planner/dryrun46は初回成功。
- white別役は原寸約6〜7/約6.2で胴脚が縦長、4〜5低頭身を確認できない。natural別役も約8、胸腰と脚が長い構築で標準6〜7を確認できずhold。数字1頭差だけの自動合否ではない。retro代表は約7〜7.5、細身長脚で別系統不足とは言い切れない所見を保持し、8以上の積極確認未了でhold。hair代表は約7.2〜7.5/髪等の境界次第で8近く、細い胴と十分長い腰脚を原寸肯定したため差分付き採用、strict8保証はしない。
- 4gradは代表同一衣服明暗の原寸でも系統点径変化未確認。他部位全景も確証なし、別役原寸未実施を保持。衣服だけの追加義務ではない。rough別役は縁取り/縫目/しわ/指形状と主輪郭のラフな重ね線を原寸で区別し、後者未確認。nineties別役は横眼裂、stipple/layered別役は独立した数本太まつげ未確認。stipple別役の黒目/白光2〜3は肯定、影以外の点描という初見残差も未解消。男性免除なし。
- dense/hatching/realistic各代表は初見text uncertain。原寸で未解消の文字様印の存在confirmed=trueであり、無文字合格ではなくhold。可読文字は未確認、通常の構造線/陰影と分離し切り出し外は未実見。cinematic代表は半顔が灰色面、鼻脇だけ狭い皮膚黒ベタで広い半顔黒面を確認できずhold。別役肯定をpair救済へ転用しない。
- 採用はround-eyes-bright/shojo-clean/modern-flat/pen-classic/tall-cool/elegant/hair-detail/gothic。27roleの肯定は保存し、両役肯定16枚だけ公開候補。元fit/dv/notes/nativebooleanと主担当採否を分離。線幅/トーン量、背景量/設備、服の丈/ひだ/低踵、頭身近似/遮蔽/画角外など、残差はrole別所見に結合。物理画材/枚数/カッター実使用/実年齢や職務を画像から断定しない。
- whole-figure追検のregion=Noneと初見のregion省略をcollectorが同一視し重複assert。元collector/失敗を保存し、image+region+実質問一致へ限定訂正、同call ID/rawから復旧し再実見0。builder初回はkernelのPython3.14依存pathを3.12子へ継承したPillow import失敗で、builder実処理前。通常terminalの既存3.12環境で同一builder成功、生成再送/製品変更なし。
- ZIP2268013bytes/SHA520032ef383c0d29149a40ba531ee3b0ca4860403f56ca3be7a47e879fb38cd9。旧33bundle426pair全record+8=34bundle434pair候補。画像git外、新16枚monoL/元比率長辺1024以下/thumb白pad384×512、L変換はcaller process_imageから同SHA store calleeへ委譲。17実装/baseline3同SHA、docs2+registryだけ。Caddy/認証/権限/workflow/保護変更なし、廃止CI復活なし。
- 回帰は直前checks/Site実測と426→434pair増加からprivate360秒余裕を事前保存し自身prepost。元製品180秒/commands/合否/本番deadline不変。prepareforeground→回帰background notify→統合foreground。固定asset往復/通常Actions/本番受入receiptは別gate。

## 説明用2枚組：少女・サスペンス（2026-11-08）

- 22葉44monoを1画像1独立process/新turnで生成、44完成/44固有session/拒否0/未送信0。literal全44初見none、原寸13件を保存。両役positive12組24枚のみ候補、未達/未確認10枝は旧公開維持。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engine保証なし。
- 成人女性資料保存庫整理係の丸ケース（顎丈ボブ/長袖blouse腰丈jacketふくらはぎ丈skirt平短靴）と成人男性記録館備品係の蓋角箱（横分短髪/長袖shirt袖なしvestpants平短靴）、入口と広場。旧閉店後の古店で二人が指輪を見る場面と親の小さい光1つ/半顔影/少まつげ/長細顔などを追加せず、L3実6項目だけ。22API+親/5sourceSHA/全digest/medium全None/adjustments空を生成前照合、実bg5keys明示unknown停止、decor等は遠い扉だけ、hatch背景衝突のみ両言語元以下へ。
- hold10=white-space/natural-quiet/shojo-digital/pencil-soft/decor-flowers/shojo-classic/nineties-sharp/stipple-dreamy/retro-shojo/layered-gorgeous。whiteは4〜5低頭身の定義に対し約6/5.5〜6という全身構築不足。natural別役は全身原寸で約8.5〜9頭身/脚の長身化が明瞭で6〜7標準体未確認、厳密寸法式は追加しない。4gradは代表同一衣服明暗でも系統的点径変化未確認、他部位全景確証なし/別役native未実施。衣服限定追加義務ではなく密度差/粒overlayは代用しない。nineties別役は原寸で横眼裂、初見full/microを上書きしない。stipple/layered別役は太上瞼とは別の数本太まつげ未確認、男性免除なし。
- retro代表の全身原寸はconfirmedfalse/約7前後で8以上を明確に確認できない。ただし髪/顎/足先位置の不確実さ、約1頭身差で別系統の構築不足までは断定できないという所見も保持し、今回は高頭身確認未了として保留。hair代表は原寸confirmedtrue/約7.5で8前後の数え方差、すらりと長い胴脚の構築を肯定したため差分付き採用。元全景7程度/fitpartialも保持し厳密8以上の保証をしない。明確なnaturalの長身化と未確定retroを混同せず、好ましいbooleanを得る再実見なし。
- pen/hatching別役の瞳内部大白光は原寸確認、白目と分離。dense別役は原寸で均一粒状面と明確黒影、石壁舗装の面区分を確認。材質テクスチャは残差として保持し、粒そのものを禁止せず、広い連続/ぼけ明暗への粒overlayが目立たない所見へ結合。native切り出し外の顔/全景は未再点検。元fit/dv/notes/native争点boolean/主担当採否を別保存し、positive siblingでpair救済しない。
- 採用にも線幅/トーン広用、背景量/設備/近さ、表面の細線、服のひだ/丈/低踵、頭身近似/遮蔽/画角外などを元role別所見で保持。全語数値の完全再現/実画材/物理トーン枚数/カッター実使用/年齢職務断定なし。retro/hatching原画の生成り調は保持し、指定monoの配布L化を処理として分離。
- planner適応時、scene語の先行置換で旧rationale literal照合が失敗。未実行template/失敗/要求0を保存し、source/proseを先にplaceholder保護して一回renderへ訂正。planner実行/dryrun44は初回成功、生成再送なし。ZIP3980821bytes/SHAb2ddf69ce25f489bd67769c39d98f7e9aa9a036a49eb4adabf58596bc8d4117e、旧32bundle414pair全record+12=33bundle426pair候補。画像git外、新24枚L/元比率長辺1024以下/thumb白pad384×512。L変換はcaller process_image→同SHA store.py target_mode/convertへ委譲、caller literal convert(L)重複は義務にしない。docs2+registryのみ、17実装/通常baseline3files保持。Caddy/認証/権限/workflow/保護変更なし、廃止CI復活なし。
- 回帰は直前checks319.69秒/Site197.31秒/総540.1236392213032秒と414→426pair増加を事前評価し、私用collector360秒維持/自身prepost。元製品180秒/commands合否/本番deadline不変。prepareforeground→回帰background notify→統合foreground、固定asset往復/通常Actions/本番受入receiptは別ゲート。

## 説明用2枚組：少女・バレエ・ダンス（2026-11-08）

- 21葉42monoを1画像1独立process/新turnで生成、42完成/42固有session/拒否0。literal全42初見none、原寸9件を保存し、両役positive13組26枚のみ候補、8枝は旧公開維持。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engine保証なし。
- 成人女性舞踊スタジオ受付係の丸ケース/成人男性市民会館舞台係の蓋角箱、肩髪長袖blouse腰丈jacket足首skirt平短靴/短髪長袖shirt袖なしvestpants平短靴、入口/広場をscene分離。旧13歳スケーター/お団子髪/スケート衣装/両腕開き反身/リンク客席と親描法を追加せず実6項目。21API+親/5sourceSHA/ja-en-tags全digestを生成前照合。medium全None/adjustments空、hatching背景衝突のみ両言語元以下へ。bg6keys明示unknown停止、effect/decorは遠い扉だけ。planner/inspector/dryrun42初回成功、generation再送なし。
- hold8=white-space/shojo-digital/pencil-soft/decor-flowers/shojo-classic/spotlight/nineties-sharp/stipple-dreamy。whiteは4〜5頭身の定義に対し初見代表約5.5〜6/別役約6頭身、代表小眼も漫画的大眼で、描法の肯定と人物構築不足を分離。4gradは代表同一衣服明暗の原寸で系統的網点径変化を未確認、密度差/粒overlayを代用せず、他部位全景も確証なし。衣服限定追加義務ではなく別役原寸未実施を保持。spotlight代表は原寸で外眼側/鼻脇/頬上部に影があるが頬大部〜顎は白く、片側の広い半顔黒影は未確認。髪/顎下/首と区別し厳密50%面積は追加要件にしない。別役の半顔影肯定は保持。nineties別役は横長アーモンド眼裂。stipple別役は太い上瞼/目尻とは別の数本太まつげ未確認、男性免除なし。positive siblingでpair救済なし。
- clean/rough別役の黒い瞳内部に大白光があることを原寸確認、白目と区別し切り出し外の初見所見を保持。他native未実施範囲を実施済にせず、元fit/dv/notes、nativeの争点confirmed、主担当採否を別保存。採用にも線幅/トーン広用、背景量/近さ/設備、ひだ/袖折返し/裾丈/低踵、頭身近似/遮蔽/画角外等の残差を保持。全語数値の完全一致/実画材/物理トーン枚数/カッター実使用/年齢職業断定なし。
- ZIP4466310bytes/SHAa9326f2178968c05c1ef16a7ab6a606a182ef17495ab8e802f9d203f0f3e2805、旧31bundle401pair全record保持＋13=32bundle414pair候補。新26枚mono L/元比率長辺1024以下/thumb白pad384×512。L変換はprocess_image caller→同SHA store.pyのtarget_mode/convertへ委譲、builder自身のliteral convert(L)重複は要件にしない。docs2+registryのみ、17実装同SHA/baseline3files保持、Caddy/認証/権限/workflow/保護変更なし/廃止CI復活なし。直前checks309.73秒/Site185.49秒/総519.7761秒と401→414pair増加から私用collector事前360秒維持/自身prepost、元製品180秒/commands/合否/本番deadline不変。prepareforeground/回帰background/統合foreground、固定asset往復/通常Actions/本番受入は別ゲート。

## 説明用2枚組：少女・芸能・アイドル（2026-11-08）

- 24葉48monoを1画像1独立process/新turnで生成、48完成/48固有session/拒否0。全48literal初見・原寸12件を保存し両役positive15組30枚のみ候補、9枝は旧公開維持。初見47none/1readable、hatching代表の庇印は原寸uncertain。採用30枚none、追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced falseで実engine保証なし。
- 成人女性劇場衣装係の無地丸ケース/成人男性音楽ホール備品係の無地蓋角箱、肩髪長袖blouse腰丈jacket足首skirt平短靴/短髪長袖shirt袖なしvestpants平短靴、入口/広場をscene分離。旧16歳アイドル/サイドテール/フリル短ケープ/マイク/ウインク歌唱/客席と、親の上下太長まつげ/星光瞳/艶唇/黒髪太白帯/暗toneスポットライト紙吹雪/長首尖顎を継承せず実6項目だけ。24API+親/実source5SHA/ja-en-tags全文digestを生成前照合、medium全None/placement adjustments空、hatching背景衝突のみ両言語元以下で線密度へ。bg6keys明示/unknown停止、effect/decorは遠い扉だけ、描法語はstyleだけ。
- hold9=shojo-digital/pencil-soft/decor-flowers/shojo-classic/nineties-sharp/spotlight/stipple-dreamy/layered-gorgeous/hatching-handmade。4gradは代表同一衣服明暗のnativeでも系統的網点径変化を未確認。密度差/不規則粒/粒overlayと区別し、衣服限定追加義務ではなく他部位全景確証なし、別役native未実施を保持。nineties別役は原寸で横長アーモンド眼裂。spotlight/stipple/layered別役は太い上瞼境界とは別の数本太まつげが未確認、男性免除なし。spotlightの半顔黒影/集中線は肯定し、暗く隠れる側は未確認。hatching代表の庇印は初見readableを保持し原寸uncertain、confirmed trueは文字様印の存在で無文字合格ではない。判読不能を非文字へ変換せず範囲外も未確認。positive siblingでpair救済なし。
- comic両役は原寸で主外輪郭の少量近接重ね線を確認（代表スカート左外/別役ズボン左腿膝外）。内部しわ/縫い目/箱厚み線と区別、全線重ね義務なし。hair代表は複数の平らな網点濃淡面/髪と瞳の白光を原寸確認。髪服靴各々への同時併存/物理的枚数/カッター実使用は要件にしない。他役の未実施nativeを済にせず、元fit/dvとnamed findings・主担当採否を分離。
- 採用にも線幅差/トーン広用、背景の扉装飾/量/近さ、巻尺裁縫道具/ブラウスひだ/裾丈/低踵、頭身近似/画角外等の残差を保持。retro原画の淡セピアは保存し、指定monoの配布L化は処理として明示。全語・数値完全一致/実年齢/職業断定/実画材/engine保証なし。effectは遠い平らな場所と集中線を今回初見で確認、以前cohortの否定を輸入しない。
- planner/inspector初回成功。dryrun CLIの旧想定flagはargparse exit2（出力/attempt0）を保存し実parserのpositional jobs/--output、--runなしへ訂正、planner再実行/生成再送なし。生成後は旧scratch testenv消失でverifier開始前exit127、原因不明を保存してABI互換の既存Hermes/Pillow kernelで同一offline verifierを実行、48完成/48session確認、生成再送なし。新scratch v2 testenvをPython3.12.3/同じrequirementsとhttpx2 2.16.0/httpx0.28.1/PyYAML6.0.3で再構築。provider/認証/永続設定変更なし。
- ZIP4331755bytes/SHAfc70f10a2a590b626aaafa43c82e1f16312066b73908be8966da67d1ada0c269、旧30bundle386pair全record保持＋15=31bundle401pair候補。画像git外/全mono L/長辺1024以下元比率/thumb白pad384×512。docs2+registryのみ、17実装同SHA/通常baseline3files保持、Caddy/認証/権限/workflow/保護変更なし/廃止CI復活なし。直前checks297.49秒/SiteTests177.58秒/総499.2103秒と386→401増加から私用collectorのみ事前360秒維持/selfprepost、元製品180秒/commands合否/本番deadline不変。固定asset往復/通常Actions/本番受入は別ゲート。

## 説明用2枚組：少女・魔法少女（2026-11-08）

- 23葉46枚を1画像1独立process/新turnで生成、46完成/46固有session/拒否0。literal全46初見と原寸10件を保存し、両役positive15組30枚のみ候補配布。8枝は旧公開維持。初見45none/1uncertain、採用30枚はnone。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced falseで実engine保証なし。
- 成人女性天文館受付係の無地丸ケース/成人男性博物館案内係の無地蓋角箱、肩髪/長袖shirt短腰apron足首skirt平短靴/短髪丸襟長袖shirtpants平短靴、入口/広場をscene分離。旧14歳変身少女/大リボン長ツインテール/フリル衣装/ハート杖/ウインクピース/雲上星と、親の幼丸頬大頭/巨大丸目星光/太丸単純線/白抜星ハート/少髪線をL3へ追加せず実6項目。source23API+親/5SHA/exporter/実6項目/ja-en-tags全digestを生成前照合、全medium None/placement adjustments空。hatching背景flat-tone衝突だけ生成前両言語元以下で線密度へ。bg6keys明示対応/unknown停止、effect/decor疎scene、描法語はstyleだけ。planner/dryrun46は初回成功。
- hold8=shojo-digital/pencil-soft/decor-flowers/shojo-classic/effect-power/nineties-sharp/dense-quiet/stipple-dreamy。4gradは代表同一衣服明暗の原寸でも系統的点径変化を未確認。濃淡/密度差/不規則粒/粒overlayを代用せず、衣服限定の追加義務でなく他部位全景も確証なし。他役原寸未実施。effect両役は太線と集中線が見えても、遠い平らな場所指定に対し具体的な建築/ガラス扉/植栽/舗装の透視描写があり、背景量の微差として主描法差を救済しない。nineties別役は原寸で横長アーモンド眼裂、stipple別役は太上瞼とは別の数本太まつげ未確認。dense代表の入口ガラス掲示/書籍展示カードの微小印は原寸uncertain、confirmed trueは未解消文字様印の存在で無文字合格ではない。範囲外は未確認、positive siblingでpair救済なし。
- comic両役は原寸で主外輪郭の短い近接重ね線を確認（代表スカート左外縁、別役肩上腕外/ズボン外）。髪束/内部しわ縫い目/箱厚みを除外し全線重ね義務なし。hatching別役の瞳内大白光は白目と分離して原寸確認。髪/服/靴各々への同時併存や実画材/物理トーン枚数/工具は要件にしない。元fit/dv/notes/falseを保持しnative条項補足と主担当採否を分離。hairの複数トーン/光沢等は初見のままで未実施nativeを済にしない。
- 採用にもトーン広用/線幅差、具体的背景や展示物の増加/近さ、名札/ケース持ち手/留具/胸当てapron/裾丈/低踵、頭身近似/画角外等の残差を保持し全語数値完全一致は主張しない。元所見が微差と呼んでも真の主描法不足は保留。職業看板/実年齢/画材/engineの追加断定なし。
- 古い実行kernelの内部bridge消失で冗長summary保存が失敗、元summaryは既に保存済み。標準resetと実artifact再読で回復、再生成0。復元native collectorはcrop注記prefixを未処理でJSONDecodeError、元driver/失敗を保全しraw.scale_noteの完全一致prefixだけを解析時に除外して原返却を保持。画像再実見/再生成なし。
- ZIP4379605bytes/SHAee393aa8b6754a6a68eb43c52f2270f46e3562fafcb32c2958cd91773f532da8、旧29bundle371pair全record保持＋15=30bundle386pair候補。新全mono L/元比率長辺1024以下/thumb白pad384×512。docs2+registryのみ、アプリ/Caddy/認証/権限/workflow/保護不変、廃止CI復活なし。直前checks283.97秒/SiteTests171.78秒/全478.4308秒と371→386pair増加による300秒への余裕不足を根拠に、私用collectorのみ実行前360秒/自身pre-post結合。製品180秒/commands/合否/本番deadline不変。prepareforeground/回帰background/統合foreground。固定asset往復/通常Actionsと本番受入receiptは別ゲート。

## 説明用2枚組：少女・宮廷ロマン（2026-11-08）

- 22葉44枚を1画像1独立process/新turnで生成、44完成/44固有session/拒否0。literal全44初見と原寸12件を保存。両役positive13組26枚のみ候補配布、9枝は旧公開維持。初見43none/1uncertainで採用26枚はnoneのみ。追加生成/文字消去0。requested gpt-image-2.6-sunburst/reported_model null/model_enforced false、実engine保証なし。
- 成人女性宮殿記録係の無地閉帳簿/成人男性道具係の無地蓋木箱、長袖ブラウス・腰帯・足首スカート/長袖シャツ・袖なし腰丈ベスト・長ズボン・平短靴、記録室入口/道具庫前中庭をsceneに分離。旧17歳侍女/かんざし/そばかす/広帯宮廷衣装/顔前薬草/朱柱反瓦灯籠、親の巨大目/四角光星/放射まつげ/lace/流房淡tone/長首をL3へ足さず実6項目。全medium None/placement adjustments空、taisho-lyricは実source使用。源5SHA/6項目/exporter/API実文/ja-en-tags完全digest結合、hatching背景flat-tone衝突のみ生成前両言語元以下で線密度へ。bg全key対応/unknown停止、decor/ornament疎scene、植物曲線と円はstyleだけ。planner/dryrun44は初回成功。
- hold9=white-space/shojo-digital/pencil-soft/decor-flowers/shojo-classic/nineties-sharp/dense-quiet/layered-gorgeous/taisho-lyric。white両役の全身は約6〜7/約6頭身で4〜5低い構築が未達。4gradは初見で点径変化が不明瞭、代表同衣服明暗の原寸でも系統点径変化未確認。密度/不規則粒/滑階調overlayを代用せず、衣服だけに必須という追加義務でもない。他部位全景に確証なし、別役原寸未実施。nineties別役は横長アーモンドの眼裂、網点複数濃淡と髪白抜きは肯定でも縦長大目未達。dense代表本背は原寸でも未解消の文字様印、confirmed trueは印存在で無文字合格でない。layered別役は太上瞼線とは別の数本太まつげ未確認、男性免除なし。taisho別役は「少し垂れた大きな黒い瞳」が未確認。positive siblingでpair救済しない。
- shojo-clean/pen-classic別役は原寸で瞳内の大きな白光を白目と分離確認。hair-detail両役は複数の網点濃淡面/髪暗部の白い光沢/瞳内の大白光を原寸確認。各部位同時併存/物理枚数/実工具は要件にしない。元fit/dv/text/notesを改変せず、native局所/主担当採否/画角外を別管理。roughの少量重ね線/ハッチの線密度陰影と網点なし等は初見のままで新native済とはしない。
- 採用にも網点広用、線幅揺れ、背景建築/棚/小物/植栽の増加や近さ、薄い木目/石材表面線、頭身近似、服丈/低踵/袖まくり/画角外を残差保持。全語・数値の完全再現ではなく、主描法不足を美しさで救済しない。職務看板/実年齢/物理画材/engineの追加断定なし。
- ZIP4406347bytes/SHA403eb80d3c70040302467c216195511991eb9683b63119d7633a9b9cd43cfbf5、旧28bundle358pair全record保持＋13=29bundle371pair候補。新mono L/元比率長辺1024以下/thumb白pad384×512。変更docs2+registryのみ。アプリ/Caddy/認証/権限/workflow/保護設定不変、廃止CI復活なし。私用collector300秒は直前checks273.58秒/SiteTests163.35秒/全459.764秒を根拠に事前凍結し自身pre/postへ。元product180秒/commands/合否/本番deadline不変。prepare別foreground/回帰background/統合foreground。固定asset往復と通常Actions、本番受入/receiptは別ゲート。

## 説明用2枚組：少女・ファンタジー（2026-11-08）

- 25葉50枚を1画像1独立process/新turnで生成し50完成/50固有session/拒否0。確定literal style/sceneで全50初見、原寸12件を保存。両役positive17組34枚だけ候補配布、8枝は旧公開維持。全初見text none、追加生成/文字消去0。requested gpt-image-2.6-sunburst、reported_model null/model_enforced falseで実engine保証ではない。
- 成人女性陶工の無地鉢/成人男性薬草店員の無地蓋壺、長袖チュニック・腰エプロン・足首スカート/襟なし長袖チュニック・腰ベルト・長ズボン・平短ブーツ、工房前/店前広場をscene分離。旧18歳和風娘/着物/赤面/鬼火/夜縁側や親の面長切れ長模様瞳光/流髪トーン/長首/つる花をL3へ加えず、実6項目だけ。全medium None/placement adjustments空。hatching-handmade背景flat-tone衝突だけ生成前両言語元以下で線密度へ。bg decor/ornament/effectは明示疎scene、未知key停止。art-nouveau植物曲線と円はstyleにだけ含め、sceneで補わない。planner/dryrunは初回成功。
- hold8=white-space/shojo-digital/pencil-soft/decor-flowers/shojo-classic/comic-lively/nineties-sharp/stipple-dreamy。white-space両役は約6〜6.5/約6頭身で4〜5の低い構築未確認。4grad代表は同一衣服明暗の系統点径変化を原寸未確認、密度/不規則粒/滑階調overlayで代用しない。他役原寸未実施。comic代表左袖外主輪郭の短並走は確認したが別役の見える外輪郭は整理単線でhold。nineties別役は横長アーモンド眼裂、stipple別役は上瞼太線とは別の数本太まつげ未確認。各positive siblingをpair救済しない。
- 原寸のshojo-clean/rough-light別役は瞳内の比較的大きな白光を白目から分離確認。hair-detail両役は全体の複数網点濃淡と髪など暗部内の白い光沢、別役瞳白光を確認。部位ごとの同時併存/物理トーン枚数/カッター実使用は義務にしない。初見fit/dv/text/notesを改変せず、原寸のnamed clause補足と主担当採否を分離し、切出外の足や全景は元観察保持。hatching両役の線密度陰影/網点なしは初見で確認し新原寸済とはしない。
- 採用にもトーン広用/線幅揺れ/近店舗棚窯植栽/背景量と柄量/木目石畳等表面線/頭身近似/衣服丈/低踵/袖まくり/画角外を残差保持。modern-flatなど初見の「主描法不十分」は元所見のまま、主担当は滑らかな輪郭と平面網点の可視性、計画上許容の線量/背景量から差分採用であり完全一致ではない。低頭身や点径gradなど真の未確認を美しさで救済しない。職業看板や実年齢/画材工程/engineの追加証明なし。
- 視覚metadata collectorはcontext replayによる同tool_call_id/同一結果bytesのmessage重複で一意件数assertが停止した。元失敗を保存し、同call IDかつ完全同bytesだけ重複排除、全message IDを保持して保存を回復。画像再実見/再生成/製品変更なし。
- ZIP5667757bytes/SHA7fc6713aa4a85f19b491f313168c496aef3a6c83b091dccb1b90658c492012c6、旧27bundle341pair全record＋17=28bundle358pair候補。新全mono L/元比率長辺1024以下/thumb白pad384×512。変更docs2+registryのみ。アプリ/Caddy/認証/権限/workflow/保護不変、廃止CI復活なし。通常Actionsと本番healthy/readiness/API画像/日英UI操作/最終receiptは別ゲート。
- 直前checks260.45秒/SiteTests154.70秒/回帰438.36秒を根拠に私用collector事前300秒/自身pre/post入力結合。元product180秒/commands/合否/本番deadlineは不変。prepare別foreground→回帰のみbackground→統合別foregroundとし、旧timeout/手続falseは免除しない。


## 説明用2枚組：少女・ラブコメ（2026-11-08）

- 23葉46枚を1画像1独立process/新turnで生成し、46完成/46固有session/拒否0。確定literal style/sceneで全46初見＋native13。両役positiveの15組30枚だけ候補配布し、8枝は旧公開維持。追加生成/文字消去0。初見text none44/uncertain2を保全し、採用30枚はnoneのみ。requested gpt-image-2.6-sunburst、reported_model null/model_enforced falseで実engine保証ではない。
- 成人女性手芸用品店職員/成人男性書店職員、無地蓋箱/紙袋、長袖shirt短腰apron足首skirt/長袖shirtpants平短靴、店舗前/書店前広場をscene分離。旧18歳女子大生/ヘアピンボブ/大パーカー/スマホ胸抱え/赤面ぐるぐる目口ぱくぱく/夜の部屋ベッドクッションぬいぐるみを不継承。親丸顔大頭5頭身/2白光/短まつげ/黒髪形/頬斜線ハートをL3へ加えず実6項目のみ。source5SHA/exportercanonical/API実文、全mediumNone/placement adjustments空を結合。hatching-handmade背景flat-tone衝突だけ生成前両言語元以下で線密度へ修正し、他placement旧公開不変。bgdecor含む網羅unknown停止、decor/effectは疎sceneで柄語をsceneに混ぜない。
- planner初回は親ID置換がsource repoパスまで変え、存在しない新worktreeのbuild_tree importでModuleNotFoundError。旧driver/0要求/jobs未作成/product不変を保全し、repoの1literalを実sourceへ修正してplanner/dryrun46成功後に初要求。生成ソースと後で作るfreshmain公開worktreeを分離する。
- native13はquestions13/notes4+4+5。shojo-clean別役は瞳内部の大きな白光を白目から分離確認。comic代表は左袖肘付近/スカート左外主輪郭、別役は肩袖外（特に右袖）/ズボン外の一部に少量近接並走を確認して条項だけ訂正。髪/内部しわ/縫い/箱袋厚み除外、全線重ね義務なし。rough両役の初見positiveは新nativeを実施したことにせず保持。
- hair-detail代表は髪/服/庇/背景の複数網点濃淡面と髪帯状艶/瞳大光/窓反射白抜きをnative確認。nineties代表もエプロン/スカート/背景の網点濃淡と髪白線/幅白抜きはnative positive。各部位での同時併存/実トーン2〜3枚/カッター実使用は義務にせず、全体の可視表現だけ確認し画材/工程は証明しない。
- hold8=white-space/shojo-digital/pencil-soft/popart-dots/dense-quiet/decor-flowers/shojo-classic/nineties-sharp。white-space両役は全身初見で約5.5〜6/約7頭身となり4〜5低い人物構築が未確認。元dv trueや「主描法不足でない」も保全し、主担当が人物構築不足として別途hold。4grad代表は同一衣服の網点径そのものの系統的変化をnative未確認、密度/不規則粒/鉛筆粒/滑階調overlayと別、他役native未実施。pencil別役の本/看板の初見uncertainは保全し、gradでpair保留のため文字だけを消す/不要再実見しない。
- popart両役は顔皮膚/手の点が細粒、濃面は網目状で、肌と影にひと目で大きい独立丸点をnative未確認。髪ベタ/黒目/服の丸点を皮膚の確認へ転用せず、初見dv trueをfalseへ上書きしない。nineties別役は上下瞼の眼裂が横長アーモンドで縦長大目未確認、虹彩縦丸や代表positiveで救済しない。dense別役は左書店の本背/表紙/扉越し本の細印がnative classification uncertainでhold、判読不能だから無害とせず元text uncertainを維持。代表positiveは保持し配布からpair除外。
- 元fit/defining_visible/notes/uncertainの全文を保持し、native局所補足/主担当採否を分離。crop外足/全景は初見のまま、未実施nativeを済にしない。採用にも網点広用/線幅揺れ/近店舗棚商品植栽/背景柄量/表面質感/頭身近似/裾丈/低踵/胸当てapron/ペン/持ち物位置/画角外の残差を保持。看板職業表示の義務追加なし、全語数値完全再現false/実年齢職務材質/実画材engine/工具枚数は未証明。美しさで主描法不足救済しない。
- ZIP4443137bytes/SHAce77aa469794a8445019ebd887bd90c408f5b52b53237b11baa5f629559533d5、旧26bundle326pair全record保持＋15=27bundle341pair候補。新全mono L/元比率長辺1024以下/thumb白pad384×512。docs2+registryのみでアプリ/Caddy/認証/権限/workflow/保護設定は不変。固定archiveを既存通常Actionsで配置し、本番healthy/readiness/公開API画像/日英UI操作/最終receiptを別ゲートにする。廃止CI再有効化なし。
- 直前checks248.28秒/SiteTests148.37秒/全回帰419.56秒を根拠に私用collector事前300秒/自身入力結合、元product180秒/commands/合否/本番deadline不変。outer420秒を考慮してprepare別foreground/回帰だけbackground/統合別foregroundとし、旧timeout/手続falseは免除しない。


## 説明用2枚組：少女・学園恋愛（2026-11-08）

- 23葉46枚を1画像ごとの独立process/新turnで生成。46完成/46固有session/拒否0、確定literal style/sceneで全46初見+native13。全初見text none、追加生成/文字消去0。requested gpt-image-2.6-sunburstだがreported_model null/model_enforced falseで実engine保証ではない。
- 成人女性大学図書館職員と成人男性大学事務職員、本/封筒、長袖カーディガン丸首足首丈スカート/長袖シャツ長ズボン平短靴、図書館前/大学中庭をscene分離。旧16歳中性少女/耳見せショート/リボン制服/窓もたれ本抱え赤面横目/夕廊下ロッカーを不継承。親の巨大目/5〜6白光/髪淡トーン/赤面/花柄をL3styleへ加えず実6項目のみ。全medium None、hatching-handmadeだけ背景flat-tone衝突を生成前両言語元以下で線密度へ置換、他placement旧公開不変。bgはdecor含む実key網羅unknown停止、decorは遠入口/門一つの疎scene。planner適応初回は旧rationale全文literal置換assertで0要求停止を保全し、実source field境界で説明文を訂正後dryrun46と源照合を通した。
- 両役positive16組32枚のみ候補配布。hold7=white-space/shojo-digital/pencil-soft/decor-flowers/shojo-classic/nineties-sharp/stipple-dreamy。4grad枝の代表は同カーディガン明暗の系統点径変化をnative未確認、密度/不規則粒/滑階調overlayと別。別役native未実施も保持。white-spaceは全身初見で約6〜7/約6頭身となり4〜5の低い人物構築が未確認、初見の微差分類は保全し主担当はhold。nineties別役は横長アーモンド眼裂、stipple別役は瞳黒面/複数白光可視だが上瞼と別の数本太いまつげ未確認でhold。代表positiveを配布へ混ぜず、男性だからまつげ義務を免除しない。
- rough-light別役の左袖、comic両役の肩袖/スカートやズボン外主輪郭の少量近接並走重ねをnativeで部位確認へ訂正。髪/内部しわ/縫い/本厚みと区別、全輪郭重ね義務なし。shojo-clean別役は瞳内大白光を白目と分離確認。hatching-handmade代表の服陰は線密度で、明瞭規則網点/滑階調なしとnative確認、明部粒状質感と髪黒面は別残差。
- hair-detail別役の最初のnative接続エラーは原記録保全し同画像/質問/regionだけ再実見。続く質問は髪服靴それぞれに網点濃淡面と白抜きの同時併存を求める読み方となり原文より強かったため、質問/falseを保全してextraで訂正。extraのconfirmed=falseも「既存false維持」を新flagへ誤適用した返却としてliteral保持。ただしextra.findingsは全体の網点濃淡面・ズボン折陰・髪鋭白筋・両瞳白光を明示可視とするため、主担当はそのnamed evidenceから部位同時併存義務なしの可視確認で差分採用。物理枚数/カッター実使用は証明せず、靴光の弱さも残差。フラグ取得のための反復検査/再生成なし。
- 元fit/defining_visible/初見全文は全46で保持し、native局所補足と主担当採否を分離。crop外の足/全景は元初見保持、未実施別役nativeを済にしない。採用にも網点広用/近建物門や書架植栽増/背景や花柄量/線粒質感/頭身近似/スカート丈/低踵/無字名札追加/画角外を残差として保持。学校所属/職業の看板を追加義務にせず、全語数値完全再現false/実年齢職務材質/物理工具枚数画材engine未証明。真の主描法不足は美しさで救済しない。
- 新画像は元比率/長辺1024以下mono L、thumbは白余白384×512。旧25bundle310pair全record保持＋16=26bundle326pair候補。アプリ/試験/木/Caddy/認証/権限/workflow変更なし。固定SHA archiveを既存通常Actionsから配置、本番healthy/readiness/API画像UI操作/最終receiptは別ゲート。廃止CIを再有効化しない。
- 直前checks235.36秒/SiteTests137.20秒/全回帰395.22秒を根拠に私用collector300秒を回帰実行前設定し、自身をpre/post入力へ含める。元product180秒/commands/合否/本番deadline不変。外側420秒transportを考慮しprepare/回帰background/統合foregroundを分離。旧timeout/手続falseは不変。


## 説明用2枚組：少年・線で彫る劇画調（2026-11-08）

- 21葉42枚を1画像ごとの独立process/新turnで生成。42完成/42固有session/拒否0。確定literal style/sceneで全42初見+native12、追加生成/文字消去0。requested gpt-image-2.6-sunburstだがreported_model null/model_enforced false、実engine保証ではない。
- 成人園芸作業員/植物園職員、苗鉢/金属じょうろ、長袖シャツ/短腰エプロン/ズボン/平短ブーツ、温室前/庭広場をscene分離。旧35歳大柄男/厚首肩腕/袖まくり作業シャツ/胸前握拳/眉寄せ遠望/夕埠頭船倉庫を不継承。親の劇画男骨格/平行線をL3完結styleへ加えず、実6項目だけを使用。mediumは全None、hatch衝突3葉だけ生成前両言語元以下置換、bg実6key網羅unknown停止/effect疎scene。他placement旧公開不変。
- 両役positive17組34枚を候補配布。hold4=pencil-soft/nineties-sharp/brush-wild/scratchy-dryは旧公開維持。pencil代表同シャツ点径可変grad、nineties代表縦長大眼裂、brush代表主輪郭大筆幅変動+白抜けカスレ、scratchy別場面主輪郭乾途切れがnative未確認。pencil別場面も初見grad未確認でnative未実施。nineties別役/brush別役/scratchy代表のpositiveをそのまま保持し、片役だけ配布しない。
- rough代表は肩袖ズボン少量並走重ねと、別の目領域で瞳内白光を確認。comic代表は膝外主輪郭、別役は袖ズボンの少量重ねを確認、肩袖単線の観察は残す。graphic-flat両役は人物襟/前端/袖折れ/袖口/ズボンの硬鋭線と短上瞼小黒瞳をnative確認へ部位限定訂正。顔髪曲線禁止/全角形身体義務を足さず建物直線で代用しない。
- cinematic別役は右目尻〜頬側〜顎の皮膚黒ベタ影をnative確認し、初見顔影不足をその条項だけ訂正。shadow別役も左目尻〜頬〜顎の皮膚影を髪眉瞳首と分離して確認。厳密50%の追加義務は課さない。元fit/defining_visibleと初見全文を保全し、nativeは局所補足。切出外の足/全景は元初見保持、未実施別役nativeを済にしない。全42初見text none。
- 採用にも網点広用/近景花壇草花や温室骨組み増/背景量/線や粒の質感/頭身近似/低踵/袖まくり/胸当てエプロン/両手添え/じょうろの太腿前位置/道具追加/画角外を残差保持。入口一か所の両開きは扉一枚禁止という追加義務にはしない。nineties代表初見の目不足を微差とした分類は必須構築不足として別hold。全語数値完全再現ではなく実年齢職務/実材質/物理トーン枚数/カッター/定規/画材engineは未証明。
- 画像は元比率/長辺1024以下mono L、thumbは白余白384×512。旧24bundle293pair全record保持＋17=25bundle310pair候補。アプリ/試験/木/Caddy/認証/権限/workflow変更なし。固定SHA archiveを既存通常Actionsから配置、本番healthy/readiness/API画像UI操作/最終receiptは別ゲート。廃止CIを再有効化しない。
- 直前checks223.60秒/SiteTests129.39秒を根拠に私用collector300秒を回帰実行前に設定し、driver自身をpre/post入力に含める。元product180秒/commands/合否/本番deadline不変。前回の連結外側420秒timeoutを反復しないためprepare/回帰/統合は別呼出とする。旧外側失敗/手続falseは不変。


## 説明用2枚組：少年・顔を線で刻む奇抜な美形（2026-11-08）

- 22葉44枚を1画像ごとの独立process/新turnで生成。44完成/44固有session/拒否0、確定literal文で初見44+native7。requested gpt-image-2.6-sunburstだがreported_model null/model_enforced false、実engine保証ではない。
- 成人木工作業員/配達員、木片/空木箱/無地布包、長袖上着/丸首/ズボン/平短靴、作業場/倉庫前広場の独立一姿勢をscene分離。旧18歳盛髪青年/高襟学生服/顔横開指/あご上げ/洋館坂道不継承。hatch衝突3葉だけ生成前両言語同長以下修正、bg実key全網羅unknown停止/effect疎scene、他placement旧公開不変。
- engraving--shonen-carved-engravingはliteral保持。実exporter/repairs.TARGETS/RECIPES/APIへ結合してbase engraving/medium repair-engravingを記録。白背景none/無トーン無ベタを保持し、共有styleへ戻さない。実見でも両役の形沿い平行線と交差線の間隔による影/明瞭な網点広ベタなし/白背景を確認、背景正面や頭身等の残差は別保存。
- 両役positive17組34枚を候補配布、5葉holdは旧公開維持、追加生成/文字消去0。hold=comic-lively/digital-modern/sharp-stylish/nineties-sharp/scratchy-dry。comic代表の肩袖ズボン主輪郭少量並走重ねはnative確認へ部位訂正したがapp整理単線でhold。digital app同上着面の系統点径grad、sharp代表主輪郭の入り抜き強弱、nineties代表縦長大眼裂、scratchy app乾欠けがnative未確認。代表/別役の初見positiveを合格で上書きせず保持し、片役だけを配布しない。
- graphic-flat app初見の曲線を全角形身体義務にせず、人物襟角/前端/袖折/袖口手首/ズボンの硬鋭線と短上瞼小黒瞳をnativeで確認へ部位限定訂正。建築だけを根拠にしない。元fit/defining_visibleは全44で保全しnative局所補足を分離、crop外は元全景保持。未実施別役nativeを済にしない。全44初見text none。
- 採用にも網点広用/近作業場道具や広場設備増/背景量/木目地面等質感/頭身近似/線幅/低踵/配達鞄追加/画角外を残差保持。全語数値完全再現ではなく、実年齢職務/物理枚数/カッター/定規/実画材engineは未証明。主描法不足を美しさや背景量の許容差で救済しない。
- 画像は元比率/長辺1024以下mono L、thumbは白余白384×512。旧23bundle276pair全record保持＋17=24bundle293pair候補。アプリ/試験/木/Caddy/認証/権限/workflow変更なし。固定SHA archiveを既存通常Actionsへ配置、本番healthy/readiness/API画像UI操作/最終receiptは別ゲート。廃止CIを再有効化しない。
- 直前checks207.53秒実測を根拠に私用collectorを回帰実行前300秒設定しdriver自身をpre/post入力へ含める。元product validator180秒/commands/合否/本番deadline不変、過去timeoutや手続false不変。
- 今回の連結prepare/回帰/統合の外側呼出は600秒指定でも420秒でtimeout。回帰8commandsは全exit0でresultと677pre/post/currentを保存済み、統合receiptは未完了だった。元driver/部分fixture/外側失敗を保全し、同じassertionsの別私用integration driverと新fixtureだけで統合を再実行。678pre/post/current一致、旧276/新17/34画像/非対象2739全field/restart不変を確認。回帰の不要再実行/製品や本番deadline弱化なし。


## 説明用2枚組：少年・時代劇／剣客（2026-11-08）

- 25葉50枚を1画像ごとの独立process/新turnで生成し、50完成・50固有session・拒否0。確定style6項目と場面原文で全50実見、native9。requested gpt-image-2.6-sunburstだがreported_model null/model_enforced false、実engine独立証明ではない。
- 成人旅人と行商人、閉じた無地扇/蓋籠、小袖/帯/袴/足袋/平草履、宿場/渡し場の独立一姿勢。旧16歳少年忍び/首布/手甲/逆手短刀/低い身構え/竹林を継承しない。styleとsceneを分離し、hatch/flat衝突は3葉だけ生成前両言語同長以下置換、他placement/旧公開不変。bg実key網羅/unknown停止、effectは道端/川岸の縁だけを要求。
- 両役positive17組34枚を候補配布。8葉保留は旧公開維持、追加生成/文字消去0。保留はcomic-lively/gentle-soft/pencil-soft/digital-modern/nineties-sharp/brush-wild/scratchy-dry/inkwash-quiet。
- comic代表はnativeで袴左外縁等の主輪郭少量並走重ねを確認し初見弱さを部位限定訂正。ただし別場面は整理単線で重ね未確認、pair除外。grad3代表は同小袖面の点径可変grad未確認、gentleは細均一線も未確認。nineties代表は眼裂横長で縦長大目未確認、別場面の縦長眼可視と分離。brush代表主輪郭大筆幅揺れ/かすれ、scratchy別場面乾欠け未確認。inkwash代表は筆幅とかすれ可視だが別の縁の拡散にじみ未確認。未実施別役nativeを済にせず、元fit/defining_visibleを保全しnativeは局所補足に限定。
- digital代表左奥軒下/brush別場面左上梁札の微小印は初見text uncertain。今回のnativeはその文字領域の再分類ではなく、未確定を残してpair除外。文字消去/再送/描法語のsceneへの後付けなし。
- 採用にも網点広用/近杭・門・川岸草石・木々家並みの増/背景量/木目水反射や編み質感/頭身近似/足袋曖昧や足指露出/扇先少開/背荷追加/服筆跡/画角外を残差保持。遠平形だけの完全再現とも全語数値完全一致とも主張しない。実年齢職務/物理トーン枚数/カッター/定規/実画材は画像から未証明。
- 画像は元比率を保持し長辺1024以下、mono L JPEG。thumbだけ384×512へ白余白。旧22bundle259pair全record保持＋17=23bundle276pair候補。アプリ/試験/木/Caddy/認証/権限/workflow変更なし。固定SHA archiveを既存通常Actionsで配置するが、本番健康/API/JPEG/日英UI/コピー/receiptは別ゲート。CI自動起動は廃止のまま。
- 直前checks197.21秒実測を根拠に、今回も私用testcollectorを実行前300秒へ設定してdriver自身をpre/postに含める。元product validator180秒とcommands/判定/本番deadlineは不変。過去timeout/手続falseを免除しない。


## 説明用2枚組への更新（方式採用済み・段階公開）

- 1枝に代表の絵と別場面の2枚。2枚を通して男女を含め、構図・題材・背景は枝の特徴に合わせる。一覧は代表のサムネイル、詳細は2枚と各生成文。元画の縦横比を保ち、足先や背景を一律の3:4 cropで落とさない。既存の白黒/彩色区分は維持。
- `tools/manga_catalog/generate_explanatory.py` は確定済みjobs JSONを検査し、`--run`がないと生成しない。1画像ごとに新process・新画像turn IDを使い、当該promptだけを送る。履歴・直前の画像・conversation IDの持越しを拒否。要求は `gpt-image-2.6-sunburst`、既存Codex経路のみ。認証情報は従来provider内で解決し、記録しない。
- 完了画像・要求・応答・モデルの要求値/報告値・実寸・画像SHAをgit外の作業先へ保存。完了分は依頼と画像SHAを照合して再利用。中断した要求は自動再送せず、使用上限/認証/不明エラーで次の波を止める。既定2並列、最大4。
- Storeの `put_sample_pair` とloopback専用 `/internal/sample-pairs/<id>` は両画像を検査してから一度のstate保存で切り替える。完全な新プロンプトを入れる場合も同じcommitで2枚を交換し、古い画像を再利用した言葉だけの変更は拒否。旧画像ファイルは保全。再取り込みは冪等。CLIは `python -m app.cli import-pairs`（JSONL）。本番への手動取込み許可を意味せず、公開は既存GitOps/Actionsと承認済み配布記録を経る。
- 2枚組の完全プロンプトは枝単位で完結させるため、親の古い背景・顔や共通網点制約を重ねない。従来枝の生成文・API・画像・版・比較は変更しない。新方式の語は2枚と対応付け、管理画面で変更した語は公開値と分けて再生成待ちとして保存する。新2枚がそろうまで公開プロンプトと版は変えない。変更後の生成文へ旧画像を付け替える取込、古い生成依頼で待機語を取り消す取込も拒否。1枚だけの置換は新方式の枝で拒否。
- 2026-11-07に本人が試作方式と可変縦横比を採用し、同方式での続行を承認。初回公開は `shojo-penonly` の代表＋別場面。低頭身試作の黒/トーン量・動作の部分適合は別に保持し、全5512枚を一括合格とはしない。
- `explanatory_bundles.json` は2枚組アーカイブのSHAと対象を固定する。`prepare_samples.py` の末尾から `prepare_explanatory.py` を呼び、32枝以内の小分け配布をすべて検証してから `seed/pairs/<bundle SHA>/` へ置く。全件を一度にメモリへ載せない。通常Actions/Docker起動時だけ承認済みpairを適用し、適用記録の同じpairは再起動で管理の待機語や後日の更新を巻き戻さない。旧画像を削除せず、置換前の枝state（APIトークン等の全体stateは含めない）を `/data/pair-history/` に固定SHA名で退避する。旧コードへ戻してもvolumeのpairが自動復旧されるとは限らないため、画像巻戻しは旧state/画像の保存記録を用いて別途行う。
- mainでCI自動起動が廃止済みのため、無断再有効化しない。新旧の回帰はローカルで実行し、検査の実行結果と未実施の配布/配備を分けて記録する。


Genko Studio の利用者が、ジャンルを 1段目 → 2段目 → 3段目 とたどってマンガの絵柄を選ぶサイトと、
Genko が読む API。見本の絵はすべて生成 AI で作る。実在の作家・作品の名前は、プロンプトにも表示にも入れない。

## 3段目・少年・不良／ヤンキーの説明用2枚組（2026-11-08）

- 23葉46依頼すべて完成/46固有session。全46原画を保存済み確定style/scene原文で個別実見、原寸8補足後、両役positive16組32枚だけを採用候補とする。7葉は旧公開維持、追加生成0。生成成功/採否/配布/本番受入は別記録。
- 保留7葉：comic代表の主輪郭重ね、digital代表の点径可変grad、nineties代表の縦長大目、delinquent-rough代表の乾欠け+縦長大目、brush代表の大筆幅揺れ+カスレ、scratchy別場面の主輪郭乾欠けはnativeでも未確認。fine-tall別場面の追加helmet極小印はnativeで未確定字形へ分類しhold（confirmed trueは印存在の確認で無文字合格ではない）。nineties別場面タンク印も初見未確定のまま、文字native未実施を済にしない。
- graphic-flat別場面はnativeで人物襟角/前端/袖折/袖口手首/ズボンの硬鋭線と短い上瞼+小黒瞳を確認し、初見不足を部位限定訂正。髪顔肩指曲線を不一致にせず、全曲線禁止/全角形義務を追加しない。元fit/defining_visibleは不変、native局所falseやglyph分類は別所見として保全。
- native返却にはcrop像を元全景と取り違えた「元全景でも足が画角外」等の文があり、その所見を保全した上で、指定region外の足/扉欠落や職業識別表示を新たな義務へしない。元初見で見えた全身/遠景は否定しない。digital/scratchy末尾の追加原寸crop未実施という文も保全し、今回指定region以外の追検証を主張しない。未実施別役nativeも未確認のまま。
- source6項目/catalog/実APIを照合。realistic-dense/scratchy-dry/muscle-hatch3葉だけhatchと顔/背景flat-tone衝突を生成前に両言語短縮整合。旧17歳少年/学生服/脱色髪/鼻絆創膏/両手ポケット/商店街参照構図は継承せず、成人配達員/バイク乗りの独立した一姿勢、無地jacket/丸首シャツ/ズボン/短靴、helmet/配達箱/工具case、路地/駐車場をsceneへ分離。
- bg実key全網羅/unknown停止/effect3葉は路地や駐車場の縁だけを生成前assert。それでも原画には近壁配管箱/細密バイク/駐車設備等が増え、網点量/背景量/線幅/頭身近似/服帯やパイピング/低踵/ケース位置/陰影/画角外とともに残差を保持。元fitとadopt_with_differencesを分離、全語数値完全再現false。実年齢/職業/画材/物理枚数/カッター/定規/engineは画像から断定しない。文字消去なし。
- 新32枚はmono L、元比率/長辺1024以下、thumb白余白384×512。要求gpt-image-2.6-sunburst、reported_model=null/model_enforced=falseで実engine保証なし。asset5627375bytes/SHA `d8ecfd3de8483f8da28fd512a7f643fd10f5147f63d33dc1541e6da5caaec031`。旧21bundle243全record保持+新16=22bundle259組。元job/原画/session/style/scene/実全文とJPEGを結合、画像はgit外。
- docs2+registryだけ。アプリ/試験/木/Caddy/認証/権限/保護/workflow不変。前cohortのchecks実測185.3秒を根拠に、実行前に私用collectorだけper-child300秒を設定しdriver自体をpre/post入力へ追加、元product validatorの180秒や本番deadlineを変更しない。同SHA17実装所見再利用/旧243同baseline隔離/日英UI/独立差分review→新PRhead固定merge/許可済みmain既存サービス別Actions→healthy/readiness/API画像UI/最終receipt正保存を別ゲートとする。過去手続falseは不変、廃止CI復活なし。

## 3段目・少年・冒険の説明用2枚組（2026-11-08）

- 25葉50依頼全完成/50固有session。全50原画を保存した確定style/scene原文で個別実見、原寸9補足後に両役positive18組36枚だけを採用候補とする。7葉は旧公開維持。追加生成0、生成・採用・配布・本番受入を分離する。
- 保留7葉：ligne-claire両役は写実的で細かな線だけの背景という描法が簡略模式表現に留まるため、背景量の許容差で救済しない。comic-lively代表の肩〜袖主輪郭重ねはnativeで確認し部位限定訂正したが、別場面はnativeでも未確認で組を保留。gentle-soft/pencil-soft/digital-modern各代表の点径可変grad、nineties-sharp代表の縦長大目、brush-wild代表の大筆幅揺れ+カスレは原寸でも未確認。gentle代表の細均一線不足も残る。別役の未実施nativeは確認済みにしない。
- graphic-flat両役はnativeで人物の襟/前端/袖/手首/裾/ズボン輪郭の硬く鋭い線と、短い上瞼線+小黒瞳を確認し初見不足を部位限定訂正。全曲線禁止や全角形身体の架空義務を足さず、crop外の足や全身は初見全景の所見を保持する。元fit/defining_visibleは上書きせず、局所nativeのfalseも別保存する。
- source6項目/catalog/実APIを照合。realistic-dense/muscle-hatch2葉だけhatchとflat-toneの衝突を生成前に両言語短縮整合。旧15歳少年/半袖/スカーフ/大リュック/帆船甲板/指差しを継承せず、成人道案内人/旅人、杖/籠/ロープと山道/川辺の独立した一姿勢をsceneへ分離。男女は組全体、低/高頭身と動作枝は全身、標準静止代表は顔手/別場面は全身。
- bg実keyを全網羅しunknown停止、effect3葉は尾根道/川岸の縁だけで詳細場面を混ぜない生成前assert。それでも生成された近景岩草や水面は残差として記録。主描法を可視確認した採用にも網点広用/背景量/樹皮ロープ等の質感/頭身近似/線幅/低踵/背負荷追加/袖まくり/持つ位置/画角外が残り、元fitとadopt_with_differencesを分離、全語数値完全再現false。実年齢/職務/物理画材/枚数/カッター/定規/engineは断定しない。全初見text none、文字消去なし。
- prepare_plans初回は一括置換がsource repo pathも未作成worktreeへ変えModuleNotFoundErrorで生成前停止0要求。原失敗を保存し実source repo指定だけ訂正してcanonical export/API照合後に生成した。metadata verifierのsession表示は実distinct数から出力し50を確認。前工程の誤stdoutや手続falseを遡及変更しない。
- 新36枚はmono L元比率/長辺1024以下、thumb白余白384×512。requested gpt-image-2.6-sunburstだがreported_model=null/model_enforced=falseで実engine保証なし。asset7437399bytes/SHA `2244fc17ece6f0824b1db406b2f4697207c31fe4618d1ffa123031fcab030bd1`。旧20bundle225全record保持+新18=21bundle243組。元job/原画/session/style/scene/全文と配布JPEGを結合し、画像はgit外。
- 初回ローカル回帰はchecks.pyがcollectorの180秒でtimeoutし後続未実行。元pre-SHA/部分logと0〜3の成功を保全、製品ソースを変えず私用collectorで同SHAのfailed+not-run4〜7だけ300秒枠で実行し、checks185.3秒を含め8commands成功を確認。既存driver/本番deadline/CIは変更しない。
- docs2+registryのみ。17同SHA実装所見を前工程から再利用し、通常seed+旧225同baseline隔離/非対象全field/restart/日英UI/独立差分review後に新PR/head固定merge/許可済みmain既存サービス別Actions。本番healthy/readiness/API画像UI/最終receipt正保存は別ゲート。廃止CI/認証/権限/workflow/本番直接writeは変更しない。

## 3段目・少年SF・メカの説明用2枚組（2026-11-08）

- 25葉50依頼すべて完成、50固有session。全50原画を確定style/scene原文で個別実見し原寸6補足、両役positive20組40枚だけを採用候補とする。保留5葉は旧公開維持。追加生成0、生成成功・採用・配布・本番受入を分ける。
- comic-lively代表の主輪郭少量重ね、gentle-soft/digital-modern各代表の点径可変grad、nineties-sharp代表の縦長大目、scratchy-dry別場面の主輪郭乾欠けが原寸でも未確認の5葉を保留。gentle代表は細均一線不足も残し、元defining_visible=false/fit=partialを不変とする。未実施別役nativeを確認済みにしない。全初見text=none、文字消去なし。
- cinematic-light別場面の初見顔影不足はnativeで顔左目外側→頬顎の皮膚黒ベタ影を髪/眉瞳/顎下首影から分離確認し、部位限定訂正。元fit partialは変えず、正確50%の追加義務もない。主輪郭と内部ハッチ、粒径と密度差、横長眼と縦長大目を区別する。
- source6項目/catalog/実APIを照合し、realistic-dense/scratchy-dry/muscle-hatch3葉だけhatchと顔/背景flat-tone衝突を生成前に両言語短縮整合。旧18歳パイロット/装甲スーツ/ヘルメット/巨大ロボット格納庫は継承せず、成人整備員/輸送係、スパナ/部品ケースと無地長袖作業シャツ等の独立した一姿勢をstyleから分離。男女は組全体、低/高頭身と動作枝は両役全身、標準体静止代表は顔手/別場面は全身。
- scene背景は実source key none/simple/effect/normal/dense/realclearを網羅、unknownは生成前停止。effect3枝rough-energy/effect-power/bold-blackには整備通路/貨物口の縁だけを与え、詳細作業台/配管/戸棚混入なしを生成前assert。それでも原画には近景の枠/設備/通路などを追加した差があり、集中線/主線/白黒面/人物構築の可視確認と背景量の残差を分離する。背景まで完全適合したとはしない。旧ミステリーboldの背景計画ミスや保留を遡及変更しない。
- 元fitと主担当adopt_with_differencesを分離、全語・全数値完全再現false。採用にも網点広用/背景設備増/強遠近/線幅/頭身近似/袖まくり/ケース位置/低踵/表面線/画角外を残差として保持。実年齢・職務・ケース内容・物理画材・トーン枚数・カッター/定規使用・engineは画像から断定しない。
- metadata verifierは全50sessionをassertしartifactへ正保存したが、末尾stdoutだけ旧unique_sessions=46 literalが残った。generation-verifier-stdout-correctionへ元stdout/実driverSHA/正50一意session根拠を保存。生成物や検証artifactを件数合わせで改変せず、再生成・再decodeのための再実行もしていない。
- 新40枚は全mono L、元比率/長辺1024以下、thumb白余白384×512。requested gpt-image-2.6-sunburstだがreported_model=null/model_enforced=falseで実engine保証なし。固定asset7177306bytes/SHA `84acd1754b2810e6b0e90ef61617fad2f417fbb4f6be5fcf073ce3678474a980`。旧19bundle205組全record保持+新20=20bundle225組。原画/job/scene/実全文/style/sessionと配布JPEGを結合し、画像はgit外。
- docs2+registryのみ。アプリ/試験/木/Caddy/認証/権限/保護/workflow不変。同SHA17実装の前工程所見を再利用、通常legacy+旧205組同baseline隔離Store/全非対象node/restart/日英UIと独立差分review後、新PR/head固定merge/許可済みmain既存サービス別Actions。本番healthy/readinessを先確認しAPI/画像/UI/最終receipt正保存を別ゲートとする。廃止CI復活なし、checks0をCI成功と呼ばない。

## 3段目・少年ミステリーの説明用2枚組（2026-11-08）

- 23葉46依頼すべて完成、46固有session。全46原画を確定style/scene原文で実見し原寸15補足、両役positive9組18枚だけを採用候補とする。14葉は旧公開維持。追加生成0、生成成功・採用・配布・本番受入を分離する。
- 採用はretro-showa/ligne-claire/fine-clean/graphic-flat/fine-tall/pen-classic/sharp-stylish/mystery-cool/shadow-dramaticの9葉。graphic-flat別場面の初見硬線/小線目不足は、nativeで人物襟/前端/袖/手首/ズボン輪郭の硬鋭線と小さな上瞼線+黒瞳を確認し部位限定訂正。元fit=partialは変えず、曲線禁止や全角形身体の架空義務は追加しない。
- 保留14葉：round-eyes-bright/dense-quiet/dark-fine/tone-layered-hot/realistic-denseは展示札/本紙面/本背glyphが原寸でも未確定。comic-livelyは代表主輪郭少量重ね、gentle-soft/pencil-soft/digital-modernは代表点径可変grad、nineties-sharpは代表縦長大目、brush-wildは代表主輪郭の大きな筆幅揺れ+かすれ、scratchy-dryは別場面主輪郭乾欠けが未確認。cinematic-light別場面の顔影なしはnativeで顔右目尻外→頬顎の皮膚影を髪眉瞳/首と分離確認して訂正したが、初見glyph未確定は未実施文字nativeで解決した扱いにせず保留。読めないだけで無文字合格にせず、可読文字と未確定glyphを分離する。
- bold-blackはsource背景key=effectをplannerがactionと誤照会し、両sceneへ詳細な資料室/展示室を入れた。原画も詳細遠近となり、遠い平形だけのstyleと不一致のためpair保留。元plans/jobs/request/原画を変えずplanning-scene-conflict-notesへ原因と所見を保全。他枝の独立positiveだけを先へ進める。保留別役の未実施nativeや画角外は未確認のまま、文字消去や回避生成なし。
- source6項目/catalog/実APIを照合し、realistic-dense/scratchy-dry2葉だけhatchとflat-toneの衝突を生成前に両言語短縮整合。旧巻き毛大学生/あご2指/タートルネック/洋館書斎構図を継承せず、成人博物館職員/資料整理員の独立した一姿勢、鍵/小箱、無地の袖付きシャツ/ズボンと場所をstyleから分離。男女は組全体、低/高頭身は両役全身、標準体代表は顔手/別場面は全身。
- 元fitと主担当のadopt_with_differencesを分離し、全語・全数値完全再現とはしない。採用候補にも網点量の増加/線幅/背景棚追加/約3.5頭身や高頭身近似/衣服陰影/低踵/画角外が残る。実年齢・職務・画材・物理トーン枚数・カッター/定規使用・engineは画像から断定しない。主輪郭と内部ハッチ、粒径と密度差、縦長大目と横長眼を混同しない。
- 新18枚はmono L、元比率/長辺1024以下、thumb白余白384×512。要求gpt-image-2.6-sunburst、reported_model=null/model_enforced=falseで実engine保証なし。固定asset2155710bytes/SHA `aff2db5be6af378b8b6d47b5fcc450076420f7e0eaf25b4bde928a73f8420f78`。旧18bundle196組全record保持+新9=19bundle205組。原画/job/scene/全文/style/sessionと配布JPEGを結合し、画像はgit外。
- docs2+registryだけ。アプリ/試験/木/Caddy/認証/権限/保護/workflow不変。同SHA17実装の前工程所見を再利用し、通常legacy+旧196組同baselineの隔離Store/全非対象node/restart/日英UIと独立差分review後、新PR/head固定merge/許可済みmainの既存サービス別Actionsへ進む。廃止CI復活なし、checks0をCI成功と呼ばず、本番API/UI/画像/healthyと最終receipt正保存を公開完了の別ゲートにする。

## 3段目・少年ファンタジーの説明用2枚組（2026-11-08）

- 25葉50依頼すべて完成、50固有session。50原画を確定style/scene原文で個別実見し原寸7補足、両役positive19組38枚だけを採用候補とする。6葉は旧公開維持。追加生成0、生成成功・採用・配布・本番受入は別記録。
- 保留はcomic-lively別場面の主輪郭少量重ね、gentle-soft/pencil-soft/digital-modern各代表の粒径可変網点grad、nineties-sharp代表の縦長大目、scratchy-dry代表の主輪郭の乾いた途切れが未確認の6葉。別役の未実施nativeは確認済みにせず、両役positiveだけ配布する。
- cinematic-light別場面の初見顔影未確認は、同原画nativeで目外側から頬/顎へ続く顔皮膚の黒影を髪/眉/瞳/顎下首影から分離して確認し、部位限定で訂正した。元fit=partialは不変。exact50%の面積義務を追加せず、元所見と補足を別保存する。
- source6項目/catalog/実APIを照合し、realistic-dense/scratchy-dry/muscle-hatch3葉だけhatchとflat-toneの衝突を生成前に両言語短縮整合。旧16歳魔法使い/魔法陣/親構図/参照画像を継承せず、成人旅人/宿主人/配達人の一姿勢ずつと荷物/宿をstyleから分離。男女は組全体、低/高頭身と体格/動作は全身、通常代表は顔手、別場面は全身。
- 低頭身/顔/線/白黒面/ハッチ等の主描法が可視の候補でも、頭身近似/線幅/網点量/背景や木目の増加/閉眼/衣服や低踵/画角外/遮蔽は差分として保持する。元fitと主担当の差分採用を分離し、全語・全数値完全再現とはしない。実年齢・物理画材・トーン枚数・カッター使用・定規実使用は画像から断定しない。主輪郭のかすれと内部ハッチ、大きい縦長目と横長眼、粒径と密度差を混同しない。
- 新38枚は全mono L、元比率/長辺1024以下、thumb白余白384×512。要求gpt-image-2.6-sunburstだがreported_model=null/model_enforced=falseで実engine保証なし。固定asset7391358bytes/SHA `28fc13d651461bc0ce3e2bbdb028875e07aa8da27453f17195d8737eccfbc9e4`。旧17bundle177組全record保持+新19=18bundle196組。原画/job/scene/実生成文/style/sessionと配布JPEGを結合し、画像はgit外。
- 変更はregistryとdocs2だけ。アプリ/試験/木/Caddy/認証/権限/保護/workflow不変。同SHA17実装の技術所見を前工程から再利用し、通常legacy+旧177組同baselineの隔離Store/全非対象node/restart/日英UIと独立差分reviewを確認後、新PR/head固定merge/許可済みmainの既存サービス別Actionsを使用する。廃止CI復活なし、checks0をCI成功と呼ばず、本番API/UI/画像/healthyと最終receipt保存を公開完了の別ゲートにする。

## 3段目・少年ラブコメの説明用2枚組（2026-11-08）

- 21葉42依頼すべて完成し、42原画を確定style/scene原文で個別実見。原寸13補足後、両役positiveの13組26枚だけ採用候補とする。8葉は旧公開維持。全42固有session、1画像1独立process/新turn/確定promptのみ、追加生成0。
- 保留はcomic-livelyの主輪郭重ね、gentle-soft/pencil-soft/digital-modern/blush-cuteの粒径可変grad未確認、dense-quiet/realistic-denseの本背glyph未確定、nineties-sharp代表男性目の縦長大構築未確認。文字と断定せず保留する。grad別役4件は初見の未確認を保持して除外、未実施nativeを完了扱いにしない。
- graphic-flatは初見で硬鋭線が未確認だったが、両役の原寸で人物の襟/前端/袖折/手首/ズボン等へ確認できたため部位限定訂正。曲線や丸い肩の存在を全角形化の義務へ拡張しない。cinematic-light/shadow-dramaticの別場面は顔皮膚の大きな黒影を髪眉瞳/首影と分離して原寸確認した。元fit=full/partialは維持し、主担当の差分採用と分ける。
- 6項目/catalog/実APIを照合。realistic-denseだけhatchとflat-toneの衝突を生成前に両言語短縮整合。既存color-gradationの土台line/faceは、保存したL3とL2実APIに共通の細柔線/丸大目白光3/丸幼顔/頬斜線へ送信前に具体化した。ranking-colorの肌/髪/服の色階調と背景色面を保持し、白黒トーン縛りを混ぜず他20monoをカラー化しない。
- 新しい成人書店員/客の一場面ずつをstyleから分離。男女は組全体、全身が必要な枝は全身。旧学校/親構図/参照画像は継承しない。採用にも線幅/網点量/背景量/頭身近似/閉眼/光点厳密数/服や低踵/画角外/遮蔽を残す。全語・全数値完全再現ではなく、実年齢/実画材/物理トーン枚数/カッター使用は未証明。
- 白黒24枚はL、既存彩色2枚はRGBで元比率を保ち長辺1024以下、thumbは白余白384×512。実job.expressionから私用builderの処理とprocessing説明を同時分岐し、archive→prepare→Storeでmode/寸法/SHAを確認する。合成RGB事前試験と実採用画像の取込受入は別記録。
- 固定assetは3673024bytes、SHA `e50a5d1bf5eb229dfc27e6efd95edec3c6e64c6dcd9ddbe1efdb7033c7a6ad4f`。旧16bundle164組の全record保持+新13=17bundle177組。画像はgit外、manifest/元job/原画/session/実生成文を結合。要求モデルはgpt-image-2.6-sunburst、reported_model=null/model_enforced=falseで実engine保証なし。
- 変更はregistryとdocs2だけ。アプリ/試験/木/Caddy/認証/権限/保護/workflowは不変。通常legacy+旧164組同baselineの隔離検証/日英UI/独立差分reviewを通してから新PR/head固定merge/許可済みmainの既存サービス別Actionsを使用する。廃止CIを再有効化せずchecks0をCI成功と呼ばない。配備成功・healthy・本番API/UI・最終receipt保存後のpublishedは別ゲート。

## 3段目・少年スポーツの説明用2枚組（2026-11-07）

- 24葉48依頼すべて完成し、48原画を保存済みの確定style/scene質問で個別実見。原寸10補足後、両役positiveの14組28枚だけを採用候補とする。10葉は旧公開維持。生成成功と画像採用/公開/本番受入を分け、追加生成はない。
- 保留はcomic-lively別場面の人物主輪郭の重ね線、graphic-flat別場面の硬く鋭い主線、gentle-soft/pencil-soft/sweat-fresh/digital-modern代表の粒径可変網点grad、cinematic-light/shadow-dramatic別場面の顔皮膚半面blackが原寸でも未確認。effect-power代表の靴タンとdense-quiet別場面の収納箱ラベル状の印は字形か通常形か未確定であり、実文字/署名と断定せず配布除外する。cinematic別場面の奥のラベルも未確定のまま、顔の影不足で除外。grad4葉の別役4件は初回未確認を保持し、未実施の原寸確認を完了扱いにしない。
- fitのfull/partialは元所見のまま保存し、主担当の差分採用と分離する。頭身・線幅・網点の広用・少量のsmooth/床反射・背景量・閉眼/髪や衣服の遮蔽・場面/姿勢/無地服の縁取り等の残差、画角外未確認を保持し、全語完全再現は主張しない。実画材/枚数/カッター/実年齢/実engineは未証明。原画実見サービスの接続失敗1件を保存し、原画と質問を変えず実見だけ再実行した（生成再送ではない）。result.pixel_sizeを配列と誤期待した初回検査のschema誤りも記録し、実際の文字列表記と独立decode寸法を照合した。
- 6項目/catalog/24実APIを照合し、新しい成人選手/コーチの一姿勢と競技施設の場面をstyleから分離。親の大きな目・汗・速度線や旧参照構図は継承しない。hatchの顔/背景flat-tone矛盾2葉は生成前に両言語元以下へ置換。muscle-mass--shonen-sports-muscle-massというexport専用keyを保持し、repairs/exportの由来を介して既存のwhite背景と彫刻線の網点・黒ベタ不使用を保全する。共有styleへ戻して別親へ漏らさない。
- style・実生成全文・独立新原画2枚を一組で更新し、旧15bundle150組全recordを保持して固定SHA asset14組だけ追加する。変更はregistry+文書2件、アプリ/試験/木/Caddy/認証/権限/保護/workflowは不変。前段の同SHA17実装所見を再利用し、通常legacy+旧150組同baselineの隔離Store/日英UI/独立差分review後、許可済みmainの既存サービス別Actionsで配置。本番受入は別ゲート。廃止CIは再有効化せず、checks0を成功とは呼ばない。

## 3段目・少年バトルの説明用2枚組（2026-11-07）

- 25葉50依頼から49枚が完成し、全原画を個別実見した。両役positiveの15組30枚だけを採用候補とする。muscle-hatch代表のprovider安全拒否を再送・言換えせず保全し、完成した別場面単体を配布しない。全50依頼成功とは扱わない。
- 原寸11補足を元所見へID/role/attemptで結合。chibi-comic代表の頭上印は普通の笑い強調マーク、retro-showa代表の標識はバス絵記号と横線/四角区画として、初回の文字様印疑いを解消した。comic-lively/scratchy-dryの人物主輪郭の重ね線/乾いた途切れ、digital-modernの粒径可変網点、cinematic-light別場面の顔皮膚black半面、nineties-sharpの縦長大目、ink-splashのblack縁にじみは原寸でも核心未確認。dense-quietの地図微小印、tone-layered-hotの器具印、brush-wildの缶印は字形か形/装飾か未確定で、読める文字とは断定せず9葉を視覚保留する。各保留組の別役4件は初回未確認のまま配布除外で、未実施の原寸確認を完了と数えない。
- 採用組も元fit（sharp-stylish別場面はfull、他はpartial）と差分採用を分離し、頭身・目・線幅・灰/網点量・smooth・背景密度・遮蔽・題材差を保全する。代表で見えない下半身の比率は未確認。実トーン枚数・カッター工程・実画材・実年齢・実エンジンや全語完全再現は保証しない。現場係という職務を画像だけで特定できないことは、元語にない記章等の追加義務にしない。
- 完成styleの6項目と実公開APIを生成前に照合し、題材を新しい成人現場係の日常活動へ分離した。旧怪物/刀/一律腰上の参照構図と親の顔・共通網点制約は継承しない。hatchと顔/背景flat-toneの衝突を3葉だけ生成前に両言語元以下で置換したが、共有定義や保留葉の旧公開語は変更しない。style・実生成全文・独立新原画2枚を一組で更新し、生成後の語付替えはない。
- 旧14bundle135組全recordを保持し、新しい固定SHA asset15組のみ追加する。変更はregistry・文書2件とchecks.pyの試験条件だけで、アプリ・木・Caddy・認証・権限・保護・workflowは不変。初回の旧親継承試験は新しく採用した枝完結styleまで親変更を継承すると誤期待して失敗したため、旧方式の通常seedを残してpair shardだけ除外するfixtureへ修正し、別試験で親変更時のcomplete pair全record/語/version/画像の再起動保持と旧方式兄弟のversion増分を同時保護する。初回失敗は保全し、仕様を変えて通さない。通常legacy seed+旧135組同baselineの隔離Store・日英UI・独立差分review後、許可済みmainの既存サービス別Actionsで配置する。本番受入は別ゲート、廃止CIは復活せず登録checks0を成功と呼ばない。

## 3段目・少年学園の説明用2枚組（2026-11-07）

- 23葉46依頼のうち45枚が完成し全原画を個別実見。代表と別場面が両方positiveの16組32枚だけを採用候補とする。初回27完成・安全拒否1で停止した記録を保持し、未送信だった別9分類18依頼だけを元job不変で有限継続した。digital-modern代表はprovider安全拒否のまま再送・言換えせず、完成した別場面単体も配布しない。全46件成功とは扱わない。
- gentle-soft / pencil-soft / sweat-fresh / blush-cuteは粒径可変の網点階調を原寸でも確定できず保留。dense-quiet / realistic-dense代表の本背の印は文字か罫線か原寸でも未確定で保留（読める文字とは断定しない）。保留6葉と安全拒否1葉は旧公開の語・見本を維持する。全体・原寸所見と厳密fit=partialを保全し、採用16組も頭身・目形・線幅・トーン量・背景密度・smooth・遮蔽・題材差の残る差分採用とする。物理的トーン枚数・カッター実使用・実年齢・実エンジンや全語完全再現を保証しない。
- 6項目の完成styleを枝完結語へ組み直し、人物・服・場所・姿勢は各題材に分離。新語と実生成文と新2枚を同時に更新し、旧親の顔・共通トーン制約・参照画像を引き継がない。生成前にrealistic-denseのno toneと顔/背景のflat-tone衝突を両言語元以下で解消したが、共有定義と非対象葉には適用しない。この保留葉の語を先行公開しない。
- 旧13bundle119組全recordを保持し、固定SHAの1asset16組だけ追加。変更はregistryと文書2件のみ。通常legacy seed+旧119組を同一baselineにした隔離Store・日英UI・独立差分レビュー後、既存サービス別Actionsの許可済みmainから配置する。本番受入は配置後の別ゲート、廃止CIは再有効化せず登録checks0を成功と呼ばない。アプリ・木定義・認証・権限・保護・workflowは変更しない。

## 1段目の説明用2枚組（2026-11-07）

- 10ジャンル20枚を独立生成して実見。初回4枝8枚、描法を短い完結語に置換して再生成した3枝6枚、比率や黒白を具体化して再生成した3枝6枚を選んだ。旧試作と語は別記録で保全し、選んだ画像と実生成文だけを同時更新する。
- 数値や微細指定の完全再現ではない。児童は約3〜3.5頭身（語は4）、4コマは約5.5〜6頭身（語は5）、ホラー代表は扉奥に少量の灰色が残る。主な線・目・黒白・体型を説明する見本として採用し、厳密未達所見も記録する。非現実的な頭身から実年齢を断定せず、任意の場面の再現率も保証しない。
- 現環境でGitHub Release assetのバイナリupload/downloadを実行し、既公開ペン線archiveの往復SHA一致を確認した。以後の新bundleは `release_tag` とasset名から直接取得して、従来どおり固定SHAと全画像/語の記録を検査する。既存 `release_bodies` 分割は保全し、両方の指定/不明なtag/不正なasset名は拒否する。従来の本文分割を全件へ増やす無駄を避けるだけで、認証・権限・課金・公開先を変更しない。

## 2段目・少年漫画の説明用2枚組（2026-11-07）

- 12分類24枚を独立生成・個別実見し、9分類18枚を初回から採用。保留3分類は場面を保ち、両言語で短く置換した完結styleで6枚を再生成した。太い筆と黒白面が見える時代劇の2枚を追加し、計10分類20枚を配布する。バトルと線で彫る劇画調は線・顔・骨格・背景密度の未達が残るため旧公開を維持し、新画像も語も採用しない。
- 採用は微細な全指定の完全再現を意味しない。冒険は約4〜4.3頭身（語は約5）で別場面の目の光が欠け、ファンタジーは約8頭身（語6〜7）・ケープが長め、ミステリーは顔以外の街灯・横断歩道にも白が広がる。顔を線で刻む美形は約9〜10頭身（語約8）、不良の別場面は三白眼・角顎が弱め。時代劇は太墨・黒白面が改善した一方、顔・腕の細線や石段の灰色が残る。ほかにも光点数、線幅、背景量等の微差がある。主要描法を伝える見本として差分つき採用し、厳密未達という元所見も保全する。
- 新しい固定SHAの1assetを既存3bundleへ追加するだけで、アプリ・木定義・Caddy・認証・workflowを変更しない。既公開の1段目10枝とペン線1枝、対象外の下位枝は保持する。配布前の実アーカイブ検証・隔離起動と日英スマホ幅/PC幅確認を経て、通常Actionsで配置し本番を確認する。画像原画、全生成要求と応答、採否記録、配布JPEGとの結合はgit外で保持する。

## 2段目・少女漫画の説明用2枚組（2026-11-07）

- 既公開のペン線1分類は保持し、残12分類24枚を独立生成・実見した。乙女ちっくの丸顔が弱かった2枚は、場面を変えず、元より短い完結styleへ置換して再生成。初回11組22枚と新しい乙女ちっく2枚を選び、計12分類24枚を配布候補とする。髪飾りなど見本固有情報は題材に分離した。
- 全指定の完全再現ではない。学園恋愛は約6頭身（語約7）、魔法少女は約3〜3.5頭身（語4〜5）と長めのマント、乙女ちっくは丸顔が改善した一方で別場面が髪込み約3.8頭身（語約5）。昭和の星の瞳は約6頭身（語約5）と少し細い顎が残る。ファンタジーの頭身とケープ丈、ラブコメの濃いズボンのトーン、背景や髪の線量、目の光の形・数も差がある。バレエ代表の手先等は一部画角外で、別場面の接地表現に軽い違和感がある。
- 芸能の別場面の灰色は原寸で確認し、微細粒状トーンと柔らかな光帯・床反射の明暗移行が併用される。全面が無粒子のぼかし主体という見立ては撤回したが、完全な平面トーン・ぼかしゼロとは扱わない。サスペンスの背景も完全均一な面ではない。主描法の見える見本として差分付き採用し、厳密未達という元所見と採用理由を分けて保持する。
- 新しい固定SHAの1assetを旧4bundle・21組へ追加する。アプリ・木定義・Caddy・認証・権限・workflowは変更しない。通常seedを両側へ含めた隔離起動と日英UIを検証後、既存サービス別Actionsを許可済みmainの検証済みmergeで実行する。既公開分・無関係の下位枝を保持し、本番公開後に画像とAPIと画面を確認する。

## 2段目・青年漫画の説明用2枚組（2026-11-07）

- 14分類28枚を独立生成・実見し、初回9組18枚を採用。保留5分類は場面を保ちstyleを両言語で短く置換して10枚を再生成し、犯罪・裏社会、ダークファンタジー、職業もの、美化しない写実の4組8枚を追加した。計13分類26枚を配布候補とする。アクションは速く荒い輪郭線が弱いため旧公開を維持し、新語も画像も採用しない。
- 戦記の灰色は原寸で粒状の平面トーンと短線・擦れの併用を確認し、全体が鉛筆の密線主体という見立ては撤回した。美化しない写実の初回は写真調の連続陰影と粒子感が優勢だったため不採用とし、明瞭な細ペン線と網点を具体化した新しい2枚だけを採用した。写真入力は使っていない。
- 全語完全再現ではない。犯罪・裏社会は黒側の目の白い隙間、細めの輪郭、約8頭身（語約7）や振り返りの弱さが残る。ダークファンタジーと職業ものも約8頭身寄りで、背景の線量や頬骨・あご等に差がある。歪む街は約4頭身（語5）、拙い人物は袖や清書感が整いすぎる。ほかにも灰色の粒感、目の光、冷汗、背景量、カートの動作や画角外の頭身等の残差がある。主要な顔・描線・面処理を示す差分付き見本として採用し、元の厳密未達所見も保全する。「無文字の地図」を白紙必須に変えるなど、元語にない失敗条件は加えない。
- 新しい固定SHA asset1件を旧5bundle・33組へ追加するだけで、アプリ・木定義・Caddy・認証・権限・workflowは変更しない。旧組と対象外の枝を保持し、通常seedを含む隔離起動、日英のスマホ幅/PC幅、独立レビューを経て既存サービス別Actionsの許可済みmainから配置。本番は別途readbackする。

## 2段目・女性漫画の説明用2枚組（2026-11-07）

- 全11分類22枚を1枚1process・固有turnで独立生成して個別実見し、同じ確定styleの代表＋別場面を11組の配布候補とする。男女は2枚全体で示す。百合は女性2人の代表と男性の別場面で同じ抒情的描法を示すもので、下流の人物性別を絵柄名から強制しない。
- 全語完全再現ではない。家族・育児は別場面が約5頭身（語6）、暮らしは約4（語5）、コメディも約3.5〜4（語5）。大人の恋愛の灯が多め、髪や衣服の階調、ラブロマンスの線量、オフィスの振り返り、時代ロマンの細線と人物の黒影量、耽美の背景密度と広い衣服トーンなどに差がある。主な人物構成と線・面処理が伝わる差分付き見本として採用し、画角外の比率や厳密な数値・光点数の達成は保証しない。
- 初回の視覚質問に元文にない条件の混入があったため、元所見を保存したまま確定文と照合して訂正した。時代ロマンの和柄は背景であり着物柄の義務ではなく、暮らしの髪は淡いトーンで白髪・瞳の白点の義務はない。耽美は多数の細線の髪と広い肩で、黒髪の白帯・細肩の義務はない。コメディの黒い笑口やサスペンスの下まぶた灰色も元要件ではない。時代ロマン・暮らし・耽美の6原画を確定文で再実見し、語も画像も変えずに判定を訂正。これは不適合な語への旧画像の付け替えや、未達事項の隠蔽ではない。
- オフィスは原寸で服の硬い灰色面の段分けが主体と確認し、補助的な弱い階調と背景下部の柔らかな濃淡は残差として保持。サスペンスの別場面は前髪とは別に鼻脇から口・あごへ続く黒い影面を原寸確認した。半面の厳密50%や完全な平面トーン・ぼかしゼロとは主張しない。実エンジンの独立保証もない。
- 旧6bundle・46組を保持し、固定SHA asset1件・11組22枚を追加する。アプリ・木定義・Caddy・認証・権限・workflowは変更しない。通常seedを両側へ含む隔離起動、日英のスマホ幅/PC幅、独立差分レビューを経て、既存サービス別Actionsの許可済みmainから配置。本番の画像・API・画面・操作は配置後の別工程で確認する。

## 2段目・児童漫画の説明用2枚組（2026-11-07）

- 11分類22枚を独立生成して実見。初回9組18枚を採用し、なぞときの細い目と図形モダンの棒状手足が弱かった2組は、場面を保ち元以下の長さの完結styleへ置換して4枚を再生成した。なぞときは細い横長の目が改善した新2枚を採用。計10組20枚を配布候補とする。図形モダンは人物の図形化と別場面の棒脚は改善したが、代表の幅ある脚が残るため旧公開を維持し、新しい語も画像も配布しない。
- 全語完全再現ではない。ホビー・スポーツは別場面が約3頭身（語4）、動物は約2.5（語3〜4）、ギャグは髪込みで約2頭身弱の箇所がある。動物の子犬には瞳以外に小さな黒い鼻があり、黒塗り禁止の厳密未達を保持。学習の黒目・球の濃淡、魔法の瞳の星形と周囲の白抜き星、おばけの白いレンガ塀や頭身、背景の線量・舗装・草、漫符数、振り向き等にも差がある。主な人物構成と描線・面処理が示せる差分付き見本として採用し、元の厳密不採用所見と主担当の採用理由を分けて保全する。
- 冒険の別場面は原寸で、髪・眉・瞳・首影とは別に目尻下から頬の側面・あご脇に続く黒い影面を確認し、初回の「顔の片側影不足」という見立てを撤回した。正確な半面積や顔全面の黒塗りを要求するものではない。なぞときの新2枚も背景に微細な階調や戸枠の描き込みがあり、顔以外の紙・手・靴の白も残る。厳密な頭身・完全平面・白抜き範囲の達成は保証しない。
- 旧7bundle・57組を保持し、固定SHA asset1件・10組20枚を追加する。通常seedを両側へ含む隔離Storeと日英のスマホ幅/PC幅、独立差分レビューを経て既存サービス別Actionsの許可済みmainから配置。本番の画像・API・画面・操作確認は配置後の別工程。アプリ・木定義・Caddy・認証・権限・workflowは変更しない。

## 2段目・劇画の説明用2枚組（2026-11-07）

- 承認済み段階展開。12分類24枚を独立生成・個別実見後、初回9組18枚、同一styleの別場面を保持して代表のみ新候補を作ったひげ太体1組、人物の黒白対比へ具体化して両画像を再生成したハードボイルド1組、計11組22枚を配布候補とする。冒険活劇は短いstyleで2枚とも再生成したが眉下の独立した顔皮膚影が未確認で両attempt保留、旧公開を保持する。
- 男女は2枚組全体で示し、ひげ太体の男性限定形を女性へ強制しない。ひげ太体は初回代表の髪小印が文字か髪描写か原寸でも未確定だったため、style/題材完全不変で代表だけ新独立候補を作った。第2代表では署名様小印が見当たらず、初回別場面と同一literal styleでrole別の実job/原画/session/attemptへ結合。元小印を署名と断定せず元holdも保全し、採用画像を偽装コピーしない。
- 主描法の可視を採用理由とし全語完全再現とはしない。時代劇の肩袖裾の筆太細と黒で切り出す形、任侠の幅広顔/slit目と黒白、刑事の整理細線と顔の硬縁中灰影、戦記の灰沈み/疲頬、社会派の低contrast平灰、スポーツの汗白光/飛滴/張る顎首/人物勢い線/集中線、怪奇の広白目と顔皮膚の硬黒影、歴史の静線/鼻筋/淡中灰、凄惨の全面溝線/見開き小瞳/歯と歯ぐき、ひげ太体の体形/黒ひげ、ハードボイルドの強黒白人物と淡霧背景を確認。凄惨別場面の上歯付根に数pxの灰歯ぐきを原寸確認、下歯ぐき同時露出を追加条件にしない。
- 顔手の細い整線、全輪郭少筆未達、髪細部、滑らかな階調、灰面積、限定顔影、線幅・頭身（スポーツ別場面約9〜10頭身等）、背景過密、画角外、遮蔽、題材差を保持。怪奇の灰はliteralで禁止されておらず白黒漫画を二値限定と誤読しない。ハードボイルドの顔皮膚に黒面影を必須とする追加義務も作らない。元fit=partial/保留と主担当の差分採用を分離し、制作順序・実画材・実運筆回数・実年齢・実engineを保証しない。傷口・流血なし。生成29枚と採用候補22枚を区別。
- 旧12bundle108組の全recordを保持、新asset `manga-explanatory-20261107-l2-gekiga.zip` の11組のみ追加。2,840,376bytes、SHA `494ec0d8a90303f7fefb5c98ac079efc8199739cc3ed37afa631fc0a53585f3e`。原画・実job・所見・原寸補足・role別由来はgit外 `~/manga-style/samples/explanatory-l2-gekiga-20261107/` へ保存。変更sourceはregistry+文書2件のみ。
- 通常legacy seed＋旧108組同一baselineの隔離Storeで対象更新/非対象全node全field不変/再起動不変を確認、日英/390・1280pxを検証して独立差分reviewへ。新PR/head固定merge、既存サービス別Actionsの許可済みmain同mergeで通常配置する。廃止CIを再有効化せず登録check0をCI成功と呼ばない。配備後API/画像/画面/コピー/healthyは本番受入として別確認し、最終receipt保存成功後だけ台帳公開へ進める。

## 2段目・エッセイ漫画の説明用2枚組（2026-11-07）

- 承認済み段階展開。10分類20枚の独立生成・個別実見後、初回7組、同一styleの代表を保持して別場面だけ単一姿勢へ作り直した健康1組、硬縁の平面影へ具体化して2枚とも再生成した仕事1組、計9組18枚を配布候補とする。旅行は場面不変・短いstyleで2枚再生成しても人物主輪郭の短線gap不足が残るため、両attemptを保留し旧公開を保持する。
- 各枝は代表＋別場面、男女は組全体で示す。新しいstyleには題材・人物・場所・服を混ぜず、親の旧顔や旧overrideを重ねない。健康は初回代表と第2別場面のstyleが完全同一で、各roleの実job/原画/session/attempt由来を保持する。複数段階の体操だった初回別場面を配布へ含めず、代表を新attemptへ偽装コピーしない。仕事はstyle変更に伴い両画像を新規生成。全jobのstyle digestはja/en/tags完全3key。
- 主描法の可視性を理由に差分採用。日記の縦線目・白線画、育児の丸いちび体形、食の丸顔体・太丸線・白い照り、人物自身にも短い断続線と淡髪を使うペット、太均一マーカーと丁寧な小物の趣味、鼻なし横線目の単純人物と写実的な描線背景のルポ、丸目の白光・頬斜線の恋愛、白主体でno toneの健康、硬縁平面灰影へ改善した仕事を確認。仕事の原寸所見は影が主に硬縁平面と確認する一方、複数灰/一部内部smooth/目白光未確認を保持する。灰1色の完全再現とはしない。
- 頭身、線量、濃灰髪、目白光数、滑らかな服・背景階調、背景の描き込み、画角外、遮蔽、題材動作差は残差として記録。初回/追加のfit=partialや保留を上書きせず、実画材・運筆回数・実年齢・実engine独立保証も主張しない。生成25枚と採用18枚、配布前候補と本番受入を区別する。
- 旧11bundle99組の全recordを保持し、新固定SHA asset `manga-explanatory-20261107-l2-essay.zip` の9組だけ追加する。1,812,764bytes、SHA `b835f35d4d9c318a6789c0e5bd54dc7ebdcf70d856b7c9724661145fabcf2c91`。画像原画・job・実要求・所見・role別採用・固定manifestとの結合はgit外 `~/manga-style/samples/explanatory-l2-essay-20261107/` に保全する。registry+文書2件以外のsourceは変更しない。
- 通常legacy seed＋旧99組を同一baselineへ入れた隔離Storeで対象だけ更新・非対象全node不変・再起動不変を確認し、日英/390・1280pxを検証する。独立差分review後、新PR/head固定merge、既存サービス別Actionsの許可済みmainへ固定して通常配置する。廃止CIを復活させず、check0をCI成功と呼ばない。配備後のAPI/画像/画面/コピー/healthyは別の本番受入とし、最終receipt保存成功後だけ公開台帳へ進める。

## 2段目・ホラー漫画の説明用2枚組（2026-11-07）

- 全10分類20枚を独立生成し、確定styleと別題材を分けて個別実見。初回から怪談・心理・宇宙的恐怖・民俗・学校・少女・異形・都市伝説の8組16枚を採用し、配布候補とする。妖怪とパニックは人物輪郭の墨筆強弱・荒い速描が弱いため保留。場面不変・元以下の長さのstyleで4枚を再生成したが、妖怪は主輪郭が滑らか、パニック代表も長い連続線が主体で核心不足が残るため2組とも旧公開を保持する。パニックの第2別場面は単体で改善を認めても、代表が未採用なので組として配布しない。
- 全語完全再現ではない。怪談は濃灰の髪、細筆の抑揚、約8〜8.5頭身（語7）と背景量、代表の床反射の滑らかな明暗移行が残る。心理の壁・戸口の歪みは控えめで通常遠近も混在、約7.5〜8頭身と弱い壁階調。宇宙的恐怖は角形の人物・直線・幾何学黒影と無トーンの対比が可視だが、男性約8頭身（語7）、袖等の一部曲線や研究器具の追加がある。
- 民俗は広い昼白と鋭い黒影・小さな黒目を示すが、線が清書寄りで背景の石垣・建具が多い。学校は約3〜3.3頭身（語4）で制服・机・空やバケツに連続階調。少女は大きな瞳・白い光・まつげと夜の黒影が男女で見える一方、約8頭身（語7）、広い灰色の服と粒状感、温室の葉・床の細部が残る。
- 異形は溶けた墨のようにしたたる黒影縁が背景・戸口へ出る。元語は人物自身の影だけに限定していない。青白い面長顔と小瞳は可視だが、汗は光というより白い滴、輪郭線の震えは弱く、周囲の震え記号とは区別する。衣服の灰色面も広い。都市伝説は頭上の丸い光と円外の黒、現実寄りの目・細線が可視だが、光縁・壁床に連続階調、約8頭身強（語7）と配管・ひび・擦れが残る。元のfit・未達所見と主担当の差分採用を分けて保全し、実年齢・実画材・描画速度・一筆の運筆回数は画像から断定しない。
- 旧10bundle・91組を保持し、固定SHA asset1件・8組16枚だけ追加する。生成jobのstyle hashは日英とtagsの完全styleを対象とし、実生成全文・原画・固有session・配布JPEGを結合。アプリ・木定義・Caddy・認証・権限・workflowは変更しない。通常legacy seedを両側へ含む隔離Store、日英のスマホ幅/PC幅、同SHA実装所見を再利用する独立差分レビュー後、既存サービス別Actionsの許可済みmainから配置し本番の画像・API・画面・操作を確認する。

## 2段目・ギャグ漫画の説明用2枚組（2026-11-07）

- 全13分類26枚を独立生成して個別実見し、初回9組18枚を採用。シュール、ファンタジー、昭和、汚しギャグの4組は、場面不変・両言語とも元以下の長さのstyleで8枚を再生成し、新8枚だけを追加する。全13組26枚が配布候補であり、公開後の受入は別工程。初回4組の保留所見・原画・要求は上書きしない。
- シュールは写実ペン・網点・黒い顔影と短い白い筒胴との落差が改善。ただし約2〜2.5頭身（語4）で脚は幅あるズボン形、机や郵便受けにも網点が入る。ファンタジーは空内だけ網点となり、空外の白い面との対比を確認。約4〜5頭身、線幅差・草花量・荷物が残る。新語の「白い輪郭線/white outlines」は線色を白と解するなら未達で、実画は白地の黒輪郭。元の空外無トーンという主描法に基づく差分採用であり、語を画像へ付け替えたり完全適合としない。
- 昭和は原寸でも初回の太い囲み口と肉厚の唇を区別できず保留したが、新2枚は口穴を幅ある白い唇が囲む。約2.5〜3.5頭身（語4）、線幅差と衣服・背景・カップの連続階調は残る。汚しは初回原寸で歯ぐき未確認、新代表は広い帯、新別場面は細い歯ぐきまで可視。別場面は新語の幅広い帯には未達、粗いかすれも弱く細密線主体の部分がある。しわ・ぎょろ目・不揃い歯・歯ぐき・骨ばり・無トーンの主描法で差分採用し、髪線量、黒ベタ、交差線、両手かご、背景の傷も保全する。
- 初回採用にも残差がある。ドタバタは約2〜2.5頭身（語3）、別場面の残像は頭後ろの2〜3弧で全身輪郭重複ではない。学園は別場面約5頭身（語4）、ちびの袋・服に淡い連続階調、ブラックは約4〜6頭身（語3）で影の縁に粒やぼけ、ラブコメは約6.5〜7（語6）と光点の厳密数未確認。スポーツは別場面約5（語4）・汗多め、ホラーは約4〜4.5（語3）。ヘタウマは線の乱れといびつさが弱めで細い二重輪郭の腕、人形大人は約5（語4）。元語にない一本線腕必須・上下唇分離必須・各自別かご必須・しわ面積100%等を採否条件へ足さない。全語完全再現や任意場面の再現率は保証しない。
- 生成jobのstyle hashは日英本文2項目、配布manifestのcomplete_style hashはtagsを含む3項目を対象とする。元job/completeは書き換えず、日英全文prompt、同組2role、原画、各session、配布JPEGを実値で結合し、hashのscope差も別記録へ保持する。
- 旧9bundle・78組を保持し固定SHA asset1件・13組26枚を追加。アプリ・木定義・Caddy・認証・権限・workflowは不変。通常legacy seedを両側へ含める隔離Store、日英のスマホ幅/PC幅、独立差分レビュー後、既存サービス別Actionsの許可済みmainから配置し本番の画像・API・画面・操作を確認する。

## 2段目・4コマ漫画の説明用2枚組（2026-11-07）

- 全11分類22枚を独立生成・実見。各画像は1場面の見本で、4コマの枠やページ配置を生成文に加えない。初回10組20枚を採用し、ストーリー4コマの代表背景が写真調に寄ったため、場面不変・元より短い完結styleで2枚とも再生成。人物・建物・地面へペン輪郭と平らな網点面を具体化し、新2枚を追加して11組22枚を配布候補とする。
- 全語完全再現ではない。家族は約3.6頭身（語4〜5）、動物は約2.8（語4）、新聞風は約3〜3.3（語4）、ギャグは約2寄り（語3）、ファンタジーは約5（語4）、趣味は約6（語5）、職場は約7〜7.5（語6）。学園の光点数や線幅、新聞風のC形寄りの鼻、背景量・衣服トーン・星・漫符・動作等にも差がある。主な顔・体の構成、描線と面処理が伝わる差分付き見本として採用し、元の厳密不採用所見も保全。見た目のデフォルメから人物の実年齢を断定しない。
- 職場の女性は原寸で、面長の大人顔・明瞭な顎と小〜中の目・主な白い光1つを確認し、初回の丸大目という見立てを訂正。男らしい強い顎は元文の義務ではない。丸い餅の形の人物は2枚とも、首のない頭胴連続体と小さな丸い突起手足が成立し、丸顔に普通の胴体を付けただけではない。網点のまだらさや髪の線量などの差は残る。
- ストーリーの初回代表背景は原寸でも連続階調が主だったため不採用のまま保持。再生成した代表は反射まで線・網点・白黒面が主体となり、別場面も明瞭なペン線が主体。ただし別場面は約8頭身（語6〜7）で、空・ガラス・金属帯に広い濃淡が残る。目の光2つも厳密未確認。改善した主描法を示す差分付き採用で、完全な平面階調・数値達成を保証しない。
- 旧8bundle・67組を保持し、固定SHA asset1件・11組22枚を追加。通常seedを両側へ含む隔離Store、日英のスマホ幅/PC幅、独立差分レビュー後、既存サービス別Actionsの許可済みmainから配置する。アプリ・木定義・Caddy・認証・権限・workflowは不変。公開後の画像・API・画面・操作確認は別工程として実施する。

## 置き場所

| もの | 場所 |
|---|---|
| アプリ（公開ページ・API・管理画面） | `costlab-auth/manga/`（コンテナ `manga-style`、compose は `costlab-auth/docker-compose.yml`） |
| 木の定義（1〜3段目の名前・説明・言葉） | `tools/manga_catalog/`（`genres.py`・`styles.py`・英語の表示は `i18n_en.py`） |
| コンテナに入る木 | `costlab-auth/manga/app/catalog.json`（**手で直さない**。`python3 tools/manga_catalog/export_site_tree.py` で作る） |
| 見本の絵・管理の状態 | named volume `costlab-auth_manga_style_data`（コンテナの `/data`）。**git に入れない** |
| 最初の見本（試作の 2 枚） | `costlab-auth/manga/app/seed/`（空の volume で起動したとき 1 回だけ取り込む） |
| Caddy | `caddy/Caddyfile` の `manga.akiba.tokyo.jp`（`/admin` だけ costlab-auth のログイン） |

デプロイは他の costlab-auth のサービスと同じ（`costlab-auth/**` が main に入ると akiba-deploy が
`costlab-auth-deploy.sh` を走らせ、compose 全体を build → up する）。管理者の追加操作は要らない。

## 公開ページ

- `/`（1段目）→ `/n/<id>`（2段目・3段目）。`?lang=ja|en` で画面の言語、`&plang=ja|en` でプロンプトの言語。
- 枝のページの並び（本人の指示）: 上に次の段の選択肢 → 見本の絵 → プロンプト → 「この絵柄を使う」と API の URL。
  下の段がある枝で見本がまだ無いときは、空の見本の枠を出さない。PC では見本を左、プロンプトと URL を右に並べる。
- 「この絵柄を使う」（`genko://use-style?id=<id>`）は、どの枝のページにも出す（2026-09-28、Genko の試験で
  共有された URL から Genko に渡せなかったため）。普通のブラウザでは「Genko Studio で開きます（Genko が入っていないと
  何も起きません）」を添え、その下に「URL をコピー」（`https://manga.akiba.tokyo.jp/v1/styles/<id>`）。
  Genko の中（`?client=genko` か User-Agent に `GenkoStudio`）では今までどおりボタンだけ。
- 題名は枝ごとに一意ではない（3段目の絵柄は、どの 2段目の下でも同じ題名）。名前だけで伝わって別の分類の絵柄が
  選ばれ、制作をやり直したことがある（2026-09-28）。そのため:
  - 枝のページは、題名のすぐ上に分類の道筋（例: ギャグ漫画 › シュール › ゆるい手描きの落書き風）、題名の下に id を出す。
  - 同じ題名の絵柄がほかの分類にあれば、ページのいちばん下（API の URL の下）の「同じ名前の絵柄」で知らせ、
    道筋付きのリンクを並べる（同じ 1段目の中を先に）。お知らせは初め題名の下に出したが、このサイトはプロンプトを
    取りに来る所なので、本人の指示で下に移した（2026-09-28）。
  - 一覧のカード・検索結果・管理画面の表にも、題名の上に分類を添える。
  - 「プロンプトをコピー」「URL をコピー」は、先頭に「絵柄: <分類の道筋>（id: <id>）」の 1 行を付けてコピーする。
- `/search?q=<言葉>`: 名前・分類（日英）・説明・id から探す（スペース区切りは全部を含むもの）。最初の 200 件まで。
  トップページと、全ページのヘッダー（「絵柄を探す」）から入る。

## API（Genko が読む。形を変えない。欄は足すだけ）

- 使い方のページ: `https://manga.akiba.tokyo.jp/api`（全ページの一番下からリンク。日英。中身は `costlab-auth/manga/app/api_doc.py`）。
  API の欄を足したら、このページの欄の一覧も足す（検査で、API が返す欄とページの欄の一致を見ている）。
- `GET /v1/tree` … 公開中の木。`?lang=en` で英語の名前（既定は日本語）。
  - `path`（2026-09-28 追加）: 1段目からその枝までの題名の並び（最後がその枝）。例: `["ギャグ漫画", "シュール", "ゆるい手描きの落書き風"]`。
- `GET /v1/styles/{id}` … 1 つの枝。`prompt` は ja・en・tags を両方持つ（題材は入れない）。
  `samples[].prompt` はその絵を作った言葉。`license.generated` は常に true、`artist_names` は常に false。
  - `path`: 上の段（1段目から親まで）の `{id, title}` の並び。上の段から順。1段目は空の配列
    （2026-09-28、Genko 側の前提に合わせた。それまではその枝自身も最後に入っていた）。
  - `prompt`: 1段目は「共通＋1段目」、2段目は「共通＋2段目」、3段目は「共通＋2段目＋『仕上げの絵柄（上と違う所はこちらに従う）: 』＋3段目」。
    3段目の言葉が 2段目の言葉と食い違う所（ベタの量・頭身など）は 3段目が勝つ（2026-09-27、Genko 側の指摘で見本と同じ形にそろえた）。
  - `reference`: 絵柄の基準として一番よい見本の番号（`samples` の何番目か、0 から。依頼の仕様どおり）。見本は各枝 1 枚なので、
    見本があれば 0、無ければ null。参照画像の枚数ではない。
  - `model.version`: その見本を作った画像生成のモデル名（依頼の仕様「分かれば」）。
  - `children`（2026-09-27 追加）: 公開中の 1 つ下の段（`id`・`title`・`summary`・`thumbnail_url`）。3段目は空。
    エージェントは `/v1/styles/{1段目}` → `children` → `/v1/styles/{2段目}` → `children` とたどれる。全件は `/v1/tree`。
- 見本の絵を差し替えるか、その枝か上の段の言葉を変えると、`version` が上がり `updated_at` が変わる。
- CORS は GET だけ。限定公開（管理画面で切り替え）のときは `Authorization: Bearer <トークン>` が要る。

## 管理画面（https://manga.akiba.tokyo.jp/admin）

ログインは keiba・stock と同じ ID・パスワード（costlab-auth）。できること:

- 木の確認と修正（表示名・説明・この段の言葉を日英で。実在の名前・かぎかっこは保存できない。「元の内容に戻す」あり）
- 枝を隠す・公開する（隠すと、その下の段も含めてサイト・API・画像から消える）
- 絵の作り直し（「作り直しを頼む」で一覧に載る。画像のアップロードで差し替えもできる）
- API の限定公開とトークン（トークンは作ったときに 1 回だけ表示。保存するのはハッシュだけ）

## 見本の絵を入れる（Hermes の作業）

```sh
docker exec manga-style python -m app.cli queue                      # 作り直しの一覧
docker exec manga-style python -m app.cli prompt <id> --lang en      # その枝の見本のプロンプト
docker exec -i manga-style python -m app.cli put <id> - --model-version gpt-image-2.5-sunburst < picture.png
docker exec -i manga-style python -m app.cli import < samples.jsonl  # 承認済みの見本をまとめて入れる
```

`put` は PNG/JPEG を 768×1024（3:4）にして保存する。既存の白黒枝は L、新しい彩色枝（差し色を含む）は RGB を保持し、プロンプトを記録し、版を上げ、作り直しの依頼を消す。
`import` は 1 行 1 枚の JSON（`id`・`image_b64`・`prompt {ja, en}`・`model_version`・`created_at`）を読み、
**その絵を実際に作ったプロンプト**を記録する。同じ絵と同じプロンプトをもう一度入れても何も変わらない（やり直してよい）。
`/internal/*` はコンテナの中（127.0.0.1）からしか通らない。Caddy でも 404 にしている。

## 言葉の組み立て（2026-09-27 本人が 1段目・2段目を承認）

- API の `prompt`: 1段目は「共通＋1段目の言葉」。2段目から下は「共通＋2段目以下の言葉」で、**1段目の言葉は足さない**
  （2段目の言葉はそれだけで完結した絵柄。1段目を足すと 1段目の顔に戻る）。
- 共通の言葉は画材の決まりだけ（白黒、影はベタ・中間は網点・光は白、ぼかし禁止）。顔・目・線・頭身は各段の言葉に書く。
- 見本の絵: 1段目は全ジャンル同じ人物（`genres.py` の `CHARACTER`）と場所で 1 枚。2段目は 2 枚で作る。
  1枚目＝そのジャンルらしい場面（`scene.l2_scene`）を 1段目の言葉で、2枚目＝1枚目の絵を渡して 2段目の言葉で描き直す
  （`build_tree.L2_EDIT`）。記録するプロンプトは 2 枚分をつないだもの。
- 承認済みの見本は全 2,734 枝（1段目 10・2段目 117・3段目 2,607）。`tools/manga_catalog/approved_samples.json`
  （画像の sha256、その絵を作ったプロンプトの sha256、その絵を作ったときの API の `prompt` の sha256）。
- **プロンプトは絵と組で変える**（2026-09-27 本人「プロンプトを更新する場合は、必ず絵も更新しなさい　これは絶対です」）。
  木の言葉を変えて、見本を作った言葉か API の `prompt` のどちらかが記録と食い違うと検査が落ちる。言葉を変えたら、
  その言葉で絵を作り直して記録ごと入れ替える。古い言葉を絵のために残す欄（以前の `sample_words`）は置かない。
  管理画面で言葉を直したときは、ほかの言葉で作った見本がある枝が自動で「作り直しの一覧」に載る。
- 3段目の見本（2026-09-27、本人の指示で 2段目の見本とは別の絵から作る）も 2 枚で作る。
  1枚目＝その 2段目の元の場面（`l3_scenes.py` の `L3_SCENES`）を 2段目の言葉で、2枚目＝1枚目の絵を渡して
  「2段目の言葉。仕上げの絵柄（上と違う所はこちらに従う）: 3段目の言葉」で描き直す。
  元の場面は、そのジャンルの今の人気作を調べて主役と舞台の型だけを取った（作品名は入れない）。バトルは学生にしない。
- 3段目の言葉のうち、共通の「ぼかし禁止」と食い違う 3 語（鉛筆の線・グラデーショントーン・墨のにじみ）は、
  ぼかしを使わない言い方に置き換えた（長さは元以下）。

## 絵柄の追加（2026-09-28 本人「インターネットから調査して、今のカタログシステムに載っておらず明らかに異なる絵柄を探しなさい」「OKです、追加しましょう」）

- 3段目の絵柄に 16 件を足した（103 → 119 絵柄、3段目 2,181 → 2,244 枝）。例: ヘタウマの味、引目鉤鼻の大和絵、浮世絵の平らな面、
  切り絵、影絵のシルエット、黒地に白い削り線、銅版画の平行線、欧州のくっきり線、ゴム手足の昔のアニメ、大きな網点のポップアート など。
- 選び方: 外部の資料（百科事典・技法の解説）で見た目の特徴を確かめ、今の 6 項目の言葉では表せない絵柄だけを残した。
  今の絵柄に近いもの、見た目を資料で確かめられないものは外した。調べた記録と出典はリポジトリの外
  （作業場所の `research/new_style_report.md`）に置く。成果物に実在の作家・作品の名前を残さない決まりのため、ここには書かない。
- 6 項目の値を 27 個足した（線 5・ベタとトーン 6・目と顔 9・頭身 3・背景 3・雰囲気 1）。どれも同じ項目の今の一番長い言葉より短い。
  今ある値と絵柄は 1 字も変えていない（今ある 2,291 枝の見本の言葉と API の `prompt` は変わらず、絵も作り直していない）。
- 見本は今までの 3段目と同じ作り方（2段目ごとの元の場面を、新しい絵柄の言葉で描き直す）。
- 同じ日に、顔と体の作りを丸ごと変える 2 つ（ヘタウマの味・図形で組んだモダン）は 2段目に移した
  （本人「大きく絵柄が変わるのであれば第2段とかでは？」「進めなさい」）。3段目の見本は 2段目の言葉で描いた場面を
  描き直すので、2段目の顔に戻り、この 2 つは出なかった。2段目なら顔・線・体の作りを言葉に書ける。
  - 2段目「ギャグ漫画 > ヘタウマの味」と「児童漫画 > 図形で組んだモダン」を足した（2段目 100 → 102）。言葉と元の場面は
    今の作品を調べて書いた（作品名は入れない）。
  - 3段目から 15 枝を外した: ヘタウマの味 5・図形で組んだモダン 4、候補から選んでも元の場面に近いままだった 6
    （大きな網点・引目鉤鼻・浮世絵・大正の抒情画 各 1、縦読み漫画の美形 2）。外した枝のほかの枝の言葉と絵は変えていない。

## 日本の漫画から足した絵柄（2026-09-28 本人「日本の漫画から…今の絵柄カタログのプロンプトで描ける絵は除外」「有名マンガ以外のものや成年マンガは無いのですか？」「OKです　それぞれの絵柄のプロンプトを実装しなさい」）

- 少年・少女・女性・青年・ガロ系・ホラー・ギャグ・児童・BL・成年（エロ劇画・ゲイ漫画・レディースコミック・おとな漫画）、
  有名作以外の古い作品やインディーから、本文の絵を集めて見た。今の枝の見本と横に並べて、今の言葉では出ない 17 の絵柄を選んだ。
  調べた記録と出典は作業場所（`research/jp_manga/`）に置く。成果物に実在の作家・作品の名前を残さない決まりのため、ここには書かない。
- 顔と体の作りから変わる 9 つは 2段目に置いた（2段目 102 → 111）。言葉は、顔の形・目・頭身・線を具体的な形の言葉で書いた
  （抽象語では上手な絵に戻った、ヘタウマの経験から）。長さは今ある 2段目の最長以下。
  - 少年漫画 > 顔を線で刻む奇抜な美形、少女漫画 > 70年代の乙女ちっく・昭和の星の瞳、女性漫画 > 90年代の耽美、
    青年漫画 > 手描きで歪む街・簡単な顔とペンの風景、劇画 > 皮膚を刻む凄惨な劇画・ひげと太い体の男たち、
    ギャグ漫画 > しわだらけの汚しギャグ。
  - 「簡単な顔の人物＋ペンで描き込んだ風景」の系統（6 人の作家に共通）は、2段目 1 つ（簡単な顔とペンの風景）にまとめ、
    違いを 3段目にした。
  - 成年の絵柄から選んだもの（ひげと太い体の男たち）も、見本は服を着た上半身と周りの背景で作る。性的な場面は描かない。
- 白と黒の置き方が変わる 9 つは 3段目に置いた（117 → 126 絵柄。117 は、2段目に移した 2 つを除いた数）。6 項目の値を 16 個足した（線 3・ベタとトーン 5・目と顔 3・
  頭身 1・背景 1・雰囲気 3）。新しい 2段目の下と、合う今の 2段目（11 か所。3段目は 25 枝を超えない）に足した。
  - 斜線を重ねた灰色の画面、水でにじむ墨の線、白黒の模様で埋める町、点描で描き込む妖怪画、線とベタの静かな叙情、
    夜の叙情の黒と白、細いペンの町ととぼけた人物、昭和の絵物語のペン画、とがった走り書きの昭和ギャグ。
  - 足した値のうち 6 つ（にじむ墨の線・とがった走り書き・細いペンの描き込み・斜線の灰色・白黒の模様・針金の手足）は、
    同じ項目の今の最長の値より長い。組み立てた API の `prompt` と見本の言葉は、どの枝も今ある枝の最長を超えない。
  - 初めは今ある 2段目 18 か所に置いたが、見本を作って候補から選んでも元の場面のままだった 9 か所は外した
    （元の場面がもともと細い線の描き込みや今風の整った顔で、斜線の灰色・にじむ墨・平行線とベタ・白黒の模様・
    絵物語のペン画が出なかった）。斜線の灰色とにじむ墨は、元の場面が白い線画の新しい 2段目にも 1 つずつ置いた。
- 3段目は 2,270 → 2,477 枝（新しい 2段目の下に 195、今ある 2段目に 12）。合わせて 2,382 → 2,598 枝。
  今ある 2,382 枝の見本の言葉と API の `prompt` は 1 字も変えていない（絵も作り直していない）。

## 日本の漫画から足した絵柄（3 回目、2026-09-29 本人「wikipediaではなく、日本の漫画から…違いのある漫画の素材を調査しなさい」「実装しなさい」）

- 前の 2 回と重ならない 148 人の本文の絵を見た（少年・少女・女性・青年・劇画・BL・成年・ガロ系・インディー・ギャグ・4コマ・
  児童・エッセイ・ホラー）。今の枝の見本と横に並べて、今の言葉では出ない 10 の絵柄を選んだ。調べた記録と出典は作業場所
  （`research/jp_manga/report3.md`）に置く。成果物に実在の作家・作品の名前を残さない決まりのため、ここには書かない。
- 顔と体の作りから変わる 6 つは 2段目に置いた（2段目 111 → 117）。言葉は形を具体的に書き、長さは今ある 2段目の最長以下。
  - 少年漫画 > 線で彫る劇画調、少女漫画 > ペン線だけの端正な少女漫画、青年漫画 > 美化しない普通の人の写実・
    拙い人物と描き込んだ背景、ギャグ漫画 > 表情のない人形のような大人、4コマ漫画 > 丸い餅の形の人物。
  - 1段目の下の 2段目が 12 を超えたので（青年 14、少女・ギャグ 13）、検査の上限を 12 から 14 にした。
- 描き込みと白黒の置き方が変わる 4 つは 3段目に置いた（126 → 130 絵柄）。6 項目の値を 6 個足した（ベタとトーン 2・目と顔 2・
  頭身 1・背景 1。どれも同じ項目の今の最長以下）。
  - 服の柄をペンで埋める（ペン線だけの少女漫画の下と、元の場面の服が無地の昭和の星の瞳）、
    昔のモダンな町（表情のない人形のような大人の下）、
    異様にふくらんだ筋肉（元の場面の人物が細身の、少年漫画 > スポーツと青年漫画 > アクション）、
    ひびと破片を細い線で描く（美化しない普通の人の写実の下と、ホラー漫画 > パニック・ゾンビ）。
  - 筋肉は、初めは線で彫る劇画調の下に置いたが、元の場面の男がもともと筋骨たくましく、候補 4 枚でも違いが
    出なかったので置き直した。70年代の乙女ちっくの下の柄も、元の場面の服がもともと格子の柄で外した。
  - ひびと破片は、初めの言葉（背景は質感を描き込まない）では違いが出なかったので、公開前に言葉を
    「トーンもベタも使わない白い紙の線画」に替えて絵も作り直した。青年漫画 > SF・犯罪・裏社会と劇画 > 戦記の下にも
    試したが、候補を作っても元の場面のままだったので置いていない。
- 3段目は 2,477 → 2,604 枝（新しい 2段目の下に 123、今ある 2段目に 4）。合わせて 2,598 → 2,731 枝。
  今ある 2,598 枝の見本の言葉と API の `prompt` は 1 字も変えていない（絵も作り直していない）。

## 点の輪郭と鉛筆の粒（2026-09-30）

- サイトとリポジトリの定義を読み、日本の漫画の本文で確認した要素から3絵柄を追加した（130 → 133絵柄）。
  ギャグ漫画 > シュール > 輪郭も点で描く、劇画 > 時代劇 > 粒と擦れの濃い鉛筆画、
  青年漫画 > 日常 > 薄い粒の柔らかな陰影。実在の名前を含む出典はリポジトリ外の調査記録に置く。
- 本人の「AI独特の線」「書きすぎ」の指摘に合わせ、顔・服・背景の細線と影を減らし、白い余白を増やした見本を作った。
  追加3枝だけに `medium` を指定する。点の輪郭と粒のある鉛筆の面は、既存の「灰色はすべて網点」の共通文と
  両立しないため、この3枝のAPI用共通文と見本の描き直し文だけを別にする。
- 元の場面（1枚目）は既存の2段目の文で作る。新しい3枝の描き直し（2枚目）は完成した絵柄の文だけを使い、
  親の細部指定を引き継がず省略を優先する。既存2,731枝のAPI用・見本用の文と画像記録は変えていない。
- 追加画像は非公開リポジトリのReleaseに、分割したbase64のアーカイブとして置く（クラウドからのバイナリ転送が
  `Bad Content-Length` で失敗するため、Release本文から復元する）。`sample_bundles.json` にアーカイブのSHA-256を固定し、
  `prepare_samples.py` が画像・生成文・作成日時・モデル情報を承認記録と照合して `app/seed/additions/` に配置する。
  画像はgitに入れない。CIと通常・手動デプロイの両方で同じ検査を行い、不一致なら配置前に止まる。
- コンテナ起動時に既存volumeへ一度だけ追加する。既に画像がある枝は差し替えない。再起動でも版は変わらない。
  生成ツールがモデルの版を返さなかったため、新しい見本には `image_gen (version not reported)` と記録した。

## 網点の面・帯の体・虹彩の輪（2026-09-30）

- 日本の漫画の本文を調べ、既存133絵柄・104要素との違いを確認した3系統を追加した（136絵柄・108要素、全2,737枝）。
  女性漫画 > ヒューマンドラマ > 網点の面で描く、ギャグ漫画 > 昭和ギャグ > 平たい帯の体、
  青年漫画 > 職業もの > 輪で描く大きな虹彩。実在の名前を含む出典はリポジトリ外に置く。
- 網点の面では外周線を省き、白と2種類の網点の境で形を作る。帯の体では腕を幅のある平たい帯にし、
  虹彩は目の外形とは別の大きな輪で描く。髪・服・背景の細線を抑えた見本と、その生成文を対で登録する。
  既存2,734枝のAPI用・見本用の文と画像記録は変えていない。
- 追加画像は従来の検証付きRelease配布を使う。各アーカイブの見本記録を結合してから配置するため、
  共通名の `manifest.json` を画像の重複として扱わないようにした。複数アーカイブの結合を検査する。

## 検査

- `.github/workflows/manga-style-validate.yml`: catalog.json が木の定義と一致、`tests/checks.py`、
  `tests/power.py`（わざと壊して検査が落ちることを確かめる）、`tests/caddy_routing.py`（本番と同じ
  caddy:latest で Caddyfile のブロックを動かす）、compose と Caddy の配線、実イメージの起動。

## 注意（Caddy の forward_auth と Cookie）

manga のブロックでは `copy_headers Cookie` を**書かない**。Caddy 2.11 以降、`copy_headers` は認証の応答に
その見出しが無いと、元のリクエストから**消して**次へ渡す。costlab-auth の 204 には Cookie が無いので、
app に Cookie が届かず、app 側のログイン再確認が必ず失敗する（2026-09-26、ログイン直後に
`{"error":"forbidden"}` になった）。書かなくても Cookie は costlab-auth にも app にも元のまま届く。
keiba・stock・preview のブロックにも同じ行があるが、あちらの app は Cookie を読まないので影響は出ていない。


## 既存の絵柄との差を確認した彩色追加（2026-10-11）

- 現行の見本と同じ人物土台・場面から生成し、白黒にない彩色差を実画像で確認した5枝をレベル3に追加。合計は全2,742枝。
  - 女性漫画 > ラブロマンス、大人の恋愛、少年漫画 > ラブコメ、青年漫画 > アクションに「土台の線を保つカラー階調」。
  - 女性漫画 > 百合に「白黒と黄緑の差し色」。黄緑の同系色の濃淡を許す。
- 原作漫画との完全一致ではなく、既存カタログにない可視の描法差を採否に使う。人物土台の差が確定した場合だけレベル2にする。今回は人物土台4候補の非重複が未確定なので追加しない。
- 新しい語で5枚すべてを再生成し、日英の見本/スタイルプロンプトと画像SHAを採用記録に対応付ける。既存2,737組の語・画像記録・monoの版fingerprintは変更しない。
- 新枝のAPIは `expression: color`（単一差し色も含む）。禁止項目から「色」だけを除外し、文字/フキダシ/コマ枠/署名/透かしの禁止、画像のサイズ制限、管理者認証は維持。RGB保持は新枝だけに明示適用する。
- 画像は固定SHAの配布bundleを通常のCI/Actionsで配置。既存の採用ガードとpair検査は維持する。


## 絵本本文の調査から素材描法を追加（2026-10-15）

- 顔・頭胴・四肢の土台が違う場合はレベル2、同じ土台の素材・線・彩色だけが違う場合はレベル3。既存APIの無変更対照12枚を生成し、首なし丸体や白丸目だけの追加は見送った。
- 多色色紙の重なり、色クレヨンの擦れ、色線と透明な淡彩、布と刺繍の浅いレリーフ、色粘土の浅いレリーフを、それぞれ既存の図形・ヘタウマ・ペンの風景・動物・丸い餅の形の人物の下へ1枝ずつ追加。全2,747枝。
- 新語の掲載候補5枚と参照なし別場面5枚を作成し、可視の描法差を確認。別場面の粘土は丸顔を保つが、短胴は部分再現。素材の再現と人体土台の再現を分離して記録する。原作の完全一致は条件にしない。
- 既存2,742組のAPI/見本語・採用記録を保全。新5枝だけRGB/colorを明示し、既存の白黒枝、認証・同一origin・採用/ペア検査は維持。画像は固定SHAの配布bundleをCIと通常Actions経由で配置する。


## X中心の高表示漫画100件から平面彩色を追加（2026-10-15）

- 公開データから漫画本文100例を実見し、人物構築と線・階調・彩色を分離して関連19土台へ対応候補を記録。表示回数はfxtwitterの第三者取得値で、取得日時と公式syndicationの著者・画像対応を保存。X全体の順位や絵柄単独の人気原因とはしない。
- 現行API語を変えない関連人物型の対照10枚を生成。首なし丸塊は衣服なしで既存mochi語に再現したため、新L2は採用しない。鼻口の個別変形や青い淡彩には部分対応を残す。
- 人物の土台を共有する「輪郭を保つ平面カラー」を、丸い餅の形の人物、育児エッセイ、図形人物、昭和ギャグの下へL3として各1枝だけ追加。全2,751枝。均一な多色面と少量の単純色影を使い、既存のカラー階調や紙/布/粘土/クレヨンとは可視の描法を分ける。
- 藍一色の候補は掲載用に差が出たが、別場面の網点限定を確認できず不採用・非公開で保留。初回独立レビューの全体不合格は保持し、採用可の4枝だけを同じ画像SHA・同じ実語/jobで再結合する。別場面のretro誇張顔と図形構築は部分再現で、平面彩色の再現とは分離。
- 旧2,747組のAPI/見本語・採用記録を完全保全。新4枝だけcolor/RGB、既存mono fingerprintと認証・採用ガード・通常配布/Actions経路は変更しない。生成モデルの要求ラベルは実エンジンの証明ではない。


## FANZA公開本文の絵柄調査と成人土台への平面カラー展開（2026-10-15）

- 公式コミック月間人気順20枠を保持。安全に扱える5作品の本文/本文抜粋を確認し、残り15は未成年示唆/成人根拠不足で本文未確認として別記。別枠100作品は100サークルで、上位20と作品/サークルID重複なし。表紙だけの合本や未観察予備は数えない。
- 現行117L2を含む161API語、64掲載見本、無変更APIの関連人物型8対照を比較。新L2確定0。既存の平面カラーを細い輪郭・自然な成人の3土台へ展開するL3であり、新技法3種類ではない。
- 新枝は `josei-office-flat-color` / `josei-comedy-flat-color` / `seinen-profession-flat-color`。全2,754枝、新3だけcolor/RGB。既存2,751のAPI/見本語・採用記録・mono fingerprintを保全する。
- 背景語は新3だけ短い語へ置換し掲載/別場面を全6再生成。旧語/旧6は研究側attempt-1で保全。既存4の平面カラーに変更を漏らさないよう、生成bundleの共有style keyを分離する。branch IDと表示タイトルは維持。
- 公開サンプル番号と本の頁番号を区別し、広告の見出し/色フィルター/検閲処理を本文技法と数えない。原作画像は生成入力や公開見本へ使わず、新見本は成人の着衣・非性的場面のみ。
- 独立視覚は3候補採用可。コメディの別場面人物構築は部分転用で、描法転用とは別判定。原作完全一致・全身/隠れた指・未試行場面の成功率は保証しない。通常の採用ガード/CI/Actions配置を維持する。

## FANZA商業本文の調査と輪郭を抑えた立体カラー（2026-10-15）

- 月間上位20枠を保持し、本文は上位3＋別100＝103作品を実見。上位17は安全選別等により本文未確認のまま別記し、別作品で置き換えない。別100は公式作者ID100/系列ID100一意、上位20との作者/系列/作品重複なし。表紙・目次・広告・扉を本文と区別する。
- 比較は公開2,754枝の実語を基準に、全117L2を含む172API、75掲載見本（旧64は同一JPEGの実見を再利用、新11は追加実見）、無変更APIの新規対照2＋同語既往1を使用。作品別の完全再現検証とはしない。
- 自然な成人の人物構築は既存土台へ対応させ、新L2は追加しない。輪郭線への依存を抑え、肌・髪・布などの材質と連続した色の陰影で立体を描くL3を、`seinen-profession-volumetric-color` と `seinen-plainreal-volumetric-color` に配置する。1描法の2配置であり、2種類の新技法ではない。
- 初回4配置のうちoffice/comedyは既存色階調との可視差が不明のため保留。保持2の実語/画像をそのまま保存し、別場面を同じAPI語・参照0で生成。独立視覚レビューは保持2を採用可とした。原作の完全模写、全身頭身、任意場面での成功率や実制作工程は保証しない。
- 新2のみcolor/RGB。既存2,754のAPI/見本語・採用record・旧mono fingerprintと認証/採用/通常Actions経路を保全。原作画像を生成入力・公開素材にせず、新見本は成人の着衣・非性的日常場面のみ。要求modelラベルから実エンジンを断定しない。
## 同じプロンプトで別のモデルが描いた比較の絵（2026-10-18）

- 本人の依頼: 今の見本は GPT Image の作例として残し、WAI-Illustrious-SDXL でも描いて並べる（「同じプロンプトでどう変わるのかの対比」）。
  「プロンプトは直しません」（2026-10-18）。見本を作った英語のプロンプト（`samples[reference].prompt.en`）を 1 字も変えずに渡す。
- 条件は全枝共通: `wai-illustrious-sdxl-v17.0`、seed 20261018、20 steps、CFG 5、euler_a、768x1024、ネガティブプロンプトなし。
  生成は PS5（`D:/PS5-AI/catalog-wai/`。`tools/run_wai.py`、記録は `manifest.jsonl`）。2段目・3段目の見本は 2 枚の工程
  （場面を描き、その絵を渡して描き直す）で作ったが、比較の絵は 2 枚分の言葉をつないだ英文から 1 枚で描く（画面にも書く）。
- **絵柄の一部ではない**。`/v1/styles` の `samples`・`reference`・`model`・`version`・`updated_at` は変えず、`comparisons[]` を足しただけ。
  Genko は今までどおり `samples[reference]` を参考画像に使う。
- 記録: `costlab-auth/manga/compare/records.json`（git）。画像ごとに JPEG の SHA-256・バイト数、元にした英文の SHA-256、
  並べる見本画像の SHA-256、PNG の SHA-256、PS5 のジョブ id、作成日時。画像は Release の zip（git に入れない）。
- 配置: `tools/manga_catalog/prepare_compare.py`（`prepare_samples.py` の最後に呼ぶので CI・通常デプロイ・手動で同じ）。
  zip と各画像のハッシュ、英文が今の見本の英文と同じこと、見本の画像が並べた時のものと同じことを確かめ、
  `compare/files/<id>.jpg` に置く。画像やzipが記録と違えば置く前に止まる。英文か見本が変わった枝は止めずに置かない
  （比較は絵柄の一部ではないので、カタログの変更を止めない。作り直すか記録から外す）。Dockerfile は `compare/` を `app/` より先に COPY する
  （約 2,700 枚の層を app の変更のたびに作り直さない）。
- 表示: 見本が差し替わった枝・言葉が変わった枝では、古い比較の絵を出さない（画面・API・画像の URL すべて）。
  作り直すまでその枝は比較なし。隠した枝は今までどおり何も出さない。
- 追加の手順: `python D:/PS5-AI/catalog-wai/tools/make_compare_bundle.py --repo C:/GitHub/akiba-infra --tag <tag>` で
  まだ載せていない成功分を zip にして records.json に足す → `gh release create <tag> --prerelease` で zip を上げる →
  PR。zip は 1 つ数百 MB まで（`prepare_compare.py` の上限 512 MB）。
- 試験: `costlab-auth/manga/tests/test_compare.py`（CI の checks に入れた）。


### 説明用2枚組：青年・ノワール3段目の4組8枚
- 承認済みの枝別「代表＋別の場面」。21枝42枚を各1独立process・新turnで生成し、両役採用の4枝8枚だけを固定SHAのRelease assetへ結合。対象は `seinen-noir-bold-black` / `seinen-noir-fine-tall` / `seinen-noir-graphic-flat` / `seinen-noir-sharp-stylish`。17枝は旧公開を保持する。
- 旧39bundle466pairの全recordを保持して40bundle470pair候補へ。画像と実生成文とcomplete styleを同時更新し、元比率・白余白thumb・mono Lを維持。追加生成0。源6項目とsceneを分離し、親の半顔ベタや旧sceneを自動継承しない。graphic別役は約7〜7.5頭身の標準体近似で厳密6〜7保証ではない。元fit/nativefalse/文字uncertainは別保存し、全語完全再現や実engineは保証しない（requested `gpt-image-2.6-sunburst` / reported null / enforced false）。
- アプリ/Caddy/認証/権限/workflow/保護設定/廃止CIは不変。固定archive/SHAと通常prepare・既存Actionsを用い、独立reviewと本番API・画像・日英390/1280表示・操作・healthy確認を公開受入のgateとして維持する。


### 説明用2枚組：青年・SF3段目の8組16枚
- 承認済みの枝別「代表＋別の場面」。24枝48monoを各1独立process・新turnで生成し、両役採用の8枝16枚だけを固定SHAのRelease assetへ結合。対象は `seinen-scifi-bold-black` / `seinen-scifi-brush-wild` / `seinen-scifi-deadpan-seinen` / `seinen-scifi-fine-tall` / `seinen-scifi-muscle-hatch` / `seinen-scifi-retro-seinen` / `seinen-scifi-sharp-stylish` / `seinen-scifi-tone-layered-hot`。16枝は旧公開を保持する。
- 旧40bundle470pair全recordを保持して41bundle478pair候補へ。画像と実生成文とcomplete styleを同時更新し、元比率・白余白thumb・mono Lを維持。追加生成0。源6項目とsceneを分離し、親の人物構築・描法・旧sceneを自動継承しない。tone-layered-hot別役は約7強〜7.5でも標準胴脚構築の近似を原寸肯定し、厳密6〜7保証ではない。元fit/nativefalse/notesは別保存し、全語完全再現や実engineは保証しない（requested `gpt-image-2.6-sunburst` / reported null / enforced false）。
- アプリ/Caddy/認証/権限/workflow/保護設定/廃止CIは不変。固定archive/SHAと通常prepare・既存Actionsを使い、独立reviewと本番API・画像・日英390/1280表示・操作・healthy確認を公開受入gateとして維持する。


### 説明用2枚組：青年・ダークファンタジー3段目の4組8枚
- 承認済みの枝別「代表＋別の場面」。24枝48monoを各1独立process・新turnで生成し、両役採用の4枝8枚だけを固定SHAのRelease assetへ結合。対象は `seinen-darkfantasy-bold-black` / `seinen-darkfantasy-brush-wild` / `seinen-darkfantasy-gothic` / `seinen-darkfantasy-sharp-stylish`。20枝は旧公開を保持する。
- 旧41bundle478pair全recordを保持して42bundle482pair候補へ。画像と実生成文とcomplete styleを同時更新し、元比率・白余白thumb・mono Lを維持。追加生成0。源6項目とsceneを分離し、親の人物構築・描法・旧sceneを自動継承しない。brush-wild別役の主線は原寸cropで太細差と乾いた欠けを個別肯定、元部分fit/未確認/notesは別保存。全語完全再現や実画材/実engineは保証しない（requested `gpt-image-2.6-sunburst` / reported null / enforced false）。
- アプリ/Caddy/認証/権限/workflow/保護設定/廃止CIは不変。固定archive/SHAと通常prepare・既存Actionsを使い、独立差分reviewと本番API・画像・日英390/1280表示・操作・healthy確認を公開受入gateとして維持する。


### 説明用2枚組：青年・戦争3段目の3組6枚
- 承認済みの枝別「代表＋別の場面」。23枝46monoを各1独立process・新turnで生成し、両役採用の3枝6枚だけを固定SHAのRelease assetへ結合。対象は `seinen-war-bold-black` / `seinen-war-graphic-flat` / `seinen-war-sharp-stylish`。20枝は旧公開を保持する。
- 旧42bundle482pair全recordを保持して43bundle485pair候補へ。画像・実生成文・complete styleを同時更新し、元比率・白余白thumb・mono Lを維持。追加生成0。源6項目とsceneを分離し、親の戦闘・負傷・武器・人物構築・旧sceneを自動継承しない。graphic別役は全身近似7前後の標準構築を原寸肯定。shadow別役は構築肯定と別に背景扉の濃淡変化でhold、brush別役は太細肯定と別に乾いた主線未確認でhold。元fit/notes/nativefalseと主担当採否は別保存し、全語完全再現や実画材/実engineは保証しない（requested `gpt-image-2.6-sunburst` / reported null / enforced false）。
- アプリ/Caddy/認証/権限/workflow/保護設定/廃止CIは不変。固定archive/SHAと通常prepare・既存Actionsを使い、独立差分reviewと本番API・画像・日英390/1280表示・操作・healthy確認を公開受入gateとして維持する。

## 2026-11-09：青年・ギャンブルの説明用5組10枚
- 承認済みの枝別「代表＋別の場面」。23枝46monoを1画像1独立process・新turnで生成し、実見後に両役採用の5枝10枚だけを追加。対象は `seinen-gambling-fine-tall` / `seinen-gambling-bold-black` / `seinen-gambling-sharp-stylish` / `seinen-gambling-caricature` / `seinen-gambling-muscle-hatch`。18枝は旧公開を保持。
- 旧43bundle485pairを保持して44bundle490pair候補へ。全初見46と標準体の限定確認8を保存。頭身・目・描線・背景面の未達や未確認をhold理由として維持し、美しさで免除しない。採用分もトーン量、上着の垂れ・遮蔽、画角、小物追加などの差を元所見と別の採否に保存する。画像・実生成文・complete styleを同時更新し、元比率・白余白thumb・mono Lを維持。追加生成0。
- **本人の指示によりGitHub Actionsを起動せず直接配置する。** PR/独立差分review/通常prepare/本番API・画像・日英390/1280表示・操作・actual healthy確認は維持。同SHAアプリの既存imageを固定照合し、新pairseed-onlyのnetwork-free layerを作ってmanga-styleのみ更新する。既存データ・安全/資源設定と他サービス、rollback用imageを保持。アプリ/Caddy/認証/権限/workflow/保護設定/廃止CIは変更しない。requested `gpt-image-2.6-sunburst` / reported null / enforced falseを保持し、全語完全再現・実画材・実engineは保証しない。

## 2026-11-09：青年・グルメの説明用4組8枚
- 承認済みの代表＋別場面。20葉40monoを各1独立生成sessionで作り、初見40と限定7predicateを保存。両役採用のfine-tall / retro-seinen / bold-black / sharp-stylishの4枝8枚だけを追加し、16枝は旧公開を保持する。採否は主担当が元fit/notesと別fieldに保存。
- 旧44bundle490pairを保持して45bundle494pair候補へ。fine-tall代表の主輪郭は細く概ね均一と限定確認し、髪線密度・トーン量の差は残差として保存。標準体や小目の未達、網点サイズ変化・乾いた主線・背景面の未確認などを他の特徴や美しさで免除しない。追加生成0、画像・実生成文・complete styleを同時更新。元比率・白余白thumb・mono Lを維持し、全語再現や物理画材・実年齢・実engineは保証しない。
- 本人指示によりGitHub Actionsを起動せず、PR/独立差分review/通常prepare/本番API・画像・日英390/1280表示・操作・actual healthyを維持してmanga-styleだけ直接配置する。同SHAアプリを固定しnew pairseed-only/network-free layerを追加。既存データ・安全/資源/volume/network設定、他サービス、rollback imageを保持。アプリ/Caddy/認証/権限/workflow/保護設定/廃止CIは変更しない。


### 説明用2枚組：青年・職業の3段目（2026-11-09）

- 23枝46枚を各1画像1独立process/turn、参照・過去履歴なしで生成（白黒42枚、既存彩色枝の4枚はカラー）。全46初見と限定7wholeを記録し、両役を採用した `seinen-profession-fine-tall`・`seinen-profession-bold-black`・`seinen-profession-sharp-stylish` の3枝6枚だけを配布する。残20枝・既存彩色2枝の公開prompt/sample/versionは置換しない。
- 元のpartial/full・定義描法flag・文字uncertainと限定false、単役positiveを保存。細線量・トーン面積・背景量・姿勢/靴など許容残差を採用理由と分離し、全語完全再現とはしない。標準体の未成立や主描法の不足・未確認はhold。カラーを白黒化せず、連続彩色の枝を写真調というラベルやmonoの階調禁止で拒否しない。
- 旧45bundle494pairを先頭完全保持し、新1bundle3pairで46bundle497pair（公開受入後994枚）となる。配布は `manga-explanatory-20261109-l3-seinen-profession.zip`。元比率・長辺1024以下、今回6枚はL、thumbだけ白余白384×512。生成原画・旧公開・原採否は保全する。
- `gpt-image-2.6-sunburst` は要求モデルの受理と生成成功の記録。`reported_model=null` / `model_enforced=false` であり実engineは保証しない。
- ローカル回帰・実Store統合・公開前独立review・PR/mergeと本番受入を維持し、本人指定によりGitHub Actionsを起動せず `manga-style` の新seed-only layerだけを直接配置する。認証・Caddy・権限・保護設定・他サービスは不変。


## 説明用2枚組：青年・サスペンスの3段目（2026-11-09）

- 23分類46枚を1画像1独立sessionで生成・全初見。原文の描法/人物構築/背景を分けて確認し、fine-tall・bold-black・muscle-hatchの3分類6枚のみ採用。20分類は旧公開を維持する。
- 46初見の40partial/6full、文字none46と元notesを保持。追加10wholeは限定predicateで1true/9false、採用を完全な語句再現とは呼ばない。網点の範囲・線の若干の強弱・紙/封筒位置・靴などは各役の残差を記録する。
- 初見Bは600秒上限を超えた633.48046秒のため、適合reviewとして扱わず元資源違反を保存。親が原観察とactualcall/画像/style/promptを照合し、必須の公開前統合reviewで採否と記録再利用を確認する。元違反を後続成功で消さない。
- 旧47bundle501pairを保持し48bundle504pair候補へ。原画/ZIPはgitへ入れず、固定SHAのRelease assetと通常seed/startup経路を使う。アプリ・認証・workflow・保護設定は変更しない。
- 本人指示によりGitHub Actionsを起動せず、新seedだけを既存アプリ同SHAのnetwork-free layerへ追加しmanga-styleだけ配置。回帰/統合/UI/独立reviewと本番API・画像・画面・操作・actual healthyを別gateとし、受入後だけ台帳publishedへ遷移する。

## 説明用2枚組：青年・手描きで歪む街の3段目（2026-11-09）

- 21分類42monoを各1画像1独立sessionで生成し全初見。deadpan-seinen / graphic-flat / woodcut / bold-black / sharp-stylishの両役5組10枚だけを配布候補とし、残16分類は旧公開を保持する。単役positive16件のうち、pairに揃わない6件も記録として保全する。
- 元8full34partial、textnone42、全notesとactualcallを保存。限定12wholeでは標準構築8件が未確認。髪・顎・靴底の境界差だけでなく小頭と長い胴脚の構築に基づく所見として保持し、機械的な一頭差の判定にしない。
- graphic-flat両役は人物主輪郭・小さい目を限定確認し、別役は近似的な標準構築を確認。曲線禁止・瞳禁止は追加しない。brush-wildの主輪郭カスレ未確認は美しさで免除しない。muscle-hatch代表の限定質問には一助詞の送信差があり、元rawと差を保全しpositive採用証拠から除外する。独立hold後の不要な別役検査は行わない。
- 旧48bundle504pairを先頭保持し49bundle509pair候補へ。新ZIP `manga-explanatory-20261109-l3-seinen-warped.zip` を固定SHAで検証。原画・ZIPはgitへ入れず、画像・実生成文・complete styleを一組で扱う。元比率とLを保ち長辺1024以下、thumbのみ白余白384×512。requestedモデルの受理・生成成功と実engineの保証は区別し、reported null / enforced falseを保持する。
- ローカル回帰・実Store統合・日英390/1280表示・独立公開review・PR/merge・本番受入は別gate。GitHub Actionsを起動せず、同SHAアプリへ新seedだけをnetwork-free layerで加えmanga-styleだけ直接配置する。既存原稿/採否/公開、認証・Caddy・権限・workflow・安全/資源/volume/network・他サービスを維持し、receipt全SHA/fullreadback後だけpublishedへ遷移する。

## 説明用2枚組：青年・簡単な顔とペンの風景の3段目（2026-11-09）

- 26分類52枚を1画像1独立sessionで生成（白黒50・既存カラー枝2）。pen-street / yokai-stipple / bold-black / sharp-stylishの両役4組8枚を配布候補とし、残22分類は旧公開を維持する。全52役の理由とpositive18役（pairに揃わない10役を含む）を保存。
- 初見9full43partial・文字none51/uncertain1、限定16wholeの1true15falseと元notesを保全。限定の肯定は質問predicateのみ。標準構築はdeadpan別役だけ肯定したが、代表の小さい瞳を小さい目全体と混同せずpair hold。人物の小頭/長胴脚構築、主輪郭のカスレ、影限定の線陰影の未確認を美しさや他描法で免除しない。独立hold後の不要companion検査は行わない。
- カラー枝の色線・淡彩の肯定と約5頭身構築の未確認を分離し、連続した淡彩や紙肌・水彩という見た目だけでは拒否しない。今回は未採用なのでカラーの公開prompt/sample/versionを変えない。pattern-town別役の文字様印uncertainも元のまま残す。
- 旧49bundle509pairを先頭保持し50bundle513pair候補へ。新ZIP `manga-explanatory-20261109-l3-seinen-penscape.zip` を固定SHAで検証し、原画・ZIPはgitへ入れない。新8画像はL・元比率・長辺1024以下、thumbは白余白384×512。画像/実生成文/complete styleを一組で更新し、requestedモデルの受理/生成成功と実engine保証を区別する。
- 回帰・実Store統合・日英390/1280表示・独立公開review・PR/merge・本番受入を別gateとする。回帰前からsecrets checkerのworkflow全35入力もpre/post manifestへ束縛。GitHub Actionsは起動せず、アプリ同SHAへ新seed-onlyのnetwork-free layerを加えmanga-styleだけ直接配置。認証・Caddy・権限・workflow・保護設定・安全/資源/volume/network・他サービスを保持し、receipt fullreadback全SHA後だけpublishedへ進める。
## 説明用2枚組：青年・美化しない普通の人の写実の3段目（2026-11-09）

- 22分類44枚を1画像1独立sessionで生成（白黒42・既存立体カラー2）。bold-black / crack-debris / muscle-hatchの両役3組6枚だけを配布候補とし、残19分類は旧公開を保持。全44役の理由とpositive17役（pairに揃わない11役を含む）を保全する。
- 元8full36partial/textnone44、限定18wholeの1true17false、全raw/actual質問/画像/complete-style SHAを保存。標準体構築15別役は髪/顎/靴底の境界差と小頭/長い胴脚の別構築を区別し未確認を保持。名目一頭差や厳密式だけの否定はしない。deadpan代表の小瞳を目全体の小ささへ代用せず、brush-wildの主輪郭カスレ不足を内部線や背景質感で代用しない。
- crack-debris代表は限定確認で小目/低鼻/短顎/平たい顔を肯定し、美醜の印象を採否基準にしない。graphic-flatへ曲線禁止/瞳禁止を追加せず、別役構築holdは保持。独立hold後の不要companion/網点/明部粒子検査は取消し、元の未確認を肯定で消さない。物理画材/トーン枚数/カッターの使用は断定しない。
- 立体カラーは実親参照の人物構築を具体化し、抑えた墨輪郭/連続多色陰影/光沢接触影を保持。親mono網点や旧L2接頭辞の眼鏡/ひげは混ぜない。髪房と簡潔背景色面の未確認を保持し、写真風ラベルや連続陰影だけで拒否しない。未採用なのでカラーの公開prompt/sample/versionは変えない。
- 旧50bundle513pairを先頭保持し51bundle516pair候補へ。新ZIP `manga-explanatory-20261109-l3-seinen-plainreal.zip` を固定SHAで検証、原画/ZIPはgitへ入れない。新6枚はL・元比率・長辺1024以下、thumb白余白384×512。画像/実生成文/complete styleを一組で更新、requestedモデルと実engine保証は区別する。
- 回帰前からworkflow全35入力を含む実readerをpre/post SHAへ束縛。回帰/実Store統合/日英390・1280表示/独立公開review/PR merge/本番受入を別gateとする。GitHub Actionsを起動せず、既存同SHAアプリへnewseed-onlyのnetwork-free layerを追加しmanga-styleだけ直接配置。認証/Caddy/権限/workflow/保護/安全資源/volume/network/他サービスを維持し、receipt fullreadback全SHA後だけ台帳publishedへ遷移する。

## 説明用2枚組：青年「拙い人物と描き込んだ背景」の3段目（2026-11-09）

- 承認済みの全枝更新に沿い、各枝の実際の描法を示す代表と別場面を、画像ごとに新しい独立セッションで40枚生成した。親名の四角頭や4〜5頭身を全3段目へ追加せず、各枝の完結した絵柄の原文を優先した。
- 初見40枚と限定確認20件を結合し、`seinen-clumsy-graphic-flat` と `seinen-clumsy-bold-black` の2分類4枚を公開候補にした。他18分類は旧公開画像と原文を保持する。原観察のpartial/未確認・文字様印のuncertain、単独で肯定された10役も保存する。
- 近似人物構築の確認を描法の肯定と混同せず、曲線の存在を曲線禁止へ拡張しない。全身の構築、目全体、人物主輪郭、ズボンの線と点状面は別の限定判定として保持した。
- 既存51bundle516組を保持して新しい固定SHAの1bundle2組だけを追加する候補。可変比率のグレースケールJPEG、白余白384×512サムネイル、各画像の日英実生成文を一組にする。公開確定は回帰・統合・画面・独立レビュー・PRと、本番受入の後。GitHub Actionsは起動せず、承認済みのseed-only直接配置を維持する。

### 大人の恋愛の説明用2枚組（2026-11-09）

25分類50枚を独立生成し、各原画を実見した。night-lyric、elegant、tall-cool、hair-detail、gothic、retro-shojo、layered-gorgeousの7分類14枚を差分付き採用とし、18分類は旧公開を保持する。主描法・人物構築・陰影の量と方法を別に確認し、元のpartialやuncertainを上書きしない。開始時の52bundle518組を保全し、53bundle525組の固定SHA候補を追加する。新ZIPのSHA-256は `fb72ce8cf412e2f147ee47ba349414f0fe38cd7ae3c149f5198d61ce5dfc8cdf`。回帰・統合・独立レビューと、GitHub Actionsを起動しないseed-only直接配置後の実画面・本番受入を別gateとする。


### お仕事・オフィスの説明用2枚組候補（2026-11-09）

22分類44枚（白黒42・カラー2）を画像ごとの独立セッションで生成し、全44原画の初見と13件の限定確認を結合した。chibi-comic、bold-comic、hair-detailの3分類6枚だけを差分付き採用とし、残19分類は旧公開を維持する。元9full/35partial・文字none44と全flags、単役positive11件のうちpairに揃わない5件も保存する。

bold-comic別場面は、髪込み約3.6から頭頂の幅を考慮した約4.0〜4.4頭身と大頭・低頭身の構築を確認。標準体6件とカラー約8頭身1件は、名目一頭差だけでなく小頭と長胴脚の別構築が未確認の理由。elegant代表の平網点true/少量false、tall-cool別場面の柱面内の連続濃淡、nineties別場面の横長目/尖顎を別々に保持する。hair-detail両役の網点濃淡面と明瞭白抜きは原寸で確認し、物理枚数/工具は断定しない。独立hold後の不要companionは取消す。

配置専用repairの原文を各枝ごとに保持し、親officeの顔や8頭身を全L3へ足さない。カラーflat-colorは現親参照の線/眼顔髪/体形を具体化したが今回は保留で、公開prompt/sample/versionは変更しない。曲線禁止の発明や、背景限定の質感禁止を衣服・靴へ広げることはしない。

旧53bundle525組のprefixを保持し、54bundle528組の候補として新固定SHA ZIP `manga-explanatory-20261109-l3-josei-office.zip`（SHA `56ccfa4146c949ec5a7c024e4742a9dbef786ed4b15a5750f85bcad9e8f27dcf`）を追加する。新6画像はL・元比率・長辺1024以下、thumb白余白384×512、実生成文とcomplete styleを一組にする。回帰・統合・日英画面・独立レビュー・PR/mergeと本番受入は別gate。GitHub Actionsは起動せず同SHAアプリへ新seedだけをnetwork-free layerで追加しmanga-styleだけ直接配置する。認証/Caddy/権限/安全資源/volume/network/他serviceを保持し、receipt fullreadbackと全SHA照合後だけpublishedへ進める。


### 家族・育児の説明用2枚組候補（2026-11-09）

20分類40枚を画像ごとの独立セッションで生成し、初見40枚と限定11件（人物構築8・網点量1・網点面と白抜き2）を照合した。chibi-comic、bold-comic、hair-detail、retro-shojoの4分類8枚を差分付き採用とし、16分類は旧公開を維持する。初見9full/31partial・文字none40、限定4true/7false、単役positive11件のうちpairに揃わない3件と各roleの残差を保全する。

bold-comic別場面は髪込み約3.5から頭頂推定約3.8〜4.1の境界幅と大頭・短い胴脚を確認し、4頭身寄りの低め構築として採用。hair-detail代表は髪の厚みを含む近似の8頭身以上の細胴長脚、両役は原寸で網点濃淡面と明瞭な白抜き光を確認した。物理トーン枚数・カッター・実画材は断定しない。6〜7標準体6件は小頭に対する長い胴脚という別配分を未確認理由として保留。elegant代表の平トーンtrue/少量falseを保存し、独立hold後の不要確認は取消す。背景の花柄面を人物のトーン量へ混入せず、粒だけで非平坦とせず、黒髪をハッチング枝のベタ全面禁止へ拡張しない。

各枝の実6fieldと配置専用doodleの黒点2個・鼻なし・髪3形等を保持し、親名から子どもの登場や共通の顔・頭身を全枝へ追加しない。代表の部屋と別場面の台所はsample-onlyに分離する。タオルの垂れ方、低い踵、窓の距離、retro-shojoの淡セピア地色などを全語完全一致へ改称せず、元原画を保持して承認済みL変換で配布する。

旧54bundle528組を保全し、55bundle532組の候補へ新固定SHA ZIP `manga-explanatory-20261109-l3-josei-family.zip`（SHA `0f223570a9ef2a973a1611e0e8aede5287e01845638791617763c208732e3cc2`）だけを追加。新8枚はL・元比率・長辺1024以下、thumb白余白384×512、実生成文とcomplete styleを一組にする。回帰・隔離Store・日英UI・独立レビュー・PR/merge後、GitHub Actionsを起動せずマンガserviceの新seedだけ直接配置する。旧公開・認証・Caddy・workflow・権限・CPU0.5/RAM384MiB/PID128・volume/network・他serviceを保持し、本番receipt fullreadbackと全SHA照合後だけpublishedへ進める。


### ラブロマンスの説明用2枚組候補（2026-11-10）

23分類46枚を画像ごとの独立セッションで生成し、初見46件と限定12件（人物構築6・網点量2・網点面と白抜き3・柱面1）を照合した。chibi-comic、bold-comic、tall-cool、hair-detail、gothic、retro-shojo、layered-gorgeousの7分類14monoを差分付き採用し、16分類の旧公開を維持する。元13full/33partial、文字none45/uncertain1、限定5true/7false、positive18role/単役positive4と残差を保全。未解決のバックル文字様印を無文字合格へ書き換えない。

標準6〜7頭身5件は小頭に対して長い胴脚という別構築を未確認理由とし、bold-comic別場面は髪込み約3.2/頭頂考慮約3.5〜3.8と大頭・短胴脚の配分から約4頭身寄りを肯定。名目一頭差の自動判定にはしない。elegant/pen-classic代表は平網点true/少量falseを分離し、美しさで数量未達を免除しない。hair-detail両役とlayered-gorgeous別場面の網点濃淡面・白抜き光、hair-detail別場面の柱の白面/平網点帯/硬い境界を確認した。物理トーン枚数・実カッター・画材は不明。独立hold後の相方、バックル、睫毛、背景など不要確認は取消し、未実行とmissing coverageを混同しない。

実6field・配置専用flatmodern/roughを優先。参照型カラーのline/eyesは現親の具体語へ解決し、元prop6〜7を保つがカラー組は今回hold。roughの「枝」は英語sourceのcatalog branch指定で、木の枝状の眼という義務を加えない。髪3束/しわ2本等の独立未達は残す。親顔・2人登場・恋愛動作を全L3へ追加せず、画廊の女性＋封筒と駅前の男性＋閉じた傘をsample-onlyへ分離する。左右の手、傘の高さ、低踵、場所の情報量、生成り地色、光点厳密数など残差を保全し、全語完全一致とは呼ばない。

旧55bundle532組prefixを保持し、56bundle539組候補へ新固定SHA ZIP `manga-explanatory-20261110-l3-josei-love.zip`（SHA `8e679dc93f2c7e03680a1fe707922e961188736f1397aff3e2a00f2175d228b2`）だけを追加。新14枚はL・元比率・長辺1024以下、thumb白余白384×512。converterは前Familyとの実5parameter全buffer一致（repo/日付/cohort/題名/source head）で再利用し、新payload/採否/実行は別に検証する。回帰・隔離Store・日英UI・独立review・PR/merge後、GitHub Actionsを起動せず新seedだけ直接配置。本番receipt全SHA/fullreadback後だけpublishedとし、認証/Caddy/workflow/UID/volume/network/CPU0.5/RAM384MiB/PID128/他serviceと旧原画・採否・受入証拠を保持する。


### 百合の説明用2枚組候補（2026-11-10）

25分類50枚を個別の独立セッションで生成、初見50件を照合した。chibi-comic/night-lyric/tall-cool/gothicの4分類8monoを差分付き採用候補とし、21分類の旧公開を維持する。原8full/42partial、文字none50、positive15役/単役positive7を保全。左右の手、袋を持つ高さ、入口の描写量、低い踵、不可視部などの残差を全語完全一致と呼ばない。

実6fieldとmediumを優先。ranking-spotの黒白/平網点/黄緑差し色・同系濃淡許可を保持し、参照顔/首/灰色髪だけ現親から具体化。明示の強弱ペン線・6〜7標準・白黄緑簡単背景・明るさを親の細線/7〜8頭身/花びら/静けさで上書きしない。親genre名から女性2人や恋愛動作を追加せず、図書室の女性と歩道入口の男性をsample-onlyへ分離。spot組は今回はholdで新ZIPに含めない。

人物構築8＋主限定6＝14確認、raw2true12falseを保存。身体近似と小頭長胴脚の別構築、平網点と少量配置、柱の隣接平面と同一面内gradation、太い上瞼と独立した数本の睫毛を分離した。retro代表は境界幅を含むすらり体と眼の限定肯定があるが、相方の独立太睫毛線が未確認でpairhold。主限定4とbody先行4の計8件はJSON出力例quote escapeによるliteral質問差を保全し、原文predicateは同一でもexact-Q肯定へ改称せず、採用肯定には未使用。body indexのunverified4/observations_complete=false、契約literal条件未達を肯定で書換えない。再実見・再生成で好ましいboolを取り直さず、旧失敗・原raw・actualQと不要確認取消を別保存。選択4組8枚の肯定は一致した初見と原文別裁定に結合する。

旧56bundle539組prefixを保持し、57bundle543組候補へ新ZIP `manga-explanatory-20261110-l3-josei-yuri.zip`（760734bytes、SHA `93f0a83aef4ea55c0f80510ebbfc5edd20ce21f209d54189c72fd493eb6706c5`）だけを追加する。converterは実4parameter全buffer一致（repo/cohort/題名/source head、同じ日付は数えない）、新payload/採否/実行は別に検証する。生成前容量不足を保存し、完了済み専用darkfantasy worktreeのclosure1199とclean/旧receipt/cleanup/sites非重複を照合したうえでsitesだけ可逆sparse、原画/Git objects/証拠/本番data/他taskは不変。

回帰・隔離Store・日英UI・独立review・PR/Release往復/merge後、GitHub Actionsを起動せず新seedだけ直接配置。本番receipt全SHA/fullreadback後だけpublished。認証/Caddy/workflow/UID/volume/network/CPU0.5/RAM384MiB/PID128と他サービスを保持する。


### ヒューマンドラマの説明用2枚組候補（2026-11-10）

24分類48monoを個別の独立セッションで生成し、初見48＋限定14＝62確認を束縛した。rough-light/tall-cool/hatching-handmade/gothicの4分類8枚を差分付き採用候補とし、20分類の旧公開を維持する。元3full/45partial、文字none47/uncertain1、positive12役/単役positive4を保全。限定は構築6whole/描法5（2whole3crop）/目3crop、raw2true12false、全14literal一致。原flagsと主担当採否を分離する。

構築6件は境界幅と小頭長胴脚の別構築を分離してhold。elegant/pen-classic別場面は平網点の存在と人物への少量配置を分けて後者hold、hair-detail別場面は柱同一面内の広い濃淡を平面や硬い影境界と区別しhold。retro/layered別場面は独立した太睫毛数本が未確認、nineties別場面は尖顎肯定/縦長大眼不一致。性別による免除なし。rough別場面の袖外周/裾の少量並走線、hatching代表の首服ハッチと胸影カケアミを限定肯定し初見と結合。独立hold後の不要な相方確認は取消し、文字uncertainや他未確認を肯定で上書きせずmissing coverageにも数えない。

実6fieldとrepair-inkbleed/toneshapes独自recipeを保持し、親顔/灰髪を全L3へ一律追加しない。placement hookの白地と独自recipe墨形1個の整合を分離した。失敗planner/attempt0/容量不足/reader失敗は保全。公民館女性/共同住宅男性はsample-only、墨にじみは建物や本を持たない人物。袋位置/入口の描込量/生成り地/不可視部/実工程不明など残差を全語完全一致と呼ばない。

旧57bundle543組prefixを保持し、58bundle547組候補へ新ZIP `manga-explanatory-20261110-l3-josei-drama.zip`（1376986bytes、SHA `35e14f2f2e0ce732560e9d7cf1b6a902ebd020f37c8df41444516d5539eadf4e`）だけ追加する。新8枚はL/元比率/長辺1024以下、thumb白余白384×512。回帰・隔離Store・日英UI・独立review・PR/Release往復/merge後、GitHub Actionsを起動せず新seedだけ直接配置。本番receipt全SHA/fullreadback後のみpublished。認証/Caddy/workflow/UID/volume/network/CPU0.5/RAM384MiB/PID128と他サービスを保持。

### 時代ロマンの説明用2枚組候補（2026-11-10）

25分類50monoを各画像の独立セッションで生成し、全50job/原画/実送信文/新規sessionを照合。初見50（独立44＋主担当独自媒体6）と限定9＝実59確認を結合した。tall-cool/gothicの2分類4枚を差分付き採用候補とし、23分類の旧公開を維持する。元full2/partial48、文字none50、限定2true7false（6whole3crop）、positive9役/単役positive5を保全。元flagsと主担当採否を分離し、全語完全一致とは呼ばない。

標準構築4件は髪/顎/履物境界と着物による遮蔽を考慮しても小頭に対する首下の縦の量が長い別構築としてhold。retro/layered別場面は太い上瞼と独立した太睫毛数本を分離し、後者未確認、性別による免除なし。hair-detail両役は袖/腰の段階的トーンと髪白抜き光を肯定したが、別場面の瞳内の大きな白光が未確認でhold。notesの辞書型と全値を維持し、髪/額の白を瞳光へ転用しない。不要になったrough眼/layered代表bodyの追加実見と、未採用切り絵の実画素topology確認は取消し、肯定やmissing coverageへ置換しない。

実6fieldと浮世絵/切り絵/筆墨独自recipe・placement白背景hookを保持し、親の筆/うりざね顔/和柄を全L3へ一律追加しない。昭和初期の縁側女性/木門前男性はsample-onlyへ分離。採用2分類は主線/大黒ベタ対比/切長眼/細面/8以上すらりと、gothicの花柄/不穏さを肯定。家屋の近さ/細密量、包み位置、足袋未確認などの残差を保存する。source17は既存肯定と同SHA、converterは実3parameter全buffer変換（parent ID、公開base SHA、題名）であり、同じ日付を編集として数えない。新payload/採否/実行は別検証。source後のmain追加は実行closure非重複の記録文書だけで、関連runtime/source11/policyは不変。

旧58bundle547組prefixを保持し、59bundle549組候補へ新ZIP `manga-explanatory-20261110-l3-josei-period.zip`（542246bytes、SHA `eaca1a37ef445d3d0e06a22cc5c1ccfd86db77b443725d3cc9b2d7bb407724bd`）だけ追加。4新JPEGはL/元比率/長辺1024以下、thumbは白余白384×512。回帰・隔離Store・日英UI・独立review・PR/Release往復/merge後、GitHub Actionsを起動せず新seedだけ直接配置。本番receipt全SHA/fullreadback後のみpublished。認証/Caddy/workflow/UID/volume/network/CPU0.5/RAM384MiB/PID128と他serviceを保持。

### 料理・暮らしの説明用2枚組候補（2026-11-10）

21分類42monoを画像ごとの独立セッションで生成し、42job/原画/実送信文/42固有sessionを照合。初見42と限定9＝実51確認を結合し、doodle-casual/chibi-comic/bold-comic/rough-light/retro-shojoの5分類10枚を差分付き採用候補とする。16分類は旧公開を維持。元full11/partial31、文字none41/uncertain1、限定4true5false（8whole1crop）、positive14役/単役positive4、notesのstr/list/dict全型値を保持し、全語完全一致とは呼ばない。

bold-comic別場面とretro-shojo代表の近似構築を境界幅と見える釣り合いから限定肯定。名目一頭差や厳密式では否定せず、natural-quiet/real-fine別場面は小頭と長い首下の別構築としてhold。elegant代表とpen-classic別場面は人物の広い衣服面の網点と要所少量を分離しhold。hair-detail両役の見える段階的トーンと白抜きは肯定したが、別場面の床同一タイル内のぼけた反射濃淡は背景white/flat条件に未一致でhold。物理素材枚数/カッターの使用は断定しない。elegant相方の限定実見は事前条件で取消し、肯定やmissing coverageへ置換しない。独立hold後の文字/眼/粒径などの追加も行わず、元uncertainは不変。Fの許可inputを次batchに限定せず先に表示した出力economy差は保存し、資源/保護操作scope適合と分離、fresh全体契約passとはしない。

実6fieldとmedium Noneを保持し、親のサインペン/丸顔/点目/5頭身/淡tone髪を一律追加しない。台所の女性/食卓そばの男性、枝群ごとの小物/構図/背景はsample-only。背景要素量/距離/服丈/画角外などの残差は元所見とともに保存。source17は以前の技術肯定と同SHA、converterはparent ID/公開base SHA/題名の実3parameter全buffer変換とし、新payload/採否/実行は別検証する。

旧59bundle549組prefixを保持し、60bundle554組候補へ新ZIP `manga-explanatory-20261110-l3-josei-lifestyle.zip`（1179803bytes、SHA `788d273b9bb8dd3bcae436fcb774c06abe74150bfc066ab87f46e2136bfb70db`）だけ追加。新10JPEGはL/元比率/長辺1024以下、thumbは白余白384×512。回帰/隔離Store/日英UI/独立review/PR/Release往復/merge後、GitHub Actionsなしで新seedだけ直接配置。本番receipt全SHA/fullreadback後だけpublishedとし、認証/Caddy/workflow/UID/volume/network/CPU0.5/RAM384MiB/PID128・他service・rollbackを保持する。

## 説明用2枚組：女性・サスペンス（2026-11-10）

- 見本帳の目的を「現行プロンプトで実際に何が出るかを人が見て判断すること」として運用。頭身・描法・トーン量・場面の指定との差は観察記録に残し、掲載可否の選別条件にしない。プロンプトの見直しと再生成は、その後の人の判断による別工程。
- 女性・サスペンス20枝40monoの実出力を全件掲載対象とする。40固有session、生成記録と原画SHAの対応を確認済み。新たな生成や適合判定の追加AI審査なし。旧4組のみ選別した候補と元fit/false/null/保留所見は履歴として保存し、全指定一致とは改称しない。
- 旧61bundle558組を保全し、新20組を固定SHAで追加する62bundle578組。画像・実生成文・枝完結styleの組を保持する。既存アプリは変更せず、実payloadの隔離Store取込・配信画像/文章対応と表示・独立の配布確認を経てPR/merge後にGitHub Actionsなしで新seedだけ直接配置する。

## 生成済み実出力の復旧掲載（2026-11-10）

- 見本帳は現行の記録済みプロンプトが実際に返した結果を人へ見せるもの。過去に描法/頭身/トーン量/場面の適合で保留した665枝1330枚を、新規生成や画像AI再採点なしで掲載対象へ戻す。元の不一致・未確認・保留所見は履歴として保全し、掲載を全指定適合へ改称しない。プロンプト見直しは後の人の判断。
- 全665枝の最新記録済み完了attemptを使用（657枝attempt1、8枝attempt2）。1330固有session・原画/job/complete/実生成文/完結styleを照合。1310monoと20colorの元表現を保持する。見た目による過去候補の選別なし。
- 既存のZIP制限8MiB（圧縮済み）/65項目/64MiB（展開合計）を守り、16組以下かつ実バイト量で43archiveへ分割。初回21archiveは8MiB超過で通常prepareが拒否し履歴保全。JPEGを再圧縮せず同じ1330ファイルを再梱包した。旧62bundle578組は不変、新規43を加え105bundle1243組とする。アプリ/認証/権限/workflowは不変。PR/Release/merge後にActionsを起動せず新seedだけ直接配置し、配信と最低限の表示確認後に公開を確定する。

## 見本帳seed起動時の保存コスト修正（2026-11-10）

- 復旧665組の初回配置はstartup内で時間を使い、626秒のreadiness確認中も502/unhealthyだったため旧イメージへ戻した。旧イメージでhealthy/公開200を確認。原画・Release43ZIP・過去所見・失敗証拠・本番volumeは削除せず、公開確定もしていない。
- 起動中の2枚組取込は、1組ごとに全stateを2回直列化・保存していた。実Storeの2組fixtureで5回の全体保存を再現。lifespanで公開前・lock保有中のpair seed取込に限り保存をまとめ、通常は最後に1回、後続shard拒否時は正常済み分を保存して元例外を再送出する。通常の手動更新は即時保存のまま。画像・manifest検査/履歴/原画保全/版管理/再開の冪等性は維持する。
- CPU0.5/RAM384MiB/PID128/healthcheck・認証・Caddy・workflowを変えない。新規画像生成・再圧縮なし。別PRの試験・隔離負荷確認・読取レビュー後にmanga-styleのみ直接反映し、元665組の公開readbackを再開する。


### 2026-11-10 女性・90年代の耽美：実出力21枝42枚

承認済みの説明用2枚組を21枝へ追加。各画像を独立process/sessionで生成し、現在の6fieldを変更せず、実生成プロンプト・枝完結style・原画と対応させる。外観の適合採否・画像AIの追加審査はしない。monoはL、元画角を保ち長辺1024以下、thumbのみ白余白384×512。新1bundle 21pairを加えて106bundle/1264pair。旧1243組・原画・旧所見・既知安全拒否2件を保全。

配置前に通常prepare、隔離Storeで旧1243→1264の追加・非対象2735保持・再起動不変、最小UI、独立読取確認を行う。GitHub Actionsは起動せず、feature/mergeへ[skip ci]を付ける。アプリ・権限・workflowは変更しない。マージ後は固定SHAのReleaseを往復検証し、既存image上へ新seedだけ追加してmanga-styleのみ直接配置、全21組42画像とAPI保持・実ブラウザ表示を読戻す。全2756枝の完了ではなく、当該cohort公開後にも1490pendingと安全hold2が残る。


### 2026-11-10 児童漫画・ホビー対戦：実出力22枝44枚

承認済みの見本帳を22枝へ継続。現在の6fieldを変更せず、各画像を独立process/sessionで生成。親L2の円盤ホビー題材を卓上の少年と広場の少女の別場面に分離し、styleに題材の人物・場所を混ぜない。外観の適合採否・画像AIは追加しない。新1ZIPを旧106bundle/1264pairへ加え、候補は107bundle/1286pair。原画・元所見・失敗・安全拒否を保全。

通常prepare、実dirの旧seedを使うfresh隔離取込・非対象2734保持・版更新一回・再起動不変、最小UIと限定独立読取を行う。GitHub Actionsは起動せずfeature/mergeへ[skip ci]。merge後はRelease往復SHA、既存imageへ新seedだけoffline layer、manga-styleのみ直接配置。本番全22組44画像の配信・保持・health・UI・receipt読戻し後にpublishedを進める。アプリ/認証/権限/workflowは変更しない。cohort後も1468pendingと再送禁止の安全hold2が残り、全2756枝完了ではない。


### 2026-11-10 児童・冒険/ギャグ：実出力45枝90枚

既承認の児童冒険24枝と児童ギャグ21枝を、同じ2workerで45枝90枚の1cohortへまとめた。現行6fieldを変更せず、独立process/session、実生成文と枝完結style/原画の対応を保持。外観AI/適合採否/retry-to-fitなし。親L2の承認題材はsceneだけへ使用。新2ZIP（8,178,379/6,751,713bytes）を旧107bundle/1286pairに加え、候補109bundle/1331pair。旧archiveは実ファイルへ直接resolveしたpool symlinkで参照し、長いsymlink連鎖を増やさず同SHAを保つ。全consumer上限は不変。

通常prepare、fresh実dir/hardlink旧seed取込・非対象2711保持・版一回/restart不変、最小UI/限定読取を経てPR/Releaseへ。GitHub Actionsなし、feature/mergeに[skip ci]、既存imageへ新seedだけoffline layer、manga-styleのみ直接配置。CPU/RAM/PID・volume/network/ports/security・アプリ/認証/権限/workflowは変更しない。本番45組90画像/45thumb/2711controls/health/UI/receipt全読戻し後にpublishedへ進める。原画/旧公開/失敗/元所見/安全hold2を保全。当cohort後も1423pending+hold2が残り全2756枝完了ではない。

## 児童8群の175枝350枚を実出力見本として追加

児童の動物23・学習21・魔法21・学校21・スポーツ21・ミステリー23・モンスター24・図形21、計175枝について、現行6項目を変えず独立した代表・別場面の350枚を追加する。元の承認済み題材を使い、画角・付随背景・無地服の矛盾だけ場面側で調整した。全画像は別process/session、参照・過去会話継承なし。mediumNoneの白黒枝が対象で、別medium4枝はpending維持（外観の採否保留ではない）。

これはプロンプトへの適合合格集ではなく、今のプロンプトが実際に出した絵を人が判断する見本帳である。外観AI採点・好みの再試行・旧所見の改称はしない。原画・実生成文・枝完結style・SHA・sessionを対応付ける。要求modelと実engine保証は区別する。

新7ZIPは既存109bundle/1331pairを保ち、合計116bundle/1506pair。8MiB/4MiB member/64MiB展開/65entries/32pair/128bundleのguardは不変。取込・非対象2581保持・版一回・再起動保持と9UI（8親の新白黒390ja＋既存カラー1280en）を確認した。viewport emulationであり物理端末の試験ではない。通常実装・既存試験の同SHA証拠は再利用し、新payloadを独立確認する。

GitHub Actionsは起動せず、feature/mergeの[skip ci]・run0を確認する。PR/Release往復SHAを維持し、review済みseedだけ既存imageへの新layerとしてmanga-styleへ直接配置する。CPU0.5/RAM384MiB/PID128、UID/read-only/volume/network/security/Caddy/認証/権限・他serviceを変えない。全配信とhealth/UI、受入receipt全読戻し後だけ正式publishedへ進める。未来の配布完了をこの追加説明で先取りしない。

## 4コマ系243枝486枚と同JPEG再梱包

既承認の4コマ系11親について、mediumNone243枝の現行6項目を変更せず、代表と別場面の486枚を各1独立process/sessionで生成した。各画像は1場面であり、コマ割りを指定しない。元L2題材はscene側に使い、画角・付随背景・無地服の矛盾だけ調整する。実出力見本帳なので外観AI採点・好みの再試行・適合による選別をしない。別medium20枝と安全拒否2件は保全する。

配布数が120へ達する前に、既存116bundle/1506pairと新243pairを、画像を描き直さず再圧縮せず70bundle/1749pairへ再梱包する。旧ZIPと原画・Git履歴・旧採否は保存し、JPEG全3498枚のbytesと枝別JSON recordの原文字列bufferをそのまま運ぶ。配布アーカイブ全体のmanifest配列の外枠とZIP SHAだけは梱包に応じて変わる。8MiB ZIP/4MiB member/64MiB展開/65entries/32pair/128bundleのguardは緩和しない。

通常prepare1749、fresh実dir/hardlink旧1506→1749の取込で、旧1506の再取込0、旧6028画像ファイルSHA不変、非対象2513nodeの型を含む全内容不変、新243だけ版一回、restart全state不変/再取込0を確認した。11親の新mono390ja＋既存カラー1280enの12UIを実decode/可視/比率/overflowで確認。viewport emulationで物理端末の試験ではない。既存17実装とnative8の同SHA証拠を再利用し、今回の新画像・再梱包・保持経路は別に独立確認する。

直接配置する新imageでは、旧116seedディレクトリを残して混在させず、新しい70ディレクトリへimage内だけで完全置換する。読み取り専用bindから全payloadのファイル集合/SHAを検査してから、固定のimage path /srv/manga/app/seed/pairsだけを置換する。build中だけUSER root、終了時は既存の10002:10002へ戻し、ネットワークなし・pullなし、1つの新filesystem layerに限定する。旧base image・元ZIP・本番volume・アプリコードは変えない。既存CPU0.5/RAM384MiB/PID128、read-only/capdrop/security/ports/network/UID・他service不変を読戻す。

GitHub Actionsは起動しない。feature/merge双方[skip ci]・run0を確認し、0checksをCI成功と呼ばない。PR/Release70asset往復SHA/同byte prepare受入を維持し、本番全配信/healthy/12UI/receipt全読戻し後だけ243をpublishedに加える。全2756枝の完了とは区別する。

## ギャグ系286枝572枚の実出力追加

既承認のギャグ系13親のmediumNone286枝について、現行6項目とtagsを変えず、代表/別場面の572枚を各1独立process/sessionで生成した。男女はpair全体で示し、全画像に2人を固定しない。1画像1場面、外観AI採点/適合による選別/好みのretryを行わず現行promptの実出力として載せる。別medium5枝はpending、安全拒否2件は保存して再送しない。

新572JPEGだけ1回encodeし、旧70ZIP1749pairは不変のまま新12ZIP286pairを追加する。全82bundle2035pair、8MiB ZIP/4MiB member/64MiB展開/65entries/32pair/128bundle guardは不変。通常prepare2035/86inputs、fresh実dir/hardlink旧70/1749→82/2035で旧再取込0・旧7000files SHA不変・非対象2470nodeの全field型保持・新286だけ版一回・restart全state不変/再取込0を確認した。fixture説明の旧件数だけ置換残りがあり、実行driver/resultは保存しactual old_pairs1749へ別acceptanceで訂正した。製品再実行はしない。

13親newmono390jaと既存color1280enの14UIを実decode/可視/比率/overflowで確認する。viewport emulationで物理端末試験ではない。既存実装17/native8/87cases(2skip)とconverterは同SHA所見を再利用し、新572のliteral要求/来歴/style/画像結合・取込・配布は今回の独立読取確認へ結合する。

GitHub Actionsは起動せずfeature/merge双方[skip ci]とexact head run0/checks0を読戻す。0checksをCI成功と呼ばない。Release12往復SHAと同byte正常prepareを結合し、既存local base imageへ新12seed584filesだけnetworknone/pullfalseで1filesystemlayer追加する。旧70seed/app/既存baseと本番volumeを保持、runtime UID10002/CPU0.5/RAM384MiB/PID128/read-only/capdrop/security/ports/networkと恒常30serviceを変えない。manga-styleだけno-deps/no-buildで直接配置し、本番286/572/286thumb/2470controls/healthy/14UIとreceipt完全読戻し後のみ正式publishedへ加える。全2756枝完了とは区別する。

## ホラー系216枝432枚の実出力追加

既承認ホラー10親のmediumNone216枝、現行6項目/tagsを変えず432枚を各1独立process/sessionで生成。男女はpair全体/1画像1場面。外観AI/適合採点/好みretryなし、実出力とliteral生成文/枝完結styleを対応させ、改善は掲載後の人の判断とする。別medium3と安全拒否2は保持し再送しない。

新432JPEGだけ1回encode、旧82ZIP2035pairは不変、新10ZIPで92bundle2251pairへ追加。8MiB/4MiB/64MiB/65entries/32pair/128bundle guard不変。通常prepare2251/96inputs、fresh実dir/hardlink old82/2035→92/2251で旧再取込0/旧8144filesSHA不変/非対象2540node全field型保持、新216だけ版一回/restart全state保持・再取込0を確認。fixture説明も最後に明示指定し実countと一致。旧source17/native8/87cases2skip/同じconverterは同SHA所見を再利用、新payload来歴/consumer/保持/11UIを別に確認する。viewport emulationで物理端末試験ではない。

Actionsは起動せずfeature/merge双方[skip ci]/exact run0/checks0を読戻しCI成功と呼ばない。PR/Release10往復SHA/同byteprepareを経て、既存local imageへ新seed442filesだけnetworknone/pullfalseで1filesystemlayer追加。app/旧82seed/base/本番volume/UID10002/CPU0.5/RAM384MiB/PID128/security/network/ports/恒常30を保持しmanga-styleだけno-deps/no-buildでdirectする。本番216/432/216thumb/2540controls/healthy/11UIとreceipt全読戻し後だけpublished。全2756枝未完と区別し、原画/過去false/採否/超過を保存する。

## エッセイ系220枝440枚の実出力追加

承認済み10親のmediumNone220枝、現行6項目/tags無修正・1画像1独立process/sessionで440枚生成。男女はpair全体、1画像1場面。外観AI/適合選別/retryなし、実出力とliteral生成文/枝完結styleを対応させ、改善は掲載後の人の判断。別medium3と安全拒否2を保持し再送しない。mediumは公開APIに無いroot fieldでなくcatalog style-keyから解決。

新440JPEGだけ1回encode、旧92ZIP2251pairは不変、新10ZIPで102bundle2471pair候補。通常prepare2471/106inputs/CLI0、8MiB/4MiB/64MiB/65entries/32pair/128bundles guard不変。新専用worktreeは無関係sitesを初めから展開せず、全reviewed sourceは同SHAで存在し、原画/証拠/他task/本番data/Git objectに干渉しない。

fresh realdir/hardlink old92/2251→102/2471の隔離取込と全typed2536非対象nodes/旧9008filesSHA/旧import0/新版1回/restart保持を確認する。旧source17/native8/87cases2skipとconverterは同SHA所見/宣言parameter変換後全buffer同一を明示再利用し、新payload440来歴/consumer/保持/11UIを分けて確認する。390/1280はviewport emulationで物理端末試験ではない。pendingとnot_appearance_holdの実型を検査し、文字列heldの有無をgateにしない。原false/超過を保持する。

Actions非使用、feature/merge双方[skip ci]/exactrun0checks0（CI成功ではない）、workflow/保護/権限/Caddy/認証は不変。PR/Release新10asset実downloadSHA/同byteprepare後、新450seedfilesだけnetworknone/pullfalseで既存imageへ1layer追加し、manga-styleだけno-deps/no-buildでdirect。CPU0.5/RAM384MiB/PID128/UID10002/旧seed/app/volume/network/security/恒常30を保持。本番220pairs440images220thumb/2536controls/healthy/11UIとreceipt全読戻し後だけpublished。全2756未完と区別しrollback image/composeと全履歴を保持。


### 劇画の実出力245枝490枚（2026-11-11）

- 現行の枝完結styleと、実際に送った日英の生成promptを2枚の絵と組にする。外観の一致判定を掲載gateに戻さず、修正判断は掲載後の人に委ねる。source6field/tagsは無修正。
- 元263枝526要求は445完了・1安全拒否・80未送信で停止。元summary、request/result/attempt/failed、原画と成功済み片方を保持する。拒否された瓶開け描写を再送・言換え・別経路へ切替しない。同描写の未送信17枝は予防保留とし、実API拒否とは別集計。
- 拒否内容と異なる既承認の工房・木箱scene23枝46要求だけ、元job無変更・未送信・fresh process/sessionで別rootに実行して完了した。元の失敗batchを成功へ改称せず、245完全組490枚（元222組444枚＋別23組46枚）だけを来歴検証済みの出版集合にする。成功片方のみの1枚は未採用のまま保全。
- 新490枚のみ元比率を保持してL JPEGへ一度変換し、新13ZIP/503membersを追加する。旧102ZIP2471組のJPEG/recordは不変、候補115bundle2716組。8MiB/4MiB/64MiB/65entries/32pair/128bundle guardを維持する。
- 原生成526の失敗summaryと別46の成功summaryをそれぞれ保存し、出版集合は専用verified-selection（API成功responseではない）で実Rootと490 roleを結ぶ。部分検証成功と元全件batch失敗を別fieldで保持する。新しい選択境界は独立読取確認へ、変更していないconverter/Store/native8の所見は同SHAで再利用する。
- 通常prepare/隔離・旧record/画像/版/restart/実browserで技術配信を検証し、PR/mergeとRelease全asset往復SHAを経てActionsなしの既承認direct方式でmanga-styleだけを配置する。公開受入とreceipt読戻し前は候補でありpublishedと数えない。別medium20/安全拒否/未送信予防保留を完了扱いにしない。


### 最終medium20枝40枚の実出力（2026-11-11）

- 残20枝は12モノクロ/8カラー、16親。qualified style keyをそのまま実exporterに照合し、repair登録の配置限定bg値だけを既存sourceとして保持する。raw共有ARCHと配置値の相違を新しいprompt修正と誤認しない。
- medium/base/finished styleを展開済みの現行API complete promptを日英tags含めliteralで使い、新しい承認済みsceneだけをsample側へ追加。矛盾や旧指定の改善を先取りせず、現在のpromptの実出力として見せる。source6field/tags不変、20枝のstyleは現在APIと完全一致。2枚の人物/場面は既承認L2から、1枚ごと独立process/session、要求2.6とreported null/enforced falseを分離。
- 全20に既存complete/attemptが無いことを確認して40枚だけ生成、40固有session/拒否0。新24枚L/16枚RGBだけ一回元比率JPEGへ変換、新1ZIP41members/旧115ZIP2716pair保持→116bundle2736pair候補。通常guardは不変。
- 直前に受入済みの私的2716 stateをfresh実directoryへコピーし、mutable metadataは実copy、immutable image filesだけhardlink。元state全同値/元file全SHAを確認し、2716の冷再取込を繰り返さず旧再取込0/新20だけ一回更新/全非対象typed/旧file/restartを検証する。本番dataはfixture入力にしない。
- 独立読取・実browser・PR/merge/Release往復SHA後、Actionsなしdirectでmanga-styleのみ新seed layerを配置し、本番全件/実UI/receipt後にpublishedへ。安全拒否3枝/同じ拒否描写の未送信予防17枝は別保全し、再送・言換え・経路変更せず未完として区別する。


## 説明用2枚組：残20枝の場面変更（2026-11-11）

- 利用者「それは、シーンを変えなさい」に従い、元style20を無変更で別の行為・小道具・場所へ変更。新37枚を独立process/sessionで生成し、既存成功兄弟3枚は元prompt/原画のまま保持、20pair40role/40固有session。元のAPI安全拒否3/同描写の未送信予防17/元失敗summaryを保全し、新場面成功を元要求の成功へ改称しない。年齢変更や経路変更の回避ではない。
- 学園代表は16歳を維持して中庭の水やり、バトル代表は成人男性の鉢植え並べ、劇画の新代表は読書、新applicationは積み木並べ。場面以外の6field/タグ/元style/過去の既承認bg修正chainは変えない。外観fitで絵を隠さず、現在の実出力とliteral生成promptを示す。
- 新40役のみ一回JPEG化、8MiB制限を維持して新2ZIP42members、旧116bundle2736pairの記録/画像不変→118bundle2756pair候補。通常prepareの初回容量失敗を保持し、公開済み旧scifiのsitesだけを可逆sparse/全non-sites2352SHAとHEADを保全、再生成/再encodeせずprepareだけ再開して実2756成功。
- 受入済みM私的state10948imageからfresh realdirへmutable metadata copy/immutable images hardlink。before全state同値/旧import0/new20版1回40image/非対象2736typed/旧SHA/restart0を検証し、本番dataをfixtureにしない。
- 配置は独立読取と主担当gate受入後、feature/merge双方[skip ci]/workflow35policy2不変/Actions0checks0（CI成功ではない）。Release新2実downloadSHA往復と同bytes成功prepareを別ownerで結合。稼働M image/app10同SHAから新42seedだけoffline1layer/全bytecheck→manga-styleだけdirect、CPU0.5RAM384MiBPID128/security/volume/network/ports/恒常30維持。
- 本番20pair40image20thumb/all2756/非対象2736/healthy/実UI21/receipt全読戻し後だけ台帳published。原拒否/安全履歴/成功兄弟/全原画/旧公開/本番volume/Git/rollback imageは保持する。
