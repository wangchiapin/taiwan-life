# 台鐵 train 的圖片清單與提示詞（給 Gemini 用）

2026-11-02 寫好（第一版草稿，尚未修改）。共 10 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/train/index.html`，圖片放 `games/train/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天是在台北車站大廳（主角收到 LINE）；Ami 已經先到新竹，所以結果／結局圖是 Ami 在新竹車站出口；售票窗口、驗票閘門、月台、車廂各是不同場景。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。售票員、乘客也不露臉（背影、遠景，或在脖子處切掉）。
- **沒有可讀的文字**：招牌、價錢、電子看板、車票上的字都畫成空白或抽象線條（遊戲用文字卡片顯示車次、時間、月台）。
- **同一個遊戲場景要一致**：同一個售票窗口、同一節車廂，用已確認的圖當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台鐵車站大廳：高天花板、一排售票窗口（玻璃隔板，下方有收錢小盤）、旁邊有自動售票機；進站有自動驗票閘門（可放紙本車票或刷悠遊卡）。
- 月台：黃色安全線、天花板下掛電子看板（時間、車種、車次、往哪裡、月台）。
- 自強號車廂：兩人座加兩人座（2+2）、藍色座椅、行李架在上方，座位號碼貼在椅背或扶手；區間車是長條座椅，這個遊戲不畫區間車。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（站在台北車站大廳，手機收到 Ami 的 LINE） | 無（文字生圖，第一張先做） |
| 2 | `counter.jpg` | COUNTER / SOLD / TK_CHECK / PAY / PAY_FIX / CHANGE（售票窗口） | 無（文字生圖） |
| 3 | `ticket.jpg` | TICKET（拿到車票，看印得對不對） | 上傳已確認的 counter.jpg（編輯式） |
| 4 | `gate.jpg` | GATE（驗票閘門） | 無（文字生圖） |
| 5 | `platform.jpg` | PLATFORM / CAR（月台，抬頭看電子看板） | 無（文字生圖） |
| 6 | `aisle.jpg` | CAR（走上車，車廂走道） | 無（文字生圖） |
| 7 | `seat.jpg` | SEAT（找到座位） | 上傳已確認的 aisle.jpg（編輯式） |
| 8 | `result.jpg` | RESULT（Ami 在新竹車站出口等你，看手機收到成果） | 無（文字生圖＋Ami 頭肩參考圖） |
| 9 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 10 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing straight ahead across the big main hall of Taipei Main Station, slightly looking down at the phone. A pair of plain, ordinary bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible) holds a smartphone in the lower part of the frame; the phone screen shows only abstract blank chat-bubble shapes. Far ahead: rows of blank ticket-window counters under a high ceiling, an electronic departure board with only abstract blank lines, travelers with suitcases seen from behind and far away. No faces of any person, no readable text anywhere.
```

## 2. counter.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing straight at a Taiwan Railway station ticket-window counter with a glass partition, about 1 m away. Behind the glass a ticket clerk in a plain railway uniform sits, cropped at the neck so no face is visible. On the counter: a small tray for money, a ticket printer, a computer monitor showing only abstract blank lines. In the lower foreground, one plain bare hand (no ring, no watch, no nail polish, no sleeve visible) rests on the counter edge. Blank signs, no readable text anywhere.
```

## 3. ticket.jpg

```
Edit the attached image (the confirmed ticket-window counter). Keep the counter, glass partition, clerk (no face), colors, 16-bit pixel art illustration style and camera angle completely identical. Change only this: the plain bare hand in the foreground now holds a small pale-yellow paper train ticket (the printed lines on it are only abstract gray bars, no letters or numbers) just above the counter. No readable text.
```

## 4. gate.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing straight toward a row of three Taiwan Railway automatic ticket gates inside a station concourse, about 2 m away. A stairway down to the platforms is visible beyond the gates. One plain bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a small paper ticket near the right-hand gate slot. A blank overhead sign with abstract shapes, no letters. No faces, no readable text.
```

## 5. platform.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing on a covered Taiwan Railway platform and looking up and slightly to the left at an electronic information board hanging from the roof; the board shows only abstract amber horizontal bars, no letters or numbers. A train waits on the track to the right with its doors open. A yellow safety line along the platform edge, a few waiting passengers seen from behind and far away. No faces, no readable text.
```

## 6. aisle.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), just inside the door of a Taiwan Railway express train car, facing straight down the center aisle. Rows of blue two-by-two seats on both sides, luggage racks above, a blank electronic sign above the far door. A few passengers seen only from behind (heads and shoulders, no faces). No hands in frame, no readable text anywhere.
```

## 7. seat.jpg

```
Edit the attached image (the confirmed train car). Keep the car interior, colors, pixel-art style and camera height completely identical. Change only the camera: move forward a few steps and turn slightly to the right so the view is directed at one window-side pair of seats, an empty seat in front and a plain bare hand (no ring, no watch, no nail polish, no sleeve visible) resting on the seat-back. The seat number plate is a blank small rectangle. No faces, no readable text.
```

## 8. result.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image. Camera at eye level, facing the character from the front, medium shot from the waist up. The character stands just outside the exit of a Taiwan station building in Hsinchu on a sunny day, looking at her smartphone with a happy, curious expression; she wears a different outfit from the reference (a plain light-green cardigan over a white top) and a small shoulder bag. Behind her: a blank station-exit sign with no letters, a taxi stand, a few potted trees. The phone screen shows only abstract blank chat bubbles. No readable text anywhere.
```

## 9. end_good.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. Same station-exit scene, camera angle and pixel-art style as the confirmed result.jpg. Change only this: she smiles broadly, holds her phone up to the camera with one hand and waves with the other. Keep everything else identical. No readable text.
```

## 10. end_bad.jpg

```
Edit the attached image (the confirmed end_good.jpg). Keep the station exit, camera angle, outfit, pixel-art style and the character's appearance (dark brown skin, long wavy black hair) completely identical. Change only her expression and pose: she looks worried, brows slightly raised, one hand holding the phone down at her chest, the other hand resting on her cheek. No readable text.
```
