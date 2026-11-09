# 菜市場：8 張菜的照片提示詞（給 Gemini 用）

2026-11-09 開始做。一次做一張，Ben 確認後再做下一張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的，整段複製貼上就能用。

## 規格
- 風格：**真實食物照片**（不是像素風），跟麵包店的麵包卡片同一種：食物特寫、佔滿畫面、柔和自然窗光、淺景深、背景模糊、色調偏暖。
- 正方形。Gemini 出圖後縮成 **480×480、JPG、品質約 84**，放到 `games/market/images/`，檔名照下表。缺哪張，遊戲就自動顯示 emoji。
- 沒有人、沒有手、沒有文字、沒有標籤、沒有價格牌、沒有商標。
- 拍攝方向（8 張都一樣，畫面才一致）：相機在食物前方約 40 公分、高度約 30 公分，往下約 45 度，食物置中。

## 做法（2026-11-09 改成九宮格一次出圖，Claude 自己切）
一張 3×3 九宮格，每格一種菜，Claude 切開、縮成 480×480 放進 `games/market/images/`。
格子順序（由左到右、由上到下）：

| 格 | 檔名 | 內容 |
|---|---|---|
| 1 | `item_pork.jpg` | 豬肉（梅花肉厚片）|
| 2 | `item_beef.jpg` | 牛肉 |
| 3 | `item_chicken.jpg` | 雞肉（雞腿）|
| 4 | `item_egg.jpg` | 雞蛋（一盒）|
| 5 | `item_fish.jpg` | 魚（一條）|
| 6 | `item_cabbage.jpg` | 高麗菜（一顆）|
| 7 | `item_bokchoy.jpg` | 小白菜（一把）|
| 8 | `item_tomato.jpg` | 番茄（三顆）|
| 9 | `basket.jpg` | 空的菜籃（備用，之後可當「籃子」圖）|

提示詞見對話；如果某一格畫得不好，再單獨重畫那一格。

## 第二批：新增 9 種（2026-11-09）九宮格提示詞
格子順序（由左到右、由上到下）：1 排骨 `item_rib` ／2 絞肉 `item_mince` ／3 雞腿 `item_leg` ／4 蝦 `item_shrimp` ／5 花枝 `item_squid` ／6 蛤蜊 `item_clam` ／7 螃蟹 `item_crab` ／8 玉米 `item_corn` ／9 洋蔥 `item_onion`。
Claude 切開、去掉背景的燈、縮成 360×360 JPG（跟第一批一樣）。

提示詞（整段複製）：
```
A single square image made of a clean 3x3 grid of nine separate realistic food photographs, separated by thin white gutters, no borders, no text, no labels, no prices, no logos, no people, no hands. Each cell is one close-up product photo, the food filling most of the cell, centered, shot from about 40 cm in front of the food, camera about 30 cm high, looking down at about 45 degrees. Soft natural window light, warm tone, shallow depth of field, blurred plain neutral background (a simple wooden or white tray surface), no light bulbs, no lamps, no windows and no other objects in the background. The same photographic style in all nine cells, like groceries at a Taiwanese traditional market. Cells, left to right, top to bottom: (1) raw pork spare ribs, cut into short pieces, on a white tray; (2) a mound of fresh raw ground pork, pink and slightly coarse; (3) two raw chicken drumsticks with skin, pale yellow; (4) a pile of fresh raw whole shrimp with shells, grey-blue and translucent; (5) one whole fresh cuttlefish, pale pinkish-white with tentacles, on crushed ice; (6) a handful of fresh clams in shells, brown and cream, slightly wet; (7) one whole raw crab, reddish-brown shell, claws tied or folded, on crushed ice; (8) two ears of fresh yellow corn, partly peeled husk showing the kernels; (9) two whole brown-skinned onions, one cut in half showing white layers.
```
