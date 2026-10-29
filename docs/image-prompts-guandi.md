# 關帝廟 guandi 的圖片清單與提示詞（給 Gemini 用）

2026-10-29 寫好。共 16 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的，整段複製貼上就能用。
遊戲程式在 `games/guandi/index.html`，圖片放 `games/guandi/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 先看這裡：共通規則（和麵店、超商、鹽酥雞那批一致）

- **一次做一張**：做完一張，Ben 確認，再做下一張。照下面的編號順序做（第 1 張是底圖，後面很多張用它當底圖）。
- **底圖規則**：寫著「上傳已確認的 xxx.jpg（編輯式）」的，把那張圖一起上傳，再貼提示詞（提示詞已經寫成「保持全部一樣，只改…」）。只拿同一個遊戲的圖互相當底圖；不要拿別的遊戲的圖當底圖。
- **Ami 參考圖**：從已推上去的飲料店遊戲 `games/drinks/images/end_good.jpg` 裁出 Ami 的頭和肩膀（只要人，不要背景）。`start.jpg` 手機頭像和 `end_good.jpg` 都要附這張。提示詞裡已寫「只抄人物，背景和衣服不要」。
- **主角沒有性別**：第一人稱視角，只看得到雙手（普通的手，沒有戒指、手錶、手環、指甲油，看不到袖子），臉和身體不入鏡。
- **Ami 全程陪伴**：遊戲裡 Ami 只在旁邊陪，不幫忙。所以圖裡 Ami 不要比手勢、不要指東西；要出現時就是站在主角旁邊看著。
- **沒有可讀的文字、沒有真的神像臉**：匾額、告示牌、籤詩、登記單、價目牌都畫成空白或看不懂的線條（遊戲用文字卡片顯示內容）。神像只畫成「穿紅綠袍的坐像」的剪影感，臉部模糊；不要畫成特定的真實神像或寺廟。
- **畫風**：暖色 16-bit 像素風、正方形（跟飲料店、冰淇淋那批一致）。
- **檔案規格**：Gemini 出的 2048×2048 原圖，縮成 **720×720、JPG、品質約 84**，放到 `games/guandi/images/`，檔名照下面寫的。

## 台灣實景核對（依一般台灣關帝廟常見的樣子寫的，Ben 看過覺得不對的地方請直接說）

- **三個門**：台灣廟宇正面（三川殿）通常有三個門：**中門**平常關著，是給神明、或大典時才開的；**右邊（面對廟）是龍邊，從這裡進**；**左邊是虎邊，從這裡出**。龍門、虎門的門板或牆面常有龍、虎的彩繪或浮雕。
- **龍進虎出**的方向都是「面對廟」看。從廟裡面往外走時，虎邊的門在你的**右手邊**（因為你背對神明、面向外面），遊戲選項裡已經寫了「面對廟，在左邊」，圖不要畫反。
- **天公爐**：在廟的最前面（前殿外面或前殿門口），一個大銅香爐，面向天空／大殿；先在這裡拜天公。
- **主殿**：關聖帝君坐像在最裡面正中央，前面是供桌、大香爐；神像穿紅袍（綠袍也有）、長鬍子（臉要模糊）；旁邊常有周倉、關平（可不畫）。
- **點火處**：廟門口旁邊有一個點香用的小爐或點火台；香架上整齊插著線香；有些廟有告示牌寫「請勿用嘴吹香」。
- **筊杯**：紅色、像半個月亮的一對木頭杯（一面平、一面圓），放在供桌上。
- **籤筒與籤櫃**：竹籤筒（細長竹籤）在供桌旁邊；旁邊有小抽屜的木頭**籤櫃**，抽屜上有號碼；廟公／志工從抽屜拿出籤詩紙。
- **光明燈**：登記處（服務台）桌上有登記單和簽字筆；牆上有成排的小燈座（光明燈），每盞下面一張紅紙。
- **平安符**：另一張小桌，放著一堆小紅袋平安符，旁邊有投香油錢的紅色箱子，沒有人看守（自己拿）。
- **過爐**：在大香爐上方，把平安符拿在手上，順時針繞三圈，煙在往上飄。

---

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `gate.jpg` | GATE（廟門口三個門，選要走哪個門） | 無（文字生圖，第一張先做） |
| 2 | `exit.jpg` | EXIT（拜完要離開，選要走哪個門） | 上傳已確認的 gate.jpg（編輯式） |
| 3 | `start.jpg` | START（站在廟門口，手機收到 Ami 的 LINE） | 無（文字生圖）；Ami 臉用「Ami 參考圖」 |
| 4 | `fire.jpg` | FIRE（在點火處把香點著，要熄火） | 上傳已確認的 gate.jpg（編輯式） |
| 5 | `heaven.jpg` | HEAVEN（天公爐前面，先拜天公） | 上傳已確認的 gate.jpg（編輯式） |
| 6 | `main.jpg` | MAIN（主殿裡，站在關公神像前說話） | 無（文字生圖，主殿第一張） |
| 7 | `throw.jpg` | THROW（供桌上的筊杯，丟筊） | 上傳已確認的 main.jpg（編輯式） |
| 8 | `draw.jpg` | DRAW（籤筒，抽籤） | 上傳已確認的 main.jpg（編輯式） |
| 9 | `cabinet.jpg` | SLIP_NUM（籤櫃，廟公拿籤詩紙給你） | 上傳已確認的 main.jpg（編輯式） |
| 10 | `read.jpg` | READ（手裡拿著籤詩紙，Ami 在旁邊） | 上傳已確認的 main.jpg（編輯式） |
| 11 | `desk.jpg` | REGISTER、PAY、PAY_FIX、CHANGE（光明燈登記處，付錢找錢） | 無（文字生圖，登記處第一張） |
| 12 | `amulet.jpg` | AMULET（桌上一堆平安符和香油錢箱） | 上傳已確認的 desk.jpg（編輯式） |
| 13 | `guolu.jpg` | GUOLU（大香爐上方過爐） | 上傳已確認的 main.jpg（編輯式） |
| 14 | `result.jpg` | RESULT（成績頁） | 上傳已確認的 start.jpg（編輯式） |
| 15 | `end_good.jpg` | END（錯 2 次以內：Ami 笑，輕鬆） | Ami 參考圖（從飲料店 end_good.jpg 裁頭肩） |
| 16 | `end_bad.jpg` | END（錯比較多：Ami 溫柔安慰） | 上傳已確認的 end_good.jpg（編輯式） |

> 有些關卡暫時共用圖：PAY、PAY_FIX、CHANGE 都用 `desk.jpg`。「廟公被抓到說錯時的尷尬表情」`*_sorry.jpg` 這版先不做（程式也還沒接），之後要加再說。

---

### 1. `gate.jpg`

- 用在：GATE（廟門口三個門）
- 檢查重點：三個門都看得到；右邊（龍邊）門板有龍的彩繪、左邊（虎邊）門板有虎的彩繪，中間大門關著；右邊那個門是開的；告示牌是空白；雙手在畫面下緣；沒有可讀文字。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle morning light, the look of a charming Taiwan-life pixel-art game. Scene: the front of a traditional Taiwanese temple, seen from outside in the temple courtyard. Camera: first-person, standing about 8 meters in front of the temple at eye level (about 150 cm above the ground), looking straight at the temple front; the camera is perfectly level (no tilt) and the temple is centered. The temple front has a curved red-tiled roof with small upturned ceramic decorations, red pillars, and THREE doorways side by side: the big middle door is closed and shut; the door on the RIGHT side of the frame has a painted dragon on its door panels and is open; the door on the LEFT side of the frame has a painted tiger on its door panels and is also visible. A blank wooden sign stands at the right-hand door. A large plain wooden plaque (no text, just empty dark wood) hangs above the middle door. Stone paving in the foreground. The player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) hang in the lower part of the frame. No readable text anywhere, no logos.
```

