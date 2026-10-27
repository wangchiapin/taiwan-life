# 新三個遊戲的圖片提示詞：麵店、超商購物、鹽酥雞（給 Gemini 用）

2026-10-27 寫好。三個遊戲共 23 張圖。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的，整段複製貼上就能用。

## 先看這裡：共通規則

- **一次做一個遊戲、一次做一張**：做完一張，Ben 確認，再做下一張。每個遊戲照下面的編號順序做（第一張是底圖，後面很多張要用它當底圖）。
- **底圖規則**：寫著「上傳已確認的 xxx.jpg（編輯式）」的，把那張圖一起上傳，再貼提示詞（提示詞已經寫成「保持全部一樣，只改…」）。同一個遊戲的圖才能互相當底圖；不要拿別的遊戲、別的地點的圖當底圖（Gemini 會連背景一起抄過去）。
- **Ami 參考圖**：從已推上去的飲料店遊戲 `games/drinks/images/end_good.jpg` 裁出 Ami 的頭和肩膀（只要人，不要辦公室背景）。start.jpg 的手機頭像和三張 end_good.jpg 都要附這張。提示詞裡已經寫了「只抄人物，背景和衣服不要」。
- **主角沒有性別**：第一人稱視角，只看得到雙手（普通的手，沒有戒指、手錶、手環、指甲油，看不到袖子），臉和身體不入鏡。店員、老闆是各遊戲自己的 NPC，Ami 的衣服每個遊戲可以不同。
- **沒有文字、沒有真的商標**：招牌、價目表、標籤都畫成空白或看不懂的線條。價格、金額、折數、袋子裡有什麼，都是遊戲用文字卡片顯示，圖上不能出現會跟它打架的內容。
- **第一張沒有參考圖**：畫風靠文字。如果畫風跟前面的遊戲差太多，跟我說，我調整提示詞；請不要自己拿別的遊戲的圖當參考。
- **畫風**：暖色 16-bit 像素風、正方形（跟冰淇淋、飲料店那批一致）。
- **檔案規格**：Gemini 出的 2048×2048 原圖，縮成 **720×720、JPG、品質約 84**，放到 `games/<遊戲>/images/`，檔名照下面寫的。缺哪張，遊戲就自動顯示表情符號。

## 台灣實景核對（我依一般台灣店家常見的樣子寫的，Ben 看過覺得不對的地方請直接說）

- **麵店（noodle）**：櫃台點餐；櫃台旁有玻璃小菜櫃（滷蛋、豆干、海帶、燙青菜，台灣人說的「黑白切／滷味」）；大湯鍋冒煙、長柄撈麵網；櫃台上有蔥花盒、辣椒醬；白色麵碗；背景是紅色塑膠椅和小圓桌；老闆圍裙、肩上掛毛巾。
- **超商購物（conbini）**：櫃台有收銀（POS）螢幕、手持掃描槍（掃手機載具條碼）、發票機；店員背後有微波爐、咖啡機；櫃台旁有關東煮鍋；店員穿背心；便當是黑色長方形盒加透明蓋；騎樓下停機車；買酒要滿十八歲、查證件。⚠️「結帳按按鈕抽折扣」是遊戲自己設計的玩法，台灣超商結帳時通常沒有這個按鈕，所以 draw.jpg 的按鈕是設計出來的道具。
- **鹽酥雞（yansuji）**：傍晚的鹽酥雞攤：玻璃櫃裡一籃一籃的生料；後面是油鍋和長柄撈網；櫃台上有胡椒鹽、辣椒粉罐，一排小碗（蔥花、蒜末、洋蔥丁）；白色紙袋加紅色塑膠袋；竹籤；老闆戴帽子、圍裙、袖套、薄手套；雞排用剪刀剪成條。

---

## 麵店（noodle）　→ `games/noodle/images/`

