"""3段目の見本の元の場面（2段目ごとに 1 枚）と、3段目の言葉の前に置く一文。

2026-09-27 本人の指示: 3段目の見本は 2段目の見本と別の絵から作る（「3段目は2段目と絵は変えるのですよね？」）。
バトルは学生にしない（「ヤンキーなどとも被るため学生からは遠ざけたバトルもの」）。元の場面は、そのジャンルの今の
人気作を調べて主役と舞台の型だけを取る（「今時のバトル漫画を調べて、それに沿った主役、舞台を元に絵を描きなさい」）。
作品名・人物名は入れない。

見本の作り方（build_tree.sample_steps）:
  1枚目 = 共通 + 2段目の言葉 + この場面 + 描かないもの（文字から 1 枚）。
  2枚目 = 1枚目の絵を渡し、L2_EDIT の {look} に「2段目の言葉。L3_LEAD 3段目の言葉」を入れて描き直す。
"""

L3_LEAD = {"ja": "仕上げの絵柄（上と違う所はこちらに従う）: ", "en": "Finished style (where it differs from the above, follow this): "}

L3_SCENES = {
    "shonen-battle": {
        "ja": "題材: 20歳くらいの青年の腰から上を縦長の構図で、周りの背景とともに。怪物を狩る仕事をしている。頭全体と刀の刃先まで画面に収まる。少し長めの黒髪が無造作に額にかかる。白いシャツ、細い黒のネクタイ、黒いスーツの上着。両手で刀の柄を胸の前で握り、刃を顔の横に斜め上へ立てて構える。刃は顔にかからない。静かな無表情で、鋭い目で正面を見据え、口は閉じる。正面からやや斜めを向く。 場所: 夜の都会のビルの谷間。背後にビルより大きな怪物の影を黒ベタで塗り、白く抜いた目を数個。ビルは定規の線の簡単な形で、窓や看板を1つずつ描かない。",
        "en": "Subject: A young man of about 20 who hunts monsters for a living, seen from the waist up in a tall vertical composition, his whole head and the tip of his sword inside the picture, the surrounding background visible. Slightly long, messy black hair falling over his forehead. A white shirt, a thin black tie and a black suit jacket. He grips the hilt of a katana with both hands in front of his chest, the blade raised diagonally upward beside his face without covering it. A calm, expressionless face, sharp eyes fixed straight ahead, mouth closed. Facing the viewer, turned slightly to one side. Setting: a city street between tall buildings at night: behind him a monster larger than the buildings, drawn as a solid black silhouette with a few white eyes cut out; buildings as simple ruled shapes, windows and signboards not drawn one by one.",
    },
    "shonen-sports": {
        "ja": "題材: 17歳くらいの少年のサッカーのストライカーの腰から上を縦長の構図で、周りの背景とともに。頭全体と両腕とボールが画面に収まる。汗で額に張りつく短い髪、番号も文字もない体にぴったりした練習着。胸でボールを受けた直後で、ボールが胸の前に浮かび、両腕を大きく広げて体を支える。目を見開き、不敵に笑う。正面からやや斜めを向く。 場所: 夜の屋内練習場。人工芝は平らなトーン、ゴールのネットは細い線を数本、天井の照明は白い四角。",
        "en": "Subject: A 17-year-old boy soccer striker seen from the waist up in a tall vertical composition, his whole head, both arms and the ball inside the picture, the surrounding background visible. Short hair damp with sweat and sticking to his forehead, a tight plain training shirt with no numbers or letters. He has just trapped the ball on his chest; the ball floats in front of his chest, his arms spread wide for balance. Wide-open eyes and a daring, hungry grin. Facing the viewer, turned slightly to one side. Setting: an indoor training pitch at night: artificial turf as flat tone, a goal net as a few thin lines, the ceiling lights as white rectangles.",
    },
    "shonen-romcom": {
        "ja": "題材: おだやかで品のある17歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。長いまっすぐな黒髪、きちんとした丸襟の制服。ケーキ屋のカウンター越しに、小さなケーキの箱を両手で大事そうに持ち、目を細めて正面へやわらかくほほえむ。正面からやや斜めを向く。 場所: 放課後の小さなケーキ屋の店内。ガラスのショーケースのケーキは簡単な丸い形、カウンター、棚の品物は1つずつ描かない。",
        "en": "Subject: A gentle, graceful 17-year-old girl seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long straight black hair, a neat school uniform with a round collar. Across the counter of a cake shop she holds a small cake box carefully in both hands and smiles softly toward the viewer, her eyes narrowed. Facing the viewer, turned slightly to one side. Setting: inside a small cake shop after school: a glass showcase with cakes as simple rounded shapes, a counter, shelves not drawn item by item.",
    },
    "shonen-fantasy": {
        "ja": "題材: 16歳くらいの少年の魔法使い見習いの腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と魔法陣全体が画面に収まる。無造作な短い黒髪、簡素な上着に革のベルト、フード付きの旅のマント。片手を前に突き出し、手のひらの前に円い魔法陣が白い細い線で浮かぶ。もう片方の手に飾りのない木の杖。落ち着いて集中した目で正面を見据える。正面からやや斜めを向く。 場所: 草原の丘。城壁のある町と遠くの山は平らな灰色の影、草は平らなトーンで1本ずつ描かない。",
        "en": "Subject: A 16-year-old boy apprentice mage seen from the waist up in a tall vertical composition, his whole head, both hands and the whole magic circle inside the picture, the surrounding background visible. Short messy black hair, a hooded traveling cloak over a simple tunic with a leather belt. He thrusts one open hand forward; a round magic circle hangs in the air in front of his palm, drawn as thin white lines; his other hand holds a plain wooden staff. A calm, focused look straight ahead. Facing the viewer, turned slightly to one side. Setting: a grassy hill: a walled town and distant mountains as flat grey silhouettes, grass as flat tone, not drawn blade by blade.",
    },
    "shonen-mystery": {
        "ja": "題材: 20歳くらいの大学生の青年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。大きくふくらんだ細かい巻き毛、無地のタートルネックに前を開けた上着。2本の指をあごに当て、横にいる相手をじっと見つめて考え込む。口は閉じる。正面からやや斜めを向く。 場所: 古い洋館の書斎。背が無地の本の並ぶ高い本棚、倒れたティーカップのある机、白いカーテンの窓。",
        "en": "Subject: A 20-year-old university student seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A big mop of tight curly hair, a plain turtleneck sweater under an open jacket. He rests two fingers against his chin and stares steadily at someone off to one side, thinking hard, lips closed. Facing the viewer, turned slightly to one side. Setting: the study of an old Western-style mansion: tall bookshelves with plain spines, a desk with a tipped-over teacup, a window with white curtains.",
    },
    "shonen-scifi": {
        "ja": "題材: 18歳くらいの少年のパイロットの腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とヘルメットが画面に収まる。短い髪、肩と胸に硬い装甲板の付いた、体にぴったりしたパイロットスーツ（マークなし）。ヘルメットを片腕に抱え、もう片方の手を小さく上げて、自信のある笑顔。正面からやや斜めを向く。 場所: 巨大な格納庫。背後に立つロボットの脚と大きな手を定規の線と平らなトーンで。通路とケーブルは簡単な線。",
        "en": "Subject: An 18-year-old boy pilot seen from the waist up in a tall vertical composition, his whole head, both hands and the helmet inside the picture, the surrounding background visible. Short hair, a fitted pilot suit with hard armor plates on the shoulders and chest and no markings. He holds his helmet under one arm and raises the other hand in a small wave, a confident smile. Facing the viewer, turned slightly to one side. Setting: a huge hangar: behind him the lower leg and giant hand of a standing robot, drawn with ruled lines and flat tone; catwalks and cables as simple lines.",
    },
    "shonen-adventure": {
        "ja": "題材: 15歳くらいの少年の冒険家の腰から上を縦長の構図で、周りの背景とともに。頭全体と両腕と指さす手が画面に収まる。無造作な短い髪、袖をまくった半袖のシャツ、首に結んだスカーフ、背中に大きなリュック。船の手すりにもたれ、片腕で遠くを指さして、口を大きく開けて笑う。正面からやや斜めを向く。 場所: 帆船の甲板。帆とロープは簡単な線、海は平らなトーン、水平線に小さな島。",
        "en": "Subject: A 15-year-old boy adventurer seen from the waist up in a tall vertical composition, his whole head, both arms and his pointing hand inside the picture, the surrounding background visible. Messy short hair, a short-sleeved shirt with the sleeves rolled up, a scarf tied around his neck, a big backpack on his back. He leans on the ship's railing and points far ahead with one arm, laughing with his mouth wide open. Facing the viewer, turned slightly to one side. Setting: the deck of a sailing ship: sails and ropes as simple lines, the sea as flat tone, a small island on the horizon.",
    },
    "shonen-school": {
        "ja": "題材: 16歳くらいの少年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。やわらかいマッシュの髪、ネクタイをゆるめた白いシャツ、首に掛けたヘッドホン。屋上の柵に背をもたれ、片手に食べかけのパン、もう片方の手を軽く上げて、くつろいだ笑顔。正面からやや斜めを向く。 場所: 昼休みの学校の屋上。金網の柵は交差する線を数本、遠くの町の屋根は平らな影、空は白く残す。",
        "en": "Subject: A 16-year-old boy seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A soft mushroom haircut, a white shirt with a loosened necktie, headphones hanging around his neck. He leans back against the rooftop fence, a half-eaten bread roll in one hand, the other hand raised in a casual wave, a relaxed friendly grin. Facing the viewer, turned slightly to one side. Setting: the school rooftop at lunchtime: a chain-link fence as a few crossing lines, distant town roofs as flat silhouettes, the sky left white.",
    },
    "shonen-delinquent": {
        "ja": "題材: 17歳くらいの不良の少年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。後ろになでつけた脱色した髪（淡いトーン）、前を開けた丈の長い学生服、鼻すじに小さなばんそうこう。両手をポケットに入れ、あごを上げて相手を見下ろし、口の端を上げて不敵に笑う。正面からやや斜めを向く。 場所: 古い商店街のアーケード。閉まったシャッターは平らな灰色の板、屋根は定規の線、看板は文字のない白い四角。",
        "en": "Subject: A 17-year-old delinquent boy seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Bleached hair swept back, shown as pale tone, a long open school jacket, a small bandage across the bridge of his nose. Both hands in his pockets, chin raised, looking down at someone with one corner of his mouth lifted in a bold smirk. Facing the viewer, turned slightly to one side. Setting: an old shopping arcade: closed shop shutters as flat grey panels, the arcade roof as ruled lines, signboards as blank white rectangles.",
    },
    "shonen-period": {
        "ja": "題材: 16歳くらいの少年の忍びの腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と短い刀が画面に収まる。後ろで結んだ短い髪、首に長い布を巻き、黒っぽい軽い着物に手甲。低く身をかがめ、短い刀を逆手に胸の前で構え、もう片方の手を平らに前へ出し、鋭い目で横をうかがう。正面からやや斜めを向く。 場所: 竹林の小道。竹は平らな縦のトーンの帯、葉は1枚ずつ描かない、差し込む光は白い帯を数本。",
        "en": "Subject: A 16-year-old boy ninja seen from the waist up in a tall vertical composition, his whole head, both hands and the short blade inside the picture, the surrounding background visible. Short hair tied at the back, a long scarf-like cloth around his neck, a light dark-colored kimono with arm guards. He crouches low, holding a short blade in a reverse grip in front of his chest, the other hand held flat forward, sharp eyes glancing to the side. Facing the viewer, turned slightly to one side. Setting: a bamboo grove path: bamboo stalks as flat vertical tone bands, leaves not drawn one by one, a few thin rays of light as white bands.",
    },
    "shojo-school": {
        "ja": "題材: 背が高く中性的で端正な顔の16歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。耳の見えるショートカット、リボンタイのブレザーの制服。放課後の廊下の窓にもたれ、表紙が無地の本を胸に抱え、少し頬を赤らめて横目で見て、小さくはにかむ。正面からやや斜めを向く。 場所: 夕方の校舎の廊下。窓は白い四角、床に斜めの光の白い帯、ロッカーは定規の線。",
        "en": "Subject: A tall 16-year-old girl with a boyish, handsome face seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Short hair that shows her ears, a blazer school uniform with a ribbon tie. She leans against a window in the school corridor after class, a book with a plain cover held against her chest, glancing sideways with a faint blush and a small shy smile. Facing the viewer, turned slightly to one side. Setting: a school corridor at dusk: windows as white rectangles, slanting light as white bands on the floor, lockers as ruled lines.",
    },
    "shojo-romcom": {
        "ja": "題材: 18歳くらいの女子大生の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ヘアピンを留めたあごまでのボブ、大きめのパーカー。画面を自分に向けたスマホを両手で胸に抱え、顔を真っ赤にし、目をぐるぐるにして口をぱくぱくさせて慌てる。正面からやや斜めを向く。 場所: 夜の自分の部屋。ベッドとクッションとぬいぐるみは簡単な丸い形、窓は黒い四角。",
        "en": "Subject: An 18-year-old university girl seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A chin-length bob with a hair clip, an oversized hoodie. She clutches her phone to her chest with both hands, the screen turned toward her; her face is bright red, eyes spinning, mouth flapping in panic. Facing the viewer, turned slightly to one side. Setting: her bedroom at night: a bed with cushions and a plush toy as simple rounded shapes, a window as a dark rectangle.",
    },
    "shojo-fantasy": {
        "ja": "題材: 和風の幻想の世界の18歳くらいの娘の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。花の髪飾りを付けた長いまっすぐな黒髪を下ろし、白い着物に淡い柄の羽織。両手を胸の前で重ね、頬を赤らめて見上げる、期待とはにかみの表情。周りに白い炎の形の鬼火が数個、黒地に白く抜いて浮かぶ。正面からやや斜めを向く。 場所: 夜の古い屋敷の縁側。木の柱は平らなトーン、石灯籠、花の枝は平らな柄トーン。",
        "en": "Subject: An 18-year-old young woman in a Japanese-style fantasy seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long straight black hair worn down with a flower hair ornament, a white kimono with a pale patterned haori. Her hands rest one over the other at her chest; she looks up with flushed cheeks and a hopeful, shy expression. Around her float a few white flame-shaped spirit fires, drawn as white shapes on black. Facing the viewer, turned slightly to one side. Setting: the veranda of an old Japanese mansion at night: wooden pillars as flat tone, a stone lantern, a branch of blossoms as a flat pattern tone.",
    },
    "shojo-palace": {
        "ja": "題材: 東洋風の宮廷で侍女として働く17歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。簡素なかんざしで一つにまとめた髪、少しのそばかす、帯の広い長袖の宮廷の衣装。小さな薬草の束を顔の前にかかげ、目を細めて賢そうに見つめ、小さく笑う。正面からやや斜めを向く。 場所: 宮殿の回廊。朱塗りの柱は平らな濃いトーン、反った瓦屋根の端は定規の線、吊り灯籠は簡単な形。",
        "en": "Subject: A 17-year-old girl who serves as a maid in an Eastern-style imperial palace, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Hair tied up in a simple bun with a plain hairpin, a few freckles, a long-sleeved court dress with a wide sash. She holds up a small bundle of medicinal herbs to her face and examines it with narrowed, clever eyes and a small knowing smile. Facing the viewer, turned slightly to one side. Setting: a palace corridor: lacquered pillars as flat dark tone, a curved tiled roof edge as ruled lines, hanging lanterns as simple shapes.",
    },
    "shojo-magical": {
        "ja": "題材: 変身した直後の14歳くらいの魔法少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と杖が画面に収まる。大きなリボンの長いツインテール、ふくらんだ袖と胸の大きなリボンのフリルの多い変身衣装。ハートの飾りの付いた短い杖を掲げてウインクし、もう片方の手でピースサイン。正面からやや斜めを向く。 場所: 雲の上の空。雲は平らなトーンの形、大きな星形と小さな星はトーンから白く抜いた形。",
        "en": "Subject: A 14-year-old magical girl just after her transformation, seen from the waist up in a tall vertical composition, her whole head, both hands and the wand inside the picture, the surrounding background visible. Long twin tails with big ribbons, a frilly transformation dress with puffed sleeves and a large bow at the chest. She raises a short wand topped with a heart-shaped ornament and winks, the other hand making a V sign. Facing the viewer, turned slightly to one side. Setting: high in the sky above the clouds: clouds as flat tone shapes, a large star shape and a few small stars as white shapes cut out of the tone.",
    },
    "shojo-showbiz": {
        "ja": "題材: ステージで歌う16歳くらいのアイドルの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とマイクが画面に収まる。サイドテールの長い髪、リボンと短いケープのフリルのステージ衣装。マイクを口元に持ち、もう片方の手を客席へ伸ばし、片目を閉じて明るい笑顔で歌う。正面からやや斜めを向く。 場所: コンサートのステージ。スポットライトは上からの白い帯、下の客席は暗い塊にペンライトの白い点がたくさん。",
        "en": "Subject: A 16-year-old idol girl performing on stage, seen from the waist up in a tall vertical composition, her whole head, both hands and the microphone inside the picture, the surrounding background visible. Long hair in a side ponytail, a frilly stage costume with ribbons and a short cape. She holds a microphone near her mouth and stretches her other hand toward the audience, singing with a bright smile and one eye closed. Facing the viewer, turned slightly to one side. Setting: a concert stage: spotlights as white bands from above, the audience below as a dark mass with many white dots for penlights.",
    },
    "shojo-dance": {
        "ja": "題材: 氷の上を滑る13歳くらいの少女のフィギュアスケーターの腰から上を縦長の構図で、周りの背景とともに。頭全体と広げた両腕が画面に収まる。きちんとまとめたお団子の髪、透けるスカートのスケート衣装、小さな飾りは白い点。両腕を大きく優雅に広げ、背を少しそらし、明るく楽しそうな笑顔。正面からやや斜めを向く。 場所: スケートリンク。氷は白く残し細い傷の線を数本、フェンスはトーンの帯、観客席は遠くの平らな暗い形。",
        "en": "Subject: A 13-year-old girl figure skater gliding on the ice, seen from the waist up in a tall vertical composition, her whole head and both outstretched arms inside the picture, the surrounding background visible. Hair tied in a neat bun, a skating dress with a sheer skirt and small decorations drawn as white dots. Both arms spread wide and gracefully, her back slightly arched, a bright joyful smile. Facing the viewer, turned slightly to one side. Setting: an ice rink: the ice left white with a few thin scratch lines, the rink wall as a band of tone, the spectator stands as a distant flat dark shape.",
    },
    "shojo-suspense": {
        "ja": "題材: 16歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。長いまっすぐな髪、無地の白いドレス。息をひそめて扉の細いすき間から中をのぞき、片手を扉の端に、もう片方の手で古い鍵を胸に握る。目を見開いた緊張と疑いの表情。正面からやや斜めを向く。 場所: 夜の古い洋館の廊下。廊下は黒ベタ、扉のすき間から細い白い光の帯、壁紙は平らなトーン。",
        "en": "Subject: A 16-year-old girl seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long straight hair, a plain white dress. She peeks through a narrow gap of a door, holding her breath; one hand is on the door edge, the other clutches an old key against her chest; a tense, suspicious look with wide eyes. Facing the viewer, turned slightly to one side. Setting: a corridor of an old Western-style mansion at night: the corridor in solid black, a thin band of white light falling through the door gap, wallpaper as flat tone.",
    },
    "shojo-drama": {
        "ja": "題材: 65歳くらいの女性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とカメラが画面に収まる。短い白髪（淡いトーン）、ブラウスに編んだカーディガン、スカーフ。小さなビデオカメラを胸の高さに持ち、海の方を見つめて静かに決意のこもった笑み。風に髪がゆれる。正面からやや斜めを向く。 場所: 海辺の堤防。海は平らなトーン、水平線は1本の線、カモメは小さな白い形を数羽。",
        "en": "Subject: A woman of about 65 seen from the waist up in a tall vertical composition, her whole head, both hands and the camera inside the picture, the surrounding background visible. Short grey hair shown as pale tone, a knitted cardigan over a blouse, a scarf. She holds a small video camera at chest height and looks out toward the sea with a quiet, determined smile, the wind moving her hair. Facing the viewer, turned slightly to one side. Setting: a seawall by the sea: the sea as flat tone, the horizon as one line, a few seagulls as small white shapes.",
    },
    "shojo-scifi": {
        "ja": "題材: 宇宙飛行士を夢見る15歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とヘルメットが画面に収まる。短いポニーテール、文字のない丸いワッペンの付いた訓練用のつなぎ。宇宙服のヘルメットを両腕で胸に抱え、目を見開いて希望に満ちた顔で夜空を見上げ、口を少し開く。正面からやや斜めを向く。 場所: 夜の丘。空は黒ベタに星の白い点、遠くの発射台のロケットは簡単な白い影。",
        "en": "Subject: A 15-year-old girl who dreams of becoming an astronaut, seen from the waist up in a tall vertical composition, her whole head, both hands and the helmet inside the picture, the surrounding background visible. A short ponytail, a training jumpsuit with a plain round patch and no letters. She hugs a space helmet to her chest with both arms and looks up at the night sky with wide, hopeful eyes and parted lips. Facing the viewer, turned slightly to one side. Setting: a hill at night: the sky in solid black with stars as white dots, a distant rocket on a launch tower as a simple white silhouette.",
    },
    "seinen-action": {
        "ja": "題材: 普通の暮らしをしようとしている殺し屋の30歳くらいの男性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と拳銃が画面に収まる。短く刈った髪、無地のTシャツに前を開けた上着。拳銃を両手で下に向けて低く構え、落ち着いた無表情で横を見る。正面からやや斜めを向く。 場所: 昼の立体駐車場。コンクリートの柱と梁は定規の線、止まった車は簡単な平らな形、硬い斜めの影。",
        "en": "Subject: A man of about 30 who is a professional killer trying to live an ordinary life, seen from the waist up in a tall vertical composition, his whole head, both hands and the pistol inside the picture, the surrounding background visible. Close-cropped hair, a plain T-shirt under an unzipped casual jacket. He holds a pistol low with both hands, pointed at the ground, and glances sideways with a calm, blank face. Facing the viewer, turned slightly to one side. Setting: a multi-storey car park in the daytime: concrete pillars and ceiling beams as ruled lines, parked cars as simple flat shapes, hard diagonal shadows.",
    },
    "seinen-noir": {
        "ja": "題材: 裏社会の依頼を引き受ける40歳くらいの弁護士の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。少し白髪の混じったオールバック、薄いあごひげ、暗い色の三つ揃いのスーツ。机に着き、口の前で指を組み、冷たく読めない目で正面を見る。正面からやや斜めを向く。 場所: 夜の古い雑居ビルの小さな事務所。ブラインドから白い横縞の光が暗い部屋に差す、机のスタンド、書類は簡単な積み重ねの形。",
        "en": "Subject: A lawyer of about 40 who takes cases from the criminal underworld, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Slicked-back hair with a little grey, a thin beard, a dark three-piece suit. He sits at a desk with his fingers steepled in front of his mouth, looking straight ahead with cold, unreadable eyes. Facing the viewer, turned slightly to one side. Setting: a small office in a shabby building at night: window blinds throwing white horizontal stripes across the dark room, a desk lamp, files as plain stacked shapes.",
    },
    "seinen-scifi": {
        "ja": "題材: 崩れた世界を旅する20歳くらいの若い女性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い黒髪、額に上げたゴーグル、フード付きの上着、大きなリュック、胸にかかるライフルの肩ひも。片手で肩ひもを持ち、もう片方の手を目の上にかざし、落ち着いて警戒した顔で遠くを見る。正面からやや斜めを向く。 場所: 文明が滅んで長い時がたった都市の廃墟。崩れたビルは平らな灰色の形、ひび割れた道路の草は平らなトーンで1本ずつ描かない。",
        "en": "Subject: A young woman of about 20 traveling through a ruined world, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Short black hair, goggles pushed up on her forehead, a hooded jacket, a large backpack, the strap of a rifle across her chest. She holds the strap with one hand and shades her eyes with the other, looking far ahead with a calm, alert face. Facing the viewer, turned slightly to one side. Setting: a ruined city long after civilization collapsed: broken buildings as flat grey shapes, a cracked road with weeds shown as flat tone, not drawn blade by blade.",
    },
    "seinen-darkfantasy": {
        "ja": "題材: 30歳くらいの傭兵の剣士の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と剣の柄が画面に収まる。荒い短い黒髪、鼻すじを横切る傷、使い込んだ革の鎧にぼろぼろのマント。長い剣を肩にかつぎ片手で握り、疲れた険しい顔で正面をにらむ。正面からやや斜めを向く。 場所: 夕暮れの戦場。折れた槍と旗は黒い影、空は平らなトーン、カラスは小さな黒い形を数羽。",
        "en": "Subject: A mercenary swordsman of about 30 seen from the waist up in a tall vertical composition, his whole head, both hands and the sword hilt inside the picture, the surrounding background visible. Rough short black hair, a scar across the bridge of his nose, a tattered cloak over worn leather armor. A long sword rests on his shoulder, gripped by one hand; he glares straight ahead with a grim, weary face. Facing the viewer, turned slightly to one side. Setting: a battlefield at dusk: broken spears and flags as dark silhouettes, the sky as flat tone, a few crows as small black shapes.",
    },
    "seinen-war": {
        "ja": "題材: 古代中国の戦乱の世の20歳くらいの若い将軍の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と槍の柄が画面に収まる。結い上げた短い髪、肩当てのある札を重ねた鎧、短いマント。長い槍を体の前に斜めに握り、歯を食いしばって前をにらむ、闘志に満ちた顔。正面からやや斜めを向く。 場所: 広い平原の戦場。遠くの軍勢は平らな灰色の帯、旗は印のない無地、土ぼこりは平らなトーン。",
        "en": "Subject: A young general of about 20 in an ancient Chinese warring-states army, seen from the waist up in a tall vertical composition, his whole head, both hands and the spear shaft inside the picture, the surrounding background visible. Short hair tied up, layered lamellar armor with shoulder guards, a short cape. He grips a long spear held diagonally across his body and glares forward, teeth clenched, full of fighting spirit. Facing the viewer, turned slightly to one side. Setting: a vast plain battlefield: distant armies as flat grey bands, plain flags without symbols, dust as flat tone patches.",
    },
    "seinen-gambling": {
        "ja": "題材: 28歳くらいの勝負師の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とカードが画面に収まる。整えた髪、細いふちなし眼鏡、襟元をゆるめた暗い色の細身のスーツ。カードの台に着き、表が無地のトランプを2本の指にはさんで顔の横に掲げ、半分閉じた計算高い目で薄く笑う。正面からやや斜めを向く。 場所: 地下の賭場。台は平らなトーン、チップは無地の小さな円、奥は黒ベタ、吊りランプは白い円。",
        "en": "Subject: A gambler of about 28 seen from the waist up in a tall vertical composition, his whole head, both hands and the card inside the picture, the surrounding background visible. Neat hair, thin rimless glasses, a sharp dark suit with a loosened collar. Sitting at a card table, he holds up one playing card between two fingers beside his face, its face blank, and smiles thinly with half-closed, calculating eyes. Facing the viewer, turned slightly to one side. Setting: an underground gambling den: a card table as flat tone, chips as small plain discs, the room behind in solid black, one hanging lamp as a white circle.",
    },
    "seinen-gourmet": {
        "ja": "題材: 50歳くらいの男性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。整えた短い白髪まじりの髪、袖をまくったシャツにエプロン。家の台所のコンロの前で、小皿で汁の味見をして静かに満足そうに笑い、片手はお玉を鍋の上に持つ。湯気は白い曲線を数本。正面からやや斜めを向く。 場所: 片付いた家の台所。鍋と棚は簡単な形、タイルは1枚ずつ描かない。",
        "en": "Subject: A man of about 50 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Neat short grey hair, an apron over a button-up shirt with the sleeves rolled up. Standing at the stove of a home kitchen, he tastes the soup from a small plate with a quiet, satisfied smile, one hand holding a ladle over the pot; steam rises as a few white curls. Facing the viewer, turned slightly to one side. Setting: a tidy home kitchen: pots and shelves as simple shapes, tiles not drawn one by one.",
    },
    "seinen-profession": {
        "ja": "題材: 小さな古本屋を営む30歳くらいの男性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ゆるく後ろで結んだ長めの髪、袖をまくったシャツに暗い色のエプロン。古い本の表紙を布でそっと拭き、やさしく集中した顔で見下ろす。正面からやや斜めを向く。 場所: 古本屋の店内。背が無地の本の詰まった高い本棚は縦線の列と平らなトーン、小さな帳場。",
        "en": "Subject: A man of about 30 who runs a small second-hand bookshop, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Longish hair tied back loosely, a dark apron over a shirt with rolled sleeves. He carefully wipes the cover of an old book with a cloth, looking down at it with a gentle, focused face. Facing the viewer, turned slightly to one side. Setting: inside the bookshop: tall bookshelves full of books with plain spines, drawn as rows of vertical lines and flat tone, a small counter.",
    },
    "seinen-daily": {
        "ja": "題材: ひとりでキャンプをする17歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とマグが画面に収まる。ニット帽、厚いダウンジャケット、マフラー。小さなたき火のそばに座り、湯気の立つマグを両手で持ち、目を細めてくつろいだ満足そうな笑顔。息と湯気は白い曲線を数本。正面からやや斜めを向く。 場所: 冬の湖畔のキャンプ場。小さなテント、湖は平らなトーン、山は平らな影、火は炎の形を数個。",
        "en": "Subject: A 17-year-old girl on a solo camping trip, seen from the waist up in a tall vertical composition, her whole head, both hands and the mug inside the picture, the surrounding background visible. A knit hat, a thick down jacket, a scarf. She sits by a small campfire, holding a steaming mug with both hands, eyes half closed in a relaxed, content smile; her breath and the steam as a few white curls. Facing the viewer, turned slightly to one side. Setting: a lakeside campsite in winter: a small tent, the lake as flat tone, mountains as flat silhouettes, the fire as a few flame shapes.",
    },
    "seinen-suspense": {
        "ja": "題材: 45歳くらいの普通の父親の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。後退した生え際、細い眼鏡、シャツにカーディガン。夜の暗い台所に立ち、スマホを耳に押し当て、顔に汗、目を見開いて恐怖に震え、もう片方の手で流し台のふちをつかむ。正面からやや斜めを向く。 場所: 夜の家の台所。部屋は黒ベタ、開いた冷蔵庫の光が白い帯、窓は黒い四角。",
        "en": "Subject: An ordinary father of about 45 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A receding hairline, thin glasses, a cardigan over a shirt. Standing in a dark kitchen at night, he presses a phone to his ear, sweat on his face, his eyes wide and shaking with fear, the other hand gripping the edge of the sink. Facing the viewer, turned slightly to one side. Setting: a home kitchen at night: the room in solid black, light from the open refrigerator falling as a white band, the window as a black rectangle.",
    },
    "josei-romance": {
        "ja": "題材: 仕事を辞めて暮らしをやり直す28歳くらいの女性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ふんわり広がる天然の巻き毛、ゆったりしたニット。古い木造アパートのベランダに座り、ひざを抱えて組んだ腕にあごをのせ、目を半分閉じてやわらかくしんみり笑う。正面からやや斜めを向く。 場所: 夕方の古いアパートのベランダ。洗濯物は白い形、手すりは定規の線、夕方の空は平らなトーン。",
        "en": "Subject: A woman of about 28 who has quit her job to start over, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Voluminous natural curly hair, a loose knit sweater. She sits on the veranda of an old wooden apartment, knees drawn up, chin resting on her folded arms, eyes half closed with a soft, wistful smile. Facing the viewer, turned slightly to one side. Setting: an old apartment veranda at dusk: laundry hanging as plain white shapes, a railing as ruled lines, the evening sky as flat tone.",
    },
    "josei-office": {
        "ja": "題材: 残業する26歳くらいの会社員の女性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。低い位置のポニーテール、眼鏡、ブラウス、無地のカードの付いた首かけのひも。ノートパソコンの前に座り、両手をキーボードに置いたまま、真っ白な画面を死んだ目で見つめる。パソコンの横にエナジードリンクの缶。正面からやや斜めを向く。 場所: 夜のオフィス。ほかの机は暗く、天井の照明はほとんど消え、彼女の机だけ明るい。窓は黒い四角。",
        "en": "Subject: An office worker of about 26 working late, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A low ponytail, glasses, an office blouse, a lanyard with a blank card. She sits in front of a laptop, both hands on the keyboard, staring at the blank white screen with dead, exhausted eyes; an energy-drink can stands beside the laptop. Facing the viewer, turned slightly to one side. Setting: an office at night: the other desks dark, ceiling lights mostly off, only her desk lit, windows as black rectangles.",
    },
    "josei-family": {
        "ja": "題材: いっしょに料理をする32歳くらいの母親と5歳くらいの娘の腰から上を縦長の構図で、周りの背景とともに。2人の頭とすべての手が画面に収まる。母親は低いポニーテールにエプロン、娘は小さな踏み台に乗り小さなエプロンで泡立て器でボウルを混ぜる。母親はそばにかがみ、あたたかく笑って見守る。正面からやや斜めを向く。 場所: 明るい家の台所。戸棚と道具は簡単な形、窓からの日差しは白い帯。",
        "en": "Subject: A mother of about 32 and her daughter of about 5 cooking together, both seen from the waist up in a tall vertical composition, both heads and all hands inside the picture, the surrounding background visible. The mother has a low ponytail and an apron; the girl stands on a small stool in a tiny apron and stirs a bowl with a whisk. The mother bends down beside her, watching with a warm, laughing smile. Facing the viewer, turned slightly to one side. Setting: a bright home kitchen: cupboards and utensils as simple shapes, sunlight from the window as white bands.",
    },
    "josei-love": {
        "ja": "題材: 20歳くらいの女子大生の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。やわらかい長い髪（淡いトーン）、冬のコートの下にニットのドレス、マフラー。胸の前で小さな手話の形をつくり、背の高い相手を見上げて、頬を赤らめてはにかみ、うれしそうに笑う。雪は白い点。正面からやや斜めを向く。 場所: 冬の夜の駅前の通り。街灯、店先は文字のない看板の簡単な形。",
        "en": "Subject: A university student of about 20 seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long soft hair shown as pale tone, a knit dress under a winter coat, a scarf. She makes a small hand sign in front of her chest and looks up at someone taller with a shy, happy smile and flushed cheeks; snow falls as white dots. Facing the viewer, turned slightly to one side. Setting: a street in front of a station on a winter night: street lamps, shop fronts as simple shapes with blank signs.",
    },
    "josei-yuri": {
        "ja": "題材: 夕暮れの川の土手に並んで座る16歳くらいの女子高生2人の腰から上を縦長の構図で、周りの背景とともに。2人の頭とすべての手が画面に収まる。1人はショートヘアにカーディガン、もう1人は長い髪にリボンタイ。長い髪の少女は目を閉じて相手の肩に頭をのせ、ショートヘアの少女はやさしく緊張して頬を赤らめて見つめる。草の上で2人の指先がふれる。正面からやや斜めを向く。 場所: 川の土手。川は平らなトーン、遠くの橋は平らな影、草は1本ずつ描かない。",
        "en": "Subject: Two high-school girls of about 16 sitting side by side on a riverside embankment at sunset, both seen from the waist up in a tall vertical composition, both heads and all hands inside the picture, the surrounding background visible. One has short hair and a cardigan, the other has long hair and a ribbon tie. The long-haired girl rests her head on the other's shoulder with closed eyes; the short-haired girl looks at her with a gentle, nervous blush; their fingers touch on the grass. Facing the viewer, turned slightly to one side. Setting: a riverside embankment: the river as flat tone, a distant bridge as a flat silhouette, grass not drawn blade by blade.",
    },
    "josei-drama": {
        "ja": "題材: 35歳くらいの小説家の女性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ぼさぼさの短い髪、ゆったりした大きめのシャツ。散らかった机で真っ白な画面のノートパソコンに向かい、声をかけられたように肩越しに振り返る、ぎこちなく戸惑った顔。正面からやや斜めを向く。 場所: 夜の散らかった書斎。背が無地の本の山、紙は無地の白い形、窓は暗い四角。",
        "en": "Subject: A novelist of about 35 seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Short messy hair, a loose oversized shirt. She sits at a cluttered desk with a laptop showing a blank white screen and turns to look back over her shoulder with an awkward, uncertain face, as if someone has just spoken to her. Facing the viewer, turned slightly to one side. Setting: a cluttered study at night: piles of books with plain spines, papers as blank white shapes, the window as a dark rectangle.",
    },
    "josei-period": {
        "ja": "題材: 昭和初期の20歳くらいの新妻の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。低い位置のまとめ髪、縞の着物に白い割烹着。たたんだシャツを胸に抱え、深く頬を赤らめてうつむき、はにかんでうれしそうに笑う。正面からやや斜めを向く。 場所: 古い木造の家の縁側。障子は細い格子の線の白い板、庭の物干し竿、日差しは白い帯。",
        "en": "Subject: A young newlywed wife of about 20 in early Showa-era Japan, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Hair in a low bun, a simple striped kimono with a white cooking smock over it. She holds a folded shirt to her chest and blushes deeply, looking down with a shy, happy smile. Facing the viewer, turned slightly to one side. Setting: the veranda of an old wooden house: paper sliding doors as white panels with thin lattice lines, a laundry pole in the garden, sunlight as white bands.",
    },
    "josei-lifestyle": {
        "ja": "題材: 料理が好きな30歳くらいの女性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短いボブ、セーターに無地のエプロン。手作りの料理を山盛りにした大皿を両手で食卓に置き、得意そうに笑う。皿から湯気が白い曲線を数本。正面からやや斜めを向く。 場所: 小さな部屋の食卓。2脚のいすのテーブル、鉢植えと棚は簡単な形、窓は白い四角。",
        "en": "Subject: A woman of about 30 who loves cooking, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A short bob, a plain apron over a sweater. She sets a large plate piled with homemade food on the dining table with both hands, smiling proudly; a few curls of steam rise from the plate. Facing the viewer, turned slightly to one side. Setting: a small apartment dining room: a table with two chairs, potted plants and a shelf as simple shapes, the window as a white rectangle.",
    },
    "josei-comedy": {
        "ja": "題材: 飲みに出た33歳くらいの会社員の女性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。くずれたまとめ髪、襟元をはずしたブラウス。小さな居酒屋のカウンターに突っ伏してビールのジョッキを握り、おおげさな涙を流しながら笑う、赤い頬。正面からやや斜めを向く。 場所: 小さな居酒屋。文字のない提灯、壁の品書きは無地の白い札、カウンターは定規の線。",
        "en": "Subject: An office worker of about 33 on a night out, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A messy updo, an office blouse with the collar undone. She slumps over the counter of a small izakaya, gripping a beer mug, crying comic tears and laughing at the same time, cheeks flushed. Facing the viewer, turned slightly to one side. Setting: a small izakaya: paper lanterns with no letters, menu tags on the wall as blank white strips, a counter as ruled lines.",
    },
    "josei-suspense": {
        "ja": "題材: 35歳くらいの主婦の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。きちんとした肩までの髪、無地のブラウス。薄暗い廊下に立ち、画面の暗い夫のスマホを両手で持ち、冷たく見開いた目で見つめ、唇をきつく結ぶ。正面からやや斜めを向く。 場所: 夜のマンションの玄関。廊下は黒ベタ、半開きの扉からの光は白い帯、玄関の靴は簡単な形。",
        "en": "Subject: A housewife of about 35 seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Neat shoulder-length hair, a plain blouse. Standing in a dim hallway, she holds her husband's phone in both hands, its screen dark, and stares at it with cold, wide eyes, lips pressed tight. Facing the viewer, turned slightly to one side. Setting: the entrance hall of an apartment at night: the hallway in solid black, light from a half-open door as a white band, shoes at the entrance as simple shapes.",
    },
    "kodomo-hobby": {
        "ja": "題材: コマの対戦をする10歳くらいの男の子の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。とがった髪にハチマキ、Tシャツに短い上着。おもちゃの発射器を片手で前に突き出し、放ったばかりのコマがスピード線とともに飛び出す。口を大きく開けて叫び、もう片方の手は拳。正面からやや斜めを向く。 場所: テーブルの上の丸い対戦台。台のくぼみは簡単な曲線の形、後ろの観客は平らな灰色の影。",
        "en": "Subject: A boy of about 10 in a spinning-top battle, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Spiky hair with a headband, a short jacket over a T-shirt. He thrusts a toy launcher forward with one hand, having just released a spinning top that shoots out with speed lines, shouting with his mouth wide open, the other hand clenched. Facing the viewer, turned slightly to one side. Setting: a round battle stadium on a table: the stadium bowl as simple curved shapes, the crowd behind as a flat grey silhouette.",
    },
    "kodomo-adventure": {
        "ja": "題材: 探検する10歳くらいの女の子の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い二つ結び、ポケットの多いベスト、半ズボン、小さなリュック。洞窟の入口にしゃがんで懐中電灯で暗闇を照らし（光は白い帯）、肩越しに振り返ってわくわくした笑顔。正面からやや斜めを向く。 場所: 森の中の洞窟の入口。洞窟は黒ベタ、岩は簡単な形、外の木は平らな影。",
        "en": "Subject: A girl of about 10 exploring, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Short pigtails, a vest with many pockets, shorts, a small backpack. She crouches at the entrance of a cave and shines a flashlight into the darkness, the beam as a white band, looking back over her shoulder with an excited grin. Facing the viewer, turned slightly to one side. Setting: a cave entrance in a forest: the cave in solid black, rocks as simple shapes, trees outside as flat silhouettes.",
    },
    "kodomo-gag": {
        "ja": "題材: 小さなおじいさんの腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。はげ頭、大きな白いひげ、短い夏の着物。両腕を振り上げて片ひざを上げたおかしなポーズで、歯を見せて大きく笑い、目が飛び出す。正面からやや斜めを向く。 場所: 古い家の庭。木の塀は定規の線、松は平らな影、飛び石は簡単な形。",
        "en": "Subject: A tiny old man seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A bald head, a huge white mustache, a short summer kimono. He strikes a ridiculous pose with both arms flung up and one knee raised, a wide toothy grin and bulging eyes. Facing the viewer, turned slightly to one side. Setting: the garden of an old house: a wooden fence as ruled lines, a pine tree as a flat silhouette, stepping stones as simple shapes.",
    },
    "kodomo-animal": {
        "ja": "題材: 2本足で立つ小さく丸い子ねこのキャラクターの全身を縦長の構図で、周りの背景とともに。子ねこ全体が画面に収まる。大きな丸い目、小さな耳、小さなリュック。小さな花を両手で掲げ、口を開けてうれしそうに笑う。正面からやや斜めを向く。 場所: 野原。草は平らなトーンで1本ずつ描かない、花は簡単な形を数個、大きな白い雲。",
        "en": "Subject: A small round kitten character standing on two legs, seen as a whole body in a tall vertical composition, the whole kitten inside the picture, the surrounding background visible. Big round eyes, small ears, a tiny backpack. It holds a small flower up with both paws and smiles happily with its mouth open. Facing the viewer, turned slightly to one side. Setting: a meadow: grass as flat tone, not drawn blade by blade, a few flowers as simple shapes, a big white cloud.",
    },
    "kodomo-learning": {
        "ja": "題材: 理科の授業の10歳くらいの男の子の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、額に上げたゴーグル、袖をまくった大きすぎる白衣。試験管を光にかざし、目を見開いて興味しんしんに口を開け、もう片方の手は説明するように人さし指を立てる。正面からやや斜めを向く。 場所: 学校の理科室。フラスコの並ぶ棚は簡単な形、実験台、黒板は何も書かない。",
        "en": "Subject: A boy of about 10 in a science lesson, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short hair, goggles pushed up on his forehead, a lab coat too big for him with the sleeves rolled up. He holds a test tube up to the light and peers at it with wide, curious eyes and an excited open mouth, the other hand raised with one finger up as if explaining. Facing the viewer, turned slightly to one side. Setting: a school science room: shelves with flasks as simple shapes, a lab table, a chalkboard left blank.",
    },
    "kodomo-magical": {
        "ja": "題材: 変身した直後の9歳くらいの女の子の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。2つのお団子の髪、大きなリボンと小さな冠のふんわりしたフリルのドレス。ハート形のコンパクトを両手で掲げ、口を大きく開けて笑う。周りに小さな星の白い形。正面からやや斜めを向く。 場所: 夕方の町の広場。建物は簡単な平らな形、後ろに大きな星形をトーンから白く抜く。",
        "en": "Subject: A girl of about 9 who has just transformed, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Hair in two round buns, a puffy frilly dress with a big ribbon and a small crown. She holds a heart-shaped compact up with both hands and smiles widely with her mouth open, surrounded by small stars as white shapes. Facing the viewer, turned slightly to one side. Setting: a town square at dusk: buildings as simple flat shapes, one large star shape behind her as a white shape cut out of the tone.",
    },
    "kodomo-school": {
        "ja": "題材: 小学生の11歳くらいの女の子の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。カチューシャの長いまっすぐな髪、背中のランドセル、ブラウスにカーディガン。小さな包みのプレゼントを両手で背中に隠し、頬を赤らめて横を見て、口を結んではにかむ。正面からやや斜めを向く。 場所: 放課後の校門。門と柵は定規の線、校舎は平らな形、桜の木は平らな柄トーン。",
        "en": "Subject: A girl of about 11 at elementary school, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long straight hair with a hairband, a school backpack on her back, a simple blouse and cardigan. She hides a small wrapped present behind her back with both hands and glances to the side, blushing, lips pressed in a shy smile. Facing the viewer, turned slightly to one side. Setting: the school gate after school: the gate and fence as ruled lines, the school building as a flat shape, a cherry tree as a flat pattern tone.",
    },
    "kodomo-sports": {
        "ja": "題材: バスケットボールをする10歳くらいの女の子の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とボールが画面に収まる。短いポニーテール、番号も文字もない袖なしのユニフォーム、手首にリストバンド。腰の横で低くドリブルし、歯を見せて大きく笑いながら前へ突き進む。汗のしずくが飛ぶ。正面からやや斜めを向く。 場所: 学校の体育館。木の床は線を数本の平らなトーン、ゴールとボードは簡単な形、壁は無地。",
        "en": "Subject: A girl of about 10 playing basketball, seen from the waist up in a tall vertical composition, her whole head, both hands and the ball inside the picture, the surrounding background visible. A short ponytail, a sleeveless basketball jersey with no numbers or letters, a sweatband on her wrist. She dribbles the ball low beside her hip and charges forward with a big determined grin, sweat drops flying. Facing the viewer, turned slightly to one side. Setting: a school gym: the wooden floor as flat tone with a few lines, the basket and backboard as simple shapes, the walls plain.",
    },
    "kodomo-mystery": {
        "ja": "題材: 探偵ごっこをする10歳くらいの女の子の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と虫めがねが画面に収まる。ボブの髪、チェックの鳥打ち帽、短いケープのコート。大きな虫めがねを片目に当て（目がレンズで大きく見える）、賢そうににやりと笑い、もう片方の手で床を指さす。正面からやや斜めを向く。 場所: 古い家の居間。敷物に足あとが数個の簡単な形、家具は簡単な形、カーテンの窓。",
        "en": "Subject: A girl of about 10 playing detective, seen from the waist up in a tall vertical composition, her whole head, both hands and the magnifying glass inside the picture, the surrounding background visible. A bob haircut, a checked hunting cap, a short cape coat. She holds a big magnifying glass up to one eye, which looks huge through the lens, and grins cleverly, pointing at the floor with her other hand. Facing the viewer, turned slightly to one side. Setting: the living room of an old house: a rug with a few footprints as simple shapes, furniture as simple shapes, a window with curtains.",
    },
    "kodomo-monster": {
        "ja": "題材: パジャマの9歳くらいの男の子と小さなおばけの腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とおばけ全体が画面に収まる。ぼさぼさの髪、しま模様のパジャマ。懐中電灯を持って驚いて跳び上がり、目を丸くして口を開ける。顔の横に大きな人なつこい目の小さな丸いおばけが浮かび、同じく驚く。正面からやや斜めを向く。 場所: 夜の暗い寝室。部屋は黒ベタ、懐中電灯の光は白い帯、ベッドとおもちゃは簡単な形。",
        "en": "Subject: A boy of about 9 in pajamas and a small ghost, seen from the waist up in a tall vertical composition, his whole head, both hands and the whole ghost inside the picture, the surrounding background visible. Messy hair, striped pajamas. He holds a flashlight and jumps in surprise, eyes round and mouth open, while a small round ghost with big friendly eyes floats beside his face, also surprised. Facing the viewer, turned slightly to one side. Setting: a dark bedroom at night: the room in solid black, the flashlight beam as a white band, a bed and toys as simple shapes.",
    },
    "yonkoma-family": {
        "ja": "題材: 45歳くらいの母親の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。丸い顔、短いパーマの髪、セーターにエプロン。お玉を振り回し、横にいる誰かをおおげさに怒った顔でしかる。ふくらんだ頬、大きく開けた口。正面からやや斜めを向く。 場所: 家族の茶の間。低いテーブルの食器は簡単な形、ふすま、テレビは無地の暗い箱。",
        "en": "Subject: A mother of about 45 seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A round face, short permed hair, an apron over a sweater. She waves a ladle and scolds someone off to the side with a comically angry face, puffed cheeks and a big open mouth. Facing the viewer, turned slightly to one side. Setting: a family dining room: a low table with dishes as simple shapes, a sliding door, a television as a plain dark box.",
    },
    "yonkoma-school": {
        "ja": "題材: 内気な16歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ヘアクリップの長い髪、制服の上に前開きのジャージ。ギターケースを両腕で抱えてうつむき、緊張で震え、頭の周りに汗のしずく、ひきつった作り笑い。正面からやや斜めを向く。 場所: 放課後の音楽室。ピアノといすは簡単な形、何も書かない黒板、窓は白い四角。",
        "en": "Subject: A shy 16-year-old girl seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long hair with a hair clip, a zip-up track jacket over her school uniform. She hugs a guitar case in both arms and looks down, trembling nervously, sweat drops around her head and a wobbly forced smile. Facing the viewer, turned slightly to one side. Setting: a school music room after class: a piano and chairs as simple shapes, a blank blackboard, windows as white rectangles.",
    },
    "yonkoma-office": {
        "ja": "題材: 25歳くらいの若い会社員の男性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。乱れた短い髪、ネクタイのゆるんだ白いシャツ。机に突っ伏して腕をだらりと下げ、開いた口から小さな白い魂の形がふわりと抜け出す。疲れ切ったうずまきの目。正面からやや斜めを向く。 場所: 夕方のオフィス。書類の山は無地の白い形、画面が無地のモニター、窓は平らなトーンの四角。",
        "en": "Subject: A young office worker of about 25 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Messy short hair, a white shirt with a loose necktie. He lies slumped face-down on his desk, arms dangling, while a tiny white soul-shaped wisp floats out of his open mouth; exhausted swirl eyes. Facing the viewer, turned slightly to one side. Setting: an office at dusk: stacks of documents as plain white shapes, a computer monitor with a blank screen, the window as a flat tone rectangle.",
    },
    "yonkoma-slice": {
        "ja": "題材: 喫茶店で働く15歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。小さな髪飾りの長いまっすぐな髪、フリルのエプロンの給仕の制服。コーヒーカップをのせた丸いお盆を持ち、落ち着いて少し眠そうな顔。横のカウンターにふわふわの小さなねこが座る。正面からやや斜めを向く。 場所: 木のあたたかい喫茶店。カウンターと棚は簡単な形、レースのカーテンの窓は平らな柄トーン。",
        "en": "Subject: A 15-year-old girl who works in a café, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long straight hair with a small hair ornament, a café waitress uniform with a frilled apron. She holds a round tray with a coffee cup and looks calm and a little sleepy, while a small fluffy cat sits on the counter beside her. Facing the viewer, turned slightly to one side. Setting: a cozy wooden café: the counter and shelves as simple shapes, a window with lace curtains as flat pattern tone.",
    },
    "yonkoma-animal": {
        "ja": "題材: ソファに並んで座る大きなふわふわの犬とまるまる太ったねこの全身を縦長の構図で、周りの背景とともに。2匹とも画面に収まる。犬は舌を出してうれしそうに笑い、しっぽを振る。ねこは背すじを伸ばして座り、不機嫌な顔で横目に犬をにらむ。正面からやや斜めを向く。 場所: 居間。ソファは簡単な丸い形、クッション、カーテンの窓。",
        "en": "Subject: A big fluffy dog and a chubby round cat sitting side by side on a sofa, both whole bodies in a tall vertical composition, both animals inside the picture, the surrounding background visible. The dog grins happily with its tongue out and its tail wagging; the cat sits upright and glares sideways at the dog with a grumpy face. Facing the viewer, turned slightly to one side. Setting: a living room: the sofa as simple rounded shapes, a cushion, a window with curtains.",
    },
    "yonkoma-newspaper": {
        "ja": "題材: 50歳くらいの父親の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。薄くなった髪、シャツにカーディガン。低いテーブルに座り、紙面が無地の新聞を広げて持ち、上からのぞいて少し驚いた顔。テーブルに湯のみ。正面からやや斜めを向く。 場所: 畳の部屋。障子は白い板、低いテーブル、鉢植え。",
        "en": "Subject: A father of about 50 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Thinning hair, a cardigan over a shirt. He sits at a low table and holds up a newspaper with blank pages, peering over the top of it with a mildly surprised face; a cup of tea sits on the table. Facing the viewer, turned slightly to one side. Setting: a tatami room: paper sliding doors as white panels, a low table, a potted plant.",
    },
    "yonkoma-story": {
        "ja": "題材: 美術を学ぶ16歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。長いゆるい巻き髪（淡いトーン）、制服にゆったりしたカーディガン。古いアパートの外階段に座り、何も描いていないスケッチブックをひざにのせ鉛筆を持ち、誰かを見上げてあたたかく笑う。正面からやや斜めを向く。 場所: 古いアパートの外階段。手すりは定規の線、鉢植え、空は白く残す。",
        "en": "Subject: A 16-year-old girl who studies art, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long wavy hair shown as pale tone, a school uniform with a loose cardigan. She sits on the outdoor stairs of an old apartment building, a sketchbook with a blank page on her knees and a pencil in her hand, looking up at someone with a warm smile. Facing the viewer, turned slightly to one side. Setting: the outdoor staircase of an old apartment building: railings as ruled lines, potted plants, the sky left white.",
    },
    "yonkoma-gag": {
        "ja": "題材: テニス部のユニフォームの小柄な少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とラケットが画面に収まる。丸い顔、短い髪、サンバイザー。テニスラケットを頭の上でめちゃくちゃに振り回し、うずまきの目で狂ったように大きく笑う。ボールは見当違いの方向へ飛んでいく。正面からやや斜めを向く。 場所: テニスコート。ネットは交差する線を数本、コートの線は白い帯、フェンスは簡単な線。",
        "en": "Subject: A short girl in a tennis club uniform seen from the waist up in a tall vertical composition, her whole head, both hands and the racket inside the picture, the surrounding background visible. A round face, short hair, a sun visor. She swings a tennis racket wildly over her head with a crazed wide grin and spiral eyes, a tennis ball flying off in the wrong direction. Facing the viewer, turned slightly to one side. Setting: a tennis court: the net as a few crossing lines, the court lines as white stripes, the fence as simple lines.",
    },
    "yonkoma-fantasy": {
        "ja": "題材: ダンジョンを管理する15歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、簡素なドレスにフード付きのマント。片手にランタン、もう片方の手に白紙をはさんだ板を持ち、まじめで少し疲れた顔で通路を点検する。足もとから小さなスライムがのぞく。正面からやや斜めを向く。 場所: 石のダンジョンの通路。石の壁は平らなトーンのブロックで1つずつ描かない、ランタンの光は白い円、通路の奥は黒ベタ。",
        "en": "Subject: A 15-year-old girl who manages a dungeon, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Short hair, a hooded cloak over a simple dress. She holds up a lantern in one hand and a clipboard with a blank sheet in the other, checking the corridor with a serious, slightly tired face, while a tiny slime monster peeks at her feet. Facing the viewer, turned slightly to one side. Setting: a stone dungeon corridor: stone walls as flat tone blocks, not drawn one by one, the lantern light as a white circle, the far end in solid black.",
    },
    "yonkoma-hobby": {
        "ja": "題材: 山登りが好きな15歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。バケットハット、軽い登山用の上着、リュック。トレッキングポールを持って山頂に立ち、息を切らしながらうれしそうに笑う。顔に汗のしずく。正面からやや斜めを向く。 場所: 山頂。遠くの峰は平らな灰色の影、下の雲は平らなトーン、小さな石積み。",
        "en": "Subject: A 15-year-old girl who loves mountain climbing, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A bucket hat, a light hiking jacket, a backpack. She holds trekking poles and stands at a mountain summit, out of breath but smiling happily, sweat drops on her face. Facing the viewer, turned slightly to one side. Setting: a mountain summit: distant peaks as flat grey silhouettes, clouds below as flat tone, a small rock cairn.",
    },
    "gag-slapstick": {
        "ja": "題材: 25歳くらいの若い警察官の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、記章も文字もない警察の制服、頭から飛んでいく帽子。街灯の柱に顔から激突した直後で、顔がおかしくつぶれ、目が回り、腕をばたつかせ、頭の周りに小さな星の白い形が回る。正面からやや斜めを向く。 場所: 夜の繁華街の通り。看板は文字のない白い四角、建物は定規の線の簡単な形。",
        "en": "Subject: A young police officer of about 25 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short hair, a police uniform with no badges or letters, a cap flying off his head. He has just slammed face-first into a lamppost; his face is comically squashed, eyes spinning, arms flailing, small stars circling his head as white shapes. Facing the viewer, turned slightly to one side. Setting: a nightlife street: signboards as blank white rectangles, buildings as simple ruled shapes.",
    },
    "gag-surreal": {
        "ja": "題材: 川辺の石段に並んで座る男子高校生2人の腰から上を縦長の構図で、周りの背景とともに。2人の頭とすべての手が画面に収まる。1人は眼鏡、もう1人は坊主頭、2人とも白いシャツ。完全に無表情で前を見つめ、2人の間の石段に大きな魚が横たわっているのに気にしない。正面からやや斜めを向く。 場所: 川辺。川は平らなトーン、石段は定規の線、遠くの橋は平らな影。",
        "en": "Subject: Two high-school boys sitting side by side on the stone steps of a riverbank, both seen from the waist up in a tall vertical composition, both heads and all hands inside the picture, the surrounding background visible. One wears glasses, the other has a buzz cut; both wear white shirts. They stare ahead with completely blank, deadpan faces, while a huge fish lies on the step between them and they ignore it. Facing the viewer, turned slightly to one side. Setting: a riverside: the river as flat tone, stone steps as ruled lines, a distant bridge as a flat silhouette.",
    },
    "gag-school": {
        "ja": "題材: 端正すぎて優雅すぎる男子高校生の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。整えた髪、眼鏡、ボタンをきっちり留めたブレザー。教室の机で完璧に背すじを伸ばして落ち着いた顔で座るが、頭の上に消しゴム、鼻の上に鉛筆がのっている。正面からやや斜めを向く。 場所: 教室。机と何も書かない黒板は定規の線の簡単な形、窓は白い四角。",
        "en": "Subject: A handsome, overly elegant high-school boy seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Neat hair, glasses, a perfectly buttoned school blazer. He sits at his classroom desk with a flawless straight posture and a serene face, while an eraser is balanced on top of his head and a pencil is balanced on his nose. Facing the viewer, turned slightly to one side. Setting: a classroom: desks and a blank blackboard as simple ruled shapes, windows as white rectangles.",
    },
    "gag-chibi": {
        "ja": "題材: 2頭身の小さなデフォルメの女の子の全身を縦長の構図で、周りの背景とともに。全身が画面に収まる。丸い顔、涙のたまった大きな目、短い二つ結び。頭ほどの大きなおにぎりを両腕で抱えてよろよろし、うれしくて口が波線。正面からやや斜めを向く。 場所: 公園のレジャーシート。シートは簡単なチェックの柄トーン、かごは簡単な形、木は平らな影。",
        "en": "Subject: A tiny super-deformed girl only two heads tall, seen as a whole body in a tall vertical composition, the whole figure inside the picture, the surrounding background visible. A round face, huge teary eyes, short pigtails. She hugs a rice ball as big as her head with both arms and wobbles, her mouth a wavy line of joy. Facing the viewer, turned slightly to one side. Setting: a picnic blanket in a park: the blanket as a simple checked pattern tone, a basket as a simple shape, trees as flat silhouettes.",
    },
    "gag-black": {
        "ja": "題材: にこやかな40歳くらいの会社員の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。きちんとなでつけた髪、無地のスーツにネクタイ。もみ手をしながら大きな作り笑いで丁寧におじぎをするが、後ろの壁に映る影は角の生えた悪魔で、ずるそうに笑っている。正面からやや斜めを向く。 場所: 会議室。黒い影のために壁は白く残す、机といすは簡単な形。",
        "en": "Subject: A smiling office worker of about 40 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Neatly combed hair, a plain suit and tie. He bows politely with a wide, fake salesman smile, hands rubbing together, while his shadow on the wall behind him is a horned devil with a sly grin. Facing the viewer, turned slightly to one side. Setting: a meeting room: the wall left white for the black shadow, a table and chairs as simple shapes.",
    },
    "gag-romcom": {
        "ja": "題材: 生徒会のプライドの高い女子高生の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。リボンを付けた長いまっすぐな黒髪、きちんとした制服。生徒会の机に着き、手の甲で口元を隠して、半分閉じたたくらむ目でにやりと笑う。頬に汗のしずくが1つ。正面からやや斜めを向く。 場所: 生徒会室。長い机、棚と窓は簡単な形、何も書かないホワイトボード。",
        "en": "Subject: A proud high-school girl on the student council, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long straight black hair with a ribbon, a neat school uniform. She sits at the student council desk, covering her mouth with the back of her hand and smirking with half-closed, scheming eyes, a single sweat drop on her cheek. Facing the viewer, turned slightly to one side. Setting: a student council room: a long desk, shelves and a window as simple shapes, a blank whiteboard.",
    },
    "gag-sports": {
        "ja": "題材: ダイビング部の筋肉質な大学生の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、水着、額に上げた水中マスク、背中にボンベ。両腕の力こぶを見せるばかばかしい勝利のポーズで、大口を開けて笑う。正面からやや斜めを向く。 場所: 小さなダイビング船のある浜辺。海は平らなトーン、砂は白く残す、ヤシの木は平らな影。",
        "en": "Subject: A muscular university student in a diving club, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short hair, swim trunks, a diving mask pushed up on his forehead, a scuba tank strapped on his back. He strikes an absurd triumphant pose with both arms flexed and roars with laughter. Facing the viewer, turned slightly to one side. Setting: a beach with a small dive boat: the sea as flat tone, the sand left white, a few palm trees as flat silhouettes.",
    },
    "gag-fantasy": {
        "ja": "題材: 魔王の城にとらわれた16歳くらいの姫の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。長い髪、小さなティアラ、ネグリジェ。魔物から取り上げた大きなふかふかの枕を抱え、目を半分閉じて眠たげに得意げな顔。後ろで角のある小さな魔物がおおげさに泣く。正面からやや斜めを向く。 場所: 暗い城の部屋。石の壁は平らなトーン、格子の窓、ベッドは簡単な形。",
        "en": "Subject: A captive princess of about 16 in a demon king's castle, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long hair, a small tiara, a nightgown. She hugs a huge fluffy pillow she has taken from a monster, eyes half closed with a sleepy, triumphant face, while a small horned monster behind her cries comically. Facing the viewer, turned slightly to one side. Setting: a room in a dark castle: stone walls as flat tone, a barred window, a bed as a simple shape.",
    },
    "gag-horror": {
        "ja": "題材: 幽霊が見える女子高生の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。長い髪、制服。バスの座席でこわばって座り、スマホを持ってまっすぐ前を見つめる。固まった作り物の無表情に大きな汗のしずく。顔のすぐ横に目のたくさんある巨大で不気味な幽霊がのぞき込む。正面からやや斜めを向く。 場所: バスの車内。座席とつり革は簡単な形、窓は白い四角。",
        "en": "Subject: A high-school girl who can see ghosts, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long hair, a school uniform. Sitting stiffly on a bus seat, she holds her phone and stares straight ahead with a frozen, forced blank face and a big sweat drop, while a huge grotesque ghost with many eyes leans in right beside her face. Facing the viewer, turned slightly to one side. Setting: inside a bus: seats and hand straps as simple shapes, windows as white rectangles.",
    },
    "gag-retro": {
        "ja": "題材: 昔のギャグ漫画の中年の父親の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。太い口ひげ、頭に巻いたハチマキ、肌着に腹巻き、甚平の上着。片手を腰に当て、もう片方の手を上げた得意げなポーズで、大口を開けて笑う。正面からやや斜めを向く。 場所: 昭和の古い商店街。店先と看板は文字のない簡単な形、電柱。",
        "en": "Subject: A middle-aged father in an old-fashioned gag comic, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A thick mustache, a band tied around his head, a belly band over an undershirt, a summer kimono jacket. He strikes a proud pose with a hand on his hip and the other hand raised, laughing with a wide open mouth. Facing the viewer, turned slightly to one side. Setting: an old Showa-era shopping street: shop fronts and signboards as simple shapes with no letters, a telephone pole.",
    },
    "horror-kaidan": {
        "ja": "題材: ろうそくの明かりで怪談を語る14歳くらいの少年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。まっすぐな黒髪、暗い色の着物。暗い部屋で前に1本のろうそくを置いて座り、下から照らされた顔で薄く笑い、人さし指を立てて語る。後ろの障子に、長い髪の背の高い女の影が立つ。正面からやや斜めを向く。 場所: 暗い畳の部屋。部屋は黒ベタ、障子は淡い板、火のついていないろうそくが数本。",
        "en": "Subject: A boy of about 14 telling ghost stories by candlelight, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Straight black hair, a dark kimono. He sits in a dark room with a single candle in front of him, the light from below on his face, a thin smile, one finger raised as he speaks; on the paper sliding door behind him stands the silhouette of a tall woman with long hair. Facing the viewer, turned slightly to one side. Setting: a dark tatami room: the room in solid black, the sliding door as a pale panel, several unlit candles.",
    },
    "horror-psychological": {
        "ja": "題材: 17歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。小さなリボンの長い髪、制服にかわいいカーディガン。うさぎのぬいぐるみをぎゅっと抱きしめて甘く笑うが、目は光のない黒い丸で空っぽ。正面からやや斜めを向く。 場所: 淡い色合いの寝室。かわいい家具とクッションは簡単な形、後ろの扉にはたくさんの錠と鎖。",
        "en": "Subject: A 17-year-old girl seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long hair with a small ribbon, a cute cardigan over a school uniform. She hugs a stuffed rabbit tightly and smiles sweetly, but her eyes are empty black circles without highlights. Facing the viewer, turned slightly to one side. Setting: a pastel bedroom: cute furniture and cushions as simple shapes, while the door behind her is covered with many locks and chains.",
    },
    "horror-cosmic": {
        "ja": "題材: 夜の浜辺に立つ30歳くらいの男性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、ウインドブレーカー。恐怖で固まって見上げ、黒目は小さく口が震える。背後の海から、何よりも巨大な、無数の目を持つ形のないものがせり上がる。正面からやや斜めを向く。 場所: 夜の浜辺。海は暗い平らなトーン、巨大なものは白い目がたくさんある黒い塊、空は黒ベタ。",
        "en": "Subject: A man of about 30 standing on a beach at night, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short hair, a windbreaker. He looks up in frozen terror, eyes tiny and mouth trembling, at a gigantic shapeless thing with countless eyes rising from the sea behind him, far larger than anything else. Facing the viewer, turned slightly to one side. Setting: a night beach: the sea as flat dark tone, the huge thing as a black mass with many white eyes, the sky in solid black.",
    },
    "horror-folk": {
        "ja": "題材: 夏の山あいの村の16歳くらいの少年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い黒髪、白い半袖のシャツ。顔に汗を浮かべ、山道に立ち止まり、横の何かを見つめて恐れがつのる。両手はこわばって下がる。正面からやや斜めを向く。 場所: 夏の山村の道。しめ縄の小さな祠、杉の木は平らな暗い影、夏の日差しは強い白い光と黒い影。",
        "en": "Subject: A 16-year-old boy in a rural village in summer, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short black hair, a white short-sleeved shirt. Sweat on his face, he stands still on a mountain road and stares at something off to the side with growing dread, his hands hanging stiffly. Facing the viewer, turned slightly to one side. Setting: a mountain village road in summer: a small shrine with a sacred straw rope, cedar trees as flat dark silhouettes, summer sunlight as hard white light and black shadows.",
    },
    "horror-school": {
        "ja": "題材: 暗くなった学校にいる13歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ボブの髪、セーラー服。女子トイレの個室の前で両手を胸の前で握って凍りつき、個室の扉の下のすき間から青白い手がのびる。正面からやや斜めを向く。 場所: 夕暮れの古い学校のトイレ。タイルは1枚ずつ描かない、個室の扉は平らなトーンの板、窓は淡い四角。",
        "en": "Subject: A 13-year-old girl at school after dark, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A bob haircut, a sailor-style school uniform. She stands frozen in front of a toilet stall in the girls' bathroom, both hands clasped at her chest, while a pale hand reaches out from the gap under the stall door. Facing the viewer, turned slightly to one side. Setting: an old school bathroom at dusk: tiles not drawn one by one, stall doors as flat tone panels, the window as a pale rectangle.",
    },
    "horror-shojo": {
        "ja": "題材: 美しい15歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。長いゆるい巻き髪、長いまつげの大きな目、レースの黒いゴシックのドレス。顔にひびの入った陶器の人形を抱き、やさしく愛おしそうに笑いかける。周りにとげのあるバラのつるがはう。正面からやや斜めを向く。 場所: 古い洋風の部屋。暗いカーテンの窓、バラととげは黒い形、壁は平らなトーン。",
        "en": "Subject: A beautiful 15-year-old girl seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long wavy hair, large eyes with long lashes, a black gothic dress with lace. She holds a porcelain doll with a cracked face and smiles softly and lovingly at it, while thorny rose vines creep around her. Facing the viewer, turned slightly to one side. Setting: an old Western-style room: a window with dark curtains, roses and thorns as black shapes, the wall as flat tone.",
    },
    "horror-creature": {
        "ja": "題材: 20歳くらいの青年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、パーカー。左腕が裂けて、先に鋭い歯の並ぶうごめく触手に変わり、目を見開いてがく然と見つめ、もう片方の手で手首をつかむ。正面からやや斜めを向く。 場所: 夜の路地裏。路地は黒ベタ、街灯1本の光は白い円すい、ごみ袋は簡単な形。",
        "en": "Subject: A young man of about 20 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short hair, a hoodie. His left arm splits open into writhing tendrils ending in rows of sharp teeth; he stares at it in shock, eyes wide, the other hand gripping his wrist. Facing the viewer, turned slightly to one side. Setting: a back alley at night: the alley in solid black, a single street lamp as a white cone of light, trash bags as simple shapes.",
    },
    "horror-urban": {
        "ja": "題材: 夜の踏切にいる20歳くらいの若い女性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。長い髪、パーカーとトートバッグ。画面の暗いスマホを掲げたまま目を見開いて凍りつき、背後の線路の向こうに腕が長すぎる背の高いやせた人影が立つ。正面からやや斜めを向く。 場所: 夜の踏切。遮断機と警報機は簡単な形、線路は定規の線、空は黒ベタ。",
        "en": "Subject: A young woman of about 20 at a railway crossing at night, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long hair, a hoodie and a tote bag. She holds up her phone, its screen dark, and freezes with her eyes wide, while across the tracks behind her stands a tall, thin figure with arms that are far too long. Facing the viewer, turned slightly to one side. Setting: a railway crossing at night: the crossing gate and signal as simple shapes, the tracks as ruled lines, the sky in solid black.",
    },
    "horror-yokai": {
        "ja": "題材: 妖怪が見えるやさしい16歳くらいの少年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。明るくやわらかい髪（淡いトーン）、白い制服のシャツ。小さな神社の石段に座り、そばに座る一つ目の傘の妖怪と小さな狐の妖怪2匹を、やさしく少しさびしげに笑って見下ろす。茂みからほかの小さな妖怪がのぞく。正面からやや斜めを向く。 場所: 森の中の小さな神社。鳥居は簡単な形、木は平らな影、葉は1枚ずつ描かない。",
        "en": "Subject: A gentle 16-year-old boy who can see yokai, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Light soft hair shown as pale tone, a white school shirt. He sits on the stone steps of a small shrine and looks down with a kind, slightly sad smile at a one-eyed umbrella yokai and two small fox spirits that sit beside him, while more small yokai peek from the bushes. Facing the viewer, turned slightly to one side. Setting: a small shrine in the woods: a torii gate as a simple shape, trees as flat silhouettes, leaves not drawn one by one.",
    },
    "horror-panic": {
        "ja": "題材: 必死に逃げる24歳くらいの若い会社員の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。乱れた髪、ネクタイをゆるめ袖をまくった白いシャツ。こちらへ走りながら恐怖で肩越しに振り返り、口を開けて叫ぶ。腕を突き出したゾンビの群れが追ってくる。正面からやや斜めを向く。 場所: 街の通り。ゾンビの群れは暗い平らな影、乗り捨てられた車と建物は簡単な形。",
        "en": "Subject: A young office worker of about 24 running for his life, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Messy hair, a white shirt with a loosened necktie and rolled sleeves. He runs toward the viewer and looks back over his shoulder in terror, mouth open in a scream, while a crowd of zombies with outstretched arms chases him. Facing the viewer, turned slightly to one side. Setting: a city street: the zombie crowd as dark flat silhouettes, abandoned cars and buildings as simple shapes.",
    },
    "essay-diary": {
        "ja": "題材: 35歳くらいの女性（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ゆるく結んだ髪、部屋着。ソファにうつぶせに倒れ込み、片腕を床にだらりと下げ、床にスマホ。完全に力の抜けた空っぽの顔で、点の目と一本線の口。正面からやや斜めを向く。 場所: 一日の終わりの居間。ソファとクッションは簡単な形、壁に数字のない時計。",
        "en": "Subject: A woman of about 35, the author herself, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Hair loosely tied, loungewear. She lies face down on the sofa, one arm hanging down to the floor where her phone lies, her face completely drained and blank, dot eyes and a flat line mouth. Facing the viewer, turned slightly to one side. Setting: a living room at the end of the day: a sofa and cushions as simple shapes, a clock on the wall with no numbers.",
    },
    "essay-parenting": {
        "ja": "題材: 33歳くらいの母親（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。お団子にしたぼさぼさの髪、しみのついたTシャツ。泣く幼児を片腕に抱え、もう片方の手に離乳食のスプーン。てんやわんやで泣き笑いの顔に汗のしずく。正面からやや斜めを向く。 場所: 散らかった台所。おもちゃとベビーチェアは簡単な形、飛び散った食べ物は小さな黒い点。",
        "en": "Subject: A mother of about 33, the author herself, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Messy hair in a bun, a stained T-shirt. She holds a crying toddler under one arm and a spoon of baby food in the other hand, with a frazzled, laughing-crying face and sweat drops. Facing the viewer, turned slightly to one side. Setting: a messy kitchen: toys and a high chair as simple shapes, food splattered as small black dots.",
    },
    "essay-travel": {
        "ja": "題材: ひとり旅をする30歳くらいの女性（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。日よけの帽子、半袖のシャツ、大きなリュック。白紙の紙の地図を逆さまに広げて持ち、首をかしげて困った顔。正面からやや斜めを向く。 場所: 外国の古い町の石畳の通り。アーチ窓の建物は簡単な形、教会の塔は平らな影。",
        "en": "Subject: A woman of about 30 traveling alone, the author herself, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A sun hat, a short-sleeved shirt, a big backpack. She holds up an unfolded paper map with blank paper, turned upside down, and tilts her head with a puzzled face. Facing the viewer, turned slightly to one side. Setting: a stone-paved street in a foreign old town: buildings with arched windows as simple shapes, a church tower as a flat silhouette.",
    },
    "essay-food": {
        "ja": "題材: ひとりでラーメンを食べる28歳くらいの会社員の女性（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短いボブ、ブラウス。小さなラーメン屋のカウンターで大きなどんぶりから箸で麺を持ち上げ、頬をふくらませ、目を閉じて至福の顔。湯気は白い曲線を数本。正面からやや斜めを向く。 場所: 小さなラーメン屋。カウンターは定規の線、品書きは無地の白い札、文字のない提灯。",
        "en": "Subject: An office worker of about 28, the author herself, eating ramen alone, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. A short bob, an office blouse. She sits at the counter of a small ramen shop, lifting noodles with chopsticks from a big bowl, cheeks puffed, eyes closed in pure bliss; steam rises as a few white curls. Facing the viewer, turned slightly to one side. Setting: a small ramen shop: the counter as ruled lines, menu tags as blank white strips, a paper lantern with no letters.",
    },
    "essay-work": {
        "ja": "題材: 30歳くらいの看護師（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。後ろで結んだ髪、名札に文字のない看護師の制服。夜の病院の廊下で医療用のワゴンを押し、疲れているけれど一人でほほえむ。こめかみに小さな汗のしずく。正面からやや斜めを向く。 場所: 夜の病院の廊下。廊下は定規の線、扉は平らなトーンの板、天井の照明は白い四角。",
        "en": "Subject: A nurse of about 30, the author herself, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Hair tied back, a nurse's uniform with no name tag text. She pushes a medical cart down a hospital corridor at night, tired but smiling to herself, a small sweat drop on her temple. Facing the viewer, turned slightly to one side. Setting: a hospital corridor at night: the corridor as ruled lines, doors as flat tone panels, ceiling lights as white rectangles.",
    },
    "essay-health": {
        "ja": "題材: 入院している40歳くらいの女性（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、入院着。点滴スタンドの横のベッドで体を起こし、弱々しいけれど明るい笑顔で小さくピースサイン。正面からやや斜めを向く。 場所: 病室。白いベッド、カーテンは淡い平らなトーン、窓は白い四角。",
        "en": "Subject: A woman of about 40, the author herself, in a hospital, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Short hair, a hospital gown. She sits up on a hospital bed next to an IV stand and gives a weak but cheerful smile and a small V sign. Facing the viewer, turned slightly to one side. Setting: a hospital room: a white bed, a curtain as flat pale tone, the window as a white rectangle.",
    },
    "essay-pet": {
        "ja": "題材: 犬とねこと暮らす35歳くらいの女性（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と2匹が画面に収まる。くずれたポニーテール、ゆったりしたセーター。床に座って笑い、大きな犬が肩に全体重でもたれかかり、ねこがひざの上で丸くなる。正面からやや斜めを向く。 場所: 居間の床。敷物、ソファ、ペットのおもちゃは簡単な形。",
        "en": "Subject: A woman of about 35, the author herself, with her dog and cat, seen from the waist up in a tall vertical composition, her whole head, both hands and both animals inside the picture, the surrounding background visible. Hair in a messy ponytail, a loose sweater. She sits on the floor laughing, while a big dog leans its whole weight on her shoulder and a cat curls up on her lap. Facing the viewer, turned slightly to one side. Setting: a living room floor: a rug, a sofa and pet toys as simple shapes.",
    },
    "essay-hobby": {
        "ja": "題材: 推しのアイドルのコンサートにいる28歳くらいの女性（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ポニーテール、無地のTシャツ。白い棒のペンライトを2本掲げ、満面の笑みでうれし涙を流す。正面からやや斜めを向く。 場所: コンサート会場。周りの観客は暗い影にペンライトの白い点がたくさん、遠くのステージは白い形。",
        "en": "Subject: A woman of about 28, the author herself, at a concert of her favorite idol, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Hair in a ponytail, a plain T-shirt. She raises two penlights, shown as white bars, crying tears of joy with a huge smile. Facing the viewer, turned slightly to one side. Setting: a concert hall: the crowd around her as dark silhouettes with many white dots for penlights, the stage far away as a white shape.",
    },
    "essay-report": {
        "ja": "題材: 取材に出かけた30歳くらいの記者の女性（作者自身）の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、ポケットの多い上着。白紙の手帳とペンを持ち、横にいる人の話を熱心に興味深そうに聞く。正面からやや斜めを向く。 場所: 漁港。漁船と網は簡単な形、海は平らなトーン、カモメは小さな白い形。",
        "en": "Subject: A reporter of about 30, the author herself, on a field trip, seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Short hair, a jacket with many pockets. She holds a notebook with blank pages and a pen, listening intently to someone off to the side with an earnest, curious face. Facing the viewer, turned slightly to one side. Setting: a fishing port: fishing boats and nets as simple shapes, the sea as flat tone, gulls as small white shapes.",
    },
    "essay-love": {
        "ja": "題材: 30代の夫婦（作者と夫）の腰から上を縦長の構図で、周りの背景とともに。2人の頭とすべての手が画面に収まる。妻はくずれたお団子の髪に部屋着、夫は短い髪にスウェット。2人でソファに座り、妻は夫の肩にもたれてアイスを食べながらくつろいで笑い、夫は眠そうな顔でテレビを見る。正面からやや斜めを向く。 場所: 夜の小さな居間。テレビは無地の暗い箱、スタンドの明かり、クッションは簡単な形。",
        "en": "Subject: A married couple in their 30s, the author and her husband, seen from the waist up in a tall vertical composition, both heads and all hands inside the picture, the surrounding background visible. She has a messy bun and loungewear; he has short hair and a sweatshirt. They sit on a sofa together; she leans on his shoulder eating ice cream with a relaxed smile, while he watches the television with a sleepy face. Facing the viewer, turned slightly to one side. Setting: a small living room at night: the television as a plain dark box, a lamp, cushions as simple shapes.",
    },
    "gekiga-samurai": {
        "ja": "題材: 30歳くらいの流浪の剣客の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と刀の柄が画面に収まる。後ろで結んだ伸び放題の長い黒髪、無精ひげ、着古した着物。右手で腰の刀の柄を握って抜く寸前、正面へ鋭い殺気の目を向ける。正面からやや斜めを向く。 場所: 曇り空の下の風の吹く草原。風になびく草は平らなトーン、空は平らなトーン。",
        "en": "Subject: A wandering swordsman of about 30 seen from the waist up in a tall vertical composition, his whole head, both hands and the sword hilt inside the picture, the surrounding background visible. Long unkempt black hair tied back, stubble, a worn kimono. His right hand grips the hilt of the katana at his waist, ready to draw, and he fixes a piercing, deadly stare ahead. Facing the viewer, turned slightly to one side. Setting: a windswept grass field under a cloudy sky: the grass bent by the wind as flat tone, the sky as flat tone.",
    },
    "gekiga-yakuza": {
        "ja": "題材: 45歳くらいの任侠の親分の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。なでつけた短い髪、頬の傷、暗い色の着物に羽織。畳にあぐらをかいて小さな杯を持ち、重く無言のにらみで正面を見る。正面からやや斜めを向く。 場所: 和室。文字のない掛け軸、ふすまは平らな板、畳は線を数本の平らなトーン。",
        "en": "Subject: A yakuza boss of about 45 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short slicked hair, a scar on his cheek, a dark kimono with a haori. He sits cross-legged on tatami holding a small sake cup, staring ahead with a heavy, silent glare. Facing the viewer, turned slightly to one side. Setting: a traditional Japanese room: a hanging scroll with no writing, sliding doors as flat panels, tatami as flat tone with a few lines.",
    },
    "gekiga-crime": {
        "ja": "題材: 50歳くらいのベテランの刑事の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。角刈り、深いしわ、ネクタイのゆるんだよれたスーツ。取調室の机に両方の拳をついて身を乗り出し、画面の外の容疑者をにらみつける。正面からやや斜めを向く。 場所: 取調室。机のスタンドの光は白い円すい、壁は平らな灰色のトーン、隅は黒ベタ。",
        "en": "Subject: A veteran detective of about 50 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A crew cut, deep wrinkles, a rumpled suit with a loose tie. He leans over the desk of an interrogation room with both fists on the table, glaring at the suspect off-frame. Facing the viewer, turned slightly to one side. Setting: an interrogation room: a desk lamp as a white cone of light, walls as flat grey tone, the corners in solid black.",
    },
    "gekiga-war": {
        "ja": "題材: 第二次世界大戦の南の島の戦いの22歳くらいの若い兵士の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と小銃が画面に収まる。鉄かぶと、汗でぬれた軍服。たこつぼにうずくまって小銃を胸に抱え、恐怖で目を見開き、顔を汗が流れる。正面からやや斜めを向く。 場所: 密林の戦場。折れたヤシの木は黒い影、煙は輪郭のない平らなトーン、土のうは簡単な形。",
        "en": "Subject: A young soldier of about 22 in a World War II Pacific island battle, seen from the waist up in a tall vertical composition, his whole head, both hands and the rifle inside the picture, the surrounding background visible. A steel helmet, a sweat-soaked uniform. He crouches in a foxhole clutching his rifle to his chest, eyes wide with fear, sweat running down his face. Facing the viewer, turned slightly to one side. Setting: a jungle battlefield: broken palm trees as black silhouettes, smoke as flat tone patches without outlines, sand bags as simple shapes.",
    },
    "gekiga-hardboiled": {
        "ja": "題材: 無口な腕利きの狙撃手の45歳くらいの男の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手とライフルが画面に収まる。短い髪、太い眉、四角いあご、暗い色のスーツ。夜明けの超高層ビルの屋上の端から狙撃銃を構え、片目をスコープに当て、まったくの無表情。正面からやや斜めを向く。 場所: 夜明けの超高層ビルの屋上。下の街は平らな灰色のブロック、空は平らなトーン、給水タンクは簡単な形。",
        "en": "Subject: A silent professional sniper of about 45 seen from the waist up in a tall vertical composition, his whole head, both hands and the rifle inside the picture, the surrounding background visible. Short hair, thick eyebrows, a square jaw, a dark suit. He aims a sniper rifle from the edge of a skyscraper rooftop at dawn, one eye to the scope, face utterly expressionless. Facing the viewer, turned slightly to one side. Setting: a skyscraper rooftop at dawn: the city below as flat grey blocks, the sky as flat tone, a water tank as a simple shape.",
    },
    "gekiga-social": {
        "ja": "題材: 26歳くらいの若い研修医の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、手術着の上に白衣、首に聴診器。夜の病院の廊下に立ち、両脇で拳を握りしめ、怒りと疑いに満ちた目で唇をかむ。正面からやや斜めを向く。 場所: 夜の病院の廊下。廊下は定規の線、非常灯は白い四角、奥は黒ベタ。",
        "en": "Subject: A young resident doctor of about 26 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short hair, a white coat over scrubs, a stethoscope around his neck. He stands in a hospital corridor at night with his fists clenched at his sides, his eyes full of anger and doubt, biting his lip. Facing the viewer, turned slightly to one side. Setting: a hospital corridor at night: the corridor as ruled lines, an emergency light as a white rectangle, the far end in solid black.",
    },
    "gekiga-sports": {
        "ja": "題材: 試合中の24歳くらいのボクサーの腰から上を縦長の構図で、周りの背景とともに。頭全体と両方のグローブが画面に収まる。短い髪、腫れた目、血のにじむ唇、汗の光る裸の上半身。両方のグローブを上げてガードし、その上から折れない闘志の激しい目でにらむ。正面からやや斜めを向く。 場所: ボクシングのリング。ロープは太い線を数本、上の照明は白い形、観客は暗い塊。",
        "en": "Subject: A boxer of about 24 in the middle of a fight, seen from the waist up in a tall vertical composition, his whole head and both gloves inside the picture, the surrounding background visible. Short hair, a swollen eye, a bleeding lip, bare torso with sweat. He raises both gloves in a guard and glares over them with a fierce, unbroken will. Facing the viewer, turned slightly to one side. Setting: a boxing ring: the ropes as a few thick lines, the ring lights as white shapes above, the crowd as a dark mass.",
    },
    "gekiga-kaiki": {
        "ja": "題材: 悪魔に変わりつつある40歳くらいの男の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。顔の半分は角と牙とにらむ目の悪魔に変わり血管が浮き、残りの半分はまだ人間で苦しみに叫ぶ。かぎ爪の手で自分の顔をつかむ。正面からやや斜めを向く。 場所: 夜の燃える町。炎は黒と白の炎の形、建物は暗い影、煙は平らなトーン。",
        "en": "Subject: A man of about 40 turning into a demon, seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Half of his face has turned into a demon with a horn, fangs and a glaring eye, veins bulging; the other half is still human and screaming in agony; his clawed hand grips his face. Facing the viewer, turned slightly to one side. Setting: a burning town at night: flames as black and white flame shapes, buildings as dark silhouettes, smoke as flat tone.",
    },
    "gekiga-historical": {
        "ja": "題材: 戦国時代の40歳くらいの武将の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と軍配が画面に収まる。濃いひげ、豪華な甲冑、大きな前立ての兜。軍配を高く掲げて軍勢に命じ、威圧するにらみで叫ぶ。正面からやや斜めを向く。 場所: 城の下の戦場。印のない無地ののぼり旗、遠くの兵は平らな灰色の帯、城は平らな影。",
        "en": "Subject: A samurai general of about 40 in the Warring States period of Japan, seen from the waist up in a tall vertical composition, his whole head, both hands and the war fan inside the picture, the surrounding background visible. A thick beard, ornate armor, a helmet with a large crest. He raises a war fan high to command his army and shouts with a commanding glare. Facing the viewer, turned slightly to one side. Setting: a battlefield below a castle: plain banners without symbols, distant troops as flat grey bands, the castle as a flat silhouette.",
    },
    "gekiga-adventure": {
        "ja": "題材: たくましい元兵士の30歳くらいの男の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。傷のある顔、軍帽、厚い襟巻き、背中に猟銃。雪の森をかき分けて進み、息は白いかたまり、強く決意に満ちた顔。正面からやや斜めを向く。 場所: 北の雪の森。高い木は平らな暗い縦の形、雪は白く残す、雪片は白い点。",
        "en": "Subject: A rugged former soldier of about 30 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A scarred face, a military cap, a thick scarf, a hunting rifle on his back. He trudges through a snowy forest, breath as a white puff, with a tough, determined look. Facing the viewer, turned slightly to one side. Setting: a snowy forest in the north: tall trees as flat dark vertical shapes, snow left white, snowflakes as white dots.",
    },
    # 2026-09-28 3段目から 2段目に移した 2 つ（今の作品を調べて主役と舞台の型だけを取った。作品名は入れない）
    "gag-hetauma": {
        "ja": "題材: 25歳くらいの青年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短いぼさぼさの黒髪、無地のTシャツ、ジャージの上着。眠そうな無表情で、片手を軽く上げてあいさつする。正面からやや斜めを向く。 場所: 何もない昼の野外。青年の後ろの地面に、目を回して倒れた巨大な怪物（丸いかたまりに角と点の目）が横たわる。背景は地平線の線1本と小さな雲1つだけで、ほかは白い紙。",
        "en": "Subject: A young man of about 25 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short messy black hair, a plain T-shirt and a track jacket. He raises one hand in a casual greeting with a sleepy, blank face. Facing the viewer, turned slightly to one side. Setting: an empty open place by day; behind him on the ground lies a huge knocked-out monster with spinning eyes, drawn as a round lump with horns and dot eyes. The background is only one horizon line and one small cloud, the rest white paper.",
    },
    "kodomo-geometric": {
        "ja": "題材: 7歳くらいの女の子の全身を縦長の構図で、周りの背景とともに。頭から足先まで全身が画面に収まる。おかっぱ頭、大きな丸いボタンの服、長靴。両腕を大きく広げて片足で跳ね、口を開けて笑う。正面を向く。 場所: 雨上がりの小さな町。家は四角と三角、木は丸、空に大きな丸い雲、地面に水たまり。",
        "en": "Subject: A girl of about 7 seen as a whole body in a tall vertical composition, her whole body from head to feet inside the picture, the surrounding background visible. A bob haircut, a dress with big round buttons, rain boots. She spreads both arms wide and hops on one foot, laughing with her mouth open. Facing the viewer. Setting: a small town after the rain: houses as squares and triangles, trees as circles, a big round cloud in the sky and puddles on the ground.",
    },
    # 2026-09-28 日本の漫画の調査で足した 2段目 9 つ（今の作品を調べて主役と舞台の型だけを取った。作品名は入れない）
    "shonen-carved": {
        "ja": "題材: 18歳くらいの青年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。高く盛り上げた癖のある黒髪、襟の高い丈の長い学生服の上着を前を開けて着る。片手を顔の横に斜めに添え、指を大きく開いた気取ったポーズ。あごを上げ、自信に満ちた鋭い目で正面を見る。口は閉じる。正面からやや斜めを向く。 場所: 夕方の古い洋館の前の坂道。建物は定規の線の簡単な形、空は平らなトーン。",
        "en": "Subject: A young man of about 18 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Tall, swept-up wavy black hair, a long high-collared school jacket worn open. One hand held diagonally beside his face with the fingers spread wide in a posed, dramatic gesture. Chin raised, a confident, piercing look straight ahead, mouth closed. Facing the viewer, turned slightly to one side. Setting: a slope in front of an old Western-style mansion at dusk: the building as simple ruled shapes, the sky as flat tone.",
    },
    "shojo-otome": {
        "ja": "題材: 16歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。肩までのふわふわの巻き毛に小さなリボン、丸い襟のギンガムチェックのドレスに白いエプロン。窓辺で両手を組んで頬に寄せ、目を細めてはにかむ。正面からやや斜めを向く。 場所: 屋根裏の小さな部屋。窓は白い四角、レースのカーテンは線だけ、窓辺に小さな鉢植えを1つ。",
        "en": "Subject: A girl of about 16 seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Fluffy shoulder-length curly hair with a small ribbon, a gingham dress with a round collar and a white apron. By the window she clasps her hands together against her cheek and smiles shyly, her eyes narrowed. Facing the viewer, turned slightly to one side. Setting: a small attic room: the window as a white rectangle, lace curtains in line only, one small potted plant on the windowsill.",
    },
    "shojo-starry": {
        "ja": "題材: 12歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。長い巻き毛の髪に大きなつばの帽子、フリルの襟のドレス。胸の前で両手を組み、少し上を見上げて、夢見るようにほほえむ。正面からやや斜めを向く。 場所: 洋館の庭の小道。遠くの木と柵は線だけの簡単な形で、空は白く残す。",
        "en": "Subject: A girl of about 12 seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Long curly hair under a wide-brimmed hat, a dress with a frilled collar. She clasps her hands in front of her chest, looks slightly upward and smiles dreamily. Facing the viewer, turned slightly to one side. Setting: a garden path of a Western-style mansion: distant trees and a fence as simple line-only shapes, the sky left white.",
    },
    "josei-tanbi": {
        "ja": "題材: 20代前半の男性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。肩にかかる長い黒髪、襟の高い黒いロングコート、細い銀縁の眼鏡。片手で前髪をかき上げ、横目で冷たく見下ろす。口は閉じる。正面からやや斜めを向く。 場所: 夜の古い教会の前。尖ったアーチの扉と窓は簡単な線、背景は黒ベタ。",
        "en": "Subject: A man in his early twenties seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Long black hair falling past his shoulders, a high-collared black long coat, thin silver-rimmed glasses. He brushes his bangs back with one hand and looks down coldly out of the corner of his eye, mouth closed. Facing the viewer, turned slightly to one side. Setting: in front of an old church at night: pointed arch doors and windows as simple lines, the background solid black.",
    },
    "seinen-warped": {
        "ja": "題材: 12歳くらいの少年の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。丸坊主の頭、だぶだぶのジャンパー。歩道橋の手すりに腰かけ、両手をポケットに入れ、口を開けてにやりと笑う。正面からやや斜めを向く。 場所: 夕方の雑多な繁華街を見下ろす歩道橋の上。ビル・看板・電線・室外機がびっしり並ぶ。看板は文字のない白い四角。",
        "en": "Subject: A boy of about 12 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A shaved head and a baggy bomber jacket. He sits on the railing of a pedestrian bridge, both hands in his pockets, grinning with his mouth open. Facing the viewer, turned slightly to one side. Setting: on a pedestrian bridge above a crowded downtown street at dusk: buildings, signboards, electric wires and air-conditioner units packed together; signboards as blank white rectangles.",
    },
    "seinen-penscape": {
        "ja": "題材: 30歳くらいの男性の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、よれたシャツにゆるいズボン。古い木の橋の欄干にもたれ、片手に麦わら帽子を持ち、ぼんやりと川を眺める。口は閉じる。正面からやや斜めを向く。 場所: 夏の昼の古い下町の川べり。木造の家並み、板塀、電柱、柳の木、川面。",
        "en": "Subject: A man of about 30 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short hair, a rumpled shirt and loose trousers. He leans on the railing of an old wooden bridge, a straw hat in one hand, gazing absently at the river, mouth closed. Facing the viewer, turned slightly to one side. Setting: an old downtown riverside on a summer afternoon: rows of wooden houses, board fences, utility poles, a willow tree and the river surface.",
    },
    "gekiga-grotesque": {
        "ja": "題材: 40歳くらいの剣士の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手と刀の刃先まで画面に収まる。後ろで束ねた乱れた長い髪、着古した着物と袴。両手で刀の柄を握って刃を斜め上に立て、刃は顔にかからない。目を大きく見開き、歯を食いしばった狂気の形相で正面を見据える。正面からやや斜めを向く。 場所: 夕暮れの城の石垣の下。石垣と松は平らなトーンの簡単な形。",
        "en": "Subject: A swordsman of about 40 seen from the waist up in a tall vertical composition, his whole head, both hands and the tip of his sword inside the picture, the surrounding background visible. Long, disheveled hair tied at the back, a worn kimono and hakama. He grips the hilt of a katana with both hands, the blade raised diagonally upward without covering his face. Eyes stretched wide open, teeth clenched, a face of mad fury staring straight ahead. Facing the viewer, turned slightly to one side. Setting: below the stone wall of a castle at dusk: the stone wall and pine trees as simple shapes in flat tone.",
    },
    "gekiga-bearded": {
        "ja": "題材: 45歳くらいの大工の男の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短く刈った髪、濃いあごひげと口ひげ、袖をまくったシャツに作業用のエプロン。作業台に両手をついて、目を細めておだやかに笑う。正面からやや斜めを向く。 場所: 昼の木工の作業場。棚と作業台は定規の線の簡単な形、窓は白い四角。",
        "en": "Subject: A carpenter of about 45 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Close-cropped hair, a thick full beard and moustache, a shirt with rolled-up sleeves and a work apron. Both hands resting on the workbench, he smiles gently with narrowed eyes. Facing the viewer, turned slightly to one side. Setting: a woodworking shop by day: shelves and the workbench as simple ruled shapes, the window as a white rectangle.",
    },
    "gag-grimy": {
        "ja": "題材: 80歳くらいのやせた老人の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。はげ頭に白いまばらな髪、ぼろぼろの着物。両手を上げて指を曲げ、目をむいて大口を開けて叫ぶ。正面からやや斜めを向く。 場所: 何もない昼の野原。地平線の線1本と小さな雲1つだけで、ほかは白い紙。",
        "en": "Subject: A skinny old man of about 80 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. A bald head with a few scraggly white hairs, a ragged kimono. He raises both hands with curled fingers, eyes bulging, and shouts with his mouth wide open. Facing the viewer, turned slightly to one side. Setting: an empty field by day: only one horizon line and one small cloud, the rest white paper.",
    },
    # 2026-09-29 日本の漫画の 3 回目の調査で足した 2段目 6 つ（調べた作品の主役と舞台の型だけを取った。作品名は入れない）
    "shonen-linecarved": {
        "ja": "題材: 35歳くらいの大柄な男の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短く刈った黒髪、袖をまくった厚手の作業シャツ、太い首と厚い肩と太い腕。片手の拳を胸の前で握り、眉を寄せて静かに遠くを見据える。口は閉じる。正面からやや斜めを向く。 場所: 夕方の港の埠頭。遠くの船と倉庫は簡単な形、空は白く残す。",
        "en": "Subject: A large man of about 35 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Close-cropped black hair, a heavy work shirt with rolled-up sleeves, a thick neck, broad shoulders and thick arms. He clenches one fist in front of his chest and gazes quietly into the distance with knitted brows, mouth closed. Facing the viewer, turned slightly to one side. Setting: a harbour pier at dusk: distant ships and warehouses as simple shapes, the sky left white.",
    },
    "shojo-penonly": {
        "ja": "題材: 17歳くらいの少女の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。肩までの黒い巻き毛、白い丸襟のブラウスに細いリボン、カーディガン。本を両手で胸に抱え、少し伏し目がちに窓の外を見る。口は閉じる。正面からやや斜めを向く。 場所: 古い図書室の窓辺。本棚は簡単な線、窓の外の木は線だけ、空は白く残す。",
        "en": "Subject: A girl of about 17 seen from the waist up in a tall vertical composition, her whole head and both hands inside the picture, the surrounding background visible. Shoulder-length curly black hair, a white round-collared blouse with a thin ribbon, a cardigan. She holds a book against her chest with both hands and looks out of the window with slightly lowered eyes, mouth closed. Facing the viewer, turned slightly to one side. Setting: by the window of an old library: bookshelves as simple lines, the tree outside the window in line only, the sky left white.",
    },
    "seinen-plainreal": {
        "ja": "題材: 35歳くらいの太った男の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。ぼさぼさの短い髪、厚い眼鏡、無精ひげ、よれたパーカー。コンビニの袋を片手に下げ、もう片手で眼鏡を押し上げ、不安そうに横を見る。口は少し開く。正面からやや斜めを向く。 場所: 夜の住宅街の路地。電柱と塀は簡単な形、街灯の光の輪の外は暗いトーン。",
        "en": "Subject: A heavyset man of about 35 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Messy short hair, thick glasses, stubble, a rumpled hoodie. A convenience-store bag hangs from one hand; with the other he pushes his glasses up, glancing sideways uneasily, mouth slightly open. Facing the viewer, turned slightly to one side. Setting: a residential back street at night: utility poles and walls as simple shapes, dark tone outside the circle of a streetlight.",
    },
    "seinen-clumsy": {
        "ja": "題材: 40歳くらいの男の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。七三分けの髪、くたびれたスーツにネクタイ。事務机の前に立ち、両手に書類の束を持って、表情を変えずに正面を見る。口は閉じる。正面からやや斜めを向く。 場所: 小さな古い事務所。机・棚・電話・ファイルは簡単な形、壁の掲示は文字のない白い四角。",
        "en": "Subject: A man of about 40 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Hair parted neatly to one side, a worn suit and tie. He stands in front of an office desk holding a stack of papers in both hands and looks straight ahead without expression, mouth closed. Facing the viewer, turned slightly to one side. Setting: a small old office: desks, shelves, a telephone and files as simple shapes, notices on the wall as blank white rectangles.",
    },
    "gag-deadpan": {
        "ja": "題材: 45歳くらいの会社員の男の腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。短い髪、眼鏡、スーツにネクタイ。両手を体の横に下ろして立ち、表情を変えずに正面を見る。口は閉じる。正面からやや斜めを向く。 場所: 昼のバス停。標識の柱1本とベンチ1つだけで、ほかは白い紙。",
        "en": "Subject: A male office worker of about 45 seen from the waist up in a tall vertical composition, his whole head and both hands inside the picture, the surrounding background visible. Short hair, glasses, a suit and tie. He stands with both hands hanging at his sides and looks straight ahead without expression, mouth closed. Facing the viewer, turned slightly to one side. Setting: a bus stop by day: only one sign pole and one bench, the rest white paper.",
    },
    "yonkoma-mochi": {
        "ja": "題材: 5歳くらいの子どもの腰から上を縦長の構図で、周りの背景とともに。頭全体と両手が画面に収まる。丸いニット帽、厚手のセーター。両手を小さく上げて、目をうるませて小さく笑う。正面からやや斜めを向く。 場所: 昼の公園。遠くの木と雲は簡単な線、ベンチ1つ。",
        "en": "Subject: A child of about 5 seen from the waist up in a tall vertical composition, the whole head and both hands inside the picture, the surrounding background visible. A round knitted cap and a thick sweater. The child raises both little hands and smiles a small smile with teary eyes. Facing the viewer, turned slightly to one side. Setting: a park by day: distant trees and clouds as simple lines, one bench.",
    },
}