### 2. `exit.jpg`

- 用在：EXIT
- 底圖：上傳已確認的 gate.jpg（編輯式）
- 檢查重點：這次是在廟裡面往外看（背對神明）；三個門還在；虎邊的門（面對廟時在左邊，所以從裡面看是在畫面**右邊**）；不要畫反。

```
Edit the attached image. Keep the same temple, the same pixel-art style and the same warm lighting, and change ONLY the camera position: now the camera is standing just INSIDE the temple, at the front hall, looking OUT toward the courtyard at the three doorways from the inside (the player has their back to the main hall). The big middle door is closed. From this inside view, the tiger-painted door is on the RIGHT side of the frame and the dragon-painted door is on the LEFT side of the frame (they are the same doors as before, seen from behind). A soft afternoon light comes through the doorways. Keep the player's two plain bare hands at the bottom of the frame. No readable text.
```

### 3. `start.jpg`

- 用在：START（廟門口，手機收到 Ami 的 LINE）
- 檢查重點：手機螢幕是 LINE 聊天介面但沒有可讀文字；Ami 的頭像是她的臉；背景是廟門口；手是普通的手。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle morning light, the look of a charming Taiwan-life pixel-art game. Scene: first-person view of a plain bare hand (no rings, no watch, no nail polish, no sleeve) holding a smartphone at chest height; the phone screen shows a messaging-app chat with a small round avatar of a friendly young woman at the top and three green speech bubbles filled with unreadable squiggle lines. Behind the phone, slightly out of focus, is the red-pillared front of a traditional Taiwanese temple with a curved red-tiled roof. Use the attached reference image ONLY for the young woman's face and hair in the small avatar; do not copy its background or clothes. No readable text anywhere.
```

### 4. `fire.jpg`

- 用在：FIRE
- 底圖：上傳已確認的 gate.jpg（編輯式）
- 檢查重點：還是同一間廟；畫面是廟門口旁邊的點火處；雙手拿著三炷香，香頭有小火；香架上有線香；沒有用嘴吹的動作。

```
Edit the attached image. Keep the same temple, the same pixel-art style and the same warm lighting, and change ONLY the camera framing: move the camera to the right-hand side of the temple entrance, one step from a small stone incense-lighting stand, looking at it at chest height. On the stand a small flame burns; to the side is a wooden rack holding neat rows of unlit incense sticks. The player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) hold three incense sticks over the flame, the tips glowing with small orange flames. A blank wooden sign stands next to the stand. The painted dragon door is visible softly in the background. No readable text.
```

### 5. `heaven.jpg`

- 用在：HEAVEN
- 底圖：上傳已確認的 gate.jpg（編輯式）
- 檢查重點：天公爐是一個大銅香爐，在前面；後面看得到大殿入口；雙手拿香；Ami 在旁邊看著（可選，不要比手勢）。

```
Edit the attached image. Keep the same temple, the same pixel-art style and the same warm lighting, and change ONLY the camera framing: move the camera inside the front courtyard, close to a large round bronze incense burner standing on a stone base facing the main hall (this is the burner for the Heavenly Emperor). Thin incense smoke rises from it. Behind it, the open doorway of the main hall shows warm red light inside. The player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) hold three incense sticks in front of the chest. A friendly young woman with shoulder-length hair stands a little to the right, just watching quietly with a gentle smile, her hands at her sides (use the attached Ami reference ONLY for her face and hair, not for background or clothes — if no reference is attached, draw a generic friendly young woman). No readable text.
```

### 6. `main.jpg`

- 用在：MAIN（主殿，面對關公神像）
- 檢查重點：神像坐在正中央，穿紅袍、長鬍子，臉模糊；供桌上有香爐、水果、蠟燭；兩側有紅柱；雙手拿香；沒有可讀文字。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle candlelight, the look of a charming Taiwan-life pixel-art game. Scene: the main hall of a traditional Taiwanese Guan Gong (Lord Guan) temple. Camera: first-person, standing about 3 meters in front of the main altar at eye level (about 150 cm), looking straight ahead; perfectly level, centered. In the center of the altar sits a statue of a bearded deity in a red robe with a green sash, hands in front, his face intentionally soft and unspecific (not a real statue). In front of him: a long red-and-gold offering table with a big bronze incense burner in the middle, plates of fruit, two red candles, and a pair of red crescent-shaped wooden divination blocks on the right end of the table. Red pillars on both sides, hanging red lanterns, golden carved panels. Thin incense smoke. The player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) hold three incense sticks at the bottom of the frame. A friendly young woman stands a bit to the right of the player, quietly watching with a calm smile, hands at her sides (Ami reference for face and hair only). No readable text; plaques are blank.
```