**劇情**：Ami 用 LINE 交代要點什麼（麵種、大小碗、辣度、蔥、小菜、內用外帶）。你走進一間台灣街邊小麵店，在櫃台跟老闆點餐，老闆複誦、端麵、結帳找錢，最後吃到麵（或老闆弄錯被你抓到）。

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `shop.jpg` | NOODLE、SIZE、SPICY、SCAL、EAT、ORDER_CHECK（點餐、複誦的主畫面） | 無（文字生圖，第一張先做） |
| 2 | `side.jpg` | SIDE（老闆問要不要加小菜） | 上傳已確認的 shop.jpg（編輯式） |
| 3 | `bowl.jpg` | HANDOVER（老闆把麵端上來，你要核對對不對） | 上傳已確認的 shop.jpg（編輯式） |
| 4 | `pay.jpg` | PAY、PAY_FIX、CHANGE（報價、付錢、找錢） | 上傳已確認的 shop.jpg（編輯式） |
| 5 | `start.jpg` | START（走到店門口，手機收到 Ami 的 LINE） | 無（文字生圖）；Ami 的臉用「Ami 參考圖」（見上面共通規則） |
| 6 | `result.jpg` | RESULT（成績頁） | 上傳已確認的 start.jpg（編輯式） |
| 7 | `end_good.jpg` | END（全對的結局：Ami 開心） | Ami 參考圖（從已推上去的飲料店 end_good.jpg 裁頭肩） |
| 8 | `end_bad.jpg` | END（有錯的結局：Ami 尷尬） | 上傳已確認的 end_good.jpg（編輯式） |

### noodle 1. `shop.jpg`

- 用在：NOODLE、SIZE、SPICY、SCAL、EAT、ORDER_CHECK（點餐、複誦的主畫面）
- 底圖：無（文字生圖，第一張先做）
- 檢查重點：老闆在正中央；左邊小菜櫃、右邊大湯鍋；櫃台上有蔥花和辣椒醬；雙手在畫面下緣；沒有可讀文字；沒有性別明確的主角。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Scene: inside a small everyday Taiwanese street noodle shop at midday, seen from the customer's side of the counter. Camera: first-person, standing at the counter at eye level (about 150 cm above the floor), looking straight ahead at the owner who stands about 1.5 meters away behind the counter; the camera is perfectly level (no tilt), the owner is centered, and the top edge of the stainless-steel counter runs across the lower third of the frame. The owner: a friendly middle-aged man with short black hair, a white short-sleeve shirt, a dark green apron and a small towel over one shoulder, smiling, both hands resting on the counter. On the left side of the counter: a glass display cabinet of braised side dishes (brown braised eggs, squares of dried tofu, strips of dark seaweed, and a plate of blanched green vegetables). On the right side: a big stainless-steel stockpot with rising steam, a long-handled noodle strainer basket hanging beside it, and a stack of plain white noodle bowls. On the counter in front of the owner: a small steel tray of chopped scallions and a jar of red chili paste. Behind the owner: a wide wooden menu board with unreadable squiggle lines. Far background on the left: a few red plastic stools and a small round table. Tiled floor. The view is the player's own first-person point of view: the player's two plain bare hands are visible at the bottom of the frame (neutral skin tone, no rings, no watch, no bracelet, no nail polish, no sleeves). The player's face and body are never shown. No readable text anywhere: every sign, menu board, price tag and label is blank or shows only unreadable squiggle lines; no real brand logos.
```

### noodle 2. `side.jpg`

- 用在：SIDE（老闆問要不要加小菜）
- 底圖：上傳已確認的 shop.jpg（編輯式）
- 檢查重點：還是同一間店、同一個老闆；小菜櫃變成主角，四種小菜看得清楚；老闆用手比向小菜櫃。若整個房間被重畫，重來一次。

```
Edit the attached image. Keep the same shop, the same owner (face, hair, clothes), the same objects, the same lighting and the same pixel-art style, and change ONLY the camera framing: move the camera about one step closer and turn it about 30 degrees to the left (still first-person, eye level about 150 cm, perfectly level with no tilt) so the glass display cabinet of braised side dishes fills the center-right of the frame, with the braised eggs, squares of dried tofu, strips of dark seaweed and a plate of blanched greens all clearly visible, each with a small blank price tag. The owner now stands just behind and beside the cabinet, smiling and gesturing toward it with one open hand. The player's two plain bare hands stay at the bottom of the frame (no rings, no watch, no nail polish, no sleeves). No readable text.
```

### noodle 3. `bowl.jpg`

- 用在：HANDOVER（老闆把麵端上來，你要核對對不對）
- 底圖：上傳已確認的 shop.jpg（編輯式）
- 檢查重點：碗裡的料不要畫得太清楚（遊戲會另外用文字卡片顯示蔥、辣、小菜，圖不能跟它打架）；蒸氣蓋住配料。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: the owner is now setting a steaming bowl of noodles down on the counter toward the player with both hands, smiling. It is a plain white Taiwanese noodle bowl with noodles in it, and white steam rises from it and partly hides the toppings — show no specific toppings (no visible scallions, no egg, no chili oil). A pair of chopsticks rests on the counter beside the bowl. The player's two plain bare hands stay at the bottom of the frame, open and ready to receive the bowl. No readable text.
```

