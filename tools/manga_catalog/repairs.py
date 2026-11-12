"""全件再確認で指摘された29枝だけの、画材と描き直し方法の置換。"""
from __future__ import annotations

# 共通文には顔・構図を持たせず、枝の選択を尊重する。長さは既存共通文以下。
RECIPES = {
    'flatmodern': ('白黒のすっきりした漫画。目を細い小さい楕円に置換、虹彩も小さく、まつげときらめきなし。髪は3房の白黒形、服は白地に少量の平網点。背景1形。立体陰影・ぼかしなし。', 'Clean black-and-white manga. REPLACE big romance eyes with SMALL NARROW OVALS and SMALL irises, no lashes or sparkles. Hair THREE white-and-black locks. WHITE clothes with a LITTLE flat halftone. ONE setting shape. No volumetric shading or blur.'),
    'flatkaidan': ('白黒の怪談漫画。目は横長の細い切れ長、黒髪は真っすぐな房。廊下と床は一様な暗い平網点1面、反射は白い帯1本。床の段階陰影・ぼかしなし。顔と服は白。', 'Black-and-white ghost manga. Eyes LONG NARROW slits, hair straight BLACK locks. Corridor AND floor ONE uniformly DARK flat halftone, reflection ONE WHITE band. NO tonal fade, gradation or blur on the floor. WHITE faces and clothes.'),
    'flatdiary': ('白黒の日記漫画。力を抜いた表情のまま、垂れたまぶたの下に大きい瞳と白光を描く。服とソファは白い輪郭のみ、床は白、影は接触部の小さな網点だけ。背景1形。', 'Black-and-white diary manga. Keep the relaxed expression, but LARGE visible irises and white highlights under drooping lids. Clothes AND sofa WHITE contours ONLY. WHITE floor, shading ONLY tiny flat halftone patches at contacts. ONE setting shape.'),
    'rough': ('白黒の未清書の鉛筆下描き、完成清書にしない。探る二重輪郭と目立つ途切れ。髪は雑な外周3束、服はしわ2本。髪細線・清書輪郭・灰面なし。背景1形以外は白い紙。目は枝の形。', 'UNFINISHED rough pencil CONSTRUCTION SKETCH, NOT final manga ink. Loose searching DOUBLE contours with VISIBLE gaps. Hair only THREE rough outer loops, clothes TWO folds. NO hair strands, clean contours or grey fills. ONE background shape and WHITE paper. Eyes as specified by the branch.'),
    'flat': ('白黒の漫画。白い紙、黒ベタ、輪郭の明瞭な平らな網点で描く。頬・服・背景をぼかして丸く塗らない。枝で指定する線・目・余白を優先する。', 'Black-and-white manga: white paper, solid blacks, sharply bounded flat halftone. No blurred volumetric rendering on cheeks, clothes or scenery. Follow the branch for lines, eyes and white space.'),
    'white': ('白黒の漫画。服は輪郭としわ2本だけ、顔・服は白い紙。灰面と細密線なし。背景は形1個、残りは白。枝の線と目を優先。', 'Black-and-white manga. Clothes ONLY contours and TWO folds. WHITE faces and clothes, NO grey fills or fine detail. ONE background shape, the rest WHITE. Follow branch line and eye shapes.'),
    'doodle': ('白黒の落書き漫画。目を小さい黒点2個に置換、瞳の白光・まつげ・鼻を描かない。髪は3個の形、服は輪郭としわ2本。少し揺れる少数の丸線、背景1個以外は白。', 'Black-and-white crude diary doodle. REPLACE eyes with TWO tiny solid BLACK DOTS, NO eye whites, highlights, lashes or nose. Hair THREE shapes, clothes contours and TWO folds. FEW wobbly round lines, ONE setting shape and blank WHITE paper.'),
    'pencil': ('白黒の鉛筆漫画。ざらざらした灰色の鉛筆細線、紙粒の途切れを残し黒い清書線にしない。網点は小面2個。白背景に遠い輪郭1個。顔と服を滑らかに塗り込まない。', 'Black-and-white pencil manga. ROUGH grey pencil lines with visible granular gaps, NOT clean black ink lines. Halftone only TWO small patches. ONE distant setting outline on WHITE paper. No smooth rendered shading on faces or clothing.'),
    'cutout': ('白黒の切り絵漫画。すべての黒は細い黒い橋でつながった一枚の形。顔そのものも黒い一枚の形、目と口は白い穴。白い顔に黒い目を置かない。植物・空も黒をつなぐか省く。孤立黒・描線・灰色・網点なし。', 'Black-and-white cut-paper manga. ALL black areas form ONE UNBROKEN black cutout joined by visible black bridges. Faces themselves are SOLID BLACK with WHITE eye and mouth HOLES. NEVER black eyes on white faces. Connect EVERY plant and sky element, or OMIT it. No isolated black marks, drawn lines, grey or halftone.'),
    'silhouette': ('白黒の影絵漫画。人物・服・小物は内部に線も白もない純黒の形。背景は白い紙に簡単な形だけ。灰色・網点・顔の描き込みは使わない。', 'Black-and-white silhouette manga. Figures, clothes and props are pure BLACK shapes with NO internal lines or white marks. WHITE paper background, only simple shapes. No grey, halftone or facial details.'),
    'lineonly': ('白黒の線画漫画。髪・服・物・背景は細い均一な線だけ、内側は白い紙。ひびや破片も一本ずつの線。黒ベタ・網点・灰色・影は使わない。', 'Black-and-white line-art manga. Hair, clothes, props and scenery are thin uniform lines with WHITE interiors. Cracks and fragments are individual lines. No solid black, halftone, grey or shadows.'),
    'engraving': ('白黒の彫刻線の漫画。陰影は形に沿う離れた平行線と交差線の間隔だけ。髪や服の最暗部にも白い隙間を残す。黒ベタ・網点・塗り込みなし。背景は遠い小さな輪郭1個以外は白。', 'Black-and-white engraved manga. Shading ONLY by spacing of separated form-following parallel and crossing lines. WHITE gaps even in darkest hair and clothing. No solid black, halftone or filled rendering. Background ONE SMALL distant contour only, otherwise WHITE paper.'),
    'ink': ('白黒の筆の漫画。太細の揺れ、かすれと縁のにじみを残す。黒は縁のにじむ筆面、白は紙。背景はかすれた筆線1本のみ、庭・家具・建物を描かない。網点・清書線なし。', 'Black-and-white brush manga. Preserve varying thickness, broken strokes and bleeding edges. Black is bleeding brushed ink, white is paper. Background ONLY ONE broken brush stroke, NO garden, furniture or architecture. No halftone or polished linework.'),
    'inkbleed': ('白黒のにじみ墨の漫画。輪郭はにじんで揺れる線、黒はむらのある墨だまり、灰は縁のにじんだ墨のしみ。網点・清書線なし。棚・本・建物を消し、背景は白い紙に墨形1個のみ。', 'Black-and-white bleeding-ink manga. Uneven bleeding contours, pooled black ink, grey as ink stains with bleeding edges. No halftone or polished lines. DELETE shelves, books and architecture; background ONLY ONE uneven ink shape on WHITE paper.'),
    'yamato': ('白黒の大和絵漫画。顔を下ぶくれに置換。目は瞳のない短い横線2本、鼻は短い折れ線、口は小さい線。細い均一な輪郭と白い衣服。鎧の陰影も消す。背景は遠い城の輪郭1個のみ。髪以外のベタ・網点・立体陰影なし。', 'Black-and-white Yamato-e manga. REPLACE the face with LOWER WIDE cheeks, TWO narrow horizontal eye DASHES without pupils, ONE short angular bent-line nose and TINY mouth. THIN uniform contours and WHITE clothing interiors. DELETE armor shading. ONE distant castle outline only. No blacks outside hair, no halftone or volumetric shading.'),
    'ukiyoe': ('白黒の浮世絵漫画。細い均一な線、黒・灰・白の平らな面、顔は細い吊り目と長い鼻。顔と首は白。陰影と光沢を付けず、背景を簡単な形に省く。', 'Black-and-white ukiyo-e manga. Thin uniform lines, FLAT black, grey and white areas; narrow upturned eyes, long nose. WHITE faces and necks. No shading or gloss. Simple setting shapes.'),
    'points': ('白黒の点輪郭漫画。輪郭は離れた黒点の列、内側は白い紙。影は少数の小さな点の塊だけ。髪・服・小物に密点面や網点やベタを作らない。', 'Black-and-white dotted-contour manga. Separate black dots along contours, WHITE interiors. Shadows only FEW small dot clusters. NO dense dotted fills, halftone or solid blacks in hair, clothes or props.'),
    'ligne': ('白黒のくっきり線の漫画。太さ一定の輪郭、写実的な目を小さい点2個に置換し鼻は短線。人物は白、背景は影なしの線だけ。網点・灰色・立体陰影を使わない。', 'Black-and-white clear-line manga. Uniform contours, REPLACE realistic eyes with TWO tiny DOTS and a short nose. WHITE figure interiors, background ONLY unshaded lines. No halftone, grey or volumetric shading.'),
    'gag': ('白黒のギャグ漫画。太く丸い少数の線、大きい輝く目を白光のない小さい黒点2個に置換。大きな単純口。髪は黒い塊、服は輪郭としわ2本だけ。白を広く残し、細密線と塗り込む陰影を使わない。', 'Black-and-white gag manga. FEW thick ROUND lines, REPLACE large shining eyes with TWO TINY BLACK DOTS, no eye whites or highlights. LARGE simple mouth. Hair black masses, clothes contours and TWO folds. Broad WHITE paper, no fine details or rendered shading.'),
    'essay': ('白黒の日記漫画。少ない揺れる細線、精密な目を黒点2個へ置換。白光・まつげ・鼻なし。服は輪郭としわ2本、飾りも単純な形。白を広く残し、網点と背景は少量。細密な清書と立体塗りはしない。', 'Black-and-white diary manga. FEW thin wavering lines, REPLACE detailed eyes with TWO tiny black dots, NO eye highlights, lashes or nose. Clothes contours and TWO folds; ornaments simple shapes. Broad WHITE paper, LITTLE flat tone and scenery. No polished detail or volumetric rendering.'),
    'childhorror': ('白黒の児童向け怪談漫画。太く丸い少数の線、丸い顔と大きい丸目。服は白い紙、背景は簡単な形と明るい平らなトーン。細密線やぼかしは使わない。', 'Black-and-white child ghost-story manga. FEW thick ROUND lines, ROUND faces and LARGE ROUND eyes. WHITE clothing, simple scenery and LIGHT flat tone. No fine details or blur.'),
    'romance': ('白黒のラブロマンス漫画。若い丸顔と小さい顎、両瞳それぞれに離れた白丸3個、左上・右上・右下。髪は単純な房、服は少数の線。白い紙と平らな網点で描き、ぼかしや立体塗りを使わない。', 'Black-and-white romance manga. Young ROUND faces, SMALL chins, LARGE eyes with EXACTLY THREE separate WHITE CIRCLES in EACH iris: upper-left, upper-right, lower-right. Simple hair locks and FEW clothing lines. WHITE paper and FLAT halftone, no blur or volumetric rendering.'),
    'drama': ('白黒のヒューマンドラマ漫画。小さい目と短い鼻と口、髪は平らな灰色の面。服も店内も少数の輪郭だけ。白を広く残し、細密線と立体陰影を使わない。', 'Black-and-white human-drama manga. Small eyes, short noses and mouths; hair ONE FLAT GREY area. Clothes and interiors use FEW contours. Broad WHITE paper, no fine detail or volumetric shading.'),
    'flattown': ('白黒の平らな漫画。太さ一定の輪郭、黒・灰・白の平らな面。柱や衣服にも光沢や影を付けない。夜空は黒に白い星。灰色は平らな網点だけ。', 'Flat black-and-white manga. Uniform contours, FLAT black, grey and white areas. NO gloss or shading on columns or clothing. BLACK night sky with WHITE stars. Grey ONLY flat halftone.'),
}