### 7. `throw.jpg`

- 用在：THROW
- 底圖：上傳已確認的 main.jpg（編輯式）
- 檢查重點：筊杯是紅色半月形，一對；一個在手上，或剛落在地上，**不要讓畫面決定聖筊／笑筊／陰筊**（結果由遊戲的卡片顯示，圖要看不出結果）。

```
Edit the attached image. Keep the same hall, the same altar, the same pixel-art style and the same warm lighting, and change ONLY the framing: lower the camera slightly and tilt it a little downward, so the lower half of the frame shows the player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) holding a pair of red crescent-shaped wooden divination blocks together at waist height, the blocks held so that their faces are NOT clearly visible (seen from the side or from above, with no clear flat/round result). The altar and the red candle glow blurred in the upper background. The young woman stays at the right edge, quietly watching. No readable text.
```

### 8. `draw.jpg`

- 用在：DRAW
- 底圖：上傳已確認的 main.jpg（編輯式）
- 檢查重點：竹籤筒在供桌旁邊或桌上；雙手拿著籤筒輕輕搖，一支細竹籤從筒口往上冒出來；籤上沒有可讀文字。

```
Edit the attached image. Keep the same hall, the same altar, the same pixel-art style and the same warm lighting, and change ONLY the camera framing: move the camera a step to the right and lower it slightly so a round bamboo fortune-stick holder (a tall cylinder holding many thin bamboo sticks) fills the center of the frame. The player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) hold the holder at both sides and tilt it gently; one thin bamboo stick has just risen out of the top a little higher than the others. The sticks have only blank red tips (no numbers, no text). The altar is softly blurred behind. No readable text.
```