### noodle 4. `pay.jpg`

- 用在：PAY、PAY_FIX、CHANGE（報價、付錢、找錢）
- 底圖：上傳已確認的 shop.jpg（編輯式）
- 檢查重點：鈔票只有顏色，沒有可讀數字或人像（金額由遊戲的文字顯示）；老闆手掌向上伸出。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: the owner now holds out one open palm over the counter toward the player, as if asking for payment, still smiling. The player's right hand holds out two or three paper banknotes fanned slightly (red, green and brown tones like Taiwan's banknotes, with no readable numbers and no portraits), and the player's left hand rests on the counter. Both hands are plain and bare (no rings, no watch, no nail polish, no sleeves). No readable text.
```

### noodle 5. `start.jpg`

- 用在：START（走到店門口，手機收到 Ami 的 LINE）
- 底圖：無（文字生圖）；Ami 的臉用「Ami 參考圖」（見上面共通規則）
- 檢查重點：街邊麵店正面、正對；右下角手機上的圓形頭像看得出是 Ami（長黑髮、深褐膚色）；雙手沒有飾品。這張完成後，result.jpg 用它當底圖。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Scene: the front of a small everyday Taiwanese street noodle shop at midday, with a covered sidewalk arcade, an open front where the glass cabinet of braised side dishes and a steaming stockpot are visible inside, a blank hanging shop sign, a couple of red plastic stools and a small round table on the sidewalk, scooters parked at both edges, and a narrow strip of asphalt street in the foreground. Camera: first-person, standing at the edge of the street about 5 meters from the shop, eye level (about 150 cm), looking straight at the storefront, perfectly level (no tilt), the shop centered. In the lower right, the player's right hand holds up a smartphone upright, screen facing the player, showing a LINE-style chat: two white speech bubbles on the left and one green bubble on the right, all filled with unreadable squiggles, and a small round profile picture next to the white bubbles that shows Ami's face (long wavy black hair, deep brown skin). The player's left hand hangs relaxed at the bottom left. The player's face and body are never shown; hands are plain and bare (neutral skin tone, no rings, no watch, no bracelet, no nail polish, no sleeves). The attached reference image shows Ami (head and shoulders). Copy only the character — her face, deep brown skin and long wavy black hair — and ignore the reference image's background and clothes. No readable text anywhere: every sign, menu board, price tag and label is blank or shows only unreadable squiggle lines; no real brand logos.
```

### noodle 6. `result.jpg`