TARGETS = {
    'shonen-sports-muscle-mass': 'engraving', 'shonen-carved-engraving': 'engraving',
    'josei-office-doodle-casual': 'doodle', 'josei-office-natural-quiet': 'white',
    'josei-office-pencil-soft': 'pencil', 'josei-family-doodle-casual': 'doodle',
    'josei-love': 'romance', 'josei-love-modern-flat': 'flatmodern', 'josei-love-rough-light': 'rough',
    'josei-drama': 'drama', 'josei-drama-ink-bleed': 'inkbleed',
    'josei-period-ukiyoe-flat': 'ukiyoe', 'josei-period-kirie': 'cutout',
    'josei-period-inkwash-quiet': 'ink', 'josei-comedy-doodle-casual': 'doodle',
    'kodomo-animal-kirie': 'cutout', 'gag': 'gag', 'gag-surreal-dot-contours': 'points',
    'gag-deadpan-modern-town': 'flattown', 'horror-kaidan': 'flatkaidan',
    'horror-folk-kirie': 'cutout', 'horror-school': 'childhorror',
    'horror-urban-kagee': 'silhouette', 'horror-panic-crack-debris': 'lineonly',
    'essay': 'essay', 'essay-diary-gentle-soft': 'flatdiary', 'essay-travel-kirie': 'cutout',
    'gekiga-historical-hikime-yamato': 'yamato', 'gekiga-adventure-ligne-claire': 'ligne',
}