### 9. `cabinet.jpg`

- 用在：SLIP_NUM
- 底圖：上傳已確認的 main.jpg（編輯式）
- 檢查重點：木頭籤櫃有很多小抽屜（每個抽屜有小黃銅把手，號碼看不清楚）；一個抽屜被拉開；一位廟公（中年男人，穿簡單的白襯衫、深色背心）站在籤櫃旁邊，手裡拿著一張紙（空白或看不懂的線條）；你的手裡拿著一支籤。

```
Edit the attached image. Keep the same hall, the same pixel-art style and the same warm lighting, and change ONLY the camera framing and the people: the camera now faces a tall dark-wood cabinet full of tiny square drawers, each with a small brass handle and a tiny blank paper label. One drawer is pulled open. Standing next to the cabinet is the temple keeper: a friendly middle-aged man with short black hair, a plain white short-sleeve shirt and a dark vest, holding a single slip of paper (blank, only unreadable squiggle lines) toward the camera with both hands. In the lower part of the frame the player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) hold one thin bamboo stick. No readable text, no numbers.
```

### 10. `read.jpg`

- 用在：READ
- 底圖：上傳已確認的 main.jpg（編輯式）
- 檢查重點：手裡拿著一張窄長形的紙（籤詩紙），上面是**看不懂的線條**（遊戲另外顯示詩）；Ami 在旁邊，微笑，看著紙，沒有指東西；背景是大殿柔焦。

```
Edit the attached image. Keep the same hall, the same pixel-art style and the same warm lighting, and change ONLY the framing: the camera is at chest height, closer; the player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) hold a tall narrow strip of pale paper with only unreadable vertical squiggle lines on it, at the center of the frame. The young woman (Ami) stands at the right side, leaning in slightly, looking at the paper with a gentle smile, her hands at her sides (not pointing). The red-and-gold altar is softly blurred behind. No readable text.
```

### 11. `desk.jpg`