- 用在：RESULT（成績頁）
- 底圖：上傳已確認的 start.jpg（編輯式）
- 檢查重點：只剩店面和空馬路；手和手機都不見了；其他一模一樣。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: remove the smartphone and both of the player's hands completely, and fill the space behind them with the empty street and sidewalk that would naturally be there. The result is just the empty storefront scene. No readable text.
```

### noodle 7. `end_good.jpg`

- 用在：END（全對的結局：Ami 開心）
- 底圖：Ami 參考圖（從已推上去的飲料店 end_good.jpg 裁頭肩）
- 檢查重點：臉、膚色、長波浪黑髮要跟飲料店的 Ami 一模一樣；背景是單純米色；筷子和蒸氣不要太搶。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Head-and-shoulders portrait of Ami, centered, facing the camera straight on at eye level, camera perfectly level, on a plain flat cream background (no scenery). The attached reference image shows Ami (head and shoulders). Copy only the character — her face, deep brown skin and long wavy black hair — and ignore the reference image's background and clothes. Outfit: an olive-green zip jacket over a cream t-shirt, with a brown patterned woven shoulder strap crossing her chest. Expression: delighted, a big open-mouth smile, bright eyes. She holds a pair of wooden chopsticks up near her shoulder, with a small curl of white steam beside them. No readable text, no logos.
```

### noodle 8. `end_bad.jpg`

- 用在：END（有錯的結局：Ami 尷尬）
- 底圖：上傳已確認的 end_good.jpg（編輯式）
- 檢查重點：只有表情變了（尷尬、一滴汗）；衣服、髮型、背景、筷子都不變。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: her expression becomes awkward and a little disappointed — eyebrows tilted up in the middle, a small closed-mouth wry smile, and one blue sweat drop on her cheek. The chopsticks stay in her hand, held a little lower. Her outfit, pose, hair, face shape and the plain cream background stay exactly the same.
```

---

## 超商購物（conbini）　→ `games/conbini/images/`

**劇情**：Ami 用 LINE 交代要買便當、啤酒、泡麵。你在泡麵架比兩種特價哪個兩份比較便宜，到櫃台回答加熱、買酒出示證件、手機載具、按按鈕抽折扣，最後算錢、付錢、找錢、拿發票。

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `counter.jpg` | HEAT、ALCOHOL、CARRIER、CARRIER_CHECK（櫃台結帳的主畫面） | 無（文字生圖，這個遊戲先做這張） |
| 2 | `shelf.jpg` | PROMO（泡麵架上比兩種特價哪個比較便宜） | 無（文字生圖，另一個位置，不要拿 counter.jpg 當參考） |
| 3 | `draw.jpg` | DRAW（按按鈕抽折扣） | 上傳已確認的 counter.jpg（編輯式） |
| 4 | `pay.jpg` | PAY、PAY_FIX、CHANGE（看螢幕報價、付錢、找錢） | 上傳已確認的 counter.jpg（編輯式） |
| 5 | `start.jpg` | START（走到超商門口，手機收到 Ami 的 LINE） | 無（文字生圖）；Ami 的臉用「Ami 參考圖」 |
| 6 | `result.jpg` | RESULT（成績頁） | 上傳已確認的 start.jpg（編輯式） |
| 7 | `end_good.jpg` | END（全對的結局：Ami 開心） | Ami 參考圖（從已推上去的飲料店 end_good.jpg 裁頭肩） |
| 8 | `end_bad.jpg` | END（有錯的結局：Ami 尷尬） | 上傳已確認的 end_good.jpg（編輯式） |

### conbini 1. `counter.jpg`

- 用在：HEAT、ALCOHOL、CARRIER、CARRIER_CHECK（櫃台結帳的主畫面）
- 底圖：無（文字生圖，這個遊戲先做這張）
- 檢查重點：店員在正中央；櫃台上有便當、一瓶茶、兩杯泡麵（不要放啤酒，因為不買酒的局也用這張）；沒有真的品牌商標；雙手在畫面下緣。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Scene: behind the checkout counter of a Taiwanese convenience store in the early evening, seen from the customer's side. Camera: first-person, standing at the counter at eye level (about 150 cm above the floor), looking straight ahead at the clerk who stands about 1.2 meters away behind the counter; the camera is perfectly level (no tilt), the clerk is centered, and the top edge of the counter runs across the lower third of the frame. The clerk: a friendly young person with a black ponytail, wearing a plain striped vest with no logo over a white shirt, smiling. On the counter in front of the clerk: a black rectangular bento box with a clear lid, a plastic bottle of tea, and two instant-noodle cups. On the right side of the counter: a customer-facing point-of-sale screen showing only an abstract pale panel, a handheld barcode scanner on its stand, and a small receipt printer. On the left side of the counter: a steaming stainless-steel pot of oden with skewers and a ladle. Behind the clerk: two microwave ovens on a shelf, a coffee machine, and shelves of small goods. Bright white ceiling lights, pale tiled floor. The view is the player's own first-person point of view: the player's two plain bare hands are visible at the bottom of the frame (neutral skin tone, no rings, no watch, no bracelet, no nail polish, no sleeves). The player's face and body are never shown. No readable text anywhere: every sign, menu board, price tag and label is blank or shows only unreadable squiggle lines; no real brand logos.
```

