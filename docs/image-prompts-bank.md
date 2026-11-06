# 銀行 bank 的圖片清單與提示詞（給 Gemini 用）

2026-11-06 寫好（第一版草稿，尚未修改）。共 9 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/bank/index.html`，圖片放 `games/bank/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天是在家附近的街上（主角站在路邊收到 LINE，街角看得到銀行）；其餘關卡都在同一間銀行分行裡（大廳、取號機、填單桌、臨櫃窗口）；結果／結局圖是 Ami 在自己家門口。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。行員也不露臉（背影、側後方，或鏡頭把臉裁掉）。
- **沒有可讀的文字**：招牌、叫號螢幕、取號機按鈕、匯款單、存摺、鈔票面額都畫成空白或抽象線條（遊戲用文字卡片顯示號碼牌、帳號、金額、鈔票張數）。
- **同一個遊戲場景要一致**：同一間銀行，用已確認的 `lobby.jpg` 當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣的銀行分行大廳：入口附近有取號機，旁邊常有大廳服務的行員；一排候位椅；臨櫃窗口有玻璃隔板，上方有叫號螢幕；填單桌是站著寫字的高桌，筆用鏈子繫著。這是依印象畫的，**待確認**。
- 取號機螢幕上有「存款、提款、匯款」這類按鈕（遊戲內文字寫在劇情，圖上畫成空白按鈕）。
- 台幣鈔票：千元鈔偏棕色、百元鈔偏紅色；圖上只畫顏色與抽象圖案，不寫數字。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（家附近的街上，手機收到 Ami 的 LINE；街角看得到銀行） | 無（文字生圖，第一張先做） |
| 2 | `lobby.jpg` | ENTER（走進銀行大廳，行員站在取號機旁） | 無（文字生圖） |
| 3 | `ticket.jpg` | TICKET（取號機的螢幕） | 上傳已確認的 lobby.jpg（編輯式） |
| 4 | `table.jpg` | FORM（桌子上填匯款申請書，等叫號） | 上傳已確認的 lobby.jpg（編輯式） |
| 5 | `counter.jpg` | CALL / ID / REPEAT / WITHDRAW（臨櫃窗口前和行員說話） | 上傳已確認的 lobby.jpg（編輯式） |
| 6 | `cash.jpg` | CASH（點鈔票） | 上傳已確認的 counter.jpg（編輯式） |
| 7 | `result.jpg` | RESULT（Ami 在家門口收到成果訊息） | 無（文字生圖＋Ami 頭肩參考圖） |
| 8 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 9 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing along a quiet Taipei residential street, slightly looking down at the phone. A pair of plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the lower part of the frame; the phone screen shows only abstract blank chat-bubble shapes. Far ahead: low apartment buildings with blank signs, scooters parked at the curb, a mid-size bank building at the corner with an abstract blank sign band (no letters), a few pedestrians seen from behind and far away. No faces of any person, no readable text anywhere.
```

## 2. lobby.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing just inside the glass entrance of a Taiwan bank branch, looking straight into the lobby. Bright clean lobby with light floor tiles; on the left a freestanding ticket-number machine with a blank touch screen; a bank clerk in a uniform vest stands beside it, seen from three-quarter back or cropped at the chin, no face visible; in the background a row of customer chairs, a long counter with glass dividers and a few blank number display screens (abstract lines only). One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) is visible at the lower right. No faces of any person, no readable text anywhere.
```

## 3. ticket.jpg

```
Edit the attached image (the confirmed bank lobby). Keep the lobby, clerk (no face), colors, 16-bit pixel art style and camera height completely identical. Change only this: move the camera forward to stand right in front of the ticket-number machine; its touch screen shows three abstract blank button shapes in a column (no letters, no numbers); one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) reaches toward the middle button from the lower right. No faces, no readable text.
```

## 4. table.jpg

```
Edit the attached image (the confirmed bank lobby). Keep the lobby style, colors and 16-bit pixel art style identical. Change only this: the camera now looks down at a standing-height writing table with a pen on a small chain, and a blank bank form lying on it (abstract printed boxes and gray lines, no letters, no numbers); one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds the pen and writes in a box at the lower right; in the soft-focus background the row of customer chairs and the counter from the confirmed image. No faces, no readable text.
```

## 5. counter.jpg

```
Edit the attached image (the confirmed bank lobby). Keep the lobby style, colors and 16-bit pixel art style identical. Change only this: the camera now stands in front of one teller window, centered, at eye height, looking straight through the glass divider; the bank clerk behind the counter is seen cropped at the chin (no face), in a uniform vest, typing on a keyboard beside a blank computer screen; on the counter a passbook, a card-like resident certificate and a form lie (abstract blank shapes, no letters or numbers); one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rests at the lower right. No faces, no readable text.
```

## 6. cash.jpg

```
Edit the attached image (the confirmed teller window counter). Keep the bank interior, clerk (no face), colors, 16-bit pixel art style and camera position completely identical. Change only this: on the counter lie two neat stacks of banknotes, one of larger brownish bills and one of smaller reddish bills (abstract designs, no numbers, no letters), and a small plastic cash tray; one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) touches the top bill at the lower right as if counting. No faces, no readable text.
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