def apply_repairs(tree):
    by = {n['id']: n for n in tree['nodes']}
    if not set(TARGETS) <= set(by):
        raise ValueError('改修対象のIDが木にない')
    for name, (ja, en) in RECIPES.items():
        tree['media']['repair-' + name] = {
            'common': {'ja': ja, 'en': en, 'tags': 'monochrome, manga, ' + name},
            'retain_parent_look': True,
            'edit': {
                'ja': '指定の手描き漫画へ描き直す。元の目・髪細線・服の模様・陰影・細密背景をすべて消す。人物・しぐさ・表情だけを保ち、背景は仕上げ指定の最少の形へ置換。絵柄: {look}。最終の描法: ' + ja + '文字・フキダシ・コマ枠・署名・透かし・色なし。',
                'en': 'Convert this scene to the specified hand-drawn manga. DELETE the original eyes, all hair strands, clothing patterns, shading and detailed scenery. Keep only character identity, gesture and expression. REPLACE scenery with the minimum shapes required by the FINISHED style. Style: {look}. FINAL drawing method: ' + en + ' No text, balloons, borders, signatures, watermarks or color.',
            },
        }
    for nid, name in TARGETS.items():
        n = by[nid]
        n['medium'] = 'repair-' + name
        if n['level'] == 3 and name in ('cutout', 'engraving', 'ink', 'inkbleed', 'yamato', 'ukiyoe'):
            n['words'] = dict(n['words'])
            n['words']['ja'] = n['words']['ja'].replace('人物の後ろは白か平らなトーン1枚。場所は遠くの簡単な形だけ', '人物の後ろは白。場所は遠くの簡単な形だけ')
            n['words']['en'] = n['words']['en'].replace('behind the figure plain white or one flat tone; the place shown only as distant simple shapes', 'behind the figure WHITE; the place only distant simple shapes')
    return tree
