"""閲覧モデルと絵柄一覧。既存Storeの絵・生成文・版には書き込まない。"""
from __future__ import annotations

import re
from urllib.parse import urlencode

GPT = 'gpt-image'
ANIMA = 'anima-turbo'
MODEL_COOKIE = 'manga_model'
MODELS = {
    GPT: {'id': GPT, 'name': 'GPT Image', 'status': 'available'},
    ANIMA: {'id': ANIMA, 'name': 'Anima Turbo', 'status': 'preparing'},
}
PAGE_SIZE = 48

# 題材名ではなく、人物構築/時代的描法そのものを示す既存L2。元のIDは変えない。
LOOK_GROUPS = frozenset({
    'shonen-carved', 'shonen-linecarved', 'shojo-otome', 'shojo-starry', 'shojo-penonly',
    'seinen-warped', 'seinen-penscape', 'seinen-plainreal', 'seinen-clumsy', 'josei-tanbi',
    'kodomo-geometric', 'yonkoma-mochi', 'yonkoma-newspaper', 'gag-retro', 'gag-hetauma',
    'gag-grimy', 'gag-deadpan', 'gekiga-grotesque', 'gekiga-bearded', 'horror-shojo',
})

TEXT = {
    'ja': {
        'site_name': 'マンガ・アニメの絵柄見本帳', 'heading': '絵から、使いたい絵柄を。',
        'intro': '大分類からそのまま見本を一覧。気になる描き方を絞って、モデル別のプロンプトを持ち帰れます。',
        'model_label': '生成モデル', 'all': 'すべて', 'category': '大分類',
        'filter': '絞り込み', 'topic': '題材・雰囲気（任意）', 'line': '線の特徴',
        'proportion': '人物の比率', 'finish': '仕上げ', 'expression': '白黒・カラー',
        'apply': 'この条件で探す', 'clear': '条件をクリア', 'results': '{n}件の絵柄',
        'search': '絵柄・特徴を検索', 'placeholder': '絵柄名、特徴、id で検索',
        'none': '見つかりませんでした。条件を変えてお試しください。',
        'previous': '前へ', 'next': '次へ', 'page': '{page} / {pages}ページ',
        'empty_heading': 'Anima Turbo の見本を準備中です',
        'empty_text': 'ここに Anima Turbo 専用の絵柄・プロンプト・生成画像を追加していきます。まだ登録されていません。',
        'empty_note': 'GPT Image の見本や文を、このモデルのものとして表示することはありません。',
        'empty_prompt': '絵柄のプロンプト', 'empty_sample': 'モデル専用の見本',
        'registered': '登録待ち', 'basic': 'この大分類の基本の絵柄',
        'topic_basic': 'この分類自体の絵柄を見る', 'detail': '絵柄の詳細',
        'sample_copy': '実生成プロンプトをコピー', 'style_copy': '絵柄プロンプトをコピー',
        'model_prefix': 'モデル: {name}', 'model_note': 'モデル別の見本とプロンプトを表示しています。',
        'requested_version': '生成時のモデル指定', 'compare': 'モデルを並べて見る',
        'compare_note': '同じ絵柄を目指したモデル別の見本です。同条件の性能比較ではありません。',
        'back': '絵柄一覧へ', 'filter_note': '特徴はプロンプトの指定から分類しています。出力の適合を保証するものではありません。',
    },
    'en': {
        'site_name': 'Manga & Anime Style Book', 'heading': 'Find your next drawing style.',
        'intro': 'Browse examples directly by category, narrow the look, and take the prompt for your selected model.',
        'model_label': 'Image model', 'all': 'All', 'category': 'Category', 'filter': 'Filters',
        'topic': 'Subject / mood (optional)', 'line': 'Linework', 'proportion': 'Proportions',
        'finish': 'Rendering', 'expression': 'Monochrome / color', 'apply': 'Apply filters',
        'clear': 'Clear filters', 'results': '{n} styles', 'search': 'Search styles and features',
        'placeholder': 'Style, feature, or id', 'none': 'No matches. Try changing the filters.',
        'previous': 'Previous', 'next': 'Next', 'page': 'Page {page} of {pages}',
        'empty_heading': 'Anima Turbo examples are being prepared',
        'empty_text': 'Model-specific styles, prompts, and generated examples will be added here. None are registered yet.',
        'empty_note': 'GPT Image examples and prompts are never presented as Anima Turbo outputs.',
        'empty_prompt': 'Style prompt', 'empty_sample': 'Model-specific examples',
        'registered': 'Not yet registered', 'basic': 'The category’s base style',
        'topic_basic': 'View this category’s own style', 'detail': 'Style details',
        'sample_copy': 'Copy actual generation prompt', 'style_copy': 'Copy style prompt',
        'model_prefix': 'Model: {name}', 'model_note': 'Examples and prompts belong to the selected model.',
        'requested_version': 'Requested generation model', 'compare': 'View models side by side',
        'compare_note': 'Examples aim at the same look; this is not a controlled performance comparison.',
        'back': 'Back to styles', 'filter_note': 'Features describe the prompt instructions, not a guarantee that the output follows them.',
    },
}

