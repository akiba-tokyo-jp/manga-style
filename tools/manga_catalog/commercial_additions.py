"""商業本文の観察に基づく立体カラー。人物構築は既存L2を保つ。"""
from copy import deepcopy
from styles import ARCH,ITEMS,ORDER

PARENTS=('seinen-profession','seinen-plainreal')
KEY='volumetric-color'
MEDIUM='commercial-volumetric-color'
NEW_IDS=frozenset(p+'-'+KEY for p in PARENTS)
TITLE='輪郭を抑えた立体カラー'
SUMMARY='人物の形を保ち、材質ごとの連続した色の陰影で立体を描く。'
ARCH_EN={KEY:('Volumetric color with subdued outlines',
              'Preserve figure construction and show volume through continuous material-specific color shading.')}
VALUES=(
    ('墨の外輪郭を抑え、材質と明暗の境で形を作る',
     'suppress drawn ink outlines and define forms with material and lighting boundaries'),
    ('多色の連続した陰影で肌・髪・布を分け、光沢と接触影で丸みを示す',
     'use continuous full-color shading for skin, hair and cloth, with highlights and contact shadows for volume'),
    ('土台の目鼻と顔形を保ち、細部は少量の明暗で示す',
     'preserve base eye, nose and face shapes and indicate details with a few tonal cues'),
    ('土台の頭胴と四肢の比率を保つ',
     'preserve base head, torso and limb proportions'),
    ('背景も簡潔な立体色面と陰影で場所を示す',
     'show the setting with simple volumetric colored forms and shadows'),
    ('落ち着いた自然な立体感', 'calm natural depth'),
)


def apply_additions(tree,make_node,arch_words):
    tree=deepcopy(tree)
    for item,(ja,en) in zip(ORDER,VALUES):
        ITEMS[item][1][KEY]=(ja,ja,en,en,1)
    ARCH[KEY]=(TITLE,SUMMARY,' '.join([KEY]*len(ORDER)))
    common={
        'ja':'輪郭を抑えた立体カラーの漫画描法。人物の形は土台に従い、材質と連続した色の陰影で描く。網点より色の階調を主体にする。',
        'en':'Full-color volumetric manga rendering with subdued ink outlines. Preserve base figure construction and render materials with continuous color shading rather than screentone.',
        'tags':'color, volumetric shading, subdued outlines',
    }
    tree['media'][MEDIUM]={
        'common':common,'expression':'color','retain_parent_look':True,
        'edit':{
            'ja':'元の絵は人物・ポーズ・表情・構図・場所の手本として使う。人物の形を保ち、全体を指定の立体カラーで描き直す。絵柄: {look}。最終の描法: '+common['ja']+'文字・フキダシ・コマ枠・署名・透かしなし。',
            'en':'Use the reference for people, pose, expression, composition and setting. Preserve figure shapes and redraw the whole scene in the specified volumetric color. Style: {look}. FINAL rendering: '+common['en']+' No text, balloons, borders, signatures or watermarks.',
        },
    }
    for parent in PARENTS:
        leaf=make_node(parent+'-'+KEY,parent,3,TITLE,SUMMARY,arch_words(KEY))
        leaf['medium']=MEDIUM
        tree['nodes'].append(leaf)
    return tree