### conbini 2. `shelf.jpg`

- 用在：PROMO（泡麵架上比兩種特價哪個比較便宜）
- 底圖：無（文字生圖，另一個位置，不要拿 counter.jpg 當參考）
- 檢查重點：兩種泡麵明顯不同、各有一張特價標籤（沒有可讀字）；一手提著籃子；畫面簡單乾淨。價格由遊戲的文字卡片顯示，圖上不要有數字。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Scene: the instant-noodle aisle inside a Taiwanese convenience store in the early evening. Camera: first-person, standing in the aisle about 60 cm from the shelf, eye level (about 150 cm above the floor), looking straight at the shelf, perfectly level (no tilt), the shelf fills the frame. On the central shelf: two clearly different kinds of instant noodles side by side — on the left, neat stacks of red cup noodles; on the right, neat stacks of yellow-and-blue bowl noodles — and each stack has a bright starburst-shaped promotion tag with unreadable marks. Shelves above and below hold assorted snacks drawn in a simpler, less detailed way. Bright white ceiling lights, pale tiled floor. At the bottom left, the player's left hand holds a small red plastic shopping basket with a bento box and a drink bottle in it; at the bottom right, the player's right hand reaches toward the shelf. Both hands are plain and bare (neutral skin tone, no rings, no watch, no bracelet, no nail polish, no sleeves); the player's face and body are never shown. No readable text anywhere: every sign, menu board, price tag and label is blank or shows only unreadable squiggle lines; no real brand logos.
```

### conbini 3. `draw.jpg`

- 用在：DRAW（按按鈕抽折扣）
- 底圖：上傳已確認的 counter.jpg（編輯式）
- 檢查重點：螢幕只有抽象的彩色光芒，沒有數字或文字（折扣是幾折由遊戲文字顯示）；按鈕是紅色圓形大按鈕；手指懸在按鈕上方。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: the customer-facing point-of-sale screen now shows an abstract bright rainbow starburst (no text, no numbers), and a small round red push button on a little stand sits on the counter in front of the screen. The clerk smiles and gestures toward the button with one open hand. The player's right index finger hovers just above the button, about to press it, and the player's left hand rests on the counter. Both hands are plain and bare (no rings, no watch, no nail polish, no sleeves). No readable text.
```

### conbini 4. `pay.jpg`

