# 高鐵 hsr 的圖片清單與提示詞（給 Gemini 用）

2026-11-03 寫好（第一版草稿，尚未修改）。共 11 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/hsr/index.html`，圖片放 `games/hsr/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲（包含台鐵）的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天是在高鐵台北站大廳（主角收到 LINE）；Ami 已經先到台中，所以結果／結局圖是 Ami 在高鐵台中站出口；服務櫃檯、票閘、指示牌、月台、候車位置、車廂各是不同場景。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。站務員、乘客也不露臉（背影、遠景，或在脖子處切掉）。
- **沒有可讀的文字**：招牌、價錢、電子看板、車票上的字都畫成空白或抽象線條（遊戲用文字卡片顯示車次、時間、停靠站）。
- **同一個遊戲場景要一致**：同一個服務櫃檯、同一節車廂，用已確認的圖當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 高鐵站大廳：很寬敞、明亮、天花板高，橘色與深灰色的現代感；有服務櫃檯（站務員在玻璃後面）和一排自動售票機；進站是一排自動票閘，紙本車票插進去。這是依印象畫的，**待確認**。
- 月台：有玻璃的月台安全門（月台門）、地上有一格一格的候車位置標線，天花板掛電子看板；高鐵列車是白色加橘色線條的子彈頭外型。
- 標準車廂座位：兩人座加三人座（2+3）、座椅有頭枕、行李架在上方。商務車廂較寬，座位是一人座加兩人座（1+2）。這個遊戲只畫標準車廂內部。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（站在高鐵台北站大廳，手機收到 Ami 的 LINE） | 無（文字生圖，第一張先做） |
| 2 | `counter.jpg` | COUNTER / SOLD / TK_CHECK / PAY / PAY_FIX / CHANGE（服務櫃檯） | 無（文字生圖） |
| 3 | `ticket.jpg` | TICKET（拿到車票，看印得對不對） | 上傳已確認的 counter.jpg（編輯式） |
| 4 | `gate.jpg` | GATE（票閘） | 無（文字生圖） |
| 5 | `signs.jpg` | DIRECTION（過了票閘，兩個指示牌：南下、北上） | 無（文字生圖） |
| 6 | `platform.jpg` | BOARD（月台，抬頭看旅客資訊看板） | 無（文字生圖） |
| 7 | `spot.jpg` | CAR（月台上的候車位置標線） | 上傳已確認的 platform.jpg（編輯式） |
| 8 | `seat.jpg` | SEAT（車廂裡找到位子） | 無（文字生圖） |
| 9 | `result.jpg` | RESULT（Ami 在台中站出口等你，看手機收到成果） | 無（文字生圖＋Ami 頭肩參考圖） |
| 10 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 11 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing straight ahead across the spacious, bright main concourse of a Taiwan High Speed Rail station, slightly looking down at the phone. A pair of plain, ordinary bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible) holds a smartphone in the lower part of the frame; the phone screen shows only abstract blank chat-bubble shapes. Far ahead: a service counter and a row of ticket vending machines with blank signs, a wide high ceiling with orange accents, a few travelers with suitcases seen from behind and far away. No faces of any person, no readable text anywhere.
```

## 2. counter.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing straight at the service counter of a Taiwan High Speed Rail station, about 1 m away. Behind the counter a station staff member in a plain dark-gray and orange uniform stands, cropped at the neck so no face is visible. On the counter: a small tray for money, a ticket printer, a computer monitor showing only abstract blank lines. In the lower foreground, one plain bare hand (no ring, no watch, no nail polish, no sleeve visible) rests on the counter edge. Blank signs, no readable text anywhere.
```

## 3. ticket.jpg

```
Edit the attached image (the confirmed service counter). Keep the counter, the staff member (no face), colors, 16-bit pixel art illustration style and camera angle completely identical. Change only this: the plain bare hand in the foreground now holds a small pale-yellow paper train ticket (the printed lines on it are only abstract gray bars, no letters or numbers) just above the counter. No readable text.
```

## 4. gate.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing straight toward a row of automatic ticket gates of a Taiwan High Speed Rail station, about 2 m away. Escalators going up to the platforms are visible beyond the gates. One plain bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a small paper ticket near the right-hand gate's ticket slot. A blank overhead sign with abstract shapes, no letters. No faces, no readable text.
```

## 5. signs.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), just past the ticket gates of a Taiwan High Speed Rail station, looking straight ahead at two overhead direction signs that point left and right; each sign is a blank rectangle with only an abstract arrow shape and a simple colored stripe (orange for one, dark gray for the other), no letters or numbers. Escalators lead up on both sides. A few travelers seen from behind and far away. No hands in frame, no faces, no readable text.
```

## 6. platform.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing on a covered platform of a Taiwan High Speed Rail station and looking up and slightly to the left at an electronic passenger information board hanging from the roof; the board shows only abstract amber horizontal bars, no letters or numbers. Glass platform screen doors on the right, and behind them a sleek white bullet train with an orange stripe waiting. Painted boarding-position marks on the floor. A few waiting passengers seen from behind and far away. No faces, no readable text.
```

## 7. spot.jpg

```
Edit the attached image (the confirmed high-speed rail platform). Keep the platform, glass screen doors, train, colors, pixel-art style and camera height completely identical. Change only the camera: look straight down and slightly forward at the floor so that one painted boarding-position mark (an abstract rectangle with a simple blank number square, no digits) fills the lower half of the frame, with the glass screen door and the train in the upper half. A plain bare hand is not needed. No faces, no readable text.
```

## 8. seat.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), inside a Taiwan High Speed Rail standard-class car, looking down the aisle slightly toward the right at a window-side row of seats (two seats on the left of the aisle and three on the right). Gray-blue seats with headrests, luggage racks above, a bright window. One window seat in front is empty; a plain bare hand (no ring, no watch, no nail polish, no sleeve visible) rests on the seat-back. Seat numbers are blank small rectangles. No faces, no readable text.
```

## 9. result.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image. Camera at eye level, facing the character from the front, medium shot from the waist up. The character stands just outside the exit of a Taiwan High Speed Rail station in Taichung on a sunny day, looking at her smartphone with a happy, curious expression; she wears a different outfit from the reference (a plain light-blue jacket over a white top) and a small shoulder bag. Behind her: a modern wide station building with orange accents and a blank sign with no letters, a taxi and bus waiting area, a few potted trees. The phone screen shows only abstract blank chat bubbles. No readable text anywhere.
```

## 10. end_good.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. Same station-exit scene, camera angle and 16-bit pixel art style as the confirmed result.jpg. Change only this: she smiles broadly, holds her phone up to the camera with one hand and waves with the other. Keep everything else identical. No readable text.
```

## 11. end_bad.jpg

```
Edit the attached image (the confirmed end_good.jpg). Keep the station exit, camera angle, outfit, 16-bit pixel art style and the character's appearance (dark brown skin, long wavy black hair) completely identical. Change only her expression and pose: she looks worried, brows slightly raised, one hand holding the phone down at her chest, the other hand resting on her cheek. No readable text.
```
