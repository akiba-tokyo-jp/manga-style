"""本文絵柄の調査から、既存の平面彩色を成人の土台へ展開する。"""
from copy import deepcopy

PARENTS=('josei-office','josei-comedy','seinen-profession')
NEW_IDS=frozenset(parent+'-flat-color' for parent in PARENTS)


def apply_additions(tree,make_node,arch_words):
    tree=deepcopy(tree)
    base=next(n for n in tree['nodes'] if n['id']=='essay-parenting-flat-color')
    for parent in PARENTS:
        words=arch_words('flat-color')
        replacements={
            'ja':('背景も白地と少数の色面、ぼかさない','背景も明瞭な色面、ぼかさない'),
            'en':('background in white space and a few unblurred colored shapes','background in clear colored shapes without blur'),
        }
        for lang,(old,new) in replacements.items():
            assert words[lang].count(old)==1 and len(new)<=len(old)
            words[lang]=words[lang].replace(old,new)
        leaf=make_node(parent+'-flat-color',parent,3,base['title'],base['summary'],words)
        leaf['medium']=base['medium']
        tree['nodes'].append(leaf)
    return tree
