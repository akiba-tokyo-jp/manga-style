"""Text of the API guide page (/api), per language. The page template renders these blocks as they are.

Block kinds: {"p": text}, {"code": text}, {"ul": [text, ...]}, {"ol": [text, ...]}.
FIELDS lists every key of the JSON the API returns; tests check that the live responses have no
undocumented key.
"""

API_DOC = {
    "ja": {
        "title": "API の使い方",
        "lead": "このサイトの絵柄は、プログラムから JSON で読めます。読み取りだけで、登録は要りません。",
        "sections": [
            {"heading": "使う URL は 2 つ", "blocks": [
                {"code": "GET {origin}/v1/tree"},
                {"p": "公開中のすべての枝（1〜3段目）。各枝の id・parent（親の id。1段目は null）・level・title・summary・thumbnail_url。"},
                {"code": "GET {origin}/v1/styles/{id}"},
                {"p": "1 つの枝の絵柄。プロンプト、見本の絵、1 つ下の段の一覧（children）が入っています。"},
                {"p": "どちらも ?lang=en を付けると、名前と説明が英語になります（既定は日本語）。プロンプトは常に日本語と英語の両方が入っています。"},
            ]},
            {"heading": "絵柄の選び方", "blocks": [
                {"ol": [
                    "1段目の一覧は、/v1/tree のうち parent が null の枝です。",
                    "/v1/styles/{1段目の id} の children から 2段目を選び、/v1/styles/{2段目の id} を読みます。",
                    "その children から 3段目を選びます。どの段で止めてもかまいません（下の段はおまかせになります）。",
                ]},
            ]},
            {"heading": "画像生成での使い方", "blocks": [
                {"ul": [
                    "prompt.en（または prompt.ja）を絵柄の指定として使い、その後ろに描きたい人物・場面を書き足します。prompt には題材は入っていません。",
                    "avoid は、絵に入れてはいけない物（文字・フキダシ・効果音の描き文字・コマ枠・署名・透かし・色）です。",
                    "samples[reference].url の見本の絵を、絵柄の参考画像として渡せます。",
                    "従来方式の3段目の prompt は「2段目の言葉 ＋『仕上げの絵柄（上と違う所はこちらに従う）: 』＋ 3段目の言葉」です。食い違う所（ベタの量・頭身など）は 3段目の言葉に従ってください。",
                ]},
            ]},
            {"heading": "Genko Studio から使う", "blocks": [
                {"p": "枝のページを ?client=genko 付きで開くと「この絵柄を使う」が出て、genko://use-style?id={id} を開きます。普通のブラウザでは、かわりにその枝の API の URL をコピーできます。"},
            ]},
            {"heading": "そのほか", "blocks": [
                {"ul": [
                    "HTTPS で、誰でも読めます。CORS は GET だけ許可しています。",
                    "限定公開にしているときは Authorization: Bearer <トークン> が要ります（無いと 401）。",
                    "無い id や公開していない枝は 404（{\"error\": \"not found\"}）。GET 以外は 405 です。",
                    "従来の見本は768×1024のJPEGです。説明用2枚組は元の縦横比を保ち長辺1024以下、白黒枝はL・彩色枝はRGB。縮小画像は384×512で、2枚組は余白を付けて全体を残します。",
                    "見本の絵か言葉が変わると version が上がり、updated_at が変わります。",
                ]},
            ]},
        ],
        "tree_heading": "/v1/tree の nodes[] の欄",
        "style_heading": "/v1/styles/{id} の欄",
        "examples_heading": "実際の応答",
    },
    "en": {
        "title": "API guide",
        "lead": "The styles on this site can be read as JSON by programs. Read-only; no sign-up is needed.",
        "sections": [
            {"heading": "Two URLs", "blocks": [
                {"code": "GET {origin}/v1/tree"},
                {"p": "Every published branch (levels 1 to 3), each with id, parent (the parent id; null at level 1), level, title, summary and thumbnail_url."},
                {"code": "GET {origin}/v1/styles/{id}"},
                {"p": "One branch: its prompt, its sample image and the branches one level below (children)."},
                {"p": "Add ?lang=en for English names and descriptions (Japanese by default). Prompts always carry both Japanese and English."},
            ]},
            {"heading": "Choosing a style", "blocks": [
                {"ol": [
                    "Level 1 is the branches of /v1/tree whose parent is null.",
                    "Pick a level-2 branch from children of /v1/styles/{level-1 id}, then read /v1/styles/{level-2 id}.",
                    "Pick a level-3 branch from its children. You may stop at any level (the levels below are left open).",
                ]},
            ]},
            {"heading": "Using it for image generation", "blocks": [
                {"ul": [
                    "Use prompt.en (or prompt.ja) as the style and append the person and scene you want. The prompt has no subject.",
                    "avoid lists what must not appear: text, speech balloons, sound-effect lettering, panel borders, signatures, watermarks and colour.",
                    "The sample image samples[reference].url can be passed as a style reference image.",
                    "A legacy level-3 prompt is the level-2 words + \"Finished style (where it differs from the above, follow this): \" + the level-3 words. Where they disagree (amount of black, head-to-body ratio and so on), follow the level-3 words.",
                ]},
            ]},
            {"heading": "From Genko Studio", "blocks": [
                {"p": "A branch page opened with ?client=genko shows \"Use this style\", which opens genko://use-style?id={id}. In an ordinary browser you can copy the branch's API URL instead."},
            ]},
            {"heading": "Other notes", "blocks": [
                {"ul": [
                    "HTTPS, readable by anyone. CORS allows GET only.",
                    "When the API is limited, send Authorization: Bearer <token> (401 without it).",
                    "Unknown or unpublished branches return 404 ({\"error\": \"not found\"}). Methods other than GET return 405.",
                    "Legacy samples are 768×1024 JPEG. Explanatory pairs retain their aspect ratio at up to 1024 pixels on the long edge: L for monochrome and RGB for color branches. Their 384×512 thumbnails are padded, not cropped.",
                    "When a sample image or the words change, version goes up and updated_at changes.",
                ]},
            ]},
        ],
        "tree_heading": "Fields of nodes[] in /v1/tree",
        "style_heading": "Fields of /v1/styles/{id}",
        "examples_heading": "Live responses",
    },
}

