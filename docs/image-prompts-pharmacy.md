# 藥局 pharmacy 的圖片清單與提示詞（給 Gemini 用）

2026-11-05 寫好（第一版草稿，尚未修改）。共 8 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/pharmacy/index.html`，圖片放 `games/pharmacy/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天是在家附近的街上（主角站在路邊收到 LINE）；其餘關卡都在街角的小藥局櫃檯前；結果／結局圖是 Ami 在自己家門口（她感冒在家休息）。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。藥師也不露臉（背影、側後方，或鏡頭把臉裁掉）。
- **沒有可讀的文字**：招牌、藥盒、說明書、價目、收銀螢幕都畫成空白或抽象線條（遊戲用文字卡片顯示品名、吃法、價錢）。
- **同一個遊戲場景要一致**：同一間藥局，用已確認的 `inside.jpg` 當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣的社區藥局：櫃檯後面是穿白袍的藥師，牆上貨架有各種藥盒、保健品，櫃檯上有玻璃展示櫃；招牌常有綠色十字，這裡畫成抽象符號、不寫字。這是依印象畫的，**待確認**。
- 藥盒外盒內有說明書（仿單），上面寫用法用量；這裡簡化成「說明書」一張紙。
- 家門口：一般台灣公寓的玄關，有鞋櫃和鞋子。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（家附近的人行道，手機收到 Ami 的 LINE） | 無（文字生圖，第一張先做） |
| 2 | `inside.jpg` | ENTER / SYMPTOM / ALLERGY / ASK / WARN（在藥局櫃檯前和藥師說話） | 無（文字生圖） |
| 3 | `box.jpg` | PICK（核對藥盒上的品名） | 上傳已確認的 inside.jpg（編輯式） |
| 4 | `label.jpg` | DOSE（核對說明書上的吃法） | 上傳已確認的 box.jpg（編輯式） |
| 5 | `counter.jpg` | PAY / PAY_FIX / CHANGE（付錢、找錢） | 上傳已確認的 inside.jpg（編輯式） |
| 6 | `result.jpg` | RESULT（Ami 在家門口收到成果訊息） | 無（文字生圖＋Ami 頭肩參考圖） |
| 7 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 8 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing along a quiet Taipei residential street, slightly looking down at the phone. A pair of plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the lower part of the frame; the phone screen shows only abstract blank chat-bubble shapes. Far ahead: low apartment buildings with blank signs, scooters parked at the curb, a small shop with a green cross-shaped abstract symbol (no letters) down the street, a few pedestrians seen from behind and far away. No faces of any person, no readable text anywhere.
```

## 2. inside.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing in front of the counter of a small Taiwan neighborhood pharmacy, centered, looking straight at the counter. Behind the counter the pharmacist is seen from behind-three-quarter angle or cropped at the chin, wearing a white coat, no face visible, reaching toward a shelf. Wall shelves behind with rows of abstract colored medicine boxes (blank, no text), a glass display case on the counter with small boxes, bright white-green lighting. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rests on the counter edge at the lower right. No faces of any person, no readable text anywhere.
```

## 3. box.jpg

```
Edit the attached image (the confirmed pharmacy counter). Keep the pharmacy interior, the pharmacist seen from behind (no face), colors, 16-bit pixel art style and camera position completely identical. Change only this: move the camera slightly forward and down so a single medicine box lies on the counter in the center of the frame, its front showing only abstract blank colored bands and a plain white label area (no letters, no numbers), one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holding the box edge at the lower right. No faces, no readable text.
```

## 4. label.jpg

```
Edit the attached image (the confirmed medicine box on the counter). Keep the pharmacy counter, colors, 16-bit pixel art style and camera height completely identical. Change only this: the box is now opened and a folded instruction leaflet lies next to it, unfolded, showing only abstract gray lines and a small blank pill-icon table (no letters, no numbers); one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) points at the leaflet from the lower right. No faces, no readable text.
```

## 5. counter.jpg

```
Edit the attached image (the confirmed pharmacy counter). Keep the pharmacy interior, colors, 16-bit pixel art style and camera position completely identical. Change only this: on the counter lie a small white paper bag, a box of throat lozenges and the medicine box; the pharmacist (seen from behind-three-quarter, no face) holds out a hand with abstract paper bills and coins (blank, no numbers); in the lower foreground one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a banknote. A small blank cash register screen (abstract lines only). No faces, no readable text.
```

## 6. result.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image. Camera at eye level, facing the character from the front, medium shot from the waist up. She stands in the doorway of her apartment in Taipei, wearing a plain gray cardigan over a white top, a thin scarf around her neck, holding a small white paper pharmacy bag in one hand and looking at her smartphone in the other with a relieved expression. Behind her: a tidy entryway with shoes, warm afternoon light. The phone screen shows only abstract blank chat bubbles. No readable text anywhere.
```

## 7. end_good.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. Same doorway scene, camera angle and 16-bit pixel art style as the confirmed result.jpg. Change only this: she smiles warmly, holds the pharmacy bag up toward the camera and waves her other hand. Keep everything else identical. No readable text.
```

## 8. end_bad.jpg

```
Edit the attached image (the confirmed end_good.jpg). Keep the doorway scene, camera angle, outfit, 16-bit pixel art style and the character's appearance (dark brown skin, long wavy black hair) completely identical. Change only her expression and pose: she looks worried, brows slightly raised, one hand holding the pharmacy bag down at her chest, the other hand resting on her cheek. No readable text.
```
