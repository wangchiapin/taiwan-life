# 電信行 telecom 的圖片清單與提示詞（給 Gemini 用）

2026-11-07 寫好（第一版草稿，尚未修改）。共 10 張。提示詞是英文（給 Gemini），說明是中文。每個提示詞都是完整的（畫風、視角、限制都寫在裡面），整段複製貼上就能用。
遊戲程式在 `games/telecom/index.html`，圖片放 `games/telecom/images/`，缺圖時自動顯示表情符號（遊戲照樣能玩）。

## 共通規則

- **一次做一張**：做完一張，Ben 確認，再做下一張，照下面順序。
- **畫風**：和飲料店（games/drinks/images）一樣的 16-bit 像素風插畫、暖色調。**不要拿別的遊戲的場景圖當參考圖**（生成器會照抄背景）；只有 Ami 用下面的人物參考圖。
- **Ami 長相要固定**：深棕膚色、波浪長黑髮。先到 `games/drinks/images/call.jpg`，**用它的頭肩裁切**（只留 Ami 的頭和肩膀）當角色參考圖上傳，提示詞已寫「只複製這個人物，忽略背景」。不要只用文字描述 Ami。衣服可以不同。
- **劇情真正發生的地點**：手機聊天是在家附近的街上（主角站在路邊收到 LINE，街角看得到電信行）；其餘關卡都在同一間電信行裡（入口、櫃檯、方案海報牆）；結果／結局圖是 Ami 在自己家門口。
- **主角沒有性別**：第一人稱，臉和身體不入鏡，只看得到普通的手（沒有戒指、手錶、手環、指甲油，袖子不要露出）。店員也不露臉（背影、側後方，或鏡頭把臉裁掉）。
- **沒有可讀的文字**：招牌、海報、價格、螢幕、單據、護照、鈔票面額都畫成空白或抽象線條（遊戲用文字卡片顯示方案、價錢、門號）。
- **同一個遊戲場景要一致**：同一間電信行，用已確認的 `shop.jpg` 當底圖，寫成編輯式（keep everything identical, change only X）。
- **檔案規格**：2048×2048 原圖縮成 **720×720、JPG、品質約 84**，檔名小寫，照下表。

## 台灣實景核對（Ben 看過覺得不對請直接說）

- 台灣的電信行／電信公司門市：櫃檯後面有電腦和單據印表機，牆上有方案海報，側邊有展示手機的架子；辦預付卡時店員會看護照和居留證並掃描／拍照存檔。這是依印象畫的，**待確認**。
- 換 SIM 卡：店員用卡針退出卡槽、換上新卡。圖上只畫小卡片與抽象形狀。
- 手機沒訊號時，狀態列左上角顯示空的訊號格（遊戲內的字「無服務」不畫在圖上）。

## 圖片清單

| 順序 | 檔名 | 用在哪一關 | 底圖 |
|---|---|---|---|
| 1 | `start.jpg` | START（家附近的街上，手機收到 Ami 的 LINE；街角看得到電信行） | 無（文字生圖，第一張先做） |
| 2 | `shop.jpg` | ENTER（走進電信行，店員在櫃檯後） | 無（文字生圖） |
| 3 | `counter.jpg` | DOCS / REPEAT / TOPUP（櫃檯前給證件、聽店員複誦、問儲值） | 上傳已確認的 shop.jpg（編輯式） |
| 4 | `plan.jpg` | PLAN（看牆上的方案海報） | 上傳已確認的 shop.jpg（編輯式） |
| 5 | `pay.jpg` | PAY / PAY_FIX / CHANGE（櫃檯付錢找錢） | 上傳已確認的 counter.jpg（編輯式） |
| 6 | `sim.jpg` | SIM（拿到新卡和單據，核對門號） | 上傳已確認的 counter.jpg（編輯式） |
| 7 | `nosignal.jpg` | NOSIGNAL（手機沒訊號，請店員幫忙） | 上傳已確認的 counter.jpg（編輯式） |
| 8 | `result.jpg` | RESULT（Ami 在家門口收到成果訊息） | 無（文字生圖＋Ami 頭肩參考圖） |
| 9 | `end_good.jpg` | END 好結局（Ami 開心） | 上傳已確認的 result.jpg＋Ami 頭肩參考圖 |
| 10 | `end_bad.jpg` | END 壞結局（Ami 擔心） | 上傳已確認的 end_good.jpg（編輯式） |

---

