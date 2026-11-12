#!/usr/bin/env python3
"""マンガの絵柄カタログ: ジャンルの木（段階 1）を組み立てて検査する。

  genres.py  1段目・2段目（言葉・見本用の服装と場所・3段目の候補）
  styles.py  3段目（6項目を決めた完成した絵柄）

出力:
  tree.json  木の JSON（利用者が決めた形 + scenes / character / l2_edit）
  tree.html  人が確認するための一覧

プロンプトの組み立て（2026-09-27 本人が 1段目・2段目を承認）:
  API の prompt   1段目 = 共通＋1段目の言葉。2段目から下 = 共通＋2段目以下の言葉（1段目の言葉は足さない。
                  2段目の言葉はそれだけで完結した絵柄で、1段目を足すと 1段目の顔に戻る）。
  見本の絵        1段目 = 共通＋1段目＋題材＋人物（CHARACTER）＋場所＋描かないもの（文字から 1 枚）。
                  2段目 = 2 枚で作る。1枚目: 共通＋1段目＋その 1段目の場面（l2_scene）＋描かないもの。
                          2枚目: 1枚目の絵を渡して L2_EDIT（2段目の言葉で描き直す）。
                  3段目 = 2 枚で作る（2026-09-27 本人の指示で、2段目の見本とは別の絵から作る）。
                          1枚目: 共通＋2段目＋その 2段目の場面（l3_scenes.L3_SCENES）＋描かないもの。
                          2枚目: 1枚目の絵を渡して L2_EDIT（{look} = 2段目。L3_LEAD 3段目）。

絵と言葉は必ず組で変える（2026-09-27 本人「プロンプトを更新する場合は、必ず絵も更新しなさい　これは絶対です」）:
  approved_samples.json は、枝ごとに見本の絵の sha256、その絵を作った言葉の sha256（prompt_sha256）、
  その絵を作ったときの API の prompt の sha256（style_prompt_sha256）を持つ。今の木から組み立てた言葉と
  どちらかでも食い違うと検査が落ちる。言葉を変えたら、その言葉で絵を作り直し、記録ごと入れ替える。
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from pathlib import Path

from genres import CHARACTER, L1
from l3_scenes import L3_LEAD, L3_SCENES
from styles import ARCH, FACE_VISIBLE, ITEMS, ORDER, STYLE_MEDIUM

OUT = Path(__file__).resolve().parent  # tree.json / tree.html (review outputs; not committed)
APPROVED = Path(__file__).resolve().parent / "approved_samples.json"  # 本人が承認した見本の記録（画像は volume）

COMMON = {
    # 画材の決まりだけ（白黒、描かない3択、網点、ぼかし禁止）。顔・目・髪・線は各段の言葉に書く。
    "ja": "モノクロの日本のマンガのコマ。白黒とグレーとスクリーントーンだけで描く。線は輪郭と要所だけに引き、描かずに表せる所は次の3つで表す: 影や暗い所はベタで塗る、中間の陰は平らな網点トーンを貼る、光の当たる所は白く残す。灰色はすべて網点で表し、なめらかなグレーやぼかしは使わない。デジタル絵画のような塗り（エアブラシのぼかし、光のにじみ）はしない。",
    "en": "Black-and-white Japanese manga panel, greyscale and screentone only. Ink only the contours and essential interior lines; wherever something can be shown without lines, use one of three means: fill shadows and dark areas with solid black ink, lay flat halftone screentone for mid-tones, and leave lit areas as plain white paper. Every grey must be a visible halftone dot pattern; no smooth grey gradients or soft blur anywhere. No digital-painting rendering: no airbrushed gradients, no glow, bloom or rim light.",
    "tags": "monochrome, greyscale, manga, screentone, halftone dots, spot blacks, white space",
}

SUBJECTS = {
    "upper_body": {
        "ja": "10代後半の人物の上半身と、周りの背景。少し驚いた表情（目をいつもより少し見開き、口を少し開ける）。正面からやや斜めを向く。",
        "en": "Upper body of a person in their late teens with the surrounding background visible. Slightly surprised expression: eyes opened a little wider than usual, mouth slightly open. Facing the viewer, turned slightly to one side.",
        "tags": "upper body, background, slightly surprised, three-quarter view",
    },
}

# 2段目の見本の 2枚目: 1枚目（その 1段目の場面）の絵を渡し、2段目の絵柄で一から描き直す。
# 「場面はそのまま、描き方だけ変える」と頼むと元の絵とほぼ同じになった（2026-09-27、少年の 10 枚で確認）。
L2_EDIT = {
    "ja": "この白黒マンガの絵は、場面の手本としてだけ使う: 同じ人物、同じポーズと表情、同じ構図、同じ場所。絵全体を、別の作者が描いたとひと目でわかる、はっきり違うマンガの絵柄で一から描き直す。線の質、目と顔の形、頭身、黒とトーンの量を、次の絵柄のとおりに変える。元の線、目、陰影をなぞったり残したりしない。新しい絵柄: {look}。白黒とグレーとスクリーントーンだけで描く: 影はベタ、中間の陰は平らな網点、光は白い紙。なめらかなグレー、エアブラシ、光のにじみは使わない。文字・数字・フキダシ・効果音の描き文字・コマ枠・署名・透かしを入れない。色は使わない。",
    "en": "Use this black-and-white manga picture only as a guide for the scene: the same character, the same pose and expression, the same composition and the same place. Redraw the whole picture from scratch in a clearly different manga drawing style, so that a reader sees at a glance that a different artist drew it: the line quality, the shape of the eyes and face, the body proportions and the amount of black and tone must change as described below. Do not trace or keep the original line work, eyes or shading. New drawing style: {look}. Black-and-white Japanese manga, greyscale and screentone only: shadows as solid black ink, mid-tones as flat halftone dots, lit areas as plain white paper; no smooth grey gradients, no airbrush, no glow. No text, no letters, no numbers, no speech balloons, no sound-effect lettering, no panel borders or frame lines, no signature, no watermark. No color at all.",
}
STEP_LABELS = {
    "ja": ("1枚目（元の場面）: ", "2枚目（1枚目の絵を元に描き直す）: "),
    "en": ("Step 1 (the scene picture): ", "Step 2 (redrawn from the step 1 picture): "),
}

AVOID = ["文字", "フキダシ", "効果音の描き文字", "コマ枠", "署名", "透かし", "色"]
AVOID_WORDS = {
    "ja": "文字・数字・フキダシ・効果音の描き文字・コマ枠・署名・透かしを入れない。色は使わず、白黒とグレーだけで描く。",
    "en": "No text, no letters, no numbers, no speech balloons, no sound-effect lettering, no panel borders or frame lines, no signature, no watermark. No color at all: strictly black, white and grey.",
}

# 新しく足した画材だけに適用する。既存の共通文と描き直し文はそのまま。
SPARSE = {
    "ja": "描き込みを極めて少なくする。顔は単純な目・小さな鼻・口だけで、顔に影や細線を足さない。髪は3個ほどの単純なまとまりにする。服は輪郭と2、3本のしわだけ、服の内側はほぼ白。影は全体の2割未満の小さな部分だけ。肌の細かな線、髪の一本一本、布の模様や織り目、ハッチングは描かない。小物も単純な形にする。背景は遠くの形を1個だけ示し、紙の大部分を完全な白で残す。",
    "en": "Make an extremely sparse drawing. Faces have only simple eyes, a small nose and a mouth, without facial shading or extra lines. Hair is about three simple masses. Clothing has only its contour and two or three folds, with almost entirely white interiors. Shadows occupy small patches covering less than a fifth of the picture. Omit skin texture, individual hair strands, fabric patterns or weave, and hatching. Simplify all props to basic shapes. Indicate only one distant background shape and leave most of the paper completely white.",
}
MEDIA = {
    "dots": {"common": {
        "ja": "モノクロの日本のマンガのコマ。顔・髪・体の輪郭を、離れた黒い点の列で作る。影は小さな点の塊だけにして、白を広く残す。連続した輪郭線、面を埋める細密な点描、規則的な網点、ぼかしは使わない。" + SPARSE["ja"],
        "en": "Black-and-white Japanese manga panel. Form face, hair and body contours with rows of separate black dots. Shade only a few small areas with clusters of dots, leaving broad white space. No continuous outlines, dense stippling across whole surfaces, regular halftone or blur. " + SPARSE["en"],
        "tags": "monochrome, manga, dotted contours, sparse dot clusters, white space",
    }},
    "graphite": {"common": {
        "ja": "モノクロの日本のマンガのコマ。要所だけを少ない鉛筆の線で描く。灰色は影の部分だけ、鉛筆の粒と擦れが見えるむらのある面で表す。白い紙を広く残す。網点トーン、エアブラシ、光のにじみは使わない。" + SPARSE["ja"],
        "en": "Black-and-white Japanese manga panel. Use few pencil lines at essential places. Grey belongs only in shadows, as uneven patches with visible pencil grain and rubbing. Leave broad white paper. No halftone screentone, airbrush or glow. " + SPARSE["en"],
        "tags": "monochrome, manga, pencil grain, rubbed graphite, sparse lines, white space",
    }},
}
MEDIA["toneshapes"] = {"common": {
    "ja": "モノクロの日本のマンガ。顔・髪・服・背景の外周の線を引かず、白・濃さ2種類の平らな網点・少量の黒の面の境で形を作る。目と口は小さな形だけ残す。髪や服を細線で埋めず、模様・ハッチング・ぼかしを使わない。背景は遠くの形1個だけにし、紙の大半は白い余白。",
    "en": "Monochrome Japanese manga. No outer contour lines on faces, hair, clothes or backgrounds. Define forms with boundaries between white, two densities of flat halftone and a little solid black. Keep eyes and mouths as tiny internal shapes. No fine interior lines in hair or clothes, patterns, hatching or blur. Only one distant background shape; most of the paper is blank white.",
    "tags": "monochrome, manga, no outlines, two-density halftone shapes, sparse detail, white space",
}}
for _medium in MEDIA.values():
    _medium["edit"] = {
        "ja": "非常に単純な手描きのマンガにする。写実的な描き込みや、細かくきらきらした目は使わない。元の絵から人物・ポーズ・表情・場所だけを取り出し、一から描き直す。元の顔・線・陰影・細部はすべて捨てる。絵柄: {look}。" + _medium["common"]["ja"]
              + "絵全体を紙の中央の3分の2の範囲に小さく収め、上下左右の端は広い白い余白にする。頭と手を余白の内側に全部収める。髪の内側に細線を足さず、服の影は襟や袖の奥の小さな部分だけにする。" + AVOID_WORDS["ja"],
        "en": "Draw very simple hand-drawn manga. No realistic rendering or detailed sparkling anime eyes. Take only the people, poses, expressions and setting from the reference and rebuild from scratch. Discard ALL original faces, lines, shading and detail. Drawing style: {look}. " + _medium["common"]["en"]
              + " Draw the entire scene SMALL within the central two thirds of the canvas, with wide blank white margins on ALL FOUR sides. Complete heads and hands must fit inside those margins. No fine interior marks in the hair. Clothing shadows belong only in tiny areas inside collars or sleeves. " + AVOID_WORDS["en"],
    }

# この2系統は元の普通の人体・小さな目に戻りやすいので、形を具体的に指定する。
MEDIA["flatbands"] = {"common": {
    "ja": "白黒の単純なマンガ。頭と手だけは普通の形。胴は薄い台形の板、腕は幅のある長い長方形の帯2枚を角で折りつなぐ。前腕は胴より長く、先に普通の手が付く。肩も平たい板にして、丸い腕・腹・筋肉の立体感を省く。細い硬い輪郭、少量の網点、顔は点の目。服のしわは2本まで、背景の形は1個だけ。大半は白い紙。",
    "en": "Very simple black-and-white manga. ONLY heads and hands retain ordinary shapes. The torso is a thin trapezoid PLATE. Each arm is TWO LONG, WIDE, FLAT RECTANGULAR STRIPS joined at sharp corners; each forearm is longer than the torso, ending in an ordinary hand. Shoulders are flat plates. No rounded arms, belly, muscles or cylindrical volume. Thin hard outlines, a little flat halftone, dot eyes, at most two clothing folds and one background shape. Mostly blank white paper.",
    "tags": "monochrome, manga, flat trapezoid torso, long wide strip arms, sharp corners, sparse outlines, white space",
}}
MEDIA["ringeyes"] = {"common": {
    "ja": "白黒の単純なマンガ。目を顔の上半分の大半を占めるほど大きくし、それぞれ白目の外形と内側の虹彩の輪を大きな楕円2個で描く。虹彩の輪は目の外形より少し小さく、内側は白いまま。瞳孔はごく小さな点1個。まつげ・光・虹彩の模様は描かない。髪は細線や白いつやの筋を足さず、3個ほどの単純な黒い形だけ。顔に影や細線を足さない。服の内側はほぼ白、しわは2本まで。背景は本棚の形1個だけ。大半は白い紙。",
    "en": "Very simple black-and-white manga. Enlarge the eyes to occupy MOST OF THE UPPER HALF OF THE FACE. Each eye has TWO LARGE OVALS: the white-eye outer outline and a separate inner IRIS RING only slightly smaller. The iris interior is EMPTY WHITE except ONE extremely tiny black pupil dot. No eyelashes, highlights or iris texture. Hair is ONLY about THREE SIMPLE SOLID BLACK MASSES, with NO interior strands or white highlight lines. No facial shading or extra facial marks. Clothing interiors are almost entirely WHITE with at most TWO fold lines; show the apron with only a pale flat halftone patch. Background is ONE simple shelf shape. Mostly blank white paper.",
    "tags": "monochrome, manga, oversized double-oval eyes, large empty white iris rings, tiny pupils, sparse lines, white space",
}}
for _key in ("flatbands", "ringeyes"):
    MEDIA[_key]["edit"] = {
        lang: ("元の絵から人物・ポーズ・場所だけを取り、顔と体の形を一から変えて描く。絵柄: {look}。" if lang == "ja" else
               "Use the reference ONLY for character identity, pose and setting. Rebuild faces and bodies from scratch with radically different shapes; discard the original anatomical proportions and eyes. Drawing style: {look}. ")
        + MEDIA[_key]["common"][lang]
        + ("頭と手をすべて入れ、四辺に広い白い余白を残す。" if lang == "ja" else " Keep complete heads and hands inside wide blank margins on all four sides. ")
        + AVOID_WORDS[lang] for lang in ("ja", "en")
    }
MEDIA["ringeyes"]["edit"]["ja"] += "絵全体は画面中央の幅・高さ6割の中に小さく収め、四辺に2割ずつ完全に白い余白を残す。頭頂も画面の上から2割以上下に置く。"
MEDIA["ringeyes"]["edit"]["en"] += " Draw the ENTIRE picture SMALL inside the central 60 percent of BOTH canvas width and height. Leave 20 percent of the canvas completely BLANK WHITE on EACH of all four sides. The top of the hair must start at least 20 percent below the top edge."

# 成果物に残してはいけない名前の簡易チェック（書く側で避けたうえでの二重チェック）
DENY = [
    "ジャンプ", "マガジン", "サンデー", "チャンピオン", "りぼん", "なかよし", "花とゆめ", "マーガレット",
    "コロコロ", "ボンボン", "きらら", "ガロ", "モーニング", "ヤンジャン", "ビッグコミック", "アフタヌーン",
    "ジブリ", "ディズニー", "Disney", "Ghibli", "Jump", "手塚", "鳥山", "尾田", "藤子", "石ノ森", "赤塚",
    "水木", "楳図", "永井", "大友", "三浦", "荒木", "冨樫", "さいとう", "池上", "小池", "高橋留美子",
    "萩尾", "竹宮", "池田理代子", "CLAMP", "伊藤潤二", "梶原", "井上雄彦", "ドラゴンボール",
    "ワンピース", "ONE PIECE", "NARUTO", "BLEACH", "ジョジョ", "北斗", "ガンダム", "エヴァ", "ポケモン",
    "ドラえもん", "アンパンマン", "サザエ", "鬼太郎", "ゲゲゲ", "ゴルゴ", "こち亀", "ベルサイユ", "ベルばら",
    "セーラー戦士", "美少女戦士", "クトゥルフ", "ラヴクラフト", "Lovecraft", "Cthulhu", "Tezuka", "Toriyama",
    "AKIRA", "攻殻", "寄生獣", "進撃", "鬼滅", "呪術", "銀魂", "よつばと", "けいおん", "あずまんが",
    "スラムダンク", "SLAM DUNK", "あしたのジョー", "キャプテン翼", "美味しんぼ", "孤独のグルメ",
    "in the style of", "風の絵柄で", "先生",
]

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_arch(key: str) -> dict:
    """ARCH の "線 トーン 目と顔 頭身 背景 雰囲気" を項目ごとの値にする。"""
    vals = ARCH[key][2].split()
    if len(vals) != len(ORDER):
        raise SystemExit(f"{key}: 6項目でない: {vals}")
    out = {}
    for item, v in zip(ORDER, vals):
        if v not in ITEMS[item][1]:
            raise SystemExit(f"{key}: {item} に {v} が無い")
        out[item] = v
    return out


def arch_words(key: str) -> dict:
    spec = parse_arch(key)
    ja, en, tags = [], [], []
    for item in ORDER:
        _, vja, ven, vtags, _ = ITEMS[item][1][spec[item]]
        ja.append(vja)
        en.append(ven)
        tags.append(vtags)
    return {"ja": "、".join(ja), "en": ", ".join(en), "tags": ", ".join(tags)}


def arch_detail(key: str) -> int:
    """描き込みの量（並べる順番に使う）。"""
    spec = parse_arch(key)
    return sum(ITEMS[item][1][spec[item]][4] for item in ORDER if item != "atmos")


def arch_items(key: str) -> dict:
    """項目ごとの短い名前（確認用）。"""
    spec = parse_arch(key)
    return {ITEMS[item][0]: ITEMS[item][1][spec[item]][0] for item in ORDER}


def node(nid, parent, level, title, summary, words):
    return {"id": nid, "parent": parent, "level": level, "title": title, "summary": summary, "words": words}


def build() -> dict:
    nodes, scenes = [], {}
    for l1 in L1:
        nodes.append(node(l1["key"], None, 1, l1["title"], l1["summary"], l1["words"]))
        sc = l1["scene"]
        scenes[l1["key"]] = {k: sc[k] for k in ("place", "l2_scene") if k in sc}
        for ch in l1["children"]:
            l2id = f"{l1['key']}-{ch['key']}"
            nodes.append(node(l2id, l1["key"], 2, ch["title"], ch["summary"], ch["words"]))
            for k in ch["remove"]:
                if k not in l1["base"]:
                    raise SystemExit(f"{l2id}: 除く {k} が 1段目の候補に無い")
            chosen = [k for k in l1["base"] if k not in ch["remove"]]
            for k in ch["add"]:
                if k in chosen:
                    raise SystemExit(f"{l2id}: 足す {k} は既にある")
                if k not in ARCH:
                    raise SystemExit(f"{l2id}: 足す {k} が styles.py に無い")
                chosen.append(k)
            # シンプル → 描き込みの順（同じなら元の順）
            chosen = sorted(chosen, key=lambda k: (arch_detail(k), l1["base"].index(k) if k in l1["base"] else 99))
            for k in chosen:
                title, summary, _ = ARCH[k]
                leaf = node(f"{l2id}-{k}", l2id, 3, title, summary, arch_words(k))
                if k in STYLE_MEDIUM:
                    leaf["medium"] = STYLE_MEDIUM[k]
                nodes.append(leaf)
    tree = {"version": 1, "common": COMMON, "subjects": SUBJECTS, "avoid": AVOID,
            "character": CHARACTER, "scenes": scenes, "l2_edit": L2_EDIT,
            "l3_scenes": L3_SCENES, "l3_lead": L3_LEAD, "media": dict(MEDIA), "nodes": nodes}
    from repairs import apply_repairs
    from ranking_additions import apply_additions
    from picturebook_additions import apply_additions as apply_picturebooks
    from x100_additions import apply_additions as apply_x100
    from fanza_additions import apply_additions as apply_fanza
    from commercial_additions import apply_additions as apply_commercial
    tree = apply_x100(apply_picturebooks(apply_additions(apply_repairs(tree), node, arch_words), node, arch_words), node, arch_words)
    return apply_commercial(apply_fanza(tree, node, arch_words), node, arch_words)


# ---------------------------------------------------------------------------
# プロンプトの組み立て（段階 2 の見本と API で使う）
# ---------------------------------------------------------------------------
def chain(tree: dict, node_id: str) -> list:
    by = {n["id"]: n for n in tree["nodes"]}
    out, cur = [], by[node_id]
    while cur is not None:
        out.append(cur)
        cur = by.get(cur["parent"]) if cur["parent"] else None
    return list(reversed(out))


def prompt_nodes(tree: dict, node_id: str) -> list:
    """API の prompt に入れる段。1段目はその言葉、2段目から下は 2段目以下の言葉（1段目は足さない）。"""
    ch = chain(tree, node_id)
    return ch if len(ch) == 1 else ch[1:]


def style_prompt(tree: dict, node_id: str) -> dict:
    """API の prompt: 共通の言葉＋その枝の段の言葉（題材・人物・場所は含めない）。

    3段目は、3段目の言葉の前に L3_LEAD（上と違う所はこちらに従う）を置く。見本の描き直しと同じ形で、
    2段目の言葉と食い違う所（ベタの量・頭身など）は 3段目の言葉が勝つ。
    """
    ns = prompt_nodes(tree, node_id)
    c = tree.get("media", {}).get(ns[-1].get("medium"), {}).get("common", tree["common"])
    lead = tree["l3_lead"] if ns[-1]["level"] == 3 else {"ja": "", "en": ""}
    return {
        "ja": " ".join([c["ja"]] + [n["words"]["ja"] + "。" for n in ns[:-1]] + [lead["ja"] + ns[-1]["words"]["ja"] + "。"]),
        "en": " ".join([c["en"]] + [n["words"]["en"] + "." for n in ns[:-1]] + [lead["en"] + ns[-1]["words"]["en"] + "."]),
        "tags": ", ".join([c["tags"]] + [n["words"]["tags"] for n in ns]),
    }


def scene_for(tree: dict, node_id: str) -> dict:
    """見本の場所と 2段目の場面は 1段目ごと。"""
    return tree["scenes"][chain(tree, node_id)[0]["id"]]


SUBJECT_USES = {"upper_body": ("person", "place")}


def sample_steps(tree: dict, node_id: str, subject: str = "upper_body") -> list[dict]:
    """見本の絵を作る言葉（1段目は 1 枚、2段目・3段目は 2 枚）。いつも今の言葉で組み立てる。"""
    ch = chain(tree, node_id)
    me = ch[-1]
    sc = scene_for(tree, node_id)
    words = me["words"]
    c = tree["common"]
    if me["level"] == 2:
        l1 = ch[0]["words"]
        edit = tree.get("media", {}).get(me.get("medium"), {}).get("edit", tree["l2_edit"])
        return [
            {"ja": " ".join([c["ja"], l1["ja"] + "。", sc["l2_scene"]["ja"], AVOID_WORDS["ja"]]),
             "en": " ".join([c["en"], l1["en"] + ".", sc["l2_scene"]["en"], AVOID_WORDS["en"]])},
            {lang: edit[lang].replace("{look}", words[lang]) for lang in ("ja", "en")},
        ]
    if me["level"] == 3:
        # 1枚目は 2段目の言葉で、2段目の見本とは別の場面から作る。
        l2 = ch[1]["words"]
        scene = tree["l3_scenes"][ch[1]["id"]]
        lead = tree["l3_lead"]
        look = {"ja": l2["ja"] + "。" + lead["ja"] + words["ja"], "en": l2["en"] + ". " + lead["en"] + words["en"]}
        edit = tree.get("media", {}).get(me.get("medium"), {}).get("edit", tree["l2_edit"])
        medium = tree.get("media", {}).get(me.get("medium"), {})
        if "medium" in me and not medium.get("retain_parent_look", False):
            look = words
        return [
            {"ja": " ".join([c["ja"], l2["ja"] + "。", scene["ja"], AVOID_WORDS["ja"]]),
             "en": " ".join([c["en"], l2["en"] + ".", scene["en"], AVOID_WORDS["en"]])},
            {lang: edit[lang].replace("{look}", look[lang]) for lang in ("ja", "en")},
        ]
    c = tree.get("media", {}).get(me.get("medium"), {}).get("common", c)
    sub = tree["subjects"][subject]
    uses = SUBJECT_USES[subject]
    style = [n["words"] for n in prompt_nodes(tree, node_id)]
    ja = [c["ja"]] + [w["ja"] + "。" for w in style] + ["題材: " + sub["ja"]]
    en = [c["en"]] + [w["en"] + "." for w in style] + ["Subject: " + sub["en"]]
    if "person" in uses:
        ja.append(f"人物: {tree['character']['ja']}")
        en.append(f"The person: {tree['character']['en']}.")
    if "place" in uses:
        ja.append(f"場所: {sc['place']['ja']}。")
        en.append(f"Setting: {sc['place']['en']}.")
    ja.append(AVOID_WORDS["ja"])
    en.append(AVOID_WORDS["en"])
    return [{"ja": " ".join(ja), "en": " ".join(en)}]


def join_steps(steps: list[dict]) -> dict:
    if len(steps) == 1:
        return dict(steps[0])
    return {lang: "\n\n".join(label + st[lang] for label, st in zip(STEP_LABELS[lang], steps)) for lang in ("ja", "en")}


def sample_prompt(tree: dict, node_id: str, subject: str = "upper_body") -> dict:
    """見本の絵の言葉（2段目は 2 枚分をラベル付きで 1 つにする）。"""
    return join_steps(sample_steps(tree, node_id, subject))


def prompt_digest(prompt: dict) -> str:
    return hashlib.sha256(json.dumps(prompt, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def approved_samples() -> dict:
    """見本の記録（id -> 画像の sha256・作成日時・モデルの版・見本の言葉と API の prompt の sha256）。"""
    return json.loads(APPROVED.read_text(encoding="utf-8"))["samples"]


# ---------------------------------------------------------------------------
# 検査
# ---------------------------------------------------------------------------
def check(tree: dict) -> list[str]:
    problems = []
    ids = {}
    for n in tree["nodes"]:
        if not ID_RE.match(n["id"]):
            problems.append(f"id の形が違う: {n['id']}")
        if n["id"] in ids:
            problems.append(f"id が重複: {n['id']}")
        ids[n["id"]] = n
        for k in ("ja", "en", "tags"):
            if not n["words"].get(k, "").strip():
                problems.append(f"{n['id']}: words.{k} が空")
    kids = {}
    for n in tree["nodes"]:
        kids.setdefault(n["parent"], []).append(n)
        if n["parent"] is not None and n["parent"] not in ids:
            problems.append(f"{n['id']}: 親が無い")
    if not (8 <= len(kids[None]) <= 12):
        problems.append(f"1段目の数 {len(kids[None])}")
    for a in kids[None]:
        l2 = kids.get(a["id"], [])
        # 2段目は 1段目ごとに約 10（初めの決まり）。調べて足した絵柄で 12 を超えたので、上限を 14 にした（2026-09-29）。
        if not (8 <= len(l2) <= 14):
            problems.append(f"{a['id']}: 2段目の数 {len(l2)}")
        for b in l2:
            l3 = kids.get(b["id"], [])
            # 色線淡彩の実見追加1枝に限り、既存25描法の親を26まで許す。
            limit = 26 if b['id'] == 'seinen-penscape' else 25
            if not (20 <= len(l3) <= limit):
                problems.append(f"{b['id']}: 3段目の数 {len(l3)}")
            if len({c["title"] for c in l3}) != len(l3):
                problems.append(f"{b['id']}: 3段目の表示名が重複")
            # 顔の一覧で見分けがつくか: 顔で見える4項目のうち2つ以上が違うこと
            keys = [c["id"][len(b["id"]) + 1:] for c in l3]
            specs = {k: parse_arch(k) for k in keys}
            for i, k1 in enumerate(keys):
                for k2 in keys[i + 1:]:
                    diff = sum(specs[k1][it] != specs[k2][it] for it in FACE_VISIBLE)
                    if diff < 2:
                        problems.append(f"{b['id']}: {k1} と {k2} は顔で見分けにくい（違い {diff}）")
    parts = [json.dumps(tree[k], ensure_ascii=False)
             for k in ("common", "subjects", "character", "scenes", "l2_edit", "l3_scenes", "l3_lead", "media")]
    parts.append(json.dumps(AVOID_WORDS, ensure_ascii=False))
    parts += [json.dumps({k: n[k] for k in ("title", "summary", "words")}, ensure_ascii=False) for n in tree["nodes"]]
    for key, sc in tree["scenes"].items():
        if "l2_scene" not in sc:
            problems.append(f"{key}: 2段目の見本の場面（l2_scene）が無い")
    l2_ids = {n["id"] for n in tree["nodes"] if n["level"] == 2}
    if set(tree["l3_scenes"]) != l2_ids:
        problems.append(f"3段目の見本の場面が 2段目と一致しない: 不足 {sorted(l2_ids - set(tree['l3_scenes']))[:5]} "
                        f"余分 {sorted(set(tree['l3_scenes']) - l2_ids)[:5]}")
    # 見本の記録: 全枝にあり、今の木から組み立てた「見本の言葉」と「API の prompt」が、その絵を作ったときと
    # 1 字違わず一致する。言葉だけ変えて絵を作り直さないと、ここで落ちる。
    approved = approved_samples()
    want = set(ids)
    if set(approved) != want:
        problems.append(f"承認済みの見本の枝が木と一致しない: 不足 {sorted(want - set(approved))[:5]} "
                        f"余分 {sorted(set(approved) - want)[:5]}")
    for nid, a in approved.items():
        if nid not in ids:
            continue
        if prompt_digest(sample_prompt(tree, nid)) != a["prompt_sha256"]:
            problems.append(f"{nid}: 見本の言葉が、見本の絵を作った言葉と食い違う（言葉を変えたら絵も作り直す）")
        if prompt_digest(style_prompt(tree, nid)) != a.get("style_prompt_sha256"):
            problems.append(f"{nid}: API の prompt が、見本の絵を作ったときと食い違う（言葉を変えたら絵も作り直す）")
    for part in parts:
        for d in DENY:
            if d in part:
                problems.append(f"名前らしき語 {d!r}: {part[:80]}")
        if any(q in part for q in "「」『』《》"):
            problems.append(f"かぎかっこ（作品名の疑い）: {part[:80]}")
    return problems


# ---------------------------------------------------------------------------
# 確認用の一覧
# ---------------------------------------------------------------------------
def render_html(tree: dict) -> str:
    kids = {}
    for n in tree["nodes"]:
        kids.setdefault(n["parent"], []).append(n)
    e = html.escape
    count = {lv: sum(1 for n in tree["nodes"] if n["level"] == lv) for lv in (1, 2, 3)}
    total = sum(count.values())
    ex_id = "shonen-battle-bold-black"
    ex = sample_prompt(tree, ex_id, "upper_body")
    out = [
        "<!doctype html><html lang='ja'><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width,initial-scale=1'>",
        "<title>絵柄カタログ ジャンルの木（確認用）</title>",
        "<style>body{font-family:system-ui,sans-serif;margin:1rem;line-height:1.55;max-width:64rem}"
        "details{margin:.3rem 0 .3rem .9rem}summary{cursor:pointer;padding:.15rem 0}"
        ".w{color:#555;font-size:.85rem}.id{color:#888;font-size:.78rem;font-family:monospace}"
        ".sc{color:#487;font-size:.85rem}h1{font-size:1.3rem}"
        "table{border-collapse:collapse;font-size:.82rem;margin:.3rem 0 .8rem}"
        "td,th{border:1px solid #ccc;padding:.2rem .4rem;vertical-align:top}th{background:#f3f3f3}"
        "pre{white-space:pre-wrap;background:#f4f4f4;padding:.6rem;font-size:.82rem}</style>",
        "<h1>絵柄カタログ ジャンルの木（段階 1・確認用・画像なし）</h1>",
        f"<p>1段目 {count[1]}・2段目 {count[2]}・3段目 {count[3]}（計 {total} 枝。見本は各 1 枚で {total} 枚）</p>",
        "<h2>決まりごと</h2><ul>",
        "<li>1段目の見本: 全ジャンル同じ人物・構図。場所だけジャンルに合わせる（緑の字）。</li>",
        f"<li>1段目の見本の人物: {e(tree['character']['ja'])}</li>",
        "<li>2段目の見本: 1段目ごとの元の場面の絵を、2段目の絵柄で描き直す。</li>",
        "<li>段の受け持ち: 1段目＝ジャンルの見た目、2段目＝細かいジャンルの見た目（それだけで完結。API では 1段目を足さない）、3段目＝6項目。</li>",
        "<li>3段目の見本: 2段目ごとの元の場面（2段目の見本とは別の絵）を、3段目の絵柄で描き直す。</li>",
        "<li>3段目は完成した絵柄。1つ選べば6項目が全部決まる。一覧はシンプル→描き込みの順。</li>",
        "<li>同じ2段目の中の3段目は、顔で見える4項目（線・ベタとトーン・目と顔・雰囲気）のうち2つ以上が違う。</li>",
        "</ul>",
        f"<h2>見本の言葉の例（{e(ex_id)} の見本）</h2><pre>{e(ex['ja'])}\n\n{e(ex['en'])}</pre>",
        "<h2>木</h2>",
    ]
    for a in kids[None]:
        sa = tree["scenes"][a["id"]]
        out.append(f"<details><summary><b>{e(a['title'])}</b> <span class='id'>{e(a['id'])}</span> — {e(a['summary'])}</summary>")
        out.append(f"<p class='w'>言葉: {e(a['words']['ja'])}</p><p class='sc'>見本の場所: {e(sa['place']['ja'])}</p>"
                   f"<p class='sc'>2段目の見本の元の場面: {e(sa['l2_scene']['ja'])}</p>")
        for b in kids.get(a["id"], []):
            l3 = kids.get(b["id"], [])
            out.append(f"<details><summary><b>{e(b['title'])}</b> <span class='id'>{e(b['id'])}</span> — {e(b['summary'])}（3段目 {len(l3)}）</summary>")
            out.append(f"<p class='w'>言葉: {e(b['words']['ja'])}</p>")
            out.append("<table><tr><th>#</th><th>表示名</th><th>線</th><th>ベタとトーン</th><th>目と顔</th><th>頭身</th><th>背景</th><th>雰囲気</th></tr>")
            for i, cnode in enumerate(l3, 1):
                k = cnode["id"][len(b["id"]) + 1:]
                it = arch_items(k)
                out.append(f"<tr><td>{i}</td><td><b>{e(cnode['title'])}</b><br><span class='id'>{e(cnode['id'])}</span></td>"
                           + "".join(f"<td>{e(it[ITEMS[x][0]])}</td>" for x in ORDER) + "</tr>")
            out.append("</table></details>")
        out.append("</details>")
    out.append("</html>")
    return "\n".join(out)


def main() -> int:
    tree = build()
    problems = check(tree)
    if problems:
        print(f"検査で問題 {len(problems)} 件:", *problems[:60], sep="\n  ")
        return 1
    (OUT / "tree.json").write_text(json.dumps(tree, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (OUT / "tree.html").write_text(render_html(tree), encoding="utf-8")
    lv = {k: sum(1 for n in tree["nodes"] if n["level"] == k) for k in (1, 2, 3)}
    print("OK", lv, "total", sum(lv.values()), "images", sum(lv.values()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