TREE_FIELDS = {
    "ja": [
        ("id", "枝の id（英小文字・数字・ハイフン）。"),
        ("parent", "親の枝の id。1段目は null。"),
        ("level", "段（1〜3）。"),
        ("title", "表示名。"),
        ("summary", "一言の説明。"),
        ("thumbnail_url", "その枝の見本の縮小画像（384×512）。見本が無ければ null。"),
        ("path", "1段目からこの枝までの表示名の並び（最後がこの枝）。例: [\"ギャグ漫画\", \"シュール\", \"ゆるい手描きの落書き風\"]。同じ表示名の枝がほかの分類にもあるので、名前だけで絵柄を決めない。"),
    ],
    "en": [
        ("id", "Branch id (lowercase letters, digits and hyphens)."),
        ("parent", "Parent branch id; null at level 1."),
        ("level", "Level (1 to 3)."),
        ("title", "Display name."),
        ("summary", "One-line description."),
        ("thumbnail_url", "Thumbnail of the branch's sample (384×512); null without a sample."),
        ("path", "Display names from level 1 down to this branch (this branch last), e.g. [\"Gag manga\", \"Surreal\", …]. The same name exists under other categories, so never pick a style by its name alone."),
    ],
}

STYLE_FIELDS = {
    "ja": [
        ("id", "枝の id。"),
        ("path", "上の段（1段目から親まで）の id と表示名の並び。上の段から順。1段目は空の配列。"),
        ("level", "段（1〜3）。"),
        ("title", "表示名。"),
        ("summary", "一言の説明。"),
        ("expression", "\"mono\" は白黒、\"color\" はカラー。既存の枝は mono のまま。"),
        ("model", "id は \"chatgpt-image\"。version は見本を作った画像生成のモデル名（見本が無ければ null）。"),
        ("prompt", "ja・en・tags。共通の言葉 ＋ その枝までの言葉（1段目は 1段目だけ、2段目から下は 2段目から）。題材は入っていない。"),
        ("avoid", "絵に入れてはいけない物。"),
        ("samples", "見本の絵。従来はupper_bodyの1枚。更新した枝はrepresentative（代表）とapplication（別の場面）の2枚。各要素はsubject・url・prompt（日英の実際の生成文）。"),
        ("reference", "絵柄の基準として一番よい見本が samples の何番目か（0 から）。見本が無ければ null。参照画像の枚数ではない。"),
        ("license", "generated は常に true、artist_names は常に false、terms は利用条件。"),
        ("version", "見本の絵か言葉が変わると上がる番号。"),
        ("updated_at", "最後に変わった日時（UTC）。"),
        ("children", "公開中の 1 つ下の段（id・title・summary・thumbnail_url）。3段目は空。"),
        ("comparisons", "比較の絵（2026-10-18 追加）。見本を作ったプロンプト（samples[0].prompt.en）を変えずに別の画像生成モデルで描いた絵。"
                        "model（id・version・name）、url、prompt_from、settings（seed・steps・cfg_scale・sampler・size・negative_prompt）、created_at。"
                        "絵柄の指定ではない（参考画像には samples[reference] を使う）。無い枝は空の配列。足しても version は変わらない。"),
    ],
    "en": [
        ("id", "Branch id."),
        ("path", "Ids and names of the levels above (from level 1 down to the parent), top first; an empty list at level 1."),
        ("level", "Level (1 to 3)."),
        ("title", "Display name."),
        ("summary", "One-line description."),
        ("expression", "\"mono\" is black-and-white and \"color\" is full color. Existing branches stay mono."),
        ("model", "id is \"chatgpt-image\"; version is the image model that made the sample (null without a sample)."),
        ("prompt", "ja, en and tags: the common words + the words down to this branch (level 1 alone; from level 2 down otherwise). No subject."),
        ("avoid", "What must not appear in the picture."),
        ("samples", "Sample images: one legacy upper_body, or representative followed by application for an updated branch. Each has subject, url and prompt (the actual Japanese and English generation text)."),
        ("reference", "Index in samples of the best sample for the style (from 0); null without a sample. Not a count of reference images."),
        ("license", "generated is always true, artist_names always false; terms are the conditions of use."),
        ("version", "Goes up when the sample image or the words change."),
        ("updated_at", "When it last changed (UTC)."),
        ("children", "Published branches one level below (id, title, summary, thumbnail_url); empty at level 3."),
        ("comparisons", "Comparison pictures (added 2026-10-18): the prompt that made the sample (samples[0].prompt.en), unchanged, drawn by "
                        "another image model. model (id, version, name), url, prompt_from, settings (seed, steps, cfg_scale, sampler, size, "
                        "negative_prompt) and created_at. Not the style (use samples[reference] as the reference image). An empty list when "
                        "there is none; adding one does not change version."),
    ],
}

EXAMPLE_IDS = ("shonen", "shonen-battle", "shonen-battle-bold-black")