## 1. start.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), facing along a quiet Taipei residential street, slightly looking down at the phone. A pair of plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the lower part of the frame; the phone screen shows only abstract blank chat-bubble shapes. Far ahead: low apartment buildings with blank signs, scooters parked at the curb, a small phone shop on the corner with an abstract blank sign band and a plain glass door. No faces of any person, no readable text anywhere.
```

## 2. shop.jpg

```
16-bit pixel art illustration, warm muted colors, square 1:1 image, first-person point of view. Camera at standing eye height (about 1.6 m), standing just inside the glass door of a small Taiwan phone/telecom shop, looking straight toward the service counter at the back. Bright clean shop with light floor tiles; a long counter with a computer monitor (blank screen) and a receipt printer; behind it a shop clerk in a plain polo shirt seen from three-quarter back or cropped at the chin, no face visible; on the side walls blank colorful plan posters (abstract shapes only) and a shelf of display phones. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) is visible at the lower right. No faces of any person, no readable text anywhere.
```

## 3. counter.jpg

```
Edit the attached image (the confirmed phone shop). Keep the shop, clerk (no face), colors, 16-bit pixel art style and camera height completely identical. Change only this: the camera now stands in front of the counter, centered at eye height, looking across it; on the counter lie a passport (plain dark cover, no text) and a card-like resident certificate (abstract blank shapes), and the clerk's hand holds a small scanner. One plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) rests at the lower right. No faces of any person, no readable text anywhere.
```

## 4. plan.jpg

```
Edit the attached image (the confirmed phone shop). Keep the shop style, colors and 16-bit pixel art style identical. Change only this: the camera now looks at the wall of plan posters from about two meters away, at eye height; three posters in a row show abstract blank price tags and simple data-bar shapes (no letters, no numbers); one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) points toward the middle poster from the lower right. No faces of any person, no readable text anywhere.
```

## 5. pay.jpg

```
Edit the attached image (the confirmed counter.jpg). Keep the shop, clerk (no face), camera position and 16-bit pixel art style completely identical. Change only this: remove the passport and card; on the counter lie a printed receipt slip (abstract gray lines only) and a small cash tray with a few banknotes (abstract designs, no numbers); one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds out a bill toward the tray at the lower right. No faces of any person, no readable text anywhere.
```

## 6. sim.jpg

```
Edit the attached image (the confirmed counter.jpg). Keep the shop, clerk (no face), camera position and 16-bit pixel art style completely identical. Change only this: on the counter lie a tiny SIM card and its plastic holder card (blank abstract shapes) beside a printed slip (abstract gray lines only, no numbers); one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) picks up the slip at the lower right. No faces of any person, no readable text anywhere.
```

## 7. nosignal.jpg

```
Edit the attached image (the confirmed counter.jpg). Keep the shop, clerk (no face), camera position and 16-bit pixel art style completely identical. Change only this: one plain, ordinary bare hand(s) (no ring, no watch, no bracelet, no nail polish, no sleeve visible) holds a smartphone in the foreground, tilted so we see the top-left status bar showing an empty signal icon (abstract shapes, no letters) and a puzzled-looking blank screen; the clerk reaches out a hand to take the phone. No faces of any person, no readable text anywhere.
```

## 8. result.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. 16-bit pixel art illustration, warm muted colors, square 1:1 image. Camera at eye level, facing the character from the front, medium shot from the waist up. She stands in the doorway of her apartment in Taipei, wearing a plain mustard cardigan over a white top, holding her smartphone in one hand and reading it with a calm, pleased expression. Behind her: a tidy entryway with a shoe cabinet and shoes, warm afternoon light. The phone screen shows only abstract blank chat bubbles. No readable text anywhere.
```

## 9. end_good.jpg

```
Use the attached reference image ONLY for the character: copy only this person (the woman with dark brown skin and long wavy black hair), ignore its background completely. Same doorway scene, camera angle and 16-bit pixel art style as the confirmed result.jpg. Change only this: she smiles warmly and gives a thumbs-up with her free hand while holding the phone with the other. Keep everything else identical. No readable text.
```

## 10. end_bad.jpg

```
Edit the attached image (the confirmed end_good.jpg). Keep the doorway scene, camera angle, outfit, 16-bit pixel art style and the character's appearance (dark brown skin, long wavy black hair) completely identical. Change only her expression and pose: she looks worried, brows slightly raised, the phone held down at her chest, the other hand resting on her cheek. No readable text.
```
