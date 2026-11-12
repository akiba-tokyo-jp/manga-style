"""絵本本文を調査した素材描法。人物土台を共有する5つのL3だけを追加する。"""
from copy import deepcopy
from styles import ARCH, ITEMS, ORDER

# 親は既存土台。素材だけを増やし、図形・点目・丸体などを新L2に数えない。
PLACEMENTS = {'paper-collage': 'kodomo-geometric', 'color-crayon': 'gag-hetauma',
              'color-wash': 'seinen-penscape', 'textile-relief': 'kodomo-animal',
              'clay-relief': 'yonkoma-mochi'}
TITLES = {
    'paper-collage': ('多色色紙の重なり', 'Colored-paper layers'),
    'color-crayon': ('色クレヨンの擦れ', 'Grainy color crayon'),
    'color-wash': ('色線と透明な淡彩', 'Dry colored lines and light washes'),
    'textile-relief': ('布と刺繍の浅いレリーフ', 'Fabric and stitched shallow relief'),
    'clay-relief': ('色粘土の浅いレリーフ', 'Colored-clay shallow relief'),
}
METHODS = {
    'paper-collage': (('紙片の切断縁で形を作る', 'form shapes with cut-paper edges'),
                      ('多色の紙片に刷毛むらと薄い重なり', 'multicolor paper pieces with brush marks and thin overlaps'),
                      ('背景も重ねた色紙の簡単な形', 'background in simple layered paper shapes')),
    'color-crayon': (('粒のある太い色線で輪郭を描く', 'outline with thick grainy colored strokes'),
                     ('多色を擦り重ね、紙目の白い抜けを残す', 'rub multiple colors in layers, leaving white paper grain'),
                     ('背景は擦れた色面と短い色線', 'background in rubbed color patches and short strokes')),
    'color-wash': (('乾いた細い褐色と灰緑の線', 'dry fine brown and grey-green lines'),
                   ('透明な淡色と少量の色線の重なり', 'transparent pale color washes and a few layered colored strokes'),
                   ('背景は細線と薄い色面で場所を示す', 'background places indicated by fine lines and pale color patches')),
    'textile-relief': (('布の裁ち端と糸の縫目で形を作る', 'define shapes with fabric edges and stitched thread'),
                      ('多色の布の織り目と刺繍、浅い厚みの影', 'multicolor fabric weave and embroidery with shadows from shallow thickness'),
                      ('背景も布片と糸で簡潔に組む', 'background assembled simply from cloth pieces and thread')),
    'clay-relief': (('色粘土の丸い盛り上がりの縁', 'rounded raised edges of colored clay'),
                   ('多色粘土の押し跡と延ばし筋、浅い重なり影', 'multicolor clay with press marks, spreading grooves and shallow overlap shadows'),
                   ('背景も薄い粘土の面で簡潔に組む', 'background assembled from simple thin clay layers')),
}
ARCH_EN = {k: (en, en + ' over the existing figure construction.') for k, (_, en) in TITLES.items()}
NEW_IDS = frozenset(parent + '-' + key for key, parent in PLACEMENTS.items())


def apply_additions(tree, make_node, arch_words):
    tree = deepcopy(tree)
    for key, parent in PLACEMENTS.items():
        title, _ = TITLES[key]
        line, tone, bg = METHODS[key]
        values = (line, tone,
                  ('土台の目鼻と顔形を保つ', 'preserve the base eye, nose and face shapes'),
                  ('土台の頭胴と四肢の比率を保つ', 'preserve base head, torso and limb proportions'),
                  bg, ('手作りの素朴で温かな空気', 'a warm handmade mood'))
        for item, (ja, en) in zip(ORDER, values):
            ITEMS[item][1][key] = (ja, ja, en, en, 1)
        ARCH[key] = (title, title + 'で人物と場所を仕上げる絵柄。', ' '.join([key] * len(ORDER)))
        medium_id = 'picturebook-' + key
        common = {
            'ja': 'カラーの手作り絵本の描法。' + line[0] + '。' + tone[0] + '。人物の形は土台に従い、素材の描き方だけを変える。網点なし。',
            'en': 'Color handmade picture-book rendering. ' + line[1] + '. ' + tone[1] + '. Keep base figure construction and change only the material rendering. No screentone.',
            'tags': 'color, picture book, ' + key,
        }
        tree['media'][medium_id] = {
            'common': common, 'expression': 'color', 'retain_parent_look': True,
            'edit': {
                'ja': '元の絵は人物・ポーズ・表情・構図・場所の手本として使う。人物の形を保ち、全体を指定の素材描法で描き直す。絵柄: {look}。最終の画材: ' + common['ja'] + '文字・フキダシ・コマ枠・署名・透かしなし。',
                'en': 'Use the reference for people, pose, expression, composition and setting. Preserve figure shapes and redraw the whole scene using the specified material. Style: {look}. FINAL medium: ' + common['en'] + ' No text, balloons, borders, signatures or watermarks.',
            },
        }
        leaf = make_node(parent + '-' + key, parent, 3, title, ARCH[key][1], arch_words(key))
        leaf['medium'] = medium_id
        tree['nodes'].append(leaf)
    return tree
