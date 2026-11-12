"""Xの漫画本文調査から、人物構築を保つ平面彩色と単色インクを追加。"""
from copy import deepcopy
from styles import ARCH, ITEMS, ORDER

PLACEMENTS = {
    'flat-color': ('yonkoma-mochi', 'essay-parenting', 'kodomo-geometric', 'gag-retro'),
}
TITLES = {'flat-color': ('輪郭を保つ平面カラー', 'Base contours with flat colors')}
METHODS = {
    'flat-color': (
        ('土台の太さと強弱の輪郭線', 'contours with the base weight and pressure'),
        ('肌と服は均一な多色ベタ、影は少量の単純な色面', 'skin and clothes in uniform flat colors, with a few simple flat shadow shapes'),
        ('背景も白地と少数の色面、ぼかさない', 'background in white space and a few unblurred colored shapes'),
        ('軽快で簡潔な空気', 'a light, concise mood')),

}
ARCH_EN = {key: (en, en + ' over the existing figure construction.')
           for key, (_, en) in TITLES.items()}
NEW_IDS = frozenset(parent + '-' + key for key, parents in PLACEMENTS.items() for parent in parents)


def apply_additions(tree, make_node, arch_words):
    tree = deepcopy(tree)
    for key, parents in PLACEMENTS.items():
        title, _ = TITLES[key]
        line, tone, bg, mood = METHODS[key]
        values = (line, tone,
                  ('土台の目鼻と顔形を保つ', 'preserve the base eye, nose and face shapes'),
                  ('土台の頭胴と四肢の比率を保つ', 'preserve base head, torso and limb proportions'),
                  bg, mood)
        for item, (ja, en) in zip(ORDER, values):
            ITEMS[item][1][key] = (ja, ja, en, en, 1)
        ARCH[key] = (title, title + 'で人物と場所を仕上げる絵柄。', ' '.join([key] * len(ORDER)))
        medium_id = 'x100-' + key
        common = {'ja': 'カラー漫画の描法。' + line[0] + '。' + tone[0] + '。人物の形は土台に従い、彩色の描法だけを変える。',
                  'en': 'Color manga rendering. ' + line[1] + '. ' + tone[1] + '. Preserve base figure construction and change only the coloring method.',
                  'tags': 'color, manga, ' + key}
        tree['media'][medium_id] = {
            'common': common, 'expression': 'color', 'retain_parent_look': True,
            'edit': {'ja': '元の絵は人物・ポーズ・表情・構図・場所の手本として使う。人物の形を保ち、全体を指定の彩色描法で描き直す。絵柄: {look}。最終の画材: ' + common['ja'] + '文字・フキダシ・コマ枠・署名・透かしなし。',
                     'en': 'Use the reference for people, pose, expression, composition and setting. Preserve figure shapes and redraw the whole scene using the specified coloring. Style: {look}. FINAL medium: ' + common['en'] + ' No text, balloons, borders, signatures or watermarks.'}}
        for parent in parents:
            leaf = make_node(parent + '-' + key, parent, 3, title, ARCH[key][1], arch_words(key))
            leaf['medium'] = medium_id
            tree['nodes'].append(leaf)
    return tree