- 用在：PAY、PAY_FIX、CHANGE（看螢幕報價、付錢、找錢）
- 底圖：上傳已確認的 counter.jpg（編輯式）
- 檢查重點：螢幕是空白的亮面（金額由遊戲文字顯示）；店員手掌向上；鈔票沒有可讀數字。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: the clerk now holds out one open palm over the counter toward the player, as if asking for payment, still smiling; the point-of-sale screen shows only a plain blank bright panel with no text and no numbers. The player's right hand holds out two or three paper banknotes fanned slightly (red, green and brown tones like Taiwan's banknotes, with no readable numbers and no portraits), and the player's left hand rests on the counter. Both hands are plain and bare (no rings, no watch, no nail polish, no sleeves). No readable text.
```

### conbini 5. `start.jpg`

- 用在：START（走到超商門口，手機收到 Ami 的 LINE）
- 底圖：無（文字生圖）；Ami 的臉用「Ami 參考圖」
- 檢查重點：正面、正對的超商外觀；招牌色帶不能有真的商標；右下角手機頭像看得出是 Ami。這張完成後，result.jpg 用它當底圖。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Scene: the front of a typical Taiwanese convenience store in the early evening, with a floor-to-ceiling glass front, a pair of automatic sliding glass doors in the center, bright white interior light showing shelves inside, a horizontal sign band in generic green, white and orange stripes with no logo and no text, a covered sidewalk arcade, a few scooters parked at both edges, and a narrow strip of asphalt street in the foreground. Camera: first-person, standing at the edge of the street about 5 meters from the store, eye level (about 150 cm), looking straight at the storefront, perfectly level (no tilt), the doors centered. In the lower right, the player's right hand holds up a smartphone upright, screen facing the player, showing a LINE-style chat: two white speech bubbles on the left and one green bubble on the right, all filled with unreadable squiggles, and a small round profile picture next to the white bubbles that shows Ami's face (long wavy black hair, deep brown skin). The player's left hand hangs relaxed at the bottom left. The player's face and body are never shown; hands are plain and bare (neutral skin tone, no rings, no watch, no bracelet, no nail polish, no sleeves). The attached reference image shows Ami (head and shoulders). Copy only the character — her face, deep brown skin and long wavy black hair — and ignore the reference image's background and clothes. No readable text anywhere: every sign, menu board, price tag and label is blank or shows only unreadable squiggle lines; no real brand logos.
```

### conbini 6. `result.jpg`

- 用在：RESULT（成績頁）
- 底圖：上傳已確認的 start.jpg（編輯式）
- 檢查重點：只剩店面和空馬路；手和手機都不見了；其他一模一樣。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: remove the smartphone and both of the player's hands completely, and fill the space behind them with the empty street and sidewalk that would naturally be there. The result is just the empty storefront scene. No readable text.
```

### conbini 7. `end_good.jpg`

- 用在：END（全對的結局：Ami 開心）
- 底圖：Ami 參考圖（從已推上去的飲料店 end_good.jpg 裁頭肩）
- 檢查重點：臉、膚色、長波浪黑髮要跟飲料店的 Ami 一模一樣；背景單純米色；塑膠袋上沒有真的商標。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Head-and-shoulders portrait of Ami, centered, facing the camera straight on at eye level, camera perfectly level, on a plain flat cream background (no scenery). The attached reference image shows Ami (head and shoulders). Copy only the character — her face, deep brown skin and long wavy black hair — and ignore the reference image's background and clothes. Outfit: a light gray hoodie, with a brown patterned woven shoulder strap crossing her chest. Expression: delighted, a big open-mouth smile, bright eyes. She holds up a white plastic shopping bag in one hand, with the top of a bento box and a drink can peeking out of it (no logos, no text on the bag). No readable text, no logos.
```

### conbini 8. `end_bad.jpg`