- 用在：REGISTER、PAY、PAY_FIX、CHANGE
- 檢查重點：廟的服務台（木頭桌）；桌上有登記單（空白格子）、毛筆或原子筆、一個紅色小銀行盤；廟公坐在桌後；牆上有成排的小光明燈座（紅色，每盞下面一張空白紅紙）；雙手在畫面下緣。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Scene: the service desk of a traditional Taiwanese temple, next to the main hall. Camera: first-person, standing at the desk at eye level (about 150 cm), looking straight at the temple keeper who sits about 1 meter away behind a wooden desk; perfectly level, centered. The temple keeper: a friendly middle-aged man with short black hair, a plain white short-sleeve shirt and a dark vest, smiling, both hands on the desk. On the desk: a blank registration form with empty boxes, a pen, a small red tray for money, and a small calculator. Behind him on the wall: neat rows of tiny red lamp holders (the kind used for blessing lamps), each with a blank red paper tag, softly glowing. The player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) rest at the bottom of the frame. No readable text, no numbers.
```

### 12. `amulet.jpg`

- 用在：AMULET
- 底圖：上傳已確認的 desk.jpg（編輯式）
- 檢查重點：沒有人看守這張桌子；桌上一堆小紅袋平安符；旁邊一個紅色的香油錢箱（上面有投錢的縫）；Ami 站在旁邊看著，沒有幫忙拿。

```
Edit the attached image. Keep the same temple, the same pixel-art style and the same warm lighting, and change ONLY the framing: move the camera a few steps to the side to a small separate wooden table by the wall, with NO temple keeper in the frame. On the table: a neat pile of small red cloth protection charms on strings, and next to them a red wooden donation box with a coin slot on top. The player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) reach toward the pile. The young woman (Ami) stands at the right edge, watching with a calm smile, her hands at her sides. The lamp wall is faintly visible in the far background. No readable text.
```

### 13. `guolu.jpg`

- 用在：GUOLU
- 底圖：上傳已確認的 main.jpg（編輯式）
- 檢查重點：大香爐在畫面中央，煙往上飄；手拿著小紅袋平安符，在爐上方；有一個圓形的箭頭（順時針）**不要畫**，動作由文字說明。

```
Edit the attached image. Keep the same hall, the same pixel-art style and the same warm lighting, and change ONLY the framing: the camera is at chest height, close to the big bronze incense burner in the main hall; thin incense smoke rises from many burning sticks. The player's two plain bare hands (no rings, no watch, no nail polish, no sleeves) hold a small red cloth protection charm on a string just above the burner, over the smoke. The altar and red candles are softly blurred behind. No arrows, no readable text.
```

### 14. `result.jpg`

- 用在：RESULT
- 底圖：上傳已確認的 start.jpg（編輯式）
- 檢查重點：手機螢幕變成成績／清單樣子（看不懂的線條、一個小星星圖案）；背景還是廟門口。

```
Edit the attached image. Keep the same hand, the same phone, the same temple in the background and the same pixel-art style, and change ONLY the phone screen: it now shows a simple report-card layout with a small row of yellow stars at the top and several short unreadable lines below, and the chat bubbles and avatar are gone. No readable text.
```

### 15. `end_good.jpg`

- 用在：END（錯 2 次以內）
- 底圖：Ami 參考圖
- 檢查重點：Ami 在廟門口，開心、輕鬆地笑；背景是廟門（紅柱、龍邊門）；Ami 的衣服可以和飲料店不同；沒有文字。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle golden afternoon light, the look of a charming Taiwan-life pixel-art game. Scene: a friendly young woman (Ami) stands at the front of a traditional Taiwanese temple, just outside the tiger-painted left doorway, smiling happily and looking relaxed, one hand lifted in a small wave toward the camera. Use the attached reference image ONLY for her face, hair and general look; do not copy its background or clothes. She wears a light jacket and a small shoulder bag. Behind her: the red pillars and curved red-tiled roof of the temple, soft clouds. Camera: first-person at eye level, about 2.5 meters from her, perfectly level, centered. No readable text.
```

### 16. `end_bad.jpg`

- 用在：END（錯比較多）
- 底圖：上傳已確認的 end_good.jpg（編輯式）
- 檢查重點：還是同一個 Ami、同一個地點；表情變成溫柔、有點不好意思地笑（不是難過）；手改成輕輕拍拍的姿勢或放在身側。

```
Edit the attached image. Keep the same woman (face, hair, clothes, bag), the same temple, the same lighting and the same pixel-art style, and change ONLY her expression and pose: she now gives a gentle, slightly sheepish smile with soft eyebrows, one hand lightly rubbing the back of her neck, the other at her side, as if comforting a friend after a messy day. No readable text.
```
