# 菜市場：8 張菜的照片提示詞（給 Gemini 用）

2026-11-09 開始做。一次做一張，Ben 確認後再做下一張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的，整段複製貼上就能用。

## 規格
- 風格：**真實食物照片**（不是像素風），跟麵包店的麵包卡片同一種：食物特寫、佔滿畫面、柔和自然窗光、淺景深、背景模糊、色調偏暖。
- 正方形。Gemini 出圖後縮成 **480×480、JPG、品質約 84**，放到 `games/market/images/`，檔名照下表。缺哪張，遊戲就自動顯示 emoji。
- 沒有人、沒有手、沒有文字、沒有標籤、沒有價格牌、沒有商標。
- 拍攝方向（8 張都一樣，畫面才一致）：相機在食物前方約 40 公分、高度約 30 公分，往下約 45 度，食物置中。

## 順序
| 順序 | 檔名 | 內容 |
|---|---|---|
| 1 | `item_pork.jpg` | 豬肉（梅花肉厚片，約一斤）|
| 2 | `item_beef.jpg` | 牛肉 |
| 3 | `item_chicken.jpg` | 雞肉 |
| 4 | `item_egg.jpg` | 雞蛋（一盒）|
| 5 | `item_fish.jpg` | 魚（一條）|
| 6 | `item_cabbage.jpg` | 高麗菜（一顆）|
| 7 | `item_bokchoy.jpg` | 小白菜（一把）|
| 8 | `item_tomato.jpg` | 番茄 |

## 1. `item_pork.jpg`（豬肉）

```
Create a square (1:1) photorealistic food photograph, in the style of a bakery product photo: one single food item shown large, filling most of the frame, with soft natural window light coming from the left, shallow depth of field, a softly blurred warm background, slightly warm color tone, appetizing, sharp focus on the food. Subject: a thick slice of fresh raw Taiwanese pork shoulder (梅花肉), pink-red with thin white fat marbling, about 600 grams, lying on a clean, slightly worn round wooden chopping block at a traditional Taiwanese market stall. Camera: about 40 cm in front of the meat and about 30 cm above it, looking down at roughly 45 degrees, the meat centered in the frame. Background: a blurred traditional market stall with a warm hanging light bulb, nothing recognizable. No people, no hands, no text, no labels, no price tags, no logos, no watermark. Real photograph, not an illustration, not pixel art.
```