- 用在：END（有錯的結局：Ami 尷尬）
- 底圖：上傳已確認的 end_good.jpg（編輯式）
- 檢查重點：只有表情變了（尷尬、一滴汗）；衣服、髮型、背景、塑膠袋都不變。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: her expression becomes awkward and a little disappointed — eyebrows tilted up in the middle, a small closed-mouth wry smile, and one blue sweat drop on her cheek. The shopping bag stays in her hand, held a little lower. Her outfit, pose, hair, face shape and the plain cream background stay exactly the same.
```

---

## 鹽酥雞（yansuji）　→ `games/yansuji/images/`

**劇情**：Ami 用 LINE 交代要買什麼（鹽酥雞、雞排、甜不辣、四季豆、米血、杏鮑菇、薯條，各幾份）、雞排切不切、辣不辣、蔥蒜洋蔥要不要。你在鹽酥雞攤一樣一樣點，老闆複誦、現炸、裝袋，最後結帳找錢。

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `stall.jpg` | ITEM、CUT、SPICY、TOPS、ORDER_CHECK（點餐、複誦的主畫面） | 無（文字生圖，這個遊戲先做這張） |
| 2 | `bag.jpg` | HANDOVER（老闆把裝好的袋子遞給你，你要核對） | 上傳已確認的 stall.jpg（編輯式） |
| 3 | `pay.jpg` | PAY、PAY_FIX、CHANGE（報價、付錢、找錢） | 上傳已確認的 stall.jpg（編輯式） |
| 4 | `start.jpg` | START（走到鹽酥雞攤前，手機收到 Ami 的 LINE） | 無（文字生圖）；Ami 的臉用「Ami 參考圖」 |
| 5 | `result.jpg` | RESULT（成績頁） | 上傳已確認的 start.jpg（編輯式） |
| 6 | `end_good.jpg` | END（全對的結局：Ami 開心） | Ami 參考圖（從已推上去的飲料店 end_good.jpg 裁頭肩） |
| 7 | `end_bad.jpg` | END（有錯的結局：Ami 尷尬） | 上傳已確認的 end_good.jpg（編輯式） |

### yansuji 1. `stall.jpg`

- 用在：ITEM、CUT、SPICY、TOPS、ORDER_CHECK（點餐、複誦的主畫面）
- 底圖：無（文字生圖，這個遊戲先做這張）
- 檢查重點：老闆在正中央；玻璃櫃裡的料看得出七種之中的幾種；一排小碗（蔥、蒜、洋蔥）和辣椒粉罐在櫃台上；沒有可讀文字。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Scene: a Taiwanese fried-chicken street stall (yansuji) under a covered sidewalk at dusk, seen from the customer's side of the counter, with warm hanging bulbs and a dim blue evening street far in the background. Camera: first-person, standing at the counter at eye level (about 150 cm above the floor), looking straight ahead at the owner who stands about 1.3 meters away behind the counter; the camera is perfectly level (no tilt), the owner is centered, and the top edge of the glass display counter runs across the lower third of the frame. The owner: a friendly middle-aged woman wearing a cap, a dark apron, long arm sleeves and thin disposable gloves, smiling, holding a pair of tongs. The glass display counter in front holds metal baskets of raw ingredients: flat chicken cutlets, small pieces of chicken, tan tianbula pieces, green beans, brownish rice-cake cubes, sliced king oyster mushrooms and french fries. On top of the counter, on the owner's side: a row of small bowls holding chopped scallions, minced garlic and diced onion, two stainless shakers of pepper salt and chili powder, a pair of kitchen scissors, and a stack of white paper bags. Behind the owner: a big round deep fryer with bubbling oil and a wire strainer basket hanging beside it, and a blank signboard. The view is the player's own first-person point of view: the player's two plain bare hands are visible at the bottom of the frame (neutral skin tone, no rings, no watch, no bracelet, no nail polish, no sleeves). The player's face and body are never shown. No readable text anywhere: every sign, menu board, price tag and label is blank or shows only unreadable squiggle lines; no real brand logos.
```

### yansuji 2. `bag.jpg`

- 用在：HANDOVER（老闆把裝好的袋子遞給你，你要核對）
- 底圖：上傳已確認的 stall.jpg（編輯式）
- 檢查重點：袋子是白色紙袋（有一點油漬）、外面套紅色塑膠袋；看不到裡面的東西（遊戲會另外用文字卡片顯示袋子內容）。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: the owner now holds out a packed order across the counter toward the player with both hands, smiling: a white paper bag with a few faint oil spots and a little steam rising from it, the top folded over and stapled, sitting inside a thin red plastic carrier bag. The contents are not visible. The tongs are put down on the counter. The player's two plain bare hands stay at the bottom of the frame, open and ready to receive the bag (no rings, no watch, no nail polish, no sleeves). No readable text.
```

### yansuji 3. `pay.jpg`

- 用在：PAY、PAY_FIX、CHANGE（報價、付錢、找錢）
- 底圖：上傳已確認的 stall.jpg（編輯式）
- 檢查重點：鈔票只有顏色，沒有可讀數字；老闆手掌向上伸出。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: the owner now holds out one open palm over the counter toward the player, as if asking for payment, still smiling, with the tongs put down. The player's right hand holds out two or three paper banknotes fanned slightly (red, green and brown tones like Taiwan's banknotes, with no readable numbers and no portraits), and the player's left hand rests on the counter. Both hands are plain and bare (no rings, no watch, no nail polish, no sleeves). No readable text.
```

