# 自助洗衣店 laundry 的圖片清單與提示詞（給 Gemini 用）

2026-11-08 寫好（第一版草稿，尚未修改）。共 9 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/laundry/index.html`，圖片放 `games/laundry/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天是在家裡（客廳地上一堆髒衣服）；其餘關卡都在同一間自助洗衣店裡（一排洗衣機、烘衣機、櫃檯、摺衣桌、等候椅）；結果／結局圖是 Ami 在自己家門口。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。店員也不露臉（背影、側後方，或鏡頭把臉裁掉）。
- **沒有可讀的文字**：招牌、價格、螢幕、公告都畫成空白或抽象線條（遊戲用文字卡片顯示金額）。
- **同一個遊戲場景要一致**：同一間洗衣店，用已確認的 `shop.jpg` 當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣的自助洗衣店：明亮、白色或淺色磁磚地，一排前開式洗衣機（下排）和烘衣機（疊在上面或另一側），機台正面有小螢幕和投幣孔，牆邊有摺衣桌、塑膠椅、洗衣精販賣機，有的有櫃檯。這是依印象畫的，**待確認**。
- 洗衣機是前開式、圓形玻璃門；烘衣機也是圓門，機台上的數字和字都畫成空白。
- 店員是否常駐待確認；圖上店員只在櫃檯後面、不露臉。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（在家，手機收到 Ami 的 LINE，地上一堆髒衣服） | 無（文字生圖，第一張先做） |
| 2 | `shop.jpg` | ENTER（走進洗衣店，一排洗衣機，店員在櫃檯後） | 無（文字生圖） |
| 3 | `coins.jpg` | COINS（櫃檯前換零錢，遞鈔票、收硬幣） | 上傳已確認的 shop.jpg（編輯式） |
| 4 | `washer.jpg` | LOAD / WASHSET / INSERT（洗衣機前放衣服、看螢幕、投幣） | 上傳已確認的 shop.jpg（編輯式） |
| 5 | `wait.jpg` | WAIT（坐在椅子上等，洗衣機轉動） | 上傳已確認的 shop.jpg（編輯式） |
| 6 | `dryer.jpg` | DRYSET / DRYPAY / TAKEOUT（烘衣機前設定、投幣、拿衣服） | 上傳已確認的 washer.jpg（編輯式） |
| 7 | `result.jpg` | RESULT（Ami 在家門口收到成果訊息） | 無（文字生圖＋Ami 頭肩參考圖） |
| 8 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 9 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), in a small Taipei apartment living room, looking slightly downward at a big pile of crumpled clothes (T-shirts, jeans, socks, plain colors, no logos) on the floor next to a laundry basket. A pair of plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the lower part of the frame; the phone screen shows only abstract blank chat-bubble shapes. Soft daylight from a window on the left. No faces of any person, no readable text anywhere.
```

## 2. shop.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing just inside the glass door of a bright, clean Taiwan self-service laundromat, looking straight toward the back wall. A row of front-loading washing machines with round glass doors along the back wall (small blank screens and coin slots on their fronts), dryers stacked on the right side, a folding table and plastic chairs on the left, a small service counter at the far right with a shop clerk in a plain apron seen from three-quarter back or cropped at the chin, no face visible. Light floor tiles, white walls. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a bag of laundry at the lower right. No faces of any person, no readable text anywhere.
```

## 3. coins.jpg

```
Edit the attached image (the confirmed laundromat). Keep the shop, clerk (no face), colors, 16-bit pixel art style and camera height completely identical. Change only this: the camera now stands in front of the service counter at the right, looking across it at eye height; on the counter lies a plain banknote (abstract design, no numbers) and a small stack of ten identical round coins; the clerk's hand pushes the coins toward the viewer. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) is held out at the lower right. No faces of any person, no readable text anywhere.
```

## 4. washer.jpg

```
Edit the attached image (the confirmed laundromat). Keep the shop, colors and 16-bit pixel art style identical. Change only this: the camera now stands about one meter in front of one empty front-loading washing machine in the middle of the row, at chest height, looking straight at its round open glass door and the small blank screen and coin slot above it; one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a few T-shirts and jeans near the open door at the lower right, with a few round coins in the other palm. No faces of any person, no readable text anywhere.
```

## 5. wait.jpg

```
Edit the attached image (the confirmed laundromat). Keep the shop, colors and 16-bit pixel art style identical. Change only this: the camera sits on a plastic chair at the left side, at seated eye height (about 1.1 m), looking toward the row of machines where one washing machine's round glass door shows colorful clothes tumbling with soapy water; one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rests on the knee at the lower edge holding a smartphone with an abstract blank screen. No faces of any person, no readable text anywhere.
```

## 6. dryer.jpg

```
Edit the attached image (the confirmed washer.jpg). Keep the shop, colors, camera height and 16-bit pixel art style identical. Change only this: the camera now stands in front of a stacked dryer (round glass door at chest height, a small blank display and coin slot beside it), the door is open and warm, slightly wrinkled clothes (T-shirts, jeans, socks) are being pulled out onto a folding table next to it; one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) reaches in at the lower right. No faces of any person, no readable text anywhere.
```

## 7. result.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image. Camera at eye level, facing the character from the front, medium shot from the waist up. She stands in the doorway of her apartment in Taipei, wearing a plain mustard cardigan over a white top, holding her smartphone in one hand and reading it with a calm, pleased expression. Behind her: a tidy entryway with a shoe cabinet and shoes, warm afternoon light. The phone screen shows only abstract blank chat bubbles. No readable text anywhere.
```

## 8. end_good.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. Same doorway scene, camera angle and 16-bit pixel art style as the confirmed result.jpg. Change only this: she smiles warmly and gives a thumbs-up with her free hand while holding the phone with the other. Keep everything else identical. No readable text.
```

## 9. end_bad.jpg

```
Edit the attached image (the confirmed end_good.jpg). Keep the doorway scene, camera angle, outfit, 16-bit pixel art style and the character's appearance (dark brown skin, long wavy black hair) completely identical. Change only her expression and pose: she looks worried, brows slightly raised, the phone held down at her chest, the other hand resting on her cheek. No readable text.
```
