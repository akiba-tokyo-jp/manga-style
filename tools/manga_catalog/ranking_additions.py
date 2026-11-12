"""人物土台を共有する、実生成で差が確認された彩色5枝だけを追加する。"""
from __future__ import annotations
from copy import deepcopy
from styles import ARCH, ITEMS, STYLE_MEDIUM

COLOR_PARENTS = ('josei-love', 'josei-romance', 'shonen-romcom', 'seinen-action')
ARCH_EN = {'color-gradation': ('Base contours with color shading', 'Preserved figures and contour weight with restrained color shading.'), 'spot-accent': ('Black and white with one accent', 'Preserved figures in black and white with one flat yellow-green accent.')}


def register_styles():
    ITEMS['line'][1]['parentline'] = ('土台の輪郭線', '土台の輪郭線の太さと強弱を保つ', 'retain base contour weight and pen pressure', 'preserved base contours', 1)
    ITEMS['tone'][1]['color'] = ('色の階調', '肌と衣服は控えめな色階調、影も彩色に合わせる', 'skin and clothes in restrained color gradation, coordinated shadows', 'color shading', 2)
    ITEMS['tone'][1]['spot'] = ('一点の差し色', '黒白と平らな網点に、黄緑一色の平らな差し色', 'black, white and flat halftone with one flat yellow-green accent color', 'single yellow-green accent', 1)
    ITEMS['eyes'][1]['parent'] = ('土台の目と顔', '土台の目・鼻・顎と首肩の形を保つ', 'preserve the base eye, nose, jaw, neck and shoulder shapes', 'preserved base face', 1)
    ITEMS['bg'][1]['colorplain'] = ('簡潔な色面の背景', '背景は色面と簡潔な線で描く', 'background in colored shapes and concise lines', 'simple colored background', 1)
    ITEMS['bg'][1]['spotplain'] = ('一色の背景面', '背景は白と黄緑の簡単な面だけ', 'background only simple white and yellow-green shapes', 'simple spot-color background', 0)
    ARCH['color-gradation'] = ('土台の線を保つカラー階調', '人物と輪郭線の土台を保ち、色階調で仕上げる絵柄。', 'parentline color parent normal colorplain quiet')
    ARCH['spot-accent'] = ('白黒と黄緑の差し色', '人物の土台を保ち、黒白と一色の面で仕上げる絵柄。', 'pen spot parent normal spotplain bright')
    STYLE_MEDIUM['color-gradation'] = 'ranking-color'
    STYLE_MEDIUM['spot-accent'] = 'ranking-spot'


def apply_additions(tree, make_node, arch_words):
    register_styles()
    tree = deepcopy(tree)
    for medium, expression, ja, en in [
        ('ranking-color', 'color', 'カラー漫画。土台の輪郭線を保ち、肌・髪・衣服を控えめな色面と階調で塗る。顔と骨格は保つ。人物と場所を自然な彩色で仕上げる。', 'Full-color manga. Keep base contour weight; color skin, hair and clothes with restrained shapes and shading. Preserve faces and bodies. Finish people and setting with natural coloring.'),
        ('ranking-spot', 'color', '黒白と平らな網点の漫画。黄緑の差し色を平らな面で置く。同系色の濃淡を許す。人物の土台を保ち、他色・ぼかし・発光なし。', 'Black, white and flat halftone manga with flat yellow-green accent shapes. Tints of the same accent are allowed. Keep base figures; no other colors, blur or glow.')
    ]:
        tree['media'][medium] = {
            'common': {'ja': ja, 'en': en, 'tags': 'manga, ' + expression}, 'expression': expression, 'retain_parent_look': True,
            'edit': {'ja': '元の絵は人物・ポーズ・表情・構図の手本として使う。顔・首肩の形を保ち、全体を指定の描法で描き直す。絵柄: {look}。最終の画材: ' + ja + '文字・フキダシ・コマ枠・署名・透かしなし。',
                     'en': 'Use the reference for people, pose, expression and composition. Preserve face, neck and shoulder shapes, and redraw the whole scene using the specified method. Style: {look}. FINAL medium: ' + en + ' No text, balloons, borders, signatures or watermarks.'}
        }
    for parent, key in [(p, 'color-gradation') for p in COLOR_PARENTS] + [('josei-yuri', 'spot-accent')]:
        title, summary, _ = ARCH[key]
        leaf = make_node(parent + '-' + key, parent, 3, title, summary, arch_words(key))
        leaf['medium'] = STYLE_MEDIUM[key]
        tree['nodes'].append(leaf)
    return tree