### yansuji 4. `start.jpg`

- 用在：START（走到鹽酥雞攤前，手機收到 Ami 的 LINE）
- 底圖：無（文字生圖）；Ami 的臉用「Ami 參考圖」
- 檢查重點：傍晚的攤位正面；右下角手機頭像看得出是 Ami。這張完成後，result.jpg 用它當底圖。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Scene: the front of a Taiwanese fried-chicken street stall (yansuji) at dusk, under a covered sidewalk arcade: a glass display counter with baskets of raw ingredients, a big round deep fryer with a little steam, warm hanging bulbs glowing, a blank signboard with a simple cartoon drumstick icon and no text, a couple of plastic stools, scooters parked at both edges, and a narrow strip of asphalt street in the foreground under a dim blue evening sky. Camera: first-person, standing at the edge of the street about 5 meters from the stall, eye level (about 150 cm), looking straight at the stall, perfectly level (no tilt), the stall centered. In the lower right, the player's right hand holds up a smartphone upright, screen facing the player, showing a LINE-style chat: two white speech bubbles on the left and one green bubble on the right, all filled with unreadable squiggles, and a small round profile picture next to the white bubbles that shows Ami's face (long wavy black hair, deep brown skin). The player's left hand hangs relaxed at the bottom left. The player's face and body are never shown; hands are plain and bare (neutral skin tone, no rings, no watch, no bracelet, no nail polish, no sleeves). The attached reference image shows Ami (head and shoulders). Copy only the character — her face, deep brown skin and long wavy black hair — and ignore the reference image's background and clothes. No readable text anywhere: every sign, menu board, price tag and label is blank or shows only unreadable squiggle lines; no real brand logos.
```

### yansuji 5. `result.jpg`

- 用在：RESULT（成績頁）
- 底圖：上傳已確認的 start.jpg（編輯式）
- 檢查重點：只剩攤位和空馬路；手和手機都不見了；其他一模一樣。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: remove the smartphone and both of the player's hands completely, and fill the space behind them with the empty street and sidewalk that would naturally be there. The result is just the empty stall scene. No readable text.
```

### yansuji 6. `end_good.jpg`

- 用在：END（全對的結局：Ami 開心）
- 底圖：Ami 參考圖（從已推上去的飲料店 end_good.jpg 裁頭肩）
- 檢查重點：臉、膚色、長波浪黑髮要跟飲料店的 Ami 一模一樣；背景單純米色；紙袋上沒有可讀文字。

```
Cozy 16-bit pixel art illustration, square 1:1 image, clean chunky pixel outlines, soft warm color palette, warm gentle lighting, the look of a charming Taiwan-life pixel-art game. Head-and-shoulders portrait of Ami, centered, facing the camera straight on at eye level, camera perfectly level, on a plain flat cream background (no scenery). The attached reference image shows Ami (head and shoulders). Copy only the character — her face, deep brown skin and long wavy black hair — and ignore the reference image's background and clothes. Outfit: a light blue denim jacket over a mustard-yellow knit top, with a brown patterned woven shoulder strap crossing her chest. Expression: delighted, a big open-mouth smile, bright eyes. She holds up a white paper bag with a few faint oil spots and a little steam in one hand, close to her shoulder (no text on the bag). No readable text, no logos.
```

### yansuji 7. `end_bad.jpg`

- 用在：END（有錯的結局：Ami 尷尬）
- 底圖：上傳已確認的 end_good.jpg（編輯式）
- 檢查重點：只有表情變了（尷尬、一滴汗）；衣服、髮型、背景、紙袋都不變。

```
Edit the attached image. Keep everything identical — the same place, the same layout, the same characters (face, hair, clothes), the same lighting, the same pixel-art style, the same camera angle and framing — and change ONLY the following: her expression becomes awkward and a little disappointed — eyebrows tilted up in the middle, a small closed-mouth wry smile, and one blue sweat drop on her cheek. The paper bag stays in her hand, held a little lower. Her outfit, pose, hair, face shape and the plain cream background stay exactly the same.
```
