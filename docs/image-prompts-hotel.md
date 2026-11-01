# 飯店 hotel 的圖片清單與提示詞（給 Gemini 用）

2026-11-01 寫好（第一版草稿，尚未修改）。共 9 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/hotel/index.html`，圖片放 `games/hotel/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天在 Ami 家裡或街上，不是在飯店櫃台；櫃台、房間、電話分別是不同場景。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子也不要露出有性別的款式）。櫃台人員、房務員也不露臉（背影、剪影、或在脖子處切掉）。
- **沒有可讀的文字**：招牌、價錢、螢幕、房卡上的字都畫成空白或抽象線條（遊戲用文字卡片顯示內容）。
- **同一個遊戲場景要一致**：同一間房間／同一個櫃台，用已確認的圖當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣商務／平價旅館的大廳不大：玻璃自動門、櫃台後方有牆面和一排房卡格、櫃台上有一個小鈴和一台電腦螢幕、旁邊有一個行李推車。
- 房間：雙人床白色床單、床頭櫃上有**房間電話**（有分機按鍵）、牆上有冷氣面板（遙控器放在床頭）、書桌上有吹風機（常掛在浴室或書桌抽屜）、迷你冰箱（迷你吧）、浴室有淋浴間。
- 房務員穿制服，推房務車（上面有毛巾和備品）。
- 退房時在櫃台把房卡放在櫃台上，櫃台用電腦結帳。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（站在飯店門口，手機收到 Ami 的 LINE） | 無（文字生圖，第一張先做） |
| 2 | `desk.jpg` | DESK / DESK_CHECK / CHECKOUT（櫃台辦入住與退房） | 無（文字生圖） |
| 3 | `room.jpg` | ROOM（走進房間，冷氣、吹風機、浴室） | 無（文字生圖） |
| 4 | `phone.jpg` | REPORT1 / REPORT2 / ROOMNO / HK_CHECK（在房間裡拿起電話） | 上傳已確認的 room.jpg（編輯式） |
| 5 | `housekeeper.jpg` | HK_DONE（房務員站在房門口） | 上傳已確認的 room.jpg（編輯式） |
| 6 | `checkout.jpg` | CHECKOUT（把房卡放在櫃台上；選用，沒有時用 desk.jpg 的話可略過） | 上傳已確認的 desk.jpg（編輯式） |
| 7 | `result.jpg` | RESULT（Ami 在家看手機收到成果） | 無（文字生圖＋Ami 頭肩參考圖） |
| 8 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳 result.jpg 已確認的版本＋Ami 參考圖 |
| 9 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

> 檔名 `checkout.jpg` 若沒有做，遊戲會自動顯示 emoji；也可以把程式裡的 CHECKOUT 圖改成 `desk.jpg`（程式屬於修改階段，這次先不動）。

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing straight ahead toward the glass automatic door of a small Taiwanese business hotel entrance, slightly looking down at the phone. A pair of plain, ordinary bare hands (no rings, no watch, no bracelet, no nail polish, no sleeves visible) holds a smartphone in the lower part of the frame; the phone screen shows only abstract blank chat-bubble shapes, no readable text. Beyond the glass door: a small lobby with a front desk in the far background, a luggage cart, a potted plant. Above the door, a blank hotel sign with no letters. Daytime street light. No faces of any person, no text anywhere.
```

## 2. desk.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing straight at a Taiwanese hotel front desk counter, about 1.5 m away. Behind the counter a front-desk staff member stands, cropped at the neck so no face is visible, wearing a plain dark vest and white shirt. On the counter: a small service bell, a computer monitor showing only abstract blank lines, a tray of blank key cards. On the wall behind: a rack of room-key slots (no numbers), a plain clock with no numerals. In the foreground at the bottom edge, one plain bare hand (no rings, no watch, no nail polish) rests on the counter edge. No readable text anywhere.
```

## 3. room.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera just inside the door of a Taiwanese business hotel room at standing eye height (about 1.6 m), facing straight toward the window at the far end. Left side: a double bed with plain white bedding and a nightstand with a beige room telephone; right side: a small desk with a hair dryer lying on it, a mini fridge under the desk, and a wall-mounted air conditioner high on the wall above the bed with a small blank display. At the far left an open bathroom door shows a shower. No people, no faces, no hands. No readable text; any screens or panels are blank.
```

## 4. phone.jpg

```
Edit the attached image (the confirmed hotel room). Keep the room, furniture, colors, pixel-art style and layout completely identical. Change only the camera: move closer to the nightstand at the left, same standing eye height, looking down slightly at the beige room telephone. Add one plain, ordinary bare hand (no ring, no watch, no bracelet, no nail polish, no sleeve visible) lifting the telephone handset. Keep the phone's buttons as blank shapes with no numbers or letters. No faces, no readable text.
```

## 5. housekeeper.jpg

```
Edit the attached image (the confirmed hotel room). Keep the room, furniture, colors, pixel-art style and layout completely identical. Change only this: the room door at the camera side is now open and a hotel housekeeper stands in the doorway, seen from the neck down (no face visible), wearing a plain uniform and holding a small toolbox; a housekeeping cart with folded towels is partly visible in the corridor behind. Same camera position and height as the original. No readable text.
```

## 6. checkout.jpg

```
Edit the attached image (the confirmed hotel front desk). Keep the desk, background, staff member (no face), colors, pixel-art style and camera angle completely identical. Change only this: the plain bare hand in the foreground now places a blank key card flat on the counter; the staff member's hand points at the monitor. No readable text.
```

## 7. result.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image. Camera at eye level, facing the character from the front, medium shot from the waist up. The character sits on a sofa in a cozy living room at home, looking at her smartphone with a happy, curious expression; she wears a different outfit from the reference (a plain light-green cardigan over a white top). Behind her: a bookshelf, a floor lamp, a window with curtains. The phone screen shows only abstract blank chat bubbles. No readable text anywhere.
```

## 8. end_good.jpg

```
Use the attached reference images ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore their backgrounds completely. Same living-room scene, camera angle and pixel-art style as the confirmed result.jpg. Change only this: she smiles broadly, holds her phone up to the camera with one hand and gives a thumbs-up with the other. Keep everything else identical. No readable text.
```

## 9. end_bad.jpg

```
Edit the attached image (the confirmed end_good.jpg). Keep the living room, camera angle, outfit, pixel-art style and the character's appearance (dark brown skin, long wavy black hair) completely identical. Change only her expression and pose: she looks worried, brows slightly raised, one hand holding the phone down at her chest, the other hand resting on her cheek. No readable text.
```