FACETS = {
    'expression': [('mono', '白黒', 'Monochrome'), ('color', 'カラー', 'Color')],
    'line': [('thin', '細い線', 'Fine lines'), ('thick', '太い線', 'Thick lines'), ('rough', '荒い線', 'Rough lines')],
    'proportion': [('chibi', '低頭身', 'Chibi'), ('standard', '等身大', 'Standard'), ('realistic', '写実寄り', 'Realistic')],
    'finish': [('solid', '黒ベタ', 'Solid blacks'), ('tone', 'トーン', 'Screentone'), ('lineonly', '線画', 'Line art')],
}
# タグを全文の主張に昇格させず、既存の「指定の特徴」だけを検索する。
TERMS = {
    'line': {'thin': ('thin lines', 'fine line', 'delicate line', '細い線', '細く', '繊細'),
             'thick': ('thick line', 'bold line', 'heavy-pressure', '太い線', '太く'),
             'rough': ('rough', 'scratchy', 'wobbly', '荒い', '荒々', '震え')},
    'proportion': {'chibi': ('chibi', 'super-deformed', 'low head', '低頭身', '2頭身', '3頭身'),
                   'standard': ('standard proportion', 'about 7 heads', 'standard body', '等身大', '標準体'),
                   'realistic': ('realistic', 'true-to-life', '写実', '現実に近い')},
    'finish': {'solid': ('solid black', 'black fill', '黒ベタ'),
               'tone': ('screentone', 'halftone', '網点', 'トーン'),
               'lineonly': ('line art', 'line-only', 'pen-only', '線画', 'ペン線だけ')},
}


def select_model(query_value, cookie_value=None):
    """共有URLを優先。API呼出元はcookieを渡さずlegacy defaultを固定する。"""
    if query_value is not None:
        if query_value not in MODELS:
            raise ValueError('unknown model')
        return query_value
    return cookie_value if cookie_value in MODELS else GPT


def model_url(path, lang, genko=False, model=GPT, **extra):
    params = {'lang': lang, 'model': model, **extra}
    if genko:
        params['client'] = 'genko'
    return path + '?' + urlencode({k: v for k, v in params.items() if v not in (None, '')})


def features_match(prompt, values, expression):
    if values.get('expression') and values['expression'] != expression:
        return False
    tags = prompt.get('tags', '').casefold()
    # Native tags are authoritative for facets; Japanese words are a fallback only when tags are absent.
    text = tags or prompt.get('ja', '').casefold()
    if values.get('finish') == 'tone' and re.search(r'\b(?:no|without)\s+(?:screen|half)tones?\b|トーン(?:なし|無し)|トーンを使わ', text):
        return False
    return all(not values.get(name) or any(term in text for term in choices[values[name]])
               for name, choices in TERMS.items())


def catalogue_page(s, *, model, lang, root='', topic='', q='', page=1, facets=None):
    """題材は任意。既存IDの同名スタイルを統合せず、48枚ずつ返す。"""
    facets = facets or {}
    if root and (not s.visible(root) or s.base[root]['level'] != 1):
        raise ValueError('unknown category')
    if topic and (not s.visible(topic) or s.base[topic]['level'] != 2
                  or (root and s.chain(topic)[0] != root)):
        raise ValueError('unknown topic')
    for name, value in facets.items():
        if value and value not in {v[0] for v in FACETS[name]}:
            raise ValueError('unknown filter')
    visible = [nid for nid in s.order if s.visible(nid)]
    roots = [nid for nid in visible if s.base[nid]['level'] == 1]
    topics = [nid for nid in visible if s.base[nid]['level'] == 2 and
              nid not in LOOK_GROUPS and (not root or s.chain(nid)[0] == root)]
    if model != GPT:
        return {'ids': [], 'total': 0, 'page': 1, 'pages': 1, 'roots': roots, 'topics': topics}
    words = q.casefold().split()
    matches = []
    for nid in visible:
        n = s.base[nid]
        chain = s.chain(nid)
        if root and chain[0] != root:
            continue
        if topic and topic not in chain:
            continue
        # L2題材の基本見本は題材を選んだ時か明示検索時に直接選べる。通常一覧は見た目を優先。
        if n['level'] == 2 and nid not in LOOK_GROUPS and not topic and not q:
            continue
        prompt = s.style_prompt(nid)
        if words:
            hay = ' '.join([nid, *s.path_titles(nid, 'ja'), *s.path_titles(nid, 'en'),
                            s.shown(nid, 'summary', lang), prompt.get('tags', '')]).casefold()
            if not all(w in hay for w in words):
                continue
        if not features_match(prompt, facets, s.expression(nid)):
            continue
        matches.append(nid)
    pages = max(1, (len(matches) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page, pages))
    start = (page - 1) * PAGE_SIZE
    return {'ids': matches[start:start + PAGE_SIZE], 'total': len(matches), 'page': page,
            'pages': pages, 'roots': roots, 'topics': topics}
